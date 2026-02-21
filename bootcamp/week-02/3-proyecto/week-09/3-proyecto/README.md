# 🔌 Proyecto Semana 09: API con Ports & Adapters

## 🏛️ Tu Dominio Asignado

**Dominio**: `[El instructor te asignará tu dominio único]`

> ⚠️ **IMPORTANTE**: Cada aprendiz trabaja sobre un dominio diferente.

### 💡 Ejemplo Genérico de Referencia

> Los ejemplos usan **"Warehouse"** (Almacén) que NO está en el pool.
> **Debes adaptar TODO a tu dominio asignado.**

| Concepto | Ejemplo Genérico | Adapta a tu Dominio |
|----------|-----------------|---------------------|
| Port | `IItemPort` | `I{YourEntity}Port` |
| Adapter | `ItemAPIAdapter` | `{YourEntity}APIAdapter` |
| Use Case | `TransferItemUseCase` | `{YourAction}{YourEntity}UseCase` |

---

## 🎯 Objetivo

Implementar **Ports & Adapters (Arquitectura Hexagonal básica)**:

- Ports (interfaces) para definir contratos
- Adapters para implementaciones concretas
- Inversión de dependencias
- Testabilidad mejorada

---

## 📦 Requisitos Funcionales (Adapta a tu Dominio)

### Ports (Interfaces)

```python
# Ejemplo genérico (Warehouse)
from typing import Protocol

class IItemPort(Protocol):
    """Puerto para operaciones de Item"""
    
    async def get_by_sku(self, sku: str) -> Item | None:
        """Obtener item por SKU"""
        ...
    
    async def save(self, item: Item) -> Item:
        """Guardar item"""
        ...
    
    async def transfer_zone(
        self, 
        item_id: int, 
        target_zone_id: int
    ) -> Item:
        """Transferir item a otra zona"""
        ...

class INotificationPort(Protocol):
    """Puerto para notificaciones"""
    
    async def notify_low_stock(self, item: Item) -> None:
        """Notificar stock bajo"""
        ...
```

### Adapters

```python
# Ejemplo genérico
class SQLAlchemyItemAdapter:
    """Adapter para persistencia con SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_sku(self, sku: str) -> Item | None:
        result = await self.session.execute(
            select(ItemModel).where(ItemModel.sku == sku)
        )
        row = result.scalar_one_or_none()
        return Item.from_orm(row) if row else None
    
    async def save(self, item: Item) -> Item:
        model = ItemModel(**item.model_dump())
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return Item.from_orm(model)

class EmailNotificationAdapter:
    """Adapter para notificaciones por email"""
    
    async def notify_low_stock(self, item: Item) -> None:
        # Lógica de envío de email
        await send_email(
            to="warehouse@company.com",
            subject=f"Low stock: {item.sku}",
            body=f"Item {item.name} has only {item.quantity} units"
        )

class FakeNotificationAdapter:
    """Adapter fake para testing"""
    
    def __init__(self):
        self.notifications: list[Item] = []
    
    async def notify_low_stock(self, item: Item) -> None:
        self.notifications.append(item)
```

### Use Cases con Inyección

```python
# Ejemplo genérico
class TransferItemUseCase:
    """Caso de uso: transferir item entre zonas"""
    
    def __init__(
        self,
        item_port: IItemPort,
        notification_port: INotificationPort
    ):
        self.item_port = item_port
        self.notification_port = notification_port
    
    async def execute(
        self, 
        item_id: int, 
        target_zone_id: int
    ) -> Item:
        item = await self.item_port.transfer_zone(
            item_id, 
            target_zone_id
        )
        
        if item.quantity < 10:
            await self.notification_port.notify_low_stock(item)
        
        return item
```

### Dependency Injection en FastAPI

```python
# Ejemplo genérico
def get_item_port(
    session: AsyncSession = Depends(get_session)
) -> IItemPort:
    return SQLAlchemyItemAdapter(session)

def get_notification_port() -> INotificationPort:
    if settings.ENVIRONMENT == "test":
        return FakeNotificationAdapter()
    return EmailNotificationAdapter()

@app.post("/items/{item_id}/transfer")
async def transfer_item(
    item_id: int,
    target_zone_id: int,
    item_port: IItemPort = Depends(get_item_port),
    notification_port: INotificationPort = Depends(get_notification_port)
):
    use_case = TransferItemUseCase(item_port, notification_port)
    return await use_case.execute(item_id, target_zone_id)
```

---

## 🗂️ Estructura del Proyecto

```
starter/
├── main.py
├── ports/
│   ├── __init__.py
│   ├── item_port.py
│   └── notification_port.py
├── adapters/
│   ├── __init__.py
│   ├── sqlalchemy_item.py
│   ├── email_notification.py
│   └── fake_notification.py
├── use_cases/
│   └── transfer_item.py
├── domain/
├── dependencies.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## ✅ Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| Ports definidos correctamente | 15 |
| Adapters implementados | 15 |
| Use Cases funcionan | 10 |
| **Adaptación al Dominio** (35%) | |
| Ports relevantes al negocio | 12 |
| Use Cases específicos | 13 |
| Originalidad (no copia ejemplo) | 10 |
| **Calidad del Código** (25%) | |
| Inversión de dependencias | 10 |
| Testabilidad demostrada | 10 |
| Código limpio | 5 |
| **Total** | **100** |

---

## ⚠️ Política Anticopia

- ❌ **No copies** el ejemplo genérico "IItemPort/TransferItemUseCase"
- ✅ **Diseña** ports específicos de tu dominio
- ✅ **Crea** use cases relevantes para tu negocio

---

## 📚 Recursos

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports and Adapters](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)
- [Pool de Dominios](../../../_apprentices-only/dominios/POOL-DOMINIOS.md)

---

**Tiempo estimado:** 3 horas

[← Volver a Prácticas](../2-practicas/) | [Recursos →](../4-recursos/)
