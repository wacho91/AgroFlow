from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.nomina import Jornalero
from .....models.tenancy import Tenant

router = APIRouter()

# === SCHEMAS ===
class JornaleroCreate(BaseModel):
    nombre_completo: str
    documento: str
    telefono: Optional[str] = None
    tipo: str = "temporal"

class JornaleroResponse(JornaleroCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[JornaleroResponse])
async def get_jornaleros(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Jornalero).order_by(Jornalero.nombre_completo))
    return result.scalars().all()

@router.post("/", response_model=JornaleroResponse)
async def create_jornalero(jornalero: JornaleroCreate, db: AsyncSession = Depends(get_db)):
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalars().first()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="No hay un Tenant (Organización) creado.")
    
    nuevo_jornalero = Jornalero(
        tenant_id=tenant.id,
        **jornalero.dict()
    )
    db.add(nuevo_jornalero)
    await db.commit()
    await db.refresh(nuevo_jornalero)
    return nuevo_jornalero

# === NUEVAS RUTAS: ACTUALIZAR Y ELIMINAR ===
@router.patch("/{jornalero_id}", response_model=JornaleroResponse)
async def update_jornalero(jornalero_id: uuid.UUID, payload: JornaleroCreate, db: AsyncSession = Depends(get_db)):
    db_jornalero = await db.get(Jornalero, jornalero_id)
    if not db_jornalero:
        raise HTTPException(status_code=404, detail="Jornalero no encontrado")
    
    for field, value in payload.dict().items():
        setattr(db_jornalero, field, value)
    
    await db.commit()
    await db.refresh(db_jornalero)
    return db_jornalero

@router.delete("/{jornalero_id}", status_code=204)
async def delete_jornalero(jornalero_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    db_jornalero = await db.get(Jornalero, jornalero_id)
    if not db_jornalero:
        raise HTTPException(status_code=404, detail="Jornalero no encontrado")
    
    await db.delete(db_jornalero)
    await db.commit()
    return None