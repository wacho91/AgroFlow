"""Modelos de inventario y insumos."""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import String, Numeric, Boolean, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
from .mixins import UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin
from .enums import EstadoInsumo, MetodoValoracion

class Insumo(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "insumos"
    
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String(30), default="kg", nullable=False)
    stock_actual: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    stock_minimo: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_promedio: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    estado: Mapped[EstadoInsumo] = mapped_column(
        String(30), default=EstadoInsumo.ACTIVO.value, nullable=False
    )
    metodo_valoracion: Mapped[MetodoValoracion] = mapped_column(
        String(30), default=MetodoValoracion.PROMEDIO_PONDERADO.value, nullable=False
    )
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)