"""Demand domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Lead(BaseModel):
    """Lead entity."""

    lead_id: UUID
    property_id: UUID
    prospect_id: str | None = None
    lead_created_date: datetime.date | None = None
    lead_source_id: UUID | None = None
    agent_id: UUID | None = None
    unit_type_interest: str | None = None
    status: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    source_ingestion_id: UUID | None = None
    created_at: datetime.datetime


class LeadSource(BaseModel):
    """LeadSource entity."""

    source_id: UUID
    property_id: UUID
    source_name: str
    source_category: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class LeadEvent(BaseModel):
    """LeadEvent entity."""

    event_id: UUID
    lead_id: UUID
    event_type: str
    event_date: datetime.date
    agent_id: UUID | None = None
    response_time_min: int | None = None
    outcome: str | None = None
    reason_lost: str | None = None
    notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CommunicationEvent(BaseModel):
    """CommunicationEvent entity."""

    event_id: UUID
    lead_id: UUID | None = None
    resident_id: UUID | None = None
    property_id: UUID
    channel: str
    direction: str
    event_date: datetime.datetime
    notes: str | None = None
    created_at: datetime.datetime


class TourEvent(BaseModel):
    """TourEvent entity."""

    event_id: UUID
    lead_id: UUID
    property_id: UUID
    agent_id: UUID | None = None
    tour_date: datetime.date
    tour_type: str | None = None
    outcome: str | None = None
    duration_minutes: int | None = None
    units_shown: dict[str, Any] | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ApplicationEvent(BaseModel):
    """ApplicationEvent entity."""

    event_id: UUID
    lead_id: UUID | None = None
    property_id: UUID
    unit_id: UUID | None = None
    application_date: datetime.date
    status: str
    screening_score: str | None = None
    decision_date: datetime.date | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class Agent(BaseModel):
    """Agent entity."""

    agent_id: UUID
    property_id: UUID
    agent_name: str
    agent_type: str | None = None
    is_active: bool = True
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CrmAssignmentInterval(BaseModel):
    """CrmAssignmentInterval entity."""

    interval_id: UUID
    lead_id: UUID
    agent_id: UUID
    assigned_from: datetime.date
    assigned_to: datetime.date | None = None
    created_at: datetime.datetime


class ConversionMetricSnapshot(BaseModel):
    """ConversionMetricSnapshot entity."""

    snapshot_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    period_label: str
    total_leads: int | None = None
    total_tours: int | None = None
    total_no_shows: int | None = None
    total_applications: int | None = None
    total_leases: int | None = None
    avg_days_lead_tour: Decimal | None = None
    avg_days_tour_app: Decimal | None = None
    avg_days_app_lease: Decimal | None = None
    created_at: datetime.datetime
