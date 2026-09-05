# Bank Transaction System

![CI](https://github.com/kimtour/bank-transaction-api/actions/workflows/tests.yml/badge.svg)
![Live Smoke Test](https://github.com/kimtour/bank-transaction-api/actions/workflows/live-smoke.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Render](https://img.shields.io/badge/Hosted_on-Render-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A full-stack banking portfolio application demonstrating backend engineering, REST API design, JWT authentication, financial business rules, a responsive browser dashboard, automated testing, CI/CD, Docker packaging and live cloud deployment.

## Live application

- **Live banking dashboard:** https://samuel-kimani-bank-api-demo.onrender.com/
- **Interactive Swagger API:** https://samuel-kimani-bank-api-demo.onrender.com/docs
- **Health check:** https://samuel-kimani-bank-api-demo.onrender.com/health
- **OpenAPI contract:** https://samuel-kimani-bank-api-demo.onrender.com/openapi.json
- **GitHub Actions:** https://github.com/kimtour/bank-transaction-api/actions

The dashboard is a real client of the same FastAPI backend. Register or log in, create accounts, deposit or withdraw funds, transfer between accounts and inspect transaction history directly in the browser.

The demo runs on Render's free web-service tier. A first request after inactivity can take longer while the service wakes up. SQLite is intentionally used for disposable portfolio data, so records can reset after a restart or redeploy.

## Dashboard features

- Register and log in through the live JWT authentication API
- Session token stored in the browser for the demo session
- Account overview and KES balance summary
- Create KES, USD or EUR accounts
- Deposit and withdraw funds
- Transfer funds between accounts
- Recent transaction history and status badges
- Live API health indicator
- Responsive desktop and mobile layout
- Direct links to Swagger documentation and GitHub

## Documentation

- [`docs/INTERVIEW_DEMO.md`](docs/INTERVIEW_DEMO.md) - focused panel walkthrough and interview talking points.
- [`docs/TECH_STACK.md`](docs/TECH_STACK.md) - explanation of the frontend, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, PyJWT, Pytest, HTTPX, GitHub Actions, Docker and Render.
- [`docs/BUILD_FROM_SCRATCH.md`](docs/BUILD_FROM_SCRATCH.md) - step-by-step setup from `git clone` through deployment.
- [`docs/HOSTING.md`](docs/HOSTING.md) - Render configuration, deployment flow and live verification.
- [`scripts/live_smoke.py`](scripts/live_smoke.py) - automated end-to-end verification against the public Render service.

## What this project demonstrates

- Full-stack application design with HTML, CSS, JavaScript and FastAPI
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
- Automated API and dashboard tests with Pytest
- GitHub Actions CI on pushes and pull requests
- Full live authenticated post-deployment verification
- Docker image build verification
- Environment-based configuration
- Render Infrastructure as Code through `render.yaml`

## Architecture

```text
Browser
  |
  v
HTML + CSS + JavaScript dashboard
  |
  v
Render Web Service
  |
  v
Uvicorn
  |
  v
FastAPI REST API
  |
  +--> Pydantic request validation
  |
  +--> JWT authentication
  |
  v
Service layer / financial rules
  |
  v
SQLAlchemy ORM
  |
  v
SQLite
```

The frontend and API are deployed together from one repository and one Render web service. The dashboard calls the live API through same-origin requests, while `/docs` remains available for direct API demonstrations.

For a production banking workload, the SQLite layer would be replaced by PostgreSQL or another managed persistent database with migrations, stronger concurrency controls and production observability.

## Project structure

```text
bank-transaction-api/
|
|-- app/
|   |-- main.py              # FastAPI routes and dashboard hosting
|   |-- database.py          # SQLAlchemy engine and sessions
|   |-- models.py            # Database tables
|   |-- schemas.py           # Pydantic request and response models
|   |-- security.py          # Password hashing and JWT authentication
|   |-- services.py          # Banking business rules
|   `-- static/
|       |-- index.html       # Live dashboard structure
|       |-- styles.css       # Responsive banking UI
|       `-- app.js           # Browser-to-API integration
|
|-- tests/test_api.py        # API and dashboard tests
|-- scripts/live_smoke.py    # Hosted end-to-end verification
|-- .github/workflows/       # CI and live smoke workflows
|-- Dockerfile               # Container build
|-- render.yaml              # Render Infrastructure as Code
|-- requirements.txt         # Python dependencies
`-- README.md
```

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Live banking dashboard |
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

- Dashboard: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## Fast live demo flow

The easiest portfolio demonstration is now through the dashboard:

```text
Open live dashboard
  -> Register a user
  -> Create two KES accounts
  -> Deposit or withdraw funds
  -> Transfer between the accounts
  -> Show the updated balances
  -> Show recent transaction history
  -> Open /docs to demonstrate the underlying REST API
  -> Open GitHub Actions to show CI and live verification
```

You can still demonstrate the API directly through Swagger or curl.

### Register

```bash
curl -X POST https://samuel-kimani-bank-api-demo.onrender.com/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel-demo","password":"StrongPass123"}'
```

### Login

```bash
curl -X POST https://samuel-kimani-bank-api-demo.onrender.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"samuel-demo","password":"StrongPass123"}'
```

## Automated testing

Run locally:

```bash
pytest -q
```

The suite covers dashboard/static assets, health checks, registration/login, protected resources, account creation, deposits, duplicate references, insufficient funds, successful transfers and balances, transaction history, invalid tokens, zero-value validation, same-account transfers, currency mismatch and account ownership.

## CI and deployment verification

### CI workflow

`.github/workflows/tests.yml` performs:

```text
Checkout repository
  -> Python 3.12
  -> install dependencies
  -> compile application
  -> run Pytest
  -> build Docker image
```

### Live end-to-end smoke workflow

`.github/workflows/live-smoke.yml` runs `scripts/live_smoke.py` against the public Render deployment. It verifies:

```text
Dashboard HTML, CSS and JavaScript
  -> /health
  -> Swagger and OpenAPI contract
  -> register a unique temporary user
  -> login and obtain JWT
  -> create two KES accounts
  -> transfer KES 750
  -> verify resulting balances
  -> verify transaction history
```

This proves not only that the site is reachable, but that the deployed frontend assets, authentication, database writes and core banking transfer flow work.

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

**Same-origin frontend integration** keeps the portfolio deployment simple while still demonstrating a real browser client consuming protected APIs.

**Environment configuration** separates code from deployment-specific settings and secrets.

**Infrastructure as Code** keeps the Render deployment configuration version-controlled in `render.yaml`.

**Post-deployment end-to-end testing** proves the hosted dashboard, authentication, account creation, transfer and transaction-history flow after code changes.

## Production improvements

A production version would add PostgreSQL, Alembic migrations, structured audit logs, rate limiting, refresh-token strategy, managed secrets, monitoring, distributed tracing, database transaction isolation, row-level locking, stronger frontend session controls and integration with a core banking or payment platform.

## Interview talking points

1. Translating financial requirements into API contracts and validation rules.
2. Building a browser dashboard that consumes the protected REST API rather than duplicating business logic.
3. Protecting transactions from duplicates, invalid amounts, currency mismatch and insufficient funds.
4. Securing customer resources through JWT authentication and ownership checks.
5. Testing both success paths, failure cases and frontend asset delivery.
6. Moving compilation, tests and Docker verification into CI.
7. Defining deployment with version-controlled Infrastructure as Code.
8. Verifying the hosted system with an authenticated end-to-end smoke test.
9. Extending the service to M-Pesa, core banking systems or other payment channels.

## Author

Samuel Mutua Kimani
