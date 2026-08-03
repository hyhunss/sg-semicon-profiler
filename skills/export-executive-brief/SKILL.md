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

2. **Resolve the input.** Use a user-supplied Step 3 JSON path when given. Otherwise locate the most recently modified `output/*/03_qualified_shortlist.json`. If multiple files remain genuinely ambiguous, ask the user to choose. If none exists, tell the user to run `$qualify-us-prospects` first and stop without creating outputs.

3. **Treat Step 3 JSON as canonical.** Read the complete file and require `sme_name`, `generated_at`, `executive_summary`, and `qualified_shortlist`. Preserve all names, classifications, roles, clusters, stages, actions, paths, timing signals, evidence descriptions, scores, and verification questions exactly. Do not browse, rescore, reinterpret, or introduce new commercial claims. If required data is missing or malformed, identify the field and stop so Step 3 can be corrected.

4. **Load visualization foundations.** Read these bundled reference files completely before rendering: `references/theory-and-principles.md`, `references/task-abstraction-and-chart-selection.md`, `references/layout-hierarchy-and-self-explanatory-ux.md`, `references/interaction-models-and-progressive-disclosure.md`, `references/perception-color-and-encoding.md`, `references/mobile-first-responsive-visualization.md`, `references/editorial-infographic-system.md`, `references/storytelling-annotation-and-critique.md`, and `references/embedded-visualization-self-use.md`. Apply progressive disclosure, semantic color encoding, visual hierarchy, direct labeling, meaningful annotation, accessibility, responsive layout, embedded-layer QA, and `@media print` rules within this skill.

5. **Generate the standalone HTML dashboard.** Write one complete, highly polished HTML5 document to `04_executive_dashboard.html`. Embed all CSS and light inline interaction JavaScript directly in the file. Escape all JSON-derived text before inserting it into HTML.
   - **Zero external dependencies:** Do not use CDN scripts, external web fonts, framework libraries, network requests, or remote images. The file must work completely offline when opened directly in Chrome, Edge, or Safari.

## HTML design

### Typography and base setup

- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Page background `#F8FAFC`; body text `#0F172A`.
- Centered container with `max-width: 1140px` and responsive padding.

### Semantic color palette

- Primary navy: `#0F172A` and `#1E293B`; accent blue: `#0072FF`.
- Priority badge: background `#ECFDF5`, text `#047857`, border `#A7F3D0`.
- Strategic badge: background `#EFF6FF`, text `#1D4ED8`, border `#BFDBFE`.
- Watchlist badge: background `#F1F5F9`, text `#475569`, border `#CBD5E1`.

Use semantic headings, accessible color contrast, visible keyboard focus, responsive tables or cards, and no decorative clutter.

### Required layout sections

1. **Header banner**
   - Title: `SG Semicon US Expansion Briefing`.
   - Display `sme_name` and `generated_at` exactly as stored.
   - Feature `executive_summary.headline` prominently.

2. **KPI metrics row**
   - Total Shortlisted Targets: length of `qualified_shortlist`.
   - Immediate Action Targets: count whose `classification` is exactly `Priority`.
   - Key US Clusters Covered: count of unique, non-empty `us_cluster` values.

3. **Executive action board — Action Now**
   - Show every `Priority` candidate in source order in emerald-accented cards.
   - Display prospect, US cluster, best buyer path, recommended SBF stage, and recommended SBF action.
   - If none exists, state that the canonical shortlist contains no Priority candidates.

4. **Full shortlist score visualizer**
   - Show every candidate in source order on one aligned `0–20` total-score scale using pure inline CSS progress bars.
   - Print the exact total score and classification beside each mark.
   - Keep classification visually distinct from score and state that classification reflects actionability rather than a mechanical score band.

5. **Strategic and long-term routes**
   - Show `Strategic` and `Watchlist` candidates in source order.
   - Use native `<details><summary>` disclosures for score breakdown, key evidence, and the next verification question.
   - Show every score component and total exactly as stored. For each evidence item, preserve its source title, supported claim, evidence excerpt, source date, accessed date, and URL. Make valid URLs clickable without fetching them.

6. **Critical unknowns and SBF next steps**
   - Render `executive_summary.critical_unknowns` as concise bullets.
   - Render `recommended_next_steps` as a separate action list.
   - Preserve source order and wording. If either array is empty, state that none were recorded in Step 3.

## Print and PDF behavior

Include `@media print` styles that:

- switch to a white background and high-contrast dark text;
- remove shadows, decorative borders, hover effects, and controls without print value;
- expand `<details>` content for printing;
- prevent cards, table rows, and evidence blocks from splitting where practical;
- avoid horizontal scrollbars and clipped content;
- preserve sensible multi-page spacing and headings.

Do not claim that browser PDF pagination will be identical across operating systems or browsers.

## Conversation handoff

After the HTML is written and checked:

1. Verify that the HTML contains no external dependency or network-request references and includes every required section.
2. Render a compact Markdown table for Priority candidates with prospect, US cluster, recommended SBF stage, and next SBF action. If there are no Priority candidates, state that plainly.
3. Provide a clickable absolute local path to `04_executive_dashboard.html`.
4. End with these choices:
   - Double-click `04_executive_dashboard.html` to open it in a browser.
   - Press `Ctrl+P` or `Cmd+P` in the browser to save it as a PDF report.
   - Stop.

## Quality bar

- Keep the HTML fully self-contained and offline-capable.
- Match all scores, claims, and URLs in the canonical JSON exactly; do not add, omit, or alter decision content.
- Keep the interface clean, responsive, printable, highly readable, and executive-ready.
- Keep Step 4 presentation-only. Return analytical corrections to Step 3 rather than silently repairing them here.
