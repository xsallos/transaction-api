__all__ = (
    "Transaction",
    "CustomerSummary",
    "ProductSummary",
    "TransactionsPaginated",
    "BulkTransactionResult",
    "Currency",
)

import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional, Set, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from .access import TransactionActiveRecord


class Currency(enum.Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"

    @classmethod
    def all_values(cls) -> Set[str]:
        return set(cls.__members__.values())


class Transaction(BaseModel):
    transaction_id: UUID
    timestamp: datetime
    amount: float = Field(gt=0)
    currency: Currency
    customer_id: UUID
    product_id: UUID
    quantity: int = Field(gt=0)

    @field_validator("timestamp")
    def validate_timestamp(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            if value.endswith("Z"):
                value = value.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(value)
            except Exception:
                raise ValueError(
                    f"Timestamp must be provided in ISO 8601 format, received: {value}"
                )

    @field_validator("currency")
    def validate_currency(cls, value: str) -> str:
        if value not in Currency.all_values():
            raise ValueError(f"Unsupported currency: {value}")

        return value

    def to_active_record(self) -> TransactionActiveRecord:
        return TransactionActiveRecord(
            transaction_id=self.transaction_id,
            timestamp=str(self.timestamp),
            amount=self.amount,
            currency=self.currency.value,
            customer_id=self.customer_id,
            product_id=self.product_id,
            quantity=self.quantity,
        )

    @classmethod
    def from_csv(cls, row: dict):
        return cls(**row)


class CustomerSummary(BaseModel):
    customer_id: UUID
    total_revenue: Decimal
    unique_products_count: int
    last_transaction_date: Optional[datetime]


class ProductSummary(BaseModel):
    product_id: UUID
    total_quantity: int
    total_revenue: Decimal
    unique_customers_count: int


class TransactionsPaginated(BaseModel):
    total_count: int
    page: int
    page_size: int
    items: List[Transaction]

    def dict(self, **kwargs):
        return {
            "_pagination": {
                "totalCount": self.total_count,
                "currentPage": self.pages_count,
                "size": self.page_size,
            },
            "items": [item for item in self.items],
        }


class BulkTransactionResult(BaseModel):
    success: int
    failure: int
