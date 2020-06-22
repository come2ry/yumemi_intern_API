from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

from app.api.api_v1.endpoints import group, scan, words
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    words.router,
    prefix="/words",
    tags=["words"]
)
