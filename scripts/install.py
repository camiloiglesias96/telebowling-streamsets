#!/usr/bin/python3

from os import getenv
from termcolor import colored, cprint
from pyfiglet import Figlet
from app.app import App
from datetime import datetime
from database.mysql import TableChecksum
from checksum_system.checksums import Checksum

bowling_system = App().get_current_bowling_system()

figlet = Figlet(font='slant')

if bowling_system is not None:

    print(figlet.renderText('TELEBOWLING'))

    cprint('INSTALLING DATA . . .', 'white', 'on_yellow')

    base_system_tables = bowling_system.tables

    records = []

    for table in base_system_tables:
        record = {
            'table_name': table, 
            'checksum':None,
            'last_update': datetime.today()
        }
        records.append(record)

    TableChecksum().truncate_table()
    
    if records is not None:
        TableChecksum().insert_many(records).execute()
        cprint('SUCCESS INSTALLED', 'white', 'on_green')

    Checksum().update_table_checksums()
else:
    raise Exception(""" The .env vars isn't configured. Remember fill the .env file """)