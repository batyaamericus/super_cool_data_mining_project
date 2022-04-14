import logging
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine
import config
import db_details
from config import db_setup_logger


engine = create_engine(config.ENGINE_URL, future=True)


def create_db():
    """
    creating a database into which we will put all of the information about the jobs we will scrape
    """
    if not database_exists(config.ENGINE_URL):
        db_setup_logger.info('database did not exist, creating it')
        create_database(config.ENGINE_URL)
    db_setup_logger.info('database exists, no action taken')


def create_tables():
    """
    creates the tables in our comeet_jobs database
    """
    db_details.Base.metadata.create_all(engine, checkfirst=True)
