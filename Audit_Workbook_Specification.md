# Audit Workbook Specification

The single authoritative document for everything the auditor collects across both assessment types. Covers all scored and non-scored data across desk research, observation, interviews, mystery shop, competitive research, and technology assessment. Every field in the Complete Data Inventory (Sections 3–6, 8, 10) that originates from auditor activity is specified here.

---

## 1. Overview

### Two Assessment Types

This workbook supports two distinct workflows. The full engagement builds on door opener data — nothing is re-collected.

**Door Opener Assessment** — Strictly public data. No property contact, no site visit, no phone calls. Pure desk research. Purpose: initial diagnostics, competitive positioning, and sales pitch to win the engagement.

**Full Engagement Assessment** — Everything from the door opener plus mystery shops, site visit, management interview, financial benchmark intake, unit-level field templates, and technology stack audit. Purpose: complete property assessment with full scoring.

### Workflow Badges

Every section in this document is tagged with one of three badges:

| Badge | Meaning |
|-------|---------|
| **`[DOOR OPENER]`** | Collected during the door opener from public sources only |
| **`[FULL ENGAGEMENT]`** | Collected only during a full engagement (requires property access or contact) |
| **`[DOOR OPENER → VERIFIED ON-SITE]`** | Initially collected from public sources during the door opener, then verified and corrected during the full engagement site visit |

### Door Opener Workflow Checklist

Complete in order. Estimated time: 1–2 days desk research.

| Step | Section | Description |
|------|---------|-------------|
| 1 | 1 — Assessment Setup | Set property name, address, units, class, comp set (public sources) |
| 2 | 2A — Online Reputation | Review scores and counts across all platforms |
| 3 | 2B — Google Business Profile | GMB claimed/optimized check |
| 4 | 2C — Digital/Social Presence | Audit all social platforms + additional channels |
| 5 | 2D — Website Quality | Full website audit |
| 6 | 2E — Listing Audit | Platform coverage, per-platform assessment, photo/content quality, accuracy |
| 7 | 3A — Building Amenities | Record from listings and website (mark as unverified) |
| 8 | 3B — Unit Amenities | Record from listings (mark as unverified) |
| 9 | 3C — Market Context | CoStar, market reports, public data |
| 10 | 3D — Resident Events | Record from social media and website (mark as unverified) |
| 11 | 3E — Resident Services + Mobile App | Record from website and app stores (mark as unverified) |
| 12 | 10A — Comp Property Details | Per comp: name, address, units, year, class |
| 13 | 10B — Comp Building Amenities | Per comp: from listings/website |
| 14 | 10C — Comp Unit Amenities | Per comp: from listings |
| 15 | 10D — Comp Unit Pricing | Per comp: all available units from listings |
| 16 | 10E — Comp Occupancy | Per comp: estimate from available units / total |
| 17 | 10F — Comp Online Reputation | Per comp: same platform audit as subject |
| 18 | 10G — Comp Digital Presence | Per comp: same social audit as subject |
| 19 | 10H — Comp Listing Assessment | Per comp: analyst-assessed 0-10 scores |
| 20 | 10I — Comp Resident Services | Per comp: from website |
| 21 | 10J — Comp Resident Events | Per comp: from social/website |
| 22 | 10K — Comp Mobile App | Per comp: from app stores |
| 23 | 12 — Evidence (Door Opener) | Compile all screenshots |

### Full Engagement Workflow Checklist

Assumes door opener is already complete. Estimated time: 3–4 days including comp tours.

| Step | Section | Description |
|------|---------|-------------|
| 1 | 3A–3E — Property Profile | Verify and correct all door opener data on-site |
| 2 | 4 — Mystery Shop (Subject) | Phone shop, in-person tour, follow-up evaluation |
| 3 | 5 — Site Visit Observation | Office, model, condition, capital, deferred, unit walks, back-of-house |
| 4 | 6 — Field Audit Templates | Vacancy observations, move-in/turnover/renewal interviews |
| 5 | 7 — Management Interview | All subsections (staffing, marketing, leasing, operations, etc.) |
| 6 | 8 — Tour Observation | Auditor shadow of a live tour |
| 7 | 9 — Financial Data Collection | Owner's budget intake, marketing costs, retention costs |
| 8 | 10L — Comp Mystery Shops | Mystery-tour each comp property |
| 9 | 11 — Technology Stack Assessment | Full 16-category capability audit |
| 10 | 12 — Evidence (Full Engagement) | Compile all photos, documents, and certificates |

### Data Collection Methods

| Method | Assessment Type | Description |
|--------|----------------|-------------|
| Desk Research | Door Opener | Public data from listings, review sites, social media, websites, app stores, market reports |
| Site Observation | Full Engagement | Physical property inspection, unit walks, back-of-house |
| Management Interview | Full Engagement | Structured interview with PM and/or leasing staff (60–90 min) |
| Mystery Shop | Full Engagement | Secret shopper evaluation — phone + in-person tour + follow-up |
| Resident/Staff Interviews | Full Engagement | On-site interviews tied to specific units (move-in, turnover, renewal, expiring) |
| Financial Benchmark Intake | Full Engagement | Owner/asset manager call for budget data |
| Technology Assessment | Full Engagement | Per-platform capability audit of the property's tech stack |

### Assessment-Level Configuration `[DOOR OPENER]`

Set before any data collection begins. All fields obtainable from public sources except Owner Contact.

| Parameter | Format | Public Source | Description |
|-----------|--------|--------------|-------------|
| Property Name | Text | Listings / CoStar | |
| Street Address | Text | Listings / CoStar | |
| City / State / ZIP | Text | Listings / CoStar | |
| Total Units | Number | Listings / CoStar | |
| Year Built | Number | Listings / CoStar | |
| Property Class | Select: A / B / C / D | Analyst assessment | |
| Building Type | Select: High-Rise / Mid-Rise / Garden / Townhome / Mixed | Listings / Google Maps | |
| Buildings | Number | Google Maps / Listings | |
| Stories | Number | Listings / Google Maps | |
| Total Sq Ft | Number | CoStar | |
| Lot Size | Text | CoStar / County records | |
| Parking Spaces | Number | Listings / Google Maps | Estimate if not listed |
| Assessment Date Range | Date range | — | Start/end dates for all date-dependent metrics |
| Comp Set | List | CoStar / Analyst selection | 3–5 competitive properties with addresses |
| Owner Contact | Text | — | Full engagement only — for financial benchmark intake scheduling |

---

## 2. Pre-Audit Digital Review `[DOOR OPENER]`

All data in this section is publicly available. Collected during the door opener via desk research; does not need to be repeated during a full engagement.

Requires laptop/desktop with internet access.

### 2A. Online Reputation `[DOOR OPENER]`

**Public source:** Review platform profile pages

**Platforms to check:** Google, Yelp, Apartments.com, ApartmentRatings, Facebook, Zillow

For each platform, record:

| Field | Format | Instructions |
|-------|--------|--------------|
| Platform URL | URL | Link to the property's profile page |
| Profile exists | Y/N | Does the property have a profile on this platform? |
| Review count | Number | Total reviews on this platform |
| Average rating | Number (1 decimal) | Platform-reported average star rating |
| Reviews in last 90 days | Number | Count reviews with post dates within last 90 days |

**Computed outputs (auto-calculated):**
- Avg Review Score: Volume-weighted average across all platforms
- Review Volume: Sum of all review counts
- Review Recency: Sum of reviews in last 90 days
- Platform Coverage: Count of platforms with profiles and reviews

**Evidence:** Screenshot of each platform profile page showing rating and review count.

### 2B. Google Business Profile `[DOOR OPENER]`

**Public source:** Google Maps / Google Business Profile

| Field | Format | Instructions |
|-------|--------|--------------|
| GMB Claimed | Y/N | Is the Google Business Profile claimed (not showing "Claim this business")? |
| GMB Optimized | Y/N | Check all: business hours listed, 10+ photos, business description filled, categories set, services listed. All must be present for Y. |

**Evidence:** Screenshot of the full Google Business Profile.

### 2C. Digital/Social Presence `[DOOR OPENER]`

**Public source:** Social media platform profiles, property website

For each platform (Facebook, Instagram, TikTok, LinkedIn, YouTube):

| Field | Format | Instructions |
|-------|--------|--------------|
| URL / Handle | URL/Text | Link to profile |
| Account exists and active | Y/N | Active = posted within last 60 days |
| Follower/like count | Number | Current followers (Instagram, TikTok, LinkedIn, YouTube) or page likes (Facebook) |
| Post Frequency | Select | Daily / 2-3x/Week / Weekly / Bi-Weekly / Monthly / Rarely / Never |

Additional channels:

| Field | Format | Instructions |
|-------|--------|--------------|
| Blog/Content Marketing | Y/N | Does the property have a blog or content marketing program? |
| Email Marketing | Y/N | Email marketing campaigns for prospects or residents? |
| Paid Advertising Used | Y/N | Any paid digital advertising? |
| Paid Ad Platforms | Text | Which platforms? (Google, Facebook, Instagram, etc.) |

**Computed outputs:**
- Total Audience Size: Sum of followers/likes across all active platforms
- Post Consistency: Average posts per week per active platform (sample last 30 days)

**Evidence:** Screenshot of each platform profile showing follower count and recent posts.

### 2D. Website Quality `[DOOR OPENER]`

**Public source:** Property website

Visit the property's website (not ILS listings) and record:

| Field | Format | Instructions |
|-------|--------|--------------|
| Website URL | URL | |
| Website Exists | Y/N | Property has a dedicated website (not just an ILS listing page) |
| Mobile Responsive | Y/N | Open on mobile device or use browser dev tools mobile view |
| Live Chat | Y/N | Chat widget or chatbot present |
| Contact Form | Y/N | Working contact/inquiry form (test submit if possible) |
| Floor Plans | Y/N | Floor plan images or diagrams available and downloadable |
| Photo Gallery | Y/N | Dedicated photo gallery section |
| Unit Availability | Y/N | Shows current available units with pricing |
| Virtual Tours | Y/N | 3D walkthrough, virtual tour, or video tour available |
| Online Application Available | Y/N | Application can be started from the website |
| Tour Scheduling Available | Y/N | Prospects can schedule tours from the website |

**Evidence:** Screenshots of website homepage, floor plans page, and availability page.

### 2E. Listing Audit `[DOOR OPENER]`

**Public source:** ILS listing platforms, property website

**Platforms to audit:** Apartments.com, Zillow, Rent.com, Trulia, Realtor.com, Craigslist, Facebook Marketplace, property website (minimum 3 platforms)

#### Platform Coverage

For each platform where the property is listed:

| Field | Format | Instructions |
|-------|--------|--------------|
| Listed on [Platform] | Y/N | Active listing present? |
| Building Page URL | URL | Link to the listing |

Summary fields:

| Field | Format | Instructions |
|-------|--------|--------------|
| Platform count | Number | Count of platforms with active listings |
| ILS coverage | Tiered | Both Apartments.com + Zillow = "Both"; one = "One"; neither = "Neither" |
| Listing Posting Method | Select | Centralized Syndication / Partial Syndication / Manual Per Platform |
| Syndication Tool | Text | Name of syndication tool if used |
| Who Manages Listings | Select | In-house / PM Company / External Agency / Mix |
| Update Frequency | Select | Real-time / Daily / Weekly / Manual |

#### Per-Platform Listing Assessment

For each platform where listed, complete a listing assessment card:

| Field | Format | Instructions |
|-------|--------|--------------|
| Platform | Text | |
| Photo Count | Number | Total photos on this listing |
| Photo Quality (1-10) | Number | Overall quality rating |
| Description Quality (1-10) | Number | Quality of the text description |
| Description Word Count | Number | |
| Floor Plan Available | Y/N | |
| Virtual Tour Available | Y/N | |
| Amenities Listed | Y/N | |
| Pricing Accurate | Y/N | Matches PM system / other platforms |
| Matches Availability | Y/N | Available units match reality |
| Contact Info Accurate | Y/N | |
| Listing URL | URL | |
| Notes | Text | |

#### Photo Quality (primary listing platform)

| Field | Format | Instructions |
|-------|--------|--------------|
| Hero/Primary Image Present | Y/N | Strong, high-quality featured image |
| Exterior Building Shots Count | Number | Number of exterior photos |
| Unit Interior - Living Room Shown | Y/N | |
| Unit Interior - Kitchen Shown | Y/N | |
| Unit Interior - Bedrooms Shown | Y/N | |
| Unit Interior - Bathrooms Shown | Y/N | |
| Unit Interior - Features Shown (closets, balcony) | Y/N | |
| Amenity Photo - Pool | Y/N | |
| Amenity Photo - Fitness Center | Y/N | |
| Amenity Photo - Clubhouse | Y/N | |
| Other Amenity Photos Count | Number | |
| Total Amenities at Property | Number | |
| Amenities Photographed Count | Number | |
| Lifestyle/Community Photos Count | Number | |
| Professional Photographer Used | Y/N | Ask management |
| Last Photo Update Date | Date | Ask management |
| Shows Actual Units | Select | Yes / No / Mix |

#### Content Quality (primary listing platform)

| Field | Format | Instructions |
|-------|--------|--------------|
| Unique Selling Points Mentioned | Y/N | Description highlights what makes this property different |
| Neighborhood Context Included | Y/N | Mentions nearby amenities, transit, schools, entertainment |
| Call-to-Action Included | Y/N | "Schedule a tour," "apply today," or similar |
| Contact Info Clear | Y/N | Phone and/or email clearly displayed |
| Floor Plans Available | Y/N | Floor plan images on listing |
| Unit Specs Accurate | Y/N | Square footage and bed/bath counts match reality |
| Amenities Fully Listed | Y/N | All community and unit amenities listed |
| Pet Policy Stated | Y/N | Pet policy clearly stated |
| Lease Terms Mentioned | Y/N | Available lease term lengths mentioned |

#### Listing Accuracy (cross-platform comparison — minimum 3 platforms)

| Field | Format | Instructions |
|-------|--------|--------------|
| Pricing Accurate Across Platforms | Y/N | Same pricing shown on all platforms |
| Availability Accurate | Y/N | Available units match across platforms and PM system |
| Unit Types/Sizes Correct | Y/N | Unit types, bed/bath counts, square footages consistent |
| Amenities List Accurate | Y/N | Same amenities listed everywhere |
| Photos Match Property Condition | Y/N | Photos represent current condition (verify during site visit) |
| Specials Updated | Y/N | Advertised promotions are current (not expired) |
| Contact Info Current | Y/N | Phone numbers, emails, office hours correct |
| Error Details | Text | Note any discrepancies found |

**Evidence:** Screenshots of listing pages on 3+ platforms with key differences highlighted.

---

## 3. Property Profile and Intake

The property's identity — details, amenities, market context, and unit features. Sections 3A–3E are initially populated from public sources during the door opener, then verified and corrected on-site during the full engagement.

### 3A. Building Amenities (~40 Y/N fields) `[DOOR OPENER → VERIFIED ON-SITE]`

**Door opener source:** ILS listings, property website, Google Maps photos
**Full engagement:** Verify each amenity on-site during property walk. Mark each as Confirmed / Corrected / Not Listed.

Check presence of each amenity. During door opener, record Y/N/Unknown from public sources. During full engagement, walk the property and verify each entry.

| Verification Status | Meaning |
|---------------------|---------|
| Confirmed | On-site observation matches door opener data |
| Corrected | Door opener data was wrong — updated with on-site finding |
| Added | Amenity exists but was not listed in any public source |
| Not Available | Cannot be determined from public sources (door opener only) |

**Core:** Pool, Fitness Center, Clubhouse, Business Center
**Premium:** Hot Tub, Co-working Space, Theater, Guest Suites
**Convenience:** Package Lockers, Valet Trash, Concierge, Dry Cleaning, Package Service, Doorman
**Recreation:** Yoga Studio, Sports Courts, Playground, BBQ Area, Fire Pits, Bike Storage, Kids Playroom, Game Room
**Pet:** Dog Park, Dog Wash, Pet Spa
**Dining:** Onsite Restaurant, Demonstration Kitchen, Event/Catering Kitchen
**Event:** Event Venue / Ballroom, Roof Deck
**Parking:** EV Charging Stations, Resident Parking, Guest Parking, Valet Parking, Gated Community, Controlled Access
**Parking Type:** Select: None / Open / Carport / Covered / Garage

For each amenity, record: **Value** (Y/N) | **Source** (Listing / Website / Google Maps / On-Site) | **Verification** (Confirmed / Corrected / Added — full engagement only)

### 3B. Unit Amenities (~30 Y/N fields) `[DOOR OPENER → VERIFIED ON-SITE]`

**Door opener source:** ILS listings, property website, floor plan descriptions
**Full engagement:** Verify by touring units or confirming with management. Mark each as Confirmed / Corrected / Added.

**Kitchen:** Dishwasher, Garbage Disposal, Microwave, Stainless Steel Appliances, Granite/Quartz Countertops
**Bathroom:** Soaking Tub, Jetted Tub, Dual Vanities, Separate Shower, Heated Floors, Steam Shower, Bidet, Frameless Glass Shower
**Laundry:** In-Unit Washer/Dryer, W/D Hookups Only, Shared/Common Laundry
**Climate:** Central A/C, In-Unit Thermostat Control, Smart Thermostat
**Flooring:** Hardwood/Vinyl Plank Flooring, Carpet, Updated Fixtures & Hardware
**Storage:** Walk-In Closet, Balcony/Patio, Private Outdoor Space, In-Unit Storage, Private Garage/Parking Option
**Tech:** Smart Locks, USB Outlets, Pre-Wired for Internet/Cable, In-Unit Alarm/Security System
**Other:** Ceiling Fans, Window Blinds/Treatments, Pet-Friendly Unit Features, ADA Accessible Units Available
**Plus:** Other Unit Amenity (Text)

For each amenity, record: **Value** (Y/N) | **Source** (Listing / Website / Unit Tour) | **Verification** (Confirmed / Corrected / Added — full engagement only)

### 3C. Market Context `[DOOR OPENER]`

**Public source:** CoStar, local market reports, Census data, BLS

Collect from CoStar, local market reports, or public economic data:

| Field | Format | Instructions |
|-------|--------|--------------|
| Submarket Name | Text | |
| Submarket Vacancy % | Number | Current submarket vacancy rate |
| Submarket Avg Rent (per sq ft) | Number | |
| YoY Rent Growth % | Number | Year-over-year rent growth for submarket |
| New Supply (units) | Number | Units under construction or delivered in last 12 months |
| Employment Growth % | Number | Local employment growth |
| Population Growth % | Number | Local population growth |
| Median Household Income | Number | |

### 3D. Resident Events `[DOOR OPENER → VERIFIED ON-SITE]`

**Door opener source:** Social media posts, property website events page, Google Business Profile posts
**Full engagement:** Verify and expand during management interview. Mark each as Confirmed / Corrected / Not Available.

| Field | Format | Door Opener Source | Instructions |
|-------|--------|--------------------|--------------|
| Management-Hosted Events Offered | Y/N | Social media / website | Look for event photos, announcements |
| Event Frequency | Select | Social media post history | Weekly / Monthly / Quarterly / 2x/year / Annually / Never |
| Last Event Date | Date | Social media posts | Date of most recent event post |
| Event Attendance Rate (%) | Number | Not available (door opener) | Typical attendance as % of residents — full engagement only |
| Events Budget ($ Annual) | Number | Not available (door opener) | Full engagement only |
| Event Types | Checklist | Social media / website | Social / Holiday / Appreciation / Fitness/Wellness / Educational / Food & Beverage / Other |
| Resident Event Hosting Available | Y/N | Website | Can residents book community spaces for their own events? |
| Rentable Event Spaces Available | Y/N | Website | |
| Space Rental Fee Structure | Select | Not available (door opener) | Free / Flat Fee / Hourly / Deposit Only — full engagement only |
| Avg Rental Revenue ($/month) | Number | Not available (door opener) | Full engagement only |
| Booking System in Place | Y/N | Website | |
| Event Types Allowed | Checklist | Website | Private Parties / Meetings / Classes / Other |

### 3E. Resident Services + Mobile App `[DOOR OPENER → VERIFIED ON-SITE]`

**Door opener source:** Property website (services page), App Store / Google Play (mobile app), ILS listings
**Full engagement:** Verify and expand during management interview and site visit. Mark each as Confirmed / Corrected / Not Available.

**Services (all Y/N):**
Valet Trash Service, Package Management System, Concierge Services, Housekeeping/Cleaning Services, Amenity Rental Program, Pet Care Services, Day Care Services, Valet Parking, Guest Suites Available, Pool Side Valet & Services, In-Unit Dining Room Service, Dry Cleaning Services
**Plus:** Other Services (Text)

For each service, record: **Value** (Y/N) | **Source** (Website / Listing / On-Site) | **Verification** (Confirmed / Corrected / Added — full engagement only)

**Resident Mobile App:**

| Field | Format | Door Opener Source | Instructions |
|-------|--------|--------------------|--------------|
| Resident Mobile App Available | Y/N | App Store / Google Play | Search for property name or PM company app |
| Online Rent Payment | Y/N | App Store description | |
| Amenity Reservation | Y/N | App Store description | |
| Resident Services Access | Y/N | App Store description | |
| Service/Maintenance Requests | Y/N | App Store description | |
| Package Notifications | Y/N | App Store description | |
| Guest Access Management | Y/N | App Store description | |
| Community Forum / Chat | Y/N | App Store description | |
| Lease / Document Access | Y/N | App Store description | |
| Other Mobile Capabilities | Text | App Store description | |

---

## 4. Mystery Shop Protocol `[FULL ENGAGEMENT]`

Conducted by a secret shopper posing as a prospective resident. The shopper should have a credible prospect profile (move-in timeline, budget, unit type preference). Applied identically to the subject property AND each competitor.

### 4A. Mystery Shop Overview

| Field | Format | Instructions |
|-------|--------|--------------|
| Mystery Shop Conducted | Y/N | |
| Date Conducted | Date | |
| Agent Name | Text | Name of leasing agent who conducted the tour |

### 4B. Phone Shop

Call the leasing office during business hours. Record:

| Field | Format | Instructions |
|-------|--------|--------------|
| Phone: Friendly Professional Greeting | Y/N | Was the greeting warm and professional? |
| Phone: Answered Within 3 Rings | Y/N | Phone answered within 3 rings (or did it go to VM/hold)? |
| Phone: Enthusiasm & Positive Attitude | Y/N | Did the agent demonstrate enthusiasm about the property? |
| Phone: Described Community & Features | Y/N | Did the agent proactively describe the community? |
| Phone: Asked Qualifying Questions | Y/N | Did the agent ask about needs (timeline, budget, size)? |
| Phone: Offered Incentives/Specials | Y/N | Were any current promotions mentioned? |
| Phone: Matched Apartment to Needs | Y/N | Did the agent suggest a specific unit or floor plan? |
| Phone: Attempted to Schedule Tour | Y/N | Did the agent try to book a tour? |
| Phone: Collected Contact Info | Y/N | Did the agent ask for name, email, or phone number? |
| Telephone — Impression Score (1-10) | Number | Overall impression of the phone experience |
| Phone Response Time | Number | Time until phone was answered |
| Phone Response Unit | Select | Minutes / Hours |
| Email Response Time | Number | Time until email inquiry was responded to |
| Email Response Unit | Select | Minutes / Hours |

### 4C. In-Person Tour

Visit the property for a scheduled tour. Record:

**Greeting:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Prompt Acknowledgment | Y/N | Were you acknowledged within 1 minute of entering? |
| Eye Contact & Smile | Y/N | Did the agent make eye contact and smile? |
| Handshake / Introduced by Name | Y/N | Did the agent introduce themselves by name? |
| Asked Prospect's Name | Y/N | Were you asked your name? |
| Built Rapport | Y/N | Did the agent engage in small talk or rapport-building? |
| Offered Refreshments | Y/N | Were water, coffee, or other refreshments offered? |
| Greeting — Impression Score (1-10) | Number | Overall impression of the greeting |

**Needs Assessment:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Asked Move-In Timeline | Y/N | Were you asked when you need to move? |
| Asked Floor Plan / Size | Y/N | Were you asked about preferred unit size? |
| Asked Budget / Price Range | Y/N | Were you asked about budget? |
| Asked Lifestyle Needs | Y/N | Were you asked about lifestyle preferences (pets, parking, etc.)? |
| Asked What's Most Important | Y/N | Were you asked what matters most in your next home? |
| Actively Listened | Y/N | Did the agent demonstrate active listening? |
| Needs Assessment — Impression Score (1-10) | Number | Overall impression of needs assessment |

**Timing:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Wait Time | Minutes | Time from arrival to first acknowledgment |
| Tour Duration | Minutes | Total time of the tour (from leaving office to returning) |

**Tour Conduct:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Showed Model or Available Unit | Y/N | Were you shown an actual unit? |
| Highlighted Features & Benefits | Y/N | Did the agent point out specific features and explain their value? |
| Pointed Out Amenities | Y/N | Were community amenities shown and explained? |
| Tailored to Prospect Needs | Y/N | Was the tour customized based on your stated needs? |
| Demonstrated Product Knowledge | Y/N | Could the agent answer questions confidently? |
| Competitive Landscape Knowledge | Y/N | Could the agent speak about nearby competitors? |
| Submarket/Neighborhood Knowledge | Y/N | Could the agent describe the neighborhood? |
| Discussed Lease Terms & Costs | Y/N | Were lease terms, pricing, and move-in costs discussed? |
| Property Curb Appeal Observed | Y/N | Did the property exterior make a positive first impression? |
| Fair Housing Compliance Observed | Y/N | Were all interactions consistent with fair housing practices? |
| Presentation — Impression Score (1-10) | Number | Overall impression of the tour/presentation |

**Closing:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Asked for the Lease | Y/N | Did the agent directly ask you to apply? |
| Overcame Objections | Y/N | When you expressed hesitation, did the agent address it? |
| Discussed Next Steps | Y/N | Were clear next steps outlined? |
| Created Urgency | Y/N | Did the agent create urgency? |
| Provided Pricing & App Info | Y/N | Were you given pricing details and application information? |
| Closing — Impression Score (1-10) | Number | Overall impression of the close |

**Fair Housing (scored separately):**

| Field | Format | Instructions |
|-------|--------|--------------|
| No discriminatory statements or questions | Y/N | |
| Consistent treatment regardless of protected class | Y/N | |
| Proper handling of accommodation requests | Y/N | |
| Fair Housing — Impression Score (1-10) | Number | |

**Property Condition (shopper's observation):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Curb appeal and grounds well-maintained | Y/N | |
| Leasing office clean and well-presented | Y/N | |
| Model / show unit in good condition | Y/N | |
| Common areas and amenities clean | Y/N | |
| Signage and wayfinding clear | Y/N | |
| Property Condition — Impression Score (1-10) | Number | |

### 4D. Follow-Up Evaluation

Wait 48 hours after the tour, then record:

| Field | Format | Instructions |
|-------|--------|--------------|
| Contact Received | Y/N | Did you receive any follow-up contact? |
| Was Personalized | Y/N | Was the follow-up personalized (not generic template)? |
| Referenced Visit Details | Y/N | Did the follow-up reference specific details from your visit? |
| Made Another Close Attempt | Y/N | Did the follow-up include another attempt to get you to apply? |
| Follow-Up — Impression Score (1-10) | Number | Overall impression of follow-up |
| Follow-up timing | Select | Same day / Next day / Within 48 hours / After 48 hours / Never |
| Follow-up method | Select | Phone / Email / Text / Multiple Methods / None |

**Overall Assessment:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Overall Experience (1-10) | Number | |
| Strengths Observed | Text | |
| Gaps / Areas for Improvement | Text | |

**Evidence:** Screenshots of follow-up emails/texts received. Notes from phone follow-up.

---

## 5. Site Visit — Observation `[FULL ENGAGEMENT]`

### 5A. Office Environment

| Field | Format | Instructions |
|-------|--------|--------------|
| Office Location/Visibility | Text | Description of where the office is and how easy it is to find |
| Office Hours - Weekday | Text | e.g., "9am-6pm" |
| Office Hours - Saturday | Text | |
| Office Hours - Sunday | Text | |
| Days Open Per Week | Number | |
| Visitor Parking Available | Y/N | |
| Exterior Signage Clear | Y/N | |
| Wayfinding Signs | Y/N | Clear directional signage from property entrance to office |
| Waiting Area Seating | Y/N | Guest seating in or near leasing office |
| Refreshments Offered | Y/N | Water, coffee, or snacks available |
| WiFi Available | Y/N | Guest WiFi accessible |
| Restroom Available/Clean | Y/N | |
| Marketing Materials Displayed | Y/N | Brochures, flyers, community info |
| Technology/Tablets Used | Y/N | Technology setup for presentations |
| Accessibility | Tiered | Parking + clear signage = "Parking+Signage"; only one = "One" |
| Professional Setup | Tiered | Both marketing materials + tech = "Materials+Tech"; only one = "One" |

### 5B. Model Unit

| Field | Format | Instructions |
|-------|--------|--------------|
| Model Available | Y/N | Is a designated model unit available for tours? |
| Model Quality | Tiered | Fully furnished / Partial / None |
| Model Positioning | Tiered | Typical / Best-case / Aspirational |
| Model Bedrooms/Baths | Text | Unit type of the model |
| Smell/Ambiance Observation | Text | Notes on scent, lighting, feel |
| Lighting Quality Observation | Text | Natural light, fixtures, overall brightness |

### 5C. Overall Property Condition

Walk the entire property. Rate each category:

| Field | Format | Instructions |
|-------|--------|--------------|
| Overall Condition Rating | Tiered: Excellent / Good / Fair / Poor / Critical | General impression of the entire property |
| Common Areas Rating | Tiered: Excellent / Good / Fair / Poor / Critical | Lobbies, hallways, stairwells, laundry rooms, elevators |
| Exterior Presentation | Tiered: Excellent / Good / Fair / Poor / Critical | Grounds, parking, signage, lighting, landscaping, building facades |
| Amenities Condition Rating | Tiered: Excellent / Good / Fair / Poor / Critical | Pool, gym, clubhouse, dog park, playgrounds, business center |
| Issues Count | Number | Count of distinct observable physical issues |
| Specific Issues Noted | Text | Description of each issue |

**Rating definitions:**
- **Excellent:** Like-new or recently renovated, no visible issues
- **Good:** Well-maintained, minor wear consistent with age, no deferred items
- **Fair:** Functional but showing wear, some deferred maintenance visible
- **Poor:** Multiple deferred items, significant wear, negatively impacts experience
- **Critical:** Unsafe conditions, major system failures, immediate attention required

**Evidence:** Photos of each area rated. Photos of each counted issue.

### 5D. Capital Asset Condition

For each system, visually inspect and interview management about age and maintenance history:

| System | Condition Rating | Type/Material | Install/Replace Year | Last Service Date | Observation Method |
|--------|-----------------|---------------|---------------------|-------------------|-------------------|
| Roof | Good / Fair / Poor / Critical | Flat / Pitched / Metal / Tile / Other | Year | Date | Visual from ground + management interview |
| HVAC Systems | Good / Fair / Poor / Critical | Central / PTAC / Mini-Split / Boiler / Other | Year | Date | Equipment age, complaints, WO history |
| Plumbing | Good / Fair / Poor / Critical | — | — | — | Pipe material, visible leaks, water pressure |
| Plumbing Riser Age | Years (if known) | — | — | — | Ask management; record "Unknown" if not available |
| Electrical | Good / Fair / Poor / Critical | — | — | — | Panel condition, wiring age, capacity concerns |
| Electrical Panel Age | Years (if known) | — | — | — | Ask management; record "Unknown" if not available |
| Siding / Facade | Good / Fair / Poor / Critical | — | — | — | Walk exterior for cracking, peeling, water damage |
| Windows | Good / Fair / Poor / Critical | — | — | — | Seal integrity, condensation, operability |
| Parking Surfaces | Good / Fair / Poor / Critical | — | — | — | Striping, drainage, cracking, potholes |
| Elevator Present | Y/N | — | — | — | Record whether property has elevators (separate from condition) |
| Elevators | Good / Fair / Poor / Critical / N/A | — | — | Last Inspection Date | Ride each elevator, check certificate, ask about issues |
| Water Heaters | Good / Fair / Poor / Critical | Tank / Tankless / Boiler | Year | — | Management interview |
| Fire/Life Safety Systems | Good / Fair / Poor / Critical | — | — | Last Inspection Date | Sprinklers, alarms, extinguishers, emergency lighting |

**Tier definitions:**
- **Good:** Functional, well-maintained, >50% remaining useful life
- **Fair:** Functional but aging, approaching midlife
- **Poor:** Frequent repairs, approaching end of useful life, replacement should be planned
- **Critical:** At or past useful life, replacement needed now

**Evidence:** Photos of each system. Document age and service dates.

### 5E. Deferred Maintenance

During the property walk, document all deferred maintenance items:

| Field | Format | Instructions |
|-------|--------|--------------|
| Number of Deferred Items | Number | Count of distinct items that should have been addressed |
| Critical Systems Affected | Y/N | Any deferred items on major systems (roof, HVAC, plumbing, electrical, structural)? |
| Safety Hazards Present | Y/N | Any deferred items creating safety risks? |
| Deferred Maintenance Details | Text | Description of all deferred items |
| Estimated Deferred Cost ($) | Number | Rough total cost estimate for all deferred items |

For each deferred item, record: location, description, affected system, estimated severity.

**Evidence:** Photo of each deferred maintenance item.

### 5F. Fire / Safety Compliance

| Field | Format | Instructions |
|-------|--------|--------------|
| Fire/Safety Inspection Current | Y/N | Ask to see certificate / last inspection report |
| Last Fire Inspection Date | Date | |
| Open Fire Code Violations | Y/N | |
| Open Violation Count | Number | |
| Violation Details | Text | |
| No Open Code Violations (any type) | Y/N | Check with local jurisdiction if possible |
| ADA Compliance Met | Y/N | Observe accessible units and common areas |
| Insurance Current | Y/N | Ask to see certificate of insurance |
| Last REAC / NSPIRE Score | Number | If HUD/LIHTC property |
| Elevator Inspection Current | Y/N | If applicable |
| Last Elevator Inspection Date | Date | If applicable |

**Evidence:** Photos of inspection certificates, violation notices.

### 5G. Unit Condition — Vacant Walks

**Sampling protocol:** Walk a minimum of 3 vacant units (or all if fewer than 3). If 10+ vacant units, walk at least 5. Select across different floor plans, buildings, and floor levels.

For EACH unit walked, rate each category independently:

**Scoring condition categories:**

| Category | Format | What to Observe |
|----------|--------|-----------------|
| Flooring | Excellent / Good / Fair / Poor | Carpet wear, hard surface condition, transitions, stains, damage |
| Walls / Paint | Excellent / Good / Fair / Poor | Paint condition, patches, holes, scuff marks, stains, trim |
| Kitchen Cabinets & Countertops | Excellent / Good / Fair / Poor | Cabinet doors, drawer operation, countertop surface |
| Kitchen Appliances | Excellent / Good / Fair / Poor | Age, condition, cleanliness, operation (open fridge, check stove) |
| Bathroom Fixtures & Tile | Excellent / Good / Fair / Poor | Faucets, toilet, shower/tub, tile, grout, caulking |
| Windows & Blinds | Excellent / Good / Fair / Poor | Window operation, seal condition, blind function |
| Doors & Hardware | Excellent / Good / Fair / Poor | Door operation, locks, handles, weatherstripping, closet doors |
| Lighting Fixtures | Excellent / Good / Fair / Poor | Fixture condition, all bulbs working, cover plates present |
| HVAC (in-unit) | Excellent / Good / Fair / Poor | Thermostat operation, filter condition, vent covers, noise |
| Overall Cleanliness | Excellent / Good / Fair / Poor | Is the unit move-in ready? Dust, debris, cleaning quality |
| General Finish Level | Dated / Acceptable / Updated / Modern | Overall interior finish relative to market expectations |

**Readiness checklist (per unit):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Cleanliness Acceptable | Y/N | |
| Odor Present | Y/N | |
| Pest Evidence | Y/N | |
| Water Damage / Staining | Y/N | |
| Appliances Functional | Y/N | Test all appliances |
| Windows / Blinds Intact | Y/N | |
| HVAC Operational | Y/N | |
| Overall Unit Ready to Show | Y/N | Could a prospect see this unit today? |
| Condition Notes | Text | |

**Aggregation:** After walking all units, average each scoring category across all sampled units.

**Evidence:** Photos of each category in each unit walked. Note unit number on each photo.

### 5H. Maintenance Back-of-House Inspection

Visit the maintenance shop/office area during the site visit:

| Field | Format | Instructions |
|-------|--------|--------------|
| Shop / Work Area Organized | Y/N | |
| Parts Inventory Visible and Labeled | Y/N | Common parts stocked and organized |
| Safety Equipment Present | Y/N | Goggles, gloves, etc. available |
| Fire Extinguisher Present and Current | Y/N | |
| Chemical Storage Compliant | Y/N | Labeled, ventilated, properly stored |
| Vehicle / Cart Condition | Good / Fair / Poor | Maintenance vehicles/carts |
| Back-of-House Cleanliness | Good / Fair / Poor | |

---

## 6. Field Audit Templates — Unit-Level Data `[FULL ENGAGEMENT]`

These are row-per-unit worksheets. Each template targets a specific population of units/residents. PM data fields are pre-populated from system exports; the auditor fills the remaining columns during on-site interviews or observation.

### 6A. Template 1: Vacancy Observations

**Target:** All currently vacant units.

**Pre-populated from PM:** Unit #, Unit Type, Beds, Baths, SqFt, Floor, Prior Tenant Rent, Move-Out Date, Move-Out Reason, Make-Ready Start, Make-Ready End, Market Rent, Asking Rent

**Auditor fills (per unit):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Marketed (Y/N) | Y/N | Is this unit independently listed for rent? |
| Like-Kind Listing Live Date | Date | When did a listing go live for this unit type? |
| Marketed Date | Date | When was this specific unit first marketed? |
| Listing Platform | Text | Where is it listed? |
| Listing Type | Text | Direct / Syndicated / Both |
| Representative Unit | Y/N | Is another unit used as the show unit for this floor plan? |
| Last Refresh Date | Date | When was the listing last refreshed? |
| Leasing Agent | Text | Agent assigned to this unit |
| Tours Scheduled | Number | |
| Tours Completed | Number | |
| Applications Received | Number | |
| Showing Method | Select | Self-guided / Agent-led / Virtual |
| Why Still Vacant | Text | |
| Concession Type | Text | |
| Concession Proactive/Reactive | Select | Was the concession offered proactively or in response to prospect negotiation? |
| Notes | Text | |

### 6B. Template 2: Move-In Interviews

**Target:** Recent move-ins (last 30–90 days).

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Move-In Date, Monthly Rent, Lease Start, Lease End, Lease Term, Concession Amount

**Auditor fills (per move-in):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Leasing Agent | Text | Who closed the lease? |
| Lead Source | Text | How did the tenant find the property? |
| Tours Before Lease | Number | |
| Days: Lead to Tour | Number | |
| Days: Tour to Application | Number | |
| Days: Application to Lease | Number | |
| Ghost/No-Show Before Lease | Y/N | Did this prospect no-show before eventually leasing? |
| Screening Score/Outcome | Text | |
| Concession Type | Text | |
| Concession Proactive/Reactive | Select | |
| Broker Involved | Y/N | |
| Broker Fee | Number | |
| Leasing Fee | Number | |
| Broker Co-Op Fee | Number | |
| Showing Method | Select | Self-guided / Agent-led / Virtual |
| Notes | Text | |

### 6C. Template 3: Turnover Interviews

**Target:** Recent move-outs (last 30–90 days).

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Move-Out Date, Move-Out Reason (PM-recorded), Rent at Departure, Tenure, Turnover Cost Total + breakdown

**Auditor fills (per move-out):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Resident's Stated Primary Reason for Leaving | Select | Rent Increase / Maintenance Issues / Staff or Management / Bought Home / Job Relocation / Roommate or Relationship Change / Neighborhood or Safety / Upgraded Unit Elsewhere / Downgraded for Cost / Lease Violation / Other |
| Unit Condition at Move-Out | Select | Good / Fair / Poor / Damaged |
| Make-Ready Scope | Select | Standard / Heavy / Full Renovation |
| Lease Break Fee Collected (amount) | Number | |
| Holdover Rate Charged | Y/N | |
| Screening Score (original) | Text | What was this tenant's screening score at move-in? |
| Agent Who Placed Tenant | Text | |
| Concession at Original Move-In | Y/N | |
| Original Concession Amount | Number | |
| Original Move-In Rent | Number | |
| Number of Renewals | Number | |
| Renewal Rejected Reason | Text | If applicable |
| Notes | Text | |

### 6D. Template 4: Renewal Context

**Target:** Residents approaching lease expiration (60–90 days out) or currently on month-to-month.

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Current Rent, Lease End, Tenure, Renewal Count

**Auditor fills (per resident):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Renewal Contacted | Y/N | Has management reached out about renewal? |
| Renewal Offer Date | Date | |
| Renewal Offered Rent | Number | |
| Renewal Offered Term | Text | |
| Renewal Outcome | Select | Accepted / Declined / Pending / No Response |
| Renewal Accepted Date | Date | |
| Renewal Rejected Reason | Text | |
| Resident Sentiment | Select | Happy / Neutral / Unhappy / At-Risk |
| Competitor Offer Amount | Number | If resident mentioned a competitor offer |
| Notes | Text | |

### 6E. Template 5: Lease Expiring Audit

**Target:** All leases expiring within 120 days.

**Pre-populated from PM:** Unit #, Unit Type, Tenant Name, Current Rent, Lease End, Months Remaining

**Auditor fills (per lease):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Renewal Contacted | Y/N | |
| Resident Sentiment | Select | Happy / Neutral / Unhappy / At-Risk |
| Expected Outcome | Select | Likely to Renew / Likely to Vacate / Unknown |
| Notes | Text | |

### 6F. Template 6: Recently Leased

**Target:** Leases signed in the last 30–60 days.

**Pre-populated from PM:** Unit #, Unit Type, Lease Start, Monthly Rent, Concession Amount

**Auditor fills (per lease):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Showing Method | Select | Self-guided / Agent-led / Virtual |
| Concession Type | Text | |
| Concession Proactive/Reactive | Select | |
| Leasing Agent | Text | |
| Lead Source | Text | |
| Notes | Text | |

### 6G. Template 7: CRM Lead Upload

**Target:** Lead/prospect data when PM traffic report is not available.

**Auditor fills (per lead):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Prospect ID | Text | |
| Contact Date | Date | |
| Contact Type | Text | Phone / Email / Walk-in / Web |
| Source | Text | ILS platform, referral, etc. |
| Agent | Text | |
| Unit Type Interest | Text | |
| Tour Date | Date | |
| Tour Type | Text | In-person / Virtual / Self-guided |
| Tour Outcome | Text | Completed / No-show / Cancelled |
| App Date | Date | |
| Lease Date | Date | |
| Reason Lost | Text | |

---

## 7. Management Interview `[FULL ENGAGEMENT]`

Structured interview with the property manager. Schedule 60–90 minutes.

### 7A. Organizational Structure & Staffing

**Organization:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Property Manager Name | Text | |
| PM Tenure (months) | Number | How long has the current PM been in this role? |
| PM Certifications | Text | CAM, CPM, ARM, etc. |
| Assistant Manager | Text | Name/title |
| Leasing Agent Count | Number | FTE count |
| Leasing Agent Names | Text | |
| Maintenance Tech Count | Number | FTE count |
| Other Staff | Text | Any other on-site roles |
| Open Positions | Number | Currently unfilled positions |
| Open Position Details | Text | What roles are open? |
| Staff Turnover Rate (%) | Number | Staff departures in trailing 12 months / average headcount |
| Avg Staff Tenure (months) | Number | Average months of employment across current staff |

**Compensation:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Property Manager Salary Range | Text | |
| Assistant Manager Salary Range | Text | |
| Leasing Staff Salary Range | Text | |
| Maintenance Staff Salary Range | Text | |
| Admin/Office Staff Salary Range | Text | |
| Maintenance On-Call Compensation | Text | |
| Benefits Package | Select | Full / Partial / None |
| Health Insurance Offered | Y/N | |
| Retirement/401k Offered | Y/N | |
| Housing Discount/Free Housing | Y/N | |
| Total Annual Payroll Budget | Number | |
| Overall Comp vs Market | Select | Above Market / At Market / Below Market |

### 7B. Leasing Model

| Field | Format | Instructions |
|-------|--------|--------------|
| Leasing Model | Select | In-House Leasing Team / Outside Brokerage / Hybrid (Both) |
| Brokerage Name | Text | If applicable |
| Brokerage Contract Type | Select | Exclusive / Non-Exclusive / Preferred |
| Property Oversight Level | Select | High / Moderate / Low |
| Lead Routing | Select | Brokerage Handles All / Property Qualifies then Brokerage / Split by Source |
| Leasing Agent Base Salary Range | Text | |
| Leasing Commission Structure | Text | |
| Leasing Renewal Bonuses | Text | |
| Leasing Team vs Individual | Select | Team / Individual / Hybrid |
| Leasing Agent Comp vs Market | Select | Above Market / At Market / Below Market |
| Leasing Commission Per Lease ($) | Number | |
| In-House Leasing Cost Per Lease ($) | Number | |
| Broker Co-Op Fee Schedule | Text | |
| Concession Authority Level | Select | Agent / Manager / Regional / Owner |
| Concession Policy Documented | Y/N | |

**Brokerage Oversight (if applicable):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Formal Service Agreement | Y/N | |
| Performance Metrics Tracked | Y/N | |
| Regular Reporting/Accountability Meetings | Y/N | |
| Ability to Request Specific Agents | Y/N | |
| Performance Guarantees / Termination Clause | Y/N | |

### 7C. Digital Marketing

| Field | Format | Follow-up if Yes |
|-------|--------|-------------------|
| Do you run paid social media advertising? | Y/N | Which platforms? Monthly budget? Who manages? |
| Do you run Google Ads / PPC campaigns? | Y/N | Monthly budget? Keywords targeted? Who manages? |
| Do you have email or SMS marketing campaigns? | Y/N | For prospects, residents, or both? Frequency? |

### 7D. Referral Program

| Field | Format | Follow-up if Yes |
|-------|--------|-------------------|
| Resident Referral Program Exists | Y/N | How does it work? |
| Referral Incentive Offered | Y/N | What is the incentive (cash, rent credit, gift card)? |
| Referral Incentive Amount ($) | Number | |
| Referral Tracking System | Y/N | What system? Can you show me? |
| Referrals Received Last 12mo | Number | |
| Referral Conversion Rate (%) | Number | |
| Local Business Partnerships | Y/N | Which businesses? |
| Influencer/Creator Collaborations | Y/N | Examples? |
| Co-Branded Content or Events | Y/N | Examples from last 6 months? |

### 7E. Corporate Relocation Program

| Field | Format | Follow-up if Yes |
|-------|--------|-------------------|
| Corporate Relocation Program Exists | Y/N | Describe it |
| RMC Partnerships | Y/N | Which ones? |
| Corporate Rates/Packages Offered | Y/N | What's the structure? |
| Furnished/Short-Term Options Available | Y/N | How many units? Term lengths? |
| Dedicated Relocation Contact | Y/N | Who? Title? |

### 7F. Broker/Locator Program

| Field | Format | Follow-up if Yes |
|-------|--------|-------------------|
| Broker Program Exists | Y/N | |
| Offers Broker Commission | Y/N | |
| Broker Commission Structure | Select | 1 Month's Rent / ½ Month's Rent / $1,000 Per Lease / Other |
| Broker Portal Access | Y/N | Can you show me? |
| Broker Marketing Materials | Y/N | Can I see them? |
| Direct Broker Contact | Y/N | Who? |
| Broker Lead Tracking | Y/N | What system? |
| Broker Events/Outreach | Y/N | Examples from last 12 months? |

### 7G. Lead Management

| Field | Format | Instructions |
|-------|--------|--------------|
| CRM System Used | Text | |
| Avg Email Response Time (min) | Number | |
| Avg Phone Response Time (min) | Number | |
| Follow-Up Process Documented | Y/N | Doc+Auto = documented AND automated; Doc only = manual |
| Automated Follow-Up | Y/N | |
| Follow-Up Touch Count | Number | How many touches in the nurture sequence? |
| After-Hours Handling | Select | Auto-response / Answering Service / Voicemail / None |
| Weekend Handling | Select | In-person / Auto-response / Answering service / VM / None |
| Lead Nurturing Process | Y/N | |
| Re-engagement Campaigns | Y/N | |

**Verification:** Send a test email inquiry before the interview. Record response time. Call after hours and on a weekend to verify handling claims.

### 7H. Tour Scheduling

| Field | Format | Instructions |
|-------|--------|--------------|
| Phone Scheduling Available | Y/N | |
| Email Scheduling Available | Y/N | |
| Online Self-Booking Available | Y/N | Verify on website |
| Text Scheduling Available | Y/N | |
| Weekend Availability | Y/N | |
| Evening Availability | Y/N | |
| Broker Scheduling/Access Program | Y/N | |
| Same-Day Tours Accepted | Y/N | |
| Walk-Ins Accepted | Y/N | |

### 7I. Conversion Metrics

For each of 4 time periods (Last 30 Days, Last 90 Days, Last 6 Months, Last 12 Months):

| Field | Format | Instructions |
|-------|--------|--------------|
| Total Leads Received | Number | |
| Total Tours Conducted | Number | |
| Total Tour No-Shows | Number | |
| Total Applications Received | Number | |
| Total Leases Signed | Number | |
| Avg Days: Lead to Tour | Number | |
| Avg Days: Tour to App | Number | |
| Avg Days: App to Lease | Number | |

Plus: Primary Scoring Period | Select | Last 30 Days / Last 90 Days / Last 6 Months / Last 12 Months

### 7J. Leasing Process

Walk through the entire process step by step:

| Element | Format | Verification |
|---------|--------|--------------|
| Expectations communicated to applicants upfront | Y/N | Ask to see the document/email |
| Online application available | Y/N | Verify on website |
| Mobile-friendly application | Y/N | Test on phone |
| Application status communication | Y/N | How are applicants notified? |
| Credit check performed | Y/N | |
| Background check performed | Y/N | |
| Income verification performed | Y/N | What documentation required? |
| Rental history verification | Y/N | How many prior landlords? |
| Employment verification | Y/N | |
| Electronic lease signing | Y/N | What platform? |
| Clear move-in cost breakdown provided | Y/N | Ask to see a sample |
| Deposit/fee payment online | Y/N | |
| Move-in date scheduling process defined | Y/N | |
| Pre-move-in unit inspection | Y/N | By staff or resident? |
| Move-in checklist provided | Y/N | Ask to see a sample |
| Utility setup guidance provided | Y/N | Written or verbal? |
| Key/access handoff process defined | Y/N | |
| Welcome package provided | Y/N | Ask to see one |
| New resident orientation | Y/N | In-person or virtual? How long? |
| Resident portal setup assistance | Y/N | Staff-assisted or self-service? |
| Community rules & policies reviewed | Y/N | |
| Emergency procedures communicated | Y/N | |
| Amenity walkthrough during onboarding | Y/N | |
| Typical app processing speed | Select | Same day / 1-2 days / 3-5 days / 5+ days |
| Typical screening turnaround | Select | Same day / 1-2 days / 3-5 days / 5+ days |
| Typical approval speed | Select | Same day / 1-2 days / 3+ days |
| Typical lease turnaround | Select | Same day / 1-3 days / 3-5 days / 5+ days |

**Screening criteria detail:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Minimum Credit Score | Number | |
| Income-to-Rent Ratio | Number | e.g., 3x |
| Background Check Provider | Text | |
| Decision Timeline (days) | Number | |
| Denial Rate (%) | Number | |
| Application Fee ($) | Number | |
| Move-In Costs ($) | Number | Total typical move-in costs |
| Defined Screening Criteria Documented | Y/N | Ask to see the document |
| Consistent Application of Criteria | Y/N | How do you ensure consistency? |
| Adverse Action Notice Process | Y/N | Ask to see template |

### 7K. Training & Development

| Field | Format | Follow-up |
|-------|--------|-----------|
| Formal Training Program | Y/N | Ask to see documentation |
| Onboarding Duration (days) | Number | |
| Ongoing Training Frequency | Select | Weekly / Monthly / Quarterly / Annually / Never |
| Coaching Frequency | Select | Weekly / Monthly / Quarterly / Never |
| Performance Reviews | Select | Monthly / Quarterly / Annually / Never |
| Certifications Required | Y/N | Which ones? |
| Product Knowledge Training | Y/N | What does it cover? |
| Sales/Closing Training | Y/N | Who delivers it? |
| Fair Housing Training | Y/N | How often? Last completed? |
| CRM/Systems Training | Y/N | |
| Other Training | Text | |

### 7L. Tour Experience (management-reported)

| Field | Format | Instructions |
|-------|--------|--------------|
| Pre-Tour Confirmation Sent | Y/N | |
| Pre-Tour Reminder Sent | Y/N | |
| Tour Route Defined | Y/N | Is there a standard tour route? |
| Tour Route Logical | Y/N | Does the route make sense? |
| Amenities Highlighted on Tour | Y/N | |
| Common Areas Shown | Y/N | |
| Post-Tour Follow-Up Process | Text | Describe the standard follow-up process after a tour |
| Follow-Up Timing | Number (hours) | How soon after the tour does the first follow-up occur? |

### 7M. Renewal & Retention Process

| Field | Format | Follow-up |
|-------|--------|-----------|
| Defined Renewal Process Exists | Y/N | Ask to see documentation |
| Renewal Offer Communicated in Writing | Y/N | Email, letter, or both? |
| Renewal Pricing Strategy Defined | Y/N | How are increases determined? |
| Resident Satisfaction Assessed Before Renewal | Y/N | How? Survey, call, visit? |
| Renewal Negotiation Flexibility | Y/N | What authority does staff have? |
| Electronic Renewal Signing Available | Y/N | |
| Proactive Retention Outreach Program | Y/N | Describe it |
| Retention Incentives Offered | Y/N | What types? |
| Retention Incentive Types Offered | Text | Rent credit, upgrade, etc. |
| Average Renewal Incentive Value ($) | Number | |
| Resident Feedback/Survey Program | Y/N | Frequency? Platform? |
| Exit Interview / Move-Out Survey | Y/N | |
| Resident Communication Frequency | Select | Weekly / Monthly / Quarterly / Rarely |
| Renewal Rent Increase Policy | Text | How are increases determined? |
| DNR Review Process Exists | Y/N | Who reviews? |
| DNR Criteria Documented | Y/N | Ask to see criteria |
| DNR Decisions Reviewed by Management | Y/N | Who approves? |
| DNR Communication Timeline Defined | Y/N | How many days notice? |
| Occupied Apartment Program Exists | Y/N | How does it work? |
| Non-Renewal Triggers Showing Communication | Y/N | How quickly? |
| NTV Response Speed | Select | Same day / 1-3 days / 3-5 days / 5+ days |
| Pre-Move-Out Unit Assessment | Y/N | Who does it? When? |
| Move-Out Checklist Provided | Y/N | Ask for sample |
| Outreach Timeline | Select | 120+ days / 90 days / 60 days / 30 days |
| Turnover Timeline Target (days vacant) | Number | What is the target turn time? |
| Annual Retention Program Spend | Number | |
| Renewal Incentive Budget | Number | |
| Holdover Rate Premium (%) | Number | |

### 7N. Maintenance & Property Condition

**Response Times:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Emergency Response Time Avg (hours) | Number | |
| Routine Initial Response Time Avg (hours) | Number | |

**Systems:**

| Field | Format | Instructions |
|-------|--------|--------------|
| Formal Maintenance Request System | Y/N | Portal, app, or software — ask for demo |
| Preventive Maintenance Program | Y/N | |
| PM Schedule Documented | Y/N | |
| Maintenance Process Documentation (SOPs) | Y/N | Ask to see documentation |
| Vendor Management Process | Text | |
| Parts Inventory System | Y/N | Visit maintenance shop to verify |

**Work Order Data (6-Month):**

| Field | Format | Instructions |
|-------|--------|--------------|
| Total Work Orders Completed | Number | |
| Resolved Within 3 Days | Number | |
| Resolved Within 4-7 Days | Number | |
| Resolved Within 8-30 Days | Number | |
| Still Open >30 Days | Number | |

### 7O. Screening Process

| Field | Format | Instructions |
|-------|--------|--------------|
| Defined Screening Criteria Documented | Y/N | Ask to see the document |
| Credit Check Required | Y/N | |
| Background Check Required | Y/N | |
| Income Verification Required | Y/N | What documentation? What income ratio? |
| Rental History Verification Required | Y/N | How many prior landlords? |
| Employment Verification Required | Y/N | |
| Consistent Application of Criteria | Y/N | How do you ensure consistency? |
| Adverse Action Notice Process | Y/N | Ask to see template |

---

## 8. Tour Observation (Auditor Shadow) `[FULL ENGAGEMENT]`

The auditor observes a REAL leasing tour by shadowing a leasing agent with a genuine prospect (or with a team member role-playing if no live tour is available).

**Protocol:** Introduce yourself to the leasing agent as the auditor. Explain you'll be observing. Position yourself to observe without interfering.

Record the same fields as the Mystery Shop (Section 4C) MINUS the Phone and Follow-Up sections:

- Greeting (6 Y/N items + Impression Score)
- Needs Assessment (6 Y/N items + Impression Score)
- Wait Time (minutes) and Tour Duration (minutes)
- Tour Conduct (10 Y/N items + Impression Score)
- Closing (5 Y/N items + Impression Score)
- Fair Housing (3 Y/N items + Impression Score)

**Purpose:** Second observation point to triangulate against the mystery shop. Different observer, different prospect, different day.

---

## 9. Financial Data Collection `[FULL ENGAGEMENT]`

### 9A. Owner's Budget / Benchmark Intake

Collected from the property owner or asset manager (not the on-site team). Schedule a dedicated call.

**Revenue (owner's annual budget):**

| Line Item | Format | Notes |
|-----------|--------|-------|
| Gross Potential Rent | $/year | Based on all units at current asking rents |
| Loss to Lease | $/year | |
| Budgeted Vacancy Loss | $/year | Owner's vacancy assumption |
| Budgeted Concessions | $/year | |
| Bad Debt/Collections Loss | $/year | |
| Utility Reimbursements | $/year | |
| Parking Revenue | $/year | |
| Pet Revenue | $/year | |
| Late Fees | $/year | |
| Application Fees | $/year | |
| Lease Break Fee Revenue | $/year | |
| Other Income | $/year | Any other income sources |
| Effective Gross Income | $/year | GPR - Vacancy - Concessions + Other Income |

**Expenses (owner's annual budget):**

| Line Item | Format | Notes |
|-----------|--------|-------|
| Payroll & Benefits | $/year | All on-site staff |
| Management Fee | $/year or % | |
| Leasing Commissions | $/year | |
| Marketing & Advertising | $/year | |
| Repairs & Maintenance | $/year | Day-to-day maintenance |
| Contract Services | $/year | Landscaping, pest control, etc. |
| Make-Ready/Turnover | $/year | |
| Utilities | $/year | Property-paid utilities |
| Insurance | $/year | |
| Property Taxes | $/year | |
| Trash Removal | $/year | |
| Pest Control | $/year | |
| Landscaping | $/year | |
| Snow Removal | $/year | |
| Security | $/year | |
| Legal | $/year | |
| Accounting | $/year | |
| Technology/Software | $/year | |
| Office/Admin | $/year | |
| Training | $/year | |
| Travel | $/year | |
| Capital Reserves | $/year | |
| HOA/Condo Fees | $/year | If applicable |
| Other Expenses | $/year | |
| Total Operating Expenses | $/year | Sum of all expense lines |
| Net Operating Income | $/year | EGI minus Total OpEx |

**Capital:**

| Line Item | Format | Notes |
|-----------|--------|-------|
| Capital Expenditures (budget) | $/year | Planned CapEx for current year |
| Capital Reserves (target) | $/year or $ balance | Target reserve balance or annual contribution |

**Evidence:** Copy of the owner's budget document (PDF, Excel, or print). If the owner won't share the full document, the line items above must be provided verbally and confirmed in writing.

### 9B. Marketing & Acquisition Cost Breakdown

| Field | Format | Instructions |
|-------|--------|--------------|
| Total Annual Marketing Spend | Number | |
| Marketing Spend: ILS/Listing Platforms | Number | |
| Marketing Spend: Paid Digital (Google/Social) | Number | |
| Marketing Spend: Traditional/Print | Number | |
| Marketing Spend: Other | Number | |
| Application Processing Cost (per app) | Number | |
| Lease Administration Cost (per lease) | Number | |

### 9C. Retention Costs

| Field | Format | Instructions |
|-------|--------|--------------|
| Annual Retention Program Spend | Number | |
| Renewal Incentive Budget | Number | |
| Holdover Rate Premium (%) | Number | |

---

## 10. Competitive Set Research

Collect data on 3–5 competitive properties identified during assessment setup. Sections 10A–10K are public data collected during the door opener. Section 10L (comp mystery shops) is full engagement only.

### For Each Comp Property

#### 10A. Property Details `[DOOR OPENER]`

**Public source:** ILS listings, CoStar, property website

| Field | Format | Source |
|-------|--------|--------|
| Property Name | Text | |
| Address | Text | |
| Total Units | Number | Listing, website, or ask on phone |
| Year Built | Number | Listing or CoStar |
| Property Class | Select: A / B / C / D | Auditor assessment |
| Distance from Subject (miles) | Number | Google Maps |

#### 10B. Building Amenities `[DOOR OPENER]`

**Public source:** ILS listings, property website, Google Maps photos

Same checklist as subject property (Section 3A). ~40 Y/N fields. Record which amenities each comp advertises publicly.

#### 10C. Unit Amenities `[DOOR OPENER]`

**Public source:** ILS listings, property website, floor plan descriptions

Same checklist as subject property (Section 3B). ~30 Y/N fields.

#### 10D. Unit Pricing Data (up to 40 rows per comp) `[DOOR OPENER]`

**Public source:** ILS listing platforms (Apartments.com, Zillow, etc.)

For each available unit advertised:

| Field | Format | Source |
|-------|--------|--------|
| Beds | Select | Studio / 1 / 2 / 3 / 4 |
| Baths | Select | 1 / 1.5 / 2 / 2.5 / 3 |
| Unit Type | Text | |
| Sq Ft | Number | |
| Asking Rent | Number | |
| Rent/SF | Formula | Auto-calculated |
| Floor | Text | |
| Available (Y/N) | Y/N | |
| Pvt Outdoor Space | Y/N | |
| Concession Amt ($) | Number | |
| Days Listed | Number | |
| Notes | Text | |

**Summary by unit type (Studio, 1-Bed, 2-Bed):**

| Field | Format |
|-------|--------|
| Average Asking Rent | $/month |
| Average Square Footage | SF |
| Average PPSF | $/SF |

#### 10E. Occupancy `[DOOR OPENER]`

**Public source:** Estimate from available units listed / total units (from CoStar or listing)

| Field | Format | Source |
|-------|--------|--------|
| Occupancy Rate | % | Estimate from available units / total units |

#### 10F. Online Reputation `[DOOR OPENER]`

**Public source:** Same review platforms as subject (Section 2A)

Same platform list as subject (Section 2A). Per platform: score, count, reviews in 90 days.

#### 10G. Digital Presence `[DOOR OPENER]`

**Public source:** Social media profiles, property website

Same platform list as subject (Section 2C). Per platform: URL, follower count, active Y/N, post frequency. Plus: property website URL.

#### 10H. Listing & Marketing Assessment (analyst-assessed 0-10 scores) `[DOOR OPENER]`

**Public source:** Analyst assessment based on publicly available listing/marketing data

| Field | Format |
|-------|--------|
| Platform Coverage (0-10) | Number |
| Photo Quality (0-10) | Number |
| Content Quality (0-10) | Number |
| Listing Accuracy (0-10) | Number |
| Website Quality (0-10) | Number |
| Social Marketing (0-10) | Number |
| Partnership & Referral (0-10) | Number |

#### 10I. Resident Services `[DOOR OPENER]`

**Public source:** Property website, ILS listings

Same services list as subject (Section 3E). All Y/N. Plus: Other Services (Text).

#### 10J. Resident Events `[DOOR OPENER]`

**Public source:** Social media posts, property website events page

| Field | Format | Source |
|-------|--------|--------|
| Management-Hosted Events Offered | Y/N | Check social media, website, or call |
| Resident Events Frequency | Select | Weekly / Monthly / Quarterly / 2x/year / Annually / Never |
| Event Types Offered | Text | |
| Resident Event Hosting Available | Y/N | |
| Rentable Event Spaces Available | Y/N | |
| Space Rental Fee Structure | Select | Free / Flat Fee / Hourly / Deposit Only |

#### 10K. Resident Mobile App `[DOOR OPENER]`

**Public source:** App Store, Google Play Store

| Field | Format | Source |
|-------|--------|--------|
| Resident Mobile App Available | Y/N | Check app stores or ask on phone |
| Online Rent Payment | Y/N | |
| Amenity Reservation | Y/N | |
| Resident Services Access | Y/N | |
| Maintenance Requests | Y/N | |
| Package Notifications | Y/N | |
| Guest Access | Y/N | |
| Community Forum | Y/N | |
| Lease/Document Access | Y/N | |
| Other Capabilities | Text | |
| Communication Frequency | Select | Weekly / Monthly / Quarterly / Rarely |

#### 10L. Mystery Shop — Comp Tour `[FULL ENGAGEMENT]`

Each comp property is mystery-toured using the identical evaluation checklist as the subject property (Section 4). Same phone shop, in-person tour, and follow-up evaluation. This ensures apples-to-apples scoring.

**Evidence:** Screenshots of comp listings, photos of comp property exteriors (taken during tour), mystery shop notes.

---

## 11. Technology Stack Assessment `[FULL ENGAGEMENT]`

Per-platform capability audit. For each technology platform used at the property (up to 15), record:

| Field | Format | Instructions |
|-------|--------|--------------|
| Platform Name | Text (or select from 37 known platforms) | |
| Annual Cost ($) | Number | |
| Staff Mobile Access | Y/N | |
| Functions Handled | Checklist | Which of the 16 categories below? |

### 16 Technology Function Categories

For each function, check which specific capabilities are active:

**1. Property Management:** Lease tracking & administration, Unit management (vacancies, turns), Financial reporting (basic), Document storage & management, Vendor management, Resident ledger management, Compliance tracking, Reporting & analytics, Online portal integration

**2. CRM / Lead Management:** Multi-source lead capture, Automated lead follow-up / drip campaigns, Lead pipeline tracking, Task reminders & scheduling, Lead scoring & prioritization, Reporting & analytics (lead source, conversion), Guest card management, Tour scheduling integration, Communication tracking (email, call, text)

**3. Leasing Software:** iPad / mobile tour app, Unit availability display (real-time), Prospect info capture on tour, Self-guided tour management, Tour scheduling & calendar, Digital floor plan presentation, Application start during tour, Photo / video sharing during tour, Tour route mapping

**4. Maintenance / Work Orders:** Work order creation & tracking, Preventive maintenance scheduling, Vendor management & dispatch, Parts inventory management, Mobile access for technicians, Resident communication on WO status, Reporting (response times, completion rates), Asset management

**5. Resident Portal:** Online rent payment, Maintenance request submission & tracking, Communication / messaging with staff, Access to lease documents & community info, Package tracking notifications, Amenity reservation system, Community event calendar, Lease renewal management, Mobile app availability, Smart home device integration, Resident satisfaction surveys

**6. Marketing / ILS Management:** ILS syndication, Social media management & scheduling, Email marketing campaigns, Website content management, Analytics & reporting, Reputation management integration, Virtual tour hosting

**7. Accounting / Financial:** AP automation, AR automation, Budgeting & forecasting, General ledger, Financial reporting (P&L, Balance Sheet), Bank reconciliation, PM software integration, Invoice processing

**8. Screening / Background Checks:** Credit check, Criminal background, Eviction history, Income / employment verification, Identity verification, Rental history verification, Automated decisioning, Adverse action letter generation

**9. Lease Management / E-Signatures:** Lease document generation, Electronic signature, Lease template management, Addendum / amendment support, Lease compliance tracking, Document storage & retrieval, Bulk lease generation, Audit trail / signature verification

**10. Communications / Messaging:** Bulk email / newsletter, SMS / text messaging, In-app messaging / chat, Automated notifications, Emergency mass communication, Multi-channel communication, Communication history / logging

**11. Smart Home / Access Control:** Smart lock / keyless entry, Smart thermostat control, Leak / water sensor monitoring, Package locker integration, Access control (gates, doors, elevators), Video intercom / doorbell, Lighting / energy management, Remote device management dashboard

**12. Utility Billing / Submetering:** RUBS, Submetering integration, Utility billing generation, Resident utility portal, Vacant unit utility management, Utility data analytics

**13. Payments Processing:** Online rent payment processing, ACH / bank transfer, Credit / debit card, Auto-pay / recurring, Payment reminders, Late fee automation, Partial payment handling, Payment reconciliation

**14. Renewal Management:** Renewal offer generation, Automated renewal reminders / workflow, Renewal pricing recommendations, E-sign for renewal leases, Renewal tracking / pipeline, Retention analytics / reporting, Move-out intent tracking

**15. Collections:** Past-due balance tracking, Automated collection notices, Payment plan management, Skip tracing / locate services, Collections agency integration, Legal / eviction filing support, Bad debt tracking & write-off

**16. Vendor Management:** Vendor database / directory, Vendor compliance tracking, Bid / proposal management, Purchase order processing, Invoice management, Vendor performance tracking, Contract management

### Technology Summary

| Field | Format | Instructions |
|-------|--------|--------------|
| Total Annual Technology Spend ($) | Number | |
| Tech Spend Per Unit ($) | Number | |
| Number of Active Integrations | Number | System-to-system connections |
| Staff Mobile Access Available | Y/N | |
| Resident Mobile App Available | Y/N | |
| Automation Level | Select | High / Moderate / Low / Minimal |
| Redundant Systems Identified | Select | None / Some / Many |
| Technology Gaps / Pain Points | Text | |

---

## 12. Evidence & Documentation Requirements

### Door Opener Evidence `[DOOR OPENER]`

All door opener evidence is screenshots — no physical photos or documents required.

| Screenshot | Source | Section |
|------------|--------|---------|
| Google Business Profile | Google Maps | 2B |
| Each review platform profile (Google, Yelp, Apartments.com, ApartmentRatings, Facebook, Zillow) | Review platforms | 2A |
| Each social media profile (Facebook, Instagram, TikTok, LinkedIn, YouTube) | Social platforms | 2C |
| Website homepage | Property website | 2D |
| Website floor plans page | Property website | 2D |
| Website availability page | Property website | 2D |
| Listing pages on 3+ ILS platforms | ILS platforms | 2E |
| Cross-platform comparison notes (pricing/availability discrepancies) | ILS platforms | 2E |
| Each comp property listing page | ILS platforms | 10D |
| Each comp review profile | Review platforms | 10F |
| Each comp social media profile | Social platforms | 10G |
| Each comp website homepage | Comp websites | 10G |
| Comp mobile app store page (if app exists) | App Store / Google Play | 10K |

### Full Engagement Evidence `[FULL ENGAGEMENT]`

Everything from the door opener evidence above, plus:

**Required Photos (minimum):**

| Category | Minimum Count | Notes |
|----------|---------------|-------|
| Property exterior | 5 | Front, sides, signage, parking, landscaping |
| Leasing office | 3 | Exterior, interior, setup |
| Common areas | 3 per area | Lobby, hallways, laundry, mailroom |
| Each amenity | 2 per amenity | Current condition |
| Each vacant unit walked | 11+ per unit | One per scoring category + readiness checklist items |
| Each deferred maintenance item | 1 each | With location reference |
| Each capital system inspected | 1 each | Showing condition |
| Maintenance back-of-house | 3 | Shop overview, parts area, chemical storage |
| Comp property exteriors | 2 per comp | Taken during comp mystery tour |

**Required Documents (copies or photos):**

| Document | Source |
|----------|--------|
| Fire/safety inspection certificate | Management |
| Insurance certificate | Management |
| Owner's annual budget | Owner |
| Screening criteria document | Management |
| Sample renewal letter | Management |
| Sample move-in checklist | Management |
| Training program documentation | Management |
| Maintenance SOP documentation | Management |
| Concession policy documentation | Management |
| Brokerage service agreement | Management (if applicable) |

**Required Screenshots (full engagement additions):**

| Screenshot | Source |
|------------|--------|
| Follow-up emails from mystery shop | Mystery shop |
| Mystery shop follow-up texts | Mystery shop |

---

## 13. Audit Execution Timeline

### Door Opener Timeline `[DOOR OPENER]`

Pure desk research — no property contact, no site visits.

| Phase | Timing | Activities |
|-------|--------|------------|
| Subject property — digital audit | Day 1 | Section 2 (reputation, GMB, social, website, listings) |
| Subject property — public profile | Day 1 | Sections 3A–3E from public sources (amenities, market, events, services) |
| Comp research — online | Day 1–2 | Sections 10A–10K (per comp: details, pricing, amenities, reputation, digital, services, events, mobile app) |
| Evidence compilation | Day 2 | Section 12 — Door Opener Evidence (all screenshots) |

**Total estimated time:** 1–2 days desk research.

### Full Engagement Timeline `[FULL ENGAGEMENT]`

Assumes door opener is already complete. Builds on existing door opener data.

| Phase | Timing | Activities |
|-------|--------|------------|
| Mystery shop — phone | 2–3 days before site visit | Section 4B |
| Mystery shop — tour | 1–2 days before site visit | Section 4C |
| Mystery shop — follow-up check | 48 hours after tour | Section 4D |
| Financial benchmark intake | Before or during site visit | Section 9A (owner call) |
| Site visit — verify property profile | Day 1 on-site | Sections 3A–3E (verify and correct door opener data) |
| Site visit — observation | Day 1 on-site | Section 5 (office, model, condition, capital, deferred, unit walks, back-of-house) |
| Site visit — field audit templates | Day 1 on-site | Section 6 (vacancy observations, interviews) |
| Site visit — management interview | Day 1 on-site | Section 7 (all subsections) |
| Site visit — tour observation | Day 1 on-site | Section 8 |
| Site visit — technology assessment | Day 1 on-site | Section 11 |
| Comp tours (mystery shop) | Within 1 week of subject visit | Section 10L |
| Evidence compilation | After all site work | Section 12 — Full Engagement Evidence (photos, documents, certificates) |

**Total estimated field time:** 3–4 days including comp tours.

---

## Authoritative References

- **Scoring structure and weights:** Scoring Model Specification + Scoring Model Workbook
- **Locked-in weight values:** Scoring Weights Final (`Scoring_Weights_Final_Update.json`)
- **Computation rules and data sources:** Computation Rules Workbook
- **Scoring thresholds:** Scoring Thresholds Calibration
- **Complete field inventory (all 1,100+ fields):** Complete Data Inventory
- **Engine architecture:** Analytical Engine Specification
