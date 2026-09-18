"""Servicios del contexto de costos."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.base import BaseService
from src.models.costos import (
    Actividad,
    CicloProductivo,
    CostoActividad,
    Cultivo,
    Finca,
    Lote,
)


class FincaService(BaseService[Finca]):
    model = Finca

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_codigo(
        self, tenant_id: uuid.UUID, codigo: str
    ) -> Finca | None:
        stmt = select(Finca).where(
            Finca.tenant_id == tenant_id, Finca.codigo == codigo
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()


class LoteService(BaseService[Lote]):
    model = Lote

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def list_by_finca(
        self, finca_id: uuid.UUID, *, offset: int = 0, limit: int = 20
    ) -> tuple[list[Lote], int]:
        return await self.list(
            offset=offset, limit=limit, filters={"finca_id": finca_id}
        )


class CultivoService(BaseService[Cultivo]):
    model = Cultivo

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class CicloProductivoService(BaseService[CicloProductivo]):
    model = CicloProductivo

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def list_by_lote(
        self, lote_id: uuid.UUID, *, offset: int = 0, limit: int = 20
    ) -> tuple[list[CicloProductivo], int]:
        return await self.list(
            offset=offset, limit=limit, filters={"lote_id": lote_id}
        )


class ActividadService(BaseService[Actividad]):
    model = Actividad

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)


class CostoActividadService(BaseService[CostoActividad]):
    model = CostoActividad

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def list_by_ciclo(
        self, ciclo_id: uuid.UUID, *, offset: int = 0, limit: int = 20
    ) -> tuple[list[CostoActividad], int]:
        return await self.list(
            offset=offset, limit=limit, filters={"ciclo_id": ciclo_id}
        )
