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

# Creamos el motor asíncrono. 
# Si es SQLite, le quitamos el "check_same_thread" para que FastAPI funcione bien.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

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