"""Scoring Config domain models — generated from Database_Schema_Specification.md DDL."""

from __future__ import annotations

import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ScoringRubricVersion(BaseModel):
    """ScoringRubricVersion entity."""

    version_id: UUID
    version_label: str
    is_active: bool = False
    config: dict[str, Any]
    created_at: datetime.datetime


class BenchmarkVersion(BaseModel):
    """BenchmarkVersion entity."""

    version_id: UUID
    version_label: str
    benchmark_type: str
    data: dict[str, Any]
    is_active: bool = False
    created_at: datetime.datetime


class MetricRegistry(BaseModel):
    """MetricRegistry entity."""

    metric_id: UUID
    metric_name: str
    domain: str
    grain: str
    description: str | None = None
    formula: str | None = None
    required_inputs: dict[str, Any] = Field(default_factory=dict)
    output_type: str
    version: str
    created_at: datetime.datetime


class DiagnosticPackage(BaseModel):
    """DiagnosticPackage entity."""

    package_id: UUID
    package_name: str
    domain: str
    version: str
    required_inputs: dict[str, Any] = Field(default_factory=dict)
    optional_inputs: dict[str, Any] = Field(default_factory=dict)
    grain: str | None = None
    description: str | None = None
    is_active: bool = True
    created_at: datetime.datetime


class ImpactModelCatalog(BaseModel):
    """ImpactModelCatalog entity."""

    model_id: UUID
    model_name: str
    formula: str
    required_inputs: dict[str, Any] = Field(default_factory=dict)
    optional_refinements: dict[str, Any] = Field(default_factory=dict)
    low_high_params: dict[str, Any] = Field(default_factory=dict)
    double_count_rules: dict[str, Any] = Field(default_factory=dict)
    narrative: str | None = None
    version: str
    created_at: datetime.datetime
