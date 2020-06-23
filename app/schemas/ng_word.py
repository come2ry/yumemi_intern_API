import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi.logger import logger as fastapi_logger
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)

# POST Requestで受け取る形式
class NgWordsParams(BaseModel):
    ng_word: constr(min_length=1, max_length=50)
    group: constr(min_length=1, max_length=50)

# DBに挿入する時の形式
class NgWordsParamsInDB(BaseModel):
    ng_word: constr(min_length=1, max_length=50)
    group_id: PositiveInt

# DBに含まれる形式の基盤
class NgWordsInDBBase(BaseModel):
    id: PositiveInt
    ng_word: constr(min_length=1, max_length=50)
    group_id: PositiveInt

# DBに含まれる形式
class NgWordsInDB(NgWordsInDBBase):
    class Config:
        orm_mode = True
