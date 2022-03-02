import csv
import requests
from bs4 import BeautifulSoup
import json
import re

list_of_urls=[]
with open('urls.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        list_of_urls.append(row['link'].replace('/'.join(row['link'].split('/')[-2:]),''))

i=0
for url in list_of_urls:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('script', type='text/javascript')
    lol=0
    for i in results:
        name_of_element = re.search('COMPANY_DATA = ({.*})', i.get_text())
        if name_of_element:
            company_data= json.loads(name_of_element.group(1))

            pattern = 'COMPANY_POSITIONS_DATA = (\[{.*}\])'
            position_data_raw = re.search(pattern, i.get_text()).group(1)
            positions_data = json.loads(position_data_raw)

            for index, position in enumerate(positions_data):
                try:
                    print(index+1)
                    print('Position:', position['name'])
                    print('Department:', position['department'])
                    print('Location:', position['location']['name'])
                    print('Employment type:', position['employment_type'])
                    print('About:')
                    for y in position['custom_fields']['details']:
                        print('\t', y['value'])
                    print('\n\n')
                except TypeError as ex:
                    print(ex)