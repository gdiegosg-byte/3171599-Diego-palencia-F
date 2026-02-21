"""
Schemas Pydantic - Plataforma de Servicios de Limpieza
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal
from enum import Enum


class ServiceType(str, Enum):
    RESIDENTIAL = "residencial"
    COMMERCIAL  = "comercial"
    INDUSTRIAL  = "industrial"
    POST_WORK   = "post_obra"
    DEEP        = "profunda"


class ServiceStatus(str, Enum):
    PENDING     = "pendiente"
    CONFIRMED   = "confirmada"
    IN_PROGRESS = "en_proceso"
    COMPLETED   = "completada"
    CANCELLED   = "cancelada"


class ServiceBase(BaseModel):
    service_code: str = Field(..., examples=["LIM-0042"])
    client_name: str = Field(..., min_length=2, max_length=100)
    client_email: EmailStr
    client_phone: str
    service_type: ServiceType
    address: str = Field(..., min_length=10, max_length=300)
    area_m2: float = Field(..., gt=0, le=10000)
    price_per_hour: Decimal = Field(..., gt=0, decimal_places=2)
    scheduled_date: datetime
    notes: str | None = Field(default=None, max_length=500)
    is_active: bool = True


class ServiceCreate(ServiceBase):

    @field_validator("service_code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        import re
        v = v.strip().upper()
        if not re.match(r"^LIM-\d{4}$", v):
            raise ValueError("El código debe tener el formato LIM-XXXX (ej: LIM-0042)")
        return v

    @field_validator("client_name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("client_phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        digits = "".join(filter(str.isdigit, str(v)))
        if len(digits) == 10:
            return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
        elif len(digits) == 12 and digits.startswith("57"):
            digits = digits[2:]
            return f"+57 {digits[:3]} {digits[3:6]} {digits[6:]}"
        raise ValueError("Teléfono inválido. Use 10 dígitos (ej: 3001234567)")

    @field_validator("scheduled_date")
    @classmethod
    def validate_date(cls, v: datetime) -> datetime:
        if v <= datetime.now():
            raise ValueError("La fecha del servicio debe ser en el futuro")
        return v


class ServiceUpdate(BaseModel):
    client_name: str | None = None
    client_email: EmailStr | None = None
    client_phone: str | None = None
    service_type: ServiceType | None = None
    address: str | None = None
    area_m2: float | None = Field(default=None, gt=0, le=10000)
    price_per_hour: Decimal | None = Field(default=None, gt=0)
    scheduled_date: datetime | None = None
    notes: str | None = None
    status: ServiceStatus | None = None
    is_active: bool | None = None

    @field_validator("client_phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        digits = "".join(filter(str.isdigit, str(v)))
        if len(digits) == 10:
            return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
        elif len(digits) == 12 and digits.startswith("57"):
            digits = digits[2:]
            return f"+57 {digits[:3]} {digits[3:6]} {digits[6:]}"
        raise ValueError("Teléfono inválido. Use 10 dígitos (ej: 3001234567)")

    @field_validator("scheduled_date")
    @classmethod
    def validate_date(cls, v: datetime | None) -> datetime | None:
        if v is None:
            return v
        if v <= datetime.now():
            raise ValueError("La fecha del servicio debe ser en el futuro")
        return v


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime | None = None


class ServiceList(BaseModel):
    items: list[ServiceResponse]
    total: int
    skip: int
    limit: int
