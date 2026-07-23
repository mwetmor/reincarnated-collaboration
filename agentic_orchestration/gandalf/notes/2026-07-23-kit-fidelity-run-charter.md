# KIT-FIDELITY — Canon-Kit Mechanical-Replica Run (charter)

**Conductor:** gandalf `RUN-CONDUCTOR`. **Chartered:** 2026-07-23, on Matt's RL-6 ruling closing
REPLICA-1 (ledger: `agentic_orchestration/gandalf/notes/2026-07-22-replica-1-godot-sim-window-run.md`,
CLOSED at RL-6). **Predecessor:** REPLICA-1 (built the Godot sim-window; Matt watched; verdict below).
**Successor slot:** the boss-stack forks, DEFERRED behind this run at RL-6.
**Desirable-run-pattern fit:** §2 (all four questions YES). **Charter author conducts** (intent
residency): this charter was elicited from Matt's five fork rulings (§0), embedded verbatim below.

---

## §0 Why this run exists — FIDELITY, not policy (the blocker Matt named)

REPLICA-1 built a Godot "window" (`replica-frame/v1`) that renders the battle sim's own fights from
per-tick semantic frames. Matt watched BLIND + AWARE bowazon live and delivered the verdict that
closed the run: **the fight shape is degenerate.** All enemies immediately converge on the player's
point and clump; blind-vs-aware outcomes are decided by hair-level clustering differences against the
AOE blast radius (win = the clump fits inside; had the first burst not wiped 100%, the player dies in
milliseconds either way). His words: *"geometry and AI have nothing to do with what's happening"* at
the level that matters.

**Root cause, established IN REPLICA-1 (RL-3, Disc #11), accepted as the run's true finding:** the
ref-set `kit_id`s are **LABELS on the gate's neutral BC-cells.** `_build_martial_player_class`
synthesizes generic martial kits from canon *coordinates*; the mobs are synthetic too. Nothing
mechanical from the canon kit reaches the sim — no real skill, no real damage, no real defense. The
window did its job faithfully (his 2-fight eyeball MATCHED the 144-fight trace diagnostic); the
window showed that **the fighters are coordinate-parameterized shells, not mechanical replicas.**
Fidelity, not policy, is the blocker. AI testing is SHELVED (Matt).

**This run's thesis:** compile the canon RECORDS into **mechanically real sim fighters** — real
skills, real numerics, real monsters harvested from the source games — and make the fidelity
**measurable on screen.** Every damage floater reads `12,500 (87%)`: the realized RDR number, and
what percentage that is of the value the *original source game* would produce for the same hit. The
window becomes a **fidelity gauge** (§9). When mechanics + numerics are true, the gauge reads ≈100%;
any on-screen deviation is pipeline drift made visible. Matt's watch session becomes a **measurement
instrument**, not a taste check.

### §0.1 Matt's five fork rulings (verbatim — the charter's spine)

> **F1 —** *"select 5 that we have mechanics for."*
> **F2 —** *"moot due to F1."*
> **F3 —** *"We need to create the join key that will allow us to determine what each damage value as
> derived from our sim represents as a percentage of the expected value from the original source game.
> I would like to see the damage numbers as follows in the godot script: (sample for concept) 12,500
> (87%); the 87% is the percentage versus the expected RDR damage based on the calculated relationship
> to the original game's damage. And it should be the same for received damage (and % of expected)."*
> **F4 —** *"We selected these 5 games because we have the capability to access their databases which
> contain monster data! Once we gather the monster data from the respective database, we need to apply
> the join key to develop skills/stats and expected damage dealt/taken."*
> **F5 —** *"yes"* (the replica window rides along as standing instrumentation — every gate's output
> visible in it).

**The five games are the corpus's own record-bearing games** — the only five with mechanics AND
accessible source databases: **poe1 · poe2 · d2 · gd · le.** F1 selects five KITS from these; F4
harvests MONSTERS from these five databases. F2 is moot because F1 already bounds the kit pool to
what we have mechanics for.

---

## §1 Substrate facts (PINNED — all verified by conductor probes 2026-07-22, `corpus.db` READ-ONLY
except where a gate populates a NAMED table)

`corpus.db` at `agentic_orchestration/research/curated/corpus.db`.

- **267 `corpus_class='record'` rows** in `canon_corpus`: **poe1 94 · d2 60 · gd 41 · le 36 ·
  poe2 36.** (Per-game via `kit_id` prefix census; conductor-verified.)
- **`kit_mapping.mapping_json` 267/267** (skills / motion_frame / resource_economy / trigger_grammar /
  t4_doors / scaffold).
- **`skill_geometry_band` 265/267 · `recognition_hook` 265/267.**
- **`canon_probe_facts` 4780 rows** across 10 families (delivery / footprint / control / defense /
  economy / element / movement / geo_text / rank1_upgrade / sources_used).
- **`kit_citations` 1287.**
- **`mechanic_gap_docket` — 43 OPEN + 19 matt-ratified,** keyed by `mechanism_class`, with
  `evidence_kits` (JSON array) + `source_kit_id`. **This is the KF-1 disqualifier.**
- **F3 rails — both exist, both confirmed:**
  - **`kit_numeric`** — 10 cols. `source_value` REAL **IMMUTABLE** (with `source_anchor` verbatim
    quote), `source_scale`, `rdr_value` REAL **DERIVED** ("*sim reads THIS only*"; NULL until a rule
    runs), `rule_id` → `normalization_rule`, `rule_version_applied` (staleness), `verify_ledger_id`.
    Currently **2 seed rows** (`poe1-glacial-hammer` more_damage_390, `poe2-walking-calamity`
    more_frequent_200), both with **`rdr_value` NULL, `rule_id` NULL.**
  - **`normalization_rule`** — `rule_id` (e.g. `N-D3-SET-01`), `rule_version` (bump → corpus-wide
    re-derive of dependents), `source_scale`, `rule_owner` (**= sim-seam sign-off**, gamora/star-lord),
    `formula_ref` (pointer, not inline math), `status` proposed/active/superseded. Currently
    **0 rows.**
  - **`kit_acceptance_assert`** — EXISTS (310 rows already), with `assert_text`, `expected_state`,
    `last_result` green/red/untested, **`routed_docket_id`** (red-test doctrine: red assert → docket).
    **KF-4's per-kit acceptance asserts have a home.**
- Also present: `kit_dossier`, `verify_ledger`, `door_registry`, `kit_door_arg`, `canon_engine_key`,
  `kit_deviation`.

### §1.1 Engine + Godot state (PINNED)

- Engine HEAD **`2f43045`** + one **unpushed** gamora commit **`1564e2f`** — the REPLICA-1 frame
  emitter (`src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py` + `spatial_engine.py`
  `frame_sink`/`on_hit` hooks; observability-only, default-off). **Gate-2 PASSED** (jack-ryan finding
  `agentic_orchestration/qa/findings/2026-07-22-gate2-replica1-frame-emitter.md`).
- **This run BUILDS ON that emitter.** `replica-frame/v1` is **additive-only within v1** (spec §6) —
  so `expected` + `pct` fields on `damage` events are **legal additive extensions, no version bump.**
- Godot playback scene landed (drax **`90d79c5`**).
- **Engine + Godot pushes are QUEUED on Matt** (non-blocking for this run — frames are local; note
  carried, not gated).

---

## §2 Desirable-pattern fit test (all four YES — pattern doc:
`agentic_orchestration/operating-procedures/desirable-run-pattern.md`)

- **F1 — Enumerable?** **YES.** Bounded substrate = **the pilot-5 kits' `canon_corpus` records +
  their `kit_mapping` skill lists + per-game STARTER monster sets** — every element a finite,
  listable enumeration, **frozen at KF-gate entry.** The kit pool is 267 records; the pilot is 5;
  the monster harvest is bounded to *starter sets* (mobs appearing in pilot encounters), not full
  bestiaries. Countable, listable, diffable.
- **F2 — Decidable?** **YES.** Every gate KF-1..KF-7 has a **decidable exit predicate** the run
  checks without Matt (§3): rows populated / rules ACTIVE / `rdr_value` non-NULL / acceptance asserts
  green / headless harness green. Where doneness needs judgment (what "expected" means, the % gauge
  denominator), that judgment is converted **pre-launch** into PINS A + B (§4), ratified by Matt at a
  named commitment-boundary.
- **F3 — Pre-drainable?** **YES.** The five forks were drained by the ELICITOR pass into Matt's five
  rulings (§0.1). Residual forks are **reasoning-boundaries** (rule formula details, per-game harvest
  source, compiler mapping, `numeric_key` naming) — ruled in-run veto-open. The two genuine
  *commitment*-boundaries (Pins A/B) are surfaced as PROPOSED-pending-Matt (§4), not assumed.
- **F4 — Authority-resident?** **YES.** The conductor (gandalf) holds design authority for the
  residual reasoning-boundaries; the *numeric* sign-offs route to `rule_owner` (gamora/star-lord
  sim-seam) per the `normalization_rule` schema; jack-ryan Gate-2 gates every engine diff;
  Matt holds Pins A/B + all commitment-boundaries (§7).

---

## §3 Gates KF-1..KF-7 (decidable exit predicates + executor seams)

Sub-agent routing per the conductor-economics corollary (pattern §2.1): pieces route to **NAMED**
agents in their seams; the conductor writes no production code.

### KF-1 — Pilot-5 selection (conductor + named-gandalf)

**Instrument:** from the 267 records, **DISQUALIFY** any kit cited in **any of the 43 OPEN dockets**
(appears in a docket's `evidence_kits` JSON array OR as its `source_kit_id`) — an open docket means
the mechanism is not yet resolved, so the kit cannot be compiled truthfully. **RANK** the survivors by
**(a) `kit_mapping` completeness** (all six mapping facets present) **× (b) damage-data source
coverage** (does the kit have `kit_numeric` seed rows and/or `kit_citations` with anchored damage
quotes, so a join key CAN be derived). Aim for **cross-game spread** where the top ranks permit (not
5 poe1 kits) so the harvest exercises multiple source databases (F4). **The mismatch-degenerate
REPLICA-1 cells are NOT auto-carried** — they were labels; the pilot is selected fresh on mechanics.

**Exit predicate:** a ranked candidate list exists with the top 5 named + 3 next-ranked reserves
(fallback pool, §5); each of the 5 passes: not-in-open-docket ∧ mapping-complete ∧ has-derivable-
damage-source. **Output = a self-contained selection-evidence brief to Matt** (§6): the 5 kits, why
each (mapping + damage coverage), the reserves, and the disqualified-notables — readable in-chat, no
doc-spelunking (RL-6 binding). Matt sees the pilot before mechanization spends.

### KF-2 — Join-key registry population for the pilot 5 (elrond curation + gamora/star-lord sign-off)

Build the **join key** F3 requires: the calculated relationship between each source-game damage value
and its RDR equivalent, so a realized sim number can be expressed as a % of expected.

- **elrond** curates the pilot kits' `kit_numeric` rows: `source_value` IMMUTABLE with `source_anchor`
  verbatim quote (kit-side anchored-source discipline), `source_scale` named.
- **gamora/star-lord** (the `rule_owner` seam) author the `normalization_rule` rows: the source_scale →
  RDR transform, `formula_ref` pointing at the transform script (not inline math), then derive
  `rdr_value` for every pilot `kit_numeric` row.
- **DUAL-COLUMN DISCIPLINE HELD:** `source_value` never mutates; `rdr_value` is derived; the sim reads
  `rdr_value` only. A `rule_version` bump re-derives dependents.

**Exit predicate:** for all pilot-5 kits — every `kit_numeric` row has **`rdr_value` non-NULL**, its
`rule_id` points to a `normalization_rule` with **`status='active'`** and `rule_owner` sign-off
recorded, and `rule_version_applied` matches the active rule version. `source_value` bit-unchanged
from KF-2 entry (dual-column audit).

### KF-3 — Monster harvest (legolas Mode B → elrond curation → join key applied)

F4: harvest monster data from the five source-game databases; apply the join key to develop monster
skills/stats/expected dealt + taken.

- **legolas Mode B** over the five source-game databases (poe1 · poe2 · d2 · gd · le), **BOUNDED to
  starter sets** = the specific mobs that appear in the pilot encounters (§5 bound), NOT full
  bestiaries. Read-only crawl; anchored sources.
- **elrond** curates the harvest into **new monster tables** mirroring the kit-side anchored-source
  discipline (`source_value` IMMUTABLE + verbatim anchor; `rdr_value` derived) — schema is an
  **additive** `MIGRATION` (new tables, no existing-column change; non-additive schema change is a
  commitment-boundary HALT, §7).
- The **join key** (KF-2 rules, extended for monster scales as needed — new rules, `rule_owner`
  sign-off) develops each monster's skills, stats, and **expected damage dealt / taken.**

**Exit predicate:** every starter-set monster used by a pilot encounter has curated stats + skills +
`rdr_value`-derived expected-dealt and expected-taken, under active `normalization_rule`s with
`rule_owner` sign-off; anchors present; harvest bounded to starter sets (bestiary excess logged as a
next-lap admission, never silently pulled).

### KF-4 — Kit compiler (gamora/rocket: canon record → sim fighter)

Replace label-synthesis with mechanical compilation **for the pilot only.**

- **gamora/rocket** build a compiler: a pilot kit's `canon_corpus` record + `kit_mapping` skills +
  `kit_numeric` `rdr_value`s → a **real sim fighter** with real skills (geometry/range/element from
  `skill_geometry_band`), real damage (from `rdr_value`), real resource economy.
- **`_build_martial_player_class` label-synthesis is RETIRED for the pilot** (the shells that caused
  the degenerate shape). Non-pilot kits still route through the old path — no corpus-wide engine
  churn; this is a bounded compilation seam.

**Exit predicate:** for each pilot kit, its **`kit_acceptance_assert` rows are GREEN** (the table
exists; asserts of the form `projectiles_per_cast == N`, `primary_geometry == 'line'`, etc., authored
against the canon record and evaluated against the compiled fighter). A red assert routes to a docket
per the red-test doctrine (`routed_docket_id`) and triggers a pilot SWAP (§5) — never a silent
mechanic invention.

### KF-5 — Expected / pct plumbing (gamora: sim computes; jack-ryan Gate-2)

The SIM computes `expected` and `pct` per hit (zero-derivation law, §8) per Pins A/B.

- **gamora**: at each resolved hit, the sim computes **`expected`** (per Pin A) and **`pct`** =
  realized `rdr_value` / expected (per Pin B denominator), for BOTH dealt and received. The
  `replica_frame_emitter` carries **additive** `expected` + `pct` fields on the `damage` event
  (v1-additive, no version bump). Observability-only; default-off; ZERO combat-logic change in the
  same commits (the REPLICA-1 emitter discipline).
- **jack-ryan Gate-2** on the engine diff (BLOCK authority): zero-combat-logic-change confirmed,
  determinism byte-identical (same seed → same trace incl. new fields), non-finite guard on the new
  floats.

**Exit predicate:** emitted `damage` events carry `expected` + `pct` for dealt AND received; Gate-2
PASS on the engine diff; determinism gate green.

### KF-6 — Godot floaters `12,500 (87%)` dealt + received (drax)

- **drax**: the playback scene renders the floater as **`<rdr_value> (<pct>%)`** exactly per F3
  ("12,500 (87%)") for **both dealt and received** damage — reading `amount`/`expected`/`pct`
  straight from the frame (zero-derivation, §8: the window DISPLAYS; the sim COMPUTES).
- **Precondition (separate fix agent already on it):** the REPLICA-1 fight-picker defect (app ends
  after the second fight, RL-6) is being fixed alongside the `/canon` serving fix; the KF watch needs
  the picker working. Non-blocking for KF-1..KF-5; gates only KF-7.

**Exit predicate:** headless harness GREEN (0 errors / 0 leaks); a pilot fight loads and shows
`N (pct%)` floaters for dealt and received; picker advances across pilot fights.

### KF-7 — Matt watch session (the fidelity-gauge instrument)

**drax scene + KF-2/3/4/5 outputs all live in it.** Matt watches the pilot-5 kits fight harvested
starter-set monsters, floaters reading `12,500 (87%)` dealt + received.

**Exit predicate:** Matt watches; **acceptance is his own inspection verdict** — he can read the
gauge and say where fidelity holds (≈100%) and where the pipeline drifts (deviation). **Output = a
self-contained watch brief + controls card** (§6): what he's seeing, how to read the gauge, the
scrubber controls — readable in-chat, no doc-spelunking (RL-6 binding).

---

## §4 PINS A + B (PROPOSED-pending-Matt — commitment-boundary, §7)

The one place "expected" and the "%" gauge need a definition that is taste, not derivable. Both are
surfaced as PROPOSED with a stated conductor lean; **Matt ratifies** (answering them myself is the
ELICITOR failure).

- **PIN A — what "expected" MEANS.** **Conductor lean: crit-weighted mean roll (full expectation) at
  the documented build point** — i.e. expected = the statistical mean of the source game's damage for
  that hit including crit contribution, evaluated at the specific character build the kit's record
  documents. *Alternative:* non-crit mean roll (ignores crit; simpler, but understates a
  crit-centric kit's true expectation and would make the gauge read low for crit builds).
  **Lean rationale:** the gauge should compare against what the source game actually PRODUCES on
  average, and crit is part of that production; a crit-weighted mean is the honest "expected value of
  the original game's damage" F3 asks for.
- **PIN B — the floater `%` denominator.** **Conductor lean: use the actual target's normalized
  defense at hit time (live, whole-pipeline gauge)** — the pct compares realized RDR damage against
  expected *for the real target as it stands this hit*, so the gauge measures the WHOLE pipeline
  (kit numerics × monster defense × compilation), catching drift anywhere. **PLUS a fixed
  reference-dummy pct computed internally** as a run-gate instrument (an invariant baseline that
  isolates kit-side drift from target-side variance — used to gate KF-2/KF-5, not necessarily shown).
  *Alternative:* dummy-only floater (show the pct only against a fixed reference dummy) — cleaner,
  invariant number, but hides target-defense-driven drift, which is exactly the fidelity the run
  wants visible. **Lean rationale:** the live denominator makes the watch session a whole-pipeline
  measurement; the internal dummy keeps a stable gate signal.

**Both pins ratify at the KF-2-entry Matt brief** (they gate what KF-2/KF-5 compute). Veto-open once
ratified.

---

## §5 Pre-registered honorable fallbacks (pinned before results — the run cannot grow scope silently)

- **Pilot-kit SWAP.** If a pilot kit's damage data proves too sparse to derive a join key mid-run
  (KF-2), OR a `kit_acceptance_assert` goes red on a mechanic the compiler can't truthfully build
  (KF-4), **swap in the next-ranked reserve** from KF-1's list. Documented in the ruling ledger;
  never patched by inventing numbers.
- **Starter-set-not-bestiary bound on harvest (KF-3).** The monster harvest is bounded to mobs
  appearing in pilot encounters. Any richer bestiary data legolas surfaces is a **next-lap
  admission**, logged, not pulled into this run.
- **Mechanic discovered gapped mid-run.** If compilation hits a mechanism the sim genuinely does not
  model (the R-1..R-4 engine-frontier territory), the disposition is: **new `mechanic_gap_docket`
  row** (mechanism_class + evidence_kits + source_kit_id) **+ pilot SWAP** — **never** silent scope
  growth and **never** engine-mechanic improvisation. Compiling EXISTING mechanics is in scope;
  ADDING a mechanic is out (§7).
- **Playback stall fallback (inherited).** If live Godot playback stalls, batch MP4 renders from the
  same frames via drax's walkthrough harness — Matt still watches the fidelity gauge this cycle.

---

## §6 Declared Matt interface (RL-6 lesson BINDING: no decision point requires opening a doc)

- **Self-contained in-chat briefs at exactly three points:** **KF-1** (pilot selection — the 5, the
  why, the reserves), **Pin A/B ratification** (at KF-2 entry — the two definitions, leans,
  alternatives, consequence), **KF-7** (watch — what he's seeing + how to read the gauge + controls
  card). Each brief carries options + context + consequence **readable in-chat**; a fork table that
  points into a long doc is a failed interface (RL-6, Matt: *"I honestly can't find the information
  needed to rule"*).
- **Red-flag pings only** otherwise.
- **Push-as-you-go on the collab repo** (charter + ledger + briefs commit-and-push as produced).
- **Engine + Godot pushes QUEUED on Matt** (the REPLICA-1 emitter `1564e2f` + Godot ahead-of-remote +
  this run's KF-5 engine diff + KF-6 Godot diff) — non-blocking for the run (frames + registry are
  local); carried as a Matt push-queue note, ruled at Matt's timing.

---

## §7 Halt taxonomy (pattern §4 — the distinction that separates the run histories)

**Commitment-boundary HALT (Matt-reserved / Gate-2 / committed-truth / external danger):**

- **Pins A + B ratification** (§4) — definitional taste, Matt's call.
- **Any non-additive schema change** — new tables are additive (allowed under `MIGRATION`); renaming/
  removing/retyping an existing column, or a `replica-frame` MAJOR bump, HALTS to Matt.
- **Any engine-MECHANIC addition beyond compilation of existing mechanics** — the R-1..R-4 frontier
  (new projectile-flight ticks, new avoidance branch, a mechanism the sim doesn't model) is **OUT of
  scope**; discovering the need is a docket + swap (§5), not an in-run engine capability build.
- **jack-ryan Gate-2 BLOCK** on any engine diff (KF-5, and any KF-4 engine touch).
- **decisions-log / committed-truth contradiction**, external-state danger.

**Reasoning-boundary HALT (conductor rules in-run, veto-open, logged) — the failure this run
eliminates:**

- `normalization_rule` **formula details** (the source_scale → RDR transform math) — ruled with the
  `rule_owner` sim-seam, veto-open.
- **Per-game harvest source selection** (which table/endpoint in each source database) — legolas
  Mode B call, ruled in-run.
- **Compiler mapping details** (how a specific `kit_mapping` facet becomes a sim skill parameter) —
  gamora/rocket, ruled in-run.
- **`numeric_key` naming** and acceptance-assert wording — curation calls, ruled in-run.

The founding exemplar (pattern §4): a reasoning-boundary that formerly killed runs is now ruled
in-run under the run's own gates + jack-ryan; only genuine commitment-boundaries reach Matt.

## §8 Zero-derivation law (restated for the new fields)

The **SIM computes `expected` and `pct`**; the **window only DISPLAYS them.** The Godot scene reads
`amount` / `expected` / `pct` from the frame and renders `<rdr_value> (<pct>%)` — it never recomputes
expected, never recomputes the ratio, never rolls damage, never selects targets (REPLICA-1 spec §7,
inherited whole). If the renderer needs a value to show the gauge that isn't in the frame, that is a
**schema field to add in v1 (additive) + re-emit** — never a Godot computation. There is no second
combat implementation; fidelity is exact **by construction**.

## §9 The fidelity-gauge meaning (why the watch session is a measurement instrument)

At **true mechanics + true numerics**, the gauge reads **≈100%** — realized RDR damage equals the
expected value derived from the source game. **On-screen deviation = pipeline drift made visible:** a
kit reading 60% means its numerics or compilation lost fidelity somewhere between the anchored
`source_value` and the realized hit; a monster's received-damage % drifting means the harvest or the
join key is off for that mob. The watch session (KF-7) stops being a taste check and becomes a
**diagnostic read of where the compilation pipeline is faithful and where it drifts** — which is
exactly the instrument REPLICA-1's degenerate-shape verdict demanded. The window Matt already has
becomes the acceptance instrument of THIS run once real kits fight real monsters in it.

---

## Ruling ledger

*(Format per REPLICA-1: dated, decidable, veto-open.)*

- **KFL-1 (2026-07-23, conductor): CHARTER RATIFIED + RUN LAUNCHED at KF-1.** DRIFT-CRITIC pass
  complete: substrate facts re-verified against live corpus.db, including the authoring agent's
  load-bearing correction (`kit_acceptance_assert` already holds **310 rows** with `routed_docket_id`
  — KF-4's exit is therefore "pilot asserts GREEN," not "table exists"; conductor re-probed, confirmed).
  Three authoring tensions reviewed + accepted: five-games identity (§0.1 tail), assert-table state
  (§1), Pin-B two-headed resolution (§4 — flagged for Matt's scrutiny at ratification). KF-1 fires
  immediately (read-only selection analysis; its output IS Matt's first brief). Pins A/B were offered
  to Matt in-chat ahead of the KF-2-entry gate; the gate still binds if unanswered. Veto-open.
- **KFL-2 (2026-07-23, conductor): KF-1 EXECUTED + VERIFIED — exit predicate MET.** Named-gandalf
  selection (evidence: `2026-07-23-kf1-pilot-selection-evidence.md`, commit `46f7b1ac`). Conductor
  spot-probes: open-docket kit census = **43 exact**; **pilot-5 ∩ open-docket-kits = ∅**;
  le-frost-claw citation softness confirmed (2 cites). **Pilot:** d2-firewall-sorc ·
  gd-flames-of-ignaffar-purifier · poe2-bonestorm · poe1-cyclone · le-frost-claw. **Reserves:**
  d2-ww-barb · d2-fire-sorc (the LE-swap) · poe1-frost-blades. Selection brief delivered to Matt
  in-chat (§6 brief 1); roster ratification is Matt's, with one named sub-decision (LE-spread vs
  d2-fire-sorc swap). Veto-open.
- **KF-2..KF-7:** pending. KF-2 entry gates on Matt: roster + Pins A/B.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
