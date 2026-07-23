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
- **KF-2/KF-3:** CLOSED (KFL-10a). **KF-4:** in flight (gamora compiler). **KF-5..KF-7:** pending.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
