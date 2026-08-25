# KC2 LIFT RUN — charter + ruling ledger (desirable-run pattern)

> **STATUS:** LAUNCHED 2026-08-25 (Matt's launch word; ledger L-1) — RUN IN FLIGHT. Successor to the **KC2 MODEL-COMPLETION RUN** (`2026-08-24-kc2-model-completion-run-charter.md`, RUN CLOSED at L-95). Conductor: gandalf `RUN-CONDUCTOR` (charter's author conducts — intent residency, desirable-run-pattern § 2 element 3).
> **Pattern authority:** `agentic_orchestration/operating-procedures/desirable-run-pattern.md`. **Fit test § 3: all four YES** (evaluated at § 3 below).

---

## § 0 — Intent (whose words, what outcome)

**Matt's charter-intent (KC2-MC, verbatim, still governing):** *"the goal is to provide the baton which will allow the godot team to immediately create a version of it that is playable as the character. This is why I want all aspects present."*

**Matt's wire-honesty challenge (2026-08-25, verbatim):** *"It seems like may still be missing aspects of the player character based on your wording within this section (inventory, devotion, CDR).. If this is true, then the simulation is not accurate, let alone able to be played."*

**The answer of record (KC2-MC L-94) and this run's mission:** baton-v2 is a **BEHAVIORAL twin** — player-side numbers are footage-measured EFFECTIVE values (post-CDR, post-gear); the sim is accurate at that declared layer and a playable character is buildable NOW from Layer-1 + effective values. What is NOT yet buildable is the **MECHANISTIC world+kit**: state-machine monsters, true stat blocks, DoT/control/proc machinery, summons as actors, crit, target selection. **This run LIFTS that layer.** Terminal artifact: **baton-v3 — the mechanistic twin** — plus the D-CP2-1 walls+pools sim sibling and the D-CP2-2 per-skill interrupt flag, so the Godot team receives world + kit + arena as MECHANISM, not only as measured effect.

## § 1 — Bounded substrate (count it, list it, diff it)

The domain is the baton-v2 model pack's own absence registry — `kc2-model-pack-v2-E-s09-cp150-mpol2-20260825_163811/model/provenance.json` (`blocks_playability: true` rows), pack digest `302620c76347fae1183136457e7276f4e0011a955f7a87605e33e740a40a875d`; reference pack `b1034c77944dd84dde0e6d2e47d610067c0799e690a979d9561307de7844a6ed` (cross-pins model). **Nine rows, frozen at launch:**

| # | absent_id | class | substrate pin (path · sha256) |
|---|---|---|---|
| B1 | `ABS-TARGET-SELECTION` — how the pilot chooses which body to fight next | **NOT-YET-DECODED** (the only one; also a named 160-residual candidate, L-88) | none — this is the run's single DECODE lap |
| B2 | `ABS-AI-STATE-MACHINE` — 43-state monster controller: transitions + conditions | DECODED-NOT-YET-LIFTED | `data/kc2/d3_roster_controller_params.csv` · `41abf9da90d45138d0292ae03d8223d2af6f623834c3b3795664783d0c6e997b` |
| B3 | `ABS-MONSTER-STAT-BLOCKS` — per-record stat blocks, tier-16 roll pool | DECODED-NOT-YET-LIFTED | `data/kc2/pm4_band_b_ehp_by_wave.csv` · `3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024` |
| B4 | `ABS-WAVE-ROLL-POOLS` — pool membership + roll rules, waves 150–160 | DECODED-NOT-YET-LIFTED | `data/kc2/pe6_crucible_wave_pools_v2.csv` · `bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587` |
| B5 | `ABS-DOT-STACKING` — DoT application + stacking function | DECODED-NOT-YET-LIFTED | `data/kc2/d4c_dot_stacking_decode_README.md` · `63b2e2002bf7264a833d057c8cc0d857920d36f8b43780832f0d943092ffdb2b` |
| B6 | `ABS-CONTROL-APPLICATION` — control-family params + **concurrency law** (⚑ highest-value row for a Godot implementer: overlapping controls BURN each other's wall-clock, S-8; queue/refresh semantics would be WRONG) | DECODED-NOT-YET-LIFTED | `data/kc2/d7_control_application_parameters.csv` · `3f2c7250142ec2cdb95f22699f2426f9f1b5bd9faca870d1ee4952e0266b3f06` |
| B7 | `ABS-SUMMON-BODIES` — the two player summons as first-class actor templates (Layer-2 caveat: summons carry NO PATH in the recording, R-L53-2 — absence in the REFERENCE, not the model) | DECODED-NOT-YET-LIFTED | `data/kc2/d9_summon_bodies.csv` · `db6c42c445a21a54f5c18b4843bd85c38b744bae303ea3c6623d3a216e0269bc` |
| B8 | `ABS-DEVOTION-PROCS` — 8 devotion procs: host bindings, triggers, chances, ICDs | DECODED-NOT-YET-LIFTED | `data/kc2/d6_player_kit_residual.csv` · `71f2d6fc02e4526d02d85d10f3dd667bf6100b4db6dea8d29c3e4929e00b50bb` |
| B9 | `ABS-CRIT-MODEL` — crit model + limb selection | DECODED-NOT-YET-LIFTED | `src/reincarnated/simulation/kc2/offense.py` · `c0e17671ea806a3bc9ec6cb50cecc02f71d01685e6f55f15205e815aff01451a` |

**Plus two Matt-ruled build items (D-CP2, not absences):** **W1** — the walls+pools sim sibling (D-CP2-1: authored walls + spawn-pool DoT ticks in BOTH sim and live; behavior policy avoids pools; a **NEW gamora sibling, never a regrade** — K-7). **W2** — the per-skill `interrupts_channel` flag (D-CP2-2: skill-property conditional; mouse-binding demotes to referent-explanation + default-assignment heuristic).

Discoveries beyond these eleven items are FINDINGS for the next lap, never silent scope growth.

## § 2 — Decidable target-state

The run is DONE when every row below evaluates, without Matt:

1. **Per-blocker closure (B2–B9):** each block LIFTED into the baton pack as **rows-not-fields** with **(value, scope, provenance) triples** (DR-1/DR-2/DR-3 pack laws carry forward), schema-valid — **OR HONEST-FAIL declared as a named absence with pin + what-was-searched** (the honorable fallback; a failed lift is a processable finding, not a terminal event).
2. **B1 (target selection):** DECODED (mechanism + parameters, provenance-pinned) or **UNDECODABLE-FROM-SUBSTRATE declared** with the searched surfaces listed; if undecodable from save/DBR substrate, one galadriel footage lap fires before the declaration stands. Either way its 160-residual candidacy is ADJUDICATED (closes or survives by name).
3. **W1 sealed:** walls+pools sibling built to a **pre-registered prereg (D4: criteria pinned before the build)**, sealed KC2-MC cells UNTOUCHED (K-7: digests `ad61ad2a…`/`20b05cb4…` re-hash unchanged), graded against its OWN prereg — never against the wall-less referent's seals.
4. **W2 landed:** `interrupts_channel` as a skill-property in the baton skill rows, with the three measured rates (Blitz 0.385 · Vire's Might 0.136 · War Cry 0.000) carried as reference evidence.
5. **baton-v3 CUT:** digest-pinned model+reference pack pair, cut receipt, MIGRATION note; census counts stated PRE and matching POST; digests **derived, never retyped**.
6. **jack-ryan Gate-2** on the cut: no BLOCK outstanding.

## § 3 — Fit test (desirable-run-pattern § 3)

- **F1 Enumerable? YES** — 9 registry rows + 2 ruled build items; every DECODED block file+sha pinned; countable, listable, diffable.
- **F2 Decidable? YES** — per-blocker LIFTED-or-HONEST-FAIL, schema validation, prereg'd gates, digest identity; § 2 evaluates in-run.
- **F3 Pre-drainable? YES — already drained:** the foreseeable forks were converted at KC2-MC checkpoint #2 (D-CP2-1 Matt-verbatim, D-CP2-2, D-CP2-3) + standing laws (K-7, bands-not-tape, ship-ratios D-MPOL2-2, G5=0.0960 uptime correction, DR-1/2/3, D4, R-L80-2 commit law). Residual forks are reasoning-boundaries (lift-shape choices against pinned substrate).
- **F4 Authority-resident? YES** — conductor authored the specs the lifts serve (SKIRT + F-5) and holds the KC2 design lineage; commitment-boundaries (§ 5) still HALT to Matt.

## § 4 — Seats + wave plan (seams execute; conductor writes no production code)

| Wave | Seat | Piece | Gate |
|---|---|---|---|
| **1 (parallel lifts + decode)** | legolas | B1 target-selection decode lap (save/DBR/telemetry substrate first; escalate to galadriel footage lap only on UNDECODABLE) | § 2.2 |
| 1 | elrond | curation pass on B2–B8 substrate files: schema of each lifted table, join keys, absence rows where the CSVs are thin | schema-valid tables |
| 1 | gamora | W1 walls+pools sibling **prereg** (D4 — prereg commits ALONE before build) | prereg on record |
| **2 (mechanistic sim)** | gamora | W1 build + B5/B6/B7/B8/B9 lifted into sim (DoT stacking, control concurrency law, summons as actors, devotion procs, crit) + W2 flag | § 2.3/§ 2.4; sealed cells re-hash unchanged |
| 2 | gandalf sub-agent | spec-amendment pass: SKIRT + F-5 updated to D-CP2 rulings (supersession notes already appended at run close; this pass integrates) | specs consistent with D-CP2 |
| **3 (assembly)** | star-lord | baton-v3 cut: B2–B9 lifted rows + W2 + B1 outcome into digest-pinned pack pair + receipt + MIGRATION | § 2.5 |
| 3 | jack-ryan | Gate-2 on the cut | § 2.6 |

Sub-agents commit (R-L80-2: staging inspection as its OWN read call BEFORE commit; `git commit --only <paths>` with `-m` placed so it cannot eat a pathspec; never `git add -A`), **never push — the conductor releases pushes per-fold.**

## § 5 — Matt interface + commitment boundaries

- **Owner-eye checkpoints at each wave seal** (KC2-MC cadence). Red-flag pings only between seals.
- **HALT-to-Matt boundaries:** any product-seam commitment (e.g., SKIRT OQ-5's "binding exclusivity as a PROJECT input rule" — flagged, Matt's alone); any charter amendment; any result that would move a sealed grade of record; jack-ryan BLOCK; taste/naming calls.
- **Veto-open ruling ledger** below; every in-run ruling reversible until Matt's next checkpoint.
- **Push posture:** per-fold conductor-released pushes to `collaboration` + `engine` (KC2-MC precedent; the 2026-08-25 Matt ruling stands — autonomous runs do not embargo the shared trunk). Matt may narrow at launch word.

## § 6 — Standing laws carried in (pre-drained, cite-by-name)

D-CP2-1 (Matt verbatim: *"live walls for both, dot ticks in spawn pools for both (have the sim stay out of there)"*) · D-CP2-2 (per-skill `interrupts_channel` flag) · D-CP2-3 (mouse-exclusivity is referent binding-config, not product commitment) · K-7 sealed-cells-untouched · D4 prereg-before-build · bands-not-tape · D-MPOL2-2 ratios-not-levels · G5=0.0960 · DR-1 provenance-or-fail · DR-2 rows-not-fields · DR-3 triples · digests derived-not-retyped PRE==POST · R-L80-2 commit law + L-93 `--only -m` footgun (message flag consumes a pathspec → wrong SUCCESS) · `git -C <path>` on every cross-repo git op · coverage-gates-before-accuracy-gates (F-5 G-0) · EoR-consistent never promoted · instrument-per-figure · UNMEASURABLE named.

## § 7 — Ruling ledger (append-only; one row per fold/ruling)

| Row | Date | Event / ruling | Boundary class |
|---|---|---|---|
| L-0 | 2026-08-25 | Charter authored at KC2-MC run close (L-95). Substrate frozen: 9 registry rows (pins above) + W1/W2. Launch awaits Matt's word in a fresh session. | commitment (launch is Matt's) |
| L-1 | 2026-08-25 | **RUN LAUNCHED — Matt's word received in a fresh session ("This message is my LAUNCH WORD for the KC2 LIFT RUN… Begin with Wave-1. Push as you go").** Launch-state verification (slate-freshness, OP § 4.10 g-3; digests derived-not-retyped): **8/8 pinned substrate files re-hash OK** against § 1 pins; pack pair located at `src/reincarnated/output/`; receipt (`kc2-baton-v2-cut-receipt-20260825_163811.json`) digests match charter pins — model `302620c7…a875d` (10 members) / reference `b1034c77…44a6ed` (6 members); `provenance.json` `blocks_playability` = **9 rows, IDs = B1–B9 exactly**; both Matt queues glanced — no open row gates this run (charter ARCHITECT note holds). `ENABLE_PROMPT_CACHING_1H=1` confirmed live per Matt's launch-prompt ask. Push posture at launch word: per-fold conductor releases STAND (Matt did not narrow). **WAVE-1 FIRES per § 4:** legolas B1 target-selection decode lap (save/DBR/telemetry substrate FIRST; galadriel footage lap only on UNDECODABLE, routed via conductor) ∥ elrond B2–B8 curation pass (per-table schema, join keys, thin-row absences named; DR-1/DR-2/DR-3 lift shapes proposed) ∥ gamora W1 walls+pools sibling **prereg ALONE** (D4; D-CP2-1 verbatim carried; K-7 sealed digests `ad61ad2a…`/`20b05cb4…` named untouchable). Seats commit per R-L80-2 + the L-93 `-m`-eats-first-pathspec caution; seats never push — conductor releases per-fold. | reasoning (launch mechanics; the launch itself is Matt's word above) |

---

*Chartered 2026-08-25, gandalf (`RUN-CONDUCTOR`), at the close of the KC2 MODEL-COMPLETION RUN. ARCHITECT gate: the open-questions surface was drained at KC2-MC checkpoint #2 (D-CP2-1..3); no `matt_decision_needed/` rows outstanding for this run at charter time.*
