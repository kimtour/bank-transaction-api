# Technology Stack Explained

This page explains the main tools used in the Bank Transaction API and how they fit together.

## Development tools

- **VS Code**: editor/IDE used to write, run and debug the Python project.
- **Git**: version-control system used to track changes locally.
- **GitHub**: remote repository used to store the code and run CI workflows.
- **`git clone`**: copies the GitHub repository onto a local computer.
- **`venv`**: creates an isolated Python environment for this project.

## Application stack

- **Python 3.12**: programming language used by the service.
- **FastAPI**: REST API framework that defines endpoints and automatically produces OpenAPI/Swagger documentation.
- **Uvicorn**: ASGI web server that runs the FastAPI application.
- **Pydantic**: validates request/response data before business logic runs.
- **SQLAlchemy**: ORM that maps Python classes and operations to relational database tables and queries.
- **SQLite**: lightweight file-based relational database used for the disposable demo environment.
- **PyJWT**: creates and validates JWT access tokens used by protected endpoints.

## Testing and automation

- **Pytest**: automated Python testing framework used by the 11-test application suite.
- **HTTPX / FastAPI TestClient**: sends simulated HTTP requests to the FastAPI application during tests.
- **`.github/workflows/tests.yml`**: CI workflow that installs Python 3.12 dependencies, compiles the app, runs Pytest and builds the Docker image.
- **`.github/workflows/live-smoke.yml`**: post-deployment workflow that runs a real end-to-end test against Render.
- **`scripts/live_smoke.py`**: verifies landing page, health, Swagger, OpenAPI, registration, login, JWT authentication, account creation, transfer balances and transaction history on the public deployment.

## Packaging and deployment

- **`requirements.txt`**: pinned Python dependencies required by the application and CI environment.
- **`Dockerfile`**: instructions for packaging the application, Python runtime and dependencies into a Docker image.
- **`render.yaml`**: Render Infrastructure-as-Code configuration defining the free hosted web service, Python version, build command, start command, health check and environment variables.
- **Render**: hosts the public demonstration service.

## End-to-end application flow

```text
VS Code
  -> Python
  -> FastAPI
  -> Pydantic validation
  -> JWT authentication
  -> service-layer banking rules
  -> SQLAlchemy ORM
  -> SQLite
  -> Uvicorn
  -> Render
```

Quality and delivery flow:

```text
Code change
  -> Git commit
  -> GitHub push
  -> CI compile/test/Docker build
  -> Render deployment
  -> live authenticated E2E smoke test
```

## Interview summary

> I use VS Code to develop the Python service. FastAPI exposes the REST endpoints, Pydantic validates requests, SQLAlchemy communicates with SQLite, PyJWT protects authenticated routes, and Uvicorn runs the service. Pytest and HTTPX provide automated API testing, GitHub Actions performs CI and Docker verification, Render deploys the application from `render.yaml`, and a separate live smoke workflow proves that registration, authentication, account creation and transfers work on the hosted service.
