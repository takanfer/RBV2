"""Competitive domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class CompetitiveSet(BaseModel):
    """CompetitiveSet entity."""

    comp_set_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    set_name: str
    valid_from: datetime.date | None = None
    valid_to: datetime.date | None = None
    created_at: datetime.datetime


class CompetitiveSetMember(BaseModel):
    """CompetitiveSetMember entity."""

    member_id: UUID
    comp_set_id: UUID
    competitor_property_id: UUID
    distance_miles: Decimal | None = None
    created_at: datetime.datetime


class CompFloorplan(BaseModel):
    """CompFloorplan entity."""

    comp_floorplan_id: UUID
    competitor_property_id: UUID
    unit_type: str | None = None
    bedrooms: Decimal | None = None
    bathrooms: Decimal | None = None
    sqft: int | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CompListingObservation(BaseModel):
    """CompListingObservation entity."""

    observation_id: UUID
    competitor_property_id: UUID
    comp_floorplan_id: UUID | None = None
    assessment_id: UUID | None = None
    observation_date: datetime.date
    bedrooms: Decimal | None = None
    bathrooms: Decimal | None = None
    unit_type: str | None = None
    sqft: int | None = None
    asking_rent: Decimal | None = None
    rent_per_sqft: Decimal | None = None
    floor: str | None = None
    is_available: bool | None = None
    private_outdoor: bool | None = None
    concession_amount: Decimal | None = None
    days_listed: int | None = None
    confidence_score: Decimal | None = None
    notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CompPropertyObservation(BaseModel):
    """CompPropertyObservation entity."""

    observation_id: UUID
    competitor_property_id: UUID
    assessment_id: UUID | None = None
    observation_date: datetime.date
    occupancy_rate_pct: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CompMarketingAssessment(BaseModel):
    """CompMarketingAssessment entity."""

    assessment_score_id: UUID
    competitor_property_id: UUID
    assessment_id: UUID | None = None
    platform_coverage: Decimal | None = None
    photo_quality: Decimal | None = None
    content_quality: Decimal | None = None
    listing_accuracy: Decimal | None = None
    website_quality: Decimal | None = None
    social_marketing: Decimal | None = None
    partnership_referral: Decimal | None = None
    created_at: datetime.datetime
