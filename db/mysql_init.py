import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


def orm_init():
    mysql_host = settings.MYSQL_HOST
    mysql_user = settings.MYSQL_USER
    mysql_password = settings.MYSQL_PASSWORD
    mysql_port = settings.MYSQL_PORT
    mysql_db = settings.MYSQL_DB
    logger.info('connecting to mysql')
    engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/' + mysql_db,
                           pool_pre_ping=True,
                           convert_unicode=True,
                           connect_args=dict(use_unicode=True),
                           echo=False)
    session_maker = sessionmaker(bind=engine)
    mysql_session = scoped_session(session_maker)
    return mysql_session
