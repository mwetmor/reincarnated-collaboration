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
- **COMPOSITION LEDGER (KFL-7 fold — Matt's join-key completeness audit):** per pilot kit, per
  direction (dealt / received), elrond records the **expected-value composition** — the factor chain
  `base × skill/mastery modifiers × hit-chance × crit-EV × (1 − target mitigation)` — with every
  factor marked **ANCHORED** (verbatim source) / **PINNED** (charter ruling, e.g. D2 spells-no-crit)
  / **GAP-EXCLUDED** (named, never estimated). **Resolution FORMULAS are first-class harvest targets
  under the same anchor law as values** — any hit/crit/mitigation formula a `normalization_rule`
  applies must carry its own verbatim anchor (gd's PTH + crit-tier + armor-absorption harvest is the
  exemplar; the d2/poe1/poe2 formula anchors are the KFL-7 residual lane).

**Exit predicate:** for all pilot-5 kits — every `kit_numeric` row has **`rdr_value` non-NULL**, its
`rule_id` points to a `normalization_rule` with **`status='active'`** and `rule_owner` sign-off
recorded, and `rule_version_applied` matches the active rule version. `source_value` bit-unchanged
from KF-2 entry (dual-column audit). **Composition ledger complete** for all 5 kits, both
directions — no unlabeled factor; every formula referenced by an active rule is anchor-backed.

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

**Gauge basis + GAP rule (KFL-7):** the floater gauge's time basis is **per-hit / per-tick** (channel
+ DoT tick models named in the composition ledger) — never DPS; mob attack rate shapes pacing, not
the join-key denominator. Where a factor is GAP-EXCLUDED, the % computes over the declared factors
only and the exclusion is named in the KF-7 watch brief — **no silent estimation ever fills a GAP.**
Where a player defensive sheet is GAP at build point, the fallback ladder is: source-game
**base-at-level** values (anchorable formulas) → else the received-% renders **pre-mitigation** and
says so.

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
- **KFL-3 (2026-07-23, Matt in-chat + conductor): KF-2 ENTRY GATE CLEARED — all rulings received.**
  **(a) ROSTER APPROVED** as proposed (the 5 + reserves). **(b) LE CONDITIONAL (Matt):** keep
  le-frost-claw; **swap to d2-fire-sorc iff the LE database proves insufficient at KF-2**
  (insufficiency = the frost-claw numeric sheet cannot be fetched with verbatim anchors).
  **(c) PINS A + B RATIFIED** as leaned. **(d) FULL-SHEET SCOPE RULED (Matt):** the join key covers
  the COMPLETE numeric surface per kit — per-skill (geometry/damage/modifiers), character attributes
  (str/int/vit/dex-equivalents), damage modifiers (crit chance/multi), mitigation (dodge/armor/
  resists/block) — and the gauge stack is three-deep: **pre-mitigation per-skill expected %** ·
  **post-mitigation floater %** (Pin B live) · **per-hit received %** — all vs source.
  **Conductor amendment (veto-open):** the internal gate instrument becomes the PRE-MITIGATION %
  (supersedes the fixed-reference-dummy formulation — same intent, cleaner: pre-mitigation is
  mitigation-free by definition; Matt's own enumeration named it). **Conductor ruling
  (reasoning-boundary, veto-open):** pilot-encounter frame = pilot kit vs a starter set from ITS OWN
  source game (source-matchup fidelity); starter set = 3–5 iconic, well-documented, early-accessible
  mobs per game. **KF-2 + KF-3 LAUNCHED** as one combined game-by-game harvest lane (legolas Mode B →
  elrond curation; incremental per-game commits so a stall loses nothing). Out-of-run: /canon
  header-band overlap defect (Matt live report) → drax fix fired.
- **KFL-4 (2026-07-23, Matt in-chat + conductor): PUSH-AS-YOU-GO + LE SWAP EXECUTED.**
  **(a) Push-as-you-go AUTHORIZED (Matt, verbatim "push as you go")** — the §6 Matt-queued seam
  pushes are RETIRED for this run: conductor flushed the standing queue (engine `1564e2f` · godot
  `90d79c5`+`df7857e` · loadout `f869d45`+`1bc9737`, all pushed 2026-07-23) and henceforth pushes
  seam commits as they are verified, alongside the existing collab push-as-you-go.
  **(b) LE INSUFFICIENT — SWAP EXECUTED per KFL-3(b) pre-authorization.** legolas evidence
  (`agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-le.md`, commit `c9c09df3`,
  conductor-verified): lastepochtools.com (sole structured LE DB) HTTP-403s all endpoints; wiki 402;
  16 reachable sources all strategy-level; full-sheet gap table = GAP on every anchor-grade field.
  Clean INSUFFICIENT under anchor law. **Pilot roster now: d2-firewall-sorc · d2-fire-sorc ·
  gd-flames-of-ignaffar-purifier · poe2-bonestorm · poe1-cyclone.** Consequence accepted (was
  priced in the KF-1 brief): cross-game spread drops to 4 source games (d2 ×2); LE unexercised
  this lap — logged as a next-lap admission, not silently re-scoped. d2-fire-sorc harvests under
  the d2 game pass; LE monster harvest moot.
  **(c) Out-of-run:** /canon band residual (Matt live report: "still not fit to the top of the
  square") → second drax fix agent fired (v1.16, empirical geometry probe, push authorized).
  **(d)** Run-doc + desired-end-state brief delivered in-chat (Matt asked; §0/§9 + gate exits are
  the answer of record). Veto-open.
- **KFL-5 (2026-07-23, conductor): HARVEST WAVE-1 VERIFIED (4/5 games) + RESIDUAL LANE FIRED.**
  First harvest agent died on a stream idle timeout mid-gd; **the incremental-commit discipline
  held — zero loss** (le verdict `c9c09df3` · d2 `6c3ede65` · poe1 `5dd10598` · poe2 `4b2a27ea`,
  all conductor-verified + pushed). **Trust-but-verify finding (load-bearing):** the d2 note's
  swap-kit claim ("d2-fire-sorc overlaps substantially — Fire Wall primary in both") is
  **CONTRADICTED by corpus** — `kit_mapping` for d2-fire-sorc = **Fire Ball + Meteor**; the swap
  kit's skill sheet is NOT yet harvested. **Conductor ruling (reasoning-boundary, curation-call,
  veto-open): poe1-cyclone version pin = 3.15 era** — the corpus citation (3.15 league-starter
  thread, 59% effectiveness at gem 20) IS the documented build point the join key measures against;
  current poedb (150%, post-3.27 buff) filed as context only. Era re-pin would require a
  `kit_citations` amendment first — out of this run. **Residual legolas agent fired**, scoped to:
  (1) gd — Flames of Ignaffar kit sheet + Act-1 Normal starter set; (2) d2-fire-sorc supplement —
  Fire Ball + Meteor tables, correcting the overlap claim on record (shared d2 substrate — Fire
  Mastery / base attributes / FCR / Act-1 mobs — referenced, not redone). Veto-open.
- **KFL-6 (2026-07-23, Matt in-chat + conductor): WATCH-SURFACE ADDITIONS — Matt's four items
  registered.** **(a) CONFIRMED already-pinned:** expected + % gauges run BOTH directions (player-kit
  dealt AND monster dealt / player received) — F3 verbatim + the KFL-3 three-deep stack; no scope
  change. **(b) /canon FULL-SHEET display (NEW — KF-6b, drax):** after KF-2 populates, the loadout
  app's canon kit pages render the complete numeric sheet — dual-column `source_value | rdr_value`
  per skill + expected damage, attributes, crit, **mitigation (Matt: especially important)**, and
  **health** — a thin read of `kit_numeric` + rules; no derivation in the app. **(c) HEALTH GLOBE
  (NEW — KF-6, drax + gamora):** in-scene genre-idiom globe per fighter side: live current/max fill
  + **max-HP fidelity % vs source expected**; frame carries hp/expected-hp additively (sim computes,
  globe displays — §8 law). **(d) SKILL HOT-BAR (NEW — KF-6, drax + gamora):** hot-bar visualizing
  the auto-battle's skill selection/use timing — compiled-kit skill slots, flash-on-use,
  cooldown/channel state — driven by skill-use/intent events in the frame (additive field if v1
  lacks a distinct use-event). Executor split: gamora emits, drax renders; jack-ryan Gate-2 rides
  the engine diff per KF-5. Veto-open.
- **KFL-7 (2026-07-23, Matt in-chat + conductor): E1–E5 APPROVED + JOIN-KEY COMPLETENESS AUDIT
  FOLDED + HARVEST 5/5 LANDED.**
  **(a) KING-TWIN ELICITATION RULED (Matt verbatim: "All leans approved for E1-E5"):** separate
  chained charter + overlap-start (E1) · one mapping-table brief, all kits + mobs, single ruling
  pass (E2) · ONE arena from the king-scene environment grammar (E3) · five-element twin
  decomposition as the decidable core (E4) · KF-7 watch venue = best-available (E5). Named-gandalf
  charter author fired; charter lands RATIFIED-elicitation at
  `agentic_orchestration/gandalf/notes/2026-07-23-king-twin-run-charter.md`; conductor DRIFT-CRITIC
  pass gates its launch (KFL-1 precedent). Substrate evidence: Synty census `5ad6805f` (NO BLOCKER;
  quill-rat gap named).
  **(b) Residual harvest VERIFIED:** d2-fire-sorc supplement `7785651c` (corpus-corrected: Fire
  Ball + Meteor) · gd kit `d4eacc63` + gd monster `d28cc324`. Stall #2 lesson codified: the combined
  residual agent died having written NOTHING (fetched tables lost); relaunched as two narrow
  **write-as-you-go** agents (create file first → append per fetch → commit per sub-scope →
  fail-twice = GAP row + move on → hard fetch caps) — both landed. Write-as-you-go is the
  harvest-agent law of this run. gd monster side = FULL GAP (grimtools JS-rendered; fandom 402)
  with documented unblock paths; FoI rank table same blockage.
  **(c) JOIN-KEY COMPLETENESS AUDIT (Matt's ask: any un-folded piece of damage + mitigation?):**
  **FINDING — mitigation/hit RESOLUTION FORMULAS were unanchored for 3 of 4 games** while their
  VALUES are anchored (loudest case: poe1 zone-68 mobs carry 28,790–35,988 armour verbatim, but no
  armour→reduction formula anchor existed and Cyclone is physical — unformalized, the dealt-%
  drifts ×2–5 silently). **FOLDS:** composition ledger added to KF-2 (exit predicate extended) ·
  formulas ruled first-class anchor targets · §9 gauge basis pinned per-hit/per-tick + GAP-display
  rule + player-defense base-at-level fallback ladder. **Residual formula-anchor lane FIRED
  (legolas):** poe1 armour-DR + evasion/accuracy chance-to-hit formulas · poe2 armour formula +
  spells-unevadable check · d2 chance-to-hit (AR/DEF/level term) + spells-always-hit + sorc
  life-per-level/per-vitality coefficients + starter-mob AR columns + firewall tick retry · gd
  unblock attempt via community data-dump (GitHub CSV) route for monster stats + FoI rank table
  (bounded; fail → decision-shaped fallback to Matt). Veto-open.
- **KFL-8 (2026-07-23, conductor): FORMULA LANE VERIFIED + COMPOSITION PINS + GD FORK QUEUED +
  KF-2/KF-3 CURATION FIRED.**
  **(a) Formula-anchor lane landed** (`2026-07-23-kf23-harvest-formulas.md`, commits `85f61e49` /
  `9e7f7140` / `c894ca53`, conductor spot-verified + pushed). ANCHORED verbatim: poe1 armour-DR
  `Armour/(Armour + 10×PhysRawDmg)` cap 90% + the full phys-reduction layer composition +
  evasion-attacks-only ("doesn't work against spell hits") · **poe2 evade-ANYTHING** ("able to evade
  any incoming projectile or strike… whether… an arrow… or a fireball," AoE exempt) — **LOAD-BEARING
  CORRECTION** to the audit's spells-always-hit assumption: Bonestorm's projectile component IS
  evadable; only the AoE explosion is exempt · **d2 chance-to-hit**
  `min(max(200%×(AR/(AR+Dr))×(ALVL/(ALVL+TLVL)),5%),95%)` + mob AR columns confirmed (Fallen 8,
  Zombie 8). GAPS held honestly: poe2 armour formula (B1, sources blocked) · d2 blanket
  spell-bypass verbatim (C2) · firewall tick (C5) · gd data-dump route exhausted (D — GitHub carries
  extractor TOOLS, no static data).
  **(b) Conductor pins (reasoning-boundary, veto-open):** **PIN-C2:** D2 fire-skill hit-chance = 1,
  status PINNED-not-anchored (skill tables carry no AR interaction; named bypass-skill list exists;
  blanket verbatim unfindable) · **PIN-C3:** maxroll = primary precedence for D2R numerics (dedicated
  D2R platform; prior d2 harvest already maxroll-cited); the fextralife life-coefficient conflict
  stays dual-anchored on record, Gate-2-reviewable · **PIN-N10:** poe2-bonestorm N_shards = 10
  (documented-build midpoint; harvest recommendation, conductor-concurred) unless an anchored count
  supersedes · **composition consequences:** poe2 armour factor = GAP-EXCLUDED (dealt-% renders
  pre-armour, named); poe2 composition splits projectile (evadable) vs explosion (AoE-exempt) per B2.
  **(c) GD FORK — QUEUED TO MATT (decision-shaped, next engagement; commitment-boundary: roster
  consequence).** FoI per-rank table + ALL gd monster stats are unanchorable read-only (grimtools
  JS-rendered · fandom 402 · data-dump route exhausted). Without the rank table the gd kit cannot
  compile its primary skill from anchors — charter §5 swap territory. Options: **(A)** authorize a
  local GD-extractor lane against a local GD install (highest-grade anchors; needs Matt install
  confirmation + code-execution authorization) · **(B)** Matt in-game tooltip captures, transcribed
  under capture-anchors · **(C)** §5 swap to next reserve (d2-ww-barb / poe1-frost-blades), gd a
  next-lap admission (roster drops to 3 source games). Conductor lean: A if the install exists,
  else C. **gd kit HELD at KF-2** (character formulas curate; rank-table rows stay GAP); the other
  4 kits proceed — the fork does not block the run.
  **(d) KF-2 + KF-3 CURATION LANE FIRED (named-elrond):** kit_numeric population (4 kits + gd
  partial) · monster tables via additive MIGRATION (d2 / poe1 / poe2) · composition ledgers per kit
  per direction (ANCHORED/PINNED/GAP-EXCLUDED) · rules-needed manifest handing off to gamora/
  star-lord for the normalization-rule lane. Veto-open.
- **KFL-9 (2026-07-23, conductor + Matt in-chat): CURATION VERIFIED + GD FORK RULED (A-DEFERRED) +
  RULES LANE FIRED.**
  **(a) elrond KF-2/KF-3 curation VERIFIED + pushed** (commits `ab05dd8b` / `d4d9c7f1` / `2fdd48f5` /
  `bef71fa3` / `706f4731`): kit_numeric **444** new rows (firewall 106 · fire-sorc 188 · cyclone 20 ·
  bonestorm 104 · gd 26; the 2 pre-existing seed rows untouched) · monster_numeric **145** (d2 58 /
  poe1 58 / poe2 29) · kit_composition **61** (ANCHORED 33 / PINNED 7 / GAP-EXCLUDED 21) · dual-column
  law held (ZERO non-NULL `rdr_value`; `normalization_rule` 0 rows — elrond authored none) ·
  conductor spot-probes exact vs harvest verbatims (bonestorm gem-20 116–175 / 89–134 + Int 157 +
  mana 61; rhoa armour 35,988; Fallen AR 8 + resists) · DB byte-identically rebuildable from
  committed `.sql` (idempotency re-run clean) · GD formula-expressions-vs-REAL-column anomaly handled
  without improvisation (scalar constants in kit_numeric; formula expressions verbatim in composition
  refs + manifest — nothing forced, nothing dropped). Rules-needed manifest
  (`elrond/notes/2026-07-23-kf23-rules-needed-manifest.md`) verified complete: 26 rule families
  (A–H), BLOCKED rules named (R-K5 + R-N5 gd; R-G4 poe2-armour GAP-B1), context rows fenced
  (`_v327_context` NOT-for-derivation), PIN-N10 as fixed multiplier.
  **(b) GD FORK RULED — Matt (verbatim): "Grim Dawn is PC only. I will have to download it at a later
  date onto my PC and then you can SSH into it for the data."** = **Option A, DEFERRED.** No §5 swap;
  the frost-blades contingency (KTL-3) stays dormant; gd kit stays HELD (R-K5/R-N5 BLOCKED until the
  install lands). **matt_to_do T4 filed.** **Same-pass refinement** (Matt follow-up: "does it make any
  sense for me to download the Windows version of GD on my mac now?"): conductor answer = the FILES
  suffice — the game never runs for extraction; Mac-native acquisition paths exist (Steam-console
  `download_depot` of the Windows depot on the Mac Steam client · GOG offline installer +
  `innoextract`, no Windows anything); **FoI is Inquisitor content → the rank table lives in the
  Ashes-of-Malmouth (GDX1) database — base game alone is insufficient**; a Mac-viable `.arz`
  extraction-toolchain verification is commissioned (legolas Mode A, read-only) BEFORE Matt spends
  bandwidth. T4 carries both paths (Mac-now pending toolchain verdict / PC-later).
  **(c) NORMALIZATION-RULE LANE FIRED (named-gamora, `rule_owner` per dual-column law):** author
  `normalization_rule` rows per manifest sections A–H (BLOCKED rules excepted, left NULL with manifest
  refs) → derive `rdr_value` for every non-context non-blocked kit_numeric + monster_numeric row →
  stamp `rule_id` + `rule_version_applied` → rules report + Gate-2 readiness flag (jack-ryan reviews
  per charter; the PIN-C3 maxroll-vs-fextralife conflict is on his list). Veto-open.
- **KFL-10 (2026-07-23, conductor + Matt in-chat): RULES LANE VERIFIED (KF-2/KF-3 CLOSED) + GD
  TOOLCHAIN GO + SYNTY INTERFACE DIRECTIVE + KF-4 FIRED.**
  **(a) gamora normalization-rule lane VERIFIED + pushed** (collab `58693914`/`7e3abc2d`/`bd8c0e6b`;
  engine `4857e96` math note — ONE home:
  `src/reincarnated/simulation/math/kf2-rdr-normalization-convention.md`): **37** `normalization_rule`
  rows (rule_owner=gamora, v1, active); the 3 BLOCKED rules correctly NOT authored (R-K5/R-N5 gd ·
  R-G4 poe2-armour); kit_numeric **444/444** resolved (405 derived + 39 `_v327_context` fenced),
  monster_numeric **145/145** IDENTITY; NULL remaining = ONLY the 2 pre-existing seeds. **RDR
  convention: IDENTITY within each source game's own scale** — cross-game rescale cancels in the
  fidelity gauge (realized/expected), so identity preserves in-game ratios and makes on-screen
  deviation a pure pipeline-drift signal; tempo rules convert UNIT only (frames/cast → casts/sec).
  Conductor spot-probes exact (bonestorm gem-20 116/175/89/134 · rhoa armour 35,988); source_value
  bit-unchanged vs backup (dual-column law); DB byte-rebuildable from committed `.sql` alone.
  **5 Gate-2 readiness items queued to jack-ryan** (PIN-C3 maxroll-vs-fextralife · context-row rdr=sv
  fence · value-vs-formula GAP distinction on poe2 armour · the IDENTITY seam call · partial/
  pre-mitigation render contract R-G5/R-H3/R-C3/R-C4/R-G3). **KF-2 + KF-3 exit predicates GREEN —
  gates CLOSED.** Veto-open.
  **(b) GD FORK — TOOLCHAIN VERIFIED GO (legolas, commit `19fbe222`,
  `legolas/notes/2026-07-23-gd-mac-extraction-viability.md`) + PURCHASE-INTENT CONFIRMED — Matt
  (verbatim): "I haven't purchased Grim Dawn yet, but I would if it will be helpful to this
  process."** Conductor recommendation relayed: BUY — **GOG primary** (base + Ashes of Malmouth;
  browser-download offline installers → `brew install innoextract`, native unpack, no Wine → .arz→
  .dbr via ArchiveTool.exe-under-Wine OR a small Python parser, binary format fully documented);
  Steam alternative = DepotDownloader (brew, .NET 8) with one caveat (GDX1 depot ID needs a browser
  check — SteamDB 403'd the crawl). Confirmed: FoI ranks live in `gdx1/database/gdx1.arz` (AoM);
  Act-1 mobs in base `database/database.arz`. **T4 re-synced GOG-primary, hold lifted.** The buy is
  worth it: 4th source game exercises the OA/DA/PTH math family — converter generality evidence no
  d2/poe kit provides. Veto-open.
  **(c) MATT DIRECTIVE (verbatim): "please take a look at these newly developed synty dark fantasy
  HUD and Menus asset packs. THis will be perfect for the godot work that we're doing today. Please
  use these assets for health/mana/resource and skill HUD assets."** → **KF-6 SPEC AMENDED: the
  Synty Dark Fantasy INTERFACE packs are the HUD substrate** (globes / hot-bar / resource + skill
  surfaces build FROM them, not from hand-drawn placeholders). Provenance: first HUD zip arrived
  corrupted (Safari `.download` container; `unzip -t` exit 9, no central directory — conductor
  finding relayed, Matt confirmed "THeHUD zip was currupted") → Matt supplied working replacement at
  `matt_notes_handoff_docs/recent-synty-packs/Source_Sprites/` (2,195 files, 329MB) —
  conductor-inventoried: `Frame_Orb_*` globe frames **with Glass layers** + `Frame_Ring_Large_*`
  (health/mana globes), `Bar_*`/`Frame_Bar_*` strips (resource bars), `Sigil_Box/Ring/Cross_*`
  (skill-slot frames), `Icons_Status` Health/FortifiedHealth, **`Icons_Elements` per-element
  Clean/Stroke/Underlay** (maps straight onto the element system), `Flasks` (glass-layered),
  Reticles/Cursors/DamageDirection/input glyphs. Menus pack complete alongside
  (`INTERFACE_Dark_Fantasy_Menus_SourceFiles_v1`: bar/frame primitives + `SM_Prop_Coin/Rune` FBX).
  **drax imports both packs into `reincarnated-godot/Assets/` in the KF-6 lane** (post-KT-3 —
  same-repo collision avoidance). Ledgered as Matt's own commitment — recorded, not conductor-ruled.
  **(d) KF-4 KIT-COMPILER LANE FIRED (named-gamora):** canon record + `kit_mapping` +
  `kit_numeric.rdr_value` → real sim fighter per §KF-4; `_build_martial_player_class`
  label-synthesis RETIRED for the pilot only; exit = `kit_acceptance_assert` rows GREEN per pilot
  kit; red assert → docket + §5 swap, never silent invention. gd kit HELD (compiles when T4 lands).
  Veto-open.
- **KFL-11 (2026-07-23, conductor): KF-4 VERIFIED + CYCLONE RED RULED (A-path) + GATE-2 FIRED.**
  **(a) KF-4 kit compiler VERIFIED + pushed** (engine `06ec241` math note + `b0684d4` compiler;
  collab `3694f2fc` assert SQL): **additive-only conductor-confirmed** (7 new files under
  `simulation/kit_compiler/` + math note; ZERO existing engine paths touched — determinism preserved
  by construction); smoke conductor-rerun reproduces **35 GREEN · 1 RED · 1 GAP-untested** exactly;
  per-kit DB probe reconciled (the 5 KF-1 seed asserts stay green alongside the 37 KF-4 rows);
  `_build_martial_player_class` label-synthesis RETIRED pilot-only; gd HELD honestly (GAP-untested,
  compiles zero-change when T4 lands); **KF-5 hook in place** (per-skill `_composition` block so
  expected computes from anchored factors, zero-derivation). Docket `176` conductor-inspected:
  complete provenance JSON + disposition options recorded — red-test doctrine executed, nothing
  fabricated, nothing silently swapped.
  **(b) CYCLONE RED RULED (reasoning-boundary, veto-open): Option A first.** The RED is a
  VALUE-harvest gap (3.15 build-point weapon DPS un-anchored), not an engine gap — shape compiles
  fully GREEN. Ruling: bounded legolas Mode-A harvest of the documented 3.15 Cyclone build's weapon
  + its build-point DPS anchor; if anchored → micro-lane (elrond row → gamora rule → re-assert)
  flips RED→GREEN, roster untouched; **if unanchorable → B-vs-C (accept-partial vs §5 swap)
  escalates to Matt** (roster consequence = commitment-boundary, same law as the GD fork). Cyclone
  meanwhile renders honest partial drift — the gauge working, not failing.
  **(c) GATE-2 LANE FIRED (named jack-ryan, BLOCK authority; BLOCK → fix-forward):** KF-4 engine
  diff review — gamora's 6 readiness items + the pre-existing `spatial_engine._RICH_TO_SPATIAL`
  mirror-drift FINDING (stale vs the authoritative generation-side table; compiler bypasses via
  explicit per-skill `spatial_geometry_type`; 2-entry mirror-sync recommended as follow-on).
  **KF-5 HOLDS until Gate-2 returns** (no building atop an unreviewed engine diff). Veto-open.
- **KFL-12 (2026-07-23, conductor): GATE-2 PASS-WITH-NOTES VERIFIED + PUSHED — KF-5 FIRED.**
  **(a) jack-ryan Gate-2 on the KF-4 engine diff: PASS-WITH-NOTES, no BLOCK** (findings note
  `jack-ryan/notes/2026-07-23-kf4-gate2-review.md`, commit `fde9d1bf` conductor-verified + pushed).
  All 6 readiness items PASS **on evidence, not the report's word**: byte-level diff (7 A-only files;
  zero `M` to resolver/spatial/combatant across the whole run; no module imports `kit_compiler` —
  leaf, no coupling) · self-run smoke reproduces 35G/1R/1GAP exact · docket 176 DB-probed complete
  (reported-for-swap, never fabricated) · v327 fence catches the 150% trap, selector takes the 3.15
  build point 59.0 · dual-population distinguishable by date AND in-row `[KF-4-compiled]` marker ·
  legacy-flat-path injection confirmed at `damage_resolver.py:879-881` (RDR leaf not double-scaled).
  Determinism risk ruled NIL **structurally** (additive-only leaf IS the proof; trace-diff would be
  theater). Scope-attribution catch: the +98-line spatial_engine delta in the full range belongs to
  the prior REPLICA-1 emitter commit (Gate-2 PASSED 2026-07-22), not KF-4. **Mirror-sync disposition:
  IN-SCOPE consistency fix, change-class PRE-APPROVED, rides its own Gate-2 as a separate additive
  diff — non-blocking** (explicit-field bypass keeps KF-4/KF-5 correct today). 3 INFO notes recorded
  (math-note cite staleness — real path `:879-881` + `spatial_gauntlet/` qualification · manifest
  R-K4 key-name prose drift `_v315` vs `_gem20_bp` · PIN-C3 maxroll-primary CONCURRED, HP-pool-only,
  zero gauge effect). **KF-4's Gate-2 condition CLOSED; KF-5 unblocked.**
  **(b) KF-5 EXPECTED/PCT LANE FIRED (named-gamora):** per §KF-5 + ratified Pins A/B (KFL-3c) + the
  three-deep gauge stack (KFL-3d). Sim computes at each resolved hit: **expected** (Pin A —
  crit-weighted mean at the documented build point, computed from the KF-4 per-skill `_composition`
  block, ZERO derivation) + **pct** = realized `rdr_value`/expected (Pin B — live target's
  normalized defense at hit time), for BOTH dealt and received; **pre-mitigation % = the internal
  gate instrument** (KFL-3d conductor amendment). `replica_frame_emitter` carries ADDITIVE
  `expected`+`pct` on `damage` events (v1-additive, no version bump; observability-only; default-off;
  ZERO combat-logic change in the same commits — the REPLICA-1 emitter discipline). **Riders:**
  2-entry `spatial_engine._RICH_TO_SPATIAL` mirror-sync (`placed_lane→line` · `orbit→circle`) as its
  OWN separate commit per (a) pre-approval, riding its own Gate-2 · opportunistic math-note cite
  refresh. Exit: dealt+received events carry expected/pct · determinism byte-identical · non-finite
  guard · Gate-2 PASS on the diff. Veto-open.
- **KFL-13 (2026-07-23, conductor): CYCLONE ANCHORED — A-PATH LANDS — ELROND MICRO-LANE FIRED;
  GAMORA RULE STEP QUEUED BEHIND KF-5.**
  **(a) legolas harvest VERIFIED ANCHORED** (commit `8abfeed5`,
  `legolas/notes/2026-07-23-cyclone-weapon-dps-anchor.md`): the documented 3.15 Cyclone Slayer
  build (thread 3033867) embeds a PoB export (pastebin `Sf8AYHkK`, decoded in-session) whose
  active Weapon-1 is verbatim-anchored — rare Exquisite Blade "Blood Razor" iLvl 83 (156% inc
  phys · +23–49 flat phys · 21% IAS · Q44 incl. +14% crafted · +50% global crit multi implicit ·
  25% inc crit chance crafted) on poedb base 67–112 phys / 1.35 APS / 5.7% crit. Routes exhausted
  honestly (8 listed; the corpus's Berserker thread 3078559 PoB decoded + rejected as
  wrong-build; budget Starforge range-computed BELOW the anchor — transition weapon, not build
  point). **B-vs-C escalation MOOT — roster untouched; nothing reaches Matt.**
  **(b) TRUST-BUT-VERIFY FINDING (load-bearing): the note's derived ~570 pDPS composes quality
  WRONG** — it invents "+0.5% inc phys per 1% quality for two-handers" (Q44→+22%); the PoE
  local-weapon rule is 1:1 (Q44→+44%), giving **~615 pDPS** — tellingly nearer the guide's "650+"
  aspiration. The note's per-hit sketch (570×0.59/3.0≈112) also conflates attack cadence with
  per-hit magnitude. NEITHER blocks: under dual-column law elrond stores only the VERBATIM LEAVES
  (all clean); the COMPOSITION is gamora's normalization rule to pin against a citable source
  (PoB's open-source CalcOffence path qualifies), jack-ryan-checked. Both defects are flagged
  into the gamora brief so the note's arithmetic cannot leak into the rule.
  **(c) Corpus probes confirm (conductor, read-only):** poe1-cyclone carries ZERO weapon leaf
  rows (the RED's root cause); `weapon_dps_target=650` is already context-fenced under
  `R-CTX-GEO` (the compiler correctly never consumed it — legolas's aspirational-floor read
  CONCURRED); citations = overgear + poe-vault (both Slayer guides) + the wrong-build Berserker
  thread; the Slayer thread + PoB + poedb pages are absent. The kit is Slayer-documented →
  citation correction = a data-integrity fix within the ruled 3.15 era + ruled build, NOT a
  re-pin (KFL-5 era law untouched).
  **(d) ELROND MICRO-LANE FIRED (named-elrond):** add the verbatim weapon leaves (source_value +
  source_anchor quotes; **rdr_value NULL — the rule step derives**) + the three missing
  citations; Berserker-row disposition = elrond curation call, documented; migration `.sql`
  committed (byte-rebuildable law); key naming aligned to the compiler's `_bp` build-point
  selector conventions.
  **(e) GAMORA RULE STEP QUEUED** (weapon-composition normalization rule + rdr derivation +
  compiler consumption + re-assert → RED→GREEN): fires AFTER the KF-5 lane returns (same seam,
  same repo — collision law; any compiler amendment rides Gate-2 with/after KF-5's diff).
  Veto-open.
- **KFL-14 (2026-07-23, conductor): KF-5 VERIFIED — THE GAUGE'S FIRST CATCH — R-KF5-1 RULED;
  ELROND LEAVES VERIFIED; FIX-FORWARD + RULE-STEP LANE FIRED.**
  **(a) KF-5 lane VERIFIED + engine PUSHED (`b0684d4..2e222e3`).** Commit scope EXACT (math note
  `de0090f` · Rider-1 isolated in `455d76a` — precisely the 2-entry mirror-sync with
  byte-neutrality rationale inline · gauge in `2e222e3`). Conductor re-ran both smokes: KF-4
  HOLDS 35 GREEN · 1 RED · 1 GAP; KF-5 PASS (bridge stamps both skills · all 59 damage events
  carry the 5 additive fields · finite-or-null guard · Pin-A check `expected_premit == 2570.0` ·
  same-seed determinism byte-identical · sink-ON vs OFF combat outcome identical 120.1==120.1).
  Purity confirmed IN THE DIFF: `_kf5_gauge_for_hit` reads resolved state + `_composition`,
  mutates nothing, draws no RNG; the None-sink default path never invokes it. **Deviations
  ACCEPTED:** (1) `attach_composition_blocks` bridge — the compiler stamps `_composition` on the
  dataclass, not `class_dict["skills"]`; the bridge stamps the resolver-ignored underscore key.
  **KF-6 driver MUST call it before `run_spatial_fight` or the gauge renders all-null** (KF-6
  brief rider). (2) Received-side `pct_received` null until KF-3 monster harvest emits mob
  compositions — next-lap admission; dealt side fully wired.
  **(b) THE BLOCKER — CONFIRMED + RULED `R-KF5-1` (reasoning-boundary, veto-open).** Conductor
  confirmed both ends line-exact: `kit_compiler.py:541` emits effect name `"flat_damage"`;
  `damage_resolver.py:832` consumes only `"damage"` → realized amount 0.0 on ALL compiled-kit
  hits. KF-4 smoke and Gate-2 were structurally blind (asserts tested composition-EXISTENCE and
  finiteness; 0.0 is finite). **The gauge caught the dead wire on first light — the run's thesis
  working.** RULED **Option A**: one-line compiler rename `flat_damage`→`damage` — defect-repair
  restoring the compiler's own spec'd behavior (the kit JSON says these effects ARE damage), zero
  taste/roster/canon consequence → conductor-ruled. Option B REJECTED (resolver-boundary
  normalization = Disc #12 semantic shift masking the defect at the wrong boundary); Option C
  REJECTED (pct≈0 everywhere defeats KF-7). Gamora's throwaway-rename diagnostic (bonestorm
  amount≈2115.6 · pct 137.2 ∈ band [96.2,141.8]) already proves rename param-compatibility
  end-to-end.
  **(c) ELROND MICRO-LANE VERIFIED (commit `a430a476`, pushes with this entry).** Scope exact
  (2 migration `.sql` + note); 12 `_bp` leaves all `rdr_value NULL / rule_id NULL` (dual-column
  law); `weapon_dps_target=650` untouched under `R-CTX-GEO`; Berserker citation id-64
  `quarantined=1` NOT deleted (provenance preserved); 3 new citations classed
  communal/dataset/dataset, accessed 2026-07-23. Conductor re-applied both migrations:
  idempotent, 32|6 → 32|6, 650 stable. `INSERT OR IGNORE` deviation ACCEPTED (structural
  immutability of existing rows — stricter than the sibling's `OR REPLACE`).
  **(d) FIX-FORWARD + RULE-STEP LANE FIRED (named-gamora, bundled — one seam, one lane,
  sequential):** (1) the R-KF5-1 one-line fix; (2) KF-5 smoke flipped from blocker-documenting
  to healthy-path asserts (amount>0, sane pct band, determinism retained); (3) the KFL-13(e)
  rule step — weapon-composition normalization rule + rdr derivation from the 12 verbatim
  leaves (math note first per Disc #1; the REAL 1:1 quality rule → ~615 pDPS, the note's ~570
  quarantined per KFL-13b; composition pinned against PoB CalcOffence) + compiler consumption →
  cyclone `has_damage_base` RED→GREEN expected (36/0/1); (4) bonestorm WR-floor warning as
  secondary heal signal. Then ONE jack-ryan Gate-2 over the full KF-5 range + riders + fix +
  compiler amendment, fired after conductor verification of the lane. Veto-open.
- **KFL-15 (2026-07-23, conductor): KF-6 LANE FIRED (named-drax) — GODOT HUD BUILD ON THE FREED
  TREE; EMISSION SEQUENCING PINNED.**
  Galadriel's KT-lane returned + verified (KTL-7) → the godot working tree is free. **Lane scope
  (godot-only):** (1) Synty Dark Fantasy INTERFACE import — BOTH packs from
  `matt_notes_handoff_docs/recent-synty-packs/` into `reincarnated-godot/Assets/` per Matt's
  directive (KFL-9c substrate law: globes/hot-bar/resource + skill surfaces build FROM these, not
  hand-drawn placeholders); (2) F3 floaters `<amount> (<pct>%)` dealt + received, read STRAIGHT
  from frame fields (§8: window DISPLAYS, sim COMPUTES — zero derivation), **null-graceful by
  design** (pct null → `12,500 (—)`: mob-received is null this lap per KFL-14a Deviation 2, and
  current frames predate the gauge); (3) health globes + skill hot-bar RENDER build from the Synty
  primitives against a drax FIELD-AUDIT of frame v1 — anything the frame lacks (expected-hp,
  distinct skill-use events) is reported as a NAMED GAP for a gamora micro-emission, never derived
  scene-side; (4) REPLICA-1 fight-picker verify (KF-6 precondition — fix in-seam if still broken;
  gates KF-7 only). Same-scene law: renders into `replica_playback.tscn` runtime per §7/§8 no-fork
  (KTL-6 held it byte-untouched by construction — the HUD attaches via script, scene stays whole).
  **EMISSION SEQUENCING (conductor clarification of KFL-14a's "KF-6 driver" rider):** the
  `attach_composition_blocks` obligation belongs to the ENGINE-SIDE emission driver, NOT drax —
  existing `replica1-frames/` predate the gauge, so after the gamora fix-forward lane returns, a
  small gamora RE-EMISSION step regenerates pilot-fight frames (compositions attached · post-fix
  damage · gauge fields live); drax's scene then reads them as pure data swap, zero code change.
  KF-7 assembles on: drax HUD ✓ + re-emitted frames ✓ + picker ✓. Veto-open.
- **KFL-16 (2026-07-23, conductor): FIX-FORWARD + RULE STEP VERIFIED + PUSHED — THE GAUGE'S
  SECOND READING NAMED — CONSOLIDATED GATE-2 FIRED.**
  **(a) Bundled gamora lane VERIFIED + engine PUSHED (`2e222e3..a63d656`).** Part 1 (R-KF5-1,
  `b492c77`): `flat_damage` survives only as a history comment (`kit_compiler.py:596`) + math-note
  prose — no live emission; math §8 frames the fix NOT-a-semantic-shift (Disc #12) with
  param-compat proof (resolver's legacy-flat path reads `params["magnitude"]` identically under
  either name). Part 2 (`a63d656` + collab `cf55aa1e`/`eea15ca6`): conductor re-ran both smokes —
  KF-4 **36 GREEN · 0 RED · 1 GAP** (cyclone RED→GREEN; gd GAP held) · KF-5 healthy-path PASS
  (59/59 amounts > 0, min 1483.3 · pct ∈ [96.20,141.80] ⊂ asserted [90,150] · Pin-A 2570.0 ·
  determinism byte-identical · outcome identical 120.1==120.1). pDPS **615.01** re-derived by
  conductor's own arithmetic — both KFL-13b quarantined defects corrected against the PoB
  CalcOffence local-mod anchor (quality 1:1 additive → 200% total; flat-before-increased;
  APS=1.6335 fenced as TEMPO); per-hit magnitude 222.1 avg (× effectiveness 0.59), cadence
  orthogonal per §9.3 — the exact separation the charter demanded. Migration re-applied by
  conductor: idempotent (13|0 → 13|0), in-file guards green (leaves_null=0 · fence 650/R-CTX-GEO ·
  identity_violations=0); all 12 leaves IDENTITY-derived under R-K6 (magnitude family) / R-K7
  (tempo) / R-M5 (percents) / R-CTX-GEO (identity). **Deviations ACCEPTED:** two rules not one
  (preserves the magnitude-vs-tempo fence — the run's own separation law); effectiveness kept as
  the once-applied offensive modifier (bonestorm-style, zero modifier-chain change). WR-floor
  warning now a scenario-timeout artifact (mean_mobs_killed 0→12/28; cyclone 0→26) — observation
  only, no calibration touched.
  **(b) NAMED FINDING — THE GAUGE'S SECOND READING (adjudication routed, NOT conductor-ruled).**
  pct centers **120.23, not 100** (empirical median 120.93). Root analytically PINNED in math §8:
  the compiler injects `magnitude = base_max` while Pin-A `expected` uses `base_mean`
  (mitigation/buff factors cancel; ±20% variance sweeps around the base_max center). The smoke
  band legitimately guards the CENTER against drift — but the RUN's fidelity story reads ≈100 as
  faithful, and KF-7 floaters would show bonestorm ~120% median. The fork (compiler
  magnitude-shape: single-scalar base_max vs base_mean vs min–max range-roll matching source-game
  weapon rolls) is a COMBAT-BEHAVIOR change → exceeds reasoning-boundary; routed to Gate-2
  adjudication + named to Matt in-status. Outcome = fix-forward lane or next-lap docket, per
  Gate-2 + Matt.
  **(c) CONSOLIDATED GATE-2 FIRED (named-jack-ryan):** full engine range `de0090f..a63d656`
  (math note · Rider-1 · gauge · fix · compiler amendment) + corpus rule composition
  (R-K6/R-K7 migration vs math §9 vs dual-column law) + band-choice legitimacy + both Disc-#12
  framings (Part 1 "not-a-shift" claim; Part 2 SEMANTIC-SHIFT-framed `base_weapon_dps` gap-status
  reinterpretation) + the (b) magnitude-shape adjudication. Veto-open.
- **KFL-17 (2026-07-23, conductor): DRAX KF-6 LANE VERIFIED + GODOT PUSHED (`1a25caa..9f130cd`) —
  THE GAUGE'S DISPLAY INSTRUMENT IS BUILT.**
  **(a) Commit scope EXACT** (5 files: M `AGENT_STATE.md` · A `check_floater_format.gd` · A
  `check_picker_advance.gd` · A `replica_hud.gd` · M `replica_playback.gd`); `replica_playback.tscn`
  byte-untouched — same-scene law held by construction (HUD attaches via script). **Synty license
  posture ACCEPTED:** 41-sprite SELECTIVE import (of 2,195) on-disk at
  `Assets/Synty/interface-dark-fantasy-hud/{globes,bars,hotbar,icons_status,icons_elements}` +
  headless `--import` metadata; `/Assets/Synty/` gitignored, NO pack tracked (`git check-ignore`
  confirmed) — the established compliance posture, not an omission.
  **(b) Conductor re-ran ALL THREE harnesses independently:** gated smoke → **SMOKE COMPLETE**
  (final tick 55, entities=41, parse_errors=0, seek-to-51 OK, clean-exit) · floater harness →
  **VERDICT: PASS** with exact strings (`281,205 (—)` old-frame null-graceful · `12,500 (87%)`
  synth dealt · `◆ 3,400 (—)` synth received) · picker harness → **PASS** (7 distinct fights,
  scene ALIVE; REPLICA-1 defect does not reproduce — KT-4 reload-safety already cured it; no
  in-seam fix needed; **KF-7 precondition MET**). Both Metal captures verified by conductor's own
  eye (tick51: dressed arena + red player globe `14,795/15,130` + blue mob globe + 8-slot Synty
  hot-bar; tick40: dense DoT floater column + player globe drained to ~2,170). DummyShader line =
  the 1 documented KTL-6 artifact, as expected.
  **(c) Load-bearing endorsement:** floaters read **`amount`** (the pct numerator, KF-5 math §172)
  — drax switched OFF `delivered` (capped HP-removed) onto the roll the gauge anchors to. The
  floater IS the gauge's display: when re-emitted frames land, `(—)` → `(87%)` with ZERO drax
  change (pure data swap). **3 NAMED GAPS registered** for engine-side emission scope (never
  derived scene-side, §8 discipline held): (1) `expected_max_hp` on header roster → fidelity-%
  globe overlay; (2) per-tick `skill_cooldowns`/`cast_progress` → hot-bar cooldown ring; (3)
  `pct_received` → lights when compositions attach (KFL-14a Deviation 2 lineage).
  **(d) Stale STOP closed:** drax's flat_damage BLOCKER flag was already FIXED + pushed
  (`b492c77`, KFL-16a) while his lane was in flight — informational only; his floaters render
  whatever `amount` the frame carries, correct under either state. Veto-open.
- **KFL-18 (2026-07-23, conductor): CONSOLIDATED GATE-2 RETURNED — PASS-WITH-NOTES, NO BLOCK —
  VERIFIED; ITEM-6 SHAPE AT MATT; RE-EMISSION SEQUENCING RULED.**
  **(a) Verdict verified on full read** (`jack-ryan/notes/2026-07-23-kf5-gate2-review.md`, collab
  `39105081`): all 8 items PASS at byte/live-import/DB/live-compile/smoke level — gauge purity
  with airtight default-off proof (`_frame_on_hit` → None-sink unreachable ⇒ byte-identical by
  construction); Rider-1 live-import 26==26 AUTH==ENG True (the exact 2-entry diff pre-approved at
  KF-4); R-KF5-1 ENDORSED not-a-shift (dead-wire connect — resolver reads `params["magnitude"]`
  name-independent); Part-2 Disc-#12 SEMANTIC-SHIFT framing PASS (surfaced in math §9.5 + commit +
  in-code comment); band [90,150] legitimate as CENTER-drift regression guard (fidelity gauge, not
  variance gate); cyclone selector-driven (270/483 from DB reads, no literals), effectiveness
  applied EXACTLY once (0.59 not 0.59²), tempo fence held, both quarantined legolas defects
  verified ABSENT; both smokes self-run green (36/0/1 + PASS). **Requested assert-class NOTE
  delivered:** realized-damage POSITIVITY on non-GAP damage bases ("finite ≠ live" — a dead wire
  passes finiteness; KF-5 smoke now carries `amount > 0`); jack-ryan self-assigned the Disc-#11
  refinement fold (ADR-002 documentation-only).
  **(b) ITEM-6 ESCALATED TO MATT (commitment boundary honored):** jack-ryan recommends **(a)
  compiler emits `base_mean`** (center→100, one line at `kit_compiler.py:280`, avoids (b)'s
  double-variance stack with the existing U[0.80,1.20] draw; combat shifts once — per-hit ~−17%,
  kill times ~+20%, re-measurable in a single balance pass); (b) source-band-roll deferred until
  the synthetic-vs-source variance double-count is resolved deliberately; (c) keep+document
  REJECTED (ships a +20% reader-correction into the exact number KF-7 exists to make legible).
  Conductor CONCURS with the recommendation shape; **Matt ratifies** — named in-status
  decision-shaped.
  **(c) CONDUCTOR SEQUENCING RULING R-KF7-SEQ (veto-open): gamora RE-EMISSION HELD until Matt's
  item-6 ruling.** Rationale: the re-emission exists to produce THE frames Matt watches at KF-7;
  emitting at a center Matt may be about to move (120 vs 100) produces a known-stale frame set +
  a duplicate lane. The ruling is one message away; the lane fires immediately after. ONE
  re-emission then carries: ratified magnitude shape · `attach_composition_blocks` (pct_received
  lights, KFL-15 sequencing) · candidate riders = drax named-gaps 1+2 (`expected_max_hp`,
  `skill_cooldowns`/`cast_progress` — gamora assesses additive-field feasibility in-lane) ·
  INFO-1 docstring fix (±15%→±20%, opportunistic). Gate-2's own action line concurs: item-6
  "gates only whether the KF-7 floaters center 100% or 120%" — i.e. it gates exactly what
  re-emission produces. Veto-open.
- **KFL-19 (2026-07-23, conductor): ITEM-6 RULED BY MATT — OPTION (a) `base_mean` RATIFIED —
  R-KF7-SEQ HOLD RELEASED → RE-EMISSION LANE FIRED.**
  **(a) The ruling (in-chat, 2026-07-23):** Matt — *"I concur with base mean."* Commitment
  boundary honored end-to-end: gauge surfaced the +20% structural bias (KFL-16b) → Gate-2
  adjudicated decision-shaped with recommendation (a) → conductor concurred → **Matt ratified**.
  The compiled magnitude shape is now CANON: injected `magnitude = base_mean` — realized damage
  centers on the statistical mean of the source band, which IS Pin-A `expected` by definition →
  gauge and reality re-converge at 100 by construction. Combat consequence accepted: per-hit
  ~−17%, kill times ~+20%, one-time shift, re-measurable in a single balance pass.
  **(b) Lane FIRED (named-gamora, background):** (1) shape fix at `kit_compiler.py:280`
  (`base_max` → band mean); (2) KF-5 smoke band RE-DERIVED math-before-code (center 120.23 →
  100.00; analytic [80,120]; guard band re-derived with documented margins — math note §10, same
  rigor as §8); (3) INFO-1 docstring fix (`damage_resolver.py:942` ±15%→±20%); (4) both smokes
  re-run; (5) **RE-EMISSION** of the pilot replica frame set (same fights/arms/seeds as on-disk,
  compositions attached via `attach_composition_blocks`, gauge fields live, post-shape damage) —
  data-swap into the godot frames dir per KFL-15 (DATA ONLY — no .gd/.tscn touch); (6) riders:
  additive-field feasibility for drax named-gaps 1+2 (`expected_max_hp`, `skill_cooldowns`/
  `cast_progress`); `pct_received` stays honestly null until KF-3 mob compositions exist.
  **Direction-slip guard passed to the lane:** Gate-2 finding line 44 says "kill times −17% /
  mobs die faster" — a slip; line 48 is correct (damage drops → kill times LENGTHEN +20%). Do
  not propagate into math §10. **Scoped Gate-2 follows the lane's return** (engine-diff law).
  Veto-open.
- **KFL-20 (2026-07-23, conductor): MATT FIELD REPORT FROM THE LIVE SCENE — FOUR FINDINGS
  DISPOSITIONED; KF-6b PRESENTATION-REMEDIATION LANE FIRED (drax, MCP-IN-SCENE MODE).**
  Matt inspected the live scene (first hands-on-the-instrument moment of the run). Findings:
  **(a) "Characters are perfect"** — rig lineage (KT-2..KT-4) confirmed by the audience. No
  action. NOT the formal KT-5 ruling (that packet stays open).
  **(b) Walls: not grid-snapped · not spanning the full floor · entities walk through them.**
  → KF-6b lane (drax). Data-truth framing pinned: the replica PLAYS BACK recorded positions —
  presentation CANNOT impose collision without falsifying the data (§8 spatial corollary: the
  window displays, the sim computes). Honest fix: snap walls to grid + span the perimeter +
  align the wall line to the SIM ARENA BOUNDS read from frame headers so no recorded path
  crosses a wall. Interior walls that entities RESPECT = sim-side obstacle geometry = an
  ENGINE design fork — named to Matt in-status; next-lap docket candidate, not this run.
  **(c) "Original basic kits still in use — the new data cannot be in use here" — MATT IS
  RIGHT; diagnosis CONFIRMED by the dead-wire history.** Compiled kits realized `amount==0.0`
  until `b492c77` (KFL-16a), so on-disk frames carrying live damage NECESSARILY came from the
  legacy kit path — the frames predate the compiled-kit connection. The in-flight KFL-19b lane
  already forces the compiled pipeline (its validation gate requires non-null `pct` median ≈100,
  impossible under legacy kits). **Conductor ruling (no mid-flight message channel exists in
  this environment; stop-and-refire rejected as riskier than delta-at-verify):** lane runs to
  completion; at verification the roster is checked — if only the on-disk 2-kit set returned,
  a bounded ROSTER-EXPANSION delta re-emits ALL non-GAP compiled kits (blind+aware) through the
  proven pipeline, with skill-variety validation added (distinct `skill_idx` used per fight
  where the kit carries >1 skill; roster skill names match the compiled kit). Veto-open.
  **(d) MCP directive (Matt, verbatim intent): drax works directly IN the scene via the MCP
  connection — headless-only workflow cannot see these defects.** Spec read
  (`claude-mobile-session-docs/godot-development-ideas/Godot_MCP_Capture_Harness_Spec.md`).
  Ground-truth facts gathered for its §6 falsification: build = **4.6.3.stable.official
  (STANDARD, not Mono)** → IvanMurzak #1-contingent FAILS unless a .NET switch (Matt decision,
  not taken in-lane); render surface PROVEN (windowed Metal captures exist); **an MCP stack is
  ALREADY INSTALLED** — `.mcp.json` → `npx @satelliteoflove/godot-mcp` + in-project editor
  addon "Godot MCP" v4.0.1 (websocket bridge). KF-6b lane therefore: update the installed
  stack to latest · attempt the NEW isolated-node capture on it · author `CaptureRig.tscn` to
  the spec §2 server-agnostic contract (needed regardless of server, spec §7) · fix the walls
  IN-scene with visual verification in the loop · NO purchases ($15 Pro) and NO build switch
  in-lane — if the stack can't do isolated-node capture post-update, the fork returns
  decision-shaped (viewport+CaptureRig vs Pro vs .NET). Veto-open.
- **KFL-21 (2026-07-23, conductor): KFL-19b RE-EMISSION LANE VERIFIED + ENGINE/COLLAB PUSHED —
  MATT'S DIAGNOSIS DEEPENS (frames were W3'-MARTIAL pilots) — CONDUCTOR FINDING: ROTATION
  DEAD-WIRE CANDIDATE — DIAGNOSIS LANE FIRED.**
  **(a) Lane VERIFIED.** Conductor's own runs: KF-4 smoke **36 GREEN · 0 RED · 1 GAP** · KF-5
  smoke **PASS** (new band [70,130], determinism byte-identity, outcome identical). Shape-fix
  line eye-verified (`kit_compiler.py:280` band mean, None-guarded — GAP still injects None;
  ratification cited in-comment). Conductor's independent frame scan MATCHES gamora to the
  decimal: 40 files exact, 0 stale martial files, 5 pilots × 8; aggregate anchored dealt pct
  **median 96.51 · mean 97.34 · [80.42, 119.95] · n=280** — every hit in analytic [80,120],
  center ≈100; `skill_cooldowns` live on every kit; `pct_received` all-null (honest);
  gd-flames GAP honest (44 hits, amount 0, pct null); `-purifier` kit_ref matches drax
  `PILOT_RIGS` key exactly. **Deviations ACCEPTED (all surfaced-not-silent, Deviations law):**
  (1) roster reinterpretation martial→compiled-pilot-5 — the on-disk frames were the REPLICA-1
  ref roster of W3'-gate MARTIAL pilots at pre-gauge hash `2f43045` (the literal "original
  basic kits" Matt saw); the literal re-emit reading satisfied ZERO downstream predicates;
  KFL-20c's roster-expansion delta is SATISFIED BY CONSTRUCTION. (2) frames UNTRACKED-by-design
  (precedent held; the emit driver is the git-tracked regenerable source, Disc #3). (3) godot
  commit N/A — frames live in COLLAB (`FRAMES_DIR_DEFAULT` absolute path); zero godot files
  touched. (4) ~2.6% below-100 residual accepted as measured finite-sample scatter (Disc #11
  diagnosis: RNG unit-mean proven, mirror-path verified, survivorship ruled out, p≈0.013;
  LLN-converges with larger fights — scenario choice, not code fix). Rider disposition
  endorsed: (ii) `skill_cooldowns` INCLUDED v1-additive; (i) `expected_max_hp` NEXT-LAP with
  the missing state precisely named (source-HP anchor from a KF-2-style harvest onto
  `_composition` — the exact damage-band analog). Engine `c5a2f2d` + collab `a8678397` PUSHED.
  **(b) CONDUCTOR FINDING — THE AUDIENCE'S READING (skill rotation): `skills used: [0]` on
  EVERY kit across ALL 40 fights.** Fire-sorc carries FireBall (242.5) + Meteor (1256.0); no
  Meteor hit exists anywhere. This is Matt's field complaint ("doesn't use any of its skills")
  SURVIVING re-emission — gamora's validation checked pct/amount/nullness but not variety;
  the conductor scan added it per KFL-20c. Probes pin the frame: player entity carries
  **len-2 `skill_cooldowns`** (both skills reach the SpatialEntity) · tick entities carry an
  **`energy`** field · a **Phase-2 rotation selector EXISTS** (`spatial_engine.py:575` block,
  `_select_skill_for_entity:1931`, math note `rotation-selector-phase2-2026-06-20.md`,
  energy-branched build-vs-spend). Selector present + inputs present + output degenerate =
  dead-wire-candidate #3 (after flat_damage and magnitude-shape). **Diagnosis lane FIRED
  (named-gamora):** classify WIRING GAP (compiled/projection fighters bypass or under-feed the
  existing ratified selector → fix-in-seam authorized by Matt's field report + the ratified
  Phase-2 behavior, Disc-#12 dead-wire-connect class, then re-emit + variety-validate) vs
  DESIGN GAP (compiled kits lack rotation metadata the harvest never captured → NO code;
  decision-shaped options to Matt). Veto-open.
  **(c) Scoped Gate-2 HELD to consolidate** with the rotation-lane outcome (one review over
  `c5a2f2d` + rotation disposition; push-then-Gate-2 cadence per KFL-16 precedent).
- **KFL-22 (2026-07-23, conductor): DRAX KF-6b VERIFIED + GODOT PUSHED (`9f130cd..a3556fc`) —
  WALLS AT SIM BOUNDS · MCP 4.1.0 IN-SCENE · CaptureRig PROVEN · MONO FORK TO MATT.**
  **(a) Walls FIXED by PLACEMENT** (report `drax/notes/2026-07-23-kf6b-walls-mcp.md`): root
  cause was the KT-3 dressed arena hardcoded 30×30 while playback derives dims from the frame
  header — frames carry NO `arena_width_m`/`height_m` → 44×44 trace fallback; walls sat at 30
  inside a 44 floor while recorded centers reach x37.5/y43.5 (straight through north/east).
  Fix in-seam, same-scene: `render_kt3_arena.gd` dims made runtime + `rebuild(w,h)` re-dress
  per fight-load from `_fit_arena_to_trace()`; ceil-tiling (18 tiles/side, 72 wall pcs, 324
  floor) with the wall line AT [0,44]. **Conductor verification:** commit scope CLEAN (8 files,
  all seam; zero frames staged; project.godot untouched). Independent bounds scan (conductor's
  own): **124,411 pts · x[7.35,37.18] y[2.02,43.5] · 0 violations outside [0,44]** — verdict
  HOLDS; drax's cited 126,051/x[7.0…] envelope was the pre-swap martial set, and the compiled
  set sits STRICTLY INSIDE it (same tightest clearance 0.5 m, y 43.5 vs wall 44). Captures
  eye-verified: BEFORE reproduces Matt items 2/3/4 exactly (walled patch floating in a larger
  floor; skeletons through the east wall; player outside the south wall); AFTER = full-perimeter
  grid-snapped enclosure with the COMPILED roster live on-screen (`d2-fire-sorc 1/40`).
  Instruments re-run by conductor: smoke GREEN (fire-sorc default, parse_errors=0, clean-exit) ·
  floater PASS with real-frame **`359 (94%)`** (live gauge pct — the KF-5→KF-7 chain visible
  on screen) · picker PASS (7 fights). Mid-lane frame swap absorbed per the KFL-20 guard
  (DEFAULT_FIGHT + floater retarget tick 51→19, assertion widened to well-formed; null-graceful
  still proven via the synth path) — ACCEPTED.
  **(b) MCP directive EXECUTED with plumbing honesty:** MCP tools are not in the sub-agent tool
  surface → drax drove the addon websocket DIRECTLY (`ws://127.0.0.1:6550`; handshake proved
  the stack live). In-project addon updated **4.0.1→4.1.0** (new `reload_scene`, `uid://`
  resolution; gitignored infra, version recorded in AGENT_STATE; the drax `class_name` collision
  patch preserved + re-verified against 4.1.0). Editor-viewport capture works; the runtime scene
  is procedural, so wall verification correctly ran on the RUNNING scene (Metal captures).
  **(c) Isolated-node capture NOT SHIPPED on this server** (all candidate commands
  UNKNOWN_COMMAND — it is the IvanMurzak/.NET feature; $15 Pro is viewport-only + no-purchases
  law). **Fork returns decision-shaped to Matt: STANDARD+CaptureRig (working today, $0) vs
  Mono build switch for IvanMurzak isolated-node.** Meanwhile `CaptureRig.tscn` +
  `capture_rig.gd` authored to spec §2 (locked turntable, 4 cams 0/90/180/270 AABB-framed,
  pinned key+fill+env, #2b2b2b, 1024px, per-angle SubViewports) and PROVEN: d2-skeleton 2×2
  composite + meta (aabb 1.93×1.70×0.28 m, tri 3574) eye-verified. Spec §6.2 GATE settled
  empirically: SubViewport readback is NULL under pure `--headless` on 4.6.3/M2 → capture runs
  WINDOWED. **(d) Drax finding endorsed → RIDER on the in-flight rotation lane:** header lacks
  arena dims; re-emission stamps `arena_width_m`/`height_m` (additive v1, zero-derivation).
  Matt field-report scorecard: item 1 (characters) untouched · items 2/3/4 (walls) FIXED +
  verified · item "new data not in use" RESOLVED on-screen (compiled roster live) pending
  rotation variety (KFL-21b). Veto-open.
- **KFL-23 (2026-07-23, conductor): ROTATION-DIAGNOSIS LANE VERIFIED — CLASS B DESIGN GAP,
  ZERO CODE — CAPTURE-PATH FORK AT MATT — CONSOLIDATED GATE-2 FIRED (KFL-21c RELEASED).**
  **(a) Lane VERIFIED** (report `gamora/notes/2026-07-23-kf7-rotation-diagnosis.md`, collab
  `94939a3c`): engine HEAD unchanged at `c5a2f2d` (tree noise only — zero simulation code);
  40 frames untouched (mtime 06:11 = the re-emission write; rider + validation-table branch
  correctly did NOT fire — both gate on re-emission). Conductor eye-verified the selector code
  (`_dps_score:2073` = `dm/max(cd,0.5)`; mana-family → `greedy_capstone():2124`; role gates
  `ai_strategies.py:456-464` + spatial mirrors all key off `skill.role`) and re-ran the compile
  probe INDEPENDENTLY: **every skill of every compiled kit carries `role=None,
  cooldown_seconds=None, cast_priority=None`** — fire-sorc FireBall dm 2.63 == Meteor 2.63
  (first-wins `max()` → **Meteor structurally unreachable**); bonestorm 10.0 vs 1.0 (greedy
  CORRECTLY skips the control skill). **The selector is faithful; the discriminating input does
  not exist upstream — NOT the flat_damage pattern (missing INPUT, not disconnected wire).**
  Per-kit taxonomy endorsed: firewall/cyclone mono-skill legitimate (cyclone = the charter's
  named channel-commit case); fire-sorc + bonestorm genuine gap; gd-flames GAP-moot until T4.
  Zero-code disposition CORRECT under Class B law.
  **(b) COMMITMENT BOUNDARY → AT MATT (capture-path fork, decision-shaped in status):**
  Path 1 = harvest per-skill `role` (KF-2 schema extension, cross-seam elrond/legolas dispatch;
  fixes the gap at its true location; lights the EXISTING role gates with zero selector change;
  generalizes to the full corpus) — gamora long-term lean + conductor lean. Path 3 = curated
  per-kit `cast_priority` for the pilot-5 (in-seam stopgap; ~10-line priority-tiebreak branch +
  hand table Matt must ratify per kit; high demo fidelity, does not generalize). **Path 2
  (geometry→role heuristic) REJECTED by gamora AND conductor** — fabricates a design signal
  from geometry, launders a global ruling as a derivation, lowers fidelity, and would poison a
  later Path-1 migration (heuristic-role frames Matt has watched become the felt baseline).
  Conductor sequencing lean: watch brief proceeds on the damage-faithful frames WITH the
  rotation gap named (rotation was never in KF-7's exit predicate — it is a surfaced finding);
  Matt's path ruling charters the NEXT lap, blocks nothing in-run. Veto-open.
  **(c) Consolidated scoped Gate-2 FIRED** (jack-ryan, named): Part 1 = engine range
  `a63d656..c5a2f2d` (ratified base_mean shape at `kit_compiler.py:280`, smoke band re-center,
  INFO-1 docstring, rider-ii `skill_cooldowns`; + positivity-assert NOTE disposition check);
  Part 2 = ENDORSE-or-CHALLENGE the Class B classification (soundness only — the path fork
  stays at Matt). Findings to `jack-ryan/notes/2026-07-23-kf7-consolidated-gate2.md`.
- **KFL-24 (2026-07-23, conductor): CONSOLIDATED GATE-2 VERIFIED (PASS-WITH-NOTES + ENDORSE,
  NO BLOCK) — ALL RUN GATES GREEN — WATCH BRIEF DELIVERED — RUN EXIT PREDICATE MET.**
  **(a) Gate-2 VERIFIED** (findings `jack-ryan/notes/2026-07-23-kf7-consolidated-gate2.md`,
  collab `913fdaa4`, scope clean — findings file only). Part 1 (engine `a63d656..c5a2f2d`):
  **PASS-WITH-NOTES, 4 GREEN / 0 RED / 0 GAP** — magnitude ruling-exact at source + live +
  smoke + per-kit arithmetic; band [70,130] a genuine center-drift guard (base_max regression
  corner 144.28 RED / base_min corner 63.8 RED; same ±20% envelope, center slid to 100);
  INFO-1 docstring resolved; `skill_cooldowns` pure-read null-safe v1-additive. Positivity
  assert CLOSED (landed at `b492c77`, inherited, 59/59 amount>0). Jack-ryan self-corrected his
  prior direction slip authoritatively: **damage÷1.202, kill-time×1.202**. Part 2: **ENDORSE**
  — Class B sound at SOURCE level (`SkillRow` carries no rotation discriminator; `ordinal` is
  provenance not intent; `factor_role` is damage-math not rotation); all three capture paths
  confirmed to presuppose new input (none is a latent wire). **Conductor's independent
  reproduction:** all four live primary magnitudes match the findings TO THE DECIMAL
  (bonestorm 257.0 · fire-sorc 242.5 · cyclone 376.5 · firewall 1308.0); Meteor 1256.0 = its
  own band mean (consistent). **One representational nuance (no bounce):** `:280` injects None
  for GAP but assembled effect params coerce to `0.0` (conductor probe) — the BINDING predicate
  is frame-level honesty and it HOLDS (gd-flames amount 0 / pct null). Bone Cage magnitude 0.0
  noted for the next-lap rotation charter: a firing control skill emits honest 0-damage
  floaters — correct for a cage.
  **(b) RUN EXIT PREDICATE MET.** KF-1..KF-7 all closed-or-verified; watch brief + controls
  card delivered to Matt (RL-6 self-contained). Run enters WATCH state: Matt watches the 40
  compiled-pilot fights on the fidelity instrument. **Open forks AT MATT (each charters a next
  lap; none blocks the run close):** (1) rotation capture-path — Path 1 harvest `role` (gamora
  + conductor lean) vs Path 3 curated pilot-5 `cast_priority` stopgap vs Path 2 REJECTED;
  (2) Mono/.NET build switch for isolated-node capture vs STANDARD+CaptureRig (conductor lean:
  stay STANDARD); (3) KT-5 King-twin verdict (KING-TWIN run close). Next-lap docket candidates
  carried: sim-side obstacle geometry (interior walls entities respect); `expected_max_hp`
  source-HP harvest anchor; arena-dims header stamp (rider re-arms on any future re-emission);
  cooldown/cast-progress additive fields; skill-idx variety validation (re-arms with rotation).
- **KFL-25 (2026-07-23, conductor): MATT RULINGS + FIELD REPORT v2 — RUN RE-OPENED (KF-8
  CHARTERED: CONDUCTOR-IN-SCENE VERIFY + CORRECT).**
  **(a) RULING R1 — rotation:** START Path 1 (harvest per-skill rotation data) with a PROBE
  fired now to gather/locate the data; **FALLBACK = hand-authored `cast_priority` for the
  pilot-5** if the source material lacks it. (Matt wrote "#2 hand authored for these 5" — the
  description matches the memo's Path 3; intent unambiguous, ledgered as hand-authored-5. The
  geometry→role heuristic remains REJECTED.) **Probe lane FIRED (named-legolas, Mode A):**
  does already-collected source material carry per-skill rotation/role signals; extract the
  pilot-5's actual source rotations with citations; assess harvestable-at-scale vs
  hand-author. Report → `legolas/notes/2026-07-23-rotation-metadata-probe.md`.
  **(b) RULING R2 — FIELD REPORT v2 + RE-OPEN DIRECTIVE (verbatim intent):** drax's work NOT
  snapped to grid for the levels; camera WAY off; does NOT replicate the king scene; Matt
  suspects the live source-joined battle data (source DBs, join key per character) is NOT in
  use — "same initial made up data from before the king scene." DIRECTIVE: conductor inspects
  LITERALLY IN GODOT (MCP wire; **.NET/Mono switch PRE-AUTHORIZED by Matt if needed for
  conductor eyes**); "Do not end this run until you verify ALL of these facts and then correct
  them yourself." **CHARTER OVERRIDE (Matt-ratified): the conductor no-production-code law is
  SUSPENDED for KF-8 scope** — conductor corrects in-scene with own-eye verification per edit.
  **(c) CONDUCTOR SELF-AUDIT (ledgered):** KFL-22 verification rubric was DATA-HONESTY (wall
  line vs recorded positions) — NOT TWIN-FIDELITY (replicates the king scene). Grid arithmetic
  self-indicts: 44 ∉ 2.5·ℤ (17.6 tiles → ceil 18 → tile field 45 vs wall line 44 = off-grid
  seam BY CONSTRUCTION). Camera never compared against the king rig. Rubric gap owned.
  **(d) KF-8 GATE — five facts to verify in-scene, then correct:** (i) grid-snap of levels
  (tile field vs wall line vs floor plane); (ii) camera vs the king-scene rig; (iii) twin
  register fidelity (king-crypt dressing cadence at the rebuilt scale); (iv) per-character
  data provenance — join-key audit of what is source-joined TODAY (player skills/damage/
  element: compiled + byte-verified) vs NOT (player HP = rider-(i) named gap; mobs = neutral
  synthetics, KF-3 gap; rotation = R1); (v) imported-twin snapping audit (what drax imported
  vs the king scene). Corrections by conductor; harvest-class gaps (mob join, source HP)
  return decision-shaped as next-lap laps, not silent scene hacks.
- **KFL-26 (2026-07-23, conductor): KF-8 EXECUTED — five facts verified LIVE, corrected by
  conductor, re-verified; BYTE-CHAIN LOCKED; Mono fork RESOLVED.**
  **(a) INSTRUMENT + BEFORE WALK:** NEW `scripts/kf8_verify_twin.gd` (SceneTree walk of the
  LIVE replica scene, `[kf8]` VERDICT lines per fact) confirmed Matt numerically on every
  count: walls at raw sim bound 44.0 ∉ 2.5·ℤ (residue 1.5); 18-tile floor field spans 45 →
  pierced 1.0 m past walls; 3/4 pillars + arch off-lattice; 4 m debug grid clashing with the
  2.5 m tile lattice; camera FOV 46 / pitch −54.4° / dist 1.05× / target y=0 vs king register
  FOV 30 / rake −34.6° / 1.498×max-dim / target (w/2, 0.5, h/2).
  **(b) CORRECTIONS (charter-override scope, conductor-authored):** `render_kt3_arena.gd`
  quantizes DRESSING up to whole tiles (44→45; sim dims stay data authority — architecture
  snaps, data doesn't); `replica_playback.gd` carries the king register as the camera HOME
  re-established per fight-load (orbit/zoom = deviation from king home); debug grid
  proxies-only. AFTER walk: **all five facts GREEN**; smoke GREEN; Metal capture eye-verified
  (`gandalf/captures/2026-07-23-kf8/kf8_after_tick40.png`). Godot commit `3315953` PUSHED.
  **(c) FACTS iii/v:** king lighting/env register matches VERBATIM (never broken — bg/ambient/
  glow/KeyLight all exact); rig heights at register (player 1.88 m ≈ 1.85 target; mobs
  1.43–1.73 in band); entity positions remain continuous sim floats BY DESIGN.
  **(d) BYTE-CHAIN LOCKED (Matt directive "no MADE UP SKILLS / MADE UP STATS" —
  source→compiled→frames→scene):** corpus `kit_numeric` Fire Ball (227+258)/2 = **242.5** =
  compiled magnitude EXACT; Meteor 987+269 = **1256** EXACT; fireball manacost **14.5** EXACT;
  Fire Mastery +163% → **×2.63** EXACT (R-M1). Frame
  `replica-d2-fire-sorc__blind__…seed20260722` damage event carries
  `expected_premit = 637.775 = 242.5 × 2.63` TO THE THIRD DECIMAL; `source_id = d2-fire-sorc`
  byte-equal join key; `skill_idx 0 = "Fire Ball"` per header roster; realized `amount`
  358.8/346.9 with `pct` 93.77/90.65 (the gauge vs source expectation; aggregate median 96.51
  · n=280). The scene renders these very fields (KF-6 §8 zero-derivation). The dm-tie root
  (Meteor never fires) is SOURCE-FAITHFUL — mastery multiplies both fire skills; the sim-side
  first-wins resolver is the cause → rotation lane (R1). Provenance truth table: KFL-25d.
  **(e) NEW FINDING — Meteor energy_cost is a MADE-UP DEFAULT:** compiled 10.0 is the
  `_skill_energy_cost` fall-through (kit_compiler.py:656–670 branches Fire Wall / Cyclone /
  Fire Ball ONLY); source manacost **26 EXISTS in corpus** under R-T3 (IDENTITY: per-cast mana
  stays per-cast). A genuine instance of Matt's feared class — masked today by the dm-tie, but
  MUST land WITH the dm-tie fix or Meteor over-fires ~2.6× when the tie breaks. Gamora seam;
  joins the `flat_damage` rename (KF-5 §BLOCKER) as a two-line compiled-kit fidelity patch.
  **(f) MONO FORK RESOLVED — STANDARD build suffices:** MCP addon 4.1.0 command surface
  enumerated from `addons/godot_mcp/commands/*.gd` + wire PROVEN end-to-end (editor launch,
  handshake, scene tree, editor+game screenshots, run/stop, runtime state, freeze/step).
  No .NET switch needed; KT-5 conductor-eye verification unblocked on the standard build.
  Instrument cleanup done (game stopped, editor quit).
  **(g) ROTATION PROBE VERIFIED (R1 Path 1):** legolas
  `legolas/notes/2026-07-23-rotation-metadata-probe.md` (`631ae85a` pushed) — corpus has NO
  machine-readable role/cast_priority; pilot-5 rotations fully documented WITH source
  citations; 7-value role enum (α) recommended (~60-70% mechanically derivable + LLM-label
  remainder); the hand-author fallback CONTENT is thereby already delivered. Nuance ledgered:
  probe's "energy_cost or cooldown" mechanism recap is loose — mechanism of record remains
  KFL-23 dm-tie first-wins (now source-faithful per (d)).
  **(h) TASTE FORKS parked for Matt (Fork-3-compliant — observed, NOT silently changed):**
  (1) action reads small at 44 m span under the proportional king pose (options: tighter dist
  factor / action-follow cam as deviation from king home); (2) edge bone-deco reads large at
  rebuilt scale (genre-honest crypt dressing; Matt's eye rules).
- **KFL-27 (2026-07-23, MATT RULING): RUN LOGGED AS FAILED. Run CLOSED.**
  Matt's verdict, delivered after the KF-8 closeout report, recorded verbatim-intent: **the
  KIT-FIDELITY run is FAILED.** Logged without softening. The conductor's own failure
  taxonomy (evidence-grounded; grounds are the run's record, not projected motives):
  **(1) Verification-claim inflation — twice.** KFL-22 claimed VERIFIED on a data-honesty
  rubric while the owner's question was twin-fidelity (owned at KFL-25c); KFL-26 claimed
  all-green and the owner ruled the run failed anyway. The owner's eye is the instrument of
  record; the run's gates twice measured a narrower rubric than the owner's question.
  **(2) Decidability bought by predicate-narrowing = intent leak.** Exit predicates (KF-1..
  KF-7, then the five KF-8 facts) were all formally MET — and the run still failed its
  purpose. The charter converted "watchable source-faithful twin" into checkable predicates
  that no longer covered the intent. This is a charter-time ELICITOR/ARCHITECT failure by the
  conductor-author: "replicates the king scene" and "source data visibly in use" only became
  gates when Matt forced them (field report v2), not at launch.
  **(3) Fidelity gates gauged the JOINED fraction; they never audited COVERAGE.** The watched
  surface is majority-synthetic: 40/41 entities unjoined (KF-3 mob gap), player HP unjoined,
  Meteor cost a compiler default, and the flagship kit never casts its signature skill
  (dm-tie → rotation gap). A fidelity run must gate on what fraction of the VISIBLE SCENE is
  source-joined, not only on the accuracy of the joined minority. The byte-chain lock (KFL-26d)
  is real — and it certifies a sliver of what the camera shows.
  **(4) Matt field checks arrived too late in the interface design.** The declared Matt
  interface (§6) put the owner's eyes at the END (watch brief). Both failures were caught by
  Matt's eyes, neither by the run. Presentation-surface runs need mid-run owner eye
  checkpoints as pre-registered gates, not post-hoc field reports.
  **DISPOSITION:** run CLOSED — FAILED. The failure is of the RUN (charter + gates + claims),
  NOT of the artifacts' honesty: the byte-chain evidence, kf8 instrument, corrected scene,
  captures, probe report, and ledger stand as pushed inputs to next laps. Per pattern §4 a
  FAIL is a processable finding — the next-lap docket + conductor lessons live in the
  wind-down (`gandalf/notes/2026-07-23-kit-fidelity-run-wind-down.md`). A desirable-run-
  pattern amendment observation (coverage-gates + owner-eye checkpoints + rubric-gap
  discipline) is QUEUED for a future session, not executed in wind-down.
- **KF-2/KF-3:** CLOSED (KFL-10a). **KF-4:** VERIFIED + Gate-2 PASS (KFL-12a); post-fix 36/0/1.
  **KF-5:** VERIFIED + consolidated Gate-2 **PASS-WITH-NOTES** (KFL-18a); item-6 **RULED (a)**
  by Matt (KFL-19a). **KF-6:** VERIFIED + pushed (KFL-17). **KF-6b:** VERIFIED + pushed
  (KFL-22); **KFL-22 rubric gap OWNED at KFL-25c**. **KF-7:** re-emission VERIFIED + pushed
  (KFL-21a); rotation Class B (KFL-23a); **rotation RULED R1: Path 1 + probe, fallback
  hand-authored-5** (KFL-25a, probe IN FLIGHT); consolidated Gate-2 VERIFIED (KFL-24a).
  **KF-8: EXECUTED (KFL-26) — five facts verified + corrected; byte-chain LOCKED; godot
  `3315953` pushed. RUN VERDICT: FAILED (KFL-27, Matt ruling 2026-07-23) — RUN CLOSED.
  Artifacts stand; failure taxonomy + next-lap docket in KFL-27 and the wind-down doc.**

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
