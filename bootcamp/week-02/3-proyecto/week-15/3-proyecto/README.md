# 🐳 Proyecto Semana 15: Containerización y CI/CD

## 🏛️ Tu Dominio Asignado

**Dominio**: `[El instructor te asignará tu dominio único]`

> ⚠️ **IMPORTANTE**: Cada aprendiz trabaja sobre un dominio diferente.

### 💡 Ejemplo Genérico de Referencia

> Los ejemplos usan **"Warehouse"** (Almacén) que NO está en el pool.
> **Debes adaptar TODO a tu dominio asignado.**

| Concepto | Ejemplo Genérico | Adapta a tu Dominio |
|----------|-----------------|---------------------|
| Container Name | `warehouse-api` | `{your-domain}-api` |
| Environment Vars | `WAREHOUSE_DB_URL` | `{DOMAIN}_DB_URL` |
| GitHub Actions | `warehouse-ci.yml` | `{domain}-ci.yml` |

---

## 🎯 Objetivo

Implementar **containerización y CI/CD completo**:

- Dockerfile multi-stage optimizado
- Docker Compose para desarrollo
- GitHub Actions para CI/CD
- Deployment automatizado

---

## 📦 Requisitos Funcionales (Adapta a tu Dominio)

### Dockerfile Multi-Stage

```dockerfile
# Ejemplo genérico (Warehouse)
# ===========================================
# Stage 1: Builder
# ===========================================
FROM python:3.14-slim AS builder

# Instalar uv
ENV UV_SYSTEM_PYTHON=1
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copiar solo archivos de dependencias primero (cache layer)
COPY pyproject.toml uv.lock* ./

# Instalar dependencias de producción
RUN uv sync --frozen --no-dev

# ===========================================
# Stage 2: Production
# ===========================================
FROM python:3.14-slim AS production

# Crear usuario no-root
RUN groupadd -r warehouse && useradd -r -g warehouse warehouse

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_SYSTEM_PYTHON=1

RUN pip install --no-cache-dir uv

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copiar código fuente
COPY --chown=warehouse:warehouse src/ ./src/

# Cambiar a usuario no-root
USER warehouse

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# Ejemplo genérico - docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: warehouse-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://warehouse:secret@db:5432/warehouse
      - JWT_SECRET=${JWT_SECRET}
      - ENVIRONMENT=production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/ready"\]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - warehouse-network
    restart: unless-stopped

  db:
    image: postgres:17-alpine
    container_name: warehouse-db
    environment:
      POSTGRES_USER: warehouse
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: warehouse
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U warehouse"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - warehouse-network

  redis:
    image: redis:7-alpine
    container_name: warehouse-redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - warehouse-network

volumes:
  postgres_data:

networks:
  warehouse-network:
    driver: bridge
```

### Docker Compose Override (Desarrollo)

```yaml
# Ejemplo genérico - docker-compose.override.yml
services:
  api:
    build:
      target: builder  # Usar stage de desarrollo
    volumes:
      - ./src:/app/src:ro  # Hot reload
    environment:
      - DATABASE_URL=sqlite:///./dev.db
      - ENVIRONMENT=development
      - DEBUG=true
    command: ["uv", "run", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]
```

### GitHub Actions - CI

```yaml
# Ejemplo genérico - .github/workflows/ci.yml
name: Warehouse API CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:17-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv sync --frozen
      
      - name: Run linting
        run: uv run ruff check .
      
      - name: Run type checking
        run: uv run mypy src/
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
        run: uv run pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: warehouse-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitHub Actions - CD

```yaml
# Ejemplo genérico - .github/workflows/cd.yml
name: Warehouse API CD

on:
  push:
    tags:
      - "v*"

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /opt/warehouse-api
            docker compose pull
            docker compose up -d
            docker image prune -f
```

### Makefile para Comandos Comunes

```makefile
# Ejemplo genérico - Makefile
.PHONY: help build up down logs test lint clean

help:
	@echo "Comandos disponibles:"
	@echo "  make build   - Construir imágenes Docker"
	@echo "  make up      - Levantar servicios"
	@echo "  make down    - Detener servicios"
	@echo "  make logs    - Ver logs"
	@echo "  make test    - Ejecutar tests"
	@echo "  make lint    - Ejecutar linting"
	@echo "  make clean   - Limpiar todo"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f api

test:
	docker compose run --rm api uv run pytest -v

lint:
	docker compose run --rm api uv run ruff check .

clean:
	docker compose down -v --rmi all
	docker system prune -f
```

---

## 🗂️ Estructura del Proyecto

```
starter/
├── src/
│   └── main.py
├── tests/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── .dockerignore
├── Makefile
├── pyproject.toml
└── .env.example
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| Dockerfile optimizado | 15 |
| Docker Compose funciona | 15 |
| CI pipeline pasa | 10 |
| **Adaptación al Dominio** (35%) | |
| Nombres y variables adaptados | 12 |
| Configuración específica | 13 |
| Originalidad (no copia ejemplo) | 10 |
| **Calidad del Código** (25%) | |
| Multi-stage build | 10 |
| Security best practices | 10 |
| Documentación | 5 |
| **Total** | **100** |

---

## ⚠️ Política Anticopia

- ❌ **No copies** los nombres "warehouse-api/warehouse-db"
- ✅ **Adapta** nombres de contenedores a tu dominio
- ✅ **Crea** variables de entorno específicas

---

## 📚 Recursos

- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [uv with Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [Pool de Dominios](../../../_apprentices-only/dominios/POOL-DOMINIOS.md)

---

**Tiempo estimado:** 3 horas

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
