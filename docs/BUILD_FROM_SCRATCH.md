# Build the Bank Transaction API from Scratch

This guide shows the development sequence from an empty computer folder to the hosted API.

## 1. Clone the repository

```bash
git clone https://github.com/kimtour/bank-transaction-api.git  # Copy the GitHub repository onto your computer.
cd bank-transaction-api                                        # Move the terminal into the project folder.
```

## 2. Open the project in VS Code

```bash
code .  # Open the current project folder in Visual Studio Code.
```

Install the Microsoft **Python** and **Pylance** extensions in VS Code, then select the Python interpreter from the project's `.venv` environment after creating it.

## 3. Create and activate a virtual environment

```bash
python3 -m venv .venv       # Create an isolated Python environment named .venv.
source .venv/bin/activate   # Activate that environment on macOS/Linux.
```

## 4. Install project dependencies

```bash
python -m pip install -r requirements.txt  # Install all pinned application and testing dependencies.
```

Key packages:

- `fastapi`: creates REST API endpoints.
- `uvicorn`: runs the FastAPI application as a web server.
- `sqlalchemy`: maps Python models to relational database tables and queries.
- `pydantic`: validates incoming and outgoing API data.
- `pyjwt`: creates and validates JWT authentication tokens.
- `pytest`: runs automated tests.
- `httpx`: provides HTTP request support used by FastAPI testing tools.

## 5. Understand the project structure

```text
app/main.py                   # FastAPI application and HTTP routes.
app/models.py                 # SQLAlchemy database tables.
app/schemas.py                # Pydantic request and response validation models.
app/services.py               # Banking business rules such as transfer validation.
app/security.py               # Password hashing and JWT authentication.
app/database.py               # SQLAlchemy engine and database sessions.
app/config.py                 # Environment-based configuration.
tests/test_api.py             # 11 automated API test cases.
scripts/live_smoke.py         # End-to-end verification against the public Render service.
.github/workflows/tests.yml   # CI compilation, tests and Docker build.
.github/workflows/live-smoke.yml  # Hosted end-to-end smoke workflow.
render.yaml                   # Render deployment configuration.
```

## 6. Run the API locally

```bash
cp .env.example .env                 # Create a local environment configuration file.
python -m uvicorn app.main:app --reload  # Start FastAPI and reload after source-code changes.
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

## 7. Run automated tests

```bash
pytest -q  # Run the automated API test suite with compact output.
```

The suite validates authentication, account creation, deposits, transfers, transaction history, insufficient funds, duplicate references, invalid tokens, invalid amounts, account ownership, same-account transfers and currency mismatch handling.

## 8. Build the Docker image

```bash
docker build -t bank-transaction-api .  # Build the Docker image using the project's Dockerfile.
```

The CI workflow performs this build automatically as well, which verifies that the container packaging remains valid after changes.

## 9. Commit and push changes

```bash
git status                              # Show files that have changed.
git add .                               # Stage all project changes for a commit.
git commit -m "Update banking API"     # Save a versioned snapshot of the staged changes.
git push origin main                    # Upload the new commit to GitHub's main branch.
```

## 10. Continuous Integration

`.github/workflows/tests.yml` automatically:

```text
Push code
  -> checkout repository
  -> install Python 3.12
  -> install requirements.txt
  -> compile app
  -> run pytest
  -> build Docker image
  -> report success or failure
```

## 11. Cloud deployment

`render.yaml` tells Render how to deploy the application:

```text
GitHub main branch
  -> Render reads render.yaml
  -> install Python dependencies
  -> start Uvicorn
  -> check /health
  -> expose public URL
```

Live URLs:

- Landing page: https://samuel-kimani-bank-api-demo.onrender.com/
- Swagger UI: https://samuel-kimani-bank-api-demo.onrender.com/docs
- Health: https://samuel-kimani-bank-api-demo.onrender.com/health

## 12. Verify the actual hosted banking flow

`.github/workflows/live-smoke.yml` runs:

```bash
python scripts/live_smoke.py  # Test the deployed Render API end to end.
```

The script automatically:

```text
checks /health, /, /docs and /openapi.json
  -> registers a unique temporary user
  -> logs in and obtains JWT
  -> creates two KES accounts
  -> transfers KES 750
  -> verifies balances
  -> verifies transaction history
```

This confirms that the real hosted API can execute the core authenticated banking workflow, not only that the web server is reachable.

## Development lifecycle summary

```text
Requirements
  -> API/database design
  -> implement models and schemas
  -> implement business rules
  -> add authentication
  -> test locally
  -> write automated tests
  -> build Docker image
  -> commit with Git
  -> push to GitHub
  -> CI runs
  -> Render deploys
  -> live end-to-end smoke test verifies the hosted banking flow
```
