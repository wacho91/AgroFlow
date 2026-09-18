import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# Importar el engine y la Base
from .database import Base, engine

# === BUSCADOR INTELIGENTE DE ROUTERS (Arquitectura Hexagonal) ===
router = None
try:
    # Intento 1: La ruta que viste en la captura (infrastructure/api/v1)
    from .infrastructure.api.v1 import router as found_router
    router = found_router
except ImportError:
    try:
        # Intento 2: Quizás la nombraron en plural (infrastructure/api/v1/routers)
        from .infrastructure.api.v1.routers import router as found_router
        router = found_router
    except ImportError:
        try:
            # Intento 3: Quizás la pusieron directo en infrastructure
            from .infrastructure.router import router as found_router
            router = found_router
        except ImportError:
            print("⚠️ Advertencia: No se encontró el router de rutas. Revisa la carpeta infrastructure.")
# ===============================================================

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # === MAGIA: Crear tablas automáticamente en SQLite ===
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas verificadas/creadas en la base de datos local (SQLite).")
    except Exception as e:
        logger.error(f"⚠️ Error al crear tablas: {e}")
    
    yield

    # Shutdown
    await engine.dispose()

# Crear la app
app = FastAPI(
    title="AgroFlow API",
    description="SaaS B2B AgroTech para gestión de fincas agrícolas.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS
origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
origins = [o.strip() for o in origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas si se encontraron
if router:
    app.include_router(router)

@app.get("/", tags=["health"])
async def root():
    return {"message": "AgroFlow API running", "docs": "/docs"}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}