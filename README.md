# SG Semicon US Expansion

Use this Codex plugin to support Singapore semiconductor and semiconductor-adjacent SMEs preparing for US market expansion.

It includes two skills:

- `singapore-semiconductor-profiler`: research one company website and add a structured profile to:

```text
data/companies.xlsx
```

- `map-sme-capability`: turn an SME website or document into a concise Markdown capability profile with US buyer-intent search queries.

The output is meant for market-entry, customer-matching, and business-development research. It is designed for analysts who need consistent company profiles, evidence links, clear confidence levels, and practical US prospecting angles.

## Quick Start

From a Codex thread opened in your project folder, ask:

```text
Use $singapore-semiconductor-profiler to profile https://example.com.sg into data/companies.xlsx
```

Or ask:

```text
Use $map-sme-capability to map https://example.com.sg for US buyer prospecting.
```

Replace `https://example.com.sg` with the SME website you want to profile or map.

The profiler workflow will:

1. Check that `data/companies.xlsx` can be opened or created.
2. Check whether the company website is already in `data/companies.xlsx`.
3. Skip the company if the existing row is fresh and evidence-complete.
4. Research the company website if the row is missing, old, or missing evidence fields.
5. Create a structured company profile.
6. Check the profile against the workbook field checklist before writing to Excel.
7. Verify the evidence URLs before writing to Excel.
8. Add or update one row in the `companies` sheet.

The capability-mapping workflow will:

1. Read a company website or uploaded company-profile document.
2. Extract the physical technical capabilities and remove marketing language.
3. Generate three US buyer-intent search queries.
4. Save an editable Markdown capability profile in the current project folder.

## Who Should Use This

This plugin is for business analysts at SBF or Singaporean SMEs who are preparing company profiles, prospecting logic, and US market-entry research.

You do not need Python, uv, a virtual environment, or local scripts. The plugin is prompt/skill based and uses Codex plus spreadsheet-capable tooling.

## What The Workbook Contains

The workbook uses one sheet:

```text
companies
```

Each row is one company. The `website` column is the main identifier, so the workbook should not contain duplicate rows for the same company website.

Core columns:

| Column | What it means |
| --- | --- |
| `company_name` | Official or best-supported company name. |
| `website` | Company website used for the profile. |
| `business_summary` | Short description of what the company does. |
| `semicon_role` | The company's role in the semiconductor ecosystem. |
| `products_services` | Main products, services, or capabilities. |
| `target_customer_type` | Types of customers likely to buy from this company. |
| `buyer_need` | Customer problem or procurement need the company serves. |
| `evidence_url` | Strongest source URL used for the profile. |
| `evidence_urls` | All source URLs used for the profile, usually 1 to 5 links. |
| `evidence_summary` | Short explanation of how the evidence supports the row. |
| `confidence` | `high`, `medium`, or `low`. |
| `research_quality` | Whether the evidence was complete, limited, thin, inaccessible, or conflicting. |
| `last_checked` | Date the company was last researched. |
| `notes` | Analyst-facing caveats or useful context. |

## How To Review A Row

After a profile is added, review these fields first:

1. `company_name`: Is this the right company?
2. `website`: Is this the correct website?
3. `semicon_role`: Does the role make sense?
4. `products_services`: Are the offerings specific enough?
5. `target_customer_type` and `buyer_need`: Would these help match the company to US customers?
6. `evidence_urls`: Do the links support the claims?
7. `confidence` and `research_quality`: Is the row ready to use, or does it need human review?

## Confidence Guide

Use this as a practical interpretation guide when reviewing rows:

| Value | Meaning |
| --- | --- |
| `high` | The company website has clear, direct, multi-page evidence. |
| `medium` | The evidence is useful, but some details are limited or the category is imperfect. |
| `low` | The website is thin, inaccessible, unclear, or only weakly connected to semiconductors. |

## Research Quality Guide

| Value | Meaning |
| --- | --- |
| `complete` | At least 3 relevant company-site pages support the main fields. |
| `limited_site` | The site is accessible but has few useful pages. |
| `thin_evidence` | The pages are readable, but semiconductor relevance is weak. |
| `inaccessible_site` | The website could not be accessed or parsed well enough. |
| `conflicting_sources` | Sources disagree in a meaningful way. |

High-confidence rows should normally have `research_quality = complete`.

## Semiconductor Role Guide

Choose the role that best describes the company:

| Role | Plain-English meaning |
| --- | --- |
| `idm` | Designs and manufactures chips. |
| `fabless` | Designs chips but does not run its own fab. |
| `foundry` | Manufactures chips for other companies. |
| `packaging_test` | Provides assembly, packaging, or test services. |
| `equipment` | Sells equipment used in semiconductor manufacturing. |
| `precision_engineering` | Makes precision parts or assemblies for semiconductor customers. |
| `materials` | Supplies materials, chemicals, gases, substrates, or related inputs. |
| `systems_integrator` | Integrates facility, cleanroom, OT, IT, automation, or security systems. |
| `distributor` | Distributes semiconductor products, equipment, or materials. |
| `software` | Provides MES, automation, EDA, analytics, or other relevant software. |
| `unclear` | The semiconductor connection cannot be verified confidently. |

## Good Row Example

A strong row usually looks like this:

```text
confidence: high
research_quality: complete
evidence_urls: 3 or more company website links
evidence_summary: Explains which pages support the role, offerings, and buyer need
notes: Only includes useful caveats
```

Example `buyer_need`:

```text
MES deployment; shop-floor visibility; WIP traceability; quality control for semiconductor manufacturing.
```

Weak rows are still useful when clearly marked. For example, if a company appears semiconductor-adjacent but has only one relevant page, use `confidence = medium` or `low` and explain the limitation in `notes`.

## Installation

In Codex:

1. Open Codex.
2. Go to Plugins.
3. Open the marketplace dropdown and click Add more.
4. Add this repository as a plugin source.
5. Start a new Codex thread after installation.

![Open Plugins](screenshots/plugins.jpg)

![Click Add more](screenshots/addmore.png)

![Add marketplace source](screenshots/addmarketplace.jpg)

The analyst machine only needs Codex and normal access to the project files. No Python, uv, virtual environment, or lockfile is required.

## Local Checks

To verify the plugin source, confirm these files exist:

- `.codex-plugin/plugin.json`
- `skills/singapore-semiconductor-profiler/SKILL.md`
- `skills/map-sme-capability/SKILL.md`

To verify a profiler run, reopen `data/companies.xlsx` and check that the `companies` sheet has exactly one row for the normalized company domain.

## Common Messages

| Message | What it means | What to do |
| --- | --- | --- |
| `already exists` | The website is already present, fresh, and evidence-complete. | No action needed unless you want a manual refresh. |
| `missing evidence fields` | The row exists but does not have the newer evidence fields filled in. | Run the profiler again for that company. |
| `stale row retained until replacement` | The row is more than 90 days old. | Run the profiler again; the old row stays until the new one validates. |
| `high confidence requires at least 3 company-site evidence_urls` | The row claims high confidence without enough company-site evidence. | Add more company-site evidence or lower confidence. |
| Evidence link cannot be opened | One or more evidence links could not be verified. | Check the pages in a browser; remove blocked or invalid links, or lower confidence if the pages cannot be verified. |

## Important Rules

- Profile one company URL at a time.
- Do not manually add duplicate rows for the same website.
- Do not create separate workbooks for different SMEs.
- Use `confidence = low` and a clear `research_quality` value when the evidence is weak.
- Include `domain`, but do not add legacy JSON fields such as `country`, `semicon_category`, or `status`.
- Keep the company workbook inside the project folder, usually as `data/companies.xlsx`.

## Design Principles

- One URL in, one Excel row out.
- One SME source in, one editable capability Markdown file out.
- The analyst reviews business usefulness and evidence quality.
- Codex handles company research, profile drafting, checklist validation, and workbook updates through spreadsheet-capable tooling.
- The workbook and Markdown files stay simple enough for downstream customer matching and prospecting.
