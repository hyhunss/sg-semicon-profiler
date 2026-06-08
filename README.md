# SG Semicon US Expansion

This plugin helps business users research Singapore semiconductor and semiconductor-adjacent SMEs for US market expansion.

It has three separate skills:

1. Map the SME's capabilities.
2. Discover a broad pool of possible US prospects.
3. Qualify the strongest prospects for deeper research or outreach.

You do not need to know Python, Git, spreadsheets, or programming. In Codex, press `$` in the thread and select the next skill, or type the skill command directly.

## Quick Start

1. Start with an SME website or company profile:

```text
$map-sme-capability for [SME website or company profile]
```

2. If the capability profile looks right:

```text
$us-prospect-discovery
```

3. If the prospect pool looks right:

```text
$qualify-us-prospects
```

You do not need to copy file paths. Step 2 and Step 3 automatically find the files created by earlier steps.

## First-Time User Example

Suppose you want to research a Singapore SME called ABC Precision.

In Codex, type:

```text
$map-sme-capability for https://www.abcprecision.sg
```

Codex will create a file like:

```text
data/abc_precision_capabilities.md
```

Open that file and check only three things:

1. Does it correctly describe what the company sells?
2. Are uncertain claims marked Medium or Low confidence?
3. Do the keyword seeds look relevant for US prospecting?

If it looks right, type:

```text
$us-prospect-discovery
```

Codex will create a file like:

```text
data/abc_precision_prospects.md
```

Open that file and check only three things:

1. Do the prospects seem related to the SME's capabilities?
2. Are the evidence links credible enough?
3. Are there clear caveats where the buyer path is uncertain?

If it looks right, type:

```text
$qualify-us-prospects
```

Codex will create a file like:

```text
data/abc_precision_qualified_prospects.md
```

This final file is the shortlist for deeper research, validation, or outreach.

## If Something Goes Wrong

If Codex asks for a website or company profile:
- Paste the SME website URL or upload the company profile.

If Step 2 cannot find a capability file:
- Run Step 1 first:

```text
$map-sme-capability for [SME website or company profile]
```

If Step 3 cannot find matching files:

* Run Step 2 first:

```text
$us-prospect-discovery
```

If the output is wrong, do not restart the whole workflow. Ask Codex to revise the current file:

```text
Revise the capability profile: [what to fix]
```

or:

```text
Revise the prospect discovery: [what to fix]
```

or:

```text
Revise the qualified shortlist: [what to fix]
```

If the SME website is vague:

* Expect more Medium or Low confidence labels.
* Do not treat the output as final.
* Add more source material if available.

## What Review Means

Review does not mean you need to rewrite the file.

For Step 1, check whether Codex understood the SME correctly.

For Step 2, check whether the prospects are at least plausibly relevant.

For Step 3, check whether the final shortlist has realistic buyer paths.

If something is wrong, tell Codex what to revise in plain English.

## Main Workflow

Use the three skills separately and in order:

```text
Step 1: $map-sme-capability
Step 2: $us-prospect-discovery
Step 3: $qualify-us-prospects
```

The review gates are part of the workflow:

1. Run `$map-sme-capability`, then review the new `data/*_capabilities.md` file.
2. If the capability profile looks accurate, run `$us-prospect-discovery`, then review the new `data/*_prospects.md` file.
3. If the broad prospect pool looks useful, run `$qualify-us-prospects`, then review the new `data/*_qualified_prospects.md` file.

Each skill prints the exact next command to type. Step 2 and Step 3 automatically look in `data/` for the right previous output file.

## What The Plugin Is Good At

Use this plugin when you want to answer:

- What does this Singapore SME actually sell?
- Which capability claims are supported by evidence?
- What US companies or projects might need this capability?
- Which EPCs, contractors, integrators, or partner routes might help reach those projects?
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

For many SMEs, an EPC, cleanroom contractor, facility integrator, or local partner can be a better first prospect than the fab owner itself.

## Install The Plugin

In Codex:

1. Open **Plugins**.
2. Open the marketplace dropdown.
3. Choose **Add more**.
4. Add the plugin link or folder provided by the project lead.
5. Start a new Codex chat after installation.

Screenshots:

![Open Plugins](screenshots/plugins.jpg)

![Add more](screenshots/addmore.png)

![Add marketplace source](screenshots/addmarketplace.jpg)

## Output Files

The main workflow creates Markdown files in your current project folder:

```text
data/*_capabilities.md
data/*_prospects.md
data/*_qualified_prospects.md
data/_latest_workflow.md
```

Markdown is plain text. You can open these files like normal documents.

`data/_latest_workflow.md` is only a convenience record of the latest run. The workflow does not depend on it; Step 2 and Step 3 still auto-detect the right files from `data/`.

## Review Checklist

After running the workflow, check:

1. Are the SME capabilities specific and evidence-backed?
2. Are unsupported claims marked Medium or Low confidence?
3. Does the prospect list explain why each candidate showed up?
4. Does the prospect list include route types, including channel/EPC or partner routes where relevant?
5. Does the qualified shortlist avoid prospects that are only large but not reachable?
6. Are buyer paths, evidence links, and next verification questions concrete enough for follow-up research?

## When Results Need Review

Review more carefully when:

- the SME website is very short
- the SME serves many industries but does not explain semiconductor work clearly
- search results mostly find competitors or supplier directories
- prospects are large fabs with unclear access routes
- evidence shows a facility project but not a direct buying need

In these cases, the qualification skill should lower confidence or move the prospect to watchlist.
