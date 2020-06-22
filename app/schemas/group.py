import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi.logger import logger as fastapi_logger
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)

from .words import WordsInDBBase

class GroupsInDBBase(BaseModel):
    id: PositiveInt
    group: constr(min_length=1, max_length=50)

class GroupsInDB(GroupsInDBBase):
    class Config:
        orm_mode = True

class Groups(GroupsInDBBase):
    pass
