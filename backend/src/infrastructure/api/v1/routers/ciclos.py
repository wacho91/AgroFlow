from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date
import uuid
from sqlalchemy.exc import IntegrityError

from .....database import get_db
from .....models.costos import CicloProductivo, Lote, Cultivo, CostoActividad, EstadoCiclo

router = APIRouter()

# === SCHEMAS ===
class CicloCreate(BaseModel):
    lote_id: uuid.UUID
    cultivo_id: uuid.UUID
    codigo: str
    nombre: Optional[str] = None
    area_sembrada_ha: Decimal

class CicloResponse(CicloCreate):
    id: uuid.UUID
    fecha_inicio: date
    estado: str
    costo_total: Decimal
    ingreso_total: Decimal
    margen_bruto: Decimal
    class Config:
        from_attributes = True

# === NUEVO SCHEMA PARA LA COSECHA ===
class CosechaCreate(BaseModel):
    produccion_real: Decimal
    precio_venta: Decimal

# === ENDPOINTS ===
@router.get("/", response_model=list[CicloResponse])
async def get_ciclos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CicloProductivo).order_by(CicloProductivo.fecha_inicio.desc()))
    return result.scalars().all()

@router.post("/", response_model=CicloResponse)
async def create_ciclo(ciclo: CicloCreate, db: AsyncSession = Depends(get_db)):
    # 1. Validamos que el lote exista
    lote = await db.get(Lote, ciclo.lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    # 2. Validamos que el cultivo exista
    cultivo = await db.get(Cultivo, ciclo.cultivo_id)
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    
    # 3. Magia financiera: Calculamos el costo que el lote ya lleva acumulado
    stmt_costos = select(func.sum(CostoActividad.costo_total)).where(CostoActividad.lote_id == lote.id)
    result_costos = await db.execute(stmt_costos)
    costo_inicial = result_costos.scalar() or Decimal("0")
    
    # 4. Creamos el ciclo productivo (La siembra)
    nuevo_ciclo = CicloProductivo(
        tenant_id=lote.tenant_id,
        lote_id=lote.id,
        cultivo_id=cultivo.id,
        codigo=ciclo.codigo,
        nombre=ciclo.nombre or f"Siembra de {cultivo.nombre}",
        fecha_inicio=date.today(),
        estado=EstadoCiclo.EN_CURSO.value,
        area_sembrada_ha=ciclo.area_sembrada_ha,
        costo_total=Decimal(str(costo_inicial)),
        ingreso_total=Decimal("0"),
        margen_bruto=Decimal("0") - Decimal(str(costo_inicial))
    )
    
    db.add(nuevo_ciclo)
    
    # Blindaje contra códigos duplicados
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un ciclo con este código. Usa uno diferente (ej. CIC-002).")
    
    await db.refresh(nuevo_ciclo)
    return nuevo_ciclo

# === NUEVO ENDPOINT: REGISTRAR COSECHA ===
@router.post("/{ciclo_id}/cosechar", response_model=CicloResponse)
async def registrar_cosecha(ciclo_id: uuid.UUID, cosecha: CosechaCreate, db: AsyncSession = Depends(get_db)):
    ciclo = await db.get(CicloProductivo, ciclo_id)
    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")
    
    if ciclo.estado == EstadoCiclo.CERRADO.value:
        raise HTTPException(status_code=400, detail="Este ciclo ya está cerrado y cosechado.")

    # 1. Calculamos el ingreso total (Kilos * Precio)
    produccion = Decimal(str(cosecha.produccion_real))
    precio = Decimal(str(cosecha.precio_venta))
    ingreso_total = produccion * precio

    # 2. Actualizamos el ciclo
    ciclo.produccion_real = produccion
    ciclo.ingreso_total = ingreso_total
    ciclo.margen_bruto = ingreso_total - Decimal(str(ciclo.costo_total))
    ciclo.estado = EstadoCiclo.CERRADO.value # Cambiamos el estado a "cerrado"
    ciclo.fecha_fin_real = date.today()

    await db.commit()
    await db.refresh(ciclo)
    return ciclo