# Singapore Semiconductor Profiler

Codex plugin for turning one Singapore semiconductor or semiconductor-adjacent
company URL into one validated row in a project-local workbook:

```text
data/companies.xlsx
```

The plugin is intentionally small. The AI researches the website and returns one
JSON object. The bundled Python script validates the JSON, prevents duplicate
domains, and writes the Excel row.

## Contract

The authoritative schema is:

```text
skills/singapore-semiconductor-profiler/schemas/company_profile.py
```

Required workbook columns:

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
confidence
last_checked
notes
```

Do not include `country`, `semicon_category`, or `status` in the JSON payload.
Those are legacy fields from older project-local experiments. The plugin now
rejects extra JSON keys.

## Use

From the project root that contains or should contain `data/companies.xlsx`:

```bash
export SKILL_DIR="/path/to/singapore-semiconductor-profiler/skills/singapore-semiconductor-profiler"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" check "https://www.example.com"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate profile.json
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" upsert profile.json
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" audit
```

The `check` command returns one of:

```text
already exists
research required: <domain>
research required: <domain> (stale row deleted)
```

Rows are considered stale after 90 days.

## Test

```bash
export SKILL_DIR="/path/to/singapore-semiconductor-profiler/skills/singapore-semiconductor-profiler"
uv run python "$SKILL_DIR/scripts/smoke_test_company_profile.py"
uv run python "$SKILL_DIR/scripts/company_profile_excel.py" validate "$SKILL_DIR/references/sample_company_profile.json"
```

The smoke test covers validation, duplicate checks, stale-row deletion, workbook
path containment, extra-key rejection, and legacy workbook columns.
