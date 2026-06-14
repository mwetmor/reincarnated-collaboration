# Dispatch — 2026-06-13 — gandalf — Recalibrate the KPM bands to the spatial instrument (oracle §2/§4.A)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-06-13 — Option (1), separate gandalf recalibration BEFORE W-C-full. Verbatim rationale: *"the band's numbers will come from spatial runs either way, so independence isn't protected by who derives them — it's protected by the band's structure (the designed AOE/single-target separation + the canaries), which must be gandalf-authored, not defaulted to the engine's own distribution. Folding into W-C-full turns the cert into 'the engine matches itself.'"*
**Status:** GATE-1 PASS (jack-ryan DESIGN-MODE, 2026-06-13 — WARN: four items folded — WARN-1 operational circularity-guard ordering, WARN-2 consumption-interface naming, WARN-3 two-tier canary disposition, INFO-3 per-cohort in acceptance). FIRES on Matt go. Then KR authors W-C-full against the corrected band.
**Estimated effort:** ~hours (design-math re-derivation against an existing baseline; you authored the original §2).
**Acceptance:** The oracle's §2 bands are re-drawn in **spatial pack-clear units** such that, against the W-C de-risk spike baseline (`output/wc-derisk-spike-2026-06-13.json`, 6 kits × 6 rooms, 5-seed), **the edge-placement canary directions and the shape-flip are reproducible as IN/BELOW/LOW-EDGE verdicts** — i.e. K1 single-target falls BELOW the density-room floor, K2 radius-AOE lands IN, K5 proxy lands IN at open_arena, K4 ≥ K2 at open_arena, and K2↔K3 rank-flip between open_arena and chokepoint. (The K4 ≠ K6 boss-survival canary is KNOWN fixture-blocked in the spike — see the canary bullet; it is NOT an acceptance gate for this dispatch.) The band must be authored from the **designed separation**, NOT set equal to the engine's observed distribution (the circularity guard below). **AND** the per-cohort band assignment (§ Scope, per-cohort bullet) is resolved to a state gamora can wire — either all four spatial cohort columns derived, or an explicit documented reduction to the cohort(s) the RESOLVE reference kits actually use, with rationale.

## Context

The W-C de-risk spike (gamora, `gamora/v-wc-derisk-spike-1`, engine `275e7a3`) produced the engine's **first verified spatial run** and surfaced the single finding that most shapes W-C-full: **a KPM-instrument mismatch.** All 36 spike cells read *below* the band floor — not because the engine under-kills, but because the band edges in `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311) are derived from the **1D 1v1-duel kill-rate** (floor 137–836), while the spatial engine clears an ≤8-mob pack at KPM ~44 (numerator bounded by pack size over the room window). jack-ryan independently confirmed this is a **real instrument mismatch, not a masked engine bug** (Gate-2, this session): the spike shows genre-correct internal differentiation (shape-flip K2/K3 by room, K6 tank lowest everywhere, mob-kill degrades correctly by room) — a masked bug yields flat output. To reach the 1D floor of 150 with 8 pack-kills would require a mechanically-impossible 3.2 s clear; the ceiling is bounded arithmetic, not under-killing.

**Consequence:** the RESOLVE cert (oracle §6.1) **cannot pass** against the 1D-unit band — every kit reads BELOW, so the band can no longer distinguish a correct AOE clear from a correct single-target rejection. The band must be re-expressed in the spatial instrument's units *before* W-C-full can certify anything. You are the oracle's design authority (§ spec header); §2 is your seam.

**Why this is its own dispatch and not folded into W-C-full (Matt's structural reason):** if gamora recalibrated the band inside the cert phase, the band would default to the engine's own observed distribution and the cert would degenerate to "the engine matches itself." Independence is protected by the band's **structure** — the designed AOE/single-target separation and the canaries — which must be **gandalf-authored from genre design**, then *imposed on* the engine as an external judge. The spatial runs supply only the **unit-scale anchor** (what KPM is physically achievable in pack-clear); the *separation* between archetypes is your design call, not a readout.

## Required reading before starting

- **Your own oracle spec** `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — §2 (the band table you re-draw), §4.A (pack-tuning — STAYS LIVE), §5 (reference-kit verdict table + the four ⚠ canaries), §6.1 (RESOLVE cert the band must make passable), §7 (methodology hotspot — the legolas consult condition)
- **The spike baseline** `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json` (the scale anchor — what KPM each kit×room actually produces in spatial units, 5-seed) and gamora's spike note `reincarnated-engine/src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md` (the per-module triage + the KPM-mismatch finding in gamora's own words)
- **jack-ryan Gate-2** (this session's verdict, relayed via KR / handoff `skill_handoff_2026-06-13.md` cert-wave section) — the masked-bug-refutation reasoning; INFO-4 (the spike used a single "Balanced" cohort band — your recalibration must address per-cohort band assignment, since §2 has four cohort columns)
- The W-C.5 close `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` (arity = 8 ratified; do not re-open)

## Cross-seam contract change? (Principle 6 gate — KR pre-assessment)

**YES — but the SEAM SPLIT matters.** Your deliverable is the **oracle §2 band spec** (canonical doc, your authority). The **`ENCOUNTER_COHORT_KPM_BAND` code constant in gauntlet_sim.py is gamora's seam** and is updated in W-C-full, not here. Do NOT edit gauntlet_sim.py. Your recalibrated band is the *spec gamora wires to*.

**LOAD-BEARING OPEN QUESTION you must resolve + document (do not silently pick):** the existing `ENCOUNTER_COHORT_KPM_BAND` is the **1D gauntlet's production judging band** — the 1D engine still uses it and is not deleted until W-F. If the recalibration *overwrites* that constant, it breaks 1D judging mid-wave. KR's lean (not a decision): the spatial-instrument band should be a **separate band** (a spatial variant the RESOLVE cert reads), leaving the 1D band intact until W-F deletes the 1D path — but you own this call. Decide whether the recalibrated band (a) replaces the constant, (b) is a parallel spatial-only band, or (c) something else; document the choice and its W-F cleanup implication.
- **jack-ryan Gate-1 WARN-2 (fold):** your resolution must specify the concrete **consumption interface** — the *name/shape* gamora's RESOLVE cert reads to obtain the spatial band (e.g. `SPATIAL_ENCOUNTER_KPM_BAND` as a sibling constant, or a documented selector/flag on the existing structure), not merely the replace-vs-parallel decision. W-C-full wiring depends on this being unambiguous; a half-answered open question (decision made, interface left implicit) is a silent cross-seam contract drift. The interface name/shape is a **required output**, not optional.

## Scope

- [ ] **Re-draw the §2 band edges in spatial pack-clear units**, per (room × cohort), anchored to the spike baseline's achievable-KPM scale — preserving the §2 *designed separation*: density rooms (open_arena, chokepoint) demand a clear-rate single-target cannot reach; boss rooms (mini_boss, boss_with_adds) sit at single-target rates.
- [ ] **Circularity guard (the whole point — jack-ryan Gate-1 WARN-1, load-bearing):** author the edges from the designed separation, NOT by setting band = observed engine distribution. **The trap the spike data proves is live:** the AOE/single-target separation is *already visibly present in the engine's own distribution* (open_arena AOE cluster K2/K4/K5 ≈ 34–44 KPM vs single/line/tank K1/K3/K6 ≈ 7–19). If you draw the density floor "where the AOE cluster sits," you have done the forbidden thing (band = distribution) while *narrating* it as design — the design-correct edge and the distribution-fitted edge coincide, so prose cannot distinguish them. **The guard is the ORDERING, made legible:**
    - **(a) FIRST — assert the separation as a ratio/structural invariant with NO spike numbers in hand:** e.g. "the density floor sits at the clear-rate of a kit that lands its area effect on ≥6 of 8 mobs per cast; the single-target ceiling is the rate of one-target-at-a-time kills against a pressuring pack — by construction the AOE clear-rate is ≥`R`× the single-target rate because area hits N mobs per the same cast single-target spends on one." This is genre math, derivable *before* you open the JSON. State the numeric ratio `R` your design requires.
    - **(b) THEN — the spike supplies ONLY the scale anchor (one number):** what KPM a verified ≥6-of-8 AOE clear physically produces (≈34–44). Place the edge by applying your design ratio `R` to that anchor — NOT by reading where the cluster falls.
    - **(c) The doc must show (a) was asserted before (b) was applied** — that ordering IS the operational guard. If you cannot state the separation without the spike numbers, the guard has collapsed and *that itself is a finding for KR.*
    - **Second-order check:** K3 (line) reads 18.8 at open_arena — clustered with single-target K1, NOT with the AOE cluster — yet oracle §5 expects K3 @ open_arena = LOW-EDGE (in-band-near-floor), not BELOW. A distribution-fit floor lands K3 BELOW and **violates its own §5 row.** This is the concrete place "fit the distribution" and "honor the design" diverge; resolve it by design (your `R` and the LOW-EDGE definition), and surface to KR if it cannot be reconciled against the spike.
- [ ] **Per-cohort columns (jack-ryan INFO-4):** §2 has four cohort bands (DPS-min-maxer / Balanced / Defensive / Hybrid). The spike collapsed all kits to "Balanced." Decide and document how the recalibrated band assigns per-cohort edges in spatial units (re-derive all four, or justify a reduced set for the RESOLVE-cert reference kits).
- [ ] **§4.A pack-tuning STAYS LIVE:** the "raise pack 8 → 10/12 until K1 single-target falls below the floor *and* K2 AOE stays in-band" mechanism remains an active acceptance lever, now expressed against the recalibrated floor. State the recalibrated floor such that the pack-size lever is still meaningful (i.e. if at pack=8 the K1/K2 separation does not hold under the new edges, the band design directs gamora to raise pack size in W-C-full — the tuning is not frozen by the recalibration).
- [ ] **Canaries = acceptance (jack-ryan Gate-1 WARN-3 — two-tier split):** the ⚠ cells split by disposition, because they are not the same severity:
    - **(a) Edge-placement canaries — K1 BELOW density, K5 IN open_arena, K4 ≥ K2 open_arena:** pure KPM-direction reads you CAN verify against the spike. Each must be expressible as a pass/fail direction against the recalibrated band and reproducible against the baseline JSON. If any does NOT reproduce under your re-drawn edges, that is a finding KR needs BEFORE W-C-full (mis-placed edge OR a real engine gap masquerading — flag it, do not paper over it). These are acceptance gates.
    - **(b) The K4 ≠ K6 boss-survival canary (⚠C4) is KNOWN not-reproducing in the spike** — the spike reports the direction INVERTED (K4 WR≈1.0, K6 WR≈0.2) due to the **throwaway-tank fixture's DPS limitation** (gamora spike note §7), NOT an engine gap, and NOT a band-edge issue. **Document it as fixture-blocked, do NOT re-litigate it as a band finding, and confirm the recalibrated band does not depend on it for RESOLVE.** It re-validates commit-grade in W-F's boss room against rocket-hardened fixtures; it is out of this dispatch's acceptance.
    - **Do not hard-block on canary failure** — the K4≠K6 case shows a hard-block would fire on a known fixture issue and stall the dispatch. Surface-as-finding (tier a) / pre-classified-fixture-blocked (tier b) is the correct disposition.
- [ ] **legolas Mode-A consult — CONDITIONAL ONLY (Matt + Discipline #18/§7):** route a legolas methodology consult **only if** the in-band rule proves variance-sensitive — i.e. if, against the spike's 5-seed data, IN/BELOW verdicts flip seed-to-seed near an edge such that "how many seeds = in-band" becomes a live statistical question. If the 5-seed verdicts are stable (the spike reported K2 5-seed stable), do NOT route a consult — document that the variance criterion was checked and not triggered.
- [ ] Amend §2 (and §4.A / §7 as needed) in the oracle doc; mark the revision clearly (the band is now spatial-instrument; the 1D-unit table is preserved as historical-rationale or annotated per your open-question resolution).
- [ ] AGENT_STATE / notes housekeeping; (no tag — canonical/doc work, auto-commit eligible per the team commit addendum; NOT pushed — Matt's wave-close gate).

## Out of scope (explicit non-goals)

- **Editing `gauntlet_sim.py` `ENCOUNTER_COHORT_KPM_BAND`** — gamora's seam, wired in W-C-full to your spec.
- **Running new spatial runs** — the spike baseline is your scale anchor; you do not need fresh runs to re-draw the band (if you find you *do*, that itself is a finding to surface — it would mean the baseline is insufficient and W-C-full needs a wider run first).
- **Re-opening arity** (8, ratified — W-C.5 close), the §5 reference-kit count (6, no 7th — nothing promoted), or the §6 cert structure (RESOLVE/MEASURE split stands).
- **Hardening the spike fixtures into the standing reference-kit instrument** — that is rocket's post-spike-pass §5 hardening, separate; you recalibrate the band against the spike baseline as-is.
- **Pushing to remote** — Matt's wave-close gate.

## Open questions for the agent to resolve (document at completion)

- Replace-the-constant vs parallel-spatial-band vs other (the cross-seam open question above) — your call, documented with W-F cleanup implication.
- Per-cohort band derivation in spatial units (four columns vs reduced set for the RESOLVE reference kits).
- Whether any canary fails to reproduce against the spike baseline under the re-drawn edges (surface immediately if so).

## References

- Oracle §2/§4.A/§5/§6.1/§7: `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`
- Spike baseline + note: `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json`, `reincarnated-engine/src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md`
- W-C.5 close (arity = 8): `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Gate-2 verdict + INFO-4: `agentic_orchestration/skill_handoff_2026-06-13.md` (cert-wave section)

---

**Author:** knight-rider, 2026-06-13. The structural-independence move: re-draw the KPM bands in the spatial instrument's units while preserving the gandalf-authored AOE/single-target separation and canaries — so the RESOLVE cert judges the engine against an external design standard, not against its own distribution. W-C-full is authored against the corrected band once this lands.

---

## COMPLETION RECORD — gandalf, 2026-06-13

**Status:** COMPLETE. Oracle amended to **v1.2**; new **§ 2-S** authored; §4.A / §5 / §6.1 / §7 updated; 1D §2 preserved as historical-rationale. Auto-committed (canonical/doc work, team commit addendum); NOT pushed (Matt's wave-close gate). No `gauntlet_sim.py` edit (gamora's seam, wired in W-C-full).

### The ratio invariant `R` (the circularity guard, ordering-legible per WARN-1)

Stated as genre pack-arithmetic **before** opening the spike JSON: in an `N=8` density room, single-target clears in `N` kill-cycles; a qualifying area kit (≥6 of 8 per cast) clears in `⌈8/6⌉=2` cycles → **`R_expected = KPM_AOE / KPM_ST = 4`** (fixed by `N` and the 6-of-8 threshold, nothing else). **`R_floor = 2.5`** = conservative minimum separation the room must teach. The spike then supplied **only the per-room scale anchor `A`** (the KPM a verified ≥6-of-8 clear physically produces); edges = `A` ÷ a function of `R`, never "where the cluster sits." The doc is written in that order, so the guard is the legible ordering, not a claim.

### Edges drawn (Balanced cohort, spatial pack-clear units)

| Room | Floor rule | Band `(lo,hi)` | Verdict reproduction (spike) |
|---|---|---|---|
| open_arena | `A/√R_expected` (A=43) | **21.5–107.5** | K1 17→BELOW ✓ · K2 43/K4 44/K5 34→IN ✓ · K6 7→BELOW ✓ |
| chokepoint | `A/√R_floor` (A=32.4; funnel-compression rule) | **20.5–81.0** | K1 19→BELOW(4/5) · K2/K3/K4→IN ✓ · K5 22→IN · K6→BELOW |
| magic_pack | `A/R_expected` (A=35) | **8.8–87.5** | all AOE IN; K1 21→IN, K6 10→LOW-EDGE |
| elite_pack | `A/R_expected` (A=15) | **3.8–37.5** | K2/K4/K5→IN; K1/K3/K6 partial |
| mini_boss | `A/R_expected` (A=2.5) | **0.6–10.0** | SURV-judged; KPM a sanity rail |
| boss_with_adds | `A/R_expected` (A=2.2) | **0.6–8.8** | SURV-judged; KPM a sanity rail |

### Open questions — resolved + documented

- **Replace vs parallel → PARALLEL.** Recalibrated band ships as a **separate sibling constant**, leaving the 1D `ENCOUNTER_COHORT_KPM_BAND` intact until W-F deletes the 1D path (overwriting would break 1D judging mid-wave). **Consumption interface (WARN-2 required output): `SPATIAL_ENCOUNTER_KPM_BAND: dict[str, dict[str, tuple[float,float]]]` keyed `[room][cohort]→(lo,hi)`, identical shape to the 1D constant** (one-line source-swap for the RESOLVE cert's lookup). For RESOLVE it carries the `"balanced"` key only. W-F cleanup: remove the 1D constant, this becomes sole band. (§ 2-S.2.)
- **Per-cohort (INFO-4) → REDUCED to Balanced for RESOLVE.** The 6 reference kits are all Balanced-assigned; no DPS/Defensive/Hybrid cohort kit has ever run on the spatial engine, so deriving those three columns now = inventing numbers. Derived in W-D/W-F against cohort-tagged generation kits (MEASURE domain). (§ 2-S.1.)
- **Canary reproduction:** three open_arena canaries (K1 BELOW, K5 IN, K4 IN) reproduce **5/5 stable**. **K1@chokepoint is variance-sensitive (4/5 BELOW, one seed at the edge)** — see legolas trigger below.

### Canary verification

- **Reproduce (tier-a acceptance, PASS):** K1 BELOW @ open (5/5) · K5 IN @ open (5/5) · K4 IN @ open (5/5) · K4 ≥ K2 @ open on the mean. Shape-flip K2↔K3 stable across all 5 seeds.
- **Tier-a finding (does NOT reproduce robustly):** **Risk-B K4 ≥ K2 margin is 2/5 seeds** (1-tick). NOT a band-edge issue (both solidly IN every seed) — a **spawn-spread fixture issue**; surfaced for W-C-full §4.B spawn-spread tuning (rocket lever), not papered over.
- **K4 ≠ K6 boss-survival (⚠C4) → FIXTURE-BLOCKED, confirmed (tier-b).** Direction inverted (K4 WR 1.0 SURV, K6 WR 0.2 TO) because the throwaway-tank (str=50) can't out-DPS the 60k-HP boss in 240 s — it fails a DPS check, is not dying. **Not re-litigated as a band finding; the § 2-S band does NOT depend on it for RESOLVE** (boss rooms judge SURV); re-validates commit-grade in W-F against rocket-hardened fixtures.

### legolas consult — TRIGGERED (conditional condition met)

The variance criterion **fired** for **K1@chokepoint only**: 4/5 seeds BELOW, one seed (20.9) at the 20.5 floor — under the strict every-seed canary rule, "how many seeds = a canary pass near a funnel-compression edge" is a live statistical question. **Route a legolas Mode-A methodology consult** for the choke-room seed-count/majority rule before W-C-full hard-gates that canary. The three open_arena canaries are 5/5 stable and do NOT need the consult. (§ 2-S.4.)

### Findings for KR before W-C-full

1. **§5 K3@open_arena: LOW-EDGE → BELOW** (§ 2-S.3) — design-resolved (line kit in an open room has no funnel; degrades to single-target class; honoring the K1 canary forces K3@open BELOW since the engine produces them at the same rate). Already annotated in §5; flagging for the row-update record.
2. **legolas consult triggered** for K1@choke seed-count methodology (§ 2-S.4).
3. **Risk-B K4≥K2 weak (2/5)** → W-C-full §4.B spawn-spread tuning.
4. **K4≠K6 fixture-blocked** → W-F, not this dispatch.
5. **Baseline sufficiency CONFIRMED** — no fresh spatial runs needed; the one thin spot (choke canary) is a methodology consult, not a baseline halt.

**Signed:** gandalf, 2026-06-13.
