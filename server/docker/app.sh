#!/bin/bash

piccolo migrations forwards piccolo_db --auto --auto_input='y'
piccolo migrations forwards session_auth
piccolo migrations forwards user
piccolo migrations forward all
piccolo user create --username="admin" --email="admin@admin.com" --password="${ADMIN_PASSWORD}" --is_admin=True --is_superuser=True --is_active=True
piccolo migrations check

# psql -U postgres -d diploma_db -h db 

gunicorn app.main:app --workers 20 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

# gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000  --certfile=cert.pem --keyfile=key.pem --forwarded-allow-ips="*"