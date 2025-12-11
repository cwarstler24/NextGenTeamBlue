# NextGenTeamBlue – Asset Management System

Full‑stack asset management system with a FastAPI backend and a Vue 3 (Vite) frontend. The backend connects to Google Cloud SQL (MySQL) via a service account. The app includes authentication/authorization, logging, and an automated test suite. A production‑ready Docker setup is included.

---

## At a glance
- Backend: FastAPI, SQLAlchemy, Cloud SQL Python Connector
- Frontend: Vue 3, Vite, Vue Router, Axios
- Database: Google Cloud SQL (MySQL)
- Containerization: Docker + docker compose (frontend + backend + nginx)
- Auth: Bearer token (saved in browser localStorage through the Home page)

```
Browser
  ↓
Nginx (frontend container)  →  /resources/* proxied to backend
  ↓ serves Vue SPA           →  /api/* proxied to backend
FastAPI (backend container)  →  connects to Google Cloud SQL
```

---

## Repository layout

```
NextGenTeamBlue/
├─ backend/                  # FastAPI application
│  ├─ src/
│  │  ├─ main.py             # FastAPI entrypoint
│  │  ├─ app_factory.py      # App setup (CORS, routers)
│  │  ├─ api/
│  │  │  ├─ authenticate.py
│  │  │  ├─ authorize.py
│  │  │  ├─ health.py
│  │  │  └─ routes/resources.py
│  │  ├─ database/
│  │  │  ├─ database_connector.py
│  │  │  └─ database_controller.py
│  │  ├─ logger/
│  │  │  └─ logger.py
│  │  └─ security/
│  │     ├─ auth.py
│  │     └─ sanitize.py
│  ├─ tests/                 # pytest suite (api, database, logger, …)
│  ├─ requirements.txt
│  ├─ pytest.ini
│  └─ config.ini             # Backend configuration (see Security note)
│
├─ frontend/                 # Vue 3 + Vite SPA
│  ├─ src/
│  │  ├─ views/Asset*.vue
│  │  ├─ router/index.ts
│  │  └─ config/api.ts       # Auto-selects API base for dev vs Docker
│  ├─ package.json
│  └─ vite.config.ts
│
├─ Documentation/            # SQL scripts and docs
├─ Dockerfile.backend        # Backend image
├─ Dockerfile.frontend       # Frontend builder + Nginx image
├─ docker-compose.yml        # Dev/standard compose (ports 80, 8000)
├─ docker-compose.prod.yml   # Production compose + healthchecks
├─ nginx.conf                # Nginx routes Vue + proxies API
├─ .env.example              # Compose environment template
└─ README_DOCKER.md          # Detailed Docker/run guide
```

---

## Quick start

Choose one of the following setups.

### Option A) Docker (recommended)
1) Copy the environment template and edit values
   - Windows PowerShell:
     - Copy: `Copy-Item .env.example .env`
     - Edit: open `.env` and fill values (see Configuration below)
2) Place your GCP service account key at `env/gcp-key.json`
3) Start the stack
   - `docker compose up -d`
4) Open:
   - Frontend: http://localhost
   - API Docs: http://localhost:8000/docs

See the full guide in `README_DOCKER.md`.

### Option B) Local development (frontend + backend)

Backend (from repo root):
- Python venv
  - PowerShell: `python -m venv venv; .\venv\Scripts\Activate.ps1`
- Install deps: `pip install -r backend/requirements.txt`
- Configure backend: edit `backend/config.ini` (see Configuration)
- Run: `uvicorn src.main:app --reload`
  - Run from the `backend` folder: `cd backend; uvicorn src.main:app --reload`
  - API: http://127.0.0.1:8000

Frontend (in another terminal):
- Node 20+ or 22+
- `cd frontend`
- `npm install`
- `npm run dev`
- App: http://127.0.0.1:5173 (or another Vite port)

The frontend auto-detects dev mode and calls the API at http://127.0.0.1:8000 (see `frontend/src/config/api.ts`).

---

## Configuration

### Docker `.env`
Create `.env` (see `.env.example`) in the repo root:

```
INSTANCE_CONNECTION_NAME=your-project:region:instance
GCP_KEY_PATH=./env/gcp-key.json
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=teamblue-asset-ms
```

Also place your service account key at `env/gcp-key.json` (not committed).

### Backend `config.ini`
`backend/config.ini` controls DB and logging for the FastAPI app. Example fields:

```
[mysql]
db_user = YOUR_DB_USER
db_password = YOUR_DB_PASSWORD
db_name = YOUR_DB_NAME
db_port = 3306
instance_connection_name = project:region:instance

[log]
log_path = ../../log
```

Security note: Don’t commit secrets. Prefer environment secrets/Secret Manager in production.

---

## Running and endpoints

Backend root: http://127.0.0.1:8000

Key endpoints (all under `/resources`, require Authorization: Bearer <token>):
- GET `/resources/` – list assets
- GET `/resources/{id}` – asset by ID
- GET `/resources/types/` – asset types
- GET `/resources/employee/{employee_id}` – assets by employee
- GET `/resources/location/{location_id}` – assets by location
- POST `/resources/` – create asset
- PUT `/resources/{id}` – update asset
- DELETE `/resources/{id}` – delete asset
- GET `/resources/employees/` – employees for dropdowns
- GET `/resources/locations/` – locations for dropdowns

Other:
- GET `/` – API heartbeat
- GET `/docs` – Swagger UI

Frontend notes:
- Save a bearer token on the Home page; it’s stored in `localStorage` and used by API calls.
- The Asset List view includes client‑side filters for Employee ID and Type ID.
- Add/Update forms pull asset types from the backend.

---

## Testing

From the `backend` folder:
- Run tests: `pytest` (uses `backend/pytest.ini`)
- With coverage: `pytest -q --cov`

Tests are organized under `backend/tests/` (api, database, logger, query, security).

---

## Troubleshooting

Common issues:
- docker compose shows “variables not set” → Create `.env` (use `.env.example`) and ensure `GCP_KEY_PATH` points to your key file.
- 401 from API → Ensure a valid bearer token is set in the UI (Home page) or sent via `Authorization` header.
- CORS in local dev → CORS is enabled in `backend/src/app_factory.py`. If using custom hosts, update allowed origins.
- DB connectivity errors → Verify `INSTANCE_CONNECTION_NAME` and service account permissions (Cloud SQL Client role).

For Docker‑specific help, see `README_DOCKER.md`.

---

## Deployment and images

Container images can be built locally with docker compose or published to a registry (e.g., GitHub Container Registry). See the “Publish containers” notes in your project docs or ask for a CI workflow.

---

## License

Licensed under the Apache License 2.0.

Key points:
- Free for commercial and private use
- Permissive: modifications and redistribution allowed
- Includes explicit patent grant
- Must retain `LICENSE` and `NOTICE` files in redistributions
- Clearly mark any changes you make in derivative works

See the full license text in the `LICENSE` file and third-party attributions in `NOTICE`.

Add SPDX headers (recommended) at the top of source files you modify:
```python
# SPDX-License-Identifier: Apache-2.0
```

## Contributors

| Name | Role |
|------|------|
| cwarstler24 | Project Owner |
| (Add others) | Contributor |

To contribute: fork the repo, create a feature branch, submit a PR, ensure tests and lint pass.

---

# frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```
