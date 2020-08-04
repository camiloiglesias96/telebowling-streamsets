from os import getenv
from pymongo import MongoClient

class MongoDB:

    client = None

    def __init__(self):
        self.connect_to_mongo()

    def connect_to_mongo(self):
        self.client = MongoClient('{base_url}'.format(
            base_url=getenv('MONGODB_URL')
        ))