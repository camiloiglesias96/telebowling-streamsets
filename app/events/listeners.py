#!/usr/bin/python3

from os import getenv
from pubsub import pub
from app.app import App
from datetime import datetime
from database.mssql import SqlServer
from database.mongodb import MongoDB
from database.mysql import TableChecksum
from checksum_system.checksums import Checksum

# ---------- LISTENERS ---------- #
class Listeners:

    def onChecksumMismatch(self, msg: set):
        """ Event dispatched on checksums mismatch in the SQL Server DB """
        mongoClient = MongoDB().get_client()
        for table in msg:
            last_id = TableChecksum.get_by_id(table).last_inserted_id
            bowling_sys = App().get_current_bowling_system()
            id_key = bowling_sys.get_table_field_name(table)
            collection = bowling_sys.get_collection_name_by_table(table)
            table_data = bowling_sys.get_data_from_system_table(table, last_id)
            if table_data is not None:
                if bowling_sys.table_needs_cast(table):
                    table_data = [MongoDB().cast_data_type(d) for d in table_data]
                for datum in table_data:
                    action = bowling_sys.get_mongo_action(collection)
                    if action is MongoDB._UPSERT:
                        App().log('DEBUG', {'collection': collection, 'id_key': id_key})
                        mongo_insert = mongoClient[getenv('BOARD_ID')][collection].update(
                            {id_key: datum[id_key]}, 
                            datum, 
                            upsert=True)
                        if mongo_insert:
                            current_checksum = Checksum().get_base_checksum_from_table(table)
                            update = TableChecksum.update(last_inserted_id=None, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
                            update.execute()
                    elif action is MongoDB._INSERT:
                        mongo_insert = mongoClient[getenv('BOARD_ID')][collection].insert_one(datum)
                        if mongo_insert:
                            current_checksum = Checksum().get_base_checksum_from_table(table)
                            identificator = table_data[-1][id_key] if id_key is not None else None
                            update = TableChecksum.update(last_inserted_id=identificator, checksum=current_checksum[0][0], last_update=datetime.today()).where(TableChecksum.table_name == table)
            update.execute()
        mongoClient.close()

listeners = Listeners()

# ---------- TOPICS SUSCRIPTIONS ---------- #
pub.subscribe(listeners.onChecksumMismatch, 'checksum_mismatch')
