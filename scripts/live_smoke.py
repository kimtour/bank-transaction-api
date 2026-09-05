import json
import os
import time
import urllib.error
import urllib.request
import uuid
from decimal import Decimal

BASE_URL = os.getenv("BASE_URL", "https://samuel-kimani-bank-api-demo.onrender.com").rstrip("/")


def request(method, path, payload=None, token=None, retries=8):
    url = f"{BASE_URL}{path}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"User-Agent": "bank-transaction-api-live-smoke/1.0"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_error = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                text = response.read().decode("utf-8")
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return response.status, json.loads(text)
                return response.status, text
        except urllib.error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"{method} {path} returned {exc.code}: {response_body}")
            if exc.code < 500:
                raise last_error
        except urllib.error.URLError as exc:
            last_error = exc

        if attempt < retries:
            print(f"Attempt {attempt}/{retries} failed for {path}; retrying in 10 seconds...")
            time.sleep(10)

    raise RuntimeError(f"{method} {path} failed after {retries} attempts: {last_error}")


def expect_status(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected HTTP {expected}, received {actual}")


def main():
    suffix = uuid.uuid4().hex[:10]
    username = f"smoke-{suffix}"
    password = "SmokePass123"
    reference = f"SMOKE-{suffix}"

    print(f"Testing live service: {BASE_URL}")

    status, health = request("GET", "/health")
    expect_status(status, 200, "health")
    assert health["status"] == "ok"
    assert health["service"] == "bank-transaction-api"

    status, landing = request("GET", "/")
    expect_status(status, 200, "landing page")
    assert "Bank Transaction API" in landing

    status, docs = request("GET", "/docs")
    expect_status(status, 200, "Swagger UI")
    assert "Swagger UI" in docs

    status, openapi = request("GET", "/openapi.json")
    expect_status(status, 200, "OpenAPI contract")
    required_paths = {
        "/health",
        "/auth/register",
        "/auth/login",
        "/accounts",
        "/transfers",
        "/transactions",
    }
    missing = sorted(required_paths - set(openapi["paths"]))
    assert not missing, f"Live OpenAPI contract is missing paths: {missing}"

    status, registered = request(
        "POST",
        "/auth/register",
        {"username": username, "password": password},
    )
    expect_status(status, 201, "register")
    assert registered["username"] == username

    status, login = request(
        "POST",
        "/auth/login",
        {"username": username, "password": password},
    )
    expect_status(status, 200, "login")
    token = login["access_token"]
    assert token

    status, source = request(
        "POST",
        "/accounts",
        {"account_name": "Smoke Source", "opening_balance": "5000.00", "currency": "KES"},
        token=token,
    )
    expect_status(status, 201, "create source account")

    status, destination = request(
        "POST",
        "/accounts",
        {"account_name": "Smoke Destination", "opening_balance": "1000.00", "currency": "KES"},
        token=token,
    )
    expect_status(status, 201, "create destination account")

    status, transfer = request(
        "POST",
        "/transfers",
        {
            "source_account": source["account_number"],
            "destination_account": destination["account_number"],
            "amount": "750.00",
            "reference": reference,
            "description": "Automated live smoke transfer",
        },
        token=token,
    )
    expect_status(status, 200, "transfer")
    assert transfer["reference"] == reference
    assert transfer["transaction_type"] == "TRANSFER"

    status, accounts = request("GET", "/accounts", token=token)
    expect_status(status, 200, "list accounts")
    balances = {account["account_number"]: Decimal(account["balance"]) for account in accounts}
    assert balances[source["account_number"]] == Decimal("4250.00")
    assert balances[destination["account_number"]] == Decimal("1750.00")

    status, transactions = request("GET", "/transactions", token=token)
    expect_status(status, 200, "transaction history")
    assert any(item["reference"] == reference for item in transactions)

    print("LIVE E2E SMOKE TEST PASSED")
    print(f"Registered user: {username}")
    print(f"Verified transfer reference: {reference}")
    print("Verified landing page, health, Swagger, OpenAPI, auth, accounts, transfer, balances and history.")


if __name__ == "__main__":
    main()
