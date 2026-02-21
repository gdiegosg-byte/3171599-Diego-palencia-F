"""
API de Plataforma de Servicios de Limpieza
==========================================
Ejecutar:
    docker compose up --build
Documentación: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Path, Query
from schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceList
from database import services_db, get_next_id, code_exists
from datetime import datetime

app = FastAPI(
    title="Plataforma de Servicios de Limpieza",
    version="1.0.0",
)


@app.post("/servicios/", response_model=ServiceResponse, status_code=201, tags=["Servicios"])
def create_service(service: ServiceCreate):
    """Crear una nueva solicitud de servicio."""
    if code_exists(service.service_code):
        raise HTTPException(status_code=400, detail=f"El código '{service.service_code}' ya existe")

    service_id = get_next_id()
    new_service = {
        "id": service_id,
        **service.model_dump(),
        "status": "pendiente",
        "created_at": datetime.now(),
        "updated_at": None,
    }
    services_db[service_id] = new_service
    return new_service


@app.get("/servicios/", response_model=ServiceList, tags=["Servicios"])
def list_services(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    service_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    """Listar solicitudes con paginación y filtros."""
    services = list(services_db.values())
    if service_type:
        services = [s for s in services if s["service_type"] == service_type]
    if status:
        services = [s for s in services if s["status"] == status]
    total = len(services)
    return ServiceList(items=services[skip: skip + limit], total=total, skip=skip, limit=limit)


@app.get("/servicios/by-code/{service_code}", response_model=ServiceResponse, tags=["Servicios"])
def get_by_code(service_code: str):
    """Buscar por código único (ej: LIM-0042)."""
    code = service_code.strip().upper()
    for service in services_db.values():
        if service["service_code"] == code:
            return service
    raise HTTPException(status_code=404, detail=f"No existe solicitud con código '{code}'")


@app.get("/servicios/{service_id}", response_model=ServiceResponse, tags=["Servicios"])
def get_service(service_id: int = Path(..., gt=0)):
    """Obtener una solicitud por ID."""
    if service_id not in services_db:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return services_db[service_id]


@app.patch("/servicios/{service_id}", response_model=ServiceResponse, tags=["Servicios"])
def update_service(service_id: int, data: ServiceUpdate):
    """Actualizar parcialmente una solicitud."""
    if service_id not in services_db:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    stored = services_db[service_id]
    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()
    return stored


@app.delete("/servicios/{service_id}", status_code=204, tags=["Servicios"])
def delete_service(service_id: int = Path(..., gt=0)):
    """Eliminar una solicitud."""
    if service_id not in services_db:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    del services_db[service_id]


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "total_servicios": len(services_db)}
