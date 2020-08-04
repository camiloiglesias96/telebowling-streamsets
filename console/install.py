#!/usr/bin/python3

import colorama
from os import getenv, get_terminal_size
from termcolor import colored, cprint
from pyfiglet import Figlet
from app.app import App
from datetime import datetime
from database.mysql import TableChecksum
from database.mongodb import MongoDB
from checksum_system.checksums import Checksum

colorama.init()

bowling_system = App().get_current_bowling_system()

figlet = Figlet(font='slant')

if bowling_system is not None:

    print(figlet.renderText('TELEBOWLING'))

    cprint('INSTALLING DATA'.center(50), 'white', 'on_yellow')

    """ Get the current bowling system tables """
    base_system_tables = bowling_system.tables

    records = []

    mongoClient = MongoDB().client

    for table in base_system_tables:
        record = {
            'table_name': table, 
            'checksum':None,
            'last_update': datetime.today()
        }
        records.append(record)
        collection = bowling_system.get_collection_name_by_table(table)
        if not any(table for collection in mongoClient[getenv('BOARD_ID')].list_collection_names()):
            mongoClient[getenv('BOARD_ID')].create_collection(collection)

    TableChecksum().truncate_table()
    
    if records is not None:
        TableChecksum().insert_many(records).execute()
        cprint('SUCCESS INSTALLED'.center(50), 'white', 'on_green')

    Checksum().update_table_checksums()

else:
    raise Exception(""" The .env vars isn't configured. Remember fill the .env file """)