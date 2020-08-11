from .bowling_system import BowlingSystem

class BrunswickSync(BowlingSystem):
    """
        Brunswick Vector Sync System
        @author Telebowling
    """

    tables = []

    table_has_casts = {}

    big_datums = []

    id_names = {}

    collections = {}

    mongo_actions = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_SYNC'