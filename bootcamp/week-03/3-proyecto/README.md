# 🔍 Proyecto Semana 03: API de Catálogo con Búsqueda Avanzada

## 🏛️ Tu Dominio Asignado

**Dominio**: `[El instructor te asignará tu dominio único]`

> ⚠️ **IMPORTANTE**: Cada aprendiz trabaja sobre un dominio diferente.

### 💡 Ejemplo Genérico de Referencia

> Los ejemplos usan **"Warehouse"** (Almacén) que NO está en el pool.
> **Debes adaptar TODO a tu dominio asignado.**

| Concepto | Ejemplo Genérico | Adapta a tu Dominio |
|----------|-----------------|---------------------|
| Categories | `Zone` | `{YourCategory}` |
| Main Entity | `Item` | `{YourEntity}` |
| Filters | `zone`, `min_stock`, `supplier` | `{your_filters}` |

---

## 🎯 Objetivo

Construir una **API de catálogo** con búsqueda avanzada y filtros múltiples adaptada a tu dominio.

---

## 📦 Requisitos Funcionales (Adapta a tu Dominio)

### Entidades

**Category Entity:**
```python
# Ejemplo genérico (Warehouse - Zone)
Zone:
    id: int
    code: str          # A, B, C...
    name: str          # "Electronics", "Food"...
    max_capacity: int
    is_climate_controlled: bool
```

**Main Entity:**
```python
# Ejemplo genérico (Warehouse - Item)
Item:
    id: int
    sku: str
    name: str
    zone_id: int       # FK to Zone
    quantity: int
    min_stock: int
    supplier: str
    is_active: bool
```

### Search Filters (Mínimo 6)

```python
# Ejemplo genérico (Warehouse)
GET /items/?zone=A&min_stock_gte=10&supplier=ACME&is_active=true&sort_by=quantity&order=desc
```

| Filtro | Tipo | Descripción |
|--------|------|-------------|
| `zone` | str | Filtrar por zona |
| `min_stock_gte` | int | Stock mínimo >= valor |
| `quantity_lte` | int | Cantidad <= valor |
| `supplier` | str | Filtrar por proveedor |
| `is_active` | bool | Solo activos/inactivos |
| `search` | str | Búsqueda en name/sku |
| `sort_by` | str | Campo de ordenamiento |
| `order` | str | asc/desc |

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/zones/` | Listar categorías |
| POST | `/zones/` | Crear categoría |
| GET | `/items/` | Listar con filtros |
| GET | `/items/search` | Búsqueda full-text |
| GET | `/items/stats` | Estadísticas por categoría |
| GET | `/zones/{id}/items` | Items de una zona |

---

## 🗂️ Estructura del Proyecto

```
starter/
├── main.py
├── models/
│   ├── category.py
│   └── entity.py
├── schemas/
│   ├── category.py
│   ├── entity.py
│   └── filters.py
├── routers/
│   ├── categories.py
│   └── entities.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| CRUD categorías + entidades | 15 |
| Filtros funcionan (6+) | 15 |
| Búsqueda y estadísticas | 10 |
| **Adaptación al Dominio** (35%) | |
| Filtros coherentes con negocio | 12 |
| Categorías específicas | 13 |
| Originalidad (no copia ejemplo) | 10 |
| **Calidad del Código** (25%) | |
| Schemas de filtros limpios | 10 |
| Query parameters bien tipados | 10 |
| Código limpio | 5 |
| **Total** | **100** |

---

## ⚠️ Política Anticopia

- ❌ **No copies** el ejemplo genérico "Warehouse/Zone/Item"
- ✅ **Diseña** filtros específicos de tu dominio
- ✅ **Crea** categorías únicas para tu negocio

---

## 📚 Recursos

- [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Pool de Dominios](../../../_apprentices-only/dominios/POOL-DOMINIOS.md)

---

**Tiempo estimado:** 2-3 horas

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
