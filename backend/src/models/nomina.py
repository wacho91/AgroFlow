"""Modelos de nómina y jornaleros."""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import String, Boolean, DateTime, Numeric, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .mixins import UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin
from .enums import TipoJornalero

class Jornalero(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "jornaleros"
    
    nombre_completo: Mapped[str] = mapped_column(String(200), nullable=False)
    documento: Mapped[str] = mapped_column(String(50), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30))
    tipo: Mapped[str] = mapped_column(String(30), default=TipoJornalero.TEMPORAL.value, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)