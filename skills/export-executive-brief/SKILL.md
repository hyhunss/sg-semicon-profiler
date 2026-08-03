---
name: export-executive-brief
description: Fourth skill in the SG Semicon US Expansion workflow. Use after qualify-us-prospects generates a 03_qualified_shortlist.json file in the selected SME output folder, or when the user asks to export a qualified shortlist. Read the canonical Step 3 JSON without changing its analysis, create an offline single-file HTML executive dashboard and an Excel-compatible CSV, and render a compact executive summary in the conversation.
---

# Skill: export-executive-brief

Transform the canonical qualification JSON into zero-friction executive deliverables for Singapore SME leadership and SBF executives. Keep data analysis in Step 3 and presentation in Step 4.

```text
03_qualified_shortlist.json -> Excel-ready CSV + offline HTML dashboard + chat summary
```

## Inputs

- Required: `output/<safe_sme_name>/03_qualified_shortlist.json`.
- Optional context: `output/<safe_sme_name>/01_capability_profile.md`.

## Outputs

- `output/<safe_sme_name>/04_executive_dashboard.html`.
- `output/<safe_sme_name>/03_qualified_shortlist.csv`.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve the input.** Use a user-supplied Step 3 JSON path when given. Otherwise locate the most recently modified `output/*/03_qualified_shortlist.json`. If multiple files remain genuinely ambiguous, ask the user to choose. If none exists, tell the user to run `$qualify-us-prospects` first and stop without creating outputs.

3. **Treat Step 3 JSON as canonical.** Read the complete file and require `sme_name`, `generated_at`, `executive_summary`, and `qualified_shortlist`. Preserve all names, classifications, roles, clusters, stages, actions, paths, timing signals, evidence descriptions, scores, and verification questions exactly. Do not browse, rescore, reinterpret, or introduce new commercial claims. If required data is missing or malformed, identify the field and stop so Step 3 can be corrected.

4. **Load the OpenAI visualization foundations.** Before designing or writing the HTML, read these bundled upstream reference files completely: `references/theory-and-principles.md`, `references/task-abstraction-and-chart-selection.md`, `references/layout-hierarchy-and-self-explanatory-ux.md`, `references/interaction-models-and-progressive-disclosure.md`, `references/perception-color-and-encoding.md`, `references/mobile-first-responsive-visualization.md`, `references/editorial-infographic-system.md`, `references/storytelling-annotation-and-critique.md`, and `references/embedded-visualization-self-use.md`. Apply their task-first chart selection, insight-led titles, visual hierarchy, direct labeling, meaningful annotation, progressive disclosure, perceptual encoding, accessibility, responsive layout, and embedded-layer QA within this skill's fixed offline-output contract.

5. **Generate the Excel-compatible CSV.** Write `03_qualified_shortlist.csv` as UTF-8 with a byte order mark (`U+FEFF`) as the first character. Emit one row per `qualified_shortlist` item in source order and use these exact headers:

   ```text
   Prospect,Classification,Engagement Role,US Cluster,Total Score,Recommended SBF Stage,Recommended SBF Action,Best Buyer Path,Timing Signal,Evidence Strength,What to Verify Next
   ```

   Map the headers to `prospect`, `classification`, `engagement_role`, `us_cluster`, `score`, `recommended_sbf_stage`, `recommended_sbf_action`, `best_buyer_path`, `timing_signal`, `evidence_strength`, and `what_to_verify_next`. Follow RFC 4180-style escaping: wrap a field in double quotes when it contains a comma, quote, carriage return, or newline, and double every embedded quote. Use CRLF row endings for broad Excel compatibility. Do not flatten `key_evidence` or `score_breakdown` into extra columns.

6. **Generate the standalone HTML dashboard.** Write one complete HTML5 document to `04_executive_dashboard.html`. Embed all CSS and any necessary JavaScript in the file. Do not use external fonts, CDN assets, frameworks, network requests, or remote images. Escape all JSON-derived text before inserting it into HTML. The file must work offline when opened directly in Chrome, Edge, or Safari.

## HTML design

Use an executive, highly legible layout:

- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Page background `#F8FAFC`; body text `#0F172A`.
- Centered container with `max-width: 1140px` and responsive padding.
- Primary navy: `#0F172A` and `#1E293B`; accent blue: `#0072FF`.
- Priority badge: background `#DCFCE7`, text `#15803D`, border `#86EFAC`.
- Strategic badge: background `#DBEAFE`, text `#1D4ED8`, border `#93C5FD`.
- Watchlist badge: background `#F1F5F9`, text `#475569`, border `#CBD5E1`.
- Use semantic headings, accessible color contrast, visible keyboard focus, responsive tables or cards, and no decorative clutter.

Include these sections in order:

1. **Header banner**
   - Title: `SG Semicon US Expansion Briefing`.
   - Display `sme_name` and `generated_at` exactly as stored.
   - Feature `executive_summary.headline` in a prominent callout.

2. **KPI cards**
   - Total Shortlisted Targets: length of `qualified_shortlist`.
   - Immediate Action Targets: count whose `classification` is exactly `Priority`.
   - Key US Clusters Covered: count of unique, non-empty `us_cluster` values.

3. **Action Now**
   - Show every `Priority` candidate in source order.
   - Display prospect, cluster, best buyer path, recommended SBF stage, and recommended SBF action.
   - If none exists, state that the canonical shortlist contains no Priority candidates.

4. **Full Shortlist Comparison**
   - Show every candidate in source order on one aligned `0–20` total-score scale.
   - Print the exact total score and classification beside each mark.
   - Keep classification visually distinct from score and state that classification reflects actionability rather than a mechanical score band.

5. **Strategic & Long-Term Routes**
   - Show `Strategic` and `Watchlist` candidates in source order.
   - Use `<details><summary>` disclosures for score breakdown, key evidence, and the next verification question.
   - Show every score component and total exactly as stored. For each evidence item, preserve its source title, supported claim, evidence excerpt, source date, accessed date, and URL. Make valid URLs clickable without fetching them.

6. **Critical Unknowns & SBF Next Steps**
   - Render `executive_summary.critical_unknowns` as concise bullets.
   - Render `recommended_next_steps` as a separate action list.
   - Preserve source order and wording. If either array is empty, say that none were recorded in Step 3.

## Print and PDF behavior

Include `@media print` styles that:

- switch to a white background and dark text;
- remove shadows and unnecessary decoration;
- hide controls that have no print value;
- prevent cards, table rows, and evidence blocks from splitting where practical;
- expand `<details>` content for printing;
- avoid horizontal scrollbars and clipped content;
- preserve sensible multi-page spacing and headings.

Do not claim that browser PDF pagination will be identical across operating systems or browsers.

## Conversation handoff

After both files are written and checked:

1. Verify that the CSV begins with UTF-8 BOM bytes `EF BB BF`, has the exact header order, and has one data row per shortlisted prospect.
2. Verify that the HTML contains no external dependency or network-request references and includes every required section.
3. Render a compact Markdown table in the conversation for Priority candidates with prospect, US cluster, recommended SBF stage, and next SBF action. If there are no Priority candidates, state that plainly.
4. Provide clickable absolute local paths to both generated files.
5. End with these choices:
   - Double-click `04_executive_dashboard.html` to open it in a browser or print it to PDF.
   - Open `03_qualified_shortlist.csv` in Microsoft Excel.
   - Stop.

## Quality bar

- Keep the HTML fully self-contained and offline-capable.
- Include the UTF-8 BOM and correct CSV quoting.
- Match the canonical JSON exactly; do not add, omit, or alter decision content.
- Keep the dashboard clean, responsive, printable, and executive-ready.
- Keep Step 4 presentation-only. Return analytical corrections to Step 3 rather than silently repairing them here.
