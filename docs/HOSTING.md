# Free Online Hosting with Render

This project is configured for a free Render Web Service through `render.yaml`.

## One-click deployment

Use the **Deploy to Render** button in the main README.

Render will read `render.yaml` and propose a service with these settings:

- Service name: `samuel-kimani-bank-api-demo`
- Runtime: Python
- Plan: Free
- Region: Frankfurt
- Health check: `/health`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- JWT secret: generated automatically by Render
- Auto deploy: after linked CI checks pass

## Final approval steps

1. Sign in to Render.
2. Open the Deploy to Render button from the repository README.
3. Review the Blueprint.
4. Keep the Free plan selected.
5. Approve the deployment.
6. Open the generated `onrender.com` service URL.
7. Add `/docs` to open Swagger UI.

## Panel links

Once deployment finishes, keep these open before the interview:

```text
https://<your-render-service>.onrender.com/
https://<your-render-service>.onrender.com/docs
https://<your-render-service>.onrender.com/health
https://github.com/kimtour/bank-transaction-api
https://github.com/kimtour/bank-transaction-api/actions
```

## Recommended live demo

1. Open `/health` and show the service is online.
2. Open `/docs`.
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
