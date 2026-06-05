---
name: map-sme-capability
description: Map the capabilities of a Singaporean semiconductor SME
---

# Skill: map-sme-capability

## Description
Ingests a Singapore semiconductor SME's profile via a website URL or uploaded document (PDF/Word), extracts core technical capabilities, strips away marketing fluff, injects US buyer-intent search operators, and saves the output as an easily editable Markdown file (.md) tailored for business users.

## Inputs
* `source_material`: A URL to the SME's website OR the file path/name of an uploaded PDF or Word document containing the company profile.
* `sme_name`: The name of the company (used for file naming).

## Instructions
1. **Ingest the Source:** Use available tools to either scrape the provided URL or read the text contents of the provided PDF/Word document. Extract all relevant text regarding the company's services and capabilities.
2. **Analyze and Strip Fluff:** Review the extracted text. Ignore generic marketing adjectives (e.g., "world-class," "premium quality," "customer-centric") and hyper-local geographical context (e.g., "Woodlands-based").
3. **Extract Noun + Verb Core:** Identify the exact, physical technical action the company performs (e.g., what do they make, machine, test, or assemble?).
4. **Bake in US Buyer Intent:** Do not generate generic capability phrases (which return competitors). Instead, combine the extracted capabilities with high-intent B2B search triggers, procurement indicators, and US geographic constraints (e.g., using `site:us`, `AND "become a vendor"`, `AND "expanding"`). Generate exactly 3 distinct, search-ready query combinations.
5. **Write to Markdown File:** Format the final analysis using the clean, human-readable Markdown Template provided below. Use your file system tools to write this text directly to a new file named `<sme_name>_capabilities.md` in the current working directory.
6. **Confirmation:** Once the file is created, output a brief success message confirming the file name and its location. Do not print the entire text block in the chat.

## Output Markdown Template (Content of the generated file)
```markdown
# Semiconductor Capability Profile: [Insert SME Name Here]

## 1. Core Technical Capability
* **Primary Offering:** [Clear, concise technical capability - Max 5 words]

## 2. Smart Keywords for US Prospecting
*Feel free to edit, add, or delete these search terms before passing them to the search engine. The current operators are optimized to find buyers rather than competitors:*
* **Search Query 1 (Procurement/Vendor):** [Capability Keywords] AND ("supplier directory" OR "become a vendor" OR "vendor registration") site:us
* **Search Query 2 (Expansion/Growth):** [Capability Keywords] AND ("new facility" OR "expanding production" OR "R&D hub") site:us
* **Search Query 3 (Target Sector Fit):** [Capability Keywords] AND "[Insert Target US Sector 1]" site:us

## 3. Target US Sectors
*Primary industries in the United States to look for prospects:*
1. [US Industry/Sector 1]
2. [US Industry/Sector 2]