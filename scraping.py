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


# importing job position urls from finding_websites.py and splitting them to get the company's main url
list_of_urls = []
for link in finding_websites.extracted_urls:
    list_of_urls.append(link.replace('/'.join(link.split('/')[-2:]), ''))

# finding relevant elements in page
for url in list_of_urls:
    page = requests.get(url)
    if page.status_code == requests.codes.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all('script', type='text/javascript')

        for i in results:
            # extracting element with company data
            company_data_element = re.search('COMPANY_DATA = ({.*})', i.get_text())
            # extracting element with position data
            positions_data_element = re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', i.get_text())

            if company_data_element:
                company_data = json.loads(company_data_element.group(1))
                positions_data = json.loads(positions_data_element.group(1))

                print('Company Info:')
                # extracting company data
                try:
                    print('Company name:', company_data['name'])
                    print('Location:', company_data['location'])
                    print('Website:', company_data['website'])
                    if not company_data['linkedin_integrations_apply_context']:
                        print('Apply via LinkedIn')
                except TypeError as ex:
                    pass

                print('\nOpen positions:\n')
                # extracting data about positions
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
                        pass
