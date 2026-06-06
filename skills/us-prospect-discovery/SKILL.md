---
name: us-prospect-discovery
description: Second skill in the SG Semicon US Expansion workflow. Use only after the user has reviewed a map-sme-capability output. Given a capability profile with smart keyword seeds, run iterative Google Search to identify up to 20 possible US semiconductor prospects with only lightweight filtering. Stop after writing the broad prospect file, tell the user what to review, and provide the exact next copy-paste prompt for qualify-us-prospects.
---

# Skill: us-prospect-discovery

## Description
Use one SME capability profile to run iterative live Google Search, refine the search strategy, and create a broad list of possible US prospects for later qualification. This skill discovers candidates; it should not do heavy filtering or deep buyer-path reasoning.

This is step 2 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects
```

Assume the user has already reviewed the capability profile. Do not continue into qualification automatically. The user should check this skill's output before invoking the next skill. Make that easy by ending with the exact next copy-paste prompt.

## Inputs
* `capability_profile`: Path to a Markdown file created by `map-sme-capability`, usually `data/<safe_sme_name>_capabilities.md`.
* Optional `prospect_scope`: Any user-specified filters such as US-only, North America, fabs only, equipment OEMs, startups, CHIPS Act projects, or a target state.

## Output
* `data/<safe_sme_name>_prospects.md`: A concise Markdown list with up to 20 possible prospects, search-round notes, and a plain-language reason each prospect appeared.

## Core Rule
Capability seeds are starting points, not final queries. Keep discovery broad, but remove obvious noise:

```text
Capability profile -> search -> reflect -> revised search -> lightly filtered prospect list
```

## Instructions
1. **Read the capability profile:** Extract the SME name, core capabilities, confidence labels, evidence caveats, and exactly 5 smart keyword seeds.
2. **Define lightweight fit criteria:** Convert the capability profile into 3-5 simple discovery rules. A possible prospect should have at least one visible reason it might need the SME's real capability, such as a relevant facility, expansion, product line, supplier need, or semiconductor workflow.
3. **Run Search Round 1:** Use the smart keyword seeds as the first live Google Search starting points. Search the web; do not rely on memory for current projects, funding, facilities, or hiring signals.
4. **Capture candidates:** For each promising result, save the company/project name, URL, prospect type, matched capability, buying trigger or context, and a short `Why this showed up` explanation. Prefer primary or high-quality sources such as company pages, press releases, CHIPS Act releases, state economic development pages, SEC filings, credible trade press, or job postings.
5. **Apply only lightweight filtering:** Exclude clear noise: competitors, consultants, recruiters, unrelated universities, non-US entities without a clear US project, and results with no connection to the SME capability. Do not deeply rank, qualify, or reject plausible candidates because the buyer path is uncertain; that is the third skill's job.
6. **Reflect before more searching:** After each round, briefly assess what the results are finding:
   * Are results finding buyers, competitors, or generic industry noise?
   * Which exact capability terms are working?
   * Which buyer-pain or timing terms are working?
   * Which prospect types are appearing?
7. **Revise the next searches:** Run 1-3 additional search rounds with improved phrases. Use terms such as `new fab`, `capacity expansion`, `pilot line`, `vendor selection`, `facility systems`, `tool install`, `automation`, `approved supplier`, `CHIPS Act`, `hiring`, target states, or named buyer categories. For equipment logistics SMEs, use specific tool/fab actions. For software SMEs, use workflow terms such as MES, WIP tracking, SPC, recipe management, OEE, or yield monitoring when supported by the first profile.
8. **Stop at a useful pool:** Stop once there are enough plausible candidates or after 4 total search rounds. Do not force 20 prospects; 10-15 decent candidates is better than 20 weak ones.
9. **Order the list simply:** Put the most capability-relevant and timely candidates first, but do not use scoring. Heavy ranking belongs to `qualify-us-prospects`.
10. **Write the file:** Create `data/` if needed. Save as `data/<safe_sme_name>_prospects.md`, using the same safe SME name as the capability profile.
11. **Confirm only:** Output a brief success message with the file path and the number of prospects. Tell the user to review the broad prospect pool before running `qualify-us-prospects`. Include the exact next copy-paste prompt using the real capability-profile path and real prospect-discovery output path. Do not print the full Markdown in chat unless the user asks.

## Confirmation Message Template

```text
Created: data/<safe_sme_name>_prospects.md with <N> possible prospects.

Please review this broad prospect pool before continuing.

Check:
1. Are the prospects visibly related to the SME capability?
2. Are the evidence links credible enough for first-pass discovery?
3. Are caveats clear where the buyer path is uncertain?

When ready, paste this next prompt:

Use $qualify-us-prospects with <capability_profile_path> and data/<safe_sme_name>_prospects.md
```

## Output Markdown Template

```markdown
# US Prospect Discovery: [Insert SME Name Here]

## 1. Search Strategy Summary
* Source capability profile: [path]
* Prospect scope: [scope used]
* Fit rules:
  * [Rule 1]
  * [Rule 2]
  * [Rule 3]

## 2. Search Rounds
### Round 1
* Queries tried: [short list]
* Reflection: [what worked, what was noisy, what changed]

### Round 2
* Queries tried: [short list]
* Reflection: [what worked, what was noisy, what changed]

### Round 3
* Queries tried: [short list or "Not needed"]
* Reflection: [what worked, what was noisy, what changed]

### Round 4
* Queries tried: [short list or "Not needed"]
* Reflection: [what worked, what was noisy, what changed]

## 3. Ranked Prospect Shortlist
| # | Prospect | Prospect Type | Matched Capability | Buying Trigger / Context | Evidence | Why This Showed Up |
|---:|---|---|---|---|---|---|
| 1 | [Company / project] | [Fab / OSAT / equipment OEM / materials / other] | [Capability] | [Trigger or context] | [URL] | [Plain-language reason this might be relevant] |

## 4. Exclusions and Caveats
* [Competitors or noisy result types excluded]
* [Evidence gaps or scope limitations]

## 5. Recommended Next Analysis
* Run `qualify-us-prospects` to filter this broad list into the most likely prospects.
* Pay special attention to candidates where the evidence is recent but the actual buyer path is unclear.
```

## Quality Bar
* Every ranked prospect must have at least one source URL.
* The final list must contain no more than 20 prospects.
* Do not include a prospect only because it is a large semiconductor company; there must be a capability-relevant reason it appeared.
* If fewer than 20 plausible prospects are found, stop at the plausible number and say why in the caveats.
* Prefer concrete buying triggers: new fab, expansion, pilot line, reshoring, funding award, hiring, equipment install, facility commissioning, qualification, cybersecurity program, or supplier selection.
* Do not score, heavily qualify, or over-reason the candidates. Leave deep filtering to `qualify-us-prospects`.
