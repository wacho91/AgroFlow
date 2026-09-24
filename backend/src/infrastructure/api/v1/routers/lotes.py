from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.costos import Lote, Finca, CostoActividad

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
    costo_acumulado: Decimal = Decimal("0")  # <--- NUEVO CAMPO
    class Config:
        from_attributes = True

# === ENDPOINTS ===
@router.get("/", response_model=list[LoteResponse])
async def get_lotes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lote))
    lotes = result.scalars().all()

    # === MAGIA: Calculamos el costo acumulado de cada lote ===
    # Buscamos todos los costos agrupados por lote_id
    stmt_costs = select(CostoActividad.lote_id, func.sum(CostoActividad.costo_total)).group_by(CostoActividad.lote_id)
    result_costs = await db.execute(stmt_costs)
    costs_map = {row[0]: Decimal(str(row[1])) for row in result_costs.all()}

    # Construemos la respuesta combinando el lote y su costo
    lotes_response = []
    for lote in lotes:
        lote_dict = {
            "id": lote.id,
            "finca_id": lote.finca_id,
            "nombre": lote.nombre,
            "codigo": lote.codigo,
            "area_ha": lote.area_ha,
            "estado": lote.estado,
            "costo_acumulado": costs_map.get(lote.id, Decimal("0"))
        }
        lotes_response.append(LoteResponse(**lote_dict))

    return lotes_response

@router.post("/", response_model=LoteResponse)
async def create_lote(lote: LoteCreate, db: AsyncSession = Depends(get_db)):
    # Verificamos que la finca exista
    finca = await db.get(Finca, lote.finca_id)
    if not finca:
        raise HTTPException(status_code=404, detail="La finca seleccionada no existe.")
    
    # Copiamos el tenant_id de la finca al lote
    lote_data = lote.dict()
    lote_data['tenant_id'] = finca.tenant_id
    
    nuevo_lote = Lote(**lote_data)
    db.add(nuevo_lote)
    await db.commit()
    await db.refresh(nuevo_lote)
    return nuevo_lote