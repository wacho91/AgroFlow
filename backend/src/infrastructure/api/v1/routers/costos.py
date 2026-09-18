"""Router del contexto de costos."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.costos import (
    ActividadService,
    CicloProductivoService,
    CostoActividadService,
    CultivoService,
    FincaService,
    LoteService,
)
from src.database import get_db
from src.schemas.common import PaginatedResponse, PaginationParams
from src.schemas.costos import (
    ActividadCreate,
    ActividadRead,
    ActividadUpdate,
    CicloProductivoCreate,
    CicloProductivoRead,
    CicloProductivoUpdate,
    CostoActividadCreate,
    CostoActividadRead,
    CultivoCreate,
    CultivoRead,
    CultivoUpdate,
    FincaCreate,
    FincaRead,
    FincaUpdate,
    LoteCreate,
    LoteRead,
    LoteUpdate,
)

router = APIRouter()


def _paginate(items, total, pagination):
    pages = (total + pagination.size - 1) // pagination.size
    return total, pages


# ---------- Fincas ----------
@router.get("/fincas", response_model=PaginatedResponse[FincaRead])
async def list_fincas(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[FincaRead]:
    service = FincaService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[FincaRead](
        items=[FincaRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/fincas", response_model=FincaRead, status_code=status.HTTP_201_CREATED
)
async def create_finca(
    payload: FincaCreate, db: AsyncSession = Depends(get_db)
) -> FincaRead:
    service = FincaService(db)
    obj = await service.create(payload.model_dump())
    return FincaRead.model_validate(obj)


@router.patch("/fincas/{finca_id}", response_model=FincaRead)
async def update_finca(
    finca_id: uuid.UUID,
    payload: FincaUpdate,
    db: AsyncSession = Depends(get_db),
) -> FincaRead:
    service = FincaService(db)
    obj = await service.get(finca_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return FincaRead.model_validate(obj)


# ---------- Lotes ----------
@router.get("/lotes", response_model=PaginatedResponse[LoteRead])
async def list_lotes(
    tenant_id: uuid.UUID,
    finca_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[LoteRead]:
    service = LoteService(db)
    filters = {"tenant_id": tenant_id}
    if finca_id:
        filters["finca_id"] = finca_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[LoteRead](
        items=[LoteRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/lotes", response_model=LoteRead, status_code=status.HTTP_201_CREATED
)
async def create_lote(
    payload: LoteCreate, db: AsyncSession = Depends(get_db)
) -> LoteRead:
    service = LoteService(db)
    obj = await service.create(payload.model_dump())
    return LoteRead.model_validate(obj)


# ---------- Cultivos ----------
@router.get("/cultivos", response_model=PaginatedResponse[CultivoRead])
async def list_cultivos(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CultivoRead]:
    service = CultivoService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[CultivoRead](
        items=[CultivoRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/cultivos",
    response_model=CultivoRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_cultivo(
    payload: CultivoCreate, db: AsyncSession = Depends(get_db)
) -> CultivoRead:
    service = CultivoService(db)
    obj = await service.create(payload.model_dump())
    return CultivoRead.model_validate(obj)


# ---------- Ciclos ----------
@router.get(
    "/ciclos", response_model=PaginatedResponse[CicloProductivoRead]
)
async def list_ciclos(
    tenant_id: uuid.UUID,
    lote_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CicloProductivoRead]:
    service = CicloProductivoService(db)
    filters = {"tenant_id": tenant_id}
    if lote_id:
        filters["lote_id"] = lote_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[CicloProductivoRead](
        items=[CicloProductivoRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/ciclos",
    response_model=CicloProductivoRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_ciclo(
    payload: CicloProductivoCreate, db: AsyncSession = Depends(get_db)
) -> CicloProductivoRead:
    service = CicloProductivoService(db)
    obj = await service.create(payload.model_dump())
    return CicloProductivoRead.model_validate(obj)


@router.patch("/ciclos/{ciclo_id}", response_model=CicloProductivoRead)
async def update_ciclo(
    ciclo_id: uuid.UUID,
    payload: CicloProductivoUpdate,
    db: AsyncSession = Depends(get_db),
) -> CicloProductivoRead:
    service = CicloProductivoService(db)
    obj = await service.get(ciclo_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return CicloProductivoRead.model_validate(obj)


# ---------- Actividades ----------
@router.get("/actividades", response_model=PaginatedResponse[ActividadRead])
async def list_actividades(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ActividadRead]:
    service = ActividadService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[ActividadRead](
        items=[ActividadRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/actividades",
    response_model=ActividadRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_actividad(
    payload: ActividadCreate, db: AsyncSession = Depends(get_db)
) -> ActividadRead:
    service = ActividadService(db)
    obj = await service.create(payload.model_dump())
    return ActividadRead.model_validate(obj)


# ---------- Costos de actividad ----------
@router.get(
    "/costos-actividad",
    response_model=PaginatedResponse[CostoActividadRead],
)
async def list_costos_actividad(
    tenant_id: uuid.UUID,
    ciclo_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CostoActividadRead]:
    service = CostoActividadService(db)
    filters = {"tenant_id": tenant_id}
    if ciclo_id:
        filters["ciclo_id"] = ciclo_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    _, pages = _paginate(items, total, pagination)
    return PaginatedResponse[CostoActividadRead](
        items=[CostoActividadRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/costos-actividad",
    response_model=CostoActividadRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_costo_actividad(
    payload: CostoActividadCreate, db: AsyncSession = Depends(get_db)
) -> CostoActividadRead:
    service = CostoActividadService(db)
    obj = await service.create(payload.model_dump())
    return CostoActividadRead.model_validate(obj)
