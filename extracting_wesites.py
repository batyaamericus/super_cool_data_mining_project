import json
import csv

with open(r'C:\Users\Batra\PycharmProjects\ITC_pycharm\course_project\web_response.json', 'r') as raw_file:
    content = json.load(raw_file)


with open(r'C:\Users\Batra\PycharmProjects\ITC_pycharm\course_project\urls.csv', 'w', newline='\n') as url_file:
    writer = csv.DictWriter(url_file, content['results'][0].keys())
    writer.writeheader()
    for row in content['results']:
        try:
            writer.writerow(row)
        except UnicodeEncodeError as e:
            print(e)
