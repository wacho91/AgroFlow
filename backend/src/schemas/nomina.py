"""Schemas Pydantic para el contexto de nómina."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import (
    EstadoLabor,
    EstadoLiquidacion,
    TipoJornalero,
    TipoNovedadNomina,
)


# ---------- Jornalero ----------
class JornaleroBase(BaseModel):
    nombre_completo: str = Field(min_length=1, max_length=200)
    documento: str = Field(min_length=1, max_length=30)
    tipo: TipoJornalero = TipoJornalero.JORNALERO
    telefono: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=200)
    valor_jornal: Decimal = Field(default=Decimal("0"), ge=0)
    activo: bool = True
    notas: str | None = None


class JornaleroCreate(JornaleroBase):
    tenant_id: uuid.UUID


class JornaleroUpdate(BaseModel):
    nombre_completo: str | None = Field(default=None, min_length=1, max_length=200)
    telefono: str | None = None
    email: str | None = None
    valor_jornal: Decimal | None = Field(default=None, ge=0)
    activo: bool | None = None
    notas: str | None = None


class JornaleroRead(JornaleroBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- Labor ----------
class LaborBase(BaseModel):
    jornalero_id: uuid.UUID
    ciclo_id: uuid.UUID | None = None
    lote_id: uuid.UUID | None = None
    actividad_id: uuid.UUID | None = None
    fecha: date
    horas_trabajadas: Decimal = Field(default=Decimal("8"), gt=0)
    valor_jornal: Decimal = Field(default=Decimal("0"), ge=0)
    valor_total: Decimal = Field(default=Decimal("0"), ge=0)
    estado: EstadoLabor = EstadoLabor.REGISTRADA
    descripcion: str | None = Field(default=None, max_length=500)
    notas: str | None = None


class LaborCreate(LaborBase):
    tenant_id: uuid.UUID


class LaborUpdate(BaseModel):
    horas_trabajadas: Decimal | None = Field(default=None, gt=0)
    valor_jornal: Decimal | None = Field(default=None, ge=0)
    valor_total: Decimal | None = Field(default=None, ge=0)
    estado: EstadoLabor | None = None
    descripcion: str | None = None
    notas: str | None = None


class LaborRead(LaborBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- Liquidacion ----------
class LiquidacionBase(BaseModel):
    jornalero_id: uuid.UUID
    periodo_inicio: date
    periodo_fin: date
    total_jornales: Decimal = Field(default=Decimal("0"), ge=0)
    total_horas: Decimal = Field(default=Decimal("0"), ge=0)
    subtotal: Decimal = Field(default=Decimal("0"), ge=0)
    total_bonificaciones: Decimal = Field(default=Decimal("0"), ge=0)
    total_descuentos: Decimal = Field(default=Decimal("0"), ge=0)
    total_neto: Decimal = Field(default=Decimal("0"), ge=0)
    estado: EstadoLiquidacion = EstadoLiquidacion.BORRADOR
    notas: str | None = None


class LiquidacionCreate(LiquidacionBase):
    tenant_id: uuid.UUID


class LiquidacionRead(LiquidacionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    fecha_pago: date | None
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- NovedadNomina ----------
class NovedadNominaBase(BaseModel):
    jornalero_id: uuid.UUID
    liquidacion_id: uuid.UUID | None = None
    tipo: TipoNovedadNomina
    fecha: date
    valor: Decimal = Field(default=Decimal("0"), ge=0)
    cantidad: Decimal | None = None
    descripcion: str | None = Field(default=None, max_length=500)


class NovedadNominaCreate(NovedadNominaBase):
    tenant_id: uuid.UUID


class NovedadNominaRead(NovedadNominaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
