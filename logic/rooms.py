import logging

from fastapi import Depends
from sqlalchemy import func
from starlette import status
from sqlalchemy.dialects.mysql import insert

from config import settings
from db.chemas import RoomChat
from db.models import Room
from db.mysql import get_mysql_session
from exception import ExceptionHandler
from logic.users import get_user_by_name

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


async def create_new_room(room: RoomChat, session=Depends(get_mysql_session)):
    try:
        user_id = get_user_by_name(room.user_name, session)
        if not user_id:
            raise ExceptionHandler(error_status=status.HTTP_404_NOT_FOUND,
                                   error_message=f"User {room.user_name} not found")
        room.user_id = user_id
        session_query = insert(Room).values(room_name=room.room_name,
                                            user_id=room.user_id).on_duplicate_key_update(id=func.LAST_INSERT_ID(Room.id),
                                                                                          room_name=room.room_name,
                                                                                          user_id=room.user_id)
        res = session.execute(session_query)
        session.commit()
        return res.lastrowid
    except Exception as e:
        session.rollback()
        raise ExceptionHandler(error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                               error_message=f"Failed to create room {room} with error: {e}")


async def get_all_rooms(session=Depends(get_mysql_session)):
    try:
        rooms = session.query(Room).all()
        return rooms
    except Exception as e:
        logger.error(f"Failed to get all rooms with error: {e}")
        raise e
