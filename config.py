import os
import logging

'''PLEASE ENTER YOUR INFORMATION FOR THE VARIABLES BELOW:'''
USER_NAME = os.environ['username']
PASSWORD = os.environ['password']
HOST = os.environ['host']

'''DB'''
ENGINE_URL = f'mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}/comeet_jobs'

'''LOGGING'''
# db_setup_logger = logging.getLogger('db_setup')
# configuring logger for db_setup.log

# formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
# movies_file_handler = logging.FileHandler('db_setup.log')

# basicConfig code example
logging.basicConfig(filename='db_setup.log',
                    format='%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)
