import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi.logger import logger as fastapi_logger
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)


# DBに挿入する形式
class GroupsCreateInDB(BaseModel):
    group: constr(min_length=1, max_length=50)

# DBに含まれる形式の基盤
class GroupsInDBBase(BaseModel):
    id: PositiveInt
    group: constr(min_length=1, max_length=50)

# DBに含まれる形式
class GroupsInDB(GroupsInDBBase):
    class Config:
        orm_mode = True

# DBにから返す時のResponseの形式
class Groups(GroupsInDBBase):
    class Config:
        orm_mode = True