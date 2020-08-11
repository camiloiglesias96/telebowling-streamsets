from .bowling_system import BowlingSystem

class VectorPlusTwoEight(BowlingSystem):
    """
        Brunswick Vector Plus 2.8 System
        @author Telebowling
    """

    tables = []

    table_has_casts = {}

    big_datums = []

    id_names = {}

    collections = {}

    mongo_actions = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_28'



class VectorPlusFive(BowlingSystem):
    """
        Brunswick Vector Plus 5 System
        @author Telebowling
    """

    tables = []

    table_has_casts = {}

    big_datums = []

    id_names = {}

    collections = {}

    mongo_actions = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_5'