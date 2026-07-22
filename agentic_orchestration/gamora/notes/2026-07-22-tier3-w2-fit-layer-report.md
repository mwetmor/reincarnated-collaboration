# Tier-3 W2 — Fit Layer + Sim Scenarios — REPORT

**WAVE W2 of the Tier-3 Encounter-Geometry Run** · conductor gandalf `RUN-CONDUCTOR`
**Author:** named-gamora sub-agent · 2026-07-22
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` §4 W2
**Done-predicate (verbatim):** (a) fit computes over 267 kits × per-era decks without error; (b) scenario set RUNS in harness. **BOTH MET.**

**Engine HEAD:** `a57ee1f` at open + through all probe/scenario runs. **MOVED mid-session to `99aaf50`** AFTER runs completed (Lane-2 build advanced). The `a57ee1f..99aaf50` delta touched only `AGENT_STATE.md`, `gauntlet_sim.py` (the non-spatial sim), + a horde-KPM math note — **nothing in `spatial_gauntlet/`** (the probed harness). All artifacts stamped `a57ee1f`; probe verdicts re-verified stable at `99aaf50`.

**Substrate:** corpus.db md5 `d091881d` (`agentic_orchestration/research/curated/corpus.db`) — READ-ONLY, verified by md5-check in the script.

**Artifacts (all in `agentic_orchestration/gamora/notes/`):**
- `2026-07-22-tier3-w2-fit-layer-math.md` — math note (Discipline #1, math-before-code)
- `2026-07-22-tier3-w2-fit-layer.py` — fit layer + census (the compute)
- `2026-07-22-tier3-w2-fit-output.json` — 1068 fit records + census
- `2026-07-22-tier3-w2-scenario-set.py` — scenario-set driver (invokes engine by path)
- `2026-07-22-tier3-w2-scenario-run-record.json` — per-scenario run record
- this report

---

## 1 — PROBE-4 verdicts (Phase a — harness expressiveness, §7 strain formations)

Probed against the LIVE `spatial_gauntlet/` harness at HEAD `a57ee1f`; re-verified stable at `99aaf50`. **Red-flags here are a chartered honorable outcome (charter §4/§8), routed to Lane-2 as requirements per T3-V7 — NOT written into Lane-2's spec by me.**

| Probe formation | Verdict | Specific missing harness capability |
|---|---|---|
| **`cbn_corridor_arc`** (wall-bounce arc) | **PARTIAL** | Corridor geometry EXISTS (`SCENARIO_CHOKEPOINT` 10×50, 5m bottleneck y=[23,27]) + beam/bolt are `line` geometry, but **no projectile wall-reflection/bounce/LOS/occlusion**. Walls are positional bounds only (`CHOKEPOINT_Y_MIN/MAX` gate target-inclusion, `spatial_engine.py:3036/3122`). Chains capped depth-0/1 ("unbounded chains degenerate + un-simulatable", `:460`); the "reflect" hits are thorns **damage**-reflection, not geometric bounce. Corridor + line-pressure expressible; the **wall-bounce amplification** is not. |
| **`cb_crossfire`** (paired-emitter tracking) | **PARTIAL** | Single-channeler beam-lanes ARE expressible (tracking beam re-resolves against live positions, `spatial_engine.py:3116`; `line` geometry). Crossfire is **composable** as two independent `stationary_caster` channelers at opposite ends, but there is **no native paired-emitter cross-tracking primitive** that models the beam-CROSS forced-reposition zone. Expressible-by-composition, not as a first-class construct. |
| **`ts_environmental_nest`** (terrain spawner) | **PARTIAL** | Spawner is a **fixed-window GLOBAL injector**, not a killable terrain-anchored entity (`ContinuousSpawnSpec`, `arena.py:230` — clones the LAST mob, injects in a band, `engaged_cap=50`). **No source-entity whose DEATH stops spawning.** An EMPLACEMENT grid of held emitters exists (`arena.py:1343`) + continuous spawning exists, but the defining verb — **destroy-the-egg-sac-to-halt-the-burst** — is absent. Streaming-nest pressure expressible; the killable-anchor is not. |
| **`ss_phase_transform`** (mid-fight verb swap) | **CANNOT** | `preferred_behavior` is read ONCE at spawn (`spatial_engine.py:5335/5410`) and is **immutable per entity for the fight**. No HP-threshold / phase-transition / aggro-trigger swaps behavior or skill-set mid-fight. The only trigger-like tag is `proximity_trigger` — itself spawn-fixed, not a transform. The SHAPESHIFT verb (form-transition that BRINGS NEW ATTACK VERBS mid-fight) has **no expression**; requires a NEW engine mechanism (a mid-fight entity-mutation hook on a trigger). |

**Red-flag for Lane-2 routing (conductor's T3-V7 beat):** ONE capability is a true CANNOT and three are PARTIAL. The single net-new engine MECHANISM the grammar needs and the harness lacks is **`ss_phase_transform`'s mid-fight entity-mutation-on-trigger hook** (the other three are geometry/entity-model extensions of existing primitives: projectile-wall-reflection, native paired-emitter tracking, killable-spawner-entity). Note: sim-capacity §A3 (my own Lane-2 STEP-a spec, `simulation/spec/sim-capacity-extension-spec-2026-07-22.md`) verified a DIFFERENT four (swarm/volley-fan/lane/emplacement) as fully expressible — those are the COMMON formations; the Tier-3 §7 four are the deliberately-harder STRAIN cases, and they land PARTIAL×3 + CANNOT×1. The §A3 "W2 pre-hedge SATISFIED" claim holds for the common formations but does NOT cover the four strain formations, which is precisely the risk W1 §7 flagged.

---

## 2 — Fit compute census (Phase b — `fit(kit, encounter | era)`)

**TOTALITY PREDICATE MET: True.** 267 kits × 4 era decks = **1068 join rows computed, 0 errors, 0 kits dropped.**

- **Determinate join (math note §1) — TOTAL, no ruling needed.** Every kit shelves (era_year total, 267/267). Every kit resolves a family OR degrades cleanly to era-level. Per-(kit,deck): `shelf_match`, `family_present`, MESO formations, MICRO verb-class, derived-cell role — all determinate lookups against the frozen W1 artifacts.
- **v0 SCORING (math note §2) — `PROPOSAL — conductor ruling required`.** `fit_score = w_v·verb_affinity + w_t·topology_affinity + w_s·shelf_affinity`, proposed **w_v=0.50 / w_t=0.30 / w_s=0.20**. Produces a genuine per-kit spread (fit_score 0.1→1.0, full histogram) so W3 can take argmax=SHOWCASE, argmin=STRESS. **The ordering the conductor owns: accept or re-weight.**

**Distributions:** family_present {present 173, hole 11, unresolved 884}; confidence {HIGH 1010, MEDIUM 58}; scoring_basis {full 184, era_only_unresolved_family 884}; fit_score [min 0.1, mean 0.535, max 1.0].

---

## 3 — Membership-resolution status from corpus.db (the specific gap — REPORTED, not fabricated)

**The charter's four-tier family membership (gateA RATIFIED 86 · τ-PROPAGATED 44 · DOCKET-5 · fresh-draft) is NOT fully materialized in md5 `d091881d`.** What EXISTS:

- **RATIFIED tier = `atlas_gateA_labels_2026_07_14`** (byte-identical to `_refit_candidate_1`): 86 kit_ids, **6 families** {TOTEM-SENTRY 24, TRAP-MINE 23, WHIRLWIND 15, CHANNELED-BEAM 9, AURA 8, MINION-PET 7}. Of these, **46 are in the record-267 spine**; 39 annex, 1 system.
- **On the record-267 spine specifically: 5 families resolve** {TOTEM-SENTRY 16, TRAP-MINE 12, WHIRLWIND 7, CHANNELED-BEAM 6, AURA 5} = 46 kits. **MINION-PET's 7 gateA rows are ALL off-spine** (consistent with the charter's "ratified MINION-PET 7/7 off-spine" note).
- **τ-PROPAGATED 44 + DOCKET-5 tiers: NO materialized table** carries them in this md5. `mechanic_gap_docket.docket_family` is a DIFFERENT taxonomy (mechanic-gap families: "summoner-deferral", "stat-as-damage-substrate", …), NOT the 13 encounter working-labels. The `gx` column (58 distinct codes on the spine; GX-02=shapeshift) is a THIRD taxonomy with partial overlap, NOT a clean 13-family membership.
- **7 of 13 families have ZERO spine membership**: MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT, CHAIN-BOUNCE, DASH-STRIKER, IDENTITY-GAUGE. **This is load-bearing** — MELEE-STRIKE and DOT-AILMENT are two era SIGNATURE families (I and II), yet no kit resolves to them from gateA.

**How fit handled it (no fabrication):** the 221 UNRESOLVED kits still compute — they shelve by era_year and carry the shelf_affinity term at full confidence; their verb/topology terms degrade to era-level neutral (0.5) with `scoring_basis: "era_only_unresolved_family"`. No membership invented, no kit dropped. **Totality achieved despite the gap.**

**Era anomaly (reported, not corrected):** `poe1-kinetic-fusillade` has `game=poe1` but `era_year=2024` (a genuine late-PoE1 skill, `eras_normalized "3.20+"`) → shelves to IV (the shelf key is era_year per §1.2, not game). This is the 94-poe1-vs-93-era-II discrepancy in the charter's act-spine count.

**IMPLICATION for the conductor:** the fit layer's SCORING is family-keyed for only 46/267 spine kits (17%). If W3 needs family-differentiated showcase/stress across the FULL spine, the τ-PROPAGATED + DOCKET memberships must be materialized into corpus.db (a substrate task, elrond/rocket seam, NOT W2) OR the fit scoring must lean harder on the BC-axis reads directly (which ARE total, 258–267/267) rather than family-mediated verb/topology. **This is a genuine handoff gap, surfaced here as chartered.**

---

## 4 — Scenario run-record (Phase c — MESO/MICRO scenarios that RUN)

**Done-predicate MET: 9/9 unique scenarios executed-ok (9 ran-clean, 0 failed), all with COMBAT-EVIDENCED runs** (aoe_hits 16–84, elapsed 2.3–9.1s — real combat, not no-op non-crashes). Invoked the engine harness BY PATH from the collaboration repo; **zero writes to the engine repo** (T3-V7 namespace law honored).

- **15 formation records** covering the §3.3 catalogue's 11 families + the horde overrun + the 4 strain-probes:
  - **11 ran-clean** (proxy scenario expresses the formation class per sim-capacity §A3): ms_swarm_surround→open_arena, ms_wedge_advance→chokepoint, ts_anchor_screen→magic_pack, da_field_retreat→dense_cell, mpv_fan_from_position→open_arena, tm_preseed_corridor→chokepoint, ww_converge_spin→dense_cell, aura_carrier_pack→magic_pack, cb_lane_hold→boss_with_adds, ds_flank_burst→elite_pack, scenario_overrun_horde→scenario_overrun (the ≥50-concurrent cert shell, 55 mobs).
  - **3 ran-with-caveat** (proxy executes; strain mechanic MISSING per probe): cbn_corridor_arc, cb_crossfire, ts_environmental_nest.
  - **1 could-not-express** (proxy executes; strain mechanic ABSENT): ss_phase_transform.
- **2 holes** (guest-family, catalogue-only this run per charter §1): MINION-PET, IDENTITY-GAUGE — recorded as holes, never faked.

**Caveat on proxy-faithfulness:** the 11 ran-clean rows use REGISTERED arena scenarios as proxies for formation CLASSES (swarm/lane/anchor/field/beam/converge/flank/horde), per sim-capacity §A3's formation→primitive mapping. These are class-faithful (the right positional + behavior grammar) but NOT formation-exact (e.g. `ww_converge_spin` maps to `dense_cell` tight-offset packs, which approximate the converge but lack a true rotating-body geometry; `aura_carrier_pack`'s identify-and-kill-the-carrier is roster-semantic, resolved at RD-1, not sim). The scenarios RUN and exercise the class pressure; formation-exact fidelity is an RD-1 concern.

---

## 5 — Confidence carry (§8 obligation)

MEDIUM travels: **58 of 1068 fit rows carry `confidence: MEDIUM`** — the Age-II rows 17–18 formations (`tm_preseed_corridor`/II, `da_field_retreat`/II, Maxroll-only floor) + all Age-IV LE-sourced formations (1.0-era; Season-3 overhauls not reflected). Per-join-row tag, propagated from the W1 formation_catalogue `confidence`. HIGH otherwise (1010 rows).

---

## 6 — Discipline compliance

- **#1 math-before-code:** math note written BEFORE both scripts; the fit SCORING (a non-trivial modifier formula) is flagged PROPOSAL, the determinate join is proven total.
- **#2 smoke-test:** scenario set is a smoke (9 scenarios, 4 fights each, ~seconds each); no full regen.
- **#11 empirical inspection over assumption:** every probe verdict is grounded in a specific `spatial_engine.py`/`arena.py` line, not assumed; re-verified across the HEAD move.
- **#12 semantic-shifting:** N/A — no existing behavior reinterpreted; this is net-new derivation atop frozen artifacts.
- **External-system rule (ADR-006):** corpus.db READ-ONLY (md5-checked, `mode=ro` connection); zero telemetry writes; zero engine-repo writes.
- **T3-V7 one-way coupling:** red-flags reported to the conductor in this return, NOT written into Lane-2's spec.

---

## 7 — What the conductor owns from here

1. **RULE the v0 scoring** (accept w_v=0.50/w_t=0.30/w_s=0.20, or re-weight) — W3 needs the ordering to pick matched SHOWCASE/STRESS pairs.
2. **ROUTE the 4 strain-probe findings to Lane-2** (T3-V7 beat): 1 net-new mechanism (`ss_phase_transform` mid-fight mutation hook) + 3 primitive-extensions (wall-reflection, native paired-emitter tracking, killable-spawner-entity).
3. **DECIDE the membership gap** (§3): materialize τ-PROPAGATED + DOCKET memberships into corpus.db (substrate seam) OR pivot fit scoring to lean on the total BC-axis reads rather than family-mediated terms — because only 46/267 spine kits resolve a family today.
