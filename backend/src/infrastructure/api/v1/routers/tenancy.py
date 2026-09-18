"""Router de tenancy (tenants, usuarios)."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.tenancy import TenantService, UsuarioService
from src.database import get_db
from src.schemas.common import PaginatedResponse, PaginationParams
from src.schemas.tenancy import (
    TenantCreate,
    TenantRead,
    TenantUpdate,
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
)

router = APIRouter()


@router.get("/tenants", response_model=PaginatedResponse[TenantRead])
async def list_tenants(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[TenantRead]:
    service = TenantService(db)
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit
    )
    pages = (total + pagination.size - 1) // pagination.size
    return PaginatedResponse[TenantRead](
        items=[TenantRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/tenants",
    response_model=TenantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_tenant(
    payload: TenantCreate, db: AsyncSession = Depends(get_db)
) -> TenantRead:
    service = TenantService(db)
    obj = await service.create(payload.model_dump())
    return TenantRead.model_validate(obj)


@router.get("/tenants/{tenant_id}", response_model=TenantRead)
async def get_tenant(
    tenant_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> TenantRead:
    service = TenantService(db)
    obj = await service.get(tenant_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Tenant no encontrado")
    return TenantRead.model_validate(obj)


@router.patch("/tenants/{tenant_id}", response_model=TenantRead)
async def update_tenant(
    tenant_id: uuid.UUID,
    payload: TenantUpdate,
    db: AsyncSession = Depends(get_db),
) -> TenantRead:
    service = TenantService(db)
    obj = await service.get(tenant_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Tenant no encontrado")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return TenantRead.model_validate(obj)


@router.get("/usuarios", response_model=PaginatedResponse[UsuarioRead])
async def list_usuarios(
    tenant_id: uuid.UUID,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UsuarioRead]:
    service = UsuarioService(db)
    items, total = await service.list(
        offset=pagination.offset,
        limit=pagination.limit,
        filters={"tenant_id": tenant_id},
    )
    pages = (total + pagination.size - 1) // pagination.size
    return PaginatedResponse[UsuarioRead](
        items=[UsuarioRead.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post(
    "/usuarios",
    response_model=UsuarioRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_usuario(
    payload: UsuarioCreate, db: AsyncSession = Depends(get_db)
) -> UsuarioRead:
    service = UsuarioService(db)
    obj = await service.create(payload.model_dump())
    return UsuarioRead.model_validate(obj)


@router.patch("/usuarios/{usuario_id}", response_model=UsuarioRead)
async def update_usuario(
    usuario_id: uuid.UUID,
    payload: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
) -> UsuarioRead:
    service = UsuarioService(db)
    obj = await service.get(usuario_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    obj = await service.update(obj, payload.model_dump(exclude_unset=True))
    return UsuarioRead.model_validate(obj)
