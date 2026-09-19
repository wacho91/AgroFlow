import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# Importar el engine y la Base
from .database import Base, engine

# === MAGIA: Importar todos los modelos para que SQLAlchemy los detecte ===
from . import models  # noqa
# =======================================================================

# === BUSCADOR INTELIGENTE DE ROUTERS ===
router = None
try:
    # Busca en infrastructure/api/v1
    from .infrastructure.api.v1 import router as found_router
    router = found_router
except ImportError as e:
    print(f"⚠️ Advertencia: No se encontró el router. Error: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        async with engine.begin() as conn:
            # Ejecuta create_all para todas las tablas registradas en Base.metadata
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas verificadas/creadas en SQLite.")
    except Exception as e:
        logger.error(f"⚠️ Error al crear tablas: {e}")
    yield
    await engine.dispose()

app = FastAPI(title="AgroFlow API", lifespan=lifespan)

origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [o.strip() for o in origins_raw.split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if router:
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "AgroFlow API running"}