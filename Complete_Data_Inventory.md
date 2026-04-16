# Complete Data Inventory

Every data field collected across all sources. For each field: name, type, and whether it contributes to scoring.

---

## Data Collection Architecture

The platform has exactly two data on-ramps. All 1,100+ fields flow through one of these two streams:

### Stream 1: PM Data Set — What the Property Provides

System exports and operational reports uploaded by the property or pulled from their PM software and CRM. The consultant does not create this data — they ingest it.

- PM System Reports (12 categories: Rent Roll, Move-In/Out, Renewals, Work Orders, Vacancy, T12 Financials, Lease Charges, Lease Abstracts, Traffic, Lease Expirations, Aged Receivables, Renewal Offers)
- CRM / Lead Activity Log
- Charge Code Detail
- T12 Financial Statement

Documented in Sections 1, 2, and 7 below.

### Stream 2: Audit Data Set — What the Field Team Captures

Everything collected by the consultant/auditor during the engagement, through a single unified audit platform. This replaces the legacy split between a separate "intake form" and "audit workbook" — in practice, one person captures all of this data during one engagement through one interface.

- Property profile (details, amenities, market context, staffing, financials, tech stack)
- Mystery shop (subject property + each competitor)
- Competitive analysis (comp property profiles + unit-level pricing)
- Unit walks and vacancy observations (including physical condition checklist)
- Resident and staff interviews (move-in, turnover, renewal, lease expiring)
- Listing quality assessments (per ILS platform)
- Leasing process observations (tour experience, office environment, model unit)
- Conversion metrics and lead management assessment
- Back-of-house / maintenance shop inspection
- Capital asset condition assessment
- Fire / safety compliance check

Documented in Sections 3, 4, 5, 6, 8, and 10 below.

---

## 0. Assessment Configuration

Fields set once per engagement, not tied to a specific data source.

| Field | Type | Notes |
|-------|------|-------|
| Property Name | Text | Subject property |
| Property Address | Text | Full address |
| Owner / Client Contact | Text | Name, phone, email |
| Assessment Date Range | Date Range | Start and end dates defining the trailing period for date-dependent metrics |
| Comp Set | List of Properties | Properties selected for competitive analysis |
| Assessment Type | Select: Door Opener / Full Engagement | Determines which data collection sections are active |

---

## 1. PM System Data (What We Receive from the Property)

Data exported from the property management system (Yardi, RealPage, Entrata, AppFolio, etc.). System-agnostic field definitions.

### 1.1 Current Rent Roll

Point-in-time snapshot of every unit (occupied and vacant).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Critical |
| 3 | Bedrooms | Number | Critical |
| 4 | Bathrooms | Number | Critical |
| 5 | Square Footage | Number | Critical |
| 6 | Current Monthly Rent | Currency | Critical |
| 7 | Market Rent | Currency | Critical |
| 8 | Lease Start Date | Date | Critical |
| 9 | Lease End Date | Date | Critical |
| 10 | Resident Name | Text | Critical |
| 11 | Occupancy Status | Text | Critical |
| 12 | Move-In Date | Date | Important |
| 13 | Notice Date | Date | Important |
| 14 | Expected Move-Out Date | Date | Important |

### 1.2 Move-In / Move-Out Activity History

Log of all move-in and move-out events (trailing 24 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Important |
| 3 | Resident Name | Text | Important |
| 4 | Event Type (Move-In / Move-Out) | Text | Critical |
| 5 | Event Date | Date | Critical |
| 6 | Lease Start Date | Date | Important |
| 7 | Lease End Date | Date | Important |
| 8 | Reason (move-out only) | Text | Important |
| 9 | Rent Amount | Currency | Critical |

### 1.3 Lease Renewal History

Record of all lease renewals (trailing 24 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Important |
| 3 | Resident Name | Text | Important |
| 4 | Event Type | Text | Important |
| 5 | Prior Rent | Currency | Critical |
| 6 | New Rent | Currency | Critical |
| 7 | Rent Increase | Currency | Important |
| 8 | New Lease Start | Date | Critical |
| 9 | New Lease End | Date | Critical |

### 1.4 Work Order History

All maintenance work orders including make-ready/unit-turn (trailing 12 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Work Order Number | Text | Important |
| 2 | Unit Number | Text | Critical |
| 3 | Category | Text | Critical |
| 4 | Sub-Category | Text | Important |
| 5 | Description | Text | Optional |
| 6 | Date Created | Date | Critical |
| 7 | Date Completed | Date | Critical |
| 8 | Status | Text | Important |
| 9 | Priority | Text | Optional |
| 10 | Assigned To | Text | Optional |
| 11 | Cost | Currency | Critical |

### 1.5 Current Vacancy / Unit Availability

All currently vacant units.

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Critical |
| 3 | Bedrooms | Number | Important |
| 4 | Bathrooms | Number | Important |
| 5 | Square Footage | Number | Important |
| 6 | Vacancy Status | Text | Critical |
| 7 | Days Vacant | Number | Important |
| 8 | Market Rent / Asking Rent | Currency | Critical |

### 1.6 Trailing 12-Month Financial Statement (T12)

Month-by-month income and expense statement.

**Revenue:**
| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Month | Date | Critical |
| 2 | Gross Potential Rent | Currency | Critical |
| 3 | Loss to Lease | Currency | Critical |
| 4 | Vacancy Loss | Currency | Critical |
| 5 | Concessions | Currency | Important |
| 6 | Bad Debt / Write-offs | Currency | Important |
| 7 | Net Rental Income | Currency | Critical |
| 8 | Other Income | Currency | Important |
| 9 | Total Revenue | Currency | Critical |

**Expenses:**
| # | Field | Type | Priority |
|---|-------|------|----------|
| 10 | Payroll & Benefits | Currency | Critical |
| 11 | Repairs & Maintenance | Currency | Critical |
| 12 | Contract Services | Currency | Important |
| 13 | Turnover / Make-Ready | Currency | Critical |
| 14 | Marketing & Advertising | Currency | Important |
| 15 | Insurance | Currency | Important |
| 16 | Real Estate Taxes | Currency | Critical |
| 17 | Utilities | Currency | Important |
| 18 | Administrative | Currency | Important |
| 19 | Management Fee | Currency | Critical |
| 20 | Total Operating Expenses | Currency | Critical |
| 21 | Net Operating Income (NOI) | Currency | Critical |

### 1.7 Rent Roll with Lease Charges Detail

Breakdown of every recurring charge on every resident's lease.

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Important |
| 3 | Square Footage | Number | Optional |
| 4 | Resident Name | Text | Important |
| 5 | Occupancy Status | Text | Important |
| 6 | Charge Code | Text | Critical |
| 7 | Charge Description | Text | Important |
| 8 | Monthly Amount | Currency | Critical |
| 9 | Charge Start Date | Date | Important |
| 10 | Charge End Date | Date | Important |

Key charge code subsets: concession codes, pet-related codes, lease break fee codes, parking codes, utility billback codes.

### 1.8 Lease Detail / Lease Abstracts

Detailed information about each lease (trailing 24 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Unit Type | Text | Important |
| 3 | Resident Name | Text | Important |
| 4 | Lease Execution Date | Date | Critical |
| 5 | Lease Start Date | Date | Critical |
| 6 | Lease End Date | Date | Critical |
| 7 | Lease Term (Months) | Number | Important |
| 8 | Quoted Rent | Currency | Important |
| 9 | Security Deposit | Currency | Optional |
| 10 | Lease Type (New/Renewal/Transfer/MTM) | Text | Important |
| 11 | Leasing Agent | Text | Important |

### 1.9 Traffic / Leasing Activity Detail

All prospect interactions — initial contact through lease signing (trailing 12 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Prospect ID | Text | Important |
| 2 | Contact Date | Date | Critical |
| 3 | Activity/Event Type | Text | Critical |
| 4 | Lead Source | Text | Critical |
| 5 | Leasing Agent | Text | Important |
| 6 | Unit Type Interest | Text | Optional |
| 7 | Tour Outcome | Text | Optional |

### 1.10 Lease Expiration Schedule

Summary of lease expirations by unit type for the next 12 months.

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Type | Text | Critical |
| 2 | Month-to-Month Count | Number | Important |
| 3 | Expirations by Month (12 columns) | Number | Critical |
| 4 | Total | Number | Optional |

### 1.11 Aged Receivables / Delinquency

All outstanding resident balances.

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Critical |
| 2 | Resident Name | Text | Important |
| 3 | Current Balance | Currency | Critical |
| 4 | 0-30 Days | Currency | Important |
| 5 | 31-60 Days | Currency | Important |
| 6 | 61-90 Days | Currency | Important |
| 7 | 90+ Days | Currency | Important |
| 8 | Last Payment Date | Date | Optional |
| 9 | Collections Status | Text | Optional |
| 10 | Eviction Filed | Y/N | Optional |

### 1.12 Renewal Offer History (Optional)

Log of renewal offers sent to residents (trailing 12 months).

| # | Field | Type | Priority |
|---|-------|------|----------|
| 1 | Unit Number | Text | Important |
| 2 | Resident Name | Text | Important |
| 3 | Offer Date | Date | Important |
| 4 | Current Rent | Currency | Important |
| 5 | Offered Rent | Currency | Important |
| 6 | Outcome (Accepted/Declined/Counter/Pending/No Response) | Text | Important |
| 7 | Accepted Date | Date | Optional |
| 8 | Incentive Offered | Text | Optional |
| 9 | Incentive Value | Currency | Optional |

### 1.13 Derived / Computed Fields

Calculated by the platform from PM data — no additional data required.

| Field | Derivation |
|-------|------------|
| Floor / Building | Parsed from unit number |
| Holdover Status | Lease end date vs. current date + occupancy status |
| Unit Active State | Vacancy status + make-ready work order completion |
| Tenure (months) | Move-in date to move-out date |
| Original Move-In Rent | Earliest move-in event for current/departed tenant |
| Renewal Count | Count of renewal history records for current tenant |
| Concession at Original Move-In | Cross-referenced from lease charges at move-in |
| Turnover Costs (by category) | Aggregated from make-ready work orders by sub-category |
| Concession Amount | Monthly concession charge x duration |
| Net Effective Rent | Gross Rent - (Concession Amount / Lease Term) |
| Loss-to-Lease | Market Rent - Gross Rent |
| Lease Term | Months between Lease Start and Lease End |
| Days Vacant / VDOM | Date math between move-out, make-ready, listing, and move-in |
| Rent Lift | New Lease Rent - Prior Tenant Rent |
| Vacancy Cost | Days Vacant x Daily Rent Loss |
| Daily Rent Loss | Asking Rent / 30 |
| Cumulative Vacancy Cost | Daily Rent Loss x Total Vacancy Days |
| Acquisition Cost | Vacancy Cost + Make-Ready Cost + Concession + Broker Fee + Commission |
| Delinquency Rate | Units with balance > 0 / Total occupied units |

---

## 2. CRM / Lead Activity Data

Per-lead interaction log, uploaded from CRM or captured via audit workbook.

| # | Field | Type |
|---|-------|------|
| 1 | Prospect ID | Text |
| 2 | Lead Created Date | Date |
| 3 | Contact Date | Date |
| 4 | Activity Type | Text |
| 5 | Status | Text |
| 6 | Lead Source | Text |
| 7 | Agent | Text |
| 8 | Unit Type Interest | Text |
| 9 | Unit Applied | Text |
| 10 | Tour Outcome | Text |
| 11 | Response Time (minutes) | Number |
| 12 | Reason Lost | Text |
| 13 | Notes | Text |

---

## 3. Intake Form Data (What the Consultant Captures)

~380+ fields collected via the intake web app across 22 sections. Fields marked "Scored" contribute to the property's rubric score.

### 3.1 Property Details

| Field | Type | Scored |
|-------|------|--------|
| Property Name | Text | — |
| Street Address | Text | — |
| City | Text | — |
| State | Text | — |
| ZIP Code | Text | — |
| Total Units | Number | — |
| Year Built | Number | — |
| Property Class | Select: Class A / B / C / D | — |
| Buildings | Number | — |
| Building Type | Select: High-Rise / Mid-Rise / Garden / Townhome / Mixed | — |
| Stories | Number | — |
| Total Sq Ft | Number | — |
| Lot Size | Text | — |
| Parking Spaces | Number | — |

### 3.2 Building Amenities (~40 Y/N fields)

All Y/N, all scored.

**Core:** Pool, Fitness Center, Clubhouse, Business Center
**Premium:** Hot Tub, Co-working Space, Theater, Guest Suites
**Convenience:** Package Lockers, Valet Trash, Concierge, Dry Cleaning, Package Service, Doorman
**Recreation:** Yoga Studio, Sports Courts, Playground, BBQ Area, Fire Pits, Bike Storage, Kids Playroom, Game Room
**Pet:** Dog Park, Dog Wash, Pet Spa
**Dining:** Onsite Restaurant, Demonstration Kitchen, Event/Catering Kitchen
**Event:** Event Venue / Ballroom, Roof Deck
**Parking:** Parking Type (Select: None/Open/Carport/Covered/Garage), EV Charging Stations, Resident Parking, Guest Parking, Valet Parking, Gated Community, Controlled Access

### 3.3 Market Context

| Field | Type | Scored |
|-------|------|--------|
| Submarket Name | Text | — |
| Submarket Vacancy % | Number | — |
| Submarket Avg Rent (per sq ft) | Number | — |
| YoY Rent Growth % | Number | — |
| New Supply (units) | Number | — |
| Employment Growth % | Number | — |
| Population Growth % | Number | — |
| Median Household Income | Number | — |

### 3.4 Unit Amenities (~30 Y/N fields)

All Y/N, all scored.

**Kitchen:** Dishwasher, Garbage Disposal, Microwave, Stainless Steel Appliances, Granite/Quartz Countertops
**Bathroom:** Soaking Tub, Jetted Tub, Dual Vanities, Separate Shower, Heated Floors, Steam Shower, Bidet, Frameless Glass Shower
**Laundry:** In-Unit Washer/Dryer, W/D Hookups Only, Shared/Common Laundry
**Climate:** Central A/C, In-Unit Thermostat Control, Smart Thermostat
**Flooring:** Hardwood/Vinyl Plank Flooring, Carpet, Updated Fixtures & Hardware
**Storage:** Walk-In Closet, Balcony/Patio, Private Outdoor Space, In-Unit Storage, Private Garage/Parking Option
**Tech:** Smart Locks, USB Outlets, Pre-Wired for Internet/Cable, In-Unit Alarm/Security System
**Other:** Ceiling Fans, Window Blinds/Treatments, Pet-Friendly Unit Features, ADA Accessible Units Available
**Plus:** Other Unit Amenity (Text, not scored)

### 3.5 Resident Events

| Field | Type | Scored |
|-------|------|--------|
| Management-Hosted Events Offered | Y/N | Yes |
| Event Frequency | Select: Weekly / Monthly / Quarterly / 2x/year / Annually / Never | Yes |
| Last Event Date | Date | — |
| Event Attendance Rate (%) | Number | Yes |
| Events Budget ($ Annual) | Number | — |
| Event Types (select all) | Checklist: Social / Holiday / Appreciation / Fitness/Wellness / Educational / Food & Beverage / Other | — |
| Resident Event Hosting Available | Y/N | Yes |
| Rentable Event Spaces Available | Y/N | Yes |
| Space Rental Fee Structure | Select: Free / Flat Fee / Hourly / Deposit Only | — |
| Avg Rental Revenue ($/month) | Number | — |
| Booking System in Place | Y/N | Yes |
| Event Types Allowed | Checklist: Private Parties / Meetings / Classes / Other | — |

### 3.6 Resident Services + Mobile App

**Services (all Y/N, all scored):**
Valet Trash Service, Package Management System, Concierge Services, Housekeeping / Cleaning Services, Amenity Rental Program, Pet Care Services, Day Care Services, Valet Parking, Guest Suites Available, Pool Side Valet & Services, In-Unit Dining Room Service, Dry Cleaning Services
**Plus:** Other Services (Text, not scored)

**Resident Mobile App:**

| Field | Type | Scored |
|-------|------|--------|
| Resident Mobile App Available | Y/N | Yes |
| Online Rent Payment | Y/N | Yes |
| Amenity Reservation | Y/N | Yes |
| Resident Services Access | Y/N | Yes |
| Service/Maintenance Requests | Y/N | Yes |
| Package Notifications | Y/N | Yes |
| Guest Access Management | Y/N | Yes |
| Community Forum / Chat | Y/N | Yes |
| Lease / Document Access | Y/N | Yes |
| Other Mobile Capabilities | Text | — |

### 3.7 Website Quality

| Field | Type | Scored |
|-------|------|--------|
| Website Exists | Y/N | Yes |
| Website URL | URL | — |
| Mobile Responsive | Y/N | Yes |
| Online Application Available | Y/N | Yes |
| Tour Scheduling Available | Y/N | Yes |
| Live Chat Available | Y/N | Yes |
| Contact Form Available | Y/N | Yes |
| Floor Plans Downloadable | Y/N | Yes |
| Photo Gallery Present | Y/N | Yes |
| Unit Availability Shown | Y/N | Yes |
| Virtual Tours Available | Y/N | Yes |
| Google My Business Claimed | Y/N | Yes |
| Google My Business Optimized | Y/N | Yes |

### 3.8 Online Reputation

| Field | Type | Scored |
|-------|------|--------|
| Google Reviews URL | URL | — |
| Google Review Score (1-5) | Number | Yes |
| Google Review Count | Number | Yes |
| Apartments.com Page URL | URL | — |
| Apartments.com Score (1-5) | Number | Yes |
| Apartments.com Review Count | Number | Yes |
| Zillow Page URL | URL | — |
| Zillow Score (1-5) | Number | Yes |
| Zillow Review Count | Number | Yes |
| Yelp Page URL | URL | — |
| Yelp Score (1-5) | Number | Yes |
| Yelp Review Count | Number | Yes |
| ApartmentRatings Page URL | URL | — |
| ApartmentRatings Score (1-5) | Number | Yes |
| ApartmentRatings Review Count | Number | Yes |
| Facebook Page URL | URL | — |
| Facebook Score (1-5) | Number | Yes |
| Facebook Review Count | Number | Yes |
| Reviews in Last 90 Days | Number | Yes |
| Platforms with Reviews | Number | Yes |

### 3.9 Digital & Social Presence

**Per platform (Facebook, Instagram, TikTok, LinkedIn, YouTube):**

| Field | Type | Scored |
|-------|------|--------|
| URL / Handle | URL/Text | — |
| Follower / Subscriber Count | Number | — |
| Active (Y/N) | Y/N | Yes |
| Post Frequency | Select: Daily / 2-3x/Week / Weekly / Bi-Weekly / Monthly / Rarely / Never | Yes |

**Other Channels:**

| Field | Type | Scored |
|-------|------|--------|
| Blog/Content Marketing | Y/N | Yes |
| Email Marketing | Y/N | Yes |
| Paid Advertising Used | Y/N | Yes |
| Paid Ad Platforms | Text | — |

### 3.10 Partnership & Referral Programs

**Resident Referral:**

| Field | Type | Scored |
|-------|------|--------|
| Resident Referral Program Exists | Y/N | Yes |
| Referral Incentive Offered | Y/N | Yes |
| Referral Incentive Amount ($) | Number | — |
| Referral Tracking System | Y/N | Yes |
| Referrals Received Last 12mo | Number | — |
| Referral Conversion Rate (%) | Number | — |

**Broker Program:**

| Field | Type | Scored |
|-------|------|--------|
| Broker Program Exists | Y/N | Yes |
| Offers Broker Commission | Y/N | Yes |
| Broker Commission Structure | Select: 1 Month's Rent / ½ Month's Rent / $1,000 Per Lease / Other | — |
| Broker Portal Access | Y/N | Yes |
| Broker Marketing Materials | Y/N | Yes |
| Broker Events/Outreach | Y/N | Yes |
| Dedicated Broker Contact | Y/N | Yes |
| Broker Lead Tracking | Y/N | Yes |

**Corporate Relocation:**

| Field | Type | Scored |
|-------|------|--------|
| Corporate Relocation Program Exists | Y/N | Yes |
| RMC Partnerships | Y/N | Yes |
| Corporate Rates/Packages Offered | Y/N | Yes |
| Furnished/Short-Term Options Available | Y/N | Yes |
| Dedicated Relocation Contact | Y/N | Yes |

**Collaborators & Influencers:**

| Field | Type | Scored |
|-------|------|--------|
| Local Business Partnerships | Y/N | Yes |
| Influencer/Creator Collaborations | Y/N | Yes |
| Co-Branded Content or Events | Y/N | Yes |

### 3.11 Listing Platforms & Content

**Platform Coverage (per platform: Apartments.com, Zillow, Rent.com, Trulia, Realtor.com, Craigslist, Facebook Marketplace):**

| Field | Type | Scored |
|-------|------|--------|
| Listed on [Platform] | Y/N | Yes |
| [Platform] Building Page URL | URL | — |

**Plus:** Other Platforms (Text)

**Listing Management:**

| Field | Type | Scored |
|-------|------|--------|
| Listing Posting Method | Select: Centralized Syndication / Partial Syndication / Manual Per Platform | Yes |
| Syndication Tool | Text | — |
| Who Manages Listings | Select: In-house / PM Company / External / Mix | — |
| Update Frequency | Select: Real-time / Daily / Weekly / Manual | Yes |

**Content Quality:**

| Field | Type | Scored |
|-------|------|--------|
| Description Word Count | Number | Yes |
| Unique Selling Points Mentioned | Y/N | Yes |
| Neighborhood Context Included | Y/N | Yes |
| Call-to-Action Included | Y/N | Yes |
| Contact Info Clear | Y/N | Yes |
| Floor Plans Available | Y/N | Yes |
| Unit Specs Accurate | Y/N | Yes |
| Amenities Fully Listed | Y/N | Yes |
| Pet Policy Stated | Y/N | Yes |
| Lease Terms Mentioned | Y/N | Yes |

**Listing Accuracy:**

| Field | Type | Scored |
|-------|------|--------|
| Pricing Accurate Across Platforms | Y/N | Yes |
| Availability Accurate | Y/N | Yes |
| Unit Types/Sizes Correct | Y/N | Yes |
| Amenities List Accurate | Y/N | Yes |
| Photos Match Property Condition | Y/N | Yes |
| Specials Updated | Y/N | Yes |
| Contact Info Current | Y/N | Yes |
| Error Details | Textarea | — |

### 3.12 Photo Quality Assessment

| Field | Type | Scored |
|-------|------|--------|
| Hero/Primary Image Present | Y/N | Yes |
| Exterior Building Shots Count | Number | Yes |
| Unit Interior - Living Room Shown | Y/N | Yes |
| Unit Interior - Kitchen Shown | Y/N | Yes |
| Unit Interior - Bedrooms Shown | Y/N | Yes |
| Unit Interior - Bathrooms Shown | Y/N | Yes |
| Unit Interior - Features Shown (closets, balcony) | Y/N | Yes |
| Amenity Photo - Pool | Y/N | Yes |
| Amenity Photo - Fitness Center | Y/N | Yes |
| Amenity Photo - Clubhouse | Y/N | Yes |
| Other Amenity Photos Count | Number | Yes |
| Total Amenities at Property | Number | Yes |
| Amenities Photographed Count | Number | Yes |
| Lifestyle/Community Photos Count | Number | Yes |
| Professional Photographer Used | Y/N | Yes |
| Last Photo Update Date | Date | — |
| Shows Actual Units | Select: Yes / No / Mix | Yes |

### 3.13 Leasing Model & Training

**Leasing Model:**

| Field | Type | Scored |
|-------|------|--------|
| Leasing Model | Select: In-House Leasing Team / Outside Brokerage / Hybrid (Both) | Yes |
| Brokerage Name | Text | — |
| Brokerage Contract Type | Select: Exclusive / Non-Exclusive / Preferred | — |
| Property Oversight Level | Select: High / Moderate / Low | — |
| Lead Routing | Select: Brokerage Handles All / Property Qualifies then Brokerage / Split by Source | — |

**Compensation:**

| Field | Type | Scored |
|-------|------|--------|
| Leasing Agent Base Salary Range | Text | — |
| Leasing Commission Structure | Text | — |
| Leasing Renewal Bonuses | Text | — |
| Leasing Team vs Individual | Select: Team / Individual / Hybrid | — |
| Leasing Agent Comp vs Market | Select: Above Market / At Market / Below Market | — |
| Leasing Commission Per Lease ($) | Number | — |
| In-House Leasing Cost Per Lease ($) | Number | — |
| Broker Co-Op Fee Schedule | Text | — |
| Concession Authority Level | Select: Agent / Manager / Regional / Owner | — |
| Concession Policy Documented | Y/N | — |

**Training & Development:**

| Field | Type | Scored |
|-------|------|--------|
| Formal Training Program | Y/N | Yes |
| Onboarding Duration (days) | Number | Yes |
| Ongoing Training Frequency | Select: Weekly / Monthly / Quarterly / Annually / Never | Yes |
| Product Knowledge Training | Y/N | Yes |
| Sales/Closing Training | Y/N | Yes |
| Fair Housing Training | Y/N | Yes |
| CRM/Systems Training | Y/N | Yes |
| Other Training | Text | — |
| Coaching Frequency | Select: Weekly / Monthly / Quarterly / Never | Yes |
| Performance Reviews | Select: Monthly / Quarterly / Annually / Never | Yes |
| Certifications Required | Y/N | Yes |

**Brokerage Oversight (conditional on Outside Brokerage or Hybrid model):**

| Field | Type | Scored |
|-------|------|--------|
| Formal Service Agreement | Y/N | Yes |
| Performance Metrics Tracked | Y/N | Yes |
| Regular Reporting/Accountability Meetings | Y/N | Yes |
| Ability to Request Specific Agents | Y/N | Yes |
| Performance Guarantees / Termination Clause | Y/N | Yes |

### 3.14 Tour Scheduling & Lead Management

**Scheduling Methods (all Y/N, all scored):**
Phone Scheduling Available, Email Scheduling Available, Online Self-Booking Available, Text Scheduling Available

**Availability (all Y/N, all scored):**
Weekend Availability, Evening Availability, Broker Scheduling/Access Program

**Flexibility (all Y/N, all scored):**
Same-Day Tours Accepted, Walk-Ins Accepted

**Lead Management:**

| Field | Type | Scored |
|-------|------|--------|
| CRM System Used | Text | — |
| Avg Email Response Time (min) | Number | Yes |
| Avg Phone Response Time (min) | Number | Yes |
| Follow-Up Process Documented | Y/N | Yes |
| Follow-Up Touch Count | Number | Yes |
| Automated Follow-Up | Y/N | Yes |
| After-Hours Handling | Select: Auto-response / Answering Service / Voicemail / None | Yes |
| Weekend Handling | Select: In-person coverage / Auto-response only / Answering service / Voicemail only / No coverage | Yes |
| Lead Nurturing Process | Y/N | Yes |
| Re-engagement Campaigns | Y/N | Yes |

### 3.15 Conversion Metrics

For each of 4 time periods (Last 30 Days, Last 90 Days, Last 6 Months, Last 12 Months):

| Field | Type | Scored |
|-------|------|--------|
| Total Leads Received | Number | Yes |
| Total Tours Conducted | Number | Yes |
| Total Tour No-Shows | Number | — |
| Total Applications Received | Number | Yes |
| Total Leases Signed | Number | Yes |
| Avg Days: Lead to Tour | Number | — |
| Avg Days: Tour to App | Number | — |
| Avg Days: App to Lease | Number | — |

Plus: Primary Scoring Period (Select: Last 30 Days / Last 90 Days / Last 6 Months / Last 12 Months)

### 3.16 Office Environment & Model Unit

**Office Environment:**

| Field | Type | Scored |
|-------|------|--------|
| Office Location/Visibility | Text | — |
| Office Hours - Weekday | Text | — |
| Office Hours - Saturday | Text | — |
| Office Hours - Sunday | Text | — |
| Days Open Per Week | Number | Yes |
| Visitor Parking Available | Y/N | Yes |
| Exterior Signage Clear | Y/N | Yes |
| Wayfinding Signs | Y/N | Yes |
| Waiting Area Seating | Y/N | Yes |
| Refreshments Offered | Y/N | Yes |
| WiFi Available | Y/N | Yes |
| Restroom Available/Clean | Y/N | Yes |
| Marketing Materials Displayed | Y/N | Yes |
| Technology/Tablets Used | Y/N | Yes |
| Accessibility (ADA-compliant access) | Y/N | Yes |
| Professional Setup (materials + tech present) | Tiered | Yes |

**Model Unit:**

| Field | Type | Scored |
|-------|------|--------|
| Model Unit Available | Y/N | Yes |
| Model Furnished | Select: Fully / Partially / No | Yes |
| Model Bedrooms/Baths | Text | — |
| Model Represents | Select: Typical / Best-case / Aspirational | — |
| Smell/Ambiance Observation | Text | — |
| Lighting Quality Observation | Text | — |

### 3.17 Tour Experience

**Pre-Tour:**

| Field | Type | Scored |
|-------|------|--------|
| Confirmation Sent | Y/N | Yes |
| Reminder Sent | Y/N | Yes |

**Arrival:**

| Field | Type | Scored |
|-------|------|--------|
| Wait Time on Arrival (minutes) | Number | — |

**Tour Structure:**

| Field | Type | Scored |
|-------|------|--------|
| Tour Route Defined | Y/N | Yes |
| Tour Route Logical | Y/N | Yes |
| Amenities Highlighted on Tour | Y/N | Yes |
| Common Areas Shown | Y/N | Yes |
| Avg Tour Duration (minutes) | Number | — |

**Agent Behaviors (all Y/N, all scored):**
Needs Assessment Observed, Built Rapport Observed, Highlighted Benefits Observed, Overcame Objections Observed, Created Urgency Observed, Asked for Sale Observed, Showed Units Aligned to Prospect Needs, Created Differentiation in Tour Experience, Demonstrated Knowledge of Competitive Landscape, Demonstrated Knowledge of Submarket, Fair Housing Compliance Observed

**Post-Tour:**

| Field | Type | Scored |
|-------|------|--------|
| Formal Post-Tour Follow-Up Process | Y/N | Yes |
| Follow-Up Timing (hours) | Number | — |

### 3.18 Leasing Process (Application through Move-In)

**Expectation Setting:**

| Field | Type | Scored |
|-------|------|--------|
| Leasing Process Communicated & Expectations Set | Y/N | Yes |

**Application:**

| Field | Type | Scored |
|-------|------|--------|
| Online Application Available | Y/N | Yes |
| Mobile-Friendly Application | Y/N | Yes |
| Avg Application Processing Time | Select: Same day / 1-2 days / 3-5 days / 5+ days | Yes |
| Application Status Communication to Applicant | Y/N | Yes |

**Screening Steps (all Y/N, all scored):**
Credit Check Performed, Background Check Performed, Income Verification Performed, Rental History Verification, Employment Verification

| Field | Type | Scored |
|-------|------|--------|
| Screening Turnaround Time | Select: Same day / 1-2 days / 3-5 days / 5+ days | Yes |

**Approval & Lease Execution:**

| Field | Type | Scored |
|-------|------|--------|
| Approval Notification Timeline | Select: Same day / 1-2 days / 3+ days | Yes |
| Electronic Lease Signing (E-Signatures) | Y/N | Yes |
| Lease Turnaround Time (Approval to Signed) | Select: Same day / 1-3 days / 3-5 days / 5+ days | Yes |
| Clear Move-In Cost Breakdown Provided | Y/N | Yes |
| Deposit/Fee Payment Online | Y/N | Yes |

**Move-In Coordination (all Y/N, all scored):**
Move-In Date Scheduling Process, Pre-Move-In Unit Inspection, Move-In Checklist Provided to Resident, Utility Setup Guidance Provided, Key/Access Handoff Process Defined

**Onboarding (all Y/N, all scored):**
Welcome Package Provided, In-Person New Resident Orientation, Resident Portal Setup Assistance, Community Rules & Policies Reviewed, Emergency Procedures Communicated, Amenity Walkthrough During Onboarding

**Screening Criteria & Move-In Costs:**

| Field | Type | Scored |
|-------|------|--------|
| Minimum Credit Score | Number | — |
| Income-to-Rent Ratio | Number | — |
| Background Check Provider | Text | — |
| Decision Timeline (days) | Number | — |
| Denial Rate (%) | Number | — |
| Application Fee ($) | Number | — |
| Move-In Costs ($) | Number | — |

### 3.19 Organizational Structure & Staffing

**Organization:**

| Field | Type | Scored |
|-------|------|--------|
| Property Manager Name | Text | — |
| PM Tenure (months) | Number | — |
| PM Certifications | Text | — |
| Assistant Manager | Text | — |
| Leasing Agent Count | Number | — |
| Leasing Agent Names | Text | — |
| Maintenance Tech Count | Number | — |
| Other Staff | Text | — |
| Open Positions | Number | — |
| Open Position Details | Text | — |

**Staff Compensation:**

| Field | Type | Scored |
|-------|------|--------|
| Property Manager Salary Range | Text | — |
| Assistant Manager Salary Range | Text | — |
| Leasing Staff Salary Range | Text | — |
| Maintenance Staff Salary Range | Text | — |
| Admin/Office Staff Salary Range | Text | — |
| Maintenance On-Call Compensation | Text | — |
| Benefits Package | Select: Full / Partial / None | Yes |
| Health Insurance Offered | Y/N | — |
| Retirement/401k Offered | Y/N | — |
| Housing Discount/Free Housing | Y/N | — |
| Total Annual Payroll Budget | Number | — |
| Overall Comp vs Market | Select: Above Market / At Market / Below Market | Yes |
| Staff Turnover Rate (%) | Number | Yes |
| Avg Staff Tenure (months) | Number | Yes |

### 3.20 Maintenance & Property Condition

**Response Times:**

| Field | Type | Scored |
|-------|------|--------|
| Emergency Response Time Avg (hours) | Number | Yes |
| Routine Initial Response Time Avg (hours) | Number | Yes |

**Systems:**

| Field | Type | Scored |
|-------|------|--------|
| Formal Maintenance Request System | Y/N | Yes |
| Maintenance Process Documentation (SOPs) | Y/N | Yes |
| Preventive Maintenance Program | Y/N | Yes |
| PM Schedule Documented | Y/N | Yes |
| Vendor Management Process | Text | — |
| Parts Inventory System | Y/N | Yes |

**Deferred Maintenance:**

| Field | Type | Scored |
|-------|------|--------|
| Deferred Maintenance Observed | Y/N | — |
| Deferred Maintenance Details | Textarea | — |
| Estimated Deferred Cost ($) | Number | — |

**Work Order Data (6-Month, all scored):**

| Field | Type | Scored |
|-------|------|--------|
| Total Work Orders Completed | Number | Yes |
| Resolved Within 3 Days | Number | Yes |
| Resolved Within 4-7 Days | Number | Yes |
| Resolved Within 8-30 Days | Number | Yes |
| Still Open >30 Days | Number | Yes |

**Property Condition (all scored):**

| Field | Type | Scored |
|-------|------|--------|
| Overall Property Condition | Select: Excellent / Good / Fair / Poor / Critical | Yes |
| Common Area Cleanliness | Select: Excellent / Good / Fair / Poor / Critical | Yes |
| Landscaping Quality | Select: Excellent / Good / Fair / Poor / Critical | Yes |
| Pool/Amenity Maintenance | Select: Excellent / Good / Fair / Poor / Critical | Yes |
| Specific Issues Noted | Textarea | — |
| Number of Specific Issues | Number | — |

### 3.21 Renewal & Retention

**Renewal Process:**

| Field | Type | Scored |
|-------|------|--------|
| Defined Renewal Process Exists | Y/N | Yes |
| Renewal Outreach Timeline | Select: 120+ days / 90 days / 60 days / 30 days | Yes |
| Renewal Offer Communicated in Writing | Y/N | Yes |
| Renewal Pricing Strategy Defined | Y/N | Yes |
| Resident Satisfaction Assessed Before Renewal | Y/N | Yes |
| Renewal Negotiation Flexibility | Y/N | Yes |
| Electronic Renewal Signing Available | Y/N | Yes |

**Retention Efforts:**

| Field | Type | Scored |
|-------|------|--------|
| Proactive Retention Outreach Program | Y/N | Yes |
| Retention Incentives Offered | Y/N | Yes |
| Resident Feedback/Survey Program for Retention | Y/N | Yes |
| Exit Interview / Move-Out Survey Conducted | Y/N | Yes |

**Do Not Renew (DNR) Process:**

| Field | Type | Scored |
|-------|------|--------|
| DNR Review Process Exists | Y/N | Yes |
| DNR Criteria Documented | Y/N | Yes |
| DNR Decisions Reviewed by Management | Y/N | Yes |
| DNR Communication Timeline Defined | Y/N | Yes |

**Occupied Apartment Program:**

| Field | Type | Scored |
|-------|------|--------|
| Occupied Apartment Program Exists | Y/N | Yes |
| Non-Renewal Triggers Occupied Showing Communication | Y/N | Yes |
| Notice-to-Vacate Response Timeline | Select: Same day / 1-3 days / 3-5 days / 5+ days | Yes |
| Pre-Move-Out Unit Assessment Conducted | Y/N | Yes |
| Move-Out Checklist Provided to Resident | Y/N | Yes |
| Turnover Timeline Target (days vacant) | Number | — |

**Communication & Policy:**

| Field | Type | Scored |
|-------|------|--------|
| Resident Communication Frequency | Select: Weekly / Monthly / Quarterly / Rarely | Yes |
| Renewal Incentive Types Offered | Text | — |
| Average Renewal Incentive Value ($) | Number | — |
| Renewal Rent Increase Policy | Text | — |

### 3.22 Technology — Platform Inventory

Dynamic: one card per technology platform used at the property (up to 15).

**Per Platform:**

| Field | Type | Scored |
|-------|------|--------|
| Platform Name | Select from 37 known platforms or "Other" | — |
| Annual Cost ($) | Number | — |
| Staff Mobile Access | Y/N | — |
| Functions Handled | Checklist (see below) | — |
| Capabilities per Function | Sub-checklist (see below) | — |

**16 Technology Functions:**
Property Management, CRM / Lead Management, Leasing Software, Maintenance / Work Orders, Resident Portal, Marketing / ILS Management, Accounting / Financial, Screening / Background Checks, Lease Management / E-Signatures, Communications / Messaging, Smart Home / Access Control, Utility Billing / Submetering, Payments Processing, Renewal Management, Collections, Vendor Management

**Technology Coverage & Efficiency:**

| Field | Type | Scored |
|-------|------|--------|
| Total Annual Technology Spend ($) | Number | Yes |
| Tech Spend Per Unit ($) | Number | Yes |
| Number of Active Integrations | Number | Yes |
| Staff Mobile Access Available | Y/N | Yes |
| Resident Mobile App Available | Y/N | Yes |
| Automation Level | Select: High / Moderate / Low / Minimal | Yes |
| Redundant Systems Identified | Select: None / Some / Many | Yes |
| Technology Gaps / Pain Points | Textarea | — |

### 3.23 Financial Data — Revenue

| Field | Type | Scored |
|-------|------|--------|
| Gross Potential Rent (GPR) | Number | — |
| Loss to Lease | Number | — |
| Vacancy Loss | Number | — |
| Concessions | Number | — |
| Bad Debt/Collections Loss | Number | — |
| Utility Reimbursements | Number | — |
| Parking Revenue | Number | — |
| Pet Revenue | Number | — |
| Late Fees | Number | — |
| Application Fees | Number | — |
| Other Income | Number | — |
| Lease Break Fee Revenue (Annual) | Number | — |

### 3.24 Financial Data — Expenses

| Field | Type | Scored |
|-------|------|--------|
| Payroll & Benefits | Number | — |
| Management Fee | Number | — |
| Leasing Commissions | Number | — |
| Marketing & Advertising | Number | — |
| Repairs & Maintenance | Number | — |
| Contract Services | Number | — |
| Make-Ready/Turnover | Number | — |
| Utilities | Number | — |
| Insurance | Number | — |
| Property Taxes | Number | — |
| Trash Removal | Number | — |
| Pest Control | Number | — |
| Landscaping | Number | — |
| Snow Removal | Number | — |
| Security | Number | — |
| Legal | Number | — |
| Accounting | Number | — |
| Technology/Software | Number | — |
| Office/Admin | Number | — |
| Training | Number | — |
| Travel | Number | — |
| Capital Reserves | Number | — |
| HOA/Condo Fees | Number | — |
| Other Expenses | Number | — |

**Marketing & Acquisition Cost Breakdown:**

| Field | Type | Scored |
|-------|------|--------|
| Total Annual Marketing Spend | Number | — |
| Marketing Spend: ILS/Listing Platforms | Number | — |
| Marketing Spend: Paid Digital (Google/Social) | Number | — |
| Marketing Spend: Traditional/Print | Number | — |
| Marketing Spend: Other | Number | — |
| Application Processing Cost (per app) | Number | — |
| Lease Administration Cost (per lease) | Number | — |

**Retention Costs:**

| Field | Type | Scored |
|-------|------|--------|
| Annual Retention Program Spend | Number | — |
| Renewal Incentive Budget | Number | — |
| Holdover Rate Premium (%) | Number | — |

---

## 4. Mystery Shop Data (Subject + Each Competitor)

~50 Y/N checklist items + 8 impression scores (1-10) + extras, across 8 evaluation sections. Applied identically to the subject property AND each competitor property. All Y/N items and impression scores are scored.

### 4.1 Overview

| Field | Type | Scored |
|-------|------|--------|
| Mystery Shop Conducted | Y/N | Yes |
| Date Conducted | Date | — |
| Agent Name | Text | — |

### 4.2 Section 1: Telephone Contact

**Y/N Items (all scored):**
- Friendly, professional phone greeting
- Answered within 3 rings / reasonable time
- Agent showed enthusiasm and positive attitude
- Described community and features
- Asked qualifying questions (move-in, needs, budget)
- Offered incentives or specials
- Matched apartment to stated needs
- Attempted to schedule a tour
- Collected prospect contact information

**Extras:**

| Field | Type | Scored |
|-------|------|--------|
| Telephone — Impression Score (1-10) | Number | Yes |
| Phone Response Time | Number (minutes/hours) | Yes |
| Phone Response Unit | Select: Minutes / Hours | — |
| Email Response Time | Number (minutes/hours) | Yes |
| Email Response Unit | Select: Minutes / Hours | — |

### 4.3 Section 2: Greeting

**Y/N Items (all scored):**
- Prompt acknowledgment upon entering
- Eye contact and smile
- Offered handshake / introduced by name
- Asked prospect's name
- Built rapport (small talk, warmth)
- Offered refreshments

| Field | Type | Scored |
|-------|------|--------|
| Greeting — Impression Score (1-10) | Number | Yes |

### 4.4 Section 3: Needs Assessment

**Y/N Items (all scored):**
- Asked about move-in timeline
- Asked about desired floor plan / size
- Asked about budget / price range
- Asked about lifestyle needs (pets, parking, WFH)
- Asked what's most important in their search
- Actively listened to responses

| Field | Type | Scored |
|-------|------|--------|
| Needs Assessment — Impression Score (1-10) | Number | Yes |

### 4.5 Section 4: Presentation / Tour

**Y/N Items (all scored):**
- Showed model or available unit
- Highlighted features AND benefits
- Pointed out community amenities
- Tailored presentation to prospect needs
- Demonstrated product knowledge
- Demonstrated competitive landscape knowledge
- Demonstrated submarket / neighborhood knowledge
- Discussed lease terms and move-in costs
- Property curb appeal / condition observed

| Field | Type | Scored |
|-------|------|--------|
| Presentation — Impression Score (1-10) | Number | Yes |

### 4.6 Section 5: Closing

**Y/N Items (all scored):**
- Asked for the lease / closing attempt
- Overcame objections
- Discussed next steps (application process)
- Created urgency (limited availability, specials)
- Provided pricing and application information

| Field | Type | Scored |
|-------|------|--------|
| Closing — Impression Score (1-10) | Number | Yes |

### 4.7 Section 6: Follow-Up

**Y/N Items (all scored):**
- Follow-up contact received
- Follow-up was personalized (not generic)
- Referenced specific details from the visit
- Made another closing attempt in follow-up

**Extras:**

| Field | Type | Scored |
|-------|------|--------|
| Follow-Up — Impression Score (1-10) | Number | Yes |
| Follow-up timing | Select: Same day / Next day / Within 48 hours / After 48 hours / Never | Yes |
| Follow-up method | Select: Phone / Email / Text / Multiple Methods / None | — |

### 4.8 Section 7: Fair Housing

**Y/N Items (all scored):**
- No discriminatory statements or questions
- Consistent treatment regardless of protected class
- Proper handling of accommodation requests

| Field | Type | Scored |
|-------|------|--------|
| Fair Housing — Impression Score (1-10) | Number | Yes |

### 4.9 Section 8: Property Condition

**Y/N Items (all scored):**
- Curb appeal and grounds well-maintained
- Leasing office clean and well-presented
- Model / show unit in good condition
- Common areas and amenities clean
- Signage and wayfinding clear

| Field | Type | Scored |
|-------|------|--------|
| Property Condition — Impression Score (1-10) | Number | Yes |

### 4.10 Overall Assessment

| Field | Type | Scored |
|-------|------|--------|
| Overall Experience (1-10) | Number | Yes |
| Strengths Observed | Textarea | — |
| Gaps / Areas for Improvement | Textarea | — |

---

## 5. Competitive Analysis Data (Per Comp Property, Up to 5)

Each competitor property is evaluated using identical data collection depth as the subject. ~70+ fields per comp plus unit-level pricing data.

### 5.1 Property Details

| Field | Type |
|-------|------|
| Property Name | Text |
| Address | Text |
| Total Units | Number |
| Year Built | Number |
| Property Class | Select: Class A / B / C / D |
| Distance from Subject (miles) | Number |

### 5.2 Building Amenities

Identical to subject property (Section 3.2). ~40 Y/N fields across 8 categories. All scored.

### 5.3 Unit Amenities

Identical to subject property (Section 3.4). ~30 Y/N fields across 8 categories. All scored.

### 5.4 Resident Services (all Y/N, all scored)

Valet Trash Service, Package Management System, Concierge Services, Housekeeping / Cleaning Services, Amenity Rental Program, Pet Care Services, Day Care Services, Valet Parking, Guest Suites Available, Pool Side Valet & Services, In-Unit Dining Room Service, Dry Cleaning Services
Plus: Other Services (Text)

### 5.5 Resident Events

| Field | Type | Scored |
|-------|------|--------|
| Management-Hosted Events Offered | Y/N | Yes |
| Resident Events Frequency | Select: Weekly / Monthly / Quarterly / 2x/year / Annually / Never | Yes |
| Event Types Offered | Text | — |
| Resident Event Hosting Available | Y/N | Yes |
| Rentable Event Spaces Available | Y/N | Yes |
| Space Rental Fee Structure | Select: Free / Flat Fee / Hourly / Deposit Only | — |

### 5.6 Resident Mobile App

| Field | Type | Scored |
|-------|------|--------|
| Resident Mobile App Available | Y/N | Yes |
| Mobile: Online Rent Payment | Y/N | Yes |
| Mobile: Amenity Reservation | Y/N | Yes |
| Mobile: Resident Services Access | Y/N | Yes |
| Mobile: Maintenance Requests | Y/N | Yes |
| Mobile: Package Notifications | Y/N | Yes |
| Mobile: Guest Access | Y/N | Yes |
| Mobile: Community Forum | Y/N | Yes |
| Mobile: Lease/Document Access | Y/N | Yes |
| Mobile: Other Capabilities | Text | — |
| Communication Frequency | Select: Weekly / Monthly / Quarterly / Rarely | — |

### 5.7 Online Reputation

| Field | Type | Scored |
|-------|------|--------|
| Google Review Score (1-5) | Number | Yes |
| Google Review Count | Number | Yes |
| Apartments.com Score (1-5) | Number | Yes |
| Apartments.com Review Count | Number | Yes |
| Zillow Score (1-5) | Number | Yes |
| Zillow Review Count | Number | Yes |
| Yelp Score (1-5) | Number | Yes |
| Yelp Review Count | Number | Yes |
| Reviews in Last 90 Days | Number | Yes |
| Platforms with Reviews | Number | Yes |

### 5.8 Digital Presence

**Per platform (Facebook, Instagram, TikTok, LinkedIn, YouTube):**
- URL
- Follower Count
- Active (Y/N) — scored
- Post Frequency (Select: Daily / 2-3x/Week / Weekly / Bi-Weekly / Monthly / Rarely / Never) — scored

Plus: Property Website URL

### 5.9 Listing & Marketing Assessment (Analyst-Assessed 0-10 Scores)

| Field | Type | Scored |
|-------|------|--------|
| Platform Coverage (0-10) | Number | Yes |
| Photo Quality (0-10) | Number | Yes |
| Content Quality (0-10) | Number | Yes |
| Listing Accuracy (0-10) | Number | Yes |
| Website Quality (0-10) | Number | Yes |
| Social Marketing (0-10) | Number | Yes |
| Partnership & Referral (0-10) | Number | Yes |

### 5.10 Mystery Shop (Per Competitor)

Full 50-item mystery shop evaluation identical to subject property (see Section 4). Same 8 sections, same Y/N items, same impression scores.

### 5.11 Unit Pricing Data (Up to 40 Rows Per Comp)

| Field | Type |
|-------|------|
| Beds | Select: Studio / 1 / 2 / 3 / 4 |
| Baths | Select: 1 / 1.5 / 2 / 2.5 / 3 |
| Unit Type | Text |
| Sq Ft | Number |
| Asking Rent | Number |
| Rent/SF | Formula (auto-calculated) |
| Floor | Text |
| Available (Y/N) | Y/N |
| Pvt Outdoor Space | Y/N |
| Concession Amt ($) | Number |
| Days Listed | Number |
| Notes | Text |

### 5.12 Scoring Model (Three Lenses)

**Lens 1 — Weighted Composite Score (0-10):**

| Category | Weight |
|----------|--------|
| Physical Product (Amenity Score) | 25% |
| Pricing Position | 20% |
| Digital & Marketing | 20% |
| Leasing Experience (Mystery Shop Score) | 15% |
| Resident Experience | 10% |
| Online Reputation | 10% |

**Lens 2 — Dimensional Positioning Matrix:**
10 dimensions (Rent/SF Value, Amenity Set, Unit Finishes, Curb Appeal, Online Reputation, Digital Presence, Leasing Experience, Resident Services, Concession Aggressiveness, Location/Access) — each comp classified as Above / At / Below the subject.

**Lens 3 — Value Perception Score:**
Value Score = Quality Score / (Rent/SF Relative Index). >1.0 = underpriced/good value; <1.0 = overpriced/under-delivering.

---

## 6. Field Audit Data (8 Templates)

Data collected on-site by the field auditor. Pre-populated fields come from PM data; auditor-filled fields are observational and cannot be obtained any other way.

### 6.1 Template 1: Vacancy Observations

**Target:** Units currently vacant.

**Pre-populated from PM:** Unit #, Unit Type, Beds, Baths, SqFt, Floor, Prior Tenant Rent, Move-Out Date, Move-Out Reason, Make-Ready Start, Make-Ready End, Market Rent, Asking Rent

**Auditor fills:**

| Field | Type |
|-------|------|
| Marketed (Y/N) — Is this unit independently listed? | Y/N |
| Like-Kind Listing Live Date | Date |
| Marketed Date | Date |
| Listing Platform | Text |
| Listing Type (Direct/Syndicated/Both) | Text |
| Representative Unit (is another unit used as show unit?) | Y/N |
| Last Refresh Date | Date |
| Leasing Agent | Text |
| Tours Scheduled | Number |
| Tours Completed | Number |
| Applications Received | Number |
| Showing Method (Self-guided / Agent-led / Virtual) | Select |
| Why Still Vacant | Text |
| Concession Type | Text |
| Concession Proactive/Reactive | Select |
| Notes | Text |

### 6.2 Template 2: Move-In Interviews

**Target:** Recent move-ins (last 30-90 days).

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Move-In Date, Monthly Rent, Lease Start, Lease End, Lease Term, Concession Amount

**Auditor fills:**

| Field | Type |
|-------|------|
| Leasing Agent (who closed the lease) | Text |
| Lead Source (how tenant found the property) | Text |
| Tours Before Lease | Number |
| Days: Lead to Tour | Number |
| Days: Tour to Application | Number |
| Days: Application to Lease | Number |
| Ghost/No-Show Before Lease | Y/N |
| Screening Score/Outcome | Text |
| Concession Type | Text |
| Concession Proactive/Reactive | Select |
| Broker Involved | Y/N |
| Broker Fee | Number |
| Leasing Fee | Number |
| Broker Co-Op Fee | Number |
| Showing Method | Select |
| Notes | Text |

### 6.3 Template 3: Turnover Interviews

**Target:** Recent move-outs (last 30-90 days).

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Move-Out Date, Move-Out Reason, Rent at Departure, Tenure, Turnover Cost Total + breakdown

**Auditor fills:**

| Field | Type |
|-------|------|
| Unit Condition at Move-Out | Select: Good / Fair / Poor / Damaged |
| Make-Ready Scope | Select: Standard / Heavy / Full Renovation |
| Lease Break Fee Collected (amount) | Number |
| Holdover Rate Charged | Y/N |
| Screening Score (original) | Text |
| Agent Who Placed Tenant | Text |
| Concession at Original Move-In | Y/N |
| Original Concession Amount | Number |
| Original Move-In Rent | Number |
| Number of Renewals | Number |
| Renewal Rejected Reason | Text |
| Notes | Text |

### 6.4 Template 4: Renewal Context

**Target:** Residents approaching lease expiration (60-90 days) or on MTM.

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Current Rent, Lease End, Tenure, Renewal Count

**Auditor fills:**

| Field | Type |
|-------|------|
| Renewal Contacted | Y/N |
| Renewal Offer Date | Date |
| Renewal Offered Rent | Number |
| Renewal Offered Term | Text |
| Renewal Outcome | Select: Accepted / Declined / Pending / No Response |
| Renewal Accepted Date | Date |
| Renewal Rejected Reason | Text |
| Resident Sentiment | Select: Happy / Neutral / Unhappy / At-Risk |
| Competitor Offer Amount | Number |
| Notes | Text |

### 6.5 Template 5: Lease Expiring Audit

**Target:** All leases expiring within 120 days.

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Current Rent, Lease End, Months Remaining

**Auditor fills:**

| Field | Type |
|-------|------|
| Renewal Contacted | Y/N |
| Resident Sentiment | Select: Happy / Neutral / Unhappy / At-Risk |
| Expected Outcome | Select: Likely to Renew / Likely to Vacate / Unknown |
| Notes | Text |

### 6.6 Template 6: Recently Leased

**Target:** Leases signed in the last 30-60 days.

**Pre-populated from PM:** Unit #, Unit Type, Lease Start, Monthly Rent, Concession Amount

**Auditor fills:**

| Field | Type |
|-------|------|
| Showing Method | Select |
| Concession Type | Text |
| Concession Proactive/Reactive | Select |
| Leasing Agent | Text |
| Lead Source | Text |
| Notes | Text |

### 6.7 Template 7: Listing Assessment (Per Platform)

**Target:** Each ILS platform where the property is listed.

**Auditor fills (per platform):**

| Field | Type |
|-------|------|
| Platform (Zillow, Apartments.com, etc.) | Text |
| Photo Count | Number |
| Photo Quality (1-10) | Number |
| Description Quality (1-10) | Number |
| Floor Plan Available | Y/N |
| Virtual Tour Available | Y/N |
| Amenities Listed | Y/N |
| Pricing Accurate | Y/N |
| Matches Availability | Y/N |
| Contact Info Accurate | Y/N |
| Listing URL | URL |
| Notes | Text |

### 6.8 Template 8: CRM Lead Upload

**Target:** Lead/prospect data when not provided via PM Traffic report.

**Auditor fills (per lead):**

| Field | Type |
|-------|------|
| Prospect ID | Text |
| Contact Date | Date |
| Contact Type | Text |
| Source | Text |
| Agent | Text |
| Unit Type Interest | Text |
| Tour Date | Date |
| Tour Type | Text |
| Tour Outcome | Text |
| App Date | Date |
| Lease Date | Date |
| Reason Lost | Text |

### Cross-Reference: CDI Templates ↔ Audit Workbook Sections

| CDI Template | CDI Section | Audit Workbook Section | Notes |
|-------------|-------------|----------------------|-------|
| Template 1: Vacancy Observations | 6.1 | 6A | Same content and structure |
| Template 2: Move-In Interviews | 6.2 | 6B | Same content and structure |
| Template 3: Turnover Interviews | 6.3 | 6C | Same content and structure |
| Template 4: Renewal Context | 6.4 | 6D | Same content and structure |
| Template 5: Lease Expiring Audit | 6.5 | 6E | Same content and structure |
| Template 6: Recently Leased | 6.6 | 6F | Same content and structure |
| Template 7: Listing Assessment | 6.7 | 2E | Moved to Pre-Audit Digital Review in AWS (Door Opener workflow) |
| Template 8: CRM Lead Upload | 6.8 | 6G | Renumbered as Template 7 in AWS |

---

## 7. Operational Data Templates (Upload Schemas)

Exact column definitions for data uploaded during the assessment. These define what the platform ingests from PM exports and field data collection.

### 7.1 Rent Roll Appendix (31 columns)

Unit #, Beds, Baths, Unit Type, Sq Ft, Gross Rent, Concession Type, Concession Monthly Amount, Concession Start Date, Concession End Date, [4 formula columns], Lease Start, Lease End, Tenant Name, Status, Move-In Date, Notice Date, Floor, Expected Move-Out Date, Holdover Status, Holdover Rate Applied, Original Move-In Rent, Renewal Count, Market Rent for Unit Type, [2 formula columns], Notes, Unit Active State

### 7.2 Current Vacancy Snapshot (32 columns)

Unit #, Beds, Baths, Unit Type, Sq Ft, Status, Asking Rent, [2 formula columns], Prior Tenant Rent, Move-Out Date, Lease Expiration Date, Move-Out Reason, Make-Ready Start Date, Make-Ready Complete Date, Listed Online?, Like-Kind Listing Active, Like-Kind Listing Live Date, Marketed Date, Concession Amount, Concession Type, Agent Assigned, Tours Scheduled, Tours Completed, Applications Received, [4 formula columns], Floor, Why Still Vacant, Notes

### 7.3 Vacancy Timeline (23 columns)

Unit #, Beds, Baths, Unit Type, Lease End, Move-Out, Make-Ready Complete, Available Date (Vacant Ready), Like-Kind Listing Live Date, Lease Signed (VDOM End), Move-In, New Lease Start Date, Marketed, Agent Assigned, Move-Out Reason, Prior Tenant Rent, New Lease Rent, Concession Amount, Concession Type, Concession Proactive/Reactive, Floor/Building/Section, Leasing Fee/Commission, Broker Co-Op Fee, [7 formula columns]

### 7.4 Turnover Records (26 columns)

Unit #, Beds, Baths, Unit Type, Move-Out Date, Move-Out Reason, Tenure (months), Cleaning Cost, Painting Cost, Flooring Cost, Appliance Cost, Other Cost, [1 formula column], Lease Expiration Date, Holdover Rate Charged, Lease Break Fee Collected, Concession at Original Move-In, Original Concession Amount, Original Concession Type, Original Move-In Rent, Rent at Departure, Number of Renewals, Agent Who Placed Tenant, Screening Score, Floor/Building/Section, Notes

### 7.5 Listing Assessment (18 columns)

Platform, Unit Type Represented, Listing Live Date, Asking Rent, Concession Displayed, Concession Amount, Photo Count, Photo Quality, Floor Plan Available, Virtual Tour Available, Description Quality, Description Word Count, Matches Availability, Contact Info Accurate, [1 formula column], Corresponding Vacant Units, Listing URL, Notes

### 7.6 Recent Move-In Detail (34 columns)

Unit #, Beds, Baths, Unit Type, Move-In Date, Lease Start Date, Lease Signed Date, Lease End Date, Lease Term, New Tenant Rent, Prior Tenant Rent, Prior Tenant Move-Out Date, Make-Ready Complete Date, Like-Kind Listing Live Date, Agent Who Leased, Lead Source, Tours Before Lease, Days: Lead to Tour, Days: Tour to Application, Days: Application to Lease, Total Days: Lead to Lease, Ghost/No-Show Before Lease, Concession Amount, Concession Type, Concession Proactive/Reactive, Broker Involved, Broker Fee Paid, Leasing Commission Paid, Floor/Building/Section, Notes, [4 formula columns]

### 7.7 T12 Financial Statement (21 columns)

Month, Gross Potential Rent, Loss to Lease, Vacancy Loss, Concessions, Bad Debt, Net Rental Income, Other Income, Total Revenue, Payroll, R&M, Contract Services, Make-Ready, Marketing, Insurance, Taxes, Utilities, Administrative, Management Fee, Total OpEx, NOI

### 7.8 Lead Activity Log (13 columns)

Prospect ID, Lead Created Date, Contact Date, Activity Type, Status, Lead Source, Agent, Unit Type Interest, Unit Applied, Tour Outcome, Response Time (min), Reason Lost, Notes

### 7.9 Charge Code Detail / Report 55 (6 source columns → merge into Rent Roll)

Per-unit recurring charge records, merged into the Rent Roll Appendix by unit number. Used to detect concession charge codes, pet fees, parking charges, utility billbacks, and lease break fees.

| Field | Type |
|-------|------|
| Unit | Text |
| Charge Code | Text |
| Description | Text |
| Amount | Currency |
| From (Effective Date) | Date |
| To (End Date) | Date |

---

## 8. Technology Stack Inventory

16 technology function categories with specific capability checklists. Captured per platform in the intake form.

### 8.1 Property Management
Lease tracking & administration, Unit management (vacancies, turns), Financial reporting (basic), Document storage & management, Vendor management, Resident ledger management, Compliance tracking (fair housing, local regs), Reporting & analytics (basic), Online portal integration

### 8.2 CRM / Lead Management
Multi-source lead capture (ILS, website, walk-in), Automated lead follow-up / drip campaigns, Lead pipeline tracking & management, Task reminders & scheduling, Lead scoring & prioritization, Reporting & analytics (lead source, conversion), Guest card management, Tour scheduling integration, Communication tracking (email, call, text)

### 8.3 Leasing Software
iPad / mobile tour app, Unit availability display (real-time), Prospect information capture on tour, Self-guided tour management, Tour scheduling & calendar, Digital floor plan presentation, Application start during tour, Photo / video sharing during tour, Tour route mapping

### 8.4 Maintenance / Work Orders
Work order creation & tracking, Preventive maintenance scheduling, Vendor management & dispatch, Parts inventory management, Mobile access for technicians, Resident communication on WO status, Reporting (response times, completion rates), Asset management

### 8.5 Resident Portal
Online rent payment, Maintenance request submission & tracking, Communication / messaging with staff, Access to lease documents & community info, Package tracking notifications, Amenity reservation system, Community event calendar, Lease renewal management, Mobile app availability, Smart home device integration, Resident satisfaction surveys

### 8.6 Marketing / ILS Management
ILS syndication (automated listing distribution), Social media management & scheduling, Email marketing campaigns, Website content management, Analytics & reporting (traffic, leads), Reputation management integration, Virtual tour / 3D tour hosting

### 8.7 Accounting / Financial
Accounts Payable (AP) automation, Accounts Receivable (AR) automation, Budgeting & forecasting tools, General ledger management, Financial reporting (P&L, Balance Sheet), Bank reconciliation, Integration with PM software, Invoice processing

### 8.8 Screening / Background Checks
Credit check, Criminal background check, Eviction history, Income / employment verification, Identity verification, Rental history verification, Automated decisioning / recommendations, Adverse action letter generation

### 8.9 Lease Management / E-Signatures
Lease document generation, Electronic signature (e-sign), Lease template management, Addendum / amendment support, Lease compliance tracking, Document storage & retrieval, Bulk lease generation, Audit trail / signature verification

### 8.10 Communications / Messaging
Bulk email / newsletter, SMS / text messaging, In-app messaging / chat, Automated notifications (rent due, events), Emergency mass communication, Multi-channel communication (email + text + app), Communication history / logging

### 8.11 Smart Home / Access Control
Smart lock / keyless entry, Smart thermostat control, Leak / water sensor monitoring, Package locker integration, Access control (gates, doors, elevators), Video intercom / doorbell, Lighting / energy management, Remote device management dashboard

### 8.12 Utility Billing / Submetering
RUBS (Ratio Utility Billing), Submetering integration, Utility billing generation, Resident utility portal / dashboard, Vacant unit utility management, Utility data analytics / reporting

### 8.13 Payments Processing
Online rent payment processing, ACH / bank transfer, Credit / debit card payments, Auto-pay / recurring payments, Payment reminders, Late fee automation, Partial payment handling, Payment reconciliation

### 8.14 Renewal Management
Renewal offer generation, Automated renewal reminders / workflow, Renewal pricing recommendations, E-sign for renewal leases, Renewal tracking / pipeline, Retention analytics / reporting, Move-out intent tracking

### 8.15 Collections
Past-due balance tracking, Automated collection notices, Payment plan management, Skip tracing / locate services, Collections agency integration, Legal / eviction filing support, Bad debt tracking & write-off

### 8.16 Vendor Management
Vendor database / directory, Vendor compliance tracking (insurance, licensing), Bid / proposal management, Purchase order processing, Invoice management, Vendor performance tracking, Contract management

---

## 9. Summary — Field Counts by Source

| Data Source | Sections | Approx. Fields |
|-------------|----------|----------------|
| PM System Data (12 categories + derived) | 13 | ~160 |
| CRM / Lead Activity | 1 | 13 |
| Intake Form (22 sections) | 24 | ~380+ |
| Mystery Shop (8 sections, subject + each comp) | 10 | ~60 |
| Competitive Analysis (per comp, up to 5) | 12 | ~70+ per comp |
| Field Audit (8 templates) | 8 | ~85 |
| Upload Schemas (9 targets) | 9 | ~230 columns |
| Technology Stack (16 categories) | 16 | ~130 capabilities |
| **Total unique data points** | | **~1,100+** |

The platform ingests over 1,100 distinct data fields across operational exports, consultant observations, mystery shops, competitive benchmarking, and technology assessments.

---

## 10. Planned Additions — Auditor-Captured Fields (Pending Implementation)

33 new fields identified through cross-source diagnostic gap analysis. All capturable directly by the field auditor with no system integrations required. Organized by where they should be added.

### 10.1 Field Audit Template 1: Vacancy Observations — Unit Condition Checklist

Currently the auditor captures marketing/leasing status of vacant units but records physical condition only in free-text "Notes." Adding a structured condition checklist per unit walked enables cross-referencing PM "ready" status with actual physical condition and linking condition failures to CRM prospect loss reasons.

| Field | Type | Scored |
|-------|------|--------|
| Cleanliness Acceptable | Y/N | Yes |
| Odor Present | Y/N | Yes |
| Pest Evidence | Y/N | Yes |
| Water Damage / Staining | Y/N | Yes |
| Paint Condition | Select: Good / Fair / Poor | Yes |
| Flooring Condition | Select: Good / Fair / Poor | Yes |
| Appliances Functional | Y/N | Yes |
| Fixtures / Hardware Condition | Select: Good / Fair / Poor | Yes |
| Windows / Blinds Intact | Y/N | Yes |
| HVAC Operational | Y/N | Yes |
| Overall Unit Ready to Show | Y/N | Yes |
| Condition Notes | Textarea | — |

**Questions unlocked:** Ghost Inventory detection (PM "ready" vs. physically showable), unit condition linked to CRM "Reason Lost," condition failures linked to specific vendors/make-ready spend, odor/pest correlation with days vacant.

### 10.2 Field Audit Template 3: Turnover Interviews — Actual Move-Out Reason

Currently the PM system records a move-out reason entered by office staff. Adding a structured field for the resident's stated reason (captured by auditor during interview) enables detecting data sanitization where staff mask service failures.

| Field | Type | Scored |
|-------|------|--------|
| Resident's Stated Primary Reason for Leaving | Select: Rent Increase / Maintenance Issues / Staff or Management / Bought Home / Job Relocation / Roommate or Relationship Change / Neighborhood or Safety / Upgraded Unit Elsewhere / Downgraded for Cost / Lease Violation / Other | — |

**Questions unlocked:** PM move-out reason vs. actual resident-stated reason comparison (data integrity), pattern detection of staff-sanitized move-out data hiding accountability for service failures.

### 10.3 Field Audit — New Section: Maintenance Back-of-House Inspection

New audit section. The auditor already visits the maintenance shop/office area during the site visit. Formalizes the observation with a 5-minute structured checklist.

| Field | Type | Scored |
|-------|------|--------|
| Shop / Work Area Organized | Y/N | Yes |
| Parts Inventory Visible and Labeled | Y/N | Yes |
| Safety Equipment Present (goggles, gloves, etc.) | Y/N | Yes |
| Fire Extinguisher Present and Current | Y/N | Yes |
| Chemical Storage Compliant (labeled, ventilated) | Y/N | Yes |
| Vehicle / Cart Condition | Select: Good / Fair / Poor | Yes |
| Back-of-House Cleanliness | Select: Good / Fair / Poor | Yes |

**Questions unlocked:** Back-of-house discipline as predictor of make-ready quality, fire safety violation correlation, organizational culture indicator.

### 10.4 Intake Form — New Section: Capital Asset Condition

Captured by the auditor via visual inspection and property manager interview during the site visit. Most data is on equipment nameplates or known by staff. ~10 minutes of additional auditor effort.

| Field | Type | Scored |
|-------|------|--------|
| Roof Type | Select: Flat / Pitched / Metal / Tile / Other | — |
| Roof Install / Replacement Year | Number | — |
| Roof Condition | Select: Good / Fair / Poor / Critical | Yes |
| HVAC System Type | Select: Central / PTAC / Mini-Split / Boiler / Other | — |
| HVAC Install / Replacement Year | Number | — |
| HVAC Condition | Select: Good / Fair / Poor / Critical | Yes |
| Water Heater Type | Select: Tank / Tankless / Boiler | — |
| Water Heater Install Year | Number | — |
| Water Heater Condition | Select: Good / Fair / Poor / Critical | Yes |
| Elevator Present | Y/N | — |
| Elevator Last Inspection Date | Date | — |
| Elevator Condition | Select: Good / Fair / Poor / Critical | Yes |
| Plumbing Riser Age (years, if known) | Number | — |
| Electrical Panel Age (years, if known) | Number | — |
| Fire Suppression System Last Inspection Date | Date | — |
| Parking Structure Condition (if applicable) | Select: Good / Fair / Poor / Critical / N/A | Yes |

**Questions unlocked:** Preventive maintenance effectiveness vs. actual system condition, capital reserve adequacy analysis, deferred maintenance cost exposure, insurance premium correlation with visible asset risk.

### 10.5 Intake Form — New Section: Fire / Safety Compliance

Captured by asking the property manager and checking posted inspection certificates. ~3 minutes.

| Field | Type | Scored |
|-------|------|--------|
| Last Fire Inspection Date | Date | — |
| Open Fire Code Violations | Y/N | Yes |
| Open Violation Count | Number | — |
| Violation Details | Textarea | — |
| Last REAC / NSPIRE Score (if HUD/LIHTC) | Number | — |
| Last Elevator Inspection Date (if applicable) | Date | — |
| Elevator Inspection Current | Y/N | Yes |

**Questions unlocked:** Safety violation correlation with insurance expense, fire code compliance linked to maintenance shop condition, REAC score as property condition benchmark.

### 10.6 Summary of Planned Additions

| Location | New Fields | Auditor Time Added |
|----------|-----------|-------------------|
| Template 1: Vacancy Observations | 12 | Already walking units |
| Template 3: Turnover Interviews | 1 | Already interviewing |
| New: Back-of-House Inspection | 7 | ~5 min |
| New: Capital Asset Condition | 8 (intake form) | ~10 min |
| New: Fire / Safety Compliance | 5 (intake form) | ~3 min |
| **Total** | **33** | **~18 min additional** |

Once implemented, these additions bring the total platform data points from ~1,100 to ~1,133 and unlock ~10 diagnostic questions that were previously unanswerable.
