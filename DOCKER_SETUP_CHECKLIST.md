# Docker Setup Checklist

## Pre-Deployment Checklist

### Prerequisites ✓
- [ ] Docker installed on your machine
- [ ] Docker Compose installed
- [ ] Git installed and repository cloned
- [ ] GCP project with Cloud SQL instance
- [ ] Service account JSON key downloaded
- [ ] Minimum 4GB RAM allocated to Docker
- [ ] Ports 80 and 8000 available on your machine

### GCP Setup ✓
- [ ] Cloud SQL MySQL instance created
- [ ] Database tables initialized
- [ ] Service account created with Cloud SQL Client role
- [ ] Service account JSON key generated and downloaded
- [ ] Instance connection name known (format: `project:region:instance`)
- [ ] Database user and password noted

### Project Setup ✓
- [ ] Repository cloned locally
- [ ] Navigate to project root: `cd NextGenTeamBlue`
- [ ] Created `env/` directory: `mkdir -p env`
- [ ] Placed GCP key in `env/gcp-key.json`
- [ ] Set proper permissions: `chmod 600 env/gcp-key.json`
- [ ] Reviewed `.env.example` file
- [ ] Created `.env` file from example: `cp .env.example .env`
- [ ] Updated `.env` with your values:
  - [ ] `INSTANCE_CONNECTION_NAME` (from GCP)
  - [ ] `GCP_KEY_PATH` (should be `./env/gcp-key.json`)
  - [ ] `DB_USER` (from config.ini)
  - [ ] `DB_PASSWORD` (from config.ini)
  - [ ] `DB_NAME` (from config.ini)

### Verification ✓
- [ ] Verify `.env` file:
  ```bash
  cat .env
  ```
- [ ] Verify GCP key exists:
  ```bash
  ls -la env/gcp-key.json
  ```
- [ ] Verify GCP key is valid JSON:
  ```bash
  cat env/gcp-key.json | python -m json.tool > /dev/null && echo "Valid JSON"
  ```
- [ ] Verify Cloud SQL connection info is correct
- [ ] Verify config.ini database credentials match .env

## Deployment Steps

### Build Phase
- [ ] Navigate to project root
- [ ] Run build:
  ```bash
  docker-compose build
  ```
- [ ] Verify build succeeded without errors
- [ ] List images: `docker images | grep teamblue`

### Startup Phase
- [ ] Start services:
  ```bash
  docker-compose up -d
  ```
- [ ] Check service status:
  ```bash
  docker-compose ps
  ```
- [ ] Verify all services show "running"
- [ ] Wait 30-60 seconds for health checks to pass
- [ ] Review logs for any errors:
  ```bash
  docker-compose logs --tail=50
  ```

### Verification Phase
- [ ] Test backend API:
  ```bash
  curl http://localhost:8000/
  ```
- [ ] Test API documentation:
  ```bash
  curl http://localhost:8000/docs
  ```
- [ ] Test frontend:
  ```bash
  curl http://localhost:80/
  ```
- [ ] Open in browser:
  - [ ] Frontend: http://localhost
  - [ ] API Docs: http://localhost:8000/docs

### Database Connectivity
- [ ] Access backend container:
  ```bash
  docker exec -it teamblue-backend bash
  ```
- [ ] Test database connection:
  ```bash
  python -c "from src.database.database_connector import get_db_connection; \
             engine = get_db_connection(); \
             print('Connected!')"
  ```
- [ ] Exit container: `exit`
- [ ] Check backend logs for connection info:
  ```bash
  docker-compose logs backend | grep -i "connect\|sql"
  ```

### Application Testing
- [ ] Test creating asset (frontend):
  - [ ] Click "Add New Asset"
  - [ ] Fill in form
  - [ ] Click "Add Asset"
  - [ ] Verify success message
- [ ] Test asset list:
  - [ ] View all assets
  - [ ] Check data displays correctly
- [ ] Test search/filter:
  - [ ] Enter employee ID
  - [ ] Click search
  - [ ] Verify results filter
  - [ ] Click clear
  - [ ] Verify all assets display again
- [ ] Test asset update:
  - [ ] Select an asset
  - [ ] Click "Update Asset"
  - [ ] Modify data
  - [ ] Click "Update Asset"
  - [ ] Verify changes saved
- [ ] Test asset view:
  - [ ] Click on asset card
  - [ ] Verify all details display
  - [ ] Check decommission button (if active)

## Post-Deployment

### Documentation
- [ ] Read `DOCKER_GUIDE.md` for detailed information
- [ ] Read `DOCKER_SETUP_SUMMARY.md` for overview
- [ ] Keep `DOCKER_COMMANDS_REFERENCE.md` handy
- [ ] Review troubleshooting section

### Monitoring
- [ ] Set up log rotation (logs directory)
- [ ] Understand health check endpoints
- [ ] Know how to view logs: `docker-compose logs -f`
- [ ] Know how to restart services: `docker-compose restart`

### Backup & Recovery
- [ ] Backup `.env` file
- [ ] Backup GCP key location documented
- [ ] Know how to export database (if needed)
- [ ] Test recovery procedure

### Ongoing Maintenance
- [ ] Set schedule for Docker image updates
- [ ] Monitor disk usage: `docker system df`
- [ ] Monitor container memory/CPU: `docker stats`
- [ ] Review logs regularly
- [ ] Test backup/restore procedure monthly

## Troubleshooting Checklist

### If Services Won't Start
- [ ] Check Docker is running
- [ ] Check ports 80 and 8000 are available: `netstat -an | grep ':8000\|:80'`
- [ ] Check .env file exists and is valid
- [ ] Check GCP key exists: `ls -la env/gcp-key.json`
- [ ] View logs: `docker-compose logs`
- [ ] Try rebuilding: `docker-compose build --no-cache`
- [ ] Check Docker resources in preferences (min 4GB)

### If Backend Can't Connect to Database
- [ ] Verify INSTANCE_CONNECTION_NAME in .env
- [ ] Verify GCP key has Cloud SQL Client role
- [ ] Verify database user/password in .env match Cloud SQL
- [ ] Test database manually from GCP console
- [ ] Check backend logs: `docker-compose logs backend | grep -i "sql\|connect"`
- [ ] Verify service account key is valid JSON

### If Frontend Can't Connect to Backend
- [ ] Verify backend is running: `docker-compose ps`
- [ ] Test backend directly: `curl http://localhost:8000/`
- [ ] Check nginx.conf reverse proxy settings
- [ ] Check browser console for errors (F12)
- [ ] View frontend logs: `docker-compose logs frontend`
- [ ] Verify internal network: `docker network ls`

### If Database Queries Fail
- [ ] Check database tables exist
- [ ] Verify database user has proper permissions
- [ ] Test query directly via Cloud SQL console
- [ ] Check Cloud SQL SQL editor for table structure
- [ ] Verify config.ini database credentials

## Quick Restart After System Reboot

```bash
# 1. Open terminal in project directory
cd ~/NextGenTeamBlue  # or your path

# 2. Start Docker Desktop (if not auto-starting)
# Mac: open /Applications/Docker.app
# Windows: Click Docker Desktop
# Linux: sudo systemctl start docker

# 3. Start services
docker-compose up -d

# 4. Verify
docker-compose ps

# 5. Access
# Frontend: http://localhost
# API: http://localhost:8000
```

## Common Issues Quick Fixes

| Issue | Command to Try |
|-------|-----------------|
| Port already in use | `docker-compose down && docker-compose up -d` |
| Services not healthy | `docker-compose restart && docker-compose logs` |
| Database connection error | `docker-compose logs backend \| grep -i error` |
| Frontend not loading | `docker exec teamblue-frontend nginx -t` |
| Out of disk space | `docker system prune -a` |
| Services keep restarting | `docker-compose logs \| tail -50` |
| Memory issues | Increase Docker memory limit (Docker Desktop preferences) |

## Success Criteria ✓

Your deployment is successful when:
- [ ] `docker-compose ps` shows all containers "Up"
- [ ] `curl http://localhost:8000/` returns 200 status
- [ ] Frontend loads at http://localhost
- [ ] All pages render without errors
- [ ] API calls work (check browser Network tab)
- [ ] Database queries execute successfully
- [ ] Search/filter functionality works
- [ ] Asset creation/update/deletion works
- [ ] No critical errors in logs

## Next Steps

After successful deployment:
1. [ ] Set up monitoring and alerting
2. [ ] Configure backup schedule
3. [ ] Plan for scaling
4. [ ] Set up CI/CD pipeline
5. [ ] Document deployment procedures
6. [ ] Train team on Docker commands
7. [ ] Plan production deployment strategy
8. [ ] Schedule security scanning

## Support Resources

- **Docker Documentation**: https://docs.docker.com/
- **GCP Cloud SQL Docs**: https://cloud.google.com/sql/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Vue 3 Docs**: https://vuejs.org/
- **GitHub Issues**: Check repository for known issues

---

**Last Updated**: December 9, 2025
**Status**: Ready for Production

Once you've completed this checklist, your application should be fully running in Docker!
