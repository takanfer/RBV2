"""Marketing domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MarketingChannel(BaseModel):
    """MarketingChannel entity."""

    channel_id: UUID
    property_id: UUID
    channel_name: str
    channel_type: str
    platform_url: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class Campaign(BaseModel):
    """Campaign entity."""

    campaign_id: UUID
    property_id: UUID
    channel_id: UUID | None = None
    campaign_name: str
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    budget: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CampaignSpend(BaseModel):
    """CampaignSpend entity."""

    spend_id: UUID
    campaign_id: UUID
    period_month: datetime.date
    amount: Decimal
    created_at: datetime.datetime


class WebsiteObservation(BaseModel):
    """WebsiteObservation entity."""

    observation_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    observation_date: datetime.date
    website_url: str | None = None
    website_exists: bool | None = None
    mobile_responsive: bool | None = None
    live_chat: bool | None = None
    contact_form: bool | None = None
    floor_plans: bool | None = None
    photo_gallery: bool | None = None
    unit_availability: bool | None = None
    virtual_tours: bool | None = None
    online_application: bool | None = None
    tour_scheduling: bool | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class SocialObservation(BaseModel):
    """SocialObservation entity."""

    observation_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    platform: str
    profile_url: str | None = None
    is_active: bool | None = None
    follower_count: int | None = None
    post_frequency: str | None = None
    observation_date: datetime.date
    created_at: datetime.datetime


class ReputationObservation(BaseModel):
    """ReputationObservation entity."""

    observation_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    platform: str
    platform_url: str | None = None
    profile_exists: bool | None = None
    review_score: Decimal | None = None
    review_count: int | None = None
    reviews_last_90d: int | None = None
    observation_date: datetime.date
    created_at: datetime.datetime


class GoogleBusinessObservation(BaseModel):
    """GoogleBusinessObservation entity."""

    observation_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    gmb_claimed: bool | None = None
    gmb_optimized: bool | None = None
    observation_date: datetime.date
    created_at: datetime.datetime


class Listing(BaseModel):
    """Listing entity."""

    listing_id: UUID
    property_id: UUID
    unit_id: UUID | None = None
    floor_plan_id: UUID | None = None
    channel_id: UUID | None = None
    platform: str
    listing_url: str | None = None
    first_listed_date: datetime.date | None = None
    delisted_date: datetime.date | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ListingObservation(BaseModel):
    """ListingObservation entity."""

    observation_id: UUID
    listing_id: UUID | None = None
    property_id: UUID
    unit_id: UUID | None = None
    assessment_id: UUID | None = None
    platform: str
    observation_date: datetime.date
    asking_rent: Decimal | None = None
    concession_displayed: bool | None = None
    concession_amount: Decimal | None = None
    photo_count: int | None = None
    photo_quality: Decimal | None = None
    description_quality: Decimal | None = None
    description_word_count: int | None = None
    floor_plan_available: bool | None = None
    virtual_tour_available: bool | None = None
    amenities_listed: bool | None = None
    pricing_accurate: bool | None = None
    matches_availability: bool | None = None
    contact_info_accurate: bool | None = None
    listing_url: str | None = None
    notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ListingPhotoAssessment(BaseModel):
    """ListingPhotoAssessment entity."""

    assessment_photo_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    hero_image_present: bool | None = None
    exterior_shots_count: int | None = None
    living_room_shown: bool | None = None
    kitchen_shown: bool | None = None
    bedrooms_shown: bool | None = None
    bathrooms_shown: bool | None = None
    features_shown: bool | None = None
    pool_photo: bool | None = None
    fitness_photo: bool | None = None
    clubhouse_photo: bool | None = None
    other_amenity_count: int | None = None
    total_amenities: int | None = None
    amenities_photographed: int | None = None
    lifestyle_photos: int | None = None
    professional_photographer: bool | None = None
    last_photo_update: datetime.date | None = None
    shows_actual_units: str | None = None
    created_at: datetime.datetime


class ListingContentAssessment(BaseModel):
    """ListingContentAssessment entity."""

    content_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    platform_count: int | None = None
    ils_coverage: str | None = None
    posting_method: str | None = None
    syndication_tool: str | None = None
    update_frequency: str | None = None
    usp_mentioned: bool | None = None
    neighborhood_context: bool | None = None
    call_to_action: bool | None = None
    contact_info_clear: bool | None = None
    floor_plans_on_listing: bool | None = None
    unit_specs_accurate: bool | None = None
    amenities_fully_listed: bool | None = None
    pet_policy_stated: bool | None = None
    lease_terms_mentioned: bool | None = None
    pricing_consistent: bool | None = None
    availability_accurate: bool | None = None
    photos_match_condition: bool | None = None
    specials_updated: bool | None = None
    created_at: datetime.datetime


class ListingAsset(BaseModel):
    """ListingAsset entity."""

    asset_id: UUID
    listing_id: UUID
    asset_type: str
    storage_path: str | None = None
    quality_score: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class MarketingObservation(BaseModel):
    """MarketingObservation entity."""

    observation_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    observation_date: datetime.date
    observation_type: str
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
