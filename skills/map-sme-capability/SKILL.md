---
name: map-sme-capability
description: First skill in the SG Semicon US Expansion workflow. Use when given a Singapore semiconductor-supply-chain SME website or company profile. Read the source, identify what the company actually provides, separate its own capabilities from partner-supplied products and unsupported claims, and create a minimal OKF v0.2 capability bundle for review and US prospect discovery.
---

# Map SME Capability

Read one SME source and write one clear capability profile. Focus on what the company can credibly offer a US semiconductor customer.

Skill 1 initially creates `output/<safe_sme_name>/` as a minimal, conformant OKF v0.2 bundle: `index.md` declares the version and `01_capability_profile.md` is one concept document. Later skills add mixed workflow artifacts in the same directory. Treat the profile and prospect concept documents as the navigable OKF knowledge collection, but do not represent that later mixed workspace as a fully conformant bundle.

## OKF authority

`references/OKF_SPEC_v0.2.md` is the authoritative specification for this skill. When uncertain about an OKF field, bundle boundary, frontmatter, source attribution, trust, lifecycle, link, index, log, or conformance rule, read the relevant section of that file before writing or revising an output. If the question is how to apply a compliant field or body shape, then also read `references/skill-1-onn-wah-tech-okf-sample.md`. Follow the local specification over remembered conventions, examples, or guesses. Do not invent OKF requirements or fields.

## Input

- An SME website or uploaded company profile.

## Output

- `output/<safe_sme_name>/index.md`
- `output/<safe_sme_name>/01_capability_profile.md`

The capability profile is the only Skill 1 concept record and the direct input to Skills 2 and 3. `index.md` is its initial OKF directory listing; Skill 2 extends that listing when it adds the prospect collection. Do not create capability JSON, workflow-state files, logs, or additional reports.

## Method

1. Read the homepage and relevant Product, Service, Solution, or About pages. If no source is provided, ask for one.
2. Identify no more than three core capabilities that matter to semiconductor buyers. Ignore marketing language.
3. Separate:
   - what the SME itself demonstrably provides;
   - products or technology supplied through partners;
   - facts that cannot be confirmed from the source.
4. Read the runtime clock immediately before writing. Create `index.md` and the capability profile using the formats below. Every supported factual claim must cite a source from the profile's `sources` frontmatter with a keyed footnote. Then stop for review.

Use these OKF rules:

- Use the plugin's minimal metadata set: `type`, `description`, `resource`, `generated`, and `sources`. Do not add `title`, `tags`, `status`, `stale_after`, or `verified` unless the user explicitly needs that optional metadata.
- Set `generated.by` to the actual Codex agent/model identifier in the actor convention, for example `codex/gpt-5`. Do not use the skill name or invent a version. Set `generated.at` to the exact runtime-derived ISO 8601 timestamp. Never estimate either value.
- Use one `sources` item for every distinct URL cited in the body. Each source needs a stable, lowercase hyphenated `id`, `resource`, and `title`. Add `last_modified` only when the source itself states a reliable date.
- Use the source ID as the footnote label, for example `[^services]`. A claim must not cite an unlisted URL.
- Set `description` to one plain-language sentence and `resource` to the SME's main website URL. Use a descriptive, self-explanatory value for `type`.
- A limitation based on missing public evidence must say that the reviewed public sources do not establish the fact; do not state or imply that the fact is false.

Do not turn public silence about ownership, revenue, employee count, US presence, or customers into a negative conclusion. Mention such facts only under `Important limitations` when relevant. Do not perform detailed SBF eligibility analysis in this skill.

## Output format

On the initial Skill 1 run, write `output/<safe_sme_name>/index.md` in this shape. It is a reserved OKF directory listing, not a concept, so it must not have `type` frontmatter. Skill 2 will preserve this entry and add a link to its prospect subdirectory.

```markdown
---
okf_version: "0.2"
---

# SME Market-Entry Knowledge Bundle

- [Capability Profile](01_capability_profile.md) - Public-evidence-based map of the SME's supported capabilities, limitations, and US prospect-discovery directions.
```

Write `output/<safe_sme_name>/01_capability_profile.md` in this shape:

```markdown
---
type: SME Capability Profile
description: "Public-evidence-based map of [Company]'s supported capabilities, limitations, and US prospect-discovery directions."
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

## What the company does

1. **[Capability]**
   [One plain-language sentence describing what the company provides.][^services-page]

2. **[Capability]**
   [Description][^services-page]

3. **[Capability]**
   [Description][^services-page]

## Evidence

- [Supported claim].[^company-homepage]
- [Supported claim].[^services-page]

## Important limitations

- [Partner-supplied product, evidence gap, or claim that must not be assumed]

## Search directions for Skill 2

- [Capability] + [likely buyer, operational problem, or timing signal]
- [Capability] + [likely buyer, operational problem, or timing signal]
- [Capability] + [likely buyer, operational problem, or timing signal]

[^company-homepage]: [Page title]
[^services-page]: [Page title]
```

Use fewer than three capabilities, sources, or search directions when the evidence is limited. Do not pad the report. Preserve the existing capability headings and plain-language body so Skills 2 and 3 remain compatible.

Before completion, verify that:

1. `index.md` has only `okf_version: "0.2"` frontmatter and links to the capability profile.
2. The profile has one parseable YAML frontmatter block at its start and a non-empty `type`.
3. Every body footnote label matches exactly one `sources[].id`, and every cited URL appears only through that source entry.
4. `generated` is present and identifies the actual producer; do not add optional metadata unless the user requested it.
5. No capability or limitation overstates what the reviewed sources establish.

After writing, report the file path and end with:

- Continue with `$us-prospect-discovery`.
- Revise the capability profile.
- Stop.
