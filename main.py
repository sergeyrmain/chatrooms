import logging

from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRoute

from api.routes import register_routers
from config import settings

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)


@app.on_event("startup")
async def startup():
    logger.info("startup")
    register_routers(app)

    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000, debug=True)
