import hashlib
import logging
from sqlalchemy import func

from fastapi import Depends
from sqlalchemy.dialects.mysql import insert

from config import settings
from db.chemas import UserModel
from db.models import User
from db.mysql import get_mysql_session

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


async def create_new_user(user: UserModel, session=Depends(get_mysql_session)):
    try:
        hashed_password = hashlib.sha256(user.user_password.encode(settings.ENCODER)).hexdigest()
        salt = hashlib.sha256(user.user_password.encode(settings.ENCODER)).hexdigest()
        session_query = insert(User). \
            values(user_name=user.user_name, user_password=hashed_password, user_salt=salt). \
            on_duplicate_key_update(id=func.LAST_INSERT_ID(User.id),
                                    user_name=user.user_name)

        res = session.execute(session_query)
        session.commit()
        return res.lastrowid
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create user {user} with error: {e}")
        raise e


async def get_user_by_name(user_name: str, session=Depends(get_mysql_session)):
    try:
        user = session.query(User).filter(User.user_name == user_name).first()
        return user
    except Exception as e:
        logger.error(f"Failed to get user {user_name} with error: {e}")
        raise e


