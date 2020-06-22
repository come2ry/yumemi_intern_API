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
