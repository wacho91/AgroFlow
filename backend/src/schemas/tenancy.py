"""Schemas Pydantic para tenancy (tenants, usuarios)."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.enums import EstadoTenant, RolUsuario


class TenantBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=100)
    nit: str | None = Field(default=None, max_length=30)
    razon_social: str | None = Field(default=None, max_length=300)
    email_contacto: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = None
    pais: str = Field(default="CO", min_length=2, max_length=2)
    moneda: str = Field(default="COP", min_length=3, max_length=3)
    zona_horaria: str = Field(default="America/Bogota", max_length=50)


class TenantCreate(TenantBase):
    plan: str = Field(default="starter", max_length=50)
    max_usuarios: int = Field(default=5, ge=1)
    max_hectareas: Decimal = Field(default=Decimal("100"), ge=0)


class TenantUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=200)
    razon_social: str | None = Field(default=None, max_length=300)
    email_contacto: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = None
    estado: EstadoTenant | None = None
    plan: str | None = Field(default=None, max_length=50)
    fecha_inicio_plan: date | None = None
    fecha_fin_plan: date | None = None
    max_usuarios: int | None = Field(default=None, ge=1)
    max_hectareas: Decimal | None = Field(default=None, ge=0)


class TenantRead(TenantBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    estado: EstadoTenant
    plan: str
    fecha_inicio_plan: date | None
    fecha_fin_plan: date | None
    max_usuarios: int
    max_hectareas: Decimal
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_completo: str = Field(min_length=1, max_length=200)
    telefono: str | None = Field(default=None, max_length=30)
    rol: RolUsuario = RolUsuario.OPERARIO


class UsuarioCreate(UsuarioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID


class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = Field(default=None, min_length=1, max_length=200)
    telefono: str | None = Field(default=None, max_length=30)
    rol: RolUsuario | None = None
    activo: bool | None = None
    mfa_habilitado: bool | None = None


class UsuarioRead(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    activo: bool
    ultimo_acceso: datetime | None
    mfa_habilitado: bool
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
