# 28 — Engine ARPG Rebalance Design Discussion

**Captured:** 2026-05-10
**Status:** Engine queue — **demo1 v1.2 shipped 2026-05-11; queue items now active per file 16 staging.** Original 5 seasons stay as demo1 baseline until Stage A2 regen lands; new season generation tied to Stage A2 + subsequent stage completions per file 16.

**⚠️ Single-season-per-playtest cost guardrail (LOCKED 2026-05-12 — see file 16):** post-Stage-A2 LLM cost rises to ~$5-10/season (B14 multi-band + per-band monster pools + B15 sets). Regenerate AT MOST ONE season per playtest cycle as default policy. Multi-season regen requires explicit justification (cross-season meta-progression validation; Phase 0 closure sweep; specific design questions requiring cross-season comparison).

**🔧 Refactor approach (LOCKED 2026-05-12 — see file 16):** Track A is a REFACTOR of the existing engine, NOT a rewrite from scratch. All B-items extend existing infrastructure. Tag `v1.2-pre-stage-a2` on both engine + demo repos before Stage A2 begins as the restore point.
**Context:** Demo Phase 8.0.3 playtest surfaced that the demo's combat reads as adventure-game (1v1 duels) rather than ARPG (horde combat). Phase 9.5 will adapt the demo with trash adds (Option B); but several engine-side balance issues compound the genre-feel problem and won't be solved by demo-side wave restructuring alone. This document consolidates the engine-side items, sequences them, and identifies decision points for the next engine session(s).

**Sequencing locked 2026-05-10:** demo1 ships against current 5-season baseline with all known engine issues tolerated (combo class half-broken, milk/thrum awkward, gentle WIS scaling, etc.). Engine session(s) open after demo1 ship in sequential chunks; new seasons regenerate after engine fixes land. This document is the post-ship roadmap.

## Why this exists

The Reincarnated engine's class-balance loop converges classes against a 1v1 gauntlet at a 50% win-rate target. That convergence is rigorous and demonstrably correct for *adventure-game-shaped* combat (one player vs. one boss). But the demo's positional layer (Phases 6+) and the family playtest data are revealing that **ARPG genre signature requires fundamentally different combat shape**: horde fights, AOE saturation, universal CC, screen-clearing.

Several findings have been independently captured in `project_engine_state_findings.md` over the course of demo1 development. Many of them are now interconnected — they all touch the same question: *what does the engine emit that supports ARPG combat?* This document pulls them together so they can be addressed coherently rather than as one-off fixes.

This is a design discussion, not an implementation spec. The questions here include "do we even want this?" alongside "if yes, how?"

## The problem framing

| Dimension | Current engine assumption | ARPG genre expectation | Gap |
|---|---|---|---|
| Combat structure | 1v1 duels, balance-loop converges per class | Horde combat, screen-clearing as core loop | Engine has no n-vs-m sim |
| AOE prevalence | One geometry type among 16 | AOE-saturated player kits (most viable builds have AOE primary) | AOE underweighted in generation |
| CC universality | Some classes have chill/root/knockback; many don't | Genre-universal — every class has *some* CC | Distribution gaps |
| Trash design | "1v1 weak opponent that dies fast" | "Swarm fodder, low HP, low damage, high count" | Trash isn't its own design tier |
| Win-rate target | Binary (won fight in time / didn't) | Density-aware (cleared horde efficiently / didn't) | Convergence loop uninformed by horde context |
| Knockback | Stub (in `AILMENT_NAMES`, no consumer in sim) | Working positional displacement | Engine has no positional substrate |

The demo Phase 9.5 will paper over some of these by adding trash adds at the demo layer (Option B from the wave-restructure design discussion). That works for demo1 but creates engine-demo divergence: the demo invents semantics the engine sim doesn't model. Long-term, the engine should mirror the demo's pattern OR vice-versa.

## Item catalog

Items are grouped by type. Bug fixes are clear; balance tuning and architectural items have decision points.

### Category A — Bug fixes (clear bugs, no design debate)

These are documented errors. Each has a known fix; the only question is when.

**A1b. Focus skill cost generator miscalibration** *(NEW 2026-05-10 — same shape as A1)*
- Focus skill costs across all 5 seasons range 7.9 to 35.3 (median ~19); most are 13-26
- Engine spec: focus passively decays -5/sec, restores +10 per skill cast
- BUT the engine generator emits skill costs FAR larger than the +10 restore
- Result: focus classes net-lose energy on most casts (-3.7 to -25.3 per cast) PLUS -5/sec decay; pool depletes within seconds; classes feel unsustainable
- Same root cause as A1: generator calibrated against `damage_formula.md`'s wrong values
- Fix options: (a) clamp focus skill costs at ≤ FOCUS_RESTORE_PER_CAST (10), (b) raise FOCUS_RESTORE_PER_CAST to ~25 in engine, (c) per-tier scaling
- Recommendation: (b) raise restore to 25 — preserves skill cost spread for class differentiation while making focus playable
- Estimated cost: ~30-60 min once decision made; affects engine sim + regen seasons

**A1. Combo skill cost generator miscalibration** *(captured in `project_engine_state_findings.md` 2026-05-10)*
- 50% of combo skills (12 of 24 across 5 seasons) cost 13.7 to 30.0 against pool size 5
- Root cause: generator likely calibrated against the old pool=100 documented in `damage_formula.md`
- Fix: clamp combo skill costs at pool_max - 1 (max 4 for pool size 5; or max 5 if "spend everything" is intended endpoint)
- Affected skills need damage/effect rebalance since cost was inflating power budget
- Estimated cost: ~30-60 min generator change + regen affected skills

**A2. Skill geometry dimensions missing from JSON** *(captured 2026-05-10)*
- Skills carry only `geometry_type` (e.g., "cone", "line"); no `range`, `half_angle`, `area_radius`
- Demo Phase 6 worked around with a catch-all 870px hit detection for non-melee geometries
- Demo Phase 6.2 invented VFX dimensions per geometry type
- Fix: add per-geometry default dimensions + per-skill overrides
- Estimated cost: ~1 hr generator + schema change

**A3. `damage_formula.md` doc audit (10 documented errors)** *(accumulated through Phases 4.5, 5.5d)*
- Mana regen formula (additive vs multiplicative)
- Dodge cap (0.60 actual vs documented)
- Mana base regen value
- Stamina regen rate (11.6× too slow)
- Focus mechanics (direction backwards)
- Combo pool size (5 actual vs 100 documented)
- Rage gain formula (flat vs percentage-scaled)
- Crit chance cap (0.75 actual vs 0.60 documented)
- Direct heal scaling formula
- HoT damage_modifier application
- Fix: rewrite resource math sections against actual code in `_ENERGY_CONFIGS` (`combatant.py:229`), `math_model.py`, `damage_resolver.py`
- Estimated cost: ~1-2 hrs

**A4. Shield magnitude scaling** *(captured 2026-05-10)*
- Engine generator emits flat `magnitude=1000` across all shield abilities, regardless of class power
- Engine resolver has no scaling (no WIS, no `damage_modifier`)
- Asymmetric with adjacent defensive output: heal scales with WIS, HoT scales with `damage_modifier`, shield is flat
- Fix options: (a) multiplicative WIS scaling like heal; (b) `damage_modifier` scaling like HoT; (c) generator emits class-tier-scaled magnitudes
- Decision needed: which scaling model
- Estimated cost: ~30-60 min once decision made

### Category B — Balance tuning (engine balance calls)

These aren't bugs — they're design decisions where current values produce correct behavior but wrong feel. Decisions needed before implementation.

**B1. WIS-on-heal multiplier is gentle** *(captured 2026-05-10)*
- Engine: `magnitude × (1.0 + wisdom × 0.002)` — 30% bonus at 151 WIS
- Matt's playtest assessment: thin payoff for ~150 stat points; players don't stack WIS
- Compared to STR/DEX scaling damage with steeper curves, WIS becomes a low-payoff stat
- Decision: raise multiplier (e.g., 0.005 = 75% bonus at 151 WIS), accept current as utility-stat design intent, or per-skill scaling override
- Estimated cost: ~30 min + balance regen

**B2. Per-skill ailment chance scaling** *(captured 2026-05-10)*
- Engine: flat `BASE_AILMENT_CHANCE = 0.35` for every chill/root/knockback/burn/bleed
- Matt's design intent: scale chance with skill cost
  - High-cost, high-cooldown ults: 100% (before resistance) — big investment = predictable big effect
  - Mid-cost: 0.35 (current default — keep)
  - Low-cost spam: <0.35 (probably 0.15-0.25)
- Implementation options: auto-derive from `energy_cost × cooldown_seconds` ratio, per-skill explicit override, or both
- Decision: derivation model + sensible defaults
- Estimated cost: ~1-2 hrs once decision made

**B3. AOE budget rebalancing** *(NEW from this discussion)*
- ARPG genre expects most viable builds to have AOE in their primary kit
- Current engine: AOE is one geometry type among 16; distribution is uneven across archetypes
- Some archetypes have multiple AOE skills; others have none
- Decision: should generation explicitly weight AOE coverage per archetype? Or accept the natural distribution and let players pick AOE-leaning classes?
- If yes: define an "AOE coverage score" per class and target a minimum threshold
- If no: accept that some classes are single-target specialists (genre-acceptable as a sub-archetype)
- Estimated cost: ~2-4 hrs if pursued

**B5. Legendary gear abilities — original Priority 02 design intent not shipped** *(NEW 2026-05-10)*

**Confirmed via inspection of `gear_pool.json` across all seasons:** every gear item (all 200 per season, all tiers) has identical field set — no `granted_ability`, no `aura`, no `on_hit`, no `proc`, no `cast_on_attack`, no `effects` of any kind. Only `power_score` + `fit_*` dimensions + aesthetic content (name/flavor/visual_prompt). Mechanical impact across all tiers comes entirely from `fit_for_class()` × `power_score` calculation; legendaries differ from commons only in raw power, not in mechanical novelty.

**Matt's original design intent (re-surfaced 2026-05-10):**
- Auras on armor/shield: regen, thorns, minor damage aura, chill, intermittent root
- Cast-on-attack abilities on weapons OR an added 7th skill (if class already has 6)

**Current state vs design intent:** the engine produces "stat-stick legendaries with great flavor" — JRPG-accessory-shaped, not ARPG-legendary-shaped. This is a structural genre alignment issue alongside wave-restructure and per-skill ailment chance scaling.

**ARPG genre baseline reference:**
- Diablo 3 Legendaries: every legendary has a Legendary Power changing skill behavior
- Diablo 4 Aspects: legendary affixes granting new mechanics
- Path of Exile Uniques / Last Epoch Uniques: each unique has explicit special mechanic
- Pattern: legendary = mechanically novel, not statistically larger

**Schema additions to gear (legendary-tier only):**
- `granted_ability` on weapons (or 1h/2h/off_hand): ability ID or inline spec; 7th hotbar slot OR replaces existing
- `aura` on armor/shields/accessories: passive effect (regen, thorns, damage radius, intermittent chill/root, damage reduction); ticks in active_effects pattern
- `on_hit` on weapons: chance-based proc (chill / burn / heal / mini-AOE / etc.)
- `cast_on_attack`: deterministic Nth-attack trigger

**Generator considerations:**
- Only legendaries get these (preserves rarity meaning)
- Naming pipeline consumes granted ability → reflects in name + flavor text
- Class fit gates which abilities are appropriate per gear slot
- Power budget shifts: legendary stats decrease slightly to compensate for granted-ability power

**Sim adoption:**
- Convergence loop accounts for legendary builds; gear-on convergence may differ from current gear-off baseline
- May require class `damage_modifier` rebalance downward

**Demo-side consumption:**
- Hotbar handling for 7th slot
- Aura ticking via existing active_effects pattern (Phase 8.0.2 architecture supports this cleanly)
- VFX + audio for granted abilities (reuse Phase 3 geometry rendering)
- Tooltip surfacing granted ability + aura

**Estimated cost:** ~1-2 weeks engine + ~2-4 days demo integration. Significantly larger than typical Category B item; could justify its own category if more such "scope-cut from Priority 02" items surface. For now keeping in B5.

**Decision points for the design session:**
- Should ALL legendaries grant abilities, or only some? (Recommendation: all, with variable richness — some grant minor on-hit procs, some grant full skills)
- 7th hotbar slot or replace-existing-slot pattern? (Recommendation: 7th slot. Replace-existing-slot is too disruptive to class identity.)
- Aura stacking rules: multiple aura items equipped — do they all tick? Cap?
- Should engine convergence run gear-on or gear-off? (Recommendation: gear-on, with the canonical loadout from Phase 5.5f's carried_gear baseline.)

**Sequencing within Phase B:** B5 is the heaviest item in Category B by far. May want to split into its own engine session after B1-B4 land. OR if Matt wants ARPG genre-feel investment to be coherent, bundle B2 (ailment chance) + B5 (legendary abilities) + B3 (AOE budget) as the "ARPG content quality" session. Architectural cousins.

**B4. Trash tier as its own design / Swarm-tier monster generation** *(NEW from this discussion; expanded 2026-05-10 after family playtest #3)*

**Updated 2026-05-10:** Phase 9.5a (demo) ships pack-grade monsters with client-side stat override (HP×0.18, damage×0.25 of current trash baseline). This is a demo-layer override; engine convergence assumes current trash stats. Long-term, engine should emit a swarm-tier monster variant alongside the existing trash baseline, so generation produces swarm fodder natively rather than relying on demo overrides.

**Generation rule (when engine adopts):** for swarm-tier, emit:
- HP: 15-25% of current trash HP baseline
- Damage: 20-30% of current trash damage baseline
- Skills: simplified kit (1-2 abilities, not full set)
- AI: simple tier (always-attack, slow cadence)
- Drops: potion-only (no gear from swarm tier; preserve gear progression on named tiers)

**Composition rule (when engine adopts):** wave compositions can include swarm-tier mobs as adds to named-tier opponents (e.g., Wave 3 = 1 elite + 3 swarm), with engine convergence balancing the named tier against the player rather than the swarm-grade adds.
- Current trash is tuned as "1v1 weak opponent that dies fast" with full skill kit
- Demo Phase 9.5 (Option B) needs trash that's "swarm fodder" — low HP, low damage, high count, simple kit (1-2 abilities at most)
- Engine generator could emit a separate `tier=trash_swarm` variant alongside the existing `tier=trash` baseline
- OR: demo can override trash stats at runtime to convert standard trash into swarm trash
- Decision: engine support for swarm-tier trash, or demo-side override
- Estimated cost: ~1-2 hrs (engine) or ~30 min (demo-side override)

### Category C — Architectural changes (deeper engine work)

These require structural changes to the engine sim. Significant cost; only do if needed.

**C1. Multi-target dispatch in sim** *(NEW from this discussion)*
- Current engine: 1v1 sim — `resolve_skill(skill, attacker, defender)` is the unit
- ARPG horde combat needs n-vs-m: one skill cast can hit multiple defenders, multiple monsters hit one player
- Implementation: refactor `resolve_skill` to accept defender list; AOE geometries hit multiple; single-target hits one selected by AI/player choice
- Convergence loop becomes density-aware: track "kill density per second" vs simple "killed in time"
- This is the biggest architectural change — weeks of work, risk of regression
- Decision: do we need this, or can demo Phase 9.5 + future demos invent multi-target semantics on the demo side?
- Tradeoff: not doing it means engine and demo diverge structurally; doing it means a multi-week engine investment
- Estimated cost: 2-4 weeks engine work + extensive testing

**C2. Knockback consumer in sim** *(captured 2026-05-10)*
- Engine has knockback as a stub (in `AILMENT_NAMES`, applied to `active_effects`, but no consumer)
- Demo Phase 8.0.3 implemented knockback as the first real consumer (positional push + stagger)
- When engine eventually gets positional sim (C1 above), knockback consumer should mirror demo's pattern
- Specifically: check `active_effects` for "knockback" entries during action selection in `fight_engine.py:choose_action`; gate movement and skills accordingly
- This is essentially zero work without C1; trivial follow-on if C1 ships
- Estimated cost: ~1 hr if combined with C1

**C3. Convergence-target re-shaping for horde** *(NEW from this discussion)*
- Current convergence: 50% win rate against gauntlet aggregate, binary outcome per class
- ARPG balance: convergence should be density-aware — kills per minute, damage taken per kill, time-to-clear-wave
- This requires the convergence loop itself to be re-designed alongside the multi-target sim
- Only meaningful if C1 ships
- Estimated cost: ~1-2 weeks if C1 ships

### Category D — Content quality (LLM output coherence)

These items aren't about mechanical balance — they're about whether the procedurally-generated *content* (element names, skill names, anchor selection, naming pipeline) produces coherent, evocative, ARPG-appropriate output. Each was surfaced during demo1 playtest as a quality gap, not a bug.

**D1. Seasonal element name quality — collaborative design session needed** *(NEW from this discussion, 2026-05-10)*

**Problem statement.** The engine generates per-season element flavors (e.g., season 1001 renames fire→pitch, wind→thrum, water→brine, earth→basalt). Some of these flavors land beautifully; others produce LLM output that reads as awkward, off-genre, or breaks the player's immersion. Phase 8 playtest surfaced two specific examples:

| Element | Season | Tags | Why it lands wrong |
|---|---|---|---|
| `thrum` (wind) | 1001 (Trench) | deep, vibrating, resonant | Not a physical element — auditory abstraction. Hard to visualize in combat ("thrum-bolt"? "thrum-armor"?). Compound formation in names is awkward. |
| `milk` (water) | 1003 (Cathedral of Bone) | white, nurturing, vital | Has a concrete referent but strong non-combat connotations (infant, dairy, weakness, domestic). LLM produces strange flavor text and class names ("Milk-Tongued Cantor", weapons named after dairy). Off-genre for ARPG combat. |

Other borderline cases observed across the 5 seasons:

| Element | Season | Risk |
|---|---|---|
| `tear` (water, 1002) | First Saint's Crypt | Strong emotional connotation; intimate not heroic |
| `exhalation` (wind, 1002) | First Saint's Crypt | Process-oriented abstraction; not visualizable |
| `breath` (wind, 1003) | Cathedral of Bone | Same — process, not material |
| `marrow` (earth, 1002 + 1003) | Multiple | Has clear referent and works in some contexts; borderline acceptable |

By contrast, the elements that consistently work well share patterns:

| Element | Season | Why it works |
|---|---|---|
| `pitch` (fire, 1001) | Trench | Concrete physical material; visualizable; clear fire-variant; compounds nicely in names |
| `basalt` (earth, 1001) | Trench | Same — material, visualizable, fantasy-resonant |
| `brine` (water, 1001) | Trench | Concrete; ARPG-genre-appropriate (sea/preservative/salt) |
| `coal` (fire, 1005) | Ghost Town | Material, visualizable, slow-burn fire makes mechanical sense |
| `bone` (earth, 1003) | Cathedral | Concrete, fantasy-resonant, compounds in names |
| `char` (fire, 1004) | Mad King | Concrete state of matter; aggressive fire-flavor |
| `dust` (wind, 1005) | Ghost Town | Material wind variant; visualizable |
| `throne` (earth, 1004) | Mad King | Concrete + thematic (heavy stone, power) |
| `gold` (earth, 1005) | Ghost Town | Concrete material with strong fantasy/ARPG resonance |

**Pattern.** Good element flavors share these properties:
1. **Concrete physical referent.** The word names a thing you can hold/see, not a process or abstraction.
2. **Visualizable in combat.** Player can imagine "X-bolt" or "X-armor" without reaching.
3. **Fantasy/heroic associative space.** Word fits ARPG genre vocabulary (basalt, bone, char, frost — yes; milk, tear, breath — no).
4. **Strong compound formation in names.** "Frostbone Ranger" rolls; "Milkbreath Cantor" doesn't.
5. **Combat-compatible connotations.** Word doesn't drag the LLM toward soft/intimate/medical/domestic associations.

**Generator architecture (from current code).** Seasonal element flavors are generated via the anchor-driven LLM call producing replacement words for fire/wind/water/earth canonical elements. The current pipeline doesn't filter for the above properties; it uses the LLM's free-association from the season anchor's description. So season anchors with intimate/abstract themes (Cathedral of Bone, First Saint's Crypt) produce intimate/abstract element words (milk, tear, breath, exhalation), which then propagate through skill names, class names, gear flavor text, etc.

**Two design directions to discuss.** Both have tradeoffs.

**Option I — Curated allow-list of element-candidate words.**
- Maintain a list of ~50-100 vetted element flavors per canonical element (fire/wind/water/earth)
- Generator picks from the allow-list based on anchor theme; LLM doesn't free-associate
- Pros: predictable quality; bad cases impossible
- Cons: less variety long-term; requires curation maintenance; loses some emergent fits

**Option II — Scoring function on free-associated candidates.**
- LLM produces N candidate flavors per element per season
- Each candidate scored on: concreteness, visualizability, fantasy-fit, compound-formability, non-combat-connotation-penalty
- Above-threshold candidates are kept; below-threshold rejected; LLM re-rolls if all fail
- Pros: preserves emergent variety; scales without curation; can learn from regressions
- Cons: scoring function is itself a design problem; harder to reason about why a word landed well/poorly

A hybrid approach is also possible: small allow-list as a known-good fallback, scoring function as the primary path. Most generations score above threshold; if all candidates score low, fall back to allow-list.

**Decision points for the design session.**

1. **Allow-list vs scoring vs hybrid?** (Recommendation: hybrid — allow-list as floor, scoring as primary.)
2. **What's the test set?** Concretely: which words *must* score above threshold (good cases like basalt, pitch, char) and which *must* score below (known-bad: milk, thrum)? Without a labeled test set, the scoring function is hand-wavy.
3. **Who labels the threshold?** This is taste-driven content design. Probably Matt + small set of trusted reviewers.
4. **Existing seasons with bad elements — regenerate or live with?** Season 1001 has thrum; 1003 has milk. Demo1 plays through these. Two options:
   - Regenerate seasons that fail the new quality bar (means demo1 baseline data changes; affects gear pools, abilities, naming everywhere)
   - Live with current seasons as "demo1 baseline" with known-bad elements; new seasons (1006+) use the new generator
   - Recommended: live with current. Regenerating breaks demo1's testing baseline for marginal content quality gain.

**Estimated cost.** Design session ~1-2 hours of conversation; implementation depends on chosen direction:
- Allow-list: ~1-2 hrs to curate + ~1 hr generator change
- Scoring: ~3-5 hrs to design + ~2-3 hrs generator change + ongoing tuning
- Hybrid: ~3-6 hrs total

**This is engine-side work; not a demo concern.** Ships before next season generation batch. Combines naturally with other engine queue items in a single session.

**D2. Class kit composition with shaped-balance philosophy — major Engine 1 architectural upgrade** *(reframed twice 2026-05-11)*

**Design philosophy shift Matt landed:** balance should emerge from kit composition variety, not from `damage_modifier` scaling. Current engine relies heavily on the convergence loop adjusting `damage_modifier` (range 0.05-1.9× observed for hunters) to balance classes that share uniform kit shapes. Two hunters at modifiers 0.05× and 1.5× have the SAME kit shape and differ only in per-ability damage numbers — that's spreadsheet differentiation, not mechanical-identity differentiation.

Shaped balance instead: classes differ by kit *shape* (element distribution, geometry mix, AOE coverage, role coverage). Damage_modifier becomes a fine-tune lever; kit composition is the primary balance dimension. ARPG genre convention (PoE skill gems, D2 build variety) demonstrates this is the better long-term direction.

**Required generator additions:**

1. **Element distribution model per archetype.** Replace single-element-per-class with dominant + secondary distribution. E.g., fire_mage = 60% fire + 30% one secondary (thematically-affined: fire→wind OR fire→earth, NOT fire→water) + 10% another.
   - Affinity rules: fire ↔ wind/earth; water ↔ earth/wind; earth ↔ fire/water; wind ↔ fire/water; physical → any.
   - Side effect: ability name vocabulary diversifies naturally because LLM sees genuinely different element-flavor inputs per skill.

2. **Kit composition templates per archetype.** Define what axis coverage the kit MUST have:
   - Fire_mage: ≥3 fire skills, ≥1 AOE, ≥1 control, ≥1 defensive, ≥1 utility
   - Hunter: ≥4 single-target/ranged_physical skills, ≥1 AOE for tactical option, ≥1 mobility/escape
   - Hybrid_mage: heavier AOE coverage (3-4 of 6), broader element distribution
   - Etc., per-archetype
   - Constraint preserves archetype identity while enforcing diversity within identity

3. **Cycling/diversity enforcement within kit fill.** When filling slots, track axis coverage so far; bias subsequent picks toward unfilled diversity quotas. Reject same-axis-combination duplicates unless intentional spam+spender pair (Diablo Bone Spear + Bone Spirit pattern; same geometry, different cost/cooldown curves).

**AOE bias for pack-combat (revised 2026-05-11 per genre research):** Diablo 3 / 4 / PoE confirm AOE is the default clear meta; single-target is a specialist niche. Per-archetype AOE coverage targets:

| Archetype family | AOE share of kit |
|---|---|
| Controllers (fire/earth/wind/water) | 60-75% (heavy AOE; matches genre default for controllers) |
| Single-element mages (fire/water/etc.) | 40-55% (PoE/D4 elementalist standard is AOE-heavy) |
| Hunters, snipers | 20-30% (Lightning Arrow / Multishot / Tornado Shot are genre meta) |
| Warriors, brawlers | 40-50% (cleave + AOE spender is standard 2H warrior) |
| Skirmishers, rogues | 25-35% (Whirlwind / Cyclone are skirmisher meta) |
| Hybrid_mage | 65-80% (broadest area presence) |

**Original numbers were too conservative.** These revised shares only converge cleanly IF the gauntlet rewards AOE — see B10 below for the corresponding gauntlet restructure. The two levers must be co-designed; AOE skew alone without gauntlet density change will fail because convergence pulls back toward single-target.

**B6 EXTENSION — Hierarchical Skill Tree with Dimensional Threading (added 2026-05-11 per Section 4 Q4.3 closures):**

Each class kit is generated as a TREE structure (not a flat skill list). Tree structure encodes archetype identity through multiple dimensions: mathematical (power tiers + rank thresholds), geometric (parent-child unlocks), thematic (chains), color (chain palettes), power curves (tier-specific coefficients).

**Tree structure:**
- **4 TIERS (vertical / power axis):**
  - Tier 1 — Primaries (3-5 skills, spammable, available L1)
  - Tier 2 — Mids (3-5 skills, medium cost)
  - Tier 3 — Advanced (2-4 skills, build-defining)
  - Tier 4 — Keystones (1-3 skills, ultimates)
- **2-4 CHAINS (horizontal / thematic axis):**
  - Each chain runs vertically through some/all tiers
  - LLM-named thematic continuity + color palette coherence
  - **Chain count varies per class** (specialists 2 chains × 4 tiers; generalists 4 chains × 3 tiers; asymmetric depths allowed) — supports archetype emergence

**Hierarchical unlock gates:**
- Tier 1: L1 always
- Tier 2: ≥3 ranks invested in any Tier 1 parent skill
- Tier 3: ≥5 ranks invested in any Tier 2 parent skill
- Tier 4: ≥8 ranks invested in any Tier 3 parent skill

**Cross-chain unlock asymmetry (encodes archetype identity):**
- **Multi-element classes** (hybrid_mage, etc.): ANY Tier N parent skill unlocks Tier N+1 (cross-chain investment counts)
- **Single-element classes** (fire_mage, water_mage, etc.): Only SAME-CHAIN Tier N parent unlocks SAME-CHAIN Tier N+1 (strict chain investment)
- This **mechanically encodes archetype identity into the skill tree structure**

**Smooth rank cap (preserved):**
- `rank_cap_per_skill = min(15, floor(level/3.33))`
- L17 → cap 5; L33 → cap 10; L50 → cap 15
- Combined with tier gates: Tier 4 unlocks naturally around L27

**Tier-specific scaling coefficients:**
| Tier | scaling_coefficient | Per-rank power gain |
|---|---|---|
| Tier 1 | 1.05-1.08 | Modest |
| Tier 2 | 1.08-1.12 | Moderate |
| Tier 3 | 1.12-1.18 | Strong |
| Tier 4 | 1.18-1.25 | Very strong (keystone payoff) |

**Generator scope additions (extends B6 above):**
- Determine class element distribution (single vs multi) → locks cross-chain unlock rule
- Pick chain count + depths per archetype (variance allowed; novel archetypes emerge)
- Per-skill metadata: `tier` (1-4), `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- Tree validation: chain structure consistent; per-chain tier coverage; aggregate kit-size in 10-15 target

**LLM naming pipeline additions:**
- Chain-coherent skill naming (Tier 1 chain anchor + tier-progression naming)
- Context: chain affiliation + tier + parent skills + element flavor
- Same call count (~12-15 names/class); richer thematic continuity (e.g., Spark → Fireball → Inferno → Phoenix Reborn)

**B14 multi-band convergence integration:**
- Per-band optimal distribution computed against TREE (not flat skill list)
- Tier-unlock constraints checked at each band (e.g., L17 optimal can't max Tier 4 because rank cap = 5)
- Spirit Guide recommends paths through tree per band

**Demo/UI implications:**
- Skill tree visualization (D4-style branching, Last Epoch per-skill tree, or tier-row layout)
- Show unlock state per tier (locked/unlocked)
- Investment ranks visualized
- Chain color tinting for visual grouping

**Body-swap interaction:**
- At Trial or Death body-swap, new class has its OWN tree structure (potentially different chain count, tier shape, cross-chain rules per class element distribution)
- Player's earned SP is RESET across new tree (per B9c body-swap reset trigger)
- Spirit Guide recommends starting distribution on new tree for current band

**Estimated cost increment beyond B6 base:** ~1-2 weeks engine (tree structure in generator + tree-aware convergence + per-tier validation) + ~3-5 days demo (tree visualization UI). Bundled with B6 / B9 / B14 in Stage A2 (per file 16 restructure 2026-05-12).

**B10. Gauntlet restructure to match ARPG genre density (NEW 2026-05-11; co-designed with B6 AOE targets)**

**Architectural conflict identified:** the current gauntlet structure (originally 1v1 per wave; demo1 Phase 9.5a added packs client-side) does not give the engine balance loop sufficient density to reward AOE classes. AOE coverage targets in B6 will fail to converge — classes will either underperform with AOE-heavy kits or balance loop will push toward weaker AOE variants — unless the gauntlet itself matches genre-correct density.

**Genre research findings** (Diablo 3 Greater Rifts, Diablo 4 Nightmare Dungeons, Path of Exile mapping):
- Mob density target: ~80-100 monsters per minute of clear in dense layouts
- Composition: ~70% trash + ~20% magic/mid + ~10% elite/rare/named
- Pack scale: 5-15 mobs per encounter "room" typical
- Time-to-clear per trash room: 5-15 seconds in meta builds
- Boss fights stay 1v1 across all three genre touchstones

**Proposed gauntlet shape (per generated "act," replacing current 7-wave linear gauntlet):**

| Room type | Count per act | Density | Clear-time target |
|---|---|---|---|
| Trash-pack room | ~6 | 8-15 swarm/magic mobs | 5-15s |
| Magic-pack room | ~2 | 1-3 magic + 5-8 swarm | 15-30s |
| Elite room | ~2 | 1 elite + 5-8 trash | 30-60s |
| Mini-boss room | ~1 | 1 mini-boss + 3-5 trash | 30-60s |
| Boss room | ~1 | 1 boss (1v1 cinematic) | 30-60s |
| Act-boss room | 1 (final per act) | 1 act-boss (1v1 cinematic) | 60-120s |

**Per-tier rebalance** (refining file 31 Stage 10):

| Tier | HP scale | Damage scale | Count per room | Genre analog |
|---|---|---|---|---|
| swarm | 0.10× | 0.20× | 5-12 per pack | PoE white monsters; D3 trash |
| magic | 0.25× | 0.40× | 1-3 per pack | PoE magic monsters |
| trash | 0.5× | 0.6× | 1-2 per room (mid threat baseline) | (currently "Wave 2 standard") |
| elite/rare | 1.5× | 1.2× | 1 per elite room | PoE rare monsters; D3 elite packs |
| mini-boss | 4.0× | 2.0× | 1 per mini-boss room | (rare reward gate) |
| boss | 8.0× | 3.0× | 1 per boss room | Map boss / Helltide boss |
| act-boss | 10×+ | 3.5× | 1v1 final encounter | Pinnacle boss / Uber boss |

Critical change: swarm tier drops to **0.10× HP / 0.20× damage** (down from prior 0.15 / 0.25 projection) to match "trash dies in 1-2 AOE hits" genre pattern. Swarm count rises to 5-12 per pack.

**Balance loop implications:**
- Convergence loop tests classes against this restructured gauntlet
- AOE classes naturally over-perform vs swarms; balance loop sees this and accepts AOE-heavy kits
- Single-target classes need 1 AOE option to handle swarm rooms cleanly (matches genre — even pure-single-target builds in PoE/D4 carry at least one AOE)
- Act-boss 1v1 cinematic encounters still test single-target capability — kits without single-target burst fail at boss encounters

**Co-design with B6 and B7:**
- B10 (gauntlet structure) sets the testing baseline that B6 (kit composition) is balanced against
- B7 (gear variance check) runs on this restructured gauntlet
- All three must ship together; landing in isolation produces architectural mismatch

**Estimated cost:** ~1-2 weeks engine work (gauntlet generator refactor + swarm-tier integration + convergence loop updates against new structure). Can ship alongside B6 since they touch the same balance loop architecture.

### B10 V1 partial closure — B10.1 shipped at `v1.3-b10-1-structure` (2026-05-13)

**Status: B10.1 complete ✅. B10.2 complete ✅ (`v1.3-b10-2-pack-proxy`, 2026-05-14). B10 V2 (sequential rooms) deferred post-Stage A2.**

**What B10.1 delivered:**

Tier structure shipped and locked. Implemented HP ranges use ±20% variance bands around the spec target:

| Tier | HP range (factor of CLASS_HP_REFERENCE) | Damage scale (via Eff. Attr) | Armor fraction | Skills | Count/room |
|---|---|---|---|---|---|
| swarm | 0.08–0.12× (spec 0.10×) | 0.20× (eff. attr 0) | 0.3–1.0% | 1–2 | 5-12 per pack |
| magic | 0.20–0.30× (spec 0.25×) | 0.40× (eff. attr 20) | 0.8–2.0% | 1–2 | 1-3 per pack |
| trash | 0.40–0.60× (spec 0.50×) | 0.60× (eff. attr 40) | 1.5–4.0% | 2–3 | 1-2 per room |
| elite | 1.25–1.75× (spec 1.50×) | 1.20× (eff. attr 100) | 3.0–7.0% | 3–4 | 1 per room |
| mini-boss | 3.00–5.00× (spec 4.00×) | 2.00× (eff. attr 150) | 6.0–11.0% | 3–4 | 1 per room |
| boss | 6.00–10.00× (spec 8.00×) | 3.00× (eff. attr 200) | 10.0–17.0% | 4 | 1 per room |

`CLASS_HP_REFERENCE = 20,000` (tier-50 class HP reference). `BESTIARY_DISTRIBUTION`: swarm 12, magic 8, trash 12, elite 6, mini-boss 4, boss 2 = 44 total. `"standard"` tier deprecated in new generation; kept in all tables with compat redirect to "trash" in `build_reference_gauntlet()`.

**A3 gauntlet composition (primary convergence driver, L50):**

`build_reference_gauntlet()` now builds a **12-monster tier-diverse pool** (was 10 standard-tier):

| Tier slots | Count | Selection logic |
|---|---|---|
| trash | 6 | Element diversity first, then archetype variety |
| magic | 2 | Element diversity first |
| elite | 2 | Element diversity first |
| mini-boss | 1 | First available |
| boss | 1 | First available |
| **Total** | **12** | Model B (1v1, tier-diverse) |

Within each tier slot: 4-element diversity pass → archetype variety pass → top-off. "standard" monsters redirect to "trash" slots for backward compat. Fallback (non-12 `size` param): element-diverse selection across full bestiary.

**Regen cost:** ~2.4× increase from pre-B10 (12 monsters × 100 fights vs 5-10 × 100). Full regen estimated 29–34 min; smoke (~5 classes, 30 fights) ~2–3 min. To be verified empirically at B10.4.

**B10.2 (shipped ✅ `v1.3-b10-2-pack-proxy`, 2026-05-14 — pack-proxy / Model C):** Adds swarm pack-proxy semantics — `PackProxy` entity with HP = N × swarm_HP (N=8), AOE deals N× damage, single-target deals 1×. Gauntlet composition updated: 6 swarm-pack slots replace 6 trash 1v1 slots (total stays 12, cost neutral). `GAUNTLET_TIER_COMPOSITION` made public. `_make_recompose_gauntlet()` isolates recompose loop from pack-proxy signal distortion. 1286 tests → 1286 tests (no regression). Math decisions: see `design/b10-gauntlet-analysis.md` §12. V1 partial AOE signal confirmed per design/decisions-log.

**B10 V2 (deferred, post-Stage A2):** Sequential-room semantics — class fights N mobs per room with HP/resource carrying forward between encounters. Room clear rate replaces 1v1 win rate as the metric. Required for the spec's stated goal ("AOE classes naturally over-perform vs swarms"). ~3-4× regen cost increase vs V1. Not a vague "later" — see `canonical/16-project-roadmap.md` B10 V2 row.

**B10 V1 limitation (per Discipline #12):** "AOE differential achieved" cannot be claimed until B10 V2 ships. V1 establishes tier-diverse pool structure; V2 adds genre-correct sequential mechanics. Validation reports at B10.4 must use the scoped V1 claim: "tier-diverse pool structure operational; partial AOE signal via pack-proxy (B10.2)."

**Note on 'magic' tier naming (2026-05-13):** In the tier table, 'magic' (0.25× HP / 0.40× dmg) sits BELOW 'trash' (0.50× / 0.60×) in power. This is intentional: 'magic' denotes pack role (small 1-3 mob packs between swarm waves and baseline threats), not PoE's blue-quality convention (which implies stronger than baseline). Spec ordering: swarm < magic < trash < elite. Code comment at tier constants: "magic = mid-pack role, NOT blue-quality stronger-than-baseline."

**Genre-data sources consulted** (2026-05-11):
- [PoE T16 mapping strategy](https://gterahub.com/community/read-blog/4072_mmoexp-poe-the-best-t16-t16-5-mapping-strategy-after-the-corruption-scarab-nerf.html)
- [PoE map mechanics](https://www.poewiki.net/wiki/Map)
- [D4 Nightmare Dungeon meta](https://www.icy-veins.com/d4/guides/nightmare-dungeon-tier-list/)
- [D3 Greater Rift mechanics](https://maxroll.gg/d3/resources/greater-rift-explained)
- [D4 AOE vs single-target community discussion](https://us.forums.blizzard.com/en/d4/t/aoe-vs-single-target-damage/207943)

**B11. Geometry palette expansion — un-defer motion-AOE types + add radial/multi-projectile/fork (NEW 2026-05-11; expanded 2026-05-11 evening after geometry-options review; co-required with B6 + B10)**

**Problem identified:** revised B6 AOE shares (controllers 60-75%, hybrid_mage 65-80%) combined with B6's "no same-geometry duplication unless intentional spam+spender pair" rule **don't fit in the current 7-active-discrete-AOE palette.** Heavy-AOE archetypes need 8-11 AOE slots; with only 7 active-AOE geometries available, kits must repeat or fall back to passive types (aura/totem) more than feels natural.

**Math by archetype:**

| Archetype | Kit size | AOE share | AOE slots needed | 7-AOE palette adequate? |
|---|---|---|---|---|
| Fire controller | 13 | 60-75% | 8-10 | No — repeats 1-3 geometries |
| Hybrid_mage | 14 | 65-80% | 9-11 | No — repeats 2-4 geometries |
| Single-element mage | 12 | 40-55% | 5-7 | Borderline — no variety headroom |
| Warrior | 11 | 40-50% | 4-6 | Borderline |
| Hunter | 10 | 20-30% | 2-3 | Fine |
| Skirmisher | 11 | 25-35% | 3-4 | Fine |

**Current active palette** (from `09-geometry-palette-discussion.md` decisions 2026-05-08):
- Active discrete-AOE (7): cone, circle, line, melee_arc, ground_slam, ground_targeted_circle, beam_channel
- Active passive/persistent (3): aura, totem, persistent_zone
- Active single-target (4): single_target, projectile, ranged_physical, melee_strike
- Active other (2): self_buff, teleport
- Staged Phase 2 (summoner): summon_combatant, ally_target, ally_radius
- **Deferred via 2026-05-08 consumability filter:** whirlwind, dash_attack, leap_strike, trap, counter, wall_construct

**The deferral reasoning is now partly out of date.** The consumability filter rejected motion-defining geometries because "both consumers struggle" (LLM description + Three.js renderer). Since 2026-05-08, demo1 shipped:
- Phase 6 positional combat (real movement architecture)
- Phase 8.2 weapon animations (slash/thrust/cast/shoot)
- Phase 12 Super Pixel Effects pack (rich VFX for motion+AOE compound)

**The infrastructure these geometries needed now exists.** Re-evaluating each:

| Geometry | Status now | Notes |
|---|---|---|
| `whirlwind` | **Un-defer** | Rotating melee AOE while caster moves (classic D2 barbarian; D3 + PoE Cyclone meta). Demo has movement; VFX pack has rotating effects. |
| `dash_attack` | **Un-defer** | Dash through enemies dealing line damage along path (classic ARPG move). Demo has movement; line geometry already exists for visual reference. |
| `leap_strike` | **Un-defer** | Leap to target, AOE on landing (D2 barbarian / D3 monk meta). Demo has movement; ground_slam exists for landing impact. |
| `chain_lightning` | **Add new** | Projectile hits primary then arcs to N nearby targets (PoE Chain support meta). Combines projectile + multi-target dispatch. |
| `ricochet_bounce` | **Add new** | Projectile bounces between enemies (PoE Pierce/Fork hybrid). Single-skill → multi-target. |
| `vortex_pull` | **Add new** | Pulls enemies to point + applies AOE. Controllers benefit; combines positional with AOE. |
| `ring` | **Add new (2026-05-11 evening)** | Donut-shaped AOE — outer radius minus inner radius. Caster-centered (PoE Shock Nova) or ground-targeted. Currently has to be expressed as `circle` with awkward LLM hand-waving; real ring geometry unlocks the Nova archetype properly. |
| `multi_projectile` | **Add new (2026-05-11 evening)** | Radial burst — N projectiles fired simultaneously at distributed angles from caster. Hunter/skirmisher AOE answer (PoE Multishot / Tornado Shot / Spectral Throw meta); without it, ranged-physical archetypes have to lean on cone/line for AOE which feels off-archetype. |
| `fork` | **Add new (2026-05-11 evening)** | Projectile splits into N projectiles on impact (PoE Fork support). Mechanically distinct from `chain_lightning` (which jumps target-to-target) and from `ricochet_bounce` (which bounces). Pairs naturally with the multi-target dispatch infrastructure those two need. |
| `wall_construct` | **Defer further** | Directional barrier requires terrain/path mechanics not yet in sim. Phase 5+ territory. |
| `trap` / `counter` | **Defer further** | Multi-stage state machines; complexity exceeds value at current sim depth. |

**Proposed palette expansion: 9 new AOE-coded geometries** — 3 un-defer (whirlwind, dash_attack, leap_strike) + 6 add-new (chain_lightning, ricochet_bounce, vortex_pull, ring, multi_projectile, fork).

| Bucket | Before (16) | After (25) |
|---|---|---|
| Active discrete-AOE | 7 | **16** |
| Active passive/persistent | 3 | 3 |
| Active single-target | 4 | 4 |
| Active other | 2 | 2 |
| **Total active palette** | **16** | **25** |

The 16-active-discrete-AOE count gives heavy-AOE archetypes comfortable kit-variety headroom (controllers' 8-10 AOE slots draw from 16 geometries, no forced repeats). The "no same-geometry duplication unless intentional spam+spender pair" rule from B6 holds without crunching kit shapes.

**Parameter expansions on existing geometries (cross-cutting; not new geometry types):**

Several "novel-looking" AOE shapes from the 2026-05-11 geometry-options review are better expressed as parameters on existing geometries than as separate geometry types. This expands expressivity without proliferating naming/VFX/sim surface area.

| Parameter | On geometry | Values | Genre reference |
|---|---|---|---|
| `collision_mode` | `line` | `stop_on_first` \| `pierce_all` | Piercing line — PoE Lightning Arrow, Diablo Bone Spear |
| `angle_distribution` | `multi_projectile` | `spread` \| `cardinal` \| `diagonal` \| `star` | Cross/plus, X/diagonal, star/asterisk patterns (FFXIV octagram; certain PoE skills) |
| `sweep_shape` | `melee_arc` | `pie` \| `crescent` | Crescent sweep — curved arc; differentiates weapon types |
| `damage_falloff` | all radial geometries (`circle`, `ground_slam`, `ground_targeted_circle`, `ring`, `vortex_pull`, `aura`) | `uniform` \| `linear` \| `exponential` | Proximity damage — FFXIV proximity AoEs; PoE Nova falloff |

**Why parameters not new types.** Proximity damage falloff is the highest-leverage of these — it retrofits onto every radial geometry as a single per-skill parameter and is one of the cleanest "positioning matters" levers in the genre. Treating these four as parameters keeps the geometry palette at 25 (vs ~31+ if each variant were its own type) and the naming pipeline doesn't have to learn six new vocabulary buckets.

**Second-wave park list (post-B11 geometry extension — B12 letter now reserved for movement speed item below):**

Items the geometry-options review surfaced as worth adding eventually but NOT in B11 scope. Captured here so they don't get lost.

| Item | Why park (not skip) | Trigger to revisit |
|---|---|---|
| `trail` (damage on path) | Genre staple (PoE Storm Brand) and distinct from whirlwind (whirlwind = damage where you ARE; trail = damage where you WERE); but needs persistent ground tracking + time-based fade, more complex than discrete AOE | After B11 ships; pair with persistent_zone refactor |
| `persistent_ring_animated` (expanding/contracting ring over time) | Adds temporal dimension to ring; good for telegraphed player abilities | Ship after B11's `ring` lands; share geometry math |
| `rotating_zone` (sweeping AOE around fixed anchor, clock-hand style) | Channeled-zone variant; distinct from whirlwind (rotates around fixed point, not caster) | Defer; can express as channeled `persistent_zone` variant for now |
| **Telegraphed enemy AOE + asymmetric indicator scaling** | Genre game-feel pattern: player AOE indicator slightly SMALLER than hitbox (edge catches feel generous); enemy AOE indicator slightly LARGER than hitbox (dodges feel narrow). Engine produces hitbox as source of truth; demo renderer scales indicator by per-source asymmetry constant (~0.9× player, ~1.1× enemy). Free demo-side win once telegraphs ship; nests cleanly with proximity-falloff (concentric rings = soft edge). | Requires telegraphed enemy AOE to exist first (B10-adjacent VFX polish item) |

**Explicitly skipped (out of B11 scope):**

| Item | Reason skipped |
|---|---|
| Compound geometries (cone+circle, etc.) | Express as multi-effect skills rather than as a new geometry type — generator picks dual effects with different geometries on same skill |
| `spiral` | Niche in genre, VFX-heavy; benefit-to-cost ratio low |
| `checkerboard` | Almost exclusively enemy/boss mechanic in FFXIV source; doesn't fit ARPG player palette |
| `Pac-Man` (open circle) | Almost exclusively enemy attack pattern; "safe wedge" mechanic is positioning-puzzle territory, not player-ability shape |
| Tethered AoE | Solo game — no other players to tether to. Relevant only when summoner ships (Phase 2 multi-actor sim), and even then is enemy-mechanic shaped |
| Stack mark / Spread mark | MMO/raid mechanics requiring multiple players to stack or spread. Solo game — doesn't apply |

**Implementation cost (revised for 9 geometries + parameter expansions):**

| Bucket | Cost |
|---|---|
| Sim integration for 9 new geometries (~1-2 days each; multi-target dispatch shared between chain_lightning/ricochet/fork) | ~2-3 weeks |
| Parameter additions on existing geometries (collision_mode, angle_distribution, sweep_shape, damage_falloff) | ~3-5 days |
| Generator updates: include new types in archetype-allowed pools; respect new parameters | ~3-4 days |
| LLM naming context for new geometries + parameter variants | ~1 day |
| Demo VFX integration for 9 new geometries (chain/fork share; vortex pull; ring; multi_projectile fan) using Super Pixel Effects pack | ~3-5 days |
| **Total: ~3-4 weeks engine + demo work** | |

**Sequencing:** B11 logically pairs with B6 (kit composition rules need the expanded palette to work) and with C1 (multi-target dispatch in sim — chain_lightning + ricochet + fork all need this; can ship without C1 by demo-side approximation similar to Phase 9.5a AOE splash, but engine-side is cleaner).

**Genre alignment:** all 9 proposed additions have direct genre analogs (D2 Whirlwind, D3 Leap, PoE Cyclone/Chain/Fork/Multishot/Shock-Nova/Vaal Lightning Trap). Their absence from the current palette is a genuine genre-alignment gap, not a design choice. The parameter expansions (piercing line, cardinal/star distributions, crescent sweep, proximity falloff) similarly map to canonical ARPG/MMO patterns rather than invented shapes.

**Required balance loop modifications:**

1. **Recompose-first.** If a class doesn't converge at modifier=1.0, FIRST try alternative kit compositions (different element split, different AOE counts, different geometry mix) before adjusting damage_modifier. Track recomposition iterations.
2. **Tight modifier range.** Constrain final modifier to ~0.7-1.3 (vs current 0.05-1.9). Outside that range signals "kit composition is wrong" not "scale numbers harder."
3. **Diagnostic outputs.** Generation reports kit composition + recomposition iterations + final modifier with reasoning.

**Skill-name dedup at LLM layer becomes secondary safety net.** With kit-composition fix in place, LLM-side exclusion context still useful for the edge case where two slots legitimately converge on same axes (intentional spam+spender pair). Side effect of element-distribution fix: ability names diversify naturally because LLM sees varied element vocabularies per skill, not just fire-fire-fire-fire-fire-fire.

**Sharing of ability names occasionally is fine as side effect** of element distribution — different classes converging on a similar-themed name is genre-acceptable. Explicit dedup within a class kit still desirable.

**Estimated cost:** ~2-3 weeks engine refactor (generator + balance loop) + 1-2 weeks balance re-tune since changing kit composition affects every class's convergence behavior.

**This is bigger than typical Category D content polish. Promoted to Category B6 (architectural Engine 1 upgrade)** — comparable in scope to B5 (legendary gear abilities) and arguably more foundational. Suggest tackling as a focused engine sprint, possibly bundled with B3 (AOE budget rebalancing) since the AOE-coverage rules overlap.

**B12. Movement speed + boots gear slot + complete gear slot audit (NEW 2026-05-11)**

**Problem identified:** engine emits no `movement_speed` field anywhere (classes, monsters, skills). Demo synthesizes speed from `range_profile` via `movement.ts:speedForProfile` (close: 240px/s, medium: 200px/s, long: 160px/s) — which is stat-by-proxy and **contradicts the design directive that all classes can speed run at endgame**. Per `32-progression-design.md` Section 12, movement speed must be:
- Gear-driven (NOT stat-driven; STR/DEX/INT/WIS/VIT/AGI do not affect speed)
- Class-agnostic base value (eliminates `range_profile` coupling)
- Primary source: boots gear slot with movement speed affix

**Current gear schema gap** (per `17-gear-and-spirit-guide-design.md` line 159-167):
- Current effective slots: **weapon, off-hand, helmet/chest/hood/robe, ring, amulet** = ~7 slots
- Missing vs genre standard (D2/D3/D4/PoE all have): **boots, gloves, belt** = 3 missing slots
- Genre 10-12 slot complement vs Reincarnated's 7 is a real ARPG-feel parity gap

**Scope of B12:**

1. **Engine emits `movement_speed` per class.**
   - Single class-agnostic base value at endgame baseline (proposed: ~5 m/s analog, demo-unit TBD)
   - Eliminates `range_profile`-coupled speed at engine level
   - Demo's `speedForProfile` retires (per file 28 demo override map)

2. **Engine emits `movement_speed` per monster tier.**
   - Per-tier baseline (swarm slightly fast / trash baseline / elite slightly slow / bosses slow with mobility ABILITIES instead of speed)
   - Adds to the B10 tier table (HP scale, damage scale, **movement speed scale**)
   - Demo currently invents monster speed client-side

3. **Add boots, gloves, belt to gear slot schema.**
   - Update `17-gear-and-spirit-guide-design.md` § "Slot type" enumeration
   - Update generator + gear pool generation to populate the new slots
   - Update `class_fit_profile` to handle boots/gloves/belt slot eligibility
   - **Backward-incompatible** with existing 5 generated seasons — boots/gloves/belt don't exist in current seasons' gear pools (deferred-via-regeneration when B12 ships)

4. **Boots primary affix: `+% movement speed`.**
   - Generator weights movement-speed-affix probability HIGH on boots (~50-70% of boots have it as a primary roll, similar to D3/D4 boots)
   - Tier-graded affix bands per gear tier (genre median: common +5-10%, rare +10-15%, epic +15-20%, legendary +20-25%)
   - **Hard cap on gear-sourced movement speed: +25% from total gear** (matches D3/D4 standard) — proposed; open in Section 12 discussion

5. **Naming pipeline updates.**
   - Boots / gloves / belt get template names at common/uncommon, LLM names at rare+
   - Visual generation pipeline (eventual) handles boots/gloves/belt visuals — out of immediate scope but flagged

6. **Ailment / debuff interaction.**
   - Slow/chill/root ailments multiplicatively affect player's actual movement speed (proposed; matches D3 model)
   - Open: whether high-MS boots resist slows better (multiplicative) or only flat (additive)

**Estimated cost:**
- Engine: schema additions for new slots + `movement_speed` field + generator updates = ~1-2 weeks
- Demo: remove `speedForProfile` workaround; consume engine-emitted movement_speed; render new gear slots = ~2-3 days
- Season regeneration (mandatory; new slots can't backport to existing pools)
- **Total: ~1.5-2.5 weeks engine + demo + regen**

**Position in queue: ships in Stage A2 (ARPG sprint) alongside B6/B7/B10/B11.** This is foundational ARPG-feel infrastructure — speed-running is endgame-defining; missing slots is genre-parity. Belongs with the coordinated ARPG sprint, not deferred to Stage A4 (B5 legendary abilities) or later. Co-dependency: minimal — B12 is largely independent of B6/B7/B10/B11 mechanics but shares the season-regen cycle.

**Class movement abilities** (whirlwind, dash_attack, leap_strike) are already scoped in B11 — these layer on top of B12's base speed, matching genre.

**Gear resistance affix constraint (added 2026-05-11 per Section 11 closures):** B12 + B5 + future gear regen must ensure **gear can roll resistance affixes summing to ~+45% all-element resistances** across a full equipment loadout. This is required to reach the locked +75% within-season resistance cap (Trial body-swaps contribute +30% max; gear must contribute the remaining +45%). Likely implementation: per-piece resistance rolls on appropriate slots (e.g., chest +8-12% all-resistances, helmet +5-8%, gloves/boots/belt/rings/amulet contributing element-specific or smaller all-resistance rolls). Matches PoE per-piece resistance pattern. **File 17 gear schema needs a resistance-affix specification when this stage ships.**

**B13. Active mobility + telegraphs + evasion package + emergence observability (NEW 2026-05-11)**

**Problem identified:** B11 motion geometries are all OFFENSIVE (whirlwind/dash_attack/leap_strike do damage while moving). The DEFENSIVE/PURE-MOBILITY category — abilities that create separation without damage — is missing from the generator pool. Without it, the procedural class generator cannot emit "dodge-tank" / "kiting-mage" / "berserker-skirmisher" style archetypes that genre players recognize. Active evasion as a mechanical pillar also requires telegraphs (so player has windows to evade) and i-frames (so evasion is mechanically meaningful), neither of which exist in current engine sim.

**Design intent (file 32 § 12.5):**
- **Last Epoch per-class movement model.** Generator picks mobility abilities like every other ability — archetype-appropriate, emerges from generation. NOT universal D4-style Evade.
- **No guaranteed mobility per class.** Generator picks freely; some classes will have mobility, some won't. Preserves emergence-driven design.
- **Engine archetype-emergence observability required.** Surface kit-mobility-composition per-class so novel archetype clusters become detectable from convergence outputs.

**Scope of B13:**

1. **5 new defensive mobility geometries** added to palette (extending B11's offensive motion set):

| Geometry | Damage | Mechanics |
|---|---|---|
| `roll` | No | Short evasion dash; ~0.4s i-frames during animation; short CD |
| `defensive_dash` | No | Directional dash; no i-frames; reposition utility |
| `strafe_mode` | No | Toggle/sustained; movement becomes sideways while channeling main ability |
| `blink` | No | Short-range instant teleport; ~0.1-0.2s functional i-frame during animation |
| `dodge_stance` | Buff | Time-limited buff: +X% evasion (statistical) for duration; layers on top of `DODGE_CHANCE_CAP` |

Active palette expands further: 25 (post-B11) → 30 active types.

2. **Engine emits skill-timing metadata.**
   - `cast_time` per skill (windup before damage applies — enables telegraphs)
   - `damage_resolution_time` per skill (when hitbox resolves; for some skills = cast_time end; for delayed = later)
   - `i_frame_window` per evasion skill (start_offset + duration during which player is untargetable)
   - Demo's hitbox resolution respects these fields

3. **Demo: telegraph rendering.**
   - Enemy AOE shows ground indicator during `cast_time` window before damage applies
   - Indicator color = element/damage type
   - Indicator size = `1.08× hitbox` per asymmetric scaling decision (post-B11 park-list)
   - Player AOE indicator = `0.92× hitbox` (generous edges feel)
   - Trade-off: dense mob counts (B10 swarm tier with 5-12 mobs per pack) may need indicator-throttling to avoid screen clutter — open implementation question

4. **Demo: i-frame respect.**
   - Hitbox resolution checks player's i-frame window; if active, skill misses regardless of position
   - VFX shows "evading" frame (player flickers / dust trail / etc.)

5. **Archetype-emergence observability** (engine-side).
   - Engine output per class includes kit-mobility tag: `none` / `offensive_only` / `defensive_only` / `mixed`
   - Cross-class clustering surfaced in season export: "this season produced N classes with [defensive_only + tank-tier survivability] = emergent dodge-tank cluster"
   - Surface in CLI report when convergence completes
   - Spirit Guide context expanded to include "you appear to be playing a [archetype-cluster] build" for player-facing copy

6. **Slow / chill / root interaction.**
   - Slows still affect positional movement (Section 12.7 ailment question)
   - i-frames do NOT bypass slows (slows are a state, not a hit) — slowed player still moves slowly during their roll
   - Open: does roll-cancel slow effect? Genre split

**Estimated cost:**
- Engine: 5 new geometries + 3 new skill fields (cast_time, damage_resolution_time, i_frame_window) + generator updates + observability output = ~1.5-2 weeks
- Demo: telegraph rendering + i-frame logic in hitbox resolution + asymmetric indicator scaling + archetype-tag display = ~1.5-2 weeks
- Season regeneration (mandatory; new geometries can't backport)
- **Total: ~3-4 weeks engine + demo + regen**

**Position in queue: ships in Stage A2 (ARPG sprint) alongside B6/B7/B10/B11/B12.** This bundles all foundational ARPG-feel infrastructure into one coordinated landing. Co-dependency with B11: defensive mobility geometries extend B11's motion-AOE set; telegraphs + i-frames apply to ALL skills (not just B13's new ones), so demo rendering changes affect every B11 geometry too.

**Co-dependency rationale:** B13 internally couples telegraphs + i-frames + defensive mobility — they ship together or none of them work. Telegraphs without i-frames means evasion is just positional movement (decent but limited); i-frames without telegraphs means players can't anticipate when to use them; defensive mobility without either is useless.

**B14. Multi-band convergence simulator — 3-band act-aligned (NEW 2026-05-11; co-required with B6 + B9 + B10)**

**Problem identified:** Section 1 anti-pattern locked "mid-game balance debt acceptance" as REJECTED. The current convergence loop balances classes ONLY at endgame (single 50% win-rate target). This pattern is industry-standard ("your build comes online at level X") and represents real but-tolerated mid-game balance debt across D2/D3/D4/PoE. Reincarnated explicitly rejects this — convergence must validate classes at multiple progression bands, not just endgame.

**Locked architecture (Section 8 closures 2026-05-11):**

**Option β — 3-band act-aligned discrete convergence:**
- Engine converges classes at **3 band-end levels: L17, L33, L50** (matches the 3-act structure locked in Section 11)
- **9 convergence runs per class** (updated 2026-05-11 per Section 7 Q7.2 doppelganger validation lock):
  - **Kit + variance (6 runs):**
    - L17 × {gear_percentile=0.75} = 1 run
    - L33 × {gear_percentile=0.75} = 1 run
    - L50 × {gear_percentile in [0.50, 0.75, 0.95, 0.99]} = 4 runs (B7 variance check; endgame-only)
  - **Doppelganger validation (3 runs):** class vs its own doppelganger at each band (L17, L33, L50)
    - Catches class-internal balance holes (too defense-heavy can't damage self; too damage-heavy can't survive self)
    - Validation doppelganger at band level (different from runtime player-level mirror per Section 6 Q6.3)
- **Per-band optimal distribution** computed at each band — engine emits 3 "meta builds" per class (early/mid/late) instead of 1
- **Failure handling: recompose-first.** If class fails at a band, engine tries different per-band skill-point distributions before falling back to damage_modifier. If recomposition fails: regenerate class.

**Per-band gauntlet generation (locked, sub-clarification pending):**
- Engine generates a DIFFERENT gauntlet for each band (NOT same-gauntlet-scaled-stats)
- Per-band density per early/mid/late research (file 32 Section 6 reference notes):
  - **L17 band:** pack size 2-4, 90/8/2 trash/magic/elite, ~5% multi-pack overlap, ~5-15 kills/min target
  - **L33 band:** pack size 3-6, 80/15/5, ~15-25% multi-pack overlap, ~15-40 kills/min target
  - **L50 band:** pack size 5-12, 70/20/10, ~40-60% multi-pack overlap, ~80-120 kills/min target
- **Per-band monster pools (LOCKED 2026-05-11):** engine generates SEPARATE monster pool per band (A1/A2/A3 flavored). Matches genre's "5-15 new archetypes per act" pattern. ~3× monster generation LLM cost (~+$1-2/season). B10 + B14 share this generator infrastructure.

**Co-dependency with other B-items:**
- **B6 (kit composition)** convergence loop runs at each band — kit composition recomposition operates per-band
- **B9 (skill point distribution)** optimal distribution computed per-band — Spirit Guide build coach recommends different distributions per progression phase
- **B7 (variance check)** runs at endgame only (4 percentile points) — multi-band doesn't extend B7 (per Section 8 locks)
- **B10 (gauntlet structure)** generates per-band gauntlets — 3 gauntlets per season instead of 1

**Engine sim cost:**
- Convergence runs: 1 → 9 per class (9× increase; updated 2026-05-11 with doppelganger validation)
- Per-class iteration time: ~3-5 min → **~30-45 min**
- Per-season generation (~10 classes): ~30-50 min → **~5-7 hours of compute**
- **LLM cost impact: ZERO from sim work** (convergence is mechanical-only; no LLM calls)
- **LLM cost from per-band gauntlets: ~3× monster generation cost (~+$1-2/season)** — locked at interpretation (b) per Section 8 closures 2026-05-11

**Telemetry packet additions** (per Section 8 + 7 locks):
```
class.convergence_report = {
    'endgame_L50':     {winrate, iterations, dimensions_explored, optimal_distribution},
    'mid_band_L33':    {winrate, iterations, optimal_distribution},
    'early_band_L17':  {winrate, iterations, optimal_distribution},
    'variance_check_L50': {p50, p75, p95, p99},
    'doppelganger_validation': {
        'L17_mirror': {winrate, balanced: bool},
        'L33_mirror': {winrate, balanced: bool},
        'L50_mirror': {winrate, balanced: bool}
    }
}
```

**Position in queue: ships in Stage A2 (ARPG sprint) alongside B6/B7/B10/B11/B12/B13.** B14 IS the architectural foundation for multi-band balance; B6/B7/B9/B10 all extend their mechanics to operate per-band when B14 ships. Cannot ship Stage A2 with endgame-only convergence and refactor later — that's exactly the "mid-game balance debt acceptance" anti-pattern Section 1 rejected.

**Estimated cost:** ~2-3 weeks engine work (convergence loop refactor for multi-band; per-band gauntlet generation; telemetry packet extension). Independent of B6 scope but shares the convergence-loop infrastructure.

**B14.5. Recompose-first iterative tuning loop (NEW 2026-05-12 — design scope expanded during B6 generator-validated work)**

**Problem identified:** The current balance loop uses `damage_modifier` (a single numeric scalar) as the primary tuning lever to converge generated classes to target win rate. Empirical data from `v1.3-b6-generator-validated` (production season 001005) shows post-convergence `damage_modifier` values ranging 0.054–0.317 (~6× spread) for classes that all land at near-equivalent gauntlet win rates. This indicates the balance loop is masking mechanical insufficiencies — physical archetypes need 0.29 modifier while hybrid mages need 0.05 to reach the same target. The numeric scalar is papering over kit-shape variation rather than addressing it.

**Section 1 anti-pattern reminder:** Section 1 of `canonical/32-progression-design.md` locked "shaped balance over numeric balance" as the design principle. Compose first; scale last. damage_modifier should be the *fallback*, not the primary lever.

**Locked architecture (nested loops; design scope 2026-05-12):**

The balance loop structure follows cheap-inner-cycles, expensive-outer-cycles discipline:

```
for each generated class:
    try shaped-balance loop:                       # B14.5 primary (skill-level)
        cycle skill swaps within archetype role pool
        cycle geometry mix within archetype constraints  
        cycle energy/cooldown values within archetype bands
        target AOE distribution as a balance metric
    if still fails:
        cycle element-distribution variations       # B14.5 secondary (class-level)
    if still fails:
        [hook for gear loadout cycling]             # post-Priority-02 / B15-era extension
    if still fails:
        [hook for trait fill cycling]               # post-B9a + trait-affix integration
    if all fail:
        damage_modifier adjustment as last resort   # Numeric safety net
```

**B14.5 deliverable scope:**

1. **Primary loop (skill-level levers, available now from B6 primitives):**
   - Swap skills within archetype role pool
   - Modify energy/cooldown values within archetype bands
   - Swap geometries within archetype constraints
   - Target AOE distribution as a balance metric

2. **Secondary loop (element-distribution variations, available now from generator):**
   - Cycle element mix variations (e.g., 70/30 → 60/40 → 80/20 for the same archetype) and re-run primary loop
   - Outer cycle, fewer iterations than primary

3. **Architectural hooks (scaffolding only, do NOT implement):**
   - Gear loadout cycling hook — extension point for when B15 (Seasonal Sets) and Priority 02 gear architecture are mature enough to be a balance lever. Per `memory/project_trait_architecture.md`, gear cycling has TWO sub-levers: stat affix variation + trait affix variation; the interaction is non-linear and the hook should expose both.
   - Trait fill cycling hook — extension point for when B9a (intrinsic class trait pool) and gear-affix integration ship.
   - Empty function stubs with clear extension points so adding those levers later is plug-in, not redesign.

4. **damage_modifier as last resort:** Only fires after composition options exhausted. Expected outcome: mean-of-means damage_modifier ratio drops substantially because most balancing happens via composition.

**Deferred to later items (do NOT implement in B14.5 scope):**

- **Ability-level recomposition** (within-skill ability set variations): stretch goal; may not be needed if skill-level levers prove sufficient
- **Gear loadout cycling** (full implementation): tied to Priority 02 / B15 completion
- **Trait fill cycling** (full implementation): tied to B9a + gear-affix-integration completion

**Cross-system implications:**

- **B6 dependency:** B14.5 requires B6 generator's primitive library (skill pool, geometry pool, archetype templates) to draw from for composition cycling. Implementing B14.5 before B6 generator-validated would produce weak recompositions — that's why B14.5 was deferred until B6 ships. With `v1.3-b6-generator-validated` tagged 2026-05-12, B14.5 is now unblocked.

- **KI-B6-1 connection:** The wind_controller mirror-match weakness resolved in KI-B6-1 (via per-fight variance Prop 4) is a candidate test case for B14.5. If recompose-first can produce wind_controller variants with more direct-damage skills (rather than relying on per-fight damage variance to paper over the gap), per-fight variance magnitude can dial back from ±25% to ±15%. See `memory/project_ailment_damage_thematic.md` for the alternative path (thematic damage signatures on CC ailments).

- **Memory file reference:** Full architectural and lever-inventory discussion captured in `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md` and (cross-system implications) `memory/project_ailment_damage_thematic.md`.

**Implementation discipline (per Stage A2 working agreement):**

- Surface a design proposal first (markdown doc, modeled on `b6-schema-proposal.md`) before writing code. Lock the nested-loop architecture explicitly before implementation.
- Tag intermediate checkpoints (e.g., `v1.3-b14-5-design`, `v1.3-b14-5-primary-loop`, `v1.3-b14-5-secondary-loop`, `v1.3-b14-5-validated`). Small checkpoints; clean rollback.
- Math analysis before code on each major lever (per the discipline established during KI-B6-1 work — predict expected effect before implementing).

**Estimated cost:** ~1-2 weeks engine work (nested loop refactor; lever cycling implementations; architectural-hook scaffolding; revalidation against full B14 multi-band suite).

**Position in queue:** ships in Stage A2 as the natural follow-on to `v1.3-b6-generator-validated`. B14.5 is the structural fix for the "damage_modifier as primary lever" anti-pattern; it should land before B15 (Seasonal Sets) because B15's set bonuses will be balanced via the new B14.5 loop, not the old damage_modifier-primary loop.

---

### B14.5 V1 — landed 2026-05-12 (`v1.3-b14-5-primary-loop`)

**Status update 2026-05-12:** V1 primary loop shipped. The pattern below is the **canonical balance-loop architecture for all future Reincarnated engine work** — future balance work (B14.5 secondary loop, B15 set balance, future archetypes) extends this pattern; it does not replace it.

**V1 architecture as shipped (additions beyond the original locked architecture above):**

1. **Adaptive quick-estimate.** Before lever cycling, run an adaptive binary search to find a modifier where lever evaluation produces measurable signal. Iterates until WR lands in `[0.30, 0.70]` (signal range — not at 0% or 100% ceiling). Safety cap: 10 iterations. Without this, classes with extreme converged modifiers (e.g., hybrid_mage near 0.054) produce zero lever signal at modifier=1.0 evaluation, breaking the loop.

2. **Direction-aware lever logic.** Lever attempts use the eval_modifier to decide direction:
   - `eval_modifier < 0.30` (MODIFIER_LOW_THRESHOLD): kit too strong → try `reduce_dps` direction (weaken so modifier can rise toward 1.0)
   - `eval_modifier > 3.0` (MODIFIER_HIGH_THRESHOLD): kit too weak → try `increase_dps` direction
   - Between: either direction may help; lever logic chooses adaptively

3. **Hybrid rejection gate (load-bearing for correctness).** After lever cycling, run full damage_modifier binary search. Compare final converged modifier's distance from 1.0 against the eval_modifier baseline distance. If lever-modified version is NOT closer to 1.0, **revert the entire lever sequence** (restore original kit's skills) and re-run binary search on the original kit. New `recompose_outcome = "primary_loop_reverted"` captures these cases.

   Without the rejection gate: lever cycling could accept changes that make the class WORSE (acceptance criterion at eval_modifier WR doesn't perfectly correlate with final converged modifier compression). The gate guarantees V1 either improves or no-ops — never worsens.

4. **Smoke-test mode (`--smoke` CLI flag).** Generates 5 classes / 30 fights/eval / 1 band (L33) / no experimental / skips B14.2/3/4 band passes. ~51 seconds vs ~10 minutes for full regen. Use for in-development lever iteration; full regen reserved for success-metric capture and pre-tag validation.

5. **Doppelganger modifier floor (B14.4 design gap fix).** `_evaluate_doppelganger` runs at `eval_modifier = max(player_class.balance_modifier, DOPPELGANGER_MODIFIER_FLOOR)` (floor = 0.30). B14.4 was calibrated assuming modifiers in a normal range; B14.5 exposed extreme low-modifier classes (hybrid_mage ~0.054) where fights always timeout at balance_modifier → doppelganger wins every timeout via +5% HP with no kit-quality signal. Floor preserves "validate at balanced power" semantics for ~95% of classes; floored value ensures fight resolution for extremes. Uses a separate constant (`DOPPELGANGER_MODIFIER_FLOOR`, not `MODIFIER_LOW_THRESHOLD`) since the two thresholds serve different purposes (lever direction heuristic vs fight resolution guarantee) and may diverge over time. Note: the first fix attempt (modifier=1.0, ignoring balance_modifier) was rejected because it silently changed the gate from "validate at balanced power" to "validate raw damage potential" — a semantic shift, not a bug fix. Lesson codified as engineering discipline #11: semantic-shifting fixes need explicit design decision framing. See `decisions-log.md` 2026-05-12 B14.5 doppelganger gate entry.

**V1 telemetry schema additions (in `convergence_report`):**

```python
"recompose_attempts": [
    {
        "lever": "skill_swap" | "geometry_mix" | "energy_cooldown",
        "band_id": "L17" | "L33" | "L50",
        "role": str,
        "lever_specifics": {...},  # what was swapped to what
        "attempt": int,
        "before_winrate": float,
        "after_winrate": float,
        "delta": float,
        "accepted": bool,
        "rationale": str,  # "reduce_dps", "geometry_rebias_reduce_dps", etc.
    }, ...
],
"recompose_outcome": "primary_loop_converged" | "primary_loop_reverted" | "modifier_fallback" | "skipped_experimental",
"composition_pre_modifier_wr": float,   # V2 conditional-modifier decision data
"composition_sufficient_for_055": bool, # V2 conditional-modifier decision data
"modifier_clamp_observation": {...},    # V1 observe-only; V2 may enforce
```

**V1 known limitations (queued for V2):**

- **Acceptance criterion misalignment with success metric.** Levers accept based on WR shift at `eval_modifier`, not on final converged modifier compression. The hybrid rejection gate catches cases where levers worsen things, but doesn't actively *optimize* for compression. V2 should evaluate-at-converged: each lever attempt re-runs full binary search; acceptance based on modifier distance from 1.0. Cost ~2× per lever attempt but directly targets success metric.
- **Telemetry display ambiguity for reverted classes.** Displayed `final_modifier` for `primary_loop_reverted` outcomes is post-revert (original kit's converged value), not the lever-modified kit's modifier that triggered revert. V2 should also store `final_modifier_post_levers` for external verification.
- **`eval_modifier` as baseline proxy is approximate.** Quick-estimate stops when WR is in signal range, not at exact target. Directionally correct but not precise. V2 evaluate-at-converged eliminates this.
- **Success metric recalibration (2026-05-12).** The original design target ("2-3× max/min spread") used the wrong instrument. The max/min ratio is sensitive to composition variance: when a high-modifier class (hunter at 0.55, physical_warrior at 0.41) improves toward 1.0, the numerator grows and max/min INCREASES even though calibration is objectively better. The canonical metric is **mean |balance_modifier − 1.0| across taxonomy classes** (lower = better). V1 breadth test results on this metric: seeds 1005/1006/1007 showed consistent improvement (+1.5%, +1.7%, +8.1%) vs the pre-B14.5 baseline (~0.859). The max/min target (2-3×) is retired; mean |mod-1.0| < 0.80 is the V2 target. See `decisions-log.md` 2026-05-12 entry.

**V1 engineering disciplines (codified):**

The disciplines used to ship V1 efficiently are codified in `reincarnated-engine/design/working-agreement/engineering-disciplines.md` and `memory/project_iterative_dev_disciplines.md`. They apply across all future Reincarnated engine work — not just B14.5. Core principles: math-before-code on non-trivial changes, smoke-test vs full-regen discipline, no parallel regens of the same seed, right tool for the validation question, attribution clarity, schema validation at boundaries, capture decision telemetry, tag intermediate states, triage discipline, empirical inspection over assumption, **semantic-shifting fixes need explicit framing (#11)** (triggered by the doppelganger modifier=1.0 false fix; see decisions-log 2026-05-12 B14.5 doppelganger entry).

**V2 follow-on (next discrete work item after V1 + smoke-test mode + breadth test):**

- Evaluate-at-converged architecture: each lever attempt re-runs full binary search; acceptance based on `|final_modifier_post - 1.0| < |final_modifier_pre - 1.0|`
- Adds telemetry: `final_modifier_post_levers` always captured
- Resolves the V1 acceptance-criterion misalignment surfaced by class_0005 / class_0008 patterns during V1 validation
- May allow per-fight damage variance to dial back from ±25% → ±15% if compression is strong enough

**V2 deliverable scope (when V2 lands as `v1.3-b14-5-v2`):**

- Replace eval-modifier-based acceptance with converged-modifier-based acceptance
- Update telemetry schema to always capture both pre/post-lever final modifiers
- Re-tune V1 constants (RECOMPOSE_QUICK_ITERS, signal range, direction thresholds) based on V1 empirical data
- Capture decision: do we still need adaptive quick-estimate after V2 evaluates-at-converged? Likely no — the full binary search itself is the "find the converged modifier" mechanism.

---

**B15. Seasonal Sets — class-specific endgame set generation (NEW 2026-05-11 per Section 5 closures)**

**Concept:** at L50 (Act 3 endgame), one **unique class-specific gear set** unlocks per playable class per season. Set pieces are individually rare (legendary-tier or above); set bonuses apply at 2-piece / 4-piece / full-set thresholds. Real seasonal goal: gather your favorite class's weekly seasonal set. Form library trophy value: ascended set-wearing spirits become visible accomplishments + Earth meta-layer event power.

**Scope:**
- **Per-season set generation:** 5-6 sets per season (one per playable class)
- **Per-set piece count:** 5-6 pieces (genre standard for full-set bonus configurations)
- **Total set piece generation per season:** ~25-36 pieces (5-6 sets × 5-6 pieces)
- **Set thematic identity:** all pieces in a set share LLM-named thematic continuity (e.g., "Hearthwind's Pyric [Robes/Helm/Gauntlets/Boots/Belt]")
- **Set affix coherence:** all pieces emphasize the class's primary scaling stat + element + relevant traits
- **Set bonus tiers (mechanically encoded):**
  - 2-piece: stat or damage bonus (+X% element damage, +Y stat)
  - 4-piece: trait or significant power bonus (gain trait T, +X% to relevant ailment chance)
  - Full-set: cast_on_attack ability or major effect (matching B5 legendary mechanical novelty pattern)

**Drop mechanism:**
- Set pieces drop ONLY at L50 content (Act 3 endgame)
- Specific encounter types favor set drops (act-boss / Trial boss kills with elevated set piece probability)
- Drop rate calibrated so a focused L50 player can complete a set in ~3-7 hours of endgame play
- **Cross-season smuggling:** set pieces smuggle to Earth Self storage; can be "worn" by re-ascended forms in future seasons

**Generator scope additions:**
- Per-class set definition: which slots are in the set (typically 5-6 of the 10 gear slots), affix patterns per piece, set bonus mechanics
- Set bonus generation rules per archetype (fire mage set bonus emphasizes fire damage; warrior set emphasizes melee crit; etc.)
- LLM naming pipeline for set name + per-piece names with thematic continuity
- Drop table integration: set piece drops respect tier-availability curves (Section 5 Q5.1) AND specific encounter modifiers

**LLM cost impact:**
- ~25-36 LLM calls per season (set naming + flavor + visual prompts)
- ~+$1-2 per season (modest within $5-10/season budget)

**Engine integration with B6/B14:**
- B6 (kit composition) doesn't directly touch sets — sets are gear, not skills
- B14 (multi-band convergence) variance check at L50 should account for set-equipped builds AT the high-end gear percentile (95th/99th) — players with full set will be at gear ceiling

**Position in queue: Stage A4 (legendary gear abilities) is the natural home** — B15 ships alongside B5 since both touch legendary-tier gear novelty. Could alternatively ship in Stage A2 with B6/B7/B10/B11/B12/B13/B14 if you want sets available from first regenerated seasons, but adds ~1-2 weeks to Stage A2's already-large scope.

**Estimated cost:** ~1-2 weeks engine (set generation + set bonus mechanics + set-specific drop hooks) + ~3-5 days demo (set bonus UI display + completion tracking) + ongoing LLM cost.

**Co-dependency:**
- File 17 gear schema must support set piece membership flag (`set_id`, `set_position`, `set_piece_count_required` for bonuses)
- B5 (legendary mechanical novelty) — set bonuses use similar mechanical patterns (granted_ability for full-set bonuses); shared infrastructure
- **B16 (loot drop architecture) is prerequisite** — B16 provides the random-drop infrastructure that B15 builds on; set pieces ship as a specialized drop class with L50-only band restriction
- Earth meta-layer events (`../collaboration-handoff/34-earth-meta-layer.md`) — set-wearing spirits add identity / power to rift events

**B16. Loot drop architecture (NEW 2026-05-12 per Section 5 implementation gap)**

**Problem identified (Matt's catch 2026-05-12):** Section 5 of file 32 specifies drop architecture in full (per-band rarity tables, ilvl, smart-loot 70/30, monster-level-tied rates) but no B-item explicitly scoped the implementation. The implementation was implicitly assumed to live in Stage A7, but:
- **Playtest Cycle 1 (post-A2)** validates auto-pickup with rarity filter (Section 5 Q5.9 lock) — auto-pickup is testable only if drops happen
- **B15 Seasonal Sets** (Stage A4) requires drop infrastructure to ship set pieces; "drop table integration" was buried inside B15's cost estimate but isn't B15's scope
- **Playtest Cycle 3** validates set collection chase, which requires both B16 + B15 working together
- Current engine state per file 17: "loot drop mechanism doesn't exist; gear catalog is built but never connected to monster kills"

**Decision (LOCKED 2026-05-12 per Option A): ship full loot drop architecture in Stage A2.** Cleaner than splitting stub+full across A2/A7; aligns with "well-oiled before validation" preference; surfaces drop issues during Playtest Cycle 1 rather than after multiple stages have built on top.

**Scope (per Section 5 of file 32):**

1. **Drop event mechanism** — monster death triggers drop roll; spawn gear instance in world
2. **Per-band rarity tables** (Section 5 Q5.1 — already locked design):

| Band | common | uncommon | rare | epic | legendary |
|---|---|---|---|---|---|
| A1 (L1-17) | 70% | 25% | 4% | 0.9% | 0.1% |
| A2 (L18-33) | 50% | 30% | 15% | 4% | 1% |
| A3 (L34-50) | 30% | 30% | 25% | 12% | 3% |

3. **Per-monster-tier drop multipliers** (Section 5 Q5.1):
   - swarm: 0.5× drop probability (cheap fodder)
   - magic: 1.0× baseline
   - trash: 1.0× baseline
   - elite/rare: 1.5× rare-tier drop weight
   - mini-boss: 2× rare+ drop weight
   - boss: 3× rare-tier; guaranteed at least 1 rare
   - act-boss: 10× legendary weight; guaranteed at least 1 epic+; carries pre-converged `carried_gear` (existing Priority 02 mechanism preserved)

4. **Smart-loot 70/30** (Section 5 Q5.5):
   - 70% of drops weight toward player's class fit profile (per `fit_for_class` scoring from Priority 02)
   - 30% pure RNG roll from full gear pool
   - Constant across all bands (no phase shift)

5. **ilvl tracking** (Section 5 Q5.4):
   - Each dropped gear instance stamps `ilvl = monster_level` at drop time
   - ilvl is permanent on the item (preserves across season boundaries for smuggling)
   - Affix-tier eligibility gates on ilvl (Tier-N affix requires ilvl ≥ threshold; matches PoE/LE pattern)
   - Equip requirement: `stat_thresholds (B12 lock) + character_level ≥ ilvl - 3` (slight permissiveness for smuggled gear)

6. **Drop pool integration** — drops sample from the existing per-season gear pool generated by the Priority 02 generator; B16 doesn't generate gear, only DROPS gear
   - Per-class smart-loot uses existing `class_fit_profile`
   - Per-season pool persistence: dropped gear that's not picked up by the player can be re-dropped (no waste)

7. **Drop telemetry hooks** — record drop events to telemetry DB:
   - `drop_events` table: monster_id, player_class_id, band, tier, ilvl, smart_loot_flag, picked_up
   - Enables loot-economy analysis post-implementation
   - Feeds Spirit Guide marginal-value math (Priority 02 mechanism extended)

8. **Demo integration** — drops render in world; auto-pickup with rarity filter consumes them per Section 5 Q5.9 (Stage A2 demo follow-on)

**What's NOT in B16 (deferred to Stage A7 or beyond):**
- **Cross-season smuggling integration** — Section 5 Q5.6 principles are designed (gear retains ilvl, capacity limited); implementation requires Earth meta-layer infrastructure (Stage A7+ / file 34 territory)
- **`*_DROPS_PER_SLOT` per-band budget enforcement in convergence sim** — this is B14's per-band variance-check parameter, not runtime drop architecture; B14 owns it
- **Loot economy validation simulation** — "Priority 15" in old naming; walks a class through L1→L50 and measures equipped-loadout fit; separate item (could be added as B17 if needed)

**Co-dependency:**
- **B10 (per-band monster pools) is prerequisite** — B10's monster tier definitions (swarm/magic/trash/elite/etc.) are what B16 maps to drop multipliers
- **B12 (10 gear slots) is prerequisite** — B16 drops into all 10 slots; missing slots from B12 means incomplete drop targeting
- **B14 (multi-band sim) co-dependent** — B14's variance check at 0.50/0.75/0.95/0.99 percentiles samples from gear B16 dropped during simulation
- **B15 (Seasonal Sets) depends on B16** — set pieces ship as specialized drop class with L50-only band restriction; B16 must ship before B15 can land

**Estimated cost:**
- Engine: drop event mechanism + per-band rarity tables + smart-loot 70/30 + ilvl tracking + drop pool integration + telemetry hooks = **~1-2 weeks**
- Demo: drop rendering in world + pickup interaction + auto-pickup rarity filter UX + Spirit Guide review summary screen = **~3-5 days**
- **Total: ~1.5-2.5 weeks** (Stage A2 scope expansion)

**Position in queue: ships in Stage A2 (ARPG sprint) alongside B6/B7/B10/B11/B12/B13/B14.** Cannot ship before B10 + B12 (its prerequisites); should ship before B14's variance check is meaningful (so gear samples reflect actual drop output, not just generator output).

**Why ship full architecture in A2 (Option A) instead of stub-now / full-later (Option B):**
- Surfaces drop issues during Playtest Cycle 1, when fixes are cheapest
- Avoids the "stub mechanism becomes load-bearing" anti-pattern
- B15 (Stage A4) lands cleanly against finished infrastructure
- Spirit Guide auto-pickup rarity filter (Section 5 Q5.9) gets validated against real drop data, not a stub
- Matt's call 2026-05-12: "well-oiled before validation"

**B7. Gear-percentile variance check — pass/fail gate (NEW 2026-05-11)**

**Current engine state:** primary balance loop already samples gear at 75th-percentile per-fight via `run_batch_geared()` and `sample_scenario_loadout()`. The `damage_modifier` IS calibrated against gear variance at this baseline. So gear-aware balance exists; what's missing is variance-check across the gear distribution.

**Gap identified:** primary loop catches AVERAGE behavior at 75%. Doesn't catch pathological scaling at extreme gear percentiles. Demo1's "hunter with 2× legendary flat-damage items feels OP" is exactly this — class is balanced at 75% baseline; explodes at 95+ percentile gear RNG.

**Proposed addition:** secondary variance-check loop that runs the converged class at multiple gear percentiles and verifies the power curve is smooth (not exponential). Pass/fail gate; reject classes whose scaling breaks at extreme gear values for regeneration.

Specific patterns to flag:
- DPS at 95th-percentile gear > 2× DPS at 75th → flat-damage stacking pathology
- Time-to-kill at 99th-percentile < 30% of time at 75th → critical-damage stack break
- Survivability gap between 50th and 75th > 5× HP equivalent → defense-stacking pathology

**Distinct from B5** (legendary gear abilities are a gameplay feature; B7 is a quality gate).
**Distinct from B6** (B6 is class kit composition; B7 is gear-interaction validation).

**Estimated cost:** ~1-2 days engine work (extend balance loop to run variance check; define pathology thresholds; reject-and-regenerate flow). Could land alongside B6 since both touch the balance loop architecture.

**B9. Traits + skill point distribution as balance dimensions — endgame-baseline model (NEW 2026-05-11; refined to ARPG-genre-correct architecture)**

**Design philosophy:** further reduce reliance on `damage_modifier` by adding TWO new balance dimensions — leveled traits and skill point distribution. The balance loop optimizes BOTH dimensions before falling back to numeric scaling.

**Endgame-baseline framing:** balance against character level 50 (endgame), not character level 1. When progression system ships (Stage A7 per file 16; B14 multi-band sim handles the per-band balance), the engine emits per-band optimal distributions instead of just endgame state; data is structured for this. Each dimension has its own endgame placeholder value (not generic level=1).

### B9a — Trait architecture (level=4 endgame baseline)

**Structure:**
```
class Trait:
    name: str
    effect: TraitEffect           # e.g., +X% fire damage, +Y% crit chance
    min_character_level: int       # acquisition floor: 1, 12, 25, 38 (or similar)
    max_trait_level: int           # typically 4 (4 ranks of investment)
    power_curve: PowerCurve        # per-rank scaling formula
    endgame_value: float           # level=4 (max rank) value used for balance
```

**Design rules:**
- Each trait has a `min_character_level` (when player can acquire it): 1, 12-13, 25-26, 38-39
- Each trait has a `max_trait_level` (typically 4 ranks of investment)
- **Higher-floor traits start more powerful and ramp faster.** A trait unlocked at level 20 reaches peak in 30 levels (50 - 20); a trait unlocked at level 1 has 50 levels to scale gently
- **All eligible traits reach similar power at character level 50.** This is the design intent: endgame characters have balanced trait power regardless of acquisition floor
- Endgame baseline: ALL eligible traits at level=4 (max rank)

**Generator additions:**
- Per-class trait pool (5-10 traits, archetype-appropriate)
- Per-trait acquisition floor (vary across the pool: some level 1, some higher)
- Per-trait endgame-value (calibrated for "similar power at level 50" target)
- Power-curve formula per trait

**Balance loop integration:**

```
For each class:
  1. Generate kit (B6) + gear (existing) + trait pool
  2. Run convergence assuming ALL traits at level=4 (endgame state)
  3. If doesn't converge: try DIFFERENT trait pool composition (swap which traits available, vary floors and endgame values) BEFORE damage_modifier
  4. If trait-pool space exhausted: fall back to damage_modifier as fine-tune
  5. Output class with trait pool + per-trait floor + endgame values + final modifier
```

When progression system ships, engine scales-back: a level 20 character has X traits at their currently-available rank (per their `min_character_level` and per-rank curve). Data structure already supports this; no engine rework.

### B9b — Skill point distribution architecture (120-point endgame budget, variable 10-15 skill kit)

**Endgame budget:** **120 points** at character level 50 — 2 per level (100) + 20 from quests/act-boss completions.

**Per-skill cap:** **15 points** (hard cap, diminishing returns above)

**Math implication:** `120 / 15 = 8 fully-maxable skills`. Every kit size forces meaningful endgame allocation — player commits to ~8 "main" skills regardless of kit size.

**Kit size:** variable per class, 10-15 skills. Becomes a balance/feel dimension:

| Kit size | Cap sum | Budget | Allocation shape | Feel |
|---|---|---|---|---|
| 10 skills | 150 | 120 | 8 maxed + 2 partial/zero | Approachable: skip 2 weak skills |
| 12 skills | 180 | 120 | 8 maxed + 4 partial/zero | Genre baseline: real choices on 4 skills |
| 15 skills | 225 | 120 | 8 maxed + 7 partial/zero | Specialization-heavy: more than half kit unused |

**Per-archetype kit size selection** (generation-time decision):
- "Approachable" archetypes (warrior, brute, simple casters): 10-11 skills
- "Standard" archetypes (single-element mages, hunters, controllers): 12-13 skills
- "Complex" archetypes (hybrid_mage, multi-element specialists): 14-15 skills

**Structure:**
```
class Skill:  # extends existing skill model from B6
    # ... existing geometry/element/role/etc. from B6 ...
    scaling_coefficient: float    # engine-determined per skill; ~1.05–1.20 per point
    max_invested_level: int       # typically 10 (diminishing returns hard-cap)
    
class ClassSkillBudget:
    kit_size: int                 # 10-15, per-archetype determined
    total_endgame_points: int     # 120 (50 × 2/level + 20 quests/bosses)
    optimal_distribution: dict    # {skill_id: points} — engine-balanced meta build
```

**Design rules:**
- Class has 10-15 skills (kit size varies by archetype) + 120-point skill budget at endgame
- Each skill has an engine-determined `scaling_coefficient` (some skills scale faster per point, others slower — primary attacks low coefficient ~1.05; heavy spenders higher ~1.15; ultimates highest ~1.20)
- Each skill caps at `max_invested_level` (10) with hard or diminishing returns
- **Engine optimizes the 120-point distribution as "meta build" for balance reference**
- Player receives 2 points per character level + quest/boss rewards; can distribute meta OR experiment
- For kits >12 skills: meaningful endgame allocation choice (can't max everything); the choice IS the build

### B9c — Build reset mechanism

**Reset triggers (free):**
- Spirit Guide intervention when player is "struggling" (see Struggling heuristic below)
- Body swap (taking defeated Trial boss's identity; full reset implicit in identity change)
- End-game completion (final act boss defeated)
- Refusing body swap when offered (incentive to NOT swap = free guided reset)
- **🆕 Spirit Guide proactive recommendation at act transition** (added 2026-05-11 per Section 7 Q7.3 closures): when player enters a new act, Spirit Guide evaluates the band-meta build vs player's current build; if significant divergence (>30% of SP would need to relocate for new meta), Spirit Guide proactively offers a free reset to align with band-meta. Player can decline — recommendation, not mandate.

**Reset triggers (paid — endgame only):**
- Post-end-game replay: player can pay in commodities (currency, crafting materials, unique resources TBD) to reset and try different builds with the same character. Strict during the core game; paid experimentation post-completion. Genre-correct replay value.

**Reset types:**
- **Guided reset:** Spirit Guide highlights recommended skills on the tree based on shaped-balance optimal distribution (extends Phase 5.5f marginal-value philosophy to skills, not just gear)
- **Unguided reset:** body swap and end-game trigger automatic full reset; player redistributes freely

**Decision locked (Q1):** strict during play (Option A), paid at endgame. Highest build-commitment depth during the core game; ongoing experimentation supported post-completion via commodity cost.

**Struggling heuristic (Q2 framing):** "time spent underperforming against the simulation average, as compared with other players in season." Two reference points combined:

1. **Simulation-average baseline** — the engine knows expected performance for this class + current build configuration (computed during balance loop). Available from Phase 0 onward.
2. **Cohort comparison** — telemetry-driven comparison against other players in same season with similar build + character level. Requires telemetry infrastructure; available from Phase 1+ once telemetry collection is built.

**Composite metric (initial design — refine with playtest):**
- Track cumulative time where (player encounter-clear time) > 1.5× (simulation predicted clear time for this build)
- Weight by encounter difficulty (failing an act-progression encounter weights heavier than a side encounter)
- Once cohort data is available, add: time where player's cumulative XP/hour < 25th percentile of cohort with similar build at similar level
- Composite trigger: 15+ minutes accumulated underperformance in last hour of play, OR 3+ deaths to encounters where simulation-predicted clear-rate > 80%, fires Spirit Guide intervention
- Single-session cooldown on Spirit Guide intervention (don't spam — once offered per session unless explicitly dismissed and player continues struggling)

**Implementation phasing:**
- **Phase 0 (current engine):** simulation-average-only. "You're 30%+ behind the predicted clear pace for this build" triggers Spirit Guide.
- **Phase 1 (telemetry infrastructure added):** add cohort signal. "You're slower than 75% of similar builds at this point."
- **Phase 2 (refined):** contextual triggers across multiple metrics; intervention timing tuned per playtest data.

**Cohort comparison requires telemetry infrastructure** — demo1 has no telemetry collection; Vercel deployment is read-only. Telemetry would be a separate Phase 1 / Engine 2 item: anonymized per-player metrics (encounter completion times, deaths, build distribution, etc.) sent to a backend. Significant additional scope; defer until needed.

**Spirit Guide as build coach** — design philosophy:
- Spirit Guide already has marginal-value math for gear (Phase 5.5f)
- Extension to skills: same shaped-balance philosophy — engine knows the optimal distribution from the balance loop (per-band via B14), so it can recommend
- UI surfacing: highlight recommended skill point allocations on the tree at reset moments; show "current vs recommended" delta similar to gear's "Strong/Solid/Marginal/Sidegrade/Downgrade" signal
- Per Section 7 Q7.3: proactive recommendation surfaces at act-transitions AND reset moments; auto-reset recommendation when >30% SP divergence from band-meta

**Estimated cost for B9b + B9c:** ~4-5 weeks engine work (data structures + generation + balance loop integration + Spirit Guide skill-recommendation engine + UI surfacing). Larger than original 60-point estimate because of the 120/variable-kit complexity + reset mechanism + Spirit Guide extension.

**Generator additions:**
- Per-skill scaling coefficient (engine-determined during generation)
- Per-skill max-invested cap
- Class skill point budget (120 at endgame per B9b lock — 100 from levels + 20 from Trial body-swaps)
- Optimization output: best-fit 120-point distribution for 50% gauntlet win rate at endgame band (B14 produces per-band variants)

**Balance loop integration:**

```
For each class:
  1. Generate kit (B6) + gear (existing) + traits (B9a)
  2. For skill point distribution: engine optimizes 60-point allocation across the 6 kit skills
     - Tries various distributions to find optimal convergence
     - Each skill's effective power = base_power × (1 + scaling_coefficient * invested_points)
  3. If optimal distribution still doesn't converge: re-roll per-skill scaling coefficients
  4. If coefficient space exhausted: fall back to damage_modifier
  5. Output class with kit + traits + per-skill coefficients + optimal distribution + final modifier
```

**Player can diverge from optimal distribution** during play:
- Optimal distribution = engine-balanced 50% win rate at endgame
- Diverge into unconverged builds = either find new builds OR underperform
- Same dynamic as PoE skill tree: engine balances against meta; player choice can over- or under-perform

### Why B9a + B9b together

The combined design space is enormous:

| Dimension | Engine generation choice | Player choice |
|---|---|---|
| Kit composition (B6) | element distribution, geometry mix, AOE coverage | (fixed at generation) |
| Trait pool (B9a) | which 5-10 traits, floor levels, endgame values | (acquired automatically at floor) |
| Skill scaling (B9b) | per-skill coefficients, max caps | distribute 60 points |
| Gear (existing) | 75th percentile sampling | actual gear from drops |
| damage_modifier | fine-tune lever | (transparent to player) |

A class with 7 traits × varied floors + 10-15 skills × varied coefficients + 120-point distribution + Hierarchical Skill Tree structure (tier-unlock gates + cross-chain asymmetry per element distribution) has thousands of combinations to explore in the balance loop. damage_modifier becomes a LAST-resort fine-tune, hopefully in tight range (0.85-1.15).

**Estimated cost:** ~4-6 weeks engine work total (data structures + generation + balance loop refactor for both B9a and B9b + LLM contextualization for trait names + optimization algorithm for skill point distribution). Larger than B6; smaller than C1.

**Sequencing:** B9a + B9b probably build together (one architectural sprint). Logically follows B6 (kit composition is the foundation that B9 layers on top of). When B9 ships, file 29's "shaped-balance philosophy" reaches full architectural realization.

**Player-facing impact:** characters within the same class can play VERY differently based on:
- Which traits the player has unlocked (story state)
- How the player distributes skill points (player choice)
- Gear acquired (drop RNG)

That's genre-correct ARPG identity: same class, different characters, distinguishable by build choices. Exactly the depth Reincarnated needs to differentiate from "spreadsheet game" critique.

**Original framing was wrong.** The naming pipeline producing ~40% skill-name collision was treated as an LLM prompt-tuning problem: force the LLM to use exclusion context. But duplicate names are the symptom; the cause is that the class generator produces kits where multiple skill slots share the same `(geometry, element, role)` axes. Two skills with identical mechanical axes ARE essentially the same skill mechanically — just with different damage numbers and cooldowns. Forcing different name strings papers over functional redundancy.

**Real solution: enforce kit-level mechanical diversity at generation time.** Two paths, applied together:

**Path A — Expand the axis set the generator works in.** Current axes are geometry, element, role. Worth adding:
- Temporal pattern: instant / channeled / over-time / delayed-trigger / charged
- Effect category: direct damage / DoT / control / displacement / heal / shield / buff / debuff
- Resource pattern: spam (low cost) / spender (high cost) / situational (long cooldown) / sustain / ult
- Range band per skill (not just per class): melee / short / medium / long

Most impactful per cost-benefit: temporal + effect category. Players feel these directly in moment-to-moment play but the engine doesn't currently differentiate.

**Path B — Enforce diversity per axis across a class's kit.** For a class with K skills (typically 6):
- Element: stable across kit (preserve class identity); allow 1 slot for secondary element (hybrid flavor)
- Geometry: enforce ≥3 distinct geometries across kit (avoid same-geometry redundancy)
- Role: enforce ≥3 distinct roles
- Temporal: enforce mix
- Effect category: enforce mix
- Intentional pairs allowed: spam+spender pairs with same geometry but different cost/cooldown curves (Diablo Necromancer Bone Spear + Bone Spirit pattern) — explicitly permitted exception

The constraint is "diversity per dimension across kit," not "every slot is unique on every axis" (which would force combinatorial explosion).

**Outcome:** classes have distinct mechanical kits per slot, LLM gets distinct substrate to name from (so naming variety emerges naturally), skill-name collision rate drops as side effect, class identity per kit becomes more memorable.

**Constraints to preserve in the diversity enforcement:**
- Class archetype identity. Some archetypes intentionally cluster (snipers project; brawlers melee). Don't force a hunter to have cone+line+self_buff skills — that dilutes archetype identity.
- Per-archetype kit shape templates may pre-constrain which dimensions are diverse vs which are intentionally clustered.

**Engine work required:**
- Refactor class generator to operate in expanded axis space
- Add per-archetype kit-shape templates (which dimensions enforce diversity per archetype)
- Validate generated kits against diversity constraints during convergence
- Surface generation diagnostics (kit-axis-distribution report per generated class)

**Estimated cost:** ~1-2 weeks engine work (significant generator refactor) + 1 week balance re-tune since changing kit composition affects balance loop outputs.

**Promoted from D2 to its own category — this is Engine 1 maturation, not content polish.** Suggest moving to Category B as **B6** alongside other generation-quality work, OR creating new Category E (architectural generation upgrades) if more such items surface.

**D3. Anchor selector duplicate detection** *(partial finding, 2026-05-10)*

- Parallel-batch run produced "The Ghost Town of the Gold Strike" anchor for both seasons 1005 and 1006 (1006 was deleted; 1005 retained)
- Cause: anchor-selector history-awareness disrupted by DB write contention during parallel runs
- Sequential generation prevents this; the bug surfaces only under contention
- Fix: lock anchor-selector history fetch as a single transaction OR enforce sequential generation as the only supported mode
- Estimated cost: ~1 hr DB transaction work; or document sequential-only as official guidance

**D4. Single unnamed class observed** *(captured 2026-05-10)*

- Season 1002 has class_0002 with full mechanical content but template name (no LLM-generated name)
- Naming-layer one-off miss; small
- Fix: investigate naming-layer error handling; ensure no class ever ships with template name
- Estimated cost: ~1-2 hrs investigation + fix

## Sequencing recommendation

**Phase A (bug fixes) — ~3-5 hrs, do first.**
A1 + A2 + A3 + A4. Each is independent, none blocks the others, all are clear-cut. Land them in one engine session before any new season generation. Current 5 seasons stay as demo1 baseline; new seasons ship after Phase A completes.

**Phase B (balance tuning) — ~3-7 hrs for B1-B4; B5 is significantly larger (~1-2 weeks engine + ~2-4 days demo).**
B1 + B2 + B4 are most directly relevant to demo Phase 9.5. B3 is a longer discussion. B5 (legendary gear abilities) is the heaviest item — could be its own engine session OR bundled as "ARPG content quality" with B2 + B3. Recommended order:
1. B2 (ailment chance per skill cost) — Matt has already made the design call (high=100%, mid=35%, low<35%)
2. B4 (trash tier design) — decide engine vs demo-side; if engine, ~1-2 hrs
3. B1 (WIS-on-heal) — design call needed; recommended raise to 0.005 multiplier
4. B3 (AOE budget) — discussion + design before implementation
5. B5 (legendary gear abilities) — design session needed; biggest item by ~10×; consider as standalone engine sprint

**Phase C (architectural) — only if needed.**
The demo's Phase 9.5 (Option B trash adds) may resolve genre-feel sufficiently for demo1 without needing C1-C3. If family playtest #4 reveals horde combat needs deeper sim semantics, C1+C2+C3 become the next major engine investment (multi-week). Otherwise, defer indefinitely — possibly to Phase 5 (summoner) which already requires positional sim.

**Phase D (content quality) — design session first, then implementation, ~5-10 hrs total.**
D1 (seasonal element naming) is the highest-impact item — it touches the texture of the entire season's LLM output. Recommended: design session to lock direction (allow-list vs scoring vs hybrid), then implement before next season generation batch. D2 (skill-name dedup) and D3 (anchor selector) are independent prompt/generator improvements; can land alongside D1 in the same session. D4 (unnamed class) is a small one-off bug. Recommended order:
1. D1 (seasonal element naming) — design session, then implementation
2. D2 (skill-name dedup) — small prompt change, ships alongside D1
3. D3 (anchor selector duplicate) — small DB or doc change, ships alongside D1
4. D4 (unnamed class) — bug fix, ships alongside D1

All four can land in one engine session with focused work; total ~5-10 hrs once D1 design is settled.

## Decision points for Matt

These need answers before the corresponding engine work starts:

1. **Shield magnitude scaling model** (A4): heal-style WIS scaling, HoT-style `damage_modifier` scaling, or generator-emits-tier-scaled magnitudes? (Current recommendation: HoT-style — composes with class-level balance modifier.)

2. **WIS-on-heal multiplier** (B1): raise to 0.005 (75% bonus at 151 WIS), keep 0.002 as utility-stat design intent, or per-skill scaling override?

3. **Trash tier engine support** (B4): engine emits `tier=trash_swarm` variant, or demo-side override of standard trash stats? (Recommendation: demo-side override for Phase 9.5; engine support is forward-compat for demo2/Unity.)

4. **AOE coverage targeting** (B3): generation explicitly weights AOE per archetype, or accept natural distribution? (Recommendation: defer; let demo Phase 9.5 reveal which classes feel under-AOE'd.)

5. **Multi-target dispatch in sim** (C1): commit to multi-week engine investment now, or defer indefinitely (relying on demo to invent semantics)? (Recommendation: defer; revisit after family playtest #4 informs whether the divergence is painful.)

6. **Seasonal element naming approach** (D1): allow-list, scoring function, or hybrid? (Recommendation: hybrid — allow-list as floor, scoring as primary path. But this needs a real design session, not a unilateral call. Bring 10-20 known-good and 10-20 known-bad words; label them; derive scoring rubric from the labels.)

7. **Existing-season element regeneration** (D1 sub-decision): regenerate seasons 1001 (thrum) and 1003 (milk), or live with current as demo1 baseline? (Recommendation: live with current. Regenerating breaks demo1's testing/balance/gear baseline for marginal content quality gain. Apply new generator to 1006+.)

## Demo-engine boundary

This document focuses on engine-side. The demo-engine boundary matters because:

- **Demo Phase 9.5 will invent horde semantics** the engine sim doesn't model (multi-target combat, AOE budget assumptions, swarm trash behavior)
- **This creates short-term divergence** between demo behavior and engine convergence assumptions
- **Long-term, one of two paths**:
  - **Path X**: Engine eventually mirrors what the demo invents (C1-C3 ships) — engine becomes ARPG-aware
  - **Path Y**: Engine stays 1v1-sim — demo and any future visual layers invent ARPG semantics on top, accepting the divergence

Path X is more architecturally clean but expensive. Path Y is cheaper but creates ongoing translation cost between engine and demo (and any future Unity / multiplayer / etc.).

The decision doesn't need to be made until family playtest #4 data is in (after Phase 9.5 ships). If horde combat feels great with demo-only horde semantics, Path Y is fine. If the engine-demo divergence creates concrete pain (balance mismatches, generation produces classes that feel wrong in horde), Path X becomes worth the investment.

## Open questions

- How do we validate ARPG balance? Current convergence loop is 1v1; horde has no equivalent automated test. Family playtest is the only signal source. Worth designing a horde-convergence variant before C1+C3?
- Does engine sim need to model trash AT ALL in horde combat? Trash could be a pure demo-side construct (no engine generation, no engine balance) — they're not "characters" in any meaningful sense, just spawn fodder.
- If we go Path X (multi-target dispatch), what's the migration story for existing 5 seasons? Do they regenerate against the new convergence? Or do they stay as 1v1-baseline content while new seasons use the horde model?
- For D1 element naming — is the element pool *per-canonical-element* (separate lists for fire, wind, water, earth) or *cross-element* (one shared pool with element-fit scoring)? Cross-element allows surprise pairings (frost-as-water-for-Trench, rare-as-earth-for-Mad-King); per-element is simpler to curate.
- For D1 — should historic seasons' element names be retroactively scored as a sanity check on the rubric? If "milk" scores above threshold under a new rubric, the rubric isn't doing its job.

## Status of items

This catalog is current as of 2026-05-10. As items ship or decisions land, update this document. Engine session-level work should reference this doc as the starting point and update it as decisions are made.

Items currently captured in `project_engine_state_findings.md` (memory file): all of A1-A4, B1, B2, plus knockback-stub finding, plus skill-name collision (D2), plus anchor selector duplicate (D3), plus unnamed class (D4). This document supersedes the scattered memory entries for purposes of engine-session planning; the memory file remains the authoritative log of "things we've found" while this doc is the consolidated "things we should decide and do."

D1 (seasonal element naming) is captured here for the first time; previously discussed in conversation but not memorialized as a project artifact.

---

## Demo-side override removal plan

The demo currently carries several **temporary mechanical overrides** that compensate for engine-side issues. Each override has a corresponding engine queue item; when the engine item ships, the demo override should be removed and the demo re-verified against engine-faithful behavior.

This section is the **canonical map** between demo overrides and engine fixes. Engine team should reference this when shipping each fix; demo team should reference this when running cleanup passes post-engine-work.

### Override inventory (current as of 2026-05-10)

| Demo override | Location | Triggered by | Engine queue item that supersedes |
|---|---|---|---|
| Focus restore boost (10 → 25) | `combatant.ts:98` `FOCUS_RESTORE_PER_CAST` | Generator emits focus skill costs 7.9-35.3 against +10 restore | **A1b** (engine: clamp focus costs OR raise restore to ~25 natively) |
| Combo cost clamp (`min(cost, 5)`) | `combatant.ts:effectiveEnergyCost` | Generator emits combo costs 13.7-30 against pool=5 | **A1** (engine: clamp combo costs at pool_max) |
| Pack-grade trash stats (HP×0.18, dmg×0.25) | `combatant.ts:applyPackMultipliers` | Engine doesn't model swarm-tier monsters | **B4** (engine: swarm-tier generation rule) |
| AOE splash radii (hardcoded per geometry) | `main.ts:AOE_RADIUS` table | Engine emits no per-skill `area_radius` | **A2** (engine: per-skill geometry dimensions) |
| Non-melee hit range catch-all (870px) | `movement.ts:RANGE_CAST` | Engine emits no per-skill `range` | **A2** (same as above) |
| Knockback positional consumer | `main.ts:_applyPackKnockbackToActor` | Engine has knockback as stub with no consumer | **C2** (engine: positional sim adopts knockback consumer; demo-side mapping conversion needed) |
| `PX_PER_KNOCKBACK_UNIT = 60` | `main.ts` constant | Engine emits abstract `distance` units | Resolved when **C1** + **C2** land (engine emits pixel-aware values or demo retains mapping by convention) |
| Movement speed per range_profile | `movement.ts:speedForProfile` | Engine emits no `movement_speed` field | **B12** (movement_speed field + boots gear slot + slot audit; ships Stage A2) |
| Phase 7 procedural fallback for body sprites | `archetypeRenderer.ts:drawBody` try/catch | Some archetypes lack Tier 2 LPC pre-composed sprites | Demo-side polish (Phase 10); not an engine concern |

### Removal sequence

**Engine Category A ships (~3-5 hrs):**

After engine team lands A1 + A1b + A2 + A3 + A4:

1. Remove combo cost clamp from `effectiveEnergyCost`. Re-test combo classes — all 6 abilities should be reachable per engine fix.
2. Remove focus restore boost from `FOCUS_RESTORE_PER_CAST` (revert to 10). Re-test focus classes — sustain should match engine spec after engine generator emits compatible costs.
3. Remove AOE splash hardcoded radii — read `area_radius` from skill JSON instead. Re-test AOE abilities per season.
4. Remove non-melee hit range catch-all — read `range` from skill JSON instead. Re-test ability hit detection.
5. Regenerate the 5 seasons with engine A-fixes applied. Update `/public/assets/seasons/`. Re-test full 5-season playthrough.
6. Smoke-test as v0.9.5a.2 or whatever phase number is current; promote.

**Engine Category B ships (~3-7 hrs):**

After engine team lands B1 + B2 + B3 + B4 + B5:

1. Remove pack-grade stat overrides from `combatant.ts:applyPackMultipliers`. Engine now emits swarm-tier monsters with appropriate stats natively; demo just spawns them.
2. Implement consumer-side for legendary gear abilities (Phase B5 ships engine-side; demo needs to render granted abilities + auras + procs). Substantial work; possibly demo2 scope.
3. Re-tune pack-grade composition if engine's swarm-tier feel diverges from demo's manual multipliers.
4. Re-test ailment chance behavior under per-skill scaling (B2). Class identity in pack combat may shift.

**Engine Category C ships (~weeks; only if pursued):**

After engine team lands C1 (multi-target dispatch in sim):

1. Demo's invented pack semantics can defer to engine. Refactor pack tick loop to call engine sim per-pack (if engine supports it) OR keep demo-side invention if engine sim still 1v1.
2. Demo's knockback PX_PER_KNOCKBACK_UNIT conversion can adopt engine's positional convention.
3. Re-validate convergence + balance against engine multi-target outcomes.

**Engine Category D ships (~5-10 hrs):**

After engine team lands D1 + D2 + D3 + D4:

1. Regenerate seasons. New content has improved element names, deduplicated skill names, no anchor duplicates, no unnamed classes.
2. Replace `/public/assets/seasons/` with new content.
3. Re-test full 5-season demo playthrough; LLM-flavor improvements visible.

### Verification rubric for each removal

When removing a demo override:
1. **Confirm engine fix is in current data.** Inspect JSON for the corresponding new value/field. If absent, the engine fix isn't deployed yet; don't remove the demo override.
2. **Add a `BEFORE/AFTER` smoke test.** Capture the override-on behavior; remove override; verify engine-faithful behavior matches expected.
3. **Update tests** (if any) to use engine-faithful values rather than override values.
4. **Search the codebase** for any other reference to the override constant or function. Some demo overrides have follow-on assumptions in adjacent code.
5. **Tag the cleanup commit** with the engine queue item ID: e.g., `Remove demo override [A1]: combo cost clamp`.

### What this section is NOT

This is not a license to ignore demo bugs. **Demo bugs unrelated to engine queue items should be fixed in the demo as they surface.** This section only covers overrides that exist BECAUSE of engine queue items. The demo's job is to be engine-faithful at runtime; overrides are temporary scaffolding while engine fixes wait.

If a demo-side mechanic doesn't have a corresponding engine queue item, it's either:
- A correctly-engine-faithful implementation (no override exists)
- Demo-genuine UX (e.g., LMB controls, room/door state machine — features the engine doesn't model and never will)
- A demo bug (fix it directly; don't add it here)
