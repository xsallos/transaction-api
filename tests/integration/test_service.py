from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import text

from src.transaction.errors import (
    CustomerSummaryNotFound,
    ProductSummaryNotFound,
    TransactionNotFound,
)
from src.transaction.repository import TransactionRepository
from src.transaction.service import TransactionService, TransactionValidator
from tests.generators import (
    generate_csv,
    generate_transaction,
    valid_data,
    valid_headers,
)


@pytest.fixture
def repository(db_session) -> TransactionRepository:
    return TransactionRepository(session=db_session)


@pytest.fixture
def service(repository) -> TransactionService:
    return TransactionService(
        transaction_repository=repository, validator=TransactionValidator()
    )


@pytest.fixture(autouse=True)
def truncate_table(db_session):
    db_session.execute(text("TRUNCATE TABLE transactions RESTART IDENTITY CASCADE"))
    db_session.commit()


def test_create_from_csv_returns_bulk_transaction_results(service):
    csv_content = generate_csv(valid_headers(), valid_data())

    result = service.create_from_csv(content=csv_content)

    assert result.success == 2
    assert result.failure == 0


def test_get_transaction_by_id_returns_transaction(repository, service):
    transaction = repository.create(transaction=generate_transaction())

    result = service.get_by_id(transaction_id=transaction.transaction_id)
    assert result


def test_get_transaction_by_id_raises_resource_not_found(service):
    with pytest.raises(TransactionNotFound):
        service.get_by_id(transaction_id=uuid4())


def test_get_customer_summary_returns_summary(repository, service):
    customer_id = uuid4()

    for i in range(5):
        repository.create(
            transaction=generate_transaction(customer_id=customer_id, amount=20.00)
        )

    result = service.get_customer_summary(customer_id=customer_id)

    assert result
    assert result.unique_products_count == 5
    assert result.total_revenue == Decimal(400.00)  # USD


def test_get_customer_summary_raises_resource_not_found(service):
    with pytest.raises(CustomerSummaryNotFound):
        service.get_customer_summary(customer_id=uuid4())


def test_get_product_summary_returns_summary(repository, service):
    product_id = uuid4()

    for i in range(5):
        repository.create(
            transaction=generate_transaction(product_id=product_id, amount=20.00)
        )

    result = service.get_product_summary(product_id=product_id)

    assert result
    assert result.total_quantity > 1
    assert result.total_revenue == Decimal(400.00)  # USD
    assert result.unique_customers_count == 5


def test_get_product_summary_raises_resource_not_found(service):
    with pytest.raises(ProductSummaryNotFound):
        service.get_product_summary(product_id=uuid4())


def test_paginate_returns_transactions(truncate_table, repository, service):
    transaction = repository.create(transaction=generate_transaction())
    transaction_other = repository.create(transaction=generate_transaction())

    page = 1
    page_size = 10

    paginated = service.fetch_paginated(page=page, page_size=page_size)
    assert len(paginated.items) == 2

    paginated = service.fetch_paginated(
        page=page, page_size=page_size, customer_id=transaction.customer_id
    )
    assert len(paginated.items) == 1

    paginated = service.fetch_paginated(
        page=page, page_size=page_size, product_id=transaction_other.product_id
    )
    assert len(paginated.items) == 1
