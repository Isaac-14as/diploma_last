import datetime
from pydantic import BaseModel

from app.users.schemas import SUserGet


class SDeviceAdd(BaseModel):
    name: str
    type: str
    is_active: bool 
    status: str

class SDeviceGet(SDeviceAdd):
    id: int

class SValueDeviceGet(BaseModel):
    full_power: float
    active_power: float
    reactive_power: float
    voltage: float
    amperage: float
    power_factor: float
    date_of_origin: datetime.datetime
    device_id: int


class SValueFullPower(BaseModel):
    full_power: float
    date_of_origin: datetime.datetime


class SManagementAdd(BaseModel):
    info: str
    action: str
    user_id: int
    device_id: int


# class SManagementLogGet(SManagementAdd):
#     id: int
#     info: str
#     action: str
#     date_of_origin: datetime.datetime

    