# Bank Transaction API

![CI](https://github.com/kimtour/bank-transaction-api/actions/workflows/tests.yml/badge.svg)
![Live Smoke Test](https://github.com/kimtour/bank-transaction-api/actions/workflows/live-smoke.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Render](https://img.shields.io/badge/Hosted_on-Render-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A banking-focused REST API demonstrating backend engineering, API design, authentication, financial business rules, automated testing, CI/CD, Docker packaging and live cloud deployment.

## Live demo

- **Landing page:** https://samuel-kimani-bank-api-demo.onrender.com/
- **Interactive Swagger API:** https://samuel-kimani-bank-api-demo.onrender.com/docs
- **Health check:** https://samuel-kimani-bank-api-demo.onrender.com/health
- **OpenAPI contract:** https://samuel-kimani-bank-api-demo.onrender.com/openapi.json
- **GitHub Actions:** https://github.com/kimtour/bank-transaction-api/actions

The demo runs on Render's free web-service tier. A first request after inactivity can take longer while the service wakes up. SQLite is intentionally used for disposable demo data, so records can reset after a restart or redeploy.

## Documentation

- [`docs/INTERVIEW_DEMO.md`](docs/INTERVIEW_DEMO.md) - 3 to 5 minute panel walkthrough and interview talking points.
- [`docs/TECH_STACK.md`](docs/TECH_STACK.md) - explanation of FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, PyJWT, Pytest, HTTPX, GitHub Actions, Docker and Render.
- [`docs/BUILD_FROM_SCRATCH.md`](docs/BUILD_FROM_SCRATCH.md) - step-by-step setup from `git clone` through deployment.
- [`docs/HOSTING.md`](docs/HOSTING.md) - Render configuration, deployment flow and live verification.

## What this project demonstrates

- REST API engineering with FastAPI and OpenAPI
- JWT authentication and protected resources
- Relational data modelling with SQLAlchemy
- SQLite persistence for a lightweight demonstration environment
- Account creation and balance management
- Deposits, withdrawals and account-to-account transfers
- Duplicate transaction-reference protection
- Insufficient-funds, positive-amount and currency validation
- Account ownership enforcement
- Transaction history and audit-friendly references
- 11 automated API test cases with Pytest
- GitHub Actions CI on pushes and pull requests
- Live post-deployment smoke tests
- Docker image build verification
- Environment-based configuration
- Render Infrastructure as Code through `render.yaml`

## Architecture

```text
Browser / Client / Swagger UI
            |
            v
        Render Web Service
            |
          Uvicorn
            |
          FastAPI
            |
    Pydantic validation
            |
      JWT authentication
            |
       Service Layer
            |
      SQLAlchemy ORM
            |
          SQLite
```

For a production banking workload, the SQLite layer would be replaced by PostgreSQL or another managed persistent database with migrations, stronger concurrency controls and production observability.

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Obtain JWT access token |
| POST | `/accounts` | Create an account |
| GET | `/accounts` | List the authenticated user's accounts |
| GET | `/accounts/{account_number}` | Get an owned account |
| POST | `/accounts/{account_number}/deposit` | Deposit funds |
| POST | `/accounts/{account_number}/withdraw` | Withdraw funds |
| POST | `/transfers` | Transfer funds between accounts |
| GET | `/transactions` | View transaction history |

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

Open:

- Landing page: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## Quick live demo flow

### 1. Register

```bash
curl -X POST https://samuel-kimani-bank-api-demo.onrender.com/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel-demo","password":"StrongPass123"}'
```

### 2. Login

```bash
curl -X POST https://samuel-kimani-bank-api-demo.onrender.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel-demo","password":"StrongPass123"}'
```

Copy the returned token, open Swagger and use **Authorize**.

### 3. Create two KES accounts and transfer funds

```json
{
  "source_account": "1012345678",
  "destination_account": "1098765432",
  "amount": 2500,
  "reference": "TRF-DEMO-0001",
  "description": "Interview demonstration transfer"
}
```

Then use `GET /accounts` and `GET /transactions` to show the resulting balances and transaction record.

## Automated testing

Run locally:

```bash
pytest -q
```

The suite covers health checks, registration/login, protected resources, account creation, deposits, duplicate references, insufficient funds, successful transfers and balances, transaction history, invalid tokens, zero-value validation, same-account transfers, currency mismatch and account ownership.

## CI and deployment verification

### CI workflow

`.github/workflows/tests.yml`:

```text
Checkout repository
  -> Python 3.12
  -> install dependencies
  -> compile app
  -> run Pytest
  -> build Docker image
```

### Live smoke workflow

`.github/workflows/live-smoke.yml` independently checks the hosted Render service:

```text
/health
/
/docs
/openapi.json
```

The OpenAPI smoke check also confirms that core paths such as `/auth/register`, `/auth/login`, `/accounts`, `/transfers` and `/transactions` are published by the live service.

## Docker

```bash
docker build -t bank-transaction-api .
docker run -p 8000:8000 --env JWT_SECRET=demo-secret bank-transaction-api
```

## Engineering decisions

**Unique transaction references** provide idempotency protection against accidental duplicate financial instructions.

**Service-layer transaction logic** keeps financial rules separate from HTTP routing and makes testing easier.

**JWT authentication** protects account data and operations.

**Decimal financial values** reduce floating-point risks when handling money.

**Environment configuration** separates code from deployment-specific settings and secrets.

**Infrastructure as Code** keeps the Render deployment configuration version-controlled in `render.yaml`.

**Post-deployment smoke testing** verifies the public service after code changes instead of relying only on local tests.

## Production improvements

A production version would add PostgreSQL, Alembic migrations, structured audit logs, rate limiting, refresh-token strategy, managed secrets, monitoring, distributed tracing, database transaction isolation, row-level locking and integration with a core banking or payment platform.

## Interview talking points

1. Translating financial requirements into API contracts and validation rules.
2. Protecting transactions from duplicates, invalid amounts, currency mismatch and insufficient funds.
3. Securing customer resources through JWT authentication and ownership checks.
4. Testing both success paths and failure cases.
5. Moving compilation, tests and Docker verification into CI.
6. Defining deployment with version-controlled Infrastructure as Code.
7. Verifying the public deployment with an independent live smoke workflow.
8. Extending the service to M-Pesa, core banking systems or other payment channels.

## Author

Samuel Mutua Kimani
