import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import uuid

from .....database import get_db
from .....models.costos import Finca

router = APIRouter()

class ClimaResponse(BaseModel):
    finca_id: uuid.UUID
    nombre_finca: str
    temperatura: float
    sensacion: float
    humedad: int
    descripcion: str
    icono: str
    municipio: str
    alerta: Optional[str] = None

@router.get("/", response_model=list[ClimaResponse])
async def get_clima(db: AsyncSession = Depends(get_db)):
    # 1. Buscamos TODAS las fincas que tengan un municipio registrado
    result = await db.execute(select(Finca).where(Finca.municipio.isnot(None)))
    fincas = result.scalars().all()
    
    if not fincas:
        raise HTTPException(status_code=404, detail="Registra fincas con municipio para ver el clima.")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    climas_data = []
    
    # 2. Hacemos la petición a OpenWeatherMap para cada finca
    async with httpx.AsyncClient() as client:
        for finca in fincas:
            municipio = finca.municipio
            url = f"http://api.openweathermap.org/data/2.5/weather?q={municipio},CO&appid={api_key}&units=metric&lang=es"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                descripcion = data["weather"][0]["description"]
                
                # 3. Lógica de alertas agrícolas (Siempre enviamos un mensaje)
                alerta = None
                if "lluvia" in descripcion or "tormenta" in descripcion:
                    alerta = "⚠️ Alerta: Hay lluvia. Evita aplicar fertilizantes líquidos o pesticidas hoy."
                else:
                    alerta = "✅ Clima óptimo: Condiciones favorables para aplicar fertilizantes y labores de campo."
                
                climas_data.append(ClimaResponse(
                    finca_id=finca.id,
                    nombre_finca=finca.nombre,
                    temperatura=data["main"]["temp"],
                    sensacion=data["main"]["feels_like"],
                    humedad=data["main"]["humidity"],
                    descripcion=descripcion.capitalize(),
                    icono=data["weather"][0]["icon"],
                    municipio=municipio,
                    alerta=alerta
                ))
                
    return climas_data