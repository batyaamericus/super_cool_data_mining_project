import requests
from db_search_functions import DBsearch
from sqlalchemy import text
from config import db_setup_logger


def get_all_companies():
    db = DBsearch()
    conn = db.conn

    statement = text("SELECT name FROM companies")

    company_names = []
    results = conn.execute(statement)

    for result in results:
        company_names.append(result[0])

    return company_names


def api_enrichment():

    company_names=get_all_companies()

    API_KEY = "2ebf58a45a2e8784aa697aa6bfcd6a580e664d42c473c88745f656a27145f975"

    PDL_URL = "https://api.peopledatalabs.com/v5/company/search"

    H = {
      'Content-Type': "application/json",
      'X-api-key': API_KEY
    }

    sql_query = "SELECT * FROM company WHERE name="+" OR name=".join(["'{0}'".format(name) for name in company_names])

    P = {
      'sql': sql_query,
      'size': 10,
      'pretty': True
    }
    db_setup_logger.debug(f'sending initial PDL api request')
    response = requests.get(
      PDL_URL,
      headers=H,
      params=P
    ).json()
    db_setup_logger.info(f'initial PDL api request received status code: {response["status"]}')
    return response


def add_info_to_db(response):
    db = DBsearch()
    conn = db.conn

    relevant_tags = ['employee_count', 'founded', 'headline', 'industry', 'profiles', 'type']

    data = response['data']  # list of dictionaries
    if response["status"] == 200:
        for i in range(len(data)):

            statement = text(f"SELECT name FROM companies WHERE name='{data[i]['name']}'")
            results = conn.execute(statement)
            if not results:
                continue
            uid = db.get_company_uid_from_name(data[i]['name'])

            statement = text(f"INSERT INTO extra_company_info (company_uid) VALUES ('{uid}')")
            conn.execute(statement)
            for tag in relevant_tags:
                if tag == 'profiles':
                    if not data[i][tag] is None:
                        statement = text(f"UPDATE extra_company_info SET {tag}='{'; '.join(data[i][tag])}' WHERE company_uid='{uid}'")
                        conn.execute(statement)
                        conn.commit()
                elif tag == 'employee_count' or tag == 'founded':
                    if not data[i][tag] is None:
                        statement = text(f"UPDATE extra_company_info SET {tag}={data[i][tag]} WHERE company_uid='{uid}'")
                        conn.execute(statement)
                        conn.commit()
                else:
                    if not data[i][tag] is None:
                        statement = text(f"UPDATE extra_company_info SET {tag}='{data[i][tag]}' WHERE company_uid='{uid}'")
                        conn.execute(statement)
                        conn.commit()

        db_setup_logger.info(f'successfully enriched table with information from PDL api')
    else:
        print("NOTE. The carrier pigeons lost motivation in flight. See error and try again.")
        print("error:", response)
        db_setup_logger.critical(f'Enrichment failed due to an error that has occurred when trying to make an API call')
