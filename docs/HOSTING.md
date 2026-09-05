# Free Online Hosting with Render

The Bank Transaction API is deployed as a free Render Web Service from the version-controlled `render.yaml` file.

## Live service

- Landing page: https://samuel-kimani-bank-api-demo.onrender.com/
- Swagger UI: https://samuel-kimani-bank-api-demo.onrender.com/docs
- Health check: https://samuel-kimani-bank-api-demo.onrender.com/health
- OpenAPI contract: https://samuel-kimani-bank-api-demo.onrender.com/openapi.json

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
  -> run Pytest suite
  -> build Docker image
  -> CI passes
  -> Render auto-deploys
  -> Render checks /health
  -> live end-to-end smoke test verifies the public service
```

## Live end-to-end verification

`.github/workflows/live-smoke.yml` checks out the repository and runs `scripts/live_smoke.py` against the public Render URL.

The script verifies:

1. `/health` returns `status=ok` and the expected service name.
2. `/` returns the Bank Transaction API landing page.
3. `/docs` serves Swagger UI.
4. `/openapi.json` exposes the expected core API paths.
5. A unique temporary user can register.
6. The user can log in and obtain a JWT access token.
7. Two KES accounts can be created.
8. KES 750 can be transferred between them.
9. Source and destination balances are updated correctly.
10. The transaction appears in transaction history.

This verifies the running hosted application, authentication, database writes and core banking flow, not only page availability.

## Free-tier behavior

Render free web services can sleep after inactivity. The smoke script contains retry logic so a cold start has time to wake the service before it declares a failure.

The free service filesystem is ephemeral. SQLite is intentionally used only for this interview/demo deployment, so records can reset after a restart or redeploy.

For production, use PostgreSQL or another managed persistent database, database migrations, managed secrets, structured logs and monitoring.

## Interview checklist

Keep these pages ready:

```text
https://samuel-kimani-bank-api-demo.onrender.com/docs
https://samuel-kimani-bank-api-demo.onrender.com/health
https://github.com/kimtour/bank-transaction-api
https://github.com/kimtour/bank-transaction-api/actions
```

If the free service has been idle, open `/health` a few minutes before the interview to wake it up.
