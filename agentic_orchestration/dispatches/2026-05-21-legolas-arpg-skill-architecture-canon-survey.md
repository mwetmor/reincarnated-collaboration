# Dispatch — Legolas Mode A: ARPG Skill / Ability / Trait / Node Architecture Canon Survey

**Date:** 2026-05-21
**Author:** gandalf
**Recipient:** legolas (Mode A — analytical research)
**Status:** ACTIVE — fires immediately, runs parallel to math note authoring
**Priority:** MEDIUM (informs P1 W1.13 parameter values + scope refinement; not P0-blocking)
**Estimated effort:** 1-2 days of focused research + synthesis

---

## 0. TL;DR

The QD-engine P1 W1.13 (multi-dim convergence + skill tree node population) will use parameter values currently sourced from Reincarnated's existing canonical UX/story spec (canonical/32 + canonical/33 + canonical/story/b6-skill-tree-ui-scoping.md). Those parameters were authored from one design intuition before:
- The substrate-as-cohesion architectural recommitment landed
- The multi-dim convergence math became the load-bearing convergence mechanism
- The Pattern-A pathology was empirically diagnosed

**The question this commission answers:** are Reincarnated's current canonical parameter choices (chain count 2-4, tier depth 3-4, per-skill cap 15, total SP budget 120, tier-scaling coefficients 1.05→1.25 by tier, investment gates 3/5/8) aligned with what produces "ARPG fun" + diverse-emergent-archetypes at scale across the canon, OR do they diverge from canon-best-practice in ways that warrant Scope D revision before P1 W1.13 fires?

**The user's framing (Matt 2026-05-21):**
> *"We may not have had enough skills and axes to even bother seeking this wisdom before, and I'm not sure but I think we may have wide enough of a palette of these items now to warrant the research and alignment towards 'ARPG fun'!"*

The math note + Scope D are starting structure. Research findings may transform Scope D beyond recognizability — and that's acceptable.

---

## 1. Context

### 1.1 The 10 research questions

For each major ARPG game surveyed (see § 2.1 for list), document the canonical answers to:

1. **Per-skill rank caps** — what's the maximum investment per individual skill/node?
2. **Total skill-point budgets** — how many points does a fully-leveled character distribute?
3. **Tier-scaling coefficient patterns** — what's the per-rank power-gain curve per tier of skill depth?
4. **Chain count + depth distributions** — how many "trees" / "chains" / "paths" exist per class? How deep does each go?
5. **Per-class active-skill counts** — how many simultaneous active skills can a player use? What's the hotbar shape?
6. **Investment gate mechanisms** — what unlocks higher tiers (rank-in-prereq / class-level / class-level-AND-rank / other)?
7. **Keystone vs spreading patterns** — what mechanic encourages deep investment in one skill vs spreading across many? What's the typical "build-defining keystone" shape?
8. **Synergy mechanisms across skills** — how do skills interact (multiplicative? additive? trigger-based? state-machine?) and what produces the most "fun" emergent builds?
9. **Stat / trait integration** — how do per-character stats (str/dex/int) interact with skill choices? Are they orthogonal axes or coupled?
10. **Endgame progression mechanisms** — what mechanisms (paragon / glyphs / aspects / cluster jewels / mastery levels) extend the player's tuning surface beyond character creation?

### 1.2 Why this informs W1.13

The multi-dim convergence algorithm operating over chains × tiers × SP × scaling-coefficients × gates has many tunable parameters. Each parameter value should be:
- Mathematically supportable for convergence (the math note's role)
- Empirically aligned with what produces ARPG-canonical-feel + diverse-build-emergence (THIS commission's role)

Without this commission, parameter values are sourced from one design intuition. With it, they're sourced from genre best-practice synthesis.

### 1.3 Why this commission is MEDIUM priority, not HIGH

- P1 W1.13 is ~2-4 weeks out (after P0 close)
- Math note v1 can be authored using gandalf white-wizard intuition; v1.1 amendment folds in legolas findings
- Parameter values are tunable mid-implementation if research surfaces canon-divergence
- Structural Scope D shape (chains × tiers × SP × tier-scaling-preserved) is likely robust; specific values may shift

---

## 2. Research scope

### 2.1 Games to survey

**Primary canon (must-have):**

- Diablo II (the deep-chain specialist canon)
- Diablo III (rune-variant + paragon canon)
- Diablo IV (skill tree + paragon board + aspect canon)
- Diablo Immortal (mobile-scaled ARPG; reduced-complexity choices)
- Path of Exile (massive passive tree + skill gem + cluster jewel canon)
- Last Epoch (per-skill specialization tree + class passive tree canon)
- Grim Dawn (dual-mastery + skill point allocation canon)

**Secondary canon (worth including if time allows):**

- Path of Exile 2 (early data; modern variants)
- Lost Ark (Korean ARPG conventions; identity skills)
- Wolcen: Lords of Mayhem (modern hybrid ARPG)
- Marvel Heroes 2016 (skill-tree-with-character-leveling; defunct but instructive)
- Torchlight 2 / 3 (D2-shaped variants)

### 2.2 Per-game data structure

For each game, produce a structured data row with the 10 question answers + canonical citations (game wiki / community guide / dev interview / GDC talk).

### 2.3 Synthesis output

After per-game data collection, produce cross-cutting synthesis:

- **Mean / median / range** for each of the 10 questions across the canon
- **Reincarnated current spec vs canonical median** — divergences flagged
- **Best-practice patterns** — which structures produce the most build diversity? Highest player ratings? Most emergent archetypes?
- **Parameter recommendations** — what specific values for Reincarnated's chain count / tier depth / SP budget / cap / scaling / gates would align with canon best-practice?
- **Scope-D refinement notes** — does the proposed Scope D structure match canon, or should it pivot? Specifically:
  - Are tier-specific scaling coefficients (1.05→1.25) canonical, or do most ARPGs use different patterns?
  - Are 3/5/8 unlock gates canonical, or do most use level-based or hybrid gating?
  - Are 2-4 chains per class canonical, or do most use a different shape?
  - Are 5-8 active slots canonical, or do most use a different number?

---

## 3. Deliverables

Produce at:

```
agentic_orchestration/legolas/research/arpg-skill-architecture-canon-survey-2026-05-2X/
  ├── summary.md                                    — top-line findings + Reincarnated recommendations
  ├── per-game-canonical-data.md                    — per-game structured rows
  ├── parameter-recommendations.md                  — specific values to consider for Reincarnated
  ├── scope-d-divergence-flags.md                   — if any structural Scope D pivots are warranted
  └── data/
      ├── per-game-data.csv                         — machine-readable per-game per-question data
      └── parameter-comparison.csv                  — Reincarnated current vs canonical median vs recommendation
```

After review by gandalf, content may be promoted to:

```
canonical/story/arpg-skill-architecture-canon-survey-2026-05-2X.md
```

---

## 4. Methodology constraints

- **Read-only across all sources.** No procurement decisions; no commitments. Pure research.
- **Cite specifically.** Game wiki URLs + community guide references + dev interview citations + GDC talk references where applicable.
- **Estimate honestly.** When data is uncertain or contested, flag it (e.g., "PoE total skill point budget is ~120 from levels + Bandit + skill points from quests — varies by build choice; range 99-127").
- **Stay in Mode A.** No code changes, no asset acquisitions, no schema modifications.
- **Flag canon-divergence between games.** If D2 uses one pattern and D4 uses another, document both; don't average without commentary.
- **Surface "ARPG fun" patterns explicitly.** Beyond data values, what STRUCTURAL choices across canon produce the highest-rated build diversity? GDC talks + dev interviews + community meta analyses are key sources.

---

## 5. Cross-references

- `canonical/32-progression-design.md` — Reincarnated's current canonical skill tree spec (UX/story-driven)
- `canonical/33-progression-skeleton.md` — Reincarnated's progression skeleton
- `canonical/story/b6-skill-tree-ui-scoping.md` — B6 UI scoping spec
- `canonical/story/multi-dim-convergence-algorithm-2026-05-2X.md` — math note v1 (being authored in parallel)
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architecture
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC spec (target of convergence)

---

## 6. Timing

- **Start:** immediately on dispatch acceptance
- **Target completion:** 1-2 days of focused research
- **Concurrent with:** math note v1 authoring (gandalf, ~3 hours)
- **Output review:** gandalf synthesizes; identifies math note v1.1 amendment scope
- **Math note v1.1 amendment:** ~2-3 hours after research completes (only if research surfaces meaningful divergence)

---

## 7. Authority

- **Methodology questions:** route to gandalf
- **Scope/priority disputes:** gandalf decides; escalate to Matt only if gandalf+legolas cannot converge
- **If research surfaces a finding that suggests Scope D structural pivot:** flag immediately to gandalf for math note v1.1 framing decision; Matt approves any structural pivot
- **No commitment authority** — recommendations are recommendations; gandalf reviews + Matt approves before parameter values commit to W1.13 implementation

---

**Signed:** gandalf (story-and-design steward)
**For:** ARPG-canon parameter alignment + Scope D refinement for QD-engine W1.13.
