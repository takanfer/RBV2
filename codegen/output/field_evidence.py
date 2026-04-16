"""Field Evidence domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MysteryShop(BaseModel):
    """MysteryShop entity."""

    shop_id: UUID
    property_id: UUID
    assessment_id: UUID
    shop_date: datetime.date
    agent_name: str | None = None
    is_subject: bool = True
    phone_friendly_greeting: bool | None = None
    phone_answered_timely: bool | None = None
    phone_enthusiasm: bool | None = None
    phone_described_community: bool | None = None
    phone_qualifying_questions: bool | None = None
    phone_offered_incentives: bool | None = None
    phone_matched_needs: bool | None = None
    phone_scheduled_tour: bool | None = None
    phone_collected_info: bool | None = None
    phone_impression: Decimal | None = None
    phone_response_time: Decimal | None = None
    phone_response_unit: str | None = None
    email_response_time: Decimal | None = None
    email_response_unit: str | None = None
    greeting_prompt: bool | None = None
    greeting_eye_contact: bool | None = None
    greeting_handshake: bool | None = None
    greeting_asked_name: bool | None = None
    greeting_rapport: bool | None = None
    greeting_refreshments: bool | None = None
    greeting_impression: Decimal | None = None
    needs_move_timeline: bool | None = None
    needs_floor_plan: bool | None = None
    needs_budget: bool | None = None
    needs_lifestyle: bool | None = None
    needs_most_important: bool | None = None
    needs_active_listening: bool | None = None
    needs_impression: Decimal | None = None
    wait_time_minutes: Decimal | None = None
    tour_duration_minutes: Decimal | None = None
    tour_showed_unit: bool | None = None
    tour_highlighted_features: bool | None = None
    tour_amenities: bool | None = None
    tour_tailored: bool | None = None
    tour_product_knowledge: bool | None = None
    tour_competitive_knowledge: bool | None = None
    tour_submarket_knowledge: bool | None = None
    tour_lease_terms: bool | None = None
    tour_curb_appeal: bool | None = None
    tour_fair_housing: bool | None = None
    presentation_impression: Decimal | None = None
    close_asked_lease: bool | None = None
    close_overcame_objections: bool | None = None
    close_next_steps: bool | None = None
    close_urgency: bool | None = None
    close_pricing_info: bool | None = None
    closing_impression: Decimal | None = None
    followup_received: bool | None = None
    followup_personalized: bool | None = None
    followup_referenced_visit: bool | None = None
    followup_close_attempt: bool | None = None
    followup_impression: Decimal | None = None
    followup_timing: str | None = None
    followup_method: str | None = None
    fair_housing_no_discrimination: bool | None = None
    fair_housing_consistent: bool | None = None
    fair_housing_accommodations: bool | None = None
    fair_housing_impression: Decimal | None = None
    condition_grounds: bool | None = None
    condition_office: bool | None = None
    condition_show_unit: bool | None = None
    condition_common_areas: bool | None = None
    condition_signage: bool | None = None
    condition_impression: Decimal | None = None
    overall_experience: Decimal | None = None
    strengths: str | None = None
    gaps: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class VacantUnitAudit(BaseModel):
    """VacantUnitAudit entity."""

    audit_id: UUID
    assessment_id: UUID
    unit_id: UUID
    property_id: UUID
    observation_date: datetime.date
    marketed: bool | None = None
    like_kind_listing_date: datetime.date | None = None
    marketed_date: datetime.date | None = None
    listing_platform: str | None = None
    listing_type: str | None = None
    representative_unit: bool | None = None
    last_refresh_date: datetime.date | None = None
    leasing_agent: str | None = None
    tours_scheduled: int | None = None
    tours_completed: int | None = None
    applications_received: int | None = None
    showing_method: str | None = None
    why_still_vacant: str | None = None
    concession_type: str | None = None
    concession_proactive: bool | None = None
    notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ResidentInterview(BaseModel):
    """ResidentInterview entity."""

    interview_id: UUID
    assessment_id: UUID
    unit_id: UUID
    property_id: UUID
    interview_type: str
    interview_date: datetime.date
    resident_id: UUID | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
    created_at: datetime.datetime


class TourObservation(BaseModel):
    """TourObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    property_id: UUID
    observation_date: datetime.date
    data: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
    created_at: datetime.datetime
