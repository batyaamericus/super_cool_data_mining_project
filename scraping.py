import csv
import requests
from bs4 import BeautifulSoup
import json
import re
import html
import finding_websites


def printing_info(string):
    decoded_string = html.unescape(string)
    for item in BeautifulSoup(decoded_string, features="html.parser").findAll(text=True):
        print(item)

list_of_urls = []

for link in finding_websites.extracted_urls:
    list_of_urls.append(link.replace('/'.join(link.split('/')[-2:]), ''))

for url in list_of_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('script', type='text/javascript')
    for i in results:
        name_of_element = re.search('COMPANY_DATA = ({.*})', i.get_text())
        if name_of_element:
            company_data = json.loads(name_of_element.group(1))

            pattern = 'COMPANY_POSITIONS_DATA = (\[{.*}\])'
            position_data_raw = re.search(pattern, i.get_text()).group(1)
            positions_data = json.loads(position_data_raw)

            print('Company Info:')
            try:
                print('Company name:', company_data['name'])
                print('Location:', company_data['location'])
                print('Website:', company_data['website'])
                if not company_data['linkedin_integrations_apply_context'] == None:
                    print('Linked in job application')

            except TypeError as ex:
                print(ex)

            print('\nOpen positions:\n')

            for index, position in enumerate(positions_data):
                try:
                    print(index + 1)
                    print('Position:', position['name'])
                    print('Department:', position['department'])
                    print('Location:', position['location']['name'])
                    print('Employment type:', position['employment_type'])
                    print('About:')
                    for y in position['custom_fields']['details']:
                        printing_info(y['value'])
                    print('\n\n')
                except TypeError as ex:
                    print(ex)
