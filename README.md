# SG Semicon US Expansion

This Codex plugin helps Singapore Business Federation (SBF) leaders and Singapore semiconductor-supply-chain SMEs answer three practical questions:

1. What can this SME credibly offer the US semiconductor market?
2. Which US companies, projects, and market-entry routes may be relevant?
3. Which opportunities deserve priority, and how can SBF help?

The plugin produces evidence-backed decision support. It does not replace commercial due diligence or guarantee that a company will become a customer.

## What You Receive

For each SME, the plugin produces:

- A concise capability profile showing what the company can credibly offer, supporting evidence, confidence levels, and important information gaps.
- A persistent prospect library that grows across repeated search cycles, with one readable Markdown record per possible US commercial prospect, market-entry partner, or ecosystem connector.
- A focused shortlist, normally 5-8 candidates, showing capability fit, timing, buyer route, accessibility, evidence strength, the next question to verify, and a recommended SBF action.

If the evidence supports fewer strong candidates, the plugin returns a shorter list instead of padding the results.

## Who It Is For

The workflow is designed for:

- SBF leaders assessing how to support Singapore SMEs entering the US semiconductor ecosystem.
- Singapore SME executives evaluating potential US customers, partners, projects, and entry routes.
- Sector partners helping SMEs prepare for introductions, missions, market validation, establishment, or localization.

The project focuses on Singapore-owned SMEs with at least 30% Singapore citizen or permanent-resident equity, less than SGD 100 million in revenue, and fewer than 200 employees. When public information does not establish ownership or size, the plugin marks it as `Unknown` instead of guessing.

Relevant supporting activities include semiconductor equipment and services, precision engineering, testing, assembly, advanced packaging, factory software, cleanroom and facility services, tool installation and relocation, logistics, materials, and systems integration. Direct semiconductor manufacturing is not the target SME segment.

## No Technical Setup Required

This plugin is designed for business users:

- You do not need Python.
- You do not need Terminal or command-line access.
- You do not need a database or spreadsheet system.
- Put optional user-provided information in the `input/` folder.
- Find every generated report and working record in the `output/` folder.
- Open and review the Markdown (`.md`) files like ordinary documents.

The workflow uses simple folders and readable Markdown files so users can understand what was provided, what the plugin found, and what to review next.

## Before You Start

Prepare:

- The SME's website or an uploaded company profile.
- Optional customer information in `input/existing_customers.md` when the website does not adequately describe the company's customer base.
- Time to review the result at the end of each step and correct missing or inaccurate assumptions.

Do not enter company-confidential information.

The workflow runs entirely inside Codex. SME users do not install or run Python, use Terminal, or manage technical dependencies.

## The Three-Step Workflow

```text
Understand the SME -> discover possible US routes -> qualify the best candidates
```

The workflow deliberately stops for review after every step. Users can continue, revise the current result in plain English, or stop.

### Step 1 - Map SME Capability

Click **Step 1 - Map SME Capability** and provide the SME website or company profile. Users can also type:

```text
Use $map-sme-capability for https://www.example.com.sg
```

The plugin reviews the source material and identifies:

- Up to three core technical capabilities.
- Evidence and confidence for each capability.
- Important claims that should not be overstated.
- Fit with the SBF project scope.
- The most appropriate initial SBF support stage.
- Search terms that could reveal relevant US demand.

If the website does not provide useful customer information, Step 1 asks whether the user wants to update `input/existing_customers.md` or continue without it.

Review the capability report before proceeding. Correcting weak assumptions here prevents them from affecting the later prospect search.

### Step 2 - Discover US Prospects

After approving Step 1, click **Step 2 - Discover US Prospects** or type `$us-prospect-discovery`.

Before searching, the plugin displays the exact technical and buyer-signal terms it plans to use. The user can:

- Continue with the proposed terms.
- Add missing technical terms such as a specific process, packaging method, system, or service.
- Remove irrelevant terms.
- Replace inaccurate terminology.

The plugin then runs a short adaptive search cycle of up to five searches. It saves one Markdown record per possible prospect and keeps a search log showing the exact queries, results, reflections, and next direction. Running Step 2 again resumes from the accumulated library instead of overwriting the previous search.

When a known company appears again, the plugin updates its existing record with new evidence. It creates a new file only for a genuinely new buying organization. The cycle stops early after three searches produce no new prospects, but there is no fixed 20-company limit across repeated runs.

Every candidate is clearly labeled as one of:

- `Commercial prospect`: a possible buyer or end-customer project.
- `Route-to-market partner`: an equipment OEM, EPC/EPCM firm, contractor, integrator, or other organization that may provide access to a project or buyer.
- `Ecosystem connector`: an economic development organization, chamber, association, university, consortium, or public initiative that may help the SME or SBF enter a US cluster.

Review the newly created or updated records after each cycle. Users can continue discovery with another cycle, revise the search scope, or move to qualification when the accumulated library is useful.

### Step 3 - Qualify US Prospects

After approving Step 2, click **Step 3 - Qualify US Prospects** or type `$qualify-us-prospects`.

The plugin first scans the structured headers of every accumulated prospect record. It then opens the full content only for the strongest 10-20 candidates, performs targeted verification, and filters them into the final shortlist. It considers:

- Capability fit.
- Timing and urgency.
- Clarity of the likely buyer route.
- Accessibility for a Singapore SME.
- Relevance to priority US clusters.
- Strength of available evidence.

Each finalist receives a classification, a practical route to investigate, a next verification question, and a recommended SBF support action.

The recommended SBF stages are:

- `Learn`: improve market understanding and test the SME's fit.
- `Lead Generation`: create introductions and validate demand.
- `Land`: support initial US establishment, incentives, and partner selection.
- `Localize`: deepen local operations, hiring, supplier status, and scale.

Use the final shortlist to guide deeper diligence, introductions, mission meetings, partner discussions, and market-entry planning.

## Existing Customers

The optional `input/existing_customers.md` file helps the plugin understand customer patterns that may be missing from the company website.

Users can add:

- Existing customer names.
- Customer types, countries, or regions.
- Patterns such as Japanese OSAT companies with Southeast Asian operations.
- Relevant relationship or route-to-market notes.

Steps 2 and 3 exclude named existing customers and obvious corporate-group aliases from new-prospect recommendations. Existing customers are considered only when the user explicitly requests account-expansion analysis.

The SME name in the file prevents customer information from being applied to the wrong company. The file is optional; leaving it empty does not block the workflow.

## US Market Scope

The default priority clusters are:

- Central Texas.
- Arizona.
- New York.

California is deprioritized because of cost, but it is not prohibited. Candidates elsewhere in the US can appear when capability fit, timing, or market access is materially stronger.

The plugin searches beyond fab owners. Depending on the SME, practical routes may include equipment OEMs, EPC/EPCM firms, cleanroom contractors, systems integrators, approved-supplier programs, economic development organizations, chambers, industry associations, universities, and research consortia.

## Human Review

At every stage, users can revise the result in normal language. Examples:

```text
Revise the capability profile: add flip chip as a user-provided search term.
Revise the discovery scope: include more Arizona partners and fewer fab owners.
Revise the qualified shortlist: move this company to Watchlist because the buyer route is unclear.
```

The reports should be treated as structured research and decision support. Users should verify important commercial facts before outreach, investment, or market-entry decisions.

The company-level outputs support the broader SBF US semiconductor playbook. They are not, by themselves, SBF's complete 3-to-5-year strategy.

## Working Files

Users do not need to copy file paths between steps. The plugin automatically continues from the latest reviewed company record.

- `input/existing_customers.md` is optional user input.
- `output/*_capabilities.md` is the Step 1 review report.
- `output/<safe_sme_name>/search_log.md` records Step 2 searches and reflections.
- `output/<safe_sme_name>/prospects/*.md` contains one canonical Step 2 record per possible prospect.
- `output/*_qualified_prospects.md` is the Step 3 decision-support shortlist.
- Step 1 and Step 3 JSON files support reliable handoff and consistency checks. Step 2 uses structured JSON frontmatter inside each readable Markdown prospect record.

## Install the Plugin

In Codex:

1. Open **Plugins**.
2. Open the marketplace dropdown.
3. Click **Add more**.
4. Add the plugin link or folder provided by the project lead.
5. Start a new Codex task after installation or update.
