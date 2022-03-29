from sqlalchemy import text
import html2text
import pandas as pd
import database


class DBsearch:
    def __init__(self):
        self.engine = database.engine
        self.conn = self.engine.connect()
        self.conn.begin()

    def get_company_uid_from_name(self, name):
        """
        This function gets the unique company id from the database based on the company name

        :param name: name of company
        :return: uid: company uid
        """
        uid = None

        statement = f"SELECT company_uid FROM companies WHERE LOWER(name) LIKE '%{name}%'"
        ins = text(statement)

        results = self.conn.execute(ins)
        for result in results:
            uid = result[0]

        return uid

    def get_company_name_from_uid(self, uid):
        """
        This function gets the company from the database based on the company uid.

        :param uid: company uid
        :return: name: company name
        """

        statement = f"SELECT name FROM companies WHERE company_uid='{uid}'"
        ins = text(statement)

        results = self.conn.execute(ins)
        for result in results:
            return result[0]

    def get_company_info(self, uid):
        """
        This function gets company info (location and website) from the database given company uid

        :param uid: company uid
        :return: info: dictionary with company info
        """

        statement = f"SELECT location, website FROM companies WHERE company_uid='{uid}'"
        ins = text(statement)

        # making connection
        results = self.conn.execute(ins)
        for result in results:
            info = {'location': '\tCompany location: ' + result[0], 'website': '\tCompany website: ' + result[1]}
            return info

    def get_company_description(self, uid):
        """
            This function gets company description from the database given company uid

        :param uid: company uid
        :return: company description as a string
        """
        statement = f"SELECT description FROM company_description WHERE company_uid='{uid}'"
        ins = text(statement)

        # making connection
        results = self.conn.execute(ins)
        for result in results:
            return html2text.html2text(result[0])

    def get_companies_by_loc(self, locations):
        """
            This functions returns a list of names of all companies based in the locations provided in the input list.

        :param locations: space separated list of locations
        :return: list of company names
        """

        company_names = []
        for location in locations:
            location = location.lower().replace('_', ' ')
            statement = f"SELECT name FROM companies WHERE LOWER(location) LIKE '%{location}%'"
            ins = text(statement)

            # making connection
            results = self.conn.execute(ins)
            for result in results:
                company_names.append(result[0])

        return company_names

    def comp_search_db(self, search_param, display_params, posit_disp_params):
        """
        This function performs the company search and displays the output.
        
           :param search_param: search options that the user has selected
           :param display_params: display parameters that the user has selected
           :param posit_disp_params: display parameters that the user has selected for positions
        """""

        if not search_param['name'] is None:
            company_names = search_param['name']

        else:
            company_names = self.get_companies_by_loc(search_param['location'])

        for company_name in company_names:
            company_name = company_name.lower().replace('_', ' ')
            uid = self.get_company_uid_from_name(company_name)
            if uid is None:
                print(f"Company with name '{company_name.replace('_', ' ')}' does not exist")
                continue
            print('Company name: ' + company_name.replace('_', ' '))
            info = self.get_company_info(uid)

            if display_params['location'] or display_params['all']:
                print(info['location'])
            if display_params['website'] or display_params['all']:
                print(info['website'])
            if display_params['description'] or display_params['all']:
                print(self.get_company_description(uid))
            if display_params['positions'] or display_params['all']:
                name_dic = {'name': None, 'location': None, 'department': None, 'emp_type': None, 'exp_level': None,
                            'company': [company_name]}
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
                comp_uids.append(self.get_company_uid_from_name(comp_name.lower().replace('_', ' ')))

            conditions.append('company_uid=' + " OR company_uid=".join(["'{0}'".format(name) for name in comp_uids]))

        clause += ' AND '.join(["({0})".format(cond) for cond in conditions])

        return clause

    def get_position_description(self, uid):
        """
            This function returns the position description from the database based on position uid.
        :param uid: position uid
        :return: position description
        """

        statement = f"SELECT description FROM position_description WHERE position_uid='{uid}'"
        ins = text(statement)

        results = self.conn.execute(ins)
        for result in results:
            return html2text.html2text(result[0])

    def posit_search_db(self, posit_params, posit_display_params):
        """
            This function preform the search for open positions and displays the output.
           :param posit_params: search parameters selected by the user
           :param posit_display_params: output display parameters selected by the user
           :return:
        """

        where_clause = self.create_posit_where_clause(posit_params)

        statement = "SELECT * FROM positions " + where_clause
        ins = text(statement)
        sql_df = pd.read_sql(ins, self.conn)
        companies = sql_df.groupby('company_uid')

        for name, positions in companies:
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
                    print(self.get_position_description(r['position_uid']))

                print('')

        print('\n')
