from .bowling_system import BowlingSystem
from database.mongodb import MongoDB

class BrunswickSync(BowlingSystem):
    """
        Brunswick Vector Sync System
        @author Telebowling

        Attributes:
            __BROKEN_LANE   Define the lane status for broken lanes (default: 1)
    """

    __BROKEN_LANE = 1

    tables = [
        '[Sync].[dbo].[SECUsers]',
        '[Sync].[dbo].[POSProducts]',
        '[Sync].[dbo].[RSVReservations]',
        '[Sync].[dbo].[RSVReservationTypes]',
        '[Sync].[dbo].[MAGSessionGames]',
        '[Sync].[dbo].[TRNCashPayments]',
        '[Sync].[dbo].[TRNProducts]',
        '[Sync].[dbo].[POSProductGroups]',
        '[Sync].[dbo].[POSGroups]',
        '[Sync].[dbo].[MAGLaneResources]',
        '[Sync].[dbo].[APPLogPeripheralErrors]',
        '[Sync].[dbo].[APPGuestLists]'
    ]

    big_datums = [
        '[Sync].[dbo].[APPLogPeripheralErrors]'
    ]

    table_has_casts = {
        '[Sync].[dbo].[SECUsers]': False,
        '[Sync].[dbo].[POSProducts]': True,
        '[Sync].[dbo].[POSProductGroups]': False,
        '[Sync].[dbo].[POSGroups]': False,
        '[Sync].[dbo].[RSVReservations]': False,
        '[Sync].[dbo].[RSVReservationTypes]': True,
        '[Sync].[dbo].[MAGSessionGames]': False,
        '[Sync].[dbo].[TRNCashPayments]': True,
        '[Sync].[dbo].[TRNProducts]': True,
        '[Sync].[dbo].[MAGLaneResources]': False,
        '[Sync].[dbo].[APPGuestLists]': True,
        '[Sync].[dbo].[APPLogPeripheralErrors]': False
    }

    id_names = {
        '[Sync].[dbo].[SECUsers]': 'ID',
        '[Sync].[dbo].[POSProducts]': 'ID',
        '[Sync].[dbo].[POSProductGroups]': 'ID',
        '[Sync].[dbo].[POSGroups]': 'ID',
        '[Sync].[dbo].[RSVReservations]': 'ID',
        '[Sync].[dbo].[RSVReservationTypes]': 'ID',
        '[Sync].[dbo].[MAGSessionGames]': 'ID',
        '[Sync].[dbo].[TRNCashPayments]': 'ID',
        '[Sync].[dbo].[TRNProducts]': 'ID',
        '[Sync].[dbo].[MAGLaneResources]': 'Name',
        '[Sync].[dbo].[APPGuestLists]': 'ID',
        '[Sync].[dbo].[APPLogPeripheralErrors]': 'ID'
    }

    collections = {
        '[Sync].[dbo].[SECUsers]': 'employees',
        '[Sync].[dbo].[POSProducts]': 'products',
        '[Sync].[dbo].[POSProductGroups]': 'product_group',
        '[Sync].[dbo].[POSGroups]':'groups',
        '[Sync].[dbo].[RSVReservations]': 'reservations',
        '[Sync].[dbo].[RSVReservationTypes]': 'reservation_types',
        '[Sync].[dbo].[MAGSessionGames]': 'lanelogs',
        '[Sync].[dbo].[TRNCashPayments]': 'receipts',
        '[Sync].[dbo].[TRNProducts]': 'receipt_records',
        '[Sync].[dbo].[MAGLaneResources]': 'settings',
        '[Sync].[dbo].[APPGuestLists]': 'waiting_customers',
        '[Sync].[dbo].[APPLogPeripheralErrors]': 'errors'
    }

    mongo_actions = {
        'employees': MongoDB._UPSERT,
        'products': MongoDB._UPSERT,
        'product_group': MongoDB._UPSERT,
        'groups': MongoDB._UPSERT,
        'reservations': MongoDB._INSERT,
        'reservation_types': MongoDB._UPSERT,
        'lanelogs': MongoDB._INSERT,
        'receipts': MongoDB._INSERT,
        'receipt_records': MongoDB._INSERT,
        'settings': MongoDB._UPSERT,
        'waiting_customers': MongoDB._INSERT,
        'errors': MongoDB._INSERT,
    }

    sync_truncating = {
        '[Sync].[dbo].[MAGLaneResources]': 'IsBroken'
    }

    def get_broken_lines_from_mssql(self, table_name: str, field: str, exp: str):
        query = """
            SELECT {field}, {exp} FROM {table} WHERE {exp} = {broken_flag} 
        """.format(
            field=field,
            table=table_name,
            exp=exp,
            broken_flag=self.__BROKEN_LANE
        )
        return self.mssql.raw_query(query, as_dict=True)

    def get_bowling_system_name(self):
        return 'BRUNSWICK_SYNC'