import pytest

from src.transaction.errors import InvalidFileStructure
from src.transaction.service import TransactionValidator
from tests.generators import (
    generate_csv,
    invalid_data,
    invalid_headers,
    valid_data,
    valid_headers,
)


class TestTransactionValidator:

    validator = TransactionValidator()

    def test_validate_with_valid_data_returns_success(self):
        csv_content, _, _ = generate_csv(valid_headers(), valid_data())

        result = self.validator.validate(content=csv_content)

        assert result.success == 2
        assert result.failure == 0
        assert len(result.validated_items) == 2

    def test_validate_with_invalid_headers_raises_error(self):
        csv_content, _, _ = generate_csv(invalid_headers())

        with pytest.raises(InvalidFileStructure):
            self.validator.validate(csv_content)

    def test_validate_with_invalid_data_returns_multistatus(self):
        csv_content, _, _ = generate_csv(valid_headers(), invalid_data())
        result = self.validator.validate(content=csv_content)

        assert result.success == 1
        assert result.failure == 7
