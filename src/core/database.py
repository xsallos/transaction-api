__all__ = ("engine", "Base", "get_session")

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError, InternalError, ProgrammingError

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .errors import RepositoryUniqueConstraintError, RepositoryOperationalError
from ..settings import settings

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
        except IntegrityError:
            raise RepositoryUniqueConstraintError(message="Unique constraint has been violated")
        except (
                OperationalError,
                InternalError,
                ProgrammingError,
                ValueError,
        ) as error:
            raise RepositoryOperationalError(message=str(error)) from error

    return wrapper
