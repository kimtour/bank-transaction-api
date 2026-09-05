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
  -> GitHub live smoke workflow verifies the public service
```

## Live smoke verification

`.github/workflows/live-smoke.yml` runs from GitHub Actions and independently verifies:

1. `/health` returns JSON with `status=ok` and the expected service name.
2. `/` contains the Bank Transaction API landing page.
3. `/docs` serves Swagger UI.
4. `/openapi.json` contains the expected core API paths.

This makes hosting verification repeatable instead of relying only on a manual browser check.

## Free-tier behavior

Render free web services can sleep after inactivity. The smoke workflow uses retries so a cold start has time to wake the service before declaring a failure.

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
