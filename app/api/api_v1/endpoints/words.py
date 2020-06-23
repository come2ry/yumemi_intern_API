from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN

from app import crud, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("", response_model=List[schemas.Words])
async def get_words_all(group: str = None, db: Session = Depends(deps.get_db)):
    words = crud.read_word_from_group(db, group=group)
    return words


@router.post("")
async def post_word(db: Session = Depends(deps.get_db)):
    pass
