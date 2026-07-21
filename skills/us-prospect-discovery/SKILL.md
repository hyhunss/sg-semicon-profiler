---
name: us-prospect-discovery
description: Second skill in the SG Semicon US Expansion workflow. Use after the user reviews a map-sme-capability output. Run iterative live search to identify up to 20 possible US commercial prospects, route-to-market partners, and ecosystem connectors with only lightweight filtering. Default to SBF's priority clusters of Central Texas, Arizona, and New York unless the user specifies another scope, then stop for review.
---

# Skill: us-prospect-discovery

## Description
Use one SME capability profile to run iterative live Google Search, refine the search strategy, and create a broad list of possible US prospects for later qualification. This skill discovers candidates; it should not do heavy filtering or deep buyer-path reasoning.

Read `../../references/sbf-project-scope.md` before applying the default project scope. Preserve Skill 2's discovery role: label broadly, but leave heavy judgment to Skill 3.

This is step 2 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects
```

Assume the user has already reviewed the capability profile. Do not continue into qualification automatically. The user should check this skill's output before invoking the next skill. Make that easy by ending with explicit Continue, Revise, or Stop choices.

## Inputs
* `capability_profile`: Path to the canonical JSON file created by `map-sme-capability`, usually `data/<safe_sme_name>_capabilities.json`. Markdown capability files from older runs may be used only as fallback input.
* Optional `prospect_scope`: Any user-specified filters. If omitted, prioritize Central Texas, Arizona, and New York; deprioritize but do not prohibit California; include other US clusters only when the fit or timing signal is notably strong.

## Output
* `data/<safe_sme_name>_prospects.json`: The canonical structured prospect-discovery file. It must conform to `schema/prospect-discovery.schema.json`.
* `data/<safe_sme_name>_prospects.md`: A concise human-readable Markdown list rendered from the validated JSON.
* `data/_latest_workflow.json`: Optional convenience state file for the latest workflow.
* `data/_latest_workflow.md`: Optional human-readable convenience state file rendered from the workflow JSON.

## Data Contract
The prospect JSON file is the source of truth for `qualify-us-prospects`. Markdown is only for human review.

Use `schema_version: "1.1.0"` and `schema_name: "prospect_discovery"` in new prospect JSON files. Version `1.0.0` remains valid for older files. Before confirming completion:

1. Read the previous step's capability JSON and treat it as authoritative.
2. Write the prospect discovery JSON.
3. Run the bundled `scripts/validate_output.py` against it, resolving the script path from this skill's plugin root.
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
2. **Auto-detect input file:** If the user invokes this skill without a file path, first read `data/_latest_workflow.json`. Use its `capability_json` only when the file exists and its SME prefix agrees with `safe_sme_name`. If that state file is missing, malformed, or stale, scan `data/` and use the most recently modified JSON file ending with `_capabilities.json`. If no JSON exists, fall back to the latest `_capabilities.md` file and rebuild the required fields into the prospect JSON. If there is no matching file, ask the user to run `map-sme-capability` first or provide the capability profile path. If multiple candidates are equally recent or the intended company remains unclear, list the likely files and ask the user to choose.
3. **Handle revision requests:** If the user asks to revise this step's output, read the current prospect discovery JSON first. If only Markdown exists from an older run, read the Markdown as fallback and rebuild the JSON. Apply the requested edits, then reconstruct the entire JSON object perfectly according to `schema/prospect-discovery.schema.json` before touching Markdown. Never truncate the JSON output. Rewrite the Markdown only by mirroring the validated JSON changes. Rewrite the same JSON and Markdown files unless the user asks for a new file, update both workflow state files, and confirm briefly. Do not rerun the whole workflow unless the user explicitly asks.
4. **Read the capability profile:** Extract the SME name, safe SME name, core capabilities, confidence labels, evidence caveats, and exactly 5 smart keyword seeds from the JSON. If using Markdown fallback, convert the extracted fields into the same internal structure before searching.
5. **Set the default cluster scope:** Unless the user overrides it, search Central Texas, Arizona, and New York as the priority clusters. California is deprioritized because of cost, not excluded. Allow `Other US` candidates when capability fit or timing is clearly stronger. Do not force equal candidate counts by cluster.
6. **Define lightweight fit criteria:** Convert the capability profile into 3-5 simple discovery rules. A possible candidate should have at least one visible reason it could buy, enable, or connect the SME's real capability, such as a relevant facility, expansion, product line, supplier need, semiconductor workflow, market-entry program, or channel route.
7. **Define likely go-to-market routes:** Before searching, identify 2-4 practical routes implied by the SME capability. Include commercial buyers and route partners, plus relevant EDOs, chambers, trade associations, universities, research consortia, or public-sector initiatives. Label connectors clearly; do not imply they are direct buyers.
8. **Run Search Round 1:** Use the smart keyword seeds as the first live Google Search starting points. Search the web; do not rely on memory for current projects, funding, facilities, hiring signals, or cluster programs.
9. **Run route and connector searches early:** In the first two rounds, search for both end-customer projects and realistic access routes. Combine capability terms with `EPC`, `EPCM`, `cleanroom contractor`, `systems integrator`, `approved supplier`, `economic development organization`, `industry association`, `university consortium`, `semiconductor initiative`, or named priority clusters.
10. **Capture candidates:** For each promising result, save the company/project name, URL, prospect type, engagement role (`Commercial prospect`, `Route-to-market partner`, or `Ecosystem connector`), US cluster, matched capability, buying trigger or context, likely route type, and a short `Why this showed up` explanation. Prefer primary or high-quality sources such as company pages, press releases, CHIPS Act releases, state or regional EDO pages, procurement pages, contractor announcements, university consortium pages, and credible trade press.
11. **Apply only lightweight filtering:** Exclude clear noise: competitors, consultants without project access, recruiters, unrelated universities, non-US entities without a clear US project, and results with no connection to the SME capability or market-entry path. Do not deeply rank, qualify, or reject plausible candidates because the buyer path is uncertain; that is the third skill's job.
12. **Reflect before more searching:** After each round, briefly assess what the results are finding:
   * Are results finding buyers, competitors, or generic industry noise?
   * Which exact capability terms are working?
   * Which buyer-pain or timing terms are working?
   * Which prospect types are appearing?
   * Which route types are appearing: direct owner, channel/EPC, partner ecosystem, or watchlist?
13. **Protect search diversity:** If the first two rounds mostly find one narrow type of result, force the next round to search a different plausible prospect type, engagement role, cluster, or route. Examples:
   * If results are mostly software vendors, search hardware, equipment OEM, facility system, EPC, or systems-integrator terms.
   * If results are mostly fab owners, search EPC/EPCM, cleanroom contractor, tool-install, equipment OEM, or approved-supplier terms.
   * If results are mostly contractors or partners, search end-customer projects, OSATs, pilot lines, or funded facilities.
   * If results are mostly giant incumbents, search smaller OSATs, compound-semiconductor firms, pilot lines, startups, or regional facility projects.
   This is a discovery diversity check only. Do not qualify the prospects deeply here.
14. **Revise the next searches:** Run 1-3 additional search rounds with improved phrases. Use concrete project, procurement, cluster, and route terms. For equipment logistics SMEs, use specific tool/fab actions. For software SMEs, use supported workflow terms such as MES, WIP tracking, SPC, recipe management, OEE, or yield monitoring.
15. **Keep the pool balanced:** Include a useful mix of commercial prospects and route-to-market candidates when evidence supports both. Include ecosystem connectors only when they offer a plausible SBF or SME access route. Do not pad the list to satisfy a category quota.
16. **Stop at a useful pool:** Stop once there are enough plausible candidates or after 4 total search rounds. Do not force 20 prospects; 10-15 decent candidates is better than 20 weak ones.
17. **Order the list simply:** Put the most capability-relevant and timely candidates first, but do not use scoring. Heavy ranking belongs to `qualify-us-prospects`.
18. **Write the canonical JSON file:** Create `data/` if needed. Save as `data/<safe_sme_name>_prospects.json`, using the same safe SME name as the capability profile.
19. **Validate the prospect JSON:** Run the plugin's bundled `scripts/validate_output.py data/<safe_sme_name>_prospects.json`, resolving the script path from this SKILL.md location. Fix every reported error. Only if the validator cannot run because `jsonschema` is unavailable, carefully self-check against `schema/prospect-discovery.schema.json` and disclose that fallback in the confirmation. New version 1.1 files must identify priority clusters searched and include engagement role and US cluster for every candidate. The JSON must have 1-4 search rounds, 1-20 prospects, source URL arrays for every prospect, valid enum values, and no extra top-level fields.
20. **Render the Markdown review file:** Save `data/<safe_sme_name>_prospects.md` from the validated JSON. Do not add prospects, evidence, caveats, or recommendations in Markdown that are absent from the JSON.
21. **Write convenience workflow state:** Also write or update `data/_latest_workflow.json` with SME name, current step completed, capability JSON path, prospects JSON path, blank qualified JSON field, and next recommended command `$qualify-us-prospects`. Self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`. These files are only a convenience; do not require them for later steps.
22. **Confirm only:** Output a business-friendly success message with the readable review report path, the AI background record path, the number of possible candidates, what to review, the exact next command, how to revise, and how to stop. Do not print the full file contents in chat unless the user asks. The confirmation message must end with the three explicit choices in the template below.

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
  "schema_version": "1.1.0",
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
  "schema_version": "1.1.0",
  "schema_name": "prospect_discovery",
  "sme_name": "[Insert SME Name Here]",
  "safe_sme_name": "<safe_sme_name>",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "data/<safe_sme_name>_capabilities.json",
  "prospect_scope": "[scope used]",
  "priority_clusters_searched": ["Central Texas", "Arizona", "New York"],
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
      "engagement_role": "Commercial prospect",
      "us_cluster": "Central Texas",
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
* Priority clusters searched: [Central Texas / Arizona / New York / other user scope]
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
| # | Candidate | Role | US Cluster | Candidate Type | Route Type | Matched Capability | Trigger / Context | Evidence | Why This Showed Up |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | [Company / project / connector] | [Commercial prospect / Route-to-market partner / Ecosystem connector] | [Central Texas / Arizona / New York / California / Other US] | [Fab / OSAT / EPC / EDO / chamber / university consortium / other] | [Direct owner / Channel-EPC / Partner ecosystem / Watchlist] | [Capability] | [Trigger or context] | [URL] | [Plain-language reason this might be relevant] |

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
* New version 1.1 outputs must label every candidate's engagement role and US cluster.
* Default discovery must cover Central Texas, Arizona, and New York unless the user specifies another geography.
* Keep commercial prospects and ecosystem connectors clearly distinguished.
* Do not include a prospect only because it is a large semiconductor company; there must be a capability-relevant reason it appeared.
* For SMEs likely to face difficult direct fab access, include channel/EPC/partner-route candidates from the beginning instead of leaving all route-to-market work to qualification.
* If early search rounds cluster around one narrow result type, force at least one counter-search before finalizing the prospect pool.
* If fewer than 20 plausible prospects are found, stop at the plausible number and say why in the caveats.
* Prefer concrete buying triggers: new fab, expansion, pilot line, reshoring, funding award, hiring, equipment install, facility commissioning, qualification, cybersecurity program, or supplier selection.
* Do not score, heavily qualify, or over-reason the candidates. Leave deep filtering to `qualify-us-prospects`.
