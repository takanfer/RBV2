"""Assessment domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Assessment(BaseModel):
    """Assessment entity."""

    assessment_id: UUID
    tenant_id: UUID
    property_id: UUID
    client_id: UUID | None = None
    assessment_type: str
    status: str
    date_range_start: datetime.date | None = None
    date_range_end: datetime.date | None = None
    site_visit_date: datetime.date | None = None
    comp_set_id: UUID | None = None
    created_by: UUID | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AssessmentDataCoverage(BaseModel):
    """AssessmentDataCoverage entity."""

    coverage_id: UUID
    assessment_id: UUID
    domain: str
    source_system_id: UUID | None = None
    coverage_status: str
    coverage_pct: Decimal | None = None
    notes: str | None = None
    created_at: datetime.datetime


class AnalysisRun(BaseModel):
    """AnalysisRun entity."""

    run_id: UUID
    assessment_id: UUID
    rule_package_version: str
    benchmark_version: str | None = None
    transformation_version: str | None = None
    status: str
    started_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    created_at: datetime.datetime


class Scorecard(BaseModel):
    """Scorecard entity."""

    scorecard_id: UUID
    assessment_id: UUID
    analysis_run_id: UUID | None = None
    scorecard_type: str
    overall_score: Decimal | None = None
    overall_grade: str | None = None
    version: str
    created_at: datetime.datetime


class ScoreResult(BaseModel):
    """ScoreResult entity."""

    result_id: UUID
    scorecard_id: UUID
    assessment_id: UUID
    analysis_run_id: UUID | None = None
    scoring_level: str
    area_number: int | None = None
    area_name: str | None = None
    item_name: str | None = None
    sub_item_name: str | None = None
    input_type: str | None = None
    metric_value: Decimal | None = None
    normalized_score: Decimal | None = None
    weight: Decimal | None = None
    weighted_score: Decimal | None = None
    benchmark_type: str | None = None
    benchmark_reference: str | None = None
    confidence_score: Decimal | None = None
    coverage_score: Decimal | None = None
    grade_letter: str | None = None
    scope_status: str | None = None
    evidence_count: int | None = None
    version: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class Finding(BaseModel):
    """Finding entity."""

    finding_id: UUID
    assessment_id: UUID
    analysis_run_id: UUID | None = None
    finding_type: str
    domain: str
    severity: str
    title: str
    description: str
    entity_type: str | None = None
    entity_id: UUID | None = None
    evidence_refs: dict[str, Any] = Field(default_factory=dict)
    contributing_causes: dict[str, Any] = Field(default_factory=dict)
    confidence: Decimal | None = None
    rule_package_version: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime.datetime


class ImpactEstimate(BaseModel):
    """ImpactEstimate entity."""

    estimate_id: UUID
    finding_id: UUID
    assessment_id: UUID
    impact_model: str
    impact_family_id: UUID | None = None
    primary_driver_share: Decimal | None = None
    contributing_share: Decimal | None = None
    low_estimate: Decimal | None = None
    base_estimate: Decimal | None = None
    high_estimate: Decimal | None = None
    annualized_amount: Decimal | None = None
    per_unit_amount: Decimal | None = None
    formula_trace: dict[str, Any] = Field(default_factory=dict)
    assumption_trace: dict[str, Any] = Field(default_factory=dict)
    confidence: Decimal | None = None
    created_at: datetime.datetime


class Contradiction(BaseModel):
    """Contradiction entity."""

    contradiction_id: UUID
    assessment_id: UUID
    source_a_type: str
    source_a_ref: UUID | None = None
    source_b_type: str
    source_b_ref: UUID | None = None
    matching_rule: str
    contradiction_type: str
    severity: str
    affected_domains: dict[str, Any] = Field(default_factory=dict)
    trust_penalty: Decimal | None = None
    evidence_links: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None
    created_at: datetime.datetime


class Recommendation(BaseModel):
    """Recommendation entity."""

    recommendation_id: UUID
    finding_id: UUID | None = None
    assessment_id: UUID
    domain: str
    target_entity_type: str | None = None
    target_entity_id: UUID | None = None
    priority: str
    title: str
    description: str
    expected_impact: dict[str, Any] | None = None
    owner: str | None = None
    due_date: datetime.date | None = None
    status: str
    verification_evidence: dict[str, Any] | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Report(BaseModel):
    """Report entity."""

    report_id: UUID
    assessment_id: UUID
    template_name: str
    report_type: str
    status: str
    created_by: UUID | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ReportSection(BaseModel):
    """ReportSection entity."""

    section_id: UUID
    report_id: UUID
    section_type: str
    sort_order: int
    title: str | None = None
    content: dict[str, Any] = Field(default_factory=dict)
    data_bindings: dict[str, Any] = Field(default_factory=dict)
    narrative: str | None = None
    chart_spec: dict[str, Any] | None = None
    created_at: datetime.datetime


class ReportRender(BaseModel):
    """ReportRender entity."""

    render_id: UUID
    report_id: UUID
    format: str
    storage_path: str
    section_manifest: dict[str, Any] = Field(default_factory=dict)
    rendered_at: datetime.datetime
    rendered_by: UUID | None = None
