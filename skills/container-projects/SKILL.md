---
name: container-projects
description: Guidelines for containerized projects using Docker, Docker Compose, and container orchestration. Activate when working with Dockerfiles, docker-compose.yml, container images, Kubernetes manifests, or any container-based development and deployment workflows.
---

# Container-Based Projects

**Auto-activate when:** Working with `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `.dockerignore`, Kubernetes manifests (`*.yaml`, `*.yml` in k8s directories), container registries, or when user mentions Docker, containers, orchestration, or deployment workflows.

Guidelines for containerized applications using Docker, Docker Compose, and orchestration tools.

## CRITICAL: Docker Compose V2 Syntax

**NEVER use `version:` field** (deprecated) **or `docker-compose` with hyphen:**

```yaml
# ❌ WRONG
version: '3.8'
services:
  app:
    image: myapp

# ✅ CORRECT
services:
  app:
    image: myapp
```

```bash
docker compose up    # ✅ CORRECT
docker-compose up    # ❌ WRONG
```

## CRITICAL: DNS Configuration

```yaml
# ✅ ALWAYS use .internal for container DNS
services:
  app:
    environment:
      - DNS_DOMAIN=.internal

# ❌ NEVER use .local (conflicts with mDNS/Bonjour)
```

## Security Checklist

- Run as non-root user (USER directive)
- Use minimal Alpine-based images
- Never hardcode secrets or commit credentials
- Validate all input, even from trusted sources
- Include health checks for orchestration
- Use Docker secrets for sensitive data in production

## Project Structure Recognition

**Key files:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.devcontainer/`, `Makefile`, `k8s/`

## Workflow Patterns

**Before starting:** Check README, Makefile, docker-compose.yml, .env files

**Command hierarchy:** Makefile → Project scripts → Docker commands

## Base Image Selection

```dockerfile
# ✅ CORRECT - Minimal Alpine images
FROM alpine:latest
FROM python:3.11-alpine
FROM node:20-alpine

# ❌ WRONG - Large images with more vulnerabilities
FROM ubuntu:latest
FROM python:3.11
FROM node:20
```

## 12-Factor App Compliance

| Factor | Implementation |
|--------|---------------|
| Configuration | Environment variables only, never hardcoded |
| Dependencies | Explicit declarations with lockfiles |
| Stateless | No local state, horizontally scalable |
| Port Binding | Self-contained, exports via port binding |
| Disposability | Fast startup/shutdown, graceful termination |
| Dev/Prod Parity | Keep environments similar |

## Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build
FROM python:3.11-alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-dev

# Stage 2: Runtime
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

## Health Checks

```dockerfile
# HTTP service
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Database
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD pg_isready -U postgres || exit 1
```

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

## Docker Compose File Organization

```
project/
├── docker-compose.yml
├── compose/
│   ├── dev.yml
│   ├── service1.yml
│   └── service2.yml
├── .env
├── .env.development
└── .env.production
```

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

| Aspect | Development | Production |
|--------|-------------|------------|
| Base Image | Full OS for debugging | Alpine (minimal) |
| Code Mount | Volume mount for hot reload | Copied into image |
| Dependencies | Include dev tools | Runtime only |
| Ports | Exposed for debugging | Necessary only |
| Restart | no (manual control) | unless-stopped |
| Logging | DEBUG | INFO/WARN |

```yaml
# compose/dev.yml
services:
  app:
    build:
      target: development
    volumes:
      - .:/workspace:cached
    command: python run.py --reload
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=debug
```

## DevContainer Configuration

```json
{
  "name": "Project Dev Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "dev",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
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

## Makefile Integration Pattern

```makefile
.PHONY: dev build up down logs
dev:
	@docker compose -f docker-compose.yml -f compose/dev.yml up
build:
	@docker compose build
up:
	@docker compose up -d
down:
	@docker compose down
logs:
	@docker compose logs -f

# Pattern rules
run-%:
	@docker compose -f docker-compose.yml -f compose/$*.yml up
stop-%:
	@docker compose stop $*
```

## .dockerignore Best Practices

```
.git
__pycache__
*.pyc
.pytest_cache
.venv
*.egg-info
node_modules/
.devcontainer
.vscode
*.log
.env.local
*.md
!README.md
docker-compose*.yml
Dockerfile*
.coverage
.DS_Store
```

## Network Configuration

```yaml
networks:
  app_network:
    driver: bridge
  db_network:
    driver: bridge
    internal: true  # No external access
```

## Common Container Patterns

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  db:
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```

## Git Submodules in Containers

```dockerfile
RUN git clone --recurse-submodules https://github.com/user/repo.git
# Or: RUN git submodule update --init --recursive
```

## Essential Docker Commands

```bash
# Service management
docker compose up / up -d / down / down -v
docker compose restart app
docker compose build / build --no-cache

# Monitoring
docker compose ps / logs -f / logs -f app
docker stats

# Execute commands
docker compose exec app sh
docker compose run --rm app pytest

# Cleanup
docker image prune -a
docker system prune
```

## Quick Reference

**Before running containers:**
- Check README and Makefile
- Review docker-compose.yml dependencies
- Check for .env.example
- Understand dev vs production configs

**Common mistakes:**
- Using `version:` field or `docker-compose` with hyphen
- Running as root user
- Using large base images (not Alpine)
- Committing secrets
- Using `.local` domain
- Skipping health checks

---

**Note:** Container projects vary in complexity. Always check project-specific documentation before making changes to Docker configurations.
