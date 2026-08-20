# Singapore Semiconductor U.S. Expansion AI Agent: Technical Overview

## Purpose

The AI agent helps SBF prepare informed market-entry conversations with Singapore semiconductor SMEs. It turns public evidence into a capability profile, prospect library, qualified shortlist, and executive brief.

The agent prepares research and recommendations. SBF officers and SME leaders make every decision. It does not contact companies, make introductions, negotiate, spend funds, or make commitments.

## Workflow

The plugin has four skills. Each produces a reviewable output and ends with a human decision.

### 1. Map capabilities

The agent reads the SME's website or profile, identifies up to three capabilities relevant to semiconductor buyers, and links factual claims to public sources.

The SME and SBF approve the capability profile before discovery begins.

### 2. Build the U.S. prospect library

The agent searches iteratively for plausible buyers, route partners, and ecosystem connectors. Each cycle reviews prior work, explores an uncovered buyer type, route, cluster, or operating signal, adds source-backed candidates, removes duplicates, logs gaps, and selects the next search direction.

The goal is high recall: retain plausible, capability-relevant options before strict filtering. The process is systematic but cannot guarantee complete market coverage.

SBF reviews the library and can change the scope, geography, target types, exclusions, or next search cycle.

### 3. Qualify prospects

The agent applies high-precision screening based on capability fit, timing, buyer path, accessibility or SBF route, cluster relevance, and evidence strength. Fast-Fail gates remove candidates with fundamental gaps, and a transparent 20-point rubric supports relative comparison.

SBF reviews the evidence, scores, caveats, exclusions, and engagement recommendation, then decides which routes warrant validation or support.

### 4. Export the executive brief

The agent converts the approved shortlist into an offline dashboard showing priorities, evidence, unknowns, and proposed SBF actions.

SBF approves the brief and decides whether to validate a route, contact a partner, make an introduction, plan a mission, request more research, or stop.

## Technical design

- Open Knowledge Format: Capability profiles and prospect records use OKF v0.2. Readable Markdown, YAML metadata, source links, and per-claim footnotes create an inspectable evidence trail.
- Agent plugin specification: The workflow supports Agent Plugins v1.0.0. The root `plugin.json` is the portable manifest, and the four skills live in standard `skills/<skill-name>/SKILL.md` locations. A Codex-native manifest supports installation in Codex.
- Persistent state: Each SME has an output folder containing its capability profile, canonical prospect records, search history, shortlist, and dashboard. New cycles extend prior work instead of restarting.
- Subagents: Skill 2 can assign independent, bounded, read-only searches to subagents. The primary agent validates their findings, resolves duplicates, writes canonical OKF records, and remains responsible for every saved result.

## Controls and responsibilities

The agent uses public sources and does not access private procurement systems, confidential customer data, or login-gated social networks.

An announcement, award, permit, or prospect record is a signal for investigation, not proof of demand, supplier approval, buyer access, or a future contract.

SBF retains responsibility for route validation, convening, missions, and appropriate introductions. The SME retains responsibility for outreach, commercial qualification, investment, delivery, and compliance.

## Limitations

1. Skill 2 depends on available internet search tools. Search engines, source indexes, and strategies vary across agent environments. Without internet search, discovery cannot run as designed.

2. Output quality depends on input evidence. If the SME's website or profile lacks detail, the SME can provide an approved capability deck or supporting material. The agent should not infer unsupported capabilities.

3. Evidence interpretation involves model judgment. Different models, tools, or execution dates may produce different assessments. Scores should compare prospects within the same qualification run, not serve as absolute measures or predictions of commercial success.

4. Public information can become outdated. Facility plans, hiring signals, partnerships, and contact routes should be reverified before action.
