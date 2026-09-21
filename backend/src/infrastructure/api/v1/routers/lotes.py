from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.costos import Lote, Finca

router = APIRouter()

# === SCHEMAS (Pydantic) ===
class LoteCreate(BaseModel):
    finca_id: uuid.UUID
    nombre: str
    codigo: str
    area_ha: Decimal
    estado: Optional[str] = "disponible"

class LoteResponse(LoteCreate):
    id: uuid.UUID
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[LoteResponse])
async def get_lotes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lote))
    return result.scalars().all()

@router.post("/", response_model=LoteResponse)
async def create_lote(lote: LoteCreate, db: AsyncSession = Depends(get_db)):
    # Verificamos que la finca exista
    finca = await db.get(Finca, lote.finca_id)
    if not finca:
        raise HTTPException(status_code=404, detail="La finca seleccionada no existe.")
    
    nuevo_lote = Lote(**lote.dict())
    db.add(nuevo_lote)
    await db.commit()
    await db.refresh(nuevo_lote)
    return nuevo_lote