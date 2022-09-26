import logging

from fastapi import APIRouter, Depends, Query, FastAPI
from pydantic import Required
from starlette import status
from starlette.responses import JSONResponse
from typing import List

from config import settings
from db.chemas import RoomChat
from db.mysql import get_mysql_session
from db.resopnse_models import RoomsResponse
from exception import ExceptionHandler
from logic.rooms import create_new_room, get_all_rooms

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='/rooms')


@router.post('/create_room', tags=['rooms'])
async def create_room(room_name: RoomChat, session=Depends(get_mysql_session)):
    try:
        res = await create_new_room(room_name, session)
        return JSONResponse(content={'detail': res}, status_code=status.HTTP_201_CREATED)
    except ExceptionHandler as e:
        logger.error(f"Failed to create room {room_name} with error: {e}")
        return JSONResponse(content=e.error_message,
                            status_code=e.error_status)



@router.get('/get_rooms', tags=['rooms'], response_model=List[RoomsResponse], status_code=status.HTTP_200_OK)
async def get_rooms(session=Depends(get_mysql_session)):
    try:
        res = await get_all_rooms(session)
        if not res:
            return JSONResponse(content={'detail': f"no rooms"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return res
    except ExceptionHandler as e:
        logger.error(f"Failed to get rooms with error: {e}")
        return JSONResponse(content=e.error_message,
                            status_code=e.error_status)

