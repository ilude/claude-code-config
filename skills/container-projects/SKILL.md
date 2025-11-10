---
name: container-projects
description: Guidelines for containerized projects using Docker, Docker Compose, and container orchestration. Activate when working with Dockerfiles, docker-compose.yml, container images, Kubernetes manifests, or any container-based development and deployment workflows.
---

# Container-Based Projects

Guidelines for containerized applications using Docker, Docker Compose, and orchestration tools.

## CRITICAL: Docker Compose V2 Syntax

**NEVER use `version:` field in docker-compose.yml - it is deprecated:**

```yaml
# ❌ WRONG - Version field is deprecated
version: '3.8'
services:
  app:
    image: myapp

# ✅ CORRECT - Omit version field entirely
services:
  app:
    image: myapp
```

**ALWAYS use Docker Compose V2 commands (no hyphen):**

```bash
# ✅ CORRECT - Modern syntax
docker compose up
docker compose down
docker compose ps

# ❌ WRONG - Old syntax with hyphen
docker-compose up
docker-compose down
```

## Project Structure Recognition

**Container configuration files:**
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Files excluded from image
- `.devcontainer/` - Dev container configuration
- `Makefile` - Common commands and shortcuts
- `k8s/` or `kubernetes/` - Kubernetes manifests

**Environment detection:**
- Different Dockerfiles: `Dockerfile.dev`, `Dockerfile.prod`
- Multiple compose files: `compose/dev.yml`, `compose/service1.yml`
- Environment files: `.env`, `.env.development`, `.env.production`

## Workflow Patterns

**Before starting work:**

1. Check README for build/run instructions
2. Look for Makefile with common commands
3. Review docker-compose.yml for service architecture
4. Identify environment variables and .env files
5. Understand dev vs production configurations

**Preferred command hierarchy:**
1. Makefile targets: `make build`, `make up`, `make test`
2. Project scripts: `scripts/build.sh`, `scripts/start.sh`
3. Standard Docker commands if no custom workflow

## Security-First Container Practices

**CRITICAL security requirements:**

```dockerfile
# ✅ ALWAYS run as non-root user
FROM python:3.11-alpine
RUN adduser -D appuser
USER appuser

# ✅ Use minimal base images
FROM alpine:latest              # Minimal attack surface
FROM python:3.11-alpine         # Python on Alpine
FROM node:20-alpine             # Node on Alpine

# ❌ NEVER use
FROM ubuntu:latest              # Too large, more vulnerabilities
USER root                       # Security risk in production
```

**Security checklist:**
- Run containers as non-root users (add USER directive)
- Use minimal Alpine-based images
- Never expose secrets in logs or error messages
- Validate all input, even from trusted sources
- Include health checks for container orchestration
- Never commit secrets in Dockerfiles or compose files
- Use Docker secrets for sensitive data in production

## 12-Factor App Compliance

**Apply these principles to containerized applications:**

| Factor | Implementation |
|--------|---------------|
| Configuration | All config via environment variables, never hardcoded |
| Dependencies | Explicitly declared (pyproject.toml, package.json) with lockfiles |
| Stateless | No local state, horizontally scalable |
| Port Binding | Self-contained service exports HTTP via port binding |
| Disposability | Fast startup/shutdown, graceful process termination |
| Dev/Prod Parity | Keep development and production as similar as possible |

**Environment variable patterns:**
```bash
# In .env or docker-compose.yml
SERVICE_NAME_CONFIG_VAR=value    # Prefix with service name
DATABASE_URL=postgresql://...    # Connection strings
LOG_LEVEL=info                   # Runtime config
API_KEY=${API_KEY}               # Pass from host environment
```

## Multi-Stage Build Pattern

**Use multi-stage builds to reduce image size:**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-dev

# Stage 2: Runtime image
FROM python:3.11-alpine
RUN adduser -D appuser
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY . .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "run.py"]
```

**Dockerfile best practices:**
- Use multi-stage builds to minimize final image size
- Copy only necessary files (use .dockerignore)
- Layer caching: Put frequently changing files last
- Add health checks for orchestration
- Use EXPOSE for documentation
- Clean entry point (run.py, not inline commands)
- Combine RUN commands to reduce layers
- Clean up package manager cache in same layer

## Health Checks

**Container health check patterns:**

```dockerfile
# HTTP health check (web services)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Python script health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Database health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD pg_isready -U postgres || exit 1

# DNS service health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD nslookup test.internal localhost || exit 1
```

**In docker-compose.yml:**
```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Health check endpoint requirements:**
- Fast response (<1s)
- Check critical dependencies (database, cache, etc.)
- Return 200 OK when healthy
- Return 503 Service Unavailable when unhealthy

## Docker Compose File Organization

**Multi-environment structure:**

```
project/
├── docker-compose.yml          # Base/production config
├── compose/
│   ├── dev.yml                # Development overrides
│   ├── service1.yml           # Individual service configs
│   └── service2.yml
├── .env                        # Default environment
├── .env.development            # Development environment
├── .env.production             # Production environment
└── .dockerignore
```

**Complete docker-compose.yml example:**

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app_network

volumes:
  db_data:

networks:
  app_network:
    driver: bridge
```

## Development Workflow

**Development vs Production:**

| Aspect | Development | Production |
|--------|-------------|------------|
| Base Image | Full OS for debugging | Alpine (minimal) |
| Code Mount | Volume mount for hot reload | Copied into image |
| Dependencies | Include dev tools | Only runtime dependencies |
| Ports | Exposed for debugging | Only necessary ports |
| Restart | no (manual control) | unless-stopped |
| Logging | Verbose (DEBUG) | Production level (INFO/WARN) |

**Development compose override:**

```yaml
# compose/dev.yml
services:
  app:
    build:
      target: development
    volumes:
      - .:/workspace:cached      # Mount source for hot reload
    command: python run.py --reload
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=debug
    ports:
      - "5678:5678"              # Debug port
```

**Run development environment:**
```bash
# With Makefile
make dev

# Or manually
docker compose -f docker-compose.yml -f compose/dev.yml up
```

## DevContainer Configuration

**Basic .devcontainer/devcontainer.json:**

```json
{
  "name": "Project Dev Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "dev",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "zsh"
      },
      "extensions": [
        "ms-python.python",
        "ms-azuretools.vscode-docker"
      ]
    }
  },
  "postCreateCommand": "pip install -e .[dev]",
  "remoteUser": "appuser"
}
```

**DevContainer best practices:**
- Use zsh with autosuggestions for better shell experience
- Mount source code for hot reload
- Configure debugging in devcontainer.json
- Run as non-root user
- Include necessary VS Code extensions

## Makefile Integration Pattern

**Pattern rules for service management:**

```makefile
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make dev        - Start development environment"
	@echo "  make build      - Build all images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - Follow all logs"
	@echo "  make run-<svc>  - Start specific service"

# Development environment
.PHONY: dev
dev:
	@docker compose -f docker-compose.yml -f compose/dev.yml up

# Build all services
.PHONY: build
build:
	@docker compose build

# Start all services
.PHONY: up
up:
	@docker compose up -d

# Stop all services
.PHONY: down
down:
	@docker compose down

# Follow logs
.PHONY: logs
logs:
	@docker compose logs -f

# Pattern rule: run specific service
run-%:
	@docker compose -f docker-compose.yml -f compose/$*.yml up

# Pattern rule: start service in background
start-%:
	@docker compose -f docker-compose.yml -f compose/$*.yml up -d

# Pattern rule: stop specific service
stop-%:
	@docker compose stop $*
```

## .dockerignore Best Practices

**Essential .dockerignore patterns:**

```
# Version control
.git
.gitignore
.gitattributes

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.venv
*.egg-info
dist/
build/

# Node.js
node_modules/
npm-debug.log
yarn-error.log

# Development
.devcontainer
.vscode
.idea
*.log
.env.local

# Documentation
*.md
!README.md

# Docker
docker-compose*.yml
Dockerfile*
.dockerignore

# Testing
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
```

## DNS and Network Configuration

**CRITICAL DNS patterns:**

```yaml
# ✅ ALWAYS use .internal for container DNS
services:
  app:
    environment:
      - DNS_DOMAIN=.internal

# ❌ NEVER use .local (conflicts with mDNS/Bonjour)
# WRONG: DNS_DOMAIN=.local
```

**Network configuration:**
```yaml
networks:
  default:
    name: project_network
    driver: bridge

# Custom network for isolation
networks:
  app_network:
    driver: bridge
  db_network:
    driver: bridge
    internal: true  # No external access
```

## Common Container Patterns

**Multi-container applications:**
- Web + Database + Cache (app + PostgreSQL + Redis)
- Microservices architecture
- Service dependencies with health checks

**Service discovery and dependencies:**
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:alpine
```

**Volume management:**
```yaml
volumes:
  db_data:              # Named volume for persistence
  cache_data:

services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data

  cache:
    volumes:
      - cache_data:/data
```

**Resource limits:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Git Submodules in Containers

**When project uses submodules:**

```dockerfile
# Clone with submodules
RUN git clone --recurse-submodules https://github.com/user/repo.git

# Or update submodules in existing clone
RUN git submodule update --init --recursive
```

**Development workflow:**
```bash
# Work on submodule
cd /workspace/submodule
git add . && git commit -m "feat: update"
git push origin main

# Update parent to use latest
cd /workspace
git submodule update --remote submodule
git add submodule
git commit -m "chore: update submodule"
```

## Essential Docker Commands

**Compose operations:**
```bash
# Service management
docker compose up                    # Start services
docker compose up -d                 # Start in background
docker compose down                  # Stop and remove
docker compose down -v               # Stop and remove volumes
docker compose restart app           # Restart specific service

# Monitoring
docker compose ps                    # List containers
docker compose logs -f               # Follow all logs
docker compose logs -f app           # Follow specific service logs
docker compose top                   # Show running processes

# Maintenance
docker compose build                 # Build all images
docker compose build --no-cache      # Build without cache
docker compose pull                  # Pull latest images
```

**Container management:**
```bash
# Execute commands
docker compose exec app sh           # Shell into running container
docker compose exec app python       # Run Python in container
docker compose run --rm app pytest   # Run tests in new container

# Debugging
docker logs -f container_name        # Follow logs
docker inspect container_name        # Inspect configuration
docker stats                         # Resource usage
docker exec -it container_name sh    # Shell into container
```

**Image management:**
```bash
docker images                        # List images
docker build -t image_name .         # Build image
docker rmi image_name                # Remove image
docker image prune -a                # Remove unused images
docker system prune                  # Clean up everything
```

## Quick Reference

**Before running containers:**
- Check README for build instructions
- Look for Makefile with common commands
- Check for .env.example or .env.template
- Understand dev vs production configurations
- Review docker-compose.yml service dependencies

**Development best practices:**
- Use provided Makefile targets if available
- Respect existing Dockerfile patterns
- Don't modify base images without discussion
- Follow established volume mount patterns
- Use health checks for service dependencies
- Keep dev/prod environments similar

**Common mistakes to avoid:**
- Using deprecated `version:` field in compose files
- Using old `docker-compose` syntax (should be `docker compose`)
- Running containers as root user
- Using large base images instead of Alpine
- Committing secrets in Dockerfiles or compose files
- Ignoring existing Makefile commands
- Modifying production configs for dev convenience
- Using `.local` domain (conflicts with mDNS)
- Skipping health checks
- Not using multi-stage builds

**Security checklist:**
- Always run as non-root user (USER directive)
- Use minimal Alpine-based images
- Never hardcode secrets
- Validate all input
- Include health checks
- Use HTTPS for external connections
- Scan images for vulnerabilities
- Keep base images updated

---

**Note:** Container projects vary in complexity. Always check project-specific documentation before making changes to Docker configurations.
