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


class CompanyUrlInfo:
    """
    a company's comeet page (what we want to scrape)
    """
    companies = {}
    positions = {}
    def __init__(self, url):
        self.company_url = url
        self.response = requests.get(self.company_url)
        self.page = None
        if self.response.status_code == requests.codes.ok:
            self.page = BeautifulSoup(self.response.content, "html.parser")
        else:
            raise ConnectionError(f'Unable to reach {self.company_url}')
        self.script_elements = None
        self.current_company = ''
        # todo logging {url} ok, ScrapedUrl made

    def find_script_elements(self):
        """
        finds script elements within the ScrapeUrl and assigns the instance attribute
        """
        self.script_elements = self.page.find_all('script', type='text/javascript')
        # if not self.script_elements:
        #     # todo logging script elements not found
        # else:
        #     # todo logging debug script elements found

    def find_company_element_in_scripts(self):
        """
        finds the element in the ScrapeUrl's scripts which contains the company info and assigns it to the instance
        attribute
        """
        company_element = [re.search('COMPANY_DATA = ({.*})', element.get_text()) for element in self.script_elements if re.search('COMPANY_DATA = ({.*})', element.get_text())]
        if not company_element:
            # todo logging company element not found for {company_data.name}
            pass
        else:
            try:
                company_data = CompanyData(json.loads(company_element[0].group(1)))
                self.current_company = company_data.company_uid
                CompanyUrlInfo.companies[company_data.company_uid] = company_data
                # todo logging company element extracted for {company_data.name}
            except TypeError:
                # todo logging company element could not be read for {company_data.name} because of TypeError
                pass

    def find_position_element_in_scripts(self):
        """
        finds the element in the ScrapeUrl's scripts which contains the company's available positions info and assigns
        it to the instance attribute
        """
        position_element = [re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', element.get_text()) for element in self.script_elements if re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', element.get_text())][0]
        if not position_element:
            # todo logging position element not found for {position_data.name} at {self.current_company}
            pass
        else:
            try:
                positions_data = json.loads(position_element.group(1))
                for position in positions_data:
                    pos = PositionData(position, self.current_company)
                    CompanyUrlInfo.positions[pos.position_uid] = pos
                    # todo logging position element extracted for {pos.pos_name} at {self.current_company}
            except TypeError:
                # todo logging position element could not be read for {position_data.name} at {self.current_company} because of TypeError
                pass


class CompanyData:
    """
    contains info on a company
    """
    def __init__(self, scraped_url_info):
        self.company_uid = scraped_url_info['company_uid']
        self.name = scraped_url_info['name']
        self.location = scraped_url_info['location']
        self.website = scraped_url_info['website']
        self.description = scraped_url_info['description']

    def insert_info_into_company_tables(self, db_engine):
        """
        inserts the company's data into the corresponding table in our database "comeet_jobs"
        """
        with db_engine.connect() as conn:
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


class PositionData:
    """
    contains info on a position
    """
    def __init__(self, scraped_url_info, company_id):
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

    def insert_info_into_position_table(self, db_engine):
        """
        inserts the position's data into the corresponding table in our database "comeet_jobs"
        """
        with db_engine.connect() as conn:
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

    def insert_info_into_position_description_table(self, db_engine):
        """
        inserts the position's descriptions into the corresponding table in our database "comeet_jobs"
        """
        with db_engine.connect() as conn:
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
    """
    takes the urls found in "finding_websites", turns then into a ScrapeUrl and then calls the functions to find the
    script elements for the company and its positions.
    """
    for url in tqdm(finding_websites.extract_company_urls(), colour='green', write_bytes=False):
        print(f'processing: {url}')
        try:
            data_from_url = CompanyUrlInfo(url)
        except ConnectionError as ex:
            print(ex)  # todo add logging
            continue

        data_from_url.find_script_elements()
        data_from_url.find_company_element_in_scripts()
        if not data_from_url.current_company:
            pass
        else:
            data_from_url.find_position_element_in_scripts()


def fill_db_tables():
    for company in CompanyUrlInfo.companies.values():
        company.insert_info_into_company_tables(database.engine)

    for position in CompanyUrlInfo.positions.values():
        position.insert_info_into_position_table(database.engine)
        position.insert_info_into_position_description_table(database.engine)


if __name__ == '__main__':
    scraping()
    fill_db_tables()
