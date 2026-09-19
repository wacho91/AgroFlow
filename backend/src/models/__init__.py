"""
Registro central de modelos SQLAlchemy.
Usamos try/except para evitar que el servidor se caiga si falta un archivo.
"""
from .database import Base

try:
    from .audit import AuditLog, IdempotencyKey
except ImportError:
    pass

try:
    from .costos import (
        Actividad, CicloProductivo, CostoActividad, CostoSnapshot,
        Cultivo, Finca, Lote,
    )
except ImportError:
    pass

try:
    from .enums import *
except ImportError:
    pass

try:
    from .inventario import (
        Almacen, CapaConsumo, CapaKardex, CategoriaInsumo,
        Insumo, MovimientoKardex, StockActual,
    )
except ImportError:
    pass

try:
    from .nomina import (
        Jornalero, Labor, Liquidacion, NovedadNomina,
    )
except ImportError:
    pass

try:
    from .tenancy import Tenant, Usuario
except ImportError:
    pass