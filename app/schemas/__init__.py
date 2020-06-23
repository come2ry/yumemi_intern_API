from .group import GroupsCreateInDB, GroupsInDB, Groups
from .word import WordsCreate, WordsCreateInDB, WordsInDB
from pydantic import (BaseModel, PositiveInt, ValidationError, constr, validator)


# DBにから返す時のResponseの形式
class Words(BaseModel):
    word: constr(min_length=1, max_length=50)
    group: Groups

    class Config:
        orm_mode = True

    @validator('group')
    def convert_group(cls, v, values):
        if v is None:
            raise ValueError('group can not be accessible')

        return v.group
