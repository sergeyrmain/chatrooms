import logging

from fastapi import APIRouter, Depends, Query, FastAPI
from pydantic import Required
from starlette import status
from starlette.responses import JSONResponse
from typing import List

from config import settings
from db.mysql import get_mysql_session
from db.resopnse_models import RoomsResponse
from exception import ExceptionHandler

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='/chats')
