import logging
from typing import Iterator, Optional

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import settings
from db.mysql_init import orm_init

Base = declarative_base()
SessionLocal: Optional[sessionmaker] = None
engine: Optional[Engine] = None


logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


def init_connection(debug=False):
    logger.info(f'init mysql connection')

    global SessionLocal
    SessionLocal = orm_init()



def get_mysql_session() -> Iterator[Session]:
    """

    """
    if SessionLocal is None:
        init_connection()
    session = None
    try:
        session = SessionLocal
        yield session
    except:
        session.rollback()
        session.close()
        raise
    finally:
        if session:
            session.close()