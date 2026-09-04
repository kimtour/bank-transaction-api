# Interview Demo Guide

Use this page as a 3 to 5 minute walkthrough during the panel interview.

## 1. Open the repository

Start with the README and explain the goal in one sentence:

> I built a banking transaction API to demonstrate how I translate financial business rules into a secure, testable REST service with CI/CD and cloud deployment.

## 2. Open the live API

Use the hosted Swagger interface:

https://samuel-kimani-bank-api-demo.onrender.com/docs

Also keep these open:

- Landing page: https://samuel-kimani-bank-api-demo.onrender.com/
- Health check: https://samuel-kimani-bank-api-demo.onrender.com/health

Show these endpoints:

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
Browser / Client
  -> Render Web Service
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

## 6. Show CI/CD

Open the GitHub Actions tab and show the green CI workflow.

Explain:

> Every push and pull request to main runs the automated test suite. Render is configured to deploy after successful checks, so the same repository demonstrates development, testing and deployment in one flow.

## 7. Show Docker and Infrastructure as Code

Point to:

- `Dockerfile`
- `.dockerignore`
- `render.yaml`

Explain that `render.yaml` keeps the cloud service configuration version-controlled.

## Live demo sequence

1. Open `/health`.
2. Open `/docs`.
3. Register a new user.
4. Log in.
5. Copy the JWT token and click **Authorize**.
6. Create two KES accounts.
7. Transfer KES 5,000 between them.
8. Open `GET /accounts` and show the changed balances.
9. Open `GET /transactions` and show the transfer record.
10. Try a transfer that exceeds the available balance and show the validation error.

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

> The project demonstrates the full engineering flow I would use in a banking environment: define the API contract, implement business rules, secure access, test failure cases, automate quality checks through CI/CD and deploy the service to the cloud.
