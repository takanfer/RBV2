# BADS Edge-Case Rules

Defines the rules for handling edge cases in the Basic Analytic Data Set (BADS) computations: zero denominators, missing data, temporal scoping, annualization, and ambiguous formula resolution.

Every KPI computation must follow these rules. An implementing agent that encounters an edge case not covered here must stop and flag it, not guess.

---

## Sources

- `Basic_Analytic_Data_Set.md` — 124 KPIs, calculations, benchmarks
- `Scoring_Thresholds_Calibration.md` — Threshold values and annualization notes (line 191)
- `Scoring_Algorithm_Specification.md` — Missing data handling in weighted rollup
- `Scoring_Model_Specification.md` — Design Principle 9 (date range variable)
- `Analytical_Engine_Specification.md` — Date range variable definition

---

## 1. Zero Denominator Rules

Many BADS KPIs are ratios. When the denominator is zero, the formula cannot produce a valid number. These rules define what to do.

### General Rule

When a ratio's denominator is zero, the KPI value is `NULL` (missing), not zero, not infinity, not an error. `NULL` KPIs are excluded from scoring via the missing-data rules (see `Scoring_Algorithm_Specification.md` §5.4).

### Specific Cases

| KPI | Denominator | Zero Denominator Meaning | Result |
|-----|-------------|-------------------------|--------|
| Physical Occupancy Rate | Total units | No units exist (invalid property data) | `NULL` + data quality flag |
| Economic Occupancy Rate | Gross Potential Rent (GPR) | GPR is zero (no market rents set) | `NULL` + data quality flag |
| Any Per-Unit metric | Total units | No units | `NULL` + data quality flag |
| Any Per-Unit-Per-Month metric | Total units × months in period | No units or zero-length period | `NULL` |
| Vacancy Rate by Unit Type | Total units of type | Zero units of that type | `NULL` (type doesn't exist at property) |
| Renewal Rate | Expiring leases | No leases expired in period | `NULL` (no renewal opportunity) |
| Application Denial Rate | Total applications | No applications received | `NULL` |
| Controllable Turnover Rate | Total move-outs | No move-outs | `NULL` (no turnover to categorize) |
| Ghost/No-Show Rate | Scheduled tours | No tours scheduled | `NULL` |
| Conversion rates (lead-to-X) | Total leads | No leads | `NULL` |
| Financial variance % | Budget value | Budget is zero for line item | `NULL` + data quality flag |
| Utility Recovery Rate | Gross utility expense | No utility expense | `NULL` |
| Cost Per Lead / Cost Per Lease | Total leads / Total leases | No leads or leases | `NULL` |
| Pet Deposit Adequacy | Average pet damage cost | No pet damage data | `NULL` |
| Acquisition-to-Retention Ratio | Retention cost | No renewal cost data | `NULL` |

### Data Quality Flags

When a denominator is zero for a value that should never be zero (Total Units, GPR), the system should generate a data quality flag indicating likely missing or corrupt source data, in addition to returning `NULL`.

---

## 2. Missing Data Rules

### KPI-Level Missing Data

A KPI is `NULL` when any required input field is missing. Partial computation is not allowed — either all inputs are available and the KPI is computed, or the KPI is `NULL`.

**Exception: Aggregation KPIs.** KPIs that aggregate across a population (e.g., "Average Total Vacant Days") can compute if at least one data point exists. The count of available data points must be tracked.

```
FUNCTION compute_aggregate_kpi(values: LIST[FLOAT | NULL]) -> (FLOAT | NULL, INT):
    non_null = [v for v in values if v is not NULL]
    if len(non_null) == 0:
        return (NULL, 0)
    return (SUM(non_null) / len(non_null), len(non_null))
```

### Scoring Impact

When a KPI feeds a scored item and the KPI is `NULL`:
- The scored item's score is `NULL`
- The item is excluded from the area weighted average (weight redistributed)
- The area's coverage percentage decreases

Source: `Scoring_Algorithm_Specification.md` §5.4.

### Coverage Tracking

The system must track and report:
- Which KPIs were computable vs. `NULL` for each assessment
- Per-area coverage percentage (scored weight / total weight × 100)
- Per-property data completeness (KPIs computed / 124 total)

---

## 3. Temporal Scoping Rules

### Assessment Date Range Variable

All date-range-dependent KPIs use the assessment-level date range variable, set once per engagement. The date range defines the observation window for all temporal calculations.

Source: `Scoring_Model_Specification.md` Design Principle 9, `Analytical_Engine_Specification.md`.

```
assessment.date_range_start: DATE
assessment.date_range_end: DATE
assessment.date_range_months: FLOAT  # derived: (end - start) / 30.44
```

### Rule: No Hardcoded Periods

No computation may hardcode a trailing period (e.g., "trailing 12 months", "last 90 days"). All such periods must be expressed relative to the assessment date range.

### Event Inclusion Rules

| Event Type | Included If |
|-----------|------------|
| Move-out events | Move-out date falls within the assessment date range |
| Lease events | Lease start date falls within the date range |
| Work orders | Date created falls within the date range |
| Financial data | Accounting period falls within the date range |
| Reviews/ratings | Review date within the date range (or most recent as of range end) |
| Staffing snapshots | Snapshot as of date range end |

### Partial Period Handling

When the assessment date range does not align with calendar boundaries (e.g., starts March 15):

- Monthly financial data: prorate the first and last months
- Annual rates: see Annualization rules below
- Cumulative metrics (e.g., total move-outs): include only events within the range
- Point-in-time metrics (e.g., current occupancy): use the state as of the date range end

---

## 4. Annualization Rules

### When to Annualize

Any rate expressed as "annual" or "per year" must be annualized when the assessment period is not 12 months.

Source: `Scoring_Thresholds_Calibration.md` line 191 — "the computation must annualize the rate before scoring: (rate / months in period) × 12."

### Annualization Formula

```
FUNCTION annualize(rate_in_period: FLOAT, period_months: FLOAT) -> FLOAT:
    IF period_months <= 0:
        RETURN NULL
    IF period_months >= 12:
        RETURN rate_in_period  # No annualization needed for 12+ months
    RETURN (rate_in_period / period_months) * 12.0
```

### KPIs Requiring Annualization

| KPI | Original Basis | Annualization |
|-----|---------------|---------------|
| Annual Turnover Rate | Events in period / Total units | annualize(rate, months) |
| Eviction Rate | Evictions in period / Total units | annualize(rate, months) |
| Work Orders Per Unit (Annual) | WOs in period / Total units | annualize(rate, months) |
| Staff Turnover Rate | Departures in period / Total staff | annualize(rate, months) |
| Per-unit annual metrics | Sum in period / Total units | annualize(per_unit, months) |

### Minimum Period for Annualization

Annualization from very short periods produces unreliable extrapolations. The system should flag (but still compute) annualized rates from periods shorter than 3 months, and refuse to annualize from periods shorter than 1 month (return `NULL` instead).

```
FUNCTION safe_annualize(rate_in_period: FLOAT, period_months: FLOAT) -> (FLOAT | NULL, BOOL):
    if period_months < 1.0:
        return (NULL, False)
    annualized = annualize(rate_in_period, period_months)
    is_reliable = period_months >= 3.0
    return (annualized, is_reliable)
```

---

## 5. Ambiguous Formula Resolution

### Revenue Per Unit vs Revenue Per Available Unit

Both KPIs divide by total units and both use total revenue:
- **RPU** = Total Revenue / Total Units / 12
- **RevPAU** = Total Revenue / Total Units / 12 (includes vacancy drag)

Source: `Basic_Analytic_Data_Set.md` lines 100–101. These appear identical in formula. The distinction is conceptual, not computational: RPU is the label used when comparing to asking rents, RevPAU when comparing to GPR. In the implementation, they are the same calculation. Do not create two separate functions — compute once, reference by context.

### Physical-to-Economic Occupancy Gap

The subtraction is Physical − Economic (not the reverse). A positive gap means physical occupancy exceeds economic occupancy, indicating revenue leakage from concessions, bad debt, or other non-rent-generating occupancy.

### Make-Ready Cost: Standard vs Heavy

`Basic_Analytic_Data_Set.md` line 151 cites "$1,500–$3,500" for standard turns and "$3,500–$6,000" for heavy turns. The BADS computation uses all turns equally (no separate standard/heavy calculation). The benchmarks are informational context, not separate thresholds for scoring.

### "Controllable" Classification

The Controllable Turnover Rate (line 156) requires classifying move-out reasons as controllable or uncontrollable. The classification is:

- **Controllable:** maintenance/repairs, management/staff issues, service/amenity dissatisfaction, noise/neighbors, pest issues, parking issues, unit condition, safety concerns
- **Uncontrollable:** job transfer/relocation, home purchase, military deployment, death, lease violation/eviction, roommate changes, relationship changes, proximity to family

This classification must be documented in the audit instrument and consistently applied. The `move_event` table's `reason` field should map to a controlled vocabulary.

### VDOM vs Total Vacant Days

Source: `Basic_Analytic_Data_Set.md` lines 52–66. These overlap but are NOT additive — VDOM is a subset of Total Vacant Days. When computing per-event costs, use each phase's days independently. When computing total vacancy cost, use Total Vacant Days (not the sum of phase costs, which would double-count overlapping phases).

---

## 6. Rounding and Precision

| Context | Rule |
|---------|------|
| Stored KPI values | Float64, no rounding in storage |
| Displayed KPI values | 1 decimal place for percentages, whole numbers for counts/days, 2 decimal places for currency |
| Scoring input | Full precision (no rounding before scoring) |
| Score output | 2 decimal places |
| Weight sums | Validated to 0.01 tolerance |
| Financial values | 2 decimal places (cents) |

---

## 7. Negative Value Rules

Some KPIs can legitimately be negative:

| KPI | Negative Meaning | Valid? |
|-----|-----------------|--------|
| Rent Lift on Turnover | New rent is lower than prior rent | Yes — indicates rent decrease on turnover |
| Revenue Growth (YoY) | Revenue declined year-over-year | Yes |
| NOI Trend | NOI is declining | Yes |
| Financial variance % | Actual below budget (revenue) or above budget (expense) | Yes |
| Physical-to-Economic Gap | Economic occupancy exceeds physical (impossible normally) | Possible data error — flag |

KPIs that cannot be negative by definition (rates, counts, percentages): if a computation produces a negative value, clamp to 0 and generate a data quality flag.

---

## Authoritative Sources

- `Basic_Analytic_Data_Set.md` — KPI definitions and calculations (124 KPIs)
- `Scoring_Thresholds_Calibration.md` — Annualization rule (line 191)
- `Scoring_Algorithm_Specification.md` — Missing data handling
- `Scoring_Model_Specification.md` — Date range variable (Design Principle 9)
