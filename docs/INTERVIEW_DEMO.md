# Interview Demo Guide

Use this as a focused 3 to 5 minute walkthrough.

## 1. Open the live Swagger API

https://samuel-kimani-bank-api-demo.onrender.com/docs

Opening line:

> I built a banking transaction API that translates financial business rules into a secure, testable REST service with automated CI/CD and a live cloud deployment.

## 2. Show the health endpoint

Open:

https://samuel-kimani-bank-api-demo.onrender.com/health

Expected response:

```json
{
  "status": "ok",
  "service": "bank-transaction-api",
  "version": "1.0.0"
}
```

Explain that Render also uses `/health` to determine whether the service started correctly.

## 3. Show the API surface

In Swagger, point out:

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

## 4. Run a live transaction flow

1. Register a new demo user.
2. Log in and copy the returned JWT access token.
3. Click **Authorize** in Swagger and paste the token.
4. Create two KES accounts.
5. Transfer KES 5,000 between them.
6. List accounts to show the new balances.
7. Open transaction history to show the recorded transfer.
8. Attempt an excessive transfer and show the `Insufficient balance` validation.
9. Reuse a transaction reference and show duplicate-reference protection.

## 5. Explain the business rules

Highlight these controls:

- Transaction references must be unique.
- Deposits and transfers must use positive amounts.
- Withdrawals and transfers cannot exceed the available balance.
- Source and destination accounts must differ.
- Transfer currencies must match.
- Account lookup is restricted to the authenticated owner.
- Protected endpoints require a valid JWT bearer token.

## 6. Show the architecture

```text
Browser / Swagger
  -> Render Web Service
  -> Uvicorn
  -> FastAPI route
  -> Pydantic validation
  -> JWT authentication
  -> service-layer business rules
  -> SQLAlchemy ORM
  -> SQLite demo database
```

Explain that SQLite keeps the demo lightweight. A production environment would use PostgreSQL or another managed persistent database.

## 7. Show automated tests

Open `tests/test_api.py`.

The current suite covers:

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

## 8. Show CI/CD

Open:

https://github.com/kimtour/bank-transaction-api/actions

There are two important workflows:

### CI

`.github/workflows/tests.yml`:

- checks out the repository
- installs Python 3.12
- installs dependencies
- compiles the application
- runs Pytest
- builds the Docker image

### Live Smoke Test

`.github/workflows/live-smoke.yml` verifies the deployed Render service by checking:

- `/health`
- `/`
- `/docs`
- `/openapi.json`

This demonstrates both application testing and post-deployment verification.

## 9. Show deployment configuration

Open `render.yaml` and explain:

> The deployment is defined as Infrastructure as Code. Render uses the file to select Python 3.12, install dependencies, start Uvicorn, configure environment variables and check the health endpoint.

## Likely panel questions

### Why FastAPI?

FastAPI gives typed request validation, automatic OpenAPI documentation, strong Python developer ergonomics and a clean structure for REST APIs.

### Why Pydantic?

Pydantic rejects invalid request data before it reaches the banking business logic, for example zero or negative monetary amounts.

### Why SQLAlchemy?

SQLAlchemy separates Python application code from database-specific SQL and provides an ORM layer that can move from SQLite to PostgreSQL with limited application-level change.

### How do you prevent duplicate transactions?

Each transaction has a unique reference. The service checks it before processing and the database also enforces uniqueness.

### What happens if two transfers hit the same account simultaneously?

The demo uses SQLite and is not designed for high-concurrency banking workloads. In production I would use database transactions, appropriate isolation and row-level locking or another concurrency-control strategy to prevent lost updates and double spending.

### How would you integrate M-Pesa or another bank?

I would add an integration adapter or payment service that calls the external API, stores provider transaction IDs, handles callbacks/webhooks, retries transient failures safely and reconciles final states.

## Closing statement

> The project demonstrates the full engineering flow I would use in a banking environment: define the API contract, validate input, implement financial rules, secure access, test success and failure cases, automate CI, package the service and verify the live deployment.

## Supporting documentation

- [`TECH_STACK.md`](TECH_STACK.md)
- [`BUILD_FROM_SCRATCH.md`](BUILD_FROM_SCRATCH.md)
- [`HOSTING.md`](HOSTING.md)
