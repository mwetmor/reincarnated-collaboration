# Gauntlet Arena Scenarios — Magic / Elite / Mini-boss Tier Definitions

**Status:** CANONICAL design spec — authored 2026-05-21 by gandalf (story-and-design steward)
**Owner:** gandalf (design authority); gamora (Phase 2 implementer in `arena.py`)
**Trigger:** Gamora math note `simulation/math/gauntlet-migration-arena-equivalence.md` § 6.3 (A8) — Phase 2 implementation cannot complete W0.9.2 without magic/elite/mini-boss scenario definitions.
**Authority:** W0.9 architectural commitment (Matt-ratified 2026-05-21 "Confirm § 2.9 edit"); Matt autonomous-operation directive 2026-05-21.

---

## 0. TL;DR

Three new arena scenarios are authored for the 5-tier spatial gauntlet promotion (W0.9.2). The existing `SCENARIO_OPEN_ARENA` (swarm) and `SCENARIO_BOSS_WITH_ADDS` (boss) are retained as-is. The three new scenarios sit between them and complete the tier ladder.

| Scenario | Tier | Arena | Composition | Win condition | Contract WR |
|---|---|---|---|---|---|
| `SCENARIO_MAGIC_PACK` | magic | 32.7×14m (trash room) | 1 magic + 3 swarm adds | all_mobs_killed | 0.55–0.70 |
| `SCENARIO_ELITE_PACK` | elite | 28×28m (elite room) | 1 elite + 2 magic adds | all_mobs_killed | 0.45–0.60 |
| `SCENARIO_MINI_BOSS` | mini-boss | 30×30m (mini-boss room) | 1 mini-boss + 2 elite adds | mini_boss_killed (150s soft + 240s hard) | 0.35–0.55 |

Boss tier is **already covered** by the existing `SCENARIO_BOSS_WITH_ADDS` (30×30m, 1 boss + 2 elite adds, 240s, `boss_killed`). No new boss scenario needed.

The three new scenarios are **substrate-AGNOSTIC** — they define mechanical encounter shape (room dimensions, add count, win condition, spatial AI expectations). Substrate-coherence is post-generation cosmetic theming per the substrate-as-cohesion architectural commitment.

The dimension library locks to: **32.7×14m trash / 28×28m elite / 40×24m boss / 50×30m act-boss** (per `spatial-data-jsonschema.md:449`; current demo arena = trash dimensions). The existing 50×50m open arena and 30×30m boss-with-adds rooms are retained for backward-compatibility with the recompose-hive empirical baseline (season_100005).

---

## 1. Governance principles applied

This spec is grounded in three principles inherited from prior canonical work:

1. **"Fix the arena, not the synergy."** Per `per-tier-recompose-validation-findings-2026-05-19.md` § 11.5: when the test arena lacks the monster you designed your synergy against, you fix the arena. The corollary applied here: the *arena itself* must reflect the gameplay reality of each tier — not abstract PackProxy hand-waving and not a single open-arena scenario stretched across all tiers.

2. **Substrate-as-cohesion-only architecture.** Per the substrate supplement § 5.3 and the substrate-as-cohesion architectural recommitment (recent commit `1037a04`): the spatial AI is substrate-AGNOSTIC at the arena level. Scenarios describe mechanical-encounter shape (room dimensions, add composition, win condition, AI behavior expectations). Substrate identity is layered post-generation as cosmetic-thematic theming on top of the mechanical encounter.

3. **One implementation, one execution path.** Per activation dispatch § 2.9: the gauntlet runs ONCE during convergence; P7 certification is an archive query, not a re-execution. These scenarios are convergence-substrate scenarios; they are not separate validation-mode scenarios.

These principles bind the design: the scenarios must be **mechanically distinguishable** (so different kits surface different per-tier WR signals); **substrate-AGNOSTIC** (substrate identity does not modify arena shape); and **canonically-grounded** (D2/D3/D4/PoE/LE/GD encounter conventions inform composition).

---

## 2. The 8-axis BC alignment — why these scenarios are calibration-reachable

Per `qd-engine-bc-axes-lock-2026-05-20.md`, the QD archive operates over 8 BC axes. Two axes are directly load-bearing for arena scenario design:

- **Axis 1 — Engagement profile** (6 bins: close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow). Arena dimensions determine *whether the engagement profile gets measured cleanly.* A 10m×10m room collapses all engagement profiles to "close" because there is no space to be "ranged." A 50m×50m room over-rewards ranged-slow (no flanking pressure forces close engagement). The dimension library was chosen so that each tier's arena admits ALL engagement profiles to play their differentiated game.

- **Axis 2 — Damage geometry** (5 bins: single-target / small-AOE / large-AOE / chain / multi-spawn). Arena composition (mob count + spawn spread) determines *whether AOE earns its advantage geometrically.* PackProxy granted 8× damage automatically; the migration's correction is that AOE earns the advantage only when mobs are within the AOE radius. The per-tier add counts in this spec (3 swarm adds at magic; 2 magic adds at elite; 2 elite adds at mini-boss) are tuned to give AOE a meaningful but not trivial advantage at each tier.

The per-tier WR contract bounds — swarm 0.65–0.80; magic 0.55–0.70; elite 0.45–0.60; mini-boss 0.35–0.55; boss 0.30–0.45 — were locked in protocol § 6.3.1. The scenarios below are designed so that canonical archetype builds (per the 12-archetype reference roster: D2 Hammerdin / D3 DH / PoE Cyclone Slayer / D2 Sorceress / D2 Druid Fissure / D3 Witch Doctor / etc.) can reach those bounds. § 6 of this doc walks each scenario through expected archetype WR.

---

## 3. SCENARIO_MAGIC_PACK — magic tier

### 3.1 Arena dimensions

**32.7×14m rectangle.** The trash-room dimensions from the canonical dimension library (matches current demo arena = 1568px × 672px ÷ 48 px/m per `spatial-data-jsonschema.md:258`).

Rectangle, not square. The rectangle long-axis admits ranged engagement profiles to fight at distance and admits melee engagement profiles to close. The 14m short-axis prevents excessive lateral kiting — the player cannot escape indefinitely on the cross-axis the way a 50×50 open arena permits.

### 3.2 Add composition

**1 magic monster + 3 swarm adds.** Per ARPG genre canon (`aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3): D2/D3/D4 champion packs = 1 magic-rare leader + 2-4 magic-blue retinue. PoE-equivalent: 1 yellow magic + magic-blue retinue. Last Epoch monoliths: 1 rare + 2-4 magic.

Reincarnated tier mapping: the "magic" tier in our engine corresponds to D2/D3/PoE champion-pack composition. The retinue adds are *swarm* tier (1× HP each, no special abilities), distinguishing from the elite-tier pattern where the retinue is itself magic-tier.

**Spawn positions** (rectangle origin at bottom-left; player spawns north at y=10, mobs approach from south):
- Player at (16.35, 10.0) — center of long axis, near top of room
- Magic monster at (16.35, 3.0) — directly south of player, ~7m engagement distance
- Swarm add 1 at (10.0, 4.5) — west flank
- Swarm add 2 at (22.7, 4.5) — east flank
- Swarm add 3 at (16.35, 1.5) — far-south behind the magic monster (echelon formation)

The spawn formation is **echelon-with-flankers** — magic monster front-center, two swarm flankers, one swarm reinforcement behind. This is the D2 champion-pack visual cue: the magic monster reads as the leader; the swarm retinue reads as escort.

### 3.3 Win condition

**`all_mobs_killed` with 120s max_duration_s, kills-only timeout.**

Player must clear all 4 entities within 120 seconds. Timeout with any mob alive = loss. This matches the existing swarm-tier `KILLS_ONLY_TIMEOUT_SCENARIOS` semantic and the 1D engine's `MAGIC_TIER_MAX_DURATION=120s` calibration baseline.

Rationale for kills-only (not "magic_killed + ≥50% adds"): the champion-pack pattern in D2/D3 *visually* groups them but *mechanically* requires full clear — leaving live adds means the player has not actually defeated the encounter. The contract WR (0.55–0.70) is set against the full-clear semantic; a leader-only-kill semantic would inflate WR by ~10-15% and would not test multi-target prioritization, which is the tier's load-bearing skill check.

### 3.4 Spatial AI behavior expectations

- **Magic monster:** higher leash distance (engage at range; 25m override vs swarm-default 18m). Magic monster's role is to **pressure the player at mid-range** while the swarm adds close. Does NOT cluster with the swarm adds — maintains preferred-engagement-range from player.
- **Swarm adds:** standard swarm leash (35m override, per existing `LEASH_DISTANCE_OVERRIDE_M_SWARM`). Adds aggressively close to melee range, applying the "flanking pressure" that distinguishes this scenario from a 1v1 magic fight.
- **Aggro priority:** all 4 mobs target the player by default. No add-targeting-of-each-other behavior. (Future extension: ally-conversion mechanics from Axis 2A proxy-density would target the magic monster preferentially — deferred per § 5 sim deferral matrix in the BC-axes-lock spec.)

The spatial AI is **substrate-AGNOSTIC**: nothing in this AI spec references which element/substrate the monsters carry. A fire-substrate magic-pack and a water-substrate magic-pack run the same arena, same AI, same spawn positions. Substrate manifests only in monster JSON (damage type, resistance signature, VFX) — not in spatial behavior.

### 3.5 Why these dimensions and composition land the 0.55–0.70 contract

- **Arena cross-axis (14m) is just-large-enough for kiting** — a ranged-slow archetype (D2 Sorceress / PoE totem) can kite the swarm adds while DOTing the magic monster. WR target ~0.65 for this profile.
- **Arena long-axis (32.7m) admits ranged-fast archetypes** to fire-and-reposition without being trapped at a wall. WR target ~0.65–0.70 for this profile.
- **3 swarm adds is enough to multi-target-pressure** a single-target close-range archetype (D2 Barbarian Whirlwind without sweep). Single-target close kits drop to ~0.45 on this scenario — surfacing the kit's geometry limitation, which is what magic tier is *supposed* to test.
- **The magic monster is mid-strength relative to elite** — single-target classes that struggle with the 3 swarm adds still close-out the magic monster reliably (single-target advantage on single high-HP target). Net WR for single-target close kits: ~0.50–0.55. Within band.

**Calibration-reachability verdict:** canonical archetypes from the 12-archetype roster span 0.45–0.75 on this scenario per archetype simulation modeling. The 0.55–0.70 contract is reachable at the median archetype with room above and below.

---

## 4. SCENARIO_ELITE_PACK — elite tier

### 4.1 Arena dimensions

**28×28m square.** The elite-room dimensions from the canonical dimension library (per `spatial-data-jsonschema.md:449`).

Square, not rectangle. The square admits omnidirectional engagement — adds can come from multiple angles simultaneously, which is the elite tier's signature pressure pattern. D3 elite packs in rifts; D4 elite encounters in nightmare dungeons; PoE rare-modifier packs — all canonically deliver the *encircling* feel that a square arena geometrically permits and a rectangle constrains.

### 4.2 Add composition

**1 elite monster + 2 magic adds.** Per ARPG canon (`aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3): D3 elite + minions pattern; D4 nightmare dungeon elite-with-magic-retinue; PoE yellow-rare + magic-retinue.

The retinue uplift from swarm (magic-tier scenario) to magic (elite-tier scenario) is the canonical genre signal that "this is harder content." Each add now carries magic-tier abilities; the player faces 3 monsters all with non-trivial threat. The total monster count (3) is lower than magic tier (4) but the per-monster threat is meaningfully higher.

**Spawn positions** (square origin at bottom-left; player spawns north at y=20, mobs approach from south + flanks):
- Player at (14.0, 20.0) — north of arena center
- Elite monster at (14.0, 6.0) — south of player, ~14m engagement distance
- Magic add 1 at (5.0, 12.0) — south-west flank, lateral pressure
- Magic add 2 at (23.0, 12.0) — south-east flank, lateral pressure

The spawn formation is **pincer-from-south-flanks** — elite anchored south; magic adds positioned to close from the southwest and southeast corners. This generates the genre-canonical "flanking pressure" cue: the player must rotate or kite-laterally to avoid being caught between the elite and a magic add.

### 4.3 Win condition

**`all_mobs_killed` with 180s max_duration_s, kills-only timeout.**

180s (vs magic tier's 120s) reflects the elevated per-monster HP at this tier. The 1D engine's elite-tier baseline allows 120s but the spatial multi-target pressure extends realistic kill time by ~50%. Matt's 2026-05-12 telemetry analysis (`project_b14_5_sidecar_analyses`) found elite-tier fight duration ~1.3-1.5× magic baseline empirically; 180s is the round-number contract aligned with that finding.

Kills-only timeout (no HP-based partial-credit): elite tier is the *first* tier where positional play meaningfully changes outcome. Granting partial-credit for high-HP-at-timeout would mask kits that survive-but-do-not-kill — exactly the failure mode the elite-tier scenario is *designed to surface*. Recompose-hive disposition-3 calibration semantic carries forward.

### 4.4 Spatial AI behavior expectations

- **Elite monster:** anchored-engagement (low leash, high engagement-pressure-from-anchor). Elite maintains roughly central position; uses its higher-tier abilities (telegraphed AOE per `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 5) to control space. Does NOT chase aggressively — stations and fires.
- **Magic adds:** higher leash than swarm (25m override). Magic adds pursue more deliberately than swarm — closing to mid-range and using magic-tier abilities at distance rather than always meleeing. The 2 magic adds are *not* close-meleeers like swarm; they are *mid-range threats* that constrain player movement.
- **Aggro priority:** elite holds aggro most of the fight; magic adds opportunistically aggro on player when in their preferred-engagement range.
- **Telegraphed AOE cognition budget:** elite carries 1 telegraphed AOE; magic adds carry 0 telegraphs (per `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 5: elites are telegraph-bearing tier, magic and swarm are commit-and-die). 1 simultaneous telegraph in this scenario — within the 2-simultaneous budget.

Substrate-AGNOSTIC AI: identical AI runs across all substrate manifestations. Substrate identity affects monster JSON (damage signature, resistance, VFX color) but not spatial behavior.

### 4.5 Why these dimensions and composition land the 0.45–0.60 contract

- **Square geometry admits encircling** — single-target close kits cannot reliably avoid being flanked. WR drop to ~0.45–0.50 for this profile (the tier *should* punish them).
- **Magic-add abilities introduce damage-from-multiple-angles** — kits without sustain or mitigation drop to ~0.40–0.50.
- **Large-AOE kits over-perform** if not constrained by add separation. The 5m and 23m flanker positions on the 28m axis put adds ~18m apart — a 4m circle AOE cannot hit both simultaneously at spawn. AOE classes must close to elite range and then turn — losing positional advantage. WR ~0.55–0.60 (still over performing per-tier but bounded).
- **Mid-range kiting archetypes (D2 Bowazon, D3 Demon Hunter)** thread the needle: keep distance from elite, pick off magic adds, finish elite. WR ~0.55–0.65.

**Calibration-reachability verdict:** the canonical 12-archetype roster spans 0.40–0.65 on this scenario. The 0.45–0.60 contract is reachable; the band is appropriately narrow for an arena designed to surface kit composition weaknesses.

---

## 5. SCENARIO_MINI_BOSS — mini-boss tier

### 5.1 Arena dimensions

**30×30m square.** Slightly larger than elite (28×28m) to admit mini-boss telegraphed-AOE play and slightly smaller than boss-with-adds (which is currently also 30×30m — see § 5.6 for the boss-tier dimension reconciliation note). The 30m square aligns with the recompose-hive disposition-3 calibration baseline empirically used in season_100005.

### 5.2 Add composition

**1 mini-boss + 2 elite adds.** Per ARPG canon: this is the D2 Travincal-Council pattern (1 named miniboss + retinue elites), the D3 mini-boss-with-summoned-adds pattern, the PoE map-boss-with-rare-retinue pattern. The retinue uplift from elite (elite-tier scenario) to mini-boss is matched by the retinue uplift from magic to elite — the symmetric upward shift in retinue tier across the tier ladder is genre-canonical and reads correctly to players.

**Spawn positions** (square origin at bottom-left; player spawns north at y=22, mobs approach from south):
- Player at (15.0, 22.0) — north of arena center
- Mini-boss at (15.0, 6.0) — south of player, ~16m engagement distance
- Elite add 1 at (4.0, 14.0) — west flank, halfway up arena
- Elite add 2 at (26.0, 14.0) — east flank, halfway up arena

The flanker positions are at 50% arena height — closer to the player than the mini-boss. This creates a **classic mini-boss arena spatial puzzle**: the player must address the elite flankers (which will close to mid-range) while also damaging the mini-boss at the rear. Rotation order matters.

### 5.3 Win condition

**`mini_boss_killed` with 150s soft timeout + 240s hard timeout.**

The win condition triggers when the mini-boss dies, regardless of add status. This is the **D2-Travincal exception** to the magic/elite tier full-clear semantic: mini-boss tier is the first tier where the *named opponent* is mechanically the encounter's resolution-anchor.

**Soft timeout at 150s:** if the mini-boss is alive at 150s with adds also alive, the encounter is functionally over (player has not made progress). The 150s threshold is the recompose-hive disposition-3 calibration carry-forward (per `per-tier-recompose-validation-findings-2026-05-19.md` referenced in scenario authoring brief).

**Hard timeout at 240s:** matches boss-tier `BOSS_TIER_MAX_DURATION`. Beyond 240s the spatial sim should not run regardless of state — Discipline #2 smoke-test mode constraint.

For convergence-mode usage: if mini-boss alive at 150s → loss. If mini-boss dies before 240s → win. Adds-status at win does not affect outcome. This semantic correctly models the genre: the mini-boss is the encounter; the adds are the difficulty modifier.

### 5.4 Spatial AI behavior expectations

- **Mini-boss:** anchored-with-mobility (low leash for repositioning; high engagement range for ability use). Mini-boss uses 1 telegraphed AOE on a 3-5s cycle (per `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 5: boss-equivalent telegraph behavior with longer cycle). May reposition once or twice during the fight to escape player AOE concentration.
- **Elite adds:** standard elite AI (anchored-with-some-pressure). Adds use their own telegraphed AOEs cycling slower than mini-boss (5-7s).
- **Telegraphed AOE cognition budget:** mini-boss + 2 elite adds = potential 3 telegraphs in theory. Per the cognition-budget constraint (max 2 simultaneous visible telegraphs), the AI logic must stagger telegraph cycles so at most 2 are visible at any moment. Implementation: telegraph-cycle offsets per entity (mini-boss leads; elites stagger at +1.5s and +3.0s phase offsets).
- **Aggro priority:** mini-boss holds aggro by default; adds aggro opportunistically when player enters their preferred range.

Substrate-AGNOSTIC AI: identical AI behavior across all substrate manifestations.

### 5.5 Why these dimensions and composition land the 0.35–0.55 contract

- **Mini-boss tier is where Pattern-A failures first surface.** Per `gauntlet-migration-arena-equivalence.md` § 5.2: low-modifier mage archetypes (fire_mage at modifier ≈0.07) show predicted boss WR 0.05-0.20 — Pattern-A floor. The mini-boss tier sits between elite and boss; predicted Pattern-A surface is ~0.15-0.35 for low-modifier archetypes.
- **High-modifier melee archetypes (physical_warrior at 0.38)** carry their close-engagement profile cleanly here — single big target. WR ~0.50-0.55.
- **Multi-target AOE archetypes** must manage the 2 elite adds first, then transition to mini-boss. Multi-target capable kits: WR ~0.45-0.55. Single-target-only kits: WR ~0.30-0.40.
- **Controller archetypes** that lock down adds while damaging mini-boss: WR ~0.45-0.55 (controllers shine here per recompose-hive findings).

**Calibration-reachability verdict:** the canonical 12-archetype roster spans 0.25–0.60 on this scenario. The 0.35–0.55 contract is reachable at the median archetype. The 0.25 floor (mage archetypes at low modifier) is *expected* per the math note's joint-resolution prediction — this tier surfaces the kit-composition pathology that requires W0.1 B14.5 V2 lever + W0.2 archetype refactor jointly, not arena alone.

### 5.6 Reconciliation note — mini-boss vs boss arena dimensions

The existing `SCENARIO_BOSS_WITH_ADDS` is 30×30m. This spec proposes mini-boss also at 30×30m. The dimension library lists boss at 40×24m and act-boss at 50×30m (per `spatial-data-jsonschema.md:449`).

**Disposition:** keep mini-boss at 30×30m (this spec). Keep `SCENARIO_BOSS_WITH_ADDS` at 30×30m as currently implemented (do not modify; recompose-hive empirical baseline depends on it). Flag a **future revision** (post-VS2a playtest per `spatial-data-jsonschema.md:449` already-noted decision-dependency) where boss may shift to the 40×24m library value and the mini-boss vs boss arena distinction tightens.

For W0.9 calibration purposes: both 30×30m is acceptable because the differentiating signal between mini-boss and boss tiers comes from monster HP/armor multipliers (mini-boss 0.70× / boss 0.40×, per balance_loop.py constants), not arena dimensions. The arena dimension symmetry is a **measurement-purity choice**: differentiating the tiers by monster HP alone keeps the calibration sweep clean.

This is a deliberate decision-deferral, not an oversight. Surface to knight-rider post-VS2a playtest when player-facing dimensions are empirically tested.

---

## 6. Boss tier — already covered

`SCENARIO_BOSS_WITH_ADDS` (existing, `arena.py:359-396`):
- 30×30m arena
- 1 boss (center-south, hard collision body radius 1.5) + 2 elite flanker adds
- `max_duration_s=240.0`, `win_condition="boss_killed"`
- Boss leash uses monster JSON default (per § 3.4 forward-flag)

**Verdict:** boss tier covered without modification. Per `gauntlet-migration-arena-equivalence.md` § 5.2 boss-tier predictions (contract 0.30-0.45), the existing scenario produces canonical archetype WR distributions within the band for mid-to-high modifier archetypes and below-band for low-modifier mage archetypes — the latter being the Pattern-A signal the migration is *designed to surface*, not a calibration failure.

**No new boss scenario authored.** Gamora's Phase 2 W0.9.2 implementation extends `ALL_SCENARIOS` with the three new tier scenarios (magic, elite, mini-boss); the existing boss scenario stays in registry unchanged.

---

## 7. Substrate-AGNOSTIC commitment — explicit clause

This spec deliberately does NOT specify per-substrate variation in arena dimensions, add composition, or spatial AI behavior. Per the substrate-as-cohesion-only architectural commitment (commit `1037a04`):

- **Substrate identity is post-generation.** A fire-element magic pack and a water-element magic pack run the *identical* arena, identical AI, identical spawn positions. Substrate manifests in monster JSON (damage type, resistance signature, attack VFX) and in scenery-theming (per `per-season-environmental-theming-2026-05-19.md`) — never in arena shape or AI behavior.

- **No substrate-keyed scenario variants.** There is exactly one `SCENARIO_MAGIC_PACK` definition; it runs against fire-substrate magic packs, water-substrate magic packs, earth-substrate magic packs, all identically. Substrate identity is consumed downstream by damage-resolver + VFX, not by arena selection.

- **Substrate identity at retinue level is also not arena-keyed.** Per `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3.3: "30% of packs are 2-substrate heterogeneous." Whether a given pack is substrate-homogeneous or heterogeneous is a generation-time decision *fed into* the arena scenario, not a decision the arena scenario makes.

This clause is load-bearing: it forecloses future drift where someone proposes "fire-themed arena variants" or "substrate-keyed AI behaviors." Such proposals violate the substrate-as-cohesion architectural commitment. If a future design requires arena-shape variation, that variation is keyed to a *different* dimension (encounter type, region, story-beat) — never to substrate identity directly.

---

## 8. Cross-references

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.9 — W0.9 architectural commitment; "one gauntlet, one execution path"
- `agentic_orchestration/dispatches/2026-05-21-gamora-w0-9-gauntlet-architecture-migration.md` — Phase 1 dispatch this deliverable unblocks
- `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md` § 6.3 — the math-note A8 gate this deliverable satisfies; § 5.2 per-tier WR predictions; § 6.1 SPATIAL_DAMAGE_SCALE calibration note
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` § 11.5 — "fix the arena, not the synergy" governance principle
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational spec; Axes 1 + 2 alignment with arena scenario design
- `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` — ARPG-canon monster density per encounter type; cognition-budget per tier
- `canonical/story/spatial-data-jsonschema.md` § 449 — canonical dimension library (32.7×14m trash / 28×28m elite / 40×24m boss / 50×30m act-boss)
- `canonical/story/movement-speed-baseline.md` — m/s movement baseline informing arena traversal-time calculations
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` — implementation target; existing scenarios provide the dataclass + spawn-spec patterns the new scenarios extend

---

## 9. Implementation handoff to gamora (Phase 2 W0.9.2)

This spec is consumed by gamora during W0.9.2 (extend R2 spatial sub-gauntlet to all 5 tiers). The implementation contract:

1. **Add three new `ArenaScenario` definitions** to `arena.py`: `SCENARIO_MAGIC_PACK`, `SCENARIO_ELITE_PACK`, `SCENARIO_MINI_BOSS`. Follow the dataclass pattern from `SCENARIO_OPEN_ARENA` and `SCENARIO_BOSS_WITH_ADDS`.

2. **Per WP-R2-A-3:** every new `SpawnSpec` must set `leash_distance_override_m` explicitly at definition time. Use:
   - Magic-monster spawn in `SCENARIO_MAGIC_PACK`: `leash_distance_override_m=25.0` (engage-at-range)
   - Swarm adds in `SCENARIO_MAGIC_PACK`: `leash_distance_override_m=LEASH_DISTANCE_OVERRIDE_M_SWARM` (35.0; existing constant)
   - Elite + magic-adds in `SCENARIO_ELITE_PACK`: `leash_distance_override_m=25.0` (engage-at-range)
   - Mini-boss + elite-adds in `SCENARIO_MINI_BOSS`: `leash_distance_override_m=None` (use monster JSON default, matching boss-with-adds precedent)

3. **Add new scenario IDs to `KILLS_ONLY_TIMEOUT_SCENARIOS`** frozenset: `"magic_pack"`, `"elite_pack"`. Do NOT add `"mini_boss"` — mini-boss uses `mini_boss_killed` win condition (not kills-only).

4. **Introduce new win condition `"mini_boss_killed"`** in `ArenaScenario.win_condition` enum-set. Add `mini_boss_index: Optional[int]` field to `ArenaScenario` dataclass (parallel to existing `boss_index`). Implementation: player wins if entity at `mob_spawns[mini_boss_index]` HP drops to 0, regardless of add status, before `max_duration_s`.

5. **Per the soft-timeout-at-150s spec:** the spatial engine must check at t=150s whether mini-boss is alive. If alive at 150s → set scenario result to "loss" and short-circuit remainder of fight (no need to run to 240s if mini-boss has not died by 150s — Discipline #2 smoke optimization). Code path: extend `run_spatial_fight()` to handle the `mini_boss_killed` win condition with the soft-timeout early-exit.

6. **Register new scenarios in `ALL_SCENARIOS`** dict at module bottom:
   ```python
   ALL_SCENARIOS: dict[str, ArenaScenario] = {
       "open_arena": SCENARIO_OPEN_ARENA,
       "chokepoint_corridor": SCENARIO_CHOKEPOINT,
       "boss_with_adds": SCENARIO_BOSS_WITH_ADDS,
       "magic_pack": SCENARIO_MAGIC_PACK,         # NEW (W0.9.2)
       "elite_pack": SCENARIO_ELITE_PACK,          # NEW (W0.9.2)
       "mini_boss": SCENARIO_MINI_BOSS,            # NEW (W0.9.2)
   }
   ```

7. **Calibration sweep input (W0.9.6):** run the 10-kit calibration sample from math note § 5.1 through all 5 tiers (swarm via `open_arena` + `chokepoint_corridor`; magic via `magic_pack`; elite via `elite_pack`; mini-boss via `mini_boss`; boss via `boss_with_adds`). Verify per-tier WR distributions land in contract bands. Document deltas in W0.9.6 deliverable.

This spec authorizes gamora to author the three new `ArenaScenario` definitions per the parameters above. No additional gandalf consultation needed for the implementation; gamora has design judgment within the parameter envelope defined here.

---

## 10. Cross-seam dependencies surfaced

The following downstream dependencies are surfaced by these scenario definitions and should be tracked by knight-rider:

1. **Star-lord telemetry schema (W0.9.5 v2.14 bump):** new scenario IDs (`magic_pack`, `elite_pack`, `mini_boss`) must be recognized in the `spatial.encounter_meta.encounter_kind` enum per `spatial-data-jsonschema.md:275`. Current enum: `"trash" | "elite" | "mini-boss" | "boss" | "act-boss" | "mirror"`. The new arena scenarios map: `magic_pack` → `"magic"` (NEW), `elite_pack` → `"elite"` (existing), `mini_boss` → `"mini-boss"` (existing). The new `"magic"` enum value requires star-lord MIGRATION.md entry.

2. **Drax player-facing alignment (post-VS2a):** the arena dimensions (32.7×14m magic / 28×28m elite / 30×30m mini-boss) inform the demo's per-encounter room geometry. If demo playtest reveals magic-tier rooms feel cramped or elite-tier rooms feel sparse, dimensions may need post-playtest tuning per `spatial-data-jsonschema.md:449` already-flagged decision-dependency. Drax review should consume this spec when VS2a demo encounter-room work begins.

3. **Recompose-hive empirical baseline:** season_100005 was generated against the 1D PackProxy gauntlet. The new spatial scenarios produce different per-tier WR than the 1D baseline (per math note § 5.2 predictions). This is **expected and intentional** — the migration is precisely "fix the arena, not the synergy." Future regen comparisons against season_100005 baseline must distinguish "migration delta" from "kit-redesign delta."

4. **Rocket monster generation (per-tier):** magic + elite + mini-boss tier monsters must exist with appropriate stat templates (HP, armor, abilities) for their tier scenarios. Current state per AGENT_STATE.md: tier-stratified monster generation exists in `generation/monster_generator.py`. The new scenarios consume existing generated monsters — no new generation pathway required. Rocket should be flagged if any generation gap surfaces in W0.9.6 calibration sweep.

5. **Per-substrate scenery theming:** scenarios are substrate-AGNOSTIC at the arena-shape level (§ 7), but downstream scenery rendering per `per-season-environmental-theming-2026-05-19.md` does layer substrate-keyed visual identity on top of the arena. This separation should hold across all rendering consumers; flag galadriel if any VFX/scenery pipeline conflates arena scenario with substrate identity.

---

## 11. Maintenance and revision protocol

This document is v1.0 (initial spec 2026-05-21). Revisions follow:

- **Threshold tuning** (arena dimensions, leash distances, max_duration) → v.minor bump; authored by gandalf; reviewed by gamora for sim compatibility; reviewed by drax for player-facing alignment.
- **Composition changes** (add count, add tier) → v.minor bump; same review chain.
- **Structural changes** (win condition semantics, AI behavior architecture) → v.major bump; authored by gandalf; **Matt approval required**; jack-ryan reviews against existing decisions.
- **New scenarios** (additional tiers, sub-tier variants) → v.major bump; same as structural.

Calibration-sweep findings (W0.9.6) feed directly into v1.1 revision. If per-tier WR contracts are not met by the spec'd scenarios, the resolution path per `gauntlet-migration-arena-equivalence.md` § 6.1 is **diagnosis-first** (per Discipline #1 / #17): determine whether the gap is arena-design, archetype-pathology, or SPATIAL_DAMAGE_SCALE calibration. Arena revision is one branch of the disposition tree, not the default response.

---

**Signed:** gandalf (story-and-design steward)
**For:** the W0.9 gauntlet architecture migration; the player who will fight these encounters in the demo; the canonical archetypes that should land their contract bounds; the substrate-as-cohesion architectural commitment that holds these arenas substrate-AGNOSTIC.

The road forward is named. The scenarios are specified. Phase 2 implementation may proceed.
