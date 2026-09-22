from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from decimal import Decimal
from datetime import date
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.tesoreria import MovimientoTesoreria
from .....models.tenancy import Tenant

router = APIRouter()

# === SCHEMAS (Pydantic) ===
class MovimientoCreate(BaseModel):
    fecha: date
    tipo: str  # "ingreso" o "egreso"
    concepto: str
    monto: Decimal

class MovimientoResponse(MovimientoCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[MovimientoResponse])
async def get_movimientos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovimientoTesoreria).order_by(MovimientoTesoreria.fecha.desc()))
    return result.scalars().all()

@router.post("/", response_model=MovimientoResponse)
async def create_movimiento(mov: MovimientoCreate, db: AsyncSession = Depends(get_db)):
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalars().first()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="No hay un Tenant (Organización) creado.")
    
    nuevo_mov = MovimientoTesoreria(
        tenant_id=tenant.id,
        **mov.dict()
    )
    db.add(nuevo_mov)
    await db.commit()
    await db.refresh(nuevo_mov)
    return nuevo_mov

@router.delete("/{mov_id}", status_code=204)
async def delete_movimiento(mov_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    mov = await db.get(MovimientoTesoreria, mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    await db.delete(mov)
    await db.commit()
    return None