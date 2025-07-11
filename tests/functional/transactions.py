"""Example"""


def test_fetch_transactions(client):
    response = client.get(f"/transactions?page=1&size=10")
    assert response.status_code == 200
