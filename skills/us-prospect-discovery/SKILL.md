---
name: us-prospect-discovery
description: Second skill in the SG Semicon US Expansion workflow. Use after the user reviews a map-sme-capability output to run repeatable, adaptive US prospect-search cycles and build a persistent, high-recall prospect library. Create or update one OKF v0.2 Markdown concept per capability-relevant candidate while preventing duplicates, and leave deep qualification to Skill 3.
---

# Skill: us-prospect-discovery

Build a rich, persistent library of plausible US prospects through short, repeatable search cycles. Search broadly and save capability-relevant candidates while filtering obvious noise. Do not score or deeply qualify candidates.

**Division of labor:** Skill 2 is the high-recall stage: collect as many plausibly relevant US prospects as the evidence supports. Skill 3 is the high-precision stage: perform strict qualification, 20-point scoring, and filtering. Do not apply Skill 3's strict qualification during discovery. If an organization has demonstrable capability relevance, save it even when current timing or a direct buyer route is unverified; tag each missing signal as `To be verified in Step 3 / human review`.

## OKF authority

`references/OKF_SPEC_v0.2.md` is the authoritative specification for every prospect record. When uncertain about an OKF field, source attribution, trust, lifecycle, cross-link, reserved filename, or conformance rule, read the relevant section before writing or revising a record. If the question is how to apply a compliant prospect-record field or body shape, then also read `references/skill-2-onn-wah-tech-prospect-okf-sample.md`. Follow the local specification over remembered conventions, examples, or guesses. Do not invent OKF requirements or fields.

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
├── index.md
├── 01_capability_profile.md
├── 02_search_log.md
├── 02_prospects_index.tsv
└── prospects/
    ├── index.md
    ├── <prospect_id>.md
    └── ...
```

- Treat each prospect Markdown file as the canonical OKF v0.2 concept for one buying organization, route partner, project, or connector.
- Treat the root `index.md` and `prospects/index.md` as the progressive-disclosure path into the capability profile and prospect library. They are navigation only, never evidence.
- Treat `02_search_log.md` as the canonical record of approved scope, exact queries, results, reflections, and next search direction.
- Treat `02_prospects_index.tsv` as a disposable speed index derived from the prospect Markdown files. It is never evidence and never the canonical record.
- Do not create or maintain a consolidated prospect JSON or prospect report.

## Core loop

```text
load state -> find an uncovered query direction -> search -> upsert prospects
-> update in-memory state -> reflect -> mutate the next query -> repeat
-> rebuild derived indexes once -> audit -> stop and report
```

Each normal invocation is one search cycle:

- Run at most five live searches.
- Stop early after three consecutive searches produce no new prospect files.
- Evaluate every result after each search; save any candidate with direct capability relevance while filtering obvious noise.
- Let later invocations resume from the accumulated files and search log.
- When broad uncovered directions span independent regions or signal types, automatically delegate bounded, read-only searches to parallel subagents, then consolidate their results in the primary thread.

## Instructions

1. **Accept selected-prompt invocations.** If the message body is blank but selected text contains an instruction for this skill, use the selected text.

2. **Resolve the active SME.** If no capability path is supplied, choose the most recently modified `output/*/01_capability_profile.md`. Ask only when multiple SMEs remain genuinely ambiguous.

3. **Read the capability and customer context.** Extract the SME name, supported capabilities, limitations, and search directions from the Markdown profile. Derive `safe_sme_name` from its parent folder. Read `input/existing_customers.md` when present and matching. Exclude named existing customers and obvious group aliases unless the user requests account expansion.

4. **Locate and audit persistent state.** Use:

   - `output/<safe_sme_name>/02_search_log.md`
   - `output/<safe_sme_name>/02_prospects_index.tsv`
   - `output/<safe_sme_name>/prospects/`

   Use a valid TSV for the fast identity scan. If the TSV or either OKF navigation index is absent, malformed, or does not match the prospect filenames, rebuild it silently from all prospect frontmatter before searching. Open likely matching Markdown records whenever a domain, name, or alias may duplicate a candidate. An absent directory on the first run is valid.

5. **Start immediately on normal invocation.** Invoking this skill, or selecting Continue after Skill 1, authorizes the first search cycle using the supported capability profile and default geography. Do not add another confirmation checkpoint merely because no search log exists. Show the Scope Revision Template and stop only when the user explicitly asks to preview or change scope, when the active SME or capability profile is ambiguous, or when a proposed discovery term would materially extend beyond the supported capabilities. Existing search logs resume automatically unless the user requests a scope change.

6. **Initialize the search dimensions.** Construct queries from:

   ```text
   supported capability x buyer or route x geography x optional timing signal
   ```

   Lead with capability and buyer or route relevance. Add a timing signal when it improves precision, but do not make timing a mandatory query dimension. Use precise semiconductor process, equipment, packaging, software, facility, logistics, and service language. Default geography is Central Texas, Arizona, and New York. Deprioritize but do not prohibit California. Use Other US when fit or timing is materially stronger.

   In every normal cycle, allow at least one query to begin slightly broader with a supported capability plus general US contractor, OEM, integrator, supplier, or buyer terms before adding a strict state or cluster filter. Use this nationwide pass to surface organizations that operate across Central Texas, Arizona, New York, or other US clusters even when their headquarters or source page is elsewhere. It still counts toward the same five-search limit.

7. **Choose an uncovered direction.** Read `02_search_log.md` before every cycle. Do not repeat an exact query unless the user requests a freshness rerun. Prefer combinations or result types not adequately covered. Include direct buyers and realistic access routes such as EPC/EPCM firms, cleanroom contractors, systems integrators, equipment OEMs, approved-supplier routes, EDOs, chambers, associations, universities, and consortia.

8. **Search and adapt one query at a time.** Run a live web search. Prefer primary or high-quality current sources: company pages, press releases, government and CHIPS releases, procurement pages, contractor project pages, university or consortium pages, EDO pages, and credible trade press. Use open tech-discussion APIs such as Hacker News via Algolia only as secondary discovery or caveat signals. After each query, assess:

   - whether it found buyers, route partners, connectors, competitors, or noise;
   - which capability, buyer, timing, or geography term helped;
   - which result type remains underexplored.

   Change only one or two query dimensions for the next search so the reason for the mutation remains clear.

   Never run `site:linkedin.com` searches or target private social networks. Do not spend a search on login-walled or blocked pages; use open, indexed sources instead.

   When ordinary company searches produce weak or repetitive results, change to one public-signal angle:

   - Hiring: `"[capability]" ("job opening" OR careers) "[state]"`; prefer first-party career pages and public Greenhouse or Lever postings.
   - Government and awards: `"[capability]" ("CHIPS Act award" OR subcontractor) "[state]"`; prioritize CHIPS.gov, SAM.gov, and state or regional EDO releases.
   - Contractors and projects: `"[capability]" ("general contractor" OR EPC) semiconductor "[state]"`; prioritize EPC/GC portfolios, expansion announcements, and tool-install releases.
   - Tech community: fetch the public Hacker News Algolia API directly, with URL-encoded query values:
     - Stories: `https://hn.algolia.com/api/v1/search?query=[capability]+[state]&tags=story`
     - Recent stories: `https://hn.algolia.com/api/v1/search_by_date?query=[capability]+[state]&tags=story&numericFilters=created_at_i%3E[TIMESTAMP_6_MONTHS_AGO]`
     - Recent comments: `https://hn.algolia.com/api/v1/search_by_date?query=%22[exact_company_or_project_phrase]%22+[specific_cluster]&tags=comment&numericFilters=created_at_i%3E[TIMESTAMP_6_MONTHS_AGO]`

   - **Federal awards:** Treat each API request as one live search and retain the exact endpoint, non-secret filters, request date, and response URL or award identifier in the search log and prospect evidence. Start with the two target NAICS codes—`334413` (semiconductor and related device manufacturing) and `236210` (industrial building construction)—then filter by an approved cluster location. These are discovery signals, not proof of a current MES, procurement, subcontract, or buyer route.

     **USASpending template (POST):** Before use, check the live official API documentation for the currently supported Award Search path and filter schema. Use `https://api.usaspending.gov/api/v2/search/awards/` when available; if the documented current equivalent is different, use that endpoint and log the actual path. Keep the query bounded by date and cluster.

     ```http
     POST https://api.usaspending.gov/api/v2/search/awards/
     Content-Type: application/json

     {
       "filters": {
         "time_period": [{"start_date": "[YYYY-MM-DD]", "end_date": "[YYYY-MM-DD]"}],
         "naics_codes": ["334413", "236210"],
         "place_of_performance_locations": [{"country": "USA", "state": "[AZ|TX|NY]"}]
       },
       "fields": ["Award ID", "Recipient Name", "Description", "Start Date", "End Date", "Award Amount", "Awarding Agency", "Place of Performance"],
       "page": 1,
       "limit": 100,
       "sort": "Award Amount",
       "order": "desc"
     }
     ```

     **SAM.gov Contract Awards template (GET):** Use the current public Contract Awards API only with an authorized SAM.gov API key. Never place a key in a prospect file, search log, source URL, or conversation output. Query `https://api.sam.gov/contract-awards/v1/search` with `naicsCode=334413~236210`, a bounded approved/modified-date range, `placeOfPerformStateCode=[AZ|TX|NY]`, `limit=100`, and `includeSections=contractId,awardDetails,awardeeData`; add the API key only at runtime. Example request shape:

     ```text
     GET https://api.sam.gov/contract-awards/v1/search?naicsCode=334413~236210&placeOfPerformStateCode=AZ&approvedDate=[MM/DD/YYYY,MM/DD/YYYY]&limit=100&includeSections=contractId,awardDetails,awardeeData&api_key=[runtime secret]
     ```

   - **Municipal permits:** Use public permit/project portals to surface facility construction, hazardous-chemical, electrical, cleanroom, utility, or equipment/tool-hookup signals. Examples: `site:mygovernmentonline.org Taylor TX semiconductor permit`, `site:mygovernmentonline.org Taylor TX electrical permit`, and the City of Phoenix Development Services permit/project search with terms such as `semiconductor`, `fab`, `hazardous`, `electrical`, `tool install`, or a known project name. A permit proves only the stated record, location, work type, status, and date; corroborate company identity and commercial relevance with a first-party, government, contractor, or credible trade source before admitting a candidate. Do not access login-gated records, bypass portal controls, or infer a procurement need from permit language alone.

   Treat a job posting only as evidence of the stated role, location, function, and date. Do not claim that it proves construction, procurement demand, or an expansion unless the posting or a separate source says so. Likewise, do not infer a contractor or tier relationship from an award notice unless the source names it.

   Use an exact company or project phrase and a specific cluster for comment searches; never query a generic term such as `fab` alone. Use at most one Hacker News API query per cycle unless it produces a named, relevant company, project, or route worth following. Do not create a prospect from an HN mention alone; corroborate the identity and commercial relevance with an official company, project, government, contractor, or credible trade source.

   If the user asks to run one exact query, run only that query and stop the cycle after saving and logging its results.

   #### Parallel execution via subagents

   When at least two uncovered search directions are independent, automatically delegate them to parallel subagents. Prefer read-heavy discovery across:

   - Arizona fab, advanced-packaging, tool-install, contractor, and public-project signals.
   - Central Texas CHIPS awards, fab or supplier expansions, contractor projects, and first-party hiring signals.
   - New York or stronger Other US ecosystem, university, supplier, EPC, and regional-project signals.
   - At most one Hacker News Algolia query using an exact company or project phrase and a specific cluster.

   Keep the cycle within the same five-search total, including every delegated query. Spawn only the workers needed for distinct uncovered directions; do not repeat logged exact queries merely to fill a parallel batch.

   Give each subagent a bounded, read-only assignment containing the approved capabilities, target cluster or signal channel, one exact query, existing prospect identities, and the high-recall admission and exclusion rules. Require a compact structured return containing the exact query, candidate name and official domain, possible role and cluster, evidence URLs with supported claims, any timing or access signals found, caveats, ignored-result reasons, and a short reflection. Subagents must not write or edit the prospect store.

   Wait for the delegated searches, then have the primary agent:

   1. Validate the returned sources and evidence boundaries.
   2. Process each completed query separately in a deterministic order.
   3. Run the identity check and upsert canonical `prospects/<prospect_id>.md` records.
   4. Log every exact query with its own counts and reflection.
   5. Update the primary thread's in-memory identity and index state from the canonical Markdown upserts; do not rebuild derived index files during the batch.
   6. Use any remaining search slots adaptively after reviewing the combined results.

   If multi-agent tools are unavailable, the thread limit is reached, or delegation fails, continue the same uncovered searches sequentially without asking the user to configure anything. The primary agent remains responsible for all writes, deduplication, logging, validation, and final reporting.

9. **Apply high-recall candidate admission.** Create a canonical prospect Markdown record for any candidate organization that satisfies `Capability relevance`: a named process, facility, service, equipment category, or program has a direct relationship to one of the SME's supported capabilities. The evidence must support a plausible demand-side use or route-side role—for example, the candidate buys, uses, integrates, specifies, distributes, or can connect the capability to semiconductor work. A company merely advertising the same capability is normally a competitor, not a prospect. Generic semiconductor activity or company size alone does not qualify.

   Do not require current timing or a direct access route for initial admission, and do not discard a capability-relevant organization merely because it would not yet pass Skill 3's qualification or scoring threshold. Capture supported commercial context in the sourced body explanation. When timing or access is missing, add a concise caveat for Step 3 / human review and still save the record.

   **Multi-Entity List Rule:** Classify the source before setting the extraction limit.

   - From a high-density, verified industry or public source—such as an official SEMI directory, a published CHIPS Act applicant/award list, or a state EDO roster—extract up to ten (normally five to ten) directly capability-relevant organizations into separate prospect Markdown records. The list must identify the organization and a semiconductor-relevant role, location, facility, program, or route; retain the list as supporting evidence and add an official organization source whenever identity or the claimed role is unclear.
   - From an unverified general-web article, contractor round-up, blog, or broad listicle, retain the existing limit of up to two or three directly relevant organizations. Corroborate each with an official, government, contractor, or credible-trade source before admission when the article does not itself establish identity and capability relevance.

   Admit every extracted organization independently under the same capability-relevance rule. Do not convert every name on a broad list into a prospect, treat list membership as a buyer route, or relax deduplication, timestamp, OKF frontmatter, source-footnote, or index requirements because the source is high-density.

   Exclude only obvious noise: direct competitors, recruiters, generic non-semiconductor entities, generic consultants without a semiconductor route, non-US entities without a clear US operational route, named existing customers, and results supported solely by general company size. Count excluded results in the search log and explain material exclusion patterns in the reflection.

   Across repeated cycles, aim to build a rich library of 15-30+ distinct records spanning buyers, route partners, and ecosystem connectors so SME team members can browse candidates directly and Skill 3 has a broad pool to screen. Do not pad a cycle with irrelevant records merely to reach that range.

10. **Build one candidate record.** For each admitted candidate, prepare a minimal record matching the Prospect Record Contract below. Use the normalized official company domain as the filename when available: lowercase it and remove the protocol, path, trailing slash, and leading `www.`. If there is no official domain, use a stable lowercase hyphenated organization or project name. Include at least one source URL, then state the supported claim in the sourced body.

    Use `Watchlist` as `route_type` when the candidate is capability-relevant but no buyer or access route is yet visible. Do not invent timing or access text merely to fill a field; preserve the missing signal in `caveats` for Step 3 / human review. The exact query belongs only in `02_search_log.md`, not in a prospect record.

    For a lead found through the Hacker News Algolia API, use the official project or company domain as the filename, never `hn.algolia.com` or `news.ycombinator.com`. Preserve the specific discussion URL as `https://news.ycombinator.com/item?id=[story_id_or_objectID]` and the original linked article URL when available. Limit the sourced body claim to what the thread actually states and retain any uncertainty as a caveat.

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
    - Merge matched capabilities, sources, and caveats without repeated entries.
    - Merge sources by normalized URL; do not repeat the same URL.
    - Prefer the most specific current company name, role, cluster, route, and evidence prose.
    - Rewrite both the complete YAML frontmatter and the human-readable body. Never append evidence only to the body.
    - Use only the fields in the minimal Prospect Record Contract. Do not create `verified` unless a real human or deterministic process completed that verification.

13. **Use runtime-derived time values.** Immediately before writing each prospect record, search-log row, or scope update, read the current local time from the Codex runtime or system clock. Use its exact ISO 8601 timestamp for `generated.at` and search-log timestamps. Never estimate, interpolate, round, sequence, or manually generate a time value. Read the clock again for each later write. This is an internal Codex operation: never create a helper script or ask the SME user to run a command. If the runtime clock is unavailable, omit the write and report the clock failure instead of inventing a timestamp.

14. **Log every exact query and scope change.** Before searching, compare the planned query with every query already in `02_search_log.md`. Do not rerun an exact query unless the user explicitly requests a freshness rerun. After processing the query, create the log on the first search or append one row using the Search Log Contract below. Record the exact query, counts of new, updated, and ignored results, and the reflection that explains the next mutation. When the user confirms a materially revised scope, append a runtime-dated `Scope update` section before the next query row; do not replace the earlier scope. Treat the most recent confirmed scope section as active on later runs.

15. **Defer derived-index rebuilding to the end of the search cycle.** During the one-to-five-search batch, maintain an in-memory identity and index list as each canonical prospect Markdown file is created or updated. Use that state for later identity checks, but do not rewrite `02_prospects_index.tsv`, `prospects/index.md`, or the prospect-library entry in the root `index.md` after individual searches.

    After the fifth search, or immediately after the early-stop condition, run one rebuild pass: re-enumerate all canonical prospect Markdown files and replace all three derived indexes from disk. Never append blindly. Use the exact contracts below. If that final rebuild fails, retain the valid canonical Markdown records, report the index issue, and do not claim the derived indexes were refreshed.

16. **Protect diversity.** If results concentrate on one category, deliberately change the next buyer or route dimension:

    - fab owners -> EPC/EPCM, tool-install, cleanroom, integrator, or OEM routes;
    - partners -> end-customer projects, OSATs, pilot lines, or funded facilities;
    - giant incumbents -> smaller OSATs, compound-semiconductor firms, pilot lines, startups, or regional projects;
    - one cluster -> another priority cluster.
    - repetitive company pages -> hiring, government/award, contractor/project, or one HN ecosystem signal.

17. **Stop the cycle.** Stop after five searches or three consecutive searches with no new prospect files. Do not stop merely because the library has reached 20 prospects. Do not pad the library.

18. **Audit the completed store.** After the single end-of-cycle rebuild pass, re-enumerate all prospect files and self-check:

    - one file per distinct identity;
    - no repeated normalized domain;
    - no repeated normalized company name or alias without an explained separate buying organization;
    - one parseable YAML frontmatter block beginning at the file start, with a non-empty OKF `type` and controlled prospect values;
    - at least one source URL and supported claim per record;
    - only the fields in the minimal Prospect Record Contract;
    - records without visible timing or an access route include the corresponding Step 3 / human-review caveat;
    - no search-log or scope timestamp is later than a fresh runtime-clock reading;
    - every body footnote label maps to exactly one `sources[].id`, and every material body claim has a matching source footnote;
    - a valid TSV speed index with one row per prospect file and no extra rows;
    - a valid `prospects/index.md` with one link per prospect file and no extra entries;
    - a root `index.md` that links both `01_capability_profile.md` and `prospects/`.

    Fix every issue before completion.

19. **Confirm briefly.** Report searches run, new files, updated files, total prospect records, search-log path, index path, and prospect-directory path. End with:

    - Continue discovery with another cycle.
    - Revise the search scope.
    - **Run `$qualify-us-prospects` (required to re-score the library and reflect newly discovered prospects in your shortlist and dashboard).**
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

Each `prospects/<filename>.md` file is an OKF concept. Use one YAML frontmatter block at the file start. The filename supplies the stable identity; frontmatter keeps only the route, capability match, source links, and caveats needed for a fast screen. The search log preserves query history; the Markdown body preserves all business intelligence and evidence.

```markdown
---
type: US Market-Entry Prospect
description: "Potential Arizona route-to-market partner for the SME's tool-installation capability."
resource: "https://www.example.com"
generated:
  by: codex/gpt-5
  at: "[runtime-derived ISO 8601 timestamp]"
company: "Example Company"
engagement_role: Route-to-market partner
us_cluster: Arizona
route_type: Channel-EPC
matched_capabilities: [Tool installation]
sources:
  - id: example-project
    resource: "https://www.example.com/project"
caveats:
  - "Current timing: To be verified in Step 3 / human review"
  - "Access route: To be verified in Step 3 / human review"
---
```

For every source, create one stable lowercase-hyphenated source ID such as `example-project` and preserve it when the same URL is carried forward. Keep source entries to `id` and `resource`; write source names and claims only in the body beside their keyed footnotes. Every cited `[^source-id]` must have one matching Markdown definition, `[^source-id]: [Source title]`, at the end of the body. Set `generated.by` to the actual Codex agent/model identifier in the actor convention, for example `codex/gpt-5`, never a skill name or invented version. Set `generated.at` from the runtime immediately before the final write. Do not add optional metadata unless the user asks for it.

Required controlled values:

- `engagement_role`: `Commercial prospect`, `Route-to-market partner`, or `Ecosystem connector`
- `us_cluster`: `Central Texas`, `Arizona`, `New York`, `California`, or `Other US`
- `route_type`: `Direct owner`, `Channel-EPC`, `Partner ecosystem`, or `Watchlist`
- Use a missing timing or access route only as a caveat; neither requires a metadata field.

Render the human-readable body from the structured frontmatter and researched evidence. Every material body claim must carry a footnote that maps to a `sources[].id`; do not add unsupported claims.

Use this body structure:

```markdown
# [Company]

* Role: [engagement role]
* US cluster: [cluster]
* Route: [route type]

## Why this may fit
[Concise explanation]

## Matched capabilities
- [Capability]

## Evidence
- [Source title].[^source-id] [Supported claim]

## Caveats
- [Caveat or None recorded]

[^source-id]: [Source title]
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
prospect_id	company	engagement_role	us_cluster	route_type	matched_capability
```

Write one row per prospect Markdown file, sorted by `prospect_id`. Join multiple matched capabilities with `; `. Replace tabs and line breaks inside values with spaces. Require unique `prospect_id` values and an exact match between index IDs and prospect filenames without `.md`.

## OKF Navigation Index Contract

Keep the navigation indexes short and derived; they must not introduce claims beyond the canonical concept documents.

`prospects/index.md` is a reserved OKF directory listing with no frontmatter. Replace it once at the end of every search cycle with:

```markdown
# Prospect Library

* [Example Company](example.com.md) - Potential Arizona route-to-market partner for the SME's tool-installation capability.
```

Write one entry per prospect file, sorted by filename. Use the `company` value as link text and the one-sentence `description` as the entry description. Do not list `index.md` itself.

The root `index.md` is also a reserved directory listing. Preserve its `okf_version: "0.2"` frontmatter and its Capability Profile entry. Ensure its body also contains:

```markdown
# Prospect Library

* [Prospects](prospects/) - Capability-relevant US prospects, route partners, and ecosystem connectors.
```

Do not enumerate individual prospects at the root; the `prospects/` link is the progressive-disclosure boundary.

## Quality bar

- Every prospect has exactly one canonical Markdown file, a non-empty OKF `type`, and at least one evidence URL.
- Every prospect file has one YAML frontmatter block at its start, the minimal fields in the Prospect Record Contract, and `sources` whose keyed Markdown footnotes, including definitions, attribute the body claims.
- The root and prospect-directory `index.md` files provide a complete two-level discovery path without adding commercial claims.
- Every prospect has direct capability relevance to the SME, stated in a sourced body explanation rather than a separate admission field.
- Timing and buyer access are captured when available; missing signals are explicitly deferred to Step 3 / human review rather than blocking admission.
- Obvious competitors, recruiters, unrelated organizations, and other defined noise remain excluded.
- Repeated cycles build a broad 15-30+ candidate pool without padding individual cycles.
- Every exact query is recorded in the search log.
- Every `generated.at` and search-log timestamp comes directly from the Codex runtime or system clock, never model generation.
- Repeated appearances update an existing record instead of creating another file.
- Parent and subsidiary records remain separate only when they are distinct buying organizations.
- Current projects, funding, facilities, hiring, and cluster programs come from live sources.
- AI- or user-added search terms are not presented as verified SME capabilities.
- Named existing customers and obvious group aliases are excluded unless account expansion is requested.
- Discovery remains broad and unscored; Skill 3 owns qualification.
