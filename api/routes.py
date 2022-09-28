import logging
import os

from fastapi import FastAPI

from api import chatroom, users, chats, security, messages

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL)
logger.setLevel(level=LOG_LEVEL)


def register_routers(app: FastAPI) -> None:
    """ Register routers against the app

    Args:
        app: The FastAPI application
    """

    chatroom.register_router(app)
    users.register_router(app)
    chats.register_router(app)
    security.register_router(app)
    messages.register_router(app)
