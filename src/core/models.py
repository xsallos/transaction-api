from typing import NamedTuple

from pydantic import BaseModel, Field

__all__ = (
    "OffsetPaginationModel",
    "OffsetPaginationInput",
)


class OffsetPaginationInput(NamedTuple):
    page: int
    size: int

    @property
    def offset(self):
        return (self.page - 1) * self.size


class OffsetPaginationModel(BaseModel):
    class Config:
        extra = "forbid"

    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, le=100, default=10)

    @property
    def as_input(self) -> OffsetPaginationInput:
        return OffsetPaginationInput(page=self.page, size=self.size)
