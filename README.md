# SG Semicon US Expansion

Use this Codex plugin to help Singapore semiconductor and semiconductor-adjacent SMEs prepare for US prospecting.

This README covers only one skill:

```text
map-sme-capability
```

## What This Skill Does

`map-sme-capability` turns one Singapore SME website or company profile document into a short, editable Markdown capability profile.

The profile helps an analyst understand:

- what the SME actually does
- which claims are supported by source evidence
- how confident the agent is in the extracted capabilities
- which smart keyword seeds can guide the next interactive Google Search step

The keyword seeds are not final search queries. They are starting vocabulary for the next skill or analyst to adapt while searching live Google results.

## Quick Start

From a Codex thread opened in your project folder, ask:

```text
Use $map-sme-capability to map https://example.com.sg for US prospecting.
```

Replace `https://example.com.sg` with the SME website you want to map.

You can also provide a company profile document:

```text
Use $map-sme-capability on this uploaded company profile for [Company Name].
```

## Output

The skill creates one Markdown file:

```text
data/<safe_sme_name>_capabilities.md
```

The file contains:

1. Core technical capabilities
2. Evidence notes
3. Smart keyword seeds for US prospecting

## Workflow

The skill will:

1. Read the SME website or company profile document.
2. Check obvious capability pages such as Services, Products, Solutions, Industries, Certifications, Quality, Equipment, and About.
3. Extract 2 to 5 evidence notes that support the capability claims.
4. Remove generic marketing language.
5. Map up to 3 core technical capabilities.
6. Add confidence labels: High, Medium, or Low.
7. Generate exactly 5 smart keyword seeds for the next interactive Google Search skill.
8. Critique and improve the seeds so they are close to the SME's real capability.
9. Save the Markdown profile in `data/`.

## How To Review The Output

Review these parts first:

- **Core Technical Capabilities:** Are they specific and technically accurate?
- **Evidence Notes:** Do the source pages support the claims?
- **Confidence Labels:** Are weak or thin claims marked Medium or Low?
- **Smart Keyword Seeds:** Are they close enough to guide live Google Search without pretending to be final queries?

Good capability phrases are concrete:

```text
Machines tight-tolerance components
Deploys semiconductor MES workflows
Installs fab process tools
Builds fab communication networks
```

Weak capability phrases are vague:

```text
Provides world-class solutions
Supports advanced industries
Offers premium engineering services
```

## Keyword Seeds

The skill produces 5 keyword seeds:

1. Procurement
2. Production ramp
3. Tier 1 collaboration
4. Funding or new facility
5. Buyer pain

These are intentionally not perfect Google queries. They are useful starting points for the next interactive search step, where the agent or analyst should test live results and adapt the wording.

For example:

```text
semiconductor tool transport + cleanroom + new fab + USA
```

The next search skill may turn that into several live Google searches depending on what results appear.

## When The Skill Works Best

The skill works best when the SME source includes:

- semiconductor-specific pages
- services or products pages
- equipment, cleanroom, automation, software, quality, or certification details
- concrete terms such as `WIP tracking`, `SECS/GEM`, `MES`, `SPC`, `AMHS`, `cleanroom rigging`, `precision machining`, or `fab tool installation`

If the website is thin, the skill should say so through lower confidence or evidence notes.

## Installation

In Codex:

1. Open Codex.
2. Go to Plugins.
3. Open the marketplace dropdown and click Add more.
4. Add this repository as a plugin source.
5. Start a new Codex thread after installation.

![Open Plugins](screenshots/plugins.jpg)

![Click Add more](screenshots/addmore.png)

![Add marketplace source](screenshots/addmarketplace.jpg)

## Local Checks

To verify the plugin source, confirm these files exist:

- `.codex-plugin/plugin.json`
- `skills/map-sme-capability/SKILL.md`

To verify a run, check that a new file appears under:

```text
data/
```

## Design Principle

This skill is Phase 1 of the workflow:

```text
SME source -> capability profile -> keyword seeds
```

The next skill should handle Phase 2:

```text
keyword seeds -> interactive Google Search -> real US prospect candidates
```
