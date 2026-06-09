---
name: us-prospect-discovery
description: Second skill in the SG Semicon US Expansion workflow. Use only after the user has reviewed a map-sme-capability output. Given a capability profile with smart keyword seeds, or invoked with no path after a capability file exists in data/, run iterative Google Search to identify up to 20 possible US semiconductor prospects with only lightweight filtering. Stop after writing the broad prospect file and tell the user what to review before using qualify-us-prospects.
---

# Skill: us-prospect-discovery

## Description
Use one SME capability profile to run iterative live Google Search, refine the search strategy, and create a broad list of possible US prospects for later qualification. This skill discovers candidates; it should not do heavy filtering or deep buyer-path reasoning.

This is step 2 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects
```

Assume the user has already reviewed the capability profile. Do not continue into qualification automatically. The user should check this skill's output before invoking the next skill. Make that easy by ending with explicit Continue, Revise, or Stop choices.

## Inputs
* `capability_profile`: Path to the canonical JSON file created by `map-sme-capability`, usually `data/<safe_sme_name>_capabilities.json`. Markdown capability files from older runs may be used only as fallback input.
* Optional `prospect_scope`: Any user-specified filters such as US-only, North America, fabs only, equipment OEMs, startups, CHIPS Act projects, or a target state.

## Output
* `data/<safe_sme_name>_prospects.json`: The canonical structured prospect-discovery file. It must conform to `schema/prospect-discovery.schema.json`.
* `data/<safe_sme_name>_prospects.md`: A concise human-readable Markdown list rendered from the validated JSON.
* `data/_latest_workflow.json`: Optional convenience state file for the latest workflow.
* `data/_latest_workflow.md`: Optional human-readable convenience state file rendered from the workflow JSON.

## Data Contract
The prospect JSON file is the source of truth for `qualify-us-prospects`. Markdown is only for human review.

Use `schema_version: "1.0.0"` and `schema_name: "prospect_discovery"` in the prospect JSON. Before confirming completion:

1. Read the previous step's capability JSON and treat it as authoritative.
2. Write the prospect discovery JSON.
3. Validate or carefully self-check it against `schema/prospect-discovery.schema.json`.
4. Fix any schema mismatch before continuing.
5. Render the Markdown review file from the validated JSON.
6. Update `data/_latest_workflow.json`, self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`.

## Core Rule
Capability seeds are starting points, not final queries. Keep discovery broad, but remove obvious noise:

```text
Capability profile -> search -> reflect -> revised search -> lightly filtered prospect list
```

## Instructions
1. **Accept selected-prompt invocations:** If the user's message body is blank but selected text contains a prompt for this skill, treat the selected text as the user's instruction and proceed from it. Do not ask the user to paste it again.
2. **Auto-detect input file:** If the user invokes this skill without specifying a file path, use Read access to scan the current workspace's `data/` directory. Find the most recently modified JSON file ending with `_capabilities.json` and use it as the `capability_profile` input. If no JSON exists, fall back to the most recently modified Markdown file ending with `_capabilities.md` and rebuild the required fields into the prospect JSON. If there is no matching file, ask the user to run `map-sme-capability` first or provide the capability profile path. If multiple candidates have the same modified time or the intended company is unclear from the user's message, list the likely files and ask the user to choose.
3. **Handle revision requests:** If the user asks to revise this step's output, read the current prospect discovery JSON first. If only Markdown exists from an older run, read the Markdown as fallback and rebuild the JSON. Apply the requested edits, then reconstruct the entire JSON object perfectly according to `schema/prospect-discovery.schema.json` before touching Markdown. Never truncate the JSON output. Rewrite the Markdown only by mirroring the validated JSON changes. Rewrite the same JSON and Markdown files unless the user asks for a new file, update both workflow state files, and confirm briefly. Do not rerun the whole workflow unless the user explicitly asks.
4. **Read the capability profile:** Extract the SME name, safe SME name, core capabilities, confidence labels, evidence caveats, and exactly 5 smart keyword seeds from the JSON. If using Markdown fallback, convert the extracted fields into the same internal structure before searching.
5. **Define lightweight fit criteria:** Convert the capability profile into 3-5 simple discovery rules. A possible prospect should have at least one visible reason it might need the SME's real capability, such as a relevant facility, expansion, product line, supplier need, semiconductor workflow, or channel route into a facility project.
6. **Define likely go-to-market routes:** Before searching, identify 2-4 practical buyer/channel paths implied by the SME capability. For many Singapore SMEs, include both end customers and intermediaries such as EPC/EPCM firms, cleanroom contractors, facility integrators, local construction managers, equipment OEMs, approved supplier programs, public consortia, or regional economic-development ecosystems.
7. **Run Search Round 1:** Use the smart keyword seeds as the first live Google Search starting points. Search the web; do not rely on memory for current projects, funding, facilities, or hiring signals.
8. **Run channel-route searches early:** In the first two rounds, search for both end-customer projects and realistic access routes. Combine capability terms with `EPC`, `EPCM`, `cleanroom contractor`, `facility contractor`, `systems integrator`, `construction manager`, `approved supplier`, `owner's representative`, `project partner`, or named US regions. Do not wait until qualification to discover channel/EPC routes.
9. **Capture candidates:** For each promising result, save the company/project name, URL, prospect type, matched capability, buying trigger or context, likely route type (`Direct owner`, `Channel/EPC`, `Partner ecosystem`, or `Watchlist`), and a short `Why this showed up` explanation. Prefer primary or high-quality sources such as company pages, press releases, CHIPS Act releases, state economic development pages, SEC filings, credible trade press, job postings, EPC/project pages, procurement pages, or contractor announcements.
10. **Apply only lightweight filtering:** Exclude clear noise: competitors, consultants without project access, recruiters, unrelated universities, non-US entities without a clear US project, and results with no connection to the SME capability. Do not deeply rank, qualify, or reject plausible candidates because the buyer path is uncertain; that is the third skill's job.
11. **Reflect before more searching:** After each round, briefly assess what the results are finding:
   * Are results finding buyers, competitors, or generic industry noise?
   * Which exact capability terms are working?
   * Which buyer-pain or timing terms are working?
   * Which prospect types are appearing?
   * Which route types are appearing: direct owner, channel/EPC, partner ecosystem, or watchlist?
12. **Protect search diversity:** If the first two rounds mostly find one narrow type of result, force the next round to search a different plausible prospect type or route. Examples:
   * If results are mostly software vendors, search hardware, equipment OEM, facility system, EPC, or systems-integrator terms.
   * If results are mostly fab owners, search EPC/EPCM, cleanroom contractor, tool-install, equipment OEM, or approved-supplier terms.
   * If results are mostly contractors or partners, search end-customer projects, OSATs, pilot lines, or funded facilities.
   * If results are mostly giant incumbents, search smaller OSATs, compound-semiconductor firms, pilot lines, startups, or regional facility projects.
   This is a discovery diversity check only. Do not qualify the prospects deeply here.
13. **Revise the next searches:** Run 1-3 additional search rounds with improved phrases. Use terms such as `new fab`, `capacity expansion`, `pilot line`, `vendor selection`, `facility systems`, `tool install`, `automation`, `approved supplier`, `CHIPS Act`, `hiring`, target states, named buyer categories, and named route types. For equipment logistics SMEs, use specific tool/fab actions. For software SMEs, use workflow terms such as MES, WIP tracking, SPC, recipe management, OEE, or yield monitoring when supported by the first profile.
14. **Keep the pool balanced:** Include a useful mix of end customers and route-to-market candidates when evidence supports both. A final pool of 10-15 decent candidates should usually include at least 2-4 channel/EPC/partner-route candidates for SMEs whose direct access to fabs is likely difficult.
15. **Stop at a useful pool:** Stop once there are enough plausible candidates or after 4 total search rounds. Do not force 20 prospects; 10-15 decent candidates is better than 20 weak ones.
16. **Order the list simply:** Put the most capability-relevant and timely candidates first, but do not use scoring. Heavy ranking belongs to `qualify-us-prospects`.
17. **Write the canonical JSON file:** Create `data/` if needed. Save as `data/<safe_sme_name>_prospects.json`, using the same safe SME name as the capability profile.
18. **Validate the prospect JSON:** Validate or carefully self-check against `schema/prospect-discovery.schema.json`. The JSON must have 1-4 search rounds, 1-20 prospects, source URL arrays for every prospect, valid route type and prospect type enum values, and no extra top-level fields. The order of the `prospects` array is the ranking; do not add a separate rank field.
19. **Render the Markdown review file:** Save `data/<safe_sme_name>_prospects.md` from the validated JSON. Do not add prospects, evidence, caveats, or recommendations in Markdown that are absent from the JSON.
20. **Write convenience workflow state:** Also write or update `data/_latest_workflow.json` with SME name, current step completed, capability JSON path, prospects JSON path, blank qualified JSON field, and next recommended command `$qualify-us-prospects`. Self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`. These files are only a convenience; do not require them for later steps.
21. **Confirm only:** Output a business-friendly success message with the readable review report path, the AI background record path, the number of possible prospects, what to review, the exact next command, how to revise, and how to stop. Do not print the full file contents in chat unless the user asks. The confirmation message must end with the three explicit choices in the template below.

## Confirmation Message Template

```text
Created successfully:
- Broad Prospect Pool (AI Record): data/<safe_sme_name>_prospects.json
- Human-Readable Review Report: data/<safe_sme_name>_prospects.md

Found <N> potential targets and route-to-market paths. Please double-click to open 'data/<safe_sme_name>_prospects.md' to review the candidates.

Next Steps:
A. To filter and rank into a 20-point scored shortlist, type:
   $qualify-us-prospects

B. To revise, type:
   Revise the prospect discovery: [describe your changes]

C. Stop here.
```

## Workflow State Template

Use this structure for `data/_latest_workflow.json`:

```json
{
  "schema_version": "1.0.0",
  "schema_name": "workflow_state",
  "sme_name": "[SME Name]",
  "safe_sme_name": "<safe_sme_name>",
  "current_step_completed": "Step 2 - Discover US Prospects",
  "capability_json": "data/<safe_sme_name>_capabilities.json",
  "prospects_json": "data/<safe_sme_name>_prospects.json",
  "qualified_json": null,
  "next_recommended_command": "$qualify-us-prospects"
}
```

Render this human-readable companion as `data/_latest_workflow.md`:

```markdown
# Latest SG Semicon Expansion Workflow

* SME name: [SME Name]
* Current step completed: Step 2 - Discover US Prospects
* Capability JSON: data/<safe_sme_name>_capabilities.json
* Prospects JSON: data/<safe_sme_name>_prospects.json
* Prospects Markdown: data/<safe_sme_name>_prospects.md
* Qualified JSON:
* Next recommended command: $qualify-us-prospects
```

## Output JSON Template

Write this canonical file first as `data/<safe_sme_name>_prospects.json`:

```json
{
  "schema_version": "1.0.0",
  "schema_name": "prospect_discovery",
  "sme_name": "[Insert SME Name Here]",
  "safe_sme_name": "<safe_sme_name>",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "data/<safe_sme_name>_capabilities.json",
  "prospect_scope": "[scope used]",
  "fit_rules": [
    "[Rule 1]",
    "[Rule 2]",
    "[Rule 3]"
  ],
  "search_rounds": [
    {
      "round_number": 1,
      "queries_tried": ["[query]"],
      "reflection": "[what worked, what was noisy, what changed]"
    }
  ],
  "prospects": [
    {
      "prospect": "[Company / project]",
      "prospect_type": "Fab",
      "route_type": "Direct owner",
      "matched_capability": "[Capability]",
      "buying_trigger_or_context": "[Trigger or context]",
      "evidence_urls": ["[URL]"],
      "why_this_showed_up": "[Plain-language reason this might be relevant]",
      "caveats": ["[Optional caveat]"]
    }
  ],
  "exclusions_and_caveats": [
    "[Competitors or noisy result types excluded]"
  ],
  "recommended_next_analysis": [
    "Run qualify-us-prospects to filter this broad list into the most likely prospects."
  ]
}
```

## Output Markdown Template

Render this human-readable file from the validated JSON as `data/<safe_sme_name>_prospects.md`:

```markdown
# US Prospect Discovery: [Insert SME Name Here]

## 1. Search Strategy Summary
* Source capability profile path: [path]
* Prospect scope: [scope used]
* Likely route types searched: [Direct owner / Channel-EPC / Partner ecosystem / Watchlist]
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
* Diversity check: [whether earlier rounds were too concentrated, and what counter-search was tried]
* Reflection: [what worked, what was noisy, what changed]

### Round 4
* Queries tried: [short list or "Not needed"]
* Reflection: [what worked, what was noisy, what changed]

## 3. Ranked Prospect Shortlist
| # | Prospect | Prospect Type | Route Type | Matched Capability | Buying Trigger / Context | Evidence | Why This Showed Up |
|---:|---|---|---|---|---|---|---|
| 1 | [Company / project] | [Fab / OSAT / EPC / cleanroom contractor / equipment OEM / materials / other] | [Direct owner / Channel-EPC / Partner ecosystem / Watchlist] | [Capability] | [Trigger or context] | [URL] | [Plain-language reason this might be relevant] |

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
* For SMEs likely to face difficult direct fab access, include channel/EPC/partner-route candidates from the beginning instead of leaving all route-to-market work to qualification.
* If early search rounds cluster around one narrow result type, force at least one counter-search before finalizing the prospect pool.
* If fewer than 20 plausible prospects are found, stop at the plausible number and say why in the caveats.
* Prefer concrete buying triggers: new fab, expansion, pilot line, reshoring, funding award, hiring, equipment install, facility commissioning, qualification, cybersecurity program, or supplier selection.
* Do not score, heavily qualify, or over-reason the candidates. Leave deep filtering to `qualify-us-prospects`.
