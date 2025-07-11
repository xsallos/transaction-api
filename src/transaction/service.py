import csv
import io
from typing import List, NamedTuple, Optional
from uuid import UUID

from fastapi import Depends
from pydantic import ValidationError

from src.core.logging import logger

from .errors import (
    InvalidFileStructure,
    TransactionNotFound,
    CustomerSummaryNotFound,
    ProductSummaryNotFound,
)
from .models.dto import (
    BulkTransactionResult,
    Transaction,
    TransactionsPaginated,
    CustomerSummary,
    ProductSummary,
)
from .repository import TransactionRepository, get_transaction_repository


class TransactionValidator:

    _CSV_EXPECTED_HEADERS = {
        "transaction_id",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
        "quantity",
    }

    class Result(NamedTuple):
        validated_items: List[Transaction]
        success: int
        failure: int

    def validate(self, content: bytes) -> Result:
        validated = []
        success, failure = 0, 0
        seen_ids = set()

        reader = csv.DictReader(io.StringIO(content.decode()))

        # Validate headers

        headers = set(reader.fieldnames or [])

        if headers != self._CSV_EXPECTED_HEADERS:
            raise InvalidFileStructure(
                f"Invalid CSV headers.\n"
                f"Expected: {self._CSV_EXPECTED_HEADERS}\n"
                f"Received: {headers}"
            )

        # Validate rows

        for idx, row in enumerate(reader, start=1):
            try:
                transaction = Transaction(**row)

                if transaction.transaction_id in seen_ids:
                    logger.error(
                        f"Duplicate transaction_id: {transaction.transaction_id} in row {idx}"
                    )
                    continue

                seen_ids.add(transaction.transaction_id)  # Check duplicates
                validated.append(transaction)
                success += 1

            except ValidationError as error:
                errors = [
                    error.get("msg", "Invalid content") for error in error.errors()
                ]
                logger.error(f"Invalid row content: {idx}. Reason: {errors}")
                failure += 1

        return self.Result(validated_items=validated, success=success, failure=failure)


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        validator: TransactionValidator,
    ):
        self.transaction_repository = transaction_repository
        self.validator = validator

    def get_by_id(self, transaction_id: UUID) -> Transaction:
        transaction = self.transaction_repository.get_by_id(transaction_id)

        if not transaction:
            raise TransactionNotFound

        return transaction

    def fetch_paginated(
        self,
        page: int,
        page_size: int,
        customer_id: Optional[str] = None,
        product_id: Optional[str] = None,
    ) -> TransactionsPaginated:

        return self.transaction_repository.fetch_paginated(
            page, page_size, customer_id, product_id
        )

    def create_from_csv(self, content: bytes) -> BulkTransactionResult:
        result = self.validator.validate(content=content)

        for transaction in result.validated_items:
            self.transaction_repository.create(transaction=transaction)

        self.transaction_repository.persist()

        return BulkTransactionResult(success=result.success, failure=result.failure)

    def get_customer_summary(self, customer_id: UUID) -> CustomerSummary:
        summary = self.transaction_repository.get_customer_summary(
            customer_id=customer_id
        )

        if not summary:
            raise CustomerSummaryNotFound

        return summary

    def get_product_summary(self, product_id: UUID) -> ProductSummary:
        summary = self.transaction_repository.get_product_summary(product_id=product_id)

        if not summary:
            raise ProductSummaryNotFound

        return summary


def get_transaction_service(
    transaction_repository: TransactionRepository = Depends(get_transaction_repository),
) -> TransactionService:
    return TransactionService(
        transaction_repository=transaction_repository, validator=TransactionValidator()
    )
