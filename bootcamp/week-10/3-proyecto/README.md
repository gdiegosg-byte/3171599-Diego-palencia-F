# 🔷 Proyecto Semana 10: API con Arquitectura Hexagonal Completa

## 🏛️ Tu Dominio Asignado

**Dominio**: `[El instructor te asignará tu dominio único]`

> ⚠️ **IMPORTANTE**: Cada aprendiz trabaja sobre un dominio diferente.

### 💡 Ejemplo Genérico de Referencia

> Los ejemplos usan **"Warehouse"** (Almacén) que NO está en el pool.
> **Debes adaptar TODO a tu dominio asignado.**

| Concepto | Ejemplo Genérico | Adapta a tu Dominio |
|----------|-----------------|---------------------|
| Domain Entity | `Item` | `{YourEntity}` |
| Value Object | `SKU` | `{YourVO}` |
| Application Service | `ItemApplicationService` | `{YourEntity}ApplicationService` |

---

## 🎯 Objetivo

Implementar **Arquitectura Hexagonal completa**:

- Domain Layer con Entities y Value Objects
- Application Layer con Services
- Infrastructure Layer con Adapters
- Separación total de concerns

---

## 📦 Requisitos Funcionales (Adapta a tu Dominio)

### Domain Layer

```python
# Ejemplo genérico (Warehouse) - domain/entities/item.py
from dataclasses import dataclass
from domain.value_objects import SKU, Quantity

@dataclass
class Item:
    """Entidad de dominio Item"""
    id: int | None
    sku: SKU
    name: str
    quantity: Quantity
    zone_id: int
    
    def transfer_to(self, new_zone_id: int) -> None:
        """Regla de negocio: transferir zona"""
        if self.quantity.value == 0:
            raise DomainError("Cannot transfer empty item")
        self.zone_id = new_zone_id
    
    def reduce_stock(self, amount: int) -> None:
        """Regla de negocio: reducir stock"""
        self.quantity = self.quantity.subtract(amount)
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        """Regla de negocio: verificar stock bajo"""
        return self.quantity.value < threshold
```

### Value Objects

```python
# Ejemplo genérico - domain/value_objects/sku.py
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class SKU:
    """Value Object inmutable para SKU"""
    value: str
    
    def __post_init__(self):
        if not re.match(r'^[A-Z]{2}-\d{4}$', self.value):
            raise ValueError(f"Invalid SKU format: {self.value}")
    
    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class Quantity:
    """Value Object inmutable para cantidades"""
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Quantity cannot be negative")
    
    def subtract(self, amount: int) -> "Quantity":
        new_value = self.value - amount
        if new_value < 0:
            raise ValueError("Insufficient quantity")
        return Quantity(new_value)
    
    def add(self, amount: int) -> "Quantity":
        return Quantity(self.value + amount)
```

### Application Layer

```python
# Ejemplo genérico - application/services/item_service.py
from domain.entities import Item
from domain.repositories import IItemRepository
from application.dtos import ItemDTO, CreateItemDTO

class ItemApplicationService:
    """Orquesta casos de uso de Item"""
    
    def __init__(
        self,
        item_repo: IItemRepository,
        event_publisher: IEventPublisher
    ):
        self.item_repo = item_repo
        self.event_publisher = event_publisher
    
    async def create_item(self, dto: CreateItemDTO) -> ItemDTO:
        """Caso de uso: crear item"""
        # Reglas de aplicación
        existing = await self.item_repo.find_by_sku(dto.sku)
        if existing:
            raise ApplicationError("SKU already exists")
        
        # Crear entidad de dominio
        item = Item(
            id=None,
            sku=SKU(dto.sku),
            name=dto.name,
            quantity=Quantity(dto.initial_quantity),
            zone_id=dto.zone_id
        )
        
        # Persistir
        saved = await self.item_repo.save(item)
        
        # Publicar evento
        await self.event_publisher.publish(
            ItemCreated(item_id=saved.id)
        )
        
        return ItemDTO.from_entity(saved)
    
    async def transfer_item(
        self, 
        item_id: int, 
        target_zone_id: int
    ) -> ItemDTO:
        """Caso de uso: transferir item"""
        item = await self.item_repo.find_by_id(item_id)
        if not item:
            raise NotFoundError(f"Item {item_id} not found")
        
        # Regla de dominio
        item.transfer_to(target_zone_id)
        
        # Persistir cambio
        updated = await self.item_repo.save(item)
        
        return ItemDTO.from_entity(updated)
```

### Infrastructure Layer

```python
# Ejemplo genérico - infrastructure/repositories/sqlalchemy_item.py
from domain.entities import Item
from domain.value_objects import SKU, Quantity
from domain.repositories import IItemRepository
from infrastructure.models import ItemModel

class SQLAlchemyItemRepository(IItemRepository):
    """Implementación SQLAlchemy del repositorio"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_by_id(self, item_id: int) -> Item | None:
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.id == item_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def save(self, item: Item) -> Item:
        model = self._to_model(item)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    def _to_entity(self, model: ItemModel) -> Item:
        return Item(
            id=model.id,
            sku=SKU(model.sku),
            name=model.name,
            quantity=Quantity(model.quantity),
            zone_id=model.zone_id
        )
    
    def _to_model(self, entity: Item) -> ItemModel:
        return ItemModel(
            id=entity.id,
            sku=str(entity.sku),
            name=entity.name,
            quantity=entity.quantity.value,
            zone_id=entity.zone_id
        )
```

---

## 🗂️ Estructura del Proyecto

```
starter/
├── main.py
├── domain/
│   ├── entities/
│   │   ├── __init__.py
│   │   └── item.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── sku.py
│   │   └── quantity.py
│   ├── repositories/
│   │   └── item_repository.py
│   └── errors.py
├── application/
│   ├── services/
│   │   └── item_service.py
│   ├── dtos/
│   └── events/
├── infrastructure/
│   ├── repositories/
│   ├── models/
│   └── adapters/
├── api/
│   └── routers/
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| Domain Layer correcto | 15 |
| Application Layer funciona | 15 |
| Infrastructure separada | 10 |
| **Adaptación al Dominio** (35%) | |
| Value Objects relevantes | 12 |
| Reglas de negocio propias | 13 |
| Originalidad (no copia ejemplo) | 10 |
| **Calidad del Código** (25%) | |
| Capas bien separadas | 10 |
| Dependencias hacia adentro | 10 |
| Código limpio | 5 |
| **Total** | **100** |

---

## ⚠️ Política Anticopia

- ❌ **No copies** el ejemplo genérico "Item/SKU/Quantity"
- ✅ **Diseña** Value Objects de tu dominio
- ✅ **Crea** reglas de negocio propias

---

## 📚 Recursos

- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Pool de Dominios](../../../_apprentices-only/dominios/POOL-DOMINIOS.md)

---

**Tiempo estimado:** 3 horas

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
