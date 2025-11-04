# SwaB Asset Management System

FastAPI-based asset management service for tracking resources, employees, and locations. Connects to Google Cloud SQL (MySQL) with comprehensive API endpoints, authentication, logging, and automated testing.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Running the Application](#running-the-application)
5. [API Testing](#api-testing)
6. [Database Setup](#database-setup)
7. [Testing & CI](#testing--ci)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# Clone and setup
git clone <your-repository-url>
cd NextGenTeamBlue
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure database (edit config.ini with your credentials)
cp config.ini.example config.ini  # If available

# Authenticate with Google Cloud (for Cloud SQL)
gcloud auth application-default login

# Run the API
uvicorn src.main:app --reload

# Open browser testing tool
open src/index_test.html
```

---

## Project Structure

```
NextGenTeamBlue/
├── src/
│   ├── main.py                      # Main FastAPI application
│   ├── app_factory.py               # Application factory
│   ├── index.html                   # Landing/documentation page
│   ├── index_test.html              # Interactive API testing tool
│   ├── api/
│   │   ├── routes/
│   │   │   └── resources.py         # Resource/Asset endpoints
│   │   ├── authenticate.py          # JWT authentication
│   │   ├── authorize.py             # Role-based authorization
│   │   ├── health.py                # Health check endpoints
│   │   └── validate.py              # Request validation
│   ├── database/
│   │   ├── database_connector.py    # SQLAlchemy connection
│   │   └── database_controller.py   # Database operations
│   ├── logger/
│   │   └── logger.py                # Loguru logging wrapper
│   └── security/
│       ├── auth.py                  # Authentication logic
│       └── sanitize.py              # Input sanitization
├── tests/                           # Pytest test suite
│   ├── api/                         # API endpoint tests
│   ├── database/                    # Database tests
│   └── conftest.py                  # Pytest configuration
├── Documentation/
│   ├── tableCreation.sql            # Database schema
│   └── insertTables.sql             # Sample data
├── .github/workflows/               # CI/CD pipelines
│   ├── ci.yml                       # Combined lint + test + coverage
│   ├── pylint.yml                   # Code quality checks
│   ├── pytest.yml                   # Test execution
│   └── codeql.yml                   # Security scanning
├── config.ini                       # Runtime configuration
└── requirements.txt                 # Python dependencies
```

---

## Setup Instructions

### 1. Clone and Create Virtual Environment

```bash
git clone <your-repository-url>
cd NextGenTeamBlue

# Create virtual environment
python3 -m venv venv

# Activate environment
# macOS/Linux:
source venv/bin/activate
# Windows Command Prompt:
venv\Scripts\activate
# Windows PowerShell:
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Database Connection

Edit `config.ini` with your database credentials:

```ini
[mysql]
db_user = YOUR_DB_USER
db_password = YOUR_DB_PASSWORD
db_name = YOUR_DB_NAME
db_port = 3306
instance_connection_name = project-id:region:instance-name
db_host = YOUR_DB_HOST  # Optional for local MySQL

[log]
format = <green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{level}</level> - <level>{message}</level>
log_path = ./log
```

**Important:** Keep `config.ini` out of version control. Add it to `.gitignore`.

### 4. Google Cloud Authentication (for Cloud SQL)

```bash
# Install Google Cloud SDK
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Verify IAM permissions
# Ensure your account has "Cloud SQL Client" role
```

For local MySQL, skip this step and ensure `db_host` is set to `localhost` or your MySQL server address.

---

## Running the Application

### Start the FastAPI Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Custom host and port
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at:
- **API:** http://127.0.0.1:8000
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## API Testing

### Available Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Root/health check | No |
| `/health` | GET | Liveness check | No |
| `/health/ready` | GET | Readiness (DB) check | No |
| `/resources/` | GET | List all resources | Yes |
| `/resources/{id}` | GET | Get resource by ID | Yes |
| `/resources/` | POST | Create new resource | Yes |
| `/resources/{id}` | PUT | Update resource | Yes |
| `/resources/{id}` | DELETE | Delete resource | Yes |
| `/resources/employee/{id}` | GET | Get resources by employee | Yes |
| `/resources/location/{id}` | GET | Get resources by location | Yes |
| `/resources/types/` | GET | List resource types | Yes |

### Using curl

```bash
# Get all resources
curl -X GET "http://127.0.0.1:8000/resources/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create a new resource
curl -X POST "http://127.0.0.1:8000/resources/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "type_id": 2,
    "location_id": 1,
    "employee_id": 31,
    "notes": "Testing",
    "is_decommissioned": 0
  }'

# Get resource by ID
curl -X GET "http://127.0.0.1:8000/resources/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Update resource
curl -X PUT "http://127.0.0.1:8000/resources/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated notes",
    "is_decommissioned": 1
  }'
```

### Using the HTML Test Interface

Open `src/index_test.html` in your browser for an interactive testing interface:

1. **Start the API server** (see above)
2. **Open** `src/index_test.html` in a web browser
3. **Enter your Bearer token** in the token field at the top
4. **Use the buttons** to test each endpoint

Features:
- Bearer token authentication
- Get all resources/types
- Search by location or employee ID
- Get resource by ID
- Create new resources
- Update existing resources
- Delete resources
- Real-time JSON response display

**Note:** If you encounter CORS errors, ensure the API has CORS middleware enabled (already configured in `main.py`).

---

## Database Setup

### Schema Creation

```bash
# Connect to MySQL
mysql -u root -p

# Create database and tables
SOURCE Documentation/tableCreation.sql;

# Load sample data (optional)
SOURCE Documentation/insertTables.sql;
```

### Key Tables

- **Locations** - Physical locations
- **AssetTypes** - Resource type definitions
- **Asset** - Asset/resource inventory

### Connection Methods

**Google Cloud SQL:**
- Uses `cloud-sql-python-connector`
- Requires `instance_connection_name` in config
- Automatic IAM authentication

**Local MySQL:**
- Direct connection via `db_host` and `db_port`
- Standard username/password authentication

---

## Testing & CI

### Run Tests Locally

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test categories
pytest -m unit
pytest -m integration

# If you get import errors, set PYTHONPATH
PYTHONPATH=$(pwd) pytest -v
```

### Linting

```bash
# Run pylint
pylint src

# Check specific files
pylint src/main.py src/api/routes/resources.py
```

### GitHub Actions CI/CD

The project includes automated workflows:

- **`pylint.yml`** - Code quality checks (7.5 minimum score)
- **`pytest.yml`** - Test execution with JUnit XML reports
- **`codeql.yml`** - Security vulnerability scanning

Workflows run on push and pull requests to `main` and `DEV` branches.

---

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: src` | Python path not set | Run `PYTHONPATH=$(pwd) pytest` or `export PYTHONPATH=$(pwd)` |
| Cloud SQL 400/403 error | Wrong instance name or missing IAM role | Check `instance_connection_name` format and IAM permissions |
| CORS errors in browser | Missing CORS middleware | Verify `CORSMiddleware` in `main.py` |
| JSON parse error | Using `None` instead of `null` | Use valid JSON syntax (`null`, `true`, `false`) |
| Authentication failed | Invalid/expired token | Generate new JWT token |
| Connection refused | API not running | Start server with `uvicorn src.main:app --reload` |

### Logging

Logs are configured in `config.ini` and written to the `log/` directory:
- `event.log` - Application events
- `security.log` - Security-related events

View logs:
```bash
tail -f log/event.log
tail -f log/security.log
```

### Getting Help

1. Check the logs in `log/` directory
2. Verify configuration in `config.ini`
3. Ensure all dependencies are installed: `pip list`
4. Check database connectivity: `mysql -u USER -p -h HOST`
5. Review API documentation: http://127.0.0.1:8000/docs

---

## Security Notes

⚠️ **Important Security Practices:**

- Never commit `config.ini` with real credentials
- Use environment variables or Secret Manager in production
- Rotate JWT secrets regularly
- Restrict CORS origins (currently set to `*` for development)
- Use HTTPS in production
- Keep dependencies updated: `pip list --outdated`
- Review security scan results in GitHub Actions

---

## Development Workflow

1. Create feature branch from `DEV`
2. Make changes and add tests
3. Run tests locally: `pytest -v`
4. Check linting: `pylint src`
5. Commit and push
6. Create pull request
7. CI workflows will validate automatically
8. Merge after approval and passing checks

---

## Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Google Cloud SQL Python Connector:** https://github.com/GoogleCloudPlatform/cloud-sql-python-connector
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **Loguru Documentation:** https://loguru.readthedocs.io/

---

## License

This project is licensed under the **Apache License 2.0**.

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
