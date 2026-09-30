from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
import os
from datetime import datetime, timedelta
import bcrypt # <--- Usamos bcrypt directo

from .....database import get_db
from .....models.tenancy import Usuario

router = APIRouter()
SECRET_KEY = os.getenv("JWT_SECRET", "agroflow_super_secreto_2024")
ALGORITHM = "HS256"

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db), email: str = Body(...), password: str = Body(...)):
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # === MAGIA: Verificar contraseña con bcrypt directo ===
    password_bytes = password.encode('utf-8')
    hash_bytes = user.password_hash.encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, hash_bytes):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    # ======================================================
    
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}