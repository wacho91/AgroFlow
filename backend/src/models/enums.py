"""Enums nativos PostgreSQL alineados al schema.sql."""
from __future__ import annotations

import enum


class RolUsuario(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    AGRONOMO = "agronomo"
    CONTADOR = "contador"
    OPERARIO = "operario"
    AUDITOR = "auditor"


class EstadoTenant(str, enum.Enum):
    ACTIVO = "activo"
    SUSPENDIDO = "suspendido"
    CANCELADO = "cancelado"
    TRIAL = "trial"


class EstadoCiclo(str, enum.Enum):
    PLANIFICADO = "planificado"
    EN_CURSO = "en_curso"
    CERRADO = "cerrado"
    CANCELADO = "cancelado"


class TipoCosto(str, enum.Enum):
    MANO_OBRA = "mano_obra"
    INSUMOS = "insumos"
    MAQUINARIA = "maquinaria"
    SERVICIOS = "servicios"
    ARRENDAMIENTO = "arrendamiento"
    ADMINISTRATIVO = "administrativo"
    FINANCIERO = "financiero"
    OTROS = "otros"


class MetodoProrrateo(str, enum.Enum):
    HECTAREA = "hectarea"
    HORA_MAQUINA = "hora_maquina"
    UNIDAD_PRODUCIDA = "unidad_producida"
    DIRECTO = "directo"


class TipoMovimientoKardex(str, enum.Enum):
    ENTRADA_COMPRA = "entrada_compra"
    ENTRADA_DEVOLUCION = "entrada_devolucion"
    ENTRADA_AJUSTE = "entrada_ajuste"
    SALIDA_CONSUMO = "salida_consumo"
    SALIDA_VENTA = "salida_venta"
    SALIDA_MERMA = "salida_merma"
    SALIDA_AJUSTE = "salida_ajuste"
    TRANSFERENCIA_ENTRADA = "transferencia_entrada"
    TRANSFERENCIA_SALIDA = "transferencia_salida"


class MetodoValoracion(str, enum.Enum):
    PEPS = "peps"
    PROMEDIO_PONDERADO = "promedio_ponderado"
    UEPS = "ueps"
    COSTO_ESTANDAR = "costo_estandar"


class EstadoInsumo(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    DESCONTINUADO = "descontinuado"


class TipoJornalero(str, enum.Enum):
    JORNALERO = "jornalero"
    FIJO = "fijo"
    TEMPORAL = "temporal"
    CONTRATISTA = "contratista"


class EstadoLabor(str, enum.Enum):
    REGISTRADA = "registrada"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    PAGADA = "pagada"


class EstadoLiquidacion(str, enum.Enum):
    BORRADOR = "borrador"
    CALCULADA = "calculada"
    APROBADA = "aprobada"
    PAGADA = "pagada"
    ANULADA = "anulada"


class TipoNovedadNomina(str, enum.Enum):
    BONIFICACION = "bonificacion"
    DESCUENTO = "descuento"
    AUSENCIA = "ausencia"
    INCAPACIDAD = "incapacidad"
    HORAS_EXTRA = "horas_extra"
    ANTICIPO = "anticipo"
    PRESTAMO = "prestamo"
    OTRO = "otro"


class FuenteClima(str, enum.Enum):
    OPENWEATHER = "openweather"
    NOAA = "noaa"
    ESTACION_LOCAL = "estacion_local"
    MANUAL = "manual"
    SATELITE = "satelite"


class CondicionClimatica(str, enum.Enum):
    DESPEJADO = "despejado"
    NUBLADO = "nublado"
    LLUVIA_LIGERA = "lluvia_ligera"
    LLUVIA_MODERADA = "lluvia_moderada"
    LLUVIA_FUERTE = "lluvia_fuerte"
    TORMENTA = "tormenta"
    NIEBLA = "niebla"
    GRANIZO = "granizo"
    NIEVE = "nieve"
    OTRO = "otro"


class TipoCuentaBancaria(str, enum.Enum):
    CORRIENTE = "corriente"
    AHORROS = "ahorros"
    CAJA_MENOR = "caja_menor"
    INVERSION = "inversion"
    CREDITO = "credito"


class TipoMovimientoTesoreria(str, enum.Enum):
    INGRESO_COBRO = "ingreso_cobro"
    INGRESO_APORTE = "ingreso_aporte"
    INGRESO_OTRO = "ingreso_otro"
    EGRESO_PAGO = "egreso_pago"
    EGRESO_NOMINA = "egreso_nomina"
    EGRESO_INSUMO = "egreso_insumo"
    EGRESO_IMPUESTO = "egreso_impuesto"
    EGRESO_SERVICIO = "egreso_servicio"
    EGRESO_OTRO = "egreso_otro"
    TRANSFERENCIA_ENTRADA = "transferencia_entrada"
    TRANSFERENCIA_SALIDA = "transferencia_salida"
    AJUSTE_POSITIVO = "ajuste_positivo"
    AJUSTE_NEGATIVO = "ajuste_negativo"


class EstadoObligacion(str, enum.Enum):
    PENDIENTE = "pendiente"
    PARCIAL = "parcial"
    PAGADA = "pagada"
    VENCIDA = "vencida"
    ANULADA = "anulada"


class TipoObligacion(str, enum.Enum):
    CUENTA_POR_PAGAR = "cuenta_por_pagar"
    CUENTA_POR_COBRAR = "cuenta_por_cobrar"


class AccionAuditoria(str, enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    ACCESS_DENIED = "ACCESS_DENIED"
