from fastapi import APIRouter, Depends, Response

from app.users.dependencies import get_current_user, is_admin_user
from app.exceptions import *
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.schemas import *
from piccolo_db.tables import Users


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],    
)

@router.post('/register')
async def register(user: SUserRegister):
    existing_user = await Users.objects().where(Users.email==user.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user.password)
    existing_user = await Users(email=user.email, hashed_password=hashed_password, name=user.name, role=user.role).save()
    return {'status': 200, 'detail': 'Пользователь успешно зарегистрирован.'}

@router.post('/login')
async def login(user_data: SUserLogin, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie("app_access_token", access_token)
    return {'access_token': access_token}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("app_access_token")
    return {'status': 200, 'detail': 'Успешный выход из аккаунта.'}


@router.get('/get_me', response_model=SUserGet)
async def get_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get('/get_all_users', response_model=list[SUserGet], dependencies=[Depends(is_admin_user)])
async def get_all_users():
    users = await Users.select()
    return users

@router.delete('/delete_user_by_id/{user_id}', dependencies=[Depends(is_admin_user)])
async def delete_user_by_id(user_id: int):
    user = await Users.objects().where(Users.id == user_id).first()
    await user.remove()
    return {'status': 200, 'detail': 'Пользователь успешно удален.'}


@router.patch('/change_user_by_id/{user_id}', dependencies=[Depends(is_admin_user)])
async def change_user_by_id(user_id: int, corrected_user: SUserPatch):
    await Users.update().where(Users.id == user_id).values(name=corrected_user.name, role=corrected_user.role).run()
    return {'status': 200, 'detail': 'Данные пользователя изменены.'}