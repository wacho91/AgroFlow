import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from .....database import get_db
from .....models.costos import Finca

router = APIRouter()

class ClimaResponse(BaseModel):
    temperatura: float
    sensacion: float
    humedad: int
    descripcion: str
    icono: str
    municipio: str
    alerta: Optional[str] = None

@router.get("/", response_model=ClimaResponse)
async def get_clima(db: AsyncSession = Depends(get_db)):
    # 1. Buscamos la primera finca para sacar el municipio
    result = await db.execute(select(Finca).limit(1))
    finca = result.scalars().first()
    
    if not finca or not finca.municipio:
        raise HTTPException(status_code=404, detail="Registra una finca con municipio para ver el clima.")
    
    municipio = finca.municipio
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # 2. Hacemos la petición a OpenWeatherMap
    async with httpx.AsyncClient() as client:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={municipio},CO&appid={api_key}&units=metric&lang=es"
        response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="No se pudo obtener el clima. Verifica el municipio.")
        
        data = response.json()
        
    # 3. Procesamos la respuesta
    descripcion = data["weather"][0]["description"]
    
    # 4. Lógica de alertas agrícolas
    alerta = None
    if "lluvia" in descripcion or "tormenta" in descripcion:
        alerta = "⚠️ Alerta: Hay lluvia. Evita aplicar fertilizantes líquidos o pesticidas hoy."
    
    return ClimaResponse(
        temperatura=data["main"]["temp"],
        sensacion=data["main"]["feels_like"],
        humedad=data["main"]["humidity"],
        descripcion=descripcion.capitalize(),
        icono=data["weather"][0]["icon"],
        municipio=municipio,
        alerta=alerta
    )