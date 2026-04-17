# Door Opener Applicability Matrix

Maps every scored item to whether it can be scored in a Door Opener (public-data-only) assessment. Used by Phase 6 to implement the `DOOR_OPENER` assessment type.

**Rule:** If ANY sub-item within an item requires non-public data (PM system access, management interview, site visit, mystery shop, or financial records), the entire item is NOT APPLICABLE for Door Opener scoring.

**Sources:**
- Item names and types: `Computation_Rules_DATA.json`
- Data sources per item/sub-item: `Computation_Rules_DATA.json`
- Door Opener badge classification: `Audit_Workbook_Specification.md` (lines 23-25, section badges throughout)
- Scoring structure: `Scoring_Model_Specification.md`, `rbv2-project.mdc` lines 57-59

---

## Summary

| | Door Opener | Not Applicable | Total |
|--|-------------|----------------|-------|
| Items | 11 | 54 | 65 |
| Data items | 0 | 20 | 20 |
| Checklist items | 6 | 32 | 38 |
| Comparative items | 5 | 2 | 7 |

---

## Area 1 — Vacancy/Occupancy (3 items: 0 Door Opener, 3 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Occupancy Rate | Data | PM System | NO — requires PM system data |
| Average Vacant Days | Data | PM System | NO — requires PM system data |
| Aged Vacancy | Data | PM System | NO — requires PM system data |

---

## Area 2 — Marketing (8 items: 3 Door Opener, 5 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Online Reputation | Checklist | Review Platforms | **YES** — all subs from public review platforms (Audit Workbook §2A [DOOR OPENER]) |
| Digital/Social Presence | Checklist | Audit Observation (desk research) | **YES** — all subs observable from public social media profiles (Audit Workbook §2C [DOOR OPENER]) |
| Website Quality | Checklist | Audit Observation (desk research) | **YES** — all subs observable from public website (Audit Workbook §2D [DOOR OPENER]) |
| Digital Marketing | Checklist | Audit / Management Interview | NO — subs include "Social Media Paid Ads," "Google Adwords," "Email/SMS Marketing" sourced from "Audit / Management Interview" |
| Referral Program | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Corporate Relocation Program | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Broker/Locator Program | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Cost per Lead | Data | PM System / Marketing Data | NO — requires PM system / marketing spend data |

---

## Area 3 — Leasing Performance (9 items: 0 Door Opener, 9 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Conversion Metrics | Checklist | PM System / CRM | NO — all subs (Lead-to-Tour %, Tour-to-App %, etc.) require CRM data |
| Tour Observation | Checklist | Audit Observation (auditor shadow) | NO — requires physical site visit tour observation (Audit Workbook §8 [FULL ENGAGEMENT]) |
| Mystery Shop Score | Checklist | Mystery Shop | NO — requires in-person and phone mystery shop (Audit Workbook §4 [FULL ENGAGEMENT]) |
| Lead Management Quality | Checklist | Audit / Mystery Shop | NO — subs include "Follow-Up System," "Follow-Up Volume," "Advanced Programs" sourced from "Audit / Management Interview" |
| Leasing Process Quality | Checklist | Audit / Management Interview | NO — majority of subs sourced from "Audit / Management Interview" |
| Training & Development | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Tour Scheduling Quality | Checklist | Audit Observation | NO — subs include "Availability (Weekend/Evening)," "Broker Scheduling Access," "Flexibility" sourced from "Audit / Management Interview" |
| Office Environment | Checklist | Audit Observation | NO — requires physical site visit observation (Audit Workbook §5 [FULL ENGAGEMENT]) |
| Model Unit Quality | Checklist | Audit Observation | NO — requires physical site visit observation (Audit Workbook §5 [FULL ENGAGEMENT]) |

---

## Area 4 — Listings (4 items: 2 Door Opener, 2 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Platform Coverage | Checklist | Audit Observation / Management Interview | NO — subs "Update Frequency," "Management Quality," "Syndication Method" sourced from "Audit / Management Interview" |
| Photo Quality | Checklist | Audit Observation / Management Interview | NO — subs "Professional Photographer" and "Photo Recency" sourced from "Audit / Management Interview" |
| Content Quality | Checklist | Audit Observation (desk research) | **YES** — all subs observable from public listings (Audit Workbook §2E [DOOR OPENER]) |
| Listing Accuracy | Checklist | Audit Observation | **YES** — all subs observable by comparing public listings cross-platform (Audit Workbook §2E [DOOR OPENER]). Note: "Photos Match Property Condition" and "Availability Accurate" can only be fully verified on-site, but are assessable from public data comparison during Door Opener per Audit Workbook classification. |

---

## Area 5 — Pricing (5 items: 0 Door Opener, 5 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Relative to Market | Checklist | PM System + Comp Research | NO — subs "Loss-to-Lease %" and "New Leases Avg PPSF vs Market" require PM system in-place rent data |
| Concession % of GPR | Data | PM System | NO — requires PM system concession and GPR data |
| Rent Lift on Turnover | Data | PM System | NO — requires PM system lease history |
| Net Effective vs Asking Gap | Data | PM System | NO — requires PM system lease data |
| Renewal Rent Increase | Data | PM System | NO — requires PM system renewal history |

---

## Area 6 — Retention & Renewal (6 items: 0 Door Opener, 6 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Renewal Rate | Data | PM System | NO — requires PM system lease data |
| Average Resident Tenure | Data | PM System | NO — requires PM system resident history |
| Month-to-Month % | Data | PM System | NO — requires PM system lease data |
| Controllable Turnover Rate | Data | PM System | NO — requires PM system move-out reason data |
| DNR Rate | Data | PM System | NO — requires PM system DNR records |
| Renewal & Retention Process | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |

---

## Area 7 — Operations (5 items: 0 Door Opener, 5 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Units per Leasing Agent | Data | PM System / Management Interview | NO — requires staffing data |
| Units per Maintenance Tech | Data | PM System / Management Interview | NO — requires staffing data |
| Staffing Stability | Checklist | PM System / Management Interview | NO — all subs require PM system or management interview data |
| Technology Effectiveness | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Compliance | Checklist | Audit / Document Review | NO — requires access to inspection records and property documents (Audit Workbook §7 [FULL ENGAGEMENT]) |

---

## Area 8 — Financials (4 items: 0 Door Opener, 4 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Revenue | Checklist | Owner-Reported + PM System | NO — all subs require owner financial data (Audit Workbook §9 [FULL ENGAGEMENT]) |
| Expenses | Checklist | Owner-Reported + PM System | NO — all subs require owner financial data |
| Bottom Line | Checklist | Owner-Reported + PM System | NO — all subs require owner financial data |
| Capital | Checklist | Owner-Reported + PM System | NO — all subs require owner financial data |

---

## Area 9 — Maintenance & Turnovers (3 items: 0 Door Opener, 3 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Maintenance Performance | Checklist | PM System | NO — subs include Work Order Completion Rate, Avg Duration, Callback Rate, Preventive vs Reactive — all from PM system |
| Maintenance Operations Systems | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |
| Turnover Performance | Checklist | PM System | NO — subs Make-Ready Duration and Make-Ready Cost require PM system data |

---

## Area 10 — Property Condition (4 items: 0 Door Opener, 4 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Overall Property Condition | Checklist | Field Observation | NO — requires physical site walk (Audit Workbook §5 [FULL ENGAGEMENT]) |
| Capital Asset Condition | Checklist | Field Observation | NO — requires physical inspection of HVAC, roofing, plumbing, etc. (Audit Workbook §5 [FULL ENGAGEMENT]) |
| Deferred Maintenance | Checklist | Field Observation / Document Review | NO — requires site observation and maintenance records |
| Unit Condition — Vacant Walks | Checklist | Field Observation | NO — requires physical unit entry (Audit Workbook §6 [FULL ENGAGEMENT]) |

---

## Area 11 — Competitive Position (8 items: 6 Door Opener, 2 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Pricing vs Comps | Checklist (Comparative subs) | Comp Research (public listings) | **YES** — all subs compare subject vs comp pricing from public listing data (Audit Workbook §10D [DOOR OPENER]) |
| Amenity Count vs Comps | Comparative | Comp Research (public listings) | **YES** — comp amenities collected from public sources (Audit Workbook §10B [DOOR OPENER]) |
| Reputation Score vs Comps | Comparative | Comp Research (public reviews) | **YES** — comp review scores from public platforms (Audit Workbook §10F [DOOR OPENER]) |
| Mystery Shop Score vs Comps | Comparative | Comp Mystery Shop | NO — requires physical comp tours (Audit Workbook §10L [FULL ENGAGEMENT]) |
| Occupancy vs Comps | Comparative | Comp Research | NO — comp occupancy not reliably available from public data. Audit Workbook §10E [DOOR OPENER] collects "Estimated Occupancy" but this is an estimate, not a verifiable data point. Applying strict rule: unreliable source = not applicable. |
| Resident Services vs Comps | Comparative | Comp Research (public sources) | **YES** — comp resident services observable from websites/apps (Audit Workbook §10I [DOOR OPENER]) |
| Resident Events vs Comps | Comparative | Comp Research (public social media) | **YES** — comp resident events observable from social media/websites (Audit Workbook §10J [DOOR OPENER]) |
| Resident Mobile App vs Comps | Comparative | Comp Research (app stores) | **YES** — comp mobile apps verifiable in app stores (Audit Workbook §10K [DOOR OPENER]) |

---

## Area 12 — Collections & Screening (6 items: 0 Door Opener, 6 Not Applicable)

| Item | Type | Source | Door Opener |
|------|------|--------|-------------|
| Delinquency Rate | Data | PM System | NO — requires PM system AR data |
| Bad Debt Write-Off Rate | Data | PM System | NO — requires PM system financial data |
| Eviction Rate | Data | PM System | NO — requires PM system records |
| Application Denial Rate | Data | PM System | NO — requires PM system application data |
| Short-Tenure Turnover Rate | Data | PM System | NO — requires PM system lease history |
| Screening Process Quality | Checklist | Audit / Management Interview | NO — all subs sourced from "Audit / Management Interview" |

---

## Door Opener Scorable Items — Complete List

The 11 items scorable in a Door Opener assessment:

| # | Area | Item | Type |
|---|------|------|------|
| 1 | 2. Marketing | Online Reputation | Checklist |
| 2 | 2. Marketing | Digital/Social Presence | Checklist |
| 3 | 2. Marketing | Website Quality | Checklist |
| 4 | 4. Listings | Content Quality | Checklist |
| 5 | 4. Listings | Listing Accuracy | Checklist |
| 6 | 11. Competitive Position | Pricing vs Comps | Checklist (Comparative subs) |
| 7 | 11. Competitive Position | Amenity Count vs Comps | Comparative |
| 8 | 11. Competitive Position | Reputation Score vs Comps | Comparative |
| 9 | 11. Competitive Position | Resident Services vs Comps | Comparative |
| 10 | 11. Competitive Position | Resident Events vs Comps | Comparative |
| 11 | 11. Competitive Position | Resident Mobile App vs Comps | Comparative |

**Coverage:** 11 of 65 items (16.9%) across 3 of 12 areas (Areas 2, 4, 11).

**Areas with zero Door Opener coverage:** 1, 3, 5, 6, 7, 8, 9, 10, 12.

---

## Authoritative References

| Document | What This Matrix Cites It For |
|----------|-------------------------------|
| `Computation_Rules_DATA.json` | Item names, types, and data sources for all 65 items |
| `Audit_Workbook_Specification.md` lines 23-25 | Door Opener badge definitions |
| `Audit_Workbook_Specification.md` §2A-2E | [DOOR OPENER] Pre-Audit Digital Review sections |
| `Audit_Workbook_Specification.md` §10A-10K | [DOOR OPENER] Comp data collection sections |
| `Audit_Workbook_Specification.md` §4, §5, §6, §7, §8, §9 | [FULL ENGAGEMENT] sections (mystery shop, site visit, field audit, management interview, tour observation, financial data) |
| `rbv2-project.mdc` lines 57-59 | Item type counts: 20 Data, 38 Checklist, 7 Comparative |
| `Scoring_Weights_Final_Update.json` | 12 area weights, 65 item weights, 315 sub-item budgets |
