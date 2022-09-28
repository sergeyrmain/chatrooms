import logging

from fastapi import APIRouter, Depends, Query, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import Required
from starlette import status
from starlette.responses import JSONResponse
from typing import List

from config import settings
from db.chemas import Message
from db.mysql import get_mysql_session
from db.resopnse_models import MessagesResponse
from logic.messages_logic import get_chats_messages, create_new_message

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='/messages')


@router.get('/messages', tags=['messages'], response_model=List[MessagesResponse], status_code=status.HTTP_200_OK)
async def get_messages(chat_id: int = Query(Required, alias='chatId'), session=Depends(get_mysql_session),
                       form_token: str = Depends(oauth2_scheme)):
    try:
        res = await get_chats_messages(chat_id, session)
        return res
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'detail': e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.post('/messages', tags=['messages'], status_code=status.HTTP_201_CREATED)
async def create_message(message: Message=Query(Required), session=Depends(get_mysql_session),
                         form_token: str = Depends(oauth2_scheme)):
    try:
        res = await create_new_message(message, session)
        return JSONResponse(content={'detail': res}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(e)
        return JSONResponse(content={'detail': e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)