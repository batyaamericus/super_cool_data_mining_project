import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from tqdm.auto import tqdm
from sqlalchemy.dialects.mysql import insert
import database
import db_details as db
import finding_websites


class ScrapeUrl:
    def __init__(self, url):
        self.company_url = url
        self.response = requests.get(self.company_url)
        self.page = None
        if self.response.status_code == requests.codes.ok:
            self.page = BeautifulSoup(self.response.content, "html.parser")
        else:
            raise ConnectionError(f'Unable to reach {self.company_url}')
        self.script_elements = None
        self.company_data = {}
        self.position_data = []

    def find_script_elements(self):
        self.script_elements = self.page.find_all('script', type='text/javascript')
        return self.script_elements

    def find_company_element_in_scripts(self):
        company_element = [re.search('COMPANY_DATA = ({.*})', element.get_text()) for element in self.script_elements if re.search('COMPANY_DATA = ({.*})', element.get_text())][0]
        if company_element:
            self.company_data = json.loads(company_element.group(1))

    def find_position_element_in_scripts(self):
        position_element = [re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', element.get_text()) for element in self.script_elements if re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', element.get_text())][0]
        if position_element:
            self.position_data = json.loads(position_element.group(1))


class CompanyDataExtractor:
    def __init__(self, scraped_url_info, database_engine):
        self.db_engine = database_engine
        self.company_uid = scraped_url_info['company_uid']
        self.name = scraped_url_info['name']
        self.location = scraped_url_info['location']
        self.website = scraped_url_info['website']
        self.description = scraped_url_info['description']

    def insert_info_into_company_tables(self):
        with self.db_engine.connect() as conn:
            insert_company = insert(db.Company).values(
                company_uid=self.company_uid,
                name=self.name,
                location=self.location,
                website=self.website
            )
            on_duplicate_company = insert_company.on_duplicate_key_update(
                name=insert_company.inserted.name, location=insert_company.inserted.location,
                website=insert_company.inserted.website)

            insert_company_description = insert(db.CompanyDescription).values(
                company_uid=self.company_uid,
                description=self.description
            )
            on_duplicate_description = insert_company_description.on_duplicate_key_update(
                description=self.description)

            conn.execute(on_duplicate_company)
            conn.execute(on_duplicate_description)
            conn.commit()


class PositionDataExtractor:
    def __init__(self, scraped_url_info, database_engine, company_id):
        self.db_engine = database_engine
        self.position_uid = scraped_url_info['uid']
        self.pos_name = scraped_url_info['name']
        self.department = scraped_url_info['department']
        self.is_remote = scraped_url_info['location']['is_remote']
        self.location = ', '.join([k + ': ' + v for k, v in scraped_url_info['location'].items() if v and k != 'arrival_instructions' and k != 'location_uid'])
        self.employment_type = scraped_url_info['employment_type']
        self.experience_level = scraped_url_info['experience_level']
        self.time_updated = datetime.strptime(scraped_url_info['time_updated'], '%Y-%m-%dT%H:%M:%SZ')
        self.company_uid = company_id
        self.comeet_pos_url = scraped_url_info['url_comeet_hosted_page']
        self.company_pos_url = scraped_url_info['url_active_page']
        self.descriptions = scraped_url_info['custom_fields']['details']

    def insert_info_into_position_table(self):
        with self.db_engine.connect() as conn:
            insert_position = insert(db.Position).values(
                position_uid=self.position_uid,
                pos_name=self.pos_name,
                department=self.department,
                is_remote=self.is_remote,
                location=self.location,
                employment_type=self.employment_type,
                experience_level=self.experience_level,
                time_updated=self.time_updated,
                company_uid=self.company_uid,
                comeet_pos_url=self.comeet_pos_url,
                company_pos_url=self.company_pos_url
            )
            on_duplicate_position = insert_position.on_duplicate_key_update(
                pos_name=self.pos_name,
                department=self.department,
                is_remote=self.is_remote,
                location=self.location,
                employment_type=self.employment_type,
                experience_level=self.experience_level,
                time_updated=self.time_updated,
                comeet_pos_url=self.comeet_pos_url,
                company_pos_url=self.company_pos_url
            )

            conn.execute(on_duplicate_position)
            conn.commit()

    def insert_info_into_position_description_table(self):
        with self.db_engine.connect() as conn:
            for description in self.descriptions:
                insert_position_descriptions = insert(db.PositionDescription).values(
                    position_uid=self.position_uid,
                    description_title=description['name'],
                    description=description['value']
                )
                on_duplicate_position_description = insert_position_descriptions.on_duplicate_key_update(
                    description_title=insert_position_descriptions.inserted.description_title,
                    description=insert_position_descriptions.inserted.description)

                conn.execute(on_duplicate_position_description)
                conn.commit()


def scraping():
    # finding relevant elements in page
    for url in tqdm(finding_websites.extract_company_urls(), colour='green'):
        print(f'processing: {url}')
        try:
            data_from_url = ScrapeUrl(url)
        except ConnectionError as ex:
            print(ex)
            continue
        data_from_url.find_script_elements()
        data_from_url.find_company_element_in_scripts()
        data_from_url.find_position_element_in_scripts()

        try:
            company_info = CompanyDataExtractor(data_from_url.company_data, database.engine)
        except TypeError:
            continue

        company_info.insert_info_into_company_tables()

        for position in data_from_url.position_data:
            try:
                position_info = PositionDataExtractor(position, database.engine, company_info.company_uid)
            except TypeError:
                continue
            position_info.insert_info_into_position_table()
            position_info.insert_info_into_position_description_table()


if __name__ == '__main__':
    scraping()
