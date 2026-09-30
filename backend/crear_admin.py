import asyncio
import uuid
from src.database import AsyncSessionLocal
from src.models.tenancy import Tenant, Usuario
import bcrypt # <--- Usamos bcrypt directo
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Tenant).limit(1))
        tenant = result.scalars().first()
        if not tenant:
            tenant = Tenant(id=uuid.uuid4(), nombre="Finca Demo", slug="finca-demo", moneda="COP")
            db.add(tenant)
            await db.flush()

        admin_email = "admin@agroflow.com"
        result = await db.execute(select(Usuario).where(Usuario.email == admin_email))
        user = result.scalars().first()
        
        if not user:
            # === MAGIA: Encriptar contraseña con bcrypt directo ===
            password_bytes = "admin123".encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
            
            user = Usuario(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                email=admin_email,
                nombre_completo="Cristian Admin",
                password_hash=hashed_password,
                activo=True
            )
            db.add(user)
            await db.commit()
            print("✅ Usuario admin creado. Email: admin@agroflow.com | Pass: admin123")
        else:
            print("El usuario admin ya existe.")

asyncio.run(main())