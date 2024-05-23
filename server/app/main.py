from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import Mount
from sqladmin import Admin

from app.users.router import router as router_users
from app.devices.router import router as router_devices
from piccolo_db.piccolo_app import APP_CONFIG
from piccolo_admin.endpoints import create_admin
from piccolo_db.tables import *
from starlette.requests import Request

admin = create_admin([Users, Device, ValueDevice, ManagementLog, AccidentLog])

app = FastAPI(routes=[
    Mount("/admin/", create_admin(tables=APP_CONFIG.table_classes))
])

@app.middleware("http")
async def add_timeout_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["timeout"] = "1000"
    return response

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)
app.include_router(router_devices)


# from piccolo_db.tables import Device

# async def initialize_database():
#     await Device('Трансформатор 1', 'трансформатор', True, 'исправен')

#  initialize_database()