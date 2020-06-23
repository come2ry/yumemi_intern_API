from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

from app.api.api_v1.endpoints import group, scan, ng_words
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    ng_words.router,
    prefix="/ng_words",
    tags=["ng_words"]
)
