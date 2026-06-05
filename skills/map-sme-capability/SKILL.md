---
name: map-sme-capability
description: Use when given a Singapore semiconductor SME website or profile document and asked to create a simple capability profile for US prospecting searches.
---

# Skill: map-sme-capability

## Description
Turn one Singapore semiconductor SME source into one editable Markdown capability profile for US prospecting searches.

## Inputs
* `source_material`: A URL to the SME's website OR the file path/name of an uploaded PDF or Word document containing the company profile.
* `sme_name`: The name of the company (used for file naming).

## Output
* `data/<safe_sme_name>_capabilities.md`: A short Markdown profile with evidence-backed capabilities, confidence labels, and US search queries.

## Instructions
1. **Ingest the source:** Read the provided website or document. For websites, check the home page plus obvious capability pages such as Services, Products, Solutions, Industries, Certifications, Quality, Equipment, and About.
2. **Extract evidence:** Capture 2-5 short source notes that support the capability claims. Prefer concrete nouns and verbs over adjectives. If evidence is thin, say so instead of guessing.
3. **Strip fluff:** Ignore generic marketing claims (e.g., "world-class," "premium quality," "customer-centric") and local details that do not describe buying relevance.
4. **Map capabilities:** Identify up to 3 core technical capabilities. Each should be a concise noun + verb phrase describing what the company physically makes, machines, tests, assembles, fabricates, coats, inspects, designs, or supplies.
5. **Add confidence:** Mark each capability High, Medium, or Low based on how directly the source supports it.
6. **Suggest US prospecting queries:** Create exactly 3 search-ready queries from the extracted capabilities. Use buyer-intent terms such as `"supplier"`, `"vendor registration"`, `"approved supplier"`, `"contract manufacturer"`, `"new facility"`, `"expanding production"`, and US terms such as `"United States"`, `"USA"`, or `"North America"`. Avoid `site:us` as the only US filter.
7. **Write the file:** Create `data/` if needed. Save the result as `data/<safe_sme_name>_capabilities.md`, using a lowercase filename with spaces replaced by underscores.
8. **Confirm only:** Output a brief success message with the file path. Do not print the full Markdown in chat.

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
*Feel free to edit, add, or delete these search terms before passing them to the search engine. The current operators are optimized to find buyers rather than competitors:*
* **Search Query 1 (Procurement/Vendor):** [Capability Keywords] AND ("supplier" OR "vendor registration" OR "approved supplier") AND ("United States" OR USA)
* **Search Query 2 (Expansion/Growth):** [Capability Keywords] AND ("new facility" OR "expanding production" OR "R&D hub") AND ("United States" OR "North America")
* **Search Query 3 (Buyer Need):** [Capability Keywords] AND ("outsourcing" OR "contract manufacturer" OR "supplier needed") AND ("United States" OR USA)
```
