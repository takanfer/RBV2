"""
DDL-to-Pydantic model generator.

Reads SQL DDL (from .sql file or extracted from .md fenced blocks),
parses with sqlglot, and produces:
  1. .py files with Pydantic v2 BaseModel classes
  2. A VERIFICATION_REPORT.txt mapping every DDL column → model field
  3. A Shared_Type_Definitions.md human-readable summary

Usage:
    python generate_models.py <ddl_source> <output_dir> [--domain-map <json>]

When <ddl_source> is a .md file, SQL is extracted from ```sql fenced blocks.
When <ddl_source> is a .sql file, the entire file is treated as SQL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

import sqlglot
from sqlglot import exp


# ── Type mapping: SQL → Python ────────────────────────────────────────────────

SQL_TO_PYTHON: dict[str, str] = {
    "uuid": "UUID",
    "text": "str",
    "string": "str",
    "varchar": "str",
    "char": "str",
    "boolean": "bool",
    "bool": "bool",
    "integer": "int",
    "int": "int",
    "int4": "int",
    "int32": "int",
    "bigint": "int",
    "int8": "int",
    "int64": "int",
    "smallint": "int",
    "int2": "int",
    "int16": "int",
    "uint8": "int",
    "uint16": "int",
    "uint32": "int",
    "uint64": "int",
    "serial": "int",
    "bigserial": "int",
    "numeric": "Decimal",
    "decimal": "Decimal",
    "float32": "float",
    "float64": "float",
    "real": "float",
    "float": "float",
    "float4": "float",
    "float8": "float",
    "double": "float",
    "date": "datetime.date",
    "datetime": "datetime.datetime",
    "timestamp": "datetime.datetime",
    "timestamptz": "datetime.datetime",
    "jsonb": "dict[str, Any]",
    "json": "dict[str, Any]",
}


def sql_type_to_python(sql_type: str) -> str:
    """Map a SQL type string to its Python type annotation.
    Handles ClickHouse wrappers: LowCardinality(String), Nullable(Type)."""
    normalized = sql_type.lower().strip()

    # Unwrap LowCardinality(X) → X
    lc_m = re.match(r"lowcardinality\((\w+)\)", normalized)
    if lc_m:
        normalized = lc_m.group(1)

    # Unwrap Nullable(X) → X (nullability handled separately)
    null_m = re.match(r"nullable\((.+)\)", normalized)
    if null_m:
        normalized = null_m.group(1).strip()

    # Strip precision: numeric(10,2) → numeric, Decimal(12,2) → decimal
    base = re.sub(r"\(.*\)", "", normalized).strip()
    return SQL_TO_PYTHON.get(base, "Any")


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class ColumnDef:
    name: str
    sql_type: str
    python_type: str
    nullable: bool
    has_default: bool
    default_value: str | None
    fk_table: str | None
    fk_column: str | None


@dataclass
class TableDef:
    name: str
    columns: list[ColumnDef] = field(default_factory=list)
    pk_columns: list[str] = field(default_factory=list)
    is_clickhouse: bool = False


# ── DDL extraction from markdown ──────────────────────────────────────────────

def extract_sql_from_markdown(md_text: str) -> str:
    """Pull all ```sql ... ``` blocks from a markdown file."""
    blocks = re.findall(r"```sql\n(.*?)```", md_text, re.DOTALL)
    return "\n\n".join(blocks)


# ── DDL parsing with sqlglot ──────────────────────────────────────────────────

def parse_ddl(sql: str) -> list[TableDef]:
    """Parse CREATE TABLE statements from SQL using sqlglot."""
    tables: list[TableDef] = []

    # sqlglot may not handle every PG extension, so we preprocess:
    # 1. Remove CREATE INDEX statements (not CREATE TABLE)
    # 2. Remove ClickHouse-specific uppercase DDL (handled separately)
    lines = sql.split("\n")
    cleaned_lines = []
    skip_block = False
    for line in lines:
        stripped = line.strip().upper()
        if stripped.startswith("CREATE INDEX") or stripped.startswith("CREATE UNIQUE INDEX"):
            continue
        # Skip ClickHouse CREATE TABLE blocks (uppercase)
        if stripped.startswith("CREATE TABLE") and not stripped.startswith("CREATE TABLE") == False:
            pass  # let sqlglot try all
        cleaned_lines.append(line)

    cleaned_sql = "\n".join(cleaned_lines)

    # Parse each CREATE TABLE individually for robustness
    # Find all create table blocks
    create_pattern = re.compile(
        r"(create\s+table\s+\w+\s*\(.*?\);)",
        re.DOTALL | re.IGNORECASE,
    )

    for match in create_pattern.finditer(cleaned_sql):
        stmt_text = match.group(1)
        # Detect ClickHouse: uppercase CREATE TABLE
        is_ch = stmt_text.lstrip().startswith("CREATE TABLE")
        table = parse_single_create_table(stmt_text, is_clickhouse=is_ch)
        if table:
            tables.append(table)

    return tables


def parse_single_create_table(stmt_text: str, is_clickhouse: bool = False) -> TableDef | None:
    """Parse a single CREATE TABLE statement using sqlglot."""
    if is_clickhouse:
        return _fallback_parse(stmt_text, is_clickhouse=True)

    try:
        parsed = sqlglot.parse_one(stmt_text, dialect="postgres")
    except Exception:
        try:
            parsed = sqlglot.parse_one(stmt_text)
        except Exception:
            return _fallback_parse(stmt_text)

    if not isinstance(parsed, exp.Create):
        return None

    table_expr = parsed.this
    if not isinstance(table_expr, exp.Schema):
        return None

    table_name_node = table_expr.this
    table_name = table_name_node.name if hasattr(table_name_node, "name") else str(table_name_node)

    table = TableDef(name=table_name.lower())

    for col_def in table_expr.expressions:
        if isinstance(col_def, exp.ColumnDef):
            col = _extract_column(col_def, stmt_text)
            if col:
                table.columns.append(col)

    for col in table.columns:
        if col.name in _find_pk_columns(stmt_text):
            table.pk_columns.append(col.name)

    return table if table.columns else None


def _extract_column(col_def: exp.ColumnDef, raw_stmt: str) -> ColumnDef | None:
    """Extract column info from a sqlglot ColumnDef node."""
    col_name = col_def.this.name if hasattr(col_def.this, "name") else str(col_def.this)
    col_name = col_name.lower()

    # Get SQL type
    kind = col_def.args.get("kind")
    if kind:
        sql_type = kind.sql(dialect="postgres").lower()
    else:
        sql_type = "text"

    # Determine nullability and defaults from the raw line
    raw_line = _find_raw_line(raw_stmt, col_name)

    nullable = True
    has_default = False
    default_value = None

    if raw_line:
        line_upper = raw_line.upper()
        if "NOT NULL" in line_upper:
            nullable = False
        if "DEFAULT" in line_upper:
            has_default = True
            dm = re.search(r"DEFAULT\s+(.+?)(?:\s*,?\s*$)", raw_line, re.IGNORECASE)
            if dm:
                default_value = dm.group(1).strip().rstrip(",")
        if "PRIMARY KEY" in line_upper:
            nullable = False
            has_default = True

    # FK detection
    fk_table = None
    fk_column = None
    if raw_line:
        fk_m = re.search(r"REFERENCES\s+(\w+)\s*\((\w+)\)", raw_line, re.IGNORECASE)
        if fk_m:
            fk_table = fk_m.group(1).lower()
            fk_column = fk_m.group(2).lower()

    python_type = sql_type_to_python(sql_type)

    return ColumnDef(
        name=col_name,
        sql_type=sql_type,
        python_type=python_type,
        nullable=nullable,
        has_default=has_default,
        default_value=default_value,
        fk_table=fk_table,
        fk_column=fk_column,
    )


def _find_raw_line(stmt: str, col_name: str) -> str | None:
    """Find the raw DDL line for a column name."""
    for line in stmt.split("\n"):
        stripped = line.strip()
        tokens = stripped.split()
        if tokens and tokens[0].lower().strip('"') == col_name:
            return stripped
    return None


def _find_pk_columns(stmt: str) -> set[str]:
    """Find columns marked as PRIMARY KEY in the statement."""
    pks = set()
    for line in stmt.split("\n"):
        stripped = line.strip().lower()
        tokens = stripped.split()
        if len(tokens) >= 2 and "primary" in stripped and "key" in stripped:
            if not stripped.startswith("primary"):
                pks.add(tokens[0].strip('"'))
    return pks


def _fallback_parse(stmt_text: str, is_clickhouse: bool = False) -> TableDef | None:
    """Regex-based fallback parser for statements sqlglot can't handle."""
    m = re.search(r"create\s+table\s+(\w+)\s*\(", stmt_text, re.IGNORECASE)
    if not m:
        return None

    table = TableDef(name=m.group(1).lower(), is_clickhouse=is_clickhouse)
    body = stmt_text[m.end():]
    body = re.sub(r"\)\s*;?\s*$", "", body, flags=re.DOTALL)

    for line in body.split("\n"):
        stripped = line.strip().rstrip(",")
        if not stripped:
            continue
        upper = stripped.upper()
        if any(upper.startswith(kw) for kw in [
            "PRIMARY KEY", "UNIQUE", "CHECK", "FOREIGN KEY",
            "CONSTRAINT", "--", "ENGINE", "ORDER BY",
        ]):
            continue
        if stripped.startswith(")"):
            break

        col_m = re.match(r"(\w+)\s+(.+)", stripped)
        if not col_m:
            continue

        col_name = col_m.group(1).lower()
        rest = col_m.group(2)

        type_m = re.match(
            r"(Nullable\(\w+(?:\([\d,\s]+\))?\)|LowCardinality\(\w+\)|[\w]+(?:\s*\([\d,\s]+\))?)",
            rest, re.IGNORECASE,
        )
        sql_type = type_m.group(1).lower() if type_m else "text"
        python_type = sql_type_to_python(sql_type)

        if is_clickhouse:
            nullable = "nullable(" in rest.lower()
        else:
            nullable = "not null" not in rest.lower()
        has_default = "default" in rest.lower()
        default_value = None
        if has_default:
            dm = re.search(r"default\s+(.+?)(?:\s*,?\s*$)", rest, re.IGNORECASE)
            if dm:
                default_value = dm.group(1).strip()

        if "primary key" in rest.lower():
            nullable = False
            has_default = True
            table.pk_columns.append(col_name)

        fk_table = None
        fk_column = None
        fk_m = re.search(r"references\s+(\w+)\s*\((\w+)\)", rest, re.IGNORECASE)
        if fk_m:
            fk_table = fk_m.group(1).lower()
            fk_column = fk_m.group(2).lower()

        table.columns.append(ColumnDef(
            name=col_name,
            sql_type=sql_type,
            python_type=python_type,
            nullable=nullable,
            has_default=has_default,
            default_value=default_value,
            fk_table=fk_table,
            fk_column=fk_column,
        ))

    return table if table.columns else None


# ── Code generation ───────────────────────────────────────────────────────────

def snake_to_pascal(name: str) -> str:
    """Convert snake_case table name to PascalCase class name."""
    return "".join(word.capitalize() for word in name.split("_"))


def generate_field_line(col: ColumnDef) -> str:
    """Generate a single Pydantic field line."""
    py_type = col.python_type

    if col.nullable and not col.has_default:
        annotation = f"{py_type} | None"
        default = " = None"
    elif col.nullable and col.has_default:
        annotation = f"{py_type} | None"
        default = " = None"
    elif not col.nullable and col.has_default:
        if py_type == "dict[str, Any]":
            annotation = py_type
            default = " = Field(default_factory=dict)"
        elif col.default_value and "true" in col.default_value.lower():
            annotation = py_type
            default = " = True"
        elif col.default_value and "false" in col.default_value.lower():
            annotation = py_type
            default = " = False"
        else:
            annotation = py_type
            default = ""
    else:
        annotation = py_type
        default = ""

    return f"    {col.name}: {annotation}{default}"


def generate_model_class(table: TableDef) -> str:
    """Generate a Pydantic model class for a table."""
    class_name = snake_to_pascal(table.name)
    lines = [
        f"class {class_name}(BaseModel):",
        f'    """{class_name} entity."""',
        "",
    ]

    for col in table.columns:
        lines.append(generate_field_line(col))

    return "\n".join(lines)


def generate_module(tables: list[TableDef], domain_name: str) -> str:
    """Generate a full .py module for a domain."""
    needs_decimal = any(c.python_type == "Decimal" for t in tables for c in t.columns)
    needs_date = any(c.python_type in ("datetime.date", "datetime.datetime") for t in tables for c in t.columns)
    needs_any = any("Any" in c.python_type for t in tables for c in t.columns)
    needs_uuid = any(c.python_type == "UUID" for t in tables for c in t.columns)
    needs_field = any(
        c.python_type == "dict[str, Any]" and not c.nullable and c.has_default
        for t in tables for c in t.columns
    )

    parts = [
        f'"""{ domain_name.replace("_", " ").title() } domain models — generated from Database_Schema_Specification.md DDL."""',
        "",
        "from __future__ import annotations",
        "",
    ]

    stdlib_imports = []
    if needs_date:
        stdlib_imports.append("import datetime")
    if needs_decimal:
        stdlib_imports.append("from decimal import Decimal")
    if needs_any:
        stdlib_imports.append("from typing import Any")
    if needs_uuid:
        stdlib_imports.append("from uuid import UUID")
    if stdlib_imports:
        parts.extend(stdlib_imports)
        parts.append("")

    pydantic_imports = ["from pydantic import BaseModel"]
    if needs_field:
        pydantic_imports = ["from pydantic import BaseModel, Field"]
    parts.extend(pydantic_imports)
    parts.append("")
    parts.append("")

    for i, table in enumerate(tables):
        parts.append(generate_model_class(table))
        if i < len(tables) - 1:
            parts.append("")
            parts.append("")

    parts.append("")  # trailing newline

    return "\n".join(parts)


# ── Verification report ──────────────────────────────────────────────────────

def generate_verification_report(all_tables: list[TableDef]) -> str:
    """Generate VERIFICATION_REPORT.txt."""
    lines = [
        "=" * 80,
        "MODEL GENERATION VERIFICATION REPORT",
        "=" * 80,
        f"Tables processed: {len(all_tables)}",
        f"Total columns:    {sum(len(t.columns) for t in all_tables)}",
        "",
    ]

    for table in all_tables:
        class_name = snake_to_pascal(table.name)
        lines.append(f"  {table.name} → {class_name}")
        lines.append(f"  {'─' * 70}")
        lines.append(f"  {'DDL Column':<30} {'SQL Type':<20} {'Python Type':<20} {'Null':>5}")
        lines.append(f"  {'─' * 70}")
        for col in table.columns:
            null_str = "NULL" if col.nullable else "NOT"
            lines.append(f"  {col.name:<30} {col.sql_type:<20} {col.python_type:<20} {null_str:>5}")
        lines.append("")

    lines.append("=" * 80)
    lines.append("END OF VERIFICATION REPORT")
    lines.append("=" * 80)
    return "\n".join(lines)


# ── Markdown summary ─────────────────────────────────────────────────────────

def generate_markdown_summary(
    domain_tables: dict[str, list[TableDef]],
) -> str:
    """Generate Shared_Type_Definitions.md."""
    lines = [
        "# Shared Type Definitions",
        "",
        "Pydantic v2 models generated from the DDL in `Database_Schema_Specification.md`.",
        "These models live in `src/shared/models/` and are the canonical Python representation",
        "of every database entity.",
        "",
        "**Do not edit generated model files by hand.** Re-run `codegen/generate_models.py`",
        "against the DDL to regenerate after schema changes.",
        "",
        "---",
        "",
    ]

    total_tables = sum(len(tables) for tables in domain_tables.values())
    total_cols = sum(len(c) for tables in domain_tables.values() for t in tables for c in [t.columns])
    lines.append(f"**Total models:** {total_tables}")
    lines.append(f"**Total fields:** {sum(len(t.columns) for tables in domain_tables.values() for t in tables)}")
    lines.append("")

    for domain, tables in domain_tables.items():
        module_name = domain.replace(" ", "_").lower()
        lines.append(f"## {domain}")
        lines.append("")
        lines.append(f"Module: `src/shared/models/{module_name}.py`")
        lines.append("")

        for table in tables:
            class_name = snake_to_pascal(table.name)
            lines.append(f"### `{class_name}`")
            lines.append("")
            lines.append(f"Table: `{table.name}` ({len(table.columns)} fields)")
            lines.append("")
            lines.append("| Field | Python Type | Nullable | SQL Type |")
            lines.append("|-------|-----------|----------|----------|")
            for col in table.columns:
                null = "Yes" if col.nullable else "No"
                lines.append(f"| `{col.name}` | `{col.python_type}` | {null} | `{col.sql_type}` |")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


# ── Domain classification ─────────────────────────────────────────────────────

DEFAULT_DOMAIN_MAP: dict[str, str] = {
    "tenant": "infrastructure",
    "client": "infrastructure",
    "portfolio": "infrastructure",
    "user_account": "infrastructure",
    "audit_log": "infrastructure",
    "source_system": "raw_evidence",
    "source_ingestion": "raw_evidence",
    "source_asset": "raw_evidence",
    "source_record_raw": "raw_evidence",
    "mapping_rule": "raw_evidence",
    "mapping_review_queue": "raw_evidence",
    "property": "asset",
    "building": "asset",
    "floor_plan": "asset",
    "unit": "asset",
    "unit_version": "asset",
    "unit_existence_interval": "asset",
    "unit_alias": "asset",
    "calendar_day": "asset",
    "property_amenity": "asset",
    "unit_amenity": "asset",
    "market_context": "asset",
    "resident": "lease",
    "lease": "lease",
    "lease_interval": "lease",
    "lease_charge": "lease",
    "lease_event": "lease",
    "notice_event": "lease",
    "move_event": "lease",
    "renewal_offer": "lease",
    "payment_event": "lease",
    "delinquency_snapshot": "lease",
    "staff_member": "operations",
    "vendor": "operations",
    "work_order": "operations",
    "work_order_line_item": "operations",
    "work_order_status_event": "operations",
    "make_ready_cycle": "operations",
    "vacancy_cycle": "operations",
    "unit_condition_observation": "operations",
    "property_condition_observation": "operations",
    "capital_asset_observation": "operations",
    "deferred_maintenance_item": "operations",
    "fire_safety_observation": "operations",
    "back_of_house_observation": "operations",
    "field_validation": "operations",
    "budget_actual_line": "operations",
    "lead": "demand",
    "lead_source": "demand",
    "lead_event": "demand",
    "agent": "demand",
    "communication_event": "demand",
    "tour_event": "demand",
    "application_event": "demand",
    "crm_assignment_interval": "demand",
    "conversion_metric_snapshot": "demand",
    "marketing_channel": "marketing",
    "campaign": "marketing",
    "campaign_spend": "marketing",
    "listing": "marketing",
    "listing_asset": "marketing",
    "listing_observation": "marketing",
    "listing_content_assessment": "marketing",
    "listing_photo_assessment": "marketing",
    "marketing_observation": "marketing",
    "website_observation": "marketing",
    "social_observation": "marketing",
    "reputation_observation": "marketing",
    "google_business_observation": "marketing",
    "competitive_set": "competitive",
    "competitive_set_member": "competitive",
    "comp_floorplan": "competitive",
    "comp_listing_observation": "competitive",
    "comp_property_observation": "competitive",
    "comp_marketing_assessment": "competitive",
    "mystery_shop": "field_evidence",
    "vacant_unit_audit": "field_evidence",
    "resident_interview": "field_evidence",
    "tour_observation": "field_evidence",
    "assessment": "assessment",
    "assessment_data_coverage": "assessment",
    "analysis_run": "assessment",
    "scorecard": "assessment",
    "score_result": "assessment",
    "finding": "assessment",
    "impact_estimate": "assessment",
    "contradiction": "assessment",
    "recommendation": "assessment",
    "report": "assessment",
    "report_section": "assessment",
    "report_render": "assessment",
    "scoring_rubric_version": "scoring_config",
    "benchmark_version": "scoring_config",
    "metric_registry": "scoring_config",
    "diagnostic_package": "scoring_config",
    "impact_model_catalog": "scoring_config",
    "study": "workspace",
    "study_item": "workspace",
    "saved_query": "workspace",
    "result_snapshot": "workspace",
    "comparison_board": "workspace",
    "annotation": "workspace",
    "evidence_bundle": "workspace",
    "tech_platform": "intake_snapshot",
    "tech_summary": "intake_snapshot",
    "staffing_snapshot": "intake_snapshot",
    "leasing_model_snapshot": "intake_snapshot",
    "resident_event_program": "intake_snapshot",
    "renewal_retention_snapshot": "intake_snapshot",
    "partnership_referral_snapshot": "intake_snapshot",
    "fact_unit_day": "clickhouse_facts",
    "fact_lease_interval": "clickhouse_facts",
    "fact_vacancy_cycle": "clickhouse_facts",
    "fact_work_order": "clickhouse_facts",
    "fact_lead_funnel_event": "clickhouse_facts",
    "fact_listing_observation": "clickhouse_facts",
    "fact_marketing_presence_day": "clickhouse_facts",
    "fact_comp_listing_observation": "clickhouse_facts",
    "fact_score_result": "clickhouse_facts",
    "fact_finding_impact": "clickhouse_facts",
    "fact_assessment_score": "clickhouse_facts",
    "fact_assessment_finding": "clickhouse_facts",
    "fact_recommendation_status": "clickhouse_facts",
    "fact_property_kpi_period": "clickhouse_facts",
    "fact_unit_chronicity": "clickhouse_facts",
}


def classify_table(table_name: str, domain_map: dict[str, str]) -> str:
    """Return the domain for a table, or 'uncategorized'."""
    return domain_map.get(table_name, "uncategorized")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Pydantic models from DDL")
    parser.add_argument("ddl_source", help="Path to .sql or .md file with DDL")
    parser.add_argument("output_dir", help="Directory for generated output")
    parser.add_argument("--domain-map", help="JSON file with table→domain overrides")
    parser.add_argument("--single-domain", help="Force all tables into one domain module (for testing)")
    args = parser.parse_args()

    ddl_path = Path(args.ddl_source)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load DDL
    raw = ddl_path.read_text()
    if ddl_path.suffix == ".md":
        sql = extract_sql_from_markdown(raw)
    else:
        sql = raw

    # Parse
    print(f"Parsing {ddl_path}...")
    tables = parse_ddl(sql)
    print(f"  Parsed {len(tables)} tables ({sum(len(t.columns) for t in tables)} columns)")

    if not tables:
        print("ERROR: No tables parsed.")
        sys.exit(1)

    # Domain map
    domain_map = dict(DEFAULT_DOMAIN_MAP)
    if args.domain_map:
        with open(args.domain_map) as f:
            domain_map.update(json.load(f))

    # Group tables by domain
    domain_tables: dict[str, list[TableDef]] = OrderedDict()
    for table in tables:
        if args.single_domain:
            domain = args.single_domain
        else:
            domain = classify_table(table.name, domain_map)
        domain_tables.setdefault(domain, []).append(table)

    # Generate .py files
    for domain, dtables in domain_tables.items():
        module_code = generate_module(dtables, domain)
        py_path = output_dir / f"{domain}.py"
        py_path.write_text(module_code)
        print(f"  Wrote {py_path} ({len(dtables)} models)")

    # Verification report
    report = generate_verification_report(tables)
    report_path = output_dir / "VERIFICATION_REPORT.txt"
    report_path.write_text(report)
    print(f"  Wrote {report_path}")

    # Markdown summary
    md = generate_markdown_summary(domain_tables)
    md_path = output_dir / "Shared_Type_Definitions.md"
    md_path.write_text(md)
    print(f"  Wrote {md_path}")

    print(f"\nDone. {len(tables)} tables → {len(domain_tables)} modules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
