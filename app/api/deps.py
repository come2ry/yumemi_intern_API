from datetime import date, datetime, timedelta
from typing import Dict, Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from google.auth.transport import requests
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from app import crud, schemas
from app.core.config import settings
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
