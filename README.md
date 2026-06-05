# Singapore Semiconductor Profiler

Use this Codex plugin to research one Singapore semiconductor or semiconductor-adjacent company website and add a structured profile to:

```text
data/companies.xlsx
```

The output is meant for market-entry, customer-matching, and business-development research. It is designed for analysts who need consistent company profiles, evidence links, and clear confidence levels.

## Quick Start

From a Codex thread opened in your project folder, ask:

```text
Use $singapore-semiconductor-profiler to profile https://example.com.sg into data/companies.xlsx
```

Replace `https://example.com.sg` with the company website you want to profile.

The plugin will:

1. Check whether the company website is already in `data/companies.xlsx`.
2. Skip the company if the existing row is fresh and evidence-complete.
3. Research the company website if the row is missing, old, or missing evidence fields.
4. Create a structured company profile.
5. Validate the profile before writing to Excel.
6. Add or update one row in the `companies` sheet.

## Who Should Use This

This plugin is for business analysts at SBF or Singaporean SMEs who are preparing company profiles for international market-entry work.

You do not need to edit JSON or write Python for normal use. A basic Python background helps only when installing dependencies or running local checks.

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

The analyst machine should have:

- Codex
- Python 3.11+
- uv

Install Python dependencies from the plugin folder:

```bash
uv sync
```

## Local Checks

Run these from the plugin folder when you want to verify the plugin is working:

```bash
export SKILL_DIR="skills/singapore-semiconductor-profiler"
uv run python "$SKILL_DIR/scripts/smoke_test_company_profile.py"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate "$SKILL_DIR/references/sample_company_profile.json"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" audit
```

Useful commands:

```bash
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" check "https://example.com.sg"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" read "https://example.com.sg"
```

## Common Messages

| Message | What it means | What to do |
| --- | --- | --- |
| `already exists` | The website is already present, fresh, and evidence-complete. | No action needed unless you want a manual refresh. |
| `missing evidence fields` | The row exists but does not have the newer evidence fields filled in. | Run the profiler again for that company. |
| `stale row retained until replacement` | The row is more than 90 days old. | Run the profiler again; the old row stays until the new one validates. |
| `high confidence requires at least 3 company-site evidence_urls` | The row claims high confidence without enough company-site evidence. | Add more company-site evidence or lower confidence. |

## Important Rules

- Profile one company URL at a time.
- Do not manually add duplicate rows for the same website.
- Do not create separate workbooks for different SMEs.
- Use `confidence = low` and a clear `research_quality` value when the evidence is weak.
- Do not add legacy JSON fields such as `domain`, `country`, `semicon_category`, or `status`.
- Keep `COMPANIES_XLSX` inside the project folder, usually as `data/companies.xlsx`.

## Design Principles

- One URL in, one Excel row out.
- The analyst reviews business usefulness and evidence quality.
- Python handles validation and Excel writing.
- Codex handles company research and profile drafting.
- The workbook stays simple enough for downstream customer matching.
