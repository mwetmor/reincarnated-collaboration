# Skill handoff — 2026-06-13 (knight-rider)

## Session focus: BC-measurement keystone (Session 3/4 generation cascade)

Orchestrated standing up the KIT-corpus BC-measurement keystone (rocket generation → gamora simulation → BC measurement → rocket measurement-time items). NOTE: this is the **KIT-corpus characterization-via-simulation** pass, NOT the weapon/substrate BC clustering / duplicate-detection line (Cycle 14/15) — do not conflate.

## Load-bearing ground-truth finding

Went to ground truth (confirmed with gamora) before sequencing. The keystone's **middle link — the MEASURED-bin BC pipeline (Axis 4 / Axis 3B, downstream of simulation) — DID NOT EXIST.** It's a ~1–2 day build, not a held RUN. The `bc_target_*` modules are generation-side TARGET-composition (rocket), not measurement. The rocket-generation-handoff dispatch (line 15/56) assumed it existed.

**Matt reclassification (internalize):** this is a COST DISCOVERY (authorized goal needs more engineering than assumed → in-scope, KR sequences), NOT a scope amendment (goal changes → needs Matt). The only Matt gate in the whole sequence is the eventual push-to-remote.

Also confirmed: the new-cascade Season 001010 corpus has NOT been generated (last kit_space event = 2026-06-02 QDX-5, pre-cascade); `exports/season_001010/` is a stale 2026-05-16 spatial corpus (naming collision).

## What fired this session

| # | Action | State |
|---|---|---|
| 1 | **gamora BC-measurement pipeline build** dispatch | Authored + Gate-1 PASS-WITH-INFO (2 math-note INFO folded) → FIRED. `dispatches/2026-06-13-gamora-bc-measurement-pipeline-build.md` |
| 2 | **jack-ryan Gate-2** on rocket Session 3/4 cascade | PASS, no BLOCK. 180 tests re-verified, vestigial-ontology zero-branches confirmed, reachability posture correct. **Cascade cleared to generate.** jack-ryan to author Q1–Q10 decisions-log entry (parallel bookkeeping, does NOT block). |
| 3 | **elrond Q10 FACTION_LOOKUP_TABLE redraw** dispatch | Authored + Gate-1 clean PASS → FIRED. `dispatches/2026-06-13-elrond-q10-faction-lookup-table-redraw.md` |
| 4 | **star-lord consume-side MIGRATION** dispatch | Authored, SEQUENCED as fast-follow on gamora emit-schema. `dispatches/2026-06-13-star-lord-bc-measured-bin-consume-migration.md` |
| 5 | **rocket Season 001010 generation RUN** dispatch | Authored (cleared by Gate-2 PASS) → FIRED. `dispatches/2026-06-13-rocket-season-001010-generation-run.md` |

## Gamora long-pole sequencing — RESOLVED (KR call)

Two gamora long poles competed: **BC-measurement build** vs **T4-mechanic implementation** (4 new strategies + Q1/Q4/Q5 locks + Q6/Q7 convergence/bridge). **Call: BC-build FIRST** (matches gandalf's design read) — shorter pole, unblocks the reachability + cognitive-load gates, validates the measurement plumbing before the heavier T4 block lands on the same seam. T4-mechanic is the NEXT gamora dispatch, not yet authored.

## Keystone dependency chain — current state

```
CRITICAL PATH:
  [BUILD]  gamora BC-measurement pipeline   ← FIRED (math-note gated; star-lord MIGRATION downstream)
  [RUN]    rocket Season 001010 generation  ← FIRED (Gate-2 cleared; runs concurrent with build)
              └─→ EARLY WIN: cognitive_load + coupling_depth distribution → gandalf Gate 2 (Q4)  [no build dependency]
  → when build + corpus both land → sim+measure → rocket Items 7/8 (investment_profile + reachability_report)
  → gandalf Gate 1 (vestigial reachability) read

PARALLEL:
  elrond Q10 faction redraw  ← FIRED (soft-precedes the generation RUN so identity is live; off critical path)
  jack-ryan Q1–Q10 decisions-log entry  ← in flight (bookkeeping)

CONDITIONAL:
  gandalf Gate 3 (bridge math)  → only if Season 001010 generates a Golem/Mimic bridge summoner + gamora balance check (in-band, no PoE-3.8 spiral)
```

## Gandalf re-engagement triggers (no design authoring wanted until these land)

- **Gate 2 (Q4 coupling):** fires on rocket's generation-RUN cognitive_load/coupling distribution (EARLY — no build wait). gandalf makes flip-INCLUDE_COUPLING / keep-T4-only call.
- **Gate 1 (vestigial reachability):** fires on rocket Item 8 reachability_report (needs gamora BC build + corpus). Does Berserker fire? how rare is Phantom? unreachable labels = substrate evidence, report-don't-reorder.
- **Gate 3 (bridge cap):** fires only if a bridge-bearing summoner exists in the corpus; gandalf + gamora close.

## Queued / next session

- gamora T4-mechanic implementation dispatch (the deferred long pole — author after BC-build is underway/landed)
- Watch for gamora emit-schema landing → unblocks star-lord consume-side MIGRATION (sequenced, ready)
- Confirm elrond faction table populated before rocket FULL generation fire (KR coordinates; smoke can run regardless)
- rocket resource-bounds projection on the generation RUN (Disc #1.1) — large corpus + LLM identity calls; surfaced in the dispatch
- Eventual push-to-remote at keystone-close (Matt's gate — accumulate commits until then)

## DRIVING CYCLE — execution results (same date, second cycle)

Drove the dispatches to EXECUTION (a committed dispatch has no autonomous consumer — KR is the driver).

**EXECUTED + LANDED:**
- **elrond faction table — POPULATED.** 637 records, 9 factions (8 redrawn + composite "Solar Pantheon" homing mesoamerican / sub_saharan_african / south_southeast_asian). **Zero** nearest-match fallback over all 882 cells, verified against rocket's real loader. Engine `bd64ad9`, collab `a511222`.
- **rocket Season 001010 corpus — GENERATED.** 240 in-band player kits, chronicle event `kse_20260613_001`, 0 validation errors. LLM-FREE ($0, 0.5s, <500MB — all cascade fields deterministic). Faction state LIVE (185 exact + 55 Void, 0 UNASSIGNED). New orchestrator `scripts/season_001010_cascade_gen_20260613.py` (composed from Gate-2-PASS finalizer modules; no cascade code changed). Engine `ae247af`+`8810a8d`, collab `761fb60`. Tag `rocket/v-season-001010-gen-1` CLEARED to release (Gate-2 PASS-WITH-INFO).
- **EARLY-WIN distribution — IN-HAND + RULED.** cogload×coupling N=240: LOW 4 / MEDIUM 57 / HIGH 179. 26/240 (10.8%) flip a bin under Δscore=2.0×max(0,cd−1), all coupled, all at MEDIUM→HIGH boundary. **gandalf Q4 ruling: FLIP True, CLOSED** — coupled kits cluster exactly where the term crosses a bin. jack-ryan verified the computation 3 independent ways (script re-run + on-disk recompute + hand-checked flip semantics) → safe-to-consume confirmed.
- **star-lord telemetry v2.17 + export consume-schema — LANDED.** 8 additive fields (accumulator triple `a_hit_count/sum/sumsq` + 5 scalars), `ExportKitBCMeasuredBin` consume schema matching gamora §v1.67. 12/12 + 224/224 tests PASS. Engine `3da0400`, tag `star-lord/v-bc-measure-consume-1`. **Production telemetry.db apply PENDING Matt (ADR-006).**

**TRACKED-IN-FLIGHT:**
- **gamora BC-measurement build — ~50%.** Math note landed (`bc-measurement-axis4-axis3b-2026-06-13.md`, `3422be2`); bin counts confirmed against lock; signal audit DONE (the load-bearing step); aggregator/binner scaffold + smoke green (13/13, pre-registered cells). Engine `3422be2`+`ce433aa`+`51a69c5`. **Next session:** FightResult→FightTelemetry adapter; corpus driver; full run.

**BLOCKERS / open dependencies:**
- gamora **full BC coverage** (Axis-4 dodger + all Axis-3B) was gated on star-lord's 6 fields → **star-lord schema now landed**; remaining: gamora must emit the 8 fields via `fight_log` (gamora seam, next session) + production apply Matt-gate.
- gamora **Part B live wiring + proxy companion follow-on — BLOCKED:** corpus has NO charge-stack kit, NO companion records. Needs a targeted rocket generation pass emitting both.
- gandalf **Gate 1 (vestigial reachability) + rocket Items 7/8 — still HELD** behind gamora BC build completion.
- gandalf **Gate 3 (bridge math) — conditional now UNBLOCKED:** bridge-bearing summoner PRESENT (PROXY_FISSION ×16, gamora_kernel-owned). gamora balance check (army power in-band) can proceed.

**Follow-on actions owned (next cycle head):**
1. rocket: set `INCLUDE_COUPLING_IN_SEQUENCE_DEPTH = True` (gandalf Q4 ruling) — one-line amendment; re-bins 26 kits HIGH + grants resonance/charge eligibility; generates its own decisions-log entry.
2. jack-ryan: canonical write reconciling `substrate-vector-cheatsheet` § 2 to the lock (Axis-3B 0.3/0.7; Axis-3A 2–6).
3. rocket: targeted charge-stack + companion generation pass (unblocks gamora Part B + proxy companion).
4. gamora: continue BC build (adapter → corpus driver → full run); then Items 7/8 fire.
5. HIGH-heavy cogload (74.6%) calibration question — gandalf future Pattern B; ACCEPTED non-gating for now.

## CYCLE 4 — bounded-front close (representative corpus + parallel trio)

Matt directive: HOLD the full BC run; fire the rocket representative-corpus pass (cost-discovery-scoped) + the parallel-safe trio; full BC run waits for the representative corpus. All three fires returned.

**EXECUTED + LANDED:**
- **rocket Q4 flip — LANDED.** `INCLUDE_COUPLING_IN_SEQUENCE_DEPTH = True` set in `generation/kit_finalization.py`. 235 tests PASS. Re-bin N=96: 78 HIGH / 18 MEDIUM. Commit `22478c2`.
- **rocket representative corpus — GENERATED.** 96 kits, chronicle event `kse_20260613_002`, tag `rocket/v-season-001010-rep-1`. $0 / 0.2s deterministic. Does NOT clobber `kse_20260613_001`. Contents verified: **12 charge-stack kits** (6 hold / 6 spend — Axis-5 split), **12 companion records** (6 COMPANION_CONTRACT + 6 MONSTER_PACT), full **Axis-4×Axis-3B spread** (tank/mitigator/dodger/glass = 24 each; flat/variable/spiky = 32 each; all 12 cells populated). New gen script `scripts/season_001010_representative_gen_20260613.py` + math note `season-001010-representative-corpus-2026-06-13.md`. Commit `8e79119`.
- **jack-ryan canonical writes — LANDED.** Write 1 (Q4 cogload-coupling decisions-log entry) `def5ac3`. Write 3 (cheatsheet §2 reconcile: Axis-3B 0.2/0.6→0.3/0.7; Axis-3A 2–8→2–6) `0d88fb2`. Write 2 (Q1–Q10) found ALREADY EXISTENT (gandalf authored in Pattern-B batch) — left untouched, flagged stale task. jack-ryan also flagged: **rocket should NOT self-author a decisions-log entry** (dispatch line 81 said "generates its own decisions-log entry" — decisions-log is jack-ryan's sole lane; corrected).
- **gamora BC-build — ~90%, READY-TO-RUN.** Adapter `fight_result_to_telemetry` + corpus driver `run_bc_measurement_over_corpus` landed; 8 telemetry fields emission wired (dodger + Axis-3B now measurable via `BCSignals` accumulator on `CombatantState`); subset-smoke **17/17 PASS** on real `simulate_fight(measure_bc=True)`; brownfield invariant proven (30-fight md5 byte-identical). Commits `3136fd7` + `60cce7a`.
- **gamora Gate-3 bridge balance — CHECKED, IN-BAND.** Army power bounded **2.92× owner base**, `recursion_cap=4` load-bearing, no multiplicative spiral. Note `gamora/notes/2026-06-13-gate-3-bridge-balance-check.md`, commit `8c41a8f`.

**BLOCKER CLEARED:** the full BC-measurement run was HELD pending a representative corpus carrying charge-stack + companion + full profile spread. **That corpus now exists (`kse_20260613_002`).** gamora's pipeline is READY-TO-RUN — a single `run_bc_measurement_over_corpus(...)` invocation binding the provider to the gauntlet. **The hold's precondition is satisfied; releasing the hold is Matt's call** (held full run was an explicit Matt directive — KR does not auto-fire it).

**OPEN ITEMS NEEDING ROUTING:**
- **jack-ryan Gate-2 on gamora `3136fd7`** — gamora flagged the BC-pipeline commit gates that commit. Fires when KR routes it (post full-run is natural, or now on the landed pipeline).
- **COMPANION_CONTRACT / MONSTER_PACT have no CAPSTONE_LAYER2 row** — catalog gap (why the 240-kit keystone run drew 0 companions). rocket tagged closers without self-authoring canonical Layer2 data → flagged to gandalf/elrond. Representative corpus injected companions by other means for the BC run; the canonical catalog gap remains for gandalf/elrond to close.
- **Schema note for gamora:** kit-space drops top-level `energy_type`; charge-stack identified via `substrate_trace.charge_stack` + spend-skill fields.

## CYCLE 5 — full BC run driven through to gandalf Gate 1 (TERMINAL GATE REACHED)

Matt RELEASED THE HOLD: "fire the full BC run. Gate-2 folds into post-run acceptance. Drive it through to gandalf's Gate 1." Drove the full chain. Keystone COMPLETE through its terminal gate.

**Chain executed:** gamora full BC run → [jack-ryan Gate-2 ∥ rocket Items 7/8] → gandalf Gate 1.

**Two cost-discoveries surfaced + resolved mid-chain (in-scope, KR sequenced):**
1. gamora's first run BLOCKED — kit-space corpus is a lossy down-projection (drops `stat_distribution` + full skill bodies), cannot drive `simulate_fight`. gamora refused to fabricate generation primitives (Disc #4). → rocket emitted a **simulatable sibling corpus** (`output/season_001010_representative_20260613/simulatable_corpus.json`, 96/96 round-trip, $0/0.21s, serialization-only, commit `891b49d`). Join is NOT shared kit_id — uses `kit_space_kit_id` FK (bare substrate_trace tuple has 3 collisions).

**THE HEADLINE FINDING — Axis-4 collapse + inversion, root cause = missing defensive bridge:**
- MEASURED Axis-4: glass 94 / mitigator 2 / dodger 0 / tank 0 (targeted 24/24/24/24). Axis-3B: spiky 81 / variable 8 / flat 7 (targeted 32/32/32).
- Kits intended as glass measured TANKIEST (eHP_ratio glass 1.202 > dodger 1.091 > mitigator 1.029 > tank 0.982).
- **ROOT CAUSE (rocket diagnosis, jack-ryan + gandalf corroborated):** `defensive_vitality_scale` (1.8 tank → 0.55 glass) + `shield_buffer_est`/`regen_per_sec_est`/`is_dodge_built` are WRITTEN to `substrate_trace` but have **ZERO generation-side consumers** — no stat allocator reads them. Vitality is driven by energy/element priors, decoupled from the defensive label. ONE root cause for both collapse and inversion.

**jack-ryan Gate-2: PASS-WITH-INFO** (combined pipeline `3136fd7` + run `edec4c6`). Reproduced the inversion 3 ways; certified measurement methodologically sound (boss-only panel legitimate per Disc #4; brownfield invariant byte-identical; 96/96 schema-valid; locked edges intact). Finding `e879586`. INFO-1 (load-bearing): "glass takes lowest damage" holds ONLY on the 4 physical fights; on full 8-fight basis glass takes HIGHEST damage — inversion survives because HP dominates. Design around **"glass HP advantage dominates," NOT "glass is more defensive."** INFO-2: cosmetic stale md5 in AGENT_STATE.

**rocket Items 7/8 RAN** (engine `02f84bd`, collab `befa550`). Item 7 investment_profile collapsed to high 95 / scaling 1; proxy LOW-player/HIGH-proxy signal MASKED (glass rule precedes proxy rule). Item 8 reachability: fired = Arcanist 68 / Pact-holder 12 / Stormbringer 8 / Invoker 6 / Threshold 1 / Sentinel 1. Companion 6-vs-12 flag → EXPECTED (12 summoner kits; companion_records counts summoned-entity bindings).

**gandalf Gate 1: PASS-ON-CLEAN / DEFER-CONTAMINATED / BOUNCE-BERSERKER** (note `6640f56`). Framing-audit caught a stale-code divergence the report buried:
- **Berserker is a STALE-CODE BUG, not vestigial.** gandalf authored the Berserker rule into canon last session (`f2fee41` S4 §2.3 rule 10: close+rage+front-loaded+spiky → Berserker). rocket's `vestigial_labels.py:189` still has the OLD pre-`f2fee41` rule routing to Ravager + hardcodes Berserker in `STRUCTURALLY_UNREACHABLE_LABELS`. "Implement verbatim" transcribed a stale spec. → **rocket re-syncs rule 10 to canon, then re-judge.**
- **Conduit:** CONFIRMED truth-to-design-around (intentionally retired, name-only) → keep.
- **Windrunner / Phantom:** CONFIRMED bug-blocked (dodger-gated; 0 dodger kits from the collapse) → DEFER pending bridge fix + re-run.
- **Control/terrain/hybrid/Axis-1 labels:** CONFIRMED clean (deliberate corpus scope) → PASS now.
- **Bridge fix call: WIRE IT, don't redesign** — sound intent, missing wire. Matt ratifies direction.
- **Player-experience flag:** glass-as-tankiest breaks build-identity contract (defensive labels currently cosmetic); fix must restore DIFFERENTIATED defense, not HP-bloat. Arcanist 68/96 dominance = identity-label-as-theater risk if production skews mana-caster.
- **Single re-run closes 3 deferred questions:** MEASURED Axis-4 populates all 4 bins + Axis-1 measured → tests Windrunner/Phantom reachability + Berserker true reachability + corpus-identity diversity.

## KEYSTONE STATUS: COMPLETE through terminal gate. Decision points now in front of Matt:

1. **Defensive-bridge fix (rocket seam)** — wire `defensive_vitality_scale` et al. into the stat allocator. gandalf recommends WIRE not redesign; jack-ryan INFO-1 is the guardrail (validate against MEASURED Axis-4 → 24/24/24/24, not a damage proxy). Plausibly in-scope cost-discovery to "produce trustworthy reachability substrate," OR Matt scopes it as a fresh cycle. **KR did NOT auto-fire — it's a new workstream past the keystone's terminal gate.**
2. **Berserker rule-10 re-sync (rocket seam)** — code predates canon `f2fee41`; re-sync + re-judge. Small, well-bounded.
3. **BC re-run** — after (1)+(2), re-run the BC measurement; closes the deferred partition.
4. **Production telemetry.db v2.17 apply** — Matt ADR-006 gate (still pending).
5. **Keystone-close push** — all 2026-06-13 commits are local; this is the natural push moment (Matt's explicit gate).

## DEFENSIVE-BRIDGE LINE — OPENED (distinct from the CLOSED keystone)

Hard boundary: **BC-measurement keystone = CLOSED** (pushed, complete on its own terms). **Defensive-bridge line = OPENED** — remediation of the Axis-4 silent-orphan the keystone characterized. Step 1 = orphan-lever inventory (one-off vs class sizing, BEFORE any fix specced).

**Step 1 — orphan-lever inventory (rocket, engine `343c21b`):** artifact `generation/notes/bc-orphan-lever-inventory-2026-06-13.md`. Audited every measurement-formula input the lock names across all 8 axes (`bc_target` → composition → allocation → sim telemetry), classified WIRED/ORPHAN-gen/MISSING-gen/GAP-sim/DEFERRED-lock + SILENT flag.
- **SILENT-by-axis: 0/0/0/0/0/0/5/0 — all 5 on Axis 4** (`HP`←`defensive_vitality_scale`, `shield_pool`, `regen_per_sec`, `mitigation_fraction`, `evasion_misses`, all ORPHAN-gen).
- **Self-check HELD:** Axis-4 eHP rows reproduced ORPHAN-gen/SILENT, none WIRED — `defensive_vitality_scale` greps to ZERO consumers in `src/`. Keystone diagnosis CONFIRMED, not refuted.
- **Structural root cause:** Axis-4 is the ONLY axis reaching the kit through a STAT objective (`DefensiveObjective`) vs mechanic/skill selection; the objective→stat allocator was never built. All 7 other axes are mechanic-selection (sim measures selected-skill metadata) → all WIRED.
- **Second orphan:** generation allocates NO evasion-chance (`evasion_high` = abstract budget string, no allocator) → dodger bin dead for an independent second reason (sim `a_evasion_misses` telemetry IS live; kits carry no evasion stat).

**Step 1 sizing — gandalf ruling (collab `0b19cec`):** `gandalf/notes/2026-06-13-bc-orphan-sizing-ruling.md`.
- **VERDICT RATIFIED: ONE-OFF (Axis-4 only)** → architecturally entailed (one missing component, one axis), not lucky. gamora-confirm on the 2 GAP-sim sim-seam rows does NOT gate the verdict (different seam/bug-class; separable parallel footnote).
- **Fix shape: CONTAINED defensive-bridge design-spec-as-math, NOT a general allocator-wiring pass.** Scope: build the single missing `DefensiveObjective`→stat allocator (eHP layers HP/shield/regen/mitigation AND evasion-chance) so Axis-4's live formula reads non-default; touches only the Axis-4 stat-objective seam.
- **Evasion: IN SCOPE as named sub-item** (same allocator; distinct acceptance criterion — eHP orphan flattens tank↔glass, evasion orphan makes dodger bin fully unreachable).
- **Hand-off guardrails for the eventual spec:** jack-ryan's two (validate MEASURED Axis-4→24/24/24/24 not a damage proxy; differentiate via allocation not HP-bloat) + gandalf's two new (dodger `avoidance_rate>=0.40` as INDEPENDENT acceptance gate; define defensive-objective↔element-prior composition explicitly — scale/override/add — or the next silent inconsistency is born there).

**Step 2 — design-spec-as-math (gandalf, collab `864a107`):** `gandalf/notes/2026-06-13-defensive-bridge-design-spec.md`. Two wires through one allocator (W1 eHP-gradient, W2 avoidance); centroids-not-edges (corrects latent knife-edge bug: tank target was 5.0 = the threshold, centroid ~7.0); ≥2 mechanisms per bin; SCALE on derived HP (preserves STAT_BUDGET=270 + element flavor), armor/shield/regen ADD; preferred_affix→real gear affixes. Four MEASURED acceptance gates §7.

**Step 3 — BUILD (rocket, engine `fc6e47e`; collab flag `90a906e`):** `generation/defensive_allocator.py` — `allocate_defensive(...)` + `allocate_from_objective(DefensiveObjective,...)`, the single missing `DefensiveObjective`→kit consumer. W1 `M = hp_scale × (1+shield_frac+regen_frac)/(1−mitigation)`; W2 `dodge = min(0.60, base+defensive_dodge(avoidance_target))` dex-independent. Consumer = additive guarded handler on `combatant.py::from_player_class` `alteration_fields` chain. **MEASURED Axis-4: `25/22/23/26`** (from orphan baseline `0/2/0/94`, inversion fixed). Calibration sweep fired AFTER first measured pass (Disc #18 honored): START seeds 22/19/26/29 → swept 25/22/23/26. Spec survived contact (no gandalf round-back).

**Step 4 — Gate-2 (jack-ryan, collab `19648fb`): PASS-WITH-INFO.** All four gates INDEPENDENTLY RE-RUN: G1 25/22/23/26 byte-deterministic ×2, ordering preserved; G2 mechanisms 4/5/3/0 no HP-bloat; G3 dodger 23/24 ≥0.40 checked separately; G4 fire tank vs glass 29060/2769 vs 8412/158, vitality=69 both, STAT_BUDGET=270 live, sum=270. Brownfield un-altered path byte-identical. The one combat_simulator test failure = pre-existing B11-balance (verified by parent-checkout), NOT this change.
- **Cross-seam combatant.py touch: CLEARS Gate-2 as-landed, NO gamora pre-concurrence needed** (10th additive handler on gamora's own `alteration_fields` seam; no signature change; MIGRATION dict contract `defensive_objective` documented per ADR-004). **→ ROUTE flag to gamora as INFO-for-awareness** (`rocket/notes/2026-06-13-defensive-bridge-combatant-touch-flag.md`); gamora keeps within-seam authority to re-site later without re-opening the gate. **[KR: captured here for gamora's next session — non-blocking.]**
- **INFO-1:** harness `--sweep` re-runs the same (now-default) seeds twice → can't reproduce the START→swept delta; calibrated end-state IS reproducible, only the delta is prose-attested. Low-priority fix: `_START_SEEDS` table.
- **INFO-2:** calibration fit to this 96-kit corpus (low caster base armor); generalization untested but gates have wide above-gate margins (tank median 8.76 vs 5.0; dodger 0.596 vs 0.40). Real-but-unverified overfit = INFO not BLOCK.

**DEFENSIVE-BRIDGE LINE: COMPLETE end-to-end** (inventory → sizing → spec → build → Gate-2 PASS). Axis-4 silent orphan REMEDIATED + measurement-verified. The deferred keystone Gate-1 partition (Windrunner/Phantom reachability, Berserker true reachability) can now re-run against a populated Axis-4 — that re-run is the natural next move, Matt's call.

## COVERAGE-AUDIT LINE — OPENED (second parallel line; does NOT touch Axis-4 bridge)

Question: does the lock's 8-axis MEASURED surface still COVER what generation now builds? (orphan-lever asked "are the 8 axes wired?"; this asks "do the 8 axes cover the current kit?"). Critical framing: lock's "deferred" stamps treated as STALE 2026-05-20 snapshot — every deferral RE-OPENED, not re-trusted. Query note `3cb8887`.

**rocket gen-side (engine `230366e`)** `generation/notes/bc-measurement-coverage-audit-2026-06-13.md` + **gamora sim-side (engine `547d54e`)** `simulation/math/bc-measurement-coverage-audit-sim-side-2026-06-13.md`.

**STRUCTURAL HEADLINE (gamora):** `bc_measurement.py` is the sim's ONLY measurement-to-bin pipeline and it computes bins for **Axis 4 + Axis 3B ONLY** — 2 of 8. No computed bin for Axis 1, 2A, 2B, 2, 3A, 5. The `bc_*` labels read by `phase7_cohort.py`/`wave5_season_orchestrator.py` are DECLARED TARGET labels, NOT measurements — MAP-Elites currently bins 6 of 8 axes on predicted/declared labels, measured on only 2. **OPEN QUESTION (for gandalf/lock): which of those 6 are legitimately composition-derived/structural (predicted=measured, fine) vs behavioral measurement-gaps?** Do NOT assert all 6 are bugs.

**Bucket A cross-join (built in gen? × sim computes bin?):**
| Item | Axis | built gen? | sim bin? | CLASS |
|---|---|---|---|---|
| Proxy density | 2A | PARTIAL (composer hardwired 0; but 6 PROXY T4 + kernel emit live proxies — 16 PROXY_FISSION kits in keystone) | N | **ORPHAN-measure (SILENT)** |
| Charge-stack | 5 | Y (wired into rep-gen script; emits PREDICTED axis5 bin only) | N | **ORPHAN-measure (SILENT)** |
| Mobility | 1 | Y (`movement_displacement_tiles` 3.0–6.0 populated) | N | **ORPHAN-measure (SILENT)** |
| Damage-taken-converts | 5 econ | N as econ bin (still deferred pool); Y as RETRIBUTION_ENGINE T4 | N | STILL-DEFERRED (econ) / Bucket-B (T4) |
| Dodger stealth/iframe/reflection | 4 | N (none silently built — both seams confirm) | N | STILL-DEFERRED (legit) |

**ORPHAN-measure count = 3 SILENT** (proxy 2A, charge-stack 5, mobility 1) — built features the archive can't see. Caveat: each is a true bug only if its axis is behavioral (needs measurement) vs structural (predicted OK) — ties to the open question above.

**2 carried GAP-sim rows RESOLVED:** both REAL sim-side gaps (Axis-1 mobility reduction = same as mobility orphan; Axis-5 resource-fraction read). Not "already measured."

**Bucket B — UNAXISED → needs gandalf ruling (5):**
1. COMPANION_CONTRACT / MONSTER_PACT (+ companion binding — one ruling covers both)
2. RETRIBUTION_ENGINE (damage-taken-converts as T4; vengeance pool 0.40 post-mit)
3. GEOMETRY_PROPAGATION (corpse-cascade / overkill-splash recursion — novel)
4. PERSISTENCE_ENGINE (uptime-ramp / saturation — tempo-adjacent + novel)
5. PHASE_MOMENTUM (stack-to-phase window — phase/untargetable-adjacent)
AXISED (no ruling): PROXY T4→2A (axis exists, measurement is the Bucket-A gap); ELEMENT/RESOURCE/COMBAT/DEFENSE T4 families.

**HEADLINE: N — the 8-axis archive does NOT measure the current kit surface.** Two gap classes: (a) MEASUREMENT gaps — 3 ORPHAN-measure + the structural 2-of-8-axes fact; (b) COVERAGE gaps — 5 UNAXISED post-lock T4/companion features. MAP-Elites consequence (the stakes): kits differing only along an unmeasured/uncovered dimension collide → one culled → build space silently homogenized.

**rocket self-correction surfaced:** orphan-lever note line 85 said `charge_stack_generation.py` "called nowhere" — TRUE lock-relative, now FALSE (called from 2026-06-13 rep-gen script). Re-opening the deferral caught what trusting the prior note would have missed. Validates the re-open-don't-retrust framing.

**FLEX POINT (slot 6):** the 5 UNAXISED rulings are gandalf design calls (belongs-in-BC → new axis/extension, or intentionally-outside → document+close). Per Matt's directive, rulings route to Matt — KR captured + reported, did NOT pre-decide whether companion/T4 belong in the archive, did NOT auto-fire gandalf. Also surfaced for Matt: the structural-vs-behavioral open question on the 6 unmeasured axes (gandalf/lock clarification).

## CERT-WAVE (2D combat-sim certification) — WAVE-0 COMPLETE + Gate-2 CLEARED

Distinct workstream opened this session: the 2D combat-sim **certification wave** (drift-proofing the recombination trap + certifying the spatial engine). gandalf+Matt closed the Pattern-B combat-sim-architecture dialogue; two CURRENT design specs landed (commits `2ff745f` + `9da7f59`):
- `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` (v1.1) — the golden oracle (RESOLVE §6.1 / MEASURE §6.2 certs; 6 reference kits; KPM bands §2).
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` (v1.1) — wave table W-A…W-F + §3 TODAY drift-proofing moves.

**Wave-phase map:** W-A (oracle authoring) DONE · W-B (type-wall + fidelity-stamp) DONE this session · W-C.5 (coverage-audit + arity) CLOSED (`cert-wave-2d-W-C5-close-2026-06-13.md`; arity=8 ratified, second audit finding bound into W-D) · W-C (spatial engine→first run) DE-RISKED GO · W-D (build six-axis measurement) / W-E (throughput) / W-F (1D deletion + bridge re-validate, terminal) NOT YET AUTHORED.

**WAVE-0 four dispatches — ALL COMPLETE, auto-committed, NOT pushed:**
| # | Agent | Tag / commit | Result |
|---|---|---|---|
| D1 | gamora | `gamora/v-wb-typewall-rename-1` · engine `a87ffea` | `CommitGradeVerdict`/`SearchGradeEstimate` frozen types + `require_commit_grade` guard at `GauntletArchive.insert_identity`; `fight_engine.py`→`search_estimator.py` + shim; paired admit/reject test; MIGRATION §v1.69 |
| D2 | star-lord | `star-lord/v-wb-typewall-export-1` · engine `a89f21a` | `fidelity:"search"` stamp on 1D `bc_measured_bins.json`; `ExportCommitGradeVerdictDocument` + `admit_bc_for_identity` (class-identity-first); round-trip on real `kse_20260613_002` (96 kits); MIGRATION §v1.76 |
| D3 | gandalf | collab `b692570` (doc-only) | 4 1D-measured artifacts stamped SEARCH-GRADE (not historical); no axis defs touched, no conclusions reopened, JSON field left to star-lord (no D2/D3 collision) |
| D4 | gamora | `gamora/v-wc-derisk-spike-1` · engine `275e7a3` | W-C de-risk spike: first oracle-checked spatial run (K2 @ open_arena KPM 42.9, shape-flip confirmed); module triage 5/6 KEEP (M6 REBUILD-CANDIDATE); **GO validate-then-extend** |

**jack-ryan Gate-2 (this autonomous tick) — ALL PASS, ZERO WARN, ZERO BLOCK.** WAVE-0 cleared phase-complete. Four INFO findings carried forward:
- **INFO-1 (record-accuracy):** D1 rename is not literal git-R100 (new file + 34-line shim); the real invariant (md5 byte-identity `8f8fa6915f3c49a99825698f37710c1a`) holds. No action.
- **INFO-2 (cosmetic):** `verdict_types.py:32` docstring cites §v1.68 vs §v1.69 elsewhere. No action.
- **INFO-3 (carry into W-D):** export `ExportCommitGradeVerdictDocument` markers are Pydantic plain defaults (not re-pinned by validator) — asymmetric with gamora's dataclass `__post_init__`. Load-bearing class-identity wall intact + tested; defense-in-depth only. Cheapest fix if W-D wants symmetry: `@model_validator` pinning markers.
- **INFO-4 (carry into W-C-full):** spike used a single "Balanced" cohort band; W-C-full RESOLVE must handle per-cohort band assignment when recalibrating.

**THE LOAD-BEARING SPIKE FINDING — KPM-instrument mismatch (jack-ryan independently confirmed REAL, not a masked bug):** all 36 spike cells read below band floor because the spatial engine kills an ≤8-mob pack (KPM ~44, numerator bounded by pack size) while `ENCOUNTER_COHORT_KPM_BAND` was derived from the 1D 1v1-duel kill-rate (floor 150–836). jack-ryan's refuting test: a masked bug yields flat output; the spike shows genre-correct differentiation (shape-flip K2/K3 by room, K6 tank lowest everywhere, mob-kill degrades correctly). To hit floor 150 with 8 kills needs a mechanically-impossible 3.2s clear → structural arithmetic, not under-killing. **Consequence: the W-C-full RESOLVE cert CANNOT pass until `ENCOUNTER_COHORT_KPM_BAND` is recalibrated to the spatial pack-clear instrument** (gandalf seam — the band is an oracle §2 commitment). This is "the single finding that most shapes the W-C-full dispatch KR authors next."

**DECISION IN FRONT OF MATT (asked, awaiting answer):** how to sequence the KPM-band recalibration —
1. **(KR lean) Recalibrate-then-dispatch:** a short gandalf dispatch recalibrates the band first, keeping the oracle as independent judge; then author W-C-full against the corrected band. Avoids the cert-defines-its-own-target anti-pattern (gamora moving the goalposts she's certified against).
2. **Fold-into-W-C-full:** author W-C-full now with band-recalibration as gamora's first in-phase task gated on gandalf sign-off.

**NEXT-PHASE DISPATCHES HELD until Matt's routing answer** (W-C-full → W-D → W-E → W-F). W-D scope is pre-bound by the W-C.5 close §3: build measurement for the ~4.5 behaviorally-realized axes (2A pri-1, 5 pri-2, mobility-half of 1, 3A, 2B), confirm-not-rebuild the 2 composition-determined ones (Geometry 2, range-half of 1). Reference-kit set stays at 6 (no 7th — nothing promoted). Carry INFO-3 into W-D, INFO-4 into W-C-full.

## Push posture

NOT pushed. All 2026-06-13 commits accumulate; Matt gates the keystone-close push. Production telemetry.db v2.17 apply also Matt-gated (ADR-006).
- Defensive-bridge line (post keystone-close push): engine `343c21b` (rocket inventory); collab `0b19cec` (gandalf sizing ruling). Plus gandalf query note `33d4fcf`.
- Coverage-audit line: engine `230366e` (rocket gen-side) + `547d54e` (gamora sim-side); collab query note `3cb8887` + handoff.
- Cycle 1–3 engine: `bd64ad9`, `ae247af`, `8810a8d`, `3422be2`, `ce433aa`, `51a69c5`, `3da0400`; collab: `a511222`, `f5a68d0`, `761fb60`.
- Cycle 4 engine: `22478c2`, `8e79119`, `def5ac3`, `0d88fb2` (collab), `3136fd7`, `60cce7a`, `8c41a8f`.
- Cycle 5 engine: `9660f7d`, `edec4c6`, `891b49d`, `02f84bd`; collab: `286e373`, `e879586`, `befa550`, `6640f56`.
