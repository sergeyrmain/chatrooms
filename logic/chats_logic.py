import logging

from fastapi import Depends
from sqlalchemy import func
from starlette import status
from sqlalchemy.dialects.mysql import insert

from config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


