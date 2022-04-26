import requests
import json
import config


def search_for_position_urls():
    """
    finding comeet job position urls using a google API
    :return extracted_urls:
    """
    config.db_setup_logger.debug(f'sending initial Google api request')
    google_response = requests.get(config.google_api_url, headers=config.google_api_headers)
    if google_response.status_code == requests.codes.ok:
        config.db_setup_logger.info(f'initial Google api request received (status code 200)')
        reading_google_response = json.loads(google_response.text)
        extracted_urls = [job['link'] for job in reading_google_response['results']]
        return extracted_urls
    else:
        config.db_setup_logger.critical(f'unable to connect to google api, status code: {google_response.status_code}')
        raise ConnectionError('Initial url extraction unsuccessful, unable to connect to Google api.')


def extract_company_urls():
    """
    calls the search_for_position_urls function and edits the position urls to find the company urls
    :return:
    """
    config.db_setup_logger.debug(f'manually turning job pages into company pages')
    set_of_company_urls = set()
    company_comeet_link = 'https://www.comeet.com/jobs/'
    for link in search_for_position_urls():
        company_link = link.replace('/'.join(link.split('/')[-2:]), '')
        if company_link != company_comeet_link:
            set_of_company_urls.add(company_link)
        else:
            set_of_company_urls.add(link)
    config.db_setup_logger.info(f'{len(set_of_company_urls)} company pages found')
    return set_of_company_urls
