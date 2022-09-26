import logging

from celery.contrib.testing import manager
from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.responses import HTMLResponse


from config import settings


router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


def register_router(app: FastAPI) -> None:
    app.include_router(router)


@router.get("/")
async def get():
    return HTMLResponse(open("front/index.html").read())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")



@router.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, user_name: str):
    pass
