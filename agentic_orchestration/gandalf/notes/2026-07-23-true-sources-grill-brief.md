# TRUE-SOURCES grill brief — agenda for the ultra-think session

**Date:** 2026-07-23 · **Author:** gandalf (`ELICITOR` prep; runs as Pattern-B dialogue when Matt opens the session)
**Commissioned:** Matt 2026-07-23 — *"let's pause and take some time to ultra think how to get the true sources flowing in, but based on a solid plan for why — and when. Would it make sense to start with a baseline of one game, from which we can convert all others using modified join keys to our engine?"*
**Evidence base:** legolas join-surface probe (`agentic_orchestration/legolas/notes/2026-07-23-join-surface-probe.md`) · KIT-FIDELITY wind-down §3 survivals (`agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-wind-down.md`) · `agentic_orchestration/research/datamine-acquisition/ACQUISITION-LOG-2026-07-21.md` · coverage matrix 2026-07-21.
**Session output:** rulings **TSR-1..TSR-5** — they seed the VDM-2-class run charter(s). Nothing here is decided; leans are stated per ELICITOR discipline (*elicit, don't impose*) and every fork ends at Matt's ruling.

---

## §0 The owner's question

**Why** does true-source data flow into the engine, and **when** — decided sharply enough that the first flow run is charterable under the desirable-run pattern (bounded substrate, decidable target, §6 failure-lap lessons applied at charter time).

The WHY, compressed from the evidence: (a) **scale** — hand-harvest cost ~188 `kit_numeric` rows for ONE kit; 265 roster kits hold zero; the datamine lane is the only path that reaches 270. (b) **fidelity** — KIT-FIDELITY failed on a majority-synthetic surface; mobs, rotations, and full stat blocks need data web guides don't carry. (c) **verifiability** — raw files + computed oracles give byte-provable provenance where web-guide anchors give trust.

## §1 The evidence floor (five facts, all cited)

1. **The corpus is 5 kits deep in exact numbers.** `kit_numeric` holds 458 rows total; 456 sit in five kits (d2-fire-sorc 188, d2-firewall-sorc 106, poe2-bonestorm 104, poe1-cyclone 32, gd-flames-of-ignaffar-purifier 26). The other ~265 roster kits are prose/lattice only. (Probe §1.)
2. **The landing zone is already built — and empty.** `skill_geometry_band.exact_json` + `exact_source_type` were designed for datamine ingest: **0 of 490 rows populated**; every geometry band currently derives from `dossier-prose`. (Probe §1.)
3. **Raw files are on disk for 3 of 5 roster games.** D2 `Skills.txt` (256-col TSV) · PoE1 RePoE `gems.json` (2022-era; live fork `repoe-fork/repoe` exists, updated 2026-07-14) · GD `all_skills.js` (3.0 MB, complete 60-rank arrays). GD `.arz` (Steam purchase → DepotDownloader, matt_to_do T4) upgrades GD; **LE has no lane landed.** (Probe §2; acquisition log.)
4. **The three sources don't store the same KIND of number.** D2 = pre-formula raw integers (Fire Ball `EMin=12/EMax=28`) behind band-deltas + `HitShift=7` bit-shift; the corpus's VDM-1-verified anchors are **post-formula player-facing** (6–15, rankedboost). PoE1 = explicit per-level absolutes (9–14 at L1). GD = 60-rank absolute arrays (57–85 at R1). Same archetype, three scaling shapes, **two formula-positions.** (Probe §2d, §5.1.)
5. **Join keys are asymmetric.** D2 joins by English name natively; PoE1 by English dict key; GD by opaque `sk296` IDs + localization tags — **no English name in the payload**; the name-bridge table does not exist yet. Corpus `kit_id` byte-join is proven (KIT-FIDELITY: `d2-fire-sorc` corpus→compiled→frames→scene to the third decimal). (Probe §3; wind-down §3.)

## §2 The forks

### TSF-1 — Truth register: which side of the formula chain is canonical?

| Option | Shape | Cost |
|---|---|---|
| (a) **Player-facing canonical** | Schema stores what the player's tooltip shows; adapters evaluate each game's formula chain (D2: band-walk + HitShift) to produce it; raw inputs retained as provenance fields | D2 adapter must script the formula chain (currently unscripted — probe Gap #1) |
| (b) **Raw-stored canonical** | Byte-faithful to files | Corpus anchors don't join without running the formulas anyway; `EMin=12` is a number no D2 player has ever seen |
| (c) **Dual-register** | Both raw + realized as first-class columns | Schema bloat; two truths to keep synchronized |

**Precedent:** the genre's entire numeric discourse is post-formula — PoB, grimtools, and the Amazon Basin all COMPUTE player-facing values from raw precisely because raw is unreadable. VDM-1 verified post-formula anchors; the KIT-FIDELITY byte-chain proof lives on the post-formula side. Raw-only would orphan both.
**Lean:** (a), with raw retained as provenance — (c)-lite without the parallel register.
**Unlocks:** the adapter contract — what number an adapter must EMIT.

### TSF-2 — Adapter architecture: per-game adapters vs convert-through-baseline (Matt's question)

The probe's fill-status matrix (§4) delivers the verdict line: *"No source is naturally flat enough to serve as a baseline for the others without losing structurally load-bearing fields."* D2-as-baseline forces delta-reconstruction onto natively-absolute PoE/GD numbers and has no carrier for `damage_effectiveness`; PoE-as-baseline forces stat-ID vocabulary onto everything and makes D2 crit a permanent special case.

| Option | Shape | Cost |
|---|---|---|
| (a) **Per-game adapters → ONE normalized exact-fields schema** (probe §4's 12-field candidate is the draft) | Each adapter owns its game's formula/vocabulary quirks; schema stays game-agnostic | N adapters to build (but N=5, and they're small) |
| (b) **Convert through a baseline game's vocabulary** | One converter to start | Bakes the baseline's era-isms into every other game's data — the D2 HitShift worldview applied to GD rank arrays; collisions 1+2 (probe §5) are structural, not cosmetic |

**Precedent:** emulation cores target a common frontend API — nobody converts SNES through NES. Our own `normalization_rule` table already points the adapter way (per-`source_scale` transform rules).
**Lean:** (a), decisively — this is the fork I'd push back hardest on if ruled (b). **Matt's baseline intuition survives as: the baseline is the FIRST adapter — the game that proves the schema.** That reframing is TSF-3.
**Unlocks:** one schema vs one converter.

### TSF-3 — First adapter: which game proves the schema?

| | **D2** | **PoE1** | **GD** |
|---|---|---|---|
| For | Join proven end-to-end (pilot-5); richest corpus anchors (188+106 rows) = built-in verification oracle | Machine-shaped per-level absolutes — nearest to normalized already; biggest roster (94) | Clean rank-arrays; `.arz` upgrade en route (T4) |
| Against | Hardest formula chain (band-walk + HitShift + synergy calc) — unscripted | 2022-stale payload (refresh via `repoe-fork` first); stat-position fragility | Name bridge MISSING (`sk`-ID→English unscripted); crit absent from payload |

**Lean:** **PoE1 first** (cheapest schema proof) **+ D2 immediately second** (the formula-chain discipline case — and the corpus's 294 verified D2 anchor rows become the oracle that CHECKS the D2 adapter's formula evaluation: the two lanes verify each other). GD third, once the name bridge + `.arz` land. Counter-lean, defensible: D2-first because its join is already proven — cost is debugging schema and formula chain simultaneously.
**Unlocks:** the VDM-2 charter's substrate choice.

### TSF-4 — Verification oracle: what checks an adapter's output?

Options: (a) corpus `kit_numeric` anchors (VDM-1-verified; deep on 5 kits — one per roster game **except LE**); (b) community calculators (PoB, grimtools) as computed oracles; (c) both — anchors where deep, oracle spot-checks where not.
**Lean:** (c). Note the inversion worth saying out loud: **the corpus lane stops being the thing datamine replaces and becomes the thing that verifies datamine adapters.** LE flag: no deep-anchor kit AND no raw lane — the roster's verification orphan; park it last.
**Unlocks:** gate design for any flow run — rubric law: the owner's question is "does the engine consume real numbers," and the gates must measure THAT, not a proxy.

### TSF-5 — What "flowing in" MEANS, and when (the sequencing ruling)

Candidate first decidable targets (they nest — (a) ⊂ (b) ⊂ (c)):

- **(a) `exact_json` 0→N.** Populate `skill_geometry_band.exact_json` for pilot-5 kits from adapter output — the landing zone already exists; a count is the gate.
- **(b) Compiler consumption.** `kit_compiler` reads the normalized schema — retires the Meteor-cost fall-through class of bug at the root (KFL-26e).
- **(c) Surface re-run.** KIT-FIDELITY lap 2: the king-twin scene re-rendered on datamine-sourced numbers, coverage-gated per pattern §6.1.

Sequencing vs the KIT-FIDELITY docket: **mob-harvest (docket #1) should CONSUME the normalized schema, not precede it** — else mobs land in yet another ad-hoc shape and we pay the adapter tax twice.
**Lean:** thin vertical slice — (a) for pilot-5 through one adapter, verified against corpus anchors (TSF-4), THEN mob-harvest rides the schema, THEN (b)/(c). Coverage-before-accuracy applied prospectively: prove the pipe on 5 kits before pumping 270.
**Unlocks:** the WHEN — and whether mob-harvest waits.

### TSF-6 — Sim-fidelity instrument: blind hero vs source-game enemy roster *(Matt-proposed at session open, 2026-07-23)*

The **engine-truth** question, separated from **pipe-truth** (TSF-1..5): can the battle sim faithfully REALIZE a source game's spatial combat parameters — aggro range, movement speed, attack cadence, pack behavior — tested by importing ONE game's enemy roster against a fixed **blind control hero** in the engine as it is today. Enemy-side only, by design ("that may be all we need to prove this hypothesis").

Ground-truth ladder (the central sub-fork): **(a) parameter-fidelity** — realized sim behavior matches ingested params under a PINNED unit conversion; machine-decidable in-run. **(b) behavior-fidelity** — emergent dynamics vs captured source-game play; lands at the owner's eye (pattern §6.2 pre-registered checkpoint, not an end-brief). Other sub-forks: blind-hero spec (stationary "anvil" vs scripted "kite-line" — kiting is what exposes aggro/leash/reacquire); source game (GD favored — `.arz` DBRs carry monster AI fields; download in flight via T4); unit-conversion pin (probe collision #2's spatial twin — unfalsifiable fidelity without it).

Lineage: gamora's aware-vs-blind fighter ablation (2026-07-22 notes) supplies the blind-agent machinery; KIT-FIDELITY's provenance table names mobs as the 100%-synthetic layer this attacks. **Interaction with TSF-5:** if this is the definitive instrument, the spatial slice argues for running BEFORE breadth-pumping — prove the consumer, then scale the pipe — and mob-harvest's field list expands (aggro/speed/pack, not just HP/DPS). Research in flight: legolas engine-calibration + sim-fidelity methods note.
**Lean:** run it — as its own desirable-pattern run AFTER the units + ground-truth-register rulings land.
**Unlocks:** mob-harvest's true field list; where the sim-fidelity run sits in the sequence.

## §3 Session shape + parking lot

Six rulings, **TSR-1..TSR-6**, one per fork; I bring pushback where leans meet resistance. **Parked (explicitly NOT this session):** D2 1.13-vs-D2R era policy (CASC extraction is acquisition Phase-2); LE acquisition path; GD monster HP/DPS gap (browser-computed — needs its own probe); PoE radius-unit normalization; PoE2/LE adapter order beyond "after schema proven."

---

## §4 Rulings ledger (live — appended as Matt rules)

| # | Fork | Status | Date |
|---|---|---|---|
| **TSR-6a** | TSF-6/Q1 — ground-truth register | **RULED (Matt):** rung (a) parameter-fidelity is the RUN's gate (machine-decidable in-run); **both rungs required for the hypothesis PASS** — rung (b) behavior-fidelity acquired via Matt PLAYING GD on his PC under agentic screen-capture monitoring; Matt proposes OpenAI Codex 5.6 Sol via API as the capture-analysis instrument ("exceptional at screen capture"). Conductor routing note: capture-analysis lands in galadriel's seam (visual-perception steward); the model is an in-seam implementation choice; OpenAI-key provisioning = new matt_to_do row at Track-B charter time (same billing-discipline class as T3). Rung (b) = pre-registered capture checkpoint per pattern §6.2, not an end-brief. **AMENDED (Matt, later same session):** Sol NOT pre-committed — cost concern + "there may actually be better vision models"; capture-model choice goes to a vision-model mini bake-off (Sol vs peers) at Track-B charter time, galadriel seam. | 2026-07-23 |
| **TSR-6b** | TSF-6/Q2 — blind-hero spec | **RULED (Matt):** anvil + kite-line, both arms (conductor lean adopted). The kite-line attacks the TrinityCore-documented leash gap (TC #25833) — the parameter class the largest engine-recalibration community has fought longest. | 2026-07-23 |
| **TSR-6c** | TSF-6/Q3 — unit-conversion pin | **RULED (Matt):** pin principle AGREED — constant derived once at charter, logged veto-open, no post-hoc fitting; conductor executes derivation as step 0. Conductor note: Track A may LAUNCH on a provisionally-pinned K from DBR internals (gameengine.dbr globals + characterRunSpeed), declared veto-open; Matt's PC capture session later upgrades K to externally-anchored — Track A does NOT block on the capture. | 2026-07-23 |
| — | Substrate event | **GD Definitive LANDED** (~10 GB; T4 struck → DONE): `database.arz` 56M + `GDX1.arz` 40M + `GDX2.arz` 32M + Crucible ×3; **ArchiveTool.exe + DBREditor.exe in-depot** — extraction agent-executable. legolas calibration research (`legolas/notes/2026-07-23-engine-calibration-and-sim-fidelity-research.md`, pushed `cc53fbe0`) confirms grimtools spatial-NEGATIVE ×3 sources: **.arz is the sole carrier** of GD aggro/sight/leash/speed/pack fields — no community resource anywhere documents them. | 2026-07-23 |
| **TSR-1** | Truth register | **RULED (Matt):** (a) player-facing canonical; raw file values retained as provenance columns. | 2026-07-23 |
| **TSR-2** | Adapter architecture | **RULED (Matt):** (a) per-game adapters → ONE normalized exact-fields schema; convert-through-baseline rejected. Baseline intuition survives as "the first adapter proves the schema" (= TSR-3). Research support was five-for-five: every calibration community runs one-reference→one-target; none converts through a baseline. | 2026-07-23 |
| **TSR-3** | First adapter | **DEFERRED-FOR-EVIDENCE (Matt):** "probe the new GD data so that we have the full source list explored before we decide." GD .arz extraction+probe COMMISSIONED same turn (legolas, background; note lands at `legolas/notes/2026-07-23-gd-arz-extraction-probe.md`). Ruling re-presents when the probe files. | — |
| **TSR-4** | Verification oracle | **RESOLVED-SHARPENED (veto-open):** Matt's model confirmed — the unit of verification is the ADAPTER, not the kit; sharpened to per-FORMULA-FAMILY coverage (compiler-test-suite shape: one anchor kit per formula family per game proves the code path; burden O(families×games) ≈ 15–25 anchor kits total across 5 games, 5 already banked — never 270). Three-tier stack: (1) family anchors gate adapter first-PASS; (2) in-pipe mechanical asserts on EVERY row (non-null, monotonic rank arrays, range bounds — oracle-free); (3) sampled spot-checks vs community calculators (N random kits/game) for per-record weirdness. LE = verification orphan (no anchors, no raw lane), parked last. | 2026-07-23 |
| **TSR-5** | Sequencing — what "flowing in" means first | **RULED (Matt):** thin vertical slice agreed. Timing sub-question ("when does the battle-sim monster test fit?") answered: the GD probe is shared upstream of everything → **TSF-6 Track-A run charters IMMEDIATELY post-probe** (prove the consumer first; smallest data dependency — monster records + unit pin + gamora's existing blind-hero machinery, NO schema needed) ∥ skill slice charters the moment TSR-3 rules; parallel-safe (gamora vs elrond/star-lord seams, no shared writes; sim-test failure doesn't block pipe work — adapters are needed regardless). Track B rides Matt's PC capture session, independent timing. | 2026-07-23 |

**Conductor-pinned decision rules (reasoning-boundary, veto-open):** (i) difficulty-tier for any GD comparison pins to **Normal** — base DBR values ≈ Normal; Veteran/Elite/Ultimate are multiplied tiers (legolas Risk #3); (ii) pathfinding residuals quarantined via flat-open-topology arena — parameter gates never conflated with pathing-implementation divergence (legolas Risk #4, independently matching the conductor's pre-registered finding class); (iii) attack-cadence fields flagged animation-time-vs-logic-time at import (legolas Risk #2) — movement/aggro import clean, cadence imports carry a conversion flag.

---

**Signed:** gandalf (`ELICITOR`), 2026-07-23. The forks are drawn; the rulings are yours.
