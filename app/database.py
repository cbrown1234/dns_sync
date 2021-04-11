from functools import lru_cache
from typing import Iterator

from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.config import settings


def get_db(db_url=settings.SQLALCHEMY_DATABASE_URL) -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker(db_url).get_db()


@lru_cache()
def _get_fastapi_sessionmaker(
    db_url=settings.SQLALCHEMY_DATABASE_URL,
) -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    return FastAPISessionMaker(db_url)


Base = declarative_base()
