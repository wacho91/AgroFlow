"""
AgroFlow — Punto de entrada de la aplicación FastAPI.
Arquitectura Hexagonal · SQLAlchemy Async · PostgreSQL (Supabase).
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import dispose_engine
from src.infrastructure.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Ciclo de vida: startup / shutdown."""
    # --- Startup ---
    # Aquí se pueden inicializar pools, cache, tracing, etc.
    yield
    # --- Shutdown ---
    await dispose_engine()


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="API de gestión agropecuaria — AgroFlow",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS — permitir el origen del Frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # Routers modulares (v1)
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    async def health() -> JSONResponse:
        return JSONResponse(
            {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}
        )

    return app


app = create_app()
