# Wave-D Engine Spec — DR-lift · Wave-C Fidelity Ledger · Slice-0 Vocab-Loader Repoint

**STATUS:** **DRIFT-CRITIC PASSED — CONCUR-WITH-CORRECTIONS (2026-07-17) — GATE-1 FIRED** (SPEC-AUTHOR complete 2026-07-17; DRIFT-CRITIC independent verification + rulings annex at §11 tail; gate corrections folded in-place pre-build per Wave-C precedent; jack-ryan Gate-1 in flight; **all rulings veto-open at Gate-1 + Matt**.)
**Date:** 2026-07-17
**Author:** gandalf (SPEC-AUTHOR work unit, autonomous atlas-parity run cycle 4 — the LAST engineering wave)
**Authority:** Matt autonomous-run delegation 2026-07-16 (sub-agents iterate engine toward 100% atlas mechanical parity) + S2 census V11 THE SCOREBOARD (`agentic_orchestration/research/curated/atlas/s2-readiness-census-v11-2026-07-17.md`) ranking the final residue tail post-Wave-C-landed. **This spec MINTS NO RULINGS; open questions in §11 route to gandalf-prime DRIFT-CRITIC + jack-ryan Gate-1 for veto-open adjudication.**

**Companion docs:**
- `./wave-c-trigger-mark-engine-spec.md` — the immediate predecessor spec (STATUS discipline · §7.5 DR-collapse-into-LC alternative that Wave-D reopens · §9 byte-neutrality theorem · §11 escalation format · §12 seam routing · Gate-2 MVP-deferral fidelity ledger this spec inherits at §5)
- `./wave-b-economy-engine-spec.md` — Wave-B economy ledger (RS/PC/AM/RC lifts; §7.5 DR-VS-family-adjacency note that flagged DR as thin-roster + not-first-class-RDR-economy; the `_DEFERRED_ECON_BINS` machinery Wave-D inherits at empty)
- `./ailment-layer-engine-spec.md` — canonical-names discipline · fear ailment registry entry Wave-D's §5.a extends at the sim consumer (the flee-AI fidelity item)
- `../../agentic_orchestration/research/curated/atlas/s2-readiness-census-v11-2026-07-17.md` — THE SCOREBOARD (558/564 = 98.94% expressible-now; DR is the last econ bin; Wave-D projection 560/564 = 99.29%)
- `../../agentic_orchestration/research/curated/corpus.db` — DB truth for the 2-kit DR roster (single-writer = elrond; this spec writes ZERO rows)
- `../../agentic_orchestration/legolas/research/megaprobe-2026-07-12/hot-facts.jsonl` (:8) + `.../vs-facts.jsonl` (:17) — the megaprobe facts where DR was assigned to `hot-norseman-frost-avalanche` + `vs-queen-sigma` and where the mech_note verbatims originate ("DR in old vocab = draft/pool-management"; "DR = draft/pre-converged. The build economy is CHOOSING WHAT NOT TO TAKE") — **GATE CORRECTION 2026-07-17 (DRIFT-CRITIC): DR provenance is the 07-12 megaprobe, NOT the econ-recrawl-2026-07-16 application sheet (independent grep: zero hits for either kit in that sheet)**
- `../../agentic_orchestration/jack-ryan/notes/2026-07-17-wave-c-gate2.md` — the Wave-C Gate-2 finding whose CONCUR-with-NOTE deferrals populate Wave-D's §5 fidelity ledger
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/foundation/grouping_vocabulary_loader.py` — the vocab-loader whose `_REL_CANDIDATES` seeks the DISSOLVED `canonical/story/` path (Wave-D slice-0 target)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` — `_DEFERRED_ECON_BINS` frozenset (currently empty post-Wave-C; Wave-D §4 must NOT re-populate it) + `_ECON_BIN_COST_TYPE_MAP`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/resource_economy.py` — 44-field surface post-Wave-C; Wave-D §4 extends only if §11.a rules the drain-bin path (not the collapse path)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_engine.py` — per-tick loop + fear/taunt EXCLUSIVE law (~:1414); §5.a flee-AI steering rides here if landed
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` — curse variant applier :97-126 + LC hp_cost payment; §5.b decrepify movement-composition rides here if landed
- `/Users/admin/Games/reincarnated-engine/config/ailments.yaml` — curse variant enum (:353-390); §5.b extends only at the sim consumer, not the registry

---

## §0 — TL;DR

Wave-D closes the atlas-parity run. **THE HEADLINER is a SLICE-0 hygiene fix** (vocab-loader path drift, ~5 min) that unblocks 4 test files' collection. **THE LEVER is DR (2 kits — the last econ bin)** — census +2, projection **558/564 → 560/564 = 99.29%**, engine-side parity COMPLETE after this wave. **THE QUALITY SURFACE is a Wave-C Gate-2 fidelity ledger** — 4 CONCUR-with-NOTE deferrals adjudicated at expressibility, upgraded to full-fidelity here (fear flee-AI, decrepify movement-composition, orbit 2D sub-projectile motion, placed-lane persistent collider/LOS). **THE LOUD FLAG is at §4/§11.a**: DB truth on the 2 DR kits shows they are **draft/pool-hygiene** economies (roguelite offer-pool investment + VS meta-progression), NOT continuous-drain-while-active. The charge instruction's assumed "drain grammar" is empirically wrong for these kits; §4 states the observed shape and §11.a routes the bin-lift-vs-collapse-vs-defer decision to Gate-1.

**Scope IN (three thrusts):**

| # | Thrust | V11 tail | DB re-verify | Wave-D treatment | Kits |
|---|---|---|---|---|---|
| 0 | **Slice-0 vocab-loader repoint (rocket seam)** | (debt) | (repo hygiene) | Repoint `_REL_CANDIDATES` to post-reorg canonical location or engine-internal | 0 census kits · 4 test-collection files |
| 1 | **DR lift-vs-collapse-vs-defer (econ bin, §11.a ruled)** | 2 | 2 | See §4 + §11.a — SPEC-AUTHOR LEAN (D) DEFER + census-honest, but Gate-1 rules | 2 kits IF lifted OR 0 kits IF deferred |
| 2 | **Wave-C fidelity ledger (a) fear flee-AI (b) decrepify movement-composition (c) orbit 2D motion (d) placed-lane collider/LOS** | (quality; not census) | (4 CONCUR-with-NOTE items from Wave-C Gate-2) | Upgrade MVP → full fidelity | **0 census kits** (all 4 items are FIDELITY, not expressibility — flipping ZERO kits, see §6) |

**Scope OUT (non-goals — stated in §NG):**
- `mechanic:shapeshift` × 3 — Matt-fork-gated GX-02 docket; not Wave-D scope.
- `ailment-wave-c+:unknown-ailment` × 1 (`di-spiritform-druid-pvp`) — Legolas 07-16 sheet unverifiable; source-truth work, not engineering.
- **Any change to `_DEFERRED_ECON_BINS`** — it is currently `frozenset()` post-Wave-C and stays empty. If §11.a rules DR-LIFT, DR routes through the live bin machinery. If §11.a rules DR-DEFER, DR stays blocked but `_DEFERRED_ECON_BINS` does NOT re-populate (the frozenset represents engine-side infeasibility, and DR at 2 kits is a design-scope decision, not an infeasibility).

**Wave-D census math (LOUD; the scoreboard is the truth):**

```
V11 baseline:      558/564 = 98.94%   (post-Wave-C-landed + econ-recrawl-application)
Wave-D IF LIFT DR: 560/564 = 99.29%   (+2 kits, +0.35pp)
Wave-D IF DEFER:   558/564 = 98.94%   (no change; DR stays blocked with econ:DR gap)
Wave-D fidelity:   558/564 = 98.94%   (ZERO census kits from fidelity work; those kits are already expressible)
```

Post-Wave-D, engine-side parity is **COMPLETE**. The remaining 4 blocked kits (shapeshift 3 + unknown-ailment 1) are gated on Matt rulings and source truth, NOT on engineering. No Wave-E is authorized against this spec.

**Design north star:** Wave-B lifted the econ family. Wave-C lifted the trigger family + residue tail. Wave-D **closes the ledger honestly**. If DR is a genuine bin, we lift. If DR is a labeling artifact for two non-drain mechanics (the DB shape says it is), we defer without re-populating `_DEFERRED_ECON_BINS`. The engine's mechanical state either matches the atlas or names the gap; it does not paper over misclassification.

**Byte-neutrality theorem:** Absent new fields, today's behavior is byte-identical (§7). Wave-D introduces zero implicit-default changes; every new field's absence = today's semantics; the DR opt-in clause applies ONLY to the 2-kit roster if §11.a rules LIFT.

**Escalations this doc raises (7 items, count-check §11):**
- (a) **DR bin lift vs collapse-into-LC vs defer** — the load-bearing ruling; DB evidence says the 2 kits are draft/pool-hygiene, not drain.
- (b) DR-vs-LC boundary statement (only meaningful if §11.a rules LIFT).
- (c) Drain tick cadence + interaction with RS reservation floor (only meaningful if §11.a rules LIFT).
- (d) Fidelity ledger placement — Wave-D spec sections vs amendment-riders on Wave-C spec.
- (e) Fear flee-AI steering model — velocity-vector-away vs waypoint-flee vs disengage-timer.
- (f) Orbit motion model — analytic extension (widen N-multiplier) vs simulated sub-projectiles (per-tick position).
- (g) Placed-lane collider scope — persistent collider (blocks entities) vs projectile-LOS occlusion (blocks projectiles only) vs both.
- Vocab-loader Slice-0 target (canonical/reap-die-rise-story/ subfolder vs engine-internal home) — treated as a rocket-seam sub-choice within Thrust 0, NOT an escalation (see §3.3).

---

## §NG — Non-goals (Wave-D explicit exclusions)

- **`mechanic:shapeshift` × 3 kits** (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul) — Matt-fork GX-02 docket OPEN. Wave-D does NOT touch shapeshift emission surface or sim consumer. Same reason as Wave-C §NG: shapeshift redefines `combatant_state` architecture.
- **`ailment-wave-c+:unknown-ailment` × 1 kit** (di-spiritform-druid-pvp) — Legolas 07-16 sheet flagged UNVERIFIABLE (no canonical DI Druid skill named "Spirit Form"; may be a community-coined PVP build label). Source-truth work, elrond re-crawl lane, not engineering.
- **Re-populating `_DEFERRED_ECON_BINS`.** It is `frozenset()` post-Wave-C. Regardless of §11.a's ruling on DR, this frozenset stays empty. Design-scope deferrals are recorded in this spec's §4 + §11.a, NOT in code as engine-side infeasibility markers.
- **New RNG streams.** Zero new rng streams in Wave-D (Discipline #62 companion + §9.2 pattern per Wave-C). Any DR sim consumer (if lifted) is deterministic; any fear-flee steering is deterministic (target-relative vector); any orbit motion is deterministic (parametric time function). Hard-drops return BEFORE any rng draw on all new branches.
- **Wave-E.** No further engineering waves authorized against this spec. If the Matt-fork GX-02 docket rules and shapeshift unblocks, that is a separate wave under separate authorization.

---

## §1 — What already EXISTS (do not rebuild)

Per current engine survey (2026-07-17 pass on Wave-C post-landing state at engine HEAD `941dbbf` — `b850800..HEAD` per Gate-2 finding):

| Component | File | State — for Wave-D purposes |
|---|---|---|
| `_DEFERRED_ECON_BINS` | `bc_target_composer.py:108` | `frozenset()` — empty post-Wave-C. **STAYS EMPTY** regardless of §11.a ruling (see §NG bullet 3). |
| `_ECON_BIN_COST_TYPE_MAP` | `bc_target_composer.py:~236` | 8 active bins post-Wave-C (Wave-B 7 + `damage-taken-converts` + `HP-economy` — both mapped to `["hp"]`). Wave-D §4 IF-LIFT would add `drain` → cost_type map (routing question at §11.a). |
| LC `hp_cost_scale` | `resource_economy.py` + `spatial_engine.py:3447` hard-drop guard | LOCKED `≤ 0.30`. Wave-D §11.a option (C) collapse-into-LC would ride this field with `hp_cost_slope="continuous-drain"` extension — NOT authorized here; §11.a rules. |
| Curse ailment registry | `ailments.yaml:353-390` + `damage_resolver.py:97-126` `_compute_sunder_amp` | 4-variant enum `{amplify, weaken, decrepify, sap}` LOCKED. Curse:amplify composes under `max_amp_cap=0.50` LOCKED. **Curse:decrepify movement-composition site is NOT WIRED** — §5.b fidelity item extends the sim consumer at this file. |
| Fear/taunt EXCLUSIVE law | `damage_resolver.py:1491-1499` (mutual-eviction) + `spatial_engine.py:~1414` (identity refresh loop) | Structurally atomic; Wave-C landed. **Flee-AI itself is NOT WIRED** — mob doesn't visibly flee in single-actor sim; §5.a fidelity item extends the sim consumer. |
| Orbit geometry | `geometry_derivation.py` post-Wave-C + `spatial_engine.py` N-scale analytic collision damage | `orbit_angular_velocity ≤ 4π` LOCKED. MVP is analytic (N-multiplier + collision damage per-tick). **2D sub-projectile motion is NOT WIRED** — §5.c fidelity item routes at §11.f. |
| Placed-lane geometry | `geometry_derivation.py` post-Wave-C + `spatial_engine.py` LOCKED-bound validation | `placed_lane_duration ≤ 15.0` LOCKED. MVP validates duration bound; **persistent collider + projectile-LOS blocking are NOT WIRED** — §5.d fidelity item routes at §11.g. |
| MAX_CHAIN_DEPTH assert | `spatial_engine.py:326` + LOUD-RAISE at :2801 | `MAX_CHAIN_DEPTH=1` LOCKED. Wave-D touches ZERO chain-depth surface (fidelity items are single-hop enhancements). |
| 972-assert QD lattice | `bc_target_cell_sampler.py:395` | LOCKED. Wave-D touches ZERO lattice surface. |
| Byte-neutrality opt-in pattern | Wave-C MAJOR-3 (§9.1 §6+§7 rows in Wave-C spec) | Precedent for Wave-D §7 opt-in clause on any new emission field: existing kits' bytes UNCHANGED; opt-in = the specific roster only (2 DR kits IF lifted). |
| Vocab-loader `_REL_CANDIDATES` | `grouping_vocabulary_loader.py:190-203` | Seeks `canonical/story/historical/` + `canonical/story/` — BOTH DISSOLVED in 2026-07-01 canonical reorg (commit `5fc2890b` swept 98 already-demoted historical docs INCLUDING `grouping-layer-vocabulary.md`). 4 test files fail collection: `test_cosmological_vocabulary.py`, `test_cp8_gear_naming.py`, `test_naming.py`, `test_no_canonical_four_in_llm_prompts.py`. **Wave-D slice-0 target.** |
| Live-runtime consumers of vocab doc | Direct: `llm/naming.py`, `llm/cosmological_vocabulary.py`. Transitive (via cosmological_vocabulary import): `llm/spirit_guide_voice.py`, `export/kit_space_emitter.py`, `generation/kit_space_skill_naming.py`, **`generation/season_generation_pipeline.py` — the emission pipeline itself**. | These read the YAML at boot. Loss of the doc breaks runtime, not just test collection. The doc is a live-runtime dependency, NOT dead reference — Slice-0 must restore or re-home. **GATE CORRECTION 2026-07-17: `season_writer.py` (named in the loader's own docstring at :168) exists only in a stale agent worktree, not main tree — the stale docstring is the claim's source; rocket updates it at slice-0. Dependency set is BROADER than drafted.** |

**Existing extension points (no new subsystems required for Wave-D):**
- DR IF-LIFT = new emission-surface fields on `resource_economy` + new cost_type map entry (`drain → ["hp"]` or similar per §11.a) + new sim consumer at `damage_resolver` (drain-tick branch) OR collapse-into-LC via `hp_cost_slope="continuous-drain"` extension.
- Fear flee-AI = sim consumer extension at `spatial_engine.py` per-tick loop; reads existing fear-marker on defender's `active_effects`; produces target-relative velocity vector.
- Decrepify movement-composition = sim consumer extension at `damage_resolver.py` `_compute_sunder_amp` neighbor + movement-modifier application per-tick.
- Orbit 2D motion = sim consumer extension at `spatial_engine.py` per-tick position update; parametric time-function (deterministic; no rng).
- Placed-lane collider + LOS = sim consumer extension at `spatial_engine.py` collision + projectile-LOS check; per-tick geometric intersection test.
- Vocab-loader repoint = one edit to `_REL_CANDIDATES` in `grouping_vocabulary_loader.py:190-203` + coordinate the doc's new home per §3.3.

---

## §2 — Slice-0: vocab-loader repoint (rocket seam; FIRES FIRST)

### 2.1 Problem statement (verified 2026-07-17)

`grouping_vocabulary_loader.py:190-203` `_REL_CANDIDATES` seeks:
1. `canonical/story/historical/grouping-layer-vocabulary.md` (post-restructure 93b8427)
2. `canonical/story/grouping-layer-vocabulary.md` (pre-restructure fallback)

Both paths DISSOLVED in commit `5fc2890b` "gandalf: reorg Tranche 1b — sweep 98 already-demoted historical docs (git holds lineage)" on 2026-07-01. The doc is git-lineage only; NO on-disk file exists post-reorg. The engine still boots with this loader as a live-runtime dependency (direct: naming.py, cosmological_vocabulary.py; transitive: spirit_guide_voice.py, kit_space_emitter.py, kit_space_skill_naming.py, season_generation_pipeline.py — per §1 gate correction). Current fallback: the loader raises `RuntimeError` UNLESS `GROUPING_VOCAB_DOC_PATH` env-var is set.

**Impact (verified against Wave-C Gate-2 item 10):**
- 4 test files fail COLLECTION: `test_cosmological_vocabulary.py`, `test_cp8_gear_naming.py`, `test_naming.py`, `test_no_canonical_four_in_llm_prompts.py`.
- Fail-mode is at test-collection time (import raises RuntimeError before any test can run), not at test-body time.
- Wave-C Gate-2 §10 logged this as **WARN — LOGGED AS ROCKET-SEAM FOLLOW-UP DEBT** (not fixed at Wave-C per charge instruction; Wave-D fires first).

### 2.2 Wave-D slice-0 acceptance criterion

The 4 test files collect again (no RuntimeError at import time). Equivalent success conditions:
1. `pytest --collect-only tests/test_cosmological_vocabulary.py tests/test_cp8_gear_naming.py tests/test_naming.py tests/test_no_canonical_four_in_llm_prompts.py` exits 0.
2. The vocab-loader `_locate_grouping_vocab_doc()` (or equivalent name; verify at rocket authoring) returns a Path to an existing file on ALL supported hosts + repo layouts.
3. `naming.py`, `cosmological_vocabulary.py`, and the transitive consumer set (§1 gate-corrected row, incl. `season_generation_pipeline.py`) import cleanly with NO env-var override needed on a fresh clone. Loader docstring's stale `season_writer.py` reference updated in the same slice.

### 2.3 SPEC-AUTHOR path recommendation (Gate-1 may prefer alternative)

Two options for the doc's new home. Both are rocket-seam decisions within Thrust 0.

**Option A (RECOMMENDED — engine-internal owned artifact):** Copy the git-lineage doc content (commit `5fc2890b:canonical/story/historical/grouping-layer-vocabulary.md`) into the engine repo at `src/reincarnated/foundation/vocab/grouping-layer-vocabulary.md` (or similar path adjacent to the loader). Update `_REL_CANDIDATES` to seek engine-internal path FIRST + retain the collab path as fallback for backward compat.

- **Pros:** eliminates cross-repo runtime dependency (a live-runtime doc SHOULD live with its runtime consumer per Discipline #13 drift-check); resilient to future canonical-repo reorgs; test-collection self-contained per engine repo.
- **Cons:** requires deciding which repo "owns" the YAML source-of-truth (rocket-seam sub-choice within Thrust 0 per §11 count-check; Gate-1 may elevate to escalation (h) if governance ratification wanted); adds one file to engine repo.

**Option B (fallback — restore to canonical/reap-die-rise-story/):** Restore the doc to `canonical/reap-die-rise-story/historical/grouping-layer-vocabulary.md` (or `canonical/reap-die-rise-story/grouping-layer-vocabulary.md` if the story folder does not gain a historical/ subfolder). Update `_REL_CANDIDATES` to seek `canonical/reap-die-rise-story/historical/` FIRST + retain pre-reorg fallback.

- **Pros:** preserves the "canonical is source-of-truth" model; minimal engine repo touch.
- **Cons:** re-introduces cross-repo runtime dependency; risks recurrence at the next canonical reorg; the 2026-07-01 reorg DELETED this doc for a reason (per commit message: "gandalf: reorg Tranche 1b — sweep 98 already-demoted historical docs"), so restoring it re-litigates that decision.

**SPEC-AUTHOR LEAN: Option A.** Engine-internal ownership matches Discipline #13 (runtime consumer owns its live-runtime data) + resilience to future collab-repo reorgs. Gate-1 may prefer B if canonical-authority policy takes precedence.

### 2.4 Rocket-seam authoring notes

- Fetch content from git-lineage: `git show 5fc2890b:canonical/story/historical/grouping-layer-vocabulary.md > <target-path>`
- Path update at `grouping_vocabulary_loader.py:190-203` — `_REL_CANDIDATES` tuple + the base_dirs tuple as needed (Option A adds engine-repo-relative as a base_dir; Option B keeps collab-repo-relative and updates the relative path).
- Env-var override `GROUPING_VOCAB_DOC_PATH` retained (test isolation contract).
- Fail-loud RuntimeError with `tried` path list retained (Discipline #11 empirical inspection).
- No test-body changes (the 4 tests should pass unchanged once collection succeeds).

---

## §3 — DR thrust (the census lever — 2 kits; SEE §4 + §11.a FOR THE LOAD-BEARING RULING)

### 3.1 Roster (DB-verified, 2 kits)

Per V11 §6 census + corpus.db read-only query at prime:

| kit_id | folk_name | game | econ_status | econ_gaps | economy_model (canon_engine_key) | resource_verbatim (canon_engine_key) | mech_note excerpt |
|---|---|---|---|---|---|---|---|
| `hot-norseman-frost-avalanche` | Frost Avalanche Norseman | hot | `gap` | `["DR"]` | `unknown` | `offer-pool-hygiene (DR — intentional narrow draft path)` | "skip every other ability — off-build upgrades dilute the offer pool = the first explicit documentation of this meta-strategy in the corpus. **DR in old vocab = draft/pool-management.** Norseman class with Frost Avalanche as signature ability." |
| `vs-queen-sigma` | Queen Sigma | vs | `gap` | `["DR"]` | `unknown` | `pre-converged-draft (100% completion unlock + per-level scaling)` | "Pre-converged-draft economy: Queen Sigma IS the convergence — 100% completion IS the draft investment. Per-level scaling (+1% Might, +1% Growth per level) compounds exponentially. 'The character's build is the hundred-percent' per mech_note framing." |

**Atlas keys:**
- hot-norseman-frost-avalanche: `_DMSSI-PLMM-DR-__-~~`
- vs-queen-sigma: `_MHSSI-PSDT-DR-__-~~`

Both kits' engine_key rows carry `econ_meter_type=n/a` — the DR tag does NOT resolve to a meter primitive at engine time.

### 3.2 Prior-wave dispositions (recorded lineage)

- **Wave-B §7.5** (2026-07-16): DR routed to Wave-C with rationale "DR is a VS-family adjacency signal — auto-fire-while-moving with drain-feel is VS-specific; may not survive V3 mechanics-leverage weighting."
- **Wave-C §7.5** (2026-07-17): DR ruled DEFER (pool-content) with alternative "DR folds into LC's `hp_cost_slope` as `escalating` OR `hp_cost_scale × cadence` as a continuous drain. If Gate-1 promotes DR to engine-mechanic path, this is the collapse."
- **Wave-C ruling WC-19** (in wave-c spec §11 tail / §7 body region + Wave-C Gate-1 CONCUR): "LC's 3 are engine-shape (hp-cost + reservation plumbing — PoE Blood Magic / Grim Dawn lineage; `hp_cost_scale ≤ 0.30` LOCK is right). DR's 2 are content-tier drop-rate meta with no engine field owed. `_DEFERRED_ECON_BINS` empties honestly rather than inventing surface for content concerns."

The Wave-C ruling reasoning (**"drop-rate meta with no engine field owed"**) IS ALREADY CONSISTENT with the DB shape observed in §3.1 — but it did NOT explicitly cite the corpus mech_note evidence. This spec surfaces that evidence explicitly.

### 3.3 What the CHARGE INSTRUCTION assumed (and what DB TRUTH says)

The re-fire brief for this spec framed DR as a **"continuous drain-while-active"** mechanic and asked for "the drain grammar — how it differs from LC's bounded per-cast hp cost and from RS reservation." This framing assumes DR is a resource-management-per-tick primitive analogous to PoE1 Blood Rage tick-cost or D2 Iron Wolf mana-drain aura.

**DB truth says the framing is empirically wrong for these 2 kits:**

1. **hot-norseman-frost-avalanche** — HoT (Halls of Torment) offer-pool draft mechanic. The player deliberately narrows their offer pool by skipping certain upgrade offers, so future offers are richer in on-build content. This is a META-progression choice at the DRAFT LAYER, not a runtime resource-consumption cost. The "drain" label is legacy vocabulary for "draft/pool-management" per the mech_note verbatim ("DR in old vocab = draft/pool-management").
2. **vs-queen-sigma** — VS (Vampire Survivors) meta-progression unlock. Queen Sigma is a character whose "build" IS the 100% completion state — the run mechanics amplify with per-level compound scaling (+1% Might, +1% Growth per level). This is not a per-tick HP drain; it is a per-level META-COMPOUND SCALING mechanic.

Neither kit has a per-tick HP-consumption loop. Neither kit's economy is bounded by an ongoing resource-draw. Both kits' "DR" atlas label is a legacy artifact from an earlier vocabulary where DR meant DRAFT-management (roguelite meta-progression), not DRAIN (per-tick resource consumption).

**Consequence for spec authoring:** SPEC-AUTHOR cannot invent a "continuous drain-while-active" bin that matches the atlas label if the DB evidence shows the atlas label is a legacy vocabulary artifact. Doing so would be reverse-engineering a mechanic to match a label rather than reading the label to match the mechanic — the exact anti-pattern Wave-B AC-2 STRIKE precedent forbids (dead code without a consumer). §4 states the observed shapes cleanly; §11.a routes the ruling.

---

## §4 — DR shape: THE OBSERVED EVIDENCE (LOUD; the ruling routes to §11.a)

### 4.1 Observed mechanic-shape summary (from corpus DB + Legolas 07-16 sheet)

- **hot-norseman-frost-avalanche:** DRAFT / POOL-HYGIENE at the offer-selection layer. Not runtime; not resource-per-tick. Genre precedent: HoT / Chrono-Trigger-descendant offer-pool systems; ARPG-lite roguelite meta-progression.
- **vs-queen-sigma:** META-PROGRESSION UNLOCK + per-level compound scaling. Not runtime resource-per-tick; not skill-level bounded cost. Genre precedent: VS unlock-tier characters; roguelite compound-progression.

Neither shape maps to a runtime engine primitive that requires new emission surface. Both are pool-content-level design concerns (roguelite session-level meta rules).

### 4.2 Three routing options (§11.a decides — SPEC-AUTHOR does NOT mint)

**Option (A) — LIFT as new `drain` bin (charge-instruction original intent).** Add `drain` to `_ECON_BIN_COST_TYPE_MAP` with `["hp"]` or `["mana"]`; add per-tick drain fields on `resource_economy` (`drain_rate_per_second`, `drain_source`, `drain_stops_at_hp_percent` runaway-guard); wire sim consumer at `spatial_engine.py` per-tick cost-payment. **Problem: this bin describes a mechanic NEITHER of the 2 kits actually implements.** Building it would be spec speculation — the AC-2 STRIKE precedent (dead code without a consumer at the kit-shape level) applies.

**Option (B) — COLLAPSE into LC as `hp_cost_slope="continuous-drain"`.** Extend Wave-C's LC `hp_cost_slope` enum from `{"flat", "escalating"}` to `{"flat", "escalating", "continuous-drain"}`. Route DR kits' economy through LC's HP-cost machinery with a `cadence_seconds` field naming the tick interval. **Problem (same as A): neither kit's actual shape is a continuous HP-drain-per-tick. Guan Yu spear / Reaper Form Lich (Wave-C LC kits) DO pay HP per cast; hot-norseman / vs-queen-sigma DO NOT pay HP per tick.** Collapse would still mis-model.

**Option (C) — DEFER (SPEC-AUTHOR LEAN, veto-open at §11.a).** DR stays blocked with `econ:DR` gap; census stays at 558/564 = 98.94%. `_DEFERRED_ECON_BINS` STAYS EMPTY (this is a design-scope decision, not an engine-side infeasibility marker). Wave-D's fidelity ledger + slice-0 hygiene are the wave's deliverables; DR is honestly named as post-Wave-D roguelite-meta-progression territory.

- **Sub-option (C.1) — DEFER with re-classification signal to elrond.** Route to elrond re-crawl lane per the "DR = draft/pool-management" evidence surfaced in this spec. If elrond agrees, both kits' `econ_gaps` re-key from `["DR"]` to a corpus-labelled bucket like `["draft-meta"]` or `["session-meta"]` and drop from the census "blocked on econ" bucket entirely (they'd move to a "roguelite meta-progression" OUT lane parallel to `mechanic:shapeshift` and `unknown-ailment`).

- **Sub-option (C.2) — DEFER without re-classification.** Both kits stay `econ:DR` gap-flagged; census shows them as blocked; no elrond touch. Simplest disposition.

### 4.3 DR-vs-LC boundary statement (only meaningful if §11.a rules LIFT or COLLAPSE)

Reserved. IF §11.a rules LIFT (A) or COLLAPSE (B), the boundary is:
- **LC:** per-cast bounded HP cost paid at cast-time (hades1-aspect-guan-yu, le-reaper-form-lich pattern). Discrete event per cast; cost_scale ≤ 0.30 max_hp per event.
- **DR:** would be per-tick continuous HP consumption while some condition holds (this is what the charge-instruction assumed). Continuous event; would need a tick_cadence_seconds + drain_stops_at floor guard.

IF §11.a rules DEFER (C), this section is dead reservation; strike at Gate-1.

### 4.4 Drain tick cadence + interaction with RS reservation floor (only meaningful if §11.a rules LIFT)

Reserved. IF §11.a rules LIFT (A), draft cadence proposal: `drain_cadence_seconds ∈ [0.5, 2.0]`, `drain_stops_at_hp_percent = 0.15` (LOCKED runaway guard — cannot drain below 15% max HP, mirroring PoE Blood Rage self-preservation behavior). Interaction with Wave-B RS reservation floor `0.25·M`: if a kit carries BOTH a DR drain and an RS reservation, the drain floor is `max(drain_stops_at_hp_percent, RS_reservation_floor)` — the kit cannot drain past the reserved cap. Discipline #12 (semantic-shift = additive widening) means Wave-B RS is untouched; DR reads it.

IF §11.a rules DEFER (C), this section is dead reservation; strike at Gate-1.

---

## §5 — Wave-C Gate-2 FIDELITY LEDGER (four CONCUR-with-NOTE items)

**LOUD: These four items are FIDELITY, not expressibility. They flip ZERO census kits.** Wave-C Gate-2 CONCUR-with-NOTE means the kits ARE ALREADY expressible (emit + resolve without error at the expressibility bar). Wave-D upgrades the sim consumers to full-fidelity semantics. The V11 census math is unchanged by any of these four items — see §6.

Four items adjudicated from Wave-C Gate-2 finding (jack-ryan note 2026-07-17-wave-c-gate2.md):
- (a) fear flee-AI movement behavior (Gate-2 §5 row 3 CONCUR-with-NOTE)
- (b) decrepify movement-composition site (Gate-2 §5 row 4 CONCUR)
- (c) orbit 2D sub-projectile motion (Gate-2 §5 row 1 CONCUR)
- (d) placed-lane persistent collider + projectile-LOS blocking (Gate-2 §5 row 2 CONCUR)

### 5.a Fear flee-AI steering (Wave-C ruling WC-17 fidelity extension)

**Baseline:** fear/taunt EXCLUSIVE law is LANDED at `damage_resolver.py:1491-1499` + `spatial_engine.py:~1414`. Mutual-eviction fires BEFORE identity-refresh loop; later-in supersedes earlier-in. Structurally atomic. Wave-C Gate-2 verified this.

**Fidelity gap:** actual flee steering is NOT wired. Mob with `fear` ailment does not visibly flee in single-actor sim — the ailment is registered, EXCLUSIVE law fires, but the mob's per-tick movement vector is unchanged. Low-fidelity outcome (expressibility ✓, presentation ✗).

**Wave-D spec addition (sim-side, no emission-side touch):** at `spatial_engine.py` per-tick loop, IF `defender.active_effects` contains a `fear` ailment marker AND the defender is not carrying a `taunt` marker (EXCLUSIVE law), THEN the defender's per-tick movement vector is set to a target-relative flee vector.

Three model options for the flee vector — GATE-1 rules at §11.e:
- **Model 1 (velocity-vector-away):** flee_vector = normalize(defender.position - fear_applier.position) × fear_flee_speed_percent × defender.base_speed. Simplest; per-tick recompute; smooth flee-away trajectory.
- **Model 2 (waypoint-flee):** at fear application, pick a random point at flee_radius from applier and route defender there via existing waypoint follow. Less compute per-tick; more predictable behavior; risks pathological corner cases (defender pathfinds INTO applier if terrain funnels).
- **Model 3 (disengage-timer):** fear applies a disengage_flag for fear_duration; during flag, defender attempts to break contact + skip attack turn. Behavior-tree-adjacent; captures D2 Terror fidelity; heaviest lift.

**SPEC-AUTHOR LEAN: Model 1 (velocity-vector-away).** Simplest sim consumer; deterministic (no rng); matches D2/D3/D4/Chronicon flee-AI genre-native (per Wave-C ruling WC-17 rationale). LOCKED runaway guards: `fear_flee_speed_percent ∈ [0.5, 1.5]`, `fear_duration_seconds ≤ 6.0`.

**Fields (rocket seam):** zero new emission-side fields (the fear ailment registry entry already carries duration). Sim-side extends `damage_resolver._compute_fear_flee_vector` (new helper, deterministic, no rng draw).

### 5.b Decrepify movement-composition (Wave-C ruling WC-16 fidelity extension)

**Baseline:** curse ailment with `curse_variant` 4-value enum `{amplify, weaken, decrepify, sap}` is LANDED at `ailments.yaml:353-390` + curse:amplify composes under `max_amp_cap=0.50` LOCKED at `damage_resolver.py:97-126`.

**Fidelity gap:** decrepify's movement-modifier composition site is NOT WIRED. The variant emits + parses + registers, but the sim consumer does not compose the movement-speed reduction into the defender's per-tick position update.

**Wave-D spec addition (sim-side, no emission-side touch):** at `damage_resolver.py` (adjacent to `_compute_sunder_amp`), add `_compute_curse_decrepify_movement_reduction(defender) -> float` returning the movement-speed multiplier ∈ [1.0 - reduction_max, 1.0]. Apply at `spatial_engine.py` per-tick movement vector composition. Interaction with fear flee-AI (§5.a) if both apply: multiplicative composition on the flee vector's magnitude.

**LOCKED runaway guards:**
- Curse:decrepify `movement_reduction_max = 0.40` LOCKED (per Wave-C §4.9 DR-classes: "curse:decrepify slow-magnitude capped at 0.40 on bosses (prevents boss immobilization via curse-slow stacking)"). Wave-C §4.9 already spec'd the cap; Wave-D wires the sim consumer.
- Composition with other movement modifiers (chill, root) is MULTIPLICATIVE (not additive) to prevent stacked full-immobilization.

**Fields (rocket seam):** zero new emission-side fields (curse:decrepify's magnitude already emitted at ailment registry). Sim-side extends `damage_resolver._compute_curse_decrepify_movement_reduction` (new helper, deterministic).

### 5.c Orbit 2D sub-projectile motion (Wave-C fidelity item on orbit geometry)

**Baseline:** orbit geometry lands as `geometry_value=orbit` with N-scale analytic collision damage (per-tick multiplier-based damage on entities within orbit path). `orbit_angular_velocity ≤ 4π` LOCKED. Wave-C Gate-2 CONCUR: expressibility ✓ (6 kits emit + validate + damage), fidelity ✗ (no actual per-tick sub-projectile positions computed).

**Fidelity gap:** orbit's sub-projectiles are treated as an aggregate damage-annulus rather than N discrete moving projectiles. Presentation-side would render as N distinct projectiles; sim-side does not track their positions per-tick.

**Wave-D spec addition (sim-side, no emission-side touch):** at `spatial_engine.py` orbit consumer, add per-tick position update for each of N sub-projectiles: `pos_i(t) = anchor + orbit_radius × (cos(ω t + phase_i), sin(ω t + phase_i))` where `phase_i = 2π i / N` for i in [0, N). Per-tick collision check against defender uses discrete sub-projectile positions.

Two model options for the fidelity choice — GATE-1 rules at §11.f:
- **Model 1 (analytic extension):** widen the N-scale analytic multiplier to include a per-tick angular-coverage check (does the defender fall within the orbit-radius annulus at this tick angle?). Damage-side stays analytic; positional side gains fidelity for VFX/telemetry. Lower compute per-tick.
- **Model 2 (simulated sub-projectiles):** track N discrete projectile positions per-tick; damage-check is per-sub-projectile-vs-defender per-tick. Higher compute per-tick (N × ticks); matches PoE1 orbit-skill VFX/damage-timing precedent; risks state-explosion if N is large.

**SPEC-AUTHOR LEAN: Model 1 (analytic extension).** Preserves Wave-C's LOCKED analytic-damage contract + adds positional fidelity for downstream consumers (VFX, telemetry, replay). Model 2 is over-engineering unless the atlas roster grows past 6 kits.

**Fields (rocket seam):** zero new emission-side fields (orbit_radius, orbit_angular_velocity, N already at Wave-C). Sim-side extends `spatial_engine._compute_orbit_position(anchor, radius, omega, phase, t) -> vec2` (new helper, deterministic, no rng).

### 5.d Placed-lane persistent collider + projectile-LOS blocking (Wave-C fidelity item on placed-lane geometry)

**Baseline:** placed-lane geometry lands as `geometry_value=placed-lane` with LOCKED-bound duration validation (`placed_lane_duration ≤ 15.0`). Wave-C Gate-2 CONCUR: expressibility ✓ (3 kits emit + validate), fidelity ✗ (no persistent collider; no projectile-LOS blocking).

**Fidelity gap:** placed-lane is inert geometry — the lane exists in the geometry manifest but does not interact with entities' collision or projectiles' line-of-sight. Wave-C §5.2 stated the LOS-blocking intent verbatim: "placed-lane BLOCKS projectile line-of-sight during duration (walls block projectiles). Defender melee-attack can cross wall (walls are per-projectile blockers, not physical barriers in RDR sim)." Wave-D wires this.

**Wave-D spec addition (sim-side, no emission-side touch):** at `spatial_engine.py` placed-lane consumer, add:
- **Persistent collider (Model A or B per §11.g):** placed-lane geometry blocks entity movement during its duration.
- **Projectile-LOS occlusion:** projectile-vs-placed-lane intersection check per-tick during projectile flight; if lane intersects projectile ray, projectile is destroyed / deflected / passes-through (LOCKED to destroyed for Wave-D per Wave-C §5.2 rationale).

Three scope options — GATE-1 rules at §11.g:
- **Model A (persistent collider only):** blocks entities but NOT projectiles. Simple entity-vs-geometry intersection per-tick. Matches "physical wall" semantics.
- **Model B (projectile-LOS occlusion only):** blocks projectiles but NOT entities. Matches Wave-C §5.2 verbatim intent ("walls are per-projectile blockers, not physical barriers in RDR sim").
- **Model C (both):** blocks entities AND projectiles. Full-wall semantics; over-engineers for a 3-kit roster.

**SPEC-AUTHOR LEAN: Model B (projectile-LOS occlusion only).** Wave-C §5.2 already ruled this verbatim; Wave-D honors the ruling. Model A + C are re-litigations, not fidelity extensions.

**Fields (rocket seam):** zero new emission-side fields (placed_lane_duration + placed_lane_extent already at Wave-C). Sim-side extends `spatial_engine._check_projectile_lane_intersection(projectile, lane) -> bool` (new helper, deterministic geometric check).

### 5.e Fidelity ledger placement — routes to §11.d

**Question:** should the four fidelity items land as Wave-D spec sections (as they do above) OR as amendment-riders on the Wave-C spec (folded into §4.5 / §5.1 / §5.2 / §11 postscript)?

**SPEC-AUTHOR LEAN: Wave-D spec sections (current placement).** Rationale:
- Wave-C is BUILT + LANDED at Gate-2 PASS; amending it re-opens a closed spec.
- Wave-D is an in-flight spec; adding fidelity items is additive to a live document.
- Amendment-riders on Wave-C would violate the "amendments fold in-place ONLY pre-build" pattern (per Wave-C ERRATA/AMENDMENT protocol distinction — Wave-B has ERRATA blockquotes post-build; Wave-C had in-place folds because they landed pre-build).
- Wave-C ERRATA blockquotes post-build ARE possible but expensive; Wave-D sections are cheaper.

Gate-1 rules at §11.d. If Gate-1 prefers Wave-C ERRATA blockquotes, §5.a-§5.d migrate as ERRATA riders on Wave-C spec's respective sections + this §5 becomes a "see Wave-C ERRATA-1..4" pointer.

---

## §6 — Census math (LOUD; the scoreboard tells the truth)

### 6.1 V11 baseline

Per V11 census `s2-readiness-census-v11-2026-07-17.md`:
- Denominator: 564 (519 corpus positives at kit grain + 45 founding roster; phantom `d2-wl-void-rift` set to negative=1)
- Expressible: 558 (98.94%)
- Blocked: 6 (1.06%)

### 6.2 Wave-D projection under each §11.a ruling

**Lever = DR (2 kits), Thrust 1.**

| §11.a ruling | Kits flipped | Post-Wave-D expressible | Post-Wave-D % | Δ vs V11 |
|---|---|---|---|---|
| (A) LIFT drain bin | +2 (both DR kits) | 560 | 99.29% | +0.35pp |
| (B) COLLAPSE into LC | +2 (both DR kits) | 560 | 99.29% | +0.35pp |
| (C) DEFER (SPEC-AUTHOR LEAN) | +0 | 558 | 98.94% | 0.00pp |
| (C.1) DEFER + elrond re-classify (as-drafted: OUT-lane) | +0 to expressible; -2 from denominator | 558 | 100.00% (of 558) | denominator −2 |
| **(C.1-REFINED, DRIFT-CRITIC 2026-07-17)** DEFER engine build + elrond classifies PER-FIGHT econ in landed vocab (NR candidate per vs-phieraggi precedent) | **+2 via data-truth** | **560** | **99.29%** | **+0.35pp; denominator UNCHANGED at 564** |

**Wave-D fidelity ledger (Thrust 2):** flips **ZERO** census kits under every §11.a ruling.
- fear flee-AI: the 4 fear kits are ALREADY expressible (Wave-C Gate-2 §5 row 3 CONCUR); Wave-D upgrades presentation fidelity, no census impact.
- decrepify movement-composition: the curse kits are ALREADY expressible (Wave-C Gate-2 §5 row 4 CONCUR); no census impact.
- orbit 2D motion: the 6 orbit kits are ALREADY expressible (Wave-C Gate-2 §5 row 1 CONCUR); no census impact.
- placed-lane collider/LOS: the 3 placed-lane kits are ALREADY expressible (Wave-C Gate-2 §5 row 2 CONCUR); no census impact.

**Wave-D slice-0 hygiene (Thrust 0):** flips ZERO census kits (repo hygiene, not corpus). Unblocks 4 test files' collection.

### 6.3 Post-Wave-D engine-side parity — COMPLETE regardless of §11.a

Under the SPEC-AUTHOR LEAN (§11.a ruling C = DEFER), post-Wave-D state is:
- 558/564 = 98.94% expressible-now
- 6 blocked kits, all gated on non-engineering paths:
  - shapeshift × 3 (Matt-fork GX-02 docket ruling)
  - econ:DR × 2 (post-Wave-D roguelite-meta-progression territory; re-classify path per §4.2 sub-option C.1)
  - unknown-ailment × 1 (source-truth work at Legolas re-crawl lane)

Under (A) or (B), post-Wave-D state is:
- 560/564 = 99.29% expressible-now
- 4 blocked kits: shapeshift × 3 + unknown-ailment × 1 (all non-engineering)

**Either way: no further engineering waves are authorized against this scoreboard.** The residual blocked tail is Matt-decision-gated + source-truth-gated. Wave-D is the last engineering wave.

### 6.4 What Wave-D DOES NOT lift

- Any kit not in the V11 blocked tail (all 558 expressible kits were already expressible pre-Wave-D).
- Any kit in the shapeshift bucket (Matt-fork gated).
- The 1 unknown-ailment kit (source-truth gated).
- Any V11 corpus row already at expressible-now status (Wave-D touches ZERO emission bytes for those kits — the byte-neutrality theorem §7 preserves this).

---

## §7 — Byte-neutrality theorem

**Theorem.** Absent any new Wave-D emission field, Wave-D code changes produce byte-identical outputs vs pre-Wave-D engine state on all existing seeds and all existing kits. Equivalently: the "default corner" of Wave-D behavior IS today's behavior.

### 7.1 Per-section neutrality checks

| Wave-D section | New default value | Absence-behavior | Byte-neutral? |
|---|---|---|---|
| §2 Slice-0 vocab-loader repoint | (no emission surface — code-path/data-doc only) | vocab-loader now finds the doc; naming.py etc. produce same YAML at boot. **Test collection: 4 tests now COLLECT (state change); 4 tests' test-body outputs unchanged (they were failing collection, so their runtime output was never generated).** **YES for emission bytes; test-collection state changes from "fail-collect" to "collect-ok" — this is the intended fix, not a regression.** |
| §4 DR IF-LIFT (Option A) | (only meaningful under §11.a ruling A) | If §11.a rules DEFER (C): NO new fields; NO composer changes; NO sim changes; byte-identical. **YES under (C).** IF §11.a rules LIFT (A): new `drain_rate_per_second=0.0` / `drain_source=null` / `drain_stops_at_hp_percent=0.15` defaults on `resource_economy`; existing kits' fields stay at defaults; only the 2 DR kits opt-in per §4.2 roster. **Emission-side opt-in clause (Wave-C MAJOR-3 pattern): no existing kit's `econ_bin` field takes the newly-lifted `drain` value at Wave-D landing — opt-in per rocket authoring on the 2-kit §3.1 roster only.** **YES under (A).** |
| §4 DR IF-COLLAPSE (Option B) | (only meaningful under §11.a ruling B) | If §11.a rules DEFER (C): NO change to `hp_cost_slope` enum. IF §11.a rules COLLAPSE (B): `hp_cost_slope` enum widens `{"flat", "escalating"}` → `{"flat", "escalating", "continuous-drain"}`; new default stays `"flat"`; existing LC kits' `hp_cost_slope` stays `"flat"` (Wave-C default). **YES under (B).** |
| §5.a Fear flee-AI | (sim-side only; no new emission fields) | Sim consumer added; existing kits' emission bytes unchanged. Sim behavior change: the 4 fear kits' defenders now flee visibly. **Sim behavior IS a fidelity change; byte-neutrality is for emission bytes, not sim behavior — see §7.2 for the sim-behavior discipline.** **YES for emission bytes.** |
| §5.b Decrepify movement-composition | (sim-side only; no new emission fields) | Same as §5.a: sim consumer added; emission bytes unchanged. **YES for emission bytes.** |
| §5.c Orbit 2D motion (Model 1 analytic extension) | (sim-side only; no new emission fields) | Same: sim consumer added; emission bytes unchanged. IF §11.f rules Model 2, that's a state-tracking addition per-sub-projectile; still sim-side only. **YES for emission bytes under any §11.f ruling.** |
| §5.d Placed-lane LOS occlusion (Model B) | (sim-side only; no new emission fields) | Same: sim consumer added; emission bytes unchanged. IF §11.g rules Model A or C, still sim-side only. **YES for emission bytes under any §11.g ruling.** |

### 7.2 Sim-behavior IS a fidelity change (LOUD distinction)

The byte-neutrality theorem covers **emission bytes** (what rocket writes to the substrate registry) — those stay byte-identical for existing kits. The theorem does NOT cover **sim behavior** — Wave-D's §5.a-§5.d fidelity items DO change sim behavior for the affected kits (a fear-marked defender flees; a decrepify-cursed defender moves slower; orbit sub-projectiles trace paths; placed-lanes occlude projectiles). This IS the intended change — expressibility ✓ → fidelity ✓. Downstream analytics that snapshot sim behavior will observe the fidelity change; downstream analytics that snapshot emission bytes will observe byte-neutrality.

### 7.3 Opt-in clause (Wave-C MAJOR-3 pattern; applies to §4 IF-LIFT or IF-COLLAPSE)

If §11.a rules LIFT (A) OR COLLAPSE (B): the Wave-C MAJOR-3 opt-in pattern applies to Wave-D §4 fields — no existing kit's `econ_bin` field takes the newly-lifted `drain` value at Wave-D landing; opt-in per rocket authoring on the 2-kit §3.1 roster only (hot-norseman-frost-avalanche + vs-queen-sigma). If §11.a rules DEFER (C): the opt-in clause is moot (no new field to opt into).

---

## §8 — Cross-bin interaction contracts (with Wave-A + Wave-B + Wave-C)

**IF §11.a rules DEFER (C) — the SPEC-AUTHOR LEAN:** this section is REDUCED to fidelity-item interactions only (§8.2, §8.3 apply; §8.1 is dead reservation).

### 8.1 DR × Wave-C LC composition (only meaningful IF §11.a rules LIFT or COLLAPSE)

Reserved. IF §11.a rules LIFT (A): a kit CAN carry both DR bin (drain-per-tick) and NOT a LC bin (per-cast HP cost) — the two bins are exclusive at the primary econ_bin field per Wave-B §5.3 single-bin-per-kit contract. IF §11.a rules COLLAPSE (B): the LC bin's `hp_cost_slope="continuous-drain"` sub-shape IS the DR path; no separate bin exists. IF §11.a rules DEFER (C): section is moot.

### 8.2 Fear flee-AI × decrepify movement-composition (§5.a × §5.b interaction)

If BOTH fear AND curse:decrepify are applied to the same defender: flee vector's magnitude multiplied by decrepify movement-reduction. Multiplicative composition (NOT additive) prevents pathological stack-immobilization. Example: flee_speed_percent=1.0 (nominal) × (1 - decrepify_reduction=0.40) = 0.60 effective flee speed. Fear/taunt EXCLUSIVE law still applies at ailment layer.

### 8.3 Orbit motion × placed-lane occlusion (§5.c × §5.d interaction)

If an orbit sub-projectile's per-tick position crosses a placed-lane's occlusion zone: projectile destroyed / passes-through per §5.d Model. Under §11.g Model B (LOS occlusion only, SPEC-AUTHOR LEAN): projectile destroyed. This is CONSISTENT with Wave-C §5.2 verbatim intent.

---

## §9 — Seam routing (rocket vs gamora slice split + sequencing)

### 9.1 rocket slice (emission / config / enum widen / vocab-loader / no sim change)

| Wave-D section | rocket surface changes |
|---|---|
| §2 Slice-0 vocab-loader | `grouping_vocabulary_loader.py` `_REL_CANDIDATES` + base_dirs repoint per §2.3 Option A OR B; git-lineage fetch of doc content; if Option A, place doc adjacent to loader in engine repo |
| §4 DR (IF §11.a rules LIFT) | `resource_economy.py` +3 keys (drain_rate_per_second, drain_source, drain_stops_at_hp_percent); `bc_target_composer._ECON_BIN_COST_TYPE_MAP["drain"] = [<cost_type per §11.b>]`; ECON_BINS enum-widen +`drain` |
| §4 DR (IF §11.a rules COLLAPSE) | `resource_economy.py` `hp_cost_slope` enum widen +`continuous-drain`; +1 key `drain_cadence_seconds` (LC-shared); no new bin in composer |
| §4 DR (IF §11.a rules DEFER) | ZERO emission-side changes |
| §5.a-§5.d Fidelity items | ZERO emission-side changes (all sim-side; rocket does not touch) |

### 9.2 gamora slice (sim consumers only; no emission-side touch)

| Wave-D section | gamora sim consumer changes |
|---|---|
| §2 Slice-0 vocab-loader | ZERO (rocket-only) |
| §4 DR (IF §11.a rules LIFT) | `damage_resolver` OR `spatial_engine` per-tick drain-cost payment branch; hard-drop guard IF hp < stops_at floor BEFORE any rng draw |
| §4 DR (IF §11.a rules COLLAPSE) | Extend Wave-C LC hp_cost_slope consumer at `spatial_engine.py:3447` to include `continuous-drain` branch |
| §4 DR (IF §11.a rules DEFER) | ZERO sim-side changes |
| §5.a Fear flee-AI | `spatial_engine` per-tick flee-vector composition on fear-marked defenders (§5.a Model 1 SPEC-AUTHOR LEAN); `damage_resolver._compute_fear_flee_vector` new helper |
| §5.b Decrepify movement | `damage_resolver._compute_curse_decrepify_movement_reduction` new helper; `spatial_engine` per-tick movement composition |
| §5.c Orbit motion | `spatial_engine._compute_orbit_position` new helper (§5.c Model 1 SPEC-AUTHOR LEAN); per-tick angular-coverage check widen |
| §5.d Placed-lane LOS | `spatial_engine._check_projectile_lane_intersection` new helper (§5.d Model B SPEC-AUTHOR LEAN); per-tick projectile-vs-lane intersection check |

### 9.3 Sequencing (soft rendezvous rocket-first; slice-0 fires standalone)

1. **Slice-0 (rocket, standalone):** vocab-loader repoint fires FIRST + independently. Success criterion = 4 test files collect. No downstream dependency.
2. **Rocket slice (IF §11.a rules LIFT or COLLAPSE):** emission-side landing per §9.1. Rocket signals gamora at completion (per Discipline #62 parallel-same-tree pattern — pathspec-only staging).
3. **Gamora slice:** sim consumers per §9.2. Soft rendezvous rocket-first (Wave-C pattern) — gamora can begin fidelity item work in parallel with rocket's slice-0 + §4 work since fidelity items don't touch rocket's surface.

### 9.4 Independence of fidelity items from §11.a ruling

The 4 fidelity items (§5.a-§5.d) are INDEPENDENT of §11.a ruling. Gate-1 can rule (C) DEFER on DR AND still authorize gamora to land the fidelity items. Slice-0 + fidelity items combined = a complete Wave-D even if DR defers.

---

## §10 — Math notes (in-spec sketches; LOCKED invariants named)

**Discipline #1 (math-before-code):** the sim consumers named in §5 have LOCKED runaway guards inline. Rocket / gamora authors math notes at `src/reincarnated/simulation/math/wave-d-*.md` per Wave-C precedent before code lands.

### 10.1 Fear flee-AI Model 1 velocity vector

```
Given: defender.position ∈ ℝ², applier.position ∈ ℝ² (fear source),
       defender.base_speed ∈ ℝ⁺, fear_flee_speed_percent ∈ [0.5, 1.5] (LOCKED range)

flee_direction = normalize(defender.position - applier.position)  # unit vector away from applier
flee_speed = defender.base_speed × fear_flee_speed_percent
per_tick_movement = flee_direction × flee_speed × dt

# Composition with §5.b decrepify (multiplicative):
IF curse:decrepify on defender:
    per_tick_movement *= (1 - curse_decrepify_movement_reduction)  # ≤ 0.40 LOCKED
```

**LOCKED invariant:** flee_speed cannot exceed `1.5 × base_speed` (LOCKED runaway guard — no fear-flee sprint exceeding base movement by more than 50%). Cannot fall below `0.5 × base_speed` (LOCKED — flee is still flee; even under maximum decrepify composition, defender still moves).

### 10.2 Orbit 2D motion Model 1 analytic extension

```
Given: anchor ∈ ℝ² (orbit center), orbit_radius ∈ ℝ⁺,
       omega ∈ [0, 4π] (LOCKED range per Wave-C),
       N ∈ ℤ⁺ (sub-projectile count),
       t ∈ ℝ⁺ (time since orbit start)

For sub-projectile i ∈ [0, N):
    phase_i = 2π i / N
    pos_i(t) = anchor + orbit_radius × (cos(omega × t + phase_i), sin(omega × t + phase_i))

Analytic angular-coverage check:
    defender_angle_from_anchor = atan2(defender.position.y - anchor.y,
                                       defender.position.x - anchor.x)
    coverage_arc_half_width = arcsin(defender.hitbox_radius / orbit_radius)  # small-angle for typical scales
    IF ∃ i ∈ [0, N): |defender_angle_from_anchor - (omega × t + phase_i)| < coverage_arc_half_width (mod 2π):
        damage_hit(defender)
```

**LOCKED invariants:** `omega ≤ 4π` (Wave-C); `orbit_radius ≥ defender.hitbox_radius` (LOCKED — orbit smaller than hitbox is degenerate and defaults to sing-hit damage-annulus). Deterministic — no rng draws.

### 10.3 Placed-lane LOS occlusion Model B

```
Given: lane geometry (segment endpoints A, B ∈ ℝ²),
       projectile ray (origin O, direction d, ∈ ℝ²),
       lane_duration ≤ 15.0 (Wave-C LOCKED)

Ray-segment intersection test per-tick during projectile flight:
    t_ray = ray parameter of intersection
    t_seg = segment parameter of intersection
    IF 0 ≤ t_ray ≤ projectile.remaining_range AND 0 ≤ t_seg ≤ 1:
        projectile destroyed (Wave-C §5.2 verbatim intent)
```

**LOCKED invariants:** lane duration ≤ 15s (Wave-C); projectile destruction is deterministic (no rng). Composition with orbit (§8.3): if orbit sub-projectile ray crosses lane, sub-projectile destroyed.

### 10.4 DR (IF §11.a rules LIFT) drain-tick cost payment

```
Given: applier.hp ∈ ℝ⁺, applier.max_hp ∈ ℝ⁺,
       drain_rate_per_second ∈ ℝ⁺, drain_cadence_seconds ∈ [0.5, 2.0] (LOCKED range),
       drain_stops_at_hp_percent = 0.15 (LOCKED runaway guard)

Per-tick check (dt in seconds):
    tick_cost = drain_rate_per_second × dt × applier.max_hp
    hp_after_tick = applier.hp - tick_cost
    IF hp_after_tick / applier.max_hp < drain_stops_at_hp_percent:
        # LOCKED hard-drop: refuses to drain past floor
        # (mirrors PoE Blood Rage self-preservation)
        drain suspended this tick; DR effect flag cleared
    ELSE:
        applier.hp = hp_after_tick
```

**LOCKED invariants:** `drain_stops_at_hp_percent = 0.15`; drain-tick cost cannot exceed `drain_rate_per_second × dt × max_hp` per tick (bounded by rate); hard-drop returns BEFORE any rng call (Discipline zero-new-RNG). Only meaningful IF §11.a rules LIFT.

---

## §11 — ESCALATIONS (contested design calls — Gate-1 rules; SPEC-AUTHOR states leans)

**Seven items. SPEC-AUTHOR LEAN stated. Gandalf-prime DRIFT-CRITIC + jack-ryan Gate-1 rule ELICIT-don't-IMPOSE; Matt veto-open. SPEC-AUTHOR does NOT mint rulings here.**

### (a) DR bin lift vs collapse-into-LC vs defer — THE LOAD-BEARING RULING

- **Options:** (A) LIFT as new `drain` bin per §4.2 Option A; (B) COLLAPSE into LC via `hp_cost_slope="continuous-drain"` per §4.2 Option B; (C) DEFER per §4.2 Option C (SPEC-AUTHOR LEAN). Sub-options (C.1) DEFER with elrond re-classification signal; (C.2) DEFER without re-classification.
- **Tradeoffs:** (A) builds a new bin whose semantics MATCH the charge-instruction assumption but DO NOT match the DB shape of the 2 kits — DB shows draft/pool-hygiene, not per-tick drain. Building (A) is authoring a bin without a consumer at the kit-shape level; Wave-B AC-2 STRIKE precedent applies (dead code without a consumer). (B) has the same mis-match problem in a different shape. (C) preserves census-honesty; `_DEFERRED_ECON_BINS` stays empty; the "engine-side parity complete" claim is HONEST at 558/564 = 98.94% rather than PADDED at 560/564 by faking a bin that describes neither kit.
- **Genre precedent:** PoE1 Blood Rage IS a genuine per-tick HP drain (would be a legitimate DR kit); D2 Iron Wolf mana-drain aura IS one; neither of THESE 2 kits is. HoT / VS pool-content mechanics are meta-progression territory (D3 Kanai's Cube, D4 Paragon glyphs — closer analogs than combat resource drains).
- **DB evidence (LOUD):** hot-norseman-frost-avalanche mech_note: "DR in old vocab = draft/pool-management"; vs-queen-sigma mech_note: "Pre-converged-draft economy: Queen Sigma IS the convergence — 100% completion IS the draft investment." Neither kit's raw_json contains a per-tick HP-consumption loop. See §3.1 + §4.1.
- **SPEC-AUTHOR LEAN: (C) DEFER (specifically C.1 with elrond re-classify signal).** Preserves census-honesty; matches DB shape; consistent with Wave-C ruling WC-19 rationale ("no engine field owed"); `_DEFERRED_ECON_BINS` stays empty (Wave-D non-goal §NG bullet 3). LOUD to Gate-1: this ruling makes Wave-D flip ZERO census kits from DR — the wave's deliverable is slice-0 hygiene + fidelity ledger + census-honest defer, NOT a padded 99.29%.

### (b) DR-vs-LC boundary statement — ONLY MEANINGFUL IF §11.a RULES LIFT OR COLLAPSE

- **Options:** (I) DR = per-tick continuous HP consumption while condition holds (charge-instruction assumption); (II) DR = per-cast bounded HP cost with a continuation flag (subset of LC's per-cast semantics with a cadence); (III) not applicable (§11.a rules DEFER).
- **Tradeoffs:** (I) is clean but requires the DB kits to actually implement per-tick drain (they don't per §4.1). (II) is a hair-splitting variant of LC's semantics that adds field surface for no shape-fit gain. (III) is coherent under (C).
- **SPEC-AUTHOR LEAN: (III) not applicable** given SPEC-AUTHOR LEAN on (a). IF Gate-1 rules (a)=LIFT or (a)=COLLAPSE, then (I) is the cleaner boundary. §4.3 is the reservation.

### (c) Drain tick cadence + interaction with RS reservation floor — ONLY MEANINGFUL IF §11.a RULES LIFT

- **Options:** (I) drain_cadence_seconds ∈ [0.5, 2.0] with drain_stops_at_hp_percent = 0.15 LOCKED; (II) drain_cadence_seconds ∈ [0.25, 1.0] with drain_stops_at_hp_percent = 0.10 LOCKED; (III) not applicable (§11.a rules DEFER or COLLAPSE).
- **Tradeoffs:** (I) matches PoE Blood Rage cadence and self-preservation floor; (II) is faster + steeper drain but risks the boss-fight-immobilization edge cases Wave-C §4.9 DR-classes warned against for curse:decrepify.
- **RS floor interaction:** IF DR + RS on same kit, drain floor is `max(drain_stops_at_hp_percent, RS_reservation_floor 0.25·M)` — drain cannot exceed the reserved cap.
- **SPEC-AUTHOR LEAN: (III) not applicable** given (a) SPEC-AUTHOR LEAN. IF Gate-1 rules (a)=LIFT, then (I) is the LEAN. §4.4 is the reservation.

### (d) Fidelity ledger placement — Wave-D spec sections vs Wave-C ERRATA riders

- **Options:** (1) fidelity items land as Wave-D §5 sections (current placement, SPEC-AUTHOR LEAN); (2) fidelity items land as Wave-C ERRATA blockquote riders on Wave-C spec's §4.5 / §5.1 / §5.2 / §11 postscript; (3) hybrid — fidelity items land in Wave-D §5 with cross-references INTO Wave-C's respective sections.
- **Tradeoffs:** (1) preserves Wave-C-is-closed principle; keeps Wave-D as the in-flight document; matches Wave-C AMENDMENT protocol (in-place folds ONLY pre-build). (2) re-opens a closed spec + violates the Wave-B ERRATA-vs-AMENDMENT distinction (ERRATA blockquotes are for post-build errata, and Wave-D isn't errata on Wave-C — it's forward continuation). (3) is a compromise but doubles the citation surface.
- **SPEC-AUTHOR LEAN: (1) Wave-D §5 sections.** Preserves Wave-C-is-closed; keeps ERRATA for genuine post-build errata (rather than forward-fidelity continuation).

### (e) Fear flee-AI steering model — velocity-vector vs waypoint vs disengage-timer

- **Options:** (1) velocity-vector-away per §5.a Model 1; (2) waypoint-flee per §5.a Model 2; (3) disengage-timer per §5.a Model 3.
- **Tradeoffs:** (1) simplest sim consumer; deterministic per-tick recompute; matches D2/D3/D4/Chronicon flee-AI genre precedent (Wave-C WC-17 rationale). (2) less compute per-tick + risks pathological corner cases. (3) heaviest lift + captures D2 Terror behavior fidelity + behavior-tree-adjacent.
- **Genre precedent:** D2 Terror = flee (Model 1); D3 Feared status = flee (Model 1); D4 Fear ailment = flee + panic actions (Model 3-adjacent); Chronicon = flee (Model 1).
- **SPEC-AUTHOR LEAN: (1) velocity-vector-away (Model 1).** Simplest + genre-native + matches Wave-C WC-17 SPEC-AUTHOR LEAN. §5.a + §10.1 are the reservations.

### (f) Orbit motion model — analytic extension vs simulated sub-projectiles

- **Options:** (1) analytic extension per §5.c Model 1; (2) simulated sub-projectiles per §5.c Model 2.
- **Tradeoffs:** (1) preserves Wave-C's LOCKED analytic-damage contract + adds positional fidelity for VFX/telemetry; lower per-tick compute; matches Wave-C damage-check semantics. (2) full per-tick per-sub-projectile state tracking; matches PoE1 orbit-skill VFX/damage-timing precedent; higher compute; risks state-explosion.
- **Genre precedent (amended at DRIFT-CRITIC — Herald of Ice is not an orbit skill):** **D2 Hurricane is the canonical analytic orbit** (aggregate pulse damage in radius, zero discrete sub-projectiles, shipped that way for 20+ years); D3 Storm Armor arc/orbit is simulated per-arc; D4 Frozen Orb sub-projectiles are simulated. Roughly split by genre; Diablo-lineage's longest-lived orbit is analytic.
- **SPEC-AUTHOR LEAN: (1) analytic extension (Model 1).** Preserves Wave-C damage contract + adds positional fidelity for downstream consumers; §5.c + §10.2 are the reservations.

### (g) Placed-lane collider scope — persistent collider vs LOS occlusion vs both

- **Options:** (A) persistent collider only per §5.d Model A; (B) projectile-LOS occlusion only per §5.d Model B; (C) both per §5.d Model C.
- **Tradeoffs:** (A) blocks entities but not projectiles — physical-wall semantics. (B) blocks projectiles but not entities — matches Wave-C §5.2 verbatim intent ("walls are per-projectile blockers, not physical barriers in RDR sim"). (C) full-wall semantics; over-engineers for 3-kit roster; contradicts Wave-C §5.2 verbatim.
- **Genre precedent:** PoE1 Frost Wall = LOS occlusion (B); D3 Waller affix = physical collider (A); D4 Wall skills = both (C). RDR's Wave-C §5.2 already ruled B verbatim.
- **SPEC-AUTHOR LEAN: (B) LOS occlusion only.** Wave-C §5.2 already ruled this; Wave-D honors the ruling. §5.d + §10.3 are the reservations.

**Count-check: 7 escalation items (a–g). Matches §0 TL;DR. The vocab-loader target sub-choice (A/B in §2.3) is TREATED AS a rocket-seam authoring decision within Thrust 0, NOT an escalation; if Gate-1 wants to elevate it, it becomes escalation (h).**

---

### DRIFT-CRITIC RULINGS — 2026-07-17 (gandalf-prime; ALL veto-open at Gate-1 + Matt)

**Verdict: CONCUR-WITH-CORRECTIONS.** Independent verification performed at prime before ruling: (i) DB truth re-derived for both DR kits (`econ_meter_type=n/a` + `economy_model=unknown` both; mech_note verbatims confirmed in `canon_corpus` AND traced to origin in megaprobe-07-12 facts); (ii) vocab-doc deletion confirmed (`D canonical/story/historical/grouping-layer-vocabulary.md` at `5fc2890b`; no live-tree copy; `_REL_CANDIDATES` seeks exactly the two dissolved paths); (iii) consumer set re-derived (BROADER than drafted — season_generation_pipeline.py transitive; stale `season_writer.py` name traced to loader docstring :168). **The drafter's refutation of the charge-instruction's "continuous drain-while-active" framing is UPHELD — the charge was wrong, the spec is right.** Corrections folded in-place pre-build (Wave-C precedent): DR-provenance citation (§ header + §12), consumer-set rows (§1, §2.1, §2.2), §2.3 governance pointer, §11.f precedent line, §6.2 C.1-REFINED row.

- **(a) DR — CONCUR (C), REFINED to C.1-REFINED.** DEFER all engine build: no drain bin (A), no LC collapse (B). Neither kit has a per-fight resource loop — building either option is authoring a mechanic to satisfy a label, the AC-2 STRIKE anti-pattern; WC-19's "no engine field owed" is STRENGTHENED by the new evidence, not reopened. **Refinement on the re-classify signal:** do NOT presume the as-drafted OUT-lane/denominator-drop. The void-rift denominator adjustment was principled (phantom kit — the skill does not exist); these are REAL kits with real per-fight behavior and belong in the denominator as EXPRESSIBLE. Charge elrond to classify the PER-FIGHT economy in landed vocab from existing megaprobe facts. **Evidence-indicated candidate: `NR`** — both kits are survivor-genre auto-fire (`movement.verbs=auto-fire-while-moving`; "avalanche fires on cooldown" / VS auto-swing), and the **vs-phieraggi precedent (econ-recrawl-2026-07-17: NR ruled for VS auto-fire, "genre-typical for VS / bullet-heavens generally")** is the same genre + same shape. The draft-meta shape (offer-pool-hygiene / pre-converged-draft) records as a **descriptor overlay** — the SS form-lock precedent from the same batch ("descriptive lineage / gx metadata, not a bin"). Census consequence IF elrond lands NR: **560/564 = 99.29% via data-truth, denominator UNCHANGED.** Fallback = C.2 (stay blocked, census-honest at 558/564) if the per-fight econ won't land in landed vocab — elrond's classification authority, not presumed here. Elrond eval FIRED IN PARALLEL with Gate-1: it is data-truth classification, not build; useful under every ruling; reversible by documented UPDATE; corpus single-writer free.
- **(b) — CONCUR (III) not-applicable** under (a). §4.3 stands as dead reservation; Gate-1 strikes or keeps.
- **(c) — CONCUR (III) not-applicable** under (a). §4.4 same.
- **(d) — CONCUR (1) Wave-D §5 sections.** Wave-C is closed at Gate-2 PASS; ERRATA blockquotes are for post-build errata, not forward continuation. Correct house-protocol reading.
- **(e) — CONCUR (1) Model 1 velocity-vector-away.** Genre-native (D2 Terror, D3 Fear, Chronicon all flee-away); deterministic; waypoint-flee (2) reads as a pathing bug half the time in genre practice (funnel-into-applier corner case named in §5.a is real); disengage-timer (3) over-engineers a single-actor sim.
- **(f) — CONCUR (1) analytic extension.** Stands on the Wave-C-LOCKED-analytic-damage-contract ground alone; the amended D2 Hurricane precedent (20+ years shipped analytic) reinforces. Model 2 is over-engineering at a 6-kit roster.
- **(g) — CONCUR (B) LOS occlusion only.** Wave-C §5.2 ruled it verbatim; (A)/(C) are re-litigations, not fidelity extensions.
- **Slice-0 target — CONCUR Option A (engine-internal home), speaking as the agent who deleted the doc at `5fc2890b`:** the deletion was correct canon-lifecycle (the doc was demoted-historical); the DEFECT was an engine live-runtime dependency on a collab-repo canon-lifecycle artifact — the loader's own docstring documents the fragility ("self-heals if gandalf relocates the doc"). Option B re-couples engine boot to every future canon reorg. Engine owns its runtime data (Discipline #13); the collab git-lineage copy remains the historical record; CANON-STEWARD raises no objection because the YAML was never live canon — it is runtime data that happened to live in a canon doc. Remains a rocket-seam sub-choice; not elevated to (h).

---

## §12 — Cross-references

**Sibling specs consulted (pattern + house model):**
- `./wave-c-trigger-mark-engine-spec.md` — STATUS discipline · escalation format · byte-neutrality theorem · fidelity ledger origin (Gate-2 CONCUR-with-NOTE)
- `./wave-b-economy-engine-spec.md` — `_DEFERRED_ECON_BINS` machinery precedent · DR-VS-family-adjacency §7.5 note (the empirical seed Wave-D re-cites at §4)
- `./ailment-layer-engine-spec.md` — fear/curse ailment registry (Wave-D §5.a-§5.b extend consumers, not registry)

**Substrate evidence:**
- `../../agentic_orchestration/research/curated/atlas/s2-readiness-census-v11-2026-07-17.md` — the scoreboard
- `../../agentic_orchestration/research/curated/corpus.db` — DB truth (raw_json + notes + flags + canon_engine_key for both DR kits)
- `../../agentic_orchestration/legolas/research/megaprobe-2026-07-12/hot-facts.jsonl` (:8) + `.../vs-facts.jsonl` (:17) — where DR was assigned + mech_note verbatims originate (GATE CORRECTION 2026-07-17; Wave-D re-reads at §4)
- `../../agentic_orchestration/legolas/research/econ-recrawl-2026-07-17/00-index.md` — the vs-phieraggi NR precedent + SS form-lock descriptor-overlay precedent cited by the DRIFT-CRITIC §11.a refinement

**Engine code touched or referenced:**
- `src/reincarnated/foundation/grouping_vocabulary_loader.py:190-203` — slice-0 target
- `src/reincarnated/generation/bc_target_composer.py:108, ~236` — `_DEFERRED_ECON_BINS` + cost_type map
- `src/reincarnated/generation/resource_economy.py` — emission surface (only touched IF §11.a rules LIFT or COLLAPSE)
- `src/reincarnated/simulation/spatial_engine.py` — per-tick loop + fear/taunt EXCLUSIVE law + orbit + placed-lane consumers
- `src/reincarnated/simulation/damage_resolver.py:97-126, :1491-1499, :3447` — curse variant + fear/taunt mutual-eviction + LC hp_cost payment
- `config/ailments.yaml:353-390` — curse variant enum (Wave-D §5.b extends sim consumer, not registry)

**Gate finding notes:**
- `agentic_orchestration/jack-ryan/notes/2026-07-17-wave-c-gate2.md` — the four CONCUR-with-NOTE deferrals Wave-D §5 upgrades

**Tags anticipated at Wave-D landing:**
- `rocket/v2.12-waved-1` — slice-0 vocab-loader repoint (standalone)
- `rocket/v2.12-waved-2` — §4 DR IF-LIFT emission surface (skipped IF §11.a rules DEFER)
- `gamora/v1.11-waved-1..N` — §5 fidelity ledger sim consumers (independent of §11.a ruling)

---

## Tracker-delta

**Canonical current-to-end-state impact:**

- `canonical/current-to-end-state/current-to-end-state-engine.md`: Wave-D IN-FLIGHT once Gate-1 PASS; delivers (i) slice-0 vocab-loader repoint, (ii) DR ruling per §11.a, (iii) 4-item fidelity ledger extending Wave-C sim consumers. Post-Wave-D-landed: engine-side atlas parity COMPLETE. Residual blocked tail (shapeshift 3 + unknown-ailment 1) is non-engineering (Matt-fork gated + source-truth gated).
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md`: post-Wave-D-landed, S5 corpus→engine migration re-opens for any DR kits IF §11.a rules LIFT/COLLAPSE (+2 kits) or the fidelity items' 15 kits (fear 4 + curse 4 + orbit 6 + placed-lane 3 + fear/curse overlap corrections) — the 15 fidelity kits' emission bytes UNCHANGED (byte-neutrality theorem §7), so their S5 migration is UNCHANGED from Wave-C post-landing state; only sim behavior gains fidelity. IF §11.a rules DEFER: only slice-0's 4 test files rewire — no substrate migration surface owed.
- `canonical/matt_decision_needed/`: **queue an entry** for §11.a (DR bin lift vs collapse vs defer — the load-bearing ruling; SPEC-AUTHOR LEAN (C) DEFER; Gate-1 stress-tests + Matt veto-open). Also queue §11.d (fidelity ledger placement; SPEC-AUTHOR LEAN Wave-D §5 sections) if governance wants ratification. The five remaining escalations (b/c/e/f/g) are gandalf-prime + jack-ryan Gate-1 rulings under Matt autonomous-run authority per Wave-C precedent — NOT Matt-gated unless a party elevates.

**Doc-lifecycle:**
- STATUS starts as DRAFT — GATE-1 NOT YET FIRED. On Gate-1 PASS: STATUS → GATE-1 PASSED — BUILD-AUTHORIZED (Wave-C precedent).
- No prior spec is superseded (Wave-D is forward continuation; Wave-B / Wave-C stay CURRENT).
- ERRATA blockquotes reserved for post-build errata (per Wave-B / Wave-C convention); pre-build amendments fold in-place.

**Decisions-log entries anticipated (jack-ryan writes at Gate-1):**
- Wave-D Gate-1 verdict + §11.a ruling disposition + fidelity ledger placement ruling.
- IF a discipline candidate surfaces at Gate-1 or Gate-2 (Wave-C precedent: parallel-same-tree hygiene became Discipline #62), a separate entry.

**Cross-agent signals:**
- **elrond signal (IF §11.a rules C.1):** re-classify DR from `econ:DR` bucket to `roguelite-meta-progression` bucket or equivalent; both kits move to OUT lane parallel to shapeshift + unknown-ailment.
- **jack-ryan Gate-1 signal:** stress-test §11.a evidence base (DB mech_notes cited verbatim in §3.1 + §4.1); verify no census-math error in §6.2; verify byte-neutrality theorem §7 covers all opt-in / no-opt-in cases; verify fidelity ledger placement matches Wave-C ERRATA-vs-AMENDMENT protocol.
- **gandalf-prime DRIFT-CRITIC signal:** rule on §11.a-g (verdict stamp per Wave-C precedent); rulings veto-open; Matt gates at read.

---

**End of Wave-D spec (2026-07-17).**
