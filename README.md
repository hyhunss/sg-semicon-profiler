# SG Semicon US Expansion

This plugin helps business users research Singapore semiconductor and semiconductor-adjacent SMEs for US market expansion.

It has three research skills, each with a different job:

1. A clear capability profile.
2. A broad list of possible US prospects.
3. A smaller qualified shortlist for deeper analysis or outreach.

The skills are designed for a human-in-the-loop workflow. Run one skill, review its output file, then run the next skill in the Codex thread. The next skill automatically looks in `data/` for the right previous output file.

You do not need to know Python, Git, spreadsheets, or programming to use the main workflow.

## Quick Start

1. Start:
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

## Main Workflow

Start with `$map-sme-capability`. It is the front door for the workflow: it explains the three-step process, says what information it needs, then creates the first output.

Use the three research skills separately and in order:

```text
Step 1: $map-sme-capability
Step 2: $us-prospect-discovery
Step 3: $qualify-us-prospects
```

The review gates are part of the workflow:

1. Run `$map-sme-capability`, then review the new `data/*_capabilities.md` file.
2. If the capability profile looks accurate, press `$` in the thread and select `$us-prospect-discovery`, or type `$us-prospect-discovery`, then review the new `data/*_prospects.md` file.
3. If the broad prospect pool looks useful, press `$` in the thread and select `$qualify-us-prospects`, or type `$qualify-us-prospects`, then review the new `data/*_qualified_prospects.md` file.

If an output is weak, incomplete, or based on the wrong interpretation of the SME, revise that stage before moving forward.

Each skill should make the next step obvious in chat. Users should not need to copy file paths, remember filenames, or come back to this README during normal use.

In Codex, press `$` in the thread and select the next skill, or type the skill command directly.

### 1. Understand The SME

Skill:

```text
$map-sme-capability
```

Use this when you have an SME website or company profile and want to understand what the company actually does.

This is also the instructional first step. It should briefly explain that the plugin will proceed in three review-gated stages before it creates the capability profile.

Output:

```text
data/*_capabilities.md
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

Review before continuing:

- Are the capabilities specific to what the SME actually sells?
- Are weak or indirect claims labeled Medium or Low confidence?
- Are the keyword seeds close enough to guide prospect discovery?

When ready, press `$` in the thread and select `$us-prospect-discovery`, or type:

```text
$us-prospect-discovery
```

### 2. Discover Possible US Prospects

Skill:

```text
$us-prospect-discovery
```

Use this after the capability profile is created. It reads the keyword seeds, runs iterative Google Search, reflects on noisy results, and creates a broad list of plausible US prospects.

This skill searches for both end customers and practical route-to-market candidates. For many Singapore SMEs, the realistic path may be through EPC/EPCM firms, cleanroom contractors, facility integrators, construction managers, equipment OEMs, approved supplier routes, public consortia, or regional partner ecosystems.

Output:

```text
data/*_prospects.md
```

This file includes:

- search-round notes
- possible prospects ordered by apparent relevance
- evidence links
- buying triggers
- route type, such as direct owner, channel/EPC, partner ecosystem, or watchlist
- why each prospect showed up
- caveats for the qualification step

Thread command:

```text
$us-prospect-discovery
```

Important: this step is intentionally broad. It finds possible prospects, not final targets. Heavy filtering and buyer-path reasoning happen in the next skill. If you do not provide a file path, the skill automatically uses the most recent `data/*_capabilities.md` file.

Review before continuing:

- Do the prospects have a visible link to the SME's capabilities?
- Are the sources credible enough for a first-pass candidate pool?
- Does the list include plausible route-to-market candidates, not only large fab owners?
- Are the caveats clear, especially where the buyer path is uncertain?

When ready, press `$` in the thread and select `$qualify-us-prospects`, or type:

```text
$qualify-us-prospects
```

### 3. Qualify The Best Prospects

Skill:

```text
$qualify-us-prospects
```

Use this after the broad prospect list is created. It reads both earlier outputs and filters the list down to the most likely prospects for deeper research or outreach.

Inputs are auto-detected from `data/` when you type `$qualify-us-prospects` or select it after pressing `$` in the thread:

```text
data/*_capabilities.md
data/*_prospects.md
```

Output:

```text
data/*_qualified_prospects.md
```

This file includes:

- top 5-8 qualified prospects
- buyer-path reasoning
- timing and accessibility assessment
- evidence strength
- key evidence links for timing signals and new verification facts
- what to verify next
- deprioritized or excluded prospects

Thread command:

```text
$qualify-us-prospects
```

Final review:

- Are the top prospects worth deeper research or outreach?
- Is each buyer path specific enough to investigate?
- Are new verification facts backed by source links?
- Are exclusions and watchlist decisions reasonable?

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

## Recommended Usage Pattern

Start here:

```text
Use $map-sme-capability for https://www.example.com.sg
```

After reviewing the capability profile, press `$` in the thread and select `$us-prospect-discovery`, or type:

```text
$us-prospect-discovery
```

After reviewing the broad prospect pool, press `$` in the thread and select `$qualify-us-prospects`, or type:

```text
$qualify-us-prospects
```

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

## Practical Rule

The plugin should help you move from broad curiosity to focused action:

```text
What does the SME sell?
Who might need it?
Who is most worth investigating next?
```
