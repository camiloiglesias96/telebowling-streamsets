import logging
from os import getenv
from bowling_systems import *
from pyfiglet import Figlet

logging.basicConfig(
    filename='logs/{env}.log'.format(env=getenv('APP_ENV')), 
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

class App:

    # Define all the avalaible systems
    avalaible_systems = {
        'BRUNSWICK_VECTOR3': vector.VectorThreeOne,
        'BRUNSWICK_VECTOR5': vector.VectorFive,
        'BRUNSWICK_VECTOR_PLUS_28': vector_plus.VectorPlusTwoEight,
        'BRUNSWICK_VECTOR_PLUS_5': vector_plus.VectorPlusFive,
        'BRUNSWICK_SYNC': sync.BrunswickSync
    }

    # Define the api settings
    api_configuration = {
        'api_base_url': getenv('API_URL'),
        'api_token': getenv('API_TOKEN'),
        'api_board': getenv('API_BOARD')
    }

    # Base system params
    base_params = {
        'current_system': None,
        'system_installed': None
    }

    def log(self, t:str, msg: str):
        """ Log message on environment log """
        logger = {
            'DEBUG': logging.debug,
            'INFO': logging.info,
            'WARNING': logging.warning
        }
        if t in logger:
            logger.get(t)(msg)

    def get_current_bowling_system(self):
        """ Get the current bowling system instance """
        return self.get_config_key(self.avalaible_systems, getenv('BOWLING_SYSTEM'))()

    def get_bowling_system(self, bw_system: str):
        """ Get specific bowling system instance """
        system = self.get_config_key(self.avalaible_systems, bw_system)
        if system is not None:
            return system()
        else:
            return None

    def app_brand(self):
        """ Print the branding telebowling script system """
        figlet = Figlet(font='slant')
        print(figlet.renderText('TELEBOWLING'))

    def get_api_setting(self, key: str):
        """ Get specific api setting """
        return self.get_config_key(self.api_configuration, key)

    def get_config_key(self, conf: dict, key: str):
        """ Get specific key based on config dict """
        if key in conf:
            return conf.get(key)
        else:
            return None