from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date
import uuid

from .....database import get_db
from .....models.costos import CostoActividad, Lote
from .....models.inventario import Insumo
from .....models.nomina import Jornalero  # <--- IMPORTADO

router = APIRouter()

class EventoCreate(BaseModel):
    lote_id: uuid.UUID
    insumo_id: Optional[uuid.UUID] = None  # Ahora es opcional
    jornalero_id: Optional[uuid.UUID] = None  # <--- NUEVO
    cantidad: Decimal
    costo_unitario: Optional[Decimal] = None
    descripcion: Optional[str] = "Aplicación de insumo"

class EventoResponse(BaseModel):
    id: uuid.UUID
    fecha: date
    lote_id: uuid.UUID
    descripcion: str
    cantidad: Decimal
    unidad_medida: Optional[str] = None
    costo_unitario: Optional[Decimal] = None
    costo_total: Decimal
    class Config:
        from_attributes = True

@router.get("/", response_model=list[EventoResponse])
async def get_eventos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CostoActividad).order_by(CostoActividad.fecha.desc()))
    return result.scalars().all()

@router.post("/", response_model=EventoResponse)
async def create_evento(evento: EventoCreate, db: AsyncSession = Depends(get_db)):
    lote = await db.get(Lote, evento.lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    cantidad = Decimal(str(evento.cantidad))
    costo_unitario = Decimal(str(evento.costo_unitario)) if evento.costo_unitario and evento.costo_unitario > 0 else Decimal("0")
    costo_total = costo_unitario * cantidad

    # Lógica si es INSUMO
    if evento.insumo_id:
        insumo = await db.get(Insumo, evento.insumo_id)
        if not insumo: raise HTTPException(status_code=404, detail="Insumo no encontrado")
        if insumo.stock_actual < cantidad: raise HTTPException(status_code=400, detail="Stock insuficiente")
        
        if costo_unitario == 0:
            costo_unitario = Decimal(str(insumo.costo_promedio)) if insumo.costo_promedio else Decimal("0")
            costo_total = costo_unitario * cantidad
            
        insumo.stock_actual = Decimal(str(insumo.stock_actual)) - cantidad
        nuevo_evento = CostoActividad(
            tenant_id=lote.tenant_id, lote_id=lote.id, tipo_costo="insumos", fecha=date.today(),
            descripcion=f"{evento.descripcion} ({insumo.nombre})", cantidad=cantidad,
            unidad_medida=insumo.unidad_medida, costo_unitario=costo_unitario, costo_total=costo_total,
            origen_tipo="insumo", origen_id=insumo.id
        )

    # Lógica si es JORNALERO (Mano de Obra)
    elif evento.jornalero_id:
        jornalero = await db.get(Jornalero, evento.jornalero_id)
        if not jornalero: raise HTTPException(status_code=404, detail="Jornalero no encontrado")
        
        nuevo_evento = CostoActividad(
            tenant_id=lote.tenant_id, lote_id=lote.id, tipo_costo="mano_obra", fecha=date.today(),
            descripcion=f"{evento.descripcion} ({jornalero.nombre_completo})", cantidad=cantidad,
            unidad_medida="jornal", costo_unitario=costo_unitario, costo_total=costo_total,
            origen_tipo="jornalero", origen_id=jornalero.id
        )
    else:
        raise HTTPException(status_code=400, detail="Debe seleccionar un insumo o un jornalero")

    db.add(nuevo_evento)
    await db.commit()
    await db.refresh(nuevo_evento)
    return nuevo_evento

@router.delete("/{evento_id}", status_code=204)
async def delete_evento(evento_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    evento = await db.get(CostoActividad, evento_id)
    if not evento: raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Si era insumo, devolvemos stock
    if evento.origen_tipo == "insumo" and evento.origen_id:
        insumo = await db.get(Insumo, evento.origen_id)
        if insumo: insumo.stock_actual = Decimal(str(insumo.stock_actual)) + Decimal(str(evento.cantidad))
    
    await db.delete(evento)
    await db.commit()
    return None