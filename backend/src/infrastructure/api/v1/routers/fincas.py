from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.costos import Finca
from .....models.tenancy import Tenant

router = APIRouter()

# === SCHEMAS (Pydantic) ===
class FincaCreate(BaseModel):
    nombre: str
    codigo: str
    area_total_ha: Decimal
    municipio: Optional[str] = None
    departamento: Optional[str] = None

class FincaResponse(FincaCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[FincaResponse])
async def get_fincas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Finca))
    return result.scalars().all()

@router.post("/", response_model=FincaResponse)
async def create_finca(finca: FincaCreate, db: AsyncSession = Depends(get_db)):
    # Buscamos el primer tenant disponible para asignarle la finca
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalars().first()
    
    if not tenant:
        raise HTTPException(status_code=400, detail="No hay un Tenant (Organización) creado.")
    
    nueva_finca = Finca(
        tenant_id=tenant.id,
        **finca.dict()
    )
    db.add(nueva_finca)
    await db.commit()
    await db.refresh(nueva_finca)
    return nueva_finca

@router.put("/{finca_id}", response_model=FincaResponse)
async def update_finca(finca_id: uuid.UUID, finca_update: FincaCreate, db: AsyncSession = Depends(get_db)):
    finca = await db.get(Finca, finca_id)
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    
    for field, value in finca_update.dict().items():
        setattr(finca, field, value)
    
    await db.commit()
    await db.refresh(finca)
    return finca

@router.delete("/{finca_id}", status_code=204)
async def delete_finca(finca_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    finca = await db.get(Finca, finca_id)
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    await db.delete(finca)
    await db.commit()
    return None