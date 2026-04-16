# Analytical Engine Specification v2.0

Defines the complete analytical architecture for the property performance analysis platform. This document supersedes the three-level analytical description in the System Concept (Section: "A complete analytical platform") with a precise, layered architecture.

---

## Architecture Overview

The analytical engine processes data through a three-stage pipeline — ingestion, normalization, and enrichment — before five structured analytical layers produce a single prioritized impact summary. A separate AI analysis layer operates alongside the structured layers as an advisory companion.

### Design Principles

- **Structured layers are authoritative.** Layers 1–5 are deterministic, reproducible, and auditable. Every finding can be traced back to specific data fields and predefined logic.
- **AI is advisory only.** The AI layer reads everything but writes into nothing. It cannot modify scores, findings, or the impact summary. Its output goes directly to the consultant as a second opinion.
- **The consultant is the arbiter.** The engine surfaces findings and the AI offers interpretations. The consultant decides what enters the client deliverable.
- **The predefined set is never finished.** New scoring criteria, diagnostic questions, entity types, and analytical techniques can be added to any layer without restructuring the others.
- **Enrichment is additive, not restrictive.** The Basic Analytic Data Set adds pre-computed KPIs to the data pool. All layers can reach past the KPIs and access any normalized field directly. Nothing is gated through the BADS.

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│              SOURCE DATA (Heterogeneous Formats)                   │
│   Yardi · RealPage · AppFolio · CRM Exports · Audit Workbooks     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    NORMALIZATION LAYER                              │
│   Canonical schema · Standardized fields · Format unification      │
│   Source-agnostic: "Unit Status" means the same thing regardless   │
│   of which PM system produced it                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              NORMALIZED DATA FOUNDATION (1,100+ Fields)            │
│           PM Data Set  +  Audit Data Set  +  CRM Data              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│         BASIC ANALYTIC DATA SET (Pre-Computation Enrichment)       │
│   124 standard KPIs derived from normalized fields + benchmarks    │
│   Computed once · Available to all layers · Additive, not gating   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              ENRICHED DATA POOL                                    │
│   1,100+ normalized fields + 124 computed KPIs + benchmarks        │
│   Single unified pool · All layers read from here                  │
└────┬──────────┬──────────┬──────────┬───────────────┬──────────────┘
     │          │          │          │               │
     ▼          ▼          ▼          ▼               ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────────┐ ┌────────────────┐
│ Layer 1 │ │ Layer 2 │ │ Layer 3 │ │  Layer 4   │ │   AI Analysis  │
│ Scoring │ │ Cohort  │ │ Correl. │ │  Emergent  │ │     Layer      │
│         │ │Profiling│ │ Diag.   │ │  Patterns  │ │  (Advisory)    │
└────┬────┘ └────┬────┘ └────┬────┘ └─────┬──────┘ └───────┬────────┘
     │  ▲        │           │            │                 │
     │  │ scores │           │            │                 │
     │  │ inform │           │            │          reads all layer
     │  │ cohort │           │            │          outputs + enriched
     │  └────────┘           │            │          data pool
     │           │           │            │                 │
     ▼           ▼           ▼            ▼                 ▼
┌─────────────────────────────────────────────┐   ┌─────────────────┐
│       Layer 5: Unified Impact Summary       │   │   Consultant    │
│  (Aggregates Layers 1–4 ONLY)               │   │   Workspace     │
│  Deterministic · Auditable · Prioritized    │   │   (Advisory     │
└─────────────────────────┬───────────────────┘   │    material)    │
                          │                       └────────┬────────┘
                          ▼                                │
                ┌───────────────────┐                      │
                │    Consultant     │◄─────────────────────┘
                │    Workspace      │
                │  (Final arbiter)  │
                └───────────────────┘
```

Key relationships:
- Source data is normalized into a canonical schema before anything else happens
- The BADS computes 124 standard KPIs from normalized data and adds them to the pool — it does not gate or filter access to the underlying fields
- All analytical layers read from the enriched data pool (normalized fields + computed KPIs)
- Layer 1 scores feed into Layer 2 (scores determine cohort ranking)
- Layers 1–4 all feed into Layer 5 (the unified summary)
- The AI layer reads the full enriched data pool AND all outputs from Layers 1–5
- The AI layer does NOT feed into Layer 5 — it outputs directly to the consultant workspace
- The consultant receives both the authoritative impact summary (Layer 5) and the AI advisory material, and decides what enters the final deliverable

---

## Pre-Computation: Basic Analytic Data Set (BADS)

### Purpose

Compute 124 standard property performance KPIs from normalized data and benchmark each against industry standards. This is the property's vital signs — an immediate performance profile available as soon as data is ingested, before any analytical layer runs.

### What It Is

A pre-computation enrichment step that derives standard metrics (rates, ratios, averages, durations, costs) from the normalized data fields. It adds these computed values and their benchmarks to the data pool. It does not analyze, diagnose, or interpret.

### What It Is Not

- Not an analytical layer — it does not produce findings, scores, or recommendations
- Not a gate — the analytical layers can access any normalized field directly, whether or not the BADS computed a KPI from it
- Not exhaustive — the 124 KPIs cover standard vital signs, but the analytical layers work with the full 1,100+ field set plus whatever the BADS adds

### KPI Categories (124 total)

1. Occupancy & Vacancy (21 KPIs)
2. Revenue (12 KPIs)
3. Expense (14 KPIs)
4. NOI & Financial Health (8 KPIs)
5. Turnover (8 KPIs)
6. Leasing Performance (12 KPIs)
7. Retention & Renewals (8 KPIs)
8. Maintenance & Work Orders (9 KPIs)
9. Delinquency & Collections (10 KPIs)
10. Staffing & Organization (7 KPIs)
11. Pet Policy & Revenue (5 KPIs)
12. Screening & Placement Quality (5 KPIs)
13. Insurance & Risk (5 KPIs)

### How Each Layer Uses BADS Output

- **Layer 1 (Scoring):** Uses Data-method scoring to grade BADS-computed KPIs against calibrated thresholds (or owner budget targets for Financials). Uses Checklist-method scoring for observational and capability items (mystery shop scores, condition assessments, amenity inventories) directly from normalized data. Uses Comparative-method scoring for market-relative items against the collected comp set.
- **Layer 2 (Cohort Profiling):** Uses computed KPIs for ranking entities into cohorts (e.g., "highest RevPAU units"), but also profiles against raw fields the BADS doesn't cover (listing quality scores, vendor assignment, auditor observations).
- **Layer 3 (Correlative Diagnostics):** References BADS KPIs when answering diagnostic questions, but many questions involve fields that have no corresponding KPI (mystery shop follow-up scores, resident interview sentiments, photo quality assessments).
- **Layer 4 (Emergent Patterns):** Detects outliers in BADS KPIs, but also scans the full normalized field set for unexpected correlations the BADS never anticipated.
- **Layer 5 (Impact Summary):** Uses BADS benchmarks for financial impact quantification alongside findings from all four layers.
- **AI Layer:** References KPIs for narrative context and benchmark comparison.

### Extensibility

New KPIs can be added to the BADS as the methodology evolves. This is a convenience — it pre-computes a metric so layers don't have to derive it independently — but it is never a prerequisite. The analytical layers can always compute any metric they need from the normalized fields directly.

### Reference Document

Full KPI definitions, calculations, benchmarks, and data source mappings: `specs/engine/Basic_Analytic_Data_Set.md`

---

## Layer 1 — Scoring (The Report Card)

### Purpose

Produce a comprehensive performance grade for the property — an overall asset score, category-level scores, and item-level scores within each category. Scores feed Layer 2 (cohort ranking), Layer 3 (diagnostic context), and Layer 5 (impact prioritization).

### Input

The enriched data pool: 1,100+ normalized fields from the PM Data Set, Audit Data Set, and CRM, plus 124 pre-computed KPIs and benchmarks from the BADS.

### Scoring Methods

Every scorable item uses exactly one of three input types. All produce a 0–10 score:

1. **Data** — a continuous numerical value from PM systems, CRM, or financial reports is compared against calibrated benchmark thresholds using piecewise linear interpolation. Used for quantitative KPIs (occupancy, response times, conversion rates, costs, durations). Area 8 (Financials) uses a special case: actual performance vs owner-reported budget targets rather than generic industry benchmarks.
2. **Checklist** — items assessed as present/absent (Y/N binary) or rated on defined criteria (Tiered multi-level). Each checklist item's sub-items share a 100-point budget. Points earned / 100 × 10 = score. Used for capability inventories (amenities, technology), process maturity (training, renewal processes), and observational assessments (mystery shop, property condition). Safety and compliance items are scored within this method under Operations.
3. **Comparative** — the property's value measured relative to its collected competitive set. Position vs comp average, scaled 0–10 via calibrated thresholds. Used for rent position, amenity comparison, reputation vs comps, leasing experience vs comps.

**Confidence modifiers** — how data contradiction density affects score trust — are planned but not yet defined in the Scoring Model Specification.

### Scoring Areas

65 items organized into 12 scoring areas:

1. **Vacancy/Occupancy** (3 items) — occupancy rate, average vacant days, aged vacancy
2. **Marketing** (8 items) — online reputation, digital/social presence, website quality, digital marketing, referral program, corporate relocation program, broker/locator program, cost per lead
3. **Leasing Performance** (9 items) — conversion metrics, lead management, training & development, tour scheduling, office environment, model unit quality, tour observation, mystery shop score, leasing process quality
4. **Listings** (4 items) — listing platform coverage, photo quality, content quality, listing accuracy & freshness
5. **Pricing** (5 items) — loss-to-lease, new leases PPSF vs market, concession % of GPR, rent lift on turnover, relative to market (includes net effective vs asking gap and renewal rent increase)
6. **Retention & Renewal** (6 items) — renewal rate, average resident tenure, month-to-month %, controllable turnover rate, DNR rate, renewal & retention process
7. **Operations** (5 items) — staffing stability, technology effectiveness, compliance, units per leasing agent, units per maintenance tech
8. **Financials** (4 items) — revenue (vs owner budget), expenses (vs owner budget), bottom line (vs owner budget), capital (vs owner budget)
9. **Maintenance & Turnovers** (3 items) — maintenance performance, maintenance operations systems, make-ready efficiency
10. **Property Condition** (4 items) — overall property condition, deferred maintenance assessment, capital asset condition, unit condition — vacant walks
11. **Competitive Position** (8 items) — pricing vs comps, amenity count vs comps, mystery shop vs comps, resident services vs comps, resident events vs comps, reputation score vs comps, occupancy vs comps, resident mobile app vs comps
12. **Collections & Screening** (6 items) — delinquency rate, bad debt write-off rate, eviction rate, application denial rate, short-tenure turnover rate, screening process quality

| Type | Count |
|------|-------|
| Data | 20 |
| Checklist | 38 |
| Comparative | 7 |
| **Total** | **65** |

### Rollup

```
Sub-item points (within checklist, sum to 100)
    └── Item scores (0–10, each from its input type method)
            └── Area scores (weighted average of item scores, weights sum to 100%)
                    └── Overall asset score (weighted average of 12 area scores, weights sum to 100%)
```

Area weights are configured (not equal by default): Vacancy/Occupancy 9%, Marketing 8%, Leasing Performance 8%, Listings 8%, Pricing 8%, Retention & Renewal 8%, Operations 8%, Financials 9%, Maintenance & Turnovers 8%, Property Condition 8%, Competitive Position 10%, Collections & Screening 8%. All weights are user-configurable. Missing items are excluded from the weighted average (not scored as zero); the system tracks coverage percentage per area.

### Output

- Overall asset score (0–10 with grade band equivalent)
- 12 area scores (each with grade band equivalent)
- Item-level scores within each area
- For each score: the specific data points, benchmarks/budget targets, scoring method, and thresholds that produced it
- Confidence level per score based on data contradiction density (planned — not yet defined)

### Key Properties

- Fully deterministic — same data always produces same scores
- Every score is traceable to specific fields, specific benchmark thresholds or budget targets, and specific scoring method
- Scoring items, benchmarks, and weights are addable and adjustable without restructuring
- Reference document: Scoring Model Specification (`specs/scoring/Scoring_Model_Specification.md`)

---

## Layer 2 — Cohort Profiling (The Pattern Finder)

### Purpose

Rank entities by performance, group them into cohorts (top / middle / bottom), and profile what the best and worst performers share — including what data is missing for each group. Data absence is a diagnostic signal.

### Input

- The enriched data pool (1,100+ normalized fields + 124 BADS KPIs)
- Layer 1 scores (scores determine initial performance ranking for some entity types)

### Entity Types Profiled

1. **Leasing Agents** — ranked by conversion metrics, mystery shop scores, follow-up compliance
2. **Units** — ranked by vacancy duration, turnover frequency, maintenance cost, condition scores
3. **Unit Types** — ranked by occupancy rate, days-on-market, rent achievement, demand, turnover rate (bedroom/bathroom configurations: 1B/1B, 2B/1B, 2B/2B, etc. — distinct from floor plans)
4. **Floors** — ranked by occupancy, rent premium, vacancy duration, turnover rate, condition scores (physical floor levels — distinct from floor plans)
5. **Floor Plans** — ranked by occupancy, days-on-market, rent achievement, demand
6. **Buildings** — ranked by occupancy, condition scores, work order density, turnover rate
7. **Individual Leasing Deals** — ranked by time-to-close, concession usage, rent achievement
8. **Concessions** — ranked by lease-up velocity, resident retention, net revenue impact (concession model types: free months, reduced rent, waived fees, etc.)
9. **Individual Listings** — ranked by days-on-market, photo quality, description quality, pricing accuracy
10. **Individual Tours** — ranked by conversion outcome, source quality, scheduling method
11. **Traffic Sources** — ranked by lead volume, conversion rate, cost per lease, retention of sourced residents
12. **Vendors** — ranked by completion time, cost, quality of work (field audit verified), callback rate
13. **Residents** — ranked by payment history, tenure, service request patterns, renewal likelihood
14. **Competitors** — ranked by rent position, occupancy, product quality, leasing experience (from mystery shops)
15. **Marketing Channels** — ranked by cost per lead, cost per lease, lead-to-tour conversion, lease retention
16. **Technology Platforms** — ranked by adoption rate, feature utilization, operational impact

### Process

For each entity type:

1. **Rank** all entities by the relevant performance metric(s)
2. **Group** into top / middle / bottom cohorts (thresholds defined per entity type)
3. **Profile each cohort** — what do the top, middle, and bottom performers each share across all available data?
4. **Identify improvement opportunities at every tier:**
   - Top: where can the best still improve, and what would have the greatest impact?
   - Middle: what differentiates them from the top (what holds them back) and from the bottom (what keeps them above)? Which differences have the greatest impact?
   - Bottom: what do they lack that both top and middle have? Which gaps have the greatest impact?
5. **Identify data gaps** — for each cohort, what data is missing or incomplete? Does data completeness itself correlate with performance tier? (If the worst-performing units all lack recent photos, that's a finding)

### Output

Every cohort analysis must list the actual candidates — the specific units, agents, vendors, deals, etc. by name or ID — not just aggregate observations about the group. The consultant needs to see exactly which entities are in each tier.

- Ranked entity list per type with cohort assignment and the specific entities named in each cohort
- Top performer profile: shared characteristics, remaining improvement opportunities, highest-impact improvements
- Middle performer profile: shared characteristics, differentiators from top (what holds them back), differentiators from bottom (what keeps them above), highest-impact changes to move up
- Bottom performer profile: shared characteristics, specific gaps versus top and middle, highest-impact gaps to address
- Data completeness analysis per cohort: missing/incomplete data as diagnostic signal, correlation between data completeness and performance tier

### Key Properties

- Cohort profiling is entity-agnostic — new entity types can be added without restructuring
- Profiles draw from ALL available data, not just the obvious performance metrics
- Data absence is treated as a finding, not ignored

---

## Layer 3 — Correlative Diagnostics (The Root Cause Engine)

### Purpose

Answer the 400+ predefined diagnostic questions from the Analytical Question Inventory. Each question is designed to identify a specific performance issue, root cause, or operational pattern by correlating data across multiple sources.

### Input

The enriched data pool (1,100+ normalized fields + 124 BADS KPIs).

### Process

1. **Answer each question** using the specific data fields referenced in its definition
2. **Classify the answer** as a strength, weakness, neutral, or data-insufficient
3. **Group related findings** — multiple questions that point to the same root cause are clustered (e.g., slow make-ready + poor vendor quality + high vacancy duration = turnover pipeline failure)
4. **Rank findings by impact** — highest to lowest estimated operational and financial impact

### Question Categories

The questions are organized into 16 diagnostic categories (see Analytical Question Inventory for the full list):

1. Vacancy & Turnover
2. Make-Ready & Maintenance
3. Leasing Performance
4. Listing Quality
5. Marketing Effectiveness
6. Pricing & Revenue
7. Retention & Renewals
8. Competitive Position
9. Property Condition
10. Staff & Systems Evaluation
11. Financial Performance
12. Data Integrity & Contradictions
13. Technology & Systems Effectiveness
14. Resident Experience & Satisfaction
15. Risk Management & Asset Preservation
16. Cohort Profiling & Pattern Recognition

Plus a Cross-Domain / Multi-Dimensional section for questions that span multiple categories.

### Output

- Each question answered with classification (strength / weakness / neutral / data-insufficient)
- Interrelated findings grouped by root cause
- Impact ranking (highest to lowest)
- For data-insufficient answers: identification of which specific data was missing

### Key Properties

- Deductive — answers predefined questions using predefined logic
- New questions can be added to any category at any time without restructuring
- Each question explicitly references the data sources and fields it requires
- Cross-source correlation is the norm, not the exception — most questions combine PM, CRM, field audit, and/or competitive data
- Reference document: Analytical Question Inventory

---

## Layer 4 — Emergent Pattern Detection (The System's Own Observations)

### Purpose

Surface patterns, anomalies, and relationships that nobody predefined. This is the inductive complement to Layer 3's deductive analysis — the system looks at all data and tells us what it sees, without being told what to look for.

### Input

The enriched data pool (1,100+ normalized fields + 124 BADS KPIs).

### Techniques

- **Statistical outlier detection** — identify fields or entities with values significantly outside normal distribution (e.g., one unit with 3x the average work order volume)
- **Unexpected correlation discovery** — find statistically significant relationships between fields that no predefined question covers (e.g., a correlation between pet deposits and renewal rates that nobody thought to ask about)
- **Temporal anomaly detection** — identify sudden changes in trends, unusual seasonality, or regime shifts (e.g., maintenance costs spiked 40% in Q3 with no corresponding increase in work order volume)
- **Cluster analysis** — find natural groupings in the data that weren't predefined as entity types (e.g., a cluster of units that share a combination of high rent, low condition score, and high turnover)
- **Data distribution analysis** — identify Pareto patterns and concentration effects (e.g., 20% of units generating 80% of work orders; one vendor receiving 60% of all contract spend)
- **Cross-entity anomaly detection** — find unusual intersections across entity types (e.g., a specific agent + specific traffic source + specific floor plan combination that has a 0% conversion rate)

### Output

- List of detected patterns, anomalies, and correlations
- Each observation tagged with: statistical confidence, data fields involved, affected entities, potential operational significance
- Observations ranked by statistical significance and potential impact
- No classification as strength/weakness — these are observations for the consultant to interpret

### Key Properties

- Purely inductive — no predefined questions, hypotheses, or expected outcomes
- The system reports what it finds; the consultant determines what it means
- New statistical techniques can be added without restructuring
- Output is tagged with confidence levels so the consultant can filter noise
- This layer will surface things that surprise the consultant — that is its entire purpose

---

## Layer 5 — Unified Impact Summary (The Action Plan)

### Purpose

Aggregate all findings from Layers 1–4 into a single, prioritized, actionable summary. This is the primary deliverable — one document that tells the consultant (and ultimately the client) what matters most and what to do about it.

### Input

- Layer 1: Scores and grades
- Layer 2: Cohort profiles and data gap findings
- Layer 3: Diagnostic answers and root cause groupings
- Layer 4: Emergent patterns and anomalies

**Not included:** AI Analysis Layer output. The impact summary is built entirely from the structured layers.

### Process

1. **Collect** all findings from Layers 1–4
2. **Deduplicate** — when multiple layers surface the same issue (e.g., Layer 1 gives maintenance a failing score, Layer 3 identifies slow make-ready as a root cause, and Layer 4 detects an outlier vendor), consolidate into a single finding with attribution to each layer that surfaced it
3. **Tag each finding** with:
   - Which layer(s) surfaced it
   - The performance issue it's tied to (vacancy, revenue, retention, etc.)
   - Financial impact estimate (annual revenue loss, cost, or missed opportunity)
   - Priority ranking (based on financial impact and feasibility of resolution)
4. **Produce a prioritized list** ordered by potential to increase property performance
5. **Group into action categories** — immediate fixes, short-term improvements, strategic initiatives

### Output

- Single prioritized finding list with financial impact estimates
- Each finding attributed to source layer(s)
- Grouped by action timeline (immediate / short-term / strategic)
- Cross-referenced to specific data points for auditability

### Key Properties

- This layer produces, not analyzes — it organizes and prioritizes what the other layers found
- Every finding is traceable back to the layer(s) and data that produced it
- The financial impact estimate makes prioritization objective, not subjective
- The consultant can override priority rankings based on client-specific context
- AI layer output is explicitly excluded to maintain auditability and reproducibility

---

## AI Analysis Layer — Cross-Check & Supporting Evidence (Advisory Only)

### Purpose

Provide an independent, AI-generated interpretive analysis of all data and all structured layer outputs. The AI layer serves as a cross-check and a source of supporting evidence. It does not produce authoritative findings and never writes into the Impact Summary. The consultant decides whether to promote any AI observation into the formal deliverable.

### Input

- All raw data (same 1,100+ fields the structured layers consume)
- All outputs from Layers 1–5 (scores, cohort profiles, diagnostic answers, emergent patterns, impact summary)

### What It Produces

**Agreement confirmations** — where the AI's interpretation aligns with structured findings, adding narrative confidence. Example: "The data strongly supports the Layer 3 finding on make-ready bottlenecks — vendor X's completion times are 2.3x the property average and the units they serviced show a pattern of re-opening within 30 days."

**Disagreement flags** — where the AI sees a different interpretation or believes a finding may be overstated or understated. Flagged for consultant review. Example: "Layer 1 scored marketing effectiveness as below average, but the lead-to-lease conversion rate is actually above submarket benchmarks — the low score may be driven by high cost-per-lead in a market where that cost is structurally high."

**Supplementary observations** — connections, industry context, or nuances the structured layers couldn't surface. Example: "This combination of high turnover, declining condition scores, and flat R&M spending is consistent with a property in the 18–24 month window after a management company transition, when deferred maintenance from the prior operator becomes visible."

**Investigation prompts** — specific questions the consultant might want to explore manually based on what the AI noticed. Example: "The data shows three residents with identical move-in dates and identical lease terms from the same traffic source — this may warrant manual verification."

### What It Does NOT Do

- Does not produce scores or rankings
- Does not modify, override, or inject findings into the Impact Summary (Layer 5)
- Does not generate client-facing recommendations directly
- Does not replace any structured layer's output
- Does not have write access to any layer's findings

### Trust Model

| Component | Nature | Role |
|---|---|---|
| Structured Layers 1–5 | Deterministic, auditable, reproducible | Record of truth |
| AI Analysis Layer | Probabilistic, interpretive, advisory | Second opinion |
| Consultant | Human judgment, client context | Final arbiter |

The AI layer's output is presented to the consultant in a dedicated advisory section of the workspace, visually and structurally separate from the authoritative findings. The consultant can:

- Read AI observations alongside structured findings for additional context
- Promote an AI observation to a formal finding if warranted (manually)
- Dismiss AI observations that are unhelpful or incorrect
- Use AI observations to guide ad hoc investigation

### Why This Separation Matters

- **Auditability** — the client deliverable is fully traceable to deterministic logic and specific data. No AI-generated conclusions appear unless the consultant explicitly promotes them.
- **Reproducibility** — running the same data through the engine always produces the same Layer 1–5 output. AI output may vary, but it never contaminates the authoritative analysis.
- **Liability** — AI-generated interpretations in a client-facing consulting deliverable carry risk. Keeping them advisory-only protects the consultant and the platform.
- **Evolution** — as AI capabilities improve, the advisory layer can expand in scope and sophistication without destabilizing the structured core. The separation allows aggressive experimentation in the AI layer with zero risk to the authoritative output.

---

## The Consultant's Workspace

Beyond the engine's automated output, the consultant retains full analytical access to all data at all times. This is not a layer — it is the environment in which the consultant works.

The consultant can:

- Run ad hoc queries against any data field or combination of fields
- Investigate specific findings from any layer in more detail
- Review AI advisory material and decide what to promote
- Override priority rankings based on client-specific context
- Add new diagnostic questions to Layer 3 based on what they discover
- Document their own observations and findings alongside the engine's output

The predefined set (Layers 1–4) is never finished. The consultant's ad hoc work is how the engine evolves — discoveries made during manual investigation become new scoring criteria, new diagnostic questions, or new entity types for future analyses.

---

## Simulated Optimal Budget (Layer 4+ Output)

### Purpose

Generate a property-specific "what-if" proforma that represents the optimal financial performance achievable based on the analytical engine's findings. This is not a generic industry benchmark — it is a budget derived from the organic strategy surfaced by the analysis for this specific property.

### Dependency Chain

The simulated budget cannot be computed until the analysis is complete. It depends on outputs from multiple layers:

1. **Layer 1 (Scoring):** Identifies where performance deviates from benchmarks — occupancy gaps, pricing misalignment, expense overruns
2. **Layer 2 (Cohort Profiling):** Identifies which units, agents, traffic sources, and vendors are top performers — the simulated budget models what happens when the bottom and middle cohorts move toward top-cohort performance
3. **Layer 3 (Correlative Diagnostics):** Identifies root causes — the simulated budget addresses these causes (e.g., if slow make-ready is driving vacancy loss, the budget models the financial impact of reducing make-ready duration to benchmark)
4. **Layer 4 (Emergent Patterns):** Surfaces opportunities the predefined analysis didn't anticipate — these may reveal additional revenue or savings to model

### What It Produces

A complete proforma mirroring the Financials scoring area structure (Revenue, Expenses, Bottom Line, Capital) with three columns per line item:

| Line Item | Actual | Owner's Budget | Optimal Simulated Budget |
|---|---|---|---|
| Gross Potential Rent | $X | $Y | $Z |
| Vacancy Loss | ... | ... | ... |
| ... | ... | ... | ... |
| Net Operating Income | ... | ... | ... |

Each simulated line item includes:
- The **value** derived from the analysis
- The **assumption** behind it (e.g., "Occupancy modeled at 95% based on comp set average and property condition score")
- The **layer(s) and findings** that informed the assumption

### How It Differs From Owner's Budget

- Owner's budget reflects the owner's stated financial targets — what they planned for
- Simulated budget reflects what the analysis says is achievable based on evidence
- The gap between them is a diagnostic signal: if the owner's budget is more aggressive than the simulated budget, their targets may be unrealistic; if the simulated budget exceeds the owner's, there is untapped potential the owner hasn't planned for

### Use in Deliverable

The three-column comparison (Actual vs Owner's Budget vs Simulated Optimal) is a primary deliverable artifact. It provides:
- A "come to Jesus" conversation with ownership about whether their targets are calibrated to reality
- A concrete financial roadmap showing what improvements (identified by the engine) translate to in dollar terms
- An evidence-based investment case for the recommended operational changes

### Key Properties

- Generated after all analytical layers complete — this is an output, not an input to scoring
- Every line item assumption is traceable to specific analytical findings
- The simulated budget is specific to this property — it uses this property's unit mix, market, comp set, and condition, not generic benchmarks
- The consultant can adjust assumptions before including in the deliverable

---

## Assessment-Level Date Range Variable

### Purpose

Many scored items and computed metrics require a date range to define the observation window. Rather than hardcoding "trailing 12 months" into each formula, the system uses an assessment-level date range variable that is set once per engagement and applied consistently to all date-dependent items.

### How It Works

- The consultant defines the date range when configuring the assessment (e.g., "January 1, 2025 – December 31, 2025" or "Trailing 12 months from assessment date")
- All items tagged as date-range-dependent automatically use this window for their data pulls and computations
- The date range is stored as assessment metadata and recorded in all outputs for auditability

### Items That Use the Date Range Variable

**Area 1 — Vacancy/Occupancy**
- Average Vacant Days

**Area 2 — Marketing**
- Cost per Lead

**Area 3 — Leasing Performance**
- Lead-to-Tour %, Tour-to-App %, App-to-Lease %, Tour-to-Lease %, Lead-to-Lease %, Cancel Rate, Ghost Rate

**Area 5 — Pricing**
- Concession % of GPR, Rent Lift on Turnover, Net Effective vs Asking Gap, Renewal Rent Increase

**Area 6 — Retention & Renewal**
- Renewal Rate, Controllable Turnover Rate, DNR Rate

**Area 7 — Operations**
- Staff Turnover Rate

**Area 8 — Financials**
- All 18 financial sub-items (Revenue 5, Expenses 9, Bottom Line 2, Capital 2 — per Scoring_Model_Specification.md lines 469-505)

**Area 9 — Maintenance & Turnovers**
- Work Order Completion Rate, Avg Work Order Completion Duration, Callback/Repeat Work Order Rate, Preventive vs Reactive Ratio, Make-Ready Duration, Make-Ready Cost
- Note: Emergency Response Time and Routine Response Time are Tiered sub-items (Scoring_Model_Specification.md lines 527-528) and do NOT use the date range variable — they are observed at time of audit.

**Area 12 — Collections & Screening**
- Delinquency Rate, Bad Debt Write-Off Rate, Eviction Rate, Application Denial Rate, Short-Tenure Turnover Rate

### Items That Do NOT Use the Date Range Variable

These are point-in-time snapshots or audit observations:
- Occupancy Rate (current snapshot)
- Aged Vacancy (current snapshot)
- Average Resident Tenure (current snapshot)
- Month-to-Month % (current snapshot)
- All Y/N checklist items (observed at time of audit)
- All Tiered audit observation items (observed at time of audit)
- All Comparative items (comp data collected during audit)
- Loss-to-Lease (snapshot of current in-place rents vs market)

---

## How the Engine Evolves

### Adding new KPIs (BADS)
Add new computed metrics and benchmarks to the Basic Analytic Data Set. These become available in the enriched data pool for all layers to use. Adding KPIs is a convenience — the analytical layers can always compute any metric they need from normalized fields directly, so new BADS KPIs are never a prerequisite.

### Adding new scoring items (Layer 1)
Add new items to any of the 12 scoring areas, adjust thresholds, add new areas, or reweight item/area contributions. Each new item specifies its input type (Data, Checklist, or Comparative), data source, and default thresholds. No restructuring required.

### Adding new entity types (Layer 2)
Define the entity, its performance metric(s), and its cohort thresholds. The profiling logic applies automatically.

### Adding new diagnostic questions (Layer 3)
Add questions to any category in the Analytical Question Inventory. Each question specifies its required data fields. The engine picks them up automatically.

### Expanding detection techniques (Layer 4)
Add new statistical methods to the emergent pattern detection toolkit. Each technique operates independently across all available data.

### Expanding AI capabilities (AI Layer)
Improve the AI's interpretive depth, add new analysis modes, or connect additional AI models. None of this affects Layers 1–5 because the AI layer has no write access to the structured output.

---

## Reference Documents

- **Scoring Model Specification** — 65 scored items across 12 areas, three input types (Data/Checklist/Comparative), rollup logic, and area/item/sub-item weights for Layer 1 (`specs/scoring/Scoring_Model_Specification.md`)
- **Basic Analytic Data Set** — 124 standard KPIs, calculations, benchmarks, and data source mappings (`specs/engine/Basic_Analytic_Data_Set.md`)
- **Complete Data Inventory** — all 1,100+ fields from all data sources (`specs/data/Complete_Data_Inventory.md`)
- **Analytical Question Inventory** — all 400+ predefined diagnostic questions for Layer 3 (`specs/engine/Analytical_Question_Inventory.md`)
- **System Concept** — foundational business requirements and data source definitions (`REBOOT/RBv1/IMPLEMENTATION/System_Concept.md`)
- **Data Collection Architecture** — PM Data Set and Audit Data Set definitions (defined in `specs/data/Complete_Data_Inventory.md`, Section: Data Collection Architecture)
