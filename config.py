import os
import logging

'''PLEASE ENTER YOUR INFORMATION FOR THE VARIABLES BELOW:'''
USER_NAME = os.environ['username']
PASSWORD = os.environ['password']
HOST = os.environ['host']

'''DB'''
ENGINE_URL = f'mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}/comeet_jobs'

'''LOGGING'''

db_setup_logger = logging.getLogger('db_setup')
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
db_output_file_handler = logging.FileHandler('db_setup.log')
db_setup_logger.addHandler(db_output_file_handler)
db_setup_logger.setLevel(logging.INFO)

# basicConfig code example
# logging.basicConfig(filename='db_setup.log',
#                     format='%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
#                     level=logging.INFO)
#
MENU_LOGGER = logging.getLogger('menu')
output_file_handler = logging.FileHandler('user_interface.log')
output_file_handler.setFormatter(formatter)
MENU_LOGGER.addHandler(output_file_handler)
MENU_LOGGER.setLevel(logging.INFO)
