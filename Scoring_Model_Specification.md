# Scoring Model Specification

Defines the complete structure and methodology of what the analytical engine scores, organized into 12 operational areas. This is the specification for Layer 1 (Scoring) of the Analytical Engine.

---

## Design Principles

1. **Scoring is infrastructure, not just a report card.** Scores feed Layer 2 (cohort profiling), Layer 3 (diagnostic context), and Layer 5 (impact prioritization). The scoring model must serve the consultant, the client, and the analytical engine.

2. **Competitive position is integrated.** A property performs in a market, not in a vacuum. Competitive data has its own scoring area (Area 11) using comparative methodology, producing a competitive profile alongside the absolute performance scores.

3. **Unified scoring function.** All input types — data metrics, checklist observations, and comparative ratios — produce a comparable 0–10 score through calibrated thresholds and piecewise linear interpolation. The scoring function is universal; the thresholds are item-specific.

4. **Three input types, one output.** Data (continuous metrics from PM systems), Checklist (human observations — Y/N binary and Tiered multi-level), and Comparative (relative to comp set). Each type has a defined method for producing a 0–10 score.

5. **Checklist 100-point budget.** Each checklist item's sub-items share a 100-point budget. Y/N sub-items earn their full point value (Y) or zero (N). Tiered sub-items earn a percentage of their point value based on the tier achieved. Points earned / 100 × 10 = score.

6. **Three-level weighting.** Sub-item points (within a checklist, sum to 100), item weights (within an area, sum to 100%), area weights (for overall score, sum to 100%). All weights are user-configurable.

7. **Every score is auditable.** Any score traces back to specific data fields, specific thresholds or rubric criteria, and a specific scoring method.

8. **Safety and compliance are scored.** These items produce scores within Operations, not just PASS/FLAG signals.

9. **Date-range-dependent items use an assessment-level variable.** Rather than hardcoding periods, the system uses a configurable date range set once per engagement. See Analytical Engine Specification for the complete list of date-dependent items.

---

## Scoring Methodology

### Input Types

**Data** — Continuous numerical values from PM systems, CRM, or financial reports (e.g., Occupancy Rate, Renewal Rate, Delinquency Rate). Scored by comparing the raw value against calibrated benchmark thresholds using piecewise linear interpolation to produce a 0–10 score.

**Checklist** — Human-derived evaluations from audit observations or management interviews. Two sub-types:
- **Y/N (Binary)** — Presence/absence. Yes = full point value; No = 0.
- **Tiered** — Multi-level categorical rating (e.g., Excellent/Good/Fair/Poor, or value ranges). Each tier maps to a percentage of the sub-item's point value.

Checklist scoring: Each checklist item has sub-items sharing a 100-point budget. Total points earned / 100 × 10 = item score (0–10).

**Comparative** — Metrics or observations evaluated relative to a competitive set. The subject property's value is compared to the comp set average. For items like occupancy and reputation, this is expressed as a percentage point difference. For pricing, this is a ratio. The difference/ratio is mapped to a 0–10 score via calibrated thresholds.

### Rollup

```
Sub-item points (within checklist, sum to 100)
    └── Item scores (0–10, each from its input type method)
            └── Area scores (weighted average of item scores, weights sum to 100%)
                    └── Overall asset score (weighted average of 12 area scores, weights sum to 100%)
```

Missing items are excluded from the weighted average (not scored as zero). The system tracks coverage percentage per area.

### Financials Scoring

Area 8 (Financials) uses a special scoring approach: each financial line item is scored by comparing the property's actual performance against the owner's own stated financial targets/budget, not generic industry benchmarks. Revenue items are scored favorably when actual exceeds budget; expense items are scored favorably when actual is below budget.

Additionally, the analytical engine produces a Simulated Optimal Budget (see Analytical Engine Specification) as a Layer 4+ output — a property-specific proforma derived from the analysis findings, providing a three-column comparison: Actual vs Owner's Budget vs Optimal.

---

## Area Weights

| Area | Weight |
|------|--------|
| 1. Vacancy/Occupancy | 9% |
| 2. Marketing | 8% |
| 3. Leasing Performance | 8% |
| 4. Listings | 8% |
| 5. Pricing | 8% |
| 6. Retention & Renewal | 8% |
| 7. Operations | 8% |
| 8. Financials | 9% |
| 9. Maintenance & Turnovers | 8% |
| 10. Property Condition | 8% |
| 11. Competitive Position | 10% |
| 12. Collections & Screening | 8% |
| **Total** | **100%** |

---

## Scoring Areas

### 1. Vacancy/Occupancy — Weight: 9%

**Question:** Are units generating revenue?

| Item | Type | Item Weight |
|------|------|-------------|
| Occupancy Rate | Data | 60% |
| Average Vacant Days | Data | 20% |
| Aged Vacancy | Data | 20% |

3 items (3 Data).

---

### 2. Marketing — Weight: 8%

**Question:** Is the property generating demand?

| Item | Type | Item Weight |
|------|------|-------------|
| Online Reputation | Checklist | 15% |
| Digital/Social Presence | Checklist | 15% |
| Website Quality | Checklist | 10% |
| Digital Marketing | Checklist | 10% |
| Referral Program | Checklist | 10% |
| Corporate Relocation Program | Checklist | 10% |
| Broker/Locator Program | Checklist | 20% |
| Cost per Lead | Data | 10% |

8 items (7 Checklist, 1 Data).

#### Sub-item Point Budgets

**Online Reputation** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Avg Review Score | Tiered | 40 |
| Review Volume | Tiered | 20 |
| Review Recency (last 90d) | Tiered | 15 |
| Platform Coverage | Tiered | 10 |
| GMB Claimed | Y/N | 10 |
| GMB Optimized | Y/N | 5 |

**Digital/Social Presence** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Social - Facebook | Y/N | 10 |
| Social - Instagram | Y/N | 10 |
| Social - TikTok | Y/N | 10 |
| Social - LinkedIn | Y/N | 10 |
| Audience Size | Tiered | 30 |
| Post Consistency | Tiered | 30 |

**Website Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Website Exists | Y/N | 30 |
| Mobile Responsive | Y/N | 10 |
| Live Chat | Y/N | 10 |
| Contact Form | Y/N | 10 |
| Floor Plans | Y/N | 10 |
| Photo Gallery | Y/N | 10 |
| Unit Availability | Y/N | 10 |
| Virtual Tours | Y/N | 10 |

**Digital Marketing** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Social Media Paid Ads | Y/N | 33 |
| Google Adwords | Y/N | 34 |
| Email/SMS Marketing | Y/N | 33 |

**Referral Program** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Referral Program Exists | Y/N | 50 |
| Referral Incentive Offered | Y/N | 10 |
| Referral Tracking System | Y/N | 10 |
| Local Business Partnerships | Y/N | 10 |
| Influencer/Creator Collaborations | Y/N | 10 |
| Co-Branded Content or Events | Y/N | 10 |

**Corporate Relocation Program** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Corp Relocation Program Exists | Y/N | 50 |
| RMC Partnerships | Y/N | 20 |
| Corporate Rates/Packages | Y/N | 10 |
| Furnished/Short-Term Options | Y/N | 10 |
| Dedicated Relocation Contact | Y/N | 10 |

**Broker/Locator Program** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Broker Program Exists | Y/N | 50 |
| Broker Portal | Y/N | 10 |
| Broker Materials | Y/N | 10 |
| Direct Broker Contact | Y/N | 10 |
| Broker Lead Tracking | Y/N | 10 |
| Broker Events/Outreach | Y/N | 10 |

---

### 3. Leasing Performance — Weight: 8%

**Question:** Is the team converting demand into leases?

| Item | Type | Item Weight |
|------|------|-------------|
| Conversion Metrics | Checklist | 25% |
| Tour Observation | Checklist | 10% |
| Mystery Shop Score | Checklist | 10% |
| Lead Management Quality | Checklist | 10% |
| Leasing Process Quality | Checklist | 10% |
| Training & Development | Checklist | 10% |
| Tour Scheduling Quality | Checklist | 10% |
| Office Environment | Checklist | 5% |
| Model Unit Quality | Checklist | 10% |

9 items (9 Checklist).

**Note:** Mystery Shop Score is also used in Competitive Position (Area 11) for comparison against comps. Tour Observation is an independent auditor-shadow observation that triangulates with the Mystery Shop.

#### Sub-item Point Budgets

**Conversion Metrics** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Lead-to-Tour % | Tiered | 15 |
| Tour-to-App % | Tiered | 15 |
| App-to-Lease % | Tiered | 10 |
| Tour-to-Lease % | Tiered | 20 |
| Lead-to-Lease % | Tiered | 20 |
| Cancel Rate | Tiered | 10 |
| Ghost Rate | Tiered | 10 |

**Tour Observation** (100 pts): 28 sub-items — Greeting (6 × 3.5–4 pts), Needs Assessment (6 × 3.5–4 pts), Wait Time (4 pts), Tour conduct (9 × 3.5–4 pts + Fair Housing 3.5 pts), Tour Duration (3 pts), Closing (5 × 3.5 pts). See Scoring Model Workbook for individual point values.

**Mystery Shop Score** (100 pts): 42 sub-items — Phone (9 × 2–2.5 pts), Greeting (6 × 2.5–3 pts), Needs Assessment (6 × 2–2.5 pts), Wait Time (2.5 pts), Tour conduct (9 × 2–2.5 pts including Curb Appeal + Fair Housing 2 pts), Tour Duration (2 pts), Closing (5 × 2.5 pts), Follow-Up (4 × 2 pts). See Scoring Model Workbook for individual point values.

**Lead Management Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Email Response Time | Tiered | 20 |
| Phone Response Time | Tiered | 20 |
| Follow-Up System | Tiered | 15 |
| Follow-Up Volume | Tiered | 15 |
| After-Hours Handling | Tiered | 10 |
| Weekend Handling | Tiered | 10 |
| Advanced Programs | Tiered | 10 |

**Leasing Process Quality** (100 pts): 27 sub-items — 23 process elements (Y/N, 3.5–4 pts each), App Processing Speed (4 pts), Screening Processing Speed (4 pts), Approval Speed (4 pts), Lease Turnaround (4 pts). See Scoring Model Workbook for individual point values.

**Training & Development** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Formal Program Exists | Y/N | 40 |
| Onboarding Duration | Tiered | 5 |
| Ongoing Frequency | Tiered | 5 |
| Coaching Frequency | Tiered | 3 |
| Certifications Required | Y/N | 2 |
| Product Knowledge Training | Y/N | 10 |
| Sales/Closing Training | Y/N | 20 |
| Fair Housing Training | Y/N | 5 |
| CRM/Systems Training | Y/N | 5 |
| Other Training Programs | Y/N | 5 |

**Tour Scheduling Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Scheduling Methods | Tiered | 40 |
| Online Self-Booking | Y/N | 15 |
| Availability (Weekend/Evening) | Tiered | 15 |
| Broker Scheduling Access | Y/N | 15 |
| Flexibility (Same-day/Walk-ins) | Tiered | 15 |

**Office Environment** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Accessibility | Tiered | 15 |
| Hours Coverage | Tiered | 20 |
| Seating Available | Y/N | 10 |
| Refreshments | Y/N | 15 |
| WiFi | Y/N | 10 |
| Restroom | Y/N | 10 |
| Professional Setup | Tiered | 10 |
| Wayfinding Signage | Y/N | 10 |

**Model Unit Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Model Available | Y/N | 70 |
| Model Quality | Tiered | 15 |
| Model Positioning | Tiered | 15 |

---

### 4. Listings — Weight: 8%

**Question:** Is the product positioned correctly?

| Item | Type | Item Weight |
|------|------|-------------|
| Platform Coverage | Checklist | 25% |
| Photo Quality | Checklist | 25% |
| Content Quality | Checklist | 25% |
| Listing Accuracy | Checklist | 25% |

4 items (4 Checklist).

#### Sub-item Point Budgets

**Platform Coverage** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Platform Count | Tiered | 35 |
| ILS Coverage | Tiered | 25 |
| Update Frequency | Tiered | 15 |
| Management Quality | Tiered | 10 |
| Syndication Method | Tiered | 15 |

**Photo Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Hero Image Present | Y/N | 10 |
| Exterior Coverage (5+) | Y/N | 10 |
| Unit Interior (all rooms/types) | Y/N | 20 |
| Amenity Coverage | Tiered | 15 |
| Lifestyle Shots (5+) | Y/N | 10 |
| Professional Photographer | Y/N | 25 |
| Photo Recency | Tiered | 10 |

**Content Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Unique Selling Points Mentioned | Y/N | 15 |
| Neighborhood Context Included | Y/N | 10 |
| Call-to-Action Included | Y/N | 10 |
| Contact Info Clear | Y/N | 15 |
| Floor Plans Available | Y/N | 10 |
| Unit Specs Accurate | Y/N | 10 |
| Amenities Fully Listed | Y/N | 10 |
| Pet Policy Stated | Y/N | 10 |
| Lease Terms Mentioned | Y/N | 10 |

**Listing Accuracy** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Pricing Accurate Across Platforms | Y/N | 15 |
| Availability Accurate | Y/N | 15 |
| Unit Types/Sizes Correct | Y/N | 15 |
| Amenities List Accurate | Y/N | 15 |
| Photos Match Property Condition | Y/N | 15 |
| Specials Updated | Y/N | 15 |
| Contact Info Current | Y/N | 10 |

---

### 5. Pricing — Weight: 8%

**Question:** Is the property priced correctly?

| Item | Type | Item Weight |
|------|------|-------------|
| Relative to Market | Checklist | 20% |
| Concession % of GPR | Data | 20% |
| Rent Lift on Turnover | Data | 20% |
| Net Effective vs Asking Gap | Data | 20% |
| Renewal Rent Increase | Data | 20% |

5 items (1 Checklist, 4 Data).

#### Sub-item Point Budgets

**Relative to Market** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Loss-to-Lease % | Data | 50 |
| New Leases (12mo) — Avg PPSF vs Market Avg PPSF | Comparative | 50 |

---

### 6. Retention & Renewal — Weight: 8%

**Question:** Are residents staying?

| Item | Type | Item Weight |
|------|------|-------------|
| Renewal Rate | Data | 30% |
| Average Resident Tenure | Data | 20% |
| Month-to-Month % | Data | 10% |
| Controllable Turnover Rate | Data | 20% |
| DNR Rate | Data | 10% |
| Renewal & Retention Process | Checklist | 10% |

6 items (5 Data, 1 Checklist).

#### Sub-item Point Budgets

**Renewal & Retention Process** (100 pts): 20 sub-items at 5 pts each — Defined Renewal Process Exists (Y/N), Renewal Offer Communicated in Writing (Y/N), Renewal Pricing Strategy Defined (Y/N), Resident Satisfaction Assessed Before Renewal (Y/N), Renewal Negotiation Flexibility (Y/N), Electronic Renewal Signing Available (Y/N), Proactive Retention Outreach Program (Y/N), Retention Incentives Offered (Y/N), Resident Feedback/Survey Program (Y/N), Exit Interview / Move-Out Survey (Y/N), DNR Review Process Exists (Y/N), DNR Criteria Documented (Y/N), DNR Decisions Reviewed by Management (Y/N), DNR Communication Timeline Defined (Y/N), Occupied Apartment Program Exists (Y/N), Non-Renewal Triggers Showing Communication (Y/N), Pre-Move-Out Unit Assessment (Y/N), Move-Out Checklist Provided (Y/N), Outreach Timeline (Tiered, 5 pts), NTV Response Speed (Tiered, 5 pts).

---

### 7. Operations — Weight: 8%

**Question:** Is the property staffed and equipped to perform?

| Item | Type | Item Weight |
|------|------|-------------|
| Units per Leasing Agent | Data | 25% |
| Units per Maintenance Tech | Data | 25% |
| Staffing Stability | Checklist | 20% |
| Technology Effectiveness | Checklist | 20% |
| Compliance | Checklist | 10% |

5 items (2 Data, 3 Checklist).

#### Sub-item Point Budgets

**Staffing Stability** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Staff Turnover Rate | Data | 25 |
| Average Staff Tenure | Data | 25 |
| PM Tenure | Data | 25 |
| Open Position Rate | Data | 25 |

**Technology Effectiveness** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Coverage Breadth | Tiered | 15 |
| Capability Depth | Tiered | 15 |
| Integration Quality | Tiered | 15 |
| Staff Mobile Access | Y/N | 10 |
| Resident Mobile Access | Y/N | 10 |
| Automation Level | Tiered | 15 |
| System Efficiency | Tiered | 10 |
| Tech Spend ROI | Tiered | 10 |

**Compliance** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Fire/Safety Inspection Current | Y/N | 25 |
| No Open Code Violations | Y/N | 25 |
| ADA Compliance Met | Y/N | 25 |
| Insurance Current | Y/N | 25 |

---

### 8. Financials — Weight: 9%

**Question:** Is the property hitting its financial targets? (scored against owner-reported benchmarks)

| Item | Type | Item Weight |
|------|------|-------------|
| Revenue | Checklist | 25% |
| Expenses | Checklist | 25% |
| Bottom Line | Checklist | 25% |
| Capital | Checklist | 25% |

4 items (4 Checklist). All sub-items are Data type, scored as actual vs owner's budget variance.

#### Sub-item Point Budgets

**Revenue** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Gross Potential Rent | Data | 20 |
| Vacancy Loss | Data | 20 |
| Concessions / Loss-to-Lease | Data | 20 |
| Other Income | Data | 20 |
| Effective Gross Income | Data | 20 |

**Expenses** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Payroll & Benefits | Data | 11 |
| Repairs & Maintenance | Data | 12 |
| Utilities | Data | 11 |
| Marketing & Advertising | Data | 11 |
| Insurance | Data | 11 |
| Real Estate Taxes | Data | 11 |
| Admin / G&A | Data | 11 |
| Contract Services | Data | 11 |
| Management Fee | Data | 11 |

**Bottom Line** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Total Operating Expenses | Data | 50 |
| Net Operating Income | Data | 50 |

**Capital** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Capital Expenditures | Data | 50 |
| Capital Reserves | Data | 50 |

---

### 9. Maintenance & Turnovers — Weight: 8%

**Question:** Are units maintained and turned efficiently?

| Item | Type | Item Weight |
|------|------|-------------|
| Maintenance Performance | Checklist | 55% |
| Maintenance Operations Systems | Checklist | 15% |
| Turnover Performance | Checklist | 30% |

3 items (3 Checklist).

#### Sub-item Point Budgets

**Maintenance Performance** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Emergency Response Time | Tiered | 20 |
| Routine Response Time | Tiered | 20 |
| Work Order Completion Rate | Data | 15 |
| Avg Work Order Completion Duration | Data | 15 |
| Callback / Repeat Work Order Rate | Data | 15 |
| Preventive vs Reactive Ratio | Data | 15 |

**Maintenance Operations Systems** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Formal Request System | Y/N | 50 |
| Maintenance Process Documentation | Y/N | 25 |
| Parts Inventory System | Y/N | 25 |

**Turnover Performance** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Make-Ready Duration | Data | 70 |
| Make-Ready Cost | Data | 30 |

---

### 10. Property Condition — Weight: 8%

**Question:** What shape is the asset in?

| Item | Type | Item Weight |
|------|------|-------------|
| Overall Property Condition | Checklist | 50% |
| Capital Asset Condition | Checklist | 15% |
| Deferred Maintenance | Checklist | 15% |
| Unit Condition — Vacant Walks | Checklist | 20% |

4 items (4 Checklist).

**Aggregation method for Vacant Walks:** Each unit is rated individually per category; scores are averaged across all sampled vacant units for each category.

#### Sub-item Point Budgets

**Overall Property Condition** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Overall Condition Rating | Tiered | 20 |
| Common Areas Rating | Tiered | 20 |
| Exterior Presentation | Tiered | 20 |
| Amenities Condition Rating | Tiered | 20 |
| Issues Count | Tiered | 20 |

**Capital Asset Condition** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Roof | Tiered | 10 |
| HVAC Systems | Tiered | 10 |
| Plumbing | Tiered | 10 |
| Electrical | Tiered | 10 |
| Siding / Facade | Tiered | 10 |
| Windows | Tiered | 10 |
| Parking Surfaces | Tiered | 10 |
| Elevators | Tiered | 10 |
| Water Heaters | Tiered | 10 |
| Fire/Life Safety Systems | Tiered | 10 |

**Deferred Maintenance** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Number of Deferred Items | Tiered | 50 |
| Critical Systems Affected | Y/N | 25 |
| Safety Hazards Present | Y/N | 25 |

**Unit Condition — Vacant Walks** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Flooring | Tiered | 9 |
| Walls / Paint | Tiered | 9 |
| Kitchen Cabinets & Countertops | Tiered | 9 |
| Kitchen Appliances | Tiered | 9 |
| Bathroom Fixtures & Tile | Tiered | 9 |
| Windows & Blinds | Tiered | 9 |
| Doors & Hardware | Tiered | 9 |
| Lighting Fixtures | Tiered | 9 |
| HVAC (in-unit) | Tiered | 9 |
| Overall Cleanliness | Tiered | 9 |
| General Finish Level | Tiered | 10 |

---

### 11. Competitive Position — Weight: 10%

**Question:** How does this property stack up?

| Item | Type | Item Weight |
|------|------|-------------|
| Pricing vs Comps | Checklist | 25% |
| Amenity Count vs Comps | Comparative | 10% |
| Reputation Score vs Comps | Comparative | 10% |
| Mystery Shop Score vs Comps | Comparative | 20% |
| Occupancy vs Comps | Comparative | 20% |
| Resident Services vs Comps | Comparative | 5% |
| Resident Events vs Comps | Comparative | 5% |
| Resident Mobile App vs Comps | Comparative | 5% |

8 items (1 Checklist, 7 Comparative).

**Note:** All comps are mystery-toured using the same evaluation checklist as the subject property. Occupancy and Reputation comparisons use percentage point difference (not ratio). Standard amenity and services lists are defined in the audit intake form.

#### Sub-item Point Budgets

**Pricing vs Comps** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Studio — Avg Price vs Comps | Comparative | 16.66 |
| Studio — PPSF vs Comps | Comparative | 16.66 |
| 1-Bed — Avg Price vs Comps | Comparative | 16.66 |
| 1-Bed — PPSF vs Comps | Comparative | 16.66 |
| 2-Bed — Avg Price vs Comps | Comparative | 16.66 |
| 2-Bed — PPSF vs Comps | Comparative | 16.70 |

---

### 12. Collections & Screening — Weight: 8%

**Question:** Is the property screening well and collecting what it's owed?

| Item | Type | Item Weight |
|------|------|-------------|
| Delinquency Rate | Data | 20% |
| Bad Debt Write-Off Rate | Data | 10% |
| Eviction Rate | Data | 20% |
| Application Denial Rate | Data | 20% |
| Short-Tenure Turnover Rate | Data | 10% |
| Screening Process Quality | Checklist | 20% |

6 items (5 Data, 1 Checklist).

#### Sub-item Point Budgets

**Screening Process Quality** (100 pts):

| Sub-item | Type | Points |
|----------|------|--------|
| Defined Screening Criteria Documented | Y/N | 12.5 |
| Credit Check Required | Y/N | 12.5 |
| Background Check Required | Y/N | 12.5 |
| Income Verification Required | Y/N | 12.5 |
| Rental History Verification Required | Y/N | 12.5 |
| Employment Verification Required | Y/N | 12.5 |
| Consistent Application of Criteria | Y/N | 12.5 |
| Adverse Action Notice Process | Y/N | 12.5 |

---

## Item Count Summary

| Area | Data | Checklist | Comparative | Total |
|------|------|-----------|-------------|-------|
| 1. Vacancy/Occupancy | 3 | 0 | 0 | 3 |
| 2. Marketing | 1 | 7 | 0 | 8 |
| 3. Leasing Performance | 0 | 9 | 0 | 9 |
| 4. Listings | 0 | 4 | 0 | 4 |
| 5. Pricing | 4 | 1 | 0 | 5 |
| 6. Retention & Renewal | 5 | 1 | 0 | 6 |
| 7. Operations | 2 | 3 | 0 | 5 |
| 8. Financials | 0 | 4 | 0 | 4 |
| 9. Maintenance & Turnovers | 0 | 3 | 0 | 3 |
| 10. Property Condition | 0 | 4 | 0 | 4 |
| 11. Competitive Position | 0 | 1 | 7 | 8 |
| 12. Collections & Screening | 5 | 1 | 0 | 6 |
| **Total** | **20** | **38** | **7** | **65** |

---

## What This Document Does NOT Define

1. **Grade bands** — the score-to-letter-grade mapping (e.g., 9–10 = A, 7–8.9 = B, etc.)
2. **Confidence modifiers** — how data contradiction density affects score trust
3. **Benchmark override rules** — how benchmarks adjust for property class, market, or engagement context

---

## Authoritative Sources

- **Locked-in weight values:** Scoring Weights Final (`REBOOT/RBv2/Scoring_Weights_Final_Update.json`)
- **Weight editing interface and sub-item point budgets:** Scoring Model Workbook (`REBOOT/RBv2/Scoring_Model_Workbook.html`)
- **Computation rules, data sources, and formulas:** Computation Rules Workbook (`REBOOT/RBv2/Computation_Rules_Workbook.html`)
- **Engine architecture, simulated optimal budget, date range variable:** Analytical Engine Specification (`REBOOT/RBv2/Analytical_Engine_Specification.md`)
- **Pre-computed KPIs and benchmarks:** Basic Analytic Data Set (`REBOOT/RBv2/Basic_Analytic_Data_Set.md`)
- **Scoring thresholds and calibration:** Scoring Thresholds Calibration (`REBOOT/RBv2/Scoring_Thresholds_Calibration.md`)
- **Audit data collection instrument:** Audit Workbook Specification (`REBOOT/RBv2/Audit_Workbook_Specification.md`)
- **Complete field inventory:** Complete Data Inventory (`REBOOT/RBv2/Complete_Data_Inventory.md`)
