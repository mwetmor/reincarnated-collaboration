# BC Bucket-B UNAXISED Rulings — 5 Post-Lock Features

**Type:** design ruling (the gandalf calls the coverage audit routed to me). Item 3 of the BC-orphan family; consumes the structural read (item 2) as its measurability criterion.
**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Triggered by:** coverage audit Bucket B — 5 generation features that map to no existing BC axis, surfaced for a belongs-in-BC vs intentionally-outside ruling. Per Matt's "route the rulings to me," KR captured the inventory and did NOT pre-decide.
**Grounded in (read, this session):** `reincarnated-engine/src/reincarnated/generation/t4_catalog_v2.py` (the actual T4 mechanic definitions + PROVISIONAL magnitudes, lines 30–183) — NOT just KR's one-line glosses.
**Criterion source:** `agentic_orchestration/gandalf/notes/2026-06-13-bc-predicted-vs-measured-structural-read.md` (the predicted-vs-measured framework) + `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3 hybrid cross-axis capture philosophy.

---

## 0. TL;DR — ZERO new axes

All five Bucket-B features are captured by EXISTING axes — most via the lock's own **cross-axis hybrid-capture
machinery** ("hybrid archetypes captured by cross-axis cell-address rather than dedicated bins") — or SPLIT with
their distinctive component intentionally-outside the mechanical archive. **None warrants a new axis.**

| # | Feature | Ruling | Home |
|---|---|---|---|
| 1 | **RETRIBUTION_ENGINE** | **AXISED** | Axis 5 — the `damage-taken-converts` bin EXISTS for exactly this mechanic |
| 2 | **PHASE_MOMENTUM** | **AXISED** (cross-capture) | Axis 1 × 3A × 3B (as built); Axis 4 iframe IF untargetability is intended (design fork) |
| 3 | **GEOMETRY_PROPAGATION** | **AXISED** (cross-capture) + scope note | Axis 2 × 3A × 3B in-fight; cascade invisible to BC (BC panel = 1D boss-duels; cascade unbuilt in both engines) — home is the spatial engine, see §2.3 amendment |
| 4 | **PERSISTENCE_ENGINE** | **AXISED** (cross-capture) | Axis 3A × 3B — same machinery as the lock's charge-up-and-release hybrid |
| 5 | **COMPANION_CONTRACT / MONSTER_PACT** | **SPLIT** | in-fight proxy → Axis 2A; companion meta-identity → OUTSIDE (Earth-meta) |

**Why zero new axes is the disciplined answer, not the lazy one:** the archive is already 68,040 cells at ~1.5%
occupancy. Each new axis MULTIPLIES the space and worsens sparsity — the lock built cross-axis capture precisely
to avoid dedicated bins for hybrids. Pre-imposing a new axis for what cross-capture handles is the substrate-led
discipline violated in reverse. The bar for a new axis is: a build identity that NO combination of existing axes
registers. None of the five clears it.

---

## 1. The criterion (from the structural read)

A feature belongs in mechanical BC only if BOTH:
- **(a) build identity** — it carries a kit-identity dimension the archive should preserve diversity along, AND
- **(b) binnable** — captured by an existing axis (incl. cross-axis hybrid cells), OR a new measurable dimension
  we're willing to build.

Fail (a) → intentionally-outside (document + close). Fail (b) with strong (a) → new-axis candidate (the high
bar). Pass both via existing axes → AXISED (document the mapping, close). The structural read adds the binnability
half: a feature that maps to a behaviorally-realized axis (proxy/resource/tempo/mobility) inherits that axis's
at-risk measurement status and folds into the bounded measurement wave — it does not get a fresh axis.

---

## 2. Per-feature rulings

### 2.1 RETRIBUTION_ENGINE → AXISED (Axis 5, `damage-taken-converts` bin)

**Mechanic (catalog):** `vengeance_pool_accrual_frac: 0.40` of post-mitigation damage taken — damage you absorb
accrues a vengeance pool you spend on offense. This is the canonical **damage-taken-converts** archetype: PoE
Cast-When-Damage-Taken, Diablo barbarian rage-on-hit.

**Ruling:** AXISED — **the lock already has a bin named for this exact mechanic.** Axis 5's 7-bin set includes
`damage-taken-converts`, and the lock's hybrid table lists verbatim: "Damage-taken-converts (CWDT, berserker
rage-on-hit) → Axis 5 (damage-taken-converts bin)." RETRIBUTION_ENGINE is not unaxised at all — it is the
mechanic the bin was designed for. **No new axis.**

**Structural-read inheritance:** Axis 5 is an at-risk behaviorally-realized axis (resource flow is fight-emergent;
the `damage-taken-converts` bin is lock-deferred per § 5). So RETRIBUTION_ENGINE's MEASUREMENT folds into the
bounded Axis-5 measurement-build (structural read priority 2) — it is binned, but its measurement ships with the
resource-economy wave, not separately. This is the case I predicted would depend on the structural read, and it
does: the ruling is "AXISED to a bin that exists but is part of the at-risk measurement wave."

### 2.2 PHASE_MOMENTUM → AXISED (cross-capture) — with a design fork

**Mechanic (catalog):** `stacks_to_phase: 5`, then a 6-second window with `phase_move_bonus: 0.20` +
`phase_damage_bonus: 0.25`. As IMPLEMENTED, the magnitudes show only a **move + damage buff window** — there is
**no untargetability / iframe / evasion parameter** in the config.

**Ruling (as built):** AXISED via cross-capture — Axis 1 (the mobility burst) × Axis 3A (tempo — the window is a
burst-cadence event) × Axis 3B (the +25% damage window is a spiky-amplitude signature, and 3B is MEASURED). A
stack-to-burst-window mechanic; cross-axis cell captures it. **No new axis.**

**Design fork I'm surfacing (not assuming):** KR's gloss said "phase/untargetable-adjacent." If the DESIGN INTENT
is that "phase" confers **untargetability** (the thematically-implied phasing), then PHASE_MOMENTUM ALSO carries
an Axis-4 **avoidance** identity — and that lands on the lock's **deferred** iframe/stealth avoidance sub-mechanism
(§ 3.7 "NO support"). As-built it does not (no avoidance param), so I rule it 1×3A×3B now. **If untargetability is
intended, that is the iframe deferral to revisit — AFTER the Axis-4 bridge proves the measured evasion path**
(the bridge fixes the evasion avoidance term; iframe is the next avoidance sub-mechanism). This is a rocket/gamora
build-intent question, not a new-axis question.

### 2.3 GEOMETRY_PROPAGATION → AXISED (cross-capture) + a BC scope boundary

**Mechanic (catalog):** two variants — CASCADE (corpse-burst: dying enemies burst, 2-tile / 50% damage, recursion
cap 3 generations) and OVERKILL (overkill damage splashes, 50% / 4-tile). Corpse-explosion-chain (Diablo
Necromancer) and overkill-splash (Last Epoch). Genuinely novel vs the lock.

**Ruling:** AXISED via cross-capture for its IN-FIGHT signature — Axis 2 (the AOE geometry, composition-determined
SAFE) × Axis 3B (the cascade detonation is a spiky-variance burst, MEASURED) × Axis 3A (tempo spike on pack
death). **No new axis.**

**The scope boundary worth documenting (the real design observation):** GEOMETRY_PROPAGATION's *distinctive*
identity — the **snowball-clear / chain-reaction-detonator** fantasy — shines in **pack-clear**, and **the BC
archive measures single-encounter (duel/gauntlet) kit identity, not map-clear identity.** In a single-encounter
gauntlet there are few corpses to cascade, so the recursion is largely dormant where BC measures. This is a
genuine SCOPE BOUNDARY of the mechanical BC archive — not a bug, and not a reason for a new axis (you cannot
measure pack-clear without a pack-clear gauntlet, which is a different instrument). Documented so nobody later
expects BC to differentiate clear-speed builds. The detonator identity is real; it lives outside BC's measurement
context, by BC's design.

> **Amendment 2026-06-13 (premise correction — Matt-flagged; conclusion UNCHANGED).** The reason above is
> corrected; the ruling is not. I originally reasoned as if "no pack sim exists" / "you cannot measure pack-clear
> without building a different instrument." **WRONG** — a real 2D spatial pack-gauntlet already exists
> (`simulation/spatial_gauntlet/spatial_engine.py`: positional x/y, AOE-by-radius, `swarm`/`magic_pack`/`elite_pack`/
> `boss_with_adds`). The correct reason GEOMETRY_PROPAGATION is invisible to BC is **two-layer**: (1) BC measurement
> is wired to the **1D `fight_engine` against a fixed 2-boss-tier DUEL panel** (gamora full-corpus run 2026-06-13,
> `simulation/AGENT_STATE.md` Session 4; boss-tier chosen because lesser mobs die to opening burst before landing a
> hit) — the spatial pack-gauntlet is a *secondary* hypothesis-test surface (`spatial_engine` docstring: "R2
> sub-gauntlet … the 1D engine is the primary convergence substrate"), **not on the BC measurement path**; and
> (2) corpse-cascade has **no sim implementation in either engine** (grep: zero on-death-burst code; the only
> on-death machinery is player-proxy fission). So the cascade is invisible to BC because BC reads boss-duels, AND
> the mechanic is unbuilt everywhere. The home for cascade identity is therefore the **spatial engine + its own
> `GauntletArchive`** (a gamora build/measurement question), which *strengthens* "no new BC axis."

### 2.4 PERSISTENCE_ENGINE → AXISED (Axis 3A × 3B cross-capture)

**Mechanic (catalog):** two variants — UPTIME (damage ramps +5%/sec to +40% over 4s of sustained output) and
SATURATION (6 stacks → +25% damage). A **sustained-uptime → damage-ramp** mechanic; the "stand and deliver" /
wind-up archetype (PoE channeling, Charged Dash family).

**Ruling:** AXISED via cross-capture — Axis 3A (tempo: ramp rewards sustained high tempo; interruption resets it,
so it selects for uninterrupted cadence) × Axis 3B (variance: the ramp is a rising-then-flat amplitude shape).
**This is the SAME cross-capture machinery the lock already uses** for "Charge-up-and-release (PoE Charged Dash,
bow-draw) → Axis 3A × Axis 3B." PERSISTENCE_ENGINE is the sustain-inverse of charge-and-release, captured by the
identical cross-axis cell logic. **No new axis.**

### 2.5 COMPANION_CONTRACT / MONSTER_PACT → SPLIT (proxy AXISED; meta-identity OUTSIDE)

**Mechanic (catalog):** the COMPANION family (2). A bound companion / pacted monster fights alongside the kit;
rocket confirms it is modeled via `proxy_combatant` in sim. One ruling covers both per KR's framing.

**Ruling — SPLIT along the kit/meta boundary:**
- **In-fight combat contribution → AXISED to Axis 2A (proxy density).** A companion that fights alongside you IS a
  proxy — an additional combatant acting on your behalf. Mechanically identical to a minion/totem; Axis 2A
  (solo / proxy-light / proxy-heavy) captures it. Axis 2A is the structural read's **priority-1** at-risk axis, so
  the companion's measured combat presence folds into the proxy measurement-build.
- **Companion META-identity → intentionally-OUTSIDE mechanical BC.** *Which* companion you bound (the
  Hall-of-Heroes hero, the cross-season form-library bond) is **Earth-meta-layer identity, not per-kit-internal
  mechanical identity.** The mechanical archive measures "this kit fights with one proxy-companion" (Axis 2A
  proxy-light); it does NOT and should NOT measure "this kit is bound to <named hero>" — that is meta-identity,
  belonging to the form-library / companion meta-layer (a different archive), exactly as the Earth-Self meta-layer
  sits outside per-season kit identity.

**No new mechanical-BC axis.** This is faithful to the Earth-meta architecture: companion-as-proxy is kit (Axis
2A); companion-as-bond is meta (outside). It connects directly to the pending Season-1 bootstrap fiction-
sequencing decision (the Hall-of-Heroes companion commitment) — the companion's meta-identity is exactly the
Hall-of-Heroes layer I'm ruling it into.

---

## 3. Two design observations that fall out (capture, don't lose)

1. **The mechanical BC archive measures single-encounter kit identity, NOT map-clear / pack-clear identity.**
   Surfaced by GEOMETRY_PROPAGATION (and partly companion-swarm). This is a real scope boundary: clear-speed /
   snowball-detonator builds register only weakly in the gauntlet. Not a bug, not a new axis — a documented limit
   of what BC measures. If clear-speed identity ever needs archive coverage, that is a separate pack-clear
   instrument, not an axis on the duel archive.
   **Amendment 2026-06-13 (Matt-flagged):** "a separate pack-clear instrument" — that instrument **substantially
   exists** (`simulation/spatial_gauntlet/`, real packs + positions; secondary R2 hypothesis-test surface with its
   own `GauntletArchive`, off the BC measurement path). So pack-clear / cascade identity is a **gamora spatial-engine
   + spatial-archive** question (implement the on-death cascade; decide whether the spatial archive captures
   clear-speed identity or it merges with BC), NOT a BC-axis question. Corrects "would need a separate instrument" →
   "the instrument exists, off the BC path"; *strengthens* the no-new-axis verdict.

2. **PHASE_MOMENTUM's potential avoidance identity lands on the lock's DEFERRED iframe/stealth avoidance path
   (Axis 4).** The Axis-4 bridge (in flight to rocket) fixes the *evasion* avoidance term; iframe/stealth/
   reflection remain lock-deferred ("NO support"). So the avoidance sub-mechanisms form a natural sequence:
   evasion (bridge, now) → iframe/phase (next, IF mechanics like PHASE_MOMENTUM are intended to confer
   untargetability). Bucket B thus feeds a future Axis-4 avoidance-extension question back to the bridge line.

---

## 4. Roll-up

- **New axes created: ZERO.** All 5 captured by existing axes (4 via cross-axis hybrid cells) or split-with-meta-
  outside (companion).
- **Routes nothing to a new-axis build.** Honors the lock's cross-capture philosophy + substrate-led discipline
  (no pre-imposed axis for cross-capturable hybrids).
- **Folds into existing in-flight work, no new threads:** RETRIBUTION_ENGINE + companion-proxy ride the bounded
  measurement wave (Axis 5, Axis 2A — structural read priorities 2 and 1); the PHASE_MOMENTUM untargetability fork
  + iframe path ride the Axis-4 avoidance-extension sequence behind the bridge.
- **Two boundaries documented:** BC = single-encounter not map-clear; avoidance sub-mechanism sequence
  (evasion → iframe).
- **Open design forks surfaced (not assumed):** (a) is PHASE_MOMENTUM's "phase" intended as untargetability?
  (rocket/gamora build-intent) — gates whether it gains an Axis-4 identity. No other forks.

---

**Signed:** gandalf, 2026-06-13
**For:** ruling the 5 Bucket-B UNAXISED features — ZERO new axes. RETRIBUTION_ENGINE → Axis 5 damage-taken-converts
(bin exists); PHASE_MOMENTUM / GEOMETRY_PROPAGATION / PERSISTENCE_ENGINE → cross-axis hybrid capture (the lock's
own machinery); COMPANION_CONTRACT / MONSTER_PACT → split (proxy AXISED to 2A, meta-identity outside to Earth-meta).
Grounded in the t4_catalog_v2 mechanic definitions; criterion from the predicted-vs-measured structural read.
