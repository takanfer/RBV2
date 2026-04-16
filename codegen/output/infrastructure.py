"""Infrastructure domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """Tenant entity."""

    tenant_id: UUID
    org_name: str
    slug: str
    settings: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserAccount(BaseModel):
    """UserAccount entity."""

    user_id: UUID
    tenant_id: UUID
    email: str
    display_name: str
    role: str
    auth_provider_id: str | None = None
    is_active: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AuditLog(BaseModel):
    """AuditLog entity."""

    log_id: UUID
    tenant_id: UUID
    user_id: UUID | None = None
    action: str
    entity_type: str
    entity_id: UUID
    before_value: dict[str, Any] | None = None
    after_value: dict[str, Any] | None = None
    reason: str | None = None
    created_at: datetime.datetime


class Client(BaseModel):
    """Client entity."""

    client_id: UUID
    tenant_id: UUID
    client_name: str
    contact_name: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Portfolio(BaseModel):
    """Portfolio entity."""

    portfolio_id: UUID
    client_id: UUID
    portfolio_name: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
