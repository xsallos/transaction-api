"""Example"""

from uuid import uuid4


def test_fetch_transactions_returns_200_on_success(client):
    response = client.get(f"/transactions?page=1&size=10")
    assert response.status_code == 200


def test_get_transaction_details_not_found_returns_404(client):
    fake_id = str(uuid4())
    response = client.get(f"/transactions/{fake_id}")
    assert response.status_code == 404
