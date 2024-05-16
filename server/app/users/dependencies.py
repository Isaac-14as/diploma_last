from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime
from dotenv import load_dotenv
import os

from app.exceptions import *
from piccolo_db.tables import Users

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def get_token(request: Request):
    token_cookies = request.cookies.get("app_access_token")
    token_headers = request.headers.get("Authorization")
    if token_cookies:
        return token_cookies
    elif token_headers:
        return token_headers
    else:
        raise TokenAbsentException

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFromatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    # user = await UsersDAO.find_by_id(int(user_id))
    user = await Users.objects().where(Users.id == int(user_id)).first()
    if not user:
        raise UserIsNotPresentException
    return user

async def is_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise NotAdminException
    return True
