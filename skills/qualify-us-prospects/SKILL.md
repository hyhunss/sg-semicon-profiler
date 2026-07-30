---
name: qualify-us-prospects
description: Third skill in the SG Semicon US Expansion workflow. Use after the user reviews the persistent prospect library created by us-prospect-discovery. Screen the lightweight prospect index, read only the strongest Markdown records, run targeted verification, and produce a 5-8 target decision-support shortlist with practical SBF actions. Fall back to prospect frontmatter automatically when the index is unavailable, and accept legacy consolidated Skill 2 files only when necessary.
---

# Skill: qualify-us-prospects

Reduce the accumulated Skill 2 prospect library into a small, evidence-backed shortlist. Own heavy filtering, buyer-path reasoning, scoring, and SBF action recommendations. Do not restart broad discovery.

```text
capability profile + prospect directory -> metadata screen -> focused reading
-> targeted verification -> top 5-8
```

## Inputs

- Skill 1 capability profile: `output/<safe_sme_name>/01_capability_profile.md`.
- Canonical Skill 2 directory, normally `output/<safe_sme_name>/prospects/`.
- Skill 2 speed index: `output/<safe_sme_name>/02_prospects_index.tsv`.
- Skill 2 search log: `output/<safe_sme_name>/02_search_log.md`.
- Optional `input/existing_customers.md`.
- Optional qualification preference such as easiest first outreach, near-term timing, specific state, or buyer route.
- Legacy fallback only: `output/<safe_sme_name>_prospects.json` or `.md`.

## Outputs

- `output/<safe_sme_name>/03_qualified_shortlist.json`
- `output/<safe_sme_name>/03_qualified_shortlist.md`

Use `schema_version: "1.2.0"` and `schema_name: "qualified_prospects"` for new JSON output. Treat `schema/qualified-prospects.schema.json` as the field contract and self-check the completed object against it.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve matching inputs.** If paths are not supplied, find the most recently modified `output/*/01_capability_profile.md` with a matching `prospects/` directory. If multiple SMEs remain genuinely ambiguous, ask the user to choose.

3. **Use legacy discovery only as fallback.** If no new prospect directory exists, accept a matching old `output/<safe_sme_name>_prospects.json` or `.md`. Never combine legacy and directory records silently. State which source is being qualified.

4. **Handle revisions narrowly.** For a requested revision to the qualified shortlist, read the current qualified JSON, apply the requested changes, reconstruct the complete schema-valid object, then render Markdown. Do not rerun discovery or qualification unless explicitly asked.

5. **Read capability and customer context.** Extract the SME's supported capabilities, important limitations, and search directions from the Markdown profile. Read `input/existing_customers.md` when present and matching. Exclude named existing customers and obvious corporate-group aliases unless the user requests account expansion.

6. **Use the speed index first.** Read `02_prospects_index.tsv` and compare its `prospect_id` values with the prospect filenames. Use it only when the header is exact, IDs are unique, every row has seven fields, and the IDs and row count match the Markdown files. If it is missing, malformed, or stale, continue automatically by scanning all prospect JSON frontmatter. Do not ask the user to repair an index and do not treat index text as evidence.

7. **Perform a lightweight metadata screen.** Compare all records on:

   - supported capability match;
   - visible timing or buying context;
   - plausible direct, EPC, contractor, OEM, integrator, consortium, or connector route;
   - accessibility for a Singapore SME;
   - priority-cluster relevance;
   - evidence specificity.

   Remove candidates that are only generally large semiconductor organizations, clear competitors, named existing customers, or records with no plausible buyer or access route.

8. **Select a focused reading set.** Choose the 10-15 most plausible records after the metadata screen, or fewer when the store is small. Read the complete Markdown only for this set. If the index was used, verify the selected records against their canonical frontmatter before qualification. Do not load 50-60 full files merely because they exist.

9. **Preserve discovery provenance.** From each selected record capture company, role, cluster, route, matched capabilities, buying triggers, why it may fit, queries, evidence, and caveats. Search terms and candidate records do not prove that the SME has a capability absent from Skill 1.

10. **Run targeted verification only.** Search narrowly when one current fact could change a likely finalist's rank: project timing, buyer path, procurement route, facility phase, hiring, contractor relationship, or access route. Do not run broad prospect searches.

11. **Structure every new fact.** Any fact introduced during qualification must appear in `key_evidence` with:

    - evidence role;
    - source focus;
    - source title and type;
    - source date or `Not stated`;
    - URL;
    - supported claim;
    - short excerpt or tight paraphrase.

    Label unsupported possibilities as inference or leave them out.

12. **Apply the 20-point rubric.**

    - Capability fit: 0-5
    - Timing or urgency: 0-4
    - Buyer-path clarity: 0-4
    - Accessibility and practical SBF route: 0-4
    - Priority-cluster fit: 0-1
    - Evidence strength: 0-2

13. **Classify finalists.**

    - `Priority`: strong fit, timely, and a specific route worth investigating now.
    - `Strategic`: important but likely long-cycle or partner-led.
    - `Watchlist`: relevant but timing, access, or evidence is not ready.

14. **Enforce evidence coverage.**

    - `Priority`: timing, capability fit, and buyer-path or accessibility evidence; at least two distinct URLs; at least one project/timing-specific source.
    - `Strategic`: timing, capability fit, and buyer-path or risk evidence.
    - `Watchlist`: capability fit and risk/caveat evidence.

    A generic company page alone cannot support `Priority`.

15. **Recommend one SBF intervention per finalist.** Assign `Learn`, `Lead Generation`, `Land`, or `Localize` and one concrete action, such as a cluster briefing, procurement-route validation, warm introduction, mission meeting, local partner search, incentive navigation, or supplier-localization support.

16. **Prefer realistic routes.** Compare direct-owner outreach with EPC, contractor, OEM, channel, integrator, and ecosystem routes. Do not rank a megafab owner highly without a specific route to investigate. Apply Central Texas, Arizona, and New York as tie-breakers, not absolute rules.

17. **Filter aggressively.** Produce 5-8 finalists and never more than 10. Return fewer than five when fewer are credible. Group non-finalists by concise exclusion reason rather than listing every weak record.

18. **Write canonical JSON first.** Use the Output Contract below. Set `source_prospect_directory` to the Skill 2 directory. When using a legacy input, use the legacy `source_prospect_discovery_path` field and its compatible schema version instead.

19. **Self-check and render.** Read `schema/qualified-prospects.schema.json` and compare the completed JSON against its required fields, controlled values, item limits, evidence requirements, and version-specific source field. Re-read the written JSON to ensure it is complete and parseable. Fix every mismatch. Render the Markdown report only from the self-checked JSON.

20. **Confirm briefly.** Report the number of prospect records screened, full records read, candidates verified, and finalists produced. Point to the qualified Markdown and JSON. End with use, revise, or stop choices.

## Output Contract

```json
{
  "schema_version": "1.2.0",
  "schema_name": "qualified_prospects",
  "sme_name": "[SME name]",
  "safe_sme_name": "<safe_sme_name>",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "output/<safe_sme_name>/01_capability_profile.md",
  "source_prospect_directory": "output/<safe_sme_name>/prospects",
  "qualification_scope": "[scope used]",
  "qualification_logic": {
    "sme_capabilities_used": ["[Capability]"],
    "must_not_overclaim_caveats": ["[Caveat]"],
    "best_buyer_paths": ["[Route]"]
  },
  "qualified_shortlist": [
    {
      "prospect": "[Company]",
      "classification": "Priority",
      "engagement_role": "Route-to-market partner",
      "us_cluster": "Arizona",
      "recommended_sbf_stage": "Lead Generation",
      "recommended_sbf_action": "[Concrete action]",
      "best_buyer_path": "[Specific buyer or access route]",
      "why_this_prospect": "[Concise reason]",
      "timing_signal": "[Current trigger]",
      "evidence_strength": "Direct",
      "key_evidence": [
        {
          "evidence_role": "Timing signal",
          "source_focus": "Project/timing-specific",
          "source_title": "[Project or timing source]",
          "source_type": "Press release",
          "source_date": "2026-07-28",
          "url": "https://example.com/project-source",
          "supported_claim": "[Current timing claim]",
          "evidence_excerpt": "[Short excerpt or tight paraphrase]"
        },
        {
          "evidence_role": "Capability fit",
          "source_focus": "Capability/background",
          "source_title": "[Capability source]",
          "source_type": "Company page",
          "source_date": "Not stated",
          "url": "https://example.com/capability-source",
          "supported_claim": "[Capability-fit claim]",
          "evidence_excerpt": "[Short excerpt or tight paraphrase]"
        },
        {
          "evidence_role": "Buyer path",
          "source_focus": "Route/access",
          "source_title": "[Buyer-route source]",
          "source_type": "Company page",
          "source_date": "Not stated",
          "url": "https://example.com/capability-source",
          "supported_claim": "[Specific buyer or access route]",
          "evidence_excerpt": "[Short excerpt or tight paraphrase]"
        }
      ],
      "score": 17,
      "what_to_verify_next": "[One verification question]"
    }
  ],
  "deprioritized_or_excluded": [
    {
      "prospect_or_group": "[Candidate or grouped category]",
      "reason": "[Reason]"
    }
  ],
  "recommended_next_steps": ["[Concrete next action]"]
}
```

## Markdown report

Render these sections:

1. Inputs and number of prospect records screened
2. Qualification logic
3. Qualified shortlist table
4. Structured evidence by finalist
5. Grouped exclusions
6. Recommended next actions

Do not introduce claims, scores, or recommendations absent from the self-checked JSON.

## Quality bar

- Read the capability profile and the Skill 2 prospect store.
- Screen every prospect through the index or, on fallback, its frontmatter.
- Read full files only for the focused 10-15 candidate set.
- Produce 5-8 finalists, never more than 10, without padding.
- Give every finalist a specific buyer path, one verification question, and one concrete SBF action.
- Meet classification-specific evidence coverage.
- Exclude named existing customers unless account expansion is requested.
- Separate direct evidence from inference.
- Treat the shortlist as company-level decision support, not SBF's complete multi-year strategy.
