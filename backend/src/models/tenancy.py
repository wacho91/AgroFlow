"""Modelos de tenancy y seguridad: tenants, usuarios."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SAEnum,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

# === IMPORTACIONES CORREGIDAS ===
from ..database import Base
from .enums import EstadoTenant, RolUsuario
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDPKMixin
# =================================

class Tenant(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "tenants"

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    nit: Mapped[str | None] = mapped_column(String(30))
    razon_social: Mapped[str | None] = mapped_column(String(300))
    email_contacto: Mapped[str | None] = mapped_column(CITEXT)
    telefono: Mapped[str | None] = mapped_column(String(30))
    direccion: Mapped[str | None] = mapped_column(Text)
    pais: Mapped[str] = mapped_column(String(2), default="CO", nullable=False)
    moneda: Mapped[str] = mapped_column(String(3), default="COP", nullable=False)
    zona_horaria: Mapped[str] = mapped_column(
        String(50), default="America/Bogota", nullable=False
    )
    estado: Mapped[EstadoTenant] = mapped_column(
        SAEnum(EstadoTenant, name="estado_tenant", native_enum=True),
        default=EstadoTenant.TRIAL,
        nullable=False,
    )
    plan: Mapped[str] = mapped_column(String(50), default="starter", nullable=False)
    fecha_inicio_plan: Mapped[date | None] = mapped_column(Date)
    fecha_fin_plan: Mapped[date | None] = mapped_column(Date)
    max_usuarios: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    max_hectareas: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("100"), nullable=False
    )
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )

class Usuario(UUIDPKMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_usuarios_tenant_email"),
    )

    # id = auth.users.id (Supabase Auth) — no autogenerado
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(CITEXT, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(200), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30))
    rol: Mapped[RolUsuario] = mapped_column(
        SAEnum(RolUsuario, name="rol_usuario", native_enum=True),
        default=RolUsuario.OPERARIO,
        nullable=False,
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    mfa_habilitado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )