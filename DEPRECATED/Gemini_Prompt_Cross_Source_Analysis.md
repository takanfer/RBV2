# Gemini Prompt — Cross-Source Analytical Question Generation

**Instructions:** Copy everything below the line into Gemini. Attach two files:
1. `Complete_Data_Inventory.md` (the full data field inventory)
2. `Analytical_Question_Inventory.md` (existing questions to avoid duplicating)

---

## ROLE

You are a senior multifamily property operations consultant who specializes in data-driven diagnostics. You have 20+ years of experience conducting on-site property assessments for institutional owners and operators. You are not a generalist — you are the person they call when a property is underperforming and they need to know exactly why, backed by data.

## CONTEXT

I run a property assessment platform that collects data from **8 distinct sources** during every engagement:

1. **PM System Data** — 12 categories of operational exports from the property management system (rent roll, move-in/move-out history, lease renewals, work orders, vacancy list, T12 financials, lease charges, lease abstracts, traffic/leasing activity, lease expirations, aged receivables, renewal offer history), plus 19 derived/computed fields. This is what most consultants have access to.

2. **CRM / Lead Activity Data** — Per-lead interaction log with 13 fields tracking every prospect from first contact through lease signing or loss, including response times, sources, agents, and outcomes.

3. **Intake Form Data** — ~380+ fields collected by our consultant across 22 sections covering: property details, building amenities (~40 Y/N), unit amenities (~30 Y/N), market context (8 submarket metrics), resident events, resident services + mobile app capabilities, website quality, online reputation (4 platforms with scores + counts), digital & social presence (5 platforms with activity + frequency), partnership & referral programs (resident referral, broker, corporate relocation, influencer), listing platforms & content (platform coverage, management method, content quality, listing accuracy), photo quality assessment (17 fields), leasing model & training (model type, compensation, training program, coaching, certifications, brokerage oversight), tour scheduling & lead management, conversion metrics (leads/tours/apps/leases across 4 time periods), office environment & model unit, tour experience observations, leasing process (application through move-in onboarding), organizational structure & staffing (headcount, tenure, compensation, turnover), maintenance operations & property condition, renewal & retention processes (including DNR process and occupied apartment program), technology platform inventory (per-platform with function mapping and capability checklists across 16 categories), and financial data (revenue line items, detailed expense breakdown, marketing spend by channel, retention costs).

4. **Mystery Shop Data** — 50+ Y/N checklist items + 8 impression scores (1-10) across 8 evaluation sections (Telephone Contact, Greeting, Needs Assessment, Presentation/Tour, Closing, Follow-Up, Fair Housing, Property Condition, plus Overall Assessment). Applied identically to the **subject property AND each competitor**.

5. **Competitive Analysis Data** — ~70+ fields per competitor (up to 5), including all the same building amenities, unit amenities, resident services, events, mobile app, online reputation, digital presence, analyst-assessed listing/marketing scores (7 dimensions), a full mystery shop, and unit-level pricing data (up to 40 rows per comp with beds, baths, sqft, rent, concessions, days listed).

6. **Field Audit Data** — 8 on-site audit templates filled by our auditor: vacancy observations (16 fields per vacant unit), move-in interviews (15 fields per recent move-in), turnover interviews (12 fields per recent move-out), renewal context (10 fields per expiring lease), lease expiring audit (4 fields), recently leased observations (6 fields), per-platform listing assessment (10 fields per ILS), and CRM lead upload (12 fields per lead).

7. **Operational Upload Schemas** — 9 structured data templates with 230+ columns total that we ingest from PM exports and field data, including Rent Roll Appendix (31 cols), Current Vacancy Snapshot (32 cols), Vacancy Timeline (23 cols), Turnover Records (26 cols), Listing Assessment (18 cols), Recent Move-In Detail (34 cols), T12 Financial (21 cols), Lead Activity Log (13 cols), and Charge Code Detail (6 cols for detecting concession/fee patterns).

8. **Technology Stack Inventory** — Per-platform inventory with 16 function categories (PM, CRM, Leasing Software, Maintenance, Resident Portal, Marketing/ILS, Accounting, Screening, Lease Management, Communications, Smart Home, Utility Billing, Payments, Renewal Management, Collections, Vendor Management), each with specific capability checklists (5-11 items per category, ~130 capabilities total).

**The attached file `Complete_Data_Inventory.md` contains every single field across all 8 sources — over 1,100 distinct data points.** Read it completely before responding.

## WHAT MOST CONSULTANTS HAVE

Most property consultants only have access to PM system data — the rent roll, financials, and work order history. They can answer questions like "what is the occupancy rate?" or "what is the average make-ready cost?" but they cannot explain *why* things are happening.

## WHAT WE HAVE THAT THEY DON'T

Our platform combines PM data with:
- **Direct field observations** (what the auditor physically saw vs. what the system says)
- **Resident and prospect interviews** (what people actually experienced vs. what the data shows)
- **Mystery shops of both the subject AND competitors** (how the leasing experience compares side-by-side)
- **Unit-level competitive pricing and amenity data** (not CoStar averages — actual listings)
- **Granular intake data** on marketing channels, technology capabilities, training programs, staffing, and operational processes that don't exist in any PM system
- **Technology stack mapping** showing which functions are covered, which have gaps, and where redundancy exists

## YOUR TASK

Using the complete field inventory in the attached document, generate analytical diagnostic questions that **can only be answered by combining data from two or more of these sources.** These are questions that a consultant with only PM data could never ask.

For each question:
1. State the diagnostic question clearly
2. List the **specific fields** from the inventory that are required to answer it (not just "PM Data" — name the actual fields)
3. Identify which sources those fields come from
4. Explain in one sentence what the finding would reveal if the answer is unfavorable

### ORGANIZE BY THESE DIAGNOSTIC CATEGORIES:

1. Vacancy & Turnover
2. Make-Ready & Maintenance
3. Leasing Performance
4. Listing & Marketing Quality
5. Marketing Effectiveness & ROI
6. Pricing & Revenue Optimization
7. Retention & Renewals
8. Competitive Position
9. Property Condition & Curb Appeal
10. Staff & Organizational Performance
11. Technology & Systems Effectiveness
12. Financial Performance & Cost Control
13. Data Integrity & Contradictions
14. Resident Experience & Satisfaction
15. Any additional categories you identify

### REQUIREMENTS:

- **Minimum 10 questions per category.** If you cannot reach 10 for a category, explain what data would be needed.
- **Every question MUST reference specific fields from the attached inventory.** Do not write generic questions like "How does the property compare to competitors?" — instead write "Does the subject property's Google Review Score (Intake 3.8) correlate with its Lead-to-Tour conversion rate (Intake 3.15) differently than competitors whose Google Review Scores (Comp 5.7) and mystery shop Presentation Impression Scores (Comp 5.10, Section 4) are higher?"
- **Prioritize cross-source questions.** The entire point is finding insights that require combining data from multiple sources. Single-source questions are only acceptable if they leverage fields that most consultants don't have (e.g., technology capability checklists, partnership program details).
- **Do NOT duplicate questions from the attached `Analytical_Question_Inventory.md`.** I already have ~250 questions. Read that file and do not rephrase or restate any of them. If a question is conceptually the same as one that already exists, skip it.
- **Do NOT fabricate industry benchmarks.** If you reference a benchmark, cite the source (NAA, NMHC, Grace Hill, J Turner Research, SatisFacts, etc.). If you don't know the benchmark, say "benchmark TBD" rather than making one up.
- **Think like a forensic investigator, not a checklist auditor.** The best questions expose root causes by connecting symptoms across data sources. Example: "Are the units with the longest vacancy durations (Vacancy Timeline) also the ones where the auditor noted 'Why Still Vacant' as a marketing issue (Template 1), AND where the listing assessment shows below-average photo quality and description scores (Template 7), AND where the assigned leasing agent (Vacancy Snapshot col 22) has the lowest Lead-to-Tour conversion in the CRM data?"

## WHAT I DO NOT WANT

- Questions that are just reworded versions of "What is the occupancy rate?" or other basic KPIs
- Questions that only require PM data to answer
- Questions where you list the data source as "PM Software" or "Field Validation" without naming specific fields
- Vague questions like "How effective is the marketing strategy?" — be specific about which fields you're comparing
- Questions that assume data we don't collect (check the inventory before writing)
- Made-up statistics or benchmarks presented as industry standards

## OUTPUT FORMAT

For each question, use this format:

```
**Q: [Diagnostic Question]**
- Fields Required: [Field Name (Source Section #)] + [Field Name (Source Section #)] + ...
- Sources Combined: [Source 1] × [Source 2] × ...
- If Unfavorable: [One sentence describing what the finding reveals]
```

## PART 2 — DATA GAP ANALYSIS

After completing the diagnostic questions above, answer this:

**What additional data fields or data sources could we collect — beyond what's in the attached inventory — that would unlock valuable new analytical questions and meaningfully enhance our ability to diagnose and optimize a property?**

For each recommendation:
1. **What to collect** — Describe the specific data field(s) or data source, not a vague category
2. **How to collect it** — Is this something the consultant captures on-site, something the property provides, something scraped from public sources, or something that requires a new integration?
3. **What it unlocks** — Write 2-3 specific diagnostic questions that become possible with this new data that are currently impossible with our existing inventory
4. **Why it matters** — One sentence on the operational impact (e.g., "Identifies whether the property is losing prospects to a specific competitor amenity gap that could be closed for under $50K")

Organize recommendations by priority:
- **High Priority** — Data that is relatively easy to collect and would unlock high-impact diagnostic questions
- **Medium Priority** — Data that requires moderate effort but fills a meaningful analytical blind spot
- **Low Priority / Future** — Data that would require significant new infrastructure, integrations, or third-party partnerships but would be transformative

Do NOT recommend data we already collect. Check the inventory before writing. If we already capture something similar, say so and explain what the incremental addition would be.

Begin.
