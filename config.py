import os
import logging

'''PLEASE ENTER YOUR INFORMATION FOR THE VARIABLES BELOW:'''
user_name = os.environ['username']
password = os.environ['password']
host = os.environ['host']

'''DB'''
engine_url = f'mysql+pymysql://{user_name}:{password}@{host}/comeet_jobs'

'''LOGGING'''
formatter = logging.Formatter('%(asctime)s-%(levelname)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
db_setup_logger = logging.getLogger('db_setup')
db_output_file_handler = logging.FileHandler('db_setup.log')
db_output_file_handler.setFormatter(formatter)
db_setup_logger.addHandler(db_output_file_handler)
db_setup_logger.setLevel(logging.INFO)

menu_logger = logging.getLogger('menu')
output_file_handler = logging.FileHandler('user_interface.log')
output_file_handler.setFormatter(formatter)
menu_logger.addHandler(output_file_handler)
menu_logger.setLevel(logging.DEBUG)


'''API DETAILS'''
# Google API
job_type_query = 'data+scientist'
google_api_url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={job_type_query}+site:www.comeet.com/jobs&num=100"
google_api_headers = {
    'x-user-agent': "desktop",
    'x-proxy-location': "EU",
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': "1cf3e6b18dmsh45dfd10636a972ap138459jsnedbb0fffe534"
    }