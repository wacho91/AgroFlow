"""Modelos de Tesorería (Ingresos y Egresos)."""
from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import String, Numeric, Date, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .mixins import UUIDPKMixin, TenantMixin, TimestampMixin

class MovimientoTesoreria(UUIDPKMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "movimientos_tesoreria"
    
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False) # "ingreso" o "egreso"
    concepto: Mapped[str] = mapped_column(String(255), nullable=False)
    monto: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)