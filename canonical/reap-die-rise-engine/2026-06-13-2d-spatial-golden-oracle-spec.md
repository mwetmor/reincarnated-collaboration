# The 2D Spatial Golden Oracle — Certification Spec

> **STATUS:** CURRENT (load-bearing as of 2026-06-13) — see `canonical/00-ground-state.md`

**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward; design authority for the oracle)
**Status:** v1.6 — design-spec-as-math; Matt-authorized 2026-06-13 ("and then the golden oracle for 2D"). gamora executes the validation; this doc is the acceptance authority. **v1.1 amendment (same day, per Matt challenge):** § 6 cert gate split into RESOLVE (W-C; orthogonal to orphans) + MEASURE (W-D/W-F; downstream of the BC coverage audit); MEASURE arity consumes the Bucket-B ruling, no longer presumes 8 axes. **v1.2 amendment (same day, dispatch `2026-06-13-gandalf-wc-kpm-band-recalibration.md`):** the § 2 band is recalibrated to the spatial pack-clear instrument (new § 2-S) after the W-C de-risk spike proved the 1D-unit band reads all-BELOW; the 1D § 2 table is preserved as historical-rationale; RESOLVE reads the new `SPATIAL_ENCOUNTER_KPM_BAND` (§ 2-S.2). **v1.3 amendment (same day, parallel hardening per Matt directive):** new § 2-S.0(b-ext) closes the *absolute-scale* half of the circularity guard — the anchor `A` (spike's own output) is cross-checked against the external TMPM-30-50 genre canon (2026-05-17, `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3.2) via the full-clear KPM↔TMPM equivalence; `A=43` open_arena confirmed in-band. CONFIRMATORY ONLY — no band number, edge, `R`, cohort, or § 5 row changed. **v1.4 amendment (same day, Matt-authorized "let's do it soon, but not too far forward"):** § 4 gains two *forward* density levers — § 4.C (cluster-density-for-cascade, `GEOMETRY_PROPAGATION`, unbuilt) + § 4.D (sustain-for-proxy, the Axis-2A-measurability **W-D prerequisite**). Flagged forward-spec, NOT current acceptance gates; no band, edge, `R`, cohort, § 5 row, or RESOLVE/MEASURE condition changed. **v1.6 amendment (same day, W-D close, Matt-ratified D1–D6 dispositions per `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`):** (a) § 5.2 gains the W-D-close amendment — the M1 gather-primitive ablation RAN and DISCHARGED-NEGATIVE (gather INVERTS the K4≥K2 margin: WITHOUT 6/9 +3.99 → WITH 1/9 −3.44; the per-seed margin is closing-time noise, the K4≥K2 mechanism is discharged-negative not left open; mobility-home reframed to kite-survival in the boss room via the existing K4 SURV-via-kite ⚠C4 cell @ cond. 5; the farming-mobility coverage-edge vs parity fork LOGGED OPEN as a design-call not a build; speed-gated gather REJECTED as rule-shopping; primitive stays in-engine default-off, brownfield-safe); (b) § 6.2 cond. 4 gains the **4-discrim** discrimination sub-clause enforcing Matt's HARD CONSTRAINT `wired-not-default ≠ discriminates`; (c) § 6.4 gates "the archive measures the current kit" on the CLEAN per-axis discrimination accounting (0 of 8 category-(e) LIVE-OBLIGATION — gandalf-interpreted W-D read records 1 discriminates-now [Geometry; Engagement range-half confirms] + 7 wired-with-named-deferred-homes → § 6.4 stays open-pending-W-F cleanly); (d) § 6.3 gains the **ARITY RULING — arity STAYS 8** (proxy-density is the existing Axis-2A [Bucket-A re-opened deferral], NOT a 9th axis; D4 wires the 8-tuple's 2A slot, D5 is arity-8). No band number, edge, `R`, cohort, or § 5 row changed; the changes are the §5.2 ablation disposition + the discrimination/arity gates. **v1.5 amendment (same day, W-C-full RESOLVE close, Matt-ratified "t-test logged not gated, and the M1 re-close as the with/without ablation"):** consolidated K4 ⚠B disposition — new § 5.1 (K4 direction CERTIFIED at RESOLVE / per-seed-margin mechanism DEFERRED to W-D / paired t-test t=2.207 p=0.029 LOGGED-not-gated) + new § 5.2 (M1 gather-primitive as a binding W-D/W-F obligation with a WITH/WITHOUT ABLATION acceptance test, Matt-sharpened from a threshold-holds test to a causation-proving test); § 2-S.5 finding 3 UPGRADED (spawn-spread DISPROVEN as the lever via gamora's 4-geometry smoke test, recorded resolved-NEGATIVE; the lever is the M1 gather-primitive, engine-movement seam); § 6.1 records RESOLVE PASS for W-C-full (36/36 §5 rows + 3 canaries + shape-flip + held anchor) with K4 = direction-certified / mechanism-deferred / t-test-logged-not-gated; § 6.1 condition 2 carve-out for K4. No band number, edge, `R`, cohort, or other §5 row changed — the change is the K4-canary *disposition* and the M1 W-D obligation.
**Authority:** Matt 2026-06-13 — authored from the Pattern-B combat-sim-architecture dialogue (this session).
**Companion docs:**
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` — the wave (§ 5) this oracle gates; the cert wave's W-A authors this, W-C validates against it
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` — § 5 commit-grade-is-the-2D-playspace; this is how commit-grade gets *proven* rather than asserted
- `canonical/story/gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md` — prior gandalf scenario-design authority (the 6 rooms' implementation spec)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the 8 axes the commit-grade BC computes from spatial telemetry (W-D)

---

## 0. TL;DR

1. **The oracle is the ground truth the 2D engine has never been measured against.** The spatial engine is ~1900 lines of built scaffolding that has **never produced a single successful, verified run.** Until we can say "for THIS known kit in THIS known room, the engine produces THIS result, and we hand-verified that result is correct from genre knowledge," every kit it characterizes is unprovable. This doc *is* that ground truth: hand-authored known-correct answers for the six existing rooms and a set of reference kits.
2. **The rooms already exist; the bands already encode the skew.** `arena.py` defines the six `ArenaScenario` objects; `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311) already sets per-room KPM targets that *encode the AOE-skew in hard numbers* — open_arena/chokepoint demand **137–836 KPM** (unreachable by single-target against 8 mobs in 120 s); boss/mini_boss expect **18–225** (single-target range). The oracle does not invent targets; it verifies the engine *realizes* the targets that are already designed.
3. **The oracle bakes in the three risks Matt named** (this session's A/B/C): pack count tuned so the high-KPM rooms are **AOE-only-reachable** (A); at least one room that rewards **movement-as-AOE-setup** (B); the **mob AI pinned** so AOE is rewarded-but-not-free (C4). Each becomes a concrete acceptance test via a reference kit whose golden result *requires* the engine to credit that dimension.
4. **The reference-kit set is the genre's diversity, used as a test instrument.** Six known-correct kits (single-target, radius-AOE, line/cone-AOE, mobile-AOE-farmer, proxy/summoner, tank). Each has an *expected per-room verdict*. The engine is certified when it reproduces all of them within tolerance — which proves it teaches the genre rather than flattening it. Two of them (single-target, proxy) are **canaries**: the engine must *reject* single-target at the density rooms and *reward* proxy at them. If it doesn't, it's lying in the genre-fatal direction.

---

## 1. What the oracle IS and IS NOT

**IS:** a hand-authored set of `(reference_kit, room) → expected_verdict` cells, derived from genre design knowledge, that the spatial engine must reproduce to be trusted as the **sole** behavioral-identity authority (per the companion doc, 1D no longer mints identity). It is the keep-vs-rewrite judge for the W-C module pass: a module is kept if the cells it touches reproduce; rebuilt if they don't.

**IS NOT:** a from-scratch room build (the rooms exist), a balance pass (it certifies the *instrument*, not the kits the instrument will later judge), or a 1D artifact (it runs exclusively on the spatial engine).

**Why now is the right point** (Matt's timing claim, affirmed): the golden answers *require* knowing what we measure. You cannot author "the correct verdict for a nova in the open arena" without the locked axes (so the verdict populates the right dimensions) and the KPM bands (so "correct clear-rate" has a number). Both are now done. The axes/labels/hypotheses work that was completed *instead of* the simulator last cycle is precisely the prerequisite that makes this oracle authorable. The detour built the ruler.

---

## 2. The anchor — the bands already encode the skew

Verified `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311), `(lo, hi)` KPM per (room, cohort):

| Room | DPS-min-maxer | Balanced | Defensive | Hybrid | Reading |
|---|---|---|---|---|---|
| **open_arena** | 193–836 | 150–664 | 368–560 | 137–728 | **HIGH — AOE-only.** 8 mobs, 120 s, all-killed. To clear at 150+ KPM you must hit many at once. |
| **chokepoint_corridor** | 182–836 | 150–664 | 368–560 | 137–728 | **HIGH — line/cone-favoring.** Funnel concentrates mobs into a line. |
| **magic_pack** | 52–614 | 47–555 | 34–380 | 44–453 | Mid. Champion + retinue. |
| **elite_pack** | 51–699 | 47–660 | 37–447 | 47–573 | Mid-high. Few tanky + adds. |
| **mini_boss** | 46–204 | 29–180 | 29–136 | 29–166 | **LOW — single-target.** |
| **boss_with_adds** | 29–225 | 22–180 | 18–151 | 21–197 | **LOW — single-target + flanking.** |

The skew is *in the bands*: the two density rooms demand a clear-rate that single-target cannot physically produce, and the two boss rooms expect single-target rates. This is the genre teaching mechanism, already designed. **The oracle's core job is to verify the engine produces KPM inside these bands for the cohort the kit belongs to — and, critically, produces KPM *outside* the band when a kit is the wrong archetype for the room** (a single-target kit must fall *below* the open_arena floor; an AOE kit must fall *below* the boss... no — an AOE kit at boss simply produces low single-target KPM, which is *in* the low boss band; the canary is the single-target kit *failing the high density floor*).

> **The table above is in the WRONG INSTRUMENT for the spatial engine. It is preserved as historical-rationale only. The live spatial band is § 2-S below.**

---

## 2-S. The spatial-instrument band — recalibrated (2026-06-13, gandalf)

> **v1.2 amendment, this session.** The W-C de-risk spike (gamora, `output/wc-derisk-spike-2026-06-13.json`) produced the engine's first verified spatial run and proved an **instrument mismatch**, jack-ryan Gate-2-confirmed as REAL (not a masked engine bug): all 36 cells read BELOW the § 2 floor because the § 2 numbers are **1D 1v1-duel kill-rate** (a fight scores 0 or 1 kill; floor 137–836) while the spatial engine **clears an ≤8-mob pack and ends** (KPM numerator bounded by pack size over the room window; pack-clears land at ≈7–44 KPM). The two are different rulers. The RESOLVE cert (§ 6.1) cannot pass against § 2; it reads § 2-S.

### 2-S.0 The circularity guard — ordering made legible (jack-ryan Gate-1 WARN-1)

The AOE/single-target separation is **already visibly present in the engine's own spike distribution** (open_arena AOE cluster K2/K4/K5 ≈ 34–44 KPM vs single/line/tank K1/K3/K6 ≈ 7–19). "Draw the floor where the AOE cluster sits" is therefore the forbidden band-=-distribution fit *disguised as design* — the design-correct edge and the distribution-fitted edge coincide and prose cannot tell them apart. The guard is the **ordering**, and this section is written in that order:

**(a) FIRST — the separation as a genre-math ratio invariant `R`, derivable with NO spike numbers in hand.**

In a density room of `N` mobs, a kit's pack-clear rate is governed by how many mobs die per kill-cycle:
- A **single-target** kit kills one mob per cycle. To clear `N` mobs it needs `N` cycles. `KPM_ST = N / (N·t_cycle) · 60 = 60/t_cycle`.
- A **qualifying area** kit landing on `m ≥ 6` of `8` mobs per cast clears the pack in `⌈8/6⌉ = 2` cycles. `KPM_AOE = 8 / (2·t_cycle) · 60 = 4·(60/t_cycle)`.
- **Therefore `R_expected = KPM_AOE / KPM_ST = 4`** — a qualifying area clear runs at **4×** the single-target clear-rate, by construction. This is pure pack-arithmetic; it is derivable before opening the JSON, and the value `4` is fixed by the room's `N=8` and the 6-of-8 qualifying threshold (oracle § 4.A), nothing else.
- **`R_floor = 2.5`** is the *conservative* minimum separation the room must teach to credit area-clear at all (it accounts for sub-qualifying casts that land on only 4–5 mobs, partial overlap, and seed noise). **`R_floor = 2.5` is the design contract; `R_expected = 4` is the construction.**

**(b) THEN — the spike supplies ONLY the scale anchor (one number per room).** The anchor `A` is *what KPM a verified ≥6-of-8 qualifying clear physically produces in that room* — the single empirical fact the band needs. Per room (verified, 5-seed means):

| Room | Anchor `A` (verified qualifying-shape clear) | Source cell |
|---|---|---|
| open_arena | **43** | K2 radius 42.9 / K4 mobile 43.9 (8/8 kills, circle) |
| chokepoint_corridor | **32.4** | K3 line 32.4 (8/8, the funnel-qualifying shape) |
| magic_pack | **35** | K4 35.4 / K2 34.4 (4/4) |
| elite_pack | **15** | K2 15.2 (3/3; tanky mobs cap the rate) |
| mini_boss | **2.5** | K3 2.5 (lone-target kill over the long window) |
| boss_with_adds | **2.2** | K1 2.2 (boss-kill over 240 s) |

**(b-ext) EXTERNAL scale cross-check — the anchor's absolute magnitude is confirmed against genre canon, not just against itself (closes the absolute-scale half of the circularity guard).** The ordering in (a)→(b)→(c) closes the *relative*-separation half of the circularity guard: `R` is asserted as pack-arithmetic before any spike number enters, so the AOE/single-target *separation* is design-led, not distribution-fitted. But the anchor `A` in (b) is the spike's own per-room output — which is internally circular for the absolute *scale*: "is ~43 KPM the right order of magnitude at all?" cannot be answered from the engine's own distribution. The external answer comes from canon.

In a **full-clear room** — which every density room is, by construction (open_arena/chokepoint are `all-killed`; every spawned mob dies before the room ends) — **kills-per-minute is identically total-monsters-per-minute**: when the kill-count equals the spawn-count over the room window, `KPM = TMPM` by definition. The anchor `A` is therefore directly comparable to the genre's TMPM canon.

**The external anchor: TMPM = 30–50.** Per `canonical/story/historical/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3.2 (2026-05-17 canon), the demo's fight context (D4-nightmare-dungeon density) targets **30–50 total-monsters-per-minute**, with genre convergence across D4-nightmare / Last Epoch Empowered / Grim Dawn Ultimate at 30–80 TMPM (§ 3.2 reasoning point 4). The open_arena qualifying-clear anchor **`A = 43 KPM ≈ 43 TMPM` sits inside the 30–50 band → the absolute scale is genre-confirmed.** The engine's first verified spatial run produces a qualifying-AOE pack-clear rate at the order of magnitude the genre says a competent AOE clear *should* run in a nightmare-density room. The chokepoint anchor (32.4) is likewise in-band; the mid rooms (35, 15) trend lower with smaller packs and tankier mobs as expected, and the boss rooms (2.5, 2.2) are single-entity windows where TMPM is not the instrument (those rooms judge on SURV + kill, § 2-S.0(c) boss row).

**Circularity guard, both halves now closed:** the *relative separation* is closed by the `R`-ordering (asserted in (a) before any spike number) — the AOE/single-target floor is design-led. The *absolute scale* is closed by this TMPM cross-check — the anchor's magnitude is confirmed from 2026-05-17 canon, not from the engine's own output. **This is CONFIRMATORY ONLY: no band number changes.** The 43-KPM anchor was already in-band; the TMPM cite makes explicit that it was always genre-correct in magnitude, closing the half-guard jack-ryan's Gate-2 would otherwise flag.

**(c) Place the edge by applying `R` to the anchor** — NOT by reading where the cluster falls:

| Room class | Floor rule | Ceiling rule | Why |
|---|---|---|---|
| **Density (open_arena)** | `A / √R_expected = A/2.0` | `A · R_floor` | Log-midpoint between qualifying-AOE (`A`) and single-target-class (`A/R_expected`); equal √R_expected = 2× ratio-margin each side. Single-target **must** fall below. |
| **Density (chokepoint)** | `A / √R_floor` | `A · R_floor` | The corridor **compresses every kit upward via queuing** (the single-target kit's next target is always adjacent — a genre-known funnel effect, assertable before the spike). So the no-funnel/funnel separator sits *higher* relative to anchor than the spread-room separator. |
| **Mid (magic, elite)** | `A / R_expected = A/4` | `A · R_floor` | Blended rooms — single-target gets **partial** credit (it can focus the champion / a tanky target), so it lands LOW-EDGE/IN, not BELOW. |
| **Boss (mini, boss)** | `A / R_expected` | `A · R_expected` | **Single-target rooms judged on SURV + kill, not KPM.** KPM is a tiny number (one entity over a long window) and is a *wide sanity rail*, not the discriminator. Survival is. |

**The recalibrated spatial band (Balanced cohort — see § 2-S.1 for the per-cohort reduction):**

| Room | `(lo, hi)` KPM spatial | Class | Reading |
|---|---|---|---|
| **open_arena** | **21.5 – 107.5** | density (spread) | AOE-only-reachable. Single-target (≈17) falls BELOW. |
| **chokepoint_corridor** | **20.5 – 81.0** | density (funnel) | Line-favoring. Single-target (≈19, queuing-boosted) falls BELOW; floor raised by funnel-compression rule. |
| **magic_pack** | **8.8 – 87.5** | mid | Champion + retinue; single-target gets partial credit (LOW-EDGE). |
| **elite_pack** | **3.8 – 37.5** | mid | Few tanky + adds; same partial-credit logic. |
| **mini_boss** | **0.6 – 10.0** | boss (SURV) | KPM is a sanity rail; SURV + boss-kill is the verdict. |
| **boss_with_adds** | **0.6 – 8.8** | boss (SURV) | Defensive-bridge home; SURV + boss-kill is the verdict. |

The separation is asserted in (a) **before** any spike number enters in (b); the floor in (c) is `A` divided by a function of `R`, never "where the cluster sits"; and the anchor's absolute magnitude is cross-checked against external TMPM canon in (b-ext), so the scale is not self-referential either. The K3-line second-order case (§ 2-S.3) is the proof the ordering bites: a distribution-fit floor would land K3@open_arena IN-with-the-AOE-cluster narration; the `R`-derived floor lands it BELOW, matching the *shape-flip design*, against the §5 pre-spike LOW-EDGE row.

### 2-S.1 Per-cohort reduction (jack-ryan INFO-4) — Balanced only, for RESOLVE

§ 2 has four cohort columns (DPS-min-maxer / Balanced / Defensive / Hybrid). The six RESOLVE reference kits are **hand-built archetype probes**, all assigned to **Balanced** (gamora spike note § 2; canary directions are cohort-robust). RESOLVE (§ 6.1) judges *only* these six. **Decision: the spatial band ships the Balanced column only.** Deriving the other three spatial columns now would mean inventing numbers — *no DPS-min-maxer / Defensive / Hybrid cohort kit has ever run on the spatial engine.* The other three cohort columns are derived in **W-D/W-F**, against cohort-tagged *generation* kits on the spatial engine (the MEASURE cert's domain, where real cohort data exists). This is the documented reduction the dispatch acceptance permits, not a deferral of work owed to RESOLVE.

### 2-S.2 Consumption interface (jack-ryan Gate-1 WARN-2) — `SPATIAL_ENCOUNTER_KPM_BAND`, parallel constant

**Replace-vs-parallel decision: PARALLEL.** The existing `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311) is the **1D gauntlet's live production judging band**; the 1D engine still uses it and is not deleted until **W-F**. Overwriting it would break 1D judging mid-wave. The recalibrated spatial band ships as a **separate sibling constant** that gamora wires in W-C-full:

- **Name/shape:** `SPATIAL_ENCOUNTER_KPM_BAND: dict[str, dict[str, tuple[float, float]]]` keyed `[room][cohort] → (lo, hi)`, **identical shape** to `ENCOUNTER_COHORT_KPM_BAND` so the RESOLVE cert's band-lookup code is a one-line source swap, not a structural rewrite. For RESOLVE it carries the **`"balanced"` cohort key only** (§ 2-S.1); the other three keys are added in W-D/W-F.
- **What gamora wires (W-C-full, gamora's seam — NOT edited here):** the RESOLVE cert reads `SPATIAL_ENCOUNTER_KPM_BAND[room]["balanced"]` for IN/BELOW/LOW-EDGE classification, replacing the spike's temporary read of `ENCOUNTER_COHORT_KPM_BAND`.
- **W-F cleanup implication:** when W-F deletes the 1D path, `ENCOUNTER_COHORT_KPM_BAND` is removed and `SPATIAL_ENCOUNTER_KPM_BAND` becomes the sole band (optionally renamed back to the canonical name at that point). No mid-wave breakage; the two coexist for exactly the W-C-through-W-E window.

### 2-S.3 The K3-line divergence — design vs distribution, resolved by design (a §5 refinement)

K3 (line) reads **18.8 at open_arena** — clustered with single-target K1 (17.3), NOT with the AOE cluster — yet §5 expects K3@open_arena = **LOW-EDGE**. Under the `R`-derived floor (21.5), K3@open = **BELOW**. This is the exact place distribution-fit and design diverge, and the resolution is **by design**: a line/cone kit in an *open* room has no funnel to align its shape on a spread spawn (x∈[18,32], y∈[8,18]); it lands ≈1 mob/cast and **correctly degrades to single-target class.** That is the shape-flip *working* (K3 choke 32.4 ≫ K3 open 18.8, ratio 1.7×), not a mis-placed edge. **You cannot place a floor that lands K1 BELOW (canary) and K3 LOW-EDGE simultaneously — the engine produces them at the same rate (17.3 vs 18.8, within seed noise).** Honoring the K1 canary forces K3@open BELOW. **Finding for KR / §5 refinement:** the §5 row `K3 @ open_arena = LOW-EDGE` overspecified (it assumed line keeps partial AOE credit in the open); the genre-correct verdict is **BELOW**. Update §5 to `K3 @ open_arena = BELOW` — a line kit in the wrong room fails the density floor, which is the diversity-generator doing its job.

---

## 3. The six rooms — golden assertions

Each room's golden behavior, stated as what a *correct* engine must produce. Room facts verified in `arena.py`.

### 3.1 open_arena (50×50, 8 swarmers, 120 s, all-killed) — the AOE god-room
- A **radius-AOE** kit clears all 8 within the band (≥150 KPM Balanced).
- A **single-target** kit **cannot reach the floor** (falls below 137–193 KPM) — it kills one at a time while the pack applies pressure. **If the engine puts single-target in-band here, it is broken (over-crediting single-target) — fail certification.**
- The room rewards **repositioning** (B): the 8 spawns are spread (x∈[18,32], y∈[8,18]); a stationary nova may not cover all 8 — a kit that *moves to gather then AOEs* should out-clear a stationary one of equal AOE. (See § 4.B.)

### 3.2 chokepoint_corridor (10×50, 5 m bottleneck at y=23–27, 8 swarmers, kills-only) — the geometry room
- A **line/cone-AOE** kit is **best here** — the funnel queues mobs into its shape.
- A **radius-AOE** kit is **worse here than in open_arena** — the corridor denies the spread it wants. **The ranking of radius-AOE vs line-AOE must FLIP between open_arena and chokepoint.** This flip is the diversity-generator (it makes AOE *shape* a build axis). **If the two rooms rank the two AOE shapes identically, the geometry isn't being simulated — fail certification.**

### 3.3 magic_pack (32.7×14, 1 magic + 3 swarm, kills-only) — champion + retinue
- Blended: AOE clears the retinue; some focus finishes the champion. In-band for AOE and proxy cohorts.

### 3.4 elite_pack (few tanky + adds) — the transition
- Rewards *some* single-target priority alongside clear. A pure-nova with no focus should sit at the *low* edge; a hybrid should sit center-band.

### 3.5 mini_boss (single-target survival) — LOW band
- Single-target and mobile-survivor kits in-band; pure-density kits at the low edge (they can still chip a lone target).

### 3.6 boss_with_adds (30×30, 1 boss r=1.5 + 2 flanking elite brutes, 240 s, boss-killed) — the climax
- **This room is the commit-grade home of the defensive bridge.** The 1D boss-duel panel (`boss/brute/physical` + `boss/brute/fire`) that produced the bridge's 25/22/23/26 was a *search-grade proxy for this room.* Certification re-validates the tank/mitigator/dodger/glass separation **here, commit-grade** (companion doc W-F).
- A **mobile** kit survives via kiting/dodging the flank pressure; a **tank** survives via eHP. Both in-band; **if the engine cannot distinguish their survival mechanism, the AI/positioning model is too coarse (C4)** — diagnostic.

---

## 4. The three risks, baked in as acceptance parameters

### A — monster count → KPM AOE-only-reachable
**Parameter:** the density rooms' pack size must make the high KPM bands **physically unreachable by single-target.**
**Acceptance test:** reference kit **K1 (single-target)** must score **below** the open_arena/chokepoint floor; reference kit **K2 (radius-AOE)** must score **in-band**. If K1 reaches the floor at pack = 8, **the pack is too small** — raise the swarmer count (8 → 10/12…) until single-target falls below the floor *and* AOE stays in-band. The current `arena.py` pack of 8 is the *starting* hypothesis; the oracle's first job is to confirm-or-raise it. This is the literal mechanism by which "not enough corpses" (Matt's original question) becomes a tuned parameter rather than a vibe.

> **The lever STAYS LIVE against the recalibrated § 2-S floor.** At pack = 8 the spike confirms the separation **holds in open_arena** (K1 17.3 BELOW the 21.5 floor; K2 42.9 IN) — so pack = 8 is *confirmed*, not merely hypothesized, for the spread room. **In chokepoint the separation is marginal:** K1 reads 18.7 (queuing-boosted) against a 20.5 floor — 4/5 seeds BELOW, one seed at the edge (§ 2-S.4). The pack-size lever is the design's response if W-C-full finds the choke K1/K2 separation does not hold robustly: raising the chokepoint swarmer count widens the K1↔K2 gap (more mobs to queue = more AOE advantage, single-target rate roughly flat). The recalibration does **not** freeze the lever; the floor is anchored to the *qualifying-clear rate*, which rises with pack size, so the band re-derives if gamora raises the pack in W-C-full. The lever's domain shifts from "is the floor reachable at all" (1D framing) to "is the K1/K2 separation robust across seeds in the funnel room" (spatial framing).

### B — movement-as-AOE-setup
**Parameter:** at least one room must reward *moving into position to land AOE*, not just standing and firing.
**Acceptance test:** reference kit **K4 (mobile-AOE farmer)** must **out-clear** an equal-AOE *stationary* kit in open_arena, by using movement to gather/reposition against the spread spawn. If the mobile kit does not beat the stationary one despite equal AOE, the engine is modeling movement only as flee, not as setup — **fail B; rebuild the movement/positioning credit.** (If needed, open_arena's spawn spread widens so a single stationary nova *cannot* cover all 8 without repositioning.)

### C4 — mob AI pinned
**Parameter:** the golden answers assume a **specified** mob behavior (the existing aggro-radius 8 m, swarm leash override 35 m, pursuit-to-player). This behavior is **pinned as part of the oracle** — if the AI changes, the golden master re-derives.
**Acceptance test:** the pinned AI must produce **realistic spread + pursuit** such that AOE is *rewarded but not free.* Specifically: mobs must **not** all collapse to a single point (which would make any AOE trivially clear every room and destroy differentiation), and must **not** scatter so widely that AOE never multi-hits. The diagnostic: if K2 (radius-AOE) trivially aces *every* room including the boss rooms, the AI is over-clumping (AOE-blob bias — the opposite failure from 1D's single-target bias). Pin the AI to the regime where § 3.1/§ 3.2's shape-flip actually manifests.

---

### Forward density levers (§ 4.C + § 4.D) — NOT current acceptance gates

A/B/C4 above are **baked-in gates** — built mechanics RESOLVE tests now. The two below are **forward**: the mechanics they exercise are not yet in the commit engine, so they do **not** gate RESOLVE (W-C). They are specced now so the density work has a design contract before it is built (Matt 2026-06-13, "soon, but not too far forward"). Each names a *preset* on one shared spawn primitive (`count` · `spacing` · `wave_structure`) — **do not raise the open_arena baseline (§ 4.A); add a new fixture when the mechanic lands.** They are two different *kinds* of density, and conflating them is the trap.

#### § 4.C — cluster-density-for-cascade (density **at a moment**)
**Parameter:** a room must reward **spatial clustering** — a hit whose geometry *propagates* to mobs packed within a spacing threshold (chain / cascade), so a propagation kit out-clears a flat-area kit of equal raw AOE *only when the pack is tight.*
**The mechanic:** `GEOMETRY_PROPAGATION` — **unbuilt in the 2D commit engine, and correctly with no representation in the 1D search estimator** (cascade is a spatial-adjacency mechanic; a range-scalar duel has no adjacency to propagate across — this lever can only ever live commit-grade).
**Spawn primitive:** a **ball-cluster** preset (~12–15 mobs, **tight** spacing, single wave) — distinct from open_arena's **spread** preset (8, wide). Governed by **inter-mob spacing, not raw count**; recursion cap 3 (anti-infinite-chain).
**Acceptance test (when built):** a 7th reference kit — **cascade/chain-AOE** — out-clears K2 (flat radius-AOE) in the ball-cluster room **and not** in spread open_arena. Wins both ⇒ the engine credits area, not adjacency; wins neither ⇒ propagation isn't modeled.
**Gate:** build + test only after `GEOMETRY_PROPAGATION` exists commit-grade. **Extends, does not gate, RESOLVE** — sequenced post-W-C.

#### § 4.D — sustain-for-proxy (density **over time**) — a **W-D prerequisite**
**Parameter:** a proxy/summoner kit reaches its true population only across a **sustained** encounter; its identity axis (Axis-2A, **mean-active-proxy-count**) cannot be read from a transient.
**The gap:** `PROXY_FISSION` is **built in generation** but Axis-2A **measures nothing** (BC coverage-audit blind spot, `agentic_orchestration/gandalf/notes/2026-06-13-bc-measurement-coverage-audit-query.md`). The current rooms clear an ≤8 pack and **end** (~11 s transient) — too short for proxy population to reach steady-state, so wiring Axis-2A against them mints **noise bins**, and a noise bin makes MAP-Elites **silently homogenize proxy-swarm kits** (cull the summoner variant the player never then sees — the precise genre-flattening this architecture exists to prevent).
**Spawn primitive:** a **sustained-wave** preset (~8–12 mobs, **medium** spacing, **N waves**) holding the encounter alive to proxy steady-state. **Validation gate FIRST:** inspect `arena.py` — `boss_with_adds` runs 240 s and may already supply enough *duration*; confirm whether its 2-add structure actually sustains a proxy population (vs. proxies idling after the adds die) before adding any new fixture.
**Acceptance test (when built):** K5 (proxy/summoner)'s mean-active-proxy-count is **stable across seeds** in the sustained room (the Axis-2A bin reproduces), where it is noise in the transient rooms.
**Gate:** **a hard prerequisite for W-D.** Axis-2A measurement-wiring (MEASURE cert condition 4, § 6.2) **cannot certify until a sustained encounter exists** — the sustained-wave fixture lands *before* Axis-2A is wired, or the wiring certifies against noise. If the Bucket-B ruling (§ 6.3) promotes proxy-density to a real axis, this is the fixture its reference kit varies on.

**Seam (both levers):** gamora builds the spawn primitive + (D) actor-lifetime / wave structure; gandalf holds the density-design contract (this § 4.C/§ 4.D); KR sequences — § 4.C post-RESOLVE, § 4.D into W-D ahead of Axis-2A wiring.

---

## 5. The reference-kit set — genre diversity as the test instrument

Six known-correct kits. Each cell is the **expected verdict** the engine must reproduce. `IN` = KPM in the room's cohort band; `BELOW` = below floor (correct rejection); `LOW-EDGE` = in-band but near floor; `SURV` = survives (boss/mini rooms judged on kill + survival).

| Ref kit | open_arena | chokepoint | magic_pack | elite_pack | mini_boss | boss_with_adds | Genre anchor |
|---|---|---|---|---|---|---|---|
| **K1 single-target** | **BELOW** ⚠ | **BELOW** ⚠ | LOW-EDGE | IN | IN | IN | D3 single-target dummy-DPS / the harness-not-playspace canary |
| **K2 radius-AOE (nova)** | IN | LOW-EDGE | IN | IN | LOW-EDGE | LOW-EDGE | PoE nova/Cyclone screen-clear |
| **K3 line/cone-AOE** | ~~LOW-EDGE~~ **BELOW** (§ 2-S.3 refinement) | **IN (best)** | IN | IN | LOW-EDGE | LOW-EDGE | Glacial Cascade / corridor-hold |
| **K4 mobile-AOE farmer** | **IN (direction CERT 9/9; ≥K2 *per-seed margin* M1-deferred — § 5.1)** ⚠B | IN | IN | IN | IN | **SURV (via kite)** ⚠C4 | D3 zoom-DH / PoE deadeye-mapper — the chase fantasy |
| **K5 proxy/summoner** | **IN** ⚠ | IN | IN | IN | LOW-EDGE | LOW-EDGE | D2 skeleton-army — the 100%-1D-fail archetype, S-tier in density |
| **K6 tank** | LOW-EDGE (Def) | LOW-EDGE | LOW-EDGE | LOW-EDGE | SURV | **SURV (eHP, ≠K4 mechanism)** ⚠C4 | the defensive-bridge tank, commit-grade |

⚠ = **canary cell** (engine must produce this *exact* direction or it is lying genre-fatally):
- **K1 BELOW at the density rooms** — single-target *must* fail to clear; if it passes, 1D's lie has leaked into 2D.
- **K5 IN at open_arena** — the summoner that fails 100 % of 1D duels *must* be density-S-tier; if it fails, proxy density isn't credited (the BC coverage-audit blind spot, made fatal).
- **K4 IN at open_arena (≥ K2)** — proves B (movement-as-setup). **The two halves of this canary are now DISPOSED separately — see § 5.1 (the W-C-full RESOLVE ruling).**
- **K4 vs K6 distinct survival at boss** — proves C4 (the AI distinguishes kite-survival from eHP-survival).

### 5.1 K4 ⚠B canary disposition — W-C-full RESOLVE ruling (Matt-ratified 2026-06-13)

> **Amendment, W-C-full close (2026-06-13).** The K4 ⚠B canary is **split into a CERTIFIED direction and a DEFERRED mechanism**, ratified by Matt ("t-test logged not gated, and the M1 re-close as the with/without ablation"). This is the design-authority read gandalf escalated; Matt declined the t-test as the gating basis. The split:

**(direction — CERTIFIED at RESOLVE):** `K4 IN @ open_arena` reproduces **9/9 seeds** (gamora cert, `output/wc-full-resolve-n9-2026-06-13.json`), and `K4 ≥ K2` holds on the **mean ordering (45.2 ≥ 41.1)**. The canary's design intent — the mobile farmer is density-viable and out-paces the stationary nova — is **met**. RESOLVE PASSES on this basis.

**(mechanism — DEFERRED to W-D, M1-gap-blocked):** the `≥ K2` *per-seed margin* reproduces only **6/9 seeds**. This is **NOT a band-edge issue** (both kits are solidly IN every seed) and **NOT spawn-spread-tunable** — gamora's four-geometry smoke test (math note § 4.5) empirically disproved spawn-spread as the lever (see § 2-S.5 finding 3, upgraded). The per-seed margin would require **movement-as-gather**, a primitive the engine *does not have*: `spatial_engine.py:1166-1193` advances the player to the **nearest** mob until in attack range, with **no reposition-to-gather-into-AOE** behaviour. K4's higher `movement_speed` therefore credits faster *closing*, not *gathering* — so the per-seed margin is **closing-time noise, not movement-as-setup credit.**

**Why the per-seed margin is NOT the gate (the load-bearing design call):** certifying the per-seed margin *now* would certify closing-time noise **as if it were the gather mechanism** — a mechanism the engine was never built to have. That is rule-shopping: minting a passing number for a movement-credit model that does not exist. **You do not certify a mechanism that does not exist.** The genre-fatal failure this canary guards against is the engine *not crediting movement at all* (modeling movement only as flee, § 4.B); the **9/9 IN direction proves movement IS credited** for closing. The per-seed margin is a *stronger* claim — that movement is credited as AOE-coverage *setup* — and that claim is honestly **not yet true**, so it is recorded as a **binding W-D obligation** (§ 5.2), not papered over with a noise-derived pass.

**(t-test — LOGGED as corroboration, NOT the gate):** jack-ryan computed the paired one-sided t-test on per-seed `K4 − K2` (kit-vs-kit paired comparison): **t = 2.207, p = 0.029** → K4 > K2 is statistically significant. This is **logged as a methodology note that the mean-ordering direction is not seed-noise** — it corroborates that the *direction* is real. It is **NOT the gating basis.** The gate basis is **direction certified (9/9 IN + mean ordering) + mechanism known-absent (M1 gap, deferred).** Matt explicitly declined the t-test as the basis: a significant difference between two kits' closing-times does not prove the gather mechanism, and the gather mechanism is what the per-seed margin would otherwise be read to certify.

### 5.2 The M1 gather-primitive — binding W-D/W-F obligation with a with/without ablation acceptance test

> **Amendment, W-C-full close (2026-06-13), Matt-sharpened.** gandalf proposed a threshold-holds re-close test ("K4 ≥ K2 per-seed margin holds ≥ seed-majority once the gather-primitive lands"). **Matt SHARPENED it to a with/without ablation** — a causation-proving test, not a threshold-holds test. This is the binding empirical criterion that re-closes the K4 ⚠B canary's deferred mechanism half.

**The obligation (named W-D/W-F item, gated — not "revisit someday"):** the engine-movement seam (rocket / engine-movement owner; KR sequences) builds an **M1 player-gather/centroid primitive** — when a combatant carries an area skill, it repositions toward the pack centroid to maximize AOE coverage before casting, rather than only closing to the nearest mob.

**The acceptance test (Matt's sharpened form — ABLATION, not threshold):** the obligation is met when the cert runs `K4 ≥ K2 @ open_arena` **WITH the gather-primitive present vs WITHOUT it (primitive ablated to the current nearest-mob behaviour)** and demonstrates that **the primitive is the CAUSE of the per-seed margin re-closing** — i.e. with-primitive the per-seed margin reproduces (≥ seed-majority), without-primitive it does not (reproducing today's 6/9 closing-time-noise result). The margin re-closing **must be attributable to the primitive**, not to closing-time noise or spawn layout. This directly protects against certifying closing-time-noise as the gather mechanism — the exact risk § 5.1 names.

**MEASURE / W-D inherits this.** This obligation is a W-D scope item; W-F may carry the commit-grade re-validation if the primitive lands after the boss-room work. Until the ablation passes, the K4 ⚠B canary's *mechanism* half is **open-and-gated**; its *direction* half is **certified-closed** (§ 5.1). RESOLVE / W-C exits on the direction; the mechanism rides into W-D as the named gate.

> **Amendment, W-D close (2026-06-13), Matt-ratified disposition (b) — the ablation RAN and returned a NEGATIVE causal result. The K4 ⚠B canary's deferred *mechanism* half is now DISCHARGED-NEGATIVE, not open.**
>
> The M1 gather-primitive was built behind a default-off flag and the with/without ablation ran on the SAME seeds + SAME spawn layout (gamora, math note `wd-six-axis-measure-build-2026-06-13.md` § 10.3; engine `5ec33bb`, tag `gamora/v-wd-six-axis-measure-1`). The result **does not re-close the per-seed margin — it INVERTS it:**
>
> | Condition | K2 KPM | K4 KPM | K4 − K2 | per-seed K4 ≥ K2 |
> |---|---|---|---|---|
> | **WITHOUT gather** (current nearest-mob) | 41.35 | 45.35 | **+3.99** | **6/9** |
> | **WITH gather** (centroid reposition) | 69.57 | 66.12 | **−3.44** | **1/9** |
>
> **Mechanism (diagnosed, Discipline #11 — not assumed):** the gather primitive is an **AOE-coverage primitive, not a K4-movement-specific one.** Both K2 (stationary nova) and K4 (mobile farmer) carry an area skill, so both gather. Gathering benefits the STATIONARY nova *more*: once mobs are pulled to the centroid, K2 clears them in place at full uptime while K4's movement-speed edge — which credited faster *closing* — no longer differentiates. K2 lifts +70% (41→70); K4 lifts +47% (45→66); the margin inverts. **This is the with/without ablation Matt sharpened, returning a clean negative: the primitive is NOT the cause of a margin re-close.**
>
> **The (b)-close (Matt-ratified):** the K4 ⚠B per-seed margin is **closing-time noise**, and the K4 ≥ K2 *mechanism* obligation is **DISCHARGED-NEGATIVE** — the primitive was built, the ablation ran, the hypothesis is disproven. It is **not left open as a "revisit someday."** The recognition → validate → commit discipline is satisfied: the deferral Matt personally ratified at W-C re-opened *on the ablation evidence* and closed against it. The **direction half stays CERTIFIED unchanged** (§ 5.1: K4 IN @ open_arena 9/9 + mean ordering ≥ K2). The per-seed margin is no longer a gate on anything.
>
> **The mobility-home reframe (where mobile-kit identity actually lives):** the empirical result re-routes the design question. A mobile kit's identity is **NOT** "out-clears a stationary nova in an open clear" — gather proves coverage, not mobility, dominates that room, and the stationary nova is already optimally positioned once the pack is gathered. A mobile kit's identity is **kite-survival under sustained pressure** — staying alive and dealing damage while a threat chases. That lives in the **boss room**, and the oracle already carries it: the existing **K4 SURV-via-kite ⚠C4 cell** (§ 5 row K4 @ boss_with_adds) under **MEASURE condition 5** (§ 6.2). So the rooms split cleanly by what they discriminate: **open_arena = a coverage room** (where K4's direction is certified but its margin-over-K2 is coverage-noise, not mobility-credit); **boss_with_adds = the mobility room** (K4 SURV-via-kite, distinct from K6 eHP-survival — the C4 canary that proves the AI distinguishes kite-survival from tank-survival). The mobility identity was never genre-fatally missing; it was being looked for in the wrong room.
>
> **The farming-mobility coverage-edge + margin-vs-parity fork — LOGGED AS AN OPEN DESIGN-CALL, NOT A BUILD (Matt's wording).** A residual design question survives the discharge: in a *farming/clear* context, should a mobile kit hold a coverage-edge over a stationary nova (margin), or is coverage-parity the genre-correct outcome (the clear room rewards coverage, and mobile vs stationary is differentiated elsewhere — kite-survival)? Diablo's zoom-Demon-Hunter and PoE's deadeye-mapper both lean *margin* (movement IS a farming edge); a strict AOE-coverage model leans *parity*. This is logged **OPEN** — it does **NOT** spawn a build, a new primitive, or a re-spec of gather. If a future room/mechanic is designed to credit farming-mobility as a coverage-edge, *that* design work re-opens this fork with its own acceptance test. For now: open design-call, no build.
>
> **Speed-gated gather REJECTED as rule-shopping (§ 5.1 reaffirmed):** the candidate "fire gather only when movement_speed exceeds a threshold so K2 doesn't gather" is gerrymandering the primitive to the kit to mint a passing number — the exact rule-shopping § 5.1 forbids. You do not gerrymander a primitive to certify a margin. Rejected.
>
> **The gather primitive stays in-engine, default-off (brownfield-safe).** It is a *correct* AOE-coverage model — it is simply not the K4-margin lever. RESOLVE re-confirmed PASS with the flag off (math note § 10.6); the production/RESOLVE path is byte-identical. The primitive is the built artifact the ablation exercised; it is not reverted. If it is ever promoted to default-on, *that* is the Discipline #12 semantic shift (closing → gathering) requiring a decisions-log entry — deferred to that promotion decision.

---

## 6. The certification gate — TWO certs, sequenced

> **Amendment 2026-06-13 (v1.1, per Matt challenge):** v1 bundled both certs into one 5-condition gate and hard-coded "the 8-axis bin" in condition 4 — which presumed the BC measurement-coverage audit's answer. It does not. The gate is now split into **RESOLVE** (gates W-C; *not* downstream of orphans) and **MEASURE** (gates W-D/W-F; downstream of the coverage audit), and MEASURE's arity consumes the Bucket-B ruling rather than presuming 8 (§ 6.3).

The oracle certifies two distinct engine responsibilities, and they gate **different wave phases** because one is downstream of the coverage audit and one is not.

### 6.1 RESOLVE cert — gates W-C (orthogonal to orphans)

> **RESOLVE CERT RESULT — PASSED for W-C-full (2026-06-13, Matt-ratified).** gamora's N=9 cert (`output/wc-full-resolve-n9-2026-06-13.json`, tag `gamora/v-wc-full-resolve-1`, math note `wc-full-resolve-cert-2026-06-13.md`) reproduced **36/36 reference-kit § 5 rows** on their pre-registered side (incl. Matt-ratified K3@open_arena = BELOW, 19.5 < 21.5), the **shape-flip** (K2 41.1 > K3 19.5 @ open; K3 33.1 > K2 25.2 @ choke, 9/9), the **held anchor** (K2@open 41.06, within ±20% of A=43), and the **three KPM canaries** (K1@open BELOW 9/9; K1@choke BELOW via t-test t=−3.75 p=0.0028; K5@open IN 9/9). **The K4 ⚠B canary RESOLVE disposition: direction CERTIFIED (9/9 IN + mean ordering 45.2 ≥ 41.1); the ≥K2 per-seed-margin *mechanism* DEFERRED to W-D (M1 gather-primitive gap, § 5.1); the paired t-test (t=2.207, p=0.029) is LOGGED as corroboration the direction is not noise, NOT used as the gate.** RESOLVE PASSES on **direction-certified + mechanism-known-absent**, not on the t-test. W-C exits; the M1 gather-primitive rides into W-D as the named with/without-ablation gate (§ 5.2).

The spatial engine **resolves combat correctly** when **all** hold:

1. **All six reference kits reproduce their § 5 row** within tolerance (tolerance per § 7), **judged against the spatial band `SPATIAL_ENCOUNTER_KPM_BAND` (§ 2-S), not the 1D § 2 table.** (§ 5 row K3@open_arena reads BELOW per the § 2-S.3 refinement.)
2. **All four canary cells** (⚠) produce their required **direction** — non-negotiable; a near-miss on a *direction* is a fail. **Caveat (§ 2-S.4): the K1@chokepoint canary is variance-sensitive at N=5 (4/5 BELOW); its strict-every-seed disposition is the subject of the triggered legolas consult — W-C-full sets the choke seed-count/majority rule before hard-gating on it. The three open_arena canaries are 5/5 stable.** **K4 ⚠B carve-out (W-C-full ruling, § 5.1): for K4 the RESOLVE *direction* is `K4 IN @ open_arena (9/9) + mean ordering ≥ K2` — that is the canary, and it PASSES. The `≥ K2` *per-seed margin* is NOT a RESOLVE gate** (it would certify a movement-as-gather mechanism the engine does not have — M1 gap); it is deferred to W-D under the with/without ablation acceptance test (§ 5.2). The paired t-test (t=2.207, p=0.029) is logged as corroboration the direction is not noise, not as the gate.
3. **The shape-flip manifests** — K2 and K3 swap ranking between open_arena and chokepoint (§ 3.2). (Spike-confirmed: K2 43 > K3 19 @ open; K3 32 > K2 26 @ choke — stable across all 5 seeds.)

This cert is **independent of the orphan/coverage question.** The reference kits are *hand-authored* known-correct, so they bypass generation's allocator orphans entirely (the built-lever-no-allocator failure that bit the defensive bridge cannot bite a kit constructed by hand). RESOLVE is the **deepest prerequisite in the whole architecture**: the engine has never produced a verified run, and the MEASURE cert below (condition 5, the defensive-bridge commit-grade re-validation) *cannot run until RESOLVE passes* — re-validating anything in the boss room needs a working spatial engine. RESOLVE is therefore **upstream of the orphan work's own final step**, not after it.

### 6.2 MEASURE cert — gates W-D / W-F (downstream of the coverage audit)

The spatial engine **measures kit identity correctly** when **both** hold:

4. **The complete axis surface is computed from spatial telemetry** — every axis *per the Bucket-B coverage ruling (§ 6.3)* is assigned from the spatial run (replacing the placeholder `bc_cell`) and **wired, not default-valued** (the Bucket-A check, on the spatial seam); the result is minted as a `CommitGradeVerdict` (companion § 3.1).
   - **4-discrim (the discrimination sub-clause — Matt HARD CONSTRAINT, 2026-06-13: `wired-not-default ≠ discriminates`).** cond. 4 as written is a **Bucket-A gate** (wired-not-default + mint). It is **NOT, on its own, a discrimination claim**, and a cond.4 PASS may **NOT** be read as § 6.4's *"the archive measures the current kit."* A `CommitGradeVerdict` mints when 8 axes are wired; that an axis is wired does **not** establish that it *separates* kits. The discrimination accounting is a **separate, named artifact**: the per-axis discrimination decomposition (gamora → gandalf, `agentic_orchestration/gandalf/notes/2026-06-13-wd-per-axis-discrimination-decompose.md`), which classifies each non-discriminating axis as (a) DEFERRED-no-mechanic, (b) REFERENCE-SET-UNDIFFERENTIATED, (c) WRONG-ROOM, (d) LOCK-EDGE mis-threshold, or (e) **LIVE OBLIGATION** (should-discriminate-now-but-doesn't with no benign reason). **cond. 4 PASS = Bucket-A satisfied; the discrimination map is what § 6.4 closes against (see § 6.4).** Downstream: the W-D export carries the explicit caveat *bins are wired-not-yet-fully-discriminating* and is **not** stamped "measures the kit."
5. **The defensive bridge re-validates commit-grade** in boss_with_adds — tank/mitigator/dodger/glass separation holds on the spatial boss room, not just the 1D duel panel.

### 6.3 The arity is NOT settled at 8 — it consumes the coverage audit

v1 said "the 8-axis bin." That presumed the May-20 lock's 8 axes still **cover** the current kit surface. They may not: generation has built proxy-density, charge-stack, T4 mechanics, and companion-binding *since* the lock (`agentic_orchestration/gandalf/notes/2026-06-13-bc-measurement-coverage-audit-query.md` — Bucket A re-opened deferrals + Bucket B unaxised features). That audit's own § 7: certifying the archive kit-complete before it runs *"would repeat the keystone's mistake one architectural layer up."* So MEASURE's arity is whatever the **Bucket-B design ruling** (routed to gandalf) determines — 8, or 8+N. If Bucket B promotes (e.g.) proxy-density to a real axis, then condition 4 wires a 9-tuple **and this oracle's reference-kit set (§ 5) grows a 7th kit that varies on the new axis** — without it, the engine would measure two kits that differ only on proxy-density as identical and cull one (the genre-flattening this whole architecture exists to prevent). The **Axis-4 defensive orphan is already handled** — sized + ruled ONE-OFF (`agentic_orchestration/gandalf/notes/2026-06-13-bc-orphan-sizing-ruling.md`), sitting in condition 5; § 6.3 is about the *broader* coverage question the second audit, still in flight, owns.

> **ARITY RULING — gandalf, 2026-06-13 (the held D4-gate question; this RESOLVES the "8 or 8+N").**
>
> **RULING: arity STAYS 8. Proxy-density is NOT a new 9th axis; it is the EXISTING Axis-2A. D4's spatial-proxy port wires the existing 8-tuple's 2A slot — it does NOT grow the tuple, and it does NOT add a 7th § 5 reference kit *as a new-axis kit*.** D5's rocket reference-kit is **arity-8**; it contributes to arity-8, not arity-9.
>
> **Why proxy is Bucket-A, not Bucket-B (the load-bearing distinction).** The Item-4 question conflated two things the audit kept separate. **Proxy-density already HAS a lock axis — Axis 2A** (`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`). It is a **Bucket-A re-opened deferral** (lock-deferred, built-since, measurement-not-yet-wired-on-the-spatial-seam), NOT a Bucket-B unaxised feature. The Bucket-B ruling (`agentic_orchestration/gandalf/notes/2026-06-13-bc-bucket-b-unaxised-rulings.md`, ratified ZERO-new-axes @ arity=8 at the W-C.5 close) already ruled the 5 genuinely-unaxised post-lock features, and **folded the companion's in-fight combat contribution INTO Axis-2A** — it did not create an axis for it. So proxy/companion are *both* already homed in the existing 2A slot. D4 builds the *mechanic + measurement* that makes 2A discriminate; it does not discover a new dimension. Wiring 2A is closing category-(a)-DEFERRED on an axis that already exists in the 8 — it is the same architectural move as the Axis-4 defensive bridge (wiring an existing-but-unmeasured lock axis), not the introduction of a new one.
>
> **The other Bucket-B unaxised features (charge-stack, T4, companion-binding per the coverage-audit) — also no new axis.** Charge-stack → Axis-5 (`damage-taken-converts`/resource economy, cross-captured). T4 mechanics (RETRIBUTION/PHASE/GEOMETRY-PROPAGATION/PERSISTENCE) → existing axes via the lock's cross-axis hybrid-capture machinery (Axis 5; Axis 1×3A×3B; Axis 2×3A×3B; Axis 3A×3B). Companion-binding → SPLIT: in-fight proxy → Axis-2A; meta-identity → intentionally OUTSIDE mechanical BC (Earth-meta layer, a different archive). **None clears the new-axis bar** — "a build identity that NO combination of existing axes registers." The bar is high *by design*: the archive is 68,040 cells at ~1.5% occupancy; each new axis MULTIPLIES the space and worsens sparsity, which is exactly why the lock built cross-axis capture instead of dedicated hybrid bins. Pre-imposing a 9th axis for what 2A + cross-capture already home would be the substrate-led discipline violated in reverse.
>
> **What the ruling sets for D4 + D5 (operational consequence):**
> - **D4 spatial-proxy port** wires an **8-tuple** (the existing 2A slot becomes discriminating once `PROXY_FISSION` measures `mean-active-proxy-count` against the § 4.D sustained-wave fixture). It does **NOT** wire a 9-tuple. It does **NOT** grow a 7th § 5 reference kit as a *new-axis* kit — note: K5 (proxy/summoner) **already exists** in the § 5 set as the proxy canary; D4 makes K5's 2A cell *discriminate*, it does not add a kit. (The § 4.C cascade lever's *7th kit* — cascade/chain-AOE — is a separate, post-RESOLVE forward-spec item and is NOT a new axis either; it varies on Axis-2 geometry.)
> - **D5 rocket reference-kit follow-on** is **arity-8** — its CC/resource/tempo/spike-differentiated kits EXERCISE existing axes (2B Control, 5 Resource, 3A Tempo, 3B Variance-spiky) that are currently category-(b) REFERENCE-SET-UNDIFFERENTIATED. D5 makes those axes *discriminate within the existing 8*; it contributes to arity-8.
>
> **Re-open condition (the discipline, not a door left ajar).** This ruling is falsifiable: it re-opens **only** if a future build identity is demonstrated that NO combination of the existing 8 axes + cross-capture registers — at which point that specific feature gets a Bucket-B ruling of its own. Proxy, charge-stack, the four T4 mechanics, and companion are all demonstrated-homed in the existing 8. **Arity = 8 STANDS.**

### 6.4 Wave exit

- **RESOLVE (§ 6.1)** = W-C exit.
- **MEASURE (§ 6.2)** = W-D exit (condition 4) + W-F exit (condition 5).
- Only when RESOLVE **and** MEASURE pass does "the archive measures the current kit" stop being a claim and become a measured fact — and only then does the 1D engine delete (companion § 4).

**The discrimination gate on "measures the current kit" (Matt HARD CONSTRAINT — load-bearing against drift).** "MEASURE pass" above is **not** "8 axes wired" (cond. 4's Bucket-A read). "The archive measures the current kit" requires, in addition to cond. 4 (W-D Bucket-A) and cond. 5 (W-F defensive bridge), that **the per-axis discrimination accounting is CLEAN** — i.e. **every axis either discriminates NOW or is on a tracked-deferred path with a named home** (the § 4-discrim categories a–d), and **zero axes are category (e) LIVE OBLIGATION** (should-discriminate-now-but-doesn't with no benign reason). This is what stops cond. 4 from masquerading as "measures the kit" when § 6.4 closes at W-F (the 1D-delete gate). The accounting artifact is gamora's decomposition (`agentic_orchestration/gandalf/notes/2026-06-13-wd-per-axis-discrimination-decompose.md`).

**W-D discrimination read (gandalf, 2026-06-13 — INTERPRETED against the known-deferred list):** I verified gamora's decomposition against the deferred-axis registry. The accounting is CLEAN. **0 of 8 axes are category (e).** Of 8 BC axes: **1 discriminates NOW** (Geometry; Engagement range-half confirms as its read-back). The other 7 are each wired-not-default with a benign, named home:

| Axis | Discriminates now? | Category | Named home (re-closes at) |
|---|---|---|---|
| 2 Geometry | YES | — | done |
| 1 Engagement (range-half) | YES | — | done |
| 1 Engagement (mobility-half) | NO | (d) LOCK-EDGE | gandalf lock-edge re-calibration on spatial telemetry (raw signal orders K4 highest correctly; the 30/min 1D-calibrated edge collapses the bins) |
| 2A Proxy | NO | (a) DEFERRED-no-mechanic | D4 spatial-proxy-mechanic port + § 4.D sustained-wave fixture |
| 2B Control | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (CC kit) |
| 3A Tempo | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (tempo-spread kit) |
| 3B Variance | PARTIAL (flat/variable YES; spiky NO) | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (spike kit) |
| 4 Defensive | NO (inverts in density rooms) | (c) WRONG-ROOM | W-F boss room (cond. 5 — the oracle's own boundary) |
| 5 Resource | NO | (b) REF-SET-UNDIFFERENTIATED | D5 rocket reference-kit (resource-diff kit) |

Because every non-discriminating axis maps to a tracked-deferred path with a named home and **none is a live obligation**, § 6.4 stays **OPEN-pending-W-F (cleanly), not open-with-a-hole.** The close fires when: (i) cond. 4 PASS [DONE at W-D], (ii) cond. 5 PASS [W-F defensive bridge], (iii) the (a)/(b)/(d) homes have landed or are tracked-deferred with the gate still acknowledging them, and (iv) the accounting re-verifies zero category-(e). The keystone mistake — trusting that what was wired discriminates — cannot recur, because the discrimination map is a named gate, not an implication of the mint.

---

## 7. Methodology-hotspot flag (Discipline #18)

The pack-size calibration (§ 4.A), the movement-credit threshold (§ 4.B), and the verdict tolerances (§ 6) are **design-math calibration choices.** Per the OP § 4.2 refinement (methodology-consultation fires AFTER a baseline exists, not before): the **first** golden master is **genre-design-authored** (this doc, gandalf seam) and validated empirically by the first spatial runs. If, after the baseline runs land, the tolerance/pack-size calibration touches a statistical-methodology question (e.g., how many seeds to call a KPM "in-band" under spatial variance, given the collision/aggro stochasticity), **that** is the point to route a legolas Mode-A methodology consult — not before. The empirical criterion that gates "oracle calibrated" is the reference kits reproducing with stable verdicts across seeds — substrate evidence, not assertion.

**Tolerance starting hypothesis (subject to the above):** a verdict is reproduced if the kit's median KPM across the commit-grade fight count lands on the correct side of the band edge (IN/BELOW/LOW-EDGE) for ≥ the seed-majority; canary cells require the correct side at *every* seed. gamora sets the seed count against the spatial variance once baseline runs exist.

### 2-S.4 — Variance-sensitivity check + legolas consult TRIGGERED (the choke canary)

The recalibration's edges were tested for seed-to-seed verdict stability against the spike's 5-seed data (the § 7 / Discipline #18 criterion for routing a consult). Results:

| Canary cell | Per-seed KPM | Floor | Stability | Disposition |
|---|---|---|---|---|
| **K1 @ open_arena** (BELOW) | 16.3 / 18.8 / 16.5 / 17.1 / 17.8 | 21.5 | **5/5 BELOW — STABLE** | Reproduces. Acceptance ✓ |
| **K5 @ open_arena** (IN) | 34.0 / 38.4 / 34.0 / 30.6 / 36.4 | 21.5 | **5/5 IN — STABLE** | Reproduces. Acceptance ✓ |
| **K4 @ open_arena** (IN ≥ K2) | 41.4 / 45.7 / 41.4 / 45.7 / 45.7 | 21.5 | **5/5 IN — STABLE** for IN; **2/5** for the ≥K2 sub-clause | IN reproduces; the *≥K2 margin* is weak — see § 2-S.5 |
| **K1 @ chokepoint** (BELOW) | 17.2 / 20.9 / 19.2 / 19.7 / 17.0 | 20.5 | **4/5 BELOW, 1 seed (20.9) at the edge** | **VARIANCE-SENSITIVE** |

**The K1@choke canary is the variance-sensitive case § 7 anticipated:** under the strict canary rule (correct side at *every* seed), one seed lands on the wrong side of a compression-room edge — so "how many seeds = a canary pass near a funnel-room edge" becomes a live statistical question, not a design question. **Per § 7 + the dispatch's conditional-only rule, the legolas Mode-A methodology consult is TRIGGERED for this cell only.** The consult question routed to KR: *for a canary in the corridor-compression regime where the single-target rate is queuing-boosted toward the floor, what seed count / majority rule certifies the canary — and is N=5 sufficient, or does W-C-full need a wider seed run for the choke room specifically?* This does **not** block the open_arena canaries (all stable); it scopes a W-C-full methodology decision for the choke room. Note the pack-size lever (§ 4.A) is the *design* response if the consult says the separation is too thin — raising the choke pack widens the K1↔K2 gap.

### 2-S.5 — Findings for KR (before W-C-full)

1. **§5 K3@open_arena refinement: LOW-EDGE → BELOW** (§ 2-S.3). Design-resolved, not a band error — surface for the §5 row update.
2. **K1@choke is variance-sensitive → legolas consult triggered** (§ 2-S.4). Scopes a choke-room seed-count methodology decision for W-C-full; does not block the open_arena acceptance gates.
3. **Risk-B (K4 ≥ K2 @ open_arena): spawn-spread DISPROVEN as the lever — resolved-NEGATIVE, the lever is an M1 gather-primitive.** ~~Initially surfaced (this finding's v1.2 form) as a fixture/spawn-spread tuning item: the IN direction reproduces; the ≥-margin (2/5 seeds spike → 6/9 seeds W-C-full N=9) does not, and § 4.B contemplated widening open_arena's spawn spread so a stationary nova cannot cover all 8 without repositioning.~~ **UPGRADED 2026-06-13 (W-C-full close): spawn-spread is empirically DISPROVEN as the lever.** gamora's four-geometry smoke test at N=9 (math note § 4.5: spike-clump / two-tight-wings / wide-arc / scattered-2D-cloud) shows **no single spawn layout satisfies all four constraints simultaneously** — K4≥K2-per-seed-margin wants spread; K3=BELOW + K5=IN + the A=43 anchor all want clump. The tension among the four constraints is **STRUCTURAL, not a tuning miss.** Root cause (Discipline #11, diagnosed): the player movement AI is *"close to the NEAREST mob until in attack range"* (`spatial_engine.py:1166-1193`) — there is **NO** *"reposition to GATHER mobs into the AOE"* primitive. K4's higher `movement_speed` (9.0 vs K2 5.75) only speeds **closing to the nearest mob**, not **gathering** — so the ≥K2 per-seed margin is **closing-time noise, not movement-as-setup credit**, and is **not robustly spawn-spread-tunable.** **The lever is an M1 player-gather/centroid primitive (engine-movement seam), NOT a spawn layout.** Recorded as **resolved-NEGATIVE** (spawn-spread eliminated as the lever; the mechanism gap is identified), not open. The K4 ⚠B canary's direction half is RESOLVE-certified; its mechanism half is the binding W-D obligation with the with/without ablation acceptance test (§ 5.1 + § 5.2). The shipped W-C-full layout is the spike-validated clump (reproduces 36/36 §5 rows incl. K1/K3/K5/shape-flip/anchor cleanly); the rejected arc/scatter geometries dropped K2 off-anchor, a second reason they were not shipped.
4. **K4 ≠ K6 boss-survival canary (⚠C4): pre-classified FIXTURE-BLOCKED, confirmed.** The spike reports the direction inverted (K4 WR≈1.0 SURV, K6 WR≈0.2 TO) because the throwaway-tank fixture (str=50) cannot out-DPS the 60k-HP boss inside 240 s — it kills the 2 adds then stalls. It is **not dying; it fails a DPS check** (gamora note § 7). This is **not a band finding and the recalibrated § 2-S band does NOT depend on it for RESOLVE** — the boss rooms judge on SURV, and the eHP-vs-kite mechanism distinction re-validates commit-grade in **W-F** against rocket-hardened fixtures. Per the dispatch's two-tier disposition this is tier-(b): documented, not re-litigated, not an acceptance gate for this recalibration.
5. **Baseline sufficiency: CONFIRMED adequate.** No fresh spatial runs were needed to re-draw the band (dispatch out-of-scope item). The 5-seed spike is sufficient as the scale anchor; the one place it is *thin* (choke canary, finding 2) is surfaced as a methodology consult, not a baseline-insufficiency halt.

---

## 8. Cross-references

- Drift-proofing + cert wave (companion; the wave this gates): `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md`
- Forward-architecture contract § 5 (commit-grade = 2D playspace): `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md`
- Prior scenario-design authority (the 6 rooms): `canonical/story/gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md`
- BC axes lock (the 8 axes commit-grade BC computes): `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- External TMPM scale anchor (§ 2-S.0(b-ext) absolute-scale cross-check): `canonical/story/historical/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 3.2 (TMPM 30-50 demo-context canon)
- Verified code anchors (2026-06-13): scenarios `spatial_gauntlet/arena.py:283-712`; KPM bands `gauntlet_sim.py:206-311`; throughput `gauntlet_sim.py:318-322`; archive insert `gauntlet_archive.py:208`; placeholder cell `balance_loop.py:2827`
- ground-state oracle registration: `canonical/00-ground-state.md` § 1

---

**Signed:** gandalf, 2026-06-13
**For:** the hand-authored ground truth that turns the 2D spatial engine from unvalidated scaffolding into a certified, sole behavioral-identity authority — six rooms anchored on the already-designed KPM bands, with Matt's three risks (AOE-only pack count, movement-as-AOE-setup, pinned mob AI) baked in as canary acceptance tests, and a reference-kit set that uses the genre's own diversity (single-target / radius-AOE / line-AOE / mobile-farmer / summoner / tank) as the instrument that proves the engine teaches the genre rather than flattening it.
