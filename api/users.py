import logging

from fastapi import APIRouter, Depends, Query, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import Required
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from db.chemas import UserModel, UserPasswordCredentials
from db.mysql import get_mysql_session
from logic.users_logic import  create_new_user

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)



def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='/users')


@router.post('/register', tags=['user'])
async def create_user(user: UserModel, session=Depends(get_mysql_session)):
    try:
        res = await create_new_user(user, session)
        return JSONResponse(content={'detail': res}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Failed to create user {user} with error: {e}")
        return JSONResponse(content={'detail': f"Failed to create user {user} with error: {e}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
