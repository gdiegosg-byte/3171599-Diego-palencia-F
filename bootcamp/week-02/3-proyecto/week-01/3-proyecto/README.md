# 🎯 Proyecto Semana 01: API Básica de tu Dominio

## 🏛️ Tu Dominio Asignado

**Dominio**: `[El instructor te asignará tu dominio único]`

> ⚠️ **IMPORTANTE**: Cada aprendiz trabaja sobre un dominio diferente.
> Consulta tu asignación en el registro de la ficha.

### 💡 Ejemplo Genérico de Referencia

> Los ejemplos usan un dominio genérico **"Warehouse"** (Almacén) que NO está en el pool de asignación.
> **Debes adaptar TODO a tu dominio asignado.**

| Concepto | Ejemplo Genérico | Adapta a tu Dominio |
|----------|-----------------|---------------------|
| Main Entity | `Item` | `{YourEntity}` |
| Welcome Endpoint | `GET /visitor/{name}` | `GET /{your_actor}/{name}` |
| Info Endpoint | `GET /item/{code}/info` | `GET /{your_entity}/{id}/info` |
| Service Endpoint | `GET /service/schedule` | `GET /service/schedule` |

---

## 📋 Descripción

En este proyecto integrador, crearás una **API básica** para tu dominio asignado que aplica todos los conceptos aprendidos en la semana:

- Configuración de Docker
- Type hints en Python
- Programación asíncrona
- Endpoints FastAPI con parámetros

---

## 🎯 Objetivos

Al completar este proyecto, habrás demostrado que puedes:

- ✅ Configurar un proyecto FastAPI con Docker
- ✅ Usar type hints correctamente
- ✅ Crear endpoints con path y query parameters
- ✅ Adaptar conceptos genéricos a tu dominio específico
- ✅ Documentar tu API

---

## 📦 Requisitos Funcionales (Adapta a tu Dominio)

### RF-01: API Information Endpoint
- **Ruta**: `GET /`
- **Descripción**: Retorna información de tu API adaptada al dominio
- **Respuesta**: `{"name": "[Your Domain] API", "version": "1.0.0", "domain": "[your-domain]"}`

**Ejemplo genérico (Warehouse):**
```json
{"name": "Warehouse Inventory API", "version": "1.0.0", "domain": "warehouse"}
```

### RF-02: Personalized Welcome
- **Ruta**: `GET /{actor}/{name}`
- **Descripción**: Mensaje de bienvenida personalizado para tu dominio
- **Parámetros**: 
  - `name` (path): Nombre de la persona/entidad
  - `language` (query, default="es"): Idioma del mensaje (es, en, fr)

**Ejemplo genérico (Warehouse):**
```bash
GET /visitor/Carlos?language=es
→ {"message": "¡Bienvenido al almacén, Carlos!"}

GET /visitor/Ana?language=en
→ {"message": "Welcome to the warehouse, Ana!"}
```

### RF-03: Entity Information
- **Ruta**: `GET /{entity}/{identifier}/info`
- **Descripción**: Información detallada de una entidad de tu dominio
- **Parámetros**:
  - `identifier` (path): Nombre/código/ID
  - `detail_level` (query, default="basic"): Nivel de detalle (basic, full)

**Ejemplo genérico (Warehouse):**
```bash
GET /item/SKU-001/info?detail_level=basic
→ {"code": "SKU-001", "name": "Widget A", "stock": 150}

GET /item/SKU-001/info?detail_level=full
→ {"code": "SKU-001", "name": "Widget A", "stock": 150, "location": "A-12", "supplier": "ACME"}
```

### RF-04: Time-Based Service
- **Ruta**: `GET /service/schedule`
- **Descripción**: Respuesta diferente según la hora del día
- **Parámetros**:
  - `hour` (query): Hora del día (0-23)
- **Lógica horaria**: Adapta a tu dominio
  - 6-11: Mensaje de mañana
  - 12-17: Mensaje de tarde
  - 18-23 o 0-5: Mensaje de noche

**Ejemplo genérico (Warehouse):**
```bash
GET /service/schedule?hour=8
→ {"message": "Morning shift - Receiving active", "available": ["receiving", "inventory"]}

GET /service/schedule?hour=14
→ {"message": "Afternoon shift - Shipping active", "available": ["shipping", "picking"]}
```

### RF-05: Health Check
- **Ruta**: `GET /health`
- **Descripción**: Estado de la API
- **Respuesta**: `{"status": "healthy", "domain": "[your-domain]"}`

---

## 🏗️ Estructura del Proyecto

```
3-proyecto/
├── README.md              # Este archivo
├── starter/               # Código inicial
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── src/
│       └── main.py        # Implementar aquí
└── solution/              # ⚠️ Solo instructores
    └── ...
```

---

## 📝 Instrucciones

### 1. Configurar el Proyecto

```bash
cd bootcamp/week-01/3-proyecto/starter
```

### 2. Implementar la API (Adaptar a tu dominio)

Abre `src/main.py` y completa los TODOs adaptándolos a tu dominio:

1. **TODO 1**: Crear FastAPI app con nombre de tu dominio
2. **TODO 2**: Implementar endpoint raíz con info del dominio
3. **TODO 3**: Implementar bienvenida personalizada
4. **TODO 4**: Implementar información de entidad
5. **TODO 5**: Implementar servicio según horario
6. **TODO 6**: Implementar health check

### 3. Ejecutar y Probar

```bash
docker compose up --build

# Probar (adapta las URLs a tu dominio)
curl http://localhost:8000/
curl http://localhost:8000/health
```

### 4. Verificar Documentación

Visita `http://localhost:8000/docs`

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| Endpoint raíz funciona | 8 |
| Bienvenida personalizada con idiomas | 10 |
| Información de entidad con niveles | 10 |
| Servicio según horario | 12 |
| **Adaptación al Dominio** (35%) | |
| Endpoints coherentes con el negocio | 12 |
| Nombres y rutas específicas | 13 |
| Originalidad (no copia del ejemplo) | 10 |
| **Calidad del Código** (25%) | |
| Type hints correctos | 10 |
| Código limpio y documentado | 10 |
| Docker funciona | 5 |
| **Total** | **100** |

---

## ⚠️ Política Anticopia

- ❌ **No copies** el ejemplo genérico "Warehouse"
- ❌ **No uses** dominios de otros compañeros
- ✅ **Adapta** completamente a tu dominio asignado
- ✅ **Demuestra** comprensión de los conceptos

---

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Pool de Dominios](../../../_apprentices-only/dominios/POOL-DOMINIOS.md)

---

**Tiempo estimado:** 2 horas

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
