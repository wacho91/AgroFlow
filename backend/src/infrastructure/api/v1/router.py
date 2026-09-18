"""Agregador de routers v1 (arquitectura hexagonal)."""
from __future__ import annotations

from fastapi import APIRouter

# === IMPORTACIONES CORREGIDAS (con puntitos) ===
from .routers import (
    costos,
    inventario,
    nomina,
    tenancy,
)
# ===============================================

api_router = APIRouter()

api_router.include_router(tenancy.router, prefix="/api/v1/tenancy", tags=["Tenancy"])
api_router.include_router(costos.router, prefix="/api/v1/costos", tags=["Costos"])
api_router.include_router(inventario.router, prefix="/api/v1/inventario", tags=["Inventario"])
api_router.include_router(nomina.router, prefix="/api/v1/nomina", tags=["Nomina"])

# === LÍNEA MÁGICA QUE FALTABA ===
router = api_router
# ================================