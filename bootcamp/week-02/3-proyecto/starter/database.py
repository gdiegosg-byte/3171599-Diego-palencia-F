"""
Base de Datos en Memoria
========================
Almacenamiento para la Plataforma de Servicios de Limpieza.
"""

services_db: dict[int, dict] = {}
_id_counter = 0


def get_next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


def code_exists(code: str) -> bool:
    return any(s["service_code"] == code for s in services_db.values())
