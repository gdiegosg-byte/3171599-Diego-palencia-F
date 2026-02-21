# ============================================
# PROYECTO: API DE SALUDO
# ============================================

from fastapi import FastAPI, HTTPException, Query, Path

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

GREETINGS: dict[str, str] = {
    "es": "¡Hola, {name}!",
    "en": "Hello, {name}!",
    "fr": "Bonjour, {name}!",
    "de": "Hallo, {name}!",
    "it": "Ciao, {name}!",
    "pt": "Olá, {name}!",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())

# ============================================
# INSTANCIA DE FASTAPI
# ============================================

app = FastAPI(
    title="Greeting API",
    description="API de saludos multiidioma",
    version="1.0.0"
)

# ============================================
# ENDPOINT RAÍZ
# ============================================

@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información general de la Greeting API."""
    return {
        "name": "Greeting API",
        "version": "1.0.0",
        "docs": "/docs",
        "languages": SUPPORTED_LANGUAGES
    }

# ============================================
# SALUDO PERSONALIZADO
# ============================================

@app.get("/greet/{name}")
async def greet(
    name: str = Path(..., description="Nombre de la persona a saludar"),
    language: str = Query("es", description=f"Idioma del saludo. Opciones: {SUPPORTED_LANGUAGES}")
) -> dict[str, str]:
    greeting_template = GREETINGS.get(language, GREETINGS["es"])
    greeting = greeting_template.format(name=name)
    final_language = language if language in GREETINGS else "es"
    return {
        "greeting": greeting,
        "language": final_language,
        "name": name
    }

# ============================================
# SALUDO SEGÚN LA HORA
# ============================================

def get_day_period(hour: int) -> tuple[str, str]:
    if 5 <= hour < 12:
        return ("Buenos días", "morning")
    elif 12 <= hour < 18:
        return ("Buenas tardes", "afternoon")
    else:
        return ("Buenas noches", "night")

@app.get("/greet/{name}/time-based")
async def greet_time_based(
    name: str,
    hour: int = Query(..., ge=0, le=23, description="Hora del día (0-23)")
) -> dict[str, str | int]:
    greeting_text, period = get_day_period(hour)
    greeting = f"{greeting_text}, {name}!"
    return {
        "greeting": greeting,
        "hour": hour,
        "period": period
    }
# ============================================
# saludo formal
# ============================================
@app.get("/greet/{name}/formal")
async def greet_formal(
    name: str = Path(..., description="Nombre o apellido de la persona"),
    title: str = Query("Sr./Sra.", description="Título formal (Dr., Ing., Prof., Lic., etc.)")
) -> dict[str, str]:
    """
    Genera un saludo formal con título.

    Args:
        name: Nombre o apellido de la persona
        title: Título formal (Dr., Ing., Prof., Lic., etc.)

    Returns:
        dict: Saludo formal
    """
    # Construir el saludo formal
    greeting = f"Estimado/a {title} {name}, es un placer saludarle."

    # Retornar la respuesta
    return {
        "greeting": greeting,
        "title": title,
        "name": name
    }

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "greeting-api",
        "version": "1.0.0"
    }
    
# ============================================
# VERIFICACIÓN
# ============================================
# Una vez completados todos los TODOs:
#
# 1. Ejecutar:
#    docker compose up --build
#
# 2. Probar en el navegador:
#    http://localhost:8000/docs
#
# 3. Verificar cada endpoint:
#    - GET /
#    - GET /greet/Carlos
#    - GET /greet/Carlos?language=en
#    - GET /greet/García/formal?title=Dr.
#    - GET /greet/Ana/time-based?hour=10
#    - GET /health
# ============================================.