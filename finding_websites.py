import requests
import json
from config import db_setup_logger


GOOGLE_API_URL = "https://google-search3.p.rapidapi.com/api/v1/search/q=data+scientist+site:www.comeet.com/jobs&num=100"
GOOGLE_API_HEADERS = {
    'x-user-agent': "desktop",
    'x-proxy-location': "EU",
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': "1cf3e6b18dmsh45dfd10636a972ap138459jsnedbb0fffe534"
    }


def search_for_position_urls():
    """
    finding comeet job position urls using a google API
    :return extracted_urls:
    """
    db_setup_logger.debug(f'sending initial Google api request')
    google_response = requests.get(GOOGLE_API_URL, headers=GOOGLE_API_HEADERS)
    if google_response.status_code == requests.codes.ok:
        db_setup_logger.info(f'initial Google api request received (status code 200)')
        reading_google_response = json.loads(google_response.text)
        extracted_urls = [job['link'] for job in reading_google_response['results']]
        return extracted_urls
    else:
        db_setup_logger.critical(f'unable to connect to google api, status code: {google_response.status_code}')
        raise ConnectionError('Initial url extraction unsuccessful, unable to connect to Google api.')


def extract_company_urls():
    set_of_company_urls = set()
    db_setup_logger.debug(f'manually turning job pages into company pages')
    for link in search_for_position_urls():
        company_link = link.replace('/'.join(link.split('/')[-2:]), '')
        if company_link != 'https://www.comeet.com/jobs/':
            set_of_company_urls.add(company_link)
        else:
            set_of_company_urls.add(link)
    db_setup_logger.info(f'{len(set_of_company_urls)} company pages found')
    return set_of_company_urls
