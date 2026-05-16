# Decisions-log entry drafts — Form-bias cadence strategy (5 entries)

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source:** Gandalf's `canonical/story/form-bias-cadence-strategy.md` (751 lines, Day-4 deliverable) — see § 8 "Decisions-log derivation notes" which specifies these five entries explicitly. Strategic-axis lock is Matt-approval-pending per the strategy doc § 5.5.
**Process:** Knight-rider drafts → jack-ryan Gate 1 (cross-seam empirical: design decisions affect rocket schema + star-lord prompts + drax display + gamora gates → triggers INVOKE per rubric) → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`.

**Target location:** before the "Recently considered, not yet decided" section, after the 2026-05-16 calibration-epoch entry (committed `c000d7d`). All 5 entries land together as a coordinated block (they cross-reference each other; splitting them across commits would invite drift).

**Companion-to:** the 2026-05-16 engine-balance-stewardship entry (Drift-7/8/9 closure + multi-dimensional divergence framework) — this set is the form-bias-side counterpart that resolves Drift-7-equivalent for the LLM/generation seam.

---

## Entry 1 — Form-bias strategic-axis locked as explicit-hybrid Phase-0

### 2026-05-16: Form-bias strategic-axis locked as explicit-hybrid Phase-0 (ARPG-canon-primary at substrate-mechanical layer + Isekai-canon-primary at narrative-skin and convergence layers); Position C reaffirmed; four catalogue-track sub-locks explicitly deferred

**Decision:** Phase-0 (the current seasonal-journey portion of Reincarnated) ships with two locked sub-positions on the form-bias / canon-match axis:

- **(a) ARPG-canon-primary at the substrate-mechanical layer.** Cluster A's mechanical schema preserved as locked in doc 37 § 4 Position C. Cluster B's mechanical math preserved (attribute math; element-tagged scaling; archetype templates). The engine ships with a substrate ARPG-fluent players will recognize at first contact.
- **(b) Isekai-canon-primary at the narrative-skin and convergence layers.** Embodiment axis added per `canonical/story/embodiment-narrative-layer.md`. Position C's narrative-skin rendering implemented. Cipher architecture (doc 37 § 6) implemented per Discipline #14 candidate. Per-season vocabulary generates against the cipher's abstract pair-structure; canonical-four labels hidden from LLM. The naming triad's per-season variants surface cosmological resonance per `canonical/story/naming-triad.md`.

**Phase-0 vs post-Phase-0:** Phase-0 holds the explicit-hybrid lock above. Post-Phase-0 (the Earth meta-layer per `canonical/story/cosmology-reincarnated.md` § "Ascension and the Court" + memory note `project_earth_meta_layer.md`) leans further isekai-side (the Court's accumulation pattern is fundamentally Solo-Leveling-Shadow-Army-shaped; the form-library mechanism is isekai-genre-canonical). Phase-0's ARPG-mechanics-substrate persists into post-Phase-0; the meta-layer presentation goes deeper into isekai canon.

**Position C reaffirmed.** The commission asked whether Q4's analysis surfaces a Position C revisit. Per gandalf's analysis (form-bias-cadence-strategy § 5.2): no. Position C (slot-as-functional-mechanic + embodiment-as-narrative-skin) is the exact architectural shape the strategic-axis lock requires. It preserves ARPG-canon at the mechanical layer and admits isekai-canon at the narrative-skin layer. Position A and Position B remain rejected for the reasons in doc 37 § 4 and reaffirmed in the strategy doc.

**Reasoning:** Per gandalf's strategy doc § 5.1 + § 5.2 + § 5.4 + § 5.5. The decision rests on the asymmetric Q3 finding (strategy doc § 3.3): the engine substrate is **ARPG-canon-comfortable across the board** (Diablo II / D3 / D4 / PoE / Last Epoch / Grim Dawn all share the weapon/armor/accessory schema + STR/DEX/INT + humanoid hero embodiment that the engine has) and **isekai-canon-incompatible at one specific cluster** (Cluster A — gear/loadout schema cannot express Slime / Spider / Dragon Hatchling embodiment per Legolas Pass 1's non-humanoid-reincarnation sub-genre evidence). Outside Cluster A, isekai-incompatibility is either neutral (Cluster C / E) or already partly-resolved (Cluster D naming-triad work).

The explicit-hybrid framing operationalizes through the cluster-localized decision framework (strategy doc § 5.4): each cluster's resolution is its own coordinated change. Form-bias work does NOT collapse into a single architectural decision; it is a coordinated bundle of cluster-localized decisions with shared discipline (Discipline #13a / #13b / #14 — see Entry 4).

**Alternatives considered (per strategy doc § 5.4):**

- **ARPG-canon-pure (revert sub-lock b):** rejected. Sacrifices the isekai-genre-correct embodiment variance the project's design lineage commits to (per `project_design_intent.md` body-swap differentiation + `project_earth_meta_layer.md` form-library framing). Phase-0 would ship as a competent-but-undifferentiated ARPG; demo VS2b's Substrate Realignment work would have no architectural home.
- **Isekai-canon-pure (revert sub-lock a):** rejected. Sacrifices the ARPG-genre-readability the Western audience needs at first contact (per Legolas Pass 4 ARPG-community discourse). Players approaching from D2 / D4 / PoE / Last Epoch would lose the build-identity vocabulary they're fluent in; the substrate would read as "exit from the genre" per strategy doc § 3.1.
- **Defer the lock pending experiment:** rejected per Matt's 2026-05-16 parallel-workstream mandate. The strategic-axis lock is structurally independent of the four deferred catalogue-track sub-locks (see Entry 3); waiting would block VS2b S1/S2 work that has no dependency on those sub-locks.
- **Single-canon collapse (no Phase-0 / post-Phase-0 split):** rejected. The post-Phase-0 Earth meta-layer is fundamentally isekai-shaped (per `project_earth_meta_layer.md`); forcing Phase-0 to commit to the same lean would over-shoot Western ARPG-audience readability at first contact.

**Cross-seam cascades:**

- **Rocket** preserves the ARPG-canon-mechanical-substrate (sub-lock a) at every dispatch. The narrative-skin layer (sub-lock b) lands at schema-emit and display-coordination boundaries. See strategy doc § 9.1 for the per-stage rocket cascade.
- **Star-lord** enforces sub-lock (b) at the LLM-visible surface. Canonical-four is hidden; per-season vocabulary is what reaches the LLM and player. Six named drift sites in Cluster E (per strategy doc § 1.1) get refactored at Stage 3. See § 9.2.
- **Gamora** preserves the ARPG-canon-mechanical-balance (sub-lock a) at the simulation layer. Per-season mechanical-signature variety is the isekai-canon affordance the doppelganger gate must validate without breaking. See § 9.3.
- **Drax** delivers sub-lock (b) at the player-facing surface. Per-embodiment narrative skin renders; the player sees isekai-canon embodiment variance honored at body-swap moments. See § 9.4.
- **Elrond** + **legolas** catalogue work is structurally independent of the strategic-axis lock; outputs inform the four deferred sub-locks (see Entry 3). See § 9.5 + § 9.6.

**Status:** Active. The 4-stage migration sequence (per Entry 5 cadence lock) implements this lock across the team.

**Related:**

- `reincarnated-collaboration/canonical/story/form-bias-cadence-strategy.md` (the full strategy doc — gandalf's 751-line Day-4 deliverable; § 5 is the authoritative source for this entry)
- `reincarnated-collaboration/canonical/story/embodiment-narrative-layer.md` (sub-lock b operationalization)
- `reincarnated-collaboration/canonical/story/pre-llm-substrate-inventory.md` (gandalf+rocket cluster framing the strategic-axis acts on)
- `reincarnated-collaboration/canonical/story/cosmology-reincarnated.md` (post-Phase-0 Earth meta-layer)
- 2026-05-08 doc 37 § 4 Position C decision (reaffirmed by this entry)
- 2026-05-16 engine-balance-stewardship entry (companion; cross-cluster discipline)
- Companion entries below: Entry 2 (three-layer model); Entry 3 (four sub-locks deferred); Entry 4 (disciplines #13a + #13b + #14); Entry 5 (cadence Option II)

---

## Entry 2 — Three-layer model + cipher-width framework

### 2026-05-16: Form-bias architecture lands as three-layer model (substrate / grouping / vocabulary); cipher-width framework explicit with width itself deferred to catalogue-mapping experiment

**Decision:** The form-bias work's operational architecture is a refined three-layer model that absorbs doc 37 § 6's two-layer cipher (substrate + vocabulary) by adding a **grouping layer** between them:

| Layer | What it is | What sees it |
|---|---|---|
| **Substrate** | Catalogue's emergent abstraction tag space. Currently Pimen's 9 (fire/water/earth/wind/ice/holy/dark/thunder/acid); eventually whatever elrond's abstraction analysis produces from the full Tier-1 catalogue crawl set. | **Engine-internal only.** LLM never sees substrate labels. Resistance translation + visual-coverage map happen here. |
| **Grouping** | The active per-season opposition structure. Selected from a finite set of valid groupings derived empirically from the substrate. **4-5 active tags per season**; chosen for thematic coherence + mechanical distinctness + role-orientation coverage. | The LLM may see the grouping *structure* (Primary Opposition / Secondary Opposition slots — abstract labels) but **not the substrate tag identities**. The player feels the grouping's archetypes in combat. |
| **Vocabulary** | Per-season LLM-generated names for the grouping's slots. Pressure / vacuum / bioluminescence / decay for deep-sea; harmony / dissonance / melody / rhythm for music-spirit. | **Player + the rest of the LLM call chain see this.** Player-facing surface lives here. |

**Why three layers and not two (load-bearing):** the two-layer cipher (substrate + vocabulary) faces the genre-canon constraint that no shipping ARPG ships above ~6-7 simultaneously-active mechanical damage types. Player-cognition ceiling on working combat memory caps simultaneous-active types at 5-7 (per Legolas Pass 4 + Pass 5 + Hollow Knight's 45-charms-but-5-8-active pattern). Substrate-wider-than-7 with all tags active per season violates the ceiling and produces Last Epoch / Grim Dawn-style mechanical overlap players struggle to distinguish in combat.

The grouping layer absorbs the bandwidth tension. Substrate is wide (catalogue coverage); active grouping is narrow (4-5 tags); player's working combat memory load is genre-canonical. Seasonal rotation across different groupings provides cross-season variety no shipping ARPG has the procedural-generation primitive to deliver.

**Genre-internal precedents** for the substrate-wide / active-narrow pattern: Solo Leveling's Shadow Army (100+ accumulated; 5-8 active per fight); Hollow Knight's charms (45 charms; 5-8 notch-equipped). The pattern ships when the active set per session passes mechanical-distinctness + role-coverage filters.

**Cipher-width framework (explicit even with cipher-width itself deferred — see Entry 3):**

When the catalogue-mapping-and-grouping experiment returns, the following decision criteria apply:

1. **Substrate-coverage criterion:** the substrate-layer width is determined by the catalogue's emergent abstraction tag space. **We discover the width; we don't pick it.**
2. **Grouping-viability criterion:** the grouping-layer width per season is determined by mechanical-distinctness + role-orientation coverage + thematic coherence + genre-recognition (Western ARPG-audience reads the grouping as legible).
3. **Outcome possibilities (all compatible with the strategic-axis lock from Entry 1):**
   - **3-5 robust groupings emerge** passing all filters → multiple-groupings architecture viable; seasonal rotation gains cross-season grouping variance as a structural pillar
   - **1-2 groupings survive** → refined-Option-A collapses to a single fixed grouping; the cipher becomes a single 4-5-tag opposition structure derived from the substrate; cross-season variety is in vocabulary + anchor, not in grouping
   - **No grouping survives** → the canonical-four cipher remains operative; catalogue-curation translation handles substrate-to-VFX mapping at visualization; doc 37 § 6 cipher is unchanged
4. **Foundation layer placement (Flag B)** resolves jointly with cipher-width (see Entry 3). If substrate is Pimen-derived (9 tags), Foundation either grows to 9 (Foundation-coupled-to-substrate; engine treats substrate as L1) or decouples (substrate becomes L2 Reincarnated-cosmology concept; Foundation stays at 4-rotating-plus-1-physical as L1 generic).

**The cipher architecture stays operative.** Per doc 37 § 6 Position (ii) and the operationalized work in `naming-triad.md` + `embodiment-narrative-layer.md` + `engine-generic-meta-structure.md`:
- Per-season vocabulary carries own mechanical signatures
- Cipher does resistance translation only (not mechanical-signature gating)
- Canonical-four labels hidden from LLM
- Per-season vocabulary is what the LLM generates; LLM sees abstract pair-structure (Primary / Secondary) at the grouping layer
- **Ailment-damage-signatures work flagged as Future** — load-bearing dependency for the doppelganger gate under Position (ii) per strategy doc § 9.1 ("Future" entry in rocket cascade). Memory note `project_ailment_damage_thematic.md` records this as DEFERRED post-KI-B6-1 with explicit "revisit after B14.5 lands" trigger; B14.5 V1 has landed (2026-05-16 calibration epoch declared `c000d7d`), but formal deferral-lifting is pending Matt confirmation in this batch. If Matt confirms the deferral is lifted, this bullet upgrades to "re-activated as load-bearing dependency" in a follow-on amendment

The three-layer model **refines** this architecture; it does not replace it. Position (ii) is preserved. The cipher's resistance-translation job is preserved. The new grouping layer adds the per-season opposition selection between substrate and vocabulary.

**Reasoning:** Per gandalf's strategy doc § 6.1 + § 6.2 + § 6.3. The three-layer model converges (a) the strategic-axis lock's structural needs (Entry 1), (b) doc 37 § 6 cipher Position (ii), (c) `engine-generic-meta-structure.md`'s pre-existing three-layer framing, and (d) the four deferred sub-locks' framework requirements (Entry 3). It is the single architectural commitment that absorbs all four catalogue-mapping-experiment outcomes without revision.

**Alternatives considered:**

- **Stay with two-layer cipher (doc 37 § 6 as-locked):** rejected. Violates the genre-canon working-combat-memory ceiling at substrate widths >7 unless additional mid-layer compression is added — which IS the grouping layer. Naming it explicitly is honest.
- **Pick cipher-width now (Option A / B / C from canonical-elements-one-pool thread):** rejected. Premature without catalogue-mapping experiment findings. The thread was re-parked and absorbed into this framework (`agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` marked CLOSED 2026-05-16 with this absorption noted).
- **Single-layer (vocabulary-only, no substrate or grouping):** rejected. Loses the cipher's resistance-translation function; loses the genre-canonical mechanical-distinctness structure.

**Cross-seam cascades:**

- **Rocket** Stage 2 dispatch (per Entry 5) emits the grouping layer alongside canonical-four; substrate stays internal.
- **Star-lord** Stage 2 + Stage 3 dispatches consume grouping labels at LLM-construction sites; substrate stays out of LLM view.
- **Gamora** doppelganger gate validates against per-season mechanical signatures (grouping-derived).
- **Elrond + legolas** catalogue work IS the substrate-layer supplier; emergent-abstraction analysis (post catalogue-mapping experiment) determines substrate width.
- **Drax** consumes grouping data for combat / loadout / encounter display; substrate never reaches drax's seam.

**Status:** Active. Framework operative now; specific cipher-width resolves at catalogue-mapping experiment landing (per Entry 3).

**Related:**

- `canonical/story/form-bias-cadence-strategy.md` § 6 (authoritative source)
- `canonical/story/engine-generic-meta-structure.md` (original three-layer framing this entry refines)
- 2026-05-08 doc 37 § 6 Position (ii) cipher (preserved by this entry)
- `canonical/story/naming-triad.md` (per-season vocabulary generation)
- `canonical/story/embodiment-narrative-layer.md` (vocabulary-layer per-embodiment modulation)
- `agentic_orchestration/gandalf/open-threads/2026-05-16-canonical-elements-one-pool.md` (parked thread CLOSED; absorbed into this entry)
- Companion entries: Entry 1 (strategic-axis); Entry 3 (sub-locks deferred); Entry 4 (disciplines the three-layer model enforces — #14 hides substrate from LLM); Entry 5 (cadence)

---

## Entry 3 — Four catalogue-track sub-locks explicitly deferred

### 2026-05-16: Four form-bias sub-locks (cipher-width, Foundation layer placement, D1 rubric reconsideration, per-season vocabulary coupling policy) explicitly deferred to catalogue-track empirical gates

**Decision:** Four specific sub-locks within the form-bias work are explicitly deferred to named catalogue-track empirical gates. They are NOT stale; they are NOT lost; they are gate-deferred with named resolution conditions. The strategic-axis lock (Entry 1) and the three-layer model (Entry 2) are structurally independent of these sub-locks — they resolve at their gates and feed into the relevant follow-on dispatches; they do not block the strategic-axis lock or the cadence (Entry 5).

| Sub-lock | Resolves when | Strategic-axis context |
|---|---|---|
| **Cipher-width** (Options A/B/C from the parked canonical-elements thread) | Elrond's emergent-grouping analysis runs against the full Pimen crawl + any additional Tier-1 catalogue sources | Three-layer model per Entry 2. Cipher width is whatever the catalogue's abstraction layer produces; we discover it, we don't pick it. |
| **Foundation layer placement** (Flag B from rocket inventory; `foundation/foundation.py:39-43` hard-codes 4-rotating + 1-physical) | Cipher-width decision + L1/L2 placement decision both land | Foundation either grows with the substrate (cipher-coupled) or decouples (substrate becomes L2 Reincarnated-cosmology concept; Foundation stays as engine-substrate concept). Per `engine-generic-meta-structure.md` three-layer model. |
| **D1 element-name pool reconsideration** | Cipher architecture is determined AND Flag A rubric-screening test runs | The 156-entry pool's allow-list / eligible / quarantine structure may or may not survive cipher migration; reconsideration is much larger than entry-by-entry review (the pool approach itself may not survive). |
| **Per-season vocabulary coupling policy** (α validation-and-regenerate / β in-prompt constraint / γ runtime fallback) | Catalogue-mapping-and-grouping experiment lands findings | Surfaced 2026-05-16 Day 4. Choice depends on empirical mapping behavior of representative per-season vocabulary against catalogue tag space. |

**Two empirical experiments resolve the sub-locks:**

- **Experiment 1 — No-seed cosmology generation test** (`agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md`). Tests residual-bias under cipher migration: after canonical-four labels are hidden from LLM, does the LLM still default-back to fire/water/earth/wind analogs because those patterns are deeply trained-in? Decision it informs: whether Cluster E's migration is sufficient on its own, or whether additional anti-bias scaffolding is required at prompt-construction time. **Runs at Stage 3 gate** (per Entry 5 cadence); not earlier (the test requires cipher migration to be in place to be meaningful).
- **Experiment 2 — Catalogue-mapping-and-grouping experiment** (`agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md`). Tests per-season vocabulary coupling against catalogue tag space; viability of multiple-groupings architecture; D1 rubric humanoid-fantasy screening (Flag A). Decisions it informs: ALL FOUR deferred sub-locks above. **Runs as soon as Matt-authorized budget allows;** sibling to the strategy doc per the parallel-workstream mandate. Currently dispatched to star-lord (`agentic_orchestration/dispatches/2026-05-16-star-lord-catalogue-mapping-experiment.md`).

**Flag A — D1 rubric screening targeted test.** A small sub-experiment of Experiment 2 OR a separate small commission running the D1 rubric's five yes/no scoring questions on a curated set of non-humanoid-cosmology candidate words (e.g., pressure, vacuum, bioluminescence, decay, entropy, resonance, drift, currents). If the rubric reliably under-scores them (Flag A confirmed), the D1 pool reconsideration needs **structural rebuild** not entry-by-entry review. If the rubric scores them as expected (Flag A negated), reconsideration is bounded.

**Reasoning:** Per gandalf's strategy doc § 5.3 + § 6.5. The parallel-workstream mandate (Matt-locked 2026-05-16) requires that VS2b work NOT be blocked on VS2a; deferring these sub-locks until catalogue findings return preserves that parallelism. The strategic-axis lock (Entry 1) and the three-layer model (Entry 2) are designed to absorb all three cipher-width outcomes without revision; the cadence (Entry 5) is designed so these sub-locks resolve at their natural gates inside Stage 3 / Stage 4 without re-opening earlier stages.

**Alternatives considered:**

- **Resolve the sub-locks now (pick cipher-width pre-experiment):** rejected. Premature; catalogue findings have not landed. Locking now invites re-work when findings contradict.
- **Block the strategic-axis lock pending sub-lock resolution:** rejected. Violates Matt's 2026-05-16 parallel-workstream mandate. Sub-locks are structurally independent of the strategic-axis lock; coupling them artificially extends the calendar.
- **Drop the sub-locks (treat as out-of-scope):** rejected. The form-bias work depends on them at Stage 3 / Stage 4 cipher-migration content; ignoring them produces stage-content gaps.

**Cross-seam cascades:**

- **Elrond:** catalogue-abstraction-analysis follow-on dispatch (post Experiment 2) feeds cipher-width + per-season vocabulary coupling.
- **Star-lord:** catalogue-mapping experiment execution (currently dispatched) supplies Experiment 2 data; cipher-migration dispatch at Stage 3 consumes outcome.
- **Rocket:** D1 pool reconsideration dispatch (post Flag A test) is rocket's seam; Foundation layer extension is also rocket's.
- **Gandalf:** strategy-doc amendment lands when Experiment 2 returns (cipher-width resolution; sub-lock 3 + sub-lock 4 final form).
- **Jack-ryan:** future gate reviews should reference this entry — sub-locks are explicitly deferred-not-stale; do not flag downstream dispatches as design-incomplete for not addressing them.

**Status:** Active (sub-locks deferred; gates named).

**Related:**

- `canonical/story/form-bias-cadence-strategy.md` § 5.3 + § 6.5 (authoritative source)
- `agentic_orchestration/gandalf/requests/2026-05-16-catalogue-mapping-and-grouping-experiment.md` (Experiment 2 commission)
- `agentic_orchestration/gandalf/requests/2026-05-16-no-seed-cosmology-generation-test.md` (Experiment 1 commission)
- `agentic_orchestration/dispatches/2026-05-16-star-lord-catalogue-mapping-experiment.md` (current Experiment 2 execution dispatch)
- `agentic_orchestration/dispatches/2026-05-16-elrond-catalogue-structural-pre-inventory.md` (the inventory scaffolding the abstraction analysis operates against)
- Companion entries: Entry 1 (strategic-axis structurally independent of these sub-locks); Entry 2 (three-layer model absorbs all three cipher-width outcomes); Entry 4 (disciplines whose deferred gates these sub-locks land at — esp. #13b outcome-attribution opacity gates the empirical experiments); Entry 5 (cadence threads the sub-lock gates into Stage 3 / Stage 4)

---

## Entry 4 — Disciplines #13a + #13b + #14 codification

### 2026-05-16: Disciplines #13a (implementation-vs-intent drift), #13b (outcome attribution opacity), #14 (internal-vs-generative schema separation) codified into engineering-disciplines.md; terminology lock formalized

**Decision:** Three new engineering disciplines are codified for inclusion in `reincarnated-engine/design/working-agreement/engineering-disciplines.md`, extending the current set of 12 with three additions. Jack-ryan authors the discipline entries themselves per the engineering-disciplines authorship discipline (#1 — math-before-code; #11 — attribution; etc. — knight-rider drafts decision; jack-ryan authors discipline text).

#### Discipline #13a — Implementation-vs-intent drift

**Statement:** Code states X; canonical doc states Y. Observable from code-reading alone. No telemetry needed. No measurement needed. **The code IS the evidence.**

**Why this is a discipline:** doc 37 § 9.1 originally drafted Discipline #13 as a single concept. Per gandalf's strategy doc § 1.3 + § 2.1, the original #13 conflates two distinct patterns and needs splitting. #13a is the half that is actionable through process gates — every code-design interaction can be asked "does this match the canonical doc's intent? if not, is the drift load-bearing?"

**Operational example:** Cluster E in the form-bias work. Doc 37 § 6 specifies canonical-four-hidden-from-LLM; `llm/naming.py:32-35` literally prepends canonical-four to every prompt. The drift is observable from code-reading alone. This is the cleanest drift instance in the project so far.

**Triggerable Gate-1 question:** "Does this dispatch's scope address a canonical-doc-vs-code drift, OR does it introduce one? If the latter, is the drift surfaced explicitly in the dispatch acceptance criteria or MIGRATION.md?"

#### Discipline #13b — Outcome attribution opacity

**Statement:** Per-variable convergence contribution unknown without ablation. This is not "drift" — it is *unmeasured composition*. An epistemic gap, not a behavioral one. **Discipline #13b is not actionable through process gates; it is actionable only through targeted empirical experiments.**

**Why this is a discipline:** the form-bias work surfaced five aggregate convergence-shape observations (per `project_b14_5_sidecar_analyses.md`): hunter modifier range 1.82; fire 23.6% over-representation; convergence-iteration distribution; etc. Each is a CANDIDATE hypothesis for "the engine's structural presupposition causes this." **None have per-variable evidence.** Discipline #13b is the discipline of refusing to make the causal claim without the ablation.

**Operational example:** the terminology lock (per `canonical/story/pre-llm-substrate-inventory.md` § 3). The word *skew* is off-limits until per-variable evidence exists. *Drift* is reserved for code-vs-intent comparisons (Discipline #13a). Cluster B observations under #13b are described as "convergence-shape observations, not attributions."

**Triggerable Gate-1 question:** "Does this dispatch make an outcome-attribution claim about which engine variables produce which observed convergence behavior? If yes, does it cite the ablation evidence supporting the claim — or is the claim acknowledged as hypothesis pending Experiment X?"

#### Discipline #14 — Internal-vs-generative schema separation

**Statement:** Internal data structures (e.g., the canonical-four substrate) must be hidden from LLM-visible surfaces. Per-instance vocabulary fills the LLM-visible slot. The cipher architecture (doc 37 § 6) is the canonical example of this discipline applied to one specific seam.

**Why this is a discipline:** the form-bias work's Cluster E (per strategy doc § 1.1) is the universal LLM-drift surface — every LLM prompt-construction site in the generation seam exposes canonical-four labels (`naming.py:26-36`, `:87`, `:89`; `selector.py:43-47`, `:394-446`; `library_generator.py:85`). The full cipher migration is ahead, not behind. Discipline #14 is the gate that catches NEW drift instances during code review before they ship.

**Operational example:** any future LLM prompt-construction site that re-introduces canonical-four-flavored labels. Discipline #14 enforces: per-instance vocabulary, NOT canonical-four leakage.

**Triggerable Gate-1 question:** "Does this dispatch introduce or modify an LLM prompt-construction site? If yes, does it pass per-instance vocabulary, or does it leak engine-internal schema labels (canonical-four substrate; archetype-tag; gear-slot labels) into the LLM-visible surface?"

### The terminology lock (formalized)

Per gandalf + Matt, 2026-05-16 Day 4:

- **Skew** is off-limits in form-bias work and downstream design until per-variable evidence exists. Skew requires decomposition (how much of observed convergence is attributable to which variable). Use "the engine has a structural presupposition toward X" (claimable from code) or "the convergence shape observed is X" (claimable from telemetry) — never the conjunction.
- **Drift** is reserved for code-vs-intent comparisons (Discipline #13a's narrow legitimate use).
- **Bias** is permissible only when qualified ("the substrate has a structural-presupposition bias toward humanoid X" — i.e., qualified to a structural claim; not an outcome claim). **Unqualified use of "bias" (e.g., "the engine has a bias toward fire") is not permitted; the structural-presupposition or convergence-shape qualifier is load-bearing.**

The terminology lock is operative across all design docs, decisions-log entries, and dispatch authoring going forward.

**Reasoning:** Per gandalf's strategy doc § 1.3 + § 2.1 + the terminology lock derivation in `pre-llm-substrate-inventory.md` § 3. The form-bias work surfaced the discipline-gap because the work itself fell into the gap (re-pasting old framing under new context; conflating structural-presupposition with outcome-attribution). Codifying the disciplines protects against the same gap in all future cross-seam design work.

**Alternatives considered:**

- **Keep #13 as one discipline (original doc 37 § 9.1 draft):** rejected per gandalf's analysis. The single-discipline framing conflates an actionable gate (#13a) with an epistemic stance (#13b); operational triggers diverge.
- **Defer codification pending more drift instances:** rejected. The form-bias work IS the second drift-instance evidence; future similar work (B-series, demo VS2b cascades) needs the disciplines in place at gate-1 time, not retrofit.
- **Discipline #14 as a Cluster E follow-on only (not a general engineering discipline):** rejected. The internal-vs-generative-schema separation pattern is broader than Cluster E; any future LLM-using seam (currently star-lord's prompt-construction; future ones in spirit-guide or elsewhere) needs the discipline.

**Cross-seam cascades:**

- **Jack-ryan:** authors the discipline entries in `engineering-disciplines.md` per ADR-002 documentation pattern. ~1 session of authoring.
- **All seams:** discipline triggers apply at Gate-1 review for any dispatch touching code-vs-canonical-doc fidelity (rocket schemas, star-lord prompts, drax displays).
- **Knight-rider:** future dispatch authoring includes the triggerable Gate-1 questions in the required-reading section where relevant.

**Status:** Active. Engineering-disciplines.md amendment is a jack-ryan follow-on dispatch (small lift; ~1 session).

**Related:**

- `canonical/story/form-bias-cadence-strategy.md` § 1.3 + § 2.1 (analysis source)
- `canonical/story/pre-llm-substrate-inventory.md` § 3 (terminology lock authoritative source)
- 2026-05-08 doc 37 § 9.1 + § 9.2b (original Discipline #13 + #14 candidate drafts; this entry codifies + splits them)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (target file for jack-ryan amendment)
- Companion entries: Entry 1 (strategic-axis decision that exercises these disciplines); Entry 2 (three-layer model that Discipline #14 enforces); Entry 3 (sub-locks whose deferred gates these disciplines enforce at — esp. #13b on the empirical experiments); Entry 5 (cadence stages where #14 enforcement lands)

---

## Entry 5 — Form-bias migration cadence: Option II (Parallelized) locked

### 2026-05-16: Form-bias migration cadence — Option II (Parallelized) locked as the staged sequence; four-stage backbone + per-stage gate definitions

**Decision:** The form-bias work proceeds along a four-stage migration sequence under **Option II (Parallelized)** cadence. All cadence options (I Sequential / II Parallelized / III Aggressive) share the same four-stage backbone; Option II is the recommended cadence based on coordination cost vs calendar trade-off + the strategic-axis lock + the three-layer model + the four deferred sub-locks.

**The critical reframing (per strategy doc § 7):** the cadence work is *staged*, not *paced*. The staging discipline is the load-bearing discipline; the "cadence options" are stage-sequencing choices, not delivery-velocity choices.

### Four-stage backbone (locked across all cadence options)

| Stage | What lands | Seam ownership | Unblocks |
|---|---|---|---|
| **Stage 1** — Add embodiment-axis as new optional field. **No removals.** | Engine emits `embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `class_role_function`, `gear_slot_labels`, `per_season_narrative_modulation` per `embodiment-narrative-layer.md` § "Engine emit requirements". Position C schema migration shape; existing gear schema stays mechanically; embodiment fields are additive. | Rocket dispatch territory. Schema-additive only. MIGRATION.md required. | Demo2 embodiment-aware display work; B-series engine work consuming `embodiment_tag`; kit-anchor rename dispatch scope clarifies. |
| **Stage 2** — Abstract pair-structure (grouping layer) added alongside canonical-four. | Engine emits per-season grouping data (Primary Opposition / Secondary Opposition labels) alongside canonical-four; LLM receives both during transition. Convergence shape compared across the same telemetry frame; "free measurement" of grouping-vs-canonical-four side-by-side. | Rocket + star-lord dispatch territory; schema-additive at engine; prompt-construction-additive at star-lord. | Per-season grouping data available downstream; loadout / drax / Pimen integration can begin consuming the grouping layer; cross-season visual-coverage map computable. |
| **Stage 3** — Hide canonical-four from LLM (cipher migration). | Star-lord dispatch territory. Discipline #14 enforcement at every prompt-construction site. `naming.py`, `selector.py`, `library_generator.py` filtered; per-instance vocabulary replaces canonical-four labels in prompts. Six named drift sites from Cluster E refactored. **Experiment 1 (no-seed cosmology test) runs at this gate.** | Star-lord dispatch territory. | Cipher architecture operationally live; Cluster E drift resolved; Discipline #14 enforced at every prompt site; Experiment 1's residual-bias finding lands. **Stage 4 scope authoring (conditional on Experiment 1 residual-bias result; Stage 4 content differs if bias confirmed vs negated — see strategy doc § 7.1).** |
| **Stage 4+** — Embodiment-as-narrative-skin in display; gear→augmentation rename; consumer cleanup. | Drax dispatch territory primarily; star-lord follow-on for LLM-flavor work. Loadout UI rename (weapon → main-hand-augmentation per active embodiment's L2 vocabulary); demo display per-embodiment lookups; combat-text generation per-embodiment vocabulary. Engine-internal field renames (gear → augmentation; doppelganger → mirror; optional housekeeping per `naming-triad.md` § "Engine-side telemetry retention"). D1 pool reconsideration (post Flag A test result). Trait architecture per-embodiment narrative skin. | Drax + rocket + star-lord. | Full strategic-axis lock has reached every cluster's resolution surface; form-bias work structurally complete; ongoing maintenance is Discipline #13a/#13b/#14 enforcement at gates, not architectural change. |

### Cadence Option II (Parallelized) — the locked choice

Stages 1 + 2 run in parallel after Stage 1 schema work is mid-flight. Stage 3 (cipher migration) starts after Stage 2 lands; Experiment 1 runs at Stage 3 gate. Stage 4 starts after Stage 3 lands. Catalogue-track sub-locks (Entry 3) resolve at their gates; if they land during the migration sequence, their outcomes feed into the relevant stage's content.

**Why Option II over Option I or III (per strategy doc § 7.3):**

- The strategic-axis lock (Entry 1) + the three-layer model (Entry 2) + the four-stage sequence are mature enough to support parallel Stage 1-2 work without ambiguity.
- Stage 3's cipher migration depends on Stage 2's grouping infrastructure but does not require Stage 1's embodiment-axis work to complete (different surfaces).
- The catalogue-mapping experiment's results land at a time that naturally informs Stage 4 (D1 reconsideration; per-season vocabulary coupling final policy), not earlier-stage work.
- Per the parallel-workstream mandate, Option II preserves throughput without inviting the coordination risk of Option III.

**Approximate timeline (per strategy doc § 7.2):** Option II ≈ 5-8 weeks total against current ~9-entity team capacity (per strategy doc § 7.2 body framing of team capacity). Compare Option I (Sequential) ≈ 8-12 weeks (per strategy doc § 7.2); Option III (Aggressive) ≈ 3-5 weeks with elevated mid-stage rework risk (per strategy doc § 7.2).

**Reasoning:** Per gandalf's strategy doc § 7. The four-stage backbone is locked across all cadence options; the cadence choice is the parallelism + sequencing trade-off. Option II is the recommended default because: (a) the strategic-axis lock and three-layer model are mature enough to support parallel Stage 1-2 work; (b) the coordination cost is moderate (rocket + star-lord coordination during Stages 1-2 overlap is small); (c) the calendar window lines up with VS2a's 3-4 month scope and Matt's parallel-workstream mandate. Option III is rejected for elevated rework risk under Experiment 1's residual-bias unknown; Option I is rejected for unnecessary calendar drag.

**Alternatives considered:**

- **Option I (Sequential):** rejected. Lowest coordination cost but longest calendar; demo2 dependencies may slip (Position C migration is Stage 1 prerequisite for demo2 embodiment-aware UI).
- **Option III (Aggressive):** rejected. Shortest calendar but high coordination cost; Experiment 1's results may force re-work if residual-bias confirms; rocket + star-lord + drax simultaneous bandwidth required at a level the current ~9-entity team may not sustain without saturation (per roadmap Risk 1 for drax).
- **Reorder stages (e.g., Stage 3 cipher migration before Stage 2 grouping):** rejected. Stage 3 depends on Stage 2's grouping infrastructure (per strategy doc § 7.1); reversing produces broken dependencies.
- **Combine Stage 3 + Stage 4:** rejected. Experiment 1's residual-bias finding gates Stage 4 content (anti-bias scaffolding if confirmed); combining produces premature Stage 4 commitments.

**Cross-seam cascades (sequencing per Option II):**

- **Rocket:** Stage 1 → Stage 2 → Stage 4. Five follow-on dispatches per strategy doc § 9.1: kit-anchor rename (held release; fires after this entry lands); embodiment-axis emit (Stage 1); pair-structure layer emit (Stage 2); D1 reconsideration (Stage 4, post Flag A test); ailment-damage-signatures (future, re-activated per doc 37 § 6.4 + memory note `project_ailment_damage_thematic.md`).
- **Star-lord:** Stage 2 → Stage 3 → Stage 4. Three follow-on dispatches per § 9.2: per-season cosmological-vocabulary generation (Stage 2); LLM prompt-leak audit + full Cluster E refactor (Stage 3); visual_prompt LLM field per-embodiment narrative skin (Stage 4).
- **Gamora:** Stage 2 → Stage 3-4. Two follow-on dispatches per § 9.3: doppelganger-mode validation under per-season mechanical signatures (Stage 2-3); convergence-framework extension for multi-dimensional divergence (Stage 3-4).
- **Drax:** Stages 1-4 cascade per § 9.4. Display-leak audit (S1-4); loadout/demo/character-sheet consumers updated as `embodiment_tag` flows through; per-season vocabulary display flows (S2-3); body-swap inventory transition UI (S4); per-embodiment visual register coverage (S4).
- **Elrond:** parallel to all stages. Catalogue-mapping experiment supplies the four deferred sub-lock resolutions (per Entry 3); substrate-layer abstraction-analysis dispatch lands post-experiment; outputs land at Stage 4 boundary of main migration.
- **Legolas:** parallel to all stages. Tier-1 full crawls; per-embodiment sprite-coverage commission (a known gap per `style-register.md` § "Per-embodiment register awareness"); follow-on commissions surfaced by catalogue experiment.

**Status:** Active. Stage 1 dispatches authorable now (knight-rider authors rocket embodiment-axis dispatch + kit-anchor rename dispatch release).

**Related:**

- `canonical/story/form-bias-cadence-strategy.md` § 7 (authoritative source for cadence)
- `canonical/story/form-bias-cadence-strategy.md` § 9 (cross-seam cascade source for the dispatch sequencing)
- `canonical/story/embodiment-narrative-layer.md` (Stage 1 + Stage 4 content source)
- `canonical/story/naming-triad.md` (Stage 2 + Stage 3 content source)
- `canonical/16-project-roadmap.md` §VS2b (VS2b workstream coordination)
- Companion entries: Entry 1 (strategic-axis the cadence implements); Entry 2 (three-layer model the cadence builds); Entry 3 (sub-locks the cadence threads through gates); Entry 4 (disciplines the cadence enforces at stages)

---

## Knight-rider notes (NOT for decisions-log; for jack-ryan Gate 1)

Cross-cutting questions for jack-ryan to test in Gate 1:

1. **Entry count justification:** five entries vs fewer (e.g., fold Entry 5 cadence into Entry 1 strategic-axis). My read: distinct entries are right — each is referenced independently by downstream dispatches (rocket dispatches cite Entry 1 + Entry 5; star-lord dispatches cite Entry 2 + Entry 4; jack-ryan future Gate 1 reviews cite Entry 3 + Entry 4). Folding loses the cross-reference cleanliness.
2. **Discipline #13a/#13b split:** Entry 4 splits doc 37 § 9.1's original Discipline #13 candidate into two. Verify the split is durable (operational triggers actually diverge) and not a documentation-only nicety.
3. **Discipline #14 codification scope:** is the discipline genuinely a project-wide engineering discipline, or is it form-bias-specific? My read per strategy doc § 6.4: project-wide (any LLM-using seam needs it). Confirm.
4. **Cross-seam sequencing in Entry 5:** does the Stage 1 → Stage 2 → Stage 3 → Stage 4 dependency chain in Entry 5 hold tightly? Specifically: does Stage 3 actually require Stage 2's grouping infrastructure, or could Stage 3 cipher migration ship before grouping? Strategy doc § 7.1 says it requires; verify.
5. **Terminology lock formalization in Entry 4:** the lock is operative across all design docs going forward. Verify the lock language is precise enough to apply at Gate 1 without judgment-call ambiguity — and that the qualified-permitted "structural-presupposition bias toward X" framing is genuinely permissible (the strategy doc body uses it).
6. **Companion-entry cross-references:** verify each entry's "Companion entries" section is bidirectional (Entry 1 references Entry 2/3/4/5; Entry 2 references Entry 1/3/5; etc.).

If all six pass with no BLOCK, this set is ready for Matt approval and commit.

---

## Drafting note for knight-rider's own future reference

This 5-entry block is the operational payload of gandalf's 751-line strategy doc. Per the strategy doc § 8, knight-rider authored these entries; jack-ryan Gate 1 review confirms before Matt approval. Once approved + committed, the cross-seam dispatch cascade per strategy doc § 9 is the next-phase knight-rider authoring work (≥15 dispatches across rocket / star-lord / gamora / drax / elrond / legolas).
