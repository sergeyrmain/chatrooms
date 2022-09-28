import logging

from fastapi import APIRouter, Depends, Query, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import Required
from starlette import status
from starlette.responses import JSONResponse
from typing import List

from config import settings
from db.mysql import get_mysql_session
from db.resopnse_models import ChatResponse
from exception import ExceptionHandler
from logic.chats_logic import get_users_chats, create_new_chat

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='/chats')


@router.get('/chats', tags=['chats'], response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
async def get_chats(user_name: str = Query(Required, alias='userName'), session=Depends(get_mysql_session), form_token: str = Depends(oauth2_scheme)):
    try:
        res = await get_users_chats(user_name, session)
        return res
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'detail': e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.post('/chats', tags=['chats'], status_code=status.HTTP_201_CREATED)
async def create_chat(user_name: str = Query(Required, alias='userName'), session=Depends(get_mysql_session), form_token: str = Depends(oauth2_scheme)):
    try:
        res = await create_new_chat(user_name, session)
        return JSONResponse(content={'detail': res}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'detail': e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
