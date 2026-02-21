# ============================================
## DOCKERFILE - Proyecto API de Saludo
# ============================================

# Usamos Python 3.14 slim
FROM python:3.14-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# Instalar uv (gestor de dependencias)
RUN pip install --no-cache-dir uv

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar pyproject.toml (y uv.lock si existe)
COPY pyproject.toml uv.lock* ./

# Crear el virtualenv y sincronizar dependencias
# No usamos --frozen, así que uv.lock se genera automáticamente si no existe
RUN uv sync --no-dev

# Copiar todo el resto del proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para correr la app
CMD ["uv", "run", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]
