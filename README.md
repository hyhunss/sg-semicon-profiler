# SG Semicon US Expansion

This plugin helps business users research Singapore semiconductor and semiconductor-adjacent SMEs for US market expansion.

It turns an SME website or company profile into:

1. A clear capability profile.
2. A broad list of possible US prospects.
3. A smaller qualified shortlist for deeper analysis or outreach.

You do not need to know Python, Git, spreadsheets, or programming to use the main workflow.

## Main Workflow

Use the three skills in order:

```text
SME website -> capability profile -> possible US prospects -> qualified shortlist
```

### 1. Understand The SME

Skill:

```text
$map-sme-capability
```

Use this when you have an SME website or company profile and want to understand what the company actually does.

Output:

```text
data/<company_name>_capabilities.md
```

This file includes:

- core technical capabilities
- source-backed evidence notes
- confidence labels
- five keyword seeds for US prospecting

Example prompt:

```text
Use $map-sme-capability to map https://www.example.com.sg for US prospecting.
```

### 2. Discover Possible US Prospects

Skill:

```text
$us-prospect-discovery
```

Use this after the capability profile is created. It reads the keyword seeds, runs iterative Google Search, reflects on noisy results, and creates a broad list of plausible US prospects.

Output:

```text
data/<company_name>_prospects.md
```

This file includes:

- search-round notes
- possible prospects ordered by apparent relevance
- evidence links
- buying triggers
- why each prospect showed up
- caveats for the qualification step

Example prompt:

```text
Use $us-prospect-discovery with data/example_capabilities.md.
```

Important: this step is intentionally broad. It finds possible prospects, not final targets. Heavy filtering and buyer-path reasoning happen in the next skill.

### 3. Qualify The Best Prospects

Skill:

```text
$qualify-us-prospects
```

Use this after the broad prospect list is created. It reads both earlier outputs and filters the list down to the most likely prospects for deeper research or outreach.

Inputs:

```text
data/<company_name>_capabilities.md
data/<company_name>_prospects.md
```

Output:

```text
data/<company_name>_qualified_prospects.md
```

This file includes:

- top 5-8 qualified prospects
- buyer-path reasoning
- timing and accessibility assessment
- evidence strength
- what to verify next
- deprioritized or excluded prospects

Example prompt:

```text
Use $qualify-us-prospects with data/example_capabilities.md and data/example_prospects.md.
```

## What The Plugin Is Good At

Use this plugin when you want to answer:

- What does this Singapore SME actually sell?
- Which capability claims are supported by evidence?
- What US companies or projects might need this capability?
- Which of those prospects are most realistic to pursue?
- What buyer path should we investigate next?

The plugin is especially useful for SMEs in areas such as:

- semiconductor MES and factory software
- fab tool moving and cleanroom rigging
- precision machining and tooling
- semiconductor equipment services
- OT/IT and facility systems integration
- advanced packaging, test, and manufacturing support

## What Counts As A Good Prospect

A good prospect is not just a large semiconductor company.

A good prospect should have:

1. A real capability fit.
2. A concrete timing signal, such as a new facility, production ramp, modernization, pilot line, tool install, or supplier-development need.
3. A plausible buyer path, such as an equipment OEM, EPC, cleanroom contractor, factory automation owner, MES owner, approved supplier route, or local partner.
4. Evidence that supports the fit, or at least a strong and clearly labeled inference.

## Recommended Usage Pattern

Run the full workflow like this:

```text
Use $map-sme-capability for https://www.example.com.sg
```

Then:

```text
Use $us-prospect-discovery with data/example_capabilities.md
```

Then:

```text
Use $qualify-us-prospects with data/example_capabilities.md and data/example_prospects.md
```

## Optional Workbook Skill

This plugin also includes:

```text
$singapore-semiconductor-profiler
```

Use it when you want to profile a Singapore semiconductor or semiconductor-adjacent company into a shared workbook:

```text
data/companies.xlsx
```

This is separate from the three-step prospecting workflow.

## Install The Plugin

In Codex:

1. Open **Plugins**.
2. Open the marketplace dropdown.
3. Click **Add more**.
4. Add the plugin link or folder provided by the project lead.
5. Start a new Codex chat after installation.

Screenshots:

![Open Plugins](screenshots/plugins.jpg)

![Click Add more](screenshots/addmore.png)

![Add marketplace source](screenshots/addmarketplace.jpg)

## Output Files

The main workflow creates Markdown files in your current project folder:

```text
data/<company_name>_capabilities.md
data/<company_name>_prospects.md
data/<company_name>_qualified_prospects.md
```

Markdown is plain text. You can open these files like normal documents.

## Review Checklist

After running the workflow, check:

1. Are the SME capabilities specific and evidence-backed?
2. Are unsupported claims marked Medium or Low confidence?
3. Does the prospect list explain why each candidate showed up?
4. Does the qualified shortlist avoid prospects that are only large but not reachable?
5. Are buyer paths and next verification questions concrete enough for follow-up research?

## When Results Need Review

Review more carefully when:

- the SME website is very short
- the SME serves many industries but does not explain semiconductor work clearly
- search results mostly find competitors or supplier directories
- prospects are large fabs with unclear access routes
- evidence shows a facility project but not a direct buying need

In these cases, the qualification skill should lower confidence or move the prospect to watchlist.

## Practical Rule

The plugin should help you move from broad curiosity to focused action:

```text
What does the SME sell?
Who might need it?
Who is most worth investigating next?
```
