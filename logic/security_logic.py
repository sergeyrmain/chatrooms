import hashlib
import logging

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from config import settings
from db.mysql import get_mysql_session
from exception import ExceptionHandler
from logic.users_logic import get_user_by_name

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode(settings.ENCODER)).hexdigest() == hashed_password


async def login_user(user_name, password, session=Depends(get_mysql_session)):
    try:
        user = await get_user_by_name(user_name, session)
        if not user:
            return False
        if not verify_password(password, user.user_password):
            return False
        return True
    except Exception as e:
        logger.error(e)
        error = ExceptionHandler(error_status=status.HTTP_500_INTERNAL_SERVER_ERROR, error_message=e)
        error.raise_exception()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token == 'undefined':
        error = ExceptionHandler(error_status=status.HTTP_401_UNAUTHORIZED, error_message='Invalid token')
        error.raise_exception()
    try:
        user = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(user)
        return user
    except Exception as e:
        logger.error(e)
        error = ExceptionHandler(error_status=status.HTTP_500_INTERNAL_SERVER_ERROR, error_message=e)
        error.raise_exception()
