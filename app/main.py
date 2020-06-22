import logging
import sys
from logging.handlers import RotatingFileHandler

from fastapi import Depends, FastAPI, Header
from fastapi.logger import logger as fastapi_logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from api.api_v1.api import api_router
from core.config import settings
from db.session import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# APIサーバシャットダウン時にDBセッションを削除
@app.on_event("shutdown")
async def shutdown_event():
    db = SessionLocal()
    db.remove()


app.include_router(
    api_router
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")