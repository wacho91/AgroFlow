from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt
import os
from datetime import datetime, timedelta

# 5 puntitos para subir hasta src/
from .....database import get_db
from .....models.tenancy import Usuario

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "agroflow_super_secreto_2024")
ALGORITHM = "HS256"

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db), email: str = Body(...), password: str = Body(...)):
    # 1. Buscamos el usuario en SQLite por su email
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalars().first()
    
    # 2. Validamos que exista y que la contraseña sea correcta
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # 3. Generamos el Token JWT
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}