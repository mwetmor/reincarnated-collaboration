# Current State → End State (LIVING)

**STATUS:** LIVING CANONICAL — the single consolidated current-vs-end-state tracker. **Every gandalf session opens this at session-start (OP § 1) and updates it during work (OP § 5).** Not a dated snapshot; a continuously-maintained instrument carried forward until both completion targets close.
**Steward:** gandalf (story-and-design steward). Updates: any gandalf session; sub-agent gandalf proposes, steady-state gandalf commits.
**Purpose:** for the game we are building (the v2 ARPG-build-depth + roguelite-descent loop), hold in ONE place: (I) what the **battle sim** currently IS and where it must go, (II) what the **content-emission pipeline** currently IS and where it must go, (III) the **engine-fit gaps the v2 design opens** (the new material), and (IV) the **owner map + forward queue**. This is the artifact every subsequent session plans from.
**Method:** reconciled against disk with file:line evidence. Provenance tags distinguish `[gandalf-verified]` (looked myself this lineage) from `[fit-audit]` (Explore-pass file:line, 2026-06-23) from `[design-doc]` (claim from the v2 design doc, not yet code-verified).
**Supersedes:** `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` (the dated spine) and `agentic_orchestration/gandalf/notes/2026-06-18-pipeline-completion-progression-memo.md` (the wind-down memo). Those remain as lineage; where they conflict with this doc, **this governs**. The B-series / P-series detail there is not re-reproduced in full — pointers below.
**End-state authority:** `canonical/reap-die-rise-story/gameplay-loop-design.md` (v2 canonical gameplay loop, END-STATE AUTHORITY) + `canonical/reap-die-rise-engine/performance-target-specs.md` (Godot density/perf targets, PERF AUTHORITY) + `canonical/reap-die-rise-engine/design-decisions-session.md` (§§2-13 systems decisions; §1 patron sketch superseded). The full v2 set + supersession map: `canonical/reap-die-rise-story/spec-index.md`. This doc tracks the engine's distance to THAT end state. *(Path A re-home 2026-06-29 — the v2 docs left `matt_notes_handoff_docs/` for `canonical/reap-die-rise/`; the `reincarnated-` prefix was dropped under the new title.)*
**Survey-mode discipline:** within each PART, *Current state* subsections are descriptive (what IS, cited). *End state* / *The gap* subsections are forward judgment (what should be / what's wrong). Kept structurally separate per the cross-cutting rule.

---

## HOW THIS DOC WORKS (living-doc protocol)

1. **Open at startup.** OP § 1 names this as a mandatory session-start read. Read the SESSION-DELTA LOG top-to-bottom first (latest governs), then the body PARTs relevant to the session's work.
2. **Prepend a SESSION-DELTA.** Each session that changes state adds a dated block at the TOP of the SESSION-DELTA LOG. **The latest delta governs all blocks and body sections below it** where they conflict (same pattern as the predecessor memo).
3. **Update the body in place.** When a state table row changes (a gap closes, a blocker clears, a new gap surfaces), edit the row AND note it in the session's delta. Never silently delete — strike with `~~...~~` + date, or move to a "closed" line, so lineage is legible.
4. **Mark completion.** When an item closes, mark it `✓ DONE (date, commit)`. When BOTH completion targets (battle-sim + emission) close AND the v2-fit gaps are dispositioned, this doc retires to historical.

---

## SESSION-DELTA LOG (latest governs all below)

### 2026-06-30 — Spec-doc GAP registered: the kit-space EMISSION architecture (§3.2/§3.3/§3.4) is LIVE but design-doc-homeless (its founding doc is being retired by the isekai purge)

The story-side purge (Matt "all v1 isekai story is gone") targeted `story/2026-06-02-season-archive-realm-expansion-pivot.md` for deletion. **Verify-then-prune HALTED it** — that doc is the **canonical commitment behind a LIVE engine subsystem**, with 8+ inbound code/data refs. Deletion is now **held** (partial-supersession banner on the doc; isekai content-model struck, engine spine preserved). Registered here so the live-behavior-vs-spec GAP is not lost:

- **§3.2 per-skill flavor-or-canonical naming** (WS1A.4-lite Q18 binary: flavor-word vs. canonical name) → `generation/kit_space_skill_naming.py`, `generation/phase5_skill_naming.py`, `llm/ws1a4_lite_flavor_judgment.py` (emits `ws1a4_flavor_decision`/`ws1a4_flavor_word_used`).
- **§3.3 continuous kit-space *emission* architecture** — stable kit-ids, **per-kit-entry output schema (NOT per-season-manifest)** → `data/kit_space/README.md`, `export/kit_space_emitter.py`.
- **§3.4 kit-space-expansion chronicle** → `data/kit_space/chronicle/CHRONICLE_SCHEMA.md` (+ live chronicle data).
- **§6 existing-season-data historical preservation** (Path α) → governs `seasons/season_000001…000200` on disk.

All **frame-neutral** (survive the isekai kill) and **NOT documented in the v2 engine spec** (`reap-die-rise-engine/` has no kit-space/chronicle/emission-schema section). This is a **build-to-spec GAP** (live subsystem, no spec home; the only design-intent home is the doc being retired + code comments pointing *at* it — e.g. `ws1a4_lite_flavor_judgment.py:5`, `kit_space_emitter.py:80`).

**OPEN ENGINE QUESTION (gates the fold + the founding doc's final deletion) — belongs in PART II (content-emission):** is the §3.3/§3.4 kit-space+chronicle emission model **still the live-v2 emission architecture, or superseded by the cycle-14 unified Godot-bundle emitter** (PART II.1 "two emit tracks that do not meet")? **If live** → author a kit-space/emission section in `reap-die-rise-engine/`, fold §3.2/§3.3/§3.4/§6, re-point the engine code comments, THEN the story-side can `git-rm` the doc. **If superseded** → §3.3/§3.4 retire by an *engine-supersession* call (star-lord/rocket + this tracker), not the isekai ruling. Owners: star-lord (emission) + rocket (kit-space gen). Routed to KR for sequencing when the purge reaches the engine spine. No engine code touched this session.

---

### 2026-06-30 — Doc-lifecycle governance system LANDED · `02-roadmap`→this-tracker rehome (all OPs/SKILLs) · perception-asymmetry build-vs-spec GAP registered · ravine prototype CANCELLED (cross-seam Q carries)

**Governance (Matt 4-part authorization: *"write up the doc, do the OP rehome, stand up the audit routine, run the verify-then-prune."*)** The doc-lifecycle governance system is installed at `agentic_orchestration/operating-procedures/canonical-doc-format.md § 6` (+ its mirror SKILL): total-vs-partial supersession (partial→banner+fold, never amputate; total→git-rm); the **4-predicate prune-safe rule** (markdown + not-never-prune + [totally-superseded OR workstream-closed working-memory] + zero references across **both** repos); three note sub-classes (evidentiary / verdict / working-memory); the standing **§ 6.6 hygiene Routine**. Ratified via a 14-scenario stress-test (`gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md` — evidentiary). The hygiene Routine is SPEC-READY but instantiation is **BLOCKED on a registered CCR environment** (`operating-procedures/canonical-hygiene-audit-routine.md`).

**Rehome — THIS doc is now the project-wide engine-delta pointer.** All **9 agent OPs + 9 SKILLs** swung session-start read #3 from the retired `canonical/02-roadmap.md` → `canonical/current-to-end-state/current-to-end-state-engine.md` (this doc). Seam owners now surface a `Tracker-delta:` to gandalf/KR (who own tracker writes) when their work opens/closes a gap.

**NEW build-vs-spec GAP registered (surfaced by the verify-then-prune sweep; no-deferral discipline):** *perception-asymmetry (player-favoring near-miss; two-layer model) is designed + foundation-built + demo-wired + telemetry-schema'd, but **NOT wired into the spatial sim** — `spatial_engine.py` does not consume it and `AOECastEvent` has no producer.* Locked constants + a registered prediction exist (`gandalf/notes/2026-06-15-gamora-brief-perception-asymmetry-sim-wiring.md`). This is a **GAP-TO-CLOSE, not an accepted deferral**; it belongs in PART I (sim gaps) when worked; owners gamora (sim) + star-lord (telemetry producer); routed to KR for sequencing.

**Verify-then-prune (item 4) — RAN; SAFE TIER EMPTY, nothing deleted, nothing pushed.** The 4-predicate rule + cross-repo reference check + **read-verify** found zero auto-prunable notes (the filename-class heuristic failed **9/9** on read — design-steward "coordination" notes embed load-bearing reasoning). 113 of 153 notes are evidentiary (the citation graph protected them); 33 surface for Matt's ratification (`gandalf/notes/2026-06-30-verify-then-prune-first-run-prune-list.md`).

**Ravine Godot prototype CANCELLED (Matt 2026-06-30); learnings PROMOTED.** Cross-seam open Q carries and **gates the seasonal-descent § 5 adjustment algorithm:** *does physical room-resizing feed the balance sim?* — the 28×28 vestigial-removal recognition (balance-sim sizes arenas for **FIGHT MATH**; ARPG rooms by **GENRE CONVENTION**). If gamora's sim models SPACE (kiting / LoS / AoE-overlap) → room-resize shifts balance; if spatially ABSTRACT → presentation-only. Route to KR/gamora. Full carry-forward: `gandalf/notes/2026-06-30-ravine-cancelled-learnings-carry-forward.md`.

**What did NOT move:** engine code (zero); PARTs I–II battle-sim / emission state unchanged except the new perception-asymmetry GAP registration above. Governance/process + one gap-registration + reorg-pointer-rewire only.

**Signed:** gandalf, 2026-06-30 (doc-lifecycle governance + rehome + perception-asymmetry GAP + verify-then-prune first-run + ravine cancellation).

---

### 2026-06-30 — Frame refinement: spirit guide RETIRED (function splits 3-way A/B/C), god≠demigod corrected, Flag #6 banter-owner RULED → hub NPC ensemble; `canonical/dead/` purged

**Cosmology corrected + refined (Matt 2026-06-30).** Two corrections compose:

1. **god ≠ demigod.** Earlier reconciliation artifacts conflated the **patron god** (Daikoku/Mahakala) with the **demigod-jailer**. Matt: *"the patron deity is most definitely not a demigod. It is a god. The demigod is the jailer."* Corrected across all frame docs.
2. **The spirit guide is RETIRED** — *not re-labeled.* Matt: *"The spirit guide is actually just gone. The function of the spirit guide is replaced in two ways: (A) by the demigod instructor during the tutorial; (B) by the death god's voice, seldom heard but can offer guidance."* The warm future-self advisor is **removed as an entity**; its advisory function splits two ways:
   - **(A)** the **demigod-jailer** (built the cage, barred from the god, selects/steers the player) → the **tutorial instructor**;
   - **(B)** the caged **death-god / patron Daikoku/Mahakala** → a voice **seldom heard but able to offer guidance** (the rare, unreadable §19.3 communion).

**Flag #6 — banter / retort-axis owner RULED (Matt 2026-06-30): the HUB NPC ENSEMBLE (the third split-corner, C).** The loop-doc (`gameplay-loop-design.md` §§14-16) had made the **patron** the chatty antagonistic-helpful banter companion + defiance↔devotion retort axis. Matt **rejected the premise** that the axis needs a single chatty voice at the shoulder: *"the banter-relationship was never one voice; it's an ensemble in the hub — the Hades model."* **Ruling:** the daily banter + defiance↔devotion axis belongs to the **hub NPC ensemble** (Rita + the cult's human faces), which IS the cult-standing economy (§23.5) given a voice — defiance↔devotion expressed through **actions** (hand-in vs. hoard §23.4), judged by the hub's NPCs. So the spirit-guide function splits **three** ways, not two: **(A)** demigod = tutorial + punctuated Mercer-mentor key beats; **(B)** death-god = rare unreadable Rorschach (§19.3); **(C)** hub ensemble = daily relationship/banter. gandalf's prior demigod-lean was WRONG (carried the rejected premise); Matt's wins on four counts (Mercer-reveal dilution, tonal collision, double-coding doesn't scale, Rorschach-better-for-defiance). **PROPAGATED** to loop-doc §§2c/14/15/16/21/22. **Engine consequence: none yet** — the §435 LLM-vs-templated tech decision is now scoped to hub-NPC banter. Full write-up: flag-memo Flag #6 + `00-index.md` §5.

**Propagation done (Matt directive #1 + Flag #6 ruling).** "Spirit guide RETIRED → 3-way split (A demigod / B death-god / C hub ensemble)" propagated across: this tracker (0.2 Frame row + III.9), `00-ground-state.md`, `reap-die-rise-story/spec-index.md` (intro + supersession map + §5), the four story-frame banners (avatar-projection, companion-as-Hall, earth-avatar-cosmograph, cosmograph-pivot), and — for the banter ruling — `gameplay-loop-design.md` §§2c/14/15/16/21/22 (the END-STATE AUTHORITY loop doc; §2c carries the consolidated ruling note + four reasons) + flag-memo Flags #6/#3/#5. III.9 below carries the corrected model.

**Path B (Matt directive #3) — `canonical/dead/` purged.** Emptied via `git rm` of its single tracked file `37-form-bias-diagnosis-and-recovery.md` (40,765 bytes; recoverable from git history). First concrete step of the broader canonical purge.

**Canonical REORG begun (Matt-agreed 2026-06-30).** Target = **3 folders**: `reap-die-rise-story/`, `reap-die-rise-engine/`, `current-to-end-state/{…-story, …-engine}`; heavy `00-ground-state.md` registry retires to a thin router stub; strategy = **(b) heavyweight-fold** (distill pertinent content into a tight spec, delete sources). **Tranche 1 FIRED** (commits a813cec + 5fc2890): 13 live clean-kills (Cluster A/B process + superseded + companion-inversion + 02-roadmap + 48-class-roster) + 98 already-demoted historical docs swept. Working set now **83 live `story/` + 15 top-level**; only `reap-die-rise/` + `story/` subdirs remain. **This tracker is itself slated to become `current-to-end-state/current-to-end-state-engine.md`** in Tranche 2 (structural skeleton). Full worklist + per-doc dispositions: `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md`. Companion-inversion doc killed *with* its S2-companion OPEN investigation preserved in companion-as-Hall §7 (sharpens Flag #4).

**What did NOT move:** engine code (zero); the battle-sim / emission state (PARTs I–II unchanged); flags **#2** (run-persistence contract) + **#4** (molt→run-trigger) still queued for Matt. *(Flags #3 + #5 RESOLVED as consequences of the #6 ruling — see flag-memo.)* Design-canon refinement + propagation + reorg-Tranche-1 only.

**Signed:** gandalf, 2026-06-30 (frame refinement + spirit-guide-retired 3-way propagation + Flag #6 banter ruling + canonical reorg Tranche 1).

---

### 2026-06-29 — Path A integration: the v2 canonical set re-homed (`canonical/reap-die-rise/`), game retitled **Reap. Die. Rise.**, patron precisely sourced, PART III sharpened by the live systems decisions

**This session integrated the 9-doc v2 design set Matt handed over** (authored across mobile sessions to 2026-06-29) and **re-registered the game's title from "Reincarnated" → "Reap. Die. Rise."** The docs left `matt_notes_handoff_docs/` for `canonical/reap-die-rise/` (the `reincarnated-` prefix dropped); the **supersession map + naming lexicon live in `canonical/reap-die-rise-story/spec-index.md`**, which governs the v2 set's internal chronology. The end-state-authority pointers (header + PART 0.1) now point at the new homes. **This delta governs the body below where they conflict.**

**What the integration establishes (load-bearing):**

1. **Naming locked** (per `00-index.md` §1 / `story-keystone.md` §18): display **Reap. Die. Rise.** (periods) · product/URL slug **reapdierise** · repo/file slug **reap-die-rise** · motto *Mete. Morere. Resurge.* · world **the Necroverse** · contested-utopia **Pax** · terminal states **Necropolis → Necrocosm**. Forward gandalf artifacts use these.

2. **The patron is now precisely sourced — and the EARLIEST sketch is dead.** Patron = **Daikoku** (Seven Lucky Gods / Shichifukujin), root **Mahakala** — a death/destruction power wearing the mask of luck; **hijacked benign fortune-deity** whose soul-feeding produces a hollow, will-draining peace (peace-as-lobotomy). This **supersedes `design-decisions-session.md` §1's Ereshkigal/Nergal "original sealed death-deity" sketch** — that section is the earliest patron pass and is **dead; do not cite it** (`story-expansion.md:177` states the shift outright). PART III.9 below is updated to this sourcing.
   - **BUT §1's device-layer is orphaned, not automatically dead** — the **trickster-jab** ("you're just a minor luck-spirit," needling the sealed/diminished wound), the **layered crackable-alias + authored-slow true-name** device, the **seven-gated descent as floor-structure**, and **descent ≠ underworld aesthetic** are *mechanisms* that survive the sourcing swap and in several cases fit **Daikoku/Mahakala better** (a death-power literally masked as a luck-god makes the "you're just a minor luck-spirit" jab cut at the *real* wound). **These need re-homing-or-retiring rulings (task #4 / Matt) — do not silently amputate them with the Ereshkigal sourcing.**

3. **III.1 (kit-vs-kit matchup-temperature) gains a concrete substrate + a probabilistic dimension.** `design-decisions-session.md` §4 confirms the gandalf-lean resolution and sharpens it: screen at the **~24×24 QD-grouping matchup matrix** (the 20-24 "classes," ~400-576 inspectable cells — **not** an unwieldy 400-kit matrix); type relationships (AoE > summon/proxy, single-target > AoE, melee/close vs ranged/kite) are a **[MEASURE] prior derived from sim data, NOT asserted**; use the matrix as a **Goldilocks generation-constraint (safety envelope guaranteeing ≥1 winnable matchup), NOT for withholding kits**. §5 adds: **matchup type = (grouping + capstone-state), and the matrix is PROBABILISTIC** — the ~1/3 conversion-capstone inversions move a kit across the matrix, so Goldilocks safety is a **confidence, not a guarantee**, with the **portal escape-valve as the backstop**. [MEASURE] the inversion **probability masses** (the matrix-as-distribution needs the weights). Folded into III.1 below.

4. **III.2 (per-kit level model) is made TRACTABLE.** `design-decisions-session.md` §12: do **not** re-run the whole season's in-band filtering at every stage (combinatorial explosion) — validate the **staging LOGIC** (stat curves, skill-unlock order, gear-scaling function) keeps a **representative grouping-level sample in-band across ~4-6 checkpoint milestones (1→50)**, fixing systematic outliers at the generator level. **Skill-unlock is the lumpy axis** (discrete, ordered → non-monotonic in-band-ness: fine@20, broken@30, fine@40) — spend the sim budget there. This converts III.2 from "substantial net-new" to "bounded checkpoint-validation." Folded into III.2 below.

5. **III.4 (the "400" scale) is RESOLVED — my refutation is ratified with a concrete derivation.** `design-decisions-session.md` §3: **launch ~100 fully-distinct kits; architect for 400+; "launch lean, grow endless."** Derive the count as `min(marketing-floor, production-ceiling, distinctiveness-ceiling)` — marketing-floor **saturates at ~100** (100 vs 400 read identically as "impossibly many"; past 100 helps retention not acquisition); production-ceiling is **[MEASURE] per-kit hours** (the likely binding wall for a solo dev — depends on library+config vs hand-build); distinctiveness-ceiling says **300-sharp beats 400-with-80-reskins** (a samey kit is *evidence against* the hook). The real hook is the **generative engine** (the *capacity*); the launch count just proves it's real. III.4 below updated from "400 illustrative" to "launch-~100 / architect-400+, count-derived."

6. **NEW engine demand surfaced — gear-as-sim-variable (III.8 amended).** `design-decisions-session.md` §7: **gear is pushed INTO the battle sim** — kits are validated **as geared units**, gear a **treatment variable** the sim tunes/measures, via `express_gear(power_level, kit) → balanced affixes` (called both for looting and for possession-transform — the same operation). "Balanced across all stages" is a **claim to VALIDATE via generate→sim→check-in-band, not a formula to assume.** **CRITICAL sawtooth-guard (a hard design invariant the sim must respect):** gear-affix scaling is by **stage of the game (itemization), NOT content-difficulty scaling by the player's live power — the Oblivion treadmill is forbidden.** Test every scaling instinct: content *fixed by depth* (✓ player rises to meet it) vs *dynamic by player power* (✗ treadmill).

7. **Scope confirmations folded in:** **co-op is CUT** (§9 — preserves the solo vision; protects scope; PVP, not co-op, is the team-gated post-launch capstone); **PVP is level-50-only, post-launch** (§8 — one bracket dissolves player-scaling/twink/fragmentation at once); the engine **scales monsters, not players** (§9), which *aligns with* the sim's existing fixed-L50 validation rather than fighting it.

**Open contradiction surfaced for Matt (Path A flag #2 — `00-index.md` §5):** `gameplay-loop-design.md` §8 keeps the **lieutenant-becoming as a persistent gain (+3, "you keep what you kill")** but §23.3 states the **champion-body is NOT kept at run-end.** *What banks across the roguelite reset — the becoming/identity, or nothing of the body?* Likely intent: the **roster/grimoire entry** (the record of who you became) banks; the **run-specific embodied power** resets. The two sections read in tension — **Matt should rule the exact persistence contract before the III.2 per-kit-level model is specced against it.** Added to the forward queue.

**What did NOT move:** the content-emission plumbing (PART II two-tracks-don't-meet) — zero movement; still rocket/star-lord seam. The III.1b summoner flip and the III.10 deferral audit (Matt-ruled 2026-06-24) are unchanged. No engine code authored — this is a design-canon integration + tracker-reconciliation session.

**Signed:** gandalf, 2026-06-29 (Path A integration).

---

### 2026-06-24 — Matt rulings on the deferral audit (III.10): proxy/charge-stack/support FLIP; VIT DELETE; HP-economy BUILD; dodge KEEP; T4 + element-ailment explained

**Matt ruled on each audited deferral.** The III.10 table is updated in place to RATIFIED dispositions; this delta governs:

1. **proxy/summon — FLIP RATIFIED.** *"Thanks for flipping PROXY."* The summoner un-gate (III.1b) is confirmed. Un-defer `_DEFERRED_PROXY_BINS`; un-defer `ProxySpawn` (the T4 mechanic-alteration, `mechanic_alteration.py:46`) on the same multi-actor-sim dependency.
2. **charge-stack — FLIP RATIFIED.** *"if it was deferred, remove the deferral."* It's build-depth; the v2 thesis IS build-depth. **damage-taken-converts** rides the same logic (identical build-mechanic class) — flipped with it.
3. **support-role — FLIP (investigation confirmed Matt's instinct).** Matt: *"we may need it for summon/proxy (but let's check the skills, maybe it already exists)."* **It already exists** — `_ROLE_DEF_BASE["support"]="mitigator"`, `_ROLE_CTRL["support"]="mixed"` `[bc_target_source.py:29-40]`, aura geometry valid for support/any-element `[ability_grammar.py:250-257]`, full support econ/level/weight tables `[bc_target_composer.py]`. It is deferred ONLY because Profile-A is solo (no ally to support). Proxies create the ally target → **support un-gates on the SAME multi-actor-sim dependency as proxy. No new mechanics to author — just un-gate.**
4. **HP-economy — BUILD (need-it; substrate-acquisition).** Matt: *"we absolutely need this."* The clarified question: v2 build-depth wants life-as-resource builds (PoE Blood Magic / low-life). This is NOT a flag-flip — the mechanic pool has **zero** HP-cost mechanics, so `check_infeasibility` returns HARD-INFEASIBLE (LC-030) correctly. "Needing it" = **author Blood-Magic-class HP-cost mechanics INTO the substrate** (rocket/elrond), then the infeasibility clears on its own. Substrate-acquisition gap, not a toggle.
5. **VIT attribute — DELETE RATIFIED.** Matt: *"VIT attribute should be deleted."* Not a flip-in — **remove entirely.** `attribute-system-2026-05-24.md` (which records "VIT deferred to v1.1+") needs a DELETE amendment; `emit_substrate_registry.py:116` VIT config entry to be removed (rocket/star-lord). Flagged to the owning docs.
6. **dodge_gated_deferred — KEEP RATIFIED.** Matt: *"dodge gate is kept, just awaiting JSON packet emission to test."* Correct layer-handoff confirmed; the gate stays, pending the JSON packet emission that lets the piloted Godot dodge layer be tested.
7. **T4 algorithm + element-conversion Variant-C ailment — AWAITING RULING.** Matt: *"I'm not sure what this represents."* Explanations provided to Matt (see below); these two stay FLAG until he rules. Neither blocks the finalize-and-push (both are measured-for-record-only today; flipping later costs nothing).

**Sequence (Matt verbatim):** *"After we finalize the flips/etc then push and wind down."* AND *"Let's not worry about the across the board [season] reference for now."* → corpus-wide season purge DEFERRED (not now); finalize III.10 flips → push → wind down. T4 + element-ailment rulings can land this session or next without gating the push.

**The two explanations Matt asked for:**
- **T4 algorithm** = the **Tier-4 (top-tier) modifier / mechanic-alteration system** (canonical 40-47). Deferred in two senses: (a) the bounded-viability validation loop measures T4 outcomes *"for record only"* and defers acting on them to Cycle 16+ `[bounded_viability_validation.py:1477]`; (b) several T4 mechanic-alterations are sim-extension-deferred — `ResourceBuffer, MechanicReplacement, ZoneControl, ConditionalModifier, ProxySpawn` `[mechanic_alteration.py:45-46]`. ProxySpawn rides the proxy flip; the other four are the genuine "highest-complexity affixes need the extended sim" set. **Likely a real refinement-defer** (the algorithm works, it's the act-on-it that waits) — but if v2 build-depth wants top-tier affixes live, it's a flip.
- **element-conversion Variant-C ailment** = when a skill **converts its damage from one element to another** (e.g., a fire skill dealing cold damage), Variant-C is the rule where the converted hit carries the **NEW element's ailment** (cold→chill/freeze) instead of the original's (fire→burn). `ELEMENT_CONVERSION_VARIANT_C_AILMENT_ENABLED = False` `[damage_resolver.py:248]`, tagged "Cycle 15 candidate." A **build-depth flavor** mechanic — conversion builds feel more correct with it on, but it's not load-bearing.

---

### 2026-06-23 (later, same session) — Matt directive: BUILD-TO-SPEC, NO DEFERRALS; purge "season-N" + accepted-deferral framing

**Matt's ruling (GOVERNS all deferral language in this doc and forward in every gandalf artifact):** *"We are just building an engine to specs and we have no need to defer anything if it is needed in the engine… We will likely need to flip these out of deferred and remove the deferred verbiage across the board."* Plus: *"get rid of references to season 1 across the board."* The engine is built to its FULL spec; "deferred" is not a disposition for anything the v2 loop needs — it is a gap-to-close.

**What this corrects in the founding block below:**

1. **Summoner/proxy is NOT a deferral — it is a GAP-TO-CLOSE (high priority).** `_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}` `[bc_target_composer.py:97,318]` zeros out every summoner kit (each emitted kit carries `"proxies": []` — `proxy_vocabulary_bridge.py:22-23`). That flag is a stale artifact of the retired Profile-A "sim is solo-only" era. It **conflicts with v2**, where summoning is a **pillar**: grimoire capture-and-summon (§11), temporal summoning (§13), summoner-as-revealed-identity (§12/§17) all need player-side proxy combatants. An engine "to spec" cannot ship summoner deferred. **Reframed → new PART III.1b, tied to the same multi-actor-sim root as the kit-vs-kit keystone (III.1).**

2. **Full deferral audit added → new PART III.10.** Answering "is anything else deferred?": yes — `charge-stack`, `damage-taken-converts`, `support-role` (`check_infeasibility` deferrals), the `VIT` attribute, the `T4` algorithm, `element-conversion` ailment, and the `HP-economy` substrate-gap. Each classified **flip (v2-build-depth needs it)** / **flag for Matt's ruling** / **keep (genuine layer-handoff)**. The ONE "deferred" that is correct and stays: `dodge_gated_deferred` — a balance-loop terminal outcome handing glass-close-ST viability to the *piloted Godot dodge layer* (a layer-handoff downstream, not a missing feature).

3. **"Season-N" content-release framing purged.** "season-1 kits / season-2 companion / six season content types / emit a season's content" were stale leaks of the **retired seasonal-release model** (archived 2026-06-02, `2026-06-02-season-archive-realm-expansion-pivot.md`). Reframed to "engine content types" / "future-product scope." **Code filenames containing "season" (`season_exporter.py`, `season_generation_pipeline.py`, `run_season_production.py`) are real on-disk artifacts → they stay as literal path cites; they are not the release-model framing.**

**Discipline note (gandalf, self-correcting):** survey-mode faithfully reports what-IS (the code says deferred), but when what-IS conflicts with the end-state this doc tracks against, the conflict is a GAP and must be surfaced as one — never passed through as an accepted disposition. Matt caught a pass-through; corrected here. Forward rule: **no "deferred" disposition for anything the v2 spec needs — it is a gap-to-close.**

---

### 2026-06-23 — TRAJECTORY SHIFT captured: ARPG-build-depth + roguelite descent; v2 frame; horde-gap verified; fit-audit consolidated

**This session founded this living doc** by consolidating the 06-18 spine + memo and absorbing two new inputs Matt handed over: the **v2 gameplay-loop design** (death-faith reframe + crystallized roguelite-descent-with-Goldilocks loop) and the **performance-target specs** (Godot 50-150 density). The trajectory is, in Matt's words, "slightly" changed — the *frame* re-registered (isekai → death-faith) and the *loop* sharpened (Goldilocks fork, grimoire economy, roguelite descent), while the engine direction (battle-sim + emission) is carried forward. The change's weight is in the **new engine demands the v2 loop opens** — captured in PART III.

**What this session established (load-bearing):**

1. **The v2 frame fits cleanly; the v2 loop-machinery has three foundational engine gaps.** The death-faith / patron / home-realm re-registration (design doc §2/§3/§14/§15) touches no engine seam and improves the story — no fit problem. The misfits are in the machinery the doc treats as "carried forward intact." Worst-first in PART III.
2. **KEYSTONE gap — there is no kit-vs-kit path in the sim** `[fit-audit: spatial_engine.py:2944 sole entry = one player-class vs list-of-monster-dicts; balance_loop.py:2051 mirror-duel deliberately retired 2026-06-16]`. Goldilocks (§9), scouting (§9), and the matchup-coverage reward all cash against a kit-vs-kit matchup-temperature the sim does not produce. **Resolution path (gandalf lean): a matchup-temperature SIGNAL — a type-chart/distance lookup over already-emitted features (element + archetype + BC-signature + resistances) — NOT a kit-vs-kit fight.** Net-new either way; gates the most → resolve first.
3. **Horde gap — VERIFIED `[gandalf-verified]`.** The balance kernel validates kits against a **maximum of 8 concurrent enemies**. All six arena shells cap at 8 (`arena.py`); all 18 endgame encounters bind to those shells (`endgame_encounter_catalog.py:33`) and never exceed 8 total (`MobSpec` count maxes at 8: catalog lines 222/352/393/524/692; densest mixed pack 6+1+1=8 lines 304-306); golden-master `mean_mobs_killed` tops out at 8.0. The performance doc's endgame target is **50-150 simultaneous** — a 6-19× gap. The just-closed defensive axis (2026-06-21, dm=5.0 boss @ 4.5s / swarm 0.20) was calibrated only at ≤8 concurrent. **BOTH the prior closing-session summary AND my own first state-of-the-build answer missed this.** Matt's instinct ("add a test/encounter/area") is correct → PART III item 3 recommends `SCENARIO_OVERRUN`.
4. **The "400" the marketing hook rests on is ~54 in the live pipeline** `[fit-audit: season_generation_pipeline.py:169 = 18 BC cells × 3 samples; :41 substrate-led no-pre-imposed-N]`. Not necessarily an architecture wall (substrate-led can scale; ~2,293 active rows), but the hook number is ~7× current output. **I refute treating 400 as a hard spec** — the design doc itself says "effectively endless"; 400 is illustrative. The real gap is *validation throughput for hundreds*, not a literal count.
5. **Per-kit level model absent — the descent is unvalidated** `[fit-audit: balance_loop.py:1935 flat-skill assumption, class stats unchanged across bands]`. The 1→50 leveling (§6), the sawtooth (§7), the +3-becoming (§8), and the §21 spacing-inequality are all unmeasurable; the sim validates at a single fixed L50 endgame point. This is doc-33 progression territory the sim has not absorbed.

**Corrections to prior records this session makes (reconcile, do not act on stale):**
- "Evicted kits become the bestiary" (prior recognition record) — **REFUTED.** Monsters are a separate generated bestiary with a closed archetype enum, not derived from kits `[fit-audit]`.
- Mega-boss = "anti-faction contrast-inversion lead" (prior record) — **SUPERSEDED.** v2 §8 sets mega-boss = "holdout champion beyond the base 400 / curated experimental kit"; v2 drops the anti-faction concept entirely (contrast moves to per-lieutenant Goldilocks temperature).
- Doc-38 Unreal platform layer — **decided-superseded but not formally restamped** (style-register retired Unreal; ground-state:52 still lists doc 38 CURRENT). KR restamp, flagged.

**What did NOT move this session:** the content-emission plumbing (two-tracks-don't-meet) — zero movement; still rocket/star-lord seam work. No code authored; this is a consolidation + capture session.

**Empirical criterion gating the next architectural commit:** the kit-vs-kit-temperature scoping (full-sim vs signal-heuristic) is the single highest-leverage resolution — recommend a joint gamora/star-lord scoping consult as the first forward move (PART IV). Until that scoping lands, Goldilocks/scouting/coverage-reward stay design-locked, not built.

**Signed:** gandalf, 2026-06-23.

---

## PART 0 — The frame: three targets, one game

### 0.1 The end state is the v2 gameplay loop

The game we are building is defined by `canonical/reap-die-rise-story/gameplay-loop-design.md` (v2, canonical). One-line: **an ARPG where one spirit, bound to a dark patron, descends procedural dungeons, bests individuated champion-kits, and — by choice — *becomes* them ("you keep what you kill"), accumulating an endless roster that is the record of who it became.** Roguelite-shaped descent (L1→50 per run, resets), sawtooth power curve, Goldilocks matchup-fork at boss floors, grimoire capture-and-summon economy, atmospheric-dark (Synty-under-Godot-lighting), single home-realm creation with face propagation.

This doc does **not** re-litigate the design doc. It tracks the **engine's distance to it.**

### 0.2 The trajectory shift (what "slightly changed" means for the engine)

| Layer | v1 (prior) | v2 (now) | Engine impact |
|---|---|---|---|
| **Frame** | warm isekai / reborn traveler / spirit guide / earth realm | death-faith / ascending conqueror / **spirit guide RETIRED → 3-way split: (A) demigod-jailer tutorial + key beats, (B) caged patron god as rare unreadable guidance, (C) hub NPC ensemble as daily relationship/banter** / time-agnostic **home realm** | **None at the seam** — re-registration only; improves story. Prior cosmograph/earth-avatar canon needs reconciliation (PART III.9). |
| **Loop** | journey-as-descent (v1 release model) | **roguelite procedural descent** + Goldilocks fork + grimoire economy | **New demands**: kit-vs-kit temperature, per-kit level model, horde density (PART III). |
| **Build depth** | implicit | **explicit ARPG build-depth pillar** ("no meta," 400 unique, parametric abilities) | Parametric-ability realization (data-layer mostly present; Godot verbs unbuilt); scale-throughput. |
| **Combat density** | unspecified | **50-150 simultaneous** (perf doc) | Horde gap — sim caps at 8 (PART III.3). |

**The honest read:** the engine *direction* (validate kits in a battle sim → emit the engine's content for Godot) is unchanged. The v2 loop adds **new measurement demands** the current sim was never built to satisfy. The work is not a pivot; it is an extension whose long poles are now visible.

### 0.3 The two engine completion targets (unchanged definitions, now serving the v2 loop)

- **(A) Battle-sim complete** = the measurement instrument is *honest* AND the bands are *ruled + wired* AND the open balance calls are *dispositioned* — **and now additionally** measures what the v2 loop demands (matchup temperature, per-level scaling, horde density). PART I.
- **(B) Content-emission complete** = one driver emits all **six** engine content types (kits / monsters / factions / gear / weapons / flavortext) into a single Godot-consumable sim-ready bundle. PART II.

---

## PART I — Battle sim: current state → end state

### I.1 Current state (what exists, cited)

- **Sole substrate = the 2D spatial gauntlet** (1D sim deleted 2026-06-16, `gamora/v1.1-1d-sim-b6-deletion`). Tick-based (0.1s), physical/magical/hybrid routing, 7×7 resistance matrix, recompose-first balance loop (4 levers before modifier search).
- **Genuinely spatial** `[fit-audit]`: real arenas, entity radii, cone/line/circle AoE, chokepoints, flanking — the *ambition* of spatial encounter design is supported at the sim level.
- **Sole fight entry** `[fit-audit: spatial_engine.py:2944]`: one player class vs a list of monster dicts. **No second-kit slot. No kit-vs-kit path.**
- **6 arena shells, all cap ≤8 concurrent** `[gandalf-verified: arena.py]`: open_arena 8 swarm, chokepoint 8 swarm, boss_with_adds 3, magic_pack 4, elite_pack 3, mini_boss 3.
- **18 endgame encounters bind to those 6 shells** `[gandalf-verified: endgame_encounter_catalog.py:33]`; max composition = 8 (catalog lines 222/352/393/524/692); `mean_mobs_killed` golden-master = 8.0.
- **Validation at fixed L50 endgame** `[fit-audit: balance_loop.py:1935]`: flat-skill assumption, class stats unchanged across bands. L17/L33/L50 labels are *monster difficulty bands*, not kit levels.
- **Pass criterion**: kit ships iff ≥9/18 eligible encounters in-band (tier_2_kpm) for ≥1 of 4 cohorts.
- **Win-condition split (boss shells)**: survive-and-kill within 240s enrage, binary; DPS/TTK measured-never-gating `[d5b7ac2]`.
- **Defensive axis CLOSED + offensive bands FINAL** (2026-06-21 G-C close): dm=5.0 boss @ cadence 4.5s, swarm 0.20 LOCKED as calibration anchors; 0.926 unmatched-resist survive+kill a watch-item `[decisions-log 4562-4649]`. **Calibrated at ≤8 concurrent only.**
- **DPS is derived, not a gate** `[fit-audit: bounded_viability_validation.py:431]`: only a ≤1.5× cross-path variance check.
- **Summoner/proxy archetype is GATED OUT today — a GAP-TO-CLOSE, not a settled disposition** `[bc_target_composer.py:97,318 _DEFERRED_PROXY_BINS={proxy-light, proxy-heavy}]`: the sim is solo-only (legacy Profile-A), so proxy-creating kits cannot be evaluated and **every emitted kit carries `"proxies": []`** `[proxy_vocabulary_bridge.py:22-23]`. v2 makes summoning a **pillar** (grimoire §11/§13, summoner-identity §12/§17) → the engine is not to-spec until this is BUILT. See PART III.1b.

### I.2 End state (where the sim must go)

The honest-instrument + ruled-bands criterion (above) **plus** three v2-driven instrument extensions:
1. A **matchup-temperature** measurement (kit-relative "too hot / just right / too cold") for Goldilocks/scouting/coverage-reward.
2. A **per-kit level-scaling** model so the 1→50 descent, the sawtooth, and the +3-becoming are validated, not assumed.
3. A **horde-density regime** (≥50 concurrent) so KPM/defensive bands certify at play-density, not at 8.

### I.3 The gap (battle sim)

Carried B-series blockers (detail: predecessor spine doc): keystone-ceiling open_arena 1.000 WR zero-variance; caster coverage-bound (3.3× HP move = ΔWR ~0.02); trial-gallery NotImplementedError; summoner spatial-combat unbuilt. **PLUS the three v2-driven extensions** — these are the new long poles, detailed in PART III (items 1, 2, 3). The sim's *direction* is sound; its *finish line moved out* the moment the v2 loop named demands it was never built to measure.

---

## PART II — Content-emission pipeline: current state → end state

### II.1 Current state — two emit tracks that do not meet

```
TRACK NEW (cycle-14 wave5) → reincarnated-loadout app JSON
  run_season_production.py → kit-candidates → gauntlet+PM1 → mechanical-archive
    → cohesion-judge LLM (faction identity / names) → joint-gate → cycle14_wave5_emitter
  KIT+FACTION-RICH, but: no monsters; skill flavor_text NULL; main_weapon NULL.

TRACK OLD (season_exporter) → exports/<id>/{metadata,classes,monsters,gear_pool,...}.json
  SIM-READY bundle, but: kit/monster/gear-only (factions ABSENT, weapon=null);
  one-shot generate-season CLI driver DELETED (b6 deletion).

THE GAP: the two tracks never meet. No single driver emits all content into one
  Godot-consumable bundle. cycle-14 content never reaches season_exporter;
  season_exporter never gets factions / weapon-descriptors / cycle-14 kits.
```

**The six-content-type honest state** (NPC struck 2026-06-18 — "npc" = a companion/mercenary ally or future Engine-2 townsfolk, which is **future-product scope**, NOT one of the engine's six current content types):

| Type | State | Evidence |
|---|---|---|
| **kits** | WORKING (solo) / **summoner GATED-OUT (gap → III.1b)** | `classes.json` full stat_distribution + skills + LLM names; every kit emits `proxies:[]` — summoner archetype unbuilt, not "deferred" |
| **monsters** | WORKING (old track) / MISSING (cycle-14) | `monsters.json` 44 w/ stats+flavor; cycle-14 is kit-only |
| **factions** | PARTIAL — generated, never written to bundle | schema `schemas.py:1174`; `_export_season_inner()` never writes it |
| **gear** | WORKING | `gear_pool.json` 200 items + rolled_effects + LLM names |
| **weapons** | PARTIAL — identity in substrate, not emitted | `main_weapon=None` everywhere; lives in `substrate_weapon_binding` |
| **flavortext** | WORKING (class/monster/gear) / GAP (cycle-14 skill NULL) | `naming.py` live Anthropic calls |

### II.2 End state

One driver emitting all six types into one sim-ready Godot bundle, with the cycle-14 kit/faction richness and the old-track monster/gear completeness joined.

### II.3 The gap (emission) — mostly rocket/star-lord plumbing; gandalf surface = content-shape specs

- (a) single driver routing cycle-14 content through (or replacing) `season_exporter` — *star-lord/rocket*
- (b) monster generation wired into the cycle-14 track — *rocket/star-lord*
- (c) `faction_clusters` actually written — *star-lord, gated on the faction content-shape spec (gandalf)*
- (d) weapon descriptor wired `substrate_weapon_binding → main_weapon` — *star-lord, gated on the weapon content-shape spec (gandalf)*
- **NEW v2 emission demands** (PART III.6): encounter-geometry-per-floor (seam-ownership unresolved); faction as presentation-restyle only (the hard invariant — III.7).
- **Emission HELD / Matt-gated** `[export/MIGRATION.md v1.81-1.82]`: telemetry supports validation; it does NOT unlock emission.

**The bridge to Godot (Track B) does not exist** — content-consumption loader + GDScript combat-parity re-implementation are greenfield and the longest pole overall. This is downstream of both A and B.

---

## PART III — The v2-design engine-fit gaps (the new material, worst-first)

Each item: what the v2 design asks · what the engine currently does · the gap · resolution path · owner. Provenance-tagged.

### III.1 — KEYSTONE: kit-vs-kit matchup-temperature (Goldilocks) [HIGHEST LEVERAGE]

- **v2 asks** (§9): each boss floor offers 3-4 lieutenants at different **matchup temperatures relative to the current kit** (too hot / just right / too cold), regenerated on every reincarnation; scouting glyphs preview temperature; the matchup-coverage reward cashes against it.
- **Engine does**: only **global** kit-vs-control validation. **No kit-vs-kit path** `[fit-audit: spatial_engine.py:2944; mirror-duel retired balance_loop.py:2051]`.
- **Gap**: three mechanics (Goldilocks, scouting, coverage-reward) rest on a measurement the sim does not produce and that was deliberately removed.
- **Resolution path (gandalf lean — now substrate-confirmed by `design-decisions-session.md` §4/§5):** Goldilocks needs a matchup-**temperature signal**, not a kit-vs-kit **fight**. §4 names the substrate concretely: a **~24×24 QD-grouping matchup matrix** (the 20-24 "classes" = the rows/columns; ~400-576 inspectable cells — **not** an unwieldy 400-kit matrix). Type relationships (AoE > summon/proxy, single-target > AoE, melee/close vs ranged/kite) are a **[MEASURE] prior derived from sim data, NOT asserted** — and kits are **multi-type** (model combined-type matchups, not independent RPS axes). Use the matrix as a **Goldilocks generation-constraint** — guarantee **≥1 winnable matchup** per spread while keeping the "too hot" counter (do NOT over-correct into all-easy boards) — **NOT for withholding kits** (strictly better: keeps all kits, fixes at the encounter layer). **§5 adds a probabilistic dimension:** matchup type = **(grouping + capstone-state)**, and the matrix is a **distribution**, not a fixed table — the ~1/3 conversion-capstone inversions move a kit across the matrix (worked example: a maximally-proxy-by-input kit becomes caster-by-behavior post-capstone), so Goldilocks safety is a **confidence, not a guarantee**, with the **portal escape-valve as the backstop**. [MEASURE] the inversion **probability masses** — the matrix-as-distribution needs the weights. **[OPEN] (§4):** whether the BC axes *align* with the matchup axes (matrix falls out cleanly) or are *orthogonal* (matchup = an added characterization layer) — **"mechanically distinct (QD) ≠ matchup-distinct" → measure the matrix separately.** ~~Compute temperature as a lookup over already-emitted features — archetype + dominant_element + BC-signature distance + resistance profile~~ (superseded 2026-06-29: the QD-grouping matrix IS that lookup, made concrete). Still **net-new** (the matrix must be *measured* — a hypothesis-test over finished kits, not asserted); the alternative — a true kit-vs-kit sim **fight** slot — is heavier net-new spatial-combat architecture and is **not** what §4 asks for.
- **Owner**: joint **gamora + star-lord scoping** (the matrix-measurement: which sim queries produce the 24×24 cells + the inversion probability masses) — the first forward consult; **gandalf** design-fit on the temperature definition + the Goldilocks safety-envelope constraint. **Resolve first; it gates the most.**

### III.1b — Summoner / player-side proxies (the grimoire-summon pillar) [HIGH — same multi-actor root as III.1] — FLIP RATIFIED (Matt 2026-06-24)

> **Status:** Matt ratified the flip 2026-06-24 (*"Thanks for flipping PROXY"*). This is no longer a recommendation — it is a confirmed gap-to-close. **Support-role rides this same un-gate** (mechanics already exist; deferred only by solo Profile-A — see below). `ProxySpawn` (T4 mechanic-alteration, `mechanic_alteration.py:46`) un-defers on the same dependency.

- **v2 asks**: summoning is a **pillar**, not flavor — the grimoire capture-and-summon economy (§11), temporal summoning of coveted champions into your next dungeon at your level (§13), and **summoner-as-revealed-identity** ("a player who chooses summoner every time *is* a summoner," §12/§17). Player-side proxy combatants are core to the loop.
- **Support-role rides this (confirmed 2026-06-24)**: support is NOT missing from the engine — `_ROLE_DEF_BASE["support"]="mitigator"`, `_ROLE_CTRL["support"]="mixed"` `[bc_target_source.py:29-40]`, aura geometry valid for support/any-element `[ability_grammar.py:250-257]`, and full support econ/level/weight tables exist `[bc_target_composer.py]`. It is `check_infeasibility`-deferred ONLY because Profile-A is solo (no ally to support). Once proxies (and/or the §14 companion ally) provide ally targets, support un-gates on the **same multi-actor-sim dependency — no new mechanics to author.**
- **Engine does**: gates the entire proxy archetype OUT. `_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}` `[bc_target_composer.py:97,318]`; `check_infeasibility` returns `is_deferred=True, reason="sim is solo-only (Profile A); proxy-creation mechanics absent"`. Every emitted kit carries `"proxies": []` `[proxy_vocabulary_bridge.py:22-23; schemas.py:1305 "production proxy_decls always [] → reads 0.0 on all real rows"]`.
- **Gap**: a **stale Profile-A artifact**, not a design disposition — and per Matt 2026-06-23 it does NOT survive as a deferral, because the v2 spec needs it. The sim cannot create, position, or resolve a player-summoned proxy that deals spatial damage / takes aggro.
- **Resolution path**: build the **player-side multi-actor path** — proxies as spatially-real combatants the player's kit creates (occupy position, deal/take damage, draw aggro). This is the **same root** as the III.1 kit-vs-kit keystone (the sim is single-actor-per-side); BUT it forces the harder branch — summoner viability genuinely needs the proxies *simulated*, so the III.1 type-chart heuristic does NOT discharge it. Un-gate `_DEFERRED_PROXY_BINS` only once the sim can evaluate proxy kits.
- **Owner**: **gamora** (multi-actor sim + proxy combat; support-role un-gate on the same path) + **rocket** (proxy-decl generation un-gate); **gandalf** design-fit on summoner viability bands + the grimoire-summon combat contract. **Scope jointly with III.1 — shared multi-actor-sim foundation.**

### III.2 — Per-kit level model (the descent is unvalidated)

- **v2 asks** (§6/§7/§8/§21): L1→50 per descent; sawtooth tuned to "power from ~2 levels prior"; +3-becoming reward; the spacing inequality (levels-per-champion ≤ levels-caught-up-between).
- **Engine does**: validates at a single fixed L50 endgame point; flat-skill assumption `[fit-audit: balance_loop.py:1935]`.
- **Gap**: "in-band" means in-band *at endgame against the control* — it says nothing about balance at L13 partway down a descent. The sawtooth, the +3-becoming, and the §21 inequality have **no validating instrument today**, and the §21 inequality is literally unfalsifiable without a per-level kit model.
- **Resolution path (made TRACTABLE by `design-decisions-session.md` §12):** ~~doc-33 progression absorbed into the sim — a per-level kit-scaling curve + a descent-band measurement. Substantial net-new.~~ (sharpened 2026-06-29.) §12 rules the method: do **NOT** re-run the entire season's in-band filtering at every stage (a combinatorial explosion, likely intractable per-season). Instead **validate the *staging LOGIC*** — stat curves, skill-unlock order, the `express_gear` scaling function (III.8) — by checking a **representative grouping-level sample stays in-band across ~4-6 checkpoint milestones (1→50)**, and fix the *systematic* outliers at the generator level (Principle: validate the generator, not the instances). **The lumpy axis = skill-unlock progression** — unlike stats/gear (smooth), skills unlock *discretely and in an order* → **non-monotonic in-band-ness** (a kit fine@20, broken@30 when a strong skill unlocks before its counterbalance, fine@40); the *partial tree's shape* can be unbalanced even when the *full* tree is balanced. **Spend the sim budget here.** This is bounded checkpoint-validation, not a full per-level rebuild — doc-33 progression supplies the staging curves the checkpoints test.
- **Owner**: **gamora** (the checkpoint-validation harness + the per-grouping in-band sample) + doc-33 progression lineage; **gandalf** the **skill-unlock checkpoint spec** (which ~4-6 milestones; the non-monotonic stress-test) + the sawtooth/+3/§21-inequality acceptance criteria. **Gated on the flag #2 persistence-contract ruling** (what banks across reset) before the +3-becoming band is specced.

### III.3 — Horde density (8 → 50-150) [gandalf-verified]

- **v2/perf asks**: 50-150 simultaneous hostiles (perf doc §3/§5; comfortable band, anti-target the PoE-juiced few-hundred); horde count is gameplay-critical and fixed across hardware tiers (a balance variable, not a render-only knob).
- **Engine does**: max **8** concurrent, ever `[gandalf-verified: arena.py 6 shells; endgame_encounter_catalog.py MobSpec max 8; mean_mobs_killed 8.0]`. The defensive axis (2026-06-21) was calibrated at ≤8.
- **Gap**: a 6-19× density gap. AoE-vs-single-target balance **inverts** with density (D3 vanilla→RoS; PoE Breach/Legion "AoE-or-die") — the same KPM band cannot judge both regimes. The engine has **no horde/gather primitive** `[arena.py:298-365: player-AI closes on nearest mob; no "reposition to GATHER into the AoE" primitive — and that was a struggle over eight mobs]`, so it cannot even *measure* AoE value at density.
- **Resolution path (gandalf recommendation):** a 7th gauntlet scenario **`SCENARIO_OVERRUN`** at the **comfortable-band floor (≥50, not the ceiling)** — "measure, don't assume" the peak. Re-fit KPM bands for the horde regime (its own bands). Build the **M1 horde-positioning primitive** (gather/funnel/kite) — the prerequisite and likely the longer pole. Expect a **defensive-axis re-fit** (50 swarm @ 0.20 ≈ 6× the incoming the bands were fit against). The 2026-06-21 close is valid *within its measured band*; the band moved.
- **Owner**: **gamora** (scenario + M1 primitive + band re-fit); **gandalf** (scenario-design spec + horde-regime KPM-band methodology).

### III.4 — The "hundreds" scale (54 today)

- **v2 asks** (§4/§20): ~400 in-band kits; the hook is the *scale that defeats netdecking* ("seven classes is the genre standard; here are four hundred").
- **Engine does**: ~54 candidates per run `[fit-audit: season_generation_pipeline.py:169 = 18 BC × 3]`; no "400" target; substrate-led, no pre-imposed N `[:41]`; ~2,293 active substrate rows could support more.
- **Gap**: the hook number is ~7× current output. **Not necessarily an architecture wall** — but the pipeline must *demonstrably* produce hundreds, and validation throughput at that scale is unproven.
- **gandalf refutation — RATIFIED + given a concrete derivation by `design-decisions-session.md` §3.** The decision: **launch ~100 fully-distinct kits; architect the engine for 400+; "launch lean, grow endless."** Don't *target* a number — **derive it as `min(marketing-floor, production-ceiling, distinctiveness-ceiling)`**: marketing-floor **saturates at ~100** (100 vs 400 read identically as "impossibly many"; past 100 helps retention, not acquisition); production-ceiling is **[MEASURE] per-kit hours** (build 10-20 to full quality, measure — *the likely binding wall for a solo dev*, and it turns entirely on library+config-parametric vs hand-build); distinctiveness-ceiling: **300-sharp beats 400-with-80-reskins** (a samey kit is *evidence against* the hook). The real hook is the **generative engine** (the *capacity* for endless distinct kits); the launch count just proves it's real. **So the engine target is: demonstrably produce ~100 in-band launch kits, architected to 400+ — and the real gap is *validation throughput at that scale + the [MEASURE] per-kit production cost*, not a literal count.** (This retires the looser "400 is illustrative" framing in favor of the §3 derivation — same conclusion, now with the marketing/production/distinctiveness math behind it.)
- **Owner**: **rocket/gamora** scale-config + throughput + the [MEASURE] per-kit-hours instrument; **gandalf** the launch-count derivation + hook-honesty framing.

### III.5 — Monsters: "one pipeline, two roles" is aspiration, not build

- **v2 asks** (§4/§5): one pipeline, two roles (monsters = fixed control, kits = treatment); named champions (lieutenants/mega-boss) ARE kits, becomable; fodder monsters are not.
- **Engine does**: a **separate** generated bestiary — `ExportMonster`, closed archetype enum (brute/caster/swarmer/sniper/controller/tank), threat-tier, built via `build_reference_gauntlet`. **Monsters are not derived from kits** `[fit-audit]`.
- **Gap**: both the prior "evicted kits → bestiary" record and the doc's "one pipeline" framing describe a unification that does not exist. **The fodder/champion split the doc relies on is sound** (and matches the engine — fodder monsters vs becomable champion-kits); what's absent is monsters-as-role-partitioned-kits.
- **Resolution path**: design call — keep the separate fixed-control bestiary (cleanest for the sim's control-variable role) and source *named champions* from the kit pipeline (which the doc already wants), OR unify. **Lean: keep fodder-monsters as the fixed control (write-once, §4); source lieutenants/mega-boss from kits.** That satisfies the doc's becomable-champions ask without forcing monsters-from-kits.
- **Owner**: **gandalf** design call; **rocket/gamora** if any unification.

### III.6 — Encounter-geometry emission + a seam-ownership conflict

- **v2 asks** (§9): the engine emits per-floor encounter JSON "including room dimensions and structure … constructed around the lieutenant's strengths and the player's weaknesses."
- **Engine does**: season export carries **zero geometry** (kit/balance/stat only); the one geometry artifact is `arena_scenarios.json` — a Godot-only sidecar, 6 fixed shells (open_arena 50×50, chokepoint 10×50), not per-matchup-tuned `[fit-audit]`.
- **Conflict**: this collides with the prior seasonal-descent decision — "**engine emits content, Godot owns geometry.**" §9 says geometry comes from the engine. **Pick one.** (Good news: the sim *is* genuinely 2D-spatial, so spatial encounter design is supported; it's the *procedural-per-matchup generation* + *emission* that don't exist.)
- **Resolution path**: a seam-ownership ruling. **Lean: engine emits an encounter *intent* (composition + spatial-parameter hints derived from the matchup), Godot realizes geometry** — preserves "Godot owns geometry" while letting the matchup shape the fight. Avoids the engine owning room-mesh layout.
- **Owner**: **gandalf + drax + knight-rider** seam-ownership call.

### III.7 — Faction is walled out of combat (CORRECT discipline — endorse)

- **v2 asks** (§6): "each floor changes the faction and element of its enemies."
- **Engine does**: hard invariant — **zero faction fields enter the fight model; any faction field in a class/monster export raises a hard error** `[fit-audit: cycle14_unified_bundle_emitters.py:330]`.
- **Split**: **element** is mechanical and fully supported (first-class dominant_element + resistances; per-floor element rotation is real and validated). **faction can only be presentation-restyle** — it cannot make a fight harder or different.
- **gandalf endorsement**: this is **healthy discipline, not a gap** — it keeps the fight model clean (D2's act-bosses differ by *abilities*, not by a "faction" tag). **The design-doc language is loose, not the engine.** Any "this lieutenant is built against your weakness" difficulty must come from **element + archetype matchup**, never from faction. Re-seat the §6 contrast at the element/archetype layer.
- **Owner**: **gandalf** design-language correction; **no engine change.**

### III.8 — Corrections & narrower-than-feared items (briefer)

- **NEW DEMAND (not a narrowing) — gear-as-sim-variable** `[design-doc: design-decisions-session.md §7]`. v2 **pushes gear INTO the battle sim**: kits are validated **as geared units**, gear a **treatment variable** the sim tunes/measures, via a `express_gear(power_level, kit) → balanced affixes` function called in two directions that are the *same operation* — looting (target-power = current stage) and possession-transform (target-power = prior-gear-power, kit = new kit). **"Balanced across all stages" is a claim to VALIDATE (generate→sim→check-in-band→adjust), NOT a formula to assume** — affixes scale non-linearly (CDR, %damage, breakpoints, capstone-synergies); the possession-transform's "preserve power level" must mean **sim-measured equivalence** ("same in-band position for the new kit"), not "same numbers." Scope at the grouping level; target *pervasive* mis-scalings. **`express_gear` is one of the staging-logic functions III.2's §12 checkpoint-validation tests.** **CRITICAL sawtooth-guard (hard invariant the sim must respect):** gear-affix scaling is **by stage of the game (itemization), NOT content-difficulty scaling by the player's live power — the Oblivion treadmill is forbidden.** Test for every scaling instinct: content *fixed by depth* (✓ player rises to meet it; backtracking-dominance preserved = the *reward*) vs *dynamic by player power* (✗ treadmill). **Owner:** gamora (express_gear in the sim as a treatment variable) + rocket (affix generation); gandalf (the validation-loop spec + the sawtooth-guard acceptance test). Cross-refs III.2 (checkpoint-validation) + III.4 (geared kits are what "in-band" must mean).
- **DPS is not a validated band** `[fit-audit: bounded_viability_validation.py:431]`. §4's "WR, KPM, and DPS all within ranges" overstates — WR + KPM gate; DPS is a ≤1.5× variance check. Minor.
- **Parametric abilities — partly already here.** The 16-type geometry palette (24 in production: chain_lightning, beam_channel, ground_slam, vortex_pull, whirlwind…) **is** the §20d "bounded library of ability primitives" — *at the data level*. Unbuilt: the Godot-side realization of each primitive as a distinct playable verb. The cash-condition is narrower than §20d fears — "realize the existing 16/24 primitives as verbs," not "invent a library."
- **Scouting glyphs — feasible, vocabulary mismatch.** `archetype_tag` + `role_orientation` are already emitted + surfaced in the demo UI. But engine labels (fire_mage, hunter…) ≠ the doc's "glass cannon / bruiser / controller" vocabulary. Needs a **label→glyph mapping** (respecting Discipline #41 — the presentation vocabulary maps to emergent clusters, does not pre-impose a taxonomy), not new generation.
- **Patron runtime banter (§15) — net-new online infra.** The engine's LLM layer is offline-batch (faction labels, kit identities, once per season). Runtime contextual banter is a different latency profile — not reusable existing plumbing. The doc's instinct to flag it as a real scope decision is correct.
- **Mega-boss source diverged** — reconcile (see SESSION-DELTA): prior "anti-faction" record superseded by v2 §8 "holdout champion beyond 400 / curated experimental kit."

### III.9 — Story-canon reconciliation (v2 supersedes a chunk of prior canon)

v2 re-registers the frame. The authoritative v2 story canon is now `canonical/reap-die-rise-story/story-keystone.md` (governs) → `story-expansion.md` (detail) → `design-decisions-session.md` §§2-13 (systems); **`design-decisions-session.md` §1's patron sketch is superseded** (see below). The following prior canon needs reconciliation (a **named forward work item**, not resolved here):
- **isekai → death-faith** (§2): reincarnation *mechanic* + world-rotation survive, re-registered as conquest.
- **patron precisely sourced — Daikoku/Mahakala (`story-expansion.md`:46/:177; supersedes `design-decisions-session.md` §1).** The patron is a **hijacked benign fortune-deity**: **Daikoku** (Seven Lucky Gods / Shichifukujin), root **Mahakala** — a death/destruction power wearing the mask of luck; soul-feeding produces a hollow, will-draining peace (peace-as-lobotomy). The **earlier Ereshkigal/Nergal "original sealed death-deity" sketch (`design-decisions-session.md` §1) is DEAD — do not cite it.** **BUT §1's DEVICE-layer is orphaned, not auto-dead** — the **trickster-jab** ("you're just a minor luck-spirit"), the **crackable-alias + authored-slow true-name** device, the **seven-gated descent as floor-structure**, and **descent ≠ underworld aesthetic** survive the sourcing-swap (several fit Daikoku/Mahakala *better* — a death-power masked as a luck-god makes the jab cut the real wound). **These need re-homing-or-retiring rulings (task #4 / Matt); do not silently amputate them with the Ereshkigal sourcing.**
- **spirit guide RETIRED** (keystone §16-17, §19.1; expansion §3): the spirit guide is **removed as an entity** (Matt 2026-06-30, not re-labeled); its advisory function splits **three ways** — **(A)** the **demigod-jailer** (the jailer who *selects and steers*; NOT the player's future self) owns the **tutorial-instruction** voice + **punctuated Mercer-mentor key beats** (§19.1; optional warm-early-then-recede tragedy-phase); **(B)** the caged, unreadable **patron god** Daikoku/Mahakala — the deity the player rarely communes with (god-speech §19.3) — owns a **rare seldom-heard guidance** voice; **(C)** the **hub NPC ensemble** (Rita + the cult's human faces) owns the **daily relationship + antagonistic-helpful banter + defiance↔devotion axis** (RULED Matt 2026-06-30, the Hades model — flag #6), which IS the cult-standing economy (loop-doc §23.5) given a voice. Reconcile the demigod-mentor against the **companion/mercenary ally** (future-product scope; **claimed-soul-sourced per the A11 two-register ruling** — `reap-die-rise-story/story-expansion.md` §12, story-tracker B3; the 2026-06-13 companion capture folded there 2026-07-01) — demigod-mentor (guidance), patron god (caged deity), hub ensemble (relationship/banter), and companion (ally) appear to be four distinct entities; confirm. **Note:** the §14 companion ally is also what un-gates support-role alongside proxies (III.1b).
- **earth realm → time-agnostic home realm** (§3): same structural function (one creation, face propagation, cultural-diversity-as-world-diversity); contemporary-Earth baggage shed. Reconcile against the earth-avatar/cosmograph creation-moment canon (`2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`).
- **cosmograph re-anchored** (§2b): "the cosmograph is the patron's domain" — the night-sky-of-kits gains a native mythology. The cosmograph SURVIVES; reconcile the pivot docs (`2026-06-05-cosmograph-pivot.md`) to the patron framing.
- **Owner**: **gandalf** — a dedicated story-canon reconciliation pass (forward queue, PART IV). Do not silently let v2 and prior records contradict.

### III.10 — Deferral audit: what else is gated, and whether v2 needs it [Matt directive 2026-06-23]

Per Matt's build-to-spec ruling, every engine deferral is re-classified: **FLIP** (v2 needs it → gap-to-close), **FLAG** (needs Matt's ruling), or **KEEP** (genuine layer-handoff, not a scope-cut). Audited against engine source this session. **Matt ruled 2026-06-24 — dispositions below are RATIFIED except the two he asked to have explained (now AWAITING).**

| Deferral | Code site | v2 read | Disposition (Matt 2026-06-24) |
|---|---|---|---|
| **proxy/summon bins** (proxy-light/heavy) | `bc_target_composer.py:97,318` | grimoire-summon pillar (§11/§13), summoner identity (§12/§17) | **FLIP — RATIFIED.** Un-gate → III.1b (high). Also un-defer `ProxySpawn` (`mechanic_alteration.py:46`). |
| **charge-stack** mechanic bin | `bc_target_composer.py:311` | stacking-resource build mechanic — the v2 thesis IS combat-build-depth | **FLIP — RATIFIED** ("remove the deferral"). |
| **damage-taken-converts** mechanic bin | `bc_target_composer.py:312` | defensive→offensive conversion (PoE-class build mechanic) | **FLIP** — rides charge-stack (same build-mechanic class). |
| **support role** | `bc_target_composer.py:313` (Profile-A solo) | proxies + companion ally (§14) create ally contexts | **FLIP — confirmed.** Mechanics ALREADY EXIST (mitigator/mixed/aura tables); deferred only by solo Profile-A → un-gates on the SAME multi-actor-sim dependency as proxy. No new mechanics. |
| **HP-economy** | `bc_target_composer.py:326` (HARD-INFEASIBLE, LC-030) | Blood-Magic-class build mechanic; pool has ZERO HP-cost mechanics | **BUILD — need-it.** NOT a flip: author HP-cost mechanics into the substrate (rocket/elrond); infeasibility clears on its own. |
| **VIT attribute** | `attribute-system-2026-05-24`; `emit_substrate_registry.py:116` | defensive/health-scaling attribute; was deferred to "v1.1" | **DELETE — RATIFIED.** Remove entirely (not flip-in). Amend `attribute-system-2026-05-24.md`; strip `emit_substrate_registry.py:116` config (rocket/star-lord). |
| **T4 modifier algorithm** | `bounded_viability_validation.py:1477`; `mechanic_alteration.py:45-46` | top-tier affix/mechanic-alteration system; "measured-for-record, Cycle 16+" | **AWAITING** — explained to Matt (Tier-4 affix system; 4 sim-extension-deferred alterations remain). Likely real refinement-defer; non-blocking. |
| **element-conversion Variant-C ailment** | `damage_resolver.py:248` | converted hit carries the NEW element's ailment; "Cycle 15 candidate" | **AWAITING** — explained to Matt (build-depth flavor for conversion builds). Non-blocking. |
| **`dodge_gated_deferred`** | `balance_loop.py` (terminal outcome) | NOT a scope-cut — hands glass-close-ST viability to the *piloted Godot dodge LAYER* | **KEEP — RATIFIED.** Gate stays; awaiting JSON packet emission to test downstream. |

**The pattern Matt named:** the engine accreted "deferred" dispositions under the old phased/Profile-A/Cycle-N staging. The v2 trajectory — *ARPG combat build-depth* — turns several of those into **direct removals of the thing the game is about** (summoner, charge-stack, damage-conversion, HP-cost are exactly the build-mechanic depth the hook promises). **Resolution (Matt 2026-06-24):** proxy + charge-stack + damage-taken-converts + support FLIP (the last three rebuild combat-build-depth; support needs no new mechanics — un-gate only); HP-economy is a substrate-BUILD (author HP-cost mechanics); VIT is DELETED outright; T4 + element-ailment stay FLAG pending explanation-then-ruling (non-blocking); `dodge_gated_deferred` is the one correct KEEP.

- **Owner**: **gamora/rocket** (the un-gates: proxy/support multi-actor-sim, charge-stack/damage-conversion bin un-defers) + **rocket/elrond** (HP-economy substrate authoring; VIT config strip) + **gandalf** (VIT doc amendment; T4 + element-ailment ruling brief if Matt wants depth). Forward-queue item (PART IV).

---

## PART IV — Owner map + forward queue

### IV.1 What's a gandalf chokepoint vs another seam's

| Work | Owner | gandalf surface |
|---|---|---|
| kit-vs-kit-temperature scoping | gamora + star-lord | design-fit on temperature definition (III.1) |
| summoner / player-side proxies + support-role (un-gate) | gamora + rocket | summoner viability bands + grimoire-summon combat contract (III.1b); support rides the same multi-actor-sim un-gate (mechanics exist) |
| deferral audit — RULED (Matt 2026-06-24) | gamora/rocket/elrond (un-gates); gandalf (VIT doc) | the ratified flip/delete/build/keep dispositions (III.10) |
| per-kit level model | gamora + doc-33 | scenario-design + sawtooth-inequality spec (III.2) |
| `SCENARIO_OVERRUN` + M1 primitive + band re-fit | gamora | scenario-design spec + horde KPM-band methodology (III.3) |
| scale throughput (hundreds) | rocket/gamora | hook-honesty framing (III.4) |
| monster/champion sourcing | rocket/gamora | the design call (III.5) |
| encounter-geometry seam | drax + KR | the seam-ownership ruling (III.6) |
| emission plumbing (a)(b)(c)(d) | star-lord/rocket | faction + weapon **content-shape specs** (gandalf) |
| Godot bridge (loader + GDScript parity) | drax + engine | content-shape fidelity review |
| doc-38 Unreal restamp | knight-rider | flag (done) |

### IV.2 gandalf forward queue (priority order)

1. **Convene the multi-actor-sim scoping consult** (gamora + star-lord) — the keystone, with TWO faces sharing one root (the sim is single-actor-per-side): (a) **kit-vs-kit matchup-temperature** (III.1 — gates Goldilocks/scouting/coverage-reward; likely a signal-heuristic) and (b) **summoner / player-side proxies** (III.1b — the grimoire-summon pillar; needs proxies genuinely simulated). Author the design-fit brief framing heuristic-vs-full-sim for (a) and the proxy-combat contract for (b).
2. **Author the `SCENARIO_OVERRUN` design spec + horde-regime KPM-band methodology** — the verified, clock-on-it gap; every band locked at 8-concurrent is a band we may re-litigate.
3. **Deferral audit RULED (Matt 2026-06-24)** (III.10) — proxy/charge-stack/damage-converts/support FLIP; VIT DELETE; HP-economy BUILD (substrate); dodge KEEP; T4 + element-ailment AWAITING explanation-ruling (non-blocking). Forward work now sits with the un-gate owners (gamora/rocket: proxy+support multi-actor-sim, charge-stack/damage-conversion bin un-defers; rocket/elrond: HP-cost substrate authoring + VIT config strip; gandalf: VIT doc amendment). Not a gandalf-authoring blocker anymore — a dispatch-sequencing item for KR.
4. **Author the faction + weapon content-shape specs** — unblocks emission plumbing (c)(d); needed regardless of trajectory.
5. **Author the per-kit-level / sawtooth-inequality stress-test spec** (III.2) — the ~4-6 checkpoint milestones + the skill-unlock non-monotonicity test; converts §7/§8/§21 from unfalsifiable to measurable. **Gated on the flag #2 persistence-contract ruling** (below) for the +3-becoming band.
6. **The story-canon reconciliation pass** (III.9) — v2 vs prior cosmograph/earth-avatar/companion records, **PLUS the `design-decisions-session.md` §1 device-orphan rulings** (trickster-jab, layered-name, seven-gate descent, descent≠underworld: re-home onto Daikoku/Mahakala or retire — several fit the new sourcing better).
7. **The encounter-geometry seam-ownership ruling** (with drax + KR).

**Matt-ruling needed (surfaced 2026-06-29, Path A flag #2 — `00-index.md` §5):** **what banks across the roguelite reset?** `gameplay-loop-design.md` §8 keeps the **lieutenant-becoming as a persistent +3 gain ("you keep what you kill")**; §23.3 states the **champion-body is NOT kept at run-end.** Likely intent: the **roster/grimoire entry** (the record of who you became) banks; the **run-specific embodied power** resets. **This is a Matt ruling, not a gandalf call — and it gates III.2** (the +3-becoming band cannot be specced until the persistence contract is fixed). Surface to Matt before #5 fires.

**Recommended first move:** #1 (multi-actor keystone — kit-vs-kit + summoner) and #2 (horde) carry the most leverage; #2 has a clock on it (8-concurrent band lock-in); #3 is a fast brief that unblocks the build-depth un-gates. #4 unblocks the spine regardless. The **flag #2 persistence ruling** is a cheap Matt-ask that unblocks #5. Sequence per knight-rider; Matt approves.

---

## PART V — What genuinely fits (the honest picture)

So the survey is not all gaps:
- **The v2 frame fits cleanly** — death-faith / patron / home-realm touch no seam and improve the story; the theology-rhymes-with-mechanics is stronger than the isekai bridge.
- **The enemy-ontology split** (fodder monsters = MultiMesh; champions = CharacterBody3D) maps cleanly onto the Jolt+MultiMesh hybrid — a correct architecture call.
- **Elements are first-class and mechanical**; per-floor element rotation is real and validated.
- **The faction infrastructure** (clusters, relationships, 6-enum) is built — it just stays presentation-side (correctly).
- **The sim is more spatially capable** than the design doc assumes (real arenas, AoE shapes, flanking) — the *ambition* of spatial encounter design is supported.
- **The parametric-ability data layer** (16/24 primitives) already exists — the work is Godot-verb realization, not invention.
- **The faction-walled-from-combat invariant** is the engine being *right* — protect it.

**One operational note for drax:** the Godot prototype runs on Mac/Metal, which the perf doc names as the *flattering* machine. Looks-fine-on-Mac will not certify the GTX-1650 floor. Burn the density target into the drax workflow now.

---

**Signed:** gandalf, 2026-06-23 (founding entry). This doc is LIVING — the next gandalf session opens it at startup and updates it. The two completion targets (battle-sim, emission) and the v2-fit gaps (PART III) are the agenda until closed.
