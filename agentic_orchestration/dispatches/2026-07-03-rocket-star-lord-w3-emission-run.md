# Dispatch — 2026-07-03 — rocket → star-lord — W3 THE EMISSION RUN (DEMO-READINESS UNATTENDED RUN)

**From:** knight-rider
**To:** rocket (Phase A: un-gate) → star-lord (Phase B: registry writer + pilot beat + full-spectrum emission + gauntlet + flavor + assemble + register), serial
**Approved by:** Matt 2026-07-03 (run fire authorized; emission exercise Matt-authorized per spec §1-C — the export/MIGRATION v1.81-1.82 hold's first Matt-authorized exercise; LLM spend authorized no-cap, key errors out, spend logged per pass)
**Single authority:** `canonical/reap-die-rise-engine/demo-readiness-run-spec-2026-07-03.md` **v1.1** — §1 criteria A–F, §3 W3, §4, §5, §6, §7. Cite it; do not re-derive.
**Estimated effort:** Phase A short; Phase B one long session (the run itself)
**gates-on:** ~~W0(all) · W1(all) · W2 · singleton-smoke-green · registry-schema-ratified~~ **ALL ✓** — W2 landed FULL (pairing η LIVE; NOT the degrade config)
**Failure policy (spec §7, load-bearing):** halt-loud, never silent-skip. Pilot beat is UNCONDITIONAL — W3 cannot skip it (§4: per-kit wall-clock at scale is the one unverified load-bearing quantity). Flavor failure: one retry → halt the wave loud + park (a NULL-riddled bundle fakes criterion B). LLM key exhaust = natural halt (G3): register partial state + spend log; per-item calls are resumable, no double-billing on survivors already named.

## Context

W0–W2 are closed with zero failure-policy invocations. Propagation is ON (gamora W0 floor cert `87c47a6`). Pairing layer is live + certified (rocket `6a7190b`, gamora `1ec8265`) — CONVERGENCE + DUAL_PROXY offerable, 63/65 valid pairs magnitude-certified. Registry schema RATIFIED-WITH-AMENDMENTS (jack-ryan, G9): the writer builds against the draft (`export/math/DRAFT-run-registry-schema-2026-07-03.md`) **+ `generation_seed INTEGER`** (manifest.json source) **+ `in_band_count INTEGER`** (queryable measured output; JSON blob retained). This dispatch executes the run the whole program has been building toward: one registered, fully-flavored, full-spectrum, six-type Godot-consumable bundle.

**E4 carry (W2 named prerequisite — NOT a blocker):** the 2 STRIKER×ECHO Mirror pairs (`{autonomous_caster, delayed_position_shadow}`, `{passive_fighter, delayed_position_shadow}`) are magnitude-UNCERTIFIED (ECHO-replay ally-attack channel absent). Kits drawing them may still emit — they merge STRIKER-only until the channel lands. If any survive the gauntlet, flag them in the bundle notes/registry record so W4 curation sees the caveat.

## Required reading before starting

- Run spec v1.1 §1, §3 W3, §4, §5, §6, §7 (+§11 Q1 load-bearing assumptions)
- `export/math/DRAFT-run-registry-schema-2026-07-03.md` + the two ratification amendments (state-board precondition-2 row)
- `export/MIGRATION.md` v1.85 (W1 six-type driver state) + `generation/MIGRATION.md` W2 entry (paired-decl fields)
- W1 completion record (`2026-07-03-star-lord-w0-w1-pipeline-completion.md`) — driver, wiring, resumability evidence
- W2 completion records (both phases, same-file) — pairing state + E4 exclusions
- Engine decisions-log `a10a695` (G1–G10)

## Math-before-code

- **Phase B pilot-beat sizing note** (Disc #1/#1.2): measured per-kit wall-clock + convergence yield from the first ~20 candidates → projection → samples-per-cell sizing for the run window. This note IS the mandatory pilot beat artifact; the full run does not fire until it exists. Include resource-bounds projection per #1.1 (peak memory vs host RAM at thousands-scale).

## Cross-seam contract change? (Principle 6 gate)

- Phase A un-gate: generation-internal config lift — **no emitted dict-shape change expected**; if the lift changes an emitted shape, MIGRATION.md before tag.
- Phase B: the bundle is THE cross-seam artifact (drax/Godot-consumable; `proxy_scaling` contract per §6). Registry DB is new external state — Matt-authorized by the run fire. MIGRATION.md entry for the registry writer + bundle landing (consumers: drax; W4 auditors).
- **Round-trip: the six-type round-trip against the REAL emitted bundle** (not proxies) is Phase B acceptance — the W1 harness carries.

## Scope

**Phase A — rocket** (`gates-on: —`, fires immediately):
- [ ] Lift `_DEFERRED_PROXY_BINS` (`bc_target_composer.py:97,318`) + `ProxySpawn` (`mechanic_alteration.py:46`); correct the stale reason-string (spec §3 W3 step 1)
- [ ] Smoke: proxy bins + ProxySpawn draw in generation; T4 suite + pairing layer offerable on eligible kits; singleton config still executable (no regression of the W0 smoke)
- [ ] MIGRATION.md if any emitted shape changes (state explicitly if generation-internal)
- [ ] AGENT_STATE.md updated · Tag: `rocket/v-demo-run-w3-ungate-1`

**Phase B — star-lord** (`gates-on: W3.phaseA`):
- [ ] **Step 0 — registry writer (#8b)**: build against the ratified draft schema **+ `generation_seed` + `in_band_count`**; launch exclusions stand (no cost_usd/git_sha/FKs). Registry row per run/batch: run_id · timestamp · config hash · bundle path · gauntlet summary · cert status (criterion F)
- [ ] **Pilot beat (UNCONDITIONAL, §4)**: first ~20 candidates → measure per-kit balance-loop wall-clock + in-band yield → sizing note (math-before-code above) → size samples-per-cell to the run window
- [ ] **Full-spectrum emission (G2)**: thousands of candidates, all six content types, T4 suite + pairing layer + proxy bins live; mechanism seam-owned (one wide run or several registered batches — all batches register)
- [ ] **Gauntlet filter**: recompose-first balance loop + ≥9/18 per kit → in-band survivor set; **the count is a measured output, not a promise** (yield honesty, §4)
- [ ] **Flavor passes — split by content class (Gate-1 #4)**: kit-identity flavor on gauntlet SURVIVORS ONLY; monster/gear/faction flavor keys off bundle-membership at assembly; ALL calls per-item → resumable; **log LLM spend per pass**
- [ ] **Bundle assembly + register** (criteria A/B/F): six types, `proxies` landing key, `proxy_scaling` contract (§6), zero hollow spots (no NULL flavor_text/main_weapon/names; monsters + gear pool + factions written); register the run
- [ ] **E4 flag**: if any Mirror-pair kit survives, flag it in the registry record/bundle notes (STRIKER-only merge caveat)
- [ ] Six-type round-trip against the REAL bundle (W1 harness) — non-NULL counts per type
- [ ] MIGRATION.md · AGENT_STATE.md · Tag: `star-lord/v-demo-run-w3-emission-1`

**Both phases: push HELD — KR pushes both repos at W3 closeout.**

## Quality criterion (OP §3.11)

**Game-quality goal this dispatch serves:** the demo opens from ABUNDANCE — a real registered bundle of fully-flavored, gauntlet-certified, six-type content in which summoners are first-class (~25% steer, pairing live) — so Matt curates a roster from real emitted options (G7), and demo work (Q7/Q8/slice) builds against real data, not scaffold.

**Refutation conditions** (surface before executing if any apply):
- Pilot beat projects a run window that cannot complete unattended at any samples-per-cell worth running (report the projection; do NOT silently shrink to a token run)
- The un-gate reveals proxy bins were never emission-viable (structural gap, not config) — halt-loud, that's a finding
- Acceptance could pass with a bundle that fakes criterion B (NULL-riddled or types present-but-empty)
- Anything requires re-opening a ratified spec (registry schema, pairing design, flavor ordering)
- Resumability assumed but not verified before the LLM pass fires (§11 Q1-iii — W1 verified it; re-verify the survivors path)

## Acceptance criteria

- [ ] Phase A: both gates lifted + stale reason-string corrected; smoke green; no W0 singleton-smoke regression
- [ ] Pilot-beat sizing note exists BEFORE the full run fires, with measured wall-clock + yield + projection
- [ ] Full-spectrum run completes (or halts loud per §7 with registered partial state)
- [ ] In-band survivor set produced; actual count reported vs the 100–400 estimate
- [ ] Flavor split executed per Gate-1 #4; spend logged per pass; zero double-billing on retries
- [ ] Bundle assembled: six types, `proxies` key, `proxy_scaling` contract, zero hollow spots — verified by the six-type round-trip with non-NULL counts
- [ ] Run(s) registered with `generation_seed` + `in_band_count` populated
- [ ] MIGRATION.md before tags

## Out of scope

- W4 verification (DRIFT-CRITIC, Gate-2, G4 hypothesis test, offer-table verify, §8 shortlist)
- Any demo work (Q7 hero rig / Q8 camera / vertical slice — gates on W4)
- ECHO-replay ally-attack channel (W2 named prerequisite — separate follow-up)
- Knob retuning if composition under/overshoots (§5: finding comes back, not a silent re-run)
- Near-dupe distinctiveness handling (launch concern, §4)
- PROXY_INVERSION (deferred-by-ruling)

## References

- Run spec v1.1 (single authority) · registry ratification (state board precondition 2) · W0/W1/W2 tags: `e57b9d8` / `cbd47b5` / `87c47a6` / `6a7190b` / `1ec8265` · decisions-log `a10a695`

---

## Completion record — Phase A (rocket) — 2026-07-03 — REFUTATION FIRED · HALT-LOUD · NO un-gate · NO tag

**Status:** HALT-LOUD per spec §7 + this dispatch's refutation condition (line 63). The un-gate reveals proxy bins were **never emission-viable via config-lift — a structural generation-pipeline gap, not a config gate.** I did NOT perform the lift and did NOT tag `rocket/v-demo-run-w3-ungate-1`. This is a finding requiring a Matt scope-ruling before W3 can proceed. **Phase B (star-lord) is BLOCKED pending that ruling** — it must not fire assuming proxy bins emit summoners.

**Full finding (evidence + probe + options):** `reincarnated-engine/src/reincarnated/generation/notes/w3-ungate-refutation-fired-2026-07-03.md`. AGENT_STATE updated with the halt.

### What I was asked to lift vs. what I found

- **`_DEFERRED_PROXY_BINS` (`bc_target_composer.py:97,318`)** — a real gate. Lifting it (verified in-memory) lets proxy bins pass `check_infeasibility` and compose a `ComposedKit`. BUT the composed kit carries **zero summon skills** → `build_proxies_surface` returns `[]` → hollow proxy-heavy kit.
- **`ProxySpawn` (`mechanic_alteration.py:46`)** — **NOT a live gate.** Line 46 is inside a docstring (lines 44–52); the `ProxySpawn` named at line 49 is the **RETIRED v1.1 dormant-register entry** (Matt ruling 2026-07-02, spec §6; provenance closed in git `f9762a8`→`d6bca67`, never designed). `ProxySpawnStrategy` was revived AS S6 of the proxy-T4 family then itself retired in the B1-REBASE. **There is no `ProxySpawn` gate to lift.**
- **Stale reason-string:** `bc_target_composer.py:321` says "proxy-creation mechanics absent." That is now itself inaccurate — the mechanic `summon_proxy_basic` EXISTS in the pool (`unified_mechanic_pool.yaml:1194`) but is `deferred: true`, AND (the real blocker) no gen-path routes a proxy bin to a summon skill. I did NOT edit the string (halting supersedes cosmetics; correcting it would imply the lift proceeded).
- **No `2026-06-24` ratification reference exists anywhere in the engine tree** (`grep -rn "2026-06-24" src/ design/` → empty). Noted; the spec authority still stands.

### The structural gap (empirically demonstrated, in-memory probe, seed 53_000_001)

Un-gate `_DEFERRED_PROXY_BINS`, compose `("mid-slow","multi-spawn","proxy-heavy","damage-pure","medium","variable","glass","steady")`, role=damage, profile=A → `ComposedKit`, **0 summon-category mechanics, 0 multi-spawn mechanics.** Three independent fatal blockers:
1. Phase 4d (`bc_target_composer.py:756-757`) is a NO-OP stub assuming `proxy_bin=="solo"`.
2. `multi-spawn` geo maps to `multi_projectile` mechanics (`:380-384`) — projectile multiplicity, not entity summoning.
3. `PoolMechanic` carries no summon discriminator (`effect_category`/`proxy_geometry`/`proxy_acquisition`) that `build_proxies_surface` requires; the sole `is_proxy_creation` mechanic (`summon_proxy_basic`) is deferred out of `ACTIVE_MECHANIC_POOL` (71→67) and, even un-deferred, lacks those fields.

Codebase's own current-state prose corroborates: `demo_summoner_kits.py:4-7` — *"no summoner kit comes out of the normal pipeline today and every kit emits `"proxies": []`."* Summoner content today is HAND-AUTHORED only.

### Smoke results

- **Proxy-draw smoke (the dispatch's step-2 requirement): FAILS by design** — proxy bins draw but produce hollow (`proxies: []`) kits. This IS the refutation.
- **W0 singleton-config smoke: not re-run** — un-gating did not proceed, so there is no regression to check against (the tree is unchanged from the certified `1ec8265` state). The W0 smoke remains green as of the last certified run; I made no code change that could regress it.

### MIGRATION disposition

**No MIGRATION.md entry.** No code was edited; no emitted dict shape changed. The `proxies` surface, `t4_alteration_output`, and all emitted shapes are byte-identical to the W2 state (`1ec8265`). Generation-internal, and in fact no-change.

### Tag / push

**No tag.** `rocket/v-demo-run-w3-ungate-1` NOT created (the un-gate it names is not emission-viable). Nothing to push. The only artifacts are the finding note + AGENT_STATE update + this completion record.

### Refutation fired

YES — dispatch line 63 / spec §7: *"The un-gate reveals proxy bins were never emission-viable (structural gap, not config) — halt-loud, that's a finding."* Condition met and honored. Routing to KR/Matt for the scope-ruling (options in the finding note §"Options for Matt"). My pragmatic non-binding read: run W3 in a proxy-degrade config (full-spectrum SOLO emission + hand-authored curated summoners flagged not-emitted, per the existing III.1b demo=curated split) THIS run, with a named gen-path follow-on wave (math-first + Gate-1) to earn generation-emitted summoners — but the criterion-C/G4 re-touch makes it Matt's call.

---

## Completion record — Phase B step 0 (star-lord) — 2026-07-03 — DONE

**Status:** COMPLETE — step-0 scope only, per KR carve-out (ruling-independent; criterion F satisfied under every Matt scope-ruling option).
**Tag:** `star-lord/v-demo-run-w3-step0-registry-1` @ `dc00b2a` (engine repo)
**Push:** HELD — KR pushes at W3 closeout (both repos together).
**Schema ratification cited:** jack-ryan G9 W0/W1-boundary fast pass (`demo-readiness-run-state-2026-07-03.md` precondition-2 row) — DONE before building. Discipline #8 (ratify-before-build) + Gate-1 #5 honored.

### Refutation check: HALTED/PARTIAL state expressibility

Surfaced before executing. Result: **NO schema re-opening required.**

`cert_status TEXT` is unconstrained (no SQL CHECK). `"HALTED"` and `"PARTIAL"` are valid values. A parked W3 (blocked pending Matt's scope-ruling) is registerable as:
- `cert_status = "HALTED"`
- `in_band_count = NULL` (gauntlet never fired)
- `gauntlet_summary = NULL`
- `notes` = halt reason + finding reference

Test Group D (5 tests) closes this refutation condition empirically: all PASS.

### What was built

**Writer:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/run_registry.py`

Table `emission_runs` in `data/emission_registry.db` (standalone SQLite, WAL mode, no FKs):
- 15 base columns from ratified draft schema
- `generation_seed INTEGER` (Amendment 1 — manifest.json source; reproducibility leg)
- `in_band_count INTEGER` (Amendment 2 — gauntlet survivors; queryable for W4/§8)
- Launch exclusions absent: no `cost_usd`, no `git_sha`, no FK columns
- `CREATE TABLE IF NOT EXISTS` — idempotent; W3 re-fire requires no migration

Public API: `initialize_registry()`, `register_run()` (INSERT OR REPLACE + Disc #8 boundary validation), `read_run()`, `list_runs()`, `update_cert_status()`, `compute_config_hash()`, `make_run_id()`. Constants: `CERT_STATUS_*`, `STAGE_*`.

### Tests

**File:** `/Users/admin/Games/reincarnated-engine/tests/test_run_registry.py`
**Result:** 48/48 PASS (Groups A–G)
- A (6): schema creation, column presence, launch exclusions absent, FK absent, idempotent DDL, PK check
- B (10): row insert + round-trip (all fields, type coercions, NULL, timestamp UTC, config hash)
- C (6): amendment fields — `generation_seed`, `in_band_count` — isolated, combined, queryable
- D (5): HALTED/PARTIAL state expressibility — refutation check CLOSED
- E (3): idempotent INSERT OR REPLACE + distinct-ID distinctness
- F (5): `_validate_run_record` boundary enforcement (Discipline #8)
- G (13): config hash determinism/length/collision, make_run_id, list_runs filters, update_cert_status

**Regression:** 4822 total PASS / 118 pre-existing fail / 0 new regressions (baseline 4774 before this session's 48 additions).

### MIGRATION.md

v1.86 prepended to `export/MIGRATION.md` before tag. Registry DB is a new external artifact. Consumer obligations: W3 register step, W4 auditors.

### AGENT_STATE.md

Updated at `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/AGENT_STATE.md`.

### What this does NOT do (per KR step-0 carve-out)

- Pilot beat NOT fired (gates on Matt scope-ruling for W3 full emission)
- Full-spectrum emission NOT run
- Generation NOT touched
- Phase B steps 1–7 NOT executed (held pending ruling)

### Carry-forward for W3 re-fire

When Matt rules and W3 re-fires (under any option): call `initialize_registry()` then `register_run()` with `generation_seed` from manifest.json and `in_band_count` from the gauntlet survivor count. If the run is blocked again, call with `cert_status=CERT_STATUS_HALTED`. The writer is re-callable without migration.

---

## Completion record — Phase B steps 1-5 (star-lord) — 2026-07-03 — IN PROGRESS (full run fired)

**Status:** Pre-run artifacts COMPLETE. Full 1,800-candidate unattended run FIRING NOW (~5.32h projected).
**KR run-disposition ruling applied:** W3 fires as SOLO FULL-SPECTRUM BATCH 1. Criterion C PARKED (summoner emission = batch 2, gates on Matt ruling `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`). `_DEFERRED_PROXY_BINS` stays gated. `proxies=[]` on all batch-1 kits = honest state.
**Engine commit:** `ea753a3` (pre-run artifacts — driver + pilot math note + tests + MIGRATION.md v1.87)
**Tag:** `star-lord/v-demo-run-w3-emission-batch1-1` — TO BE FIRED after full run completes.
**Push:** HELD — KR pushes both repos at W3 closeout.

### Phase B step 1 — Pilot beat (UNCONDITIONAL §4): DONE

**Math note:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/math/w3-pilot-beat-sizing-2026-07-03.md`

Measurements (20-kit full-gauntlet pilot, seed 55_000_000):
- Per-kit wall-clock: **10.65s** (Run B: 20 kits / 213.00s total)
- In-band yield: **64%** (18/28 configs pass the cycle-14 v1 stratified floor at full 18 encounters)
- Peak RSS: **48.7 MB** (Discipline #1.1 PASS — well under 8 GB host)

Sizing decision: **N=100 → 1,800 candidates → ~5.32h** (2.68h slack for flavor + buffer; 8h window comfortable).
Expected survivors at 64% yield: ~1,152 (well above the 100-400 estimate — honest measured output per Discipline #29).

Full run UNBLOCKED — math note exists before run fires (spec §4 requirement).

### Phase B step 2 — Driver (w3_emission_driver.py): DONE

**File:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/w3_emission_driver.py`

Key implementation notes:
- Uses `w5r2_gauntlet_sim_integration()` (NOT `run_gauntlet_sim()` directly) — this is the production path that sets `kit.wr_bracket_pass` by reading the canonical JSON output at `simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json`.
- `character_id → id` bridge applied before `build_kit_record()`: `to_character_dict()` outputs "character_id" but `_KIT_PASSTHROUGH_FIELDS` expects "id".
- `_ENGINE_ROOT = Path(__file__).parents[3]` (was incorrectly parents[4] in draft).
- `smoke_validate_bundle_from_file(require_proxies=False)` — new parameter to `one_realm_bundle_assembler.py` (backward-compat default=True); batch-1 honest state bypass.

Smoke PASS: pipeline end-to-end, 5 kits, 40 monsters, 150 gear, round-trip PASS, run_id issued.

### Phase B step 3 — Tests (Discipline #2): DONE

**File:** `/Users/admin/Games/reincarnated-engine/tests/test_w3_emission_driver.py`
**Result:** 24/24 PASS (Groups A–E):
- A: SpendLedger (6) — initial state, accumulation, resumption, summary structure
- B: _verify_resumability (5) — halt-loud on empty, missing id, passes on valid + pre-flavored
- C: smoke_validate_bundle_from_file require_proxies param (2) — False passes, True rejects
- D: smoke run integration (8) — pipeline end-to-end; id bridge; proxies=[]; proxy_scaling; round-trip; criterion C PARKED; registry notes
- E: constants/config (3) — N=100, seed=55M, registry notes required phrases

### Phase B step 4 — MIGRATION.md v1.87: DONE

New bundle artifact (`src/reincarnated/output/w3_batch1_bundle.json`), API extension to `smoke_validate_bundle_from_file`, driver constants/CLI, pilot beat math note reference, batch-1 honest-state fields.

### Phase B step 5 — Full run (IN PROGRESS)

**Command fired:** `python3 -m reincarnated.export.w3_emission_driver --n-samples 100 --seed 55000000 --dry-run-flavor`

NOTE: `--dry-run-flavor` used for the unattended run: bypasses LLM calls (wiring verified; full LLM flavor pass is a separate step once the survivor set is confirmed). This produces the gauntlet-only survivor bundle. LLM flavor passes (kit-identity on survivors, monster/gear) to be fired separately once count is confirmed and LLM key status verified.

**Projected:** ~5.32h wall-clock (1,800 candidates × 10.65s/kit). Expected survivors: ~1,152 at 64% yield.

### Report-back items (partial — full run still firing)

- Pilot-beat wall-clock per kit: **10.65s** (20-kit pilot)
- Sizing decision: **N=100 → 1,800 candidates → ~5.32h**
- Total candidates emitted: **1,800** (confirmed from run log)
- In-band survivor count: **7 REPORTED / 700 TRUE** (defect diagnosed — see below)
- Gauntlet stats: 3,047,800 total fights | 21,585s wall-clock | 10 passing legendary_ids / 22 distinct
- LLM spend per pass: **$0** (--dry-run-flavor; LLM flavor pass deferred)
- Bundle path: `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (DEFECTIVE — 7-kit bundle; true 700-kit bundle pending re-run)
- Registry row id: `86fa640c-c553-49fb-8a81-37e6242cf305` (migrated; cert_status=DEFECT-DISCOVERED; in_band_count=NULL)
- Round-trip result: PASS on defective 7-kit bundle; re-run will re-verify on true bundle
- Tag SHA: **NOT FIRED** (holds until true survivor bundle stands)
- Criterion C status: **PARKED** (summoner emission = batch 2, gates on Matt ruling 2026-07-03)

---

## Diagnosis record — Phase B post-run defect analysis (star-lord) — 2026-07-03

**Status:** TWO DEFECTS DIAGNOSED + FIXED. Re-run required. Gauntlet 6h compute RECOVERABLE (NOT repeated).
**Engine commit:** `49424e7` (defect fixes: config_to_kit overwrite + registry path + blind-spot test + MIGRATION v1.88 + AGENT_STATE)
**Tag:** NOT YET FIRED — holds until true survivor bundle stands.
**Push:** HELD — KR pushes at W3 closeout.

### Defect 1 — Impossible survivor pattern (LOAD-BEARING)

**Symptom:** Run reported 7 in-band survivors at 0.4% yield (160× discrepancy from 64% pilot). All 7 survivors were `_s99` (last sample of their BC cell). Statistically impossible by chance.

**Root cause:** `season_generation_pipeline.py:w5r2_gauntlet_sim_integration()`

```python
# BEFORE (buggy):
config_to_kit: dict[str, KitCandidate] = {}
...
config_to_kit[cfg["legendary_id"]] = kit  # OVERWRITES on each iteration
...
for legendary_id, kit in config_to_kit.items():
    if kit_emit_map.get(legendary_id, False):
        kit.wr_bracket_pass = True  # only s99 per cell — all others missed
```

`legendary_id` is derived from `kit.bc_cell_id` (not `character_id`):
- Line 1331: `f"{kit.bc_cell_id}_t4_null"`
- Line 1383: `f"{kit.bc_cell_id}_{chain_id}"`

With 100 samples per cell, all 100 kits from the same cell share one `legendary_id`. Each iteration overwrote the dict, leaving only the last enumerated kit (`_s99`). The gauntlet DID run per-sample fights — the loss was purely in Python survivor collection.

**Fix:** `config_to_kit: dict[str, KitCandidate]` → `config_to_kits: dict[str, list[KitCandidate]]`. All kits from a cell are appended; the marking loop iterates all kits per cell.

**Recoverability: YES — 6h gauntlet compute is NOT repeated.**

The canonical JSON at `src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (93 MB, 2,200 entries) encodes `season_emit` at the BC cell level — all 100 entries for the same `legendary_id` have identical `season_emit`. The fixed driver re-generates all 1,800 kits (fast, ~seconds) and reads the existing JSON to correctly mark 700 survivors.

**True survivor count (from canonical JSON):**
- Passing legendary_ids: 10 / 22
- Passing BC cells: 7 / 18
- **True in-band count: 700 kits** (7 cells × 100 samples each)
- **True yield: 38.9%** (700/1800)
- Passing cells: `endgame_bc_melee_high_flat_str_none`, `endgame_bc_melee_low_spiky_str_none`, `endgame_bc_melee_medium_variable_str_none`, `endgame_bc_mid_high_flat_dex_none`, `endgame_bc_ranged_high_flat_dex_none`, `endgame_bc_ranged_low_spiky_dex_none`, `endgame_bc_ranged_low_spiky_str_none`

### Defect 2 — Registry DB path

**Symptom:** Log: "Emission registry initialized: /Users/admin/Games/data/emission_registry.db" — outside engine repo.

**Root cause:** `src/reincarnated/export/run_registry.py:62` — `_ENGINE_ROOT = Path(__file__).parents[4]`

Correct is `parents[3]`:
- parents[0] = `src/reincarnated/export/`
- parents[1] = `src/reincarnated/`
- parents[2] = `src/`
- parents[3] = `reincarnated-engine/` ← correct
- parents[4] = `Games/` ← wrong (one level too high)

**Fix:** `parents[4]` → `parents[3]`. DB now at `reincarnated-engine/data/emission_registry.db`.

**Migration:** W3 full run row (`run_id=86fa640c-c553-49fb-8a81-37e6242cf305`) migrated to correct-path DB with `cert_status="DEFECT-DISCOVERED"`, `in_band_count=NULL`, corrected `gauntlet_summary` with both buggy and true counts annotated.

**Test blind-spot fixed:** All 48 prior tests used `:memory:` — never exercised `_DEFAULT_REGISTRY_PATH`. New test `TestSchemaCreation::test_default_registry_path_inside_engine_root` (test 49) asserts `_ENGINE_ROOT.name == "reincarnated-engine"` and `_DEFAULT_REGISTRY_PATH.is_relative_to(_ENGINE_ROOT)`. 49/49 PASS.

### Carry-forward: re-run command for KR (detached)

**KR fires this (NOT in-session):**
```bash
cd /Users/admin/Games/reincarnated-engine && \
nohup python3 -m reincarnated.export.w3_emission_driver \
  --n-samples 100 \
  --seed 55000000 \
  --dry-run-flavor \
  > /tmp/w3_batch1_rerun_$(date +%Y%m%d_%H%M%S).log 2>&1 &
echo "PID: $!"
```

Expected behavior with fix: ~minutes for generation (reads existing canonical JSON, no gauntlet re-run) → 700-kit bundle assembled → registered as new run_id with `in_band_count=700` → tag `star-lord/v-demo-run-w3-emission-batch1-1` fires.

**Honesty note:** The registry row `86fa640c...` has `cert_status=DEFECT-DISCOVERED`. The new re-run will produce a fresh `run_id`. The defective row is retained for audit trail. The tag and any flavor passes fire against the new run_id's bundle only.
