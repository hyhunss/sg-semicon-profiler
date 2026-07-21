# SG Semicon US Expansion

This Codex plugin helps the Singapore Business Federation (SBF), its sector partners, and Singapore semiconductor-supply-chain SMEs turn company capabilities into practical US market-entry targets.

It uses a three-step, human-reviewed workflow:

```text
Understand the SME -> discover possible US routes -> qualify the best candidates
```

The client-approved workflow remains intentionally simple. Each skill creates a readable report, stops for review, and lets the user continue, revise, or stop.

## Project Scope

The plugin reflects the UCLA Anderson Management Practicum scope for SBF:

- Target companies are Singapore-owned SMEs: at least 30% Singapore citizen or permanent-resident equity, less than SGD 100 million revenue, and fewer than 200 employees.
- Public evidence of ownership or company size is often unavailable. The plugin marks those items `Unknown` instead of guessing.
- The industry focus is semiconductor supporting activities such as equipment and equipment services, precision engineering, testing, assembly, advanced packaging, factory software, cleanroom and facility services, tool installation and relocation, logistics, materials, and systems integration.
- Default priority US clusters are Central Texas, Arizona, and New York.
- California is deprioritized because of cost, not prohibited. Strong opportunities elsewhere in the US can still appear.
- The plugin searches for commercial buyers and projects as well as practical access routes such as EPC/EPCM firms, equipment OEMs, cleanroom contractors, economic development organizations, chambers, industry associations, universities, and research consortia.

The outputs are company-level decision support for the broader SBF US semiconductor playbook. They are not, by themselves, SBF's complete 3-to-5-year roadmap.

## Quick Start

### Step 1 - Map SME Capability

Start with the SME website or an uploaded company profile:

```text
Use $map-sme-capability for https://www.example.com.sg
```

The skill creates:

```text
data/*_capabilities.json
data/*_capabilities.md
```

Open the Markdown report and review:

1. Are the technical capabilities accurate and evidence-backed?
2. Are unsupported claims marked Medium or Low confidence?
3. Does the SBF scope assessment correctly show known facts and evidence gaps?
4. Is the suggested SBF support stage reasonable?

If accurate, click **Step 2 - Discover US Prospects** or type:

```text
$us-prospect-discovery
```

### Step 2 - Discover US Prospects

The skill automatically continues from the capability record identified by the latest workflow state and runs iterative live searches. It creates a broad pool of up to 20 possible candidates with only lightweight filtering.

Candidates are labeled as:

- `Commercial prospect`: a possible buyer or end-customer project.
- `Route-to-market partner`: an EPC, contractor, OEM, integrator, or other practical access route.
- `Ecosystem connector`: an EDO, chamber, association, university, consortium, or public initiative that may help SBF or the SME enter a cluster.

The skill creates:

```text
data/*_prospects.json
data/*_prospects.md
```

Open the Markdown report and review:

1. Are the candidates visibly related to the SME's capabilities?
2. Are commercial prospects and connectors clearly distinguished?
3. Did the search cover Central Texas, Arizona, and New York unless another scope was requested?
4. Are the evidence links credible enough for first-pass discovery?
5. Did the search avoid becoming concentrated in one narrow candidate type?

If useful, click **Step 3 - Qualify US Prospects** or type:

```text
$qualify-us-prospects
```

### Step 3 - Qualify US Prospects

The skill automatically finds the matching capability and prospect records, performs targeted verification, and heavily filters the broad pool into the strongest 5-8 candidates.

It uses a 20-point rubric:

- capability fit: 0-5
- timing and urgency: 0-4
- buyer-path clarity: 0-4
- accessibility and practical SBF support route: 0-4
- priority-cluster fit: 0-1
- evidence strength: 0-2

For every finalist, it recommends one SBF support stage:

- `Learn`: build market understanding and test fit.
- `Lead Generation`: create introductions and validate demand.
- `Land`: support establishment, incentives, partners, and initial entry.
- `Localize`: deepen local operations, hiring, supplier status, and scale.

The skill creates:

```text
data/*_qualified_prospects.json
data/*_qualified_prospects.md
```

Use the final Markdown report to plan deeper diligence, introductions, mission meetings, or other SBF support. Review whether each finalist has a realistic route, adequate evidence, and a concrete next verification question.

## Human Review Gates

The plugin does not run all three skills automatically. The review gates protect against compounding a weak assumption:

1. Review the SME capability profile.
2. Review the broad discovery pool.
3. Review the qualified shortlist.

At every step, users can continue, revise the current output in plain English, or stop.

Example revision requests:

```text
Revise the capability profile: mark Singapore ownership as Unknown because the website does not provide ownership information.
Revise the prospect discovery: include more Arizona ecosystem connectors and fewer fab owners.
Revise the qualified shortlist: move this company to Watchlist because the procurement route is still unclear.
```

## Automatic File Detection

Users do not need to copy file paths between steps.

- Step 2 first follows `data/_latest_workflow.json`; if that pointer is unavailable or stale, it uses the latest `data/*_capabilities.json` file.
- Step 3 first follows the matching files in `data/_latest_workflow.json`; if those pointers are unavailable or stale, it uses the latest matching capability and prospect pair.
- If more than one company could be intended, Codex asks the user to choose.
- Markdown files are supported as a fallback for older runs.

The JSON files are the structured records used between skills. The Markdown files are the reports intended for business review.

Each skill validates its structured JSON output against the bundled schema before creating the readable report. This catches incomplete fields and invalid values before they reach the next step.

## Install the Plugin

In Codex:

1. Open **Plugins**.
2. Open the marketplace dropdown.
3. Click **Add more**.
4. Add the plugin link or folder provided by the project lead.
5. Start a new Codex task after installation or update so it loads the current skill instructions.
