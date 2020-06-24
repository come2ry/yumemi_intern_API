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

from app import crud, schemas, utils
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("", response_model=schemas.Scan)
async def post_scan(params: schemas.ScanParams, db: Session = Depends(deps.get_db)):
    """
    テキストを検閲する
    追加で、テキスト内に画像のurlがあれば、Vision APIのOCRで文字を抽出して読み込む
    """

    try:
        urls = utils.extract_image_url_from_text(params.text)
        if len(urls) > settings.VISION_API_LIMIT_PER_ONCE:
            # APIのレイテンシを加味して settings.VISION_API_LIMIT_PER_ONCE 枚以下に制限
            raise HTTPException(status_code=400, detail=f"Image url num is more than {settings.VISION_API_LIMIT_PER_ONCE}. The URL of the image must be no more than {settings.VISION_API_LIMIT_PER_ONCE} in the text.")

        fastapi_logger.info(urls)
        img_ocr_text = utils.extract_text_from_image_by_urls_with_OCR(urls)
        fastapi_logger.info(img_ocr_text)
        params.text += img_ocr_text

        fastapi_logger.info(params.text)
        ngWords = crud.read_ng_words_from_group(db)

        response_models_list = []
        for ngWord in ngWords:
            ng_word = ngWord.ng_word
            if ng_word in params.text:
                response_models_list += [ngWord]

        response_json = {
            "secret_found": len(response_models_list),
            "secrets": response_models_list
        }
        return response_json


    except Exception as e:
        fastapi_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))
