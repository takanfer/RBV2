"""Lease domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Resident(BaseModel):
    """Resident entity."""

    resident_id: UUID
    property_id: UUID
    resident_name: str | None = None
    household_id: UUID | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    source_system_id: UUID | None = None
    source_key: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class Lease(BaseModel):
    """Lease entity."""

    lease_id: UUID
    property_id: UUID
    unit_id: UUID
    resident_id: UUID | None = None
    lease_type: str | None = None
    lease_start: datetime.date
    lease_end: datetime.date | None = None
    lease_term_months: int | None = None
    execution_date: datetime.date | None = None
    monthly_rent: Decimal | None = None
    market_rent: Decimal | None = None
    security_deposit: Decimal | None = None
    concession_type: str | None = None
    concession_monthly: Decimal | None = None
    concession_start: datetime.date | None = None
    concession_end: datetime.date | None = None
    leasing_agent: str | None = None
    move_in_date: datetime.date | None = None
    notice_date: datetime.date | None = None
    expected_move_out: datetime.date | None = None
    actual_move_out: datetime.date | None = None
    move_out_reason: str | None = None
    occupancy_status: str | None = None
    source_ingestion_id: UUID | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    recorded_from: datetime.datetime
    recorded_to: datetime.datetime | None = None
    created_at: datetime.datetime


class LeaseInterval(BaseModel):
    """LeaseInterval entity."""

    interval_id: UUID
    lease_id: UUID
    unit_id: UUID
    valid_from: datetime.date
    valid_to: datetime.date | None = None
    monthly_rent: Decimal | None = None
    effective_rent: Decimal | None = None
    concession_value: Decimal | None = None
    interval_status: str
    recorded_from: datetime.datetime
    recorded_to: datetime.datetime | None = None


class LeaseCharge(BaseModel):
    """LeaseCharge entity."""

    charge_id: UUID
    lease_id: UUID
    unit_id: UUID
    charge_code: str
    charge_description: str | None = None
    monthly_amount: Decimal
    effective_from: datetime.date | None = None
    effective_to: datetime.date | None = None
    created_at: datetime.datetime


class LeaseEvent(BaseModel):
    """LeaseEvent entity."""

    event_id: UUID
    lease_id: UUID
    event_type: str
    event_date: datetime.date
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class NoticeEvent(BaseModel):
    """NoticeEvent entity."""

    event_id: UUID
    lease_id: UUID
    unit_id: UUID
    notice_date: datetime.date
    expected_move_out: datetime.date | None = None
    notice_type: str | None = None
    reason: str | None = None
    created_at: datetime.datetime


class MoveEvent(BaseModel):
    """MoveEvent entity."""

    event_id: UUID
    lease_id: UUID | None = None
    unit_id: UUID
    resident_id: UUID | None = None
    event_type: str
    event_date: datetime.date
    rent_amount: Decimal | None = None
    reason: str | None = None
    source_ingestion_id: UUID | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class RenewalOffer(BaseModel):
    """RenewalOffer entity."""

    offer_id: UUID
    lease_id: UUID
    unit_id: UUID
    resident_id: UUID | None = None
    offer_date: datetime.date
    current_rent: Decimal | None = None
    offered_rent: Decimal | None = None
    offered_term: str | None = None
    outcome: str | None = None
    accepted_date: datetime.date | None = None
    incentive_offered: str | None = None
    incentive_value: Decimal | None = None
    competitor_offer: Decimal | None = None
    resident_sentiment: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class PaymentEvent(BaseModel):
    """PaymentEvent entity."""

    event_id: UUID
    lease_id: UUID
    unit_id: UUID
    payment_date: datetime.date
    amount: Decimal
    payment_type: str
    payment_method: str | None = None
    created_at: datetime.datetime


class DelinquencySnapshot(BaseModel):
    """DelinquencySnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    unit_id: UUID
    resident_id: UUID | None = None
    snapshot_date: datetime.date
    current_balance: Decimal | None = None
    bucket_0_30: Decimal | None = None
    bucket_31_60: Decimal | None = None
    bucket_61_90: Decimal | None = None
    bucket_90_plus: Decimal | None = None
    last_payment_date: datetime.date | None = None
    collections_status: str | None = None
    eviction_filed: bool | None = None
    created_at: datetime.datetime
