from .bowling_system import BowlingSystem

class VectorThreeOne(BowlingSystem):

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

    id_names = {
        '[CLASSIC_LANELOG].[dbo].[LANELOG]': 'lanelog_id',
        '[CLASSIC_POS].[dbo].[EMPLOYEE]': 'id',
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]': 'receipt_record_id',
        '[CLASSIC_POS].[dbo].[PLU_LIST]': 'plu_id',
        '[CLASSIC_POS].[dbo].[RECEIPT]': 'receipt_id',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]': 'id',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]': 'reservation_id',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]': 'log_id'
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

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR3'



class VectorFive(BowlingSystem):
    """ Brunswick Vector 5 """

    tables = []

    collections = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR5'