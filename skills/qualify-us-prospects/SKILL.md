---
name: qualify-us-prospects
description: Third skill in the SG Semicon US Expansion workflow. Use only after the user has reviewed the us-prospect-discovery output. Given an SME capability profile and broad prospect-discovery file, or invoked with no paths after matching files exist in data/, filter the list into the most likely US prospects for deeper analysis or outreach. Stop after writing the qualified shortlist and tell the user what to review before using it.
---

# Skill: qualify-us-prospects

## Description
Read the outputs from both earlier skills and reduce a broad US prospect list into a smaller, qualified shortlist. This skill owns the heavy filtering, buyer-path reasoning, ranking, and tradeoff explanation. It should not restart broad discovery.

This is step 3 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects -> user reviews qualified shortlist
```

Assume the user has already reviewed both earlier files. This skill produces the final shortlist for human review; it should not restart the earlier stages.

## Inputs
* `capability_profile`: Path to the first skill's canonical JSON output, usually `data/<safe_sme_name>_capabilities.json`. Markdown capability files from older runs may be used only as fallback input.
* `prospect_discovery`: Path to the second skill's canonical JSON output, usually `data/<safe_sme_name>_prospects.json`. Markdown prospect files from older runs may be used only as fallback input.
* Optional `shortlist_size`: Target number of qualified prospects. Default: 5-8. Maximum: 10.
* Optional `qualification_scope`: User-specified preference such as easiest first outreach, highest strategic value, near-term timing, specific US state, or specific buyer route.

## Output
* `data/<safe_sme_name>_qualified_prospects.json`: The canonical structured qualified shortlist. It must conform to `schema/qualified-prospects.schema.json`.
* `data/<safe_sme_name>_qualified_prospects.md`: A compact human-readable Markdown shortlist rendered from the validated JSON.
* `data/_latest_workflow.json`: Optional convenience state file for the latest workflow.
* `data/_latest_workflow.md`: Optional human-readable convenience state file rendered from the workflow JSON.

## Data Contract
The qualified prospects JSON file is the source of truth for automation, deeper research, CRM import, and outreach planning. Markdown is only for human review.

Use `schema_version: "1.0.0"` and `schema_name: "qualified_prospects"` in the qualified JSON. Before confirming completion:

1. Read the previous skills' JSON files and treat them as authoritative.
2. Write the qualified prospects JSON.
3. Validate or carefully self-check it against `schema/qualified-prospects.schema.json`.
4. Fix any schema mismatch before continuing.
5. Render the Markdown review file from the validated JSON.
6. Update `data/_latest_workflow.json`, self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`.

## Core Rule
Treat the second skill's output as a candidate pool, not as a qualified list. Do not confuse "large semiconductor project" with "qualified prospect":

```text
capabilities.md + prospects.md -> buyer-path qualification -> top 5-8 likely prospects
```

## Instructions
1. **Accept selected-prompt invocations:** If the user's message body is blank but selected text contains a prompt for this skill, treat the selected text as the user's instruction and proceed from it. Do not ask the user to paste it again.
2. **Auto-detect input files:** If invoked without file paths, use Read access to scan the current workspace's `data/` directory. Identify JSON files ending with `_capabilities.json` and `_prospects.json` that share the exact same SME prefix. Use the most recently modified valid pair as the inputs. If no JSON pair exists, fall back to matching Markdown files ending with `_capabilities.md` and `_prospects.md` and rebuild the needed fields into the qualified JSON. If no matching pair exists, ask the user to run `us-prospect-discovery` first or provide both file paths. If more than one recent pair could be intended, list the likely pairs and ask the user to choose.
3. **Handle revision requests:** If the user asks to revise this step's output, read the current qualified shortlist JSON first. If only Markdown exists from an older run, read the Markdown as fallback and rebuild the JSON. Apply the requested edits, then reconstruct the entire JSON object perfectly according to `schema/qualified-prospects.schema.json` before touching Markdown. Never truncate the JSON output. Rewrite the Markdown only by mirroring the validated JSON changes. Rewrite the same JSON and Markdown files unless the user asks for a new file, update both workflow state files, and confirm briefly. Do not rerun the whole workflow unless the user explicitly asks.
4. **Read both inputs:** Use the capability JSON to understand what the SME can credibly sell. Use the prospect-discovery JSON as the candidate pool. If using Markdown fallback, convert the extracted fields into the same internal structure before qualifying. Do not evaluate prospects using capabilities that are not supported in the first file.
5. **Extract constraints from the capability profile:** Capture the SME name, 1-3 core capabilities, confidence labels, evidence caveats, and any terms the SME should avoid over-claiming.
6. **Extract candidates from the prospect-discovery file:** Capture prospect name, prospect type, route type if present, matched capability, buying trigger or context, evidence URL, `Why this showed up`, caveats, and any recommended next analysis. If the prospect file includes older fields such as score, confidence, or likely buyer path, treat them as helpful notes only, not final qualification.
7. **Remove weak candidates first:** Drop candidates that only match because they are generally large semiconductor companies, have no clear link to the SME capability, are likely competitors, or look unreachable without a realistic route.
8. **Do targeted verification only when needed:** If a top candidate's buyer path, timing, or evidence is unclear, run a narrow search for that candidate. Do not run broad discovery searches. Limit verification to likely top candidates or candidates where one fact would change the ranking.
9. **Source every new verification fact:** Any fact introduced during targeted verification must have a source URL in the final output. This includes named EPCs, contractors, construction managers, cleanroom square footage, groundbreaking dates, procurement routes, funding status, project phase, partnerships, or facility scope. If a new fact cannot be sourced, label it as an inference or leave it out.
10. **Prefer realistic go-to-market routes:** For Singapore SMEs, explicitly compare direct-owner outreach with channel/EPC/contractor/partner routes. Do not rank megafab owners highly unless the buyer path is specific enough to investigate.
11. **Apply the qualification test:** A qualified prospect should pass most of these questions:
   * Does the prospect need the SME's real capability?
   * Is there a concrete timing signal, such as new facility, ramp, modernization, tool install, pilot line, hiring, or supplier development?
   * Is the likely buyer path specific and plausible?
   * Is the prospect reachable for a Singapore SME through a direct buyer, partner, OEM, EPC, integrator, contractor, approved supplier, or public consortium route?
   * Is the evidence direct or a strong inference rather than a weak inference?
12. **Score with a practical 20-point rubric:**
   * Capability fit: 0-5
   * Timing / urgency: 0-4
   * Buyer-path clarity: 0-5
   * Accessibility for Singapore SME: 0-4
   * Evidence strength: 0-2
13. **Classify each finalist:** Use one of these labels:
   * `Priority`: strong fit, plausible buyer path, worth deeper analysis now.
   * `Watchlist`: good fit but timing, access, or evidence is not ready.
   * `Strategic`: large or important account, but likely long-cycle or partner-led.
14. **Filter aggressively:** Prefer 5-8 strong qualified prospects over a full list. Do not pad the shortlist. If fewer than 5 are credible, write fewer and explain why.
15. **Explain exclusions:** Group non-finalists into short reason categories such as weak buyer path, timing too early, too large/locked supplier base, indirect fit, likely competitor/channel target, or insufficient evidence.
16. **Write the canonical JSON file:** Save as `data/<safe_sme_name>_qualified_prospects.json`, using the same safe SME name as the input files.
17. **Validate the qualified JSON:** Validate or carefully self-check against `schema/qualified-prospects.schema.json`. The JSON must have 1-10 finalists, valid classification and evidence-strength enum values, integer scores from 0-20, source URL arrays for every finalist, one verification question per finalist, and no extra top-level fields. The order of the `qualified_shortlist` array is the ranking; do not add a separate rank field.
18. **Render the Markdown review file:** Save `data/<safe_sme_name>_qualified_prospects.md` from the validated JSON. Do not add finalists, evidence, exclusions, or next steps in Markdown that are absent from the JSON.
19. **Write convenience workflow state:** Also write or update `data/_latest_workflow.json` with SME name, current step completed, capability JSON path, prospects JSON path, qualified JSON path, and next recommended command `Final review complete; use, revise, or stop`. Self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`. These files are only a convenience; do not require them for later work.
20. **Confirm only:** Output a business-friendly success message with the readable review report path, the AI background record path, the number of qualified prospects, what to review, how to use it, how to revise, and how to stop. Do not print the full file contents in chat unless the user asks. The confirmation message must end with the three explicit choices in the template below.

## Confirmation Message Template

```text
Created successfully:
- Final Structured Shortlist (AI Record): data/<safe_sme_name>_qualified_prospects.json
- Final Outbound Roadmap Report: data/<safe_sme_name>_qualified_prospects.md

Qualified <N> prospects using the 20-point practical rubric. Please double-click to open 'data/<safe_sme_name>_qualified_prospects.md' to review your final strategic roadmap.

Next Steps:
A. Export/Print the report for strategic outbound actions or SBF/Enterprise Singapore grant applications.

B. To revise, type:
   Revise the qualified shortlist: [describe your changes]
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
  "current_step_completed": "Step 3 - Qualify US Prospects",
  "capability_json": "data/<safe_sme_name>_capabilities.json",
  "prospects_json": "data/<safe_sme_name>_prospects.json",
  "qualified_json": "data/<safe_sme_name>_qualified_prospects.json",
  "next_recommended_command": "Final review complete; use, revise, or stop"
}
```

Render this human-readable companion as `data/_latest_workflow.md`:

```markdown
# Latest SG Semicon Expansion Workflow

* SME name: [SME Name]
* Current step completed: Step 3 - Qualify US Prospects
* Capability JSON: data/<safe_sme_name>_capabilities.json
* Prospects JSON: data/<safe_sme_name>_prospects.json
* Qualified JSON: data/<safe_sme_name>_qualified_prospects.json
* Qualified Markdown: data/<safe_sme_name>_qualified_prospects.md
* Next recommended command: Final review complete; use, revise, or stop
```

## Output JSON Template

Write this canonical file first as `data/<safe_sme_name>_qualified_prospects.json`:

```json
{
  "schema_version": "1.0.0",
  "schema_name": "qualified_prospects",
  "sme_name": "[Insert SME Name Here]",
  "safe_sme_name": "<safe_sme_name>",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "data/<safe_sme_name>_capabilities.json",
  "source_prospect_discovery_path": "data/<safe_sme_name>_prospects.json",
  "qualification_scope": "[scope or default]",
  "qualification_logic": {
    "sme_capabilities_used": [
      "[Capability 1]"
    ],
    "must_not_overclaim_caveats": [
      "[Caveat 1]"
    ],
    "best_buyer_paths": [
      "[Buyer path 1]"
    ]
  },
  "qualified_shortlist": [
    {
      "prospect": "[Prospect]",
      "classification": "Priority",
      "best_buyer_path": "[Specific path]",
      "why_this_prospect": "[Concise reason]",
      "timing_signal": "[Trigger]",
      "evidence_strength": "Direct",
      "key_evidence_urls": ["[Source URL]"],
      "score": 18,
      "what_to_verify_next": "[Next verification question]"
    }
  ],
  "deprioritized_or_excluded": [
    {
      "prospect_or_group": "[Prospect]",
      "reason": "[Reason]"
    }
  ],
  "recommended_next_steps": [
    "[Concrete next action for the top 1-3 prospects]"
  ]
}
```

## Output Markdown Template

Render this human-readable file from the validated JSON as `data/<safe_sme_name>_qualified_prospects.md`:

```markdown
# Qualified US Prospects: [Insert SME Name Here]

## 1. Inputs Used
* Capability profile path: [path]
* Prospect discovery path: [path]
* Qualification scope: [scope or "default"]

## 2. Qualification Logic
* SME capabilities used:
  * [Capability 1]
  * [Capability 2]
  * [Capability 3]
* Must-not-overclaim caveats:
  * [Caveat 1]
* Best buyer paths:
  * [Buyer path 1]
  * [Buyer path 2]

## 3. Qualified Shortlist
| Rank | Prospect | Classification | Best Buyer Path | Why This Prospect | Timing Signal | Evidence Strength | Key Evidence | Score | What To Verify Next |
|---:|---|---|---|---|---|---|---|---:|---|
| 1 | [Prospect] | [Priority/Watchlist/Strategic] | [Specific path] | [Concise reason] | [Trigger] | [Direct/Strong inference/Weak inference] | [Source URL(s), including URLs for any new verification facts] | [0-20] | [Next verification question] |

## 4. Deprioritized or Excluded
| Prospect / Group | Reason |
|---|---|
| [Prospect] | [Reason] |

## 5. Recommended Next Step
* [Concrete next action for the top 1-3 prospects]
```

## Quality Bar
* The skill must read both the capability profile and prospect-discovery file.
* Treat the prospect-discovery file as broad discovery, not as a final ranking.
* The final shortlist should usually contain 5-8 prospects and never more than 10.
* Every finalist must have a specific buyer path.
* Every finalist must include one targeted verification question.
* Every finalist must include source URL(s) for the timing signal and for any new verification facts introduced during qualification.
* Do not include a prospect only because it is a large semiconductor company.
* Use `Priority` only when the buyer path is specific and timing is actionable.
* Clearly separate evidence from inference.
