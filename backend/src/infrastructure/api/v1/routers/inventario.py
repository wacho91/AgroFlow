"""Router del contexto de inventario / kardex."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.inventario import (
    AlmacenService,
    CategoriaInsumoService,
    InsumoService,
    MovimientoKardexService,
)
from src.database import get_db
from src.schemas.common import PaginatedResponse, PaginationParams
from src.schemas.inventario import (
    AlmacenCreate,
    AlmacenRead,
    CategoriaInsumoCreate,
    CategoriaInsumoRead,
    InsumoCreate,
    InsumoRead,
    InsumoUpdate,
    MovimientoKardexCreate,
    MovimientoKardexRead,
)

router = APIRouter()


def _pages(total: int, size: int) -> int:
    return (total + size - 1) // size


@router.get(
    "/categorias", response_model=PaginatedResponse[CategoriaInsumoRead]
)
async def list_categorias(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CategoriaInsumoRead]:
    service = CategoriaInsumoService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    return PaginatedResponse[CategoriaInsumoRead](
        items=[CategoriaInsumoRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/categorias",
    response_model=CategoriaInsumoRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_categoria(
    payload: CategoriaInsumoCreate, db: AsyncSession = Depends(get_db)
) -> CategoriaInsumoRead:
    service = CategoriaInsumoService(db)
    obj = await service.create(payload.model_dump())
    return CategoriaInsumoRead.model_validate(obj)


@router.get("/almacenes", response_model=PaginatedResponse[AlmacenRead])
async def list_almacenes(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[AlmacenRead]:
    service = AlmacenService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    return PaginatedResponse[AlmacenRead](
        items=[AlmacenRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/almacenes",
    response_model=AlmacenRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_almacen(
    payload: AlmacenCreate, db: AsyncSession = Depends(get_db)
) -> AlmacenRead:
    service = AlmacenService(db)
    obj = await service.create(payload.model_dump())
    return AlmacenRead.model_validate(obj)


@router.get("/insumos", response_model=PaginatedResponse[InsumoRead])
async def list_insumos(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[InsumoRead]:
    service = InsumoService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    return PaginatedResponse[InsumoRead](
        items=[InsumoRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/insumos", response_model=InsumoRead, status_code=status.HTTP_201_CREATED
)
async def create_insumo(
    payload: InsumoCreate, db: AsyncSession = Depends(get_db)
) -> InsumoRead:
    service = InsumoService(db)
    obj = await service.create(payload.model_dump())
    return InsumoRead.model_validate(obj)


@router.patch("/insumos/{insumo_id}", response_model=InsumoRead)
async def update_insumo(
    insumo_id: uuid.UUID,
    payload: InsumoUpdate,
    db: AsyncSession = Depends(get_db),
) -> InsumoRead:
    service = InsumoService(db)
    obj = await service.get(insumo_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return InsumoRead.model_validate(obj)


@router.get(
    "/movimientos", response_model=PaginatedResponse[MovimientoKardexRead]
)
async def list_movimientos(
    tenant_id: uuid.UUID,
    insumo_id: uuid.UUID | None = None,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[MovimientoKardexRead]:
    service = MovimientoKardexService(db)
    filters = {"tenant_id": tenant_id}
    if insumo_id:
        filters["insumo_id"] = insumo_id
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit, filters=filters
    )
    return PaginatedResponse[MovimientoKardexRead](
        items=[MovimientoKardexRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=_pages(total, pagination.size),
    )


@router.post(
    "/movimientos",
    response_model=MovimientoKardexRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_movimiento(
    payload: MovimientoKardexCreate, db: AsyncSession = Depends(get_db)
) -> MovimientoKardexRead:
    service = MovimientoKardexService(db)
    obj = await service.create(payload.model_dump())
    return MovimientoKardexRead.model_validate(obj)
