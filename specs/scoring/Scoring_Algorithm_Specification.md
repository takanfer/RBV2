# Scoring Algorithm Specification

Formal pseudocode and implementation rules for every scoring method used in the RBv2 scoring engine. This document consolidates algorithmic details from `Scoring_Model_Specification.md`, `Scoring_Thresholds_Calibration.md`, `scoring_config.json`, `Scoring_Model_Workbook.html`, and `Computation_Rules_Workbook.html` into a single implementation-ready reference.

All values in this document are sourced from those files. No values are invented.

---

## 1. Piecewise Linear Interpolation (Data and Comparative Items)

### 1.1 Breakpoint Structure

Every Data-type and Comparative-type item defines four breakpoints that map to fixed score anchors:

| Breakpoint | Score |
|------------|-------|
| Excellent  | 10.0  |
| Good       | 7.5   |
| Concern    | 5.0   |
| Poor       | 2.5   |

Source: `Scoring_Thresholds_Calibration.md` lines 9–17.

### 1.2 Direction

Each item has a **direction** that determines the ordering of breakpoints:

- **Higher is better (↑):** Excellent > Good > Concern > Poor (numerically). Values at or above Excellent = 10.0.
- **Lower is better (↓):** Excellent < Good < Concern < Poor (numerically). Values at or below Excellent = 10.0.
- **Proximity (≈):** Score is based on absolute distance from a target value (1.0 for pricing ratios). Deviation in either direction is penalized.

Source: `Scoring_Thresholds_Calibration.md` lines 19–22.

### 1.3 Interpolation Algorithm

```
FUNCTION score_piecewise_linear(raw_value, direction, excellent, good, concern, poor) -> FLOAT:
    
    # Define ordered breakpoints based on direction
    IF direction == "higher_is_better":
        breakpoints = [(excellent, 10.0), (good, 7.5), (concern, 5.0), (poor, 2.5)]
        # Breakpoints are in descending raw-value order: excellent >= good >= concern >= poor
        
        IF raw_value >= excellent:
            RETURN 10.0
        ELIF raw_value <= poor:
            # Extrapolate below Poor toward 0, clamped at 0
            IF excellent == poor:
                RETURN 0.0
            slope = (2.5 - 0.0) / (poor - (poor - (concern - poor)))
            # Linear extrapolation: score decreases from 2.5 at Poor toward 0
            extrapolated = 2.5 * (raw_value - 0) / poor  # simplified: linear from (0_raw → 0_score) to (poor → 2.5)
            RETURN MAX(0.0, extrapolated)
    
    ELIF direction == "lower_is_better":
        breakpoints = [(excellent, 10.0), (good, 7.5), (concern, 5.0), (poor, 2.5)]
        # Breakpoints are in ascending raw-value order: excellent <= good <= concern <= poor
        
        IF raw_value <= excellent:
            RETURN 10.0
        ELIF raw_value >= poor:
            # Extrapolate above Poor toward 0, clamped at 0
            extrapolated = 2.5 - 2.5 * (raw_value - poor) / (poor - concern)
            RETURN MAX(0.0, extrapolated)
    
    # Interpolate between adjacent breakpoints
    FOR i FROM 0 TO len(breakpoints) - 2:
        (v1, s1) = breakpoints[i]      # higher score end
        (v2, s2) = breakpoints[i + 1]  # lower score end
        
        IF direction == "higher_is_better":
            IF raw_value <= v1 AND raw_value >= v2:
                fraction = (raw_value - v2) / (v1 - v2)
                RETURN s2 + fraction * (s1 - s2)
        ELIF direction == "lower_is_better":
            IF raw_value >= v1 AND raw_value <= v2:
                fraction = (v2 - raw_value) / (v2 - v1)
                RETURN s2 + fraction * (s1 - s2)
    
    # Should not reach here if breakpoints are valid
    RETURN 0.0
```

### 1.4 Boundary Behavior

| Condition | Result |
|-----------|--------|
| Value at exact breakpoint | Returns the breakpoint's score exactly |
| Value between two breakpoints | Linear interpolation between the two adjacent scores |
| Value beyond Excellent (favorable direction) | Clamped at 10.0 |
| Value beyond Poor (unfavorable direction) | Extrapolated linearly toward 0.0, floored at 0.0 |
| All breakpoints identical (degenerate) | Return 10.0 if value matches, 0.0 otherwise |

Source: `Scoring_Thresholds_Calibration.md` lines 13–17 (score ranges), line 17 ("floor at 0").

### 1.5 Proximity Scoring (Method A — Comparative Pricing)

For items where deviation in either direction from a target is penalized (pricing ratios where target = 1.0):

```
FUNCTION score_proximity(raw_ratio, target, excellent_dev, good_dev, concern_dev, poor_dev) -> FLOAT:
    # target is typically 1.0 for pricing ratios
    deviation = ABS(raw_ratio - target)
    
    # Use lower-is-better interpolation on the deviation
    RETURN score_piecewise_linear(deviation, "lower_is_better", excellent_dev, good_dev, concern_dev, poor_dev)
```

Source: `Scoring_Thresholds_Calibration.md` lines 201–220 (Method A). Breakpoints: deviation ≤3% = Excellent, ≤7% = Good, ≤12% = Concern, ≤18% = Poor.

---

## 2. Checklist Scoring (100-Point Budget)

### 2.1 Algorithm

Every checklist item has sub-items that share a 100-point budget. Two sub-item types exist:

**Y/N (Binary):**
```
FUNCTION score_yn(answer: BOOL, point_value: FLOAT) -> FLOAT:
    IF answer == TRUE:
        RETURN point_value
    ELSE:
        RETURN 0.0
```

**Tiered (Multi-level):**
```
FUNCTION score_tiered(observed_tier: STRING, tier_ladder: DICT[STRING -> FLOAT], point_value: FLOAT) -> FLOAT:
    # tier_ladder maps tier names to percentages (0.0 to 1.0)
    # Example: {"Excellent": 1.0, "Good": 0.75, "Fair": 0.50, "Poor": 0.25, "None": 0.0}
    
    IF observed_tier NOT IN tier_ladder:
        RETURN 0.0  # Unknown tier earns nothing
    
    percentage = tier_ladder[observed_tier]
    RETURN point_value * percentage
```

**Checklist item score:**
```
FUNCTION score_checklist_item(sub_items: LIST[SubItem]) -> FLOAT:
    # sub_items is the list of sub-items for this checklist item
    # Each sub_item has: type (yn/tiered), point_value, answer/observed_tier
    
    total_points_earned = 0.0
    
    FOR sub_item IN sub_items:
        IF sub_item.type == "yn":
            total_points_earned += score_yn(sub_item.answer, sub_item.point_value)
        ELIF sub_item.type == "tiered":
            total_points_earned += score_tiered(sub_item.observed_tier, sub_item.tier_ladder, sub_item.point_value)
    
    # Convert 100-point budget to 0-10 score
    score = total_points_earned / 100.0 * 10.0
    RETURN CLAMP(score, 0.0, 10.0)
```

Source: `Scoring_Model_Specification.md` lines 5 (Design Principle 5), 36–39 (sub-types), 39 (formula).

### 2.2 100-Point Budget Invariant

For every checklist item, the sum of all sub-item point values MUST equal exactly 100. This is a structural constraint, not a runtime check — it must be validated at configuration time.

```
FUNCTION validate_checklist_budget(item: ChecklistItem) -> BOOL:
    total = SUM(sub_item.point_value FOR sub_item IN item.sub_items)
    RETURN total == 100.0
```

Source: `Scoring_Model_Specification.md` line 5 (Design Principle 5: "share a 100-point budget").

### 2.3 Tier Ladder Extraction

Tier ladders define the percentage each tier earns. The canonical tier ladders are defined in `Scoring_Model_Workbook.html`. Common patterns observed across items:

**4-tier ladder (most common for condition/quality ratings):**
- Excellent = 100%, Good = 75%, Fair = 50%, Poor = 25%

**4-tier ladder (with Critical):**
- Good = 100%, Fair = 66%, Poor = 33%, Critical = 0%

**Range-based tiers (for quantitative checklist sub-items):**
Each tier maps a value range to a percentage. Example from Conversion Metrics:
- Lead-to-Tour %: ≥50% = 100%, 35-49% = 75%, 20-34% = 50%, <20% = 25%

The exact tier definitions per sub-item are in `Scoring_Model_Workbook.html` and `scoring_config.json`.

### 2.4 Mixed-Type Checklist Items

Some checklist items contain sub-items scored as Data type (e.g., Staffing Stability sub-items are Data-scored within a Checklist item). In these cases:

```
FUNCTION score_data_within_checklist(raw_value, thresholds, point_value) -> FLOAT:
    # Score the raw value using piecewise linear interpolation (0-10)
    item_score = score_piecewise_linear(raw_value, thresholds.direction,
                                         thresholds.excellent, thresholds.good,
                                         thresholds.concern, thresholds.poor)
    # Convert 0-10 score to points earned out of this sub-item's budget
    RETURN (item_score / 10.0) * point_value
```

Source: `Scoring_Model_Specification.md` Area 7 Staffing Stability (lines 421–428: sub-items typed as Data), Area 9 Maintenance Performance (lines 523–532: mix of Tiered and Data).

---

## 3. Comparative Scoring (4 Methods)

### 3.1 Method A — Pricing Proximity

Used for pricing ratio comparisons where deviation from market parity (1.0) in either direction is penalized.

```
FUNCTION score_method_a(subject_value, comp_avg) -> FLOAT:
    ratio = subject_value / comp_avg
    deviation = ABS(ratio - 1.0)
    RETURN score_piecewise_linear(deviation, "lower_is_better", 0.03, 0.07, 0.12, 0.18)
```

Applies to: 7 pricing sub-items (Studio/1-Bed/2-Bed Avg Price and PPSF vs Comps, plus New Leases PPSF vs Market).

Source: `Scoring_Thresholds_Calibration.md` lines 201–220.

### 3.2 Method B — Ratio, Higher is Better

Subject outperforming comps yields higher score.

```
FUNCTION score_method_b(subject_value, comp_avg) -> FLOAT:
    ratio = subject_value / comp_avg
    RETURN score_piecewise_linear(ratio, "higher_is_better", 1.20, 1.00, 0.80, 0.60)
```

Applies to: Amenity Count vs Comps, Mystery Shop Score vs Comps, Resident Services vs Comps, Resident Events vs Comps.

Source: `Scoring_Thresholds_Calibration.md` lines 224–237.

### 3.3 Method C — Point Difference, Higher is Better

For items where the comparison is an additive difference, not a ratio.

**Occupancy vs Comps:**
```
FUNCTION score_occupancy_vs_comps(subject_occ, comp_avg_occ) -> FLOAT:
    diff = subject_occ - comp_avg_occ  # percentage points
    RETURN score_piecewise_linear(diff, "higher_is_better", 3.0, 0.0, -3.0, -6.0)
```

**Reputation Score vs Comps:**
```
FUNCTION score_reputation_vs_comps(subject_score, comp_avg_score) -> FLOAT:
    diff = subject_score - comp_avg_score  # points on 5-point scale
    RETURN score_piecewise_linear(diff, "higher_is_better", 0.5, 0.0, -0.3, -0.7)
```

Source: `Scoring_Thresholds_Calibration.md` lines 240–258.

### 3.4 Method D — Binary with Adoption Context (Resident Mobile App)

The subject is binary (has/doesn't have app). The comp set has a continuous adoption rate. Uses a custom scoring matrix with linear interpolation within ranges.

```
FUNCTION score_method_d(subject_has_app: BOOL, comp_adoption_rate: FLOAT) -> FLOAT:
    IF subject_has_app:
        ranges = [(0.0, 0.20, 10.0, 8.5),   # adoption 0-20%: score 10.0 to 8.5
                  (0.20, 0.50, 8.5, 7.0),    # adoption 20-50%: score 8.5 to 7.0
                  (0.50, 0.80, 7.0, 5.5),    # adoption 50-80%: score 7.0 to 5.5
                  (0.80, 1.00, 5.5, 5.5)]    # adoption 80-100%: score 5.5 (table stakes)
    ELSE:
        ranges = [(0.0, 0.20, 7.0, 7.0),     # adoption 0-20%: score 7.0 (not yet critical)
                  (0.20, 0.50, 4.0, 4.0),    # adoption 20-50%: score 4.0
                  (0.50, 0.80, 2.0, 2.0),    # adoption 50-80%: score 2.0
                  (0.80, 1.00, 0.5, 0.5)]    # adoption 80-100%: score 0.5
    
    FOR (low, high, score_at_low, score_at_high) IN ranges:
        IF comp_adoption_rate >= low AND comp_adoption_rate < high:
            IF high == low:
                RETURN score_at_low
            fraction = (comp_adoption_rate - low) / (high - low)
            RETURN score_at_low + fraction * (score_at_high - score_at_low)
    
    # Edge case: adoption_rate == 1.0
    RETURN ranges[-1][3]
```

Source: `Scoring_Thresholds_Calibration.md` lines 260–282.

---

## 4. Financial Variance Scoring (Area 8)

### 4.1 Variance Calculation

All Area 8 sub-items are scored by comparing actual performance to the owner's stated budget.

```
FUNCTION compute_variance_pct(actual: FLOAT, budget: FLOAT) -> FLOAT:
    IF budget == 0:
        RETURN NULL  # Cannot compute variance against zero budget
    RETURN (actual - budget) / ABS(budget) * 100.0
```

### 4.2 Revenue Items (Higher Actual = Favorable)

Applies to: Gross Potential Rent, Other Income, Effective Gross Income, Net Operating Income, Capital Reserves.

```
FUNCTION score_financial_revenue(actual, budget) -> FLOAT:
    variance_pct = compute_variance_pct(actual, budget)
    IF variance_pct IS NULL:
        RETURN NULL  # Missing data
    # Higher variance is better: +5% = Excellent, 0% = Good, -5% = Concern, -10% = Poor
    RETURN score_piecewise_linear(variance_pct, "higher_is_better", 5.0, 0.0, -5.0, -10.0)
```

### 4.3 Expense Items (Lower Actual = Favorable)

Applies to: Payroll & Benefits, Repairs & Maintenance, Utilities, Marketing & Advertising, Insurance, Real Estate Taxes, Admin / G&A, Contract Services, Management Fee, Total Operating Expenses, Vacancy Loss, Concessions / Loss-to-Lease, Capital Expenditures.

```
FUNCTION score_financial_expense(actual, budget) -> FLOAT:
    variance_pct = compute_variance_pct(actual, budget)
    IF variance_pct IS NULL:
        RETURN NULL  # Missing data
    # Lower variance is better: -5% = Excellent, 0% = Good, +5% = Concern, +10% = Poor
    RETURN score_piecewise_linear(variance_pct, "lower_is_better", -5.0, 0.0, 5.0, 10.0)
```

Source: `Scoring_Thresholds_Calibration.md` lines 113–150 (Financial variance scoring section).

---

## 5. Weighted Rollup

### 5.1 Item-Level Score to Area Score

```
FUNCTION compute_area_score(items: LIST[ScoredItem], item_weights: DICT[STRING -> FLOAT]) -> AreaScore:
    # items: list of scored items in this area, each with a score (0-10) or NULL (missing)
    # item_weights: item_name -> weight (0-100, sum to 100 within area)
    
    weighted_sum = 0.0
    weight_sum = 0.0
    scored_count = 0
    missing_count = 0
    
    FOR item IN items:
        weight = item_weights[item.name]
        
        IF item.score IS NOT NULL:
            weighted_sum += item.score * weight
            weight_sum += weight
            scored_count += 1
        ELSE:
            missing_count += 1
    
    IF weight_sum == 0:
        RETURN AreaScore(score=NULL, coverage=0.0, scored_count=0, missing_count=missing_count)
    
    area_score = weighted_sum / weight_sum
    coverage = weight_sum / SUM(item_weights.values()) * 100.0
    
    RETURN AreaScore(
        score=area_score,
        coverage=coverage,
        scored_count=scored_count,
        missing_count=missing_count
    )
```

Source: `Scoring_Model_Specification.md` lines 43–52 (Rollup section, missing-item exclusion).

### 5.2 Area Scores to Overall Asset Score

```
FUNCTION compute_overall_score(areas: LIST[AreaScore], area_weights: DICT[STRING -> FLOAT]) -> OverallScore:
    # area_weights: area_name -> weight (0-100, sum to 100 across all 12 areas)
    
    weighted_sum = 0.0
    weight_sum = 0.0
    
    FOR area IN areas:
        weight = area_weights[area.name]
        
        IF area.score IS NOT NULL:
            weighted_sum += area.score * weight
            weight_sum += weight
    
    IF weight_sum == 0:
        RETURN OverallScore(score=NULL, coverage=0.0)
    
    overall_score = weighted_sum / weight_sum
    coverage = weight_sum / SUM(area_weights.values()) * 100.0
    
    RETURN OverallScore(score=overall_score, coverage=coverage)
```

### 5.3 Weight Invariants

These must hold at configuration time (validated, not assumed at runtime):

1. All 12 area weights sum to exactly 100%.
2. Within each area, all item weights sum to exactly 100%.
3. Within each checklist item, all sub-item point values sum to exactly 100.

```
FUNCTION validate_weight_structure(config: ScoringConfig) -> LIST[ERROR]:
    errors = []
    
    area_weight_sum = SUM(area.weight FOR area IN config.areas)
    IF ABS(area_weight_sum - 100.0) > 0.01:
        errors.append(f"Area weights sum to {area_weight_sum}, expected 100.0")
    
    FOR area IN config.areas:
        item_weight_sum = SUM(item.weight FOR item IN area.items)
        IF ABS(item_weight_sum - 100.0) > 0.01:
            errors.append(f"Area '{area.name}' item weights sum to {item_weight_sum}, expected 100.0")
        
        FOR item IN area.items:
            IF item.type == "Checklist":
                point_sum = SUM(sub.points FOR sub IN item.sub_items)
                IF ABS(point_sum - 100.0) > 0.01:
                    errors.append(f"Item '{item.name}' sub-item points sum to {point_sum}, expected 100.0")
    
    RETURN errors
```

Source: `Scoring_Model_Specification.md` lines 6 (Design Principle 6: three-level weighting), 46–49 (rollup hierarchy).

### 5.4 Missing Data Handling

Missing items are **excluded** from the weighted average, not scored as zero. The weight of missing items is redistributed proportionally among present items.

This is achieved by dividing by the sum of weights of scored items only (`weight_sum`) rather than by the total possible weight.

Source: `Scoring_Model_Specification.md` line 52 ("Missing items are excluded from the weighted average (not scored as zero). The system tracks coverage percentage per area.").

---

## 6. Composite Item Scoring

### 6.1 Relative to Market (Area 5, Pricing)

This is a checklist item with mixed-type sub-items:

| Sub-item | Type | Points | Scoring Method |
|----------|------|--------|----------------|
| Loss-to-Lease % | Data | 50 | Piecewise linear (↓ lower is better): 2/5/10/20 % |
| New Leases Avg PPSF vs Market | Comparative | 50 | Method A (proximity to 1.0): ±3/7/12/18 % |

The item score is computed as a checklist: each sub-item earns points proportional to its 0-10 score, then total / 100 × 10.

```
FUNCTION score_relative_to_market(loss_to_lease_pct, subject_ppsf, market_ppsf) -> FLOAT:
    # Sub-item 1: Loss-to-Lease (Data, 50 pts)
    ltl_score = score_piecewise_linear(loss_to_lease_pct, "lower_is_better", 2.0, 5.0, 10.0, 20.0)
    ltl_points = (ltl_score / 10.0) * 50.0
    
    # Sub-item 2: PPSF vs Market (Comparative Method A, 50 pts)
    ppsf_score = score_method_a(subject_ppsf, market_ppsf)
    ppsf_points = (ppsf_score / 10.0) * 50.0
    
    total_points = ltl_points + ppsf_points
    RETURN total_points / 100.0 * 10.0
```

Source: `Scoring_Model_Specification.md` lines 375–381 (Relative to Market sub-items).

### 6.2 Vacant Unit Walk Aggregation (Area 10)

Individual units are rated; scores are averaged across all sampled vacant units.

```
FUNCTION score_vacant_walks(unit_ratings: LIST[DICT[STRING -> STRING]]) -> FLOAT:
    # unit_ratings: list of dicts, one per sampled unit
    # Each dict maps sub-item name -> observed tier
    
    IF len(unit_ratings) == 0:
        RETURN NULL  # No units sampled
    
    # Score each unit independently using the checklist algorithm
    unit_scores = []
    FOR unit_rating IN unit_ratings:
        unit_score = score_checklist_item(build_sub_items(unit_rating, VACANT_WALK_CONFIG))
        unit_scores.append(unit_score)
    
    # Average across all sampled units
    RETURN SUM(unit_scores) / len(unit_scores)
```

Source: `Scoring_Model_Specification.md` line 564 ("scores are averaged across all sampled vacant units for each category").

---

## 7. Complete Threshold Reference

All threshold values are sourced from `Scoring_Thresholds_Calibration.md` lines 26–328. The summary table at lines 288–328 lists all 33 threshold sets.

This document does not reproduce the full threshold table — it is defined authoritatively in `Scoring_Thresholds_Calibration.md` and encoded in `scoring_config.json`. Implementors MUST read both source files.

---

## 8. Implementation Notes

### 8.1 Numerical Precision

- All intermediate calculations use floating-point arithmetic (float64 / Python `float`).
- Final scores are rounded to 2 decimal places for display.
- Weight sum validations use a tolerance of 0.01 (not exact equality) to accommodate floating-point representation.

### 8.2 Annualization

Items measured over the assessment date range may need annualization before scoring. Example from `Scoring_Thresholds_Calibration.md` line 191:

> "If the assessment date range is less than 12 months, the computation must annualize the rate before scoring: (rate / months in period) × 12."

This applies to: Eviction Rate (Area 12), and potentially other rate-based items when the assessment period is not 12 months.

### 8.3 Date Range Variable

All date-range-dependent computations use the assessment-level date range variable, not hardcoded periods.

Source: `Scoring_Model_Specification.md` line 25 (Design Principle 9).

---

## Authoritative Sources

- `Scoring_Model_Specification.md` — Scoring structure, areas, items, sub-items, weights, input types
- `Scoring_Thresholds_Calibration.md` — All breakpoint values for Data and Comparative items, scoring methods A-D
- `scoring_config.json` — Machine-readable scoring configuration (12 areas, 65 items, 315 sub-items)
- `Scoring_Model_Workbook.html` — Tier ladder definitions for Tiered sub-items
- `Computation_Rules_Workbook.html` — Data source and computation method per scored item
