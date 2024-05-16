#!/bin/bash

piccolo migrations forwards piccolo_db


gunicorn app.main:app --workers 10 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

# gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000  --certfile=cert.pem --keyfile=key.pem --forwarded-allow-ips="*"