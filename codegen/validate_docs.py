"""
Documentation Cross-Reference Validator.

Mechanically validates every cross-reference across all RBv2 documentation
files against the source-of-truth files (DDL, JSON configs, service contracts,
project skeleton). Produces a report listing every mismatch.

Usage:
    python3 codegen/validate_docs.py                 # from REBOOT/RBv2/
    python3 codegen/validate_docs.py --json          # output JSON report
    python3 codegen/validate_docs.py --root /path    # override document root

Exit code 0 = clean, exit code 1 = errors found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

ROOT: Path = Path(__file__).resolve().parent.parent  # REBOOT/RBv2/

_STATIC_ALIASES: dict[str, str] = {
    "spec_1": "specs/platform/spec_1_multifamily_property_assessment_platform.md",
    "DDL": "specs/platform/Database_Schema_Specification.md",
    "ADR-001": "docs/adrs/ADR-001-python-version.md",
    "ADR-002": "docs/adrs/ADR-002-api-framework.md",
    "ADR-003": "docs/adrs/ADR-003-database-access.md",
    "ADR-004": "docs/adrs/ADR-004-schema-migrations.md",
    "ADR-005": "docs/adrs/ADR-005-package-manager.md",
    "ADR-006": "docs/adrs/ADR-006-testing.md",
    "ADR-007": "docs/adrs/ADR-007-linting-formatting.md",
    "ADR-008": "docs/adrs/ADR-008-local-development.md",
    "ADR-009": "docs/adrs/ADR-009-frontend-stack.md",
    "ADR-010": "docs/adrs/ADR-010-mobile-field-capture.md",
    "ADR-011": "docs/adrs/ADR-011-repository-structure.md",
    "ADR-012": "docs/adrs/ADR-012-ci-cd.md",
    "ADR-013": "docs/adrs/ADR-013-cloud-provider.md",
    "ADR-014": "docs/adrs/ADR-014-task-queue.md",
    "ADR-015": "docs/adrs/ADR-015-authentication.md",
    "ADR-016": "docs/adrs/ADR-016-report-rendering.md",
}

DOC_ALIASES: dict[str, str] = {}
SCAN_DIRS: list[Path] = []
EXCLUDE_PREFIXES = ["DEPRECATED/", "codegen/output/", "codegen/test_fixtures/"]

_SPEC_SUBDIRS = [
    "specs/platform", "specs/patterns", "specs/scoring",
    "specs/engine", "specs/data", "specs/auth", "specs/ui",
]


def _init_root(root_path: Path) -> None:
    global ROOT, DOC_ALIASES, SCAN_DIRS
    ROOT = root_path.resolve()

    DOC_ALIASES.clear()
    DOC_ALIASES.update(_STATIC_ALIASES)

    rules_dir = ROOT / ".cursor" / "rules"
    if rules_dir.is_dir():
        for _p in rules_dir.glob("*.mdc"):
            DOC_ALIASES[_p.name] = f".cursor/rules/{_p.name}"

    # Root-level .md files (if any remain)
    for _p in ROOT.glob("*.md"):
        DOC_ALIASES[_p.name] = _p.name

    # specs/ subdirectories
    for subdir in _SPEC_SUBDIRS:
        spec_dir = ROOT / subdir
        if spec_dir.is_dir():
            for _p in spec_dir.glob("*.md"):
                DOC_ALIASES[_p.name] = f"{subdir}/{_p.name}"

    # config/ directory
    config_dir = ROOT / "config"
    if config_dir.is_dir():
        for _p in config_dir.glob("*"):
            if _p.is_file():
                DOC_ALIASES[_p.name] = f"config/{_p.name}"

    # planning/ directory
    planning_dir = ROOT / "planning"
    if planning_dir.is_dir():
        for _p in planning_dir.glob("*.md"):
            DOC_ALIASES[_p.name] = f"planning/{_p.name}"

    adrs_dir = ROOT / "docs" / "adrs"
    if adrs_dir.is_dir():
        for _p in adrs_dir.glob("*.md"):
            DOC_ALIASES[_p.name] = f"docs/adrs/{_p.name}"

    SCAN_DIRS.clear()
    SCAN_DIRS.extend([ROOT, rules_dir, adrs_dir])
    for subdir in _SPEC_SUBDIRS:
        d = ROOT / subdir
        if d.is_dir():
            SCAN_DIRS.append(d)
    for extra in ["config", "planning"]:
        d = ROOT / extra
        if d.is_dir():
            SCAN_DIRS.append(d)


def _gt_path(relative: str) -> Path:
    """Resolve a ground truth file path, trying the given relative path first
    then falling back to the filename at ROOT level (for test fixtures)."""
    primary = ROOT / relative
    if primary.exists():
        return primary
    fallback = ROOT / Path(relative).name
    if fallback.exists():
        return fallback
    return primary


def get_files_to_scan() -> list[Path]:
    files = []
    for d in SCAN_DIRS:
        if not d.is_dir():
            continue
        for ext in ("*.md", "*.mdc"):
            for f in d.glob(ext):
                rel = f.relative_to(ROOT)
                if not any(str(rel).startswith(p) for p in EXCLUDE_PREFIXES):
                    files.append(f)
    return sorted(set(files))


def resolve_doc(name: str) -> "Path | None":
    clean = name.strip().strip("`").strip()
    if clean in DOC_ALIASES:
        return ROOT / DOC_ALIASES[clean]
    candidate = ROOT / clean
    if candidate.exists():
        return candidate
    deprecated_candidate = ROOT / "DEPRECATED" / clean
    if deprecated_candidate.exists():
        return deprecated_candidate
    for alias, path in DOC_ALIASES.items():
        if clean.lower() == alias.lower():
            return ROOT / path
    return None


# ── Error tracking ───────────────────────────────────────────────────────────

@dataclass
class ValidationError:
    pass_name: str
    file: str
    line: int
    message: str
    detail: str = ""


@dataclass
class ValidationReport:
    errors: list[ValidationError] = field(default_factory=list)
    checks: int = 0

    def error(self, pass_name: str, file: str, line: int, message: str, detail: str = ""):
        self.errors.append(ValidationError(pass_name, file, line, message, detail))

    def check(self):
        self.checks += 1


# ── Ground Truth Extractors ──────────────────────────────────────────────────

@dataclass
class DDLGroundTruth:
    tables: dict[str, list[str]] = field(default_factory=dict)
    table_lines: dict[str, int] = field(default_factory=dict)
    enum_comments: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    pg_table_count: int = 0
    ch_table_count: int = 0
    pg_tables: set[str] = field(default_factory=set)
    ch_tables: set[str] = field(default_factory=set)
    bitemporal_tables: set[str] = field(default_factory=set)
    audit_tables: set[str] = field(default_factory=set)


def extract_ddl_ground_truth(ddl_path: Path) -> DDLGroundTruth:
    gt = DDLGroundTruth()
    text = ddl_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    in_sql_block = False
    current_sql: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if line.strip() == "```sql":
            in_sql_block = True
            current_sql = []
            continue
        if line.strip() == "```" and in_sql_block:
            in_sql_block = False
            _parse_sql_block(gt, current_sql)
            continue
        if in_sql_block:
            current_sql.append((i, line))

    return gt


_SKIP_COL_KEYWORDS = frozenset({
    "primary", "foreign", "constraint", "unique", "check",
    "create", "engine", "order", "partition", "settings",
})


def _parse_sql_block(gt: DDLGroundTruth, lines_with_nums: list[tuple[int, str]]):
    current_table: "str | None" = None
    current_table_line = 0
    current_columns: list[str] = []
    current_enums: dict[str, list[str]] = {}
    in_create = False
    is_ch = False

    for line_num, line in lines_with_nums:
        stripped = line.strip()

        ct_match = re.match(r"(?i)(create\s+table)\s+(\w+)", stripped)
        if ct_match:
            if current_table:
                _store_table(gt, current_table, current_table_line,
                             current_columns, current_enums, is_ch)
            raw_kw = ct_match.group(1)
            is_ch = raw_kw[0].isupper()
            current_table = ct_match.group(2).lower()
            current_table_line = line_num
            current_columns = []
            current_enums = {}
            in_create = True
            continue

        if in_create and stripped.startswith(");"):
            if current_table:
                _store_table(gt, current_table, current_table_line,
                             current_columns, current_enums, is_ch)
            current_table = None
            in_create = False
            continue

        if in_create and current_table:
            col_match = re.match(r"\s*(\w+)\s+\w+", stripped)
            if col_match:
                col_name = col_match.group(1).lower()
                if col_name not in _SKIP_COL_KEYWORDS:
                    current_columns.append(col_name)
                    enum_match = re.search(r"--\s*(.+)$", stripped)
                    if enum_match:
                        comment = enum_match.group(1).strip()
                        values = [v.strip().strip("'\"") for v in comment.split(",")]
                        if (len(values) >= 2
                                and all(re.match(r"^[\w/\s]+$", v) for v in values)):
                            current_enums[col_name] = [v.strip() for v in values]

    if current_table:
        _store_table(gt, current_table, current_table_line,
                     current_columns, current_enums, is_ch)


def _store_table(gt: DDLGroundTruth, name: str, line: int,
                 cols: list[str], enums: dict, is_ch: bool):
    gt.tables[name] = cols
    gt.table_lines[name] = line
    if enums:
        gt.enum_comments[name] = enums
    if is_ch:
        gt.ch_table_count += 1
        gt.ch_tables.add(name)
    else:
        gt.pg_table_count += 1
        gt.pg_tables.add(name)
    if "valid_from" in cols and "valid_to" in cols:
        gt.bitemporal_tables.add(name)
    if "created_at" in cols and "updated_at" in cols:
        gt.audit_tables.add(name)


# ── Scoring Ground Truth ────────────────────────────────────────────────────

@dataclass
class ScoringGroundTruth:
    area_count: int = 0
    item_count: int = 0
    sub_item_count: int = 0
    area_names: list[str] = field(default_factory=list)
    item_names: list[str] = field(default_factory=list)
    item_types: dict[str, int] = field(default_factory=dict)


def extract_scoring_ground_truth(config_path: Path) -> ScoringGroundTruth:
    gt = ScoringGroundTruth()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    meta = data.get("metadata", {})
    gt.area_count = meta.get("total_areas", 0)
    gt.item_count = meta.get("total_items", 0)
    gt.sub_item_count = meta.get("total_sub_items", 0)
    gt.item_types = meta.get("item_type_counts", {})
    for area in data.get("areas", []):
        gt.area_names.append(area["name"])
        for item in area.get("items", []):
            gt.item_names.append(item["name"])
    if gt.area_count == 0:
        gt.area_count = len(gt.area_names)
    if gt.item_count == 0:
        gt.item_count = len(gt.item_names)
    return gt


# ── Scoring Weights Ground Truth ────────────────────────────────────────────

@dataclass
class WeightsGroundTruth:
    weight_keys: set[str] = field(default_factory=set)
    total_keys: int = 0


def extract_weights_ground_truth(weights_path: Path) -> WeightsGroundTruth:
    gt = WeightsGroundTruth()
    data = json.loads(weights_path.read_text(encoding="utf-8"))
    gt.weight_keys = set(data.keys())
    gt.total_keys = len(gt.weight_keys)
    return gt


# ── Computation Rules Ground Truth ──────────────────────────────────────────

@dataclass
class ComputationGroundTruth:
    area_names: list[str] = field(default_factory=list)
    item_names: list[str] = field(default_factory=list)
    item_types: set[str] = field(default_factory=set)


def extract_computation_ground_truth(rules_path: Path) -> ComputationGroundTruth:
    gt = ComputationGroundTruth()
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    for area in data:
        gt.area_names.append(area.get("area", ""))
        for item in area.get("items", []):
            gt.item_names.append(item.get("name", ""))
            gt.item_types.add(item.get("type", ""))
    return gt


# ── Service Ground Truth ────────────────────────────────────────────────────

@dataclass
class ServiceGroundTruth:
    services: dict[str, dict] = field(default_factory=dict)
    total_operations: int = 0


def extract_service_ground_truth(contracts_path: Path) -> ServiceGroundTruth:
    gt = ServiceGroundTruth()
    text = contracts_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    current_service: "str | None" = None
    current_data: dict = {}

    for line in lines:
        svc_match = re.match(r"^##\s+(\d+)\.\s+(.+)$", line)
        if svc_match:
            if current_service:
                gt.services[current_service] = current_data
            current_service = svc_match.group(2).strip()
            current_data = {"phase": None, "directory": None, "operations": []}
            continue

        if current_service:
            phase_match = re.match(r"\*\*Phase:\*\*\s*(\d+)", line)
            if phase_match:
                current_data["phase"] = int(phase_match.group(1))

            dir_match = re.match(r"\*\*Directory:\*\*\s*`([^`]+)`", line)
            if dir_match:
                current_data["directory"] = dir_match.group(1)

            op_match = re.match(r"\|\s*`(\w+)`\s*\|", line)
            if op_match:
                op_name = op_match.group(1)
                if op_name != "Operation":
                    current_data["operations"].append(op_name)
                    gt.total_operations += 1

    if current_service:
        gt.services[current_service] = current_data

    return gt


# ── Skeleton Ground Truth ───────────────────────────────────────────────────

@dataclass
class SkeletonGroundTruth:
    paths: set[str] = field(default_factory=set)
    service_dirs: dict[str, str] = field(default_factory=dict)
    ellipsis_dirs: set[str] = field(default_factory=set)


def extract_skeleton_ground_truth(skeleton_path: Path) -> SkeletonGroundTruth:
    gt = SkeletonGroundTruth()
    text = skeleton_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    tree_match = re.search(
        r"## 2\. Repository Structure\s*\n```\n(.*?)```", text, re.DOTALL)
    if not tree_match:
        return gt

    tree_text = tree_match.group(1)
    path_stack: list[str] = []

    for tline in tree_text.split("\n"):
        if not tline.strip():
            continue
        if tline.strip() == "/":
            path_stack = [""]
            continue

        # Measure depth by counting groups of 4 characters in leading tree chars
        leading = re.match(r"^([\s│]*)", tline)
        depth = len(leading.group(1).replace("│", " ")) // 4 if leading else 0

        name_match = re.search(r"[├└─][├└─\s]*(.+?)(?:\s{2,}#.*)?$", tline)
        if not name_match:
            continue
        name = name_match.group(1).strip().rstrip("/")
        if name == "...":
            parent_path = "/".join(p for p in path_stack[:depth] if p)
            if parent_path:
                gt.ellipsis_dirs.add(parent_path)
            continue

        path_stack = path_stack[:depth + 1]
        if len(path_stack) <= depth:
            path_stack.extend([""] * (depth + 1 - len(path_stack)))
        path_stack[depth] = name

        full_path = "/".join(p for p in path_stack if p)
        gt.paths.add(full_path)

    # Parse services table
    svc_pattern = re.compile(r"\|\s*\d+\s*\|\s*([^|]+)\|\s*`([^`]+)`\s*\|")
    for line in lines:
        m = svc_pattern.match(line)
        if m:
            gt.service_dirs[m.group(1).strip()] = m.group(2).strip()

    return gt


# ── Onramp Ground Truth ─────────────────────────────────────────────────────

@dataclass
class OnrampGroundTruth:
    ingestion_types: list[str] = field(default_factory=list)
    resolution_options: list[str] = field(default_factory=list)


def extract_onramp_ground_truth(onramp_path: Path) -> OnrampGroundTruth:
    gt = OnrampGroundTruth()
    text = onramp_path.read_text(encoding="utf-8")

    for m in re.finditer(r"`(file_import|api_pull|manual_capture|public_data)`", text):
        val = m.group(1)
        if val not in gt.ingestion_types:
            gt.ingestion_types.append(val)

    res_match = re.search(r"Resolution options:\s*`([^`]+)`(?:,\s*`([^`]+)`)*", text)
    if res_match:
        gt.resolution_options = re.findall(
            r"`(\w+)`", text[res_match.start():res_match.end()])

    return gt


# ── Shared Types Ground Truth ───────────────────────────────────────────────

@dataclass
class SharedTypesGroundTruth:
    total_models: int = 0
    total_fields: int = 0
    module_names: list[str] = field(default_factory=list)


def extract_shared_types_ground_truth(path: Path) -> SharedTypesGroundTruth:
    gt = SharedTypesGroundTruth()
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Total models:\*\*\s*(\d+)", text)
    if m:
        gt.total_models = int(m.group(1))
    m = re.search(r"\*\*Total fields:\*\*\s*(\d+)", text)
    if m:
        gt.total_fields = int(m.group(1))
    for m in re.finditer(r"^## (\w+)", text, re.MULTILINE):
        gt.module_names.append(m.group(1))
    return gt


# ── Spec1 Ground Truth ─────────────────────────────────────────────────────

@dataclass
class Spec1GroundTruth:
    requirement_ids: list[str] = field(default_factory=list)  # M1..M30, S1..S7


def extract_spec1_ground_truth(spec_path: Path) -> Spec1GroundTruth:
    gt = Spec1GroundTruth()
    text = spec_path.read_text(encoding="utf-8")
    for m in re.finditer(r"\*\*([MS]\d+)\.", text):
        rid = m.group(1)
        if rid not in gt.requirement_ids:
            gt.requirement_ids.append(rid)
    return gt


# ── PASS 1: DDL Name Validation ─────────────────────────────────────────────

_FILE_EXTENSIONS = frozenset({
    "md", "mdc", "json", "py", "sql", "html", "yml", "yaml", "toml",
    "lock", "txt", "csv", "tsx", "ts", "js", "css", "ini", "cfg",
})

_NON_TABLE_WORDS = frozenset({
    "datetime", "dict", "list", "tuple", "set", "any", "str", "int",
    "float", "bool", "none", "type", "optional", "self", "cls",
})

_TBL_COL_PAT = re.compile(r"`([a-z_][a-z0-9_]*)\.([a-z_][a-z0-9_]*)`")


def pass_1_ddl_names(report: ValidationReport, ddl_gt: DDLGroundTruth,
                     files: list[Path]):
    all_tables = set(ddl_gt.tables.keys())

    skip_files = {
        _gt_path("specs/platform/Database_Schema_Specification.md").resolve(),
        _gt_path("specs/platform/Shared_Type_Definitions.md").resolve(),
        # spec_1 uses area.item notation (vacancy.turn_cycle), not table.column
        _gt_path("specs/platform/spec_1_multifamily_property_assessment_platform.md").resolve(),
    }

    for fpath in files:
        if fpath.resolve() in skip_files:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in _TBL_COL_PAT.finditer(line):
                tbl, col = m.group(1), m.group(2)
                if col in _FILE_EXTENSIONS or tbl in _NON_TABLE_WORDS:
                    continue
                report.check()
                if tbl not in all_tables:
                    report.error("DDL Names", rel, i,
                                 f"Table `{tbl}` not found in DDL",
                                 f"Referenced as `{tbl}.{col}`")
                elif col not in ddl_gt.tables[tbl]:
                    report.error("DDL Names", rel, i,
                                 f"Column `{col}` not found on table `{tbl}`",
                                 f"Available: {', '.join(ddl_gt.tables[tbl][:10])}...")


def pass_1b_enum_values(report: ValidationReport, ddl_gt: DDLGroundTruth,
                        files: list[Path]):
    ddl_file = _gt_path("specs/platform/Database_Schema_Specification.md").resolve()

    known_enums: dict[str, tuple[str, list[str]]] = {}
    for tbl, col_enums in ddl_gt.enum_comments.items():
        for col, values in col_enums.items():
            known_enums[f"{tbl}.{col}"] = (tbl, values)

    for fpath in files:
        if fpath.resolve() == ddl_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))

        for i, line in enumerate(text.split("\n"), 1):
            # Look for lines that cite role enum values
            if "role" not in line.lower():
                continue
            if not re.search(r"`(?:admin|consultant|analyst|viewer|client)", line):
                continue
            role_vals = re.findall(
                r"`(admin|consultant|analyst|client_viewer|client_user|viewer)`",
                line)
            if len(role_vals) < 2:
                continue
            if "user_account.role" not in known_enums:
                continue
            report.check()
            ddl_vals = set(known_enums["user_account.role"][1])
            cite_vals = set(role_vals)
            if cite_vals != ddl_vals:
                report.error("Enum Values", rel, i,
                             "Role enum mismatch",
                             f"Cited: {sorted(cite_vals)}\n"
                             f"  DDL (user_account.role): {sorted(ddl_vals)}")


# ── PASS 2: Line Number Validation ──────────────────────────────────────────

def pass_2_line_numbers(report: ValidationReport, files: list[Path]):
    # `DocName.md` close to line(s) N
    line_ref_pat = re.compile(
        r"`([^`]+\.(?:md|mdc|json))`"
        r"[^`\n]{0,60}?"
        r"\blines?\s+(\d+)(?:\s*[-–]\s*(\d+))?",
        re.IGNORECASE)

    paren_line_pat = re.compile(
        r"`([^`]+\.(?:md|mdc|json))`"
        r"[^(]{0,30}?"
        r"\(lines?\s+(\d+)(?:\s*[-–]\s*(\d+))?\)",
        re.IGNORECASE)

    spec1_line_pat = re.compile(
        r"(?:spec_1|`spec_1`)"
        r"[^`\n]{0,40}?"
        r"\(line\s+(\d+)\)",
        re.IGNORECASE)

    file_length_cache: dict[str, int] = {}

    def get_file_length(doc_name: str) -> tuple:
        if doc_name in file_length_cache:
            return (True, file_length_cache[doc_name])
        target = resolve_doc(doc_name)
        if not target or not target.exists():
            return (False, 0)
        length = len(target.read_text(encoding="utf-8").split("\n"))
        file_length_cache[doc_name] = length
        return (True, length)

    seen: set[tuple] = set()

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for pat in [line_ref_pat, paren_line_pat]:
                for m in pat.finditer(line):
                    doc_name = m.group(1)
                    line_start = int(m.group(2))
                    line_end = int(m.group(3)) if m.group(3) else line_start

                    found, total = get_file_length(doc_name)
                    if not found:
                        continue

                    key = (rel, i, doc_name, line_start)
                    if key in seen:
                        continue
                    seen.add(key)
                    report.check()

                    if line_start > total:
                        report.error("Line Numbers", rel, i,
                                     f"Line {line_start} out of range for "
                                     f"`{doc_name}` ({total} lines)", "")
                    if line_end > total and line_end != line_start:
                        report.error("Line Numbers", rel, i,
                                     f"Line {line_end} out of range for "
                                     f"`{doc_name}` ({total} lines)", "")

            for m in spec1_line_pat.finditer(line):
                line_start = int(m.group(1))
                found, total = get_file_length("spec_1")
                if not found:
                    continue
                key = (rel, i, "spec_1", line_start)
                if key in seen:
                    continue
                seen.add(key)
                report.check()
                if line_start > total:
                    report.error("Line Numbers", rel, i,
                                 f"spec_1 line {line_start} out of range "
                                 f"({total} lines)", "")


# ── PASS 3: Count Validation ────────────────────────────────────────────────

def pass_3_counts(report: ValidationReport, ddl_gt: DDLGroundTruth,
                  scoring_gt: ScoringGroundTruth, service_gt: ServiceGroundTruth,
                  shared_gt: SharedTypesGroundTruth,
                  weights_gt: WeightsGroundTruth,
                  comp_gt: ComputationGroundTruth, files: list[Path]):
    specific_patterns = [
        (re.compile(r"(\d+)\s+(?:PostgreSQL|PG)\s+tables", re.IGNORECASE),
         "PG tables", ddl_gt.pg_table_count),
        (re.compile(r"ClickHouse\s+Total[^|]*\|\s*\*?\*?(\d+)", re.IGNORECASE),
         "CH total tables", ddl_gt.ch_table_count),
        # Aggregate scoring triple: "12 areas, 65 items, 315 sub-items"
        (re.compile(r"(\d+)\s+areas,\s*\d+\s+items,\s*\d+\s+sub", re.IGNORECASE),
         "scoring areas", scoring_gt.area_count),
        (re.compile(r"\d+\s+areas,\s*(\d+)\s+items,\s*\d+\s+sub", re.IGNORECASE),
         "scoring items", scoring_gt.item_count),
        (re.compile(r"\d+\s+areas,\s*\d+\s+items,\s*(\d+)\s+sub[_-]?items",
                    re.IGNORECASE),
         "scoring sub-items", scoring_gt.sub_item_count),
        (re.compile(r"\*?\*?[Tt]otal\s+models\*?\*?[:\s]*\*?\*?\s*(\d+)"),
         "models", shared_gt.total_models),
        (re.compile(r"\*?\*?[Tt]otal\s+fields\*?\*?[:\s]*\*?\*?\s*(\d+)"),
         "fields", shared_gt.total_fields),
    ]

    total_tables_pat = re.compile(r"(\d+)\s+total\s+tables\b", re.IGNORECASE)
    total_table_count = ddl_gt.pg_table_count + ddl_gt.ch_table_count

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for pat, entity_name, expected in specific_patterns:
                for m in pat.finditer(line):
                    try:
                        claimed = int(m.group(1))
                    except (IndexError, ValueError):
                        continue
                    if claimed <= 2:
                        continue
                    report.check()
                    if claimed != expected:
                        report.error("Counts", rel, i,
                                     f"Claims {claimed} {entity_name}, "
                                     f"actual is {expected}", "")

            for m in total_tables_pat.finditer(line):
                claimed = int(m.group(1))
                if claimed >= 50:
                    report.check()
                    if claimed != total_table_count:
                        report.error("Counts", rel, i,
                                     f"Claims {claimed} total tables, "
                                     f"actual is {total_table_count}", "")

    # Cross-source consistency: scoring_config vs computation_rules
    report.check()
    if len(comp_gt.item_names) != scoring_gt.item_count:
        report.error("Counts", "Computation_Rules_DATA.json", 0,
                     f"Computation rules has {len(comp_gt.item_names)} items, "
                     f"scoring_config has {scoring_gt.item_count}",
                     "These two source files should agree on item count")

    report.check()
    if len(comp_gt.area_names) != scoring_gt.area_count:
        report.error("Counts", "Computation_Rules_DATA.json", 0,
                     f"Computation rules has {len(comp_gt.area_names)} areas, "
                     f"scoring_config has {scoring_gt.area_count}",
                     "These two source files should agree on area count")

    report.check()
    if weights_gt.total_keys == 0:
        report.error("Counts", "Scoring_Weights_Final_Update.json", 0,
                     "Weights file has 0 keys", "")


# ── PASS 4: File Path Validation ────────────────────────────────────────────

def pass_4_file_paths(report: ValidationReport, skeleton_gt: SkeletonGroundTruth,
                      files: list[Path]):
    """Cross-check src/ file paths against the project skeleton tree.

    For every `src/...` path with a file extension referenced in any doc
    (outside the skeleton itself), check whether that exact path exists in
    the skeleton. If the path is NOT in the skeleton but a similar path
    (same parent dir, different leaf name) IS, flag it as a mismatch.
    If the parent directory itself isn't in the skeleton, skip it (the
    skeleton uses '...' to abbreviate; we can't validate unknown subtrees).
    """
    known_paths = skeleton_gt.paths
    if not known_paths:
        return

    # Build parent-dir -> set of full paths mapping
    dir_to_files: dict[str, set[str]] = {}
    for p in known_paths:
        parts = p.rsplit("/", 1)
        if len(parts) == 2 and "." in parts[1]:
            dir_to_files.setdefault(parts[0], set()).add(p)

    path_pat = re.compile(
        r"`((?:src|docker|db|tests|codegen|\.github|\.cursor|docs|frontend)"
        r"/[a-zA-Z0-9_./-]+\.\w+)`")

    skeleton_file = _gt_path("specs/platform/Project_Skeleton_Specification.md").resolve()

    for fpath in files:
        if fpath.resolve() == skeleton_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in path_pat.finditer(line):
                cited = m.group(1).rstrip("/")
                if "**" in cited or "<" in cited or "*" in cited:
                    continue

                parts = cited.rsplit("/", 1)
                if len(parts) != 2:
                    continue
                parent_dir, leaf = parts
                if "." not in leaf:
                    continue

                # Only validate if the parent dir has known files in skeleton
                if parent_dir not in dir_to_files:
                    continue

                # Skip dirs where skeleton uses '...' (unlisted files expected)
                if parent_dir in skeleton_gt.ellipsis_dirs:
                    continue

                report.check()
                if cited not in known_paths:
                    siblings = dir_to_files[parent_dir]
                    report.error("File Paths", rel, i,
                                 f"Path `{cited}` not in skeleton",
                                 f"Skeleton has in {parent_dir}/: "
                                 f"{', '.join(sorted(s.rsplit('/', 1)[1] for s in siblings))}")


# ── PASS 5: Operation Name Validation ───────────────────────────────────────

_OP_PREFIX_PAT = re.compile(
    r"`((?:check_|get_|create_|update_|delete_|list_|compute_|score_|compile_|"
    r"detect_|render_|export_|simulate_|refresh_|build_|resolve_|enforce_|"
    r"register_|upload_|parse_|apply_|finalize_|configure_|run_)\w+)`")


def pass_5_operations(report: ValidationReport, service_gt: ServiceGroundTruth,
                      files: list[Path]):
    all_ops: set[str] = set()
    for svc_data in service_gt.services.values():
        all_ops.update(svc_data["operations"])

    contracts_file = _gt_path("specs/platform/Service_Interface_Contracts.md").resolve()

    target_files = [
        f for f in files
        if (f.suffix == ".mdc" or f.name == "Implementation_Tasks.md")
        and f.resolve() != contracts_file
    ]

    for fpath in target_files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in _OP_PREFIX_PAT.finditer(line):
                op = m.group(1)
                report.check()
                if op not in all_ops:
                    report.error("Operations", rel, i,
                                 f"Operation `{op}` not in "
                                 f"Service_Interface_Contracts.md",
                                 f"Known: {sorted(all_ops)[:15]}...")


# ── PASS 6: Document Reference Validation ───────────────────────────────────

_INFRA_FILES = frozenset({
    "__init__.py", "conftest.py", "env.py", "alembic.ini", "ci.yml",
    "deploy.yml", "next.config.js", "package.json", "tsconfig.json",
    "tailwind.config.ts", ".gitignore", "pyproject.toml", "uv.lock",
})


def pass_6_doc_refs(report: ValidationReport, spec1_gt: Spec1GroundTruth,
                    files: list[Path]):
    doc_ref_pat = re.compile(r"`([A-Za-z0-9_-]+\.(?:md|mdc|json|html))`")
    adr_ref_pat = re.compile(r"`?(ADR-\d{3})`?")
    req_id_pat = re.compile(r"\b([MS]\d{1,2})\b")
    valid_req_ids = set(spec1_gt.requirement_ids)

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in doc_ref_pat.finditer(line):
                doc_name = m.group(1)
                if doc_name in _INFRA_FILES:
                    continue
                report.check()
                target = resolve_doc(doc_name)
                if not target or not target.exists():
                    report.error("Doc Refs", rel, i,
                                 f"Document `{doc_name}` not found",
                                 f"Searched aliases and filesystem under {ROOT}")

            for m in adr_ref_pat.finditer(line):
                adr = m.group(1)
                report.check()
                target = resolve_doc(adr)
                if not target or not target.exists():
                    report.error("Doc Refs", rel, i,
                                 f"ADR `{adr}` not found",
                                 f"Expected at docs/adrs/{adr}-*.md")

            # Requirement ID references (M1, S3, etc.)
            if re.search(r"spec_1|§\d|requirement", line, re.IGNORECASE):
                for m in req_id_pat.finditer(line):
                    rid = m.group(1)
                    if valid_req_ids and rid not in valid_req_ids:
                        report.check()
                        report.error("Doc Refs", rel, i,
                                     f"Requirement `{rid}` not found in spec_1",
                                     f"Valid IDs: M1-M30, S1-S7")


# ── PASS 7: Enum Consistency Validation ─────────────────────────────────────

def pass_7_enum_consistency(report: ValidationReport, ddl_gt: DDLGroundTruth,
                           onramp_gt: OnrampGroundTruth, files: list[Path]):
    ddl_enums: dict[str, list[str]] = {}
    for tbl, col_enums in ddl_gt.enum_comments.items():
        for col, values in col_enums.items():
            ddl_enums[f"{tbl}.{col}"] = values

    # --- Resolution options ---
    resolution_citations: list[tuple[str, int, list[str]]] = []
    resolution_pat = re.compile(
        r"(?:resolution\s+options?|resolutions?)\s*:?\s*"
        r"((?:`\w+`(?:\s*,\s*`\w+`)*)+)", re.IGNORECASE)

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        for i, line in enumerate(text.split("\n"), 1):
            for m in resolution_pat.finditer(line):
                vals = re.findall(r"`(\w+)`", m.group(1))
                if vals:
                    resolution_citations.append((rel, i, vals))

    if len(resolution_citations) >= 2:
        canonical = (set(onramp_gt.resolution_options)
                     if onramp_gt.resolution_options
                     else set(resolution_citations[0][2]))
        for rel, line_num, vals in resolution_citations:
            report.check()
            if set(vals) != canonical:
                report.error("Enum Consistency", rel, line_num,
                             "Resolution options mismatch",
                             f"Cited: {sorted(vals)}\n"
                             f"  Canonical: {sorted(canonical)}")

    # --- Role enum ---
    role_citations: list[tuple[str, int, list[str]]] = []
    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        for i, line in enumerate(text.split("\n"), 1):
            if "role" not in line.lower():
                continue
            if not re.search(r"`(?:admin|consultant|analyst|viewer|client)", line):
                continue
            role_vals = re.findall(
                r"`(admin|consultant|analyst|client_viewer|client_user|viewer)`",
                line)
            if len(role_vals) >= 2:
                role_citations.append((rel, i, role_vals))

    ddl_roles = set(ddl_enums.get("user_account.role", []))
    if ddl_roles:
        for rel, line_num, vals in role_citations:
            report.check()
            if set(vals) != ddl_roles:
                report.error("Enum Consistency", rel, line_num,
                             "Role enum mismatch with DDL",
                             f"Cited: {sorted(set(vals))}\n"
                             f"  DDL (user_account.role): {sorted(ddl_roles)}")


# ── PASS 8: Phase & Directory Consistency ──────────────────────────────────


def _svc_name_match(cited: str, canonical_set: "set[str]") -> bool:
    cited_lower = cited.lower().strip()
    for c in canonical_set:
        c_lower = c.lower()
        if cited_lower == c_lower:
            return True
        if cited_lower in c_lower or c_lower in cited_lower:
            return True
        cited_words = set(re.findall(r"\w+", cited_lower))
        canon_words = set(re.findall(r"\w+", c_lower))
        if cited_words and len(cited_words) >= 2 and cited_words.issubset(canon_words):
            return True
    return False


def pass_8_phase_consistency(report: ValidationReport,
                             service_gt: ServiceGroundTruth,
                             skeleton_gt: SkeletonGroundTruth,
                             files: list[Path]):
    canonical_phase: dict[str, int] = {}
    canonical_dir: dict[str, str] = {}
    phase_to_svcs: dict[int, "set[str]"] = {}
    for svc_name, svc_data in service_gt.services.items():
        if svc_data["phase"] is not None:
            canonical_phase[svc_name] = svc_data["phase"]
            phase_to_svcs.setdefault(svc_data["phase"], set()).add(svc_name)
        if svc_data["directory"]:
            canonical_dir[svc_name] = svc_data["directory"].rstrip("/")

    roadmap = _gt_path("planning/Deployment_Roadmap.md")
    if roadmap.exists():
        text = roadmap.read_text(encoding="utf-8")
        rel = "Deployment_Roadmap.md"
        lines_list = text.split("\n")
        in_phase_table = False
        for i, line in enumerate(lines_list, 1):
            if "|" in line and "Phase" in line and "Services Built" in line:
                in_phase_table = True
                continue
            if in_phase_table and line.strip().startswith("|---"):
                continue
            if in_phase_table and not line.strip().startswith("|"):
                in_phase_table = False
                continue
            if in_phase_table:
                m = re.match(r"\|\s*(\d)\s*\|\s*([^|]+)\|", line)
                if m:
                    phase_num = int(m.group(1))
                    svc_text = m.group(2).strip()
                    cited_services = [s.strip() for s in svc_text.split(",")]
                    canonical = phase_to_svcs.get(phase_num, set())
                    for cited_svc in cited_services:
                        if not cited_svc:
                            continue
                        report.check()
                        if not _svc_name_match(cited_svc, canonical):
                            report.error("Phase Consistency", rel, i,
                                         f"Phase {phase_num} cites `{cited_svc}`, "
                                         f"not in Contracts",
                                         f"Contracts phase {phase_num}: "
                                         f"{sorted(canonical)}")

    for skel_name, skel_dir in skeleton_gt.service_dirs.items():
        for canon_name, canon_dir in canonical_dir.items():
            if _svc_name_match(skel_name, {canon_name}):
                report.check()
                skel_leaf = skel_dir.rstrip("/").rsplit("/", 1)[-1]
                canon_leaf = canon_dir.rstrip("/").rsplit("/", 1)[-1]
                if skel_leaf != canon_leaf:
                    report.error("Phase Consistency",
                                 "Project_Skeleton_Specification.md", 0,
                                 f"Service `{skel_name}` directory mismatch",
                                 f"Skeleton: {skel_dir}\n"
                                 f"  Contracts: {canon_dir}")
                break


# ── PASS 9: Service Name & Count ──────────────────────────────────────────


def pass_9_service_consistency(report: ValidationReport,
                               service_gt: ServiceGroundTruth,
                               files: list[Path]):
    expected_count = len(service_gt.services)
    svc_count_pat = re.compile(r"(\d+)\s+services?\b", re.IGNORECASE)
    contracts_file = _gt_path("specs/platform/Service_Interface_Contracts.md").resolve()

    for fpath in files:
        if fpath.resolve() == contracts_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in svc_count_pat.finditer(line):
                claimed = int(m.group(1))
                if 10 <= claimed <= 20:
                    report.check()
                    if claimed != expected_count:
                        report.error("Service Consistency", rel, i,
                                     f"Claims {claimed} services, "
                                     f"Contracts defines {expected_count}", "")


# ── PASS 10: Scoring Name Consistency ────────────────────────────────────


def _normalize_area_name(name: str) -> str:
    return re.sub(r"^\d+\.\s*", "", name).strip()


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def pass_10_scoring_names(report: ValidationReport,
                          scoring_gt: ScoringGroundTruth,
                          comp_gt: ComputationGroundTruth,
                          weights_gt: WeightsGroundTruth):
    config_areas = scoring_gt.area_names
    comp_areas = [_normalize_area_name(a) for a in comp_gt.area_names]

    for idx, (ca, ra) in enumerate(zip(config_areas, comp_areas)):
        report.check()
        if ca.lower() != ra.lower():
            report.error("Scoring Names", "Computation_Rules_DATA.json", 0,
                         f"Area {idx+1} name mismatch",
                         f"scoring_config: '{ca}'\n  computation_rules: '{ra}'")
    if len(config_areas) != len(comp_areas):
        report.check()
        report.error("Scoring Names", "Computation_Rules_DATA.json", 0,
                     f"Area list length mismatch: scoring_config has "
                     f"{len(config_areas)}, computation_rules has "
                     f"{len(comp_areas)}", "")

    config_items = scoring_gt.item_names
    comp_items = comp_gt.item_names

    for idx, (ci, ri) in enumerate(zip(config_items, comp_items)):
        report.check()
        if ci.lower() != ri.lower():
            report.error("Scoring Names", "Computation_Rules_DATA.json", 0,
                         f"Item name mismatch at position {idx+1}",
                         f"scoring_config: '{ci}'\n  computation_rules: '{ri}'")
    if len(config_items) != len(comp_items):
        report.check()
        report.error("Scoring Names", "Computation_Rules_DATA.json", 0,
                     f"Item list length mismatch: scoring_config has "
                     f"{len(config_items)}, computation_rules has "
                     f"{len(comp_items)}", "")

    config_item_slugs = {_slugify(n) for n in config_items}
    for key in weights_gt.weight_keys:
        if not key.startswith("iw__"):
            continue
        parts = key.split("__", 2)
        if len(parts) < 3:
            continue
        item_slug = parts[2]
        report.check()
        if not any(item_slug == slug or item_slug in slug or slug in item_slug
                   for slug in config_item_slugs):
            report.error("Scoring Names", "Scoring_Weights_Final_Update.json", 0,
                         f"Weight key `{key}` has no matching item in scoring_config",
                         f"Item slug: '{item_slug}'")

    config_types = set(scoring_gt.item_types.keys()) if scoring_gt.item_types else set()
    comp_types = comp_gt.item_types
    if config_types and comp_types:
        report.check()
        if config_types != comp_types:
            report.error("Scoring Names", "Computation_Rules_DATA.json", 0,
                         "Input type names differ between sources",
                         f"scoring_config: {sorted(config_types)}\n"
                         f"  computation_rules: {sorted(comp_types)}")


# ── PASS 11: All DDL Enum Values ──────────────────────────────────────────


def pass_11_all_enums(report: ValidationReport, ddl_gt: DDLGroundTruth,
                      files: list[Path]):
    ddl_file = _gt_path("specs/platform/Database_Schema_Specification.md").resolve()

    all_enums: dict[str, list[str]] = {}
    for tbl, col_enums in ddl_gt.enum_comments.items():
        for col, values in col_enums.items():
            all_enums[f"{tbl}.{col}"] = values

    for fpath in files:
        if fpath.resolve() == ddl_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for qual_name, ddl_vals in all_enums.items():
                tbl, col = qual_name.split(".", 1)
                if f"{tbl}.{col}" not in line:
                    continue
                after_ref = line[line.index(f"{tbl}.{col}"):]
                cited_vals = re.findall(r"`([a-z][a-z0-9_]*)`", after_ref)
                ddl_set = {v.strip().lower() for v in ddl_vals}
                cited_vals_clean = [v for v in cited_vals
                                    if v != tbl and v != col and v != qual_name]
                if len(cited_vals_clean) < 2:
                    continue
                cited_set = set(cited_vals_clean)
                extra = cited_set - ddl_set
                if extra:
                    report.check()
                    report.error("All Enums", rel, i,
                                 f"`{qual_name}` cited with values not in DDL",
                                 f"Extra: {sorted(extra)}\n"
                                 f"  DDL: {sorted(ddl_set)}")


# ── PASS 12: Tech Stack Consistency ──────────────────────────────────────

_TECH_CONTRADICTIONS = [
    (re.compile(r"\b(?:use|using|chosen|selected|built with)\s+Django\b", re.IGNORECASE),
     "ADR-002 chose FastAPI, not Django"),
    (re.compile(r"\b(?:use|using|chosen|selected|built with)\s+Flask\b", re.IGNORECASE),
     "ADR-002 chose FastAPI, not Flask"),
    (re.compile(r"\bSQLAlchemy\s+ORM\b", re.IGNORECASE),
     "ADR-003 chose SQLAlchemy Core (not ORM)"),
    (re.compile(r"\b(?:use|using|chosen|selected|built with)\s+SQLModel\b", re.IGNORECASE),
     "ADR-003 chose SQLAlchemy Core, not SQLModel"),
    (re.compile(r"\b(?:use|using|managed by|install with)\s+Poetry\b", re.IGNORECASE),
     "ADR-005 chose uv, not Poetry"),
    (re.compile(r"\b(?:use|using|managed by)\s+conda\b", re.IGNORECASE),
     "ADR-005 chose uv, not conda"),
    (re.compile(r"\bMaterial\s*UI\b", re.IGNORECASE),
     "ADR-009 chose shadcn/ui, not Material UI"),
    (re.compile(r"\bAnt\s*Design\b", re.IGNORECASE),
     "ADR-009 chose shadcn/ui, not Ant Design"),
    (re.compile(r"\b(?:use|using|styled with)\s+Bootstrap\b", re.IGNORECASE),
     "ADR-009 chose Tailwind + shadcn/ui, not Bootstrap"),
]


def pass_12_tech_stack(report: ValidationReport, files: list[Path]):
    adr_dir = (ROOT / "docs" / "adrs").resolve()

    for fpath in files:
        if str(fpath.resolve()).startswith(str(adr_dir)):
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for pat, message in _TECH_CONTRADICTIONS:
                if pat.search(line):
                    report.check()
                    report.error("Tech Stack", rel, i, message,
                                 f"Line: {line.strip()[:120]}")


# ── PASS 13: CH vs PG Attribution ────────────────────────────────────────


def pass_13_db_attribution(report: ValidationReport, ddl_gt: DDLGroundTruth,
                           files: list[Path]):
    ddl_file = _gt_path("specs/platform/Database_Schema_Specification.md").resolve()
    ch_pat = re.compile(r"ClickHouse\s+(?:table\s+)?`(\w+)`", re.IGNORECASE)
    pg_pat = re.compile(r"PostgreSQL\s+(?:table\s+)?`(\w+)`", re.IGNORECASE)

    for fpath in files:
        if fpath.resolve() == ddl_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in ch_pat.finditer(line):
                tbl = m.group(1).lower()
                if tbl in ddl_gt.pg_tables:
                    report.check()
                    report.error("DB Attribution", rel, i,
                                 f"`{tbl}` attributed to ClickHouse "
                                 f"but is a PostgreSQL table", "")

            for m in pg_pat.finditer(line):
                tbl = m.group(1).lower()
                if tbl in ddl_gt.ch_tables:
                    report.check()
                    report.error("DB Attribution", rel, i,
                                 f"`{tbl}` attributed to PostgreSQL "
                                 f"but is a ClickHouse table", "")


# ── PASS 14: Bitemporal & Audit Columns ──────────────────────────────────


def pass_14_bitemporal_audit(report: ValidationReport, ddl_gt: DDLGroundTruth,
                             files: list[Path]):
    ddl_file = _gt_path("specs/platform/Database_Schema_Specification.md").resolve()
    bitemp_claim_pat = re.compile(
        r"`(\w+)`[^`\n]{0,40}(?:bitemporal|valid_from\s*/\s*valid_to)", re.IGNORECASE)
    audit_claim_pat = re.compile(
        r"`(\w+)`[^`\n]{0,40}(?:created_at\s*/\s*updated_at)", re.IGNORECASE)

    for fpath in files:
        if fpath.resolve() == ddl_file:
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in bitemp_claim_pat.finditer(line):
                tbl = m.group(1).lower()
                if tbl in ddl_gt.tables and tbl not in ddl_gt.bitemporal_tables:
                    report.check()
                    report.error("Bitemporal", rel, i,
                                 f"`{tbl}` claimed bitemporal but lacks "
                                 f"valid_from/valid_to in DDL", "")

            for m in audit_claim_pat.finditer(line):
                tbl = m.group(1).lower()
                if tbl in ddl_gt.tables and tbl not in ddl_gt.audit_tables:
                    report.check()
                    report.error("Audit Columns", rel, i,
                                 f"`{tbl}` claimed to have created_at/updated_at "
                                 f"but DDL lacks them", "")


# ── PASS 15: Internal Markdown Links ─────────────────────────────────────


def pass_15_internal_links(report: ValidationReport, files: list[Path]):
    link_pat = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in link_pat.finditer(line):
                target = m.group(2).strip()
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path_part = target.split("#")[0]
                if not path_part:
                    continue
                resolved = (fpath.parent / path_part).resolve()
                resolved_from_root = (ROOT / path_part).resolve()
                if not resolved.exists() and not resolved_from_root.exists():
                    report.check()
                    report.error("Internal Links", rel, i,
                                 f"Broken link: `{target}`",
                                 f"Resolved to neither {resolved} "
                                 f"nor {resolved_from_root}")


# ── PASS 16: Model Count vs DDL Tables ───────────────────────────────────


def pass_16_model_vs_ddl(report: ValidationReport, ddl_gt: DDLGroundTruth,
                         shared_gt: SharedTypesGroundTruth):
    total_tables = ddl_gt.pg_table_count + ddl_gt.ch_table_count
    report.check()
    if shared_gt.total_models != total_tables:
        report.error("Model vs DDL", "Shared_Type_Definitions.md", 0,
                     f"Claims {shared_gt.total_models} models but DDL has "
                     f"{total_tables} tables ({ddl_gt.pg_table_count} PG + "
                     f"{ddl_gt.ch_table_count} CH)", "")

    report.check()
    total_columns = sum(len(cols) for cols in ddl_gt.tables.values())
    if shared_gt.total_fields != total_columns:
        report.error("Model vs DDL", "Shared_Type_Definitions.md", 0,
                     f"Claims {shared_gt.total_fields} fields but DDL has "
                     f"{total_columns} columns", "")


# ── PASS 17: Data Layer Naming ───────────────────────────────────────────


def _clean_layer_name(raw: str) -> str:
    """Extract just the layer name, stripping trailing sentences or qualifiers."""
    name = raw.strip().rstrip("*").strip()
    # Stop at first period that looks like a sentence boundary (not inside parens)
    paren_depth = 0
    for i, ch in enumerate(name):
        if ch == "(":
            paren_depth += 1
        elif ch == ")":
            paren_depth = max(0, paren_depth - 1)
        elif ch == "." and paren_depth == 0 and i > 0:
            name = name[:i].strip()
            break
    return name


def pass_17_data_layers(report: ValidationReport, files: list[Path]):
    layer_pat = re.compile(
        r"Layer\s+([A-D])\s*[-–—:]\s*(.+?)(?:\s*$|\s*\|)", re.IGNORECASE)

    layer_citations: "dict[str, list[tuple[str, int, str]]]" = {}

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in layer_pat.finditer(line):
                layer_id = m.group(1).upper()
                layer_name = _clean_layer_name(m.group(2))
                layer_citations.setdefault(layer_id, []).append(
                    (rel, i, layer_name))

    _AUTHORITATIVE_DOCS = [
        "Database_Schema_Specification.md",
        "spec_1_multifamily_property_assessment_platform.md",
        "Deployment_Roadmap.md",
    ]

    for layer_id, citations in layer_citations.items():
        if len(citations) < 2:
            continue

        # Collect all names from the highest-priority authoritative doc
        canonical_names: set[str] = set()
        canonical_rel = ""
        canonical_display: list[str] = []
        for rel, _ln, nm in citations:
            doc_name = Path(rel).name
            if doc_name in _AUTHORITATIVE_DOCS:
                if not canonical_rel:
                    canonical_rel = rel
                if rel == canonical_rel:
                    canonical_names.add(nm.lower())
                    canonical_display.append(nm)
                break  # only use first authoritative doc found
        # If break didn't fire above, we need a second pass for the case
        # where the first authoritative doc has multiple entries
        if canonical_rel:
            canonical_names.clear()
            canonical_display.clear()
            for rel, _ln, nm in citations:
                if rel == canonical_rel:
                    canonical_names.add(nm.lower())
                    canonical_display.append(nm)

        if not canonical_names:
            canonical_rel = citations[0][0]
            canonical_names = {citations[0][2].lower()}
            canonical_display = [citations[0][2]]

        for idx, (rel, line_num, name) in enumerate(citations):
            if rel == canonical_rel:
                continue
            report.check()
            if name.lower() not in canonical_names:
                canon_str = " / ".join(f"'{d}'" for d in canonical_display)
                report.error("Data Layers", rel, line_num,
                             f"Layer {layer_id} name inconsistency",
                             f"Canonical: {canon_str} "
                             f"in {canonical_rel}\n  Here: '{name}'")


# ── PASS 18: Line Content Spot-Check ─────────────────────────────────────


def pass_18_line_content(report: ValidationReport, files: list[Path]):
    content_ref_pat = re.compile(
        r"`([^`]+\.(?:md|mdc))`\s+(?:lines?\s+)?(\d+)"
        r"[^`\n]{0,50}?"
        r"(?:defines?|contains?|specifies?|describes?|creates?)\s+"
        r"[`\"']?(\w[\w\s/&]+?)(?:[`\"',.\)]|$)",
        re.IGNORECASE)

    file_content_cache: "dict[str, list[str]]" = {}

    def get_lines(doc_name: str) -> "list[str] | None":
        if doc_name in file_content_cache:
            return file_content_cache[doc_name]
        target = resolve_doc(doc_name)
        if not target or not target.exists():
            return None
        result = target.read_text(encoding="utf-8").split("\n")
        file_content_cache[doc_name] = result
        return result

    for fpath in files:
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for m in content_ref_pat.finditer(line):
                doc_name = m.group(1)
                cited_line = int(m.group(2))
                keyword = m.group(3).strip().lower()

                target_lines = get_lines(doc_name)
                if not target_lines:
                    continue
                if cited_line > len(target_lines):
                    continue

                start = max(0, cited_line - 6)
                end = min(len(target_lines), cited_line + 5)
                window = " ".join(target_lines[start:end]).lower()

                key_words = [w for w in keyword.split() if len(w) > 3]
                if not key_words:
                    continue
                report.check()
                if not any(kw in window for kw in key_words):
                    report.error("Line Content", rel, i,
                                 f"Line {cited_line} of `{doc_name}` may not "
                                 f"contain '{keyword}'",
                                 f"Checked lines {start+1}-{end}")


# ── PASS 19: Section Heading References ───────────────────────────────────


def pass_19_section_refs(report: ValidationReport, files: list[Path]):
    spec1_path = _gt_path("specs/platform/spec_1_multifamily_property_assessment_platform.md")
    if not spec1_path.exists():
        return
    spec1_text = spec1_path.read_text(encoding="utf-8")

    heading_pat = re.compile(r"^#{1,4}\s+(?:§\s*)?(\d+(?:\.\d+)*)", re.MULTILINE)
    valid_sections: "set[str]" = set()
    for m in heading_pat.finditer(spec1_text):
        valid_sections.add(m.group(1))
    parents: "set[str]" = set()
    for s in valid_sections:
        parts = s.split(".")
        for j in range(1, len(parts)):
            parents.add(".".join(parts[:j]))
    valid_sections |= parents

    if not valid_sections:
        return

    spec1_section_pat = re.compile(
        r"spec_1[^;§]*§(\d+(?:\.\d+)*)", re.IGNORECASE)

    for fpath in files:
        if fpath.resolve() == spec1_path.resolve():
            continue
        text = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        in_code = False

        for i, line in enumerate(text.split("\n"), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            if "spec_1" not in line.lower():
                continue

            for segment in re.split(r";", line):
                if "spec_1" not in segment.lower():
                    continue
                for m in spec1_section_pat.finditer(segment):
                    section_num = m.group(1)
                    report.check()
                    if section_num not in valid_sections:
                        report.error(
                            "Section Refs", rel, i,
                            f"spec_1 §{section_num} not found in "
                            f"spec_1 headings",
                            f"Valid: {sorted(valid_sections, key=lambda x: [int(p) for p in x.split('.')])[:20]}...")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Documentation Cross-Reference Validator")
    parser.add_argument("--json", action="store_true", dest="json_mode",
                        help="Output JSON error report")
    parser.add_argument("--root", type=Path, default=None,
                        help="Override document root directory (default: parent of codegen/)")
    args = parser.parse_args()

    _init_root(args.root if args.root else Path(__file__).resolve().parent.parent)

    json_mode = args.json_mode

    print("=== DOCUMENTATION CROSS-REFERENCE VALIDATION REPORT ===")
    print(f"Root: {ROOT}\n")

    print("Loading ground truth...")

    ddl_gt = extract_ddl_ground_truth(_gt_path("specs/platform/Database_Schema_Specification.md"))
    print(f"  DDL: {ddl_gt.pg_table_count} PG tables, "
          f"{ddl_gt.ch_table_count} CH tables, "
          f"{sum(len(c) for c in ddl_gt.tables.values())} total columns, "
          f"{len(ddl_gt.bitemporal_tables)} bitemporal, "
          f"{len(ddl_gt.audit_tables)} with audit cols")

    scoring_gt = extract_scoring_ground_truth(_gt_path("config/scoring_config.json"))
    print(f"  Scoring: {scoring_gt.area_count} areas, "
          f"{scoring_gt.item_count} items, "
          f"{scoring_gt.sub_item_count} sub-items")

    weights_gt = extract_weights_ground_truth(
        _gt_path("config/Scoring_Weights_Final_Update.json"))
    print(f"  Weights: {weights_gt.total_keys} keys")

    comp_gt = extract_computation_ground_truth(
        _gt_path("config/Computation_Rules_DATA.json"))
    print(f"  Computation Rules: {len(comp_gt.area_names)} areas, "
          f"{len(comp_gt.item_names)} items, "
          f"{len(comp_gt.item_types)} types")

    service_gt = extract_service_ground_truth(
        _gt_path("specs/platform/Service_Interface_Contracts.md"))
    print(f"  Services: {len(service_gt.services)} services, "
          f"{service_gt.total_operations} operations")

    skeleton_gt = extract_skeleton_ground_truth(
        _gt_path("specs/platform/Project_Skeleton_Specification.md"))
    print(f"  Skeleton: {len(skeleton_gt.paths)} paths in tree")

    onramp_gt = extract_onramp_ground_truth(
        _gt_path("specs/data/Data_Onramp_Specification.md"))
    print(f"  Onramp: {len(onramp_gt.ingestion_types)} ingestion types, "
          f"{len(onramp_gt.resolution_options)} resolution options")

    shared_gt = extract_shared_types_ground_truth(
        _gt_path("specs/platform/Shared_Type_Definitions.md"))
    print(f"  Shared Types: {shared_gt.total_models} models, "
          f"{shared_gt.total_fields} fields, "
          f"{len(shared_gt.module_names)} modules")

    spec1_gt = extract_spec1_ground_truth(
        _gt_path("specs/platform/spec_1_multifamily_property_assessment_platform.md"))
    print(f"  Spec1: {len(spec1_gt.requirement_ids)} requirement IDs")

    print()

    files = get_files_to_scan()
    print(f"Files to scan: {len(files)}\n")

    report = ValidationReport()

    passes = [
        ("PASS 1: DDL Names",
         lambda: (pass_1_ddl_names(report, ddl_gt, files),
                  pass_1b_enum_values(report, ddl_gt, files))),
        ("PASS 2: Line Numbers",
         lambda: pass_2_line_numbers(report, files)),
        ("PASS 3: Counts",
         lambda: pass_3_counts(report, ddl_gt, scoring_gt, service_gt,
                               shared_gt, weights_gt, comp_gt, files)),
        ("PASS 4: File Paths",
         lambda: pass_4_file_paths(report, skeleton_gt, files)),
        ("PASS 5: Operations",
         lambda: pass_5_operations(report, service_gt, files)),
        ("PASS 6: Document References",
         lambda: pass_6_doc_refs(report, spec1_gt, files)),
        ("PASS 7: Enum Consistency",
         lambda: pass_7_enum_consistency(report, ddl_gt, onramp_gt, files)),
        ("PASS 8: Phase & Directory Consistency",
         lambda: pass_8_phase_consistency(report, service_gt, skeleton_gt,
                                          files)),
        ("PASS 9: Service Name & Count",
         lambda: pass_9_service_consistency(report, service_gt, files)),
        ("PASS 10: Scoring Name Consistency",
         lambda: pass_10_scoring_names(report, scoring_gt, comp_gt,
                                        weights_gt)),
        ("PASS 11: All DDL Enums",
         lambda: pass_11_all_enums(report, ddl_gt, files)),
        ("PASS 12: Tech Stack Consistency",
         lambda: pass_12_tech_stack(report, files)),
        ("PASS 13: CH vs PG Attribution",
         lambda: pass_13_db_attribution(report, ddl_gt, files)),
        ("PASS 14: Bitemporal & Audit Columns",
         lambda: pass_14_bitemporal_audit(report, ddl_gt, files)),
        ("PASS 15: Internal Markdown Links",
         lambda: pass_15_internal_links(report, files)),
        ("PASS 16: Model Count vs DDL",
         lambda: pass_16_model_vs_ddl(report, ddl_gt, shared_gt)),
        ("PASS 17: Data Layer Naming",
         lambda: pass_17_data_layers(report, files)),
        ("PASS 18: Line Content Spot-Check",
         lambda: pass_18_line_content(report, files)),
        ("PASS 19: Section Heading References",
         lambda: pass_19_section_refs(report, files)),
    ]

    prev_total = 0
    for name, fn in passes:
        print(f"--- {name} ---")
        fn()
        count = len(report.errors) - prev_total
        print(f"  Errors: {count}")
        prev_total = len(report.errors)

    print()

    if report.errors:
        print("=" * 70)
        print("DETAILED ERRORS")
        print("=" * 70)
        current_pass = ""
        for err in report.errors:
            if err.pass_name != current_pass:
                current_pass = err.pass_name
                print(f"\n--- {current_pass} ---\n")
            print(f"ERROR: {err.file}:{err.line}")
            print(f"  {err.message}")
            if err.detail:
                for dline in err.detail.split("\n"):
                    print(f"  {dline}")
            print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total checks: {report.checks}")
    print(f"Passed: {report.checks - len(report.errors)}")
    print(f"ERRORS: {len(report.errors)}")

    if json_mode and report.errors:
        print("\n--- JSON ---")
        print(json.dumps([
            {"pass": e.pass_name, "file": e.file, "line": e.line,
             "message": e.message, "detail": e.detail}
            for e in report.errors
        ], indent=2))

    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
