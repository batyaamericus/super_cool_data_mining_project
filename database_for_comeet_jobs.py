import pymysql.cursors

"""
creating a database into which we will put all of the information about the jobs we will scrape
"""


# creating the database "comeet_jobs"
# mysql_connection = pymysql.connect(host='localhost',
#                                    user='root',
#                                    password='abcd',
#                                    cursorclass=pymysql.cursors.DictCursor)
# with mysql_connection as mysql_connection:
#     with mysql_connection.cursor() as mysql_cursor:
#         sql_command = 'CREATE DATABASE comeet_jobs;'
#         mysql_cursor.execute(sql_command)


# connecting to the comeet_jobs database in order to fill it with the relevant tables
mysql_connection = pymysql.connect(host='localhost',
                                   user='root',
                                   password='abcd',
                                   database='comeet_jobs',
                                   cursorclass=pymysql.cursors.DictCursor)
with mysql_connection as mysql_connection:
    with mysql_connection.cursor() as mysql_cursor:
        # company tables
        # companies_table = 'CREATE TABLE companies ( \
        #                                        company_uid VARCHAR(6) PRIMARY KEY, \
        #                                        company_name VARCHAR(256) NOT NULL, \
        #                                        location VARCHAR(256), \
        #                                        website VARCHAR(256) \
        #                                        );'
        # mysql_cursor.execute(companies_table)
        # company_description = 'CREATE TABLE company_description ( \
        #                                        company_uid VARCHAR(6), \
        #                                        description LONGTEXT, \
        #                                        FOREIGN KEY (company_uid) REFERENCES companies(company_uid) \
        #                                        );'
        # mysql_cursor.execute(company_description)
        #
        # # position tables
        # positions_table = 'CREATE TABLE positions ( \
        #                                      position_uid VARCHAR(6) PRIMARY KEY, \
        #                                      position_name VARCHAR(256) NOT NULL, \
        #                                      department VARCHAR(256), \
        #                                      location VARCHAR(256), \
        #                                      employment_type VARCHAR(256), \
        #                                      experience_level VARCHAR(50), \
        #                                      time_updated DATETIME, \
        #                                      company_uid VARCHAR(6), \
        #                                      FOREIGN KEY (company_uid) REFERENCES companies(company_uid) \
        #                                      );'
        # mysql_cursor.execute(positions_table)
        positions_description = 'CREATE TABLE positions_description ( \
                                                 position_uid VARCHAR(6), \
                                                 description LONGTEXT, \
                                                 requirements LONGTEXT, \
                                                 what_will_you_do LONGTEXT, \
                                                 about_us LONGTEXT, \
                                                 you_are LONGTEXT, \
                                                 FOREIGN KEY (position_uid) REFERENCES positions(position_uid) \
                                                 );'
        mysql_cursor.execute(positions_description)
