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

@router.post("", response_model=schemas.Scan)
async def post_scan(params: schemas.ScanParams, db: Session = Depends(deps.get_db)):
    """
    検閲する
    """

    try:
        ngWords = crud.read_ng_words_from_group(db)

        response_models_list = []
        for ngWord in ngWords:
            ng_word = ngWord.ng_word
            if ng_word in params.test:
                response_models_list += [ngWord]

        response_json = {
            "secret_found": len(response_models_list),
            "secrets": response_models_list
        }

        return response_json


    except Exception as e:
        fastapi_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
