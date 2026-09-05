# Portfolio Demo Guide

Use this as a focused 3 to 5 minute walkthrough of the full-stack banking application.

## 1. Open the live banking dashboard

https://samuel-kimani-bank-api-demo.onrender.com/

Opening line:

> I built a full-stack banking transaction system. The browser dashboard is connected to a secure FastAPI REST API with JWT authentication, financial validation, automated CI/CD and live post-deployment testing.

Point out that this is a working application rather than a static mock. Registration, account creation and transfers all call the live FastAPI backend.

## 2. Register and log in

Use the dashboard to create a temporary user and log in.

Explain:

> Login returns a JWT access token. The browser uses that token in the Authorization header for protected account and transaction requests.

## 3. Create two KES accounts

Click **Create account** twice, for example:

```text
Samuel Current Account   KES 50,000
Samuel Savings Account   KES 10,000
```

Show that the dashboard updates the total KES balance and account count from API data.

## 4. Run a live transaction

Use the dashboard to:

1. Deposit money into an account.
2. Withdraw a valid amount.
3. Transfer KES 5,000 between the two accounts.
4. Show the updated balances.
5. Show the new transaction records in Recent Transactions.

Then demonstrate one validation rule, such as an excessive withdrawal or transfer.

Explain:

> The browser contains presentation logic, but the banking business rules remain in the backend service layer. The API decides whether a financial operation is valid.

## 5. Open Swagger and show the API underneath

https://samuel-kimani-bank-api-demo.onrender.com/docs

Point out:

- `POST /auth/register`
- `POST /auth/login`
- `POST /accounts`
- `GET /accounts`
- `GET /accounts/{account_number}`
- `POST /accounts/{account_number}/deposit`
- `POST /accounts/{account_number}/withdraw`
- `POST /transfers`
- `GET /transactions`
- `GET /health`

The same backend can serve both the browser dashboard and other API consumers.

## 6. Explain the business rules

Highlight these controls:

- Transaction references must be unique.
- Deposits, withdrawals and transfers must use positive amounts.
- Withdrawals and transfers cannot exceed the available balance.
- Source and destination accounts must differ.
- Transfer currencies must match.
- Account lookup is restricted to the authenticated owner.
- Protected endpoints require a valid JWT bearer token.

## 7. Show the architecture

```text
Browser
  -> HTML / CSS / JavaScript dashboard
  -> Render Web Service
  -> Uvicorn
  -> FastAPI route
  -> Pydantic validation
  -> JWT authentication
  -> service-layer banking rules
  -> SQLAlchemy ORM
  -> SQLite demo database
```

The frontend is intentionally lightweight and same-origin. It consumes the REST API without duplicating banking rules.

SQLite keeps the portfolio demo lightweight. A production environment would use PostgreSQL or another managed persistent database.

## 8. Show automated tests

Open `tests/test_api.py`.

The automated suite covers:

- dashboard HTML, CSS and JavaScript delivery
- walkthrough delivery
- health endpoint
- registration and login
- authenticated account creation
- deposits
- duplicate transaction references
- insufficient balance
- transfers and resulting balances
- transaction history
- missing authentication
- invalid JWT tokens
- zero-value request validation
- same-account transfer rejection
- currency mismatch rejection
- account ownership enforcement

Run locally with:

```bash
pytest -q
```

## 9. Show CI/CD

Open:

https://github.com/kimtour/bank-transaction-api/actions

There are two important workflows.

### CI

`.github/workflows/tests.yml`:

- checks out the repository
- installs Python 3.12
- installs dependencies
- compiles the application
- runs Pytest
- builds the Docker image

### Live Smoke Test

`.github/workflows/live-smoke.yml` runs `scripts/live_smoke.py` against the actual Render service.

It verifies:

```text
live dashboard HTML/CSS/JavaScript
  -> health, Swagger and OpenAPI
  -> register a temporary user
  -> log in and obtain JWT
  -> create two KES accounts
  -> transfer KES 750
  -> verify both balances
  -> verify transaction history
```

This provides post-deployment verification, not only local testing.

## 10. Show deployment configuration

Open `render.yaml` and explain:

> The deployment is defined as Infrastructure as Code. Render uses the file to select Python 3.12, install dependencies, start Uvicorn, configure environment variables and check the health endpoint.

## Technical discussion prompts

### Why add a frontend if the project is API-focused?

The dashboard proves that the REST API is usable by a real client. The frontend stays thin so financial validation remains in the backend service layer.

### Why FastAPI?

FastAPI provides typed request validation, automatic OpenAPI documentation, strong Python developer ergonomics and a clean structure for REST APIs.

### Why Pydantic?

Pydantic rejects invalid request data before it reaches banking business logic, for example zero or negative monetary amounts.

### Why SQLAlchemy?

SQLAlchemy separates Python application code from database-specific SQL and provides an ORM layer that can move from SQLite to PostgreSQL with limited application-level change.

### How are duplicate transactions prevented?

Each transaction has a unique reference. The service checks it before processing and the database also enforces uniqueness.

### What happens if two transfers hit the same account simultaneously?

The demo uses SQLite and is not designed for high-concurrency banking workloads. A production system would use database transactions, appropriate isolation, row-level locking or another concurrency-control strategy to prevent lost updates and double spending.

### How could M-Pesa or another bank be integrated?

Add an integration adapter or payment service that calls the external API, stores provider transaction IDs, handles callbacks or webhooks, retries transient failures safely and reconciles final states.

## Closing statement

> This project demonstrates the full engineering flow: build a user-facing client, define the API contract, validate input, implement financial rules, secure access, test success and failure cases, automate CI, package and deploy the application, then verify the live transaction flow end to end.

## Supporting documentation

- [`TECH_STACK.md`](TECH_STACK.md)
- [`BUILD_FROM_SCRATCH.md`](BUILD_FROM_SCRATCH.md)
- [`HOSTING.md`](HOSTING.md)
- [`../scripts/live_smoke.py`](../scripts/live_smoke.py)
