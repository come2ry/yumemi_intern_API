import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi.logger import logger as fastapi_logger
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)


class WordsInDBBase(BaseModel):
    id: PositiveInt
    word: constr(min_length=1, max_length=50)
    groupId: PositiveInt


class WordsInDB(WordsInDBBase):
    class Config:
        orm_mode = True


class Words(WordsInDBBase):
    pass
