from .bowling_system import BowlingSystem
from database.mongodb import MongoDB

class VectorPlusTwoEight(BowlingSystem):
    """
        Brunswick Vector Plus 2.8 System
        @author Telebowling
    """

    tables = [
        '[VectorPlus].[dbo].[SECUsers]',
        '[VectorPlus].[dbo].[Products]',
        '[VectorPlus].[dbo].[ReservationMain]',
        '[VectorPlus].[dbo].[ReservationParty]',
        '[VectorPlus].[dbo].[Sessions]',
        '[VectorPlus].[dbo].[RegisterGroups]',
        '[VectorPlus].[dbo].[ApplicationLog]',
        '[VectorPlus].[dbo].[PartyList]',
        '[VectorPlus].[dbo].[BowlerList]',
        '[VectorPlus].[dbo].[Transactions]',
        '[VectorPlus].[dbo].[LineItems]'
    ]

    big_datums = [
        '[VectorPlus].[dbo].[ApplicationLog]'
    ]

    table_has_casts = {
        '[VectorPlus].[dbo].[SECUsers]': False,
        '[VectorPlus].[dbo].[Products]': True,
        '[VectorPlus].[dbo].[ReservationMain]': False,
        '[VectorPlus].[dbo].[ReservationParty]': False,
        '[VectorPlus].[dbo].[Sessions]': False,
        '[VectorPlus].[dbo].[RegisterGroups]': False,
        '[VectorPlus].[dbo].[ApplicationLog]': False,
        '[VectorPlus].[dbo].[PartyList]': False,
        '[VectorPlus].[dbo].[BowlerList]': False,
        '[VectorPlus].[dbo].[Transactions]': True,
        '[VectorPlus].[dbo].[LineItems]': True
    }

    id_names = {
        '[VectorPlus].[dbo].[SECUsers]': 'ID',
        '[VectorPlus].[dbo].[Products]': 'ID',
        '[VectorPlus].[dbo].[ReservationMain]': 'ReservationID',
        '[VectorPlus].[dbo].[ReservationParty]': 'PartyID',
        '[VectorPlus].[dbo].[Sessions]': 'ID',
        '[VectorPlus].[dbo].[RegisterGroups]': 'ID',
        '[VectorPlus].[dbo].[ApplicationLog]': 'AppLogID',
        '[VectorPlus].[dbo].[PartyList]': 'ID',
        '[VectorPlus].[dbo].[BowlerList]': 'ID',
        '[VectorPlus].[dbo].[Transactions]': 'ID',
        '[VectorPlus].[dbo].[LineItems]': 'ID'
    }

    collections = {
        '[VectorPlus].[dbo].[SECUsers]': 'employees',
        '[VectorPlus].[dbo].[Products]': 'products',
        '[VectorPlus].[dbo].[ReservationMain]': 'reservations',
        '[VectorPlus].[dbo].[ReservationParty]': 'reservation_details',
        '[VectorPlus].[dbo].[Sessions]': 'lanelogs',
        '[VectorPlus].[dbo].[RegisterGroups]': 'product_groups',
        '[VectorPlus].[dbo].[ApplicationLog]': 'errors',
        '[VectorPlus].[dbo].[PartyList]': 'waiting_customers',
        '[VectorPlus].[dbo].[BowlerList]': 'waiting_customer_details',
        '[VectorPlus].[dbo].[Transactions]': 'receipts',
        '[VectorPlus].[dbo].[LineItems]': 'receipt_records'
    }

    mongo_actions = {
        '[VectorPlus].[dbo].[SECUsers]': MongoDB._UPSERT,
        '[VectorPlus].[dbo].[Products]': MongoDB._UPSERT,
        '[VectorPlus].[dbo].[ReservationMain]': MongoDB._INSERT,
        '[VectorPlus].[dbo].[ReservationParty]': MongoDB._UPSERT,
        '[VectorPlus].[dbo].[Sessions]': MongoDB._INSERT,
        '[VectorPlus].[dbo].[RegisterGroups]': MongoDB._UPSERT,
        '[VectorPlus].[dbo].[ApplicationLog]': MongoDB._INSERT,
        '[VectorPlus].[dbo].[PartyList]': MongoDB._INSERT,
        '[VectorPlus].[dbo].[BowlerList]': MongoDB._UPSERT,
        '[VectorPlus].[dbo].[Transactions]': MongoDB._INSERT,
        '[VectorPlus].[dbo].[LineItems]': MongoDB._INSERT
    }

    sync_truncating = {}

    def get_broken_lines_from_mssql(self, table_name: str, field: str, exp: str):
        query = """
            SELECT {field} FROM {table}' 
        """.format(
            field=field,
            table=table_name,
            exp=exp
        )
        return self.mssql.raw_query(query, as_dict=True)

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_28'



class VectorPlusFive(VectorPlusTwoEight):
    """
        Brunswick Vector Plus 5 System
        @author Telebowling
    """

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_5'