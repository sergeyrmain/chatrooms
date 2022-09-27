import logging
import jwt
from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from config import settings
from db.mysql import get_mysql_session
from exception import ExceptionHandler
from logic.security_logic import login_user, get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)
logger.setLevel(level=settings.LOG_LEVEL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def register_router(app: FastAPI) -> None:
    app.include_router(router, prefix='')


@router.post("/token")
async def token(form_token: OAuth2PasswordRequestForm = Depends(), session=Depends(get_mysql_session)):
    try:
        user = await login_user(form_token.username, form_token.password, session)
        if user:
            user_dict = {'username': form_token.username, 'password': form_token.password}
            access_token = jwt.encode(user_dict, settings.SECRET_KEY)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return {"detail": "Incorrect username or password"}
    except ExceptionHandler as e:
        logger.error(e.error_message, e.error_status)
        return JSONResponse(content={'detail': e.error_message}, status_code=e.error_status)


@router.get("/get_current_user")
async def get_user(form_token: str = Depends(oauth2_scheme)):
    res = await get_current_user(form_token)
    print(res)
    return res


@router.get('/test')
async def testing(form_token: str = Depends(get_current_user)):

    return 'hello'

