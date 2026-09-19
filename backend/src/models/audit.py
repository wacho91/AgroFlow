"""Modelos de auditoría e idempotencia."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum as SAEnum, Integer,
    String, Text, UniqueConstraint, func, JSON  # <--- JSON y String añadidos aquí
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .enums import AccionAuditoria
from .mixins import UUIDPKMixin

class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    usuario_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    accion: Mapped[AccionAuditoria] = mapped_column(SAEnum(AccionAuditoria, name="accion_auditoria", native_enum=True), nullable=False)
    tabla: Mapped[str] = mapped_column(String(100), nullable=False)
    registro_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    datos_anteriores: Mapped[dict[str, Any] | None] = mapped_column(JSON) # <--- Cambiado a JSON
    datos_nuevos: Mapped[dict[str, Any] | None] = mapped_column(JSON)     # <--- Cambiado a JSON
    ip_origen: Mapped[str | None] = mapped_column(String(50))             # <--- Cambiado INET a String
    user_agent: Mapped[str | None] = mapped_column(Text)
    request_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    exitoso: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mensaje_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class IdempotencyKey(UUIDPKMixin, Base):
    __tablename__ = "idempotency_keys"
    __table_args__ = (UniqueConstraint("tenant_id", "idempotency_key", "endpoint", name="uq_idempotency"),)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    response_status: Mapped[int | None] = mapped_column(Integer)
    response_body: Mapped[dict[str, Any] | None] = mapped_column(JSON) # <--- Cambiado a JSON
    expira_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)