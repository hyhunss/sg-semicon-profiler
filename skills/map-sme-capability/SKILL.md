---
name: map-sme-capability
description: First skill in the SG Semicon US Expansion workflow. Use when given a Singapore semiconductor-supply-chain SME website or company profile. Read the source, identify up to three core capabilities, and create a lean OKF v0.2 capability bundle for review and US prospect discovery.
---

# Map SME Capability

Read one SME source and write a focused, three-pillar capability profile. Focus strictly on what the company can credibly offer a US semiconductor customer.

Skill 1 initially creates `output/<safe_sme_name>/` as a minimal, conformant OKF v0.2 bundle: `index.md` declares the version and `01_capability_profile.md` is one concept document. Later skills add mixed workflow artifacts in the same directory. Treat the profile and prospect concept documents as the navigable OKF knowledge collection, but do not represent that later mixed workspace as a fully conformant bundle.

## OKF authority

`references/OKF_SPEC_v0.2.md` is the authoritative specification for this skill. Read it when uncertain about OKF fields, bundle boundaries, frontmatter, source attribution, trust, or links. Read `references/skill-1-onn-wah-tech-okf-sample.md` for a compliant output sample. Follow the local specification over remembered conventions, examples, or guesses.

## Input

- An SME website or uploaded company profile.

## Output

- `output/<safe_sme_name>/index.md`
- `output/<safe_sme_name>/01_capability_profile.md`

The capability profile is the only Skill 1 concept record and the direct input to Skills 2 and 3. `index.md` is its initial OKF directory listing; Skill 2 extends that listing when it adds the prospect collection. Do not create capability JSON, workflow-state files, logs, or additional reports.

## Method

1. Read the homepage and relevant Product, Service, Solution, or About pages. If no source is provided, ask for one.
2. Identify two or three revenue-generating core capabilities that matter to semiconductor buyers. Ignore general marketing copy. Use fewer when the evidence supports fewer.
3. Extract verifiable specifications, tolerances, machine models, published service scopes, or case studies as hard evidence. Omit unsupported claims and partner-supplied offerings unless the source clearly establishes the SME's role.
4. Turn each supported capability into a concise targeting vector for Skill 2: capability plus likely buyer or partner route plus US cluster or operating signal.
5. Read the runtime clock immediately before writing. Create `index.md` and the capability profile using the formats below. Every supported factual claim must cite a source from the profile's `sources` frontmatter with a keyed footnote. Then stop for review.

Use these OKF rules:

- Use the plugin's minimal metadata set: `type`, `description`, `resource`, `generated`, and `sources`. Do not add `title`, `tags`, `status`, `stale_after`, or `verified` unless the user explicitly needs that optional metadata.
- Set `generated.by` to the actual Codex agent/model identifier in the actor convention, for example `codex/gpt-5`. Do not use the skill name or invent a version. Set `generated.at` to the exact runtime-derived ISO 8601 timestamp. Never estimate either value.
- Use one `sources` item for every distinct URL cited in the body. Each source needs a stable, lowercase hyphenated `id`, `resource`, and `title`. Add `last_modified` only when the source itself states a reliable date.
- Use the source ID as a complete Markdown footnote: cite it beside the claim, for example `[^services]`, and define it once in the body as `[^services]: [Page title]`. A claim must not cite an unlisted URL.
- Set `description` to one plain-language sentence and `resource` to the SME's main website URL. Use a descriptive, self-explanatory value for `type`.
- Do not turn public silence about ownership, revenue, employee count, US presence, or customers into a negative conclusion. Omit unsupported claims instead of creating a separate limitations section. Do not perform detailed SBF eligibility analysis in this skill.

## Output format

On the initial Skill 1 run, write `output/<safe_sme_name>/index.md` in this shape. It is a reserved OKF directory listing, not a concept, so it must not have `type` frontmatter. Skill 2 will preserve this entry and add a link to its prospect subdirectory.

```markdown
---
okf_version: "0.2"
---

# SME Market-Entry Knowledge Bundle

- [Capability Profile](01_capability_profile.md) - Public-evidence-based map of the SME's core competencies, sourced evidence, and targeting vectors.
```

Write `output/<safe_sme_name>/01_capability_profile.md` in this shape:

```markdown
---
type: SME Capability Profile
description: "Public-evidence-based capability profile for [Company]."
resource: "[SME main website URL]"
generated:
  by: codex/gpt-5
  at: "[runtime-derived ISO 8601 timestamp]"
sources:
  - id: company-homepage
    resource: "[URL]"
    title: "[Page title]"
  - id: services-page
    resource: "[URL]"
    title: "[Page title]"
---

# Capability Profile: [Company]

## Core Competencies

1. **[Capability]**
   [One plain-language sentence describing what the company provides.][^services-page]

2. **[Capability]**
   [Description][^services-page]

3. **[Capability]**
   [Description][^services-page]

## Sourced Evidence

- [Verifiable specification, tolerance, machine model, service scope, or case study].[^company-homepage]
- [Verifiable specification, tolerance, machine model, service scope, or case study].[^services-page]

## Targeting Vectors

- [Capability] + [likely buyer or partner route] + [target US cluster or operating signal]
- [Capability] + [likely buyer or partner route] + [target US cluster or operating signal]
- [Capability] + [likely buyer or partner route] + [target US cluster or operating signal]

[^company-homepage]: [Page title]
[^services-page]: [Page title]
```

Use fewer than three capabilities, evidence items, sources, or targeting vectors when the evidence is limited. Do not pad the report.

Before completion, verify that:

1. `index.md` has only `okf_version: "0.2"` frontmatter and links to the capability profile.
2. The profile has one parseable YAML frontmatter block at its start and a non-empty `type`.
3. Every body footnote reference and definition matches exactly one `sources[].id`, and every cited URL appears only through that source entry.
4. `generated` is present and identifies the actual producer; do not add optional metadata unless the user requested it.
5. The body contains only `Core Competencies`, `Sourced Evidence`, and `Targeting Vectors`, and no claim overstates what the reviewed sources establish.

After writing, report the file path and end with:

- Continue with `$us-prospect-discovery`.
- Revise the capability profile.
- Stop.
