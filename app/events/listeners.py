#!/usr/bin/python3

import uuid
from os import getenv
from pubsub import pub
from app.app import App
from datetime import datetime
from app.events import dispatchers
from app.api.api import ApiConnector 
from database.mssql import SqlServer
from database.mongodb import MongoDB
from database.mysql import TableChecksum, FailedRequest
from checksum_system.checksums import Checksum

# ---------- LISTENERS ---------- #
class Listeners:

    client = MongoDB().get_client()

    def onChecksumMismatch(self, msg: set):
        """ Event dispatched on checksums mismatch in the SQL Server DB """
        for table in msg:
            table_data = None
            truncate = False
            last_id = TableChecksum.get_by_id(table).last_inserted_id
            bowling_sys = App().get_current_bowling_system()
            id_key = bowling_sys.get_table_field_name(table)
            collection = bowling_sys.get_collection_name_by_table(table)
            if table in bowling_sys.sync_truncating:
                table_data = bowling_sys.get_broken_lines_from_mssql(
                    table, id_key, bowling_sys.sync_truncating[table]
                )
                if len(table_data) <= 0:
                    self.client[getenv('BOARD_ID')][collection].delete_many({})
                    current_checksum = Checksum().get_base_checksum_from_table(table)
                    update = TableChecksum.update(last_inserted_id=None, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
                    update.execute()
                    pass
                truncate = True
            else:                
                table_data = bowling_sys.get_data_from_system_table(table, last_id)
                truncate = False
            if table_data is not None:
                if bowling_sys.table_needs_cast(table):
                    table_data = [MongoDB().cast_data_type(d) for d in table_data]
                for datum in table_data:
                    action = bowling_sys.get_mongo_action(collection)
                    if action is MongoDB._UPSERT and truncate is False:
                        App().log('DEBUG', {'datum': datum})
                        App().log('DEBUG', {'collection': collection, 'id_key': id_key, 'action': 'UPSERT'})
                        mongo_insert = self.client[getenv('BOARD_ID')][collection].update(
                            {id_key: datum[id_key]}, 
                            datum, 
                            upsert=True)
                        if mongo_insert:
                            current_checksum = Checksum().get_base_checksum_from_table(table)
                            update = TableChecksum.update(last_inserted_id=None, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
                            update.execute()
                    elif action is MongoDB._INSERT and truncate is False:
                        App().log('DEBUG', {'datum': datum})
                        App().log('DEBUG', {'collection': collection, 'id_key': id_key, 'action': 'INSERT'})
                        mongo_insert = self.client[getenv('BOARD_ID')][collection].insert_one(datum)
                        if mongo_insert:
                            current_checksum = Checksum().get_base_checksum_from_table(table)
                            identificator = table_data[-1][id_key] if id_key is not None else None
                            update = TableChecksum.update(last_inserted_id=identificator, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
                            update.execute()
                    elif action is MongoDB._UPSERT and truncate is True:
                        App().log('DEBUG', {'datum': datum})
                        App().log('DEBUG', {'collection': collection, 'id_key': id_key, 'action': 'UPSERT'})
                        self.client[getenv('BOARD_ID')][collection].delete_many({})
                        mongo_insert = self.client[getenv('BOARD_ID')][collection].insert_one(datum)
                        if mongo_insert:
                            current_checksum = Checksum().get_base_checksum_from_table(table)
                            update = TableChecksum.update(last_inserted_id=None, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
                            truncate = False
                            update.execute()
        # dispatchers.doBoardPushedData(msg)
        self.client.close()

    def onDataPushed(self, msg: set):
        """ Event dispatched after checksum mismatch data successfully loaded in Data Lake """
        api = ApiConnector()
        url = "{base}/api/board/{board}/push".format(
            base=App().get_api_setting('api_base_url'), 
            board=App().get_api_setting('api_board')
        )
        result = api.get(url)
        if result is None:
            failed_request = {
                'id': uuid.uuid4(),
                'url': url,
                'data': result,
                'persisted': result is not None,
                'created_at': datetime.today(),
                'updated_at': datetime.today()
            }
            FailedRequest().insert(failed_request).execute()

# ---------- TOPICS SUSCRIPTIONS ---------- #
listeners = Listeners()
pub.subscribe(listeners.onChecksumMismatch, 'checksum_mismatch')
pub.subscribe(listeners.onDataPushed, 'board_pushed_data')
