"""Modelos del contexto de costos de producción."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Integer,
    Numeric, String, Text, UniqueConstraint, func, JSON  # <--- JSON añadido aquí
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .enums import EstadoCiclo, MetodoProrrateo, TipoCosto
from .mixins import (
    AuditUserMixin, SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPKMixin,
)

class Finca(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "fincas"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_fincas_tenant_codigo"),)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    area_total_ha: Mapped[Decimal] = mapped_column(Numeric(12, 4), default=Decimal("0"), nullable=False)
    altitud_msnm: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    municipio: Mapped[str | None] = mapped_column(String(150))
    departamento: Mapped[str | None] = mapped_column(String(150))
    pais: Mapped[str] = mapped_column(String(2), default="CO", nullable=False)
    tipo_suelo: Mapped[str | None] = mapped_column(String(100))
    fuente_agua: Mapped[str | None] = mapped_column(String(100))
    notas: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class Lote(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "lotes"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_lotes_tenant_codigo"),)
    finca_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fincas.id"), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    area_ha: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    tipo_suelo: Mapped[str | None] = mapped_column(String(100))
    ph_suelo: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))
    drenaje: Mapped[str | None] = mapped_column(String(50))
    pendiente_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    capacidad_uso: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(30), default="disponible", nullable=False)
    notas: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class Cultivo(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "cultivos"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_cultivos_tenant_codigo"),)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    nombre_cientifico: Mapped[str | None] = mapped_column(String(200))
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    variedad: Mapped[str | None] = mapped_column(String(150))
    ciclo_dias: Mapped[int | None] = mapped_column(Integer)
    unidad_medida: Mapped[str] = mapped_column(String(30), default="kg", nullable=False)
    rendimiento_esperado: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    precio_referencia: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class CicloProductivo(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "ciclos_productivos"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_ciclos_tenant_codigo"),)
    lote_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lotes.id"), nullable=False, index=True)
    cultivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cultivos.id"), nullable=False, index=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    nombre: Mapped[str | None] = mapped_column(String(200))
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin_estimada: Mapped[date | None] = mapped_column(Date)
    fecha_fin_real: Mapped[date | None] = mapped_column(Date)
    estado: Mapped[EstadoCiclo] = mapped_column(SAEnum(EstadoCiclo, name="estado_ciclo", native_enum=True), default=EstadoCiclo.PLANIFICADO, nullable=False)
    area_sembrada_ha: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    densidad_siembra: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    produccion_estimada: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    produccion_real: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    unidad_produccion: Mapped[str] = mapped_column(String(30), default="kg", nullable=False)
    costo_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_unitario: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    ingreso_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    margen_bruto: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    notas: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class Actividad(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "actividades"
    __table_args__ = (UniqueConstraint("tenant_id", "codigo", name="uq_actividades_tenant_codigo"),)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo_costo: Mapped[TipoCosto] = mapped_column(SAEnum(TipoCosto, name="tipo_costo", native_enum=True), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    unidad_medida: Mapped[str | None] = mapped_column(String(30))
    requiere_insumo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requiere_mano_obra: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requiere_maquinaria: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class CostoActividad(UUIDPKMixin, TenantMixin, TimestampMixin, SoftDeleteMixin, AuditUserMixin, Base):
    __tablename__ = "costos_actividad"
    ciclo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ciclos_productivos.id"), nullable=True, index=True)
    actividad_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("actividades.id"))
    lote_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lotes.id"), nullable=False, index=True)
    tipo_costo: Mapped[TipoCosto] = mapped_column(SAEnum(TipoCosto, name="tipo_costo", native_enum=True), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    cantidad: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=Decimal("1"), nullable=False)
    unidad_medida: Mapped[str | None] = mapped_column(String(30))
    costo_unitario: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    metodo_prorrateo: Mapped[MetodoProrrateo] = mapped_column(SAEnum(MetodoProrrateo, name="metodo_prorrateo", native_enum=True), default=MetodoProrrateo.DIRECTO, nullable=False)
    origen_tipo: Mapped[str | None] = mapped_column(String(50))
    origen_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    documento_ref: Mapped[str | None] = mapped_column(String(100))
    notas: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)

class CostoSnapshot(UUIDPKMixin, Base):
    __tablename__ = "costos_snapshot"
    __table_args__ = (UniqueConstraint("ciclo_id", "fecha", name="uq_snapshot_ciclo_fecha"),)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    ciclo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ciclos_productivos.id"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    costo_mano_obra: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_insumos: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_maquinaria: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_servicios: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_otros: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_total: Mapped[Decimal] = mapped_column(Numeric(18, 4), default=Decimal("0"), nullable=False)
    costo_por_hectarea: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=Decimal("0"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)