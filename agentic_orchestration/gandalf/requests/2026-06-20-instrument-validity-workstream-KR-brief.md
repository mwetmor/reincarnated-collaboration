# KR brief — instrument-validity workstream (resource → rotation → DoT → mitigation → composed re-baseline → STR-lever read)

**Type:** gandalf-authored brief → **knight-rider sequences** (gamora implement + run per phase; jack-ryan Gate-2 per phase; gandalf gate-dispositions + pre-registration + STR-lever rule). Matt-authorized 2026-06-20.
**Author:** gandalf
**Supersedes / subsumes:** `gandalf/requests/2026-06-20-dot-ailment-activation-and-physical-scaling-fix-run-brief.md` — that brief is **re-pointed as Phase 3 of this workstream**. Do NOT fire it standalone; it was authored before the T1-only-firing discovery and is confounded if run before the rotation fix (the selector never fires a non-zero-tick bleed skill, so DoT-activation alone measures ~zero STR bleed regardless). Its code fixes (Findings 1 & 2) remain valid; only its position changes.
**Composes with:** the STR disposition (`gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §5a — STR ships via the floor, anchor-gap as texture, shippable only with a focus-fire LEVER); the ailment design-debt findings (`gandalf/findings/2026-06-19-ailment-system-design-debt-and-dps-mechanism-correction.md`); the Phase-0 verdicts recorded in §1 below.

---

## 0. Why this workstream (the instrument-validity frame)

Every band-fit to date (str_9pass, Arm A/B, the n=3078 distribution) was measured on a **contaminated instrument**. Four defects sit on the damage equation — two on the offense side, one on the mitigation side, one regime-level:

| # | Defect | Side | Phase-0 status |
|---|---|---|---|
| 1 | **Resource economy un-wired** — pool/cost/regen ride on the entity + telemetry-emit, but the selector never gates on energy and the pool never decrements. Every kit spends freely, forever. | offense (gating) | PARTIAL — modeled-not-wired (gamora 2026-06-20) |
| 2 | **Rotation collapses to single-tier** — selector is shortest-cooldown; `or 2.0` coercion + 0.0-cd capstones + no spender logic → only T1 ever fires. ~¾ of every kit is decorative. | offense (firing) | confirmed O3 (gamora Arm-C re-fire) |
| 3 | **DoT inert + physical-DoT mis-scaled** — DoT `ActiveEffect` never ticked in spatial; physical bleed scales on int/wis not str/dex. | offense (over-time) | confirmed (DoT brief Findings 1 & 2) |
| 4 | **Armor/resist asymmetry** — casters ate ~zero resist, inflating caster bands and boss survive+kill. | mitigation | confirmed (Arm-C diagnostic STOP) |

**The discipline that governs the whole workstream:** each fix is **fix-and-measure-ISOLATED** (bands left UNTOUCHED so each instrument-shift is visible against the *current* bands), and the bands are re-fit **ONCE**, at the tail, against the *composed* instrument. Re-fitting after each fix would be 4 wasted refits and would hide how the fixes compose. This is the multi-re-baseline-trap avoidance.

**The through-line is recompose-first.** Defects 1–3 are all "the substrate designed this; it just doesn't function in the shipping regime." The fix in every case is **port/activate the existing intent, NOT invent a new mechanic** — the kernel even holds a working, tested reference implementation for the resource economy. Same disposition as the DoT-activation ruling.

**Why this is not fire-and-forget:** there are genuine design-gates between phases. They are handled by **pre-registration** (§3): each gate carries a disposition table so KR auto-resolves the expected branch and escalates ONLY named forks to a short gandalf+Matt touchpoint (§4). This keeps sequencing with KR, decisions with Matt, and the gandalf+jack-ryan critique-pair independent of the driver.

---

## 1. Phase 0 — DONE this session (record; do NOT re-fire)

**Resource sim-state (gamora background read, 2026-06-20): VERDICT PARTIAL — modeled-but-not-wired.**
- Entity carries `energy / max_energy / energy_regen / skill_energy_costs` (`spatial_engine.py:436-442`, init `:2057-2059`/`:2150-2152`); skills carry real rolled `energy_cost` (`skill_schema.py:14`, `ability_schema.py:36`, per-role ranges `role_constraints.py:40-122`); the regen tick runs (`:1719`).
- BUT the selector + fire-gate check only cooldown + range (`:1023-1030`, `:1043-1057`, `:1580`). The pool is **never decremented**; `energy_cost` is read only to emit a `resource_spent` telemetry event (`:1585`, `:1641-1648`). The adapter even neutralizes the kernel gate (`spatial_resolver_adapter.py:192` `mana=1e9`, comment "spatial energy gating is upstream" — asserting a gate that does not exist).
- A complete **consuming** economy with 5 energy configs exists in the kernel (`combatant.py:347-385` `can_use_skill` + `_ENERGY_CONFIGS`; `ai_strategies.py:423-518` build-vs-spend) — but its only driver, 1D `fight_engine.py`, was **retired, not migrated** when spatial took over. The 2026-05-08 structural-mana bug is genuinely resolved and is a separate matter.
- **Fix size: WIRE, not BUILD.**

**Canonical design-state (gandalf read, 2026-06-20): the economy is extensively DESIGNED.**
- 8-model catalog, gear-roll-gated by class resource model (doc 42 § 2.2; doc 40 § 6).
- Per-class economy assigned to all 10 Cycle-14 classes (doc 48 § 3.1).
- Resource economy is a load-bearing **progression axis** (doc 41 §: mid-game "emerging rotation depth" → endgame "active resource management critical; full rotation depth").

**Joint implication:** Phase 1 is RATIFY/WIRE, not greenfield. The kernel configs are the port target; the doc-48 assignments are the spec.

---

## 2. The orchestration spine (KR sequences)

| Phase | Work | Seam | Dep | Parallel? | Bands |
|---|---|---|---|---|---|
| **1** | Resource-economy wiring (port kernel configs; energy_type-branched pool + gate + decrement) | gamora | Phase 0 | — | UNTOUCHED (measure delta) |
| **2** | Rotation selector (falls out of Phase 1's energy_type branch; port `ai_strategies` build-vs-spend) | gamora | Phase 1 | — | UNTOUCHED (measure delta) |
| **3** | DoT activation + physical-DoT scaling (the re-pointed DoT brief, Findings 1 & 2) | gamora | Phase 2 | — | UNTOUCHED (measure delta) |
| **4** | Armor/resist symmetry (mitigation-side) | gamora | Phase 0 | **‖ with 1–3** | UNTOUCHED (measure delta) |
| **5** | ONE composed re-baseline (all four live) → new honest bands | gamora + jack-ryan | 1,2,3,4 | — | **RE-FIT HERE** (the only refit) |
| **6** | STR-lever / (A)-vs-(B) measurement against honest bands | gamora run; gandalf rules | 5 | — | honest bands |

Dependency chain: **1 → 2 → 3** (offense-side: resource gates → rotation fires the right tiers → DoT ticks now matter). **4 runs in parallel** (mitigation-side, selector-independent). **5 waits for all of 1–4.** **6 waits for 5.** Each of 1–4 is math-note-first (Discipline #1), recompose-first, jack-ryan Gate-2, semantic-shift declared (Discipline #12 — every KPM number moves at each boundary). Each uses a **fresh disjoint seed base** (Discipline #3; known-used: `[700000,766703]`, `[619000,684303]`).

---

## 3. Phase-by-phase detail + PRE-REGISTERED GATES

### Phase 1 — Resource-economy wiring

**Work (gamora; math-note-first):** port the kernel `_ENERGY_CONFIGS` into the spatial loop. Wire (a) an energy term into `skill_ready()`/the selector so a cast gates on `energy >= effective_cost`, (b) a decrement at the cast site (`:1610-1620`, alongside the existing cooldown set + `resource_spent` event), (c) **energy_type-branched pool behavior** (the generic 100/regen-10 pool is not faithful — rage starts empty + builds on hit; focus starts full + decays; combo is discrete 0–N; charge-stack holds; stamina regens fast). The regen tick (`:1719`) already exists. Math-note estimates expected per-economy spend/regen balance BEFORE wiring, sanity-checked so no economy starves a kit to silence.

**GATE G1 (BEFORE build) — doc-48 label → kernel-config mapping. PRE-REGISTERED:**

| doc-48 class economy (class) | kernel config | status |
|---|---|---|
| charge-stack/rage (Barbarian) | `rage` (build-on-hit, starts empty) | ✓ direct |
| steady (Hoplite, Wildhunter) | `stamina-as-resource` high-regen / mana-default — rarely binds = cooldown-primary | ✓ |
| generator-spender/loader (Siege-Master) | `combo` (discrete accumulate→dump) | ✓ |
| charge-stack/stealth (Assassin) | `charge-stack` (build-and-hold) | ✓ |
| generator-spender/parry (Duelist) | `rage`-on-event / `combo` | ✓ approx |
| generator-spender/ammo (Gunslinger) | `combo` (discrete ammo; reload = refill) | ✓ |
| overflow/mana (Magus; Crusader Banner-Rally) | `mana`-default with binding cap (spam→empty→throttle) | ✓ |
| **damage-taken-converts (Skirmisher)** | **none** (rage builds on damage-DEALT, not taken) | **DEFER** |
| **HP-economy (Crusader Channel-Aura)** | **none** (no health-as-resource config in the 5) | **DEFER** |

**Auto-resolve:** port the 5 configs + mana-default → covers **8/10 classes including BOTH STR classes (Barbarian-rage, Hoplite-steady)**. The two gaps DEFER — they are 2/10 of the roster, neither is STR, and neither blocks the STR-lever read (Phase 6 driver). Revisit in a follow-on if cohesion-judge/playtest surfaces pressure.
**Escalate to gandalf+Matt ONLY IF:** (a) gamora's math-note finds the 5-config port is materially more than "wire + branch" (scope surprise), OR (b) gamora finds the kernel ALREADY implements damage-taken-converts / HP-as-resource (then port them too — cheap; confirm scope).

**GATE G2 (AFTER measure) — resource-shift magnitude. PRE-REGISTERED:** wiring the gate THROTTLES free-spammers; expected direction is KPM **flat-or-DOWN** vs the un-gated baseline, with build-spend kits showing a burst→lull rhythm.
**Auto-resolve** if the shift is in that direction.
**Escalate ONLY IF:** KPM *rises* (gate not binding → wiring failed), OR any kit flatlines to ~0 KPM (cost-vs-pool mis-scale starving a kit silent — the old structural-mana-bug shape recurring in spatial).

### Phase 2 — Rotation selector (falls out of Phase 1's branch)

**Work (gamora):** the selector branches on `energy_type`; port the `ai_strategies.py:435-438`/`:493-496` build-vs-spend logic as the template. Each economy expresses its intended shape:
- **rage** (Barbarian) → build on the swarm, spend on the anchor — *this is STR's focus-fire LEVER, native to the economy.* (Diablo 3 parallel: Rend is a Fury-spender bleed DoT — almost exactly STR's substrate-assigned bleed-as-single-target tool.)
- **steady/overflow** → greedy-capstone / spam-highest-ready. **(Honest correction, Discipline #12:** my earlier greedy-capstone ruling was *universal*; it is correct ONLY for the steady/overflow economies, and WRONG for build-spend. Now correctly scoped.)
- **combo/charges** → accumulate-then-dump. **charge-stack** → build-and-hold-then-release.

**GATE G3 (AFTER measure) — rotation-shape faithfulness. PRE-REGISTERED falsifier:** distinct economies MUST produce distinguishable tier-firing distributions.
**Auto-resolve** if rage/steady/combo/charge-stack/mana fire visibly differently.
**Escalate ONLY IF:** two distinct economies produce *identical* firing patterns (branch broken), OR the **rage economy fails to produce build-on-swarm/spend-on-anchor** (the lever does not materialize — a real design finding that directly shapes the Phase-6 STR read; escalate immediately).

### Phase 3 — DoT activation + physical-DoT scaling (re-pointed DoT brief)

**Work (gamora):** Findings 1 & 2 of the 2026-06-20 DoT brief — activate DoT ticking in the spatial engine (regime-wide: burn/bleed/drain together); route physical-DoT tick-scaling through the originating skill's attribute (martial→str/dex, caster→int/wis, mirroring direct-damage `damage_resolver.py:312`). Recompose-first: keep the existing `0.003` coefficient, **NO magnitude re-tune** this pass. Correct Finding 3 (the math-note §1.1 "DoT folds into the per-hit float" doc error, now misleading once DoT is non-zero). Now correctly positioned: with Phase 2 firing tiers above T1, the fired skills carry non-zero ticks, so the measurement is no longer confounded.

**GATE G4 (AFTER measure) — DoT contribution now non-zero. PRE-REGISTERED:** with tiers > T1 firing AND ticks active, physical bleed should contribute > 0 to STR single-target output, comparable (each on its own attribute) to caster burn.
**Auto-resolve** if STR bleed contributes and physical≈caster symmetry holds.
**Escalate ONLY IF:** STR bleed still ~0 (spender isn't firing the bleed skill, or scaling fix mis-routed), OR caster burn massively over-contributes (band-fit artifact — note for Phase-5 refit, not real over-performance).

### Phase 4 — Armor/resist symmetry (mitigation-side; ‖ with 1–3)

**Work (gamora):** correct the armor/resist asymmetry so casters mitigate the resist they currently bypass. Selector-independent — KR may run this in parallel with Phases 1–3. Math-note-first; semantic-shift declared.

**GATE G5 (AFTER measure) — mitigation symmetry. PRE-REGISTERED:** caster clear-room KPM should DROP (they now eat resist); caster boss survive+kill should fall from the inflated ~0.99 toward the martial range.
**Auto-resolve** if caster numbers come down toward martial.
**Escalate ONLY IF:** martial numbers move (they already ate resist — they shouldn't shift), OR symmetry over-corrects (casters now BELOW martial → over-mitigation).

### Phase 5 — ONE composed re-baseline (the only refit)

**Work (gamora sim + jack-ryan Gate-2):** all four fixes live. Re-fit the bands against the composed instrument. This is where the reopened Stage-2c band-refit (memo SESSION-DELTA D2) actually resolves — against the composed instrument, not piecemeal.

**GATE G6 — jack-ryan structural Gate-2 + Matt band approval.** This is jack-ryan's gate with BLOCK authority, NOT a gandalf pre-reg: mechanism correctness, V-gates, semantic-shift continuity across all four boundaries, seed hygiene, no accidental production-gate regression. New bands → decisions-log → **Matt approves** (the bands are what everything downstream is judged against; this is a Matt decision).

### Phase 6 — STR-lever / (A)-vs-(B) measurement

**Work (gamora run; gandalf rules):** STR now fires its actual economy (Barbarian rage build-spend) including the bleed-spender lever, against honest bands.

**GATE G7 — gandalf disposition. PRE-REGISTERED (re-pointed from the DoT brief O-table):**

| Outcome | Read |
|---|---|
| **O1** STR elite_pack rises into band + boss survive+kill rises from 0.000 via the rage-spender lever | the tool existed; STR ships-via-floor with a *working* lever (A-leaning); anchor-gap is now a *choice*, not a wall |
| **O2** STR rises but only partway (still below floor on elite_pack) | the lever helps but is insufficient → magnitude tuning OR more single-target tooling (B-leaning); name which |
| **O3** STR unchanged despite working economy + lever | the bleed lever is not STR's anchor answer → escalate to the (A)-vs-(B) skill investigation proper (B) |
| **O4** STR over-shoots (above ceiling on anchored packs) | lever over-funded → magnitude is the dial, not the mechanism |

This is the first **honest** probe of Matt's (A)-vs-(B) question — the kit firing its kit, through its economy, against an uncontaminated instrument.

---

## 4. Escalation protocol (how KR drives without framing design questions)

- **Default = auto-resolve.** Each gate's pre-registered "auto-resolve" branch is KR's to execute without re-ask. KR is checking outputs against the disposition tables above — NOT framing design questions.
- **Escalate = the named fork conditions only.** When a gate's "escalate ONLY IF" condition fires, KR pauses that phase and raises a **short gandalf+Matt touchpoint** (gandalf rules the design call; Matt holds the decision). KR does not auto-decide a fork.
- **jack-ryan BLOCK is structural** (Phase 5 / any phase's Gate-2), routes to Matt per normal — independent of this brief.
- **Decisions stay with Matt; sequencing stays with KR; the critique-pair stays independent of the driver.** That separation is the reason this is KR-led and not a gandalf-autonomous run (measurement-validity work: the drift-watcher cannot also be the driver).

---

## 5. Cautions (load-bearing)

- **measure-ISOLATED per phase; ONE re-baseline at Phase 5.** Do NOT touch `ENCOUNTER_COHORT_KPM_BAND` or the production gate in Phases 1–4. Bands stay as-is so each shift is visible against the current bands. The refit is Phase 5 only.
- **Semantic-shift at EVERY phase boundary (Discipline #12).** Resource-gating, rotation, DoT, and mitigation each change the meaning of every KPM/DPS field. Declare each boundary as the DPS field was declared.
- **Recompose-first: PORT, do not BUILD.** The kernel holds the working economy; `ai_strategies` holds the build-vs-spend selector. These are port targets, not design problems. No new mechanic is invented in this workstream.
- **Two economies DEFER** (Skirmisher damage-taken-converts, Crusader HP-economy). This is intentional scope-holding, not an oversight — neither blocks the 8/10 covered roster nor the STR read.
- **The DoT brief is re-pointed, not discarded.** Its Findings 1 & 2 are Phase 3; do not fire it standalone.
- **Seed hygiene (Discipline #3):** fresh disjoint seed base per phase; fix the intra-run seed-stride overflow (DoT brief §11.1) before any harness re-use.
- **The (A)-vs-(B) question is NOT answerable until Phase 6.** Resist any read of STR sufficiency before the kit fires its kit through its economy against honest bands. Today it fires one tool, ungated, forever — that measures nothing about the real kit.

---

## 6. Seam routing

- **gamora:** math-note (Discipline #1) → implement (port, recompose-first) → measure-isolated harness → results + math-note, per phase 1–5; run Phase 6. Engine simulation seam (`spatial_engine.py`, `damage_resolver.py`, `spatial_resolver_adapter.py`; port sources `combatant.py`, `ai_strategies.py`).
- **jack-ryan:** Gate-2 per phase — mechanism correctness, V-gates, semantic-shift declaration, no production-gate regression, seed hygiene; structural BLOCK at Phase 5 re-baseline.
- **gandalf:** G1 mapping ratification; pre-registered gate dispositions (G2–G5, G7); rule the Phase-6 STR-lever disposition; honest-framing record (greedy-capstone scope correction).
- **knight-rider:** sequence the spine (§2); auto-resolve gates per pre-registration; escalate ONLY named forks to gandalf+Matt; run the dispatches to the seam owners; carry the decisions-log draft for Phase-5 bands.
- **Matt:** the gate forks (when escalated); Phase-5 band approval; the Phase-6 (A)-vs-(B) read.

## 7. Hand-back chain

Phase 1 (resource wired + delta) → Phase 2 (rotation faithful + delta) → Phase 3 (DoT live + delta) ‖ Phase 4 (mitigation symmetric + delta) → Phase 5 (composed re-baseline → honest bands → Matt approves) → Phase 6 (STR fires its economy + lever against honest bands → gandalf rules O1–O4 → feeds the (A)-vs-(B) skill investigation).

---

**Signed:** gandalf, 2026-06-20. Four instrument defects on one damage equation. Fix each, measure each in isolation against the standing bands, re-fit the bands once against the composed instrument — then, for the first time, ask the real question with a real instrument: does STR's kit, fired through its own economy, turn the anchor-gap from a wall into a choice?
