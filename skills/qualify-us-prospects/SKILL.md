---
name: qualify-us-prospects
description: Third skill in the SG Semicon US Expansion workflow. Use after the user reviews the persistent prospect library created by us-prospect-discovery. Screen the lightweight prospect index, read only the strongest Markdown records, run targeted verification, and produce a 5-8 target decision-support shortlist with score breakdowns, a one-page leadership brief, and practical SBF actions. Fall back to prospect frontmatter automatically when the index is unavailable, and accept legacy consolidated Skill 2 files only when necessary.
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

Use `schema_version: "1.4.0"` and `schema_name: "qualified_prospects"` for new JSON output. Treat `schema/qualified-prospects.schema.json` as the field contract and self-check the completed object against it. Continue to accept valid legacy 1.0.0-1.3.0 outputs when revising or reading older work.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve matching inputs.** If paths are not supplied, find the most recently modified `output/*/01_capability_profile.md` with a matching `prospects/` directory. If multiple SMEs remain genuinely ambiguous, ask the user to choose.

3. **Use legacy discovery only as fallback.** If no new prospect directory exists, accept a matching old `output/<safe_sme_name>_prospects.json` or `.md`. Never combine legacy and directory records silently. State which source is being qualified.

4. **Handle revisions narrowly.** For a requested revision to the qualified shortlist, read the current qualified JSON, apply the requested changes, reconstruct the complete schema-valid object, then render Markdown. Do not rerun discovery or qualification unless explicitly asked.

5. **Read capability and customer context.** Extract the SME's supported capabilities, important limitations, and search directions from the Markdown profile. Read `input/existing_customers.md` when present and matching. Exclude named existing customers and obvious corporate-group aliases unless the user requests account expansion.

6. **Use the speed index first.** Read `02_prospects_index.tsv` and compare its `prospect_id` values with the prospect filenames. Use it only when the header is exact, IDs are unique, every row has six fields, and the IDs and row count match the Markdown files. If it is missing, malformed, or stale, continue automatically by scanning all prospect YAML frontmatter. Do not ask the user to repair an index and do not treat index text as evidence.

7. **Count the complete screening pool.** Count the exact number of distinct prospect records that will be screened from the validated index or, when the index is unavailable, from the canonical prospect directory. Store this integer as `total_prospects_screened`. Count each canonical prospect record once, include every record considered in the lightweight metadata screen whether shortlisted or excluded, and verify that the count is at least the number of finalists. Do not use the 10-15 focused-reading count or grouped exclusion count as a substitute.

8. **Perform a lightweight metadata screen.** Compare all records on:

   - supported capability match;
   - visible timing or buying context;
   - plausible direct, EPC, contractor, OEM, integrator, consortium, or connector route;
   - accessibility for a Singapore SME;
   - priority-cluster relevance;
   - evidence specificity.

   Remove candidates that are only generally large semiconductor organizations, clear competitors, named existing customers, or records with no plausible buyer or access route.

9. **Select a focused reading set.** Choose the 10-15 most plausible records after the metadata screen, or fewer when the store is small. Read the complete Markdown only for this set. If the index was used, verify the selected records against their canonical frontmatter before qualification. Do not load 50-60 full files merely because they exist.

10. **Preserve discovery provenance.** From each selected record capture company, role, cluster, route, matched capabilities, sourced body evidence, and caveats. Search terms remain in the search log and do not prove that the SME has a capability absent from Skill 1.

11. **Run targeted verification only.** Search narrowly when one current fact could change a likely finalist's rank: project timing, buyer path, procurement route, facility phase, hiring, contractor relationship, or access route. Do not run broad prospect searches or target `site:linkedin.com` or other private social networks.

    - For `timing_signal`, check recent first-party career pages or public Greenhouse/Lever postings, CHIPS.gov notices, and state or regional EDO grant and expansion announcements.
    - For `best_buyer_path`, check named EPC/GC project announcements, contractor portfolios, SAM.gov notices, CHIPS.gov releases, and state EDO announcements.
    - For possible insider timing, subcontractor discussion, or project caveats, fetch `https://hn.algolia.com/api/v1/search_by_date?query=%22[exact_prospect_or_project_phrase]%22+[specific_cluster]&tags=comment&numericFilters=created_at_i%3E[TIMESTAMP_6_MONTHS_AGO]`. URL-encode values and never use a generic term such as `fab` alone.
    - Prioritize `Job posting`, `Government notice`, and `Contractor project page` as source types when they directly support the claim.

    A job posting proves only the stated hiring activity; it does not by itself prove construction, procurement need, or expansion. A grant or award proves a buyer, contractor, or tier relationship only when the notice explicitly names that relationship. Treat HN stories and comments as `Other` sources and normally as risk/caveat or discovery evidence, not direct proof. An HN discussion alone cannot establish `timing_signal`, `best_buyer_path`, a commercial relationship, or `Priority` status. Corroborate material claims with a primary or high-quality source; otherwise label the connection as inference or leave it out.

12. **Structure every new fact.** Any fact introduced during qualification must appear in `key_evidence` with:

    - evidence role;
    - source focus;
    - source title and type;
    - source date or `Not stated`;
    - actual access date;
    - URL;
    - supported claim;
    - short excerpt or tight paraphrase.

    Use each normalized URL only once per finalist. A source can support more than one conclusion, but do not create one `key_evidence` item per role from the same page. Select its principal evidence role, then combine the tightly related supported conclusions and caveat in that one item's `supported_claim` and `evidence_excerpt`. Obtain a distinct source when a coverage rule requires another role. Normalize URLs for this check by trimming whitespace, lowercasing the scheme and host, removing a trailing slash from a non-root path, and preserving the path and query. Label unsupported possibilities as inference or leave them out.

13. **Use runtime-derived time values.** At the start of qualification and immediately before the final write, read the current local time from the Codex runtime or system clock. Use the final exact ISO 8601 timestamp returned by the environment as `generated_at` and its calendar date as `accessed_on` for every source actually opened during this run. Never estimate or manually generate either value. Preserve an older access date only when carrying forward evidence without reopening its URL. This is an internal Codex operation: never create a helper script or ask the SME user to run a command. If the runtime clock is unavailable, stop before writing rather than inventing a timestamp.

14. **Apply and expose the 20-point rubric.** The total is exactly **20 points**. Use every whole number from zero through the criterion maximum. The anchors below guide judgement; they do not prohibit intermediate scores.

    | Criterion | Max | Weight | Score range | Award the maximum when |
    |---|---:|---:|---|---|
    | Capability fit | 5 | 25% | 0-5 | The SME's documented capability addresses a specific prospect need, process step, facility package, or operating problem. |
    | Timing or urgency | 4 | 20% | 0-4 | A current expansion, ramp, qualification window, operating problem, or supplier-localisation trigger is sourced. |
    | Buyer-path clarity | 4 | 20% | 0-4 | A buyer function, sponsor, OEM, EPC, integrator, distributor, or another credible route is specifically evidenced. |
    | Accessibility and practical SBF route | 4 | 20% | 0-4 | The SME has a realistic path to reach, qualify for, and serve the prospect through a direct or partner route. |
    | Priority-cluster fit | 1 | 5% | 0-1 | The relevant site, project, or route is in Central Texas, Arizona, or New York, or clearly supports the SME's delivery model. |
    | Evidence strength | 2 | 10% | 0-2 | Two distinct, dated sources corroborate the match, including a project, operating, or route-specific signal. |

    A zero means no credible evidence or a clear mismatch. A score near the midpoint means the match is plausible but still inferred, indirect, older, or blocked by an unanswered question. Use the full scale: for example, assign 1 when only a weak signal exists, 2 when the case is plausible but unverified, 3 when support is material but incomplete, 4 when the evidence is strong with a minor gap, and the maximum only when the stated full-score condition is met. Capability fit is weighted highest because a current project is not useful if the SME cannot credibly solve its problem. Cluster fit is only a tie-breaker: it cannot compensate for missing timing, buyer route, or access.

    Store all six component scores in `score_breakdown`. Set `score` to their arithmetic sum and verify the sum exactly before writing. Do not assign a total independently. In the Markdown shortlist, display every finalist as `capability + timing + buyer path + access + cluster + evidence = total/20`, for example `5 + 4 + 2 + 2 + 1 + 2 = 16/20`.

15. **Classify finalists and order the work.** Use the total to order candidates within a class, then apply the gates and route maturity to determine the class.

    | Class | Normal score range | Required condition | SBF use |
    |---|---:|---|---|
    | `Priority` | 16-20 | All four decision conditions pass: specific need, credible capability proof, named buyer/partner route, and practical commitment or delivery path | Validate the named route now and decide whether to support an introduction or a defined market-entry action. |
    | `Strategic` | 13-15 | Strong fit, but longer-cycle, partner-led, or blocked by one clearly identified conversion requirement | Build the route, proof, or local-delivery plan before treating it as a near-term lead. |
    | `Watchlist` | 9-12 | Relevant, but timing, route, access, or evidence remains insufficient | Refresh the missing signal; do not allocate mission or outreach effort yet. |
    | Exclude or deprioritize | 0-8 | Weak fit or no credible route | Record the reason and stop work unless material new evidence appears. |

    A score cannot override a failed condition. If a candidate falls outside its normal range, keep it only when the leadership brief explicitly states why its immediate action is still justified; for example, a low-scoring `Watchlist` may merit one inexpensive route-validation question. Do not call a candidate `Priority` without current timing, a named route, and the evidence coverage in step 16.

16. **Enforce evidence coverage.**

    - `Priority`: timing, capability fit, and buyer-path or accessibility evidence; at least three evidence items with distinct normalized URLs; at least one project/timing-specific source.
    - `Strategic`: timing, capability fit, and buyer-path or risk evidence.
    - `Watchlist`: capability fit and risk/caveat evidence.

    A generic company page alone cannot support `Priority`.

17. **Recommend one SBF intervention per finalist.** Assign `Learn`, `Lead Generation`, `Land`, or `Localize` and one concrete action, such as a cluster briefing, procurement-route validation, warm introduction, mission meeting, local partner search, incentive navigation, or supplier-localization support.

18. **Prefer realistic routes.** Compare direct-owner outreach with EPC, contractor, OEM, channel, integrator, and ecosystem routes. Do not rank a megafab owner highly without a specific route to investigate. Apply Central Texas, Arizona, and New York as tie-breakers, not absolute rules.

19. **Filter aggressively.** Produce 5-8 finalists and never more than 10. Return fewer than five when fewer are credible. Group non-finalists by concise exclusion reason rather than listing every weak record.

20. **Build a one-page leadership brief.** Before the detailed shortlist, create `executive_summary` with:

    - one decision headline;
    - no more than four `action_now` items, each naming the prospect, why it matters now, and the next SBF action;
    - no more than three `strategic_routes` items for longer-cycle or partner-led options;
    - up to three portfolio-level critical unknowns.

    Treat `executive_summary.action_now` as the sole contract for immediate SBF actions. It may include a `Priority`, `Strategic`, or `Watchlist` finalist when an immediate learning, route-validation, or commercial action is justified; never derive it mechanically from classification. Match prospect names using a trimmed, case-insensitive key. Reject empty keys, normalized duplicates, and normalized collisions; do not silently merge distinct organizations. Every named organization must match exactly one `qualified_shortlist` prospect under that rule. Keep the rendered section concise enough to fit roughly one page. Do not repeat full evidence citations there; the detailed sections remain the audit trail.

21. **Make the SME-level SBF engagement recommendation.** Before writing the shortlist, answer the question an SME executive will see in the dashboard: **Should this company contact SBF now, and if so, which stage should it request?** Write one `sbf_engagement_recommendation` for the entire SME case. Do not derive it mechanically from the number of Priority prospects or from individual finalist stages.

    - `Contact SBF now`: the SME has a defined, evidenced need for SBF support now. Select the one primary stage that SBF should activate first: `Learn`, `Lead Generation`, `Land`, or `Localize`.
    - `Contact SBF after preparation`: SBF engagement is likely useful, but the SME must first close the stated readiness, proof, ownership, or delivery gap. Select the stage to request after that preparation is complete.
    - `Do not contact SBF yet`: the current evidence does not justify an SBF intervention. State the next internal preparation required and the condition that would make future engagement appropriate.

    Apply the stages consistently: `Learn` clarifies market relevance, readiness, or an opportunity hypothesis; `Lead Generation` validates buyer or partner routes and appropriate introductions; `Land` supports an initial U.S. customer, partner, or operating foothold; `Localize` supports customer-backed local delivery, partnerships, or operations. `specific_request_to_sbf` must name the support the SME should request, not promise that SBF can secure a meeting or introduction. For a `Do not contact SBF yet` decision, state that no request should be made now and direct the SME to the preparation list.

22. **Write canonical JSON first.** Use the Output Contract below. Set `source_prospect_directory` to the Skill 2 directory. When using a legacy input, use the legacy `source_prospect_discovery_path` field and its compatible schema version instead.

23. **Self-check and render.** Read `schema/qualified-prospects.schema.json` and validate the completed JSON with the JSON Schema capability available in the Codex runtime. Verify that `total_prospects_screened` equals the exact count established before the metadata screen and is at least the number of finalists. Verify that `sbf_engagement_recommendation` gives exactly one allowed contact decision and one allowed primary stage, has a concrete rationale and request, and lists only preparation that the SME can act on. Independently recompute every total from the six score components; verify that every finalist's `key_evidence` URLs are unique under the normalization rule in step 12; verify that every `action_now` and `strategic_routes` prospect matches exactly one `qualified_shortlist` prospect using the trimmed, case-insensitive key rule; reject normalized collisions; and compare `generated_at` with a fresh runtime-clock reading. Fix every mismatch before rendering Markdown. Do not create a validation script and do not ask the SME user to run technical checks.

24. **Confirm briefly.** Report the number of prospect records screened, full records read, candidates verified, finalists produced, and the SME-level SBF engagement recommendation. Point to the qualified Markdown and JSON. End with:
    - Export the executive dashboard with `$export-executive-brief`.
    - Revise the qualified shortlist.
    - Stop.

## Output Contract

```json
{
  "schema_version": "1.4.0",
  "schema_name": "qualified_prospects",
  "sme_name": "[SME name]",
  "safe_sme_name": "<safe_sme_name>",
  "generated_at": "[ISO 8601 timestamp]",
  "source_capability_profile_path": "output/<safe_sme_name>/01_capability_profile.md",
  "source_prospect_directory": "output/<safe_sme_name>/prospects",
  "total_prospects_screened": 18,
  "qualification_scope": "[scope used]",
  "qualification_logic": {
    "sme_capabilities_used": ["[Capability]"],
    "must_not_overclaim_caveats": ["[Caveat]"],
    "best_buyer_paths": ["[Route]"]
  },
  "sbf_engagement_recommendation": {
    "contact_sbf": "Contact SBF now",
    "primary_stage": "Lead Generation",
    "decision_rationale": "[Why the SME should seek this support now, based on the case-level evidence and gap]",
    "specific_request_to_sbf": "[The focused support the SME should ask SBF to provide]",
    "sme_preparation_required": ["[Preparation the SME must complete before or alongside the engagement]"]
  },
  "executive_summary": {
    "headline": "[Decision-oriented portfolio conclusion]",
    "action_now": [
      {
        "prospect": "[Company]",
        "why_now": "[Why action is timely]",
        "next_sbf_action": "[One immediate action]"
      }
    ],
    "strategic_routes": [
      {
        "prospect": "[Company]",
        "why_strategic": "[Why this matters but is not immediate]"
      }
    ],
    "critical_unknowns": ["[Portfolio-level unknown]"]
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
          "accessed_on": "2026-07-30",
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
          "accessed_on": "2026-07-30",
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
          "accessed_on": "2026-07-30",
          "url": "https://example.com/buyer-route-source",
          "supported_claim": "[Specific buyer or access route]",
          "evidence_excerpt": "[Short excerpt or tight paraphrase]"
        }
      ],
      "score_breakdown": {
        "capability_fit": 5,
        "timing_urgency": 3,
        "buyer_path_clarity": 3,
        "accessibility_sbf_route": 3,
        "priority_cluster_fit": 1,
        "evidence_strength": 2
      },
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

1. Your SBF next step: whether to contact SBF now, the one stage to request, the rationale, the specific request, and SME preparation
2. Executive decision brief
3. Inputs, total prospect records screened, and shortlisted finalists
4. Qualification logic, including the distinction between score and actionability class
5. Qualified shortlist table with the full component-score breakdown in this order: capability, timing, buyer path, access, cluster, evidence, then total `/20`
6. Structured evidence by finalist
7. Grouped exclusions
8. Recommended next actions

Do not introduce claims, scores, or recommendations absent from the self-checked JSON.

## Quality bar

- Read the capability profile and the Skill 2 prospect store.
- Screen every prospect through the index or, on fallback, its frontmatter.
- Record the exact full-pool count in `total_prospects_screened` and verify that it is at least the number of finalists.
- Read full files only for the focused 10-15 candidate set.
- Produce 5-8 finalists, never more than 10, without padding.
- Give every finalist a specific buyer path, one verification question, and one concrete SBF action.
- Show all six score components and verify that they sum to the total.
- Lead with a concise executive brief containing at most four immediate actions and three strategic routes.
- Give every newly opened evidence URL a runtime-derived access date.
- Meet classification-specific evidence coverage.
- Exclude named existing customers unless account expansion is requested.
- Separate direct evidence from inference.
- Treat the shortlist as company-level decision support, not SBF's complete multi-year strategy.
