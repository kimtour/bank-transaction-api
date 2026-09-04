# Bank Transaction API

![CI](https://github.com/kimtour/bank-transaction-api/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A production-style REST API for account management and financial transactions, built to demonstrate backend engineering, API design, security, automated testing and CI/CD practices relevant to banking systems.

## Free online demo deployment

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kimtour/bank-transaction-api)

The repository includes `render.yaml` for a free Render Web Service. The configured service name is `samuel-kimani-bank-api-demo`.

After the first Render deployment, open the service URL and append:

- `/` for the project landing page
- `/docs` for the interactive Swagger API demo
- `/health` for the health check

Render's free web services can spin down after inactivity, so the first request after an idle period may take longer. The demo uses SQLite for simplicity, so data is intentionally disposable and can reset when the free service restarts. See [`docs/HOSTING.md`](docs/HOSTING.md) for the exact deployment steps and interview checklist.

## Interview demo

Open [`docs/INTERVIEW_DEMO.md`](docs/INTERVIEW_DEMO.md) for a focused 3 to 5 minute panel walkthrough, technical talking points and likely interview questions.

## What this project demonstrates

- REST API engineering with FastAPI and OpenAPI
- JWT-based authentication and protected resources
- Relational data modelling with SQLAlchemy
- Account creation and balance management
- Deposits, withdrawals and account-to-account transfers
- Duplicate transaction reference protection
- Insufficient-funds and currency validation
- Transaction history and audit-friendly references
- Automated API tests with Pytest
- GitHub Actions CI on every push and pull request
- Docker packaging for repeatable deployment
- Environment-based configuration
- Free cloud deployment with Render Infrastructure as Code

## Architecture

```text
Browser / Client / Swagger UI
            |
            v
        Render Web Service
            |
          FastAPI
            |
       Authentication
            |
            v
       Service Layer
            |
            v
      SQLAlchemy ORM
            |
            v
          SQLite
```

SQLite keeps the demo easy to run locally and online. The database layer can be switched to PostgreSQL through `DATABASE_URL` without changing the API contract.

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Obtain JWT access token |
| POST | `/accounts` | Create an account |
| GET | `/accounts` | List authenticated user's accounts |
| GET | `/accounts/{account_number}` | Get account details |
| POST | `/accounts/{account_number}/deposit` | Deposit funds |
| POST | `/accounts/{account_number}/withdraw` | Withdraw funds |
| POST | `/transfers` | Transfer funds between accounts |
| GET | `/transactions` | View transaction history |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

- Demo landing page: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## Quick demo flow

### 1. Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel","password":"StrongPass123"}'
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel","password":"StrongPass123"}'
```

Copy the returned access token and use Swagger's **Authorize** button.

### 3. Create accounts and transfer funds

Create two KES accounts, then use `/transfers` to move funds between them.

```json
{
  "source_account": "1012345678",
  "destination_account": "1098765432",
  "amount": 2500,
  "reference": "TRF-2026-0001",
  "description": "Supplier payment"
}
```

## Automated testing

```bash
pytest
```

Tests cover health checks, registration and login, protected endpoint authentication, account creation, deposits, duplicate references, insufficient balance handling, transfers and transaction history.

## CI/CD

`.github/workflows/tests.yml` runs the automated test suite on every push and pull request to `main`. The CI badge at the top of this README reflects the current workflow status.

The Render blueprint uses `autoDeployTrigger: checksPass`, so cloud deployments can follow successful CI checks.

## Docker

```bash
docker build -t bank-transaction-api .
docker run -p 8000:8000 --env JWT_SECRET=demo-secret bank-transaction-api
```

## Engineering decisions

**Unique transaction references** provide idempotency protection against accidental duplicate financial instructions.

**Service-layer transaction logic** keeps business rules separate from HTTP routing and makes testing easier.

**JWT authentication** restricts account data to authenticated users.

**Decimal financial values** reduce the risk of floating-point errors in money calculations.

**Environment configuration** separates application code from deployment settings and secrets.

**Infrastructure as Code** keeps the free cloud deployment configuration version-controlled in `render.yaml`.

## Production improvements

A production deployment would add PostgreSQL, Alembic migrations, structured audit logs, rate limiting, refresh tokens, secret management, observability, distributed tracing, database transaction isolation, row locking and integration with a core banking or payment system.

## Interview talking points

1. Translating financial business requirements into API contracts and validation rules.
2. Protecting financial operations from duplicate instructions and insufficient funds.
3. Securing customer resources with authentication and ownership checks.
4. Reducing regression risk through automated API tests.
5. Moving quality checks into CI/CD with GitHub Actions.
6. Deploying safely after CI checks using version-controlled cloud configuration.
7. Extending the service to M-Pesa, core banking systems or other payment channels.

## Author

Samuel Mutua Kimani
