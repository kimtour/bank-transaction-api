# Bank Transaction API

A production-style REST API for account management and financial transactions, built to demonstrate backend engineering, API design, security, automated testing and CI/CD practices relevant to banking systems.

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

## Architecture

```text
Client / Swagger UI
        |
        v
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

The SQLite database keeps the demo easy to run locally. The database layer can be switched to PostgreSQL through `DATABASE_URL` without changing the API contract.

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

### 3. Create accounts

Create two KES accounts, then use `/transfers` to move funds between them.

Example transfer request:

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
pytest -q
```

Tests cover:

- Health checks
- Registration and login
- Protected endpoint authentication
- Account creation
- Deposits
- Duplicate references
- Insufficient balance handling
- Transfers and transaction history

## CI/CD

`.github/workflows/tests.yml` runs the automated test suite on every push and pull request to `main`.

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

## Production improvements

A production deployment would add PostgreSQL, database migrations with Alembic, structured audit logs, rate limiting, refresh tokens, secret management, observability, distributed tracing, transactional row locking and integration with a core banking or payment system.

## Interview talking points

This project can be used to discuss:

1. How business requirements become API contracts and validation rules.
2. How financial operations protect against duplicate instructions and insufficient funds.
3. How authentication and authorization protect customer data.
4. How automated tests reduce regression risk.
5. How GitHub Actions moves quality checks into CI/CD.
6. How the same service could integrate with M-Pesa, a core banking platform or another payment channel.

## Author

Samuel Mutua Kimani
