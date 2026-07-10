# Motion-Frame Substrate Amendment — rotational axes · proxy-behavior family · roster-of-record pin

> **STATUS:** SPEC-CURRENT v1.0 (2026-07-09) — **Matt-ratified in-session, three ruling acts:** (1) *"I agree on F1 through F6 completely"* — the motion-frame amendment moves; (2) *"let's ratify the proxy-behavior family + P0/P1/P2 staging"* — summoning gets its substrate decomposition; (3) **roster-of-record count re-pinned** — demo roster = ALL 25 numbered BC cells + the hypothesis-based kits (incl. proxy/summon + totem, totem contingent on the sim-liveness probe — probe-fail routes to Matt discussion, never a silent drop).
> **Author:** gandalf (SPEC-AUTHOR; ELICITOR grill closed same-session). **Spine source:** Matt's mobile research doc `matt_notes_handoff_docs/reap-die-rise-substrate-addendum-rotational-axes.md` — graduated into canon by this doc (lineage kept in place; its two stale cites corrected below, §1).
> **Companions:** `agnostic-loot-engine-spec.md` (coordinate space of record; §6 coverage search, §7 fairness bands, cost tiers) · `batch2-build-spec-2026-07-06.md` §8 R1 (Axis-5 reserved-empty — UNTOUCHED by this amendment) · `mob-affix-system-spec-2026-07-09.md` (third consumer; §5.1 walls DEFER) · `../current-to-end-state/surface-ledger.md` (E-slate; G1 count amendment) · `../current-to-end-state/current-to-end-state-serial-content-emission.md` §KIT ROSTER (the parseable roster table this doc pins).
> **Corrections of record carried forward:** the coordinate space is **68,040 full lattice / 12,960 live (BC survey)** — the draft-era "~64K decomposition" is a retired myth; do not re-propagate. The addendum's §6/§7 loot-doc cites resolve to the CANON pair, not the superseded draft.

---

## 0. What this is

The trajectory vocabulary had no reference-frame concept — all motion was world-frame. The locked 16-primitive geometry palette covers {transient, persistent} × {static}; **persistent × moving was structurally EMPTY**, and the survivor-like genre built itself on that quadrant (King Bible, Garlic, orbiting emitters), while ARPG canon lives there too (D2 Blessed Hammer, PoE Blade Vortex, D4 Gravitational Ball Lightning, LE's five orbital node-transforms, PoE Storm Brand). This amendment fills the quadrant as ONE parametric family, gives summoning the same decomposition treatment, and pins the kit roster of record.

Decomposition geometry after this amendment: **shape ⊗ motion-frame ⊗ temporal-envelope.**

## 1. F1 — Registry family `rotational_motion_axes` (RULED)

New substrate-registry family (sibling to family 1.5, consumed by it). Seven sub-axes per the graduated addendum, plus the review extensions:

| # | Axis | Domain | Notes |
|---|---|---|---|
| 1 | `reference_frame` | `caster_body` \| `cast_point` \| `autonomous` \| `parent_entity` \| **`target_entity`** *(review extension)* | `cast_point` = Blessed Hammer frame (does NOT follow the caster). `autonomous` composes with EXISTING trajectory axes (wander/seek) — composition, not new axes. `parent_entity` = nested loci. `target_entity` = curse-orbit / mark-satellite (reserved, no v1 cell). |
| 2 | `angular_velocity ω` | signed deg/s, banded | 0 = static satellite ring. v1 constant; time-varying ω = v2. |
| 3 | `radial_velocity dr/dt` | signed units/s | 0 = orbit · + = spiral-out (Hammerdin) · − = spiral-in/collapse. **Sign-flip-over-lifetime (boomerang) reserved v2.** |
| 4 | `orbiter_count` + `phase_spacing` | int + distribution (uniform default) | Genre caps ≈10. Our cap = dual band, §6. |
| 5 | `persistence_mode` | `duration` \| `while_channeling` \| `stack_refresh` \| `until_consumed` | `stack_refresh` = BV pattern (count is the resource). **Shared enum with the proxy family §7 — one lifecycle vocabulary, two consumers.** |
| 6 | `collision_mode` | `pierce_tick(rate)` \| `detonate_on_contact` \| `block_incoming` | `block_incoming` = defensive orbital — **rides the named walls workstream (Q15), not v2-floating.** |
| 7 | `emission_hook` | `none` \| `radial_spawn(cadence)` \| `tangential_release(trigger)` \| `detach_and_seek(trigger)` \| **`zone_spawn(cadence)`** *(review extension — orbiter lays persistent_zone trail)* | Sub-projectiles are ordinary substrate projectiles; recursion via `parent_entity`. **Recursion depth cap: 2.** |

## 2. F2 — Named-bundle primitives in family 1.5 (RULED)

`multi_projectile` precedent: bundles are NAMED PRIMITIVES so the lattice stays rectangular. Consumability status assigned:

| Primitive | Frame/params sketch | Genre anchor | Status |
|---|---|---|---|
| `orbiter_spiral` | cast_point · dr/dt+ | D2 Blessed Hammer (Hammerdin) | **CORE** |
| `orbiter_guard` | caster_body · dr/dt 0 · pierce_tick | VS King Bible, D3 Shuriken Cloud, LE Blade Shield | **CORE** |
| `orbiter_vortex` | caster_body · stack_refresh | PoE Blade Vortex, D4 Gravitational Ball Lightning | CORE-MARGINAL |
| `orbiter_brand` | cast_point/target · pierce_tick | PoE Storm Brand | CORE-MARGINAL |
| `orbiter_bombardier` | ω 0/low · radial_spawn | Winter-Orb-shaped satellite turret | **GATED — totem sim-liveness probe** (E4 lesson: emitted ≠ sim-read). Probe-fail → Matt discussion (roster contingency, §8). |
| spin-channel re-cert | body-as-orbiter degenerate | D2 WW, PoE Cyclone | migration re-certification, §4 |

**Reserves (named re-entries, never silent):** boomerang (v2 dr/dt sign-flip) · epicycle/nested (axis live via `parent_entity`, no v1 cell — legibility+perf) · spiral-in collapse (full-lattice, BC-unattested, never emits v1) · beam-spoke rotating emitter (composition demo first) · detach-and-seek (ORBITIZE operator-family territory) · `block_incoming` (walls workstream).

## 3. F3 — ONE sim kernel (RULED)

One rotational-motion kernel in gamora's `ai_strategies` seam — the canon cost-tier line already prices this: *"transform = new rotation-constraint plumbing in ai_strategies — the expensive tier, built last."* Built ONCE, consumed by every bundle. Math-note-first (Discipline #1); no per-primitive forks.

## 4. F4 — Compile-layer migration, audit-gated (RULED)

Degenerate identities become COMPILE RULES, not separate mechanics (do not regress §7 of the graduated addendum):

- **Aura** = orbiter_count → ∞ ⇒ sim-as-annular-zone, render-as-rotation (threshold compile rule).
- **Nova / expanding ring** = ω 0 · dr/dt+ · high count — existing nova MIGRATES INTO the family; **instant-nova limit case pinned** as a behavior-preservation oracle.
- **Spin-to-win** = frame caster_body, body-as-orbiter, while_channeling + pierce_tick.
- Migration is **behavior-preserving, audit-gated**: the E2 conservation harness pattern is the verifier (throughput + cost-rate conserved across representation change; any lurch = leaked law).

## 5. F5 — Defining vs flavor at the BC-cell layer (RULED)

- **DEFINING (pins per cell):** `reference_frame` · dr/dt CLASS (out/zero/in) · `persistence_mode` · collision CLASS · `emission_hook` presence.
- **FLAVOR (randomizes within cell):** element/sub-element · weapon period/culture form-tokens · count within band (2–8, dual-cap) · ω band · phase distribution. Radius DERIVED from the existing range axis. Nesting admitted-no-v1-cell.
- **Economy mapping (E2 composition):** texture maps to UPTIME — spiky orbital = few heavy loci with down-windows; flat = many weak permanent (King Bible cycling vs evolved Vespers). The k-scalar machinery applies unchanged.

## 6. F6 — Consumers staged + balance integration (RULED)

Three consumers, in order: **(1) kit emission** — orbital cells fire INSIDE the current axis run (post-E3/E4, before the ONE Q14 band re-anchor, so the re-anchor lands once on the full-texture population); **(2) ORBITIZE loot operator** (LE node-transform precedent; one shipped operator v1; §6 coverage + §7 fairness like any operator); **(3) E10 mob affixes** (the mob-affix spec has zero orbit coverage today — third consumer closes it).

Balance pre-registration (BEFORE first orbital gauntlet batch): swept-annulus AOE%-per-second attribution (not cast-shape area) · density-regime sampling (sparse/ring/surround) · blacklist candidates (orbit-stack+detonate-all; emission recursion stacking; spiral-in+detonate on packs) · dual-band count cap = min(fairness, M2 perf), provisional 8–12 · fun-signal calibrated for low-APM always-on spatial control (survivor-like genre proves the fantasy) · emission weight = minority flavor (horde-density legibility) · naming layer signals mechanic first (Ring-, Halo-, Vortex-, Waltz-).

## 7. THE PROXY-BEHAVIOR FAMILY — `proxy_behavior_axes` (RATIFIED 2026-07-09)

**Premise record (what-IS, verified):** eight proxy BC cells named since Sketch A 2026-05-24 (cells 5, 10, 11, 16, 17, 18, 24, 25); deferral flipped in ruling-space (un-gate 2026-06-24; summoner mandate 2026-07-02; E6 in-flight; C2 composite scoring ruled; gen-path landed post-W3-autopsy). **The gap:** `proxy_density` is a COUNT BIN, not a mechanical substrate — and the CURRENT convergence-path sim has NO proxy actor (`spatial_engine.py` zero proxy handling; `ProxySpawn` is generation-side only). *Precision note:* spatial proxy combat WAS specced (`simulation/math/spatial-proxy-combat-spec-2026-06-21.md`) and exercised in the demo-cert path (W2 realized-damage note; the D3 gravecaller finding — ranged archer-proxy parks at 38.9 m, the nav gap in serial tracker PART E) — that lineage is the P1/P2 build's starting substrate, not a contradiction of this gap; `combatant.py`'s PackProxy is mob-side and deprecated (W0.9.1), distinct from player proxies. Three structural forcings: the faction mandate's arithmetic (≥1 proxy-dialect order, but only the fresh population votes) · agnostic-loot §6's summoner coverage requirement · the necromancer fantasy promise.

**The family (defining axes for the eight cells — same treatment rotation got):**

| Axis | Domain |
|---|---|
| `proxy_archetype` | `stationary_emitter` (no HP/AI) \| `stationary_targetable` (HP, draws aggro) \| `mobile_minion` (nav + AI) \| `consumable_sacrificial` |
| `lifecycle` | **shared enum with §1 axis 5** — duration / while_channeling / stack_refresh / until_consumed (+ `permanent_until_killed` for HP-bearing tiers) |
| `scaling_channel` | inherited-from-caster \| own-stats \| hybrid |
| `command_verb` | none \| reposition \| detonate \| focus_target *(v1: none/detonate; reposition+focus = P2)* |
| `attribution` | per-cohort bucket keys (star-lord; the C2 machinery, already live) |

**P0 → P1 → P2 staging (RATIFIED):**

- **P0 — parametric emitters** (no HP/AI): the §1 `parent_entity` frame + `radial_spawn` hook IS the P0 proxy. The **totem sim-liveness probe is the first P0 certification** (shared gate with orbiter_bombardier — one probe, two consumers). Serves cells 16 (Familiar) + 18 (Totem Hierophant) at P0 fidelity. **Rides THIS amendment's build.**
- **P1 — stationary + targetable:** adds proxy HP + **mob aggro-choice** (the sim's scalar-distance targeting currently knows only THE PLAYER) + hit-eligibility. Real totems; Iron-Golem-as-turret. Bounded sim change; math-note-first.
- **P2 — mobile autonomous minions:** adds nav + command verbs + full attribution. The true Skelemancer (17), Carnevil (25), Spirit Wolves (24), Ancestors (5), Falconer (10), Trapsin mines (11 — placed P1-class, mobile P2-class). The expensive tier; its own dispatch series.

**E-slate placement:** the proxy substrate build joins the per-axis main line **after E3/E4, before the ONE Q14 band re-anchor** (same window as orbital emission — the re-anchor must land on a population containing BOTH new dialects, once). E6 (T4 suite) continues in-flight unchanged; this family is the substrate beneath it.

## 8. ROSTER-OF-RECORD PIN (Matt 2026-07-09)

- **Demo roster = ALL 25 numbered BC cells + the hypothesis-based kits (H-series)** — including proxy/summon cells and totem. Supersedes the G1 "~20 hand-picked" on the COUNT axis (curation act unchanged: Matt picks per-kit from the certified population; zero hand-authored content; kit-grain certification per C2 GRAIN mode).
- **Totem contingency:** bombardier/totem roster seats gate on the P0 sim-liveness probe. **Probe-fail → Matt discussion** (his words: *"assuming totem probe passes, if not let's discuss"*) — never a silent drop.
- **The parseable roster table** (K1–K25 + H-series, with status + blockers/held-rules columns) lives in `../current-to-end-state/current-to-end-state-serial-content-emission.md` § KIT ROSTER — the Glance content-emission page derives its "first glance" from it (contract §7.3).
- **Count reconciliation pinned here (survey findings 2026-07-09):** code defines 25 CellDefs; Sketch A says ~22; the 2026-07-06 fire ruling said 18; batch-1 fired 7. **The roster of record is now the 25 numbered cells** — the 18/22 counts are historical accounting, struck by this pin. Two drift items for the next generation dispatch: Twin-Blade coordinate (Sketch A `mid/high/flat` vs CellDef 9 `melee/high/variable`; the batch-1 bundle fired Sketch A's) · Dagger Assassin (cell 6) never fired in batch-1.

## 9. Gates + open register

| # | Item | State |
|---|---|---|
| G1 | Totem/P0 sim-liveness probe (gamora; shared gate: bombardier + P0 proxies) | OPEN — first gate of the build; probe-fail → Matt discussion |
| G2 | Rotational kernel math note (gamora, Disc #1) → Gate-1 | OPEN — precedes any kernel code |
| G3 | Nova/spin migration conservation audit (E2-harness pattern; instant-nova oracle) | OPEN — gates the compile-layer switch |
| G4 | P1 aggro-choice math note | OPEN — after P0 lands |
| G5 | Swept-annulus attribution + blacklist pre-registration | OPEN — before first orbital gauntlet batch |
| G6 | v2 reserves (time-varying ω · eccentricity · graze · boomerang · epicycle cell · target_entity cell) | PARKED — named re-entries |

**Signed:** gandalf, 2026-07-09 (SPEC-AUTHOR). One family for Garlic → Hammerdin → Blade Vortex → Touhou; one family for familiar → totem → Skelemancer; one roster of record. Matt ratified all three in-session; KR sequences the gates.
