#!/usr/bin/python3

import time
import colorama
from os import getenv
from app.app import App
from progress.bar import Bar
from database.mongodb import MongoDB
from termcolor import colored, cprint
from database.mysql import TableChecksum
from checksum_system.checksums import Checksum

colorama.init()

class Migrator:
    """
        Migrator Tool
        @author Telebowling
    """
    app = App()

    client = MongoDB().get_client()

    _UNIQUE_RESULT = 1
    _RANGE_FETCH = 50

    def run(self):
        """ Run the main migrator action """
        bw_system = self.app.get_current_bowling_system()
        with Bar('Migrating . . .', max=len(bw_system.tables)) as bar:
            for table in bw_system.tables:
                collection = bw_system.get_collection_name_by_table(table)
                bar.message = 'Migrating {col}'.format(col=collection)
                if table in bw_system.big_datums:
                    self.persist_big_datum(table, collection)
                else:
                    self.persist_small_datum(table, collection)
                App().log('DEBUG', 'Collection {col} migrated'.format(col=collection))
                bar.next() 
        Checksum().update_table_checksums(install=False)
        cprint('########## SYSTEM MIGRATED ##########'.center(50), 'white', 'on_green')
        self.client.close()

    def persist_big_datum(self, table: str, collection: str):
        """ Migrate big datums chunking the data """
        bw_system = self.app.get_current_bowling_system()
        field = bw_system.get_table_field_name(table)
        last_inserted = bw_system.get_first_id_from_mssql(table, field)
        last_id = bw_system.get_last_id_from_mssql(table, field)
        range_fetch = self._RANGE_FETCH if last_inserted == self._UNIQUE_RESULT else last_inserted + self._RANGE_FETCH
        if last_id:
            while last_id > last_inserted:
                datum = bw_system.get_data_from_mssql_by_range_id(table, field, last_inserted, range_fetch)
                if bw_system.table_needs_cast(table):
                    datum = [MongoDB().cast_data_type(d) for d in datum]
                insert = self.client[getenv('BOARD_ID')][collection].insert_many(datum)
                if insert.inserted_ids:
                    last_inserted = last_inserted + range_fetch
                    range_fetch = range_fetch + last_inserted
                time.sleep(20)
            TableChecksum.update(last_inserted_id=last_id).where(TableChecksum.table_name == table).execute()

    def persist_small_datum(self, table: str, collection: str):
        """ Migrate small datum """
        bw_system = self.app.get_current_bowling_system()
        datum = bw_system.get_data_from_system_table(table)
        if bw_system.table_needs_cast(table):
            datum = [MongoDB().cast_data_type(d) for d in datum]
        if len(datum) > 0:
            self.client[getenv('BOARD_ID')][collection].insert_many(datum)