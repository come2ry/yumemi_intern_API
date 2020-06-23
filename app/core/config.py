import secrets
from typing import Any, Dict, List, Optional, Union

from fastapi.logger import logger as fastapi_logger
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, HttpUrl, validator


class MysqlDsn(AnyUrl):
    allowed_schemes = {'mysql+pymysql'}
    user_required = True


class Settings(BaseSettings):
    DEBUG_MODE: bool = True

    @validator("DEBUG_MODE", pre=True)
    def assemble_DEBUG_MODE(cls, v: Optional[Union[bool, str]], values: Dict[str, Any]) -> bool:
        if isinstance(v, bool):
            return v
        elif isinstance(v, str):
            if v.lower() == "true":
                return True
            else:
                return False

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    API_LOCATION: str
    BACKEND_CORS_ORIGINS: Any = [
        "http://localhost.api.dev"
    ]

    # MYSQL
    MYSQL_SERVER: str = ''
    CLOUD_SQL_INSTANCE_NAME: str = ''
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    SQLALCHEMY_DATABASE_URI: str = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> MysqlDsn:
        # When deployed to App Engine, the `GAE_ENV` environment variable will be
        # set to `standard`
        if values.get('GAE_ENV', '') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(values.get("CLOUD_SQL_INSTANCE_NAME"))
            sqlalchemy_uri = MysqlDsn.build(
                scheme="mysql+pymysql",
                user=values.get("MYSQL_USER"),
                password=values.get("MYSQL_PASSWORD"),
                host='',
                path=f"/{values.get('MYSQL_DATABASE')}?unix_socket={unix_socket}&charset=utf8",
            )

        else:
            # If running locally, use the TCP connections instead
            # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
            # so that your application can use 127.0.0.1:3306 to connect to your
            # Cloud SQL instance

            sqlalchemy_uri = MysqlDsn.build(
                scheme="mysql+pymysql",
                user=values.get("MYSQL_USER", "root"),
                password=values.get("MYSQL_PASSWORD", "root"),
                host=values.get("MYSQL_SERVER", "127.0.0.1:3306"),
                path=f"/{values.get('MYSQL_DB') or 'yumemi_db'}?charset=utf8mb4",
            )

        return sqlalchemy_uri

    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        'encoding': "utf-8",
        'pool_size': 10,
        'max_overflow': 2,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        'convert_unicode': True,
        'echo': True,
    }

    class Config:
        case_sensitive = True


settings = Settings()
