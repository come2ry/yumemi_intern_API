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


def read_word_from_group(db: Session, group: str):
    # query = db.query(models.Words)
    # query= query.join(models.Groups)
    query = db.query(models.Groups)
    query = query.filter(models.Groups.group == group)
    query= query.join(models.Words)

    words = query.all()
    return words

def read_groups(db: Session):
    groups = db.query(models.Groups).all()
    return groups


def create_group(db: Session, obj_in: schemas.GroupsCreateInDB):
    try:
        group = models.Groups(**obj_in.dict())

        db.add(group)
        db.commit()

        # DB.に挿入されたgroupに更新
        db.refresh(group)

        return group

    except Exception as e:
        db.rollback()
        raise e


def create_words(db: Session, obj_in_list: List[schemas.WordsCreateInDB]):
    try:
        words = [models.Words(**obj_in.dict()) for obj_in in obj_in_list]

        db.add_all(words)
        db.commit()

        # # DB.に挿入されたgroupに更新
        # db.refresh(words)

        return True

    except Exception as e:
        db.rollback()
        raise e
