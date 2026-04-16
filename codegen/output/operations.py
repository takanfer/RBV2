"""Operations domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class StaffMember(BaseModel):
    """StaffMember entity."""

    staff_id: UUID
    property_id: UUID
    staff_name: str
    role: str | None = None
    tenure_months: int | None = None
    certifications: str | None = None
    is_active: bool = True
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class Vendor(BaseModel):
    """Vendor entity."""

    vendor_id: UUID
    tenant_id: UUID
    vendor_name: str
    vendor_type: str | None = None
    contact_info: dict[str, Any] = Field(default_factory=dict)
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class WorkOrder(BaseModel):
    """WorkOrder entity."""

    work_order_id: UUID
    property_id: UUID
    unit_id: UUID | None = None
    work_order_number: str | None = None
    category: str
    sub_category: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str
    assigned_to: str | None = None
    vendor_id: UUID | None = None
    cost: Decimal | None = None
    date_created: datetime.date
    date_completed: datetime.date | None = None
    is_make_ready: bool = False
    source_ingestion_id: UUID | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class WorkOrderLineItem(BaseModel):
    """WorkOrderLineItem entity."""

    line_item_id: UUID
    work_order_id: UUID
    cost_category: str
    description: str | None = None
    amount: Decimal
    created_at: datetime.datetime


class WorkOrderStatusEvent(BaseModel):
    """WorkOrderStatusEvent entity."""

    event_id: UUID
    work_order_id: UUID
    status: str
    event_date: datetime.datetime
    notes: str | None = None
    created_at: datetime.datetime


class MakeReadyCycle(BaseModel):
    """MakeReadyCycle entity."""

    cycle_id: UUID
    property_id: UUID
    unit_id: UUID
    move_out_date: datetime.date | None = None
    notice_date: datetime.date | None = None
    make_ready_start: datetime.date | None = None
    make_ready_complete: datetime.date | None = None
    ready_observed: datetime.date | None = None
    first_listing_date: datetime.date | None = None
    first_tour_date: datetime.date | None = None
    first_showing_date: datetime.date | None = None
    application_date: datetime.date | None = None
    lease_signed_date: datetime.date | None = None
    move_in_date: datetime.date | None = None
    prior_lease_id: UUID | None = None
    new_lease_id: UUID | None = None
    total_turn_days: int | None = None
    make_ready_scope: str | None = None
    total_cost: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class VacancyCycle(BaseModel):
    """VacancyCycle entity."""

    cycle_id: UUID
    property_id: UUID
    unit_id: UUID
    vacancy_start: datetime.date
    vacancy_end: datetime.date | None = None
    days_vacant: int | None = None
    prior_rent: Decimal | None = None
    new_rent: Decimal | None = None
    vacancy_cost: Decimal | None = None
    make_ready_cycle_id: UUID | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class UnitConditionObservation(BaseModel):
    """UnitConditionObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    unit_id: UUID
    observation_date: datetime.date
    observer_id: UUID | None = None
    flooring: str | None = None
    walls_paint: str | None = None
    kitchen_cabinets: str | None = None
    kitchen_appliances: str | None = None
    bathroom_fixtures: str | None = None
    windows_blinds: str | None = None
    doors_hardware: str | None = None
    lighting_fixtures: str | None = None
    hvac_in_unit: str | None = None
    overall_cleanliness: str | None = None
    general_finish: str | None = None
    cleanliness_acceptable: bool | None = None
    odor_present: bool | None = None
    pest_evidence: bool | None = None
    water_damage: bool | None = None
    appliances_functional: bool | None = None
    windows_blinds_intact: bool | None = None
    hvac_operational: bool | None = None
    ready_to_show: bool | None = None
    condition_notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class FieldValidation(BaseModel):
    """FieldValidation entity."""

    validation_id: UUID
    assessment_id: UUID
    entity_type: str
    entity_id: UUID
    field_name: str
    pm_value: str | None = None
    field_value: str | None = None
    is_match: bool | None = None
    severity: str | None = None
    notes: str | None = None
    created_at: datetime.datetime


class BudgetActualLine(BaseModel):
    """BudgetActualLine entity."""

    line_id: UUID
    property_id: UUID
    assessment_id: UUID | None = None
    line_category: str
    line_item: str
    period_month: datetime.date
    budget_amount: Decimal | None = None
    actual_amount: Decimal | None = None
    per_unit_amount: Decimal | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class PropertyConditionObservation(BaseModel):
    """PropertyConditionObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    property_id: UUID
    observation_date: datetime.date
    overall_condition: str | None = None
    common_areas: str | None = None
    exterior_presentation: str | None = None
    amenities_condition: str | None = None
    issues_count: int | None = None
    issues_detail: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class CapitalAssetObservation(BaseModel):
    """CapitalAssetObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    property_id: UUID
    system_name: str
    system_type: str | None = None
    condition_rating: str | None = None
    install_year: int | None = None
    last_service_date: datetime.date | None = None
    age_years: int | None = None
    observation_notes: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class DeferredMaintenanceItem(BaseModel):
    """DeferredMaintenanceItem entity."""

    item_id: UUID
    assessment_id: UUID
    property_id: UUID
    location: str | None = None
    description: str
    affected_system: str | None = None
    severity: str | None = None
    estimated_cost: Decimal | None = None
    is_safety_hazard: bool = False
    photo_asset_id: UUID | None = None
    created_at: datetime.datetime


class FireSafetyObservation(BaseModel):
    """FireSafetyObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    property_id: UUID
    fire_inspection_current: bool | None = None
    last_fire_inspection: datetime.date | None = None
    open_violations: bool | None = None
    violation_count: int | None = None
    violation_details: str | None = None
    no_open_code_violations: bool | None = None
    ada_compliance_met: bool | None = None
    insurance_current: bool | None = None
    reac_nspire_score: Decimal | None = None
    elevator_inspection_current: bool | None = None
    last_elevator_inspection: datetime.date | None = None
    created_at: datetime.datetime


class BackOfHouseObservation(BaseModel):
    """BackOfHouseObservation entity."""

    observation_id: UUID
    assessment_id: UUID
    property_id: UUID
    shop_organized: bool | None = None
    parts_inventory_labeled: bool | None = None
    safety_equipment_present: bool | None = None
    fire_extinguisher_current: bool | None = None
    chemical_storage_compliant: bool | None = None
    vehicle_cart_condition: str | None = None
    cleanliness: str | None = None
    created_at: datetime.datetime
