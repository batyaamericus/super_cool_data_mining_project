import os
import logging

'''PLEASE ENTER YOUR INFORMATION FOR THE VARIABLES BELOW:'''
USER_NAME = os.environ['username']
PASSWORD = os.environ['password']
HOST = os.environ['host']

'''DB'''
ENGINE_URL = f'mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}/comeet_jobs'

'''LOGGING'''
MENU_LOGGER = logging.getLogger('menu')

# configuring logger for movies.log
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
movies_file_handler = logging.FileHandler('user_interface.log')
movies_file_handler.setFormatter(formatter)
MENU_LOGGER.addHandler(movies_file_handler)
MENU_LOGGER.setLevel(logging.DEBUG)
