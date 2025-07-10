from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.database import get_session, catch_errors
from .models.access import TransactionActiveRecord
from .models.dto import (
    CustomerSummary,
    ProductSummary,
    Transaction,
    TransactionsPaginated,
)


class TransactionRepository:

    class CurrencyExchange:
        EUR = 4.3
        USD = 4.0

    def __init__(self, session: Session):
        self.session = session

    @catch_errors
    def create(self, transaction: Transaction) -> Transaction:
        model = transaction.to_active_record()

        self.session.add(model)
        self.session.flush()

        return self._from_active_record(transaction_model=model)

    def persist(self) -> None:
        self.session.commit()

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        model = (
            self.session.query(TransactionActiveRecord)
            .filter(TransactionActiveRecord.transaction_id == transaction_id)
            .first()
        )

        return self._from_active_record(model) if model else None

    def fetch_paginated(
        self,
        page: int,
        page_size: int,
        customer_id: Optional[str] = None,
        product_id: Optional[str] = None,
    ) -> TransactionsPaginated:

        query = self.session.query(TransactionActiveRecord)

        if customer_id:
            query = query.filter(TransactionActiveRecord.customer_id == customer_id)

        if product_id:
            query = query.filter(TransactionActiveRecord.product_id == product_id)

        total_count = query.count()

        models = (
            query.order_by(desc(TransactionActiveRecord.timestamp))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return TransactionsPaginated(
            total_count=total_count,
            page=page,
            page_size=page_size,
            items=[
                self._from_active_record(transaction_model=model) for model in models
            ],
        )

    def get_customer_summary(self, customer_id: UUID) -> Optional[CustomerSummary]:
        models = (
            self.session.query(TransactionActiveRecord)
            .filter(TransactionActiveRecord.customer_id == customer_id)
            .all()
        )

        if not models:
            return None

        revenue = sum(
            self._convert_to_pln(model.amount, model.currency) for model in models
        )

        products = len(set(model.product_id for model in models))

        last_transaction_date = max(model.timestamp for model in models)

        return CustomerSummary(
            customer_id=customer_id,
            total_revenue=revenue,
            unique_products_count=products,
            last_transaction_date=last_transaction_date,
        )

    def get_product_summary(self, product_id: UUID) -> Optional[ProductSummary]:
        models = (
            self.session.query(TransactionActiveRecord)
            .filter(TransactionActiveRecord.product_id == product_id)
            .all()
        )

        if not models:
            return None

        total_quantity = sum(model.quantity for model in models)

        revenue = sum(
            self._convert_to_pln(model.amount, model.currency) for model in models
        )

        customers = len(set(model.customer_id for model in models))

        return ProductSummary(
            product_id=product_id,
            total_quantity=total_quantity,
            total_revenue=revenue,
            unique_customers_count=customers,
        )

    def _from_active_record(
        self, transaction_model: TransactionActiveRecord
    ) -> Transaction:
        return Transaction(
            transaction_id=transaction_model.transaction_id,
            timestamp=transaction_model.timestamp,
            amount=transaction_model.amount,
            currency=transaction_model.currency,
            customer_id=transaction_model.customer_id,
            product_id=transaction_model.product_id,
            quantity=transaction_model.quantity,
        )

    def _convert_to_pln(self, amount: float, currency: str) -> float:
        if currency == "PLN":
            return amount
        elif currency == "EUR":
            return amount * self.CurrencyExchange.EUR
        elif currency == "USD":
            return amount * self.CurrencyExchange.USD
        else:
            return amount  # safeguard for undefined


def get_transaction_repository(
    session: Session = Depends(get_session),
) -> TransactionRepository:
    return TransactionRepository(session=session)
