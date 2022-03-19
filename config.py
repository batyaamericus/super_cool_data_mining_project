import os

'''PLEASE ENTER YOUR INFORMATION FOR THE VARIABLES BELOW:'''
USER_NAME = os.environ['username']
PASSWORD = os.environ['password']
HOST = os.environ['host']

'''DB'''
ENGINE_URL = f'mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOST}/comeet_jobs'
