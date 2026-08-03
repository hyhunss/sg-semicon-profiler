---
name: export-executive-brief
description: Fourth skill in the SG Semicon US Expansion workflow. Use after qualify-us-prospects generates a 03_qualified_shortlist.json file in the selected SME output folder, or when the user asks to export a qualified shortlist. Read the canonical Step 3 JSON without changing its analysis, create an offline single-file HTML executive dashboard, and render a compact executive summary in the conversation.
---

# Skill: export-executive-brief

Transform canonical qualification JSON artifacts into a zero-friction, board-ready HTML dashboard for Singapore SME leadership and SBF executives. Keep data analysis strictly in Step 3 and presentation in Step 4.

```text
03_qualified_shortlist.json -> Offline HTML Dashboard (Print-to-PDF Ready) + Chat Summary
```

## Inputs

- Required: `output/<safe_sme_name>/03_qualified_shortlist.json`.
- Optional context: `output/<safe_sme_name>/01_capability_profile.md`.

## Outputs

- `output/<safe_sme_name>/04_executive_dashboard.html`.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve Input Matching.** Use a user-supplied Step 3 JSON path when given. Otherwise locate the most recently modified `output/*/03_qualified_shortlist.json`. If multiple files remain genuinely ambiguous, ask the user to choose. If none exists, notify the user: "No Step 3 qualified shortlist found. Please run `$qualify-us-prospects` first." and stop without creating outputs.

3. **Treat Step 3 JSON as canonical.** Read the complete file and require `sme_name`, `generated_at`, `executive_summary`, and `qualified_shortlist`. Treat `executive_summary.action_now` as the sole immediate-action list. Match every `action_now` and `strategic_routes` prospect to exactly one `qualified_shortlist` prospect using a trimmed, case-insensitive key. Reject empty keys, normalized duplicates, and normalized collisions; never silently merge distinct organizations. If a match is missing or ambiguous, identify it and stop so Step 3 can be corrected. Preserve all source names, classifications, roles, clusters, stages, actions, paths, timing signals, evidence descriptions, scores, and verification questions exactly. Do not browse, rescore, reinterpret, derive immediate actions from classification, or introduce new commercial claims. If required data is missing or malformed, identify the field and stop so Step 3 can be corrected.

4. **Use the stable dashboard template.** Use `assets/executive-dashboard-template.html` as the complete presentation layer. Do not redesign, restyle, or reconstruct the dashboard, and do not load the files under `references/` during a normal export. Require the template to contain exactly one `__QUALIFIED_SHORTLIST_JSON__` marker.

5. **Embed canonical JSON only.** Serialize the complete Step 3 object without changing field values or array order. Before embedding, replace `<`, `>`, `&`, U+2028, and U+2029 with their JSON Unicode escapes so the payload is safe inside the template's `application/json` script element. Replace the single marker with that escaped JSON and write the result to `output/<safe_sme_name>/04_executive_dashboard.html`. Do not modify any other template text.

6. **Check the rendered artifact contract.** Confirm that the marker is gone, the embedded JSON parses back to an object deeply equal to the Step 3 source, and the output contains no external dependency or network-request code. Confirm that the template's immediate-action KPI and cards use `executive_summary.action_now`, not classification. Do not add browser, screenshot, or visual-review steps.

## Stable template contract

The bundled template owns typography, colors, responsive layout, accessibility, progressive disclosure, score bars, evidence rendering, and print behavior. Its runtime validates Step 3 cross-field matches before rendering. Update the template asset itself when the dashboard design changes; never generate one-off HTML structure in an export run.

## Conversation handoff

After the HTML is written and checked:

1. Verify that the HTML contains no external dependency or network-request references and includes every required section.
2. Render a compact Markdown table for every `executive_summary.action_now` item in source order with prospect, classification, US cluster, recommended SBF stage, and `next_sbf_action`. If the array is empty, state that Step 3 recorded no immediate-action targets.
3. Provide a clickable absolute local path to `04_executive_dashboard.html`.
4. End with these choices:
   - Double-click `04_executive_dashboard.html` to open it in a browser.
   - Press `Ctrl+P` or `Cmd+P` in the browser to save it as a PDF report.
   - Stop.

## Quality bar

- Keep the HTML fully self-contained and offline-capable.
- Use `executive_summary.action_now` as the single source for the immediate-action KPI, dashboard cards, and conversation table; never rebuild that list from classification.
- Match all scores, claims, and URLs in the canonical JSON exactly; do not add, omit, or alter decision content.
- Keep the interface clean, responsive, printable, highly readable, and executive-ready.
- Keep Step 4 presentation-only. Return analytical corrections to Step 3 rather than silently repairing them here.
