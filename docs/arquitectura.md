# AgroFlow — Documento de Arquitectura

> **Versión:** 1.0.0
> **Estado:** Aprobado para implementación
> **Autor:** Arquitecto de Software Senior
> **Clasificación:** Interno — Confidencial

---

## 1. Visión General

**AgroFlow** es una plataforma SaaS B2B AgroTech de nivel Enterprise orientada a la gestión integral de fincas agrícolas. Su propuesta de valor se apoya en cinco dominios funcionales:

1. **Costos de Producción en Tiempo Real** — cálculo por lote, ciclo, cultivo y actividad.
2. **Inventario de Insumos (Kardex)** — trazabilidad completa de entradas/salidas con valoración PEPS.
3. **Nómina de Jornaleros** — digitalización de labores, jornales, prestaciones y liquidaciones.
4. **Integración Climática** — ingesta de datos meteorológicos para correlación con rendimiento.
5. **Tesorería** — flujo de caja, cuentas por pagar/cobrar y conciliación.

El sistema se diseña bajo **Arquitectura Hexagonal (Ports & Adapters)** con principios de **Clean Architecture**, garantizando:

- Independencia del framework (FastAPI es un detalle de infraestructura).
- Independencia de la base de datos (PostgreSQL/Supabase es un detalle).
- Independencia de la UI (React es un detalle).
- Testabilidad plena del dominio sin dependencias externas.
- Aislamiento por **Bounded Contexts** (modularidad por dominio).

---

## 2. Principios Rectores

| Principio | Aplicación en AgroFlow |
|---|---|
| **Separación de Responsabilidades (SoC)** | Cada capa tiene una única razón de cambio. El dominio no conoce FastAPI, SQLAlchemy ni React. |
| **Inversión de Dependencias (DIP)** | El dominio define puertos (interfaces); la infraestructura los implementa. |
| **Regla de Dependencia** | Las dependencias apuntan siempre hacia adentro: `infrastructure → application → domain`. |
| **Modularidad por Bounded Context** | Cada contexto (Costos, Inventario, Nómina, Clima, Tesorería) es un módulo autocontenido. |
| **Zero Trust Security** | Ninguna petición es confiable por defecto. Verificación continua, mínimo privilegio, cifrado en tránsito y reposo. |
| **Multi-Tenancy** | Aislamiento por `tenant_id` a nivel de fila (RLS en Supabase) + filtro obligatorio en repositorios. |
| **Idempotencia** | Operaciones críticas (Kardex, Tesorería) usan claves de idempotencia. |
| **Observabilidad** | Logs estructurados, trazas distribuidas y métricas por caso de uso. |

---

## 3. Estructura de Carpetas Exacta
