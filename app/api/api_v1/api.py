from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

from app.api.api_v1.endpoints import group, scan, ng_word
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    ng_word.router,
    prefix="/ng_words",
    tags=["ng_words"]
)

api_router.include_router(
    scan.router,
    prefix="/scan",
    tags=["scan"]
)

api_router.include_router(
    group.router,
    prefix="/groups",
    tags=["groups"]
)
