from sqladmin import ModelView

from piccolo_db.tables import *


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name, Users.email, Users.role]
    column_details_exclude_list = [Users.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"


class DeviceAdmin(ModelView, model=Device):
    column_list = [c.name for c in Device.__table__.c]
    name = "Устройство"
    name_plural = "Устройства"
    
class ValueDeviceAdmin(ModelView, model=ValueDevice):
    column_list = [c.name for c in ValueDevice.__table__.c]
    name = "Показание"
    name_plural = "Показания"

class ManagementLogAdmin(ModelView, model=ManagementLog):
    column_list = [c.name for c in ManagementLog.__table__.c]
    name = "Событие управления"
    name_plural = "Журнал управления"

class AccidentLogAdmin(ModelView, model=AccidentLog):
    column_list = [c.name for c in AccidentLog.__table__.c]
    name = "Аварийная ситуация"
    name_plural = "Журнал аварийных ситуаций"