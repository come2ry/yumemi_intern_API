from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN

from app import crud, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=List[str])
async def get_group_all(db: Session = Depends(deps.get_db)):
    """
    プロジェクト識別子を全てList型取得
    """

    try:
        groups = crud.read_groups(db)
        response_list = [group.group for group in groups]
        response_json = jsonable_encoder(response_list)
        return response_json

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
