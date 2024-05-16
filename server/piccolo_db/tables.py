
from piccolo.table import Table
from piccolo.columns import Varchar, Timestamp, Boolean, Float, ForeignKey

class Users(Table):
    email = Varchar(length=30)
    hashed_password = Varchar()
    name = Varchar(length=40)
    role = Varchar()

class Device(Table):
    name = Varchar()
    type = Varchar()
    is_active = Boolean(default=True)
    status = Varchar(default='исправен')

class ValueDevice(Table):
    full_power = Float()
    active_power = Float()
    reactive_power = Float()
    voltage = Float()
    amperage = Float()
    power_factor = Float()
    date_of_origin = Timestamp()
    device_id = ForeignKey(references=Device)

class ManagementLog(Table):
    info = Varchar()
    action = Varchar()
    date_of_origin = Timestamp()
    user_id = ForeignKey(references=Users)
    device_id = ForeignKey(references=Device)

class AccidentLog(Table):
    info = Varchar()
    date_of_origin = Timestamp()
    device_id = ForeignKey(references=Device)