# Singapore Semiconductor US Expansion

> **AI-Powered Market-Entry Decision Support for Singapore Semiconductor SMEs & SBF Leaders**

---

## Overview

![Executive Dashboard Preview](assets/dashboard-preview.png)

In the era of the U.S. CHIPS Act, Singapore semiconductor-supply-chain SMEs entering the U.S. market face significant research costs and unfamiliar supply-chain structures.

This Codex plugin provides a structured, 4-step decision-support workflow designed for Singapore Business Federation (SBF) advisors and SME executives. Instead of generic industry overviews, it identifies candidate organizations across target U.S. semiconductor clusters (**Central Texas, Arizona, and New York**), evaluates their fit against a transparent 20-point rubric, and generates print-ready executive brief dashboards.

### Key Value Pillars
* **Pragmatic Channel Targeting**: Bypasses the high entry barriers of Tier-1 megasites by focusing on accessible secondary channels—cleanroom/EPC contractors, equipment OEMs, system integrators, and regional EDOs.
* **Evidence-Backed Qualification**: Every candidate score is tied directly to verifiable source links, access timestamps, and specific supported claims.
* **Zero-Friction Executive Briefing**: Generates single-file offline HTML dashboards that convert instantly into clean, McKinsey-formatted PDF briefs via standard print controls (`Ctrl+P` / `Cmd+P`).

---

## Quick Reference

| Stage | Command / Trigger | Primary Action | Output |
| :--- | :--- | :--- | :--- |
| **Step 1** | `$map-sme-capability <URL / File>` | Map SME core capabilities, evidence & limitations | `output/<sme>/01_capability_profile.md` |
| **Step 2** | `$us-prospect-discovery` | Discover relevant US prospects across target clusters | `output/<sme>/prospects/*.md` |
| **Step 3** | `$qualify-us-prospects` | Score & rank top candidates using 20-pt rubric | `output/<sme>/03_qualified_shortlist.md` |
| **Step 4** | `$export-executive-brief` | Render the canonical shortlist for executive review | `output/<sme>/04_executive_dashboard.html` |

> ⚠️ **Important Note on Data Cascade & Dependencies:**
> Steps 3 and 4 operate on static snapshots created by prior steps:
>
> - **Step 3 (`$qualify-us-prospects`)** scores and qualifies the active candidate pool in `prospects/`.
> - **Step 4 (`$export-executive-brief`)** renders the canonical shortlist from Step 3.
>
> **If you rerun Step 2 (`$us-prospect-discovery`) to add new prospects, you must rerun Step 3** to re-score the expanded library, followed by **Step 4** to refresh your HTML dashboard. Existing reports do not update automatically.

---

## Installation

1. Open **Plugins** in Codex.
2. Select **Add more** from the marketplace dropdown.
3. Add the plugin folder or repository URL.
4. Start a new Codex task after installation.

---

## Deliverables

For each SME, the workflow generates:

- **Capability Profile (`01_capability_profile.md`)**: A structured summary of core technical offerings, website evidence, and operational limits.
- **Prospect Library (`prospects/*.md`)**: A persistent collection of individual Markdown records for screened US prospects, market-entry partners, and ecosystem connectors.
- **Qualified Executive Shortlist (`03_qualified_shortlist.md`)**: A prioritized 5–8 candidate decision report featuring component scores, buyer routes, next verification questions, and recommended SBF actions.
- **Executive Dashboard (`04_executive_dashboard.html`)**: A self-contained, offline dashboard with executive KPIs, action priorities, evidence details, and print-ready styling.

---

## Target Segment & Scope

### Designed For
- **SBF Leaders & Advisors**: Evaluating strategic support initiatives for Singapore SMEs entering the US semiconductor ecosystem.
- **Singapore SME Executives**: Assessing potential US customers, partners, and expansion routes.
- **Industry Partners**: Guiding SMEs through market validation, missions, and establishment.

### Eligible Sector Focus
Target SMEs should be Singapore-owned (≥30% local equity, revenue < SGD 100M, <200 employees). Relevant activities include:

- Semiconductor equipment & precision engineering
- Testing, assembly & advanced packaging
- Cleanroom, facility services & tool relocation
- Factory software, logistics & systems integration

*Note: Direct semiconductor manufacturing (Fab operations) is out of scope.*

---

## Workflow Architecture

```mermaid
flowchart LR
    A[SME Website / Input] -->|Step 1: $map-sme-capability| B[Capability Profile]
    B -->|Review & Approve| C[Step 2: $us-prospect-discovery]
    C -->|Adaptive Discovery| D[Prospect Library]
    D -->|Review & Approve| E[Step 3: $qualify-us-prospects]
    E -->|20-Pt Scoring Rubric| F[Canonical Executive Shortlist]
    F -->|Review & Approve| G[Step 4: $export-executive-brief]
    G --> H[Offline HTML Dashboard]
```

### 1. Capability Mapping (`$map-sme-capability`)
Analyzes the SME’s website or company presentation to identify up to three core capabilities, supporting evidence, and search keywords for US discovery.

### 2. Prospect Discovery (`$us-prospect-discovery`)
Runs adaptive search cycles across priority US clusters using public signals (CHIPS Act awards, state EDO announcements, company career portals, contractor listings). Generates individual prospect records categorized as:
- **Commercial Prospect**: Potential buyers or end-customer projects.
- **Route-to-Market Partner**: OEMs, EPCM contractors, integrators providing buyer access.
- **Ecosystem Connector**: EDOs, industry chambers, research consortia.

### 3. Prospect Qualification (`$qualify-us-prospects`)
Screens the prospect library against a 20-point rubric assessing capability fit, timing signals, buyer accessibility, and evidence strength. Recommends specific SBF engagement stages (**Learn**, **Lead Generation**, **Land**, **Localize**).

### 4. Executive Export (`$export-executive-brief`)
Transforms the reviewed Step 3 JSON into one self-contained, print-to-PDF-ready HTML dashboard. This presentation-only step preserves the canonical shortlist without rescoring candidates or adding claims.

---

## Optional Inputs

Users can supply context in `input/existing_customers.md` to exclude current accounts or guide analogous-buyer searches:

```markdown
# Existing Customers - [SME Name]

- Customer A (US - Texas)
- Customer B (Singapore / SEA Subsidiary)

Exclusions:
- Exclude direct outreach to existing Tier-1 fab accounts in Taiwan.
```

---

## Geographic Focus

Default priority US semiconductor clusters:
1. **Central Texas** (Austin, Taylor, Round Rock)
2. **Arizona** (Phoenix, Chandler)
3. **New York** (Albany, Marcy, Fishkill)

Other US regions are evaluated when capability fit or timing signals are exceptionally strong.

---

## Human Review & Natural Language Feedback

The workflow stops for review after every step. Users can revise assumptions or scope in plain English:

```text
- "Add flip-chip packaging as a user-specified search term."
- "Focus search on Arizona partners rather than fab owners."
- "Move Candidate X to Watchlist due to unclear buyer route."
```

---

## Working Files

All outputs are saved in self-contained folders under `output/<sme_name>/`:

- `01_capability_profile.md`: Step 1 capability summary.
- `02_search_log.md`: Log of discovery queries and reflections.
- `02_prospects_index.tsv`: Lightweight speed index.
- `prospects/*.md`: Detailed records for each discovered prospect.
- `03_qualified_shortlist.md`: Final qualified executive report.
- `03_qualified_shortlist.json`: Structured archive of shortlisted candidates.
- `04_executive_dashboard.html`: Offline executive dashboard and print-to-PDF view.

---

## Limitations & Disclaimers

- **Public Data Dependency**: Prospect discovery is built strictly on open, publicly accessible web signals and public announcements. It does not access private databases or non-public procurement registries.
- **Export Control Disclaimer**: The plugin does not perform compliance reviews under US Export Administration Regulations (EAR) or ITAR. Users must independently verify regulatory compliance before commercial outreach.
