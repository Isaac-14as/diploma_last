from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from dotenv import load_dotenv
import os

load_dotenv()

DB = PostgresEngine(config={
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    })



APP_REGISTRY = AppRegistry(
    apps=["piccolo_db.piccolo_app"]
)