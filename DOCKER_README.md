# Email Detection - Docker Setup

Complete Docker containerization with Nginx reverse proxy for the Email Classification system.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Browser (localhost:80)           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Nginx Reverse Proxy (Port 80)      │
│  ✓ Static file serving                  │
│  ✓ API routing to backend               │
│  ✓ SSL/TLS termination                  │
└────┬──────────────────────────────┬────┘
     │                              │
┌────▼──────────────────┐  ┌────────▼──────────────────┐
│  Frontend Container   │  │  Backend Container        │
│  - Node 18 builder    │  │  - Python 3.11            │
│  - React build        │  │  - FastAPI + Uvicorn      │
│  - Nginx serving      │  │  - ML models loaded       │
│  (Port 3000:80)       │  │  (Port 8000)              │
└──────────────────────┘  └───────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### Access the Application

- **Frontend**: http://localhost:80 (via Nginx proxy)
- **Backend API**: http://localhost:8000 (direct access)
- **Nginx health check**: http://localhost/health

### Stop Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 📦 Services Overview

### Backend Service
- **Image**: Python 3.11 slim
- **Build**: Multi-stage build for optimized size
- **Features**:
  - FastAPI application
  - Uvicorn ASGI server
  - Health check endpoint
  - Model & vectorizer loaded
- **Environment**: 
  - `PYTHONUNBUFFERED=1`
  - `PYTHONDONTWRITEBYTECODE=1`
- **Volumes**: `./backend:/app` (for development)
- **Network**: `app-network`

### Frontend Service
- **Image**: Node 18 Alpine (builder) → Nginx Alpine
- **Build**: Multi-stage build
  - Stage 1: Node.js build environment
  - Stage 2: Nginx serving
- **Features**:
  - React production build
  - Optimized Nginx configuration
  - Static asset caching
- **Network**: `app-network`

### Nginx Service
- **Image**: Nginx Alpine
- **Port**: 80 (HTTP), 443 (HTTPS-ready)
- **Features**:
  - Reverse proxy to backend
  - Static file serving
  - API routing (`/api/*` → backend)
  - SSL/TLS support (add certificates to `./ssl/`)
  - Cache headers for static assets
  - Health check endpoint
- **Configuration**: `./nginx.conf`

## 🔧 Configuration

### Environment Variables

Create `.env` file in the root directory:

```env
# Backend
BACKEND_PORT=8000
PYTHONUNBUFFERED=1

# Frontend
FRONTEND_PORT=3000

# Nginx
NGINX_PORT=80
```

### Nginx Configuration

Edit `nginx.conf` to:
- Add SSL/TLS certificates
- Modify proxy headers
- Configure caching policies
- Add rate limiting

### Backend Configuration

Edit `backend/requirements.txt` to add/remove dependencies:

```txt
fastapi==0.123.5
uvicorn==0.38.0
scikit-learn==1.7.2
```

### Frontend Configuration

Edit `frontend/Dockerfile` to:
- Change Node.js version
- Add build arguments
- Modify Nginx image

## 🛠️ Development Tips

### Hot Reload Backend

The backend container has volumes mounted for development:

```yaml
volumes:
  - ./backend:/app
```

Changes to `app.py` will auto-reload with `--reload` flag.

### Rebuild Services

```bash
# Rebuild backend only
docker-compose build backend

# Rebuild frontend only
docker-compose build frontend

# Rebuild all
docker-compose build

# Rebuild without cache
docker-compose build --no-cache
```

### Execute Commands in Container

```bash
# Run Python in backend
docker-compose exec backend python -c "import app; print('OK')"

# Run npm in frontend
docker-compose exec frontend npm list

# Access bash in backend
docker-compose exec backend /bin/bash
```

### View Container Stats

```bash
# Monitor resource usage
docker stats

# List running containers
docker ps

# Inspect service
docker-compose exec backend python -c "import sys; print(sys.version)"
```

## 📊 Health Checks

All services have health checks configured:

```bash
# Check backend health
curl http://localhost:8000/health

# Check Nginx health
curl http://localhost/health

# Check frontend
curl http://localhost/
```

## 🔒 Production Deployment

### SSL/TLS Setup

1. Add certificates to `./ssl/` directory
2. Update `nginx.conf`:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
}
```

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
  frontend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

### Logging

Configure logging driver in `docker-compose.yml`:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Environment-Specific Builds

```bash
# Production build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging build
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

## 🐛 Troubleshooting

### Backend not connecting to frontend

Check network:
```bash
docker network ls
docker network inspect app_network
```

### Nginx 502 Bad Gateway

```bash
# Check backend is running
docker-compose logs backend

# Verify backend health
docker-compose exec nginx wget -O- http://backend:8000/health
```

### Port already in use

```bash
# Find process using port
lsof -i :80
lsof -i :8000
lsof -i :3000

# Or use docker to free ports
docker-compose down
```

### Clear Docker cache

```bash
docker system prune -a
docker volume prune
```

## 📋 File Structure

```
email-detection/
├── docker-compose.yml          # Docker Compose orchestration
├── nginx.conf                  # Nginx reverse proxy config
│
├── backend/
│   ├── Dockerfile              # Multi-stage backend build
│   ├── .dockerignore
│   ├── requirements.txt        # Python dependencies
│   ├── app.py                  # FastAPI application
│   ├── model.pkl               # ML model
│   └── vectorizer.pkl          # TF-IDF vectorizer
│
└── frontend/
    ├── Dockerfile              # Multi-stage frontend build
    ├── .dockerignore
    ├── package.json
    ├── public/
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    └── nginx.conf              # Frontend Nginx (deprecated - use root nginx.conf)
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Images
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build with Docker Compose
        run: docker-compose build
      - name: Push to registry
        run: docker-compose push
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

## 🤝 Support

For issues with Docker setup, check:
1. Docker is running: `docker ps`
2. Services are healthy: `docker-compose ps`
3. Logs: `docker-compose logs -f [service]`
4. Network connectivity: `docker network inspect app_network`

---

**Last Updated**: December 3, 2025
