from fastapi import APIRouter

api_router = APIRouter()

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

try:
    from .routers import auth
    api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
except ImportError:
    pass

# === NUEVA RUTA DE FINCAS ===
try:
    from .routers import fincas
    api_router.include_router(fincas.router, prefix="/fincas", tags=["Fincas"])
except ImportError:
    pass

# === RUTA DE LOTES ===
try:
    from .routers import lotes
    api_router.include_router(lotes.router, prefix="/lotes", tags=["Lotes"])
except ImportError:
    pass

# === NUEVA RUTA DE INSUMOS ===
try:
    from .routers import insumos
    api_router.include_router(insumos.router, prefix="/insumos", tags=["Insumos"])
except ImportError:
    pass
# =============================

# === NUEVA RUTA DE CULTIVOS ===
try:
    from .routers import cultivos
    api_router.include_router(cultivos.router, prefix="/cultivos", tags=["Cultivos"])
except ImportError:
    pass
# ==============================

# === NUEVA RUTA DE TESORERÍA ===
try:
    from .routers import tesoreria
    api_router.include_router(tesoreria.router, prefix="/tesoreria", tags=["Tesorería"])
except ImportError:
    pass
# ==============================

# === NUEVA RUTA DE EVENTOS / COSTOS ===
try:
    from .routers import eventos
    api_router.include_router(eventos.router, prefix="/eventos", tags=["Eventos Agrícolas"])
except ImportError:
    pass
# ======================================

# === NUEVA RUTA DE JORNALEROS ===
try:
    from .routers import jornaleros
    api_router.include_router(jornaleros.router, prefix="/jornaleros", tags=["Jornaleros"])
except ImportError:
    pass
# ================================

# === NUEVA RUTA DE CICLOS PRODUCTIVOS ===
try:
    from .routers import ciclos
    api_router.include_router(ciclos.router, prefix="/ciclos", tags=["Ciclos Productivos"])
except ImportError:
    pass
# ========================================

router = api_router