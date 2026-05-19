# ARPG Fight-Mechanics — Gap Analysis vs. Reincarnated Current/Desired State (2026-05-18)

**Status:** Synthesis artifact. Pairs `agentic_orchestration/gandalf/research/arpg-fight-mechanics-database-2026-05-18.md` (raw comparator data) with `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (engine/demo diagnostic) to produce per-axis gap analysis, per-commercial-path cost re-estimate, and recommended workstream priorities. Load-bearing input for Pattern-B (2026-05-19 morning).

**Authored by:** gandalf — synthesis across 4 Legolas Mode-A research returns (Wolcen, DD2, Grim Dawn, genre-baseline) + engine/demo code-trace audit + ARPG genre-design knowledge.

**Authored:** 2026-05-18 evening.

---

## § 0 — TL;DR

**Three findings, in increasing strategic weight:**

1. **The five-axis fight-integrity gap (canonical doc § 2) is real and confirmed against the genre baseline.** Every comparator (Wolcen, DD2, Grim Dawn, plus genre canon) has hard entity collision, per-skill range as a real design lever, leash/disengagement as a player option, and per-tier balance contracts. Reincarnated meets none of them. The gap is not "we're behind on polish" — it's "we are missing dimensions the genre treats as foundational."

2. **The Director's mod-first ranking is materially mis-ordered on technical grounds.** Director rec: Wolcen > Grim Dawn > Dragon's Dogma 2. Technical evidence rec: **Grim Dawn > Dragon's Dogma 2 > Wolcen**. Wolcen is in maintenance-mode end-of-life with a dormant modding community and no Workshop; Grim Dawn ships the same tools Crate uses internally and has empirical proof of 53-class injection (Dawn of Masteries). This is a Pattern-B finding that must be surfaced.

3. **The gap re-prices the commercial paths asymmetrically.** Path A (standalone) requires the full 9–15 week Track F to ship a genre-credible product. Path B (mod-first, especially into Grim Dawn) requires only ~3–5 weeks because the host game provides the spatial substrate, range, collision, and leash for free. Path C (engine-as-tool) is bimodal depending on buyer substrate. **The gap doesn't change which path is best — but it widens the cost spread between paths dramatically, in Path B's favor.**

---

## § 1 — Cross-cutting findings: what every modern ARPG has

The four research returns converge on a tight set of universals. These are not "Reincarnated would benefit from" features — they are the implicit contract a player picks up when they start an ARPG in 2026.

### § 1.1 — Universal across all comparators

| Universal | Confirmed in | Reincarnated has it? |
|---|---|---|
| **Real spatial substrate** (2D isometric or 3D) | Wolcen, DD2, Grim Dawn, D2, D3, D4, PoE, Last Epoch | **No** (engine is 1D scalar; demo is 2D but no collision) |
| **Hard entity↔entity collision** (or strong separation forces) | Wolcen (hard), DD2 (hard, with climb-physics), Grim Dawn (hard player-mob), D2/3/4/PoE/LE (varies hard/soft) | **No** (demo has none; engine has no spatial concept) |
| **Per-skill range published in tooltips** (radius / projectile / distance) | Wolcen (internal metric, mod surfaces it), Grim Dawn (Radius + Projectile in tooltips), DD2 (via animation reach; no numeric — outlier), D2/3/4 (yards), PoE (radius + travel), LE (radius) | **No** (catalogue has no per-skill range data) |
| **Disengagement as a real option** (aggro radius + leash + outrun or LOS) | Wolcen (Presence stat + LOS), Grim Dawn (large leash, several-screens reset), DD2 (LOS-break with long chase), all Diablos (leash circles), PoE (leash), LE (leash) | **No** (fight runs to 0 HP; FAR-band auto-converges) |
| **Per-tier balance as the contract** (boss tuned separately from trash) | Universal across comparators (varying rigor) | **No** (aggregate mean across 12-fight gauntlet) |
| **Boss telegraph system** (visual or animation wind-up) | DD2 (Itsuno's explicit "balance when player can judge"), Wolcen (arena hazards + animation tells, post-patch readability fixed), Grim Dawn (community criticism: telegraphs weak), D3 (strong telegraphs), D4 (strong), PoE (visible AOE markers), LE (telegraph-required design philosophy) | **No** (engine has no telegraph concept; demo has no skill-cast windup visual) |
| **Movement skill as a real build element** (dodge / dash / leap / teleport) | Wolcen (universal dodge + class-specific), DD2 (vocation-specific + late dodge mod), Grim Dawn (v1.2 universal Evade + per-mastery), all Diablos, PoE (movement skills are core), LE (movement skill slot) | **No (player-side)** (movement_speed is a mob stat, no class movement skills published) |

### § 1.2 — Variable across comparators

| Dimension | Spread |
|---|---|
| AI framework granularity | DD2 (goal-based, learning Pawn AI) > D3 (BT-heavy) > Wolcen (Kythera BT) > PoE/LE (mid) > Grim Dawn (simple — "approach until in range, attack" — engine constraint) |
| AOE footprint fidelity | Wolcen (geometrically real, 3D volumes) ≈ DD2 (geometrically real, 3D, terrain-interactive) ≈ Grim Dawn (explicit radius shapes) ≈ PoE/LE (radius math) > D3/D4 (more abstracted) |
| Movement skill centrality | PoE (essential) ≈ D3 (essential) ≈ Wolcen (essential post-launch) > D4 (strong) > Grim Dawn (strong post-v1.2) > DD2 (vocation-dependent) > LE (strong) |
| Modding ceiling | **Grim Dawn (HIGH — own tools, total-conversion proven) > DD2 (medium — REFramework recombination only) > Wolcen (LOW — XML-only, dormant) ≈ PoE/LE (minimal-none) > D2/3/4 (none official)** |

### § 1.3 — What this means for Reincarnated

**Reincarnated currently violates 7 of 7 universals.** Not partially — fully. Each violation is independently visible in playtest:

- No spatial substrate in engine → can't model boss-with-adds, can't model kiting geometry, can't model AOE coverage of spread packs
- No entity collision in demo → 8-mob stack-on-pixel artifact Matt reported
- No per-skill range → can't model out-ranging, can't model "skill misses because target too far," can't build a Ranger archetype properly
- No disengagement → fight runs forever, no chase tension, no "I have to flee and come back"
- No per-tier balance → bosses unbeatable while gauntlet reports green
- No telegraph system → bosses feel arbitrary; "I died and don't know why"
- No movement skills → kite-or-die is impossible; positioning is not a build axis

Each of these is a *foundational ARPG dimension*, not a polish item. The genre has trained the player to expect every one of them. **A standalone Reincarnated that ships violating all 7 will be evaluated as "not actually an ARPG," because that's what the violations cumulatively mean.**

---

## § 2 — Per-axis gap analysis (12 axes)

For each axis: genre standard → Reincarnated current → Reincarnated desired → gap size → closing workstream → effort → risk of not closing.

### Axis 1 — Dimensional model

| | Status |
|---|---|
| Genre standard | 2.5D isometric (looter-ARPGs) or 3D third-person (action-RPGs). Every comparator has true spatial coordinates. |
| Reincarnated current | Engine sim: 1D scalar `distance_m` (only). Demo: 2D pixel coordinates (but no collision/separation). |
| Reincarnated desired | Engine sim: spatial sub-gauntlet (Layer 2 in canonical doc § 3.2) with 2D positions + leash + per-skill range. Demo: keep 2D but add collision + separation + leash. |
| Gap size | **Severe** for engine; **medium** for demo. |
| Closing workstream | R2 (spatial sub-gauntlet, gamora + star-lord) for engine; R4 (demo collision/leash) for demo. |
| Effort | R2: 3–5 weeks; R4: 2–3 weeks. |
| Risk of not closing | Cannot test or deliver positional combat. Any "balanced" claim cannot map to player experience. Required for Path A; partially absorbed by host game in Path B. |

### Axis 2 — Collision system

| | Status |
|---|---|
| Genre standard | Hard entity↔entity in DD2/Grim Dawn/Wolcen; soft separation forces in D2/D3/D4/PoE; absolute absence is non-existent in any shipped comparator. |
| Reincarnated current | Engine: N/A (no space). Demo: **NONE — explicitly deferred at `world/movement.ts:197-199`.** |
| Reincarnated desired | Demo: soft separation force (push-apart at small radius) OR hard collision body. Engine: emergent in spatial sub-gauntlet. |
| Gap size | **Severe** (visible in playtest as 8-mob-stack-on-pixel artifact). |
| Closing workstream | R4 (drax). |
| Effort | ~1 week of the R4 budget. |
| Risk of not closing | Visual defect persists. AOE feels broken (always overkills the stack). Tactical positioning impossible. Required for Path A and Path C-spatial; absorbed by host in Path B. |

### Axis 3 — Per-skill range as design lever

| | Status |
|---|---|
| Genre standard | Per-skill range published in tooltips (Diablo yards, Grim Dawn Radius + Projectile values, Wolcen meters internal, PoE radius + travel, LE radius). Range modifiable via gear/passives in every looter-ARPG. Out-ranging is a viable build strategy in every comparator. DD2 is the outlier — range communicated via animation, no numeric tooltips. |
| Reincarnated current | One binary gate: `at_melee_range` at CLOSE_THRESHOLD (1.5m). No per-skill range data in catalogue. Demo applies hardcoded TS constants. |
| Reincarnated desired | Per-skill range as a real engine field, emitted in monster JSON + player skill catalogue. Engine sim respects it (skill cannot fire if target out of range). Demo respects it. Build modifiers on range optional but supported by schema. |
| Gap size | **Severe** (foundational genre dimension, currently entirely absent). |
| Closing workstream | R3 (rocket + star-lord + elrond — schema work + backfill across 5 shipped seasons). |
| Effort | 2–4 weeks (the schema migration is the biggest single piece). |
| Risk of not closing | Cannot build genre-credible Ranger / Sniper / Sorcerer / Brute archetypes. Cannot balance for "skill misses." Cannot model kite-able vs. close-required encounters. Required for ALL paths because every comparator wants this data from us. |

### Axis 4 — Disengagement mechanics

| | Status |
|---|---|
| Genre standard | Aggro radius + leash + outrun-viable in every comparator. Grim Dawn's leash is large; D3's is tight; PoE's mid; DD2 deliberately strict (still exists). LOS-break common. Movement skill is universal escape tool. |
| Reincarnated current | NONE. No aggro radius, no leash, no outrun, no LOS-break. Monster always advances. |
| Reincarnated desired | Per-mob aggro radius + leash distance (engine-emitted, scaled by threat_tier + substrate). Engine sim spatial sub-gauntlet supports disengagement as a valid AI choice. Demo supports outrun + leash-reset. |
| Gap size | **Severe.** |
| Closing workstream | R3 (schema fields) + R2 (engine sim spatial gauntlet uses them) + R4 (demo respects them). |
| Effort | Distributed across R2 + R3 + R4. |
| Risk of not closing | Every fight is to-the-death by design — no tactical flexibility. Bosses are unbeatable when over-tuned because player can't flee and recover. Aligns directly with Matt's playtest finding. Required for Path A; partially absorbed by host in Path B. |

### Axis 5 — Pack handling

| | Status |
|---|---|
| Genre standard | Real packs of N entities. Tier mix (trash/elite/hero/champion/boss). Hero monsters as mid-encounter surprises. Boss-with-adds is common (DD2 with ambient mobs, Wolcen Lambach add-escalation, Grim Dawn champions in packs, Diablo lineage with elite affixes). |
| Reincarnated current | **PackProxy** — N×HP single proxy entity, AOE × N multiplier. Misses death-attrition momentum, focus-fire dynamics, spatial CC, overkill waste. |
| Reincarnated desired | Real N-entity simulation in spatial sub-gauntlet for swarm + boss-with-adds scenarios. Keep PackProxy for fast 1D gauntlet (Layer 1) but don't trust it for swarm/boss balance. |
| Gap size | **Severe** for spatial truth; **acceptable** for stat-baseline 1D iteration. |
| Closing workstream | R2 (spatial sub-gauntlet simulates real N-entities). |
| Effort | Significant portion of R2. |
| Risk of not closing | Boss-with-adds (a universal genre pattern) cannot be balanced. Swarm AOE classes will be overrated; single-target classes underrated. Required for Path A and Path C-spatial; partially absorbed by host in Path B. |

### Axis 6 — AI patterns

| | Status |
|---|---|
| Genre standard | BT/FSM frameworks. Melee: approach-then-attack on cooldown. Ranged: kite-and-shoot, retreat only when threatened. Boss: multi-phase HP-gated rotation. Telegraph windows tuned for player reaction time. **Constant-flee is NOT canonical** in any comparator. |
| Reincarnated current | **Three decoupled AI implementations.** Engine sim: priority-rotation by archetype. Demo runtime: hardcoded kite-if-long (causing the constant-flee artifact). Balance loop: implicit assumption. No shared source of truth. |
| Reincarnated desired | AI specification fields in monster JSON (preferred behavior, telegraph window, aggro radius, leash, skill rotation, range profile). Engine sim and demo both read from catalogue. Range_profile redistributed (current "long"-bias produces constant-flee). |
| Gap size | **Architecturally severe** (three implementations is the gap-enabler). |
| Closing workstream | R3 (schema + catalogue migration) + R5 (demo AI parity audit). |
| Effort | R3 effort already counted; R5 ~1 week. |
| Risk of not closing | Gap recreates itself over time. Any fix to other axes drifts back out of sync. Required for ALL paths (Path B needs the AI fields to translate into host-game AI). |

### Axis 7 — AOE coverage

| | Status |
|---|---|
| Genre standard | Spatial footprint matters. Wolcen 3D volumes; DD2 3D radii × terrain; Grim Dawn explicit radius/cone/line. Most have binary in/out hit detection (falloff rare). Per-skill multi-target caps common. |
| Reincarnated current | Engine: AOE = damage × pack_size (multiplier abstraction; no geometric reality). Demo: no spatial AOE check (just hits the stack). |
| Reincarnated desired | Spatial AOE in sub-gauntlet — actual footprint queried against actual mob positions. Per-skill geometry fields in catalogue (cone/circle/line/chain + parameters). |
| Gap size | **Severe** for spatial truth; **acceptable** for 1D stat baseline. |
| Closing workstream | R2 + R3 (geometry schema). |
| Effort | Distributed. |
| Risk of not closing | AOE classes mis-balanced. Player skill expression in AOE positioning invisible. Required for Path A; partially absorbed by host in Path B. |

### Axis 8 — Balance approach

| | Status |
|---|---|
| Genre standard | Per-tier balance is the contract. Methodology varies: Grim Dawn (heavy playtest + community telemetry + hotfix); PoE (heavy playtest + league data); Wolcen (reactive); Diablo (mix of internal playtest + telemetry + balance team); DD2 (handcrafted, narrative-driven, no per-build balance philosophy). |
| Reincarnated current | Aggregate mean WR across 12-fight gauntlet. No per-tier WR thresholds. Mathematically robust at its level but operationally masks per-tier failure. |
| Reincarnated desired | Per-tier WR target floors (boss/miniboss/elite separately targeted in addition to mean). Adaptive balance loop drives toward per-tier convergence. |
| Gap size | **Severe** — the most operationally consequential gap (per canonical doc § 2.2). |
| Closing workstream | **R1** (per-tier balance targets, gamora). |
| Effort | 1–2 weeks. **Highest-leverage individual workstream.** |
| Risk of not closing | Continue to ship "balanced" classes with unbeatable bosses. Required for ALL paths (mod content with bad balance helps nobody). |

### Axis 9 — Movement skills centrality

| | Status |
|---|---|
| Genre standard | Universal class-wide dodge (Wolcen, post-v1.2 Grim Dawn, late-game DD2 via mod) + class-specific movement skills (PoE, Diablo lineage, Grim Dawn masteries, DD2 vocations). Movement is a build axis in every modern ARPG. |
| Reincarnated current | movement_speed is a per-mob stat. No player-side movement skills published. No class-wide dodge convention. |
| Reincarnated desired | At least one universal movement primitive (dodge or sprint) for player. Per-class movement skills as build options. (Open design question; gandalf Pattern-B input.) |
| Gap size | **Medium** (real, but less urgent than Axes 1-4). |
| Closing workstream | New (not yet in R1-R5 list). Design-first, then drax + rocket. |
| Effort | TBD (depends on design depth). |
| Risk of not closing | Player can't kite, can't reposition tactically. Combined with no-leash and no-collision, the demo combat space feels static. Recommended for Path A; may be absorbed by host in Path B. |

### Axis 10 — Telegraph system

| | Status |
|---|---|
| Genre standard | Boss attacks have visible wind-ups, animation tells, or arena hazard markers. DD2: Itsuno's explicit design philosophy. PoE: visible AOE telegraph rings. D3/D4: enemy affix telegraphs. Wolcen: arena hazards + animation. Grim Dawn: relatively weak (community criticism). |
| Reincarnated current | NONE. No telegraph concept in engine or demo. |
| Reincarnated desired | Per-skill telegraph window field on monster skills. Demo renders telegraph (color, ground marker, sound cue). Engine sim respects wind-up timing. |
| Gap size | **Medium-severe** (genre baseline; absence makes boss fights feel arbitrary). |
| Closing workstream | R3 (schema field) + R4 (demo rendering). |
| Effort | Distributed. |
| Risk of not closing | Bosses feel unfair ("I don't know what killed me"). Telegraph design is also part of why ARPG boss fights feel rewarding when survived. Required for Path A and Path C-spatial. |

### Axis 11 — Notable anti-patterns we should learn from comparators

| Comparator | Anti-pattern | Reincarnated relevance |
|---|---|---|
| Wolcen | Animation-commit + hard collision combo = "stuck in cast, can't move, die." | If we add hard collision (R4), don't also add long animation-commit. Soft separation may be safer. |
| Wolcen | No level scaling, HP at L75 = tens of millions (Better Expeditions mod patched). | Watch the high-end HP scaling math; don't let it inflate uncapped. |
| DD2 | No enemy level scaling → players one-shot trash by L20; intended variant-enemy tactics never matter. | Scaling discipline is load-bearing. Per-tier balance (R1) helps. |
| DD2 | No standard dodge roll → community immediately built one. | If we don't ship Axis 9 (movement skills), the community will demand it. |
| Grim Dawn | Damage Reflect mechanic poorly designed, bypassed defenses, caused one-shots → replaced in v1.1 with retaliation. | If we add reflect mechanics, design them tightly. |
| Grim Dawn | Single-threaded engine constrains AI complexity. | We're Python; we don't have this constraint in the engine. The demo is Pixi.js JS; also not a hard constraint. We can afford richer AI than Grim Dawn does. |
| All comparators | Boss telegraphs that aren't readable get patched. | Build readable telegraphs into R3/R4 from day one. |

### Axis 12 — Modding scene (for Path B viability)

Three Director-named targets, scored on mod-first viability:

| Target | Tools | Injection ceiling | Community | Recommendation |
|---|---|---|---|---|
| **Grim Dawn** | Crate ships full internal toolset (Asset Manager, World Editor, Database Editor, Quest Editor, Conversation Editor, Particle, Lua) | **New classes, skills, items, enemies, zones, factions all injectable. 53-class compilation mods proven (Dawn of Masteries).** Procedural map gen NOT engine-supported. | Active 10+ year ecosystem; NexusMods + forum; Fangs of Asterkarn sustains long-tail. | **STRONGEST candidate. Mod ladder: prove single-mastery injection → prove single-season export → prove rolling per-season releases.** |
| Dragon's Dogma 2 | REFramework (Lua API) + Asset Manager-equivalent absent | Content recombination via SkillMaker / DD2_VocationKit. **Total-conversion not feasible.** No level editor, no quest system, no scripted dialog. RE Engine patches break mods periodically. | Active (~1,100+ Nexus mods) but capability-ceilinged. | **Middle viability. Mismatch with looter-ARPG model is architectural, not cosmetic.** Best framed as "engine-as-design-input tool" for DD2, not engine-as-runtime. |
| Wolcen | No Workshop. File-replacement Umbra folders. CryEngine .PAK encrypted. XML-only modding surface. | Balance tweaks, UI, cosmetic, light mechanical. **Cannot mod Gate of Fates, skill animations, enemy models, dungeon layouts, AI behaviors.** | **Effectively dormant.** ~24 avg concurrent May 2026 (peak was 127k). Last patch July 2023. Multiplayer shut down Sept 2024. Maintenance-only. | **WEAKEST candidate.** Genre-adjacent but platform-not-viable. If pursued, the value is brand-association (recognizable name) not technical proof. |

---

## § 3 — Per-comparator viability ranking for Path B (mod-first)

**Director's recommendation:** Wolcen (#1) > Grim Dawn (#2) > Dragon's Dogma 2 (#3).
**Technical-evidence ranking:** **Grim Dawn (#1) > Dragon's Dogma 2 (#2) > Wolcen (#3).**

**The rankings are essentially inverted.** The Director likely ranked on commercial-visibility + genre-fit intuition (all three are real factors); the technical ranking weights modding-ecosystem viability heavily. **Both rankings are valid for different goals.** A mod-first effort optimizing for commercial visibility (brand recognition, press coverage) tilts toward Wolcen; a mod-first effort optimizing for technical proof + sustained community + iteration velocity tilts toward Grim Dawn. **DD2 sits in the middle on both axes** and would be the strongest *single-target* candidate if commercial-visibility and technical-feasibility were weighted equally.

**Pattern-B implication:** Q2 (mod-first target order) is not "which one first" but **"first for what goal."** Recommended framing for Matt:

- **For technical proof + iteration learning:** Grim Dawn first. Prove the export pipeline. Take the time. Build the community feedback loop with Crate-forum modders.
- **For commercial visibility:** Wolcen-flagged content (or DD2) earlier. Accept that the mod itself is harder; the press is easier.
- **For balanced approach:** Grim Dawn first (low-friction technical proof), then DD2 mod or Wolcen-themed showcase second (commercial play).

---

## § 4 — Per-commercial-path cost re-estimate (vs. Apex debrief)

The Apex Director debrief priced the paths in business terms. The fight-integrity gap re-prices them in engineering terms. Combined view:

### § 4.1 — Path A: Standalone Reincarnated-the-game

**Track-F engineering cost: ~9–15 dev-weeks** (full R1+R2+R3+R4+R5) + multi-week class-retuning sprint immediately following R1.

**Plus:** existing Phase-1 P1 commitments + new design work (Axis 9 movement skills, Axis 10 telegraphs).

**Realistic ship horizon under Path A: shifted right by 2–4 months minimum.** Standalone ARPG market is unforgiving — the gap violations *will* be reviewer-visible and player-rejected.

**Strategic shape:** Highest engineering cost, highest commercial uncertainty, deepest creative control. Path A is "we build the game we mean to build." It's also the path most exposed to the cement-deep-season-cadence problem the Director surfaced (player ecosystem may not theory-craft / story-engage at 1-week season cadence).

### § 4.2 — Path B: Mod-first

**Track-F engineering cost: ~3–5 dev-weeks** — R1 (per-tier balance) is non-optional; R3 (schema work, specifically per-skill range + per-skill geometry + AI behavior fields) is needed so host games can render our content properly. R2/R4/R5 are absorbed by host games.

**Plus:** host-specific translation layer (Grim Dawn DBR exporter; or DD2 REFramework Lua plugin; or Wolcen XML pipeline).

**Per-target cost variance:**
- **Grim Dawn first:** ~3 weeks Track F + ~4–6 weeks first mod export pipeline. **Total ~7–9 weeks to first shipped mod.**
- **DD2 first:** ~3 weeks Track F + ~6–10 weeks (RE Engine modding learning curve, recombination-only constraint forces design pivots). **Total ~9–13 weeks.**
- **Wolcen first:** ~3 weeks Track F + ~3–4 weeks (XML modding is simple) but with the asterisk that the platform community is ~24 players and shrinking. **Total ~6–7 weeks but commercially impotent.**

**Strategic shape:** Lowest engineering cost. Lowest creative control (constrained by host's combat substrate). Best commercial path-to-proof per the Director's framing. **The fight-integrity gap makes this path much cheaper than it would have been.**

### § 4.3 — Path C: Engine-as-tool / B2B SaaS

**Bimodal cost depending on buyer substrate:**

- **Spatial-ARPG buyer:** ~9–15 weeks (full Track F + buyer-specific export pipeline). Buyer expects content that respects their spatial substrate.
- **Auto-battler / idle / strategic-layer buyer:** ~3–5 weeks (R1 + minimal R3; skip R2/R4 because buyer doesn't model space). Buyer wants generation depth, not spatial fidelity.

**Plus:** operational layer (decision-tree authoring + content banking + deployment APIs + admin dashboards — Apex debrief § 5 estimate, requires Legolas Mode A scout + star-lord sit-down).

**Strategic shape:** Highest commercial upside (Director's framing). Most uncertain product surface. Highest dependency on identifying actual buyer profile.

### § 4.4 — Cross-path comparison

| Path | Track-F cost | Plus | Total to first viable ship | Risk profile |
|---|---|---|---|---|
| A — standalone | 9–15 wk | Phase-1 P1 + new design + class retuning | 5–8 months minimum | Highest engineering, highest market |
| B — Grim Dawn first | 3 wk + 4–6 wk pipeline | Mod content authoring | 7–9 weeks | Lowest engineering, low-medium market |
| B — DD2 first | 3 wk + 6–10 wk pipeline | Mod content authoring | 9–13 weeks | Medium engineering, medium market |
| B — Wolcen first | 3 wk + 3–4 wk pipeline | (Mod content) | 6–7 weeks but commercially weak | Low engineering, near-zero market |
| C — auto-battler buyer | 3–5 wk + ops layer | Operational layer | 3–6 months | Medium engineering, high market upside |
| C — ARPG buyer | 9–15 wk + ops layer | Operational layer | 5–9 months | High engineering, high market upside |

---

## § 5 — Recommended workstream priorities

Path-conditional. Pre-Pattern-B (before Matt's direction commit), no Track-F work is sequenced — the canonical doc is "diagnostic, not pre-approved roadmap amendment."

### § 5.1 — If Pattern-B commits Path A

```
R1 (per-tier balance, gamora, 1–2 wk)
    └─ triggers class-retuning sprint (multi-week, gamora + rocket)
R3 (schema migration, rocket + star-lord + elrond, 2–4 wk)
    └─ enables R2, R4, R5
R2 (spatial sub-gauntlet, gamora + star-lord, 3–5 wk) ─┐
R4 (demo collision/leash, drax, 2–3 wk)               ├── parallel after R3
R5 (demo AI parity audit, drax, 1 wk)                 ─┘
+ Axis 9 design work (movement skills)
+ Axis 10 design work (telegraphs)
```

### § 5.2 — If Pattern-B commits Path B (Grim Dawn first, recommended)

```
R1 (per-tier balance, gamora, 1–2 wk) — content tuning prerequisite
R3-subset (per-skill range + per-skill geometry + AI fields in catalogue, rocket + star-lord, ~2 wk) — host-game requirement
+ Grim Dawn DBR exporter (rocket + star-lord, 4–6 wk) — new workstream
+ Grim Dawn mod-ladder content (~ongoing) — substrate, class injection, single-season export
DEFER R2, R4, R5 until commercial signal warrants
```

### § 5.3 — If Pattern-B commits Path C

```
Validate buyer profile FIRST (Legolas Mode A research commission + star-lord conversation)
If auto-battler / idle / strategic-layer buyer:
    R1 (per-tier balance)
    R3-subset (data export, no spatial substrate)
    + Operational layer (decision tree authoring, content banking, deployment APIs, admin dashboards)
If spatial-ARPG buyer:
    Path-A workstream stack
    + Operational layer
```

### § 5.4 — If Pattern-B commits combination

If Path B + Path C parallel (recommended by Director's framing): R1 + R3 work is shared infrastructure; the host-game exporter (Path B) and buyer-export operational layer (Path C) can be authored against the same schema. This is the most-leveraged path engineering-wise.

---

## § 6 — Open questions for Pattern-B

These are questions the gap surfaces that need explicit Matt answers before Track F is sequenced:

1. **Direction commit (Q1).** Path A / B / C / combination? Per § 4.4 cost table.
2. **Mod-first target ordering (Q2).** For what goal — technical proof (Grim Dawn) or commercial visibility (Wolcen)?
3. **Per-tier WR target floors.** What WR floor for boss / miniboss / elite? Diablo II's heritage was "elite content passes ~30% of attempts." Reincarnated's answer?
4. **Demo collision soft-vs-hard.** Genre-faithful (hard) or retrofit-friendly (soft separation force)?
5. **AI unification — Option A vs B vs C** (per canonical doc § 7.5).
6. **Axis 9 (movement skills) design depth.** Universal dodge only, or per-class movement skills as build axis?
7. **Axis 10 (telegraph) design philosophy.** Telegraph windows uniform per tier, or per-skill tuned?
8. **R1 sequencing decision.** Land R1 before class-retuning sprint, or sequence them?
9. **Inversion of Director's mod-first ranking — communicate?** Pattern-B should name that the technical evidence inverts the Director's ranking. Director may want to update his view; he may have other info weighting his ranking that we don't have.
10. **Wolcen as commercial-visibility play (despite dormant modding).** Is the brand-association alone worth the engineering investment in a near-dead platform?

---

## § 7 — Recommendations to Matt

**Gandalf's pre-Pattern-B lean** (open to revision through the dialogue):

1. **Lead with the gap diagnosis in Pattern-B opening.** The fight-integrity finding is the highest-leverage piece of new context since the Director meeting. It re-prices every path. Q1 is not Q1 without it.

2. **Sequence R1 first regardless of direction.** Per-tier balance targets are required infrastructure under every path. Sequencing R1 now (~1–2 weeks of gamora) buys empirical validation of the diagnosis (the failure will appear in the metric) and produces the class-retuning workload that follows naturally. Don't wait for direction commit to fire R1.

3. **Recommended direction lean (subject to Matt's deeper read):** **Path B — Grim Dawn first**, with **Path C kept warm as parallel option once Path B proves the export pipeline.** Reasons:
   - Lowest total engineering cost
   - Strongest technical mod-platform (proven 53-class injection)
   - Aligns with Director's strongest leaning (mods-then-engine-sale ladder)
   - Sets up the Path C buyer narrative ("our engine exports content into the most-modded ARPG of the last decade")
   - Path A (standalone) costs the most and exposes the most product-market risk — DEFER, don't kill.

4. **Surface the Wolcen-ranking inversion to the Director eventually.** Not as rebuttal — as updated info. He may want to revise his rec. He may have outside info that justifies it. Either way, the technical evidence is what it is.

5. **Hold Q5 (the emotional/family dimension) as the final input, not the first.** All other questions are resolvable with research and rigor. Q5 is a life question. It should land at the end of the dialogue when everything else has been priced, so the trade is visible.

---

## § 8 — Refined findings from genre-baseline return (added after § 5)

Genre-baseline research (D2/D3/D4/PoE1/LE) returned after initial authoring. Key data points that sharpen the gap analysis:

### § 8.1 — Per-skill range gap is older than we framed it

**Diablo II in the year 2000 had richer per-skill range data than Reincarnated has in 2026.** D2's `rangeadder + Size` from Weapons.txt + monster `MeleeRng + SizeX/Y` from MonStats2.txt gave every weapon and every monster a published range value with explicit interaction. We are 26 years behind D2 on this single axis. This is the most damaging single framing for Path A (standalone) — the baseline genre player picking up Reincarnated in 2026 has 26 years of range-as-design-lever experience and will perceive its absence immediately.

### § 8.2 — D3 is the soft-collision exception, but with a cost

D3 deliberately chose soft / functionally-absent entity collision to enable the Area Damage stacking endgame meta. This is a valid design choice with a known cost: Maxroll guides explicitly document the "stack monsters infinitely tight and obliterate with Area Damage" optimization. **The community calls it cognitively boring.** D4 reset toward hard collision specifically because D3's soft model dissolved spatial positioning into a non-decision. **Implication for Reincarnated:** even if we wanted to "do what D3 does" with soft collision, the genre has since rejected that as a design dead-end. The trajectory is toward more spatial integrity, not less.

### § 8.3 — D4's leash inconsistency is exactly the player-trust failure we'd reproduce

D4 leashing is explicitly complained-about: "monsters run like 50 feet and then remember they left the stove on." Player reports document leash distances varying from "7-8 rooms" to "~10 feet" depending on zone/tier/content. **Breaks player trust in the world's rules.** Players cannot develop reliable intuition about disengagement. **Implication:** when we add leash (R3 schema fields), we MUST make it consistent and discoverable. The lesson from D4 is that inconsistent leash is worse than no leash, because it gaslights the player.

### § 8.4 — D4 dev openly acknowledged movement-skill-mandatoriness

Patch 2.5 notes: "This option has been treated as mandatory for too long" — the clearest official acknowledgment in the genre that universal movement-skill mandatoriness is a known design tension. **Implication:** if we ship Axis 9 (movement skills), design them as build options not mandatory. The trap to avoid: an Axis-9-mandatory build space (like Sorc-Teleport-D4) means every player must take the movement skill or be uncompetitive.

### § 8.5 — Last Epoch is the most aligned comparator on balance philosophy

LE explicit math-first balance approach ("we settled on Recurve Chance multiplied by 0.8 each time it recurves") + transparent skill tree philosophy ("commonly desirable nodes accessible; individual nodes shouldn't feel mandatory") is the closest in spirit to Reincarnated's sim-derived balance loop. **Implication:** LE is the most useful comparator for our balance approach — Crate's empirical-iteration model (Grim Dawn) is the modder-friendliest but not the most sim-similar; LE is the most sim-similar but the least moddable. **Pattern-B implication:** if Path C (engine-as-tool) ever targets an ARPG buyer, LE's design philosophy is the closest match to our pitch.

### § 8.6 — GGG's GDC 2019 talk and Development Manifestos are the genre's most public balance documentation

Chris Wilson's "Designing PoE to Be Played Forever" (GDC 2019) + the GGG Development Manifesto tradition is the most extensive public balance-philosophy documentation in the genre. **Implication for Reincarnated:** if we ever publish a balance manifesto (we should), GGG's manifesto register is the reference. Patterns: name the design intent, name what went wrong, name what the fix is, name what trade-offs were accepted.

### § 8.7 — Champion tier as combat + loot duality (LE innovation)

LE's Champion tier sits between Rare and Boss, with guaranteed Sealed Affix drop from a 14-affix pool. **It is simultaneously a meaningful combat challenge and a deterministic loot node.** This is a genre innovation we could absorb: a mid-tier encounter that's reliably surprising AND reliably rewarding. Reincarnated currently has trash/elite/miniboss/boss tiers in the gauntlet but no equivalent of LE's "Champion" — the encounter that's hard enough to matter and rewarding enough to seek out.

### § 8.8 — Pierce/Fork/Chain ordering is a formal genre primitive

PoE's `Pierce > Fork > Chain > Return` ordering is a formal hierarchy for projectile propagation modifiers. All five baseline games have at least one form. **Reincarnated has none.** Adding projectile propagation modifiers (even a subset — pierce alone would be a major design uplift) would be a high-value, low-cost-to-implement build axis once per-skill geometry data exists (R3).

---

## § 9 — Updates log

- **2026-05-18 evening (initial)** — File created. § 0–§ 7 authored from 3 of 4 research returns + gandalf genre knowledge.
- **2026-05-18 evening (final)** — § 8 added with refined findings from genre-baseline return. All 8 refinements integrate into existing axes; nothing in § 0–§ 7 was retracted, only sharpened. Database (§ 5 in database file) is the authoritative comparator data; this gap analysis is the authoritative synthesis.

---

*Filed 2026-05-18 evening by gandalf. The map is drawn; the road is named; the cost of each path is priced. Tomorrow we walk it together. Mithrandir signs.*
