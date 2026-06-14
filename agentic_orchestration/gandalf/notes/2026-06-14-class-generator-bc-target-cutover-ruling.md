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
- **The program (KR sequences the coupling) — THREE stages (§7.6):** Stage 1 — **rocket** (generation V-1..V-9; compose-from-BC-target + provisional-label bridge; gandalf §7 + jack-ryan Gate-2). Stage 2 — **gamora** (simulation V-S1..V-S4 + V-D7; AI keys on BC bins; label demoted). Stage 3 — **irreversibility deletion (THE GOAL — §7.9)**: delete the start-of-pipe legacy `archetype_tag` ENTIRELY (`ARCHETYPE_TEMPLATES`/`ARCHETYPE_ROLE_PRIORITY`/`_PLAYER_CONTROLLER_ARCHETYPES`/the shim/V-D1..V-D6 + correct SD-1..SD-3 + the drax presentation-coupling check §7.9). The player-facing class name is the SEPARATE end-of-pipe LLM label (`PlayerClass.name`, already built at `llm/naming.py:276` + Phase-5 cell-filtered registry); the legacy label is never player-facing. Generation-first, simulation-second, **deletion-last** — gated prove-then-delete (Stage 3 fires only after a full season runs end-to-end through the coordinate with zero label-input firing; the W-E→W-F discipline). Matt-authorized as a program 2026-06-14; deletion-as-goal confirmed 2026-06-14.
- **water_mage 1/29 is ABSORBED into Stage 1** — fallback path removed by the cutover, not patched.
- **gandalf BC-coordinate-identity design call — MADE (§7, Matt-authorized 2026-06-14).** The shared 8-tuple identity that generation *composes from* AND the simulator *keys on*; substrate binds provisionally at the **adapter** (not the composer — #13a preserved); the label demotes to derived display. Grounded at source (`ai_strategies.py:45/270-347`, the W0.2 substrate section `:405-409/:485`, `damage_resolver.py:328/842`, `skill_schema.py:6-178`) — not blind. Unblocks rocket's Stage-1 adapter+source+substrate math note AND gamora's Stage-2 AI-migration spec.
- **Still-separate queued gandalf items (NOT in this ruling):** fire_controller status-resist cross-element asymmetry; the Q4 code-flip routing.
- **Push gate (standing, Matt-gated):** collab (6c99c55, c7b6012, e60f021, + this ruling f5e95f9 & amendments incl. §7) + engine (9a46731, 42e40e4, f48dde8, 525a014) + rocket probe note (bd36d2d) remain push-ready pending Matt authorization.

---

## 7. The complete-cut design call — unified BC-coordinate identity (Matt-authorized 2026-06-14)

Matt: *"yes, trace it and make the design call. We've located the root system, let's design the complete cut and removal."* Ruled after tracing at source (`ai_strategies.py:45/160/270-347`; the W0.2 substrate section `:405-409/:485`; `damage_resolver.py:328/842`; `skill_schema.py:6-178`) — not blind.

### 7.0 The organizing principle — substitute the shared currency

The disease has ONE shape in both seams: **the archetype label is the shared currency.** Generation locks the kit by the label (`ARCHETYPE_TEMPLATES.get(label)`); the simulator pilots the kit by the label (`ARCHETYPE_ROLE_PRIORITY[label]`). The label is the hub both seams pass through — exactly the structural work the lock forbids it.

The complete cut is a single substitution: **make the `bc_target` 8-tuple the shared currency; demote the label to a derived, display-only nameplate.** Generation composes the kit FROM the coordinate (`compose_kit`); the simulator pilots the kit FROM the coordinate (bin-keyed AI). The label rides along, computed last, read as a key by nothing live. Every component below is the mechanical consequence of that one substitution.

This is what a "build" IS in the genre. A Frozen-Orb Sorc and a Blizzard Sorc share the label "Sorceress" and are different builds; what distinguishes them is their mechanical POSITION — geometry, range, tempo — not their nameplate. Making `bc_target` the load-bearing identity makes the engine's data model agree with what a build actually is. Label-as-hub is the D3-set-dungeon (class = fixed template); `bc_target`-as-hub is build-space-region identity (§3).

### 7.1 Component 1 — `bc_target` is first-class identity on BOTH seams

Promote `BcTarget` (the type `compose_kit` already consumes; `mechanic_alteration.py:224` already exposes a `BcTargetView`) to a **load-bearing field on `PlayerClass` (generation output) AND `CombatantState` (simulation input).** The substitution made concrete: the 8-tuple is what generation emits and what the simulator reads; the label is a derived string beside it.

Player consequence: two kits that occupy different cells but today collapse to the same label become — for the first time — distinguishable by the engine end-to-end. The identity the player feels (this one kites, that one face-tanks) is the identity the engine carries.

### 7.2 Component 2 — the Stage-1 zero-label source (behavior-preserving; the smuggling trap; diversification deferred)

The orchestrator emits `(element, energy, role)` (`season_orchestrator.py:1539-44`) + range (`_pick_range_profile`); today these reach a kit only THROUGH `classify_archetype → label → bc_target_for_archetype` (the amendment's blocker #2). The cut needs a **direct `(role, range, energy, element) → bc_target` map** that never materializes a label as a runtime key.

**The smuggling trap (gandalf owns catching this):** the map must NOT be "compute the label, then look up the label's coordinate" — that keeps the label as the structural hub and re-quantizes the space to the ~29 legacy points. The map goes inputs → BINS directly: role drives control-density + defensive-profile; range drives engagement-profile + damage-geometry; energy drives resource-economy + damage-tempo. The cut is the COMPOSITION MECHANISM changing from `ARCHETYPE_TEMPLATES.get(label)` (template-lookup) to `compose_kit(bc_target)` (axis-alignment). Even when a Stage-1 coordinate coincides with a legacy point, the kit is now COMPOSED from the coordinate, not looked up from the label — the coincidence is behavior-preservation, not the disease returning.

**Behavior-preserving, NOT diversifying (the one-variable discipline).** Stage 1 reproduces current behavior through a coordinate-shaped pipe. It does NOT sample off-legacy coordinates. Diversification — feeding the now-agnostic pipe coordinates the legacy labels never reached — is a SEPARATE later effort, gated on the cert-wave spatial substrate proving diversified kits actually discriminate (recognition→validate→commit). Bundling diversification into the cut would conflate the architectural change with a behavioral one — the exact cert-wave error (a regression can't be attributed). Stage 1 changes the PIPE; diversification later changes the CONTENT.

**The element subtlety (named, resolved transitionally).** Today element shapes the kit mechanically — `fire_mage` is a no-heal glass cannon, `water_mage` heals — which is element doing mechanical work the substrate-agnostic principle (#13a) forbids. Locked end state: element is SKIN (Phase-5 cohesion-judge), the coordinate is pure mechanics, a "fire" kit COULD be a sustain build. But removing element-from-mechanics is a BEHAVIORAL change, so it does NOT belong in Stage 1. Stage 1's source keeps element transitionally nudging the bins (fire→burst-tempo/no-sustain, water→sustain) so behavior holds; the nudge is marked TRANSITIONAL, removal trigger = Phase-5 cohesion-judge operational (same trigger as the shim, `w0-2 :639`). True agnosticism (element out of the coordinate) commits when Phase-5 can re-skin. This is NOT the label disease — element nudges the coordinate directly, no label-template-lookup; it is a lesser, clearly-marked, trigger-gated transitional coupling.

### 7.3 Component 3 — provisional substrate binds in the ADAPTER, not the composer (#13a preserved)

`compose_kit` FORBIDS substrate input (`w0-2 :405-409`, the #13a-partition: *"No other inputs are permitted — no substrate identity"*). But `damage_resolver.py:328/842` consumes per-skill `canonical_element` NOW, and `Skill.canonical_element` is a required field (`skill_schema.py:40`). The gap: the composer won't stamp element; the simulator needs it.

**Resolution: substrate binds in the `ComposedKit → PlayerClass` adapter, AFTER `compose_kit` returns the substrate-blind kit, from the season's `dominant_element`.** This keeps the composer pure (substrate-blind, #13a honored), and the adapter is the correct seam: it is exactly where the substrate-agnostic coordinate becomes the substrate-bound playable kit. The binding is PROVISIONAL — marked so, Phase-5 cohesion-judge the re-cohere trigger (it may re-skin to a DIFFERENT element for cohesion). The provisional element is a **Phase-5 stand-in in BOTH roles** — the coordinate-nudge (§7.2) and the skin (here) — and both retire together when Phase-5 lands. Do NOT block the cut on the unbuilt Phase-5; provisional binding feeds the simulator today.

### 7.4 Component 4 — the `PoolMechanic → Skill` adapter is a RESOLUTION layer, not glue (the contract)

Rocket's Act-1 was right that this is the load-bearing blocker, and the schema confirms WHY: `PoolMechanic` carries the MECHANICAL SHAPE (id, geometry, range, cost, cd, cc_tags) — the coordinate-space descriptor; `Skill` (`skill_schema.py:6-178`) is the fully-resolved game object needing `abilities`, `effects`, `timing`, `triggers`, `effect_category`, `power_tier`, `role`, `canonical_element`, presentation stubs. The adapter is not glue — it is the **resolution layer where a coordinate-space descriptor becomes a playable kit**, and architecturally it IS the #13a boundary (substrate-blind in → substrate-bound out).

The adapter CONTRACT I rule (rocket implements field-by-field):
1. **One `PoolMechanic` → exactly one `Skill`. No label is consulted, ever.**
2. **Mechanical shape preserved 1:1** — `geometry`, `range_m`, `energy_cost`, `cooldown_seconds`, `cc_effect`/`cc_duration_s`/`cc_slow_magnitude` come straight from the `PoolMechanic`. These ARE the coordinate; they must not be re-derived.
3. **Substrate binds here** (§7.3): `canonical_element` ← provisional `dominant_element`.
4. **Gap-field enrichment** (`abilities`, `effects`, `timing`, `triggers`, `effect_category`, `power_tier`, `color_value`, `scaling_attribute`) is keyed on the mechanic's own properties + the coordinate + the provisional substrate — **NEVER on the label.** If rocket reuses the b6 ability-construction machinery, it MUST be re-keyed off the mechanic, not the archetype, or the disease re-enters through the back door.
5. **`role`** (the per-skill identity field) comes from the mechanic's role + the coordinate's role bin, not a label.

### 7.5 Component 5 — Stage-2 sim-AI keys on BC bins (the discrimination law at the instrument)

The simulator MEASURES a kit by PLAYING it; if it plays by the label, even a perfectly axis-composed kit is measured through the label's ASSUMED behavior (V-S2 — the discrimination-law-at-the-instrument problem, **third instance** after M1.3.5 and the W-E search layer). The cut is incomplete until the instrument reads the coordinate.

The lever already exists and is already non-label: `get_priority_roles(..., preferred_behavior=...)` (`ai_strategies.py:160/331`) — the monster path (`_scripted`, `:331`) already passes a `preferred_behavior` override that bypasses the label. **Stage 2 promotes `preferred_behavior` from a monster-scripting override to the PRIMARY keying mechanism, derived from the `bc_target` bins:**
- **control-density bin → control-first ordering** — replaces the `_PLAYER_CONTROLLER_ARCHETYPES` membership test (`_common`, `:292/:45`). A kit pilots control-first because it IS control-dense, not because it's labeled controller.
- **engagement-profile bin → range/positioning** — kite vs face-tank from the actual engagement axis.
- **damage-tempo bin → rotation cadence** — burst-spike vs sustained from the actual tempo axis.

`ARCHETYPE_ROLE_PRIORITY[label]` (`:331`) and `_PLAYER_CONTROLLER_ARCHETYPES` (`:45`) retire (or demote to a fallback for any not-yet-migrated path). Player consequence: the AI pilots the kit by its mechanical shape, so when diversification later feeds off-legacy coordinates, the AI pilots them correctly — a label-keyed AI would mis-pilot every off-label kit and poison the balance loop.

### 7.6 The staging + the decoupling buffer

The two seams cannot go label-agnostic simultaneously (the label is the shared currency; the moment generation stops emitting a sim-recognizable label, the label-keyed sim breaks). The buffer that decouples them:

- **Stage 1 (rocket, generation):** add `bc_target` to `PlayerClass`; source it via the direct map (§7.2); compose via `compose_kit`; bind provisional substrate + adapt to `Skill`s (§7.3/§7.4). The label becomes OUTPUT (computed from `bc_target`) but KEEPS ITS LEGACY STRING FORMAT as a sim bridge — so the still-label-keyed simulator runs unchanged. The cut (label is OUTPUT, not INPUT) is achieved in Stage 1; the label's string FORMAT is a separate, later, cosmetic flip. water_mage 1/29 + the `KitConstraintError → 5-skill fallback` dissolve here (absorbed, not patched).
- **Stage 2 (gamora, simulation):** add `bc_target` to `CombatantState`; migrate the AI to bin-keying (§7.5). Once the AI reads the coordinate, the INTERNAL legacy-format bridge is freed (the player-facing name was always `PlayerClass.name`, the LLM end-of-pipe label — §7.9; the bridge was internal-only, never player-facing). THIS stage earns the true *"zero label-as-input in the live path"* (the live path includes the simulator).
- **Stage 3 (irreversibility — THE GOAL; deletion):** physically delete the start-of-pipe legacy `archetype_tag` and its INPUT machinery ENTIRELY — `ARCHETYPE_TEMPLATES`, `ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, the `legacy_archetype_shim` (V-D5, dies last), the deprecated-resident V-D1..V-D6 — correct the stale docs SD-1..SD-3, and sweep the drax presentation-coupling (§7.9). **The legacy `archetype_tag` is deleted root-and-branch, never player-facing. The player-facing class name is the SEPARATE end-of-pipe LLM label `PlayerClass.name`, which already exists (`llm/naming.py:276` + Phase-5 cell-filtered registry) and is unaffected by the deletion.** This is the **W-F 1D-delete pattern**: while the old machinery resides in the tree the lock is enforced by discipline alone (a regression/merge/quick-fix can re-wire to it); deletion makes the lock structural — there is nothing to revert TO. **Gate (prove-then-delete, the W-E→W-F discipline):** Stage 3 fires only after Stage 2, gated on empirical proof that a full season generates + simulates end-to-end through the coordinate with **zero label-input path firing**. Do not delete blind; delete after the coordinate path is proven load-bearing-complete.

Generation-first, simulation-second, deletion-last — three stages, sequenced via the legacy-format-output bridge, not simultaneous. The shim is load-bearing through Stages 1–2 and dies in Stage 3.

### 7.7 Routing (recommend-don't-rescope)

- **gandalf RULES** this design (§7.0–§7.6) — the substitution, five components, staging, discipline guards. MADE here.
- **KR SEQUENCES** — Stage 1 (rocket) before Stage 2 (gamora); A4 (v2.15 `ALTER TABLE` adding `archetype_label` + `recompose_energy_calibration_applied`) cross-seam to star-lord+gamora; A3 (shim ≤20%/1-bin calibration) folded into Stage 1's gate.
- **Matt AUTHORIZES** the program scope.
- **rocket** owns: the direct-map source, the adapter+substrate-binding math note (Disc #1, against §7.2/§7.3/§7.4), the field-by-field `PoolMechanic → Skill` implementation. **gamora** owns: the `CombatantState.bc_target` field + the AI bin-keying spec (against §7.5). **Gate:** jack-ryan Gate-2 + gandalf §7 review per stage.

### 7.8 The discipline guards (why this cut is bounded + safe)

- **One-variable (cert-wave):** Stage 1 changes only the pipe (label-lookup → coordinate-composition), behavior-preserving. Diversification + element-agnosticism are SEPARATE gated changes.
- **recognition→validate→commit:** the cut commits now (the lock is violated, the cure is built); diversification commits when the spatial substrate validates discrimination; element-agnosticism commits when Phase-5 can re-skin. Each expansion gated on its own empirical criterion, not bundled.
- **#13a-partition preserved:** `compose_kit` stays substrate-blind; substrate binds provisionally at the adapter; the residual element-nudge in the source is transitional + Phase-5-trigger-gated.
- **do-not-rule-blind discharged:** ruled after tracing `ai_strategies.py`, the W0.2 substrate section, `damage_resolver`'s `canonical_element` need, and the `Skill` schema — not before.

### 7.9 The two labels — delete the start-of-pipe disease; the player sees the end-of-pipe LLM label (Matt correction 2026-06-14)

A correction I owe: §7.6 first said *"the label STRING survives as display."* That conflated two DIFFERENT artifacts. There are two labels; only one is the disease, and the GOAL is to delete it.

- **Start-of-pipe legacy label** — `archetype_tag` = `{element}_{role}` (`water_mage`, `earth_controller`), produced by `classify_archetype()` at the HEAD of the pipe and consumed as the generation + simulation INPUT. **This is the vestigial disease. The GOAL is to delete it ENTIRELY — input AND every residual use; the player must NEVER see it.** (Already true at the demo subtitle — drax removed the `archetype_tag · energy_type` subtitle from normal display in v0.26, `reincarnated-demo/src/main.ts:2098`. Stage 3 completes that trajectory at the root.)
- **End-of-pipe LLM + algorithmic label** — `PlayerClass.name`, produced at the TAIL by the LLM (`llm/naming.py:276` — *"Attach LLM-generated name, flavor, and title completion to a PlayerClass"*) composing from an ALGORITHMICALLY coordinate-derived cell-filtered thematic registry (`llm/phase5_orchestrator.py:1638-1792` — the coordinate filters the registry → archetype-name candidates → the LLM composes the evocative name). **This is what the player sees; it ALREADY EXISTS and is ALREADY WIRED** (the demo displays `caster.name`, `main.ts:368/481`). This IS "the LLM and algorithmic output label at the end of the pipe" — keep it; it is the goal-state display.

**The vindication is the whole ruling's shape again: the end-of-pipe player-facing label is built; the start-of-pipe disease persists at the root.** The cut deletes the head; the LLM tail is already what remains.

**Reframe consequence — deletion is the GOAL, not a conditional tail.** The program's purpose IS the removal of the start-of-pipe `archetype_tag`-as-identity. Stage 3 is the goal realized, not optional cleanup. The internal legacy-format bridge (Stage 1–2, §7.6) is INTERNAL-ONLY — the player sees `PlayerClass.name` at every stage; the bridge merely keeps the still-label-keyed simulator running until Stage 2 migrates it, and it dies in Stage 3.

**The transitional coordinate-string `archetype_label`** (`synthesize_archetype_label` output, e.g. `"ranged-slow/large-AOE/damage-pure/glass/overflow_damage_mana"`) is NEITHER label — it is an INTERNAL structural identifier (telemetry/gamora keying during transition), self-described as *"clearly NOT a substrate-tagged archetype name"* and *"Superseded at Phase 5 by cohesion-judge thematic label"* (`bc_target_composer.py:634-635`). Scaffolding, not player-facing.

**Deletion-surface extension (do-not-rule-blind — FLAG for the sweep, not asserted):** the legacy `archetype_tag` may also be the shared currency with the PRESENTATION layer — the demo references it for class-archetype VFX-overlay matching (`reincarnated-demo/src/main.ts:1509/2108/2243`, the Starcaller/Necromancer/Frostwindz Layer-2 overlays). If those overlays key on the legacy label rather than on `PlayerClass.name`/`classElement`/the coordinate, that is a generation↔presentation coupling (parallel to the generation↔simulation coupling §5.2-5.3) and a drax-seam item in the deletion surface. **Verify with drax before Stage 3** — the Legolas sweep covered the engine, not the demo repo.

---

**Signed:** gandalf, 2026-06-14
**For:** the class-generator BC-target cutover ruling — the lock-compliant `compose_kit` + `synthesize_archetype_label` composer was built under W0.2 (2026-05-21) and shelved while every season shipped through the legacy label-locked path; the root cut is a CUTOVER to that existing composer (re-point the live path, demote the label to derived-last output), and the architectural acceptance proof is the structural removal of the KitConstraintError→5-skill fallback that the water_mage 1/29 falls into — the form-bias root retired at the generation head, the same flat-label habit the cert wave exists to kill.
