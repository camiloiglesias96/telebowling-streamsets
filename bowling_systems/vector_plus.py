from .bowling_system import BowlingSystem

class VectorPlusTwoEight(BowlingSystem):
    """ Brunswick Vector Plus 2.8 """
    
    tables = []

    collections = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_28'



class VectorPlusFive(BowlingSystem):
    """ Brunswick Vector Plus 5 """
    
    tables = []

    collections = {}

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR_PLUS_5'