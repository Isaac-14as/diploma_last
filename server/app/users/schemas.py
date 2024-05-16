from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    name: str
    role: str
    password: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str

class SUserGet(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

class SUserPatch(BaseModel):
    name: str
    role: str