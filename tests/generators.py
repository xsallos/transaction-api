__all__ = (
    "valid_headers",
    "invalid_headers",
    "valid_data",
    "invalid_data",
    "generate_csv",
)

import csv
import io
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4


def valid_headers() -> List[str]:
    return [
        "transaction_id",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
        "quantity",
    ]


def invalid_headers() -> List[str]:
    return [
        "invalid",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
    ]


def valid_data() -> List[Dict[str, Any]]:
    return [
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-01T10:00:00",
            "amount": "100.50",
            "currency": "USD",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 3,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": "75.25",
            "currency": "EUR",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 2,
        },
    ]


def invalid_data() -> List[Dict[str, Any]]:
    return [
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-01T10:00:00",
            "amount": 100.50,
            "currency": "USD",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 2,
        },
        {
            "transaction_id": "123",
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": 75.25,
            "currency": "EUR",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "02-13-2024",
            "amount": 75.25,
            "currency": "EUR",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": -1,
            "currency": "EUR",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": 100.25,
            "currency": "GBP",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": 100.25,
            "currency": "PLN",
            "customer_id": 123,
            "product_id": str(uuid4()),
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": 100.25,
            "currency": "PLN",
            "customer_id": str(uuid4()),
            "product_id": -1,
            "quantity": 1,
        },
        {
            "transaction_id": str(uuid4()),
            "timestamp": "2024-01-02T11:00:00Z",
            "amount": 100.25,
            "currency": "PLN",
            "customer_id": str(uuid4()),
            "product_id": str(uuid4()),
            "quantity": -1,
        },
    ]


def generate_csv(headers: List[str], data: Optional[List[Dict]] = None):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()

    if data:
        writer.writerows(data)

    return output.getvalue().encode(), data, headers
