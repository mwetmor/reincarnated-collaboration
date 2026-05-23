# Pre-LLM Substrate Inventory

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** Canonical-story design doc. Authored 2026-05-16 (Day 4). Prerequisite for `canonical/story/form-bias-cadence-strategy.md` (form-bias-cadence commission). Sibling to `canonical/story/embodiment-narrative-layer.md` and `canonical/37-form-bias-diagnosis-and-recovery.md`.

**Authored by:** gandalf (story + design steward), with code-accurate inventory pass by rocket (generation seam) filed at `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md`.

**Purpose:** Provide a disciplined, code-grounded description of every pre-LLM label and its associated logic in the engine that carries embodiment or cosmological implication. Name the patterns. Mark what's claimable. Mark what isn't.

**What this doc is NOT:** It is not a measurement of how the engine's labels contribute to observed convergence. It is not an attribution-style breakdown of "skew." Per the terminology lock established between gandalf and Matt on 2026-05-16 (Day 4), the word *skew* is off-limits until per-variable evidence exists. The same is true for *drift* in its outcome-claim sense. Both terms are reserved for the narrow uses Section 3 defines.

---

## 1. Why this doc exists

The form-bias diagnosis (`canonical/37-form-bias-diagnosis-and-recovery.md`) named the project's structural bias toward humanoid form and surfaced a list of "form-agnostic vs. humanoid-bound" surfaces in its § 2. That list was acknowledged in doc 37 itself as **non-exhaustive** and pending a generation-internals sweep before substantive dispatches could be authored.

Day 4 of the 2026-05-16 session brought a sharper problem. In opening dialogue I cited doc 37 § 6 as if it described the *current* state of the engine — claiming the canonical-four labels were already hidden from the LLM. Matt asked how I had verified that. I had not. Direct code-reading produced findings that contradicted my claim at every layer of the system: the canonical-four labels are saturated through engine-internal logic, every LLM call, the JSON export contract, and the player-facing UI. The diagnosis's prescription was being treated as already-implemented when nothing had shipped.

This is the **implementation-vs-intent drift** pattern doc 37 itself names as Discipline #13 candidate, caught in mirror image — I walked into the exact failure mode the doc was diagnosing.

The deeper correction came from Matt: the project has a strong *intent-baseline* (post-doc-37 cipher architecture, form-bias direction, embodiment-axis goal) but **no per-variable understanding of how individual pre-LLM components actually contribute to observed convergence.** Without that decomposition, *skew* is a directional impression, not a finding. Calling anything "drift" in the outcome sense presupposes a baseline we haven't measured.

This doc closes the implementation-side gap (what's there in code, with structural-presupposition tags) without claiming the outcome-side decomposition (what each variable contributes to observed engine output). It is descriptive in the strict sense the terminology lock requires.

The substrate this doc maps is the **prerequisite** for the form-bias-cadence strategy. Without it, the strategy doc's Q1 inventory would be incomplete and its Q2 skew characterization would commit the same epistemic error twice.

## 2. How this doc relates to others

- **Supersedes** doc 37 § 2's "form-agnostic vs. humanoid-bound" inventory. Doc 37 § 2 was a starting list; this is the exhaustive code-grounded successor. Doc 37 § 2 should be treated as superseded for inventory purposes; doc 37's diagnostic framing and architectural locks remain authoritative.
- **Prerequisite for** `canonical/story/form-bias-cadence-strategy.md` (the form-bias-cadence commission). The strategy doc's Q1 inventory references this; Q2 cluster-pattern analysis derives from this; Q4 decision framework names the catalogue-dependency gates surfaced in Section 11 below.
- **Defers to** `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md` for item-by-item code citations. That file enumerates all 53 catalogued items with file paths and line numbers. This doc synthesizes; that file enumerates.
- **Builds on** `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` (Day 4 re-engagement section). The canonical-elements thread captured the dialogue trace that produced the terminology lock and the catalogue-coupling insight; this doc operationalizes both.
- **Surfaces empirical experiments** that resolve named architectural opens: `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` (residual-bias resolution); `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` (per-season vocabulary coupling + multiple-groupings architectural choice).
- **Holds open** until the form-bias-cadence-strategy doc lands. When the strategy doc resolves, this inventory becomes the historical substrate; future edits land via the strategy doc and the decisions-log.

## 3. The terminology lock that constrains this doc's claims

This lock was established between gandalf and Matt on 2026-05-16 (Day 4) and approved as the lens for this inventory and all downstream form-bias work. The vocabulary matters because cheap words produce cheap thinking, and the form-bias work is precisely where cheap thinking would buy us a costly mistake.

| Term | Reserved for | NOT used for |
|---|---|---|
| **Drift** | Implementation-vs-intent gap. Observable directly from code by comparison to a stated design intent. *Example:* doc 37 § 6 states "hide canonical-four from LLM"; `llm/naming.py:32-35` prepends the canonical-four labels to every class/monster/gear naming prompt. The code-vs-intent comparison IS the drift instance. | The gap between intended engine output and observed engine output. That requires attribution-style decomposition and is not what we have. |
| **Structural presupposition** | Schema-shape claims readable from code alone. *Example:* `Loadout` has explicit `weapon`/`off_hand`/`armor`/`accessory` fields; the schema's shape itself presupposes hands/body/extremities/bilateral-anatomy. The presupposition is in the schema, not in any opinion about the schema. | Any inference about player perception or engine output that requires evidence beyond reading the code. |
| **Convergence shape** | Descriptive language for what the engine actually produces. *Example:* "Hunter has 1.82 modifier-range across seeds, per the B14.5 sidecar findings." Naming the observation without attributing cause. | A statement that any individual variable is responsible for a portion of that observed shape. |
| **Skew** | **Off-limits in this doc and downstream form-bias work** until per-variable evidence exists. Skew requires decomposition (how much of the observed convergence is attributable to which variable). No such decomposition has been produced. Using *skew* without the decomposition is the cheap-thinking error the terminology lock exists to prevent. | Anywhere. If a passage is tempted to say "the engine skews X," it must instead say "the engine has a structural presupposition toward X" (if claimable from code) or "the convergence shape observed is X" (if claimable from telemetry) — never the conjunction. |

Discipline #13 candidate as drafted in doc 37 § 9.1 collapses two distinct patterns and needs splitting:

- **#13a — Implementation-vs-intent drift.** Design intent unenforced in code drifts at the code surface. Observable directly. `naming.py:32-35` exhibits this. This is the discipline this doc's findings most clearly demonstrate and that the form-bias work primarily addresses.
- **#13b — Outcome attribution opacity.** Per-variable convergence contribution unknown without ablation. This is not "drift" — it is *unmeasured composition*. An epistemic gap, not a behavioral one. Discipline #13b is not actionable through process gates; it is actionable only through targeted empirical experiments (see Section 12 and the parked request files).

The form-bias-cadence-strategy doc and any decisions-log entries derived from this work should honor this split. The two patterns have different remedies and conflating them produces work that addresses neither cleanly.

## 4. The inventory at a glance

The exhaustive catalogue, with file path and line citations for every item, lives at `agentic_orchestration/gandalf/findings/2026-05-16-pre-llm-substrate-rocket-pass.md`. This section summarizes what's there at the cluster level and surfaces the patterns the cluster-shape reveals.

**53 items catalogued** across 12 named categories plus 5 discovered during the pass. Structural-presupposition tag distribution:

| Tag | Count | Where it concentrates |
|---|---|---|
| **humanoid-presupposing** | 14 | One tight schema cluster: loadout/gear |
| **form-agnostic-but-named-humanoid** | 18 | A second cluster: labels-on-mechanics, distributed across categories |
| **form-agnostic** | 9 | Role/timing/composition vocabulary, range profile, color hints |
| **embodiment-orthogonal** | 7 | Damage/ailment categories, trial mechanics, trait category enum |
| **uncertain — resolved in this doc** | 5 | See Section 13 for the five ambiguity resolutions |

The cluster shape is the most important finding in this inventory. **The 14 humanoid-presupposing items are not 14 distributed problems — they are one tight problem.** They concentrate in a single schema cluster (gear and loadout). Outside that cluster, the engine's structural presupposition is largely form-agnostic-but-named-humanoid: the mechanics are form-neutral; the labels carry humanoid weight.

This matters for the form-bias work because **fixing one cluster is operationally different from fixing 14 distributed surfaces.** A schema migration that addresses the loadout/gear cluster (per doc 37 § 4 Position C — slot-as-functional-mechanic + embodiment-as-narrative-skin) resolves the schema-shape concentration of humanoid-presupposition in one coordinated change. Re-labeling the broader form-agnostic-but-named-humanoid cluster is a separate, lower-stakes change that can stage independently.

Sections 5-8 below characterize each cluster in turn. Section 9 separately characterizes the implementation-vs-intent drift surface (Cluster E, "the universal LLM-drift inventory") which is orthogonal to the structural-presupposition cluster and addresses a different problem.

## 5. Cluster A — Humanoid-presupposing concentration (the loadout/gear schema)

**Count:** 14 items.
**Concentration:** Single schema cluster. `generation/gear_schema.py` + `generation/gear_generation.py` + `generation/gear_catalog.py`.
**Operational implication:** Schema migration territory per ADR-004. Multi-seam coordinated change (rocket schema + star-lord export + drax demo/loadout consumers).

The schema cluster's load-bearing presuppositions:

- **`Loadout` model fields** (`gear_schema.py:198-310`) — explicit `weapon`, `off_hand`, `armor`, `accessory` fields as first-class model attributes. The schema's *shape* presupposes a body with hands, a torso, and extremities.
- **`handedness` field on `GearInstance`** — values "1h"/"2h", with `off_hand` gated on `weapon.handedness == "1h"`. The schema presupposes bilateral arm anatomy: a dominant hand and an off-hand, with the option to commit both to a single object.
- **Base item type ids** (`gear_catalog.py:10-49`) — sword, staff, dagger, hammer, bow, wand, greatsword, helmet, chest, robe, hood, gauntlets, boots, belt, ring, amulet, shield, grimoire, orb, focus. These are medieval-humanoid combat equipment categories. They presuppose not just humanoid form but a specific cultural-historical reading of humanoid combat equipment.
- **`can_equip()` and `stat_requirements`** (`gear_generation.py:289-315`) — gating gear equippability on STR/DEX values. STR gates melee weapons and heavy armor; DEX gates bows. The gating logic maps humanoid physical capabilities directly onto equipment access. A crystalline construct or swarm has no natural STR in any physical sense; the schema does not contemplate this.
- **`_BASE_TYPE_STAT_AFFINITY`** (`gear_generation.py:368-396`) — same presupposition as `can_equip()` at the affix-eligibility layer.

**Why this cluster is one problem, not fourteen:**

Every item in this cluster falls under doc 37 § 4's Position C lock: *slot-as-functional-mechanic + embodiment-as-narrative-skin*. The Position-C resolution renames each humanoid-presupposing schema field to its functional analog (weapon → offensive-augmentation; armor → defensive-augmentation; accessory → accessory-augmentation; off_hand → secondary-offensive-augmentation when handedness=1h equivalent) and adds embodiment-as-display-skin so the player-facing name varies per embodiment (chest armor / viscosity layer / carapace ratio / resonance buffer).

The mechanical schema persists; the labels become functional; the narrative skin becomes embodiment-dependent. **One coordinated migration resolves the cluster.** The 14-item count is not a 14-piece complexity; it is the 14-surface manifestation of one schema-shape choice.

**What stays uncertain after the Position-C migration:** `can_equip()` and `stat_requirements` still presuppose humanoid attribute math (STR gating melee, DEX gating bows). Doc 37 § 2 names this explicitly: STR/DEX/INT "survive as abstract power dimensions divorced from physical interpretation" under structural realignment. The labels stay for engine math; the LLM-visible narrative reframes per-embodiment. This is a *narrative-skin* fix on math-bearing labels, not a math change. The cluster's structural-presupposition resolution is the schema rename; the math-bearing labels are handled at the LLM-visibility layer (Cluster E in Section 9 and Discipline #14 candidate).

## 6. Cluster B — Form-agnostic-but-named-humanoid concentration (labels-on-mechanics)

**Count:** 18 items.
**Concentration:** Distributed across element labels, class archetypes, attribute axes, geometry palette labels, material/suffix naming tables, energy-type vocabulary, canonical library names.
**Operational implication:** Per-label renaming + LLM-visibility filter work. Lower-stakes than Cluster A's schema migration; broader-surface than any single rename.

This cluster's items share a pattern: **the mechanic is form-agnostic; the label carries humanoid weight.** Examples:

- **Canonical-four element labels** (fire/water/earth/wind) — the mechanical opposition pair-structure is form-agnostic; the labels are Earth-realm classical-cosmology vocabulary that the LLM and player both see.
- **Class archetype labels** (warrior/mage/rogue/hunter/grappler/skirmisher) — stat templates and kit-composition targets are form-agnostic mechanically; the labels are humanoid social/martial roles.
- **Attribute axes** (STR/DEX/INT/WIS/VIT) — the math is form-agnostic; the labels carry humanoid-physical connotations (strength = muscular force; dexterity = manual agility).
- **Geometry palette labels** — `melee_strike`, `melee_arc`, `ground_slam`, `ranged_physical`, `leap_strike`, `whirlwind`, `dash_attack` — the AOE shapes and targeting types are abstract; the labels carry humanoid weapon-semantic gravity. (`projectile`, `circle`, `cone`, `line`, `ring`, `beam_channel`, `blink`, `teleport` are genuinely form-agnostic by both mechanic and label and live in Cluster C, not here.)
- **Material/suffix naming tables** (Cinderstone/Tideglass/Rootwood/Cloudspun; "of Embers"/"of Tides"/"of Stone"/"of Gales") — the deterministic-name-generation mechanic is form-agnostic; the specific vocabulary is Earth-realm-fantasy material culture.
- **Energy-type vocabulary** (`mana`/`focus`/`combo`/`rage`/`stamina-as-resource`) — the energy-pool mechanic is form-agnostic; the labels carry varying humanoid weight. `mana` and `focus` are abstract; `rage` and `stamina-as-resource` carry strong humanoid-experiential weight (a slime does not experience rage as a felt state).
- **Canonical library names** (`Searing Wave`, `Iron Rend`, `Stone Grasp`, `Tide Shroud`, `Wind Lance` from `library_generator.py:20-24`) — the library lookup mechanic is form-agnostic; the names are humanoid-fantasy vocabulary used as the "stable foundation" seasonal names decorate.

**The pattern's resolution is multi-surface and stages independently from Cluster A.** Each label class admits one of three treatments under the eventual form-bias work:

- **Hide from LLM-visible surfaces** (Discipline #14 candidate). The cipher architecture in doc 37 § 6 is the primary instance: canonical-four labels are hidden from LLM; per-season vocabulary fills the LLM-visible slot. Same pattern applies to class archetype labels, attribute axes, geometry labels — each can be hidden and replaced with per-instance vocabulary if the form-bias work commits to that direction.
- **Rename to form-neutral vocabulary at the engine layer.** "rage" becomes "intensity" or "drive"; "stamina-as-resource" becomes "endurance" or "throughput"; "warrior" becomes "front-line" or "engager." Mechanical math unchanged; labels shift toward form-neutrality. Risk: form-neutral labels often read as clinical or sterile (the "engineer-named-this-system" failure mode).
- **Keep humanoid labels and accept the bias as Phase-0 calibration.** The labels remain humanoid for genre legibility; the form-bias work focuses on Cluster A (schema migration) and Cluster E (LLM-visibility filter) without touching this cluster. Phase-0 ships ARPG-canon-comfortable; post-Phase-0 work expands.

The form-bias-cadence-strategy doc's Q4 should land which of the three treatments applies to which sub-cluster within B. This is a calibration question with multiple defensible answers; the strategic-axis lock (ARPG-canon-primary / Isekai-canon-primary / explicit-hybrid) drives which treatment fits which sub-cluster.

## 7. Cluster C — Form-agnostic mechanics

**Count:** 9 items.
**Concentration:** Role-orientation taxonomy, skill role vocabulary, timing vocabulary, composition mode, range profile, color hints, abstract geometry labels.
**Operational implication:** No form-bias work needed in this cluster. Catalogued for completeness; flagged as the *desirable* state the form-bias work brings other clusters toward.

These items are form-agnostic at both the mechanical and the label layer:

- **Role orientation** (damage/control/hybrid) — the 2026-05-08 Phase-2 decision was explicitly designed to be form-agnostic. The labels work for any entity form. ("Support" is excluded from solo generation as a game-design scope decision per file 29; not an embodiment claim.)
- **Skill role vocabulary** (primary_attack/burst_damage/area_damage/damage_over_time/control/mobility/defensive/sustain/utility/heal) — abstract mechanical roles. A slime's primary_attack and a humanoid's primary_attack differ in narrative but not in the mechanical role label.
- **Skill timing vocabulary** (instant/cast/charge/channel) — abstract temporal descriptions applicable to any entity form.
- **Composition mode** (single/layered/fused/triadic) — abstract structural vocabulary.
- **Range profile** (close/medium/long) — genuinely form-neutral. A slime at close range and a humanoid at close range are mechanically equivalent in this schema.
- **Color hints** (in `library_generator.py`) — hex color associations to element types; not embodiment claims.
- **Abstract geometry labels** within the geometry palette — `projectile`, `circle`, `cone`, `line`, `ring`, `beam_channel`, `blink`, `teleport`. The other palette items are in Cluster B.

The form-bias work should not touch this cluster. Its existence shows the engine's mechanical-substrate is largely form-agnostic where the labels also are; the form-bias problem concentrates where labels diverge from the mechanics' form-neutrality (Cluster B) or where the schema itself presupposes form (Cluster A).

## 8. Cluster D — Embodiment-orthogonal

**Count:** 7 items.
**Concentration:** Damage/ailment categories, trial naming-triad mechanics, spirit-guide kit-composition framing, trait category enum.
**Operational implication:** No form-bias work needed. The labels here are about *something other than embodiment entirely*.

- **Damage/ailment categories** (`burn`/`chill`/`root`/`knockback`/`bleed`) — these are mechanic-flavor labels for control and DoT effects. Their canonical-four keys are form-agnostic-but-named-humanoid at the *element* layer (Cluster B), but the ailment names themselves describe the *mechanical effect*, not the entity's embodiment.
- **Trial/Mirror/Passage naming-triad mechanics** — cosmological/player-journey concepts per `canonical/story/naming-triad.md`. The "doppelganger" technical term is retained for internal engine use; player-facing names are Trial/Mirror/Passage. These concepts are about the structure of the seasonal arc, not about entity embodiment.
- **Spirit-guide kit-composition framing** — game-design scope decisions (support excluded from solo generation; spirit-guide as marginal-value-analyzer in simulation seam). Not embodiment claims.
- **Trait category enum** (STAT/ABILITY/GRANTED) — abstract taxonomy of how traits modify gameplay. Not embodiment-related.

This cluster exists for completeness in the inventory. No further analysis required.

## 9. Cluster E — The universal LLM-drift inventory (implementation-vs-intent gap)

**This is a separate kind of finding from Clusters A-D.** It is not a structural-presupposition cluster; it is a *drift inventory* in the precise sense the terminology lock allows — a code-vs-intent comparison.

**Stated intent:** doc 37 § 6 — "the four canonical elements must be blocked from view of all LLM calls so that more forms can converge/coalesce."

**Code reality, 2026-05-16:** every LLM call in the generation seam currently exposes canonical-four labels. The universality is the finding.

The drift surface, exhaustively:

| Call site | Exposure | Frequency |
|---|---|---|
| `llm/naming.py:26-36` (`_elements_summary_line`) | Prepends `"Seasonal elements: fire={name}, wind={name}, water={name}, earth={name}"` to every class/monster/gear naming prompt | Every class, monster, gear naming call — many per season |
| `llm/naming.py:87` | Prepends `"Season theme: {canonical-four string}"` to every naming call | Every naming call |
| `llm/naming.py:89` | Includes `"Element: {skill.canonical_element}"` as a literal canonical-four string | Every skill naming call |
| `element/selector.py:43-47` | System prompt explicitly names "the season's four canonical role-slots (fire, wind, water, earth)" | Every element selection call (once per season) |
| `element/selector.py:394-446` | Element selection prompt body exposes canonical-four role-slot labels as section headers and JSON output keys | Once per season |
| `canonical/library_generator.py:85` | One-time canonical library generation prompt includes `"- Element: {canonical-four name}"` | One-time at engine setup; affects all downstream library lookups |

**Net:** there is no LLM call in the generation seam that does not currently expose canonical-four labels. The drift is universal, not partial.

**The drift's character matters for the form-bias work.** This is not a case where some LLM calls are clean and others have slipped; this is a case where the cipher architecture was specified in doc 37 § 6 but no code work has shipped against the specification. The full migration is ahead of us, not behind us.

**Why this is the cleanest drift instance in the project so far.** Implementation-vs-intent drift is observable from code-reading alone (the terminology lock's narrow legitimate use of "drift"). Doc 37 § 6 specifies; `llm/naming.py:32-35` and the other sites contradict. No telemetry needed. No measurement needed. The code IS the evidence.

**Resolution shape:** Discipline #14 candidate (Internal-vs-generative schema separation, the reviewable process check from doc 37 § 9.2b). At every LLM prompt-construction site, the canonical-four labels are stripped and replaced with per-season vocabulary; per-instance JSON output keys replace canonical-four-keyed structures; the cipher's mechanical-pair substrate stays internal. The migration is mechanical once direction is locked, but it is *broad* — every call site touched.

## 10. The three-layer model as candidate architecture

The catalogue-coupling insight surfaced 2026-05-16 (Day 4) by Matt — "even a hidden canonical key-pair driven potential element could produce an outlying catalogue-VFX-mapping" — combined with the multiple-groupings architectural refinement that emerged in the same dialogue, points to a **three-layer model** richer than doc 37 § 6's two-layer cipher (canonical-four substrate + per-season vocabulary):

| Layer | What it is | What sees it |
|---|---|---|
| **Substrate** | Catalogue's emergent abstraction tag space (currently Pimen's 9: fire/water/earth/wind/ice/holy/dark/thunder/acid; eventually whatever Elrond's abstraction analysis produces) | Engine-internal only. LLM never sees these labels. Resistance translation and visual-coverage map happen here. |
| **Grouping** | The active per-season opposition structure. Selected from a finite set of valid groupings derived empirically from the substrate. 4-5 active tags per season, chosen for thematic coherence + mechanical distinctness + role-orientation coverage. | The LLM may see the grouping structure (primary opposition / secondary opposition slots) but not the substrate tag identities. The player feels the grouping's archetypes in combat. |
| **Vocabulary** | Per-season LLM-generated names for the grouping's slots. "Pressure" / "vacuum" / "bioluminescence" / "decay" for a deep-sea cosmology; "harmony" / "dissonance" / "melody" / "rhythm" for a music-spirit cosmology if the grouping supports it. | The player and the rest of the LLM call chain see this. Player-facing surface lives here. |

**Why three layers and not two:**

A two-layer cipher (substrate + vocabulary) faces the genre-canon constraint that no shipping ARPG ships above ~6-7 simultaneously-active mechanical damage types. The player-cognition ceiling on working combat memory caps simultaneous-active types at 5-7. Substrate-wider-than-7 with all tags active per season violates the ceiling and produces Last Epoch / Grim Dawn-style mechanical overlap that players struggle to distinguish in combat.

The grouping layer absorbs the bandwidth tension. The substrate is wide (catalogue coverage); the per-season active grouping is narrow (4-5 tags); the player's working combat memory load is genre-canonical. The seasonal rotation across different groupings provides the cross-season variety that no shipping ARPG has the procedural-generation primitive to deliver.

**Genre-internal precedents** for the substrate-wide / active-narrow pattern: Solo Leveling's Shadow Army (100+ accumulated; 5-8 active per fight); Hollow Knight's charms (45 charms; 5-8 notch-equipped). The pattern ships when the active set per session passes mechanical-distinctness and role-coverage filters.

**Empirical validation status:** the multiple-groupings architecture is the *surfaced recommendation* of the gandalf-Matt 2026-05-16 dialogue, with empirical grounding deferred to the catalogue-mapping-and-grouping experiment (parked at `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`). The experiment's findings determine whether multiple-groupings is viable (3-5 robust groupings emerge passing the three filters), or whether the architecture collapses to a single fixed grouping (1-2 groupings survive; refined-Option-A becomes a single 4-5-tag cipher), or whether the genre constraint reasserts and the canonical-four cipher remains operative with catalogue-curation translation at the VFX layer.

**Relationship to doc 37 § 6 Position (ii):** the three-layer model is a refinement of Position (ii), not a contradiction. Position (ii) locked "per-season vocabulary carries its own mechanical signatures; cipher = resistance-translation only." The three-layer model honors that lock and adds the grouping-selection layer between substrate and vocabulary. The cipher (substrate) still does resistance-translation only. The grouping layer is new; the vocabulary layer is what Position (ii) already specified.

## 11. The four catalogue-track dependencies

The form-bias-cadence-strategy doc's Q4 decision framework must name four specific locks as **explicitly deferred to catalogue-track findings**. None of them resolve in dialogue; all four resolve through specific empirical milestones in the catalogue work.

| Lock | Resolves when | Why deferred |
|---|---|---|
| **Cipher-width** (Options A/B/C from the parked canonical-elements thread) | Elrond's emergent-grouping analysis runs against the full Pimen crawl + any additional Tier-1 catalogue sources | The right cipher width is whatever the catalogue's abstraction layer actually produces. We're not picking width; we're discovering it. |
| **Foundation layer placement** (Flag B from rocket inventory; `foundation/foundation.py:39-43` hard-codes 4-rotating + 1-physical) | Cipher-width decision + L1/L2 placement decision land. Foundation either grows with the substrate (cipher-coupled) or decouples (substrate becomes L2 Reincarnated-cosmology layer; Foundation stays as engine-substrate concept) | Architectural decision about layer ownership. Maps onto Q5 of the parked canonical-elements thread. Cannot resolve without empirical-substrate-shape findings. |
| **D1 element-name pool reconsideration** | Cipher architecture is determined AND Flag A rubric-screening empirical test runs (see Section 12) | Currently structured around canonical-four cipher. The 156-entry pool's allow-list / eligible / quarantine tiering may or may not survive the cipher migration. Reconsideration is much larger than entry-by-entry review (the pool approach itself may not survive). Both gates must close before dispatch is scoped. |
| **Per-season vocabulary coupling policy** (α validation+regenerate / β in-prompt constraint / γ runtime fallback) | Catalogue-mapping-and-grouping experiment lands findings | Surfaced 2026-05-16 (Day 4) by Matt. Choice depends on empirical mapping behavior of representative per-season vocabulary against catalogue tag space. |

The form-bias-cadence-strategy doc's Q4 should name each of these as a deferred-pending-empirical-input item with the specific resolution gate cited. Matt's strategic-axis lock (ARPG-canon-primary / Isekai-canon-primary / explicit-hybrid-with-defined-axis) can be made independently; the four sub-locks resolve at the catalogue milestones above and inherit the strategic-axis context.

## 12. The two decision-critical-and-unknowable flags

Per the rocket inventory pass, two findings are flagged as decision-critical and unknowable from code-reading alone. Both block specific dispatches and must resolve before the form-bias-cadence-strategy doc's recommendations land as decisions-log entries.

### Flag A — D1 rubric structurally screens for humanoid-fantasy compounds

**Where:** `element/selector.py:282-296`. Five yes/no scoring questions embedded in an LLM mini-call evaluating novel element-name candidates. Q2 asks "`{word}-bolt` or `{word}-armor`," Q4 asks "`{word}-Knight` or `{word}-Mage`." Each "Y" answer contributes +2 to `d1_score`. Threshold ≥8 = allow-list; ≥5 = eligible; <5 = quarantine.

**The structural-presupposition:** the rubric embeds humanoid-fantasy compounding into the scoring logic. A word like "pressure" (perfect for a deep-sea cosmology) likely scores 6-7 — passes "eligible" but not "allow-list" — because "pressure-Knight" sounds awkward, even though "pressure-Surge" or "pressure-Bearer" would land natively in context.

**Why unknowable from code-reading:** the *systematic-screening effect* is empirical, not structural. The schema is readable; whether the rubric reliably under-scores non-humanoid-cosmology candidates across a test set is a measurement question.

**Gates:** D1 element-name pool reconsideration dispatch. Cannot scope D1 work without knowing whether the rubric needs replacement, repair, or supplementation.

**Resolution:** targeted empirical test running the rubric on a curated set of non-humanoid-cosmology candidate words. Small scope, runnable through the existing LLM client.

### Flag B — Foundation model validator and cipher architecture extension

**Where:** `foundation/foundation.py:39-43`. A `model_validator` enforces: exactly 1 non-rotating element, named `"physical"`, plus 4 rotating elements. Any cipher expansion (Options A/B from the parked canonical-elements thread; refined-Option-A from the three-layer model) requires this validator to update — but the architectural question of *what the new validator should enforce* depends on layer-placement decisions that have not been made.

**The architectural question:** does Foundation grow with the cipher (substrate becomes 7-9 rotating + 1-physical, with the validator updated to reflect)? Or does Foundation decouple from the cipher (substrate becomes a separate L2 Reincarnated-cosmology concept; Foundation remains an L1 engine-substrate validation, perhaps now generic across "rotating dimensions" rather than canonical-four specifically)?

**Why unknowable from code-reading:** the right answer is an architectural-layer decision, not a code-state observation. The current code reflects the canonical-four lock; the future code reflects whatever layer-placement decision lands. Code-reading reveals the constraint, not the resolution.

**Gates:** any cipher migration dispatch. Cannot author the rocket / star-lord / gamora dispatches that implement the form-bias work without resolving Foundation's role under the new architecture.

**Resolution:** Q4 of the form-bias-cadence-strategy doc absorbs this question. The catalogue-mapping-and-grouping experiment's findings inform the substrate-shape decision; the layer-placement decision is then a design call (likely Matt's) on whether engine and Reincarnated-cosmology should share substrate or not.

## 13. Evidence audit — what we know; what we don't

Per the terminology lock, the evidence audit is structured to honor the difference between *what we have* and *what we wish we had.* The latter is named explicitly so future work knows where to look.

| Question we'd want to answer | Evidence we have | Evidence we don't have |
|---|---|---|
| What is the engine's current convergence shape across seasons? | Aggregate B14.5 sidecar findings (`project_b14_5_sidecar_analyses.md`): hunter modifier-range 1.82; fire over-representation 23.6% vs 20% uniform; convergence-iteration distribution; close-range-controller existence. | Per-variable attribution. Which labels contribute which fraction of which observation. |
| Does the canonical-four-in-prompt drift (Cluster E) affect generated content quality? | None directly. We have demo1 v1.2 ship + 5 fully-clean seasons in production (seeds 1001-1005) as the existing baseline. | Counter-factual: what does generated content look like with canonical-four hidden? The no-seed cosmology test (`agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`) is the empirical resolution of doc 37 § 6.5's residual-bias open question. Not yet run. |
| Does the per-season vocabulary coupling work under any of α / β / γ? | None. The question is new (surfaced 2026-05-16 Day 4). | Empirical mapping behavior of representative vocabulary against the catalogue's tag space. The catalogue-mapping-and-grouping experiment (`agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`) is the empirical resolution. Not yet run. |
| Does multiple-groupings architecture produce 3-5 robust groupings passing mechanical-distinctness + role-orientation-coverage + genre-recognition filters? | None directly. Genre precedent (Solo Leveling, Hollow Knight) suggests substrate-wide / active-narrow patterns are viable. ARPG genre precedent (D2 5; D4 6; PoE 5; Last Epoch 7; Grim Dawn 9) bounds the active-set size. | Same empirical resolution as above. |
| Does the D1 rubric systematically screen non-humanoid-cosmology candidates? | None. Flag A specifically. | Targeted test running the rubric on non-humanoid-cosmology candidates. Sub-experiment of the catalogue-mapping-and-grouping work or a separate small commission. |
| Does the form-bias work, once implemented in stages 1-3, produce convergence-shape changes that align with the design intent? | Existing telemetry will measure this *after* implementation. The staging discipline (Stage 1 add embodiment-axis; Stage 2 add abstract pair-structure layer alongside canonical-four; Stage 3 hide canonical-four from LLM) produces free measurement by comparison of stages. | This is post-implementation, not pre. Named here so the staging discipline is honored — the comparison work IS the measurement. |

The audit is mostly an audit of absence. This is honest. The form-bias work proceeds against an intent-baseline + structural-presupposition findings + a small set of bounded empirical experiments resolving named opens — not against per-variable convergence-attribution decomposition. The terminology lock exists to keep that honest as the work unfolds.

## 14. What this doc unblocks

When this doc lands and the form-bias-cadence-strategy doc is authored against it:

- **Form-bias-cadence-strategy Q1 inventory** has a code-grounded, cluster-organized, terminology-disciplined substrate to reference rather than reproduce
- **Form-bias-cadence-strategy Q2 cluster-pattern characterization** has Clusters A-E to characterize rather than 53 distributed items
- **Form-bias-cadence-strategy Q4 decision framework** has four catalogue-track dependency gates explicitly named and the three-layer model as a candidate architecture to surface
- **Engineering Disciplines #13a, #13b, #14 candidates** in `engineering-disciplines.md` can be drafted with the terminology lock as the lens; jack-ryan Gate 1 review proceeds against the lock; Matt approves with the lock as the constraint
- **The two empirical experiment request files** (no-seed cosmology test; catalogue-mapping-and-grouping experiment) have explicit framing for what each resolves and what each does not
- **Cipher migration dispatches** (rocket schema work, star-lord LLM-prompt-filter work, gamora doppelganger-gate validation under Position (ii), drax display-leak audit + body-swap UI work) can be scoped after the strategy doc lands, with the cluster organization providing the natural dispatch boundaries

## 15. Maintenance and supersession

**This doc holds open** until the form-bias-cadence-strategy doc lands. While open:

- Any pre-LLM substrate change in the engine (label rename, schema field addition, new label introduction, LLM prompt-construction change) should reference this doc's cluster organization. New items get added to the appropriate cluster with structural-presupposition tagging per Section 3's terminology lock.
- The five resolved ambiguities (anchor vocabulary; PlayerClass.skills kit-of-skills framing; rage/stamina-as-resource energy types; D1 rubric; canonical library names) are settled at the inventory level. The architectural decisions they inform (D1 rubric replacement; canonical library re-generation; etc.) remain open and resolve elsewhere.

**Supersession trigger:** when the form-bias-cadence-strategy doc lands with Q4 locks resolved AND the first cipher migration dispatch ships, this doc becomes historical substrate. Future edits land via the strategy doc and the decisions-log; this doc is preserved as the trace.

**Cross-references to maintain** as the form-bias work progresses:

- `canonical/37-form-bias-diagnosis-and-recovery.md` — § 2 is superseded by Sections 5-9 here; § 6 cipher architecture remains operative but is refined by Section 10's three-layer model; § 10 open questions are partially resolved by the empirical-experiment requests this doc surfaces
- `canonical/story/embodiment-narrative-layer.md` — Position C and the embodiment-as-narrative-skin lock remain authoritative; this doc's Cluster A characterization is the operational reading of those locks
- `canonical/story/naming-triad.md` — anchor → spirit name → embodiment-flavored name structure; this doc's Cluster D notes embodiment-orthogonality of trial/mirror/passage naming, which is consistent with the naming-triad's framing
- `canonical/story/engine-generic-meta-structure.md` § "The three-layer model" — Section 10 here is a refinement of the engine-generic three-layer model with the substrate/grouping/vocabulary cut; both docs should be kept in sync as the architecture evolves
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` — re-parked thread; resolution lives in form-bias-cadence-strategy doc Q4 + decisions-log

---

The hat stays on.

— gandalf, 2026-05-16 (Day 4)
