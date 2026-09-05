# Free Online Hosting with Render

The Bank Transaction System is deployed as a free Render Web Service from the version-controlled `render.yaml` file. The same service hosts both the banking dashboard and the FastAPI backend.

## Live service

- Banking dashboard: https://samuel-kimani-bank-api-demo.onrender.com/
- Swagger UI: https://samuel-kimani-bank-api-demo.onrender.com/docs
- Health check: https://samuel-kimani-bank-api-demo.onrender.com/health
- OpenAPI contract: https://samuel-kimani-bank-api-demo.onrender.com/openapi.json

## What Render serves

```text
/
  -> app/static/index.html banking dashboard

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
- Auto deploy: after linked repository checks pass

## Deployment flow

```text
Push to main
  -> GitHub Actions CI
  -> compile Python application
  -> test dashboard and API
  -> run banking test suite
  -> build Docker image
  -> CI passes
  -> Render auto-deploys
  -> Render checks /health
  -> dashboard and API become live
  -> live end-to-end smoke test verifies the public service
```

## Live end-to-end verification

`.github/workflows/live-smoke.yml` checks out the repository and runs `scripts/live_smoke.py` against the public Render URL.

The script verifies:

1. `/` serves the Bank Transaction System dashboard.
2. `/static/styles.css` is reachable and contains the dashboard styles.
3. `/static/app.js` is reachable and contains the API integration logic.
4. `/health` returns `status=ok` and the expected service name.
5. `/docs` serves Swagger UI.
6. `/openapi.json` exposes the expected core API paths.
7. A unique temporary user can register.
8. The user can log in and obtain a JWT access token.
9. Two KES accounts can be created.
10. KES 750 can be transferred between them.
11. Source and destination balances are updated correctly.
12. The transaction appears in transaction history.

This verifies the running hosted frontend, authentication, database writes and core banking flow, not only page availability.

## Free-tier behavior

Render free web services can sleep after inactivity. The smoke script contains retry logic so a cold start has time to wake the service before it declares a failure.

The free service filesystem is ephemeral. SQLite is intentionally used only for this portfolio/demo deployment, so records can reset after a restart or redeploy.

For production, use PostgreSQL or another managed persistent database, database migrations, managed secrets, structured logs, monitoring and stronger session management.

## Interview checklist

Keep these pages ready:

```text
https://samuel-kimani-bank-api-demo.onrender.com/
https://samuel-kimani-bank-api-demo.onrender.com/docs
https://samuel-kimani-bank-api-demo.onrender.com/health
https://github.com/kimtour/bank-transaction-api
https://github.com/kimtour/bank-transaction-api/actions
```

If the free service has been idle, open `/health` or the dashboard a few minutes before the interview to wake it up.
