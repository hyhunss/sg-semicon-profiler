---
name: us-prospect-discovery
description: Second skill in the SG Semicon US Expansion workflow. Use after the user reviews a map-sme-capability output to immediately run repeatable, adaptive US prospect-search cycles, then resume later runs from a persistent search log. Create or update one Markdown record per possible commercial prospect, route-to-market partner, or ecosystem connector while preventing duplicates. Default to Central Texas, Arizona, and New York unless the user specifies another scope, and leave deep qualification to Skill 3.
---

# Skill: us-prospect-discovery

Build a persistent library of possible US prospects through short, repeatable search cycles. Discover broadly and filter only obvious noise. Do not score or deeply qualify candidates.

This is step 2 of a review-gated workflow:

```text
map-sme-capability -> review -> repeated discovery cycles -> review -> qualify-us-prospects
```

## Inputs

- Capability profile from Skill 1: `output/<safe_sme_name>/01_capability_profile.md`.
- Optional `input/existing_customers.md`.
- Optional user changes to capabilities, buyer routes, timing signals, or geography.

## Canonical outputs

```text
output/<safe_sme_name>/
├── 01_capability_profile.md
├── 02_search_log.md
├── 02_prospects_index.tsv
└── prospects/
    ├── <prospect_id>.md
    └── ...
```

- Treat each prospect Markdown file as the canonical record for one buying organization, route partner, project, or connector.
- Treat `02_search_log.md` as the canonical record of approved scope, exact queries, results, reflections, and next search direction.
- Treat `02_prospects_index.tsv` as a disposable speed index derived from the prospect Markdown files. It is never evidence and never the canonical record.
- Do not create or maintain a consolidated prospect JSON or prospect report.
- Preserve old `output/<safe_sme_name>_prospects.json` and `.md` files as legacy artifacts; do not overwrite or delete them.

## Core loop

```text
load state -> find an uncovered query direction -> search -> upsert prospects
-> reflect -> mutate the next query -> repeat -> stop and report
```

Each normal invocation is one search cycle:

- Run at most five live searches.
- Stop early after three consecutive searches produce no new prospect files.
- Process and save useful candidates immediately after every search.
- Let later invocations resume from the accumulated files and search log.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve the active SME.** If no capability path is supplied, choose the most recently modified `output/*/01_capability_profile.md`. Ask only when multiple SMEs remain genuinely ambiguous.

3. **Read the capability and customer context.** Extract the SME name, supported capabilities, limitations, and search directions from the Markdown profile. Derive `safe_sme_name` from its parent folder. Read `input/existing_customers.md` when present and matching. Exclude named existing customers and obvious group aliases unless the user requests account expansion.

4. **Locate and audit persistent state.** Use:

   - `output/<safe_sme_name>/02_search_log.md`
   - `output/<safe_sme_name>/02_prospects_index.tsv`
   - `output/<safe_sme_name>/prospects/`

   Use a valid index for the fast identity scan. If the index is absent, malformed, or does not match the prospect filenames, rebuild it silently from all prospect frontmatter before searching. Open likely matching Markdown records whenever a domain, name, or alias may duplicate a candidate. An absent directory on the first run is valid.

5. **Start immediately on normal invocation.** Invoking this skill, or selecting Continue after Skill 1, authorizes the first search cycle using the supported capability profile and default geography. Do not add another confirmation checkpoint merely because no search log exists. Show the Scope Revision Template and stop only when the user explicitly asks to preview or change scope, when the active SME or capability profile is ambiguous, or when a proposed discovery term would materially extend beyond the supported capabilities. Existing search logs resume automatically unless the user requests a scope change.

6. **Initialize the search dimensions.** Construct queries from:

   ```text
   supported capability x buyer or route x timing signal x geography
   ```

   Use precise semiconductor process, equipment, packaging, software, facility, logistics, and service language. Default geography is Central Texas, Arizona, and New York. Deprioritize but do not prohibit California. Use Other US when fit or timing is materially stronger.

7. **Choose an uncovered direction.** Read `02_search_log.md` before every cycle. Do not repeat an exact query unless the user requests a freshness rerun. Prefer combinations or result types not adequately covered. Include direct buyers and realistic access routes such as EPC/EPCM firms, cleanroom contractors, systems integrators, equipment OEMs, approved-supplier routes, EDOs, chambers, associations, universities, and consortia.

8. **Search and adapt one query at a time.** Run a live web search. Prefer primary or high-quality current sources: company pages, press releases, government and CHIPS releases, procurement pages, contractor project pages, university or consortium pages, EDO pages, and credible trade press. After each query, assess:

   - whether it found buyers, route partners, connectors, competitors, or noise;
   - which capability, buyer, timing, or geography term helped;
   - which result type remains underexplored.

   Change only one or two query dimensions for the next search so the reason for the mutation remains clear.

   Never run `site:linkedin.com` searches or target private social networks. Do not spend a search on login-walled or blocked pages; use open, indexed sources instead.

   When ordinary company searches produce weak or repetitive results, change to one public-signal angle:

   - Hiring: `"[capability]" ("job opening" OR careers) "[state]"`; prefer first-party career pages and public Greenhouse or Lever postings.
   - Government and awards: `"[capability]" ("CHIPS Act award" OR subcontractor) "[state]"`; prioritize CHIPS.gov, SAM.gov, and state or regional EDO releases.
   - Contractors and projects: `"[capability]" ("general contractor" OR EPC) semiconductor "[state]"`; prioritize EPC/GC portfolios, expansion announcements, and tool-install releases.

   Treat a job posting only as evidence of the stated role, location, function, and date. Do not claim that it proves construction, procurement demand, or an expansion unless the posting or a separate source says so. Likewise, do not infer a contractor or tier relationship from an award notice unless the source names it.

   If the user asks to run one exact query, run only that query and stop the cycle after saving and logging its results.

9. **Apply lightweight filtering.** Keep a candidate only when there is a visible reason it could buy, enable, or connect the SME's supported capability. Exclude clear competitors, recruiters, generic consultants without project access, unrelated organizations, non-US entities without a clear US route, named existing customers, and results supported only by company size.

10. **Build one candidate record.** For each plausible candidate, prepare a complete record matching the Prospect Record Contract below. Use the normalized official company domain as `prospect_id` when available: lowercase it and remove the protocol, path, trailing slash, and leading `www.`. If there is no official domain, use a stable lowercase hyphenated organization or project name. Include the exact query that found the candidate and at least one evidence URL.

11. **Run the identity check before every write.** Compare the candidate against every existing prospect record in this order:

    1. Same normalized official domain: treat as the same record.
    2. Same normalized company name or a known alias, with one or both domains missing: treat as the same record.
    3. Same or very similar name but different official domains: pause and inspect; never merge automatically.
    4. Clear parent and subsidiary relationship: keep separate only when they are distinct buying organizations; add the relationship as a caveat.
    5. No match: create a new record.

    Normalize names only for comparison by lowercasing, removing punctuation, and ignoring common endings such as `Inc`, `Corp`, `LLC`, `Ltd`, and `Company`. Do not remove meaningful words such as `Semiconductor`, `Technology`, or a geographic division name.

12. **Create or update one Markdown file.**

    - New identity: create `output/<safe_sme_name>/prospects/<prospect_id>.md`.
    - Existing identity: rewrite the same file with the merged record.
    - Preserve `first_seen`; update `last_seen`.
    - Merge aliases, matched capabilities, buying triggers, queries, and caveats without repeated entries.
    - Merge evidence by normalized URL; do not repeat the same URL.
    - Prefer the most specific current company name, website, role, cluster, route, fit explanation, and evidence claim.
    - Rewrite both the complete JSON frontmatter and the human-readable body. Never append evidence only to the body.

13. **Log every exact query and scope change.** Before searching, compare the planned query with every query already in `02_search_log.md`. Do not rerun an exact query unless the user explicitly requests a freshness rerun. After processing the query, create the log on the first search or append one row using the Search Log Contract below. Record the exact query, counts of new, updated, and ignored results, and the reflection that explains the next mutation. When the user confirms a materially revised scope, append a dated `Scope update` section before the next query row; do not replace the earlier scope. Treat the most recent confirmed scope section as active on later runs.

14. **Rebuild the speed index after each search.** Re-enumerate all prospect Markdown files and replace `02_prospects_index.tsv` from their JSON frontmatter. Never append blindly. Use the exact header and rules in the Index Contract below. If rebuilding fails, continue using the Markdown records and report the index issue; never lose or rewrite a valid prospect record to satisfy the index.

15. **Protect diversity.** If results concentrate on one category, deliberately change the next buyer or route dimension:

    - fab owners -> EPC/EPCM, tool-install, cleanroom, integrator, or OEM routes;
    - partners -> end-customer projects, OSATs, pilot lines, or funded facilities;
    - giant incumbents -> smaller OSATs, compound-semiconductor firms, pilot lines, startups, or regional projects;
    - one cluster -> another priority cluster.
    - repetitive company pages -> hiring, government/award, or contractor/project signals.

16. **Stop the cycle.** Stop after five searches or three consecutive searches with no new prospect files. Do not stop merely because the library has reached 20 prospects. Do not pad the library.

17. **Audit the completed store.** Re-enumerate all prospect files and self-check:

    - one file per distinct identity;
    - no repeated normalized domain;
    - no repeated normalized company name or alias without an explained separate buying organization;
    - valid JSON frontmatter and controlled values;
    - matching SME name and safe name;
    - at least one exact query and evidence URL per record;
    - no claims in the body that are absent from the frontmatter;
    - a valid index with one row per prospect file and no extra rows.

    Fix every issue before completion.

18. **Confirm briefly.** Report searches run, new files, updated files, total prospect records, search-log path, index path, and prospect-directory path. End with:

    - Continue discovery with another cycle.
    - Revise the search scope.
    - Run `$qualify-us-prospects`.
    - Stop.

## Scope Revision Template

```text
Please review the requested search-scope change.

Supported capabilities:
- [term]

Additional discovery terms (not verified capabilities):
- [term or None]

Buyer and route types:
- [type]

Timing signals:
- [signal]

Geography:
- [cluster]

Reply with:
A. Continue with this scope
B. Add: [term, route, signal, or geography]
C. Remove: [item]
D. Replace: [old] with [new]
```

## Prospect Record Contract

Use JSON inside the Markdown frontmatter so later skill runs can compare records consistently:

```markdown
---
{
  "schema_version": "1.0.0",
  "schema_name": "prospect_record",
  "sme_name": "Example SME",
  "safe_sme_name": "example_sme",
  "prospect_id": "example.com",
  "company": "Example Company",
  "website": "https://www.example.com",
  "aliases": ["Example"],
  "prospect_type": "EPC",
  "engagement_role": "Route-to-market partner",
  "us_cluster": "Arizona",
  "route_type": "Channel-EPC",
  "matched_capabilities": ["Tool installation"],
  "buying_triggers": ["New fab construction"],
  "why_this_may_fit": "The company manages semiconductor construction packages that may require specialist tool-install support.",
  "first_seen": "2026-07-28",
  "last_seen": "2026-07-28",
  "discovered_by_queries": ["semiconductor tool installation EPC Arizona"],
  "evidence": [
    {
      "title": "Example project page",
      "url": "https://www.example.com/project",
      "supported_claim": "The company manages an Arizona semiconductor project."
    }
  ],
  "caveats": ["The subcontractor qualification route is not yet public."]
}
---
```

Required controlled values:

- `engagement_role`: `Commercial prospect`, `Route-to-market partner`, or `Ecosystem connector`
- `us_cluster`: `Central Texas`, `Arizona`, `New York`, `California`, or `Other US`
- `route_type`: `Direct owner`, `Channel-EPC`, `Partner ecosystem`, or `Watchlist`

Render the human-readable body from the structured frontmatter. Do not add claims to the body that are absent from the structured record.

Use this body structure:

```markdown
# [Company]

* Website: [URL or Not found]
* Role: [engagement role]
* US cluster: [cluster]
* Route: [route type]
* First seen: [date]
* Last seen: [date]

## Why this may fit
[Concise explanation]

## Matched capabilities
- [Capability]

## Buying triggers or context
- [Trigger]

## Found through
- `[Exact query]`

## Evidence
- [Source title](URL): [Supported claim]

## Caveats
- [Caveat or None recorded]
```

## Search Log Contract

```markdown
# US Prospect Search Log: [SME name]

* Capability profile: output/<safe_sme_name>/01_capability_profile.md
* Approved capabilities: [terms]
* Additional discovery terms: [terms or None]
* Buyer and route types: [types]
* Timing signals: [signals]
* Geography: [clusters]

| Timestamp | Exact query | New | Updated | Ignored | Reflection |
|---|---|---:|---:|---:|---|
| [ISO timestamp] | `[exact query]` | [N] | [N] | [N] | [What worked, what was noisy, and why the next query changed.] |
```

For a later scope change, append:

```markdown
## Scope update: [ISO timestamp]

* Approved capabilities: [terms]
* Additional discovery terms: [terms or None]
* Buyer and route types: [types]
* Timing signals: [signals]
* Geography: [clusters]
```

## Index Contract

Write UTF-8 tab-separated text with this exact header:

```tsv
prospect_id	company	engagement_role	us_cluster	route_type	matched_capability	last_seen
```

Write one row per prospect Markdown file, sorted by `prospect_id`. Join multiple matched capabilities with `; `. Replace tabs and line breaks inside values with spaces. Require unique `prospect_id` values and an exact match between index IDs and prospect filenames without `.md`.

## Quality bar

- Every prospect has exactly one canonical Markdown file and at least one evidence URL.
- Every exact query is recorded in the search log.
- Repeated appearances update an existing record instead of creating another file.
- Parent and subsidiary records remain separate only when they are distinct buying organizations.
- Current projects, funding, facilities, hiring, and cluster programs come from live sources.
- AI- or user-added search terms are not presented as verified SME capabilities.
- Named existing customers and obvious group aliases are excluded unless account expansion is requested.
- Discovery remains broad and unscored; Skill 3 owns qualification.
