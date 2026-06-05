# SG Semicon US Expansion

This plugin helps business users quickly understand what a Singapore semiconductor SME actually does.

It takes a company website or company profile and creates a short capability summary that can be used for US prospecting work.

This README covers only one skill:

```text
map-sme-capability
```

## What You Can Use It For

Use this skill when you have a Singapore semiconductor or semiconductor-adjacent SME and want to answer:

- What does this company actually do?
- What technical capabilities are supported by evidence?
- How confident should we be in those claims?
- What starting keywords could help a later Google Search step find US prospects?

The output is not a final prospect list. It is a clean starting point for the next research step.

## What You Need Before Starting

You need:

1. Codex installed and open.
2. This plugin installed in Codex.
3. A company website, such as:

```text
https://www.example.com.sg
```

Or a company profile document, such as a PDF or Word file.

You do not need to know Python, Git, spreadsheets, or programming.

## Install The Plugin

In Codex:

1. Open **Plugins**.
2. Open the marketplace dropdown.
3. Click **Add more**.
4. Add the plugin link or folder provided by the project lead.
5. Start a new Codex chat after installation.

Screenshots:

![Open Plugins](screenshots/plugins.jpg)

![Click Add more](screenshots/addmore.png)

![Add marketplace source](screenshots/addmarketplace.jpg)

You know installation worked if Codex lets you use:

```text
$map-sme-capability
```

## First Test Run

Open a new Codex chat in the folder where you want the output saved. Then type:

```text
Use $map-sme-capability to map https://www.example.com.sg for US prospecting.
```

Replace the example website with the SME website you want to analyze.

If you have a company profile document instead, upload it and type:

```text
Use $map-sme-capability on this uploaded company profile for [Company Name].
```

## What The Skill Creates

The skill creates one plain-text Markdown file in your chosen folder:

```text
data/<company_name>_capabilities.md
```

For example:

```text
data/cantier_systems_capabilities.md
```

Markdown is just a plain text format. You can open it like a normal document.

## What Is Inside The Output

The output has three sections:

1. **Core Technical Capabilities**
   - Up to three short descriptions of what the SME actually does.

2. **Evidence Notes**
   - Short notes showing which source pages support the claims.

3. **Smart Keywords for US Prospecting**
   - Five keyword seeds for the next interactive Google Search step.

The keyword seeds are not final Google searches. They are starting vocabulary. The next research step should adapt them based on live search results.

## How To Review The Output

Check these items:

1. Are the capabilities specific?
2. Do the evidence notes support the claims?
3. Are weak claims marked with Medium or Low confidence?
4. Are the keyword seeds close to what the company actually does?

Good capability examples:

```text
Machines tight-tolerance components
Deploys semiconductor MES workflows
Installs fab process tools
Builds fab communication networks
```

Weak capability examples:

```text
Provides world-class solutions
Supports advanced industries
Offers premium engineering services
```

## About The Keyword Seeds

The skill creates five keyword seed types:

1. Procurement
2. Production ramp
3. Tier 1 collaboration
4. Funding or new facility
5. Buyer pain

These are meant to help the next Google Search step start in the right direction.

Example keyword seed:

```text
semiconductor tool transport + cleanroom + new fab + USA
```

The next search step may change the wording after seeing real Google results.

## When Results Are Good

The result is usually good when the SME website has:

- clear services or products pages
- semiconductor-specific pages
- equipment, cleanroom, automation, software, quality, or certification details
- concrete technical terms such as `MES`, `AMHS`, `SECS/GEM`, `precision machining`, `cleanroom rigging`, or `fab tool installation`

## When Results Need Review

Review more carefully when:

- the website is very short
- the website uses mostly marketing language
- there is no semiconductor-specific page
- the company appears to serve many industries but does not explain its semiconductor work clearly

In these cases, Medium or Low confidence is acceptable.

## Simple Workflow

Use this plugin as Phase 1:

```text
SME website -> capability profile -> keyword seeds
```

Use another research step as Phase 2:

```text
keyword seeds -> interactive Google Search -> possible US prospects
```

## Need Help?

If the skill creates a weak profile, try again with a better source:

- a company brochure
- a capabilities page
- a product or services page
- a semiconductor-specific page

Better source material usually produces a better capability profile.
