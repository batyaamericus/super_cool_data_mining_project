import requests
from bs4 import BeautifulSoup
import json
import re
import finding_websites
from sqlalchemy.orm import Session
import db_details as db
from datetime import datetime


def scraping():
    # finding relevant elements in page
    for url in finding_websites.extract_company_urls():
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

                    # extracting company data
                    try:
                        with Session(db.engine) as session:
                            company = db.Company(
                                company_uid=company_data['company_uid'],
                                name=company_data['name'],
                                location=company_data['location'],
                                website=company_data['website']
                            )

                            company_description = db.CompanyDescription(
                                company_uid=company_data['company_uid'],
                                description=company_data['description']
                            )
                            session.add_all([company, company_description])
                            session.commit()
                    except TypeError as ex:
                        pass

                    # extracting data about positions
                    for index, position in enumerate(positions_data):
                        try:
                            with Session(db.engine) as session:
                                company_position = db.Position(
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
                                session.add(company_position)
                                session.commit()

                                for description in position['custom_fields']['details']:
                                    position_descriptions = db.PositionDescription(
                                        position_uid=position['uid'],
                                        description_title=description['name'],
                                        description=description['value']
                                    )
                                    session.add(position_descriptions)
                                    session.commit()
                        except TypeError as ex:
                            continue
                        except KeyError as ex:
                            continue


if __name__ == '__main__':
    scraping()
