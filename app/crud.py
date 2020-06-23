import json
import os
from datetime import date, datetime
from typing import Dict, List, Optional, Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger
from sqlalchemy import bindparam, or_, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, joinedload, load_only

from app import models, schemas


def read_ng_word_from_id(db: Session, ng_word_id: int):
    """
    ng_word_idからng_wordを取得する
    存在しない場合はNoneを返す
    """

    return db.query(models.NgWords).filter(models.NgWords.id == ng_word_id).one_or_none()


def delete_ng_word(db: Session, ng_word_id: int):
    """
    groupに紐づいた全てのGroupをDBからListで取得して返す
    groupを指定しないと全てのGroupが対象となる
    """

    try:
        ngWord = read_ng_word_from_id(db, ng_word_id=ng_word_id)

        if ngWord is None:
            fastapi_logger.error("Ng word not found.")
            return False

        db.delete(ngWord)
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e


def read_ng_words_from_group(db: Session, group: str = None) -> List[models.NgWords]:
    """
    groupに紐づいた全てのGroupをDBからListで取得して返す
    groupを指定しないと全てのGroupが対象となる
    """

    if group is None:
        ngWords = db.query(models.NgWords).all()
        return ngWords

    query = db.query(models.NgWords)
    query= query.join(models.Groups)
    query = query.filter(models.Groups.group == group)

    ngWords = query.all()
    return ngWords


def read_groups(db: Session) -> List[models.Groups]:
    """
    全てのGroupをDBからListで取得して返す
    """

    groups = db.query(models.Groups).all()
    return groups


def create_group(db: Session, obj_in: schemas.GroupsCreateInDB) -> models.Groups:
    """
    1件の新規GroupをDBへ挿入してGroupを返す
    ！！！DBへ存在しないことを事前に確認する必要あり！！！
    """

    try:
        group = models.Groups(**obj_in.dict())

        db.add(group)
        db.commit()

        # DBに挿入されたgroupに更新
        db.refresh(group)

        return group

    except Exception as e:
        db.rollback()
        raise e


def create_ng_word(db: Session, obj_in: schemas.NgWordsCreateInDB) -> models.NgWords:
    """
    1件のngWordをDBへ挿入してngWordを返す
    """

    try:
        ngWord = models.NgWords(**obj_in.dict())

        db.add(ngWord)
        db.commit()

        # DBに挿入されたときに付与されたidをngWord.idとして更新
        db.refresh(ngWord)

        return ngWord

    except Exception as e:
        db.rollback()
        raise e


def create_ng_words(db: Session, obj_in_list: List[schemas.NgWordsCreateInDB]) -> bool:
    """
    複数件のngWordをDBへ挿入して成功したらTrueを返す
    """

    try:
        ngWords = [models.NgWords(**obj_in.dict()) for obj_in in obj_in_list]

        db.add_all(ngWords)
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e
