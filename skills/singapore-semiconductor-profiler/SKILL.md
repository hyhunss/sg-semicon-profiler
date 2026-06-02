---
name: singapore-semiconductor-profiler
description: Use when given a Singapore semiconductor or semiconductor-adjacent company URL and asked to profile the company into data/companies.xlsx for downstream US-customer matching.
---

# Singapore Semiconductor Profiler

## Goal

Given one Singapore semiconductor or semiconductor-adjacent company URL, collect basic company information and save one normalized row into the shared Excel database.

Core rule:

```text
Company URL -> validated JSON -> Python writes one Excel row
```

The AI agent must not edit Excel directly.

Python owns:

- duplicate checking
- validation
- Excel reading and writing

AI owns:

- reading the company website
- understanding the company
- collecting a compact evidence ledger before writing the final profile
- returning one JSON object that matches the schema

## Bundled Files

- `schemas/company_profile.py`: single source of truth for the Pydantic `CompanyProfile` schema and Excel column order.
- `scripts/company_profile_excel.py`: operational layer for domain normalization, duplicate checks, validation calls, Excel reads, and Excel upserts.
- `scripts/smoke_test_company_profile.py`: quick end-to-end check for validation and Excel upsert behavior.
- `references/sample_company_profile.json`: known-good JSON fixture for `validate` and `upsert` checks.

Use the script for workbook operations. Do not manually edit `data/companies.xlsx`.

This plugin's bundled schema is authoritative. If a project-local skill, README,
or older workbook mentions `country`, `semicon_category`, or `status`, treat
those as legacy fields for that project only. Do not include them in AI JSON.

## Workflow

1. Receive one company URL.
2. Run the script's `check` command, or call `check_url(url)`, to normalize the domain and check the workbook.
3. Check `data/companies.xlsx`, sheet `companies`, for the normalized `domain`.
4. If that domain already exists, has all required evidence fields, and `last_checked` is 90 days old or newer, return `already exists` and stop.
5. If that domain exists but lacks `evidence_urls`, `evidence_summary`, or `research_quality`, research it again.
6. If that domain exists but `last_checked` is more than 90 days old, keep the old row in place and research the company again.
7. Otherwise, complete the Evidence-Led Research Protocol below.
8. Return one JSON object using the `CompanyProfile` schema.
9. Validate the JSON with `scripts/company_profile_excel.py`.
10. If valid, upsert the matching Excel row with `scripts/company_profile_excel.py`.
11. If invalid, reject the row and surface the validation error.

Typical commands from the repo root, after resolving `SKILL_DIR` to this skill
folder:

```bash
export SKILL_DIR="/path/to/singapore-semiconductor-profiler/skills/singapore-semiconductor-profiler"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" check "https://example.com.sg"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate profile.json
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" upsert profile.json
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" audit
uv run python "$SKILL_DIR/scripts/smoke_test_company_profile.py"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate "$SKILL_DIR/references/sample_company_profile.json"
```

The script writes to `data/companies.xlsx` under the current project root by default. This is the single workbook database for all Singapore company rows. Workbook saves are written through a temporary file and then replaced after the new workbook is successfully generated.

Never write Excel files outside the project root. For tests, set `SEMICON_PROJECT_ROOT=/path/to/temp-project`. If you set `COMPANIES_XLSX`, keep it relative to the project root, such as `data/companies.xlsx`.

If the workbook already exists and is missing newer columns, the script appends those columns instead of creating a second workbook. Extra legacy columns are tolerated and reported by `audit`, but they are ignored by validation and reads.

## Excel Contract

Workbook:

```text
data/companies.xlsx
```

Sheet:

```text
companies
```

Primary key:

```text
domain
```

Columns:

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

Do not create duplicate rows for the same normalized domain.

Keep the contract small. Do not add `country` because this skill is Singapore-only. Do not add `status`; use `confidence = low` and `research_quality` when a row needs human review.

Do not create one workbook per SME. All companies go into the same workbook: `data/companies.xlsx`.

Rows older than 90 days are stale. When `check_url(url)` finds a stale matching domain, it leaves the row in place and returns `research required: <domain> (stale row retained until replacement)`. After the new JSON validates, `upsert_company(profile)` replaces the stale row.

## CompanyProfile Schema

The schema lives in `schemas/company_profile.py`. Do not maintain a second schema in prose or JSON Schema.

The schema enforces:

- `domain` matches the website domain after normalization.
- `business_summary` has at least 20 characters.
- `target_customer_type` and `buyer_need` are non-empty handoff fields for downstream customer matching.
- `evidence_url` appears inside `evidence_urls`.
- high-confidence profiles have `research_quality = complete` and at least 3 distinct `evidence_urls`.
- high-confidence profiles have at least 3 company-site `evidence_urls` from the same normalized domain as `website`.
- `research_quality = complete` requires at least 3 distinct company-site `evidence_urls`.
- no extra JSON keys. Fields such as `country`, `semicon_category`, and `status` are rejected.

## Required Python Functions

The CRUD/workflow script `scripts/company_profile_excel.py` implements these MVP functions:

```python
normalize_domain(url: str) -> str
company_exists(domain: str) -> bool
read_company(domain: str) -> dict | None
delete_company(domain: str) -> bool
validate_company(data: dict) -> CompanyProfile
upsert_company(profile: CompanyProfile) -> None
check_url(url: str) -> str
process_url(url: str) -> str
workbook_audit() -> dict
```

Because Python cannot perform the AI website-reading step, `check_url(url)` owns the pre-research duplicate and freshness check. It returns `already exists`, `research required: ...`, or `research required: ... (stale row retained until replacement)`. `process_url(url)` is kept as a compatibility alias. After AI returns JSON, use `validate_company(data)` and `upsert_company(profile)`. Use `workbook_audit()` or the `audit` command when checking distribution readiness or legacy workbooks.

## Evidence-Led Research Protocol

Before returning JSON, build a compact internal evidence ledger. Do not include the ledger in the final response, but use it to populate `evidence_urls`, `evidence_summary`, `confidence`, and `research_quality`.

Review the supplied URL first, then inspect relevant navigation links. Check these page types when available:

- homepage or supplied landing page
- about, company, or profile page
- products, services, or solutions page
- industries, applications, or markets page
- semiconductor, electronics, advanced manufacturing, cleanroom, or precision engineering page
- case studies, customers, projects, news, or resources page
- contact or locations page

Use a hard cap of 8 company-site pages unless the user asks for deeper research. Prefer pages that directly support semiconductor relevance, offerings, customers, or Singapore operations.

Minimum evidence standards:

- `confidence = high` requires at least 3 distinct relevant company-site URLs from the same normalized domain as `website` and `research_quality = complete`.
- If fewer than 3 relevant pages are available, use `confidence = medium` or `low` and set `research_quality` to the limitation that best explains the gap.
- If the site is inaccessible, use `confidence = low`, `research_quality = inaccessible_site`, and explain the issue in `notes`.
- If evidence conflicts, use `research_quality = conflicting_sources` and do not use high confidence.

Allowed `research_quality` values:

- `complete`: at least 3 company-site evidence URLs were reviewed and support the main fields.
- `limited_site`: the site was accessible but exposed few relevant pages.
- `thin_evidence`: pages were accessible but semiconductor relevance or offerings were weakly supported.
- `inaccessible_site`: the company website could not be accessed or parsed sufficiently.
- `conflicting_sources`: reviewed sources gave materially conflicting signals.

Populate evidence fields:

- `evidence_url`: the single strongest source-of-truth URL.
- `evidence_urls`: 1-5 URLs reviewed and used for validation. Store the strongest URL first. High-confidence and complete profiles require at least 3 URLs from the same normalized domain as `website`.
- `evidence_summary`: concise explanation of which pages support the role, offerings, target customers, and buyer need.

## Research Rules

Use the company's own website, or the strongest supplied source, as the controlling evidence.

Choose one `semicon_role`:

- `idm`
- `fabless`
- `foundry`
- `packaging_test`
- `equipment`
- `precision_engineering`
- `materials`
- `systems_integrator`
- `distributor`
- `software`
- `unclear`

Use `idm` for integrated device manufacturers that design and manufacture chips, such as Intel-style companies.
Use `systems_integrator` for companies that integrate OT, IT, cleanroom, security, or facility systems for semiconductor plants.
Use `unclear` when the semiconductor link is weak or cannot be verified.

Use `confidence = low` when:

- the website is inaccessible or too thin
- the semiconductor connection is only implied
- the company appears adjacent rather than clearly semiconductor-specific
- the evidence page does not directly support the category
- required fields cannot be filled with confidence

Use `confidence = medium` when the evidence is direct but the allowed category is imperfect.

Use the current date for `last_checked`.

For downstream customer matching:

- `target_customer_type`: who would plausibly buy from this company.
- `buyer_need`: the customer problem or procurement need this company serves.

## AI JSON Output

For the research step, return JSON only. Do not include prose, Markdown, citations outside fields, or extra keys.

The output must conform to the Pydantic `CompanyProfile` model in `schemas/company_profile.py`.

Example:

```json
{
  "company_name": "ABC Precision Pte Ltd",
  "website": "https://www.abc.com.sg",
  "domain": "abc.com.sg",
  "business_summary": "ABC Precision provides precision engineering and machining services for semiconductor equipment customers.",
  "semicon_role": "precision_engineering",
  "products_services": "CNC machining; precision components; assembly",
  "target_customer_type": "Semiconductor equipment OEMs; automation integrators; precision component buyers",
  "buyer_need": "Precision machining; custom metal components; mechanical assemblies",
  "evidence_url": "https://www.abc.com.sg/semiconductor",
  "evidence_urls": [
    "https://www.abc.com.sg/semiconductor",
    "https://www.abc.com.sg/services",
    "https://www.abc.com.sg/about"
  ],
  "evidence_summary": "Semiconductor page supports equipment-customer relevance; services page supports CNC machining and assembly offerings; about page supports company context.",
  "confidence": "medium",
  "research_quality": "complete",
  "last_checked": "2026-05-25",
  "notes": "Semiconductor relevance is implied through equipment customers."
}
```

## Acceptance Criteria

- Same URL does not create duplicate rows.
- Existing domains are skipped before AI research.
- AI output validates against `CompanyProfile`.
- AI output with extra keys is rejected.
- High-confidence output requires complete multi-page evidence.
- Limited or thin websites are explicitly marked with `research_quality`.
- Python writes Excel.
- Excel has one row per domain.
- Legacy workbook columns are tolerated but reported by `audit`.
- Low-confidence cases use `confidence = low`.

## Non-Goals

- No separate database beyond `data/companies.xlsx`.
- No complex crawler.
- No raw JSON archive unless it is trivial and does not complicate the MVP.
- No automated refresh logic.
