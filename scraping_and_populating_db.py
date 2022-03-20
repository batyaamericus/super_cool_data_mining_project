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


def scraping():
    # finding relevant elements in page
    for url in tqdm(finding_websites.extract_company_urls()):
        print(f'processing: {url}')
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find_all('script', type='text/javascript')

            for i in results:
                # extracting element with company data
                company_data_element = re.search('COMPANY_DATA = ({.*})', i.get_text())

                if company_data_element:
                    company_data = json.loads(company_data_element.group(1))

                    # extracting company data
                    try:
                        with database.engine.connect() as conn:
                            insert_company = insert(db.Company).values(
                                company_uid=company_data['company_uid'],
                                name=company_data['name'],
                                location=company_data['location'],
                                website=company_data['website']
                            )
                            on_duplicate_company = insert_company.on_duplicate_key_update(
                                name=insert_company.inserted.name, location=insert_company.inserted.location, website=insert_company.inserted.website)

                            insert_company_description = insert(db.CompanyDescription).values(
                                company_uid=company_data['company_uid'],
                                description=company_data['description']
                            )
                            on_duplicate_description = insert_company_description.on_duplicate_key_update(
                                description=insert_company_description.inserted.description)

                            conn.execute(on_duplicate_company)
                            conn.execute(on_duplicate_description)
                            conn.commit()

                    except TypeError:
                        pass

                    # extracting element with position data
                    positions_data_element = re.search('COMPANY_POSITIONS_DATA = (\[{.*}\])', i.get_text())
                    positions_data = json.loads(positions_data_element.group(1))

                    # extracting data about positions
                    for index, position in enumerate(positions_data):
                        try:
                            with database.engine.connect() as conn:
                                insert_position = insert(db.Position).values(
                                    position_uid=position['uid'],
                                    pos_name=position['name'],
                                    department=position['department'],
                                    # is_remote=position['is_remote'],
                                    location=position['location']['name'],
                                    employment_type=position['employment_type'],
                                    experience_level=position['experience_level'],
                                    time_updated=datetime.strptime(position['time_updated'], '%Y-%m-%dT%H:%M:%SZ'),
                                    company_uid=company_data['company_uid']
                                )
                                on_duplicate_position = insert_position.on_duplicate_key_update(
                                    pos_name=insert_position.inserted.pos_name,
                                    department=insert_position.inserted.department,
                                    location=insert_position.inserted.location,
                                    employment_type=insert_position.inserted.employment_type,
                                    experience_level=insert_position.inserted.experience_level,
                                    time_updated=insert_position.inserted.time_updated)

                                conn.execute(on_duplicate_position)
                                conn.commit()

                                for description in position['custom_fields']['details']:
                                    insert_position_descriptions = insert(db.PositionDescription).values(
                                        position_uid=position['uid'],
                                        description_title=description['name'],
                                        description=description['value']
                                    )
                                    on_duplicate_position_description = insert_position_descriptions.on_duplicate_key_update(
                                        description_title=insert_position_descriptions.inserted.description_title, description=insert_position_descriptions.inserted.description)

                                    conn.execute(on_duplicate_position_description)
                                    conn.commit()

                        except TypeError:
                            continue
                        except KeyError:
                            continue


if __name__ == '__main__':
    scraping()
