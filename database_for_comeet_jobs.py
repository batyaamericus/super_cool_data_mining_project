import pymysql.cursors
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

"""
creating a database into which we will put all of the information about the jobs we will scrape
"""

Base = declarative_base()
engine = create_engine('mysql+pymysql://<user>:<password>@<host>/comeet_jobs', echo=True, future=True)

# creating the database "comeet_jobs"
mysql_connection = pymysql.connect(host='<host>',
                                   user='<user>',
                                   password='<password>',
                                   cursorclass=pymysql.cursors.DictCursor)
with mysql_connection as mysql_connection:
    with mysql_connection.cursor() as mysql_cursor:
        sql_command = 'CREATE DATABASE comeet_jobs;'
        mysql_cursor.execute(sql_command)


# connecting to the comeet_jobs database in order to fill it with the relevant tables
# company tables
class Company(Base):
    __tablename__ = 'companies'

    company_uid = Column(String(6), primary_key=True)
    name = Column(String(256))
    location = Column(String(256))
    website = Column(String(256))

    def __repr__(self):
        return f'Company(id={self.company_uid!r}, name={self.name!r}, location={self.location!r}, website={self.website!r})'


class CompanyDescription(Base):
    __tablename__ = 'company_description'

    id = Column(Integer, primary_key=True)
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return f'CompanyDescription(company_id={self.company_uid!r}, description={self.description!r})'


class Position(Base):
    __tablename__ = 'positions'

    position_uid = Column(String(6), primary_key=True)
    pos_name = Column(String(256), nullable=False)
    department = Column(String(256))
    # is_remote = Column(Boolean)
    location = Column(String(256))
    employment_type = Column(String(256))
    experience_level = Column(String(256))
    time_updated = Column(Time)
    company_uid = Column(String(6), ForeignKey('companies.company_uid'), nullable=False)

    def __repr__(self):
        return f'Position(position_id={self.position_uid!r}, position_name={self.pos_name!r}, department={self.department!r}, location={self.location!r}, employment_type={self.employment_type!r}, experience={self.experience_level!r}, time_updated={self.time_updated!r}, company_id={self.company_uid!r})'


class PositionDescription(Base):
    __tablename__ = 'position_description'

    id = Column(Integer, primary_key=True)
    position_uid = Column(String(6), ForeignKey('positions.position_uid'), nullable=False)
    description_title = Column(String(256))
    description = Column(Text)

    def __repr__(self):
        return f'Position(id={self.id!r}, position_id={self.position_uid!r}, description_title={self.description_title!r}, description={self.description!r})'


Base.metadata.create_all(engine)
