from fastapi.logger import logger as fastapi_logger
import os

import sys

sys.path.append(os.getcwd())
from app.db.init_db import init_db
from app.db.session import SessionLocal

def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    fastapi_logger.info("Creating initial data")
    init()
    fastapi_logger.info("Initial data created")


if __name__ == "__main__":
    main()