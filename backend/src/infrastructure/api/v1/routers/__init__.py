from fastapi import APIRouter
from .routers import router

api_router = APIRouter()

# === MAGIA: Cargamos automáticamente todos los routers de esta carpeta ===
try:
    from .fincas import router as fincas_router
    api_router.include_router(fincas_router, prefix="/fincas", tags=["Fincas"])
except ImportError:
    pass

try:
    from .lotes import router as lotes_router
    api_router.include_router(lotes_router, prefix="/lotes", tags=["Lotes"])
except ImportError:
    pass

try:
    from .insumos import router as insumos_router
    api_router.include_router(insumos_router, prefix="/insumos", tags=["Insumos"])
except ImportError:
    pass

try:
    from .jornaleros import router as jornaleros_router
    api_router.include_router(jornaleros_router, prefix="/jornaleros", tags=["Jornaleros"])
except ImportError:
    pass

try:
    from .auth import router as auth_router
    api_router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
except ImportError:
    pass

try:
    from .usuarios import router as usuarios_router
    api_router.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
except ImportError:
    pass

try:
    from .cultivos import router as cultivos_router
    api_router.include_router(cultivos_router, prefix="/cultivos", tags=["Cultivos"])
except ImportError:
    pass

# Exportamos el router unificado
router = api_router