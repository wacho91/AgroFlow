"""
Registro central de modelos SQLAlchemy.
Importar aquí garantiza que Alembic y Base.metadata los detecten.
"""
from src.models.audit import AuditLog, IdempotencyKey
from src.models.costos import (
    Actividad,
    CicloProductivo,
    CostoActividad,
    CostoSnapshot,
    Cultivo,
    Finca,
    Lote,
)
from src.models.enums import (
    AccionAuditoria,
    CondicionClimatica,
    EstadoCiclo,
    EstadoInsumo,
    EstadoLabor,
    EstadoLiquidacion,
    EstadoObligacion,
    EstadoTenant,
    FuenteClima,
    MetodoProrrateo,
    MetodoValoracion,
    RolUsuario,
    TipoCosto,
    TipoCuentaBancaria,
    TipoJornalero,
    TipoMovimientoKardex,
    TipoMovimientoTesoreria,
    TipoNovedadNomina,
    TipoObligacion,
)
from src.models.inventario import (
    Almacen,
    CapaConsumo,
    CapaKardex,
    CategoriaInsumo,
    Insumo,
    MovimientoKardex,
    StockActual,
)
from src.models.nomina import (
    Jornalero,
    Labor,
    Liquidacion,
    NovedadNomina,
)
from src.models.tenancy import Tenant, Usuario

__all__ = [
    # Tenancy
    "Tenant",
    "Usuario",
    # Auditoría
    "AuditLog",
    "IdempotencyKey",
    # Costos
    "Finca",
    "Lote",
    "Cultivo",
    "CicloProductivo",
    "Actividad",
    "CostoActividad",
    "CostoSnapshot",
    # Inventario
    "CategoriaInsumo",
    "Almacen",
    "Insumo",
    "StockActual",
    "MovimientoKardex",
    "CapaKardex",
    "CapaConsumo",
    # Nómina
    "Jornalero",
    "Labor",
    "Liquidacion",
    "NovedadNomina",
    # Enums
    "RolUsuario",
    "EstadoTenant",
    "EstadoCiclo",
    "TipoCosto",
    "MetodoProrrateo",
    "TipoMovimientoKardex",
    "MetodoValoracion",
    "EstadoInsumo",
    "TipoJornalero",
    "EstadoLabor",
    "EstadoLiquidacion",
    "TipoNovedadNomina",
    "FuenteClima",
    "CondicionClimatica",
    "TipoCuentaBancaria",
    "TipoMovimientoTesoreria",
    "EstadoObligacion",
    "TipoObligacion",
    "AccionAuditoria",
]
