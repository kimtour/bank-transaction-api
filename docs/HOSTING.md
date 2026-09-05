# Free Online Hosting with Render

The Bank Transaction System is deployed as a Render Web Service from the version-controlled `render.yaml` file. The same service hosts both the banking dashboard and the FastAPI backend.

## Live service

- Banking dashboard: https://samuel-kimani-bank-api-demo.onrender.com/
- Build walkthrough: https://samuel-kimani-bank-api-demo.onrender.com/walkthrough
- Swagger UI: https://samuel-kimani-bank-api-demo.onrender.com/docs
- Health check: https://samuel-kimani-bank-api-demo.onrender.com/health
- OpenAPI contract: https://samuel-kimani-bank-api-demo.onrender.com/openapi.json

## What Render serves

```text
/
  -> app/static/index.html banking dashboard

/walkthrough
  -> app/static/walkthrough.html technical build guide

/static/styles.css
  -> responsive dashboard styling

/static/app.js
  -> browser-to-API integration

/auth, /accounts, /transfers, /transactions
  -> FastAPI REST endpoints

/docs
  -> Swagger API documentation
```

## Current Render configuration

`render.yaml` defines:

- Service name: `samuel-kimani-bank-api-demo`
- Runtime: Python
- Python version: `3.12.14`
- Plan: Free
- Region: Frankfurt
- Health check: `/health`
- Build command: `python -m pip install --upgrade pip && python -m pip install -r requirements.txt`
- Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- JWT secret: generated securely by Render
- Database: SQLite for disposable demo data
- Auto deploy: when configured repository changes are deployed

## Deployment flow

```text
Push to main
  -> GitHub Actions CI
  -> compile Python application
  -> test dashboard, walkthrough and API
  -> run banking test suite
  -> build Docker image
  -> CI passes
  -> Render deploys
  -> Render checks /health
  -> dashboard, walkthrough and API become live
  -> live end-to-end smoke test verifies the public service
```

## Live end-to-end verification

`.github/workflows/live-smoke.yml` checks out the repository and runs `scripts/live_smoke.py` against the public Render URL.

The script verifies the hosted frontend, health endpoint, Swagger/OpenAPI surface, authentication, account creation, a KES transfer, resulting balances and transaction history.

This verifies the running hosted frontend, authentication, database writes and core banking flow, rather than only page availability.

## Free-tier behavior

Render free web services can sleep after inactivity. The smoke script contains retry logic so a cold start has time to wake the service before it declares a failure.

The free service filesystem is ephemeral. SQLite is intentionally used only for this portfolio deployment, so records can reset after a restart or redeploy.

For production, use PostgreSQL or another managed persistent database, database migrations, managed secrets, structured logs, monitoring and stronger session management.

## Portfolio presentation checklist

Keep these pages ready:

```text
https://samuel-kimani-bank-api-demo.onrender.com/
https://samuel-kimani-bank-api-demo.onrender.com/walkthrough
https://samuel-kimani-bank-api-demo.onrender.com/docs
https://samuel-kimani-bank-api-demo.onrender.com/health
https://github.com/kimtour/bank-transaction-api
https://github.com/kimtour/bank-transaction-api/actions
```

Open `/health` or the dashboard before a live presentation if the free service has been idle so the service is already awake.
