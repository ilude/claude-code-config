---
name: container-projects
description: Guidelines for containerized projects using Docker, Docker Compose, and container orchestration. Activate when working with Dockerfiles, docker-compose.yml, container images, Kubernetes manifests, or any container-based development and deployment workflows.
---

# Container-Based Projects

Guidelines for working with containerized applications and Docker-based projects.

## Project Structure Recognition

### Container Configuration Files
- `Dockerfile` - Container image definition
- `docker-compose.yml` or `docker-compose.yaml` - Multi-container orchestration
- `.dockerignore` - Files to exclude from image
- `Makefile` - Common commands and shortcuts
- `k8s/` or `kubernetes/` - Kubernetes manifests

### Environment Detection
- Development vs Production configurations
- Different Dockerfiles: `Dockerfile.dev`, `Dockerfile.prod`
- Multiple compose files: `docker-compose.override.yml`

## Workflow Patterns

### Before Starting Work
1. **Check README** - Build and run instructions specific to this project
2. **Look for Makefile** - Common commands may be aliased
3. **Check docker-compose.yml** - Understand service architecture
4. **Identify environment variables** - `.env` files for container configuration

### Common Commands
Respect the project's preferred workflow:
- Check for `Makefile` targets: `make build`, `make up`, `make test`
- Standard Docker commands if no Makefile
- Project-specific scripts in `scripts/` directory

## Development Workflow

### Building and Running
```bash
# Check for Makefile first
make build
make up

# Or standard Docker Compose
docker-compose build
docker-compose up

# Or Docker
docker build -t app-name .
docker run app-name
```

### Development vs Production
- **Development**: Hot reload, volume mounts, debug ports
- **Production**: Optimized images, no dev dependencies, security hardening
- Check which Dockerfile/compose file is for which environment

## Best Practices

### Image Building
- Respect existing Dockerfile patterns
- Don't change base images without discussion
- Follow multi-stage build patterns if present
- Keep image sizes reasonable

### Configuration
- Use environment variables for configuration
- Check for `.env.example` or `.env.template`
- Never commit secrets in Dockerfiles or compose files
- Use Docker secrets for sensitive data in production

### Networking
- Understand service networking in docker-compose
- Check exposed ports and service names
- Respect existing network configurations

## Common Patterns

### Multi-Container Applications
- Web + Database + Cache (e.g., app + PostgreSQL + Redis)
- Microservices architecture
- Service dependencies in docker-compose

### Volume Mounts
- Development: Source code mounted for hot reload
- Production: Named volumes for persistence
- Check existing volume configurations

### Health Checks
- Dockerfile `HEALTHCHECK` instructions
- docker-compose `healthcheck` configurations
- Startup dependencies (`depends_on`, `condition`)

## Quick Reference

**Before running:**
- ✅ Check README for build instructions
- ✅ Look for Makefile with common commands
- ✅ Check for .env.example
- ✅ Understand dev vs production configurations

**Development:**
- Use provided Makefile targets if available
- Respect existing Dockerfile patterns
- Don't modify base images without good reason
- Follow established volume mount patterns

**Common mistakes to avoid:**
- ❌ Changing base images casually
- ❌ Committing secrets in Dockerfiles
- ❌ Ignoring existing Makefile commands
- ❌ Modifying production configs for dev convenience

**Useful commands:**
```bash
# Check running containers
docker ps

# View logs
docker-compose logs -f service-name

# Execute command in container
docker-compose exec service-name bash

# Rebuild after changes
docker-compose up --build
```

---

**Note:** Container projects vary in complexity - always check project-specific documentation before making changes to Docker configurations.
