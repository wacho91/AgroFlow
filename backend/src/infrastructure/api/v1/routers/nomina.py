"""Router del contexto de nómina."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.nomina import (
    JornaleroService,
    LaborService,
    LiquidacionService,
    NovedadNominaService,
)
from src.database import get_db
from src.schemas.common import PaginatedResponse, PaginationParams
from src.schemas.nomina import (
    JornaleroCreate,
    JornaleroRead,
    JornaleroUpdate,
    LaborCreate,
    LaborRead,
    LaborUpdate,
    LiquidacionCreate,
    LiquidacionRead,
    NovedadNominaCreate,
    NovedadNominaRead,
)

router = APIRouter()


def _pages(total: int, size: int) -> int:
    return (total + size - 1) // size


@router.get("/jornaleros", response_model=PaginatedResponse[JornaleroRead])
async def list_jornaleros(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[JornaleroRead]:
    service = JornaleroService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    return PaginatedResponse[JornaleroRead](
        items=[JornaleroRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/jornaleros",
    response_model=JornaleroRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_jornalero(
    payload: JornaleroCreate, db: AsyncSession = Depends(get_db)
) -> JornaleroRead:
    service = JornaleroService(db)
    obj = await service.create(payload.model_dump())
    return JornaleroRead.model_validate(obj)


@router.patch("/jornaleros/{jornalero_id}", response_model=JornaleroRead)
async def update_jornalero(
    jornalero_id: uuid.UUID,
    payload: JornaleroUpdate,
    db: AsyncSession = Depends(get_db),
) -> JornaleroRead:
    service = JornaleroService(db)
    obj = await service.get(jornalero_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Jornalero no encontrado")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return JornaleroRead.model_validate(obj)


@router.get("/labores", response_model=PaginatedResponse[LaborRead])
async def list_labores(
    tenant_id: uuid.UUID,
    jornalero_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[LaborRead]:
    service = LaborService(db)
    filters = {"tenant_id": tenant_id}
    if jornalero_id:
        filters["jornalero_id"] = jornalero_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    return PaginatedResponse[LaborRead](
        items=[LaborRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/labores", response_model=LaborRead, status_code=status.HTTP_201_CREATED
)
async def create_labor(
    payload: LaborCreate, db: AsyncSession = Depends(get_db)
) -> LaborRead:
    service = LaborService(db)
    obj = await service.create(payload.model_dump())
    return LaborRead.model_validate(obj)


@router.patch("/labores/{labor_id}", response_model=LaborRead)
async def update_labor(
    labor_id: uuid.UUID,
    payload: LaborUpdate,
    db: AsyncSession = Depends(get_db),
) -> LaborRead:
    service = LaborService(db)
    obj = await service.get(labor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Labor no encontrada")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return LaborRead.model_validate(obj)


@router.get(
    "/liquidaciones", response_model=PaginatedResponse[LiquidacionRead]
)
async def list_liquidaciones(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[LiquidacionRead]:
    service = LiquidacionService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    return PaginatedResponse[LiquidacionRead](
        items=[LiquidacionRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/liquidaciones",
    response_model=LiquidacionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_liquidacion(
    payload: LiquidacionCreate, db: AsyncSession = Depends(get_db)
) -> LiquidacionRead:
    service = LiquidacionService(db)
    obj = await service.create(payload.model_dump())
    return LiquidacionRead.model_validate(obj)


@router.get(
    "/novedades", response_model=PaginatedResponse[NovedadNominaRead]
)
async def list_novedades(
    tenant_id: uuid.UUID,
    jornalero_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[NovedadNominaRead]:
    service = NovedadNominaService(db)
    filters = {"tenant_id": tenant_id}
    if jornalero_id:
        filters["jornalero_id"] = jornalero_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    return PaginatedResponse[NovedadNominaRead](
        items=[NovedadNominaRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/novedades",
    response_model=NovedadNominaRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_novedad(
    payload: NovedadNominaCreate, db: AsyncSession = Depends(get_db)
) -> NovedadNominaRead:
    service = NovedadNominaService(db)
    obj = await service.create(payload.model_dump())
    return NovedadNominaRead.model_validate(obj)
