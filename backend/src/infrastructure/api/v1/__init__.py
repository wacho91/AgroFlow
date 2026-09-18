from fastapi import APIRouter

# Creamos el router principal
api_router = APIRouter()

# Cargamos los routers desde la subcarpeta 'routers'
try:
    from .routers import tenancy
    api_router.include_router(tenancy.router, prefix="/tenancy", tags=["Tenancy"])
except ImportError:
    pass

try:
    from .routers import costos
    api_router.include_router(costos.router, prefix="/costos", tags=["Costos"])
except ImportError:
    pass

try:
    from .routers import inventario
    api_router.include_router(inventario.router, prefix="/inventario", tags=["Inventario"])
except ImportError:
    pass

try:
    from .routers import nomina
    api_router.include_router(nomina.router, prefix="/nomina", tags=["Nomina"])
except ImportError:
    pass

# Exportamos la variable que main.py está buscando
router = api_router