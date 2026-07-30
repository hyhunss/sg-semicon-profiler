---
name: map-sme-capability
description: First skill in the SG Semicon US Expansion workflow. Use when given a Singapore semiconductor-supply-chain SME website or company profile. Read the source, identify what the company actually provides, separate its own capabilities from partner-supplied products and unsupported claims, and write one concise Markdown capability profile for review and US prospect discovery.
---

# Map SME Capability

Read one SME source and write one clear capability profile. Focus on what the company can credibly offer a US semiconductor customer.

## Input

- An SME website or uploaded company profile.

## Output

- `output/<safe_sme_name>/01_capability_profile.md`

This Markdown file is the only Skill 1 record and the direct input to Skills 2 and 3. Do not create capability JSON, workflow-state files, or additional reports.

## Method

1. Read the homepage and relevant Product, Service, Solution, or About pages. If no source is provided, ask for one.
2. Identify no more than three core capabilities that matter to semiconductor buyers. Ignore marketing language.
3. Separate:
   - what the SME itself demonstrably provides;
   - products or technology supplied through partners;
   - facts that cannot be confirmed from the source.
4. Write the Markdown file using the format below. Every capability must have a supporting source URL. Then stop for review.

Do not turn public silence about ownership, revenue, employee count, US presence, or customers into a negative conclusion. Mention such facts only under `Important limitations` when relevant. Do not perform detailed SBF eligibility analysis in this skill.

## Output format

```markdown
# Capability Profile: [Company]

* Website: [URL]

## What the company does

1. **[Capability]**
   [One plain-language sentence describing what the company provides.]

2. **[Capability]**
   [Description]

3. **[Capability]**
   [Description]

## Evidence

- [Supported claim] — [Source](URL)
- [Supported claim] — [Source](URL)

## Important limitations

- [Partner-supplied product, evidence gap, or claim that must not be assumed]

## Search directions for Skill 2

- [Capability] + [likely buyer, operational problem, or timing signal]
- [Capability] + [likely buyer, operational problem, or timing signal]
- [Capability] + [likely buyer, operational problem, or timing signal]
```

Use fewer than three capabilities or search directions when the evidence is limited. Do not pad the report.

After writing, report the file path and end with:

- Continue with `$us-prospect-discovery`.
- Revise the capability profile.
- Stop.
