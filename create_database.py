import config
from sqlalchemy_utils import create_database
import db_details


def create_db():
    """
    creating a database into which we will put all of the information about the jobs we will scrape
    """
    create_database(config.engine.url)


def create_tables():
    """
    creates the tables in our comeet_jobs database
    """
    db_details.Base.metadata.create_all(config.engine)


if __name__ == '__main__':
    create_db()
    create_tables()
