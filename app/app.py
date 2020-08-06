import logging
from os import getenv
from bowling_systems import *

logging.basicConfig(
    filename='logs/{env}.log'.format(env=getenv('APP_ENV')), 
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

class App:

    avalaible_systems = {
        'BRUNSWICK_VECTOR3': vector.VectorThreeOne,
        'BRUNSWICK_VECTOR5': vector.VectorFive,
        'BRUNSWICK_VECTOR_PLUS_28': vector_plus.VectorPlusTwoEight,
        'BRUNSWICK_VECTOR_PLUS_5': vector_plus.VectorPlusFive,
        'BRUNSWICK_SYNC': sync.BrunswickSync
    }

    api_configuration = {
        'api_base_url': getenv('API_URL'),
        'api_token': getenv('API_TOKEN')
    }

    def log(self, t:str, msg: str):
        logger = {
            'DEBUG': logging.debug,
            'INFO': logging.info,
            'WARNING': logging.warning
        }
        if t in logger:
            logger.get(t)(msg)

    def get_current_bowling_system(self):
        return self.get_config_key(self.avalaible_systems, getenv('BOWLING_SYSTEM'))()

    def get_api_setting(self, key: str):
        return self.get_config_key(self.api_configuration, key)

    def get_config_key(self, conf: dict, key: str):
        if key in conf:
            return conf.get(key)
        else:
            return None