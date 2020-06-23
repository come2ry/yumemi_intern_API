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
async def get_words_all(db: Session = Depends(deps.get_db)):
    words = crud.read_words(db)
    return words

    # words_model_list = []
    # for word in words:
    #     words_model = schemas.Words.from_orm(word)
    #     words_model.group = words.group.group
    #     words_model_list += [words_model]
    # return words_model_list


@router.post("")
async def post_word(db: Session = Depends(deps.get_db)):
    pass
