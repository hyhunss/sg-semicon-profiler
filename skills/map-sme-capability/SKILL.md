---
name: map-sme-capability
description: Front-door and first skill in the SG Semicon US Expansion workflow. Use when given a Singapore semiconductor SME website or company profile document and asked to start US expansion research or create a capability profile. Briefly explain the three-step human-in-the-loop workflow, then create the capability profile. Stop after writing the profile, tell the user what to review, and give explicit Continue, Revise, or Stop choices.
---

# Skill: map-sme-capability

## Description
Turn one Singapore semiconductor SME source into one editable Markdown capability profile for US prospecting.

This is the front door and step 1 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects
```

When this skill is used to start the workflow, briefly orient the user before doing the work:

1. First, this skill creates a capability profile from the SME source.
2. The user reviews that profile.
3. If it looks right, `us-prospect-discovery` finds a broad pool of possible US prospects.
4. The user reviews that broad prospect pool.
5. If it looks useful, `qualify-us-prospects` filters the strongest prospects.

Do not continue into prospect discovery automatically. The user should check this skill's output before invoking the next skill. Make that easy by ending with explicit Continue, Revise, or Stop choices.

## Inputs
* `source_material`: A URL to the SME's website or the file path/name of an uploaded PDF or Word document containing the company profile.
* `sme_name`: The name of the company (used for file naming).

## Output
* `data/<safe_sme_name>_capabilities.json`: The canonical structured capability profile. It must conform to `schema/capability-profile.schema.json`.
* `data/<safe_sme_name>_capabilities.md`: A short human-readable Markdown profile rendered from the validated JSON.
* `data/_latest_workflow.json`: Optional convenience state file for the latest workflow.
* `data/_latest_workflow.md`: Optional human-readable convenience state file rendered from the workflow JSON.

## Data Contract
The JSON file is the source of truth for downstream skills. Markdown is only for human review.

Use `schema_version: "1.0.0"` and `schema_name: "capability_profile"` in the capability JSON. Use `schema_name: "workflow_state"` in the convenience workflow state JSON.

Before confirming completion:

1. Write the capability JSON.
2. Validate or carefully self-check it against `schema/capability-profile.schema.json`.
3. Fix any schema mismatch before continuing.
4. Render the Markdown review file from the validated JSON.
5. Write `data/_latest_workflow.json` and self-check that the expected workflow fields are present.
6. Render `data/_latest_workflow.md` from the workflow JSON.

## Instructions
1. **Accept selected-prompt invocations:** If the user's message body is blank but selected text contains a prompt for this skill, treat the selected text as the user's instruction and proceed from it. Do not ask the user to paste it again.
2. **Orient first-time users:** If the user is starting the workflow or sounds unsure, briefly explain the three review-gated steps before beginning. Keep this short and then proceed; do not make the user invoke a separate guide skill.
3. **Ask for missing source material:** If the user has not provided an SME website, uploaded company profile, or other source material, stop and ask for it. Do not create a profile from memory or guess the company.
4. **Handle revision requests:** If the user asks to revise this step's output, read the current capability JSON first. If only Markdown exists from an older run, read the Markdown as a fallback and rebuild the JSON. Apply the requested edits, then reconstruct the entire JSON object perfectly according to `schema/capability-profile.schema.json` before touching Markdown. Never truncate the JSON output. Rewrite the Markdown only by mirroring the validated JSON changes. Rewrite the same JSON and Markdown files unless the user asks for a new file, update both workflow state files, and confirm briefly. Do not rerun the whole workflow unless the user explicitly asks.
5. **Ingest the source:** Read the provided website or document. For websites, check the home page plus obvious capability pages such as Services, Products, Solutions, Industries, Certifications, Quality, Equipment, and About.
6. **Extract evidence:** Capture 2-5 short source notes that support the capability claims. Prefer semiconductor-specific pages and terms over generic company pages. Do not use office locations or company age as capability evidence. If evidence is thin, say so instead of guessing.
7. **Strip fluff:** Ignore generic marketing claims (e.g., "world-class," "premium quality," "customer-centric") and local details that do not describe buying relevance.
8. **Map capabilities:** Identify up to 3 core technical capabilities. Use precise semiconductor operating terms when supported, such as WIP tracking, SECS/GEM, MES implementation, SPC, recipe management, OEE, yield monitoring, advanced packaging, wafer inspection, or production ramp. For software SMEs, describe the manufacturing workflow they enable. For equipment logistics SMEs, prefer tool-specific phrases such as fab tool installation, photolithography tool relocation, metrology tool relocation, AMHS installation, cleanroom rigging, and semiconductor tool transport.
9. **Add confidence:** Mark each capability High, Medium, or Low based on how directly the source supports it.
10. **Write smart keyword seeds:** These are suggested starting points for the next interactive Google Search skill, not final searches that must be used exactly. Create exactly 5 short keyword seeds. Each seed should combine one exact capability term, one likely buyer pain or timing signal, and optional US/company context. Prefer phrases a buyer or press release would actually use. For equipment logistics SMEs, use the specific tool or fab action, not generic logistics. Avoid generic phrases that are far from the SME's real capability.
11. **Critique and improve the seeds:** Before writing the file, review each seed and ask: Is it close to the SME's real capability? Could it help the next skill find buyers after live Google iteration? Is it too broad, too crowded, or likely to only find competitors? Revise weak seeds, but do not over-optimize; the next skill will adapt them during interactive search.
12. **Write the canonical JSON file:** Create `data/` if needed. Save the result as `data/<safe_sme_name>_capabilities.json`, using a lowercase filename with spaces replaced by underscores.
13. **Validate the capability JSON:** Validate or carefully self-check against `schema/capability-profile.schema.json`. The JSON must have exactly 1-3 capabilities, 2-5 evidence notes, exactly 5 smart keyword seeds, valid confidence enum values, and no extra top-level fields.
14. **Render the Markdown review file:** Save `data/<safe_sme_name>_capabilities.md` from the validated JSON. Do not add claims in Markdown that are absent from the JSON.
15. **Write convenience workflow state:** Also write or update `data/_latest_workflow.json` with SME name, current step completed, capability JSON path, blank prospects and qualified JSON fields, and next recommended command `$us-prospect-discovery`. Self-check that the expected workflow fields are present, then render `data/_latest_workflow.md`. These files are only a convenience; do not require them for later steps.
16. **Confirm only:** Output a business-friendly success message with the readable review report path, the AI background record path, what to review, the exact next command, how to revise, and how to stop. Do not print the full file contents in chat. The confirmation message must end with the three explicit choices in the template below.

## Opening Explanation Template

Use this short explanation when the user is starting the workflow or seems unsure:

```text
I will handle this as a three-step review-gated workflow:
1. Create a capability profile from the SME source.
2. You review that profile.
3. Then the next skill discovers possible US prospects.
4. You review that broad prospect pool.
5. Then the final skill qualifies the strongest prospects.

I will start with step 1 now.
```

## Confirmation Message Template

```text
Created successfully:
- Corporate Capability Profile (AI Record): data/<safe_sme_name>_capabilities.json
- Human-Readable Review Report: data/<safe_sme_name>_capabilities.md

Please double-click to open 'data/<safe_sme_name>_capabilities.md' from the left folder tree to review the profile.

Next Steps:
A. If accurate, type the next command to discover US prospects:
   $us-prospect-discovery

B. To revise, type:
   Revise the capability profile: [describe your changes]

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
  "current_step_completed": "Step 1 - Map SME Capability",
  "capability_json": "data/<safe_sme_name>_capabilities.json",
  "prospects_json": null,
  "qualified_json": null,
  "next_recommended_command": "$us-prospect-discovery"
}
```

Render this human-readable companion as `data/_latest_workflow.md`:

```markdown
# Latest SG Semicon Expansion Workflow

* SME name: [SME Name]
* Current step completed: Step 1 - Map SME Capability
* Capability JSON: data/<safe_sme_name>_capabilities.json
* Capability Markdown: data/<safe_sme_name>_capabilities.md
* Prospects JSON:
* Qualified JSON:
* Next recommended command: $us-prospect-discovery
```

## Output JSON Template

Write this canonical file first as `data/<safe_sme_name>_capabilities.json`:

```json
{
  "schema_version": "1.0.0",
  "schema_name": "capability_profile",
  "sme_name": "[Insert SME Name Here]",
  "safe_sme_name": "<safe_sme_name>",
  "source_references": [
    "[URL or file path]"
  ],
  "generated_at": "[ISO 8601 timestamp]",
  "core_capabilities": [
    {
      "capability": "[Capability phrase]",
      "confidence": "High"
    }
  ],
  "evidence_notes": [
    {
      "note": "[Short source-backed note]",
      "source": "[URL or file path]"
    },
    {
      "note": "[Second short source-backed note]",
      "source": "[URL or file path]"
    }
  ],
  "smart_keyword_seeds": [
    {
      "label": "Procurement",
      "keyword_seed": "[Specific Capability] + [Buyer Pain] + RFP / vendor selection / approved supplier + United States"
    },
    {
      "label": "Production Ramp",
      "keyword_seed": "[Specific Capability] + production ramp / capacity expansion / pilot line + semiconductor USA"
    },
    {
      "label": "Tier 1 Collaboration",
      "keyword_seed": "[Specific Capability] + partnership / collaboration + major semiconductor company + startup / emerging company"
    },
    {
      "label": "Funding/New Facility",
      "keyword_seed": "[Specific Capability] + CHIPS Act / funding / new facility / new fab + semiconductor USA"
    },
    {
      "label": "Buyer Pain",
      "keyword_seed": "[Specific Capability] + [Relevant Buyer Pain] + United States / North America"
    }
  ],
  "caveats": [
    "[Evidence gap or must-not-overclaim note]"
  ]
}
```

## Output Markdown Template

Render this human-readable file from the validated JSON as `data/<safe_sme_name>_capabilities.md`:

```markdown
# Semiconductor Capability Profile: [Insert SME Name Here]

## 1. Core Technical Capabilities
1. **[Capability phrase]** - Confidence: [High/Medium/Low]
2. **[Capability phrase]** - Confidence: [High/Medium/Low]
3. **[Capability phrase]** - Confidence: [High/Medium/Low]

## 2. Evidence Notes
* [Short source-backed note, with page/file/URL if available]
* [Short source-backed note, with page/file/URL if available]

## 3. Caveats
* [Evidence gap or must-not-overclaim note]

## 4. Smart Keywords for US Prospecting
*These are keyword seeds for the next interactive Google Search skill. They do not need to be used exactly; they should guide the first searches and be adapted based on live results:*
* **Keyword Seed 1 (Procurement):** [Specific Capability] + [Buyer Pain] + RFP / vendor selection / approved supplier + United States
* **Keyword Seed 2 (Production Ramp):** [Specific Capability] + production ramp / capacity expansion / pilot line + semiconductor USA
* **Keyword Seed 3 (Tier 1 Collaboration):** [Specific Capability] + partnership / collaboration + major semiconductor company + startup / emerging company
* **Keyword Seed 4 (Funding/New Facility):** [Specific Capability] + CHIPS Act / funding / new facility / new fab + semiconductor USA
* **Keyword Seed 5 (Buyer Pain):** [Specific Capability] + [Relevant Buyer Pain] + United States / North America
```
