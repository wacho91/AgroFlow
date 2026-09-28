from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.costos import Cultivo
from .....models.tenancy import Tenant

router = APIRouter()

# === SCHEMAS (Pydantic) ===
class CultivoCreate(BaseModel):
    nombre: str
    codigo: str
    variedad: Optional[str] = None
    ciclo_dias: Optional[int] = 90
    unidad_medida: str = "kg"
    rendimiento_esperado: Optional[Decimal] = None

class CultivoResponse(CultivoCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[CultivoResponse])
async def get_cultivos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cultivo))
    return result.scalars().all()

@router.post("/", response_model=CultivoResponse)
async def create_cultivo(cultivo: CultivoCreate, db: AsyncSession = Depends(get_db)):
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalars().first()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="No hay un Tenant (Organización) creado.")
    
    nuevo_cultivo = Cultivo(
        tenant_id=tenant.id,
        **cultivo.dict()
    )
    db.add(nuevo_cultivo)
    await db.commit()
    await db.refresh(nuevo_cultivo)
    return nuevo_cultivo

@router.put("/{cultivo_id}", response_model=CultivoResponse)
async def update_cultivo(cultivo_id: uuid.UUID, cultivo_update: CultivoCreate, db: AsyncSession = Depends(get_db)):
    cultivo = await db.get(Cultivo, cultivo_id)
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    
    for field, value in cultivo_update.dict().items():
        setattr(cultivo, field, value)
    
    await db.commit()
    await db.refresh(cultivo)
    return cultivo

@router.delete("/{cultivo_id}", status_code=204)
async def delete_cultivo(cultivo_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    cultivo = await db.get(Cultivo, cultivo_id)
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    await db.delete(cultivo)
    await db.commit()
    return None