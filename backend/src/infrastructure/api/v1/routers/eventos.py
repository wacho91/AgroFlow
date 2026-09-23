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

router = APIRouter()

# === SCHEMAS ===
class EventoCreate(BaseModel):
    lote_id: uuid.UUID
    insumo_id: uuid.UUID
    cantidad: Decimal
    costo_unitario: Optional[Decimal] = None  # <--- NUEVO CAMPO
    descripcion: Optional[str] = "Aplicación de insumo"

class EventoResponse(BaseModel):
    id: uuid.UUID
    fecha: date
    lote_id: uuid.UUID
    descripcion: str
    cantidad: Decimal
    unidad_medida: Optional[str] = None  # <--- AGREGADO PARA EL FRONTEND
    costo_total: Decimal
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[EventoResponse])
async def get_eventos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CostoActividad).order_by(CostoActividad.fecha.desc()))
    return result.scalars().all()

@router.post("/", response_model=EventoResponse)
async def create_evento(evento: EventoCreate, db: AsyncSession = Depends(get_db)):
    # 1. Validamos que el lote exista
    lote = await db.get(Lote, evento.lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    # 2. Validamos que el insumo exista y tengamos stock
    insumo = await db.get(Insumo, evento.insumo_id)
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    
    if insumo.stock_actual < evento.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Solo hay {insumo.stock_actual} {insumo.unidad_medida} disponibles.")
    
    # 3. Calculamos el costo (Si el usuario envía un costo, lo usamos. Si no, usamos el del insumo)
    if evento.costo_unitario is not None and evento.costo_unitario > 0:
        costo_unitario = Decimal(str(evento.costo_unitario))
    else:
        costo_unitario = Decimal(str(insumo.costo_promedio)) if insumo.costo_promedio and insumo.costo_promedio > 0 else Decimal("0")
        
    cantidad = Decimal(str(evento.cantidad))
    costo_total = costo_unitario * cantidad
    
    # 4. Descontamos el inventario
    insumo.stock_actual = Decimal(str(insumo.stock_actual)) - cantidad
    
    # 5. Creamos el evento de costo (Event Sourcing)
    nuevo_evento = CostoActividad(
        tenant_id=lote.tenant_id,
        lote_id=lote.id,
        ciclo_id=None,
        tipo_costo="insumos",
        fecha=date.today(),
        descripcion=f"{evento.descripcion} ({insumo.nombre})",
        cantidad=cantidad,
        unidad_medida=insumo.unidad_medida,
        costo_unitario=costo_unitario,
        costo_total=costo_total,
        origen_tipo="insumo",
        origen_id=insumo.id
    )
    
    db.add(nuevo_evento)
    await db.commit()
    await db.refresh(nuevo_evento)
    return nuevo_evento

@router.delete("/{evento_id}", status_code=204)
async def delete_evento(evento_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    evento = await db.get(CostoActividad, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Si el evento viene de un insumo, le devolvemos el stock
    if evento.origen_tipo == "insumo" and evento.origen_id:
        insumo = await db.get(Insumo, evento.origen_id)
        if insumo:
            insumo.stock_actual = Decimal(str(insumo.stock_actual)) + Decimal(str(evento.cantidad))
    
    await db.delete(evento)
    await db.commit()
    return None