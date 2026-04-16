"""Clickhouse Facts domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class FactUnitDay(BaseModel):
    """FactUnitDay entity."""

    property_id: UUID
    unit_id: UUID
    day_date: datetime.date
    unit_version_id: UUID
    existence_status: str
    rentable_flag: int
    occupancy_state: str
    readiness_state: str
    marketing_state: str
    active_lease_id: UUID | None = None
    active_listing_id: UUID | None = None
    days_vacant: int | None = None
    asking_rent: Decimal | None = None
    effective_rent: Decimal | None = None
    concession_value: Decimal | None = None
    condition_score: Decimal | None = None
    contradiction_flags: str
    evidence_coverage: str


class FactLeaseInterval(BaseModel):
    """FactLeaseInterval entity."""

    property_id: UUID
    unit_id: UUID
    lease_id: UUID
    interval_start: datetime.date
    interval_end: datetime.date | None = None
    monthly_rent: Decimal | None = None
    effective_rent: Decimal | None = None
    concession_value: Decimal | None = None
    lease_type: str
    resident_id: UUID | None = None
    bedrooms: Decimal | None = None
    sqft: int | None = None


class FactVacancyCycle(BaseModel):
    """FactVacancyCycle entity."""

    property_id: UUID
    unit_id: UUID
    cycle_id: UUID
    vacancy_start: datetime.date
    vacancy_end: datetime.date | None = None
    days_vacant: int | None = None
    prior_rent: Decimal | None = None
    new_rent: Decimal | None = None
    vacancy_cost: Decimal | None = None
    make_ready_days: int | None = None
    make_ready_cost: Decimal | None = None


class FactWorkOrder(BaseModel):
    """FactWorkOrder entity."""

    property_id: UUID
    unit_id: UUID | None = None
    work_order_id: UUID
    category: str
    is_make_ready: int
    date_created: datetime.date
    date_completed: datetime.date | None = None
    days_to_complete: int | None = None
    cost: Decimal | None = None
    vendor_id: UUID | None = None


class FactLeadFunnelEvent(BaseModel):
    """FactLeadFunnelEvent entity."""

    property_id: UUID
    lead_id: UUID
    event_type: str
    event_date: datetime.date
    agent_id: UUID | None = None
    lead_source: str | None = None
    response_time_min: int | None = None
    outcome: str | None = None


class FactListingObservation(BaseModel):
    """FactListingObservation entity."""

    property_id: UUID
    unit_id: UUID | None = None
    observation_id: UUID
    platform: str
    observation_date: datetime.date
    asking_rent: Decimal | None = None
    photo_quality: Decimal | None = None
    description_quality: Decimal | None = None
    days_on_market: int | None = None


class FactMarketingPresenceDay(BaseModel):
    """FactMarketingPresenceDay entity."""

    property_id: UUID
    channel_id: UUID
    day_date: datetime.date
    is_active: int
    platform: str
    spend_daily: Decimal | None = None


class FactCompListingObservation(BaseModel):
    """FactCompListingObservation entity."""

    competitor_property_id: UUID
    observation_id: UUID
    observation_date: datetime.date
    bedrooms: Decimal | None = None
    sqft: int | None = None
    asking_rent: Decimal | None = None
    rent_per_sqft: Decimal | None = None
    is_available: int | None = None
    concession_amount: Decimal | None = None


class FactScoreResult(BaseModel):
    """FactScoreResult entity."""

    assessment_id: UUID
    property_id: UUID
    scorecard_id: UUID
    scoring_level: str
    area_number: int | None = None
    area_name: str | None = None
    item_name: str | None = None
    normalized_score: Decimal | None = None
    weighted_score: Decimal | None = None
    confidence_score: Decimal | None = None
    grade_letter: str | None = None
    version: str


class FactFindingImpact(BaseModel):
    """FactFindingImpact entity."""

    assessment_id: UUID
    property_id: UUID
    finding_id: UUID
    finding_type: str
    domain: str
    severity: str
    impact_model: str | None = None
    base_estimate: Decimal | None = None
    annualized_amount: Decimal | None = None
    confidence: Decimal | None = None


class FactAssessmentScore(BaseModel):
    """FactAssessmentScore entity."""

    property_id: UUID
    assessment_id: UUID
    assessment_date: datetime.date
    area_number: int | None = None
    area_name: str | None = None
    overall_score: Decimal | None = None
    grade_letter: str | None = None
    version: str


class FactAssessmentFinding(BaseModel):
    """FactAssessmentFinding entity."""

    property_id: UUID
    assessment_id: UUID
    assessment_date: datetime.date
    finding_id: UUID
    domain: str
    severity: str
    is_recurring: int
    prior_finding_id: UUID | None = None


class FactRecommendationStatus(BaseModel):
    """FactRecommendationStatus entity."""

    property_id: UUID
    assessment_id: UUID
    recommendation_id: UUID
    domain: str
    priority: str
    status: str
    status_date: datetime.date


class FactPropertyKpiPeriod(BaseModel):
    """FactPropertyKpiPeriod entity."""

    property_id: UUID
    period_start: datetime.date
    period_end: datetime.date
    kpi_name: str
    kpi_value: Decimal | None = None
    kpi_unit: str


class FactUnitChronicity(BaseModel):
    """FactUnitChronicity entity."""

    property_id: UUID
    unit_id: UUID
    assessment_id: UUID
    chronic_type: str
    duration_days: int | None = None
    cycle_count: int | None = None
    total_cost: Decimal | None = None
