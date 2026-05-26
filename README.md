# Singapore Semiconductor Profiler

This public git repository contains the Codex plugin for turning one Singapore semiconductor or semiconductor-adjacent company URL into one validated row in a project-local workbook:

```text
data/companies.xlsx
```

The plugin is intentionally small. The AI researches the website and returns one
JSON object. The bundled Python script validates the JSON, prevents duplicate
domains, and writes the Excel row.

## Install

### From Codex using the GitHub repo URL

Use this if Codex asks you to add a plugin or marketplace from a GitHub URL.

1. Copy the GitHub repo URL.
2. Paste it into Codex's plugin or marketplace install box.
3. Install **Singapore Semiconductor Profiler**.
4. Test it by asking Codex:

```text
Use $singapore-semiconductor-profiler to profile this Singapore semiconductor company URL into data/companies.xlsx.

https://www.onesystemstech.com
```

This works because the repo contains:

```text
.agents/plugins/marketplace.json
.codex-plugin/plugin.json
```

If Codex says the marketplace root does not contain a supported manifest, the
GitHub repo is missing `.agents/plugins/marketplace.json` or you are using an
old ZIP/repo version.

### From a GitHub ZIP file

For a non-technical install from a GitHub ZIP file:

1. Download the ZIP file from GitHub.
2. Unzip it.
3. Rename the unzipped folder to exactly:

```text
singapore-semiconductor-profiler
```

4. Move that folder into:

```text
~/plugins/
```

On Mac, the final folder should look like this:

```text
/Users/<your-name>/plugins/singapore-semiconductor-profiler
```

5. Open Codex.
6. If Codex shows a local plugin install option, choose this folder:

```text
/Users/<your-name>/plugins/singapore-semiconductor-profiler
```

7. If Codex does not show a local install option, restart Codex after moving the
   folder.
8. Test the plugin by asking Codex:

```text
Use $singapore-semiconductor-profiler to profile this Singapore semiconductor company URL into data/companies.xlsx.

https://www.onesystemstech.com
```

Important: this file must exist directly inside the plugin folder:

```text
~/plugins/singapore-semiconductor-profiler/.codex-plugin/plugin.json
```

If the ZIP creates a nested folder like this:

```text
~/plugins/singapore-semiconductor-profiler/singapore-semiconductor-profiler/.codex-plugin/plugin.json
```

move the inner files up one level. The `.codex-plugin` folder must be directly
inside `~/plugins/singapore-semiconductor-profiler/`.

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
