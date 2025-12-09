# 🚀 Running NextGenTeamBlue with Docker

## Quick Start (5 minutes)

### Prerequisites
- Docker installed
- GCP Cloud SQL instance ready
- GCP service account JSON key
- `.env` file configured with GCP details

### Step 1: Prepare Environment
```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your GCP details (see "Configuration" section below)
nano .env
```

### Step 2: Set Up GCP Key
```bash
# Create env directory
mkdir -p env

# Place your GCP service account key here
# The key should be at: env/gcp-key.json
# Make sure it has proper permissions:
chmod 600 env/gcp-key.json
```

### Step 3: Build & Run
```bash
# Build Docker images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps
```

✅ **That's it!** Your app is now running:
- **Frontend**: http://localhost
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/resources/

---

## Configuration

### .env File
Create a `.env` file with your GCP details:

```bash
# Google Cloud SQL
INSTANCE_CONNECTION_NAME=your-project:region:instance-name
GCP_KEY_PATH=./env/gcp-key.json
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=teamblue-asset-ms
```

**Where to find these:**
- `INSTANCE_CONNECTION_NAME`: GCP Console → Cloud SQL → Connection name
- `GCP_KEY_PATH`: Path to your service account JSON key (create at `env/gcp-key.json`)
- `DB_USER`, `DB_PASSWORD`: Your Cloud SQL instance credentials
- `DB_NAME`: Your database name (likely `teamblue-asset-ms`)

---

## Common Commands

### Start Services
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Just backend
docker compose logs -f backend

# Just frontend
docker compose logs -f frontend
```

### Check Status
```bash
docker compose ps
```

### Rebuild After Code Changes
```bash
# Rebuild backend
docker compose build backend
docker compose up -d backend

# Rebuild frontend
docker compose build frontend
docker compose up -d frontend

# Rebuild everything
docker compose build
docker compose up -d
```

### Access Container Shell
```bash
# Backend
docker exec -it teamblue-backend bash

# Frontend
docker exec -it teamblue-frontend bash
```

---

## Testing

### Verify Backend is Running
```bash
curl http://localhost:8000/
```
Should return: `{"message":"Team Blue API is live 🚀"}`

### Verify Frontend is Running
```bash
curl http://localhost/
```
Should return HTML content

### Test with Authorization Token
```bash
# Get a token from your auth system, then:
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost/resources/

# Or through the UI:
# Visit http://localhost → click Home → enter token → test
```

---

## Troubleshooting

### Services Won't Start
```bash
# Check Docker is running
docker --version

# Check for port conflicts (80, 8000)
lsof -i :80
lsof -i :8000

# View detailed logs
docker compose logs
```

### Backend Can't Connect to Database
```bash
# Check the GCP key exists
ls -la env/gcp-key.json

# Verify it's valid JSON
cat env/gcp-key.json | python -m json.tool

# Check backend logs
docker compose logs backend | grep -i "error\|connection\|gcp"
```

### Frontend Shows 500 Errors
```bash
# This is likely a backend/database issue
# Check backend logs (see above)

# Make sure your bearer token is valid
# Bearer tokens expire - get a new one from the Home page
```

### CORS Errors in Browser
```bash
# This shouldn't happen with our Docker setup
# But if it does, check nginx.conf is correct
docker exec teamblue-frontend nginx -t

# Restart frontend
docker compose restart frontend
```

---

## File Structure

---

## 🎯 What's Running

```
Your Machine (Docker)
    ↓
    ├─ Frontend Container (Nginx + Vue)
    │  └─ Port 80 - serves http://localhost
    │
    └─ Backend Container (FastAPI)
       └─ Port 8000 (internal only, proxied through nginx)
       
    Both containers connect to:
    └─ Google Cloud SQL (via service account)
```

### Frontend
- Vue 3 single-page application
- Nginx web server
- Automatically routes requests
- Located in `frontend/` directory

### Backend
- FastAPI Python application
- REST API with documentation at `/docs`
- Authentication & authorization
- Database queries
- Located in `backend/` directory

### Database
- Google Cloud SQL (MySQL)
- Accessed via service account authentication
- External to Docker (managed by GCP)

---

## Architecture Diagram

```
                Browser (http://localhost)
                          ↓
                    ┌─────────────┐
                    │   Nginx     │ (Port 80)
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
            Frontend            Backend Proxy
          (Vue App)            (/resources/*)
                │                    │
                │                    ↓
                │              ┌──────────────┐
                │              │  FastAPI     │ (Port 8000)
                │              │ - API Routes │
                │              │ - Auth Check │
                │              │ - Validation │
                │              └──────┬───────┘
                │                     │
                └─────────────┬───────┘
                              │
                      GCP Service Account
                              ↓
                      Google Cloud SQL
```

---

## Useful Links

Once running:
- **Frontend**: http://localhost
- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/

---

## Directory Layout

```
NextGenTeamBlue/
├── backend/              # Python FastAPI backend
│  ├── src/              # Application code
│  ├── requirements.txt  # Python dependencies
│  └── Dockerfile        # Backend container definition
│
├── frontend/             # Vue 3 frontend
│  ├── src/              # Vue components
│  ├── package.json      # npm dependencies
│  └── Dockerfile        # Frontend container definition
│
├── env/                  # (Create this) GCP credentials
│  └── gcp-key.json      # Your service account key
│
├── .env                  # Environment configuration
├── docker-compose.yml    # Container orchestration
├── nginx.conf            # Web server configuration
└── README_DOCKER.md      # This file
```

---

## Performance Tips

### Make Builds Faster
```bash
# First build is slowest, later builds use cache
docker compose build

# To force a clean rebuild
docker compose build --no-cache
```

### Reduce Memory Usage
Edit `docker-compose.yml` and adjust limits:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M  # Reduce if needed

  frontend:
    deploy:
      resources:
        limits:
          memory: 256M  # Reduce if needed
```

### Speed Up Development
After code changes:
```bash
# Just rebuild what changed
docker compose build backend
docker compose up -d backend

# Don't rebuild everything
```

---

## Security Notes

✅ **What's Secure:**
- GCP key is never committed to Git (.gitignore)
- Key has restricted file permissions (600)
- Internal Docker network isolates backend
- Only frontend port (80) is exposed

⚠️ **For Production:**
- Use stronger database passwords
- Implement rate limiting
- Use HTTPS instead of HTTP
- Restrict CORS origins (currently `*`)
- Run security audits
- Keep Docker images updated

---

## Still Need Help?

### If you want to understand the setup better:
- Check `docker-compose.yml` for service definitions
- Check `nginx.conf` for routing configuration
- Check `Dockerfile.backend` and `Dockerfile.frontend` for container setup

### If you have specific questions:
1. **Can't start containers?** → Check Docker is running, ports are free
2. **Can't connect to database?** → Check GCP key, INSTANCE_CONNECTION_NAME
3. **Frontend shows errors?** → Check browser console, backend logs
4. **API doesn't work?** → Check bearer token, authorization level

---

## What's Next?

1. ✅ Services are running
2. ✅ Access frontend at http://localhost
3. ✅ Save a bearer token in the Home page
4. ✅ Try viewing/creating assets
5. 🔧 Customize as needed for your team

---

## Quick Reference Card

```bash
# START
docker compose up -d

# STOP
docker compose down

# LOGS
docker compose logs -f backend

# REBUILD
docker compose build backend && docker compose up -d backend

# STATUS
docker compose ps

# RESTART
docker compose restart backend
```

---

**Enjoy!** 🚀
