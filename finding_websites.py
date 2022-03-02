import requests
import json
import csv


GOOGLE_API_URL = "https://google-search3.p.rapidapi.com/api/v1/search/q=data+scientist+site:www.comeet.com/jobs&num=100"
GOOGLE_API_HEADERS = {
    'x-user-agent': "desktop",
    'x-proxy-location': "EU",
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': "1cf3e6b18dmsh45dfd10636a972ap138459jsnedbb0fffe534"
    }

google_response = requests.get(GOOGLE_API_URL, headers=GOOGLE_API_HEADERS)
reading_google_response = json.loads(google_response.text)
extracted_urls = [job['link'] for job in reading_google_response['results']]
