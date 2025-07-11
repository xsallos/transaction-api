from src.core.errors import (
    ErrorCode,
    ResourceNotFound,
    ValidationError,
)


class TransactionNotFound(ResourceNotFound):
    INTERNAL_CODE = ErrorCode.RESOURCE_NOT_FOUND
    DEFAULT_MESSAGE = "Transaction does not exists"


class UnsupportedTransactionFormat(ValidationError):
    INTERNAL_CODE = ErrorCode.VALIDATION_ERROR
    DEFAULT_MESSAGE = "Unsupported transaction input format"


class InvalidFileStructure(ValidationError):
    INTERNAL_CODE = ErrorCode.VALIDATION_ERROR
    DEFAULT_MESSAGE = "Invalid file structure"


class CustomerSummaryNotFound(ResourceNotFound):
    INTERNAL_CODE = ErrorCode.RESOURCE_NOT_FOUND
    DEFAULT_MESSAGE = "Customer summary does not exists"


class ProductSummaryNotFound(ResourceNotFound):
    INTERNAL_CODE = ErrorCode.RESOURCE_NOT_FOUND
    DEFAULT_MESSAGE = "Product summary does not exists"
