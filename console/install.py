#!/usr/bin/python3

import colorama
from distutils.util import strtobool
from os import getenv, get_terminal_size
from termcolor import colored, cprint
from app.app import App
from datetime import datetime
from database.migrator import Migrator
from database.mysql import TableChecksum, ServiceSettings
from database.mongodb import MongoDB
from checksum_system.checksums import Checksum

colorama.init()

bowling_system = App().get_current_bowling_system()

system_is_installed = ServiceSettings.get_by_id('system_installed').value
if system_is_installed is not None:
    system_is_installed = strtobool(system_is_installed)

if bowling_system is not None and not system_is_installed:

    App().app_brand()

    cprint('INSTALLING DATA'.center(50), 'white', 'on_yellow')

    """ Get the current bowling system tables """
    base_system_tables = bowling_system.tables

    records = []

    mongoClient = MongoDB().get_client()

    # Create the MongoDB collections for BW System
    for table in base_system_tables:
        record = {
            'table_name': table, 
            'checksum':None,
            'last_update': datetime.today()
        }
        records.append(record)
        collection = bowling_system.get_collection_name_by_table(table)
        if collection not in mongoClient[getenv('BOARD_ID')].list_collection_names():
            mongoClient[getenv('BOARD_ID')].create_collection(collection)

    TableChecksum().truncate_table()
    
    if records is not None:
        TableChecksum().insert_many(records).execute()
        ServiceSettings().truncate_table()
        for param, value in App().base_params.items():
            service_param = {'param':param, 'value': value, 'created_at': datetime.today()}
            ServiceSettings().insert(service_param).execute()
        ServiceSettings.update(value=getenv('BOWLING_SYSTEM'), updated_at=datetime.today()).where(ServiceSettings.param == 'current_system').execute()
        ServiceSettings.update(value=True, updated_at=datetime.today()).where(ServiceSettings.param == 'system_installed').execute()
        cprint('[OK] SUCCESS INSTALLED'.center(50), 'white', 'on_green')
    # Install the initial checksums
    Checksum().update_table_checksums(install=True)
    mongoClient.close()

    # Run the migration process
    Migrator().run()
elif system_is_installed:
    App().app_brand()
    mongoClient = MongoDB().get_client()
    bw_system = ServiceSettings.get_by_id('current_system').value
    msg = """
        The {current_system} system is installed. Do you really want install a system {new_system} ?
    """
    print(msg.format(current_system=bw_system, new_system=getenv('BOWLING_SYSTEM')))
    answer = True if input('Default [yes]: Type "yes" to continue >> ') == 'yes' else False
    if answer:
        for table in App().get_bowling_system(bw_system).tables:
            collection = bowling_system.get_collection_name_by_table(table)
            if collection is not None:
                mongoClient[getenv('BOARD_ID')].drop_collection(str(collection))
                cprint('[INFO] COLLECCTION DROPPED {collection}'.format(collection=collection).center(50), 'white', 'on_yellow')

        if len(mongoClient[getenv('BOARD_ID')].list_collection_names()) == 0:
            TableChecksum().truncate_table()
            ServiceSettings.update(value=False, updated_at=datetime.today()).where(ServiceSettings.param == 'system_installed').execute()
            cprint('[OK] CHANGE SUCCESS'.center(50), 'white', 'on_green')
            App().log('INFO', 'Bowling system has been changed from {current_system} to {new_system}'.format(
                current_system=bw_system,
                new_system=getenv('BOWLING_SYSTEM')
            ))
            print('Execute again the install action')
    else:
        App().log('DEBUG', 'Installation closed by user')
        exit()
    mongoClient.close()
else:
    raise Exception(""" The .env vars isn't configured. Remember fill the .env file for current environment """)