"""Agregador de routers v1 (arquitectura hexagonal)."""
from __future__ import annotations

from fastapi import APIRouter

from src.infrastructure.api.v1.routers import (
    costos,
    inventario,
    nomina,
    tenancy,
)

api_router = APIRouter()

api_router.include_router(tenancy.router, prefix="/tenancy", tags=["tenancy"])
api_router.include_router(costos.router, prefix="/costos", tags=["costos"])
api_router.include_router(
    inventario.router, prefix="/inventario", tags=["inventario"]
)
api_router.include_router(nomina.router, prefix="/nomina", tags=["nomina"])
