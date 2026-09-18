"""Servicios de tenancy."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.base import BaseService
from src.models.tenancy import Tenant, Usuario


class TenantService(BaseService[Tenant]):
    model = Tenant

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_slug(self, slug: str) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.slug == slug)
        return (await self.session.execute(stmt)).scalar_one_or_none()


class UsuarioService(BaseService[Usuario]):
    model = Usuario

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_email(
        self, tenant_id: uuid.UUID, email: str
    ) -> Usuario | None:
        stmt = select(Usuario).where(
            Usuario.tenant_id == tenant_id, Usuario.email == email
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()
