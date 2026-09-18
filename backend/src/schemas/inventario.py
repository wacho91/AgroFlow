"""Schemas Pydantic para el contexto de inventario / kardex."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.models.enums import (
    EstadoInsumo,
    MetodoValoracion,
    TipoMovimientoKardex,
)


# ---------- CategoriaInsumo ----------
class CategoriaInsumoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    codigo: str = Field(min_length=1, max_length=50)
    descripcion: str | None = None
    padre_id: uuid.UUID | None = None


class CategoriaInsumoCreate(CategoriaInsumoBase):
    tenant_id: uuid.UUID


class CategoriaInsumoRead(CategoriaInsumoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ---------- Almacen ----------
class AlmacenBase(BaseModel):
    finca_id: uuid.UUID | None = None
    nombre: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    ubicacion: str | None = Field(default=None, max_length=300)
    responsable_id: uuid.UUID | None = None
    activo: bool = True


class AlmacenCreate(AlmacenBase):
    tenant_id: uuid.UUID


class AlmacenRead(AlmacenBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ---------- Insumo ----------
class InsumoBase(BaseModel):
    categoria_id: uuid.UUID | None = None
    nombre: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=50)
    descripcion: str | None = None
    unidad_medida: str = Field(default="unidad", max_length=30)
    metodo_valoracion: MetodoValoracion = MetodoValoracion.PROMEDIO_PONDERADO
    stock_minimo: Decimal = Field(default=Decimal("0"), ge=0)
    stock_maximo: Decimal | None = None
    punto_reorden: Decimal | None = None
    costo_promedio: Decimal = Field(default=Decimal("0"), ge=0)
    estado: EstadoInsumo = EstadoInsumo.ACTIVO
    es_controlado: bool = False


class InsumoCreate(InsumoBase):
    tenant_id: uuid.UUID


class InsumoUpdate(BaseModel):
    categoria_id: uuid.UUID | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=200)
    descripcion: str | None = None
    unidad_medida: str | None = Field(default=None, max_length=30)
    metodo_valoracion: MetodoValoracion | None = None
    stock_minimo: Decimal | None = Field(default=None, ge=0)
    stock_maximo: Decimal | None = None
    punto_reorden: Decimal | None = None
    estado: EstadoInsumo | None = None
    es_controlado: bool | None = None


class InsumoRead(InsumoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ---------- StockActual ----------
class StockActualRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    insumo_id: uuid.UUID
    almacen_id: uuid.UUID
    cantidad: Decimal
    costo_promedio: Decimal
    valor_total: Decimal
    updated_at: datetime


# ---------- MovimientoKardex ----------
class MovimientoKardexBase(BaseModel):
    insumo_id: uuid.UUID
    almacen_id: uuid.UUID
    tipo_movimiento: TipoMovimientoKardex
    fecha: date
    cantidad: Decimal = Field(gt=0)
    costo_unitario: Decimal = Field(default=Decimal("0"), ge=0)
    costo_total: Decimal = Field(default=Decimal("0"), ge=0)
    documento_ref: str | None = Field(default=None, max_length=100)
    ciclo_id: uuid.UUID | None = None
    lote_id: uuid.UUID | None = None
    proveedor: str | None = Field(default=None, max_length=200)
    notas: str | None = None


class MovimientoKardexCreate(MovimientoKardexBase):
    tenant_id: uuid.UUID


class MovimientoKardexRead(MovimientoKardexBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    saldo_cantidad: Decimal
    saldo_valor: Decimal
    created_at: datetime
