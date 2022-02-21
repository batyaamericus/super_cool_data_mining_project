import requests
import json

url = "https://google-search3.p.rapidapi.com/api/v1/search/q=data+scientist+site:www.comeet.com/jobs&num=1000"

headers = {
    'x-user-agent': "desktop",
    'x-proxy-location': "EU",
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': "1cf3e6b18dmsh45dfd10636a972ap138459jsnedbb0fffe534"
    }

response = requests.get(url, headers=headers)

with open(r'C:\Users\Batra\PycharmProjects\ITC_pycharm\course_project\web_response.json', 'w') as file:
    json.dump(response.json(), file)
print(response.text)