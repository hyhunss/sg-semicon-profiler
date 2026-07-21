---
name: qualify-us-prospects
description: Third skill in the SG Semicon US Expansion workflow. Use after the user reviews the broad discovery output. Heavily filter and reason over commercial prospects, route-to-market partners, and ecosystem connectors; account for SBF priority clusters and recommend a Learn, Lead Generation, Land, or Localize action for each finalist. Produce a 5-8 target decision-support shortlist, then stop for review.
---

# Skill: qualify-us-prospects

## Description
Read the outputs from both earlier skills and reduce a broad US prospect list into a smaller, qualified shortlist. This skill owns the heavy filtering, buyer-path reasoning, ranking, and tradeoff explanation. It should not restart broad discovery.

Read `../../references/sbf-project-scope.md` before applying the default project scope. This output supports the broader SBF playbook; do not describe the company shortlist itself as SBF's complete 3-to-5-year strategic roadmap.

This is step 3 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects -> user reviews qualified shortlist
```

Assume the user has already reviewed both earlier files. This skill produces the final shortlist for human review; it should not restart the earlier stages.

## Inputs
* `capability_profile`: Path to the first skill's canonical JSON output, usually `data/<safe_sme_name>_capabilities.json`. Markdown capability files from older runs may be used only as fallback input.
* `prospect_discovery`: Path to the second skill's canonical JSON output, usually `data/<safe_sme_name>_prospects.json`. Markdown prospect files from older runs may be used only as fallback input.
* Optional `input/existing_customers.md`: Private context used to improve fit reasoning and enforce existing-customer exclusion.
* Optional `shortlist_size`: Target number of qualified prospects. Default: 5-8. Maximum: 10.
* Optional `qualification_scope`: User-specified preference such as easiest first outreach, highest strategic value, near-term timing, specific US state, or specific buyer route.

## Output
* `data/<safe_sme_name>_qualified_prospects.json`: The canonical structured qualified shortlist. It must conform to `schema/qualified-prospects.schema.json`.
* `data/<safe_sme_name>_qualified_prospects.md`: A compact human-readable Markdown shortlist rendered from the validated JSON.
* `data/_latest_workflow.json`: Optional convenience state file for the latest workflow.
* `data/_latest_workflow.md`: Optional human-readable convenience state file rendered from the workflow JSON.

## Data Contract
The qualified prospects JSON file is the source of truth for automation, deeper research, CRM import, and outreach planning. Markdown is only for human review.

Use `schema_version: "1.1.0"` and `schema_name: "qualified_prospects"` in new qualified JSON files. Version `1.0.0` remains valid for older files. Before confirming completion:

1. Read the previous skills' JSON files and treat them as authoritative.
2. Write the qualified prospects JSON.
3. Run the bundled `scripts/validate_output.py` against it, resolving the script path from this skill's plugin root.
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
2. **Auto-detect input files:** If invoked without file paths, first read `data/_latest_workflow.json`. Use its `capability_json` and `prospects_json` only when both files exist, share the exact SME prefix, and agree with `safe_sme_name`. If that state file is missing, malformed, incomplete, or stale, scan `data/` for JSON files ending with `_capabilities.json` and `_prospects.json` that share the exact SME prefix, then use the most recently modified valid pair. If no JSON pair exists, fall back to a matching Markdown pair and rebuild the needed fields into the qualified JSON. If no matching pair exists, ask the user to run `us-prospect-discovery` first or provide both file paths. If more than one recent pair could be intended, list the likely pairs and ask the user to choose.
3. **Handle revision requests:** If the user asks to revise this step's output, read the current qualified shortlist JSON first. If only Markdown exists from an older run, read the Markdown as fallback and rebuild the JSON. Apply the requested edits, then reconstruct the entire JSON object perfectly according to `schema/qualified-prospects.schema.json` before touching Markdown. Never truncate the JSON output. Rewrite the Markdown only by mirroring the validated JSON changes. Rewrite the same JSON and Markdown files unless the user asks for a new file, update both workflow state files, and confirm briefly. Do not rerun the whole workflow unless the user explicitly asks.
4. **Read both workflow inputs and customer context:** Use the capability JSON to understand what the SME can credibly sell. Use the prospect-discovery JSON as the candidate pool. If using Markdown fallback, convert the extracted fields into the same internal structure before qualifying. Also read `input/existing_customers.md` when present. If its `SME name` is blank, set it to the active SME before using any entries. Use populated context only when that name matches the workflow inputs. If it names another SME, stop and ask whether to replace it or continue without it. Parse named customers separately from anonymous patterns and relationship notes. Treat this as private user-provided context, not public evidence. Do not evaluate prospects using technical capabilities that are unsupported in the first file.
5. **Extract constraints from the capability profile:** Capture the SME name, 1-3 core capabilities, confidence labels, SBF scope assessment when present, evidence caveats, and any terms the SME should avoid over-claiming. Unknown ownership or size is a verification gap, not an automatic rejection.
6. **Extract the search plan and candidates:** Capture the confirmed technical terms and their provenance when `search_term_plan` is present, plus candidate name, prospect type, engagement role, US cluster, route type, matched capability, buying trigger or context, evidence URL, `Why this showed up`, caveats, and recommended next analysis. For older files without the newer fields, infer cautiously and label the inference.
7. **Protect capability integrity:** Treat profile-supported search terms as grounded in Skill 1. Treat AI-suggested, user-added, and customer-pattern terms as discovery hypotheses unless Skill 1 or targeted verification confirms that the SME offers the relevant capability. Customer patterns may strengthen route or market-fit reasoning, but do not prove a technical capability. Do not award capability-fit points or make an unqualified capability claim from those terms alone; record the gap as a caveat or verification question.
8. **Remove weak candidates and existing customers first:** Drop candidates that only match because they are generally large semiconductor companies, have no clear link to the SME capability, are likely competitors, or look unreachable without a realistic route. Exclude every named existing customer and its obvious corporate-group aliases from the shortlist unless the user explicitly requests account-expansion analysis. Do not copy named customers into the qualified JSON, Markdown, or exclusion explanation.
9. **Do targeted verification only when needed:** If a top candidate's buyer path, timing, or evidence is unclear, run a narrow search for that candidate. Do not run broad discovery searches. Limit verification to likely top candidates or candidates where one fact would change the ranking.
10. **Source every new verification fact with evidence detail:** Any fact introduced during targeted verification must have a structured evidence item in the final output. This includes named EPCs, contractors, construction managers, cleanroom square footage, groundbreaking dates, procurement routes, funding status, project phase, partnerships, or facility scope. Each finalist must include evidence with evidence role, source focus, source title, source type, source date when available, URL, supported claim, and a short evidence excerpt. If a new fact cannot be sourced, label it as an inference or leave it out. Do not use bare URLs as final evidence.
11. **Cover the evidence roles required by the classification:** `Priority` finalists must include evidence for `Timing signal`, `Capability fit`, and either `Buyer path` or `Accessibility`. `Strategic` finalists must include evidence for `Timing signal`, `Capability fit`, and either `Buyer path` or `Risk / caveat`. `Watchlist` finalists must include evidence for `Capability fit` and `Risk / caveat`. Do not promote a prospect to `Priority` unless all three Priority evidence roles are present.
12. **Apply the higher Priority evidence standard:** Every `Priority` finalist must use at least two distinct source URLs across its evidence items, and at least one evidence item must have `source_focus: "Project/timing-specific"`. A generic company capability page alone is not enough for `Priority`, even if it mentions semiconductor work. If the two-source or project/timing-specific standard is not met, classify the prospect as `Strategic` or `Watchlist` instead.
13. **Prefer realistic go-to-market routes:** Explicitly compare direct-owner outreach with channel/EPC/contractor/partner routes and ecosystem connectors. Keep commercial prospects, route partners, and connectors clearly labeled. Do not rank megafab owners highly unless the buyer path is specific enough to investigate.
14. **Apply the qualification test:** A qualified prospect should pass most of these questions:
   * Does the prospect need the SME's real capability?
   * Is there a concrete timing signal, such as new facility, ramp, modernization, tool install, pilot line, hiring, or supplier development?
   * Is the likely buyer path specific and plausible?
   * Is the prospect reachable for a Singapore SME through a direct buyer, partner, OEM, EPC, integrator, contractor, approved supplier, or public consortium route?
   * Is the evidence direct or a strong inference rather than a weak inference?
15. **Score with a practical 20-point rubric:**
   * Capability fit: 0-5
   * Timing / urgency: 0-4
   * Buyer-path clarity: 0-4
   * Accessibility and practical SBF support route: 0-4
   * Priority-cluster fit: 0-1
   * Evidence strength: 0-2
16. **Classify each finalist:** Use one of these labels:
   * `Priority`: strong fit, plausible buyer path, worth deeper analysis now.
   * `Watchlist`: good fit but timing, access, or evidence is not ready.
   * `Strategic`: large or important account, but likely long-cycle or partner-led.
17. **Recommend the SBF intervention:** For every finalist, assign one stage and one concrete action: `Learn`, `Lead Generation`, `Land`, or `Localize`. Match the action to the SME's readiness and the finalist's role. Examples include a cluster briefing, warm introduction, mission meeting, procurement-route validation, site-selection support, incentive navigation, local partner search, or supplier-localization support.
18. **Apply cluster priority without making it absolute:** Prefer Central Texas, Arizona, and New York when other factors are comparable. California or Other US candidates can outrank them when fit, timing, and access evidence are materially stronger. State the reason.
19. **Filter aggressively:** Prefer 5-8 strong qualified candidates over a full list. Do not pad the shortlist or force a quota by cluster or engagement role. If fewer than 5 are credible, write fewer and explain why.
20. **Explain exclusions:** Group non-finalists into short reason categories such as weak buyer path, timing too early, too large/locked supplier base, indirect fit, connector without a practical route, likely competitor, or insufficient evidence.
21. **Run the final existing-customer check and write JSON:** Compare every finalist against `input/existing_customers.md` one final time, remove any named existing customer or obvious group alias unless account expansion was explicitly requested, then save as `data/<safe_sme_name>_qualified_prospects.json` using the same safe SME name as the input files.
22. **Validate the qualified JSON:** Run the plugin's bundled `scripts/validate_output.py data/<safe_sme_name>_qualified_prospects.json`, resolving the script path from this SKILL.md location. Fix every reported error. Only if the validator cannot run because `jsonschema` is unavailable, carefully self-check against `schema/qualified-prospects.schema.json` and disclose that fallback in the confirmation. New version 1.1 files must include engagement role, US cluster, recommended SBF stage, and recommended SBF action for every finalist. Confirm valid enum values, scores from 0-20, structured evidence, classification evidence coverage, one verification question per finalist, and at least two distinct URLs for every Priority finalist.
23. **Render the Markdown review file:** Save `data/<safe_sme_name>_qualified_prospects.md` from the validated JSON. Do not add finalists, evidence, exclusions, or next steps in Markdown that are absent from the JSON.
24. **Write convenience workflow state:** Also write or update `data/_latest_workflow.json` with SME name, current step completed, capability JSON path, prospects JSON path, qualified JSON path, and next recommended command `Final review complete; use, revise, or stop`. Self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`. These files are only a convenience; do not require them for later work.
25. **Confirm only:** Output a business-friendly success message with the readable review report path, the AI background record path, the number of qualified candidates, what to review, how to use it, how to revise, and how to stop. Describe the output as a company-level SBF decision-support shortlist, not the complete SBF strategic roadmap. The confirmation message must end with the three explicit choices in the template below.

## Confirmation Message Template

```text
Created successfully:
- Final Structured Shortlist (AI Record): data/<safe_sme_name>_qualified_prospects.json
- SBF Decision-Support Shortlist: data/<safe_sme_name>_qualified_prospects.md

Qualified <N> candidates using the 20-point practical rubric. Please open 'data/<safe_sme_name>_qualified_prospects.md' to review the recommended commercial routes, connectors, and SBF support actions.

Next Steps:
A. Use the shortlist to plan deeper diligence, introductions, mission meetings, or other SBF support.

B. To revise, type:
   Revise the qualified shortlist: [describe your changes]
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
  "schema_version": "1.1.0",
  "schema_name": "qualified_prospects",
  "sme_name": "[Insert SME Name Here]",
  "safe_sme_name": "sample_sme",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "data/sample_sme_capabilities.json",
  "source_prospect_discovery_path": "data/sample_sme_prospects.json",
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
      "engagement_role": "Commercial prospect",
      "us_cluster": "Central Texas",
      "recommended_sbf_stage": "Lead Generation",
      "recommended_sbf_action": "Arrange a warm introduction and validate the procurement route before a mission meeting.",
      "best_buyer_path": "[Specific path]",
      "why_this_prospect": "[Concise reason]",
      "timing_signal": "[Trigger]",
      "evidence_strength": "Direct",
      "key_evidence": [
        {
          "evidence_role": "Timing signal",
          "source_focus": "Project/timing-specific",
          "source_title": "[Source page or document title]",
          "source_type": "Press release",
          "source_date": "Not stated",
          "url": "https://example.com/project-source",
          "supported_claim": "[Specific claim this source supports]",
          "evidence_excerpt": "[Short exact phrase or tightly paraphrased excerpt from the source]"
        },
        {
          "evidence_role": "Capability fit",
          "source_focus": "Capability/background",
          "source_title": "[Source page or document title]",
          "source_type": "Company page",
          "source_date": "Not stated",
          "url": "https://example.com/capability-source",
          "supported_claim": "[Specific claim this source supports]",
          "evidence_excerpt": "[Short exact phrase or tightly paraphrased excerpt from the source]"
        },
        {
          "evidence_role": "Buyer path",
          "source_focus": "Route/access",
          "source_title": "[Source page or document title]",
          "source_type": "Company page",
          "source_date": "Not stated",
          "url": "https://example.com/capability-source",
          "supported_claim": "[Specific claim this source supports]",
          "evidence_excerpt": "[Short exact phrase or tightly paraphrased excerpt from the source]"
        }
      ],
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
| Rank | Candidate | Role | US Cluster | Classification | Best Route | SBF Stage and Action | Why This Candidate | Timing | Evidence | Score | Verify Next |
|---:|---|---|---|---|---|---|---|---|---|---:|---|
| 1 | [Candidate] | [Commercial prospect / Route-to-market partner / Ecosystem connector] | [Cluster] | [Priority/Watchlist/Strategic] | [Specific path] | [Stage: concrete action] | [Concise reason] | [Trigger] | [Structured evidence summary] | [0-20] | [Next verification question] |

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
* New version 1.1 outputs must include engagement role, US cluster, recommended SBF stage, and a concrete SBF action for every finalist.
* Treat the shortlist as company-level decision support for the broader SBF playbook, not as the complete 3-to-5-year roadmap.
* Every finalist must include structured evidence for the timing signal and for any new verification facts introduced during qualification. Do not use bare URLs as final evidence.
* Each structured evidence item must include evidence role, source focus, source title, source type, source date or `Not stated`, URL, supported claim, and a short excerpt.
* Evidence role coverage is mandatory: `Priority` needs timing, fit, and access-route evidence; `Strategic` needs timing, fit, and route or caveat evidence; `Watchlist` needs fit and caveat evidence.
* Every `Priority` prospect must have at least two distinct source URLs and at least one `Project/timing-specific` source. A generic company capability page alone cannot support a `Priority` classification.
* Do not include a prospect only because it is a large semiconductor company.
* Use `Priority` only when the buyer path is specific and timing is actionable.
* Never include a named existing customer or obvious corporate-group alias in the new-prospect shortlist unless the user explicitly requests account-expansion analysis.
* Do not copy named existing customers from the private input file into generated qualification outputs.
* Clearly separate evidence from inference.
