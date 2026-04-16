# Scoring Thresholds Calibration

Defines the specific benchmark values that map raw inputs to 0–10 scores for all Data-type and Comparative-type items. Checklist items (Y/N and Tiered) are scored via the 100-point budget system defined in the Scoring Model Workbook and do not require thresholds in this document.

---

## Scoring Function

All Data and Comparative items use **piecewise linear interpolation** between four breakpoints: **Excellent**, **Good**, **Concern**, and **Poor**. The function produces a continuous 0–10 score.

| Raw value zone | Score range |
|----------------|-------------|
| At or beyond Excellent | 10.0 |
| Between Good and Excellent | 7.5 – 10.0 (interpolated) |
| Between Concern and Good | 5.0 – 7.5 (interpolated) |
| Between Poor and Concern | 2.5 – 5.0 (interpolated) |
| Beyond Poor | 0 – 2.5 (extrapolated, floor at 0) |

**Direction** determines whether higher or lower raw values are favorable:
- **Higher is better (↑):** values ≥ Excellent = 10, values ≤ Poor extrapolate toward 0
- **Lower is better (↓):** values ≤ Excellent = 10, values ≥ Poor extrapolate toward 0
- **Proximity (≈):** values closest to target = 10, deviation in either direction is penalized

---

## Area 1: Vacancy/Occupancy

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Occupancy Rate | ↑ | 97% | 95% | 92% | 88% | % |
| Average Vacant Days | ↓ | 14 | 21 | 30 | 45 | days |
| Aged Vacancy (>60d units) | ↓ | 0% | 1% | 3% | 5% | % of total units |

**Notes:**
- Aged Vacancy is computed as count of units vacant >60 days / total units, then scored as a percentage.
- Occupancy Rate thresholds carried from V6 (`occupancy_rate`). Average Vacant Days adapted from V6 (`vdom_days`).

---

## Area 2: Marketing

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Cost per Lead | ↓ | $30 | $60 | $100 | $175 | $/lead |

**Notes:**
- Thresholds from V6 (`lead_cost_per`). Marketing spend includes paid advertising + platform subscriptions + listing fees + monthly service costs.

---

## Area 5: Pricing

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Loss-to-Lease % | ↓ | 2% | 5% | 10% | 20% | % |
| Concession % of GPR | ↓ | 2% | 4% | 7% | 12% | % |
| Rent Lift on Turnover | ↑ | 5% | 3% | 1% | 0% | % |
| Net Effective vs Asking Gap | ↓ | 1% | 3% | 5% | 8% | % |
| Renewal Rent Increase | ↑ | 5% | 3.5% | 2% | 1% | % |

**Notes:**
- Loss-to-Lease uses comp-derived market rent, not the property's internal rent matrix.
- Rent Lift on Turnover: 0% means no rent increase on turnover, which is the worst case — indicates pricing was already at or above market, or management isn't capturing turnover opportunity.
- Renewal Rent Increase thresholds from V6 (`rent_increase_pct`).
- Concession % counts free rent concessions only (excludes waived fees, deposits).

### Comparative Sub-item: New Leases (12mo) — Avg PPSF vs Market Avg PPSF

See Comparative scoring section below (Pricing Proximity method).

---

## Area 6: Retention & Renewal

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Renewal Rate | ↑ | 65% | 55% | 45% | 30% | % |
| Average Resident Tenure | ↑ | 36 | 24 | 18 | 12 | months |
| Month-to-Month % | ↓ | 5% | 10% | 20% | 30% | % |
| Controllable Turnover Rate | ↓ | 10% | 15% | 25% | 40% | % |
| DNR Rate | ↓ | 5% | 10% | 15% | 25% | % |

**Notes:**
- Renewal Rate and Controllable Turnover thresholds from V6 (`renewal_rate`, `turnover_rate`).
- DNR Rate: >25% means the property is choosing not to renew a quarter of its residents, indicating either poor screening or management problems.

---

## Area 7: Operations

### Standalone Data Items

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Units per Leasing Agent | ↓ | 100 | 150 | 200 | 300 | units/FTE |
| Units per Maintenance Tech | ↓ | 75 | 100 | 150 | 200 | units/FTE |

### Staffing Stability Sub-items

| Sub-item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|----------|-----------|-----------------|------------|----------------|------------|------|
| Staff Turnover Rate | ↓ | 15% | 25% | 40% | 60% | % annual |
| Average Staff Tenure | ↑ | 36 | 24 | 18 | 12 | months |
| PM Tenure | ↑ | 36 | 24 | 12 | 6 | months |
| Open Position Rate | ↓ | 0% | 5% | 10% | 20% | % |

**Notes:**
- Units per Leasing Agent: industry standards suggest 1 agent per 100–150 units is well-staffed. Above 200 indicates understaffing.
- PM Tenure has tighter thresholds than general staff tenure — property manager stability is critical and churn at this level is more damaging.

---

## Area 8: Financials (Variance-Based Scoring)

Financial items are scored against the owner's stated budget/benchmark. The raw input is the **variance percentage**: `(Actual - Budget) / Budget × 100`.

### Revenue Items (higher actual = favorable)

Applies to: Gross Potential Rent, Other Income, Effective Gross Income

| Variance direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Method |
|--------------------|-----------------|------------|----------------|------------|--------|
| Higher is better (↑) | +5% | 0% | -5% | -10% | `scoreHigherIsBetter` on variance % |

*Actual exceeds budget by 5%+ = Excellent. Actual 10%+ below budget = Poor.*

### Expense Items (lower actual = favorable)

Applies to: Payroll & Benefits, Repairs & Maintenance, Utilities, Marketing & Advertising, Insurance, Real Estate Taxes, Admin / G&A, Contract Services, Management Fee, Total Operating Expenses, Vacancy Loss, Concessions / Loss-to-Lease

| Variance direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Method |
|--------------------|-----------------|------------|----------------|------------|--------|
| Lower is better (↓) | -5% | 0% | +5% | +10% | `scoreLowerIsBetter` on variance % |

*Actual is 5%+ under budget = Excellent. Actual 10%+ over budget = Poor.*

### Bottom Line — Net Operating Income (higher actual = favorable)

Uses the Revenue variance pattern: +5% / 0% / -5% / -10%.

### Capital Items

| Sub-item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Notes |
|----------|-----------|-----------------|------------|----------------|------------|-------|
| Capital Expenditures | ↓ | -5% | 0% | +5% | +10% | Expense pattern — under budget is favorable |
| Capital Reserves | ↑ | +5% | 0% | -5% | -10% | Revenue pattern — above target is favorable |

**Notes:**
- All financial scoring compares actual performance against the owner's own stated targets, not industry benchmarks.
- The analytical engine also generates a Simulated Optimal Budget as a Layer 4+ output. That comparison is diagnostic context, not scored.

---

## Area 9: Maintenance & Turnovers

### Maintenance Performance Sub-items

| Sub-item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|----------|-----------|-----------------|------------|----------------|------------|------|
| Work Order Completion Rate | ↑ | 98% | 95% | 90% | 80% | % |
| Avg Work Order Completion Duration | ↓ | 1 | 2 | 5 | 10 | days |
| Callback / Repeat Work Order Rate | ↓ | 2% | 5% | 10% | 20% | % |
| Preventive vs Reactive Ratio | ↑ | 40% | 25% | 15% | 5% | % preventive |

### Turnover Performance Sub-items

| Sub-item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|----------|-----------|-----------------|------------|----------------|------------|------|
| Make-Ready Duration | ↓ | 5 | 7 | 10 | 14 | days |
| Make-Ready Cost | ↓ | $1,500 | $2,500 | $4,000 | $6,000 | $/unit |

**Notes:**
- WO Duration and Make-Ready Duration thresholds from V6 (`wo_resolution_days`, `make_ready_days`).
- Callback Rate thresholds from V6 (`repeat_pct`). Measures same-issue recurrence within the lease term.
- Make-Ready Cost is direct cost only (labor + materials + vendor invoices), excluding overhead and staff time.

---

## Area 12: Collections & Screening

| Item | Direction | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) | Unit |
|------|-----------|-----------------|------------|----------------|------------|------|
| Delinquency Rate | ↓ | 2% | 5% | 10% | 20% | % |
| Bad Debt Write-Off Rate | ↓ | 0.5% | 1.5% | 3% | 5% | % |
| Eviction Rate | ↓ | 1% | 2% | 4% | 8% | % annual |
| Application Denial Rate | ↓ | 10% | 20% | 30% | 50% | % |
| Short-Tenure Turnover Rate | ↓ | 5% | 10% | 20% | 30% | % |

**Notes:**
- Delinquency Rate from V6 (`dq_risk_pct`). Bad Debt from V6 (`bad_debt_pct`).
- Eviction Rate thresholds are calibrated to **annualized** rates. If the assessment date range is less than 12 months, the computation must annualize the rate before scoring: (rate / months in period) × 12.
- Application Denial Rate: very high denial indicates marketing targeting the wrong demographic. Low denial is fine — indicates well-qualified applicant pool.
- Short-Tenure Turnover: any early termination before lease term ends, regardless of how far into the lease.

---

## Comparative Item Scoring

Comparative items compare the subject property against the comp set. Four scoring methods (A, B, C, D) are used depending on the item's computation approach.

### Method A: Pricing Proximity (bidirectional — deviation from market penalized)

The subject/comp ratio is compared to 1.0 (market parity). Distance from 1.0 in either direction reduces the score.

| Abs(Ratio - 1.0) | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) |
|-------------------|----------------|------------|----------------|------------|
| Absolute deviation from 1.0 | ≤3% | ≤7% | ≤12% | ≤18% |

*A ratio of 0.97–1.03 = Excellent. A ratio of 0.82 or 1.18+ = Poor.*

**Applies to:**
- Studio — Avg Price vs Comps
- Studio — PPSF vs Comps
- 1-Bed — Avg Price vs Comps
- 1-Bed — PPSF vs Comps
- 2-Bed — Avg Price vs Comps
- 2-Bed — PPSF vs Comps
- New Leases (12mo) — Avg PPSF vs Market Avg PPSF

**Rationale:** Significant underpricing loses revenue. Significant overpricing loses demand. Being within ±3% of market indicates deliberate, competitive positioning.

**Diagnostic context:** The analytical engine (Layer 3+) interprets the direction — underpriced vs overpriced have different implications. The score captures the magnitude of misalignment; the diagnostic captures the direction.

### Method B: Ratio — Higher is Better (subject outperforming comps = higher score)

The subject/comp ratio is scored where values above 1.0 are favorable.

| Subject / Comp Avg ratio | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) |
|---------------------------|-----------------|------------|----------------|------------|
| Ratio value | ≥1.20 | 1.00 | 0.80 | 0.60 |

**Applies to:**
- Amenity Count vs Comps
- Mystery Shop Score vs Comps
- Resident Services vs Comps
- Resident Events vs Comps

**Interpretation:** A ratio of 1.0 means the subject matches the comp average. 1.20 means the subject is 20% above. 0.60 means 40% below.

### Method C: Point Difference — Higher is Better

For items computed as a point difference rather than a ratio.

**Occupancy vs Comps** (percentage point difference):

| Subject - Comp Avg | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) |
|---------------------|-----------------|------------|----------------|------------|
| pp difference | +3 | 0 | -3 | -6 |

*Subject 3pp above comp avg = Excellent. Subject 6pp below = Poor.*

**Reputation Score vs Comps** (point difference on 5-point scale):

| Subject - Comp Avg | Excellent (10) | Good (7.5) | Concern (5.0) | Poor (2.5) |
|---------------------|-----------------|------------|----------------|------------|
| point difference | +0.5 | 0.0 | -0.3 | -0.7 |

*On a 5-point scale, a 0.5-point advantage is significant. Being 0.7 below comp avg on reviews is a serious concern.*

### Method D: Binary with Adoption Context — Resident Mobile App vs Comps

This item is unique: the subject is binary (has app or doesn't), while the comp set has a continuous adoption rate. Uses a custom scoring matrix.

**Subject HAS app:**

| Comp Set Adoption Rate | Score | Interpretation |
|------------------------|-------|----------------|
| 0–20% | 10.0 | Major differentiator |
| 20–50% | 8.5 | Moderate differentiator |
| 50–80% | 7.0 | Meeting market expectation |
| 80–100% | 5.5 | Table stakes — no differentiation |

**Subject DOES NOT have app:**

| Comp Set Adoption Rate | Score | Interpretation |
|------------------------|-------|----------------|
| 0–20% | 7.0 | Not yet critical |
| 20–50% | 4.0 | Starting to fall behind |
| 50–80% | 2.0 | Significant gap |
| 80–100% | 0.5 | Critical deficiency |

Linear interpolation applies within each range.

---

## Summary: All Items Requiring Thresholds

| # | Item | Area | Scoring Method | Breakpoints |
|---|------|------|----------------|-------------|
| 1 | Occupancy Rate | 1 | ↑ Higher is better | 97/95/92/88 % |
| 2 | Average Vacant Days | 1 | ↓ Lower is better | 14/21/30/45 days |
| 3 | Aged Vacancy | 1 | ↓ Lower is better | 0/1/3/5 % of units |
| 4 | Cost per Lead | 2 | ↓ Lower is better | $30/60/100/175 |
| 5 | Loss-to-Lease % | 5 | ↓ Lower is better | 2/5/10/20 % |
| 6 | Concession % of GPR | 5 | ↓ Lower is better | 2/4/7/12 % |
| 7 | Rent Lift on Turnover | 5 | ↑ Higher is better | 5/3/1/0 % |
| 8 | Net Effective vs Asking Gap | 5 | ↓ Lower is better | 1/3/5/8 % |
| 9 | Renewal Rent Increase | 5 | ↑ Higher is better | 5/3.5/2/1 % |
| 10 | Renewal Rate | 6 | ↑ Higher is better | 65/55/45/30 % |
| 11 | Average Resident Tenure | 6 | ↑ Higher is better | 36/24/18/12 mo |
| 12 | Month-to-Month % | 6 | ↓ Lower is better | 5/10/20/30 % |
| 13 | Controllable Turnover Rate | 6 | ↓ Lower is better | 10/15/25/40 % |
| 14 | DNR Rate | 6 | ↓ Lower is better | 5/10/15/25 % |
| 15 | Units per Leasing Agent | 7 | ↓ Lower is better | 100/150/200/300 units |
| 16 | Units per Maintenance Tech | 7 | ↓ Lower is better | 75/100/150/200 units |
| 17 | Staff Turnover Rate | 7 | ↓ Lower is better | 15/25/40/60 % |
| 18 | Average Staff Tenure | 7 | ↑ Higher is better | 36/24/18/12 mo |
| 19 | PM Tenure | 7 | ↑ Higher is better | 36/24/12/6 mo |
| 20 | Open Position Rate | 7 | ↓ Lower is better | 0/5/10/20 % |
| 21 | Financial Revenue items (5) | 8 | ↑ Variance % | +5/0/-5/-10 % |
| 22 | Financial Expense items (12) | 8 | ↓ Variance % | -5/0/+5/+10 % |
| 23 | Work Order Completion Rate | 9 | ↑ Higher is better | 98/95/90/80 % |
| 24 | Avg WO Completion Duration | 9 | ↓ Lower is better | 1/2/5/10 days |
| 25 | Callback / Repeat WO Rate | 9 | ↓ Lower is better | 2/5/10/20 % |
| 26 | Preventive vs Reactive Ratio | 9 | ↑ Higher is better | 40/25/15/5 % |
| 27 | Make-Ready Duration | 9 | ↓ Lower is better | 5/7/10/14 days |
| 28 | Make-Ready Cost | 9 | ↓ Lower is better | $1.5k/2.5k/4k/6k |
| 29 | Delinquency Rate | 12 | ↓ Lower is better | 2/5/10/20 % |
| 30 | Bad Debt Write-Off Rate | 12 | ↓ Lower is better | 0.5/1.5/3/5 % |
| 31 | Eviction Rate | 12 | ↓ Lower is better | 1/2/4/8 % annual |
| 32 | Application Denial Rate | 12 | ↓ Lower is better | 10/20/30/50 % |
| 33 | Short-Tenure Turnover Rate | 12 | ↓ Lower is better | 5/10/20/30 % |
| 34 | Pricing vs Comps (7 items) | 5, 11 | ≈ Proximity to 1.0 | ±3/7/12/18 % |
| 35 | Amenity/Mystery/Services/Events (4) | 11 | ↑ Ratio | 1.20/1.00/0.80/0.60 |
| 36 | Occupancy vs Comps | 11 | ↑ pp difference | +3/0/-3/-6 |
| 37 | Reputation Score vs Comps | 11 | ↑ point diff | +0.5/0/-0.3/-0.7 |
| 38 | Resident Mobile App vs Comps | 11 | Custom matrix | See Method D |

**Total: 33 unique threshold sets covering all Data and Comparative items** (some sets apply to multiple items, e.g., financial variance patterns cover 17 sub-items).

---

## Calibration Notes

1. **Starting points, not final values.** These thresholds are initial calibration based on industry benchmarks and V6 experience. They should be validated against real property data from early assessments and adjusted as needed.

2. **Property class sensitivity.** These are class-agnostic defaults. The analytical engine may apply class-based adjustments at Layer 2 (cohort profiling). For example, Class A properties should achieve higher occupancy and renewal rates than Class C. Class-specific overrides are not defined here — they are a Layer 2 concern.

3. **Market sensitivity.** Some thresholds (Cost per Lead, rent-related metrics) vary significantly by market. The assessment-level configuration may include market adjustment factors in future iterations.

4. **V6 lineage.** Where V6 thresholds existed and remained appropriate, they were preserved. Items marked with V6 key names in the notes sections trace directly to `ScoringEngine.gs SCORING_BENCHMARKS`.

5. **Threshold override capability.** The platform should support per-engagement threshold overrides for markets or property types where defaults don't apply (e.g., luxury properties, student housing, senior living).
