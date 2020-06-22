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


def get_word_from_group(db: Session, group: str):
    query = db.query(models.Words)
    query= query.join(models.Groups)
    query = query.filter(models.Groups.group == group)

    words = query.all()
    return words
