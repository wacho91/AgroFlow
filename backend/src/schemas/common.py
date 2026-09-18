"""Schemas comunes: paginación y errores."""
from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parámetros de paginación reutilizables."""

    page: int = Field(default=1, ge=1, description="Página (1-indexed)")
    size: int = Field(default=20, ge=1, le=100, description="Items por página")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica."""

    model_config = ConfigDict(from_attributes=True)

    items: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    size: int = Field(ge=1)
    pages: int = Field(ge=0)


class ErrorResponse(BaseModel):
    """Formato estándar de error HTTP."""

    detail: str
    code: str | None = None
    field: str | None = None
