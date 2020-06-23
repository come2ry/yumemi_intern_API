import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi.logger import logger as fastapi_logger
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)

# POST Requestで受け取る形式
class WordsCreate(BaseModel):
    word: constr(min_length=1, max_length=50)
    group: constr(min_length=1, max_length=50)

# DBに挿入する時の形式
class WordsCreateInDB(BaseModel):
    word: constr(min_length=1, max_length=50)
    groupId: PositiveInt

# DBに含まれる形式の基盤
class WordsInDBBase(BaseModel):
    id: PositiveInt
    word: constr(min_length=1, max_length=50)
    groupId: PositiveInt

# DBに含まれる形式
class WordsInDB(WordsInDBBase):
    class Config:
        orm_mode = True

# # DBにから返す時のResponseの形式
# class Words(BaseModel):
#     word: constr(min_length=1, max_length=50)
#     group: str = None

#     class Config:
#         orm_mode = True
