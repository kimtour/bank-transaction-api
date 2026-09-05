# Technology Stack Explained

This page explains the main tools used in the Bank Transaction System and how they fit together.

## Development tools

- **VS Code**: editor/IDE used to write, run and debug the Python, HTML, CSS and JavaScript project.
- **Git**: version-control system used to track changes locally.
- **GitHub**: remote repository used to store the code and run CI workflows.
- **`git clone`**: copies the GitHub repository onto a local computer.
- **`venv`**: creates an isolated Python environment for this project.

## Frontend stack

- **HTML**: defines the banking dashboard structure, forms, account cards and transaction table.
- **CSS**: provides the responsive banking interface, layout, typography, account cards and status styling.
- **JavaScript**: connects the dashboard to the live FastAPI endpoints with `fetch`, stores the demo JWT in browser storage, updates balances and renders transaction history.
- **Same-origin API calls**: the browser frontend and FastAPI backend share one Render service, so the JavaScript calls paths such as `/accounts` and `/transfers` directly.
- **`app/static/`**: contains `index.html`, `styles.css` and `app.js`.

## Application stack

- **Python 3.12**: programming language used by the backend service.
- **FastAPI**: REST API framework that defines endpoints, serves the dashboard and automatically produces OpenAPI/Swagger documentation.
- **Uvicorn**: ASGI web server that runs the FastAPI application.
- **Pydantic**: validates request/response data before business logic runs.
- **SQLAlchemy**: ORM that maps Python classes and operations to relational database tables and queries.
- **SQLite**: lightweight file-based relational database used for the disposable demo environment.
- **PyJWT**: creates and validates JWT access tokens used by protected endpoints.

## Testing and automation

- **Pytest**: automated Python testing framework used by the 12-test application suite.
- **HTTPX / FastAPI TestClient**: sends simulated HTTP requests to the FastAPI application during tests.
- **Dashboard asset tests**: confirm that the root page, CSS and JavaScript are served by FastAPI.
- **`.github/workflows/tests.yml`**: CI workflow that installs Python 3.12 dependencies, compiles the app, runs Pytest and builds the Docker image.
- **`.github/workflows/live-smoke.yml`**: post-deployment workflow that runs a real end-to-end test against Render.
- **`scripts/live_smoke.py`**: verifies the dashboard HTML/CSS/JavaScript, health, Swagger, OpenAPI, registration, login, JWT authentication, account creation, transfer balances and transaction history on the public deployment.

## Packaging and deployment

- **`requirements.txt`**: pinned Python dependencies required by the application and CI environment.
- **`Dockerfile`**: instructions for packaging the backend and static frontend with the Python runtime and dependencies into a Docker image.
- **`render.yaml`**: Render Infrastructure-as-Code configuration defining the free hosted web service, Python version, build command, start command, health check and environment variables.
- **Render**: hosts the public full-stack demonstration application.

## End-to-end application flow

```text
VS Code
  -> HTML / CSS / JavaScript frontend
  -> FastAPI REST API
  -> Pydantic validation
  -> JWT authentication
  -> service-layer banking rules
  -> SQLAlchemy ORM
  -> SQLite
  -> Uvicorn
  -> Render
```

Request flow from the live browser dashboard:

```text
User clicks Transfer
  -> JavaScript builds JSON request
  -> fetch POST /transfers with Bearer JWT
  -> FastAPI authenticates user
  -> Pydantic validates request
  -> service layer checks financial rules
  -> SQLAlchemy updates database
  -> API returns JSON
  -> JavaScript refreshes balances and history
```

Quality and delivery flow:

```text
Code change
  -> Git commit
  -> GitHub push
  -> CI compile/test/Docker build
  -> Render deployment
  -> live dashboard + authenticated E2E smoke test
```

## Interview summary

> I use VS Code to develop the full-stack application. HTML, CSS and JavaScript provide the browser dashboard and call the same FastAPI REST endpoints that are visible in Swagger. Pydantic validates requests, SQLAlchemy communicates with SQLite, PyJWT protects authenticated routes, and Uvicorn runs the service. Pytest and TestClient provide automated application testing, GitHub Actions performs CI and Docker verification, Render deploys the application from `render.yaml`, and a separate live smoke workflow proves that the dashboard, registration, authentication, account creation and transfers work on the hosted service.
