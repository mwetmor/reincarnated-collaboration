# Batch-2 Build Spec — economy axes · economy pilot · the full fresh 18-cell fire (staged, pilot-gated)

> **STATUS:** SPEC-CURRENT v1.2 (2026-07-07) — **Matt rulings embedded (2026-07-06, same session as the faction stack): Q1 = (a) resource-economy as VARIATION AXES · Q2 = (a) full FRESH 18-cell emission · staged pilot-gated sequence (Matt: *"test it on a small, yet representative pool of variably designed kits along the curves before jumping to the full fresh 18 cell emission"*). v1.1 same-day: ADR-002 `resource_economy` generation→sim contract SIGNED (Leg B cleared) · Axis-5 cost-TYPE structural bins = reserved, empty-by-ruling (§8 R1).**
> **Author:** gandalf (SPEC-AUTHOR). **Gates:** ARCHITECT pass (gandalf, run-boundary) → jack-ryan Gate-1 → **Matt run authorization** (fires Leg A). This operationalizes `faction-derivation-stack-spec-2026-07-06.md` §10 step 2.
> **v1.2 (2026-07-07, ARCHITECT reconciliation — gandalf):** the staged sequence EXECUTED through its designed §3 HALT branch. Run authorization fired 2026-07-06 (same session as authoring; serial-content tracker, third same-day entry) · Legs A/B RAN (star-lord fire `bfb6097`→`3a09a4d`, gamora read `6c5303b`, all engine) · **Leg B = pre-registered HALT (0/50 clear)** · the escalation root-caused the failure to the INSTRUMENT, not the casters (dead mob-damage channel + fossilized 2.3384× weapon ratio; casters vindicated, +0.40 F3 margin) · the four-family gauntlet was redesigned + re-certified → **Matt ruled ARC NUMBERS RATIFIED, LEG C UN-HELD** (decisions-log 2026-07-07). **That ruling supersedes §4/§7 "gates-on: Leg B GO"** — Leg C's remaining mechanical gate is the gen-path-pilot-leg3 emission-wire close (Tier-1). §4's per-band criteria are superseded by the ratified four-family cert (mob_damage_scale 0.03 / boss_damage_scale 48.0 / boss HP 9000 / Rider-3 semantics: over-ceiling = FLAG_PASS_OVERPOWERED certify+review, floor = hard fail) wherever they conflict. **Leg-C scope additions (Matt §8-A1 ruling 2026-07-07):** (a) proxy-heavy band coverage read + C2 worst-case peak-entity measurement = REQUIRED Leg-C report items (re-homed from the leg-3 pilot); (b) rocket verifies at Leg-C dispatch whether the fire path consumes `bc_target_composer` (composer un-gate re-homed here; if unconsumed → dead-code flag, not carry).
> **Companions:** derivation-stack spec (the consumer — steps 3–5 fire on this spec's close) · `agentic_orchestration/variation-pilot-run-state-2026-07-06.md` (the closed precedent pilot, Legs 0→4) · gamora Leg-4 report + calibration note (the C2 floor's provenance) · `qa/pending/2026-07-06-leg4-light-read-jackryan.md` (byte-verification `db2df69`).

---

## 0. What this is

The staged build-and-fire plan that produces **the population the faction library is derived from**. Three legs, one authorization: build the economy axes (A), pilot them at representative scale with pre-registered GO/HALT (B), fire the full fresh 18-cell emission (C, gates-on B-GO). Pattern precedent: the variation pilot (closed 2026-07-06, zero wasted compute) — new gen-path capability is never batch-fired blind.

## 1. Banked inputs (no new rulings; cited, not reopened)

| Input | State | Source |
|---|---|---|
| Summon gen-path + INT-cell composition fix | LANDED Leg-1, Gate-2 PASS `a49ccd4` *(collab SHA; engine artifact = tag `rocket/v-pilot-leg1-summon-int-variation-1`)* | Option-1 ruling scope |
| Variation axes (mechanism) | pilot-CONFIRMED — 40/81 emit, chain-variants 15/15, G4 knob z≈−1.0 | Leg-4 report |
| **C2 two chassis bands** keyed on proxy-share 0.25 knob | RULED 2026-07-06 | AV2 relay §1 |
| **Plain-caster floor: 9.90 KPM open_arena / 11.65 chokepoint** | measured, byte-verified (`gauntlet_sim.py:393-394`, read `db2df69`) | gamora calibration note |
| magic_pack 600.0 = tick-quantization ≥-ceiling; elite_pack 426.9 = pack signal of record | diagnosed + verified | Leg-4 |
| Tiered-shells lever | preserved for batch-2 (`4cacf12`, collab SHA) | KR triage record |
| Per-cohort bucket keys | spec line handed forward (gamora) | Leg-4 §6 |
| Scale: ≥100 gauntlet-passed kits/cell × 18 BC cells | ruled (derivation-stack §3; F2 cost-veto survives at consult) | faction stack |
| No LLM anywhere in batch-2 | naming/flavor fires at derivation step 6, post-ratification | derivation-stack §9.5 |

## 2. LEG A — the economy-axes build (rocket; math-first + Gate-1)

**RULING Q1(a):** resource-economy joins the variation build as **explorable axes**, not a hand-tuned config — mana **cost curve**, **regen curve**, and **throughput/cast-cadence** as composable variation dimensions on INT-band kits. The population searches economy space; the gauntlet + C2 floor select the viable region. Substrate-led discipline applied to the economy question: *don't tune the caster — let the population vote on what a viable mana economy is.*

- Scope: rocket math-first (axis definitions, ranges, composition rules — same shape as the landed variation axes); gamora adjacency on sim consumption (the economy must actually bind in fight resolution, not just in decl).
- **Structural honesty clause:** gamora's Leg-4 read (*"band re-tune alone may be insufficient"*) is the motivating finding. Leg A builds the axes; Leg B tests whether economy space contains a floor-clearing region at all. If it does not, the problem is deeper than economy (cast mechanics / damage-vs-trash scaling) — that outcome is a designed HALT (§3), not a failure of this spec.
- Gate-1 (jack-ryan DESIGN-MODE) on the math before Leg B fires.

## 3. LEG B — the economy pilot (star-lord fire · gamora read) — gates-on: Leg A Gate-1

**RULING (Matt):** small, representative pool, **variably designed along the curves**, before the full fire.

- **Cells (2–3, spanning the INT space):** 1 **plain-caster** (proxy ~0 — the floor test) · 1 **summoner** (proxy ≥0.25 — the C2 band-2 certification test) · optionally 1 hybrid/mid cell if marginal cost is trivial (D2, §8).
- **Sampling:** ~25/cell, **coverage sampling across the axis ranges** (grid or latin-hypercube-class — rocket/gamora pick at Gate-1), never clustered at a point. The output is a *map*, so the input must span the space.
- **Instrumentation:** per-cohort bucket keys **LIVE (first use)** — proxy cohorts measure separately (fixes the empty caster_proxy baseline class of miss); measurement-report path (`measurement_report_writer.py`, MIGRATION v2.10) — no demo-bundle coupling.
- **PRE-REGISTERED GO/HALT (registered here, before any fire):**
  - **GO** = (i) ≥1 **contiguous** region of economy space in the plain-caster cell clears **bar_lo solo on BOTH shells** (9.90 open_arena AND 11.65 chokepoint), AND (ii) summoner-band certification executes with per-cohort measurement intact (kit+proxy composite scored; solo timeout non-disqualifying per C2).
  - **HALT** = zero economy configs clear → **escalates to Matt with the measured landscape** (the finding: caster viability is blocked below the economy layer; deeper structural work precedes any 18-cell fire).
- **Outputs consumed by Leg C:** viable-region bounds → per-cell **candidate budgets** for the INT cells (data-driven yield planning; martial cells anchor on batch-1's known 38.9%); validated summoner-band pass criteria; economy-identity read (where the viable region sits: cheap-sustained vs builder/spender vs flat-cost — the caster-feel finding, reported to Matt in the Leg-B report either way).

## 4. LEG C — the batch-2 fire (star-lord; detached) — gates-on: ~~Leg B GO~~ **ARC-NUMBERS ruling (Leg C UN-HELD) + gen-path-pilot-leg3 close** *(v1.2)*

**RULING Q2(a): full FRESH 18-cell emission, all axes live** (variation + economy). One fire, once.

- Per-band gauntlet criteria: **plain-caster band** = solo floor 9.90/11.65 (open_arena/chokepoint) + standing shells · **summoner band** = kit+proxy composite; solo timeout non-disqualifying (C2 / Matt 2026-07-02).
- Tiered-shells config (gamora deploys the preserved lever); per-cohort bucket keys; candidate budgets per Leg B.
- **Run class:** detached, 12–15h estimate (batch-1 = ~6h for 7 cells; Discipline #19 machinery proven), registry-registered, seed+SHA+config reproducibility per PART-C law.
- **Default: auto-continue on Leg-B GO** (the W0→W4 unattended pattern; D1, §8 — Matt may insert a pilot-report checkpoint at review).
- Close: batch-2 run report → derivation-stack §10 step 3 (elrond #18 consult) fires on the emitted population.

## 5. PROVENANCE LAW — who votes in the derivation

**Only the Leg-C population votes.** Batch-1's 700 martial kits, the 35 flavored finalists, the variation-pilot kits, and the Leg-B economy-pilot kits are the **fixture/regression bank** — instruments, never derivation members. Grounds: uniform provenance is the clustering math's integrity condition — pre-axes kits are degenerate in every new dimension, and a mixed population forms clusters around axis-*absence*. The faction library is the game's permanent social fabric (F5 stickiness); no invisible seams baked in.

## 6. Explicitly NOT in batch-2 (consumed downstream, derivation-stack §10)

Naming/flavor (step 6) · clustering + two-cut derivation (steps 3–5) · Matt cut-ratification + race diagnoses (step 5) · roster shopping (step 7) · casting director (step 8).

## 7. Sequence + seams

| Leg | What | Seam | Gates-on |
|---|---|---|---|
| A | economy-axes build (math-first) | rocket (+ gamora sim-binding) | Matt run authorization (this spec) |
| A-gate | Gate-1 on the axis math | jack-ryan | A |
| B | economy pilot: 2–3 cells × ~25, coverage-sampled; bucket keys live; pre-registered GO/HALT | star-lord (fire) · gamora (read/report) | A-gate |
| C | full fresh 18-cell emission + gauntlet, per-band criteria (four-family cert per v1.2), detached ~12–15h | star-lord (gamora shells) | ~~B-GO~~ **UN-HELD (ARC NUMBERS, 2026-07-07)** + leg-3 wire close *(the HALT → Matt branch FIRED and closed as instrument artifact)* |
| close | batch-2 run report → elrond consult fires | star-lord → elrond | C |

## 8. Defaults + open register (override points at review, not blockers)

| # | Item | Default / state |
|---|---|---|
| D1 | Auto-continue C on B-GO vs Matt checkpoint at the pilot report | **auto-continue** (pre-registered criteria make the gate mechanical; HALT always escalates) |
| D2 | Third pilot cell (hybrid/mid INT) | include iff marginal cost ~zero at Leg-B config time |
| D3 | F2 cost-veto (extend-unstable-cells after consult) | survives unchanged at derivation step 3 |
| D4 | Leg-B sampling scheme (grid vs LHS-class) | rocket/gamora pick at Gate-1 |
| D5 | **Leg-B execution: SEQUENTIAL in one registered run** (Matt asked parallel-vs-sequential 2026-07-06; cells are independent by construction — distinct seeds, read-only shells — but Leg B is minutes-class sim and one run = one SHA/config/seed ledger across cells, which the comparative map requires) | sequential, single run record |
| D6 | **Leg-C per-cell SHARDING (the parallelism that matters):** whether the 12–15h fire shards cells across processes hinges on whether the batch runner already parallelizes internally (core saturation on the single Mac host) — gamora implementation fact, resolved at dispatch. Constraints if sharded: distinct seeds per cell (holds by construction) · per-cell output paths · **ONE registry run record with a shard manifest** (PART-C seed+SHA+config law kept whole, never N loose runs) | gamora call at Leg-C dispatch |
| **R1** | **Axis-5 cost-TYPE structural bins** — HP-economy (blood magic) · damage-taken-converts (vengeance) · charge-stack (builder/spender). These are different sim *plumbing* (new resolution paths in fight resolution), not values on the Leg-A curves; batch-2's economy axes explore the **mana substrate only** | **RULED empty-for-now (Matt 2026-07-06).** Three guards, all binding: **(1) registry honesty** — the three bins register `reserved, empty-by-ruling`, never silently absent; the elrond #18 consult (derivation-stack §10 step 3) is told this coverage boundary explicitly, so the clustering never mistakes a ruled-empty region for a measured one; **(2) F5 re-entry pre-registered** — structural-cost arrival in any future batch = a re-derivation event by definition (derivation-stack §11 F5: new-branch entry; existing families expected bootstrap-stable; re-ratification scoped to affected cuts only); **(3) no unbacked claims at naming** — AI-tell discipline at step 6: no blood-magic / vengeance / builder-spender identity language for factions whose kits are mana-only |

---

**Signed:** gandalf, 2026-07-06 (SPEC-AUTHOR). Build the axes, map the space, fire once. ARCHITECT pass next; Gate-1 rides jack-ryan; Leg A fires on Matt's authorization.
