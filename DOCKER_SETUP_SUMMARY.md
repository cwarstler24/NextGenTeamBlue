# Docker Deployment Summary for NextGenTeamBlue

## Quick Start (TL;DR)

```bash
# 1. Setup credentials
cp .env.example .env
# Edit .env with your GCP details
# Place GCP key at: env/gcp-key.json

# 2. Deploy
chmod +x docker-startup.sh
./docker-startup.sh setup

# 3. Access
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

## What Was Created

### Core Docker Files

1. **Dockerfile.backend** - Python 3.11 FastAPI container
   - Installs system dependencies (MySQL client)
   - Installs Python requirements
   - Runs Uvicorn on port 8000
   - Includes health checks

2. **Dockerfile.frontend** - Multi-stage Vue 3 build
   - Stage 1: Build Vue app with Vite (Node 22)
   - Stage 2: Serve with Nginx Alpine
   - Runs on port 80
   - Includes health checks

3. **docker-compose.yml** - Development configuration
   - Backend service (FastAPI)
   - Frontend service (Nginx)
   - Shared network for inter-service communication
   - Volume mounts for logs and credentials

4. **docker-compose.prod.yml** - Production configuration
   - Resource limits and reservations
   - Always restart policy
   - Health checks configured
   - Optimized for stability

### Configuration Files

5. **nginx.conf** - Reverse proxy configuration
   - Serves Vue SPA with proper routing
   - Proxies API requests to backend
   - Handles /resources/ endpoints
   - Includes health check endpoint

6. **.env.example** - Environment template
   - GCP instance connection name
   - Database credentials
   - Credentials path
   - Port configurations

7. **DOCKER_GUIDE.md** - Comprehensive documentation
   - Architecture diagram
   - Setup instructions
   - Configuration details
   - Troubleshooting guide
   - Production deployment tips

### Management Script

8. **docker-startup.sh** - Interactive management script
   - Prerequisites checking
   - GCP credentials validation
   - Automated setup
   - Service management (start/stop/restart)
   - Logs viewing
   - Status monitoring

## How It Works

### Architecture

```
Internet → Nginx (Port 80) → Vue SPA + Reverse Proxy
                                    ↓
                            FastAPI Backend (Port 8000)
                                    ↓
                            Google Cloud SQL MySQL
```

### Google Cloud SQL Integration

**Connection Method**: Cloud SQL Python Connector with Public IP
- Located in: `backend/src/database/database_connector.py`
- Uses service account authentication
- Automatically handles SSL/TLS
- Supports both public and private IPs

**How it works**:
1. Container starts with GCP credentials mounted
2. Backend loads credentials from `GOOGLE_APPLICATION_CREDENTIALS`
3. Cloud SQL Connector authenticates to GCP
4. Secure connection established to Cloud SQL instance
5. Application queries database through SQLAlchemy

### Service Communication

**Within Docker Network** (`teamblue-network`):
- Frontend (Nginx) → Backend (FastAPI): `http://backend:8000`
- External → Frontend: `http://localhost:80`
- External → Backend: `http://localhost:8000`

**To Google Cloud SQL**:
- Backend → Cloud SQL: Via Cloud SQL Python Connector (public or private IP)
- GCP handles authentication and encryption

## Deployment Steps

### Step 1: Prepare GCP Credentials
```bash
# Get your service account JSON key from GCP Console
# Place it in the repository
mkdir -p env
cp ~/Downloads/your-gcp-key.json env/gcp-key.json
chmod 600 env/gcp-key.json  # Secure the file
```

### Step 2: Configure Environment
```bash
cp .env.example .env

# Edit .env:
# - Set INSTANCE_CONNECTION_NAME (from Cloud SQL console)
# - Set GCP_KEY_PATH (typically ./env/gcp-key.json)
# - Set DB credentials (from config.ini)
```

### Step 3: Verify Prerequisites
```bash
# Install Docker Desktop from https://www.docker.com/products/docker-desktop
# Or install Docker Engine: https://docs.docker.com/engine/install/

# Verify installation
docker --version
docker-compose --version
```

### Step 4: Build and Deploy
```bash
# Option A: Using the startup script (recommended)
chmod +x docker-startup.sh
./docker-startup.sh setup

# Option B: Manual commands
docker-compose build
docker-compose up -d
```

### Step 5: Verify Deployment
```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Test endpoints
curl http://localhost:8000/          # Backend health
curl http://localhost:80/            # Frontend health
curl http://localhost:8000/docs      # API documentation
```

## Common Tasks

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service (last 50 lines)
docker-compose logs --tail=50 backend

# Follow in real-time
docker-compose logs -f frontend
```

### Rebuild After Code Changes
```bash
# Rebuild backend only
docker-compose build backend
docker-compose up -d backend

# Rebuild frontend only
docker-compose build frontend
docker-compose up -d frontend

# Rebuild everything
docker-compose build
docker-compose up -d
```

### Access Container
```bash
# Connect to backend container
docker exec -it teamblue-backend bash

# Test database connection
python -c "from src.database.database_connector import get_db_connection; \
           engine = get_db_connection(); print('Database connected!')"

# Run Python queries
python -c "from src.database.database_connector import get_db_connection; \
           import sqlalchemy; \
           engine = get_db_connection(); \
           with engine.connect() as conn: \
               result = conn.execute(sqlalchemy.text('SELECT COUNT(*) FROM Employee')); \
               print(result.fetchall())"
```

### Stop Services
```bash
# Graceful shutdown
docker-compose down

# Stop but keep volumes
docker-compose stop

# Restart all
docker-compose restart
```

## Troubleshooting

### "Failed to connect to Cloud SQL"
**Problem**: Backend can't reach Google Cloud SQL
```bash
# Check:
1. GCP key file exists and is valid
2. Service account has Cloud SQL Client role
3. INSTANCE_CONNECTION_NAME is correct
4. Database user and password are correct

# Debug:
docker-compose logs backend | grep -i "sql\|connector\|auth"
```

### "Cannot GET /" (Frontend Error)
**Problem**: Frontend can't load
```bash
# Check:
1. Backend is running and accessible
2. Nginx configuration is correct
3. Frontend is healthy

# Debug:
docker-compose logs frontend
curl http://localhost:8000/  # Should work
docker-compose exec frontend nginx -t  # Test nginx config
```

### API Calls Failing from Frontend
**Problem**: Frontend → Backend communication issue
```bash
# Check:
1. Backend is running on port 8000
2. Nginx is configured to proxy to backend
3. Check CORS settings in backend

# Debug:
docker exec -it teamblue-frontend bash
# Inside container:
curl http://backend:8000/resources/  # Should work
```

### Container Won't Start
**Problem**: Services fail on startup
```bash
# Check logs
docker-compose logs -f

# Rebuild without cache
docker-compose build --no-cache

# Check Docker resources
docker system df

# Increase Docker memory if needed:
# Docker Desktop → Preferences → Resources
```

## Security Considerations

### Credential Management
✅ **Do**:
- Store `.env` in secure location
- Use `.gitignore` to prevent credential commits
- Rotate GCP service account keys regularly
- Set proper file permissions on key: `chmod 600`

❌ **Don't**:
- Commit `.env` or `gcp-key.json` to version control
- Share credentials in chat/email
- Use same credentials for multiple environments
- Store credentials in Docker images

### Network Security
- Services communicate over internal Docker network (not exposed)
- Only frontend (port 80) and backend (port 8000) exposed
- Cloud SQL uses SSL/TLS encryption
- GCP service account authentication

### Production Recommendations
1. Use Docker secrets instead of environment variables
2. Deploy behind load balancer with SSL/TLS
3. Use private Cloud SQL IP in VPC
4. Enable Cloud SQL Proxy for additional security
5. Implement network policies in Kubernetes
6. Regular security updates for base images
7. Scan images for vulnerabilities: `docker scan`

## Deployment Environments

### Development (Current Setup)
```bash
# Use docker-compose.yml
docker-compose up -d
```

### Production
```bash
# Use docker-compose.prod.yml with resource limits
docker-compose -f docker-compose.prod.yml up -d
```

### Google Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/teamblue-backend

# Deploy
gcloud run deploy teamblue-backend \
  --image gcr.io/PROJECT_ID/teamblue-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars INSTANCE_CONNECTION_NAME=project:region:instance
```

### Kubernetes (GKE)
```bash
# Push images to registry
docker tag teamblue-backend:latest gcr.io/PROJECT_ID/teamblue-backend
docker push gcr.io/PROJECT_ID/teamblue-backend

# Deploy manifest
kubectl apply -f k8s-deployment.yaml
```

## File Organization

```
NextGenTeamBlue/
├── Dockerfile.backend           # Backend image definition
├── Dockerfile.frontend          # Frontend image definition
├── docker-compose.yml           # Dev deployment
├── docker-compose.prod.yml      # Prod deployment
├── docker-startup.sh            # Management script
├── nginx.conf                   # Frontend reverse proxy
├── .env.example                 # Configuration template
├── DOCKER_GUIDE.md              # Detailed documentation
├── backend/
│   ├── requirements.txt         # Python dependencies
│   ├── config.ini               # Backend config
│   └── src/
│       └── database/
│           └── database_connector.py  # Cloud SQL connection
├── frontend/
│   ├── package.json             # Node dependencies
│   └── src/
├── env/
│   └── gcp-key.json            # GCP credentials (NEVER commit!)
└── logs/
    └── backend/                 # Application logs
```

## Monitoring & Health Checks

### Container Health
```bash
# View container status
docker-compose ps

# Inspect container health
docker inspect teamblue-backend --format='{{.State.Health.Status}}'
```

### Application Monitoring
```bash
# Backend logs
docker-compose logs --tail=100 backend

# Frontend access logs (via Nginx)
docker-compose logs frontend

# Check resource usage
docker stats
```

### Database Connectivity Test
```bash
# Connect to backend and test DB
docker exec teamblue-backend python -c \
  "from src.database.database_connector import get_db_connection; \
   engine = get_db_connection(); \
   print('✓ Database connection successful!')"
```

## Support & Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Cloud SQL Python Connector**: https://github.com/GoogleCloudPlatform/cloud-sql-python-connector
- **FastAPI**: https://fastapi.tiangolo.com/
- **Vue 3**: https://vuejs.org/
- **Nginx**: https://nginx.org/

## Next Steps

1. ✅ Set up Docker environment
2. ✅ Configure .env with your credentials
3. ✅ Build and run containers
4. ✅ Test application
5. ☐ Set up monitoring and logging
6. ☐ Configure CI/CD pipeline
7. ☐ Deploy to production environment
8. ☐ Set up auto-scaling policies
9. ☐ Enable backup and disaster recovery
10. ☐ Implement security scanning

---

**Questions?** Check `DOCKER_GUIDE.md` for comprehensive documentation or review the inline comments in Dockerfiles.
