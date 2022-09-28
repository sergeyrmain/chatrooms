import logging

from fastapi import Depends
from starlette import status
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func

from config import settings
from db.models import Chat, Message
from db.mysql import get_mysql_session
from exception import ExceptionHandler
from logic.users_logic import get_user_by_name

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


async def get_users_chats(user_name: str, session=Depends(get_mysql_session)):
    try:
        user = await get_user_by_name(user_name, session)

        chats = session.query(Chat.id, Chat.user_one, Chat.user_two, Message.message_time).join(Message, Message.chat_id == Chat.id).filter((Chat.user_one == user.id) | (
                Chat.user_two == user.id)).order_by(Message.message_time).distinct(Chat.id).all()
        chats = [{'id': chat.id, 'user_name': chat.user_one if chat.user_one != user.id else chat.user_two} for chat in chats]
        return chats
    except Exception as e:
        logger.error(f"Failed to get user {user_name} chats with error: {e}")
        raise e


async def create_new_chat(user_one: str, user_two: str, session=Depends(get_mysql_session)):
    try:
        session_query = insert(Chat). \
            values(user_one=user_one, user_two=user_two). \
            on_duplicate_key_update(id=func.LAST_INSERT_ID(Chat.id),
                                    user_one=user_one, user_two=user_two)

        res = session.execute(session_query)
        session.commit()
        return res.lastrowid
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create chat between {user_one} and {user_two} with error: {e}")
        raise e