import requests
import json
import csv
import config


def search_for_position_urls():
    """
    finding comeet job position urls using a google API
    :return extracted_urls:
    """
    google_response = requests.get(config.google_api_url, headers=config.google_api_headers)
    if google_response.status_code == requests.codes.ok:
        reading_google_response = json.loads(google_response.text)
        extracted_urls = [job['link'] for job in reading_google_response['results']]
        return extracted_urls
    else:
        raise ConnectionError('Url extraction unsuccessful, unable to connect to Google.')


def extract_company_urls():
    set_of_company_urls = set()
    for link in finding_websites.search_for_position_urls():
        set_of_company_urls.add(link.replace('/'.join(link.split('/')[-2:]), ''))
    return set_of_company_urls
