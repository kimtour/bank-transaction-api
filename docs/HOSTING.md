# Free Online Hosting with Render

This project is deployed as a free Render Web Service through `render.yaml`.

## Live service

- Landing page: https://samuel-kimani-bank-api-demo.onrender.com/
- Swagger API: https://samuel-kimani-bank-api-demo.onrender.com/docs
- Health check: https://samuel-kimani-bank-api-demo.onrender.com/health
- GitHub repository: https://github.com/kimtour/bank-transaction-api
- GitHub Actions: https://github.com/kimtour/bank-transaction-api/actions

## Render configuration

- Service name: `samuel-kimani-bank-api-demo`
- Runtime: Python 3.12
- Plan: Free
- Region: Frankfurt
- Health check: `/health`
- Build command: `python -m pip install --upgrade pip && python -m pip install -r requirements.txt`
- Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- JWT secret: generated automatically by Render
- Auto deploy: after linked CI checks pass

## Recommended live demo

1. Open the health endpoint and show the service is online.
2. Open Swagger at `/docs`.
3. Register a demo user.
4. Log in and copy the access token.
5. Click **Authorize** in Swagger and paste the token.
6. Create two KES accounts.
7. Transfer KES 5,000 between them.
8. Show the new balances and transaction history.
9. Attempt a transfer larger than the source balance and show the API rejection.
10. Open GitHub Actions and show the green CI workflow.

## Free-tier behavior

Render free web services may sleep after a period without traffic and can take longer on the first request after sleeping. The free service filesystem is ephemeral. This project intentionally uses SQLite for a disposable interview demo, so demo data can reset after a restart or redeploy.

For production, use PostgreSQL and managed persistent storage.
