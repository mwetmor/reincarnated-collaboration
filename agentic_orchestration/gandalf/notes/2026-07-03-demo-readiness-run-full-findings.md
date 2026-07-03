# DEMO-READINESS UNATTENDED RUN — FULL FINDINGS RECORD (W0 → W4 + carve-out session)

> **Authored:** gandalf, 2026-07-03, at Matt's halt directive ("Doc 1: full, extremely long findings document of EXACTLY what happened with the entire run we just completed").
> **Companion:** `2026-07-03-next-session-recommendations.md` (Doc 2 — what to start with next session).
> **Character:** survey-mode record. This document reports **what IS** — every claim cites its source (state board, decision file, canonical JSON, bundle, commit). Where something is wrong or open, it is labeled as such; recommendations live in Doc 2, not here.
> **Sources of record:** `agentic_orchestration/demo-readiness-run-state-2026-07-03.md` (the live state board) · `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (decision file + gamora autopsy + jack-ryan review) · `reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (bundle-of-record) · `reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (canonical fight data) · git ledgers both repos.

---

## §1 Executive summary

**The DEMO-READINESS UNATTENDED RUN (spec v1.1, G1–G10 ratified) fired 2026-07-03 and CLOSED W0 → W4.** It produced the project's first curation-scale emitted content bank: **700 battle-sim-passed kits** (38.9% yield from 1,800 candidates, 3,047,800 fights, 6.0h wall, $0 sim spend), assembled into a 45MB bundle with 40 monsters, 4 factions, and a 2-floor manifest, registered and tagged (`star-lord/v-demo-run-w3-emission-batch1-2` @ engine `2839caf`). A follow-on carve-out session stamped identity glyphs + bridged the export envelope (element pip now live) and LLM-flavored a 35-kit roster-finalist fan ($0.13). **All G7a roster-pick inputs are complete for the 7 martial seats.**

**The headline absence — your question "we don't have any casters at all?" — is confirmed: correct, zero.** The 18-cell build-chassis catalog fielded STR 4 / DEX 4 / INT 5 / WIS 5. Survivors: **STR 4/4, DEX 3/4, INT 0/5, WIS 0/5.** Every one of the 700 emitted kits runs a martial resource economy (rage or combo); **no mana-economy kit exists in the bank.** The failure decomposes (autopsy + Gate-2 review, §8):

- **4 of 10 caster cells are STRUCTURAL at generation** — the composer emitted **zero candidates** for every non-melee INT cell. No fight ever ran. No fight-side lever touches these.
- **6 of 10 caster cells are CALIBRATION on the live gate** — they composed, fought, and **PASS the boss shells** (survive-kill 94–95% / 83–92%, tier-2 survival ≈ 1.000) but die on the **clear shells**: corridor/open timeout + pack throughput above the band ceiling.
- Plus 1 martial casualty: `melee_high_flat_dex`, pure calibration, closest cell to the floor (6.00 vs 9).

**Summoners remain the second absence:** criterion C (proxy-bin un-gate) was refuted as structurally unsatisfiable in W3 Phase A — the summon-skill composition path does not exist (three blockers, §9.1). Both certified melee summoners exist from W0 re-cert but are **curated, not emitted**, and their use is Matt-gated. **The Option-1-vs-Option-2 summoner ruling is OPEN** in `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` — you halted this session before ruling.

**Third absence:** zero cross-kit role variety — skill-role composition is invariant 4/4/2/2 (ST-dmg/AoE/control/support) across all 700; `role_orientation` is phantom (hard-coded "damage").

**One batch-2 re-fire is the candidate recovery vehicle for all three absences** — that is the frame the open ruling now sits in.

**Process record:** the run survived one halt-loud refutation (W3 Phase A — the discipline worked exactly as designed), two shipped defects in the emission driver (both root-caused and fixed), one wrong recovery claim (cost 1.5h of accidental re-simulation before being killed and replaced with a 4.2s canonical-JSON recovery), one Gate-2 tag-drift WARN (resolved by re-tag), and one BLOCKed autopsy plank (gamora's cohort-B mechanism, corrected by jack-ryan's review). Zero unresolved integrity issues ride into next session; all open items are decision- or hygiene-shaped (§14).

---

## §2 The run frame

- **Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** (Gate-1 passed + folded). Criteria A–G; G1–G10 rulings ratified; decisions-log batch registered at engine `a10a695`.
- **Fire order:** `agentic_orchestration/gandalf/notes/2026-07-03-kr-relay-demo-readiness-run.md`. Orchestrator: knight-rider.
- **Wave shape:** W0 prereqs → W1 pipeline completion → W2 pairing layer → **W3 THE EMISSION RUN** → W4 verify/curate-prep.
- **Authorizations in force:** commits auto-fire · push pattern established (both repos at each wave closeout) · LLM spend no-cap (spend logged per pass) · emission exercise Matt-authorized (spec §1-C).
- **Failure policy:** spec §7 halt-loud; W2 degrade path; W3 pilot beat unconditional.
- **Failure-policy invocations across the run:** exactly **one** — the W3 Phase A refutation (§5.1). W0/W1/W2 closed with zero invocations.

---

## §3 Preconditions + W0 + W1 — exactly what closed

### Preconditions (all ✓ before W2)

1. **Decisions-log batch registration** (G1–G10 + proxy-T4 four + Q6/Q7 six) — engine `a10a695`.
2. **Registry schema mini-pass** — jack-ryan **RATIFIED-WITH-AMENDMENTS** (G9, no Matt gate): draft schema **+ `generation_seed INTEGER`** (without it the run is described, not reproducible) **+ `in_band_count INTEGER`** (G2 measured output, queryable). Launch exclusions affirmed (no cost_usd/git_sha/FKs).
3. **Singleton-config smoke green** — rocket, **28/28** (`generation/notes/w0_prereqs_smoke_2026_07_03.py`); KR re-ran live per Discipline #11.

### W0 — three parallel prereq legs

- **rocket** ✓ `rocket/v-demo-run-w0-1` @ engine `e57b9d8` — all six deliverables PASS (knob · 2-type-decl check · fixture · classifier · F-f consumer · singleton smoke). No refutation fired. Generation-internal, no MIGRATION owed. *(Post-hoc caveat: deliverable #2's "PASS" was later AMENDED by jack-ryan during the W3 adjudication — it validated the fixture/classifier layer, not the composer→kit production path; the summoner gap existed at W0 and was masked. Bounded — the other five PASSes are self-contained. §11.4.)*
- **star-lord** ✓ `star-lord/v-demo-run-w1-1` @ engine `cbd47b5` — export DDA-lock widened + W1 pipeline completion (D.1 #1/#2/#3/#4/#5/#8a + G6 stub supersession): MIGRATION v1.85; **202/202 tests**; six-type round-trip PASS with non-NULL counts; **per-item flavor resumability VERIFIED** (spec §11 Q1-iii — this is the property that later made the 35-kit shortlist-first flavor pass safe); **60 legacy stubs marked `_non_canonical`** (G6).
- **gamora** ✓ `gamora/v-demo-run-w0-dda-sweep-1` @ engine `87c47a6` — DDA propagation sweep: **propagation-live build-floor CERTIFIED at factor ×0.6** (conservative); anchors held by construction; **both demo summoners RE-CERTIFIED WR 1.0 both shells, 136s margin**; degeneracy CLEAN; Discipline #24 isolation verified; (b)-config NOT invoked — **the run proceeded propagation-ON**.

### W1 residual

- **#8b registry writer** — KR sequencing call: folded into W3 as step 0 (post-ratification; satisfies Gate-1 #5 ratify-before-build). See §5.3.

---

## §4 W2 — pairing layer (CONVERGENCE + DUAL_PROXY)

- **Gate-1 critique pair on the dispatch text:** jack-ryan ENDORSE-WITH-FOLDS (E4 fold applied) + gandalf ENDORSE ×5 NOTE → CLEARED.
- **Phase 1, rocket** ✓ `rocket/v-demo-run-w2-pairing-1` @ engine `6a7190b`: CONVERGENCE + DUAL_PROXY strategy classes live; matrix/pools **DERIVED byte-match 15/65/14×3, import-asserted** (spec drift breaks import); E0–E5 test-pinned (26 tests); **η non-vacuous** — fixture draws CONVERGENCE **0.679**, 1-type draws DUAL **0.615**, E1 refused, solo None; round-trip smoke 6/6 GREEN with rule-v/vi labels at the bundle boundary + negative-mutation proof; generation MIGRATION entry before tag.
- **Phase 2, gamora** ✓ `gamora/v-demo-run-w2-pairing-cert-1` @ engine `1ec8265`: **both members MAGNITUDE-CERTIFIED at the propagation-live 0.6 floor** — CONVERGENCE WR 1.0 both shells, t 62.6s (merge pays the ratified 0.8 tax and still clears the 300 singleton floor); DUAL WR 1.0 both cases, AQ4 in-band; fixture cert PASS, never-ships fence intact.
- **E4 disposition (the honest carve):** PRICED first, then DEFERRED with a named prerequisite — the **ECHO player-skill-replay ally-attack channel is absent from `_spawn_one_ally`**; certifying Mirror pairs against a hollow merge would be a vacuous pass. **2 pairs excluded BY NAME** (`{autonomous_caster, delayed_position_shadow}`, `{passive_fighter, delayed_position_shadow}`) → **63/65 valid pairs certified**. W3 may emit Mirror-shaped kits — they merge STRIKER-only until the channel lands. Not a W3 blocker; it rode the closeout report as a named prerequisite.
- Seeds consumed to 54M+; next-free 55M+. Failure-policy invocations: ZERO. W3 fired with FULL pairing η live.

---

## §5 W3 — THE EMISSION RUN (the run's center of gravity)

### §5.1 Phase A halt-loud: the summoner refutation (first and only §7 invocation)

Rocket's un-gate attempt **refuted the spec's premise**: criterion C ("lift `_DEFERRED_PROXY_BINS` + `ProxySpawn`; emission fires with proxy bins live") is **structurally unsatisfiable** — the generation-side summon-skill composition path does not exist:

1. **Phase 4d of `bc_target_composer.py` (`:756-757`) is a no-op stub** assuming `proxy_bin=="solo"` — verified verbatim by jack-ryan.
2. **The `multi-spawn` geometry maps to `multi_projectile`/`chain`/`fork`** (`:380-384`) — projectile multiplicity, no summon taxonomy.
3. **`PoolMechanic` carries no summon discriminator**; `build_proxies_surface` (`proxy_vocabulary_bridge.py:298-299`) documents "every exported kit gets `[]`."

Additionally: `ProxySpawn` at `mechanic_alteration.py:46` is a **docstring reference to the register Matt retired 2026-07-02** — there was nothing to lift; and the spec's "2026-06-24 ratification" reference has no provenance in the engine tree (spec v1.2 hygiene item). Lifting the gate would have composed proxy-heavy targets with **zero summon skills** → hollow kits faking criteria B/C. **Rocket performed no lift, no tag — halt-loud per §7.** Finding: `w3-ungate-refutation-fired-2026-07-03.md` @ engine `0a1706c`, collab `cc24556`. Both critics later affirmed the halt as correct and disciplined.

### §5.2 Adjudication (critique pair, parallel read-only) + KR disposition

- **jack-ryan:** structural claim **[AFFIRM]** — all 3 blockers line-verified; W0 deliverable-#2 "PASS" **[AMEND]** (masked gap, §3); Option 3 rejected; C/G4 amendments Matt-gated [AFFIRM].
- **gandalf:** refutation **[ENDORSE]**; **[CONTEST]** on jack-ryan's One-Realm §5.2 "hand-authored acceptable" citation — that language is **struck through by your 2026-07-02 ruling** ("they need to be balanced and pipeline emitted… we can pick from a seasonal emission… of battle-sim passed kits"); Option 2 is therefore a knowing reversal, not a covered case. G4's ~25% is **two promises wearing one number** (player-experienced curated-roster share vs engine-capability emitted share). Option 3 rejected hard. Lean: fire solo batch-1 now + Option 1 as follow-on.
- **KR run-disposition ruling:** W3 proceeds as **solo full-spectrum BATCH 1** under spec §4's batch mechanism; **criterion C PARKED loudly, NOT amended** (amendment is Matt-gated per both critics); summoner emission = batch 2, gated on your ruling. The decision file was opened for you at that point; nothing in the run pre-committed the ruling.

### §5.3 Step-0 registry writer (#8b — ruling-independent under all options)

✓ `star-lord/v-demo-run-w3-step0-registry-1` @ engine `dc00b2a` — `emission_runs` table, 17 cols + the 2 ratified amendments; idempotent create; **HALTED/PARTIAL run-state expressible** (the refutation-shaped gap closed); **48/48 tests**, zero regressions (4,822 vs 4,774 baseline); MIGRATION v1.86.

### §5.4 BATCH 1 — the emission itself, the defect chain, the recovery (exact sequence)

1. **Driver + pilot beat** @ engine `ea753a3` — pilot PASS at **10.65s/kit**, in-band rate **64%** (the number that later exposed DEFECT 1).
2. **Full-spectrum solo run** — an ops finding first: **sub-agent-spawned long processes die with the sub-agent session**; KR's detached relaunch (`nohup`, PID 65847, seed 55000000) is the run that completed (Discipline #3 clean). Mid-run state @ engine `0fd813e`.
3. **Terminal state of the defective run** (registry `86fa640c`): **1,800 candidates · 3,047,800 fights · 6.0h wall (21,589.7s; 11.99s/kit vs pilot 10.65) · $0 spend · round-trip PASS · criterion C PARKED** — but **in_band = 7 (0.4%)** vs pilot 64%: a **160× anomaly**. Gauntlet exited clean; Discipline #11 verification caught two defects.
4. **DEFECT 1 (survivor collection):** all 7 reported survivors were sample **`_s99`** — statistically impossible by chance. Root cause: `config_to_kit` **cell-level-key overwrite** — per-cell last-sample-only pass-evaluation; the true relation was 7 reported = true 700 ÷ 100. Bundle NOT registrable as final.
5. **DEFECT 2 (registry path):** the step-0 DB landed at **`~/Games/data/emission_registry.db` — outside the engine repo**; all 48 registry tests missed it (tmp-path blind spot).
6. **Diagnosis** @ engine `49424e7` (MIGRATION v1.88) — root-caused both defects correctly, **but its "no re-fight required" claim was WRONG AS SHIPPED** — no such code path existed. KR's fixed-driver relaunch **re-fought for 1.5h** before KR killed it (your uptime constraint) and ordered the real thing:
7. **`--recover-from-canonical`** — regenerate the 1,800 candidates deterministically + read `season_emit` from the defective run's canonical JSON (93MB, 3 consistency asserts): **4.2 seconds vs 21,585 seconds.** The fights were always sound; only the survivor mapping was broken.
8. **TRUE BUNDLE LANDED** @ engine `1112cf0` (MIGRATION v1.89), tag `star-lord/v-demo-run-w3-emission-batch1-1`: **700 kits @ 38.9% yield, 7 passing cells × 100**, registry run `f0bd67e5` with `in_band=700`. Defective run `86fa640c` retained as DEFECT-DISCOVERED for audit.
9. **Flavor PARKED (resumable per §7):** name/flavor_text/title_completion None on all 700 (dry-run); the flavor-scope question (all 700 vs shortlist-first) rode the closeout to you.
10. **Hygiene leg:** 8 smoke rows polluting the production registry (kit_count=5, diagnosis-session artifacts) → marked SMOKE-ARTIFACT + guard test; `bc_target_cell=None` on bundle kits → **fixed** @ engine `2839caf` (MIGRATION v1.90).

---

## §6 W4 — verify + curate-prep (four legs, all closed)

- **gandalf DRIFT-CRITIC** (six-type verify) — **PASS**: 5 content types live + flavor honestly parked; **700/700 weapons non-null**; NO architectural drift; curation-viable via BC-cell primary axis. Caveats registered: geometry is **cell-locked** (within a cell, kits are skin-not-shape); the 7 cells are a **diagonal slice** of the catalog; §8's "≥1 CONVERGENCE row" → DEFER to batch 2, don't drop. Verdict @ collab `136881c`.
- **jack-ryan Gate-2** — W0 DDA sweep **PASS (exemplary; #24 isolation proven structurally)** · step-0 registry **PASS** · W3 emission **PASS-WITH-FINDINGS**; **WARN: tag-drift** (`1112cf0` didn't cover the rewritten bundle) → **RESOLVED: re-tag `star-lord/v-demo-run-w3-emission-batch1-2` @ `2839caf`** (the bundle-of-record tag). Noted: TestSmokeGuard closes a *different* blind spot than the tmp-path one (that is test 49). Criterion B not met on flavor — correctly parked. Findings @ collab `8afcab7`.
- **gamora G4 hypothesis test** @ `gamora/v-demo-run-w4-g4-1` @ engine `f3c5aec` — **emitted proxy-dominant share = 0.000 [0, 0.004 CI] — STRUCTURAL** (solo batch-1), recorded per #18.1 without rationalizing; **knob-layer share 0.250000 EXACT** vs 0.25 target (live-sampler measured, monotone-proven); offer-table PASS config-correct (solo-invariance non-vacuous 0/700; the positive clause is a named batch-2 deliverable); sidecar `w4_g4_proxy_dominant_tags.json`; math note first (Discipline #1).
- **KR §8 shortlist prep** — `agentic_orchestration/w3-batch1-curation-shortlist-prep-2026-07-03.md`: **7 non-summoner seats READY** (one per surviving cell); element skew measured (82% mono-physical/mono-fire → prefer the mixed-pair tail); **2–3 summoner seats MATT-GATED**; final picks gated on flavor-scope + summoner rulings.
- **B-series reconciliation:** B3 SUPERSEDED (G6 stubs) · B4 ABSORBED into this run (necro-energy prereq no-op per G4; DDA-lock → W0; F-f consumer → W0; un-gate + run → W3) · B5 ABSORBED into W4 (§8 rubric; picks = G7a).

---

## §7 WHAT EMITTED — the 700-kit bank, exactly

### §7.1 Bundle-of-record anatomy

`reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (45MB) @ tag **`star-lord/v-demo-run-w3-emission-batch1-2`** (engine `2839caf`). Registry lineage: `86fa640c` (defective run, retained DEFECT-DISCOVERED) → `f0bd67e5` (true-bundle registration, in_band=700) → `cbeb9471` (bundle-of-record @ re-tag) → **`2d32195d`** (current, post-F1-bridge regen — §10.2).

Top-level: `bundle_version · generated_at · engine_version · season_id · schema_status · schema_note · proxy_scaling · stage2_run_record · kits (700) · monsters (40) · gear_pool · factions (4) · floor_manifest (2) · _assembly_notes`.

### §7.2 Population structure (verified against the bundle this session)

| Surviving cell | Count | Glyph | Resource | Elemental base |
|---|---|---|---|---|
| `melee_high_flat_str` | 100 | BRUISER | rage | physical (8/12 skills), mixed tail |
| `melee_low_spiky_str` | 100 | BRUISER | rage | physical, mixed tail |
| `melee_medium_variable_str` | 100 | BRUISER | rage | physical, mixed tail |
| `mid_high_flat_dex` | 100 | GLASS CANNON | **rage** | fire (8/12), mixed tail |
| `ranged_high_flat_dex` | 100 | GLASS CANNON | combo | fire, mixed tail |
| `ranged_low_spiky_dex` | 100 | GLASS CANNON | combo | fire, mixed tail |
| `ranged_low_spiky_str` | 100 | GLASS CANNON | combo | physical, mixed tail |

- **Every kit has exactly 12 skills** (verified: skill-count spread across 700 = {12: 700}).
- **Glyph spread:** BRUISER 300 · GLASS CANNON 400. **Resource spread:** rage 400 · combo 300.
- **Resource model is RANGE-determined, not attribute-determined** (verified per-cell across all 700 this session): melee×3 + mid×1 → rage; ranged×3 → combo. *(This corrects a claim I made in-session that energy was attribute-mapped — my model was wrong; the bundle and star-lord's flavor were right. §10.4.)*
- **Skill-role composition is invariant: 4/4/2/2** (ST-dmg / AoE / control / support) on every kit — no role-varied kits exist (§9.5).
- **Geometry is cell-locked:** within a cell, all 100 kits share one spatial geometry — differentiation is element + tempo/amplitude texture ("skin, not shape").

### §7.3 Anatomy of one emitted kit (verbatim from the bundle)

**`S1_endgame_bc_melee_low_spiky_str_none_s39` — "Void Marrow Breaker"** (BRUISER · physical+shadow · rage · archetype_tag "melee / low-tempo / spiky-amplitude / STR / no-proxy"):

- **Chain A (Physical), T1→T4:** `primary_attack`, range 3.0m — the bread-and-butter damage chain.
- **Chain B (Shadow), T1→T4:** `secondary_attack`, range 3.0m — the mixed-element secondary.
- **Chain C (Physical), T1–T2:** `control`, range 8.0m; **T3–T4:** `support`, range 0.0m (self).
- `proxies: []` (like all 700 — §9.1).
- Flavor (LLM, this session): *"Rage pools slow and deliberate — each blow a shadow-laced concussion that waits for bone to answer. One opening. One burst…"*

This 3-chain × 4-tier shape, with the 4/4/2/2 role split and cell-locked ranges, is the shape of **all 700** — what varies across a cell is element mix, tempo, amplitude; what varies across cells is geometry, attribute, resource.

### §7.4 The 35 flavored roster finalists (complete)

Selection: KR, deterministic (kit ids sorted, palette-greedy; reproducible from the bundle — not a hand-pick), per my axes (PRIMARY cell / SECONDARY element, mixed preferred / TERTIARY flavor). 5 per seat = 4 mixed-element + 1 mono anchor. Secondary spread across the fan: fire×3 · lightning×5 · water×4 · wind×4 · shadow×4 · earth×4 · holy×4. All 35 carry LLM name/flavor_text/title_completion as of this session (star-lord Beat B, $0.1289, engine `4786868`, tag `star-lord/v-demo-run-flavor-shortlist-1`).

**Seat 1 — melee_high_flat_str (BRUISER):** Cinder Ravager (phys+fire, s28) · Voltbreaker Ascendant (phys+lightning, s10) · Tidecrusher Incarnate (phys+water, s15) · Galeforce Ravager (phys+wind, s18) · Ironblood Rampart (mono anchor, s1)
**Seat 2 — melee_low_spiky_str (BRUISER):** Void Marrow Breaker (phys+shadow, s39) · Quarry Bone Crusher (phys+earth, s59) · Hallowed Bone Smasher (phys+holy, s19) · Ember Marrow Breaker (phys+fire, s23) · Rage Marrow Splitter (mono anchor, s0)
**Seat 3 — melee_medium_variable_str (BRUISER):** Shockwave Ironbreaker (phys+lightning, s47) · Shadowmass Ravager (phys+shadow, s30) · Pressurewall Breaker (phys+water, s21) · Galesworn Bonecrusher (phys+wind, s7) · Ironwrath Sunderborn (mono anchor, s0)
**Seat 4 — mid_high_flat_dex (GLASS CANNON, the only mid-range cell):** Cinderstone Fusillade (fire+earth, s39) · Sacrefire Fusillade (fire+holy, s90) · Scorchbolt Fusillade (fire+lightning, s21) · Ashveil Fusillade (fire+shadow, s3) · Pyrewrath Fusillade (mono anchor, s10)
**Seat 5 — ranged_high_flat_dex (GLASS CANNON):** Scorchtide Fusillade (fire+water, s49) · Emberstorm Fusillade (fire+wind, s1) · Magma Salvo Incarnate (fire+earth, s9) · Sanctum Ember Fusillade (fire+holy, s51) · Pyroclast Relentless (mono anchor, s0)
**Seat 6 — ranged_low_spiky_dex (GLASS CANNON):** Galvanic Pyre Fusillade (fire+lightning, s28) · Scalding Tide Fusillade (fire+water, s57) · Sirocco Detonator (fire+wind, s83) · Emberstrike Detonator (fire+earth, s17) · Conflagrant Salvo (mono anchor, s0)
**Seat 7 — ranged_low_spiky_str (GLASS CANNON, the odd physical-ranged chassis — flavored as martial skirmisher, no caster-fantasy):** Ignition Thrower Ascendant (phys+fire, s42) · Umbral Salvo Ascendant (phys+shadow, s25) · Radiant Spear Sunder (phys+holy, s30) · Stormjavelin Detonator (phys+lightning, s27) · Ironhurl Detonator (mono anchor, s0)

Flavor discipline held (verified): rage/combo economies written correctly per kit; GLASS CANNON flavored to the **ranged spike, not fragility** (fragility is F1-unverifiable — §9.7); no mechanic promised that a kit doesn't carry (Discipline #11).

### §7.5 The other 665

Name/flavor_text/title_completion = **None** on all 665 non-finalist kits — the parked-resumable state per your SHORTLIST-FIRST ruling. Per-item resumability was verified in W1, so any future widening (e.g., flavoring a second-choice seat candidate) is incremental, not a re-run.

---

## §8 WHAT DID NOT EMIT — the 11 failed cells, exactly

### §8.1 The gate that decides emission (jack-ryan-verified, the corrected read)

A kit emits iff `per_cohort[Balanced|Hybrid].eligible_encounters_passed >= 9` across the 6 eligible shells, where per `gauntlet_sim.py:615-667`: **CLEAR shells** pass iff `tier_2_kpm` ∈ `ENCOUNTER_COHORT_KPM_BAND[shell][cohort]`; **BOSS shells** (`boss_with_adds`, `mini_boss`) pass iff `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT` — verbatim `:624-625`: *"The KPM band is NEVER consulted for boss shells."* (The tier_1 boss-KPM path was retired 2026-06-19.) The separation is sharp: **survivors clear 11.0–18.0 eligible; every composed failure clears 3.65–6.0** — nothing sits near the floor ambiguously.

**Phantom-axis warning that rode this analysis:** `in_band` (False ×125,400), `sg_overall` (BLOCK ×125,400), and encounter-level `gauntlet_pass` are population-wide constants — survivors included. They discriminate nothing. Two independent analysts (KR's dispatch lead, gamora's first mechanism draft) were each pulled toward a non-live field; both were corrected by cross-check (§11.9).

### §8.2 The 11-cell classification (gamora's autopsy + jack-ryan's corrections; ZERO fights simulated)

| # | Cell | Attr | Mode (final) | Evidence |
|---|---|---|---|---|
| 1 | `mid_low_spiky_int_none` | INT | **STRUCTURAL** | kit_results rows = **0**; `legendary_id` absent from both tables — composer emitted zero candidates |
| 2 | `ranged_low_spiky_int_none` | INT | **STRUCTURAL** | 0 rows; zero candidates |
| 3 | `ranged_medium_variable_int_none` | INT | **STRUCTURAL** | 0 rows; zero candidates |
| 4 | `ranged_medium_variable_int_light` | INT | **STRUCTURAL** | 0 rows; zero candidates — the one proxy-`light` INT cell composed exactly as many as its `_none` siblings: none |
| 5 | `melee_high_flat_int_none` | INT | **CALIBRATION** (clear-shell) | composed (100 kit rows, all season_emit=False); Balanced eligible-passed 3.6/9; **boss survive-kill PASSED** on the live gate |
| 6 | `melee_high_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | 3.6/9; boss passed; packs above ceiling |
| 7 | `melee_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | 3.8/9; same mechanism |
| 8 | `mid_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | 3.9/9; the "REJECT=0" lead was a home-shell projection artifact — cross-shell it REJECTs 6,014 |
| 9 | `ranged_low_spiky_wis_none` | WIS | **CALIBRATION** (clear-shell) | 3.8/9; same mechanism |
| 10 | `ranged_medium_variable_wis_none` | WIS | **CALIBRATION** (clear-shell) | 3.7/9; same mechanism |
| 11 | `melee_high_flat_dex_none` | DEX | **CALIBRATION (pure)** | composed; **6.00/9 — closest cell to the floor**; passes `boss_with_adds` (100%) but fails `mini_boss` (0%) + corridor/open — amplitude tuned too hot for two shells |

### §8.3 The three mechanisms (trimodal, corrected)

- **(A) Generation gap — STRUCTURAL, 4 cells (#1–4):** the composer emitted **zero candidates for every non-melee INT cell**. No fight ever ran under their legendary_ids. Not fixable by any number; a proxy-live batch-2 **cannot fight what was never composed**. Root cause not yet diagnosed (open item — the recommended read-only rocket diagnostic, Doc 2). The apparent KR-vs-gamora evidence conflict here resolved cleanly: `encounter_id` carries the ENVIRONMENT cell (those 4 stems have 6,600 encounter rows each, REJECT 6,300/5,100/5,100 — kits from OTHER cells fighting inside those shells); `legendary_id` carries the kit's HOME cell (0 rows). Both readings internally correct; different axes.
- **(B) Clear-shell calibration — 6 composed caster cells (#5–10):** on the live gate these kits **PASS the boss shells** — `boss_with_adds` survive-kill 94–95%, `mini_boss` 83–92%, `tier_2_survival_rate` median **1.000**. **The boss is not their blocker.** They fail the CLEAR shells two ways: `chokepoint_corridor` + `open_arena` **timeout** (tier_2_kpm=0, survival 0); `elite_pack` + `magic_pack` **overkill above the band CEILING** (bands (8.26, 28.13) / (18.61, 100.0); caster tier_2_kpm reads 450/600 — and the "600" is a documented **tick-floor discretization artifact**, `t4_sim_cycling.py:720-723`, not a real KPM). Net: burst-AoE profile too hot for packs, too slow to clear corridors — a band/geometry mismatch, **not** a mana-economy collapse. *(gamora's original "single-target-sustain collapse / a band re-tune can't fix" secondary was read off the retired tier_1 boss-KPM field and was BLOCKed by jack-ryan's review; the corrected mechanism above is the ruling input. gamora owes 4 doc-only corrections — Doc 2 housekeeping.)*
- **(C) Corridor overkill — 1 martial cell (#11):** `melee_high_flat_dex` is the cleanest pure-calibration case and the nearest miss (6.00/9).

### §8.4 What a failed kit looks like (verbatim from the canonical JSON)

**`endgame_bc_ranged_low_spiky_wis_none_t4_chain_1`** — season_emit **False**. Eligible-passed per cohort: DPS-min-maxer **2/15** · Balanced **4/18** · Defensive **2/6** · Hybrid **4/18**. Against floor 9: not close. Survivor contrast: `endgame_bc_melee_high_flat_str_none_t4_chain_2` — Balanced **18/18**.

And the structural class has no sample to show: for `mid_low_spiky_int`, `ranged_low_spiky_int`, `ranged_medium_variable_int_none`, `ranged_medium_variable_int_light` there is **no kit row at all** — the absence IS the finding.

### §8.5 Autopsy side-findings

- **Defensive cohort can never pass** — its `eligible_encounters_total` is fixed at 6, below floor 9; **1,000/1,000 emit-kits** have Defensive `gauntlet_pass=False` yet emitted anyway. Orthogonal to the caster read (proven), but it's a fixture artifact worth a fix-or-document (Doc 2 housekeeping).
- **Proxy density did not move caster composition:** `int_light` composed exactly as many candidates as `int_none` — zero. The generation gap is **upstream of proxy density**. (This is the closest on-disk signal bearing on Option 1's shape; whether a heavier proxy tier changes anything is not answerable without new generation + fights.)
- **Method integrity:** ZERO fights simulated (jack-ryan verified gamora's script contains only json.load + reads); the canonical JSON is cohort/T4-keyed (2,200 kit_results rows, 125,400 encounter_results rows) — deliberately NOT 1:1 with the 1,800 driver-layer candidates.

---

## §9 MECHANICS THAT DIDN'T WORK — the consolidated catalog

1. **Summon/proxy composition (criterion C)** — does not exist. Three blockers (§5.1); `proxies: []` on all 700; G4 emitted proxy-dominant share **0.000 [0, 0.004 CI], structural**. The knob layer itself is healthy (0.250000 EXACT vs 0.25 target) — the intent dial works; the composition path it feeds does not exist.
2. **Non-melee INT composition** — 4 cells, zero candidates, root cause undiagnosed (§8.3-A). Distinct from the summon gap; this is upstream of proxy density.
3. **Caster clear-shell viability** — 6 composed INT/WIS cells fail corridors/open (timeout) + packs (over-ceiling) while passing bosses (§8.3-B). Calibration/geometry-shaped.
4. **`melee_high_flat_dex`** — pure calibration, amplitude over the corridor/open ceiling; nearest miss at 6.00/9.
5. **Cross-kit role variety** — none. 4/4/2/2 invariant ×700; no controller- or warden-leaning kits; `role_orientation` **phantom** (hard-coded `"damage"`, `season_generation_pipeline.py:1557` — correctly NOT bridged into the envelope).
6. **ECHO/Mirror ally-attack channel** — absent from `_spawn_one_ally`; 2 Mirror pairs excluded from W2 cert BY NAME (63/65); Mirror-shaped kits merge STRIKER-only until it lands.
7. **GLASS CANNON "glass" texture** — unverifiable in F1 data: `damage_multiplier` uniform ~1.01 across glyphs; `stat_distribution` F1-None. Flavor deliberately written to the ranged spike, not fragility, until a stat pass backs it.
8. **11 cycle13-legacy envelope fields** — no live W5R source; left None-honest rather than fake-bridged (F1 findings; the six live fields WERE bridged — §10.2).
9. **Defensive cohort as a gauntlet participant** — structurally unable to pass (§8.5); fixture artifact.
10. **Registry tmp-path + smoke-row hygiene** — two test blind spots found and closed (§11.2, §11.6).

---

## §10 The carve-out session (this session, post-run) — exactly what fired

Three ruling-independent carve-outs staged by KR @ collab `b9b8b31`, all fired on your "fire them both here" + key hand-off:

### §10.1 Failed-cell autopsy (gamora) + Gate-2 review (jack-ryan)

- gamora: 11-cell classification, ZERO fights, appended to the decision file @ collab `fca8d78` (engine-side script/notes @ `3417d19`). Verdict as authored: "predominantly structural."
- jack-ryan DEV-MODE review @ collab `1bb1950`: **PASS-with-notes; ONE load-bearing plank BLOCKed** — the cohort-(B) mechanism was read off the retired tier_1 field; on the live tier_2 gate the casters pass bosses and fail clear shells. **Corrected ruling input: the caster absence is HALF STRUCTURAL (4 zero-composed cells) and HALF CALIBRATION (6 clear-shell cells) — not "majority-structural + ST-sustain economy gap."** Six other planks CONFIRMED (incl. floor-9 separation, phantom-axis catch, Defensive orthogonality, int_light==int_none, zero-fights honesty). 4 doc-only corrections owed by gamora; per jack-ryan: if you rule before those land, **use the corrected decomposition in his block**.

### §10.2 F1 envelope bridge + identity_glyph stamp (star-lord Beat A)

@ engine `62abdc7`, tag `star-lord/v-demo-run-f1-glyph-1` (registry regen → `2d32195d`): the driver↔assembler vocabulary mismatch closed — **six fields bridged of the 19 hollow**: `dominant_element` (element pip LIVE — physical 400 / fire 300), `energy_type` (rage 400 / combo 300 — the envelope now *shows* the martial-only fact), `archetype_tag`, `range_profile`, `engine_version`, + NEW **`identity_glyph` (BRUISER 300 / GLASS CANNON 400)**; `role_orientation` explicitly None (phantom, never bridged); remaining 11 fields = cycle13-legacy with no live W5R source (per-field triage in engine `export/MIGRATION.md` §v2.00); round-trip smoke 5/5 asserts PASS.

### §10.3 Flavor Beat B (star-lord, after your key hand-off)

First attempt halted honestly at 0/35 (no key in env) → `matt_to_do` filed → you provided the key in-session → fresh star-lord agent completed **35/35** (name/flavor_text/title_completion), **$0.1289**, @ engine `4786868`, tag `star-lord/v-demo-run-flavor-shortlist-1`. **Key hygiene verified: zero occurrences of the Anthropic key prefix in either git tree (grep-verified pre-commit); key passed env-prefix-only, never persisted.** *(The key transited chat this session — rotation recommended; Doc 2 housekeeping.)*

### §10.4 A self-correction on the record (mine)

I claimed in-session that resource was attribute-mapped (rage=STR / combo=DEX) and flagged two flavor texts as economy flips. My own 35-kit verification scan returned **0/35 flips**; the per-cell check across all 700 showed the truth: **resource_model is range-determined** (melee/mid → rage; ranged → combo). star-lord's flavor was attribution-faithful; my model was wrong. Corrected openly at the time; recorded here so the wrong version doesn't propagate.

### §10.5 Session close

Both repos + tags pushed on your instruction. The summoner ruling session was opened (options + my Option-1 recommendation presented); **you halted before ruling** — the ruling is the open head of next session (Doc 2 §1).

---

## §11 Defects + process-findings ledger (what bit us, what we learned)

1. **DEFECT 1 — `config_to_kit` cell-level-key overwrite** (all survivors `_s99`; in_band 7 = 0.4% vs pilot 64%, a 160× anomaly). Caught by Discipline-#11 verification, root-caused @ `49424e7`, fixed. *Lesson: the pilot's in-band rate is a load-bearing invariant — the anomaly WAS the alarm.*
2. **DEFECT 2 — registry path escape** to `~/Games/data/emission_registry.db`; 48/48 tests green while writing outside the repo (tmp-path blind spot). Fixed; blind-spot test added (test 49).
3. **"No re-fight required" — WRONG AS SHIPPED.** The diagnosis asserted a recovery path that didn't exist in code; the relaunch re-fought 1.5h before being killed. The real recovery (`--recover-from-canonical`) took **4.2s**. *Lesson (now in the autopsy dispatch as binding language): a recovery claim must name an existing code path, or halt-loud.*
4. **W0 deliverable-#2 masked gap [AMEND]** — a "PASS" that validated the fixture/classifier layer while the composer path it was written to guard didn't exist. *Lesson: a check must exercise the production path, not a look-alike layer.*
5. **Tag-drift WARN** — `batch1-1` tag didn't cover the rewritten bundle; resolved by `batch1-2` @ `2839caf`. *Lesson: re-tag after any post-tag artifact rewrite.*
6. **Registry smoke-row pollution** — 8 diagnosis-session rows in production registry; marked SMOKE-ARTIFACT + guard test.
7. **Sub-agent-spawned long processes die with the session** — the 6h gauntlet only completed via KR's detached `nohup` relaunch (PID 65847). *Now standing ops practice for long runs.*
8. **Home-shell projection artifact** — `mid_medium_variable_wis` "REJECT=0" was true only inside its home shell; cross-shell it REJECTs 6,014. *Lesson: check which axis a headline number is projected on.*
9. **Phantom-axis discipline paid twice** — `in_band`/`sg_overall`/`gauntlet_pass` (population-constants) and `role_orientation` (hard-coded) were each nearly read as live coordinates; framing-audit (#23) + axis-existence checks caught both.
10. **encounter_id vs legendary_id keying** — environment-cell vs home-cell; the KR-vs-gamora "conflict" was two correct readings on different axes. *Lesson: name the key, not just the cell.*
11. **Gate description drift** — the autopsy initially described the emission gate as tier_1-based; the live gate is tier_2-based (boss-KPM retired 2026-06-19). *Lesson: gate semantics are code-anchored (`gauntlet_sim.py:615-667`), not doc-remembered.*
12. **My resource-model misattribution** (§10.4) — cheapest-refuting-test discipline (#19.1) applied to my own claim killed it in one scan.

---

## §12 Costs + throughput

| Item | Value |
|---|---|
| Candidates generated (driver layer) | 1,800 (18 cells × 100 requested; 4 INT cells composed zero) |
| Fights simulated (defective-but-sound run) | **3,047,800** |
| Gauntlet wall time | **6.0h** (21,589.7s; 11.99s/kit vs pilot 10.65s) |
| Accidental re-fight before kill | 1.5h (no artifact retained) |
| Canonical-JSON recovery | **4.2s** (vs 21,585s — ~5,100×) |
| Carve-out autopsy + review | read-only; ZERO fights |
| LLM spend — emission run | **$0** |
| LLM spend — flavor 35 kits | **$0.1289** |
| **Total LLM spend, run + carve-outs** | **≈ $0.13** |
| Emission yield | **700 / 1,800 = 38.9%**; 7 of 18 cells |

---

## §13 Chain of custody (commits + tags, in order)

**Engine:** `a10a695` decisions-log batch → `e57b9d8` W0 rocket (`rocket/v-demo-run-w0-1`) → `cbd47b5` W0/W1 star-lord (`star-lord/v-demo-run-w1-1`, MIGRATION v1.85) → `87c47a6` W0 gamora (`gamora/v-demo-run-w0-dda-sweep-1`) → `6a7190b` W2 rocket (`rocket/v-demo-run-w2-pairing-1`) → `1ec8265` W2 gamora (`gamora/v-demo-run-w2-pairing-cert-1`) → `0a1706c` W3 refutation (halt-loud) → `dc00b2a` step-0 registry (`star-lord/v-demo-run-w3-step0-registry-1`, v1.86) → `ea753a3` driver + pilot → `0fd813e` mid-run state → `49424e7` diagnosis (v1.88) → `1112cf0` true bundle (`…batch1-1`, v1.89) → `2839caf` smoke guard + bc_target_cell fix (**`…batch1-2` — bundle-of-record tag**, v1.90) → `f3c5aec` W4 G4 (`gamora/v-demo-run-w4-g4-1`) → `3417d19` autopsy notes → `62abdc7` F1 bridge + glyph (`star-lord/v-demo-run-f1-glyph-1`) → `4786868` flavor 35 (`star-lord/v-demo-run-flavor-shortlist-1`).

**Collab:** `cc24556` refutation finding → `4ce838d` true bundle landed → `136881c` gandalf drift verdict → `8afcab7` jack-ryan Gate-2 → `31ac34e` W4 closed → `1148c7c` KR handoff → `97abed2` gandalf glyph pre-run (caster-wipeout headline) → `e2ca7fb` gandalf decision-file addendum → `b9b8b31` KR carve-out staging → `fca8d78` autopsy append → `a23f881` Beat-A completion → `1bb1950` jack-ryan review verdict → `d637a2d` gandalf carve-out delta → `fdb3ed9` Beat-B completion → `c7df7f7` gandalf flavor closeout.

---

## §14 Open items at halt (register only — sequencing + recommendations are Doc 2)

1. **THE RULING (yours, open):** summoner path Option 1 vs Option 2 — `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`, now carrying the corrected half-structural/half-calibration decomposition.
2. **G7a roster picks (yours):** 1-of-5 per seat × 7 martial seats — all inputs complete (§7.4).
3. gamora's 4 doc-only autopsy corrections (jack-ryan-required).
4. Spec v1.2 hygiene: strike `ProxySpawn` lift + the "2026-06-24" reference from criterion C (jack-ryan).
5. Optional pre-ruling evidence: read-only rocket diagnostic — why do non-melee INT cells compose zero?
6. E4 ECHO ally-attack channel (named prerequisite; batch-2-adjacent).
7. Defensive-cohort fixture artifact — fix or document-as-designed.
8. GLASS CANNON fragility — stat pass to make "glass" claimable.
9. KR's remaining tracker-delta folds.
10. **API key rotation** (key transited chat this session).

---

**Signed:** gandalf, 2026-07-03 — full findings record at halt; zero unresolved integrity issues; one Matt ruling + one Matt pick session open.
