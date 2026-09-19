import asyncio
import uuid
from src.database import AsyncSessionLocal
from src.models.tenancy import Tenant, Usuario
from passlib.context import CryptContext
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    async with AsyncSessionLocal() as db:
        # 1. Buscamos o creamos un Tenant (Finca) por defecto
        result = await db.execute(select(Tenant).limit(1))
        tenant = result.scalars().first()
        if not tenant:
            tenant = Tenant(id=uuid.uuid4(), nombre="Finca Demo", slug="finca-demo", moneda="COP")
            db.add(tenant)
            await db.flush()

        # 2. Creamos el usuario Admin
        admin_email = "admin@agroflow.com"
        result = await db.execute(select(Usuario).where(Usuario.email == admin_email))
        user = result.scalars().first()
        
        if not user:
            user = Usuario(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                email=admin_email,
                nombre_completo="Administrador",
                password_hash=pwd_context.hash("Admin123#"), # Contraseña: Admin123#
                activo=True
            )
            db.add(user)
            await db.commit()
            print("✅ Usuario admin creado. Email: admin@agroflow.com | Pass: Admin123#")
        else:
            print("El usuario admin ya existe.")

asyncio.run(main())