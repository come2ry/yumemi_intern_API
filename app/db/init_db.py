
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db.base import Base  # noqa: F401
from app.db.session import engine  # noqa: F401

from fastapi.logger import logger as fastapi_logger

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


# groups = [
#     schemas.GroupsCreateInDB(group="projectA"),
#     schemas.GroupsCreateInDB(group="projectB"),
#     schemas.GroupsCreateInDB(group="projectC"),
#     schemas.GroupsCreateInDB(group="projectD"),
#     schemas.GroupsCreateInDB(group="projectE"),
#     schemas.GroupsCreateInDB(group="projectF"),
#     schemas.GroupsCreateInDB(group="projectG"),
#     schemas.GroupsCreateInDB(group="projectH"),
#     schemas.GroupsCreateInDB(group="projectI"),
#     schemas.GroupsCreateInDB(group="projectJ"),
#     schemas.GroupsCreateInDB(group="projectK"),
#     schemas.GroupsCreateInDB(group="projectL"),
#     schemas.GroupsCreateInDB(group="projectM"),
#     schemas.GroupsCreateInDB(group="projectN"),
#     schemas.GroupsCreateInDB(group="projectO"),
#     schemas.GroupsCreateInDB(group="projectP"),
#     schemas.GroupsCreateInDB(group="projectQ"),
#     schemas.GroupsCreateInDB(group="projectR"),
#     schemas.GroupsCreateInDB(group="projectS"),
#     schemas.GroupsCreateInDB(group="projectU"),
#     schemas.GroupsCreateInDB(group="projectV"),
#     schemas.GroupsCreateInDB(group="projectW"),
#     schemas.GroupsCreateInDB(group="projectX")
# ]

words = [
    schemas.NgWordsParams(ng_word="クライアント名1", group="projectA"),
    schemas.NgWordsParams(ng_word="クライアント名2", group="projectA"),
    schemas.NgWordsParams(ng_word="クライアント名3", group="projectA"),
    schemas.NgWordsParams(ng_word="悲惨", group="projectB"),
    schemas.NgWordsParams(ng_word="最悪", group="projectC"),
    schemas.NgWordsParams(ng_word="絶望", group="projectD"),
    schemas.NgWordsParams(ng_word="やめ太郎", group="projectE"),
    schemas.NgWordsParams(ng_word="しんどい", group="projectF"),
    schemas.NgWordsParams(ng_word="めちゃくちゃしんどい", group="projectG"),
    schemas.NgWordsParams(ng_word="ブラック", group="projectH"),
    schemas.NgWordsParams(ng_word="よくない", group="projectI"),
    schemas.NgWordsParams(ng_word="全然よくない", group="projectJ"),
    schemas.NgWordsParams(ng_word="悲惨", group="projectK"),
    schemas.NgWordsParams(ng_word="絶望", group="projectL"),
    schemas.NgWordsParams(ng_word="やめ太郎", group="projectM"),
    schemas.NgWordsParams(ng_word="しんどい", group="projectN"),
    schemas.NgWordsParams(ng_word="めちゃくちゃしんどい", group="projectO"),
    schemas.NgWordsParams(ng_word="ブラック", group="projectP"),
    schemas.NgWordsParams(ng_word="よくない", group="projectQ"),
    schemas.NgWordsParams(ng_word="全然よくない", group="projectR"),
    schemas.NgWordsParams(ng_word="悲惨", group="projectS"),
    schemas.NgWordsParams(ng_word="絶望", group="projectU"),
    schemas.NgWordsParams(ng_word="やめ太郎", group="projectV"),
    schemas.NgWordsParams(ng_word="めちゃくちゃしんどい", group="projectW"),
    schemas.NgWordsParams(ng_word="よくない", group="projectX"),
]


def init_db(db: Session) -> None:
    tables = Base.metadata.tables
    print(list(tables.keys()))
    # Base.metadata.drop_all(bind=engine, tables=list(tables.values()), checkfirst=True)

    try:
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        db.rollback()
        raise e

    try:
        groups = crud.read_groups(db)
        groups_search_dict = {group.group: group.id for group in groups}

        word_in_list = []
        for ng_word in words:
            group_id = groups_search_dict.get(ng_word.group, None)
            if group_id is None:
                group_in = schemas.GroupsCreateInDB(
                    group=ng_word.group
                )
                created_group = crud.create_group(db, obj_in=group_in)
                group_id = created_group.id
                groups_search_dict[ng_word.group] = group_id

            word_in_list += [schemas.NgWordsParamsInDB(
                ng_word=ng_word.ng_word,
                group_id=group_id
            )]

        is_ok = crud.create_ng_words(db, obj_in_list=word_in_list)

        if is_ok:
            print(f"DB init success")
        else:
            print(f"DB init failed")

    except Exception as e:
        db.rollback()
        raise e
