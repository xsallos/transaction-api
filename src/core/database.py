__all__ = ("engine", "Base", "get_session")

from sqlalchemy import create_engine
from sqlalchemy.exc import (
    IntegrityError,
    InternalError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..settings import settings
from .errors import RepositoryOperationalError

engine = create_engine(
    f"postgresql://{settings.db_username}:{settings.db_password}"
    f"@{settings.db_hostname}:{settings.db_port}/{settings.db_name}",
    echo=False,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def catch_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            OperationalError,
            IntegrityError,
            InternalError,
            ProgrammingError,
            ValueError,
        ) as exc:
            raise RepositoryOperationalError(message=str(exc)) from exc

    return wrapper
