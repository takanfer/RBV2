# Scoring Model Specification

Defines every item the analytical engine scores, the method used, the calibration values, the weights, and how items roll up into category and overall scores. This is the specification for Layer 1 (Scoring) of the Analytical Engine.

---

## Scoring Methods

Every scorable item uses exactly one of three methods. All methods produce a **0–10 score**.

### Method 1: Benchmark

A computed metric is compared against industry thresholds using piecewise linear interpolation.

```
Thresholds: excellent | good | concern | poor

Score mapping (lower-is-better example, e.g., VDOM days):
  value <= excellent  →  10.0
  value = good        →   7.5
  value = concern     →   5.0
  value >= poor       →   0.0
  Between thresholds  →  linear interpolation

Score mapping (higher-is-better example, e.g., occupancy rate):
  value >= excellent  →  10.0
  value = good        →   7.5
  value = concern     →   5.0
  value <= poor       →   0.0
  Between thresholds  →  linear interpolation
```

Example: Average VDOM = 24 days against thresholds {excellent: 14, good: 21, concern: 30, poor: 45}. Value falls between good (21) and concern (30). Interpolation: 7.5 − (24−21)/(30−21) × 2.5 = 7.5 − 0.83 = **6.67**.

### Method 2: Checklist

Items are assessed as present/absent, rated on defined criteria, or scored via Y/N elements. Points earned divided by points possible, normalized to 0–10.

```
Score = (Points Earned / Total Points Possible) × 10
```

Example: Amenity inventory has 114 total possible points. Property earns 72. Score = (72/114) × 10 = **6.32**.

### Method 3: Competitive

The property's value is measured relative to its collected competitive set. The property's position vs the comp average is converted to a 0–10 scale.

```
For higher-is-better (e.g., amenity count):
  Ratio = Property value / Comp average
  Score = clamp(Ratio × 5, 0, 10)

For lower-is-better (e.g., rent vs comps when evaluating value):
  Inverted ratio applied
```

### Non-Scored Signals

**Compliance flags** — legal/safety items tracked as PASS or FLAG. Not graded on a scale.

**Confidence modifiers** — data integrity and contradiction density. Modifies the confidence attached to other scores. Does not produce a performance score.

---

## Scoring Dimensions

Items are organized into 10 operational dimensions representing what the property does and how it performs.

---

### 1. Physical Asset

What the property IS — its physical product, amenities, condition, and infrastructure.

| Item | Method | Weight | Divisor | Source |
|------|--------|--------|---------|--------|
| **Building amenity inventory** | Checklist | 0.12 | 114 pts | V6 Part 1A AMEN_ keys |
| **Unit amenity inventory** | Checklist | 0.08 | 80 pts | New — see breakdown below |
| **Parking quality** | Checklist | 0.04 | included in amenity | V6 AMEN_PARK_ keys |
| **Access control** | Checklist | 0.04 | included in amenity | V6 AMEN_ACCESS_ keys |
| **Overall property condition** | Checklist | 0.12 | 100 pts | V6 Part 5B COND_ keys |
| **Common area condition** | Checklist | 0.08 | included in condition | V6 COND_COMMON_ |
| **Landscaping quality** | Checklist | 0.06 | included in condition | V6 COND_LAND_ |
| **Amenity condition** | Checklist | 0.06 | included in condition | V6 COND_AMEN_ |
| **Specific issues count** | Checklist | 0.05 | included in condition | V6 COND_ISSUES_ |
| **Deferred maintenance level** | Checklist | 0.06 | included in maint ops | V6 MAINT_DEF_ keys |
| **Resident services inventory** | Checklist | 0.06 | 60 pts | New — see breakdown below |
| **Resident events program** | Checklist | 0.05 | 50 pts | New — see breakdown below |
| **Capital asset condition** | Checklist | 0.10 | 100 pts | New — see breakdown below |
| **Unit condition (vacant walks)** | Checklist | 0.08 | per-unit scoring | New |

**New checklist point breakdowns:**

**Unit amenity inventory** (80 pt divisor):
Per Y/N unit feature present: Kitchen items 4 pts each (5 items = 20), Bathroom items 3 pts each (8 items = 24), Laundry 5 pts (3 options), Climate 3 pts each (3 items = 9), Flooring/Storage 2 pts each (6 items = 12), Tech 3 pts each (4 items = 12), Other 1 pt each (3 items = 3).

**Resident services inventory** (60 pt divisor):
Per Y/N service present: 5 pts each × 12 services = 60 pts max.

**Resident events program** (50 pt divisor):
Events offered (Y/N) 8 pts, Frequency (Never 0 / Annually 2 / Quarterly 4 / Monthly 6 / Weekly 8) max 8 pts, Attendance >50% 5 pts, Resident hosting available 5 pts, Rentable spaces 5 pts, Booking system 5 pts, Event variety (1 pt per type, max 7), Revenue generation 7 pts.

**Capital asset condition** (100 pt divisor):
Per major system (Roof, HVAC, Plumbing, Electrical, Parking Surface, Elevators — 6 systems): Condition rating (Excellent 12 / Good 9 / Fair 5 / Poor 2 / Critical 0) + Age vs expected life bonus (>50% remaining 5 / 25-50% 3 / <25% 0). Max per system ~17 pts. 6 systems × 17 ≈ 100 pts max.

**Compliance flags (not scored):**
- Fire/safety inspection currency (Intake 10.5)
- Open fire code violations (Intake 10.5)
- ADA compliance observations

---

### 2. Marketing & Visibility

How the property presents itself and attracts demand.

| Item | Method | Weight | Divisor/Thresholds | Source |
|------|--------|--------|--------------------|--------|
| **Online reputation score** | Checklist | 0.12 | 100 pts | V6 Part 1B REP_ keys |
| **Digital/social presence** | Checklist | 0.08 | 97 pts | V6 Part 1C DIGI_ keys |
| **Website quality** | Checklist | 0.10 | 100 pts | V6 Part 3A MKT_WEB_ keys |
| **Social media marketing** | Checklist | 0.08 | 110 pts | V6 Part 3B MKT_SOC_ keys |
| **Partnership & referral programs** | Checklist | 0.08 | 200 pts | V6 Part 3C MKT_PARTNER_ keys |
| **Listing platform coverage** | Checklist | 0.10 | 90 pts | V6 Part 2A MKT_PLAT_ keys |
| **Photo quality** | Checklist | 0.12 | 100 pts | V6 Part 2B MKT_PHOTO_ keys |
| **Content quality** | Checklist | 0.08 | 92 pts | V6 Part 2C MKT_CONT_ keys |
| **Listing accuracy** | Checklist | 0.10 | 100 pts | V6 Part 2D MKT_LIST_ keys |
| **Cost per lead** | Benchmark | 0.07 | see thresholds | V6 lead_cost_per |
| **Cost per lease** | Benchmark | 0.07 | see thresholds | BADS-derived |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Cost per lead | Lower | $30 | $60 | $100 | $175 | V6 lead_cost_per |
| Cost per lease | Lower | $400 | $750 | $1,200 | $2,000 | BADS-derived |

---

### 3. Leasing & Sales

How the property converts prospects into residents.

| Item | Method | Weight | Divisor/Thresholds | Source |
|------|--------|--------|--------------------|--------|
| **Lead-to-tour conversion** | Benchmark | 0.08 | see thresholds | V6 CONV_LTT |
| **Tour-to-application conversion** | Benchmark | 0.08 | see thresholds | V6 CONV_TTA |
| **Application-to-lease conversion** | Benchmark | 0.06 | see thresholds | V6 CONV_ATL |
| **Lead-to-lease conversion** | Benchmark | 0.06 | see thresholds | V6 CONV_LTL |
| **Ghost/no-show rate** | Benchmark | 0.05 | see thresholds | V6 ghost_rate |
| **Sales velocity (days)** | Benchmark | 0.04 | see thresholds | V6 CONV_DAYS |
| **Lead response time (email)** | Benchmark | 0.05 | see thresholds | V6 lead_response_min |
| **Lead response time (phone)** | Benchmark | 0.05 | see thresholds | V6 lead_response_min |
| **Follow-up touch count** | Benchmark | 0.03 | see thresholds | V6 LEAS_LEAD_FUPVOL |
| **Training & development program** | Checklist | 0.04 | 100 pts | V6 Part 4A LEAS_TRAIN_ keys |
| **Brokerage oversight** | Checklist | 0.03 | 100 pts | V6 Part 4B LEAS_BROK_ keys (conditional) |
| **Tour scheduling quality** | Checklist | 0.04 | 100 pts | V6 Part 4C LEAS_SCHED_ keys |
| **Lead management quality** | Checklist | 0.06 | 110 pts | V6 Part 4D LEAS_LEAD_ keys |
| **Office environment** | Checklist | 0.03 | 80 pts | V6 Part 4E LEAS_OFF_ keys |
| **Model unit quality** | Checklist | 0.03 | 50 pts | V6 Part 4F LEAS_MODEL_ keys |
| **Tour experience quality** | Checklist | 0.10 | 200 pts | V6 Part 4G LEAS_TOUR_ keys |
| **Mystery shop score** | Checklist | 0.10 | 110 pts | V6 Part 4H MYST_ keys |
| **Leasing process quality** | Checklist | 0.07 | 128 pts | V6 Part 4J LEAS_PROC_ keys |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Lead-to-tour conversion | Higher | 50% | 40% | 25% | 15% | V6 CONV_LTT tiers |
| Tour-to-application conversion | Higher | 55% | 45% | 30% | 20% | V6 CONV_TTA tiers |
| Application-to-lease conversion | Higher | 85% | 75% | 60% | 50% | V6 CONV_ATL tiers |
| Lead-to-lease conversion | Higher | 20% | 15% | 8% | 5% | V6 CONV_LTL tiers |
| Ghost/no-show rate | Lower | 10% | 15% | 25% | 40% | V6 ghost_rate |
| Sales velocity (days per stage) | Lower | 5 | 7 | 12 | 15 | V6 CONV_DAYS tiers |
| Lead response time (email, min) | Lower | 30 | 60 | 240 | 480 | V6 LEAS_LEAD_EMAIL tiers |
| Lead response time (phone, min) | Lower | 15 | 30 | 120 | 240 | V6 LEAS_LEAD_PHONE tiers |
| Follow-up touch count | Higher | 8 | 5 | 3 | 1 | V6 LEAS_LEAD_FUPVOL tiers |

**Compliance flags (not scored):**
- Fair housing compliance (Mystery Shop Section 7 — PASS/FLAG)

---

### 4. Pricing & Revenue

How the property prices its product and captures revenue.

| Item | Method | Weight | Source |
|------|--------|--------|--------|
| **Physical occupancy rate** | Benchmark | 0.10 | V6 occupancy_rate |
| **Economic occupancy rate** | Benchmark | 0.10 | BADS-derived |
| **Physical-to-economic gap** | Benchmark | 0.06 | BADS-derived |
| **Loss-to-lease percentage** | Benchmark | 0.10 | V6 pct_under_market (adapted) |
| **Concession percentage of GPR** | Benchmark | 0.07 | V6 conc_frequency (adapted) |
| **Bad debt percentage of GPR** | Benchmark | 0.06 | V6 bad_debt_pct |
| **Other income per unit** | Benchmark | 0.04 | BADS-derived |
| **Net effective rent vs asking** | Benchmark | 0.05 | BADS-derived |
| **Rent lift on turnover** | Benchmark | 0.06 | BADS-derived |
| **Renewal rent increase** | Benchmark | 0.05 | V6 rent_increase_pct |
| **Revenue per unit** | Benchmark | 0.06 | V6 revenue_per_unit |
| **Revenue per square foot** | Benchmark | 0.04 | BADS-derived |
| **Pet revenue per unit** | Benchmark | 0.03 | BADS-derived |
| **Pet penetration rate** | Benchmark | 0.03 | BADS-derived |
| **Vacancy loss as % of GPR** | Benchmark | 0.08 | BADS-derived |
| **Total revenue loss** | Benchmark | 0.07 | BADS-derived |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Physical occupancy rate | Higher | 97% | 95% | 92% | 88% | V6 occupancy_rate |
| Economic occupancy rate | Higher | 93% | 90% | 86% | 82% | BADS-derived |
| Physical-to-economic gap | Lower | 2 pts | 4 pts | 6 pts | 10 pts | BADS-derived |
| Loss-to-lease percentage | Lower | 2% | 4% | 7% | 12% | V6 pct_under_market adapted |
| Concession percentage of GPR | Lower | 1% | 2.5% | 4% | 7% | BADS-derived |
| Bad debt percentage of GPR | Lower | 0.5% | 1.5% | 3% | 5% | V6 bad_debt_pct |
| Other income per unit ($/mo) | Higher | $150 | $100 | $60 | $30 | BADS-derived |
| Net effective rent vs asking gap | Lower | 1% | 3% | 6% | 10% | BADS-derived |
| Rent lift on turnover | Higher | 8% | 5% | 2% | 0% | BADS-derived |
| Renewal rent increase | Higher | 5% | 3.5% | 2% | 1% | V6 rent_increase_pct |
| Revenue per unit ($/yr) | Higher | $18,000 | $14,000 | $10,000 | $7,000 | V6 revenue_per_unit |
| Revenue per SF ($/yr) | Higher | $24 | $18 | $13 | $9 | BADS-derived |
| Pet revenue per unit ($/yr) | Higher | $72 | $48 | $30 | $12 | BADS-derived |
| Pet penetration rate | Higher | 60% | 50% | 35% | 20% | BADS-derived |
| Vacancy loss as % of GPR | Lower | 3% | 5% | 8% | 12% | BADS-derived |
| Total revenue loss (vac+conc+BD) | Lower | 5% | 8% | 12% | 18% | BADS-derived |

---

### 5. Vacancy & Turns

How the property manages unit turnover and vacancy duration.

| Item | Method | Weight | Source |
|------|--------|--------|--------|
| **Average total vacant days** | Benchmark | 0.10 | V6 vdom_days (adapted for total) |
| **Average make-ready duration** | Benchmark | 0.10 | V6 make_ready_days |
| **Average listing lag** | Benchmark | 0.06 | BADS-derived |
| **Average VDOM** | Benchmark | 0.12 | V6 vdom_days |
| **Average pre-occupancy gap** | Benchmark | 0.05 | BADS-derived |
| **Average vacancy cost per event** | Benchmark | 0.08 | BADS-derived |
| **Annual turnover rate** | Benchmark | 0.10 | V6 turnover_rate (adapted) |
| **Average make-ready cost** | Benchmark | 0.07 | BADS-derived |
| **Total tenant acquisition cost** | Benchmark | 0.08 | BADS-derived |
| **Repeat turnover rate** | Benchmark | 0.06 | V6 repeat_pct |
| **Controllable turnover rate** | Benchmark | 0.06 | BADS-derived |
| **Aged vacancy percentage** | Benchmark | 0.06 | BADS-derived |
| **Shadow vacancy** | Benchmark | 0.06 | BADS-derived |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Average total vacant days | Lower | 25 | 38 | 55 | 75 | V6 vdom_days adapted |
| Average make-ready duration (days) | Lower | 5 | 7 | 10 | 14 | V6 make_ready_days |
| Average listing lag (days) | Lower | 1 | 2 | 4 | 7 | BADS-derived |
| Average VDOM (days) | Lower | 14 | 21 | 30 | 45 | V6 vdom_days |
| Average pre-occupancy gap (days) | Lower | 3 | 5 | 10 | 18 | BADS-derived |
| Average vacancy cost per event ($) | Lower | $1,500 | $3,000 | $5,500 | $9,000 | BADS-derived |
| Annual turnover rate | Lower | 35% | 48% | 58% | 70% | V6 turnover_rate adapted |
| Average make-ready cost ($) | Lower | $1,200 | $2,500 | $4,000 | $6,500 | BADS-derived |
| Total tenant acquisition cost ($) | Lower | $3,000 | $5,500 | $8,500 | $13,000 | BADS-derived |
| Repeat turnover rate | Lower | 2% | 5% | 10% | 20% | V6 repeat_pct |
| Controllable turnover rate | Lower | 30% | 42% | 55% | 70% | BADS-derived |
| Aged vacancy percentage (>60 days) | Lower | 5% | 15% | 25% | 40% | BADS-derived |
| Shadow vacancy | Lower | 0.5% | 1.5% | 3% | 5% | BADS-derived |

---

### 6. Resident Retention

How the property retains residents and manages renewals.

| Item | Method | Weight | Divisor/Thresholds | Source |
|------|--------|--------|--------------------|--------|
| **Renewal rate** | Benchmark | 0.20 | see thresholds | V6 renewal_rate |
| **Average resident tenure** | Benchmark | 0.10 | see thresholds | BADS-derived |
| **Month-to-month percentage** | Benchmark | 0.10 | see thresholds | BADS-derived |
| **Long-tenure retention rate** | Benchmark | 0.10 | see thresholds | BADS-derived |
| **DNR rate** | Benchmark | 0.05 | see thresholds | BADS-derived |
| **Renewal & retention process** | Checklist | 0.25 | 110 pts | V6 Part 5C RENEW_ keys |
| **Resident mobile app** | Checklist | 0.10 | 80 pts | New — see breakdown below |
| **Resident communication** | Checklist | 0.10 | included in renewal process | V6 RENEW_ partial |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Renewal rate | Higher | 65% | 55% | 45% | 30% | V6 renewal_rate |
| Average resident tenure (months) | Higher | 36 | 27 | 20 | 12 | BADS-derived |
| Month-to-month percentage | Lower | 3% | 6% | 10% | 18% | BADS-derived |
| Long-tenure retention rate (2yr+) | Higher | 70% | 60% | 45% | 30% | BADS-derived |
| DNR rate | Lower | 2% | 4% | 7% | 12% | BADS-derived |

**New checklist point breakdown:**

**Resident mobile app** (80 pt divisor):
Per Y/N capability: Online Rent Payment 15 pts, Maintenance Requests 15 pts, Package Notifications 10 pts, Amenity Reservation 10 pts, Lease/Document Access 10 pts, Guest Access Management 8 pts, Resident Services Access 7 pts, Community Forum/Chat 5 pts.

---

### 7. Maintenance & Operations

How the property maintains the physical asset and handles service requests.

| Item | Method | Weight | Divisor/Thresholds | Source |
|------|--------|--------|--------------------|--------|
| **Emergency response time** | Benchmark | 0.10 | see thresholds | V6 MAINT_EMERG tiers |
| **Routine response time** | Benchmark | 0.10 | see thresholds | V6 MAINT_ROUTINE tiers |
| **Work order completion rate (30-day)** | Benchmark | 0.10 | see thresholds | BADS-derived |
| **First-time fix rate** | Benchmark | 0.08 | see thresholds | BADS-derived |
| **Work orders per unit (annual)** | Benchmark | 0.06 | see thresholds | BADS-derived |
| **Average work order cost** | Benchmark | 0.05 | see thresholds | BADS-derived |
| **Preventive vs reactive ratio** | Benchmark | 0.08 | see thresholds | BADS-derived |
| **Open work order age** | Benchmark | 0.08 | see thresholds | V6 wo_resolution_days adapted |
| **Maintenance cost per unit (annual)** | Benchmark | 0.07 | see thresholds | BADS-derived |
| **Maintenance operations process** | Checklist | 0.18 | 90 pts | V6 Part 5A MAINT_ keys |
| **Back-of-house condition** | Checklist | 0.10 | 50 pts | New — see breakdown below |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Emergency response time (hours) | Lower | 1 | 2 | 4 | 8 | V6 MAINT_EMERG tiers |
| Routine response time (hours) | Lower | 4 | 24 | 48 | 72 | V6 MAINT_ROUTINE tiers |
| Work order completion rate (30-day) | Higher | 98% | 95% | 88% | 80% | BADS-derived |
| First-time fix rate | Higher | 92% | 85% | 75% | 60% | BADS-derived |
| Work orders per unit (annual) | Optimal | 4 | 5 | 7 | 10 | BADS-derived (too low may = underreporting) |
| Average work order cost ($) | Lower | $75 | $125 | $200 | $350 | BADS-derived |
| Preventive vs reactive ratio | Higher | 30% | 22% | 12% | 5% | BADS-derived |
| Open work order age (days avg) | Lower | 3 | 7 | 14 | 25 | V6 wo_resolution_days adapted |
| Maintenance cost per unit ($/yr) | Lower | $1,500 | $2,200 | $3,200 | $4,500 | BADS-derived |

**New checklist point breakdown:**

**Back-of-house condition** (50 pt divisor):
Shop organization/cleanliness 10 pts, Parts inventory organized 8 pts, Safety equipment present 8 pts, Vehicle/equipment condition 7 pts, Proper chemical storage 7 pts, Tool inventory adequate 5 pts, Documentation/records maintained 5 pts.

---

### 8. Financial Health

How the property manages money — revenue, expenses, and NOI.

| Item | Method | Weight | Source |
|------|--------|--------|--------|
| **NOI margin** | Benchmark | 0.12 | BADS-derived |
| **NOI per unit** | Benchmark | 0.12 | V6 noi_per_unit |
| **Operating expense ratio** | Benchmark | 0.12 | V6 expense_ratio |
| **Payroll as % of revenue** | Benchmark | 0.08 | BADS-derived |
| **R&M per unit (annual)** | Benchmark | 0.07 | BADS-derived |
| **Marketing per unit (annual)** | Benchmark | 0.06 | BADS-derived |
| **Utility recovery rate** | Benchmark | 0.07 | BADS-derived |
| **Management fee as % of revenue** | Benchmark | 0.06 | BADS-derived |
| **Revenue growth (YoY)** | Benchmark | 0.08 | BADS-derived |
| **Expense growth (YoY)** | Benchmark | 0.08 | BADS-derived |
| **Insurance cost per unit** | Benchmark | 0.07 | BADS-derived |
| **Capital reserve adequacy** | Benchmark | 0.07 | BADS-derived |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| NOI margin | Higher | 62% | 55% | 45% | 35% | BADS-derived |
| NOI per unit ($/yr) | Higher | $8,000 | $6,000 | $4,000 | $2,000 | V6 noi_per_unit |
| Operating expense ratio | Lower | 40% | 48% | 58% | 68% | V6 expense_ratio adapted |
| Payroll as % of revenue | Lower | 10% | 13% | 17% | 22% | BADS-derived |
| R&M per unit ($/yr) | Lower | $700 | $1,000 | $1,400 | $2,000 | BADS-derived |
| Marketing per unit ($/yr) | Optimal | $300 | $450 | $600 | $800 | BADS-derived |
| Utility recovery rate | Higher | 92% | 80% | 65% | 45% | BADS-derived |
| Management fee as % of revenue | Lower | 3% | 4% | 5.5% | 7% | BADS-derived |
| Revenue growth (YoY) | Higher | 6% | 4% | 2% | 0% | BADS-derived |
| Expense growth (YoY) | Lower | 1% | 3% | 5% | 8% | BADS-derived |
| Insurance cost per unit ($/yr) | Lower | $400 | $600 | $850 | $1,200 | BADS-derived |
| Capital reserve adequacy | Higher | 5yr+ | 3yr | 1.5yr | <1yr | BADS-derived |

---

### 9. Collections & Screening

How the property screens applicants and collects what it's owed.

| Item | Method | Weight | Source |
|------|--------|--------|--------|
| **Current delinquency rate (units)** | Benchmark | 0.10 | V6 dq_at_risk_pct adapted |
| **Current delinquency rate (dollars)** | Benchmark | 0.10 | BADS-derived |
| **Bad debt write-off rate** | Benchmark | 0.12 | V6 bad_debt_pct |
| **Eviction rate** | Benchmark | 0.08 | BADS-derived |
| **Collections efficiency** | Benchmark | 0.10 | BADS-derived |
| **Application denial rate** | Benchmark | 0.06 | BADS-derived |
| **Screening turnaround time** | Benchmark | 0.06 | BADS-derived |
| **Short-tenure turnover rate** | Benchmark | 0.10 | V6 back_to_back_pct adapted |
| **Lease break rate** | Benchmark | 0.08 | BADS-derived |
| **Early move-out rate** | Benchmark | 0.08 | BADS-derived |
| **Screening process quality** | Checklist | 0.12 | 60 pts | New — see breakdown below |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Current delinquency rate (units) | Lower | 2% | 4% | 7% | 12% | V6 dq_at_risk_pct adapted |
| Current delinquency rate (dollars) | Lower | 1% | 2.5% | 4% | 7% | BADS-derived |
| Bad debt write-off rate | Lower | 0.5% | 1.5% | 3% | 5% | V6 bad_debt_pct |
| Eviction rate | Lower | 0.5% | 1.5% | 3% | 5% | BADS-derived |
| Collections efficiency | Higher | 80% | 68% | 55% | 40% | BADS-derived |
| Application denial rate | Optimal | 15% | 22% | 30% | 40% | BADS-derived (too low or high both bad) |
| Screening turnaround time (days) | Lower | 0.5 | 1 | 3 | 5 | BADS-derived |
| Short-tenure turnover rate (<6mo) | Lower | 4% | 8% | 14% | 22% | V6 back_to_back_pct adapted |
| Lease break rate | Lower | 5% | 12% | 18% | 28% | BADS-derived |
| Early move-out rate | Lower | 8% | 15% | 22% | 32% | BADS-derived |

**New checklist point breakdown:**

**Screening process quality** (60 pt divisor):
Credit check performed (Y/N) 12 pts, Background check performed 12 pts, Income verification 10 pts, Rental history verification 10 pts, Employment verification 8 pts, Turnaround speed (Same day 8 / 1-2 days 5 / 3-5 days 2 / 5+ days 0) max 8 pts.

---

### 10. Staffing & Technology

How the property staffs and equips itself.

| Item | Method | Weight | Divisor/Thresholds | Source |
|------|--------|--------|--------------------|--------|
| **Units per leasing agent** | Benchmark | 0.14 | see thresholds | BADS-derived |
| **Units per maintenance tech** | Benchmark | 0.14 | see thresholds | BADS-derived |
| **Staff turnover rate** | Benchmark | 0.14 | see thresholds | BADS-derived |
| **Average staff tenure** | Benchmark | 0.12 | see thresholds | BADS-derived |
| **PM tenure** | Benchmark | 0.12 | see thresholds | BADS-derived |
| **Open position rate** | Benchmark | 0.10 | see thresholds | BADS-derived |
| **Technology effectiveness** | Checklist | 0.24 | 125 pts | V6 Part 6 TECH_ keys |

**Benchmark thresholds:**

| Item | Dir | Excellent | Good | Concern | Poor | Source |
|------|-----|-----------|------|---------|------|--------|
| Units per leasing agent | Optimal | 120 | 150 | 200 | 250 | BADS-derived (too low = overstaffed) |
| Units per maintenance tech | Optimal | 80 | 100 | 130 | 175 | BADS-derived (too low = overstaffed) |
| Staff turnover rate | Lower | 15% | 28% | 42% | 60% | BADS-derived |
| Average staff tenure (months) | Higher | 30 | 20 | 12 | 6 | BADS-derived |
| PM tenure (months) | Higher | 24 | 14 | 8 | 4 | BADS-derived |
| Open position rate | Lower | 3% | 8% | 15% | 25% | BADS-derived |

---

### Competitive Position (Scored Separately)

These items use Method 3 (Competitive) and produce a separate competitive position profile. They are NOT blended into the category scores above because they measure relative position, not absolute performance.

| Item | Method | Weight | Data Source |
|------|--------|--------|-------------|
| **Rent per SF vs comp average** | Competitive | 0.15 | PM Rent Roll vs Competitive Analysis 5.9 |
| **Building amenity count vs comps** | Competitive | 0.10 | Intake 3.2 vs Competitive 5.2 |
| **Unit amenity count vs comps** | Competitive | 0.08 | Intake 3.4 vs Competitive 5.3 |
| **Resident services vs comps** | Competitive | 0.06 | Intake 3.6 vs Competitive 5.4 |
| **Online reputation score vs comps** | Competitive | 0.12 | Intake 3.8 vs Competitive 5.7 |
| **Review volume vs comps** | Competitive | 0.06 | Intake 3.8 vs Competitive 5.7 |
| **Digital presence vs comps** | Competitive | 0.06 | Intake 3.9 vs Competitive 5.8 |
| **Mystery shop score vs comps** | Competitive | 0.12 | Mystery Shop 4.x (subject) vs Competitive Mystery Shop |
| **Mobile app capabilities vs comps** | Competitive | 0.05 | Intake 3.6 vs Competitive 5.6 |
| **Resident events vs comps** | Competitive | 0.04 | Intake 3.5 vs Competitive 5.5 |
| **Occupancy vs comp average** | Competitive | 0.10 | PM 1.1 vs Competitive 5.1 (if available) |
| **Concession level vs comps** | Competitive | 0.06 | PM charge codes vs Competitive 5.9 pricing |

---

## Category Weights

How the 10 dimension scores roll up into the overall asset score. Derived from mapping V6's 19 module weights to the new 10 dimensions, adjusted for the broader scope of the new model.

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **Physical Asset** | 0.08 | Product foundation; heavily weighted in competitive position separately |
| **Marketing & Visibility** | 0.10 | Demand generation; directly impacts lead volume and quality |
| **Leasing & Sales** | 0.15 | Revenue conversion; where the property monetizes its product and marketing |
| **Pricing & Revenue** | 0.14 | Revenue health and optimization; top-line performance |
| **Vacancy & Turns** | 0.12 | Largest single controllable cost center for most properties |
| **Resident Retention** | 0.10 | Renewal economics dominate long-term financial performance |
| **Maintenance & Operations** | 0.10 | Asset preservation and resident satisfaction driver |
| **Financial Health** | 0.10 | Bottom-line outcome; reflects whether all other dimensions are working |
| **Collections & Screening** | 0.06 | Risk management; smaller weight because it affects fewer units |
| **Staffing & Technology** | 0.05 | Enabling infrastructure; impacts all other dimensions indirectly |
| **Total** | **1.00** | |

V6 module weight mapping reference: V6 gave VDOM (0.10) + Pricing (0.10) + Occupancy (0.08) + Financial (0.10) = 0.38 to financial/operational metrics. V6 gave Marketing (0.08) + Listings (0.05) + Lead Mgmt (0.05) + Leasing Team (0.05) + Tour (0.05) = 0.28 to marketing/leasing. V6 gave Technology (0.03) + Staffing (0.02) + Management (0.02) + Screening (0.01) + Collections (0.01) + Pet (0.01) = 0.10 to support functions. The new weights maintain similar proportions while redistributing across the new 10-dimension structure.

---

## Rollup Structure

### Item → Category Score

```
Category Score = Σ (Item Score × Item Weight) / Σ (Item Weight)
```

Only items with data contribute. Missing items are excluded from the weighted average (not scored as zero).

**Minimum coverage rule:** A category score requires data for at least 40% of defined items (by weight) to report a score. Below that threshold, the category is flagged as "insufficient data." The system tracks coverage percentage per category.

### Category → Overall Asset Score

```
Overall Score = Σ (Category Score × Category Weight) / Σ (Category Weight)
```

If a category has insufficient data, it is excluded from the overall calculation. The system flags a data coverage warning if scored weight falls below 70% of total defined weight.

### Competitive Position — Separate Profile

The competitive position scores do NOT roll into the overall asset score. They produce:

- Per-item competitive scores (above/at/below market on each dimension)
- Composite competitive position index (weighted average of all competitive scores)
- Value score: quality index (checklist-derived product quality) / price index (rent position vs comps)

This separation exists because competitive position changes with every engagement (different comp set), while the absolute performance scores are comparable across engagements.

---

## Scale and Grade Mapping

**Scale:** 0–10 with two decimal places.

**Grade bands:**

| Grade | Score Range | Label | V6 Tier Reference |
|-------|-----------|-------|-------------------|
| A | 8.00–10.00 | Excellent | V6 Tier 1: Optimization |
| B | 5.50–7.99 | Good | V6 Tier 2: Repositioning |
| C | 3.50–5.49 | Average | V6 Tier 3: Turnaround (upper) |
| D | 2.00–3.49 | Below Average | V6 Tier 3: Turnaround (lower) |
| F | 0.00–1.99 | Poor | V6 Tier 4: Custom |

Grade bands are metadata — configurable per engagement or portfolio without changing the scoring logic. The A threshold at 8.00 aligns with V6's Tier 1 cutoff. A property scoring "good" (7.5) on everything earns a B, which is correct — a B means the property is performing well but has room for improvement.

---

## Benchmark Override Rules

Default benchmarks come from the threshold tables above. Overrides adjust benchmarks for context:

**Level 1 — Property class adjustment:** Some thresholds shift by class. Examples: NOI margin Class A 55–65% vs Class B/C 45–55%. Operating expense ratio Class A 35–45% vs Class B/C 45–55%. Revenue per unit varies significantly by class and market.

**Level 2 — Per-engagement adjustment:** The consultant adjusts specific benchmarks based on the competitive data collected for this engagement and submarket conditions.

**Level 3 — Portfolio-level defaults:** For recurring clients with multiple properties, the consultant can define a portfolio-level benchmark set.

Override precedence: engagement-specific > portfolio-level > class-adjusted default > default.

All overrides are versioned. Any score can be traced back to the specific benchmark thresholds in effect when it was computed.

---

## Compliance Flags

Items tracked outside the scoring model as PASS or FLAG:

| Item | Source | Trigger |
|------|--------|---------|
| Fair housing compliance | Mystery Shop Section 7 | Any discriminatory behavior observed |
| Fire/safety inspection current | Intake 10.5 | Inspection lapsed (>365 days) |
| Open fire code violations | Intake 10.5 | Any open violation |
| ADA compliance | Field audit observations | Accessibility barriers noted |

Flags are surfaced prominently in the impact summary (Layer 5) regardless of their financial impact because they represent legal/safety risk.

---

## Confidence Modifiers

Data integrity affects the confidence attached to scores, not the scores themselves.

| Contradiction Density | Confidence Level |
|----------------------|-----------------|
| <5% | High — scores are well-supported by consistent data |
| 5–15% | Moderate — some data conflicts exist; scores should be interpreted with caution in affected areas |
| >15% | Low — significant data conflicts; PM-derived scores may not reflect reality |

Each score carries a confidence tag based on the contradiction density in its data sources.

---

## Item Count Summary

| Dimension | Benchmark | Checklist | Competitive | Total |
|-----------|-----------|-----------|-------------|-------|
| Physical Asset | 0 | 14 | 0 | 14 |
| Marketing & Visibility | 2 | 9 | 0 | 11 |
| Leasing & Sales | 9 | 9 | 0 | 18 |
| Pricing & Revenue | 16 | 0 | 0 | 16 |
| Vacancy & Turns | 13 | 0 | 0 | 13 |
| Resident Retention | 5 | 3 | 0 | 8 |
| Maintenance & Operations | 9 | 2 | 0 | 11 |
| Financial Health | 12 | 0 | 0 | 12 |
| Collections & Screening | 10 | 1 | 0 | 11 |
| Staffing & Technology | 6 | 1 | 0 | 7 |
| Competitive Position | 0 | 0 | 12 | 12 |
| **Total** | **82** | **39** | **12** | **133** |

Plus 4 compliance flags and 1 confidence modifier system.

---

## Reference Documents

- **Basic Analytic Data Set** — 124 KPIs with benchmarks used for benchmark-method items (`REBOOT/RBv2/Basic_Analytic_Data_Set.md`)
- **Complete Data Inventory** — all 1,100+ fields referenced as data sources (`REBOOT/RBv2/Complete_Data_Inventory.md`)
- **Analytical Engine Specification** — Layer 1 definition that this scoring model implements (`REBOOT/RBv2/Analytical_Engine_Specification.md`)
- **V6 Scoring Rubric Specification** — source for reusable checklist point systems (`Version 6/Working Docs/Spec Docs/Scoring_Rubric_Specification.md`)
- **V6 ScoringEngine.gs** — source for reusable benchmark thresholds and interpolation functions (`Version 6/CODEBASE/ScoringEngine.gs`)
