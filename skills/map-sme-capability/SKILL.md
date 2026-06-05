---
name: map-sme-capability
description: Use when given a Singapore semiconductor SME website or company profile document and asked to create a simple capability profile for US prospecting.
---

# Skill: map-sme-capability

## Description
Turn one Singapore semiconductor SME source into one editable Markdown capability profile for US prospecting.

## Inputs
* `source_material`: A URL to the SME's website or the file path/name of an uploaded PDF or Word document containing the company profile.
* `sme_name`: The name of the company (used for file naming).

## Output
* `data/<safe_sme_name>_capabilities.md`: A short Markdown profile with evidence-backed capabilities, confidence labels, and smart keyword seeds for the next interactive Google Search skill.

## Instructions
1. **Ingest the source:** Read the provided website or document. For websites, check the home page plus obvious capability pages such as Services, Products, Solutions, Industries, Certifications, Quality, Equipment, and About.
2. **Extract evidence:** Capture 2-5 short source notes that support the capability claims. Prefer semiconductor-specific pages and terms over generic company pages. Do not use office locations or company age as capability evidence. If evidence is thin, say so instead of guessing.
3. **Strip fluff:** Ignore generic marketing claims (e.g., "world-class," "premium quality," "customer-centric") and local details that do not describe buying relevance.
4. **Map capabilities:** Identify up to 3 core technical capabilities. Use precise semiconductor operating terms when supported, such as WIP tracking, SECS/GEM, MES implementation, SPC, recipe management, OEE, yield monitoring, advanced packaging, wafer inspection, or production ramp. For software SMEs, describe the manufacturing workflow they enable. For equipment logistics SMEs, prefer tool-specific phrases such as fab tool installation, photolithography tool relocation, metrology tool relocation, AMHS installation, cleanroom rigging, and semiconductor tool transport.
5. **Add confidence:** Mark each capability High, Medium, or Low based on how directly the source supports it.
6. **Write smart keyword seeds:** These are suggested starting points for the next interactive Google Search skill, not final searches that must be used exactly. Create exactly 5 short keyword seeds. Each seed should combine one exact capability term, one likely buyer pain or timing signal, and optional US/company context. Prefer phrases a buyer or press release would actually use. For equipment logistics SMEs, use the specific tool or fab action, not generic logistics. Avoid generic phrases that are far from the SME's real capability.
7. **Critique and improve the seeds:** Before writing the file, review each seed and ask: Is it close to the SME's real capability? Could it help the next skill find buyers after live Google iteration? Is it too broad, too crowded, or likely to only find competitors? Revise weak seeds, but do not over-optimize; the next skill will adapt them during interactive search.
8. **Write the file:** Create `data/` if needed. Save the result as `data/<safe_sme_name>_capabilities.md`, using a lowercase filename with spaces replaced by underscores.
9. **Confirm only:** Output a brief success message with the file path. Do not print the full Markdown in chat.

## Output Markdown Template (Content of the generated file)

```markdown
# Semiconductor Capability Profile: [Insert SME Name Here]

## 1. Core Technical Capabilities
1. **[Capability phrase]** - Confidence: [High/Medium/Low]
2. **[Capability phrase]** - Confidence: [High/Medium/Low]
3. **[Capability phrase]** - Confidence: [High/Medium/Low]

## 2. Evidence Notes
* [Short source-backed note, with page/file/URL if available]
* [Short source-backed note, with page/file/URL if available]

## 3. Smart Keywords for US Prospecting
*These are keyword seeds for the next interactive Google Search skill. They do not need to be used exactly; they should guide the first searches and be adapted based on live results:*
* **Keyword Seed 1 (Procurement):** [Specific Capability] + [Buyer Pain] + RFP / vendor selection / approved supplier + United States
* **Keyword Seed 2 (Production Ramp):** [Specific Capability] + production ramp / capacity expansion / pilot line + semiconductor USA
* **Keyword Seed 3 (Tier 1 Collaboration):** [Specific Capability] + partnership / collaboration + major semiconductor company + startup / emerging company
* **Keyword Seed 4 (Funding/New Facility):** [Specific Capability] + CHIPS Act / funding / new facility / new fab + semiconductor USA
* **Keyword Seed 5 (Buyer Pain):** [Specific Capability] + [Relevant Buyer Pain] + United States / North America
```
