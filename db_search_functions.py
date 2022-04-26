from sqlalchemy import text
import html2text
import pandas as pd
import database
import config as CONF
from sqlalchemy.exc import DBAPIError, SQLAlchemyError


class DBsearch:
    def __init__(self):
        self.engine = database.engine
        self.conn = self.engine.connect()
        self.conn.begin()
        CONF.menu_logger.debug(f"DBsearch class instantiated. Connection to the database successfully opened. ")
        
    def get_company_uid_from_name(self, name):
        """
        This function gets the unique company id from the database based on the company name


        :param name: name of company
        :return: uid: company uid
        """
        uid = None
        
        statement = f"SELECT company_uid FROM companies WHERE LOWER(name) LIKE '%{name}%'"
        ins = text(statement)

        try:
            results = self.conn.execute(ins)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")


        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")
        for result in results:
            uid = result[0]

        CONF.menu_logger.debug(f"Returning (uid=): {uid}")
        return uid

    def get_company_name_from_uid(self, uid):
        """
        This function gets the company from the database based on the company uid.

        :param uid: company uid
        :return: name: company name
        """

        statement = f"SELECT name FROM companies WHERE company_uid='{uid}'"
        ins = text(statement)

        try:
            results = self.conn.execute(ins)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")

        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")
        for result in results:
            CONF.menu_logger.debug(f"Returning (name=): {result[0]}")
            return result[0]

    def get_company_info(self, uid):
        """
        This function gets company info (location and website) from the database given company uid

        :param uid: company uid
        :return: info: dictionary with company info
        """

        statement = f"SELECT location, website FROM companies WHERE company_uid='{uid}'"
        ins = text(statement)

        try:
            results = self.conn.execute(ins)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")

        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")
        
        for result in results:
            info = {'location': '\tCompany location: ' + result[0], 'website': '\tCompany website: ' + result[1]}
            CONF.menu_logger.debug(f"Returning (info=): {info} ")
            return info

    def get_company_description(self, uid):
        """
            This function gets company description from the database given company uid

        :param uid: company uid
        :return: company description as a string
        """
        statement = f"SELECT description FROM company_description WHERE company_uid='{uid}'"
        ins = text(statement)

        try:
            results = self.conn.execute(ins)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")

        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")

        for result in results:
            CONF.menu_logger.debug(f"Returning (description)")
            if result[0] is None:
                return ''
            return html2text.html2text(result[0])

    def get_companies_by_loc(self, locations):
        """
            This functions returns a list of names of all companies based in the locations provided in the input list.

        :param locations: space separated list of locations
        :return: list of company names
        """

        company_names = []
        for location in locations:
            CONF.menu_logger.debug(f"Searching for companies located in {location}")
            location = location.lower().replace('_', ' ')
            statement = f"SELECT name FROM companies WHERE LOWER(location) LIKE '%{location}%'"
            ins = text(statement)


            try:
                results = self.conn.execute(ins)
            except SQLAlchemyError as e:
                print(e)
                CONF.menu_logger.critical(f"{e}")
                raise SQLAlchemyError(f"{e._message()}")
            except DBAPIError as e2:
                print(e2)
                CONF.menu_logger.critical(f"{e2}")
                raise DBAPIError(f"{e2.message()}")

            CONF.menu_logger.debug(f"Successful execution of an SQL query to the database.")
            for result in results:
                company_names.append(result[0])

        CONF.menu_logger.debug(f"Returning (company names=): {company_names}")
        return company_names

    def get_dpl_profile(self, uid):

        statement=text(f"SELECT employee_count, founded, headline, industry, profiles, type FROM extra_company_info WHERE company_uid='{uid}'")

        try:
            results = self.conn.execute(statement)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")

        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database.")
        result_dic={}
        for result in results:
            result_dic={'employee_count' : result[0],\
                       'founded': result[1], 'headline': result[2],\
                        'industry': result[3], 'profiles': result[4],\
                        'type': result[5]}

        CONF.menu_logger.debug(f"Returning (companies dpl profiles=): {result_dic}")
        return result_dic



    def comp_search_db(self, search_param, display_params, posit_disp_params):
        """
        This function performs the company search and displays the output.
        
           :param search_param: search options that the user has selected
           :param display_params: display parameters that the user has selected
           :param posit_disp_params: display parameters that the user has selected for positions
        """""
        CONF.menu_logger.info(f"Entering company search function comp_search_db.")
        if not search_param['name'] is None:
            company_names = search_param['name']

        else:
            company_names = self.get_companies_by_loc(search_param['location'])

        for company_name in company_names:
            CONF.menu_logger.debug(f"Beginning to collect info from the database for company: {company_name}")
            company_name = company_name.lower().replace('_', ' ')
            uid = self.get_company_uid_from_name(company_name)
            if uid is None:
                print(f"Company with name '{company_name.replace('_', ' ')}' does not exist")
                continue
            print('Company name: ' + company_name.replace('_', ' '))
            CONF.menu_logger.debug(f"Calling  {self.get_company_info} with argument {uid}")
            info = self.get_company_info(uid)

            if display_params['pdl'] or display_params['all']:
                CONF.menu_logger.debug(f"Calling  {self.get_dpl_profile} with argument {uid}")
                resume=self.get_dpl_profile(uid)
                for key, val in resume.items():
                    print(key,':',val)

            if display_params['location'] or display_params['all']:
                print(info['location'])
            if display_params['website'] or display_params['all']:
                print(info['website'])
            if display_params['description'] or display_params['all']:
                CONF.menu_logger.debug(f"Calling  {self.get_company_description} with argument {uid}")
                print(self.get_company_description(uid))
            if display_params['positions'] or display_params['all']:
                name_dic = {'name': None, 'location': None, 'department': None, 'emp_type': None, 'exp_level': None,
                            'company': [company_name]}
                CONF.menu_logger.debug(f"Calling  {self.posit_search_db} with arguments name_dic= {name_dic} and posit_disp_params={posit_disp_params}")
                self.posit_search_db(name_dic, posit_disp_params)

    def create_posit_where_clause(self, posit_params):
        """
            This is a helper function that creates a single WHERE clause for the SQL query, comprised of all the
            search parameters specified by the user
        :param posit_params: parameters for open positions search
        :return: WHERE clause as a string
        """

        clause = 'WHERE '
        conditions = []
        if posit_params['name'] is not None:
            conditions.append('LOWER(pos_name) LIKE' + " OR LOWER(pos_name) LIKE ".join(
                ["'%{0}%'".format(name.lower().replace('_', ' ')) for name in posit_params['name']]))

        if posit_params['location'] is not None:
            conditions.append('LOWER(location) LIKE ' + " OR LOWER(location) LIKE ".join(
                ["'%{0}%'".format(loc.lower().replace('_', ' ')) for loc in posit_params['location']]))

        if posit_params['department'] is not None:
            conditions.append('LOWER(department) LIKE ' + " OR LOWER(department) LIKE ".join(
                ["'%{0}%'".format(dep.lower().replace('_', ' ')) for dep in posit_params['department']]))

        if posit_params['emp_type'] is not None:
            conditions.append('LOWER(employment_type) LIKE ' + " OR LOWER(employment_type) LIKE ".join(
                ["'%{0}%'".format(param.lower().replace('_', ' ')) for param in posit_params['emp_type']]))

        if posit_params['exp_level'] is not None:
            conditions.append('LOWER(experience_level) LIKE ' + " OR LOWER(experience_level) LIKE ".join(
                ["'%{0}%'".format(level.lower().replace('_', ' ')) for level in posit_params['exp_level']]))

        comp_uids = []
        if posit_params['company'] is not None:
            for comp_name in posit_params['company']:
                CONF.menu_logger.debug(f"Calling {self.get_company_uid_from_name} for company: {comp_name}")
                comp_uids.append(self.get_company_uid_from_name(comp_name.lower().replace('_', ' ')))

            conditions.append('company_uid=' + " OR company_uid=".join(["'{0}'".format(name) for name in comp_uids]))

        clause += ' AND '.join(["({0})".format(cond) for cond in conditions])

        CONF.menu_logger.debug(f"Returning {clause}")
        return clause

    def get_position_description(self, uid):
        """
            This function returns the position description from the database based on position uid.
        :param uid: position uid
        :return: position description
        """

        statement = f"SELECT description FROM position_description WHERE position_uid='{uid}'"
        ins = text(statement)

        try:
            results = self.conn.execute(ins)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")

        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")
        for result in results:
            CONF.menu_logger.debug(f"Returning")
            if result[0] is None:
                return ''
            return html2text.html2text(result[0])

    def posit_search_db(self, posit_params, posit_display_params):
        """
            This function preform the search for open positions and displays the output.
           :param posit_params: search parameters selected by the user
           :param posit_display_params: output display parameters selected by the user
           :return:
        """
        CONF.menu_logger.info(f"Entering positions search function comp_search_db.")
        CONF.menu_logger.debug(f"Calling {self.create_posit_where_clause} with argument {posit_params}")
        where_clause = self.create_posit_where_clause(posit_params)

        statement = "SELECT * FROM positions " + where_clause
        ins = text(statement)
        try:
            sql_df = pd.read_sql(ins, self.conn)
        except SQLAlchemyError as e:
            print(e)
            CONF.menu_logger.critical(f"{e}")
            raise SQLAlchemyError(f"{e._message()}")
        except DBAPIError as e2:
            print(e2)
            CONF.menu_logger.critical(f"{e2}")
            raise DBAPIError(f"{e2.message()}")
        CONF.menu_logger.debug(f"Successful execution of an SQL query to the database")
        companies = sql_df.groupby('company_uid')

        for name, positions in companies:
            CONF.menu_logger.debug(f"Calling {self.get_company_name_from_uid} with argument {name}")
            print('Company name: ', self.get_company_name_from_uid(name))

            for i, r in positions.iterrows():
                print('\tTitle:', r['pos_name'])
                if posit_display_params['department'] or posit_display_params['all']:
                    print('\tDepartment:', r['department'])
                if posit_display_params['location'] or posit_display_params['all']:
                    print('\tLocation:', r['location'])
                if posit_display_params['employment type'] or posit_display_params['all']:
                    print('\tEmployment type:', r['employment_type'])
                if posit_display_params['experience level'] or posit_display_params['all']:
                    print('\tExperience level:', r['experience_level'])
                if posit_display_params['description'] or posit_display_params['all']:
                    print('\tDescription:')
                    CONF.menu_logger.debug(f"Calling {self.get_position_description} with argument {r['position_uid']}")
                    print(self.get_position_description(r['position_uid']))

                print('')

        print('\n')
