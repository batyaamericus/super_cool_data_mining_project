from sqlalchemy import create_engine

'''USER DEFINED:'''
# user_name = 'your_username'
# password = 'your_password'
# host = 'your_host'

user_name = 'root'
password = 'abcd'
host = 'localhost'


'''OTHER'''
engine = create_engine(f'mysql+pymysql://{user_name}:{password}@{host}/comeet_jobs',
                           future=True)
google_api_url = "https://google-search3.p.rapidapi.com/api/v1/search/q=data+scientist+site:www.comeet.com/jobs&num=100"
google_api_headers = {
    'x-user-agent': "desktop",
    'x-proxy-location': "EU",
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': "1cf3e6b18dmsh45dfd10636a972ap138459jsnedbb0fffe534"
    }