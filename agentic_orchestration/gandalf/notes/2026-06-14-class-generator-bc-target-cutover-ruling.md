# Class-generator BC-target cutover ruling — complete the shelved W0.2 composer; the label is OUTPUT, never INPUT

**Type:** design-contract ruling (gandalf seam) — resolves the fourth landmine (water_mage 1/29) at its root by completing the qd-engine-bc-axes-lock migration that was built and shelved.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 — confirmed the cutover framing, sent the cutover dispatch to rocket, agreed the legolas Mode A vestigial sweep.
**Empirical grounding:** gandalf root-trace at source, 2026-06-14 (cited inline — `compose_kit`/`synthesize_archetype_label` + the live-path `season_orchestrator → class_generator.generate` trace + the `compose_kit` caller census).
**Companion docs:**
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the lock this completes (class = 8-axis cell-address; label name-on-top, never an input).
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md` — the migration that BUILT `compose_kit` (rocket, 2026-05-21; Matt "1=yes/2=yes/3=yes") and then was not wired in.
- `agentic_orchestration/gandalf/notes/2026-06-14-controller-vs-caster-primary-stat-ruling.md` — sibling landmine (same flat-label-carries-identity root).
- `agentic_orchestration/qa/findings/2026-06-14-fire-mage-b6-no-heal-pool-contradiction.md` — sibling landmine (B6 fallback; same root surfacing).
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the form-bias discipline this is the generation-head instance of.

---

## 0. TL;DR — RULING: cut at the root via CUTOVER, not rebuild

The lock-compliant substrate-agnostic composer **already exists, is structurally correct, and is bypassed in production.** `bc_target_composer.compose_kit()` composes a kit from a free 8-tuple BC-target; `synthesize_archetype_label()` derives the label LAST from the coordinate — the lock implemented exactly. It was built under **W0.2 (2026-05-21, rocket, Matt-ratified)** and then the final step — wiring it into the live path — was never taken. **Every season since 2026-05-21 generated every class through the legacy label-locked path the lock forbids.**

The root cut is therefore a **cutover to an already-built composer, not a from-scratch severance:** re-point `season_orchestrator → class_generator.generate()` at `compose_kit(bc_target)`, retire the `classify_archetype → ARCHETYPE_TEMPLATES.get → b6_builder.build(label)` round-trip, and let the label be `synthesize_archetype_label()` output. **Acceptance proof is architectural, not cosmetic:** the `KitConstraintError → pre-B6 5-skill fallback` path is *structurally removed* (it cannot fire), the water_mage coordinate composes a full kit, and no archetype label is a generation INPUT anywhere in the live path.

---

> **AMENDMENT 2026-06-14 — Act-1 probe NO-GO (rocket; ENDORSED).** Rocket's cutover-readiness probe (`agentic_orchestration/rocket/notes/2026-06-14-compose-kit-cutover-readiness-probe.md`, committed `bd36d2d`) confirms the root-cut DIRECTION is right but the **"cutover, not rebuild" framing understated the integration surface** — Act 2 is a multi-unit workstream, not a same-session re-point. The two §2 seams I called "bounded glue" are the load-bearing blockers:
> 1. **No `PoolMechanic → Skill` converter exists.** `compose_kit` returns flat `PoolMechanic` descriptors (id, geometry, range, cost, cd, cc_tags); `PlayerClass.skills` needs rich `Skill` objects (abilities for the simulator, effects, canonical_element, tier/chain, scaling, pair_ref). The W0.2 math note never specified the converter.
> 2. **The orchestrator cannot emit a free BC-target.** It emits `(element, energy, role)` (`season_orchestrator.py:1539-44`); the only current route to a `BcTarget` is `classify_archetype → archetype_tag → bc_target_for_archetype` — i.e. THROUGH the label. So "zero label-as-input in the live path" is unreachable without a net-new `(element,energy,role)→BcTarget` source (or the orchestrator emitting BC-targets directly — a separate unfinished pipeline).
> 3. **Substrate hole.** `compose_kit` is element-agnostic by design (substrate = the unbuilt Phase-5 cohesion-judge's job per W0.2), but `PlayerClass` + the simulator need per-skill `canonical_element` at generation time. (Bright spot: `mechanic_alteration.py:224` already exposes a `BcTargetView` — consumption-site #5 is partially ready.)
>
> Plus A3 (shim calibration ≤20%/1-bin gate — unrun) and A4 (v2.15 `ALTER TABLE` adding `archetype_label` + `recompose_energy_calibration_applied` — star-lord/gamora cross-seam) are open. **Rocket correctly held at the seam line** — Act 2 needs (a) a math note for the adapter + substrate-binding (Disc #1), (b) a gandalf design call (substrate-binding-at-generation vs Phase-5 + the zero-label BC-target source), (c) KR to route A4 cross-seam. **The root-cut design content of this ruling STANDS unchanged; only the readiness/sequencing framing updates.** Staged path supersedes §4's "in flight": legolas inventory → **gandalf design call (substrate-binding + zero-label source)** → rocket adapter+substrate-binding math note → gandalf review → KR routes A4 to star-lord+gamora → A3 calibration → cutover under Gate-2 + gandalf. The **substrate-binding design call is now a named gandalf-owed item** (preview lean — UNCOMMITTED pending the Legolas inventory + a substrate-binding trace: bind a PROVISIONAL per-skill substrate at generation from the season's already-chosen `dominant_element` so the simulator is fed, mark it provisional, let the eventual Phase-5 cohesion-judge re-cohere — i.e. do NOT block the cutover on the unbuilt Phase-5).

---

## 1. The load-bearing facts (empirical, verified at source 2026-06-14)

1. **The lock-compliant composer is built and correct.** `bc_target_composer.py`: `compose_kit(bc_target, …) -> ComposedKit | None | DeferredEvaluation` (:676) samples mechanics by `_axis_alignment_score` (:462), not template lookup; `synthesize_archetype_label(…)` (:621) returns the label derived from the 8 bins — name-on-top, computed last. `decompose_bc_target → CompositionObjectives` (:422) turns the tuple into directional objectives. This is the lock as code.

2. **It is shelved.** `compose_kit()` is called by **nothing** in the live path — the only caller is `legacy_archetype_shim.py:174` (a transitional label→tuple bridge). The composer's own comments admit it: `:879` "The legacy path is preserved"; `:886` "uses classify_archetype() internally — it generates kits via the existing B6 builder."

3. **The live path is the legacy label-lock.** `season_orchestrator.py:1541/1607/1625 → class_generator.generate()` → `classify_archetype()` (:363, label derived early from element+energy+role) → `ARCHETYPE_TEMPLATES.get(label)` (:371, label as lookup key) → `b6_builder.build(label)` (:535). The label is then consumed at 5+ downstream sites: stats `allocate_stats(archetype)` (:383), alteration `select_mechanic_alteration_from_kit_params(archetype_tag=…)` (:430), embodiment `_ARCHETYPE_ACTION_REGISTER`/`_ROLE_FUNCTION` (:413-414), `cross_chain_rule` (:381). `season_orchestrator.py:145` independently re-derives the label too.

4. **The water_mage 1/29 fallback lives inside this path.** `_generate_skills` (:533) gates the B6 builder on `archetype_tag in ARCHETYPE_TEMPLATES`; on `KitConstraintError` it falls through (:546) to the pre-B6 `_generate_standard_skills` (:552) — a degraded 5-skill kit. This is the symptom; the label-lock is the disease.

## 2. The ruling and why it is a cutover

**Cut at the root: wire the live path to `compose_kit`; demote the label to `synthesize_archetype_label` output.** This is not a rebuild because the replacement is built and ratified; it is a *scoped cutover* with five honest seams the rocket probe (Act 1) must close before the cutover (Act 2):

1. **Upstream BC-target source** — the orchestrator passes `(element, role, range, energy)` and lets class_generator derive a label. The cutover needs a free 8-tuple instead. `legacy_archetype_shim` proves a label→tuple bridge exists as a staging step; the end state emits BC-targets directly.
2. **`ComposedKit → PlayerClass` adapter** — `compose_kit` returns a transitional `ComposedKit` (:648); the orchestrator wants a `PlayerClass`. Bounded glue.
3. **The 5+ label-consumption sites** (§1.3) re-point to the composed output / derived-last label.
4. **Infeasibility handling** — `compose_kit`'s `None`/`DeferredEvaluation` *replaces* the `KitConstraintError → 5-skill fallback`. This is where the water_mage 1/29 dissolves: infeasibility becomes a principled composition-time outcome, not a silent degraded kit.
5. **W0.2's two deferred obligations (jack-ryan A3+A4)** — the probe confirms `compose_kit` production-readiness and whether they gate.

**Acceptance test (architectural):** (a) the `KitConstraintError → pre-B6 5-skill fallback` path is structurally removed (class_generator no longer calls `b6_builder.build(label)`); (b) the water_mage coordinate composes a full kit; (c) zero label-as-input in the live path — the label appears only as `synthesize_archetype_label` output. The 1/29 is not tuned away; its code path ceases to exist.

## 3. The genre + cert-wave rhyme (why this is the form-bias root at the generation head)

The label-keyed template lookup collapses the 68,040-cell BC space into a finite enum of named templates: two kits that should occupy different cells but classify to the same label get the *same* template → identity collapse. That is **the form-bias pathology (doc 37) at the generation head** — the flat-label-carries-identity habit the whole cert wave exists to retire, re-entering at the point of composition. In ARPG terms it is the **D3-set-dungeon rigidity** (a class IS a fixed template) the genre spent fifteen years escaping toward **build-space-region identity** (D2 Sorceress = Blizzard/Orb/Fireball/Hydra space; PoE = tree+gems; D4/PoE2 pull toward freedom). `compose_kit` + `synthesize_archetype_label` IS build-space-region identity in code; the legacy path is the set-dungeon. The four-landmine cluster — controller-vs-caster primary stat, B6 fire_mage fallback, theme-element-vs-flavor-pool, water_mage 1/29 — is **one root surfacing four times.** This ruling cuts the root; the others were its leaves.

## 4. What rocket does (IN FLIGHT — Matt sent the dispatch 2026-06-14)

- **Act 1 — cutover-readiness probe (read-only):** confirm `compose_kit` production-readiness; identify the BC-target upstream source (orchestrator-direct vs shim-staged); map the `ComposedKit → PlayerClass` adapter surface; report W0.2 deferred-obligation status.
- **Act 2 — cutover:** re-point the entry + the 5 label-consumption sites; route infeasibility through `None`/`DeferredEvaluation`.
- **Gate:** jack-ryan Gate-2 + gandalf §2 design review on the cutover + the acceptance proof.

## 5. The vestigial sweep — legolas Mode A inventory RETURNED 2026-06-14

Full inventory at `agentic_orchestration/legolas/research/2026-06-14-archetype-label-as-input-vestigial-sweep.md`. **Counts: 16 VIOLATION (9 live-path, 7 deprecated-resident) · 8 COMPLIANT-OUTPUT · 3 STALE-DOC.** INPUT-vs-OUTPUT discriminator applied as briefed.

**5.1 Generation-layer (rocket cutover scope) — completeness-checked.** V-1..V-9: `class_generator.py:363/371/373/383/413/430/533` (the 7 sites I traced), plus **two I did not enumerate** — `season_orchestrator.py:145` (`_pick_range_profile` pre-derives the label to gate `close` range — a label constraining a generation INPUT before generation begins) and `mechanic_alteration.py:932-1001` (`_bc_view_from_generation_params` reconstructs a synthetic BC-target FROM the label — the lock inverted: should receive a real BC-target from `compose_kit`). Rocket's re-point list is now exhaustive.

**5.2 — THE NEW FINDING: a second disease site in the SIMULATION layer (gamora's seam, NOT in rocket's cutover).** The label-as-input disease is not confined to generation. The fight engine and balance loop key on the label too:
- **V-S1** `ai_strategies.py:292` — `combatant.archetype in _PLAYER_CONTROLLER_ARCHETYPES` gates control-first skill selection.
- **V-S2 (load-bearing)** `ai_strategies.py:331` — `ARCHETYPE_ROLE_PRIORITY[archetype]` drives the **AI rotation order — which skills fire, when.** The simulator plays a kit according to its LABEL, not its composed mechanics.
- **V-S3** `balance_loop.py:1007/1027` — `archetype_tag != "experimental"` string-gates the recompose loops (a boolean would do).
- **V-S4** `balance_loop.py:2636…` — balance gear stats keyed by `_PHYSICAL_ARCHETYPES` label membership.
- **V-D7** `balance_loop.py:1886/1948/2030/2183` — template-by-label gates valid geometry/element modifications during recompose.

**V-S2 is the form-bias/label-bias reaching into the MEASUREMENT INSTRUMENT** — the M1.3.5 "discrimination law at the instrument" problem, **third instance** (after generation form-bias and the W-E search-layer). Two kits at *different* BC coordinates that share a legacy label are played *identically* by the AI; a kit labeled with a coordinate-string (post-`synthesize_archetype_label`) matches **no** `ARCHETYPE_ROLE_PRIORITY` key. So even a perfectly axis-composed kit is *measured* through the label's assumed behavior.

**5.3 The generation↔simulation coupling (the key sequencing finding).** The label is the shared currency between the two seams. The moment generation stops emitting recognizable labels (emits coordinate strings instead), the label-keyed simulator (V-S1..S4) breaks. They cannot both go label-agnostic independently. **Staged decoupling:** Stage 1 — rocket's generation cutover composes from a BC-target but emits a PROVISIONAL legacy-style label as a bridge (the sim keeps working); Stage 2 — gamora migrates the sim AI (V-S1/V-S2 especially) to **BC-bin keying** (control-density → control-first; engagement-profile → range behavior; damage-tempo → rotation); then the label is fully demoted to derived display. **Generation-first, simulation-second — sequenced, not simultaneous.**

**5.4 Refined STAGED acceptance (supersedes §0/§2's single test).** Stage 1 (rocket) = composes-from-BC-target + `KitConstraintError → 5-skill fallback` structurally gone + water_mage 1/29 dissolved. Stage 2 (gamora) = sim AI keys on BC bins + label demoted = the **true** "zero label-as-input in the live path." My original acceptance conflated these; the live path includes the simulator, so "zero label-as-input" provably requires Stage 2.

**5.5 Cleanup tail (post-cutover, KR-sequenced).** Deprecated-resident: V-D1 `archetype_composer.py` (deprecated, still imported), V-D2 `archetype_classifier.py` (proxies through it), V-D3 `b6_archetype_templates.py`, V-D4 `b6_kit_builder.py:82` lookup, V-D5 `legacy_archetype_shim.py` (label→BC table, the bridge to retire last), V-D6 `stat_allocator.py:118`. Stale-docs: SD-1 `bc_target_composer.py:871` severance-audit string, SD-2 `AGENT_STATE.md:2371` "confirmed working" block, SD-3 `MIGRATION.md:2848` "CONFIRMED COMPLIANT" framing — all normalize the live violation as current architecture; correct post-cutover. **8 COMPLIANT-OUTPUT sites correctly left untouched** (export/telemetry/display + `synthesize_archetype_label` = the lock done right).

## 6. Disposition

- **RULING: cut at the root by completing the W0.2 cutover to `compose_kit`** — design content STANDS; this is now a **multi-seam, two-stage PROGRAM**, not a single rocket re-point (per the Act-1 probe + the Legolas simulation finding).
- **The program (KR sequences the coupling):** Stage 1 — **rocket** (generation V-1..V-9; compose-from-BC-target + provisional-label bridge; gandalf §2 + jack-ryan Gate-2). Stage 2 — **gamora** (simulation V-S1..V-S4 + V-D7; AI keys on BC bins; label demoted). Then cleanup tail (deprecated V-D1..V-D6) + doc corrections (SD-1..SD-3). Generation-first, simulation-second — sequenced, not simultaneous (§5.3).
- **water_mage 1/29 is ABSORBED into Stage 1** — fallback path removed by the cutover, not patched.
- **gandalf-owed design call (expanded, now unblocked by the Legolas return):** the substrate-binding call (§Amendment preview lean) **expands** to a **BC-coordinate-identity call covering both seams** — what is the shared 8-tuple identity that generation *composes from* AND the simulator *keys on*, and how substrate binds at generation (provisional) vs Phase-5. This unblocks BOTH rocket's Stage-1 math note AND gamora's Stage-2 AI-migration spec. I ground the sim-AI keying (`ai_strategies.py`) + the W0.2 substrate section before ruling — not blind.
- **Still-separate queued gandalf items (NOT in this ruling):** fire_controller status-resist cross-element asymmetry; the Q4 code-flip routing.
- **Push gate (standing, Matt-gated):** collab (6c99c55, c7b6012, e60f021, + this ruling f5e95f9 & amendments) + engine (9a46731, 42e40e4, f48dde8, 525a014) + rocket probe note (bd36d2d) remain push-ready pending Matt authorization.

---

**Signed:** gandalf, 2026-06-14
**For:** the class-generator BC-target cutover ruling — the lock-compliant `compose_kit` + `synthesize_archetype_label` composer was built under W0.2 (2026-05-21) and shelved while every season shipped through the legacy label-locked path; the root cut is a CUTOVER to that existing composer (re-point the live path, demote the label to derived-last output), and the architectural acceptance proof is the structural removal of the KitConstraintError→5-skill fallback that the water_mage 1/29 falls into — the form-bias root retired at the generation head, the same flat-label habit the cert wave exists to kill.
