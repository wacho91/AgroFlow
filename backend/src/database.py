import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# Lee la URL desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor asíncrono
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    # Configuración para SQLite local
    connect_args = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # === MAGIA: Configuración SSL para PostgreSQL en la nube (Neon) ===
    connect_args = {"ssl": True}
    # =================================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db