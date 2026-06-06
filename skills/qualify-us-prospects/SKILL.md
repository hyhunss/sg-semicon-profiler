---
name: qualify-us-prospects
description: Third skill in the SG Semicon US Expansion workflow. Use only after the user has reviewed the us-prospect-discovery output. Given an SME capability profile and broad prospect-discovery file, filter the list into the most likely US prospects for deeper analysis or outreach. Stop after writing the qualified shortlist and tell the user what to review before using it.
---

# Skill: qualify-us-prospects

## Description
Read the outputs from both earlier skills and reduce a broad US prospect list into a smaller, qualified shortlist. This skill owns the heavy filtering, buyer-path reasoning, ranking, and tradeoff explanation. It should not restart broad discovery.

This is step 3 of a three-skill human-in-the-loop workflow:

```text
map-sme-capability -> user reviews capability profile -> us-prospect-discovery -> user reviews prospect pool -> qualify-us-prospects -> user reviews qualified shortlist
```

Assume the user has already reviewed both earlier files. This skill produces the final shortlist for human review; it should not restart the earlier stages.

## Inputs
* `capability_profile`: Path to the first skill output, usually `data/<safe_sme_name>_capabilities.md`.
* `prospect_discovery`: Path to the second skill output, usually `data/<safe_sme_name>_prospects.md`.
* Optional `shortlist_size`: Target number of qualified prospects. Default: 5-8. Maximum: 10.
* Optional `qualification_scope`: User-specified preference such as easiest first outreach, highest strategic value, near-term timing, specific US state, or specific buyer route.

## Output
* `data/<safe_sme_name>_qualified_prospects.md`: A compact Markdown shortlist of the most likely prospects, plus deprioritized/excluded prospects and targeted verification questions.

## Core Rule
Treat the second skill's output as a candidate pool, not as a qualified list. Do not confuse "large semiconductor project" with "qualified prospect":

```text
capabilities.md + prospects.md -> buyer-path qualification -> top 5-8 likely prospects
```

## Instructions
1. **Accept selected-prompt invocations:** If the user's message body is blank but selected text contains a prompt for this skill, treat the selected text as the user's instruction and proceed from it. Do not ask the user to paste it again.
2. **Read both inputs:** Use the capability profile to understand what the SME can credibly sell. Use the prospect-discovery file as the candidate pool. Do not evaluate prospects using capabilities that are not supported in the first file.
3. **Extract constraints from the capability profile:** Capture the SME name, 1-3 core capabilities, confidence labels, evidence caveats, and any terms the SME should avoid over-claiming.
4. **Extract candidates from the prospect-discovery file:** Capture prospect name, prospect type, route type if present, matched capability, buying trigger or context, evidence URL, `Why this showed up`, caveats, and any recommended next analysis. If the prospect file includes older fields such as score, confidence, or likely buyer path, treat them as helpful notes only, not final qualification.
5. **Remove weak candidates first:** Drop candidates that only match because they are generally large semiconductor companies, have no clear link to the SME capability, are likely competitors, or look unreachable without a realistic route.
6. **Do targeted verification only when needed:** If a top candidate's buyer path, timing, or evidence is unclear, run a narrow search for that candidate. Do not run broad discovery searches. Limit verification to likely top candidates or candidates where one fact would change the ranking.
7. **Source every new verification fact:** Any fact introduced during targeted verification must have a source URL in the final output. This includes named EPCs, contractors, construction managers, cleanroom square footage, groundbreaking dates, procurement routes, funding status, project phase, partnerships, or facility scope. If a new fact cannot be sourced, label it as an inference or leave it out.
8. **Prefer realistic go-to-market routes:** For Singapore SMEs, explicitly compare direct-owner outreach with channel/EPC/contractor/partner routes. Do not rank megafab owners highly unless the buyer path is specific enough to investigate.
9. **Apply the qualification test:** A qualified prospect should pass most of these questions:
   * Does the prospect need the SME's real capability?
   * Is there a concrete timing signal, such as new facility, ramp, modernization, tool install, pilot line, hiring, or supplier development?
   * Is the likely buyer path specific and plausible?
   * Is the prospect reachable for a Singapore SME through a direct buyer, partner, OEM, EPC, integrator, contractor, approved supplier, or public consortium route?
   * Is the evidence direct or a strong inference rather than a weak inference?
10. **Score with a practical 20-point rubric:**
   * Capability fit: 0-5
   * Timing / urgency: 0-4
   * Buyer-path clarity: 0-5
   * Accessibility for Singapore SME: 0-4
   * Evidence strength: 0-2
11. **Classify each finalist:** Use one of these labels:
   * `Priority`: strong fit, plausible buyer path, worth deeper analysis now.
   * `Watchlist`: good fit but timing, access, or evidence is not ready.
   * `Strategic`: large or important account, but likely long-cycle or partner-led.
12. **Filter aggressively:** Prefer 5-8 strong qualified prospects over a full list. Do not pad the shortlist. If fewer than 5 are credible, write fewer and explain why.
13. **Explain exclusions:** Group non-finalists into short reason categories such as weak buyer path, timing too early, too large/locked supplier base, indirect fit, likely competitor/channel target, or insufficient evidence.
14. **Write the file:** Save as `data/<safe_sme_name>_qualified_prospects.md`, using the same safe SME name as the input files.
15. **Confirm only:** Output a brief success message with the file path and number of qualified prospects. Tell the user to review the qualified shortlist before using it for deeper research or outreach. Do not give another workflow command. Do not print the full Markdown in chat unless the user asks.

## Confirmation Message Template

```text
Created: data/<safe_sme_name>_qualified_prospects.md with <N> qualified prospects.

Please review this shortlist before using it for deeper research or outreach.

Check:
1. Are the top prospects worth investigating next?
2. Is each buyer path specific enough to act on?
3. Are watchlist and exclusion decisions reasonable?
```

## Output Markdown Template

```markdown
# Qualified US Prospects: [Insert SME Name Here]

## 1. Inputs Used
* Capability profile: [path]
* Prospect discovery: [path]
* Qualification scope: [scope or "default"]

## 2. Qualification Logic
* SME capabilities used:
  * [Capability 1]
  * [Capability 2]
  * [Capability 3]
* Must-not-overclaim caveats:
  * [Caveat 1]
* Best buyer paths:
  * [Buyer path 1]
  * [Buyer path 2]

## 3. Qualified Shortlist
| Rank | Prospect | Classification | Best Buyer Path | Why This Prospect | Timing Signal | Evidence Strength | Key Evidence | Score | What To Verify Next |
|---:|---|---|---|---|---|---|---|---:|---|
| 1 | [Prospect] | [Priority/Watchlist/Strategic] | [Specific path] | [Concise reason] | [Trigger] | [Direct/Strong inference/Weak inference] | [Source URL(s), including URLs for any new verification facts] | [0-20] | [Next verification question] |

## 4. Deprioritized or Excluded
| Prospect / Group | Reason |
|---|---|
| [Prospect] | [Reason] |

## 5. Recommended Next Step
* [Concrete next action for the top 1-3 prospects]
```

## Quality Bar
* The skill must read both the capability profile and prospect-discovery file.
* Treat the prospect-discovery file as broad discovery, not as a final ranking.
* The final shortlist should usually contain 5-8 prospects and never more than 10.
* Every finalist must have a specific buyer path.
* Every finalist must include one targeted verification question.
* Every finalist must include source URL(s) for the timing signal and for any new verification facts introduced during qualification.
* Do not include a prospect only because it is a large semiconductor company.
* Use `Priority` only when the buyer path is specific and timing is actionable.
* Clearly separate evidence from inference.
