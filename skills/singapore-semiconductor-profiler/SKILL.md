---
name: singapore-semiconductor-profiler
description: Use when given a Singapore semiconductor or semiconductor-adjacent company URL and asked to profile the company into data/companies.xlsx for downstream US-customer matching.
---

# Singapore Semiconductor Profiler

## Goal

Given one Singapore semiconductor or semiconductor-adjacent company URL, collect basic company information and save one normalized row into the shared Excel workbook:

```text
data/companies.xlsx
```

Core rule:

```text
Company URL -> evidence-led profile -> one workbook row
```

This skill intentionally has no Python, uv, virtual environment, generated script, or lockfile dependency. Use spreadsheet-capable tools or the host application's spreadsheet support for workbook reads and writes.

## Bundled Files

- `references/sample_company_profile.json`: example profile object showing the expected fields and values.

Do not look for Python scripts, schemas, virtual environments, or uv commands. They are intentionally absent.

## Invocation and Plugin URI Recovery

If the user explicitly references `plugin://sg-semicon-expansion-plugin@personal` but this skill is not listed in the active context, first look for the installed personal plugin on disk before searching installable plugins. Use the newest cached `SKILL.md` matching:

```text
~/.codex/plugins/cache/personal/sg-semicon-expansion-plugin/*/skills/singapore-semiconductor-profiler/SKILL.md
```

If that file exists, load and follow it directly. Treat this as a local plugin resolution path, not as a missing-plugin failure.

## Workbook Contract

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

Columns, in this order:

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

If the workbook or sheet does not exist, create it with these headers. If the workbook exists but is missing any required header, add the missing header. Extra legacy columns such as `country`, `semicon_category`, and `status` may remain in the workbook, but do not populate them for new rows.

Store `evidence_urls` as newline-separated URLs in the workbook cell.

## Workflow

1. Receive one company URL.
2. Normalize the domain by lowercasing the hostname and removing a leading `www.`.
3. Open `data/companies.xlsx`, sheet `companies`, with spreadsheet-capable tooling.
4. If a row already exists for the normalized `domain`, inspect `last_checked`, `evidence_url`, `evidence_urls`, `evidence_summary`, and `research_quality`.
5. If the existing row is 90 days old or newer and evidence-complete, return `already exists` and stop.
6. If the existing row is stale, missing evidence fields, or low quality, research again and update that same row. Do not create a duplicate row.
7. Research the company website using the Evidence-Led Research Protocol.
8. Build one profile object using the required fields.
9. Verify the profile manually against the Validation Checklist.
10. Write the row to the workbook through spreadsheet-capable tooling.
11. Reopen or reread the workbook row and confirm the domain appears exactly once.

When checking repository state after a run, scope status checks to the workbook and generated output files unless broader Git context is necessary.

## Evidence-Led Research Protocol

Before writing the workbook row, build a compact internal evidence ledger. Do not include the ledger in the final response, but use it to populate `evidence_urls`, `evidence_summary`, `confidence`, and `research_quality`.

Review the supplied URL first, then inspect relevant navigation links. Check these page types when available:

- homepage or supplied landing page
- about, company, or profile page
- products, services, or solutions page
- industries, applications, or markets page
- semiconductor, electronics, advanced manufacturing, cleanroom, or precision engineering page
- case studies, customers, projects, news, or resources page
- contact or locations page

Use a hard cap of 8 company-site pages unless the user asks for deeper research. Prefer pages that directly support semiconductor relevance, offerings, customers, or Singapore operations.

Before using a URL in `evidence_urls`, verify that it loads or can be inspected. If a page cannot be verified, remove it from `evidence_urls` or lower confidence.

## Required Fields

- `company_name`: official or best-supported company name.
- `website`: canonical company website URL.
- `domain`: normalized website domain.
- `business_summary`: at least one specific sentence explaining what the company does.
- `semicon_role`: one allowed role from the list below.
- `products_services`: semicolon-separated products, services, or capabilities.
- `target_customer_type`: likely buyer/customer types.
- `buyer_need`: customer problem or procurement need served.
- `evidence_url`: strongest source URL; must also appear in `evidence_urls`.
- `evidence_urls`: 1-5 verified URLs used for the row.
- `evidence_summary`: concise explanation of what the evidence supports.
- `confidence`: `high`, `medium`, or `low`.
- `research_quality`: one allowed value from the list below.
- `last_checked`: current date in ISO format, such as `2026-06-05`.
- `notes`: caveats, limitations, or useful context.

## Validation Checklist

Before writing:

- The `domain` matches the normalized `website` hostname.
- `evidence_url` appears in `evidence_urls`.
- No duplicate `domain` row will be created.
- `business_summary`, `target_customer_type`, `buyer_need`, and `evidence_summary` are non-empty and specific.
- `confidence = high` only when `research_quality = complete` and at least 3 distinct same-domain company-site evidence URLs support the row.
- `research_quality = complete` only when at least 3 distinct same-domain company-site evidence URLs support the row.
- Extra legacy fields such as `country`, `semicon_category`, and `status` are not included in the profile object or populated for the new row.
- URLs in `evidence_urls` were opened or otherwise verified during the run.

## Research Quality

Allowed `research_quality` values:

- `complete`: at least 3 company-site evidence URLs were reviewed and support the main fields.
- `limited_site`: the site is accessible but exposes few useful pages.
- `thin_evidence`: pages are readable, but semiconductor relevance or offerings are weakly supported.
- `inaccessible_site`: the company website could not be accessed or parsed sufficiently.
- `conflicting_sources`: reviewed sources give materially conflicting signals.

Use `confidence = low` when the site is inaccessible or too thin, the semiconductor connection is only implied, the company appears adjacent rather than clearly semiconductor-specific, or required fields cannot be filled confidently.

Use `confidence = medium` when the evidence is direct but limited, or when the allowed category is imperfect.

## Semiconductor Role

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

Use `idm` for integrated device manufacturers that design and manufacture chips. Use `systems_integrator` for companies that integrate OT, IT, cleanroom, security, or facility systems for semiconductor plants. Use `software` for MES, automation, EDA, analytics, and other relevant software. Use `unclear` when the semiconductor link is weak or cannot be verified.

## Profile Object Shape

Use this structure internally before writing the workbook row:

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
  "last_checked": "2026-06-05",
  "notes": "Semiconductor relevance is implied through equipment customers."
}
```

## Acceptance Criteria

- Same URL does not create duplicate rows.
- Existing fresh evidence-complete domains are skipped before research.
- Stale, missing-evidence, or weak rows are updated in place.
- High-confidence output requires complete multi-page company-site evidence.
- Evidence URLs are verified before writing.
- Limited or thin websites are explicitly marked with `research_quality`.
- Excel has one row per domain.
- Legacy workbook columns are tolerated but not populated.
- Low-confidence cases use `confidence = low`.

## Non-Goals

- No Python scripts, schemas, uv commands, virtual environments, or lockfiles.
- No separate database beyond `data/companies.xlsx`.
- No complex crawler.
- No raw JSON archive unless the user explicitly asks for it.
- No automated refresh logic.
