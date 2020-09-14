from .bowling_system import BowlingSystem
from database.mongodb import MongoDB

class VectorThreeOne(BowlingSystem):
    """
        Brunswick Vector 3.1 System
        @author Telebowling
    """

    tables = [
        '[CLASSIC_LANELOG].[dbo].[LANELOG]',
        '[CLASSIC_POS].[dbo].[EMPLOYEE]',
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]',
        '[CLASSIC_POS].[dbo].[PLU_LIST]',
        '[CLASSIC_POS].[dbo].[RECEIPT]',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]',
        '[CLASSIC_BOWLING].[dbo].[SETUP]'
    ]

    big_datums = [
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]'
    ]

    id_names = {
        '[CLASSIC_LANELOG].[dbo].[LANELOG]': 'lanelog_id',
        '[CLASSIC_POS].[dbo].[EMPLOYEE]': 'id',
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]': 'receipt_record_id',
        '[CLASSIC_POS].[dbo].[PLU_LIST]': 'plu_id',
        '[CLASSIC_POS].[dbo].[RECEIPT]': 'receipt_id',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]': 'id',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]': 'reservation_id',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]': 'log_id',
        '[CLASSIC_BOWLING].[dbo].[SETUP]': 'parameter'
    }

    collections = {
        '[CLASSIC_LANELOG].[dbo].[LANELOG]': 'lanelogs',
        '[CLASSIC_POS].[dbo].[EMPLOYEE]': 'employees',
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]': 'receipt_records',
        '[CLASSIC_POS].[dbo].[PLU_LIST]': 'products',
        '[CLASSIC_POS].[dbo].[RECEIPT]': 'receipts',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]': 'waiting_customers',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]': 'reservations',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]': 'errors',
        '[CLASSIC_BOWLING].[dbo].[SETUP]': 'settings'
    }

    table_has_casts = {
        '[CLASSIC_LANELOG].[dbo].[LANELOG]': True,
        '[CLASSIC_POS].[dbo].[EMPLOYEE]': False,
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]': False,
        '[CLASSIC_POS].[dbo].[PLU_LIST]': False,
        '[CLASSIC_POS].[dbo].[RECEIPT]': True,
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]': True,
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]': True,
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]': True,
        '[CLASSIC_BOWLING].[dbo].[SETUP]': False
    }

    mongo_actions = {
        'lanelogs': MongoDB._INSERT,
        'employees': MongoDB._UPSERT,
        'receipt_records': MongoDB._INSERT,
        'products': MongoDB._UPSERT,
        'receipts': MongoDB._INSERT,
        'waiting_customers': MongoDB._INSERT,
        'reservations': MongoDB._INSERT,
        'errors': MongoDB._INSERT,
        'settings': MongoDB._UPSERT
    }

    sync_truncating = {
        '[CLASSIC_BOWLING].[dbo].[SETUP]': 'BrokenLane'
    }

    def get_broken_lines_from_mssql(self, table_name: str, field: str, exp: str):
        query = """
            SELECT {field} FROM {table} WHERE {field} LIKE '%{exp}%' 
        """.format(
            field=field,
            table=table_name,
            exp=exp
        )
        return self.mssql.raw_query(query, as_dict=True)

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR3'



class VectorFive(BowlingSystem):
    """
        Brunswick Vector 5 System
        @author Telebowling
    """

    tables = []

    table_has_casts = {}

    big_datums = []

    id_names = {}

    collections = {}

    mongo_actions = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR5'