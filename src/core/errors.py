from enum import Enum
from typing import Dict, Optional


class ErrorCode(str, Enum):
    UNKNOWN = "UNKNOWN"
    REPOSITORY_ERROR = "REPOSITORY_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"


class Error(Exception):
    """Inheritance purposes"""

    INTERNAL_CODE: ErrorCode
    DEFAULT_MESSAGE: str

    def __init__(self, message: Optional[str] = None):
        self._message = message or self.DEFAULT_MESSAGE

    @property
    def as_dict(self) -> Dict[str, str]:
        return {
            "code": self.INTERNAL_CODE,
            "message": self._message,
        }


class ResourceNotFound(Error):
    pass


class ValidationError(Error):
    pass


class RepositoryError(Error):
    pass


class RepositoryOperationalError(RepositoryError):
    INTERNAL_CODE = ErrorCode.DATABASE_ERROR
    DEFAULT_MESSAGE = "Constraint has been violated"
