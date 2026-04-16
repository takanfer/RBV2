# Basic Analytic Data Set

Standard property performance KPIs computed from ingested data and benchmarked against industry standards. This is the foundational metrics layer — the property's vital signs — computed before the five analytical layers run.

---

## Purpose

Every property assessment begins with the same question: where does this property stand on every standard performance metric? The Basic Analytic Data Set answers that question by computing a fixed set of KPIs from the ingested PM Data Set and Audit Data Set, then comparing each to industry benchmarks.

This layer serves three functions:

1. **Baseline snapshot** — an immediate performance profile available as soon as data is ingested, before any diagnostic analysis runs
2. **Benchmark reference** — industry-standard thresholds that contextualize every computed metric (is this number good, acceptable, or a problem?)
3. **Feed to analytical layers** — Layer 1 (Scoring) uses these KPIs and benchmarks as inputs for grading; Layers 2–4 reference them for cohort ranking, diagnostic answers, and anomaly detection; Layer 5 uses them for financial impact quantification

---

## Relationship to the Analytical Engine

```
┌─────────────────────────────────────────────────────┐
│           ALL DATA (1,100+ Fields)                  │
│       PM Data Set  +  Audit Data Set  +  CRM        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│        Basic Analytic Data Set (This Document)      │
│    Standard KPIs + Industry Benchmarks              │
│    Always computed · Always available                │
└──────────┬────────────────────────────────┬─────────┘
           │                                │
           ▼                                ▼
┌─────────────────────┐    ┌──────────────────────────┐
│  Layer 1: Scoring   │    │  Layers 2–5 + AI Layer   │
│  (uses KPIs +       │    │  (reference KPIs for     │
│   benchmarks for    │    │   ranking, diagnostics,  │
│   field grades)     │    │   anomaly detection,     │
│                     │    │   impact quantification) │
└─────────────────────┘    └──────────────────────────┘
```

The Basic Analytic Data Set does not replace any analytical layer. It is a pre-computed foundation that all layers consume.

---

## KPI Categories

### 1. Occupancy & Vacancy

**Key distinction:** Total Vacant Days and VDOM are different measurements with different accountability.

- **Total Vacant Days** = the entire non-revenue period from move-out to rent responsibility start. This is the basis for **vacancy cost** — every day in this span is a day the unit generates zero revenue regardless of what phase it's in.
- **VDOM (Vacant Days on Market)** = only the days after a unit is ready AND represented by leasing activity (make-ready complete + listing live or actively being shown) until a lease is signed. This isolates **leasing team performance** — how long does it take to convert a market-ready unit into a signed lease?

The vacancy lifecycle phases that compose Total Vacant Days are:

```
Move-Out → Make-Ready Complete → Listed/Shown → Lease Signed → Rent Responsibility Start
|__________|___________________|_______________|______________|
  Make-Ready    Listing Lag          VDOM        Pre-Occupancy
  (Maintenance)  (Coordination)    (Leasing)      Gap (Admin)
|_____________________________________________________________|
                    Total Vacant Days
                    (Vacancy Cost basis)
```

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| **Occupancy** | | | | |
| Physical Occupancy Rate | Occupied units / Total units | 93–95% | Class A urban: 94–96%; Class B/C suburban: 92–95% | PM 1.1: Occupancy Status, Total Units (Intake 3.1) |
| Economic Occupancy Rate | Net rental income / Gross potential rent | 88–92% | Gap from physical occupancy reveals concession and delinquency drag | PM 1.6: Net Rental Income, GPR |
| Physical-to-Economic Occupancy Gap | Physical occupancy − Economic occupancy | <3–5 points | Gap >5 points = significant concession or delinquency issue | Derived from above |
| Vacancy Rate by Unit Type | Vacant units of type / Total units of type | Varies by market | Compare to submarket vacancy rate (Intake 3.3) | PM 1.1 + PM 1.5 |
| **Total Vacancy Duration** | | | | |
| Average Total Vacant Days | Mean of (Rent Responsibility Start − Move-Out) across events | 30–45 days | Full non-revenue period; sum of all phases below | Upload 7.3: Vacancy Timeline |
| **Vacancy Lifecycle Phases** | | | | |
| Average Make-Ready Duration | Mean of (Make-Ready Complete − Move-Out) | 5–7 days | Maintenance accountability; >10 days = capacity or process problem | Upload 7.3: Make-Ready Complete, Move-Out |
| Average Listing Lag | Mean of (Listing Live or Shown − Make-Ready Complete) | 1–3 days | Coordination accountability; >5 days = units sitting ready with no market representation | Upload 7.3: Listing Live, Make-Ready Complete |
| Average VDOM | Mean of (Lease Signed − MAX(Make-Ready Complete, Listing Live)) | 14–21 days | Leasing accountability; how long to convert a ready, represented unit into a signed lease. Tight markets: 7–14 days | Upload 7.3: Lease Signed, Make-Ready Complete, Listing Live |
| Average Pre-Occupancy Gap | Mean of (Rent Responsibility Start − Lease Signed) | 3–7 days | Admin accountability; gap between closing and revenue start. >14 days = scheduling or process failure | Upload 7.3: Lease Start, Lease Signed |
| **Vacancy Financial Impact** | | | | |
| Average Vacancy Cost Per Event | Mean of (Total Vacant Days × Daily Rent) per event | $2,000–$5,000 | Total revenue lost across ALL phases of vacancy; the full cost of one turnover's non-revenue period | Upload 7.3: Total Vacant Days × (Asking Rent / 30) |
| Average VDOM Cost Per Event | Mean of (VDOM Days × Daily Rent) per event | $1,000–$3,000 | Revenue lost specifically during the leasing conversion phase; a subset of total vacancy cost | Upload 7.3: VDOM Days × (Asking Rent / 30) |
| Average Make-Ready Vacancy Cost | Mean of (Make-Ready Days × Daily Rent) per event | $500–$1,500 | Revenue lost while maintenance turns the unit; a subset of total vacancy cost | Upload 7.3: Make-Ready Days × (Asking Rent / 30) |
| Average Listing Lag Cost | Mean of (Listing Lag Days × Daily Rent) per event | $100–$500 | Revenue lost from coordination gap between ready and marketed; often the most fixable cost | Upload 7.3: Listing Lag Days × (Asking Rent / 30) |
| Average Pre-Occupancy Cost | Mean of (Pre-Occ Gap Days × Daily Rent) per event | $200–$700 | Revenue lost from scheduling gap between signing and rent start | Upload 7.3: Pre-Occ Gap × (Asking Rent / 30) |
| Annual Total Vacancy Loss | Sum of all vacancy costs across all events | — | The property-wide annual dollar cost of all non-revenue days | PM 1.6: Vacancy Loss or sum of per-event costs |
| Daily Vacancy Bleed Rate | Sum of (Daily Rent) for all currently vacant units | — | What the property is losing right now, today, per day | PM 1.5: Asking Rent for each vacant unit / 30 |
| **Vacancy Status & Forward Risk** | | | | |
| Aged Vacancy Percentage | Units vacant >60 days / Total vacant units | <15–20% | High percentage = stale inventory problem | PM 1.5: Days Vacant |
| Shadow Vacancy | Non-revenue units (models, employee, guest) / Total units | <1–2% | Each non-revenue unit costs GPR equivalent annually | PM 1.1: Occupancy Status |
| Trend Occupancy (30/60/90 Day) | Projected occupancy based on NTVs + lease expirations − expected signings | Stable or improving | Declining trend = forward risk | PM 1.1 + PM 1.10 |

### 2. Revenue

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Revenue Per Unit (RPU) | Total revenue / Total units / 12 | Varies by market | Compare to submarket avg rent (Intake 3.3) | PM 1.6: Total Revenue, Total Units (Intake 3.1) |
| Revenue Per Available Unit (RevPAU) | Total revenue / Total units / 12 (includes vacancy drag) | Compare to RPU | Gap between RPU and RevPAU = vacancy cost impact on revenue | PM 1.6: Total Revenue |
| Revenue Per Square Foot | Total revenue / Total rentable SF / 12 | Varies by market | Normalize for unit size differences; compare to submarket Avg Rent/SF (Intake 3.3) | PM 1.6 + Intake 3.1: Total Sq Ft |
| Gross Potential Rent (GPR) | Sum of market rent for all units | N/A (baseline reference) | — | PM 1.6: GPR or PM 1.1: Market Rent × units |
| Loss-to-Lease Percentage | Loss to lease / GPR | <3–5% | >5% = systematic underpricing or long-tenure drift | PM 1.6: Loss to Lease, GPR |
| Loss-to-Lease Total Annual | Sum of (Market Rent − Current Rent) × 12 for all units | — | Dollar magnitude of pricing gap | PM 1.1: Market Rent, Current Monthly Rent |
| Concession Percentage of GPR | Total concessions / GPR | <2–3% | >5% = pricing strategy or market softness issue | PM 1.6: Concessions, GPR |
| Bad Debt Percentage of GPR | Bad debt write-offs / GPR | <1–2% | >2% = screening or collections failure | PM 1.6: Bad Debt, GPR |
| Other Income Per Unit | Other income / Total units / 12 | $75–$150/unit/month | Includes parking, pet, trash, utility reimbursement, fees | PM 1.6: Other Income |
| Net Effective Rent | Average (Gross Rent − Amortized Concession) | Compare to asking rent | Gap = concession burn rate | PM 1.7: Charge codes + PM 1.1 |
| Rent Lift on Turnover | Average (New Lease Rent − Prior Tenant Rent) | Positive, 3–8% | Negative rent lift = declining market position or desperate leasing | Upload 7.3 or 7.6: Prior/New rent |
| Renewal Rent Increase | Average increase at renewal | 3–5% | Below market rent growth = loss-to-lease acceleration; above = turnover risk | PM 1.3: Prior Rent, New Rent |

### 3. Expense

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Total OpEx Per Unit | Total operating expenses / Total units / 12 | $500–$900/unit/month | Class A: $700–$900; Class B/C: $500–$750; varies significantly by region | PM 1.6: Total OpEx |
| Operating Expense Ratio | Total OpEx / Total Revenue | 35–50% | Class A: 35–45%; Class B/C: 45–55% | PM 1.6: Total OpEx, Total Revenue |
| Payroll as % of Revenue | Payroll & benefits / Total revenue | 12–15% | >18% = overstaffed or overpaid relative to revenue; <10% = possible understaffing | PM 1.6: Payroll, Total Revenue |
| Payroll Per Unit | Payroll & benefits / Total units / 12 | $100–$175/unit/month | — | PM 1.6: Payroll |
| R&M Per Unit (Annual) | Repairs & maintenance / Total units | $800–$1,200/unit/year | Older assets trend higher; <$600 may indicate deferred maintenance | PM 1.6: R&M |
| Contract Services Per Unit | Contract services / Total units / 12 | Varies | High contract + low in-house headcount = outsourced model; compare to R&M | PM 1.6: Contract Services |
| Make-Ready/Turnover Cost Per Unit | Turnover expense / Total units / 12 | $150–$300/unit/month | Or per-event: $1,500–$3,500 per turn (standard), $5,000+ (heavy) | PM 1.6: Make-Ready |
| Marketing Per Unit (Annual) | Marketing & advertising / Total units | $200–$500/unit/year | >$500 with low occupancy = buying occupancy; <$150 with high vacancy = underinvesting | PM 1.6: Marketing |
| Insurance Per Unit (Annual) | Insurance / Total units | $400–$800/unit/year | Trending up nationally 10–15%/year; spikes may indicate claims history | PM 1.6: Insurance |
| Real Estate Tax Per Unit (Annual) | Taxes / Total units | Varies by jurisdiction | Compare to local mill rate; recent reassessment may indicate appeal opportunity | PM 1.6: Taxes |
| Utility Cost Per Unit (Gross) | Utility expense / Total units / 12 | $75–$150/unit/month | — | PM 1.6: Utilities |
| Utility Recovery Rate | Utility reimbursement / Gross utility expense | 70–90% | <70% with RUBS = billing leakage; submetered properties should approach 90%+ | Intake 3.23: Utility Reimbursements / PM 1.6: Utilities |
| Management Fee as % of Revenue | Management fee / Total revenue | 3–5% | >5% = premium management or fee structure issue | PM 1.6: Management Fee, Total Revenue |
| Vacant Unit Utility Cost | Estimated utility cost for vacant units (per month) | Minimize | Properties paying full utilities on vacant units with no smart thermostat controls bleed unnecessarily | PM 1.5 (vacant count) × estimated utility per unit |

### 4. NOI & Financial Health

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Net Operating Income (NOI) | Total revenue − Total OpEx | — | Absolute number; context depends on asset size and market | PM 1.6: NOI |
| NOI Per Unit (Annual) | NOI / Total units | $6,000–$12,000/unit/year | Class A urban: $10,000–$15,000+; Class B/C: $5,000–$9,000 | PM 1.6: NOI |
| NOI Margin | NOI / Total revenue | 50–65% | Class A: 55–65%; Class B/C: 45–55% | PM 1.6: NOI, Total Revenue |
| NOI Trend (12-Month) | NOI month-over-month trajectory | Stable or growing | Declining NOI with stable occupancy = expense creep or revenue erosion | PM 1.6: Monthly NOI |
| Revenue Growth (YoY) | Current 12-month revenue / Prior 12-month revenue − 1 | 3–5% | Below market rent growth rate = falling behind | PM 1.6: Monthly Revenue |
| Expense Growth (YoY) | Current 12-month OpEx / Prior 12-month OpEx − 1 | <3–4% | Expense growth exceeding revenue growth = margin compression | PM 1.6: Monthly OpEx |
| Vacancy Loss as % of GPR | Vacancy loss / GPR | <5–7% | >7% = occupancy or pricing problem | PM 1.6: Vacancy Loss, GPR |
| Total Revenue Loss (Vacancy + Concessions + Bad Debt) | (Vacancy loss + Concessions + Bad debt) / GPR | <8–12% | Single number capturing all revenue leakage | PM 1.6 |

### 5. Turnover

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Annual Turnover Rate | Move-outs in 12 months / Total units | 45–55% | <40% = strong retention; >60% = retention crisis | PM 1.2: Move-out events |
| Average Make-Ready Duration (Days) | Mean of (Make-Ready Complete − Move-Out) | 5–7 days standard | >10 days = capacity or process issue; >15 days = critical | Upload 7.3: Vacancy Timeline |
| Average Make-Ready Cost | Mean of total turn cost per event | $1,500–$3,500 | Standard turn; heavy turns $3,500–$6,000; full renovation $8,000+ | Upload 7.4: Turnover Records |
| Make-Ready Cost Breakdown | % cleaning / paint / flooring / appliance / other | Cleaning 15–20%, Paint 20–25%, Flooring 15–25%, Appliance 10–15%, Other 15–25% | Disproportionate categories indicate specific issues | Upload 7.4: Cost breakdown fields |
| Total Tenant Acquisition Cost | Vacancy loss + Make-ready cost + Concession + Commission + Marketing allocation | $4,000–$8,500 | Single most important number for the retention business case | Derived: Upload 7.3 + 7.4 + 7.6 |
| Acquisition-to-Retention Cost Ratio | Acquisition cost / Average retention cost per renewal | 15:1 to 25:1 | Higher ratio = stronger financial case for retention investment | Derived |
| Repeat Turnover Rate | Units with 2+ vacancy events in 12 months / Total units | <3–5% | >5% = screening, placement, or unit condition issue | PM 1.2: Unit-level event count |
| Controllable Turnover Rate | Move-outs for controllable reasons / Total move-outs | <40–50% | Controllable = maintenance, management, service; uncontrollable = job transfer, home purchase, life change | PM 1.2: Move-out reason classification |

### 6. Leasing Performance

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Lead Volume (Monthly) | Total leads received per month | Varies by size/market | Track trend, not absolute; declining volume with stable spend = channel fatigue | Intake 3.15 or CRM (Section 2) |
| Lead-to-Tour Conversion Rate | Tours / Leads | 35–50% | <25% = lead quality or response time issue | Intake 3.15: Leads, Tours |
| Tour-to-Application Rate | Applications / Tours | 40–55% | <30% = tour experience, pricing, or product issue | Intake 3.15: Tours, Applications |
| Application-to-Lease Rate | Leases / Applications | 75–85% | <60% = screening too strict, process friction, or applicant fallout | Intake 3.15: Applications, Leases |
| Lead-to-Lease Conversion Rate | Leases / Leads | 10–15% | <5% = systemic funnel failure; >20% = strong or low volume | Intake 3.15: Leads, Leases |
| Ghost/No-Show Rate | No-shows / Scheduled tours | <10–15% | >25% = confirmation process failure or poor lead quality | Intake 3.15: Tour No-Shows, Tours |
| Average Lead Response Time (Email) | Mean minutes to first response | <60 minutes | <30 min = excellent; >4 hours = critical | Intake 3.14: Avg Email Response Time |
| Average Lead Response Time (Phone) | Mean minutes to first response | <30 minutes | <15 min = excellent; >2 hours = critical | Intake 3.14: Avg Phone Response Time |
| Cost Per Lead | Total marketing spend / Total leads | $50–$150 | Varies heavily by market; track by source for actionable data | Intake 3.24 (Marketing spend) / Intake 3.15 (Leads) |
| Cost Per Lease | Total marketing spend / Total leases signed | $500–$1,500 | Includes all marketing channels; benchmark against acquisition cost | Intake 3.24 / Intake 3.15 |
| Sales Velocity | Average days from first contact to signed lease | 14–30 days | Tight markets: 7–14 days; soft markets: 30–45 days | Intake 3.15: Avg Days Lead→Tour→App→Lease |
| Follow-Up Touch Count | Average number of follow-up contacts per prospect | 5–8 touches | <3 = giving up too early; >10 = inefficient targeting | Intake 3.14: Follow-Up Touch Count |

### 7. Retention & Renewals

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Renewal Rate | Renewals / Expiring leases | 50–55% | >60% = strong; <45% = retention crisis | PM 1.3 or Intake 3.15 |
| Average Resident Tenure | Mean months from move-in to move-out (or current) | 24–30 months | Longer tenure = lower turnover cost but higher loss-to-lease risk | PM 1.1: Move-In Date + PM 1.2: Move-Out Date |
| Month-to-Month Percentage | MTM leases / Total occupied units | <5–8% | >10% = renewal process failure or holdover management gap | PM 1.1: Lease End Date vs. current date |
| MTM Premium Applied | Whether holdover premium is being charged | Yes, typically 10–25% premium | Not charging MTM premium = leaving money on the table | Intake 3.21: Holdover Rate Premium |
| Renewal Outreach Timeline | Days before expiration that renewal offer is sent | 90–120 days | <60 days = too late; increases MTM risk and reduces negotiation leverage | Intake 3.21: Renewal Outreach Timeline |
| Average Renewal Rent Increase | Mean percentage increase at renewal | 3–5% | Below submarket YoY rent growth = accelerating loss-to-lease | PM 1.3: Prior Rent, New Rent |
| Long-Tenure Retention Rate | Renewal rate for residents with 2+ years tenure | >60% | If lower than overall renewal rate = long-term residents being pushed out by increases | PM 1.3 + PM 1.1: Tenure calculation |
| DNR Rate | Do-not-renew decisions / Total expiring leases | <3–5% | >5% = possible overuse; audit for consistency | Intake 3.21: DNR process fields |

### 8. Maintenance & Work Orders

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Work Orders Per Unit (Annual) | Total work orders / Total units | 3–5/unit/year | >6 = aging asset or deferred maintenance; <2 = possible underreporting | PM 1.4: Work order count |
| Emergency Response Time | Average hours from request to first action (emergency) | <2 hours | >4 hours = staffing or process failure | Intake 3.20: Emergency Response Time |
| Routine Response Time | Average hours from request to first action (routine) | <24 hours | >48 hours = backlog or capacity issue | Intake 3.20: Routine Response Time |
| Work Order Completion Rate (30-Day) | Orders resolved within 30 days / Total orders | >95% | <90% = chronic backlog | Intake 3.20: Resolution time buckets |
| First-Time Fix Rate | Orders resolved without follow-up for same issue / Total orders | >85% | <75% = quality issue, training gap, or parts availability | PM 1.4: Repeat WOs on same unit/category |
| Average Work Order Cost | Total WO cost / Total work orders | $75–$200 | Excludes make-ready; higher = vendor-heavy or complex repairs | PM 1.4: Cost |
| Preventive vs. Reactive Ratio | PM scheduled tasks / Total work orders | 20–30% preventive | <10% preventive = fully reactive maintenance culture | Intake 3.20: PM Program fields + PM 1.4 |
| Open Work Order Age | Average days open for currently unresolved orders | <7 days | >14 days average = systemic backlog | PM 1.4: Date Created, Status |
| Maintenance Cost Per Unit (Annual) | (R&M + Contract Services + Make-Ready) / Total units | $1,500–$3,000/unit/year | Combined maintenance burden; compare to asset age | PM 1.6: R&M + Contract + Make-Ready |

### 9. Delinquency & Collections

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Current Delinquency Rate (Units) | Units with balance >0 / Occupied units | <3–5% | >8% = screening or collections crisis | PM 1.11: Units with balance / PM 1.1: Occupied count |
| Current Delinquency Rate (Dollars) | Total outstanding balance / Monthly GPR | <2–3% | Dollar rate more meaningful than unit rate for severity | PM 1.11: Total balance / PM 1.6: GPR |
| Delinquency Aging — 0-30 Days | Sum of 0-30 day balances | — | Recent delinquency; may self-cure | PM 1.11: 0-30 Days |
| Delinquency Aging — 31-60 Days | Sum of 31-60 day balances | — | Persistent delinquency; collections intervention needed | PM 1.11: 31-60 Days |
| Delinquency Aging — 61-90 Days | Sum of 61-90 day balances | — | Chronic; likely heading to legal | PM 1.11: 61-90 Days |
| Delinquency Aging — 90+ Days | Sum of 90+ day balances | — | Write-off candidate; eviction likely | PM 1.11: 90+ Days |
| Bad Debt Write-Off Rate | Annual write-offs / Annual GPR | <1–2% | >2% = screening failure or collections process breakdown | PM 1.6: Bad Debt |
| Eviction Rate | Evictions filed / Total units | <1–2% | >3% = systemic screening or management issue; each eviction costs $3,500–$7,000+ | PM 1.11: Eviction Filed |
| Collections Efficiency | Amount collected on delinquent accounts / Total delinquent balance | >60–70% | Below 50% = collections process is not working | PM 1.11: Balance changes over time |
| Late Fee Enforcement | Late fees collected / Delinquent unit-months | Consistent application | Inconsistent enforcement = fair housing risk and revenue loss | Intake 3.23: Late Fees / PM 1.11 |

### 10. Staffing & Organization

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Units Per Leasing Agent | Total units / Leasing agent count | 100–150 units/agent | <75 = overstaffed; >200 = understaffed | Intake 3.19: Leasing Agent Count / Intake 3.1: Total Units |
| Units Per Maintenance Tech | Total units / Maintenance tech count | 75–100 units/tech | <60 = overstaffed; >125 = understaffed; adjust for asset age | Intake 3.19: Maintenance Tech Count |
| Staff Turnover Rate | Annual voluntary departures / Total staff | <30% | >40% = compensation, culture, or management issue; impacts operational continuity | Intake 3.19: Staff Turnover Rate |
| Average Staff Tenure | Mean months of employment for current staff | >18 months | <12 months average = chronic turnover environment | Intake 3.19: Avg Staff Tenure |
| Compensation vs. Market | Self-reported position relative to market | At or above market | Below market in all roles = retention risk and hiring difficulty | Intake 3.19: Overall Comp vs Market |
| Open Position Rate | Open positions / Total authorized positions | <5–10% | >10% for extended period = operational strain | Intake 3.19: Open Positions / Total staff |
| PM Tenure | Property manager months in role | >12 months | <6 months = transition risk; PM turnover correlates with data quality degradation | Intake 3.19: PM Tenure |

### 11. Pet Policy & Revenue

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Pet Revenue Per Unit (Annual) | Total pet revenue / Total units | $30–$60/unit/year | Growing revenue category; benchmark against comp set | Intake 3.23: Pet Revenue |
| Pet Rent vs. Market | Property pet rent / Comp average pet rent | At or above market | Underpriced pet rent = fee leakage | PM 1.7: Pet charge codes / Competitive 5.11 |
| Pet Deposit Adequacy | Average pet deposit / Average pet-related damage cost | >1.0x | <1.0 = deposits don't cover average damage | Intake 3.23 + PM 1.4 (pet-related WOs) |
| Pet Penetration Rate | Units with pets / Occupied units | 40–60% (market-dependent) | Low penetration with pet-friendly policy = marketing gap for pet amenities | PM 1.7: Pet charge code presence |
| ESA/Service Animal Percentage | ESA/SA units / Total pet units | Track, no benchmark | Rising ESA percentage = potential policy compliance risk; no pet revenue from these units | PM 1.7: Charge code analysis (no pet charges on occupied units with pets) |

### 12. Screening & Placement Quality

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Application Denial Rate | Denied applications / Total applications | 10–20% | <5% = criteria too loose; >30% = criteria too strict or poor lead quality | Intake 3.18: Denial Rate |
| Screening Turnaround Time | Average days from application to decision | Same day to 1–2 days | >3 days = friction that loses applicants to competitors | Intake 3.18: Screening Turnaround Time |
| Short-Tenure Turnover Rate | Move-outs within 6 months / Total move-ins | <8–10% | >15% = screening failure or expectation mismatch | PM 1.2: Events where tenure <6 months |
| Lease Break Rate | Lease breaks / Total move-outs | <10–15% | >20% = screening, placement quality, or product issue | PM 1.2: Move-out reason = lease break |
| Early Move-Out Rate | Move-outs before lease expiration / Total move-outs | <15–20% | High rate concentrated in specific units/types = product problem, not screening problem | PM 1.2: Move-out date vs. Lease end date |

### 13. Insurance & Risk

| KPI | Calculation | Benchmark | Class/Market Notes | Data Source |
|-----|-------------|-----------|-------------------|-------------|
| Insurance Cost Per Unit (Annual) | Insurance expense / Total units | $400–$800/unit/year | Trending up 10–15% nationally; significant regional variation | PM 1.6: Insurance |
| Insurance as % of Revenue | Insurance / Total revenue | 3–5% | >6% = claims history, high-risk profile, or shopping opportunity | PM 1.6: Insurance, Total Revenue |
| Open Safety Violations | Count of unresolved fire/building code violations | 0 | Any open violation = immediate risk; correlates with higher insurance | Intake 10.5: Open Fire Code Violations |
| Capital Reserve Adequacy | Capital reserves / Estimated replacement cost of aging systems | Sufficient to cover 3–5 year replacement cycle | Underfunded reserves = deferred maintenance time bomb | Intake 3.24: Capital Reserves + Intake 10.4: Asset condition/age |
| Fire/Safety Inspection Currency | Days since last fire inspection | <365 days | Lapsed inspection = compliance risk and potential insurance issue | Intake 10.5: Last Fire Inspection Date |

---

## Benchmark Sources and Qualifications

Industry benchmarks referenced in this document are derived from:

- **NAA (National Apartment Association)** — Survey of Operating Income & Expenses, published annually
- **NMHC (National Multifamily Housing Council)** — Quarterly survey data on rents, occupancy, and operating costs
- **IREM (Institute of Real Estate Management)** — Income/Expense Analysis for conventional apartments
- **Grace Hill / SatisFacts** — Resident satisfaction and retention benchmarks
- **J Turner Research** — Online reputation benchmarks (ORA scores)
- **Industry standard practice** — Commonly cited thresholds from NAA education, NAHMA, and regional apartment associations

All benchmarks are approximations that vary by:

- **Property class** (A/B/C/D)
- **Asset age** (newer assets have lower R&M, higher tech spend)
- **Geographic market** (coastal urban vs. suburban vs. secondary markets)
- **Unit count** (economies of scale affect per-unit metrics)
- **Management model** (self-managed vs. third-party)

The system should allow benchmark overrides at the property, submarket, and portfolio level to account for these variations. Default benchmarks serve as starting points; the consultant adjusts based on the competitive data collected for each engagement.

---

## Field Count Summary

| Category | KPIs | Primary Data Sources |
|----------|------|---------------------|
| Occupancy & Vacancy | 21 | PM 1.1, 1.5, 1.6, 1.10; Upload 7.3; Intake 3.1, 3.3 |
| Revenue | 12 | PM 1.1, 1.3, 1.6, 1.7; Upload 7.3, 7.6; Intake 3.3 |
| Expense | 14 | PM 1.5, 1.6; Intake 3.1, 3.23, 3.24 |
| NOI & Financial Health | 8 | PM 1.6 |
| Turnover | 8 | PM 1.2; Upload 7.3, 7.4, 7.6 |
| Leasing Performance | 12 | Intake 3.14, 3.15, 3.24; CRM (Section 2) |
| Retention & Renewals | 8 | PM 1.1, 1.3; Intake 3.15, 3.21 |
| Maintenance & Work Orders | 9 | PM 1.4, 1.6; Intake 3.20 |
| Delinquency & Collections | 10 | PM 1.6, 1.11; Intake 3.23 |
| Staffing & Organization | 7 | Intake 3.1, 3.19 |
| Pet Policy & Revenue | 5 | PM 1.7; Intake 3.23; Competitive 5.11 |
| Screening & Placement Quality | 5 | PM 1.2; Intake 3.18 |
| Insurance & Risk | 5 | PM 1.6; Intake 3.24, 10.4, 10.5 |
| **Total** | **124** | |

---

## Reference Documents

- **Analytical Engine Specification** — 5-layer analytical architecture that consumes these KPIs (`specs/engine/Analytical_Engine_Specification.md`)
- **Complete Data Inventory** — all 1,100+ fields referenced in data source mappings (`specs/data/Complete_Data_Inventory.md`)
- **Analytical Question Inventory** — 400+ diagnostic questions that reference these KPIs (`specs/engine/Analytical_Question_Inventory.md`)
- **Scoring Model Specification** — Layer 1 scoring methodology (`specs/scoring/Scoring_Model_Specification.md`)
- **System Concept** — data processing architecture and data model (`specs/platform/spec_1_multifamily_property_assessment_platform.md`)
