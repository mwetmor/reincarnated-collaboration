# Weapon-as-Identity-Surface — Recognition Record

> **STATUS:** CURRENT (load-bearing as RECOGNITION; architectural commitments DEFERRED per § 6) — see `canonical/00-ground-state.md`

**Date:** 2026-06-14
**Author:** gandalf (story-and-design steward; Pattern-B dialogue with Matt)
**Status:** v1 recognition record — recognition LOCKED, validate DONE, commit DEFERRED
**Authority:** Matt 2026-06-14 (Pattern-B) — recognition locked verbatim: *"the weapon is the identity-bearing SURFACE"* … *"the most coherent of all the messages above"*; validate authorized verbatim: *"fire the weapon-flow audit."*
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md` — the BC-coordinate cutover this recognition extends; Stage 3b re-open criterion (physical-pool expansion) is reframed here as the weapon-rooting work.
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the non-humanoid body-plan discipline that bounds weapon-as-identity to the humanoid branch (§ 5).
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — the precedent pattern (LLM composes from the curated weapon substrate; the rich substrate this recognition relocates identity onto).
- `canonical/story/2026-06-14-godot-pivot-modular-asset-strategy-and-dual-machine-workflow-recognition.md` — the Synty `Attachment*` weapon-sockets are the visual-layer home of the identity-bearing weapon (§ 5).
- `canonical/story/2026-06-06-atomic-substrate-registry.md` — the 89,839-row weapon-substrate library + `bc_attribute` (STR/DEX/INT/WIS) the weapon-rooting builds on.
- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` — **the buildable validate step** (rocket hand-off): roots identity on the cycle-14 BALANCED pool (`v1_scope=1`=2,499, with the manually-created caster rows), specifies the § 2 code change + the § 4 gate this record defers on (authored per Matt "author both" 2026-06-14).

---

## 0. TL;DR — Recognition Record (architectural commitments deferred per § 6)

**Recognition (LOCKED, Matt 2026-06-14):** kit identity — physical / caster / summon — is borne by the **selected weapon**, not by an element/archetype coordinate. The weapon is the identity-bearing *surface*.

**Validate (DONE — weapon-flow audit, rocket, 2026-06-14; all 5 crux findings independently re-verified by gandalf against live code, § 2):** generation today is **coordinate-rooted with the weapon as OUTPUT.** The weapon is selected *after* identity, by filtering the weapon catalogue to match the already-composed coordinate. So weapon-as-identity is a genuine **reframe — not yet built.**

**But the audit strongly VALIDATES the diagnosis.** The behavioral coordinate (the bc_target 8-tuple) has **no physical-vs-caster axis and no weapon axis.** Identity has nowhere to live in the coordinate — so the code **smuggles "physical" in as a pseudo-element** and then **falls physical kits back to label-classification + hand-authored templates** (`classify_archetype` → label → `ARCHETYPE_TEMPLATES`): *the exact label-rooting the BC-cutover spent three stages deleting.* The cutover cured the disease for the elemental path; the physical path still carries it — **because physical identity was never an element-coordinate property. It is a weapon property.** Matt's instinct is sharp precisely because the code is straining to push weapon-identity through a coordinate with no room for it.

**The load-bearing engineering insight:** weapon-as-identity is not only thematically coherent — it is **substrate-honest.** It relocates the identity root from the **sparse** physical-cost mechanic pools (rage=4 / focus=4 / combo=2 / stamina=2 — the audit's stated deferral blocker) onto the **rich** weapon substrate (89,839 rows; *"weapons have the details needed"*). It roots identity where the substrate can actually support it.

**Commit (DEFERRED per § 6):** re-rooting physical kit identity on the weapon is the **same work** as the Matt-authorized physical-pool-expansion sub-stage already cited in-code (`class_generator.py:620–655`). It needs a design spec (gandalf) → jack-ryan Gate → rocket. Empirical gate + 3 predictions named in §§ 6–7.

---

## 1. The recognition (Matt 2026-06-14)

Matt declared, of the weapon-as-identity framing: *"this is the most coherent of all the messages above: the weapon is the identity-bearing SURFACE."* Plus three substrate facts that make the reframe buildable, not aspirational:

1. **"Weapons have the details needed."** The weapon substrate is rich enough to carry identity — it is not a thin cosmetic tag.
2. **"The catalogue skews physical, but we built out a manually created caster catalogue."** The martial-vs-arcane signal exists on both sides of the weapon catalogue; the caster side was deliberately authored to balance the physical skew.
3. **"We have a specially selected pool used in cycle 14 that evens out the distribution of physical weapons vs caster weapons."** A balanced weapon pool already exists to root identity against without physical-skew distortion.

The recognition is therefore not "wouldn't it be nice" — it is "the substrate to do this already exists; the generation flow does not yet use it that way."

## 2. The validate — weapon-flow audit (rocket 2026-06-14; gandalf re-verified)

The audit answered one question: **does generation root kit identity on the selected weapon, or on a coordinate region?** Answer: **coordinate-rooted; weapon is output.** Five findings, each re-verified by gandalf against live engine code (do-not-rule-blind):

| Q | Finding | Citation (verified) |
|---|---|---|
| **Q1 — the physical/caster fork** | `is_physical = (dominant_element == "physical" or energy_type in PHYSICAL_COST_TYPES)`. The fork is **element-string + energy-rooted**, not weapon, not the coordinate tuple. | `class_generator.py:616–618`; `PHYSICAL_COST_TYPES = {"rage","combo","focus","stamina-as-resource"}` at `composed_kit_adapter.py:82` ✓ |
| **Q2 — the weapon is OUTPUT** | The weapon is bound **per bc_cell, after composition** — `select_n_substrate_weapons_per_bc_cell(...)`, the weapon filtered to MATCH the coordinate. The function name itself says "weapons **per bc_cell**." | `substrate_weapon_binding.py:457`; called downstream in `season_generation_pipeline.py` ✓ |
| **Q3 — the coordinate has no weapon axis** | The bc_target 8-tuple = `(eng, geo, proxy, ctrl, tempo, var, def, econ)`: Engagement / Damage-geometry / Proxy-density / Control-density / Damage-tempo / Damage-variance / Defensive-profile / Resource-economy. **No martial/weapon axis. No physical-vs-caster axis.** STR/DEX/INT/WIS (`bc_attribute`) lives OUTSIDE the tuple. | `bc_target_composer.py:71–92` ✓ |
| **Q4 — physical = TEMPLATE-rooted (the smuggling-trap survivor)** | When `is_physical` is True, the path runs `classify_archetype(...)` → a label (rogue / hunter / grappler / skirmisher / warrior) → `ARCHETYPE_TEMPLATES.get(archetype)` → the legacy b6 builder. **Label → template: the exact label-rooting the cutover deleted on the elemental path.** | `class_generator.py:636–642` ✓ |
| **Q5 — summon = ENTIRELY DEFERRED** | Proxy density (axis 2A) defers its non-solo bins; the composer hardcodes solo. Summon is an inert coordinate residual, not a live identity. | `_DEFERRED_PROXY_BINS = {"proxy-light","proxy-heavy"}` at `bc_target_composer.py:97`; `proxy_bin = "solo"` at `bc_target_source.py:195` ✓ |

**One-line (rocket):** *"kit identity is coordinate-rooted (with the physical sub-region template-rooted as a deferred exception); the weapon is an accessory selected after identity by filtering the weapon catalogue to match the coordinate — it is never the root."*

## 3. The synthesis — why the instinct is sharp (the diagnosis the audit validates)

The audit says "not built yet" — but its *findings* are the strongest possible evidence the reframe is correct. Three steps:

**3.1 — Identity has no home in the coordinate.** The 8-tuple (§ 2, Q3) is purely behavioral/geometric. There is no axis on which "physical vs caster" can be expressed. So when generation needs that distinction, it has nowhere coordinate-native to put it.

**3.2 — So "physical" is smuggled as a pseudo-element.** `dominant_element == "physical"` (§ 2, Q1) treats *physical* as a 9th element alongside fire / water / wind / earth. That is a category error: **physical is not an element. It is a damage-source the weapon determines.** A sword is physical because it is a sword — not because it carries a "physical element."

**3.3 — And physical can't compose, so it falls back to labels + templates.** Because the physical-cost mechanic pools are sparse (rage=4 / focus=4 / combo=2 / stamina=2), a physical coordinate cannot compose a full kit through the elemental path — it would yield a 2–5-skill degraded kit (*"the water_mage 1/29 sin in a new form,"* per the in-code comment). So physical is routed to `classify_archetype` → label → hand-authored template (§ 2, Q4). **This is the label-as-input smuggling trap the BC-coordinate cutover spent three stages deleting — still alive on the physical path.**

**3.4 — The diagnosis.** The cutover cured the label disease *for the elemental path* and could not cure it for the physical path **because physical identity never belonged in the element-coordinate at all.** It belongs on the weapon. The code is straining — pseudo-element here, template-fallback there — to route weapon-identity through a coordinate built only for behavior. Matt's reframe names the missing surface: **the weapon carries the physical-vs-caster identity; the coordinate carries only the behavior.**

**3.5 — The substrate-honest payoff (the engineering, not just the theme).** The audit's *reason* for deferring physical is pool sparsity. Weapon-as-identity may **dissolve** that blocker: the weapon substrate is rich (89,839 rows; *"weapons have the details needed"*) exactly where the physical-cost mechanic pools are sparse. Root the kit's size + geometry on the **weapon's** properties and the sparse rage/combo/focus/stamina pools stop being the kit_size bottleneck. This is the same move the engine already makes everywhere else: **match the design target to where the substrate is actually rich.** (Precedent: the weapon-substrate-composition policy — LLM composes from the curated weapon substrate, not from thin air.) Registered as Prediction 1 (§ 7).

## 4. The three-layer identity model (gandalf refinement)

Weapon-as-identity does not delete the coordinate — it puts each layer in its correct home. The weapon and the coordinate **co-arise**; they describe the same kit at different layers, and are not competing.

| Layer | Drives | Why here (genre + substrate) |
|---|---|---|
| **1 — Weapon** | **physical vs caster** | The weapon carries the martial-vs-arcane signal natively (a sword is physical; a staff is arcane). Rich substrate (89,839 rows) + the cycle-14 balanced pool. **Clean, weapon-derived.** |
| **2 — Skill composition** | **normal-caster vs proxy-caster (summon)** — a *runtime label* | Genre-true (D2 / D4 / Last Epoch): the weapon does NOT determine summoner-vs-direct; **skill investment does.** A staff that invests in minion skills is a summoner; the same staff investing in direct damage is a normal caster. Summon is a composition outcome, not a pre-assigned coordinate bin. |
| **3 — bc_target coordinate** | **behavioral descriptor** (range / role / AOE / tempo / proxy-density / defense / economy) | The MATH the simulation reads. A *descriptor* of how the kit behaves — including a proxy-**density** descriptor — NOT the identity root. The coordinate stays exactly as it is; it simply stops being asked to carry identity it has no axis for. |

**The summon corollary (resolves § 2, Q5 cleanly).** Forcing summon into a coordinate bin (proxy-light / proxy-heavy, pre-assigned at composition) is the *same* anti-pattern as smuggling physical into a pseudo-element: forcing identity into the coordinate. Matt's runtime-label is the cleaner home. Proxy-**density** survives as a behavioral descriptor (axis 2A — fine); the **driver** of summon-vs-direct moves to skill composition (Layer 2). Registered as Prediction 3 (§ 7).

## 5. The form-bias caveat — this is the HUMANOID-branch identity model (doc 37)

Weapon-as-identity presupposes a **wielder.** It is the **humanoid-branch** identity model — correct and load-bearing for the humanoid roster (which is most of the roster under the Godot Synty-modular strategy + the D5 humanoid-only delivery decision), but **not the universal identity model.** Non-humanoid forms (slime, swarm, cloud-being, serpentine — the doc-37 body-plans) derive identity from **body-plan**, not weapon. A slime has no hands. Its identity-surface is its morphology.

So the recognition is scoped: **the weapon is the identity surface for wielders; body-plan is the identity surface for non-wielders.** The non-humanoid branch needs a body-plan-as-identity-surface analog — flagged here, not resolved.

**The asset-layer bridge (a virtue, not a complication).** The Godot pivot's Synty `Attachment*` weapon-sockets (`AttachmentBack`, `AttachmentHip*`, `AttachmentShoulder*`, mapped via `part_bones` to real bones) are the **literal visual home of the identity-bearing weapon.** Weapon-as-identity is therefore not only an engine-generation reframe — it is the natural meeting point of engine-identity and visual-form: the socket where the engine's identity-weapon becomes the player's seen-weapon. The reframe pays off twice — once in generation coherence, once in asset-pipeline coherence.

## 6. The DEFER — commit gate + empirical criterion

Per recognition → validate → **commit**: the architectural commit is **deferred**, not abandoned. The commit = **re-rooting physical (and the physical/caster fork) on the weapon substrate.** It is the **same work** as the physical-pool-expansion sub-stage already named in-code (`class_generator.py:620–655`, "the Matt-authorized physical-pool-expansion sub-stage") and as the Stage-3b re-open criterion in the BC-cutover scoping ruling. **This recognition reframes what that expansion IS:** not merely "add more rows to the sparse physical-cost mechanic pools," but "**relocate the physical identity root onto the rich weapon substrate**" — which may make the mechanic-pool expansion unnecessary as a kit_size lever (Prediction 1).

**Commit path:** design spec (gandalf) → jack-ryan Gate-1 → rocket implementation → jack-ryan Gate-2.

**Empirical gate (NOT time-passage):** the spec is validated when a weapon-rooted physical kit composes to the legacy physical kit_size band (10–13 skills) **without** depending on the sparse physical-cost mechanic pools as the size source — i.e. the weapon substrate demonstrably supplies geometry + size. If it cannot, the fallback to mechanic-pool expansion remains, and the deferral holds on its original terms. This is checkable the moment the spec's composition path runs against the cycle-14 balanced weapon pool.

**Sequencing note:** this is design-spec authoring, not a live-regen change. It does NOT block the in-flight Stage-3 narrow deletion (which deletes only elemental-abandoned machinery and explicitly HOLDS the physical fallback to Stage 3b). The two are consistent: Stage-3 holds the physical fallback; this recognition names what replaces it.

## 7. Predictions registered (for empirical validation at commit)

1. **Substrate relocation dissolves the sparsity blocker.** Rooting physical identity on the weapon substrate (89,839 rows) relocates the kit_size + geometry source off the sparse physical-cost mechanic pools (rage=4 / focus=4 / combo=2 / stamina=2). The audit's stated deferral reason (pool sparsity → degraded 2–5-skill kits) ceases to be the kit_size bottleneck.
2. **Physical stops being the cutover's straggler.** Removing "physical" as a `dominant_element` pseudo-element eliminates the last label-classification fallback (`classify_archetype` → template). The physical path completes the same label-deletion the elemental path already finished — closing the smuggling trap on the one path that still carries it.
3. **One weapon + coordinate → both summoner and direct-caster.** Re-homing summon-vs-direct on skill composition (runtime label, Layer 2) rather than a pre-assigned coordinate bin (proxy-light / proxy-heavy) lets a single weapon + behavioral coordinate produce BOTH a summoner and a direct-caster depending on skill investment — matching D2 / D4 / Last Epoch genre truth, and retiring the inert deferred-proxy-bin residual.

## 8. Disposition / routing

- **gandalf:** recognition record authored (this doc); recognition LOCKED + validate DONE captured durably. **Design spec AUTHORED 2026-06-14** (Matt "author both") at `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` — element-coordinate keeps the behavioral 8-tuple; weapon (drawn from the cycle-14 balanced `v1_scope=1` pool) becomes the physical-vs-caster root; skill-composition becomes the summon runtime-label driver; non-humanoid branch flagged for a separate body-plan-as-identity treatment. Next gandalf step: review the rocket gate result → commit or revise.
- **jack-ryan:** decisions-log entry candidate — "Weapon-as-identity-surface recognition; physical-pool-expansion reframed as weapon-rooting" — and Gate-1 on the design spec when it lands.
- **rocket:** consumes the design spec at implementation; the weapon-flow audit (this doc § 2) is rocket's own finding, so the seam already holds the code-level map.
- **knight-rider:** sequences spec → Gate-1 → implementation → Gate-2 when Matt authorizes the commit; aware that this does not block Stage-3 narrow deletion (§ 6 sequencing note).
- **Stage 3b (BC-cutover scoping ruling):** its re-open criterion (physical-pool expansion) is reframed by this recognition — the expansion is weapon-rooting, not mere mechanic-pool growth.

---

**Signed:** gandalf, 2026-06-14
**For:** the weapon-as-identity-surface recognition — Matt's lock that the weapon bears kit identity (physical / caster / summon), validated by the weapon-flow audit (coordinate-rooted / weapon-as-output today, so a genuine reframe) whose findings nonetheless prove the diagnosis: the behavioral coordinate has no weapon/physical axis, so physical is smuggled as a pseudo-element and falls back to the label-template trap the BC-cutover deleted everywhere else — because physical identity is a weapon property, not a coordinate one; the reframe is substrate-honest (relocates identity onto the rich weapon substrate, off the sparse physical-cost pools), resolves into a clean three-layer model (weapon → physical/caster; skill-composition → summon runtime-label; coordinate → behavioral descriptor), is bounded to the humanoid branch (doc-37 non-humanoid forms derive identity from body-plan), bridges to the Synty weapon-sockets in the asset layer, and DEFERS the generation re-architecture to a gandalf design spec → jack-ryan Gate → rocket, gated on the weapon substrate demonstrably supplying kit_size without the sparse mechanic pools.
