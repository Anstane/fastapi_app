#!/bin/sh
cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port 8000