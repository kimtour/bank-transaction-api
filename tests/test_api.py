import os
from pathlib import Path

TEST_DB = Path("test_bank.db")
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def register_and_login(username="samuel"):
    client.post("/auth/register", json={"username": username, "password": "StrongPass123"})
    response = client.post("/auth/login", json={"username": username, "password": "StrongPass123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_login_and_create_account():
    headers = register_and_login("alice")
    response = client.post("/accounts", json={"account_name": "Alice Main Account", "opening_balance": "5000.00", "currency": "KES"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["balance"] == "5000.00"
    assert response.json()["account_number"].startswith("10")


def test_deposit_and_duplicate_reference_rejected():
    headers = register_and_login("bob")
    account = client.post("/accounts", json={"account_name": "Bob", "opening_balance": 1000}, headers=headers).json()
    path = f"/accounts/{account['account_number']}/deposit"
    payload = {"amount": 500, "reference": "DEP-001"}
    first = client.post(path, json=payload, headers=headers)
    second = client.post(path, json=payload, headers=headers)
    assert first.status_code == 200
    assert second.status_code == 409


def test_insufficient_balance_rejected():
    headers = register_and_login("carol")
    account = client.post("/accounts", json={"account_name": "Carol", "opening_balance": 200}, headers=headers).json()
    response = client.post(f"/accounts/{account['account_number']}/withdraw", json={"amount": 500, "reference": "WD-001"}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_transfer_moves_funds_and_creates_history():
    headers = register_and_login("david")
    source = client.post("/accounts", json={"account_name": "Source", "opening_balance": 3000}, headers=headers).json()
    destination = client.post("/accounts", json={"account_name": "Destination", "opening_balance": 100}, headers=headers).json()
    response = client.post("/transfers", json={"source_account": source["account_number"], "destination_account": destination["account_number"], "amount": 750, "reference": "TRF-001", "description": "Test transfer"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["transaction_type"] == "TRANSFER"
    history = client.get("/transactions", headers=headers)
    assert history.status_code == 200
    assert any(tx["reference"] == "TRF-001" for tx in history.json())


def test_protected_endpoint_requires_token():
    response = client.get("/accounts")
    assert response.status_code == 401
