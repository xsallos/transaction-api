__all__ = ("TransactionActiveRecord",)

from sqlalchemy import Column, UUID, Float, Integer, String

from src.core.database import Base


class TransactionActiveRecord(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID, primary_key=True)  # Natural key

    timestamp = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    #  Candidate for extraction in normalization process
    customer_id = Column(UUID, nullable=False, index=True)
    product_id = Column(UUID, nullable=False, index=True)
