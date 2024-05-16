from fastapi import APIRouter, Depends
from datetime import datetime, timedelta

from app.devices.schemas import *
from app.users.dependencies import get_current_user, is_admin_user
from piccolo_db.tables import AccidentLog, Device, ManagementLog, ValueDevice

router = APIRouter(
    prefix="/device",
    tags=["Devices & Устройства"],
)

async def get_value_device_by_date_time(device_id: int, date: str, time_from: str, time_to: str):
    date = datetime.strptime(date, "%Y-%m-%d").date()
    if time_from and time_to:
        time_from = datetime.strptime(time_from, "%H:%M:%S").time()
        time_to = datetime.strptime(time_to, "%H:%M:%S").time()
        datetime_from = datetime.combine(date, time_from)
        datetime_to = datetime.combine(date, time_to)
        return await ValueDevice.objects().where(
            (ValueDevice.device_id == device_id) &
            (ValueDevice.date_of_origin >= datetime_from) & 
            (ValueDevice.date_of_origin <= datetime_to)
        )
    return await ValueDevice.objects().where(
            (ValueDevice.device_id == device_id) &
            (ValueDevice.date_of_origin >= date) & 
            (ValueDevice.date_of_origin < (date + timedelta(days=1)))
        )


@router.post('/add_device', dependencies=[Depends(is_admin_user)])
async def add_device(device: SDeviceAdd):
    await Device(**device.model_dump()).save()
    return {'status': 200, 'detail': 'Устройство успешно добавлено.'}


@router.get('/get_all_devices', response_model=list[SDeviceGet], dependencies=[Depends(get_current_user)])
async def get_all_devices():
    return await Device.select()


@router.get('/get_device_by_id/{device_id}', response_model=SDeviceGet, dependencies=[Depends(get_current_user)])
async def get_device_by_id(device_id: int):
    return await Device.objects().where(Device.id == device_id).first()


@router.get('/get_value_device_by_id/{device_id}', response_model=list[SValueDeviceGet], dependencies=[Depends(get_current_user)])
async def get_value_device_by_id(device_id: int, date: str = None, time_from: str = None, time_to: str = None):
    if date:
        return await get_value_device_by_date_time(device_id, date, time_from, time_to)
    return await ValueDevice.select()


@router.get('/get_last_value_device_by_id/{device_id}', response_model=SValueDeviceGet, dependencies=[Depends(get_current_user)])
async def get_last_value_device_by_id(device_id: int):
    return await ValueDevice.select().where(ValueDevice.device_id==device_id).order_by(ValueDevice.date_of_origin, ascending=False).first()


@router.get('/get_full_power/{device_id}', response_model=list[SValueFullPower], dependencies=[Depends(get_current_user)])
async def get_full_power(device_id: int, date: str = None, time_from = None, time_to = None):
    if date:
        return await get_value_device_by_date_time(device_id, date, time_from, time_to)
    return await ValueDevice.select()


@router.patch('/device_switch/{device_id}', dependencies=[Depends(get_current_user)])
async def device_switch(device_id: int):
    device = await Device.objects().where(Device.id==device_id).first()
    await Device.update().where(Device.id==device_id).values(is_active=not device.is_active).run()
    if device.is_active:
        return {'status': 200, 'detail': 'Устройство выключено.'}
    return {'status': 200, 'detail': 'Устройство включено.'}


@router.post('/add_management_log', dependencies=[Depends(get_current_user)])
async def add_management_log(management_log_info: SManagementAdd):
    await ManagementLog(**management_log_info.model_dump()).save()
    return {'status': 200, 'detail': 'Запиcь успешно добавлена.'}


@router.get('/get_management_log', dependencies=[Depends(get_current_user)])
async def get_management_log(date: str = None, time_from: str = None, time_to: str = None):
    if date and time_from and time_to:
        date = datetime.strptime(date, "%Y-%m-%d").date()
        time_from = datetime.strptime(time_from, "%H:%M:%S").time()
        time_to = datetime.strptime(time_to, "%H:%M:%S").time()
        datetime_from = datetime.combine(date, time_from)
        datetime_to = datetime.combine(date, time_to)
        return await ManagementLog.select(ManagementLog.all_columns(), ManagementLog.user_id.all_columns(), ManagementLog.device_id.all_columns()).where(
            (ManagementLog.date_of_origin >= datetime_from) & 
            (ManagementLog.date_of_origin <= datetime_to)
        )
    if date:
        date = datetime.strptime(date, "%Y-%m-%d").date()
        return await ManagementLog.select(ManagementLog.all_columns(), ManagementLog.user_id.all_columns(), ManagementLog.device_id.all_columns()).where(
            (ManagementLog.date_of_origin >= date) & 
            (ManagementLog.date_of_origin < (date + timedelta(days=1)))
        )
    return await ManagementLog.select(ManagementLog.all_columns(), ManagementLog.user_id.all_columns(), ManagementLog.device_id.all_columns())


@router.get('/get_accident_log', dependencies=[Depends(get_current_user)])
async def get_accident_log(date: str = None, time_from: str = None, time_to: str = None):
    if date and time_from and time_to:
        date = datetime.strptime(date, "%Y-%m-%d").date()
        time_from = datetime.strptime(time_from, "%H:%M:%S").time()
        time_to = datetime.strptime(time_to, "%H:%M:%S").time()
        datetime_from = datetime.combine(date, time_from)
        datetime_to = datetime.combine(date, time_to)
        return await AccidentLog.select(AccidentLog.all_columns(), AccidentLog.device_id.all_columns()).where(
            (AccidentLog.date_of_origin >= datetime_from) & 
            (AccidentLog.date_of_origin <= datetime_to)
        )
    if date:
        date = datetime.strptime(date, "%Y-%m-%d").date()
        return await AccidentLog.select(AccidentLog.all_columns(), AccidentLog.device_id.all_columns()).where(
            (AccidentLog.date_of_origin >= date) & 
            (AccidentLog.date_of_origin < (date + timedelta(days=1)))
        )
    return await AccidentLog.select(AccidentLog.all_columns(), AccidentLog.device_id.all_columns())
