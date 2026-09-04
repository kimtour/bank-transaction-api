# Interview Demo Guide

Use this page as a 3 to 5 minute walkthrough during the panel interview.

## 1. Open the repository

Start with the README and explain the goal in one sentence:

> I built a banking transaction API to demonstrate how I translate financial business rules into a secure, testable REST service with CI/CD.

## 2. Show the API surface

Run the application locally:

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and show:

- `POST /auth/register`
- `POST /auth/login`
- `POST /accounts`
- `POST /accounts/{account_number}/deposit`
- `POST /accounts/{account_number}/withdraw`
- `POST /transfers`
- `GET /transactions`
- `GET /health`

## 3. Explain the business rules

Highlight these controls:

- A transaction reference must be unique.
- A withdrawal cannot exceed the available balance.
- A transfer cannot use the same account as both source and destination.
- Transfer currencies must match.
- The source account must belong to the authenticated user.
- Protected endpoints require a JWT bearer token.

## 4. Show the architecture

Explain the flow:

```text
Client
  -> FastAPI route
  -> JWT authentication
  -> service layer
  -> SQLAlchemy ORM
  -> SQLite database
```

Explain that SQLite keeps the demo easy to run, while the database URL can be changed to PostgreSQL for production.

## 5. Show automated tests

Open `tests/test_api.py` and point out coverage for:

- health endpoint
- registration and login
- protected routes
- account creation
- duplicate transaction references
- insufficient balance
- transfers
- transaction history

Run:

```bash
pytest
```

## 6. Show CI/CD

Open the GitHub Actions tab and show the green CI workflow.

Explain:

> Every push and pull request to main runs the automated test suite. A failed test blocks confidence in the change and gives immediate feedback before deployment.

## 7. Show Docker

Point to `Dockerfile` and `.dockerignore`.

```bash
docker build -t bank-transaction-api .
docker run -p 8000:8000 --env JWT_SECRET=demo-secret bank-transaction-api
```

## Questions the panel may ask

### Why FastAPI?

FastAPI provides typed request validation, automatic OpenAPI documentation and a clean structure for Python API services.

### How would you make this production ready?

I would use PostgreSQL, Alembic migrations, a managed secrets store, structured logs, monitoring, rate limiting, stronger password-policy controls, database-level transaction isolation and row locking for concurrent balance updates.

### How do you prevent duplicate transactions?

Each transaction uses a unique reference. The service checks the reference before processing, and the database model also enforces uniqueness.

### How would you integrate this with another bank or M-Pesa?

I would introduce an integration adapter or payment service that calls the external API, stores the external transaction ID, handles callbacks or webhooks, retries transient failures safely and reconciles final transaction states.

### What happens if two transfers hit the same account at the same time?

The demo uses SQLite, so production concurrency controls are intentionally outside its scope. With PostgreSQL I would use database transactions and row-level locking, or another concurrency strategy, to prevent lost updates and double spending.

## Closing statement

> The project demonstrates the full engineering flow I would use in a banking environment: define the API contract, implement business rules, secure access, test failure cases, automate quality checks through CI/CD and package the service for deployment.
