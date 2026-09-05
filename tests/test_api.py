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
    assert response.json()["service"] == "bank-transaction-api"


def test_register_login_and_create_account():
    headers = register_and_login("alice")
    response = client.post(
        "/accounts",
        json={"account_name": "Alice Main Account", "opening_balance": "5000.00", "currency": "KES"},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["balance"] == "5000.00"
    assert response.json()["currency"] == "KES"
    assert response.json()["account_number"].startswith("10")


def test_deposit_and_duplicate_reference_rejected():
    headers = register_and_login("bob")
    account = client.post(
        "/accounts",
        json={"account_name": "Bob", "opening_balance": 1000},
        headers=headers,
    ).json()
    path = f"/accounts/{account['account_number']}/deposit"
    payload = {"amount": 500, "reference": "DEP-001"}
    first = client.post(path, json=payload, headers=headers)
    second = client.post(path, json=payload, headers=headers)
    assert first.status_code == 200
    assert second.status_code == 409
    assert second.json()["detail"] == "Transaction reference already exists"


def test_insufficient_balance_rejected():
    headers = register_and_login("carol")
    account = client.post(
        "/accounts",
        json={"account_name": "Carol", "opening_balance": 200},
        headers=headers,
    ).json()
    response = client.post(
        f"/accounts/{account['account_number']}/withdraw",
        json={"amount": 500, "reference": "WD-001"},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_transfer_moves_funds_and_creates_history():
    headers = register_and_login("david")
    source = client.post(
        "/accounts",
        json={"account_name": "Source", "opening_balance": 3000},
        headers=headers,
    ).json()
    destination = client.post(
        "/accounts",
        json={"account_name": "Destination", "opening_balance": 100},
        headers=headers,
    ).json()
    response = client.post(
        "/transfers",
        json={
            "source_account": source["account_number"],
            "destination_account": destination["account_number"],
            "amount": 750,
            "reference": "TRF-001",
            "description": "Test transfer",
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["transaction_type"] == "TRANSFER"

    accounts = client.get("/accounts", headers=headers).json()
    balances = {item["account_number"]: item["balance"] for item in accounts}
    assert balances[source["account_number"]] == "2250.00"
    assert balances[destination["account_number"]] == "850.00"

    history = client.get("/transactions", headers=headers)
    assert history.status_code == 200
    assert any(tx["reference"] == "TRF-001" for tx in history.json())


def test_protected_endpoint_requires_token():
    response = client.get("/accounts")
    assert response.status_code == 401


def test_invalid_token_rejected():
    response = client.get("/accounts", headers={"Authorization": "Bearer not-a-valid-token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_zero_amount_is_rejected_by_validation():
    headers = register_and_login("erin")
    account = client.post(
        "/accounts",
        json={"account_name": "Erin", "opening_balance": 1000},
        headers=headers,
    ).json()
    response = client.post(
        f"/accounts/{account['account_number']}/deposit",
        json={"amount": 0, "reference": "DEP-ZERO"},
        headers=headers,
    )
    assert response.status_code == 422


def test_same_account_transfer_rejected():
    headers = register_and_login("frank")
    account = client.post(
        "/accounts",
        json={"account_name": "Frank", "opening_balance": 1000, "currency": "KES"},
        headers=headers,
    ).json()
    response = client.post(
        "/transfers",
        json={
            "source_account": account["account_number"],
            "destination_account": account["account_number"],
            "amount": 100,
            "reference": "TRF-SAME",
        },
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Source and destination accounts must differ"


def test_currency_mismatch_rejected():
    headers = register_and_login("grace")
    kes_account = client.post(
        "/accounts",
        json={"account_name": "Grace KES", "opening_balance": 1000, "currency": "KES"},
        headers=headers,
    ).json()
    usd_account = client.post(
        "/accounts",
        json={"account_name": "Grace USD", "opening_balance": 100, "currency": "USD"},
        headers=headers,
    ).json()
    response = client.post(
        "/transfers",
        json={
            "source_account": kes_account["account_number"],
            "destination_account": usd_account["account_number"],
            "amount": 100,
            "reference": "TRF-CURRENCY",
        },
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Currency mismatch"


def test_account_ownership_is_enforced():
    owner_headers = register_and_login("henry")
    outsider_headers = register_and_login("irene")
    account = client.post(
        "/accounts",
        json={"account_name": "Henry Private", "opening_balance": 1000},
        headers=owner_headers,
    ).json()
    response = client.get(f"/accounts/{account['account_number']}", headers=outsider_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"
