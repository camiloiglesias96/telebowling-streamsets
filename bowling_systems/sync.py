from .bowling_system import BowlingSystem

class BrunswickSync(BowlingSystem):
    """ Brunswick Sync System Statistics """

    tables = []

    id_names = {}

    collections = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_SYNC'