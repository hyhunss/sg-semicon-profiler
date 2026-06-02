# Singapore Semiconductor Profiler

Codex plugin for profiling Singapore semiconductor and semiconductor-adjacent companies into one shared Excel workbook.

```text
Company URL -> researched profile -> validated Excel row
```

The workbook is written to:

```text
data/companies.xlsx
```

## Who this is for

This repository is intended for business analysts at SBF or Singaporean SMEs who are preparing structured company profiles for market-entry and customer-matching work.

The usual workflow is analyst-run and stakeholder-reviewed:

1. An analyst runs the plugin in Codex on a prepared project machine.
2. The plugin updates `data/companies.xlsx`.
3. Stakeholders review the workbook or a summarized report.
4. Reviewers assess profile quality, evidence quality, confidence, and usefulness for customer matching.

## What it does

- Profiles one company URL at a time.
- Writes one normalized row per company domain.
- Prevents duplicate domain rows.
- Keeps stale rows until a validated replacement is ready.
- Requires multi-page company-site evidence for high-confidence rows.
- Records evidence URLs, evidence summary, confidence, and research quality.
- Validates output before writing Excel.

## Requirements

The analyst machine needs:

- Codex
- Python 3.11+
- uv

Install Python dependencies:

```bash
uv sync
```

Runtime dependencies are declared in `pyproject.toml`.

## Install in Codex

1. Open Codex.
2. Go to Plugins.
3. Click Add more.
4. Add this repository as a plugin source.
5. Start a new Codex thread after installation.

## Usage

From a Codex thread in the project root:

```text
Use $singapore-semiconductor-profiler to profile https://example.com.sg into data/companies.xlsx
```

The plugin will:

1. Normalize the company domain.
2. Check whether the domain already exists in `data/companies.xlsx`.
3. Skip fresh complete rows.
4. Refresh stale or evidence-incomplete rows.
5. Research relevant company-site pages.
6. Validate the final JSON profile.
7. Upsert the row into Excel.

## Output columns

The workbook uses the `companies` sheet with these core columns:

```text
company_name
website
domain
business_summary
semicon_role
products_services
target_customer_type
buyer_need
evidence_url
evidence_urls
evidence_summary
confidence
research_quality
last_checked
notes
```

## Evidence standard

High-confidence rows require:

- `confidence = high`
- `research_quality = complete`
- at least 3 distinct evidence URLs from the company website
- `evidence_url` included in `evidence_urls`

If the website is thin, inaccessible, or contradictory, use medium or low confidence and mark the limitation with `research_quality`.

Allowed `research_quality` values:

```text
complete
limited_site
thin_evidence
inaccessible_site
conflicting_sources
```

## Local checks

Run these from the repository root:

```bash
export SKILL_DIR="skills/singapore-semiconductor-profiler"
uv run python "$SKILL_DIR/scripts/smoke_test_company_profile.py"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate "$SKILL_DIR/references/sample_company_profile.json"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" audit
```

## Troubleshooting

- `already exists`: the domain is present, fresh, and evidence-complete.
- `missing evidence fields`: the row predates the evidence-led schema and should be refreshed.
- `stale row retained until replacement`: the row is old, but kept until the new profile validates.
- `high confidence requires at least 3 company-site evidence_urls`: add more company-site evidence or lower confidence.
- Validation rejects legacy JSON fields such as `country`, `semicon_category`, and `status`.
- `COMPANIES_XLSX` must stay inside the project root, such as `data/companies.xlsx`.

## Design principles

- Keep it simple.
- One URL in, one Excel row out.
- No crawler.
- No separate database.
- Python handles validation and Excel writes.
- Codex handles company research and profile drafting.
