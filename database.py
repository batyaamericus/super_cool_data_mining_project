from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database
from sqlalchemy import create_engine
import config
import db_details


engine = create_engine(config.ENGINE_URL, future=True)


def create_db():
    """
    creating a database into which we will put all of the information about the jobs we will scrape
    """
    try:
        create_database(config.ENGINE_URL)
    except ProgrammingError:
        print('Database already exists')


def create_tables():
    """
    creates the tables in our comeet_jobs database
    """
    db_details.Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()
    create_tables()