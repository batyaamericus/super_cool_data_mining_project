import logging
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
from config  import db_setup_logger


class CompanyUrlInfo:
    """
    a company's comeet page (what we want to scrape)
    """
    companies = {}
    positions = {}

    def __init__(self, url):
        db_setup_logger.debug(f'trying to make CompanyUrlInfo from {url}')
        self.company_url = url
        self.response = requests.get(self.company_url)
        self.page = None
        if self.response.status_code == requests.codes.ok:
            self.page = BeautifulSoup(self.response.content, "html.parser")
        else:
            db_setup_logger.critical(f'unable to connect to {self.company_url}')
            raise ConnectionError(f'Unable to reach {self.company_url}')
        self.script_elements = None
        self.current_company = ''
        db_setup_logger.info(f'{url} ok, CompanyUrlInfo created successfully')

    def find_script_elements(self):
        """
        finds script elements within the ScrapeUrl and assigns the instance attribute
        """
        self.script_elements = self.page.find_all('script', type='text/javascript')
        if not self.script_elements:
            db_setup_logger.warning(f'no script elements were found for {self.company_url}')
        else:
            db_setup_logger.info(f'script elements extracted for {self.company_url}')

    def find_company_element_in_scripts(self):
        """
        finds the element in the ScrapeUrl's scripts which contains the company info and assigns it to the instance
        attribute
        """
        company_element = [re.search('COMPANY_DATA = ({.*})', element.get_text()) for element in self.script_elements
                           if re.search('COMPANY_DATA = ({.*})', element.get_text())]
        if not company_element:
            db_setup_logger.warning(f'no company element was found in page')
            pass
        else:
            try:
                company_data = CompanyData(json.loads(company_element[0].group(1)))
                self.current_company = company_data.company_uid
                CompanyUrlInfo.companies[company_data.company_uid] = company_data
                db_setup_logger.info(f'company element extracted and CompanyUrlInfo made for {company_data.name}')
            except TypeError:
                db_setup_logger.warning(f'company element could not be read for {self.company_url} because of TypeError')
                pass

    def find_position_element_in_scripts(self):
        """
        finds the element in the ScrapeUrl's scripts which contains the company's available positions info and assigns
        it to the instance attribute
        """
        position_element = [re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', element.get_text()) for element in
                            self.script_elements if re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])',
                                                              element.get_text())]
        if not position_element:
            db_setup_logger.warning(f'no position elements were found for {self.current_company}')
            pass
        else:
            positions_data = json.loads(position_element[0].group(1))
            num_pos = len(positions_data)
            for i, position in enumerate(positions_data):
                try:
                    pos = PositionData(position, self.current_company)
                    CompanyUrlInfo.positions[pos.position_uid] = pos
                    db_setup_logger.info(f'position element extracted and PositionData made for {pos.pos_name} at '
                                 f'{self.current_company}')
                except TypeError:
                    db_setup_logger.warning(f'position element could not be read for position {i+1}/{num_pos} at '
                                    f'{self.current_company} because of TypeError')
                    continue


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

            db_setup_logger.debug(f'sql statement prepared for company: {self.company_uid}')

            insert_company_description = insert(db.CompanyDescription).values(
                company_uid=self.company_uid,
                description=self.description
            )
            on_duplicate_description = insert_company_description.on_duplicate_key_update(
                description=self.description)

            db_setup_logger.debug(f'sql statement prepared for description for company: {self.company_uid}')

            conn.execute(on_duplicate_company)
            db_setup_logger.debug(f'sql statement for company executed')
            conn.execute(on_duplicate_description)
            db_setup_logger.debug(f'sql statement for description for company executed')
            conn.commit()
            db_setup_logger.debug(f'sql statement for company and its description has been committed')


class PositionData:
    """
    contains info on a position
    """
    def __init__(self, scraped_url_info, company_id):
        self.position_uid = scraped_url_info['uid']
        self.pos_name = scraped_url_info['name']
        self.department = scraped_url_info['department']
        self.is_remote = scraped_url_info['location']['is_remote']
        self.location = ', '.join([k + ': ' + v for k, v in scraped_url_info['location'].items() if v and k !=
                                   'arrival_instructions' and k != 'location_uid'])
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
            db_setup_logger.debug(f'sql statement prepared for position: {self.position_uid}')

            conn.execute(on_duplicate_position)
            db_setup_logger.debug(f'sql statement for position executed')
            conn.commit()
            db_setup_logger.debug(f'sql statement for position has been committed')

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
                db_setup_logger.debug(f'sql statement prepared for description for position: {self.position_uid}')

                conn.execute(on_duplicate_position_description)
                db_setup_logger.debug(f'sql statement for description for position executed')
                conn.commit()
                db_setup_logger.debug(f'sql statement for description for position has been committed')


def scraping():
    """
    takes the urls found in "finding_websites", turns then into a ScrapeUrl and then calls the functions to find the
    script elements for the company and its positions.
    """
    db_setup_logger.debug('SCRAPER RUNNING')
    for i, url in enumerate(tqdm(finding_websites.extract_company_urls(), colour='green', write_bytes=False)):
        print(f'processing: {url}')
        try:
            data_from_url = CompanyUrlInfo(url)
        except ConnectionError as ex:
            print(ex)
            continue

        data_from_url.find_script_elements()
        data_from_url.find_company_element_in_scripts()
        if not data_from_url.current_company:
            pass
        else:
            data_from_url.find_position_element_in_scripts()

    db_setup_logger.info(f'{len(CompanyUrlInfo.companies)}/{i} companies extracted from potential company links')


def fill_db_tables():
    logging.debug('FILLING DB TABLES')
    for company in CompanyUrlInfo.companies.values():
        company.insert_info_into_company_tables(database.engine)

    for position in CompanyUrlInfo.positions.values():
        position.insert_info_into_position_table(database.engine)
        position.insert_info_into_position_description_table(database.engine)

    db_setup_logger.info(f'completed successfully, database filled')
