from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.inventario import Insumo
from .....models.tenancy import Tenant

router = APIRouter()

# === SCHEMAS (Pydantic) ===
class InsumoCreate(BaseModel):
    nombre: str
    codigo: str
    unidad_medida: str = "kg"
    stock_actual: Decimal = Decimal("0")
    stock_minimo: Decimal = Decimal("0")

class InsumoResponse(InsumoCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[InsumoResponse])
async def get_insumos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Insumo))
    return result.scalars().all()

@router.post("/", response_model=InsumoResponse)
async def create_insumo(insumo: InsumoCreate, db: AsyncSession = Depends(get_db)):
    # Buscamos el primer tenant para asignarle el insumo
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalars().first()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="No hay un Tenant (Organización) creado.")
    
    nuevo_insumo = Insumo(
        tenant_id=tenant.id,
        **insumo.dict()
    )
    db.add(nuevo_insumo)
    await db.commit()
    await db.refresh(nuevo_insumo)
    return nuevo_insumo