import logging
import time

from fastapi import Depends
from starlette import status
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func, or_

from config import settings
from db.models import Message, User
from db.mysql import get_mysql_session

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


async def get_chats_messages(chat_id: int, session=Depends(get_mysql_session)):
    try:
        messages = session.query(Message).filter(Message.chat_id == chat_id).join(User, or_(User.id == Message.sender, User.id == Message.receiver)).order_by(Message.message_time).all()
        print(messages)
        return messages
    except Exception as e:
        logger.error(f"Failed to get chat {chat_id} messages with error: {e}")
        raise e


async def create_new_message(message: Message, session=Depends(get_mysql_session)):
    try:
        current_ts = int(time.time() * 1000)
        session_query = insert(Message). \
            values(chat_id=message.chat_id, sender=message.sender, receiver=message.receiver, message_text=message.message_text, message_time=current_ts)
        res = session.execute(session_query)
        session.commit()
        return res.lastrowid

    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create message {message} with error: {e}")
        raise e

