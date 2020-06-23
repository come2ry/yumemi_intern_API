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

@router.get("", response_model=List[schemas.NgWords])
async def get_ng_words_all(group: str = None, db: Session = Depends(deps.get_db)):
    """
    プロジェクト識別子を指定して、紐づいた単語オブジェクトをリストで取得する
    groupを指定しない時、全ての単語を閲覧する
    """

    try:
        ngWords = crud.read_ng_words_from_group(db, group=group)
        return ngWords
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=schemas.NgWordsInDB)
async def post_ng_word(params: schemas.NgWordsParams, db: Session = Depends(deps.get_db)):
    """
    機密単語をDBに追加する
    登録時にプロジェクト識別子は必須項目
    """

    try:
        groups = crud.read_groups(db)
        groups_search_dict = {group.group: group.id for group in groups}

        group_id = groups_search_dict.get(params.group, None)
        if group_id is None:
            group_in = schemas.GroupsCreateInDB(
                group=params.group
            )
            created_group = crud.create_group(db, obj_in=group_in)
            group_id = created_group.id
            groups_search_dict[params.group] = group_id


    except Exception as e:
        fastapi_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))


    ngWords = crud.read_ng_words_from_group(db, group=params.group)
    ng_words_search_set = {ngWord.ng_word for ngWord in ngWords}
    if params.ng_word in ng_words_search_set:
        fastapi_logger.error("Duplicated ng word")
        raise HTTPException(status_code=409, detail="Duplicated ng word")

    try:
        ngWord_in = schemas.NgWordsParamsInDB(
            ng_word=params.ng_word,
            group_id=group_id
        )

        ngWord = crud.create_ng_word(db, obj_in=ngWord_in)
        return ngWord

    except Exception as e:
        fastapi_logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/id/{ngWordId}")
async def delete_ng_word(ngWordId: int, db: Session = Depends(deps.get_db)):
    """
    機密単語をDBから削除する
    """

    try:
        is_ok = crud.delete_ng_word(db, ng_word_id=ngWordId)
        if not is_ok:
            raise HTTPException(status_code=404, detail="Ng word deleting was failed")

        response_json = {
            "detail": "OK"
        }

        return response_json

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
