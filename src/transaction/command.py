import csv
import io
from typing import Dict

from pydantic import ValidationError as PydanticValidationError
from core.logging import logger
from transaction.models.dto import Transaction
from transaction.repository import TransactionRepository


class TransactionCreateCommand:
    EXPECTED_HEADERS = {
        "transaction_id",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
        "quantity",
    }

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, content: bytes) -> Dict[str, int]:
        success, failure = 0, 0

        reader = csv.DictReader(io.StringIO(content.decode()))

        headers = set(reader.fieldnames or [])
        # check duplicate transaction ids

        if headers != self.EXPECTED_HEADERS:
            raise InvalidHeaders("Invalid CSV headers")

        for idx, row in enumerate(reader, 1):
            try:
                transaction = Transaction(**row)
                self.transaction_repository.create(transaction=transaction)
                success += 1

            except (PydanticValidationError, Exception) as e:
                logger.error(msg=f"Invalid record: {idx}, {str(e)}")
                failure += 1

        self.transaction_repository.persist()

        return {"success": success, "failure": failure}
