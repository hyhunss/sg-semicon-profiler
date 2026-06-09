# 🇸🇬 SG Semicon US Expansion Assistant

This intelligent tool helps Singapore semiconductor and precision engineering SMEs (such as precision machining, cleanroom contractors, logistics, equipment services, and factory software vendors) discover and qualify commercial opportunities in the United States.

**💡 Our Promise:** You do not need to know anything about coding, databases, or complex spreadsheets. You only need to type three simple "chat commands" in the conversation box, following the step-by-step workflow.

---

## 🚀 Quick Start (The 3-Step Growth Pipeline)

### Step 1: Map Your Company's Capabilities

Type this command in the chat box (replace the bracket with your company's website or upload your corporate profile PDF/Word document):

```text
$map-sme-capability for [Your Website or Uploaded File Name]
```

* **What AI Does:** Automatically analyzes your business offerings and extracts your top 1-3 technical strengths, supporting evidence, and optimized target keywords.
* **What You Need to Do:** Once finished, an easy-to-read report ending in `_capabilities.md` will appear in your left folder tree. Double-click to open it and verify:

1. Are the identified technical strengths accurate?
2. Are unverified claims correctly marked as "Medium" or "Low" confidence?
3. Do the suggested prospecting keywords make business sense?

### Step 2: Discover US Prospects & Partners

If the capability report is accurate, you do not need to copy any file paths. Simply type the next command directly into the chat:

```text
$us-prospect-discovery
```

* **What AI Does:** Automatically retrieves your capability data in the background and performs multiple rounds of live US web searches to find matching buyers and projects.
* **What You Need to Do:** A broad "Market Prospect Pool" report ending in `_prospects.md` will be created in your left folder tree. Double-click it and verify:

1. Are the discovered US companies and facility projects relevant to your business?
2. Do the provided news and website links open correctly?
3. For massive accounts, did the AI list realistic indirect routes (like major EPC contractors or cleanroom builders) instead of just the factory owners?

### Step 3: Generate Your 20-Point Strategic Roadmap

If the broad prospect pool looks promising, type the final command into the chat:

```text
$qualify-us-prospects
```

* **What AI Does:** Applies a strict, practical 20-point scoring rubric (assessing technical fit, timing urgency, buyer-path clarity, and accessibility for a Singapore firm) to filter the broad list down to the most actionable 5-8 targets.
* **Your Final Output:** A final roadmap report ending in `_qualified_prospects.md` will be generated. You can print or export this document to back up your internal strategic meetings, share it with your SBF internationalization advisor, or use it as core supporting evidence when applying for Enterprise Singapore global expansion grants (such as the MRA or EDG grants).

---

## 💡 Frequently Asked Questions (For Business Users)

* **Q: I see both .json and .md files in my folder. Which one should I open?**
* **A:** Please **completely ignore the .json files**. Those are automated records used by the AI background engine to pass data securely between steps. As a business user, **only open the files ending in .md**. They open as cleanly formatted, easy-to-read text documents.

* **Q: What if I have data for multiple companies in my project folder?**
* **A:** If you are a senior consultant managing multiple accounts and the AI asks you to clarify which company you are targeting, you can override the automatic detection by typing the explicit file paths like this:

```text
$us-prospect-discovery with data/company_a_capabilities.json
$qualify-us-prospects with data/company_a_capabilities.json and data/company_a_prospects.json
```

* **Q: How do I correct the AI if a report contains an error?**
* **A:** Never restart the entire pipeline. Simply tell the AI what to fix in plain English, and it will update the documents together:

```text
Revise the capability profile: Add our ultra-precision cleanroom rigging capability to the list.
Revise the qualified shortlist: Move the third company to the excluded list because they are a direct competitor.
```
