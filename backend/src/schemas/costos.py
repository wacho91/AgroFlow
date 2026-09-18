"""Schemas Pydantic para el contexto de costos."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import EstadoCiclo, MetodoProrrateo, TipoCosto


# ---------- Finca ----------
class FincaBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    area_total_ha: Decimal = Field(default=Decimal("0"), ge=0)
    altitud_msnm: Decimal | None = None
    municipio: str | None = Field(default=None, max_length=150)
    departamento: str | None = Field(default=None, max_length=150)
    pais: str = Field(default="CO", min_length=2, max_length=2)
    tipo_suelo: str | None = Field(default=None, max_length=100)
    fuente_agua: str | None = Field(default=None, max_length=100)
    notas: str | None = None


class FincaCreate(FincaBase):
    tenant_id: uuid.UUID


class FincaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=200)
    area_total_ha: Decimal | None = Field(default=None, ge=0)
    altitud_msnm: Decimal | None = None
    municipio: str | None = None
    departamento: str | None = None
    tipo_suelo: str | None = None
    fuente_agua: str | None = None
    notas: str | None = None


class FincaRead(FincaBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- Lote ----------
class LoteBase(BaseModel):
    finca_id: uuid.UUID
    nombre: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    area_ha: Decimal = Field(gt=0)
    tipo_suelo: str | None = Field(default=None, max_length=100)
    ph_suelo: Decimal | None = None
    drenaje: str | None = Field(default=None, max_length=50)
    pendiente_pct: Decimal | None = None
    capacidad_uso: str | None = Field(default=None, max_length=100)
    estado: str = Field(default="disponible", max_length=30)
    notas: str | None = None


class LoteCreate(LoteBase):
    tenant_id: uuid.UUID


class LoteUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=200)
    area_ha: Decimal | None = Field(default=None, gt=0)
    tipo_suelo: str | None = None
    ph_suelo: Decimal | None = None
    drenaje: str | None = None
    pendiente_pct: Decimal | None = None
    capacidad_uso: str | None = None
    estado: str | None = Field(default=None, max_length=30)
    notas: str | None = None


class LoteRead(LoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- Cultivo ----------
class CultivoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    nombre_cientifico: str | None = Field(default=None, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    variedad: str | None = Field(default=None, max_length=150)
    ciclo_dias: int | None = Field(default=None, ge=0)
    unidad_medida: str = Field(default="kg", max_length=30)
    rendimiento_esperado: Decimal | None = None
    precio_referencia: Decimal | None = None
    activo: bool = True


class CultivoCreate(CultivoBase):
    tenant_id: uuid.UUID


class CultivoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    nombre_cientifico: str | None = None
    variedad: str | None = None
    ciclo_dias: int | None = Field(default=None, ge=0)
    unidad_medida: str | None = Field(default=None, max_length=30)
    rendimiento_esperado: Decimal | None = None
    precio_referencia: Decimal | None = None
    activo: bool | None = None


class CultivoRead(CultivoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- CicloProductivo ----------
class CicloProductivoBase(BaseModel):
    lote_id: uuid.UUID
    cultivo_id: uuid.UUID
    codigo: str = Field(min_length=1, max_length=50)
    nombre: str | None = Field(default=None, max_length=200)
    fecha_inicio: date
    fecha_fin_estimada: date | None = None
    area_sembrada_ha: Decimal = Field(gt=0)
    densidad_siembra: Decimal | None = None
    produccion_estimada: Decimal | None = None
    unidad_produccion: str = Field(default="kg", max_length=30)
    notas: str | None = None


class CicloProductivoCreate(CicloProductivoBase):
    tenant_id: uuid.UUID


class CicloProductivoUpdate(BaseModel):
    nombre: str | None = None
    fecha_fin_estimada: date | None = None
    fecha_fin_real: date | None = None
    estado: EstadoCiclo | None = None
    produccion_real: Decimal | None = None
    notas: str | None = None


class CicloProductivoRead(CicloProductivoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    fecha_fin_real: date | None
    estado: EstadoCiclo
    produccion_real: Decimal | None
    costo_total: Decimal
    costo_unitario: Decimal | None
    ingreso_total: Decimal
    margen_bruto: Decimal
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- Actividad ----------
class ActividadBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    tipo_costo: TipoCosto
    descripcion: str | None = None
    unidad_medida: str | None = Field(default=None, max_length=30)
    requiere_insumo: bool = False
    requiere_mano_obra: bool = True
    requiere_maquinaria: bool = False
    activo: bool = True


class ActividadCreate(ActividadBase):
    tenant_id: uuid.UUID


class ActividadUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=200)
    tipo_costo: TipoCosto | None = None
    descripcion: str | None = None
    unidad_medida: str | None = None
    requiere_insumo: bool | None = None
    requiere_mano_obra: bool | None = None
    requiere_maquinaria: bool | None = None
    activo: bool | None = None


class ActividadRead(ActividadBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


# ---------- CostoActividad ----------
class CostoActividadBase(BaseModel):
    ciclo_id: uuid.UUID
    actividad_id: uuid.UUID | None = None
    lote_id: uuid.UUID
    tipo_costo: TipoCosto
    fecha: date
    descripcion: str | None = Field(default=None, max_length=500)
    cantidad: Decimal = Field(default=Decimal("1"), ge=0)
    unidad_medida: str | None = Field(default=None, max_length=30)
    costo_unitario: Decimal = Field(default=Decimal("0"), ge=0)
    costo_total: Decimal = Field(default=Decimal("0"), ge=0)
    metodo_prorrateo: MetodoProrrateo = MetodoProrrateo.DIRECTO
    origen_tipo: str | None = Field(default=None, max_length=50)
    origen_id: uuid.UUID | None = None
    documento_ref: str | None = Field(default=None, max_length=100)
    notas: str | None = None


class CostoActividadCreate(CostoActividadBase):
    tenant_id: uuid.UUID


class CostoActividadRead(CostoActividadBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    metadata_: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
