from .group import GroupsCreateInDB, GroupsInDB, Groups
from .word import WordsCreate, WordsCreateInDB, WordsInDB
from fastapi.logger import logger as fastapi_logger
from typing import Any, Dict, List, Optional
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)


# DBにから返す時のResponseの形式
class Words(BaseModel):
    word: constr(min_length=1, max_length=50)
    group: constr(min_length=1, max_length=50)

    class Config:
        orm_mode = True

    @validator("group", pre=True, each_item=True)
    def convert_group(cls, group: Groups) -> str:
        return group.group