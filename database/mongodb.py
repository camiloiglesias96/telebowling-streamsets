from os import getenv
from decimal import Decimal
from pymongo import MongoClient
from bson.decimal128 import Decimal128

class MongoDB:
    """
        MongoDB Base Connector
        @author Telebowling
    """

    # Constant to perform UPSERT action
    _UPSERT = 1

    # Constant to perform INSERT action
    _INSERT = 2

    client = None

    def __init__(self):
        self.connect_to_mongo()

    def connect_to_mongo(self):
        """ Perfom the MongoDB connection """
        self.client = MongoClient('{base_url}'.format(
            base_url=getenv('MONGODB_URL')
        ), maxPoolSize=100, socketTimeoutMS=10000, connectTimeoutMS=10000)

    def cast_data_type(self, dict_item):
        """ Cast builtin Python classes to MongoDB BSON classes """
        if dict_item is None: return None

        for k, v in list(dict_item.items()):
            if isinstance(v, dict):
                self.cast_data_type(v)
            elif isinstance(v, list):
                for l in v:
                    self.cast_data_type(l)
            elif isinstance(v, Decimal):
                dict_item[k] = Decimal128(str(v))
        return dict_item
        
    def get_client(self):
        """ Get MongoDB from client for this base connector """
        if self.client is not None:
            return self.client
        else:
            raise ConnectionError('Connection error to MongoDB')