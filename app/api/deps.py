from datetime import date, datetime, timedelta
from typing import Dict, Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from google.auth.transport import requests
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

import crud
import schemas
from core.config import settings
from database import db_session


def get_db() -> Generator:
    try:
        yield db_session
    finally:
        db_session.close()
