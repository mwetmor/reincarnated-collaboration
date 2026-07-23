# Finding — 2026-07-23 — KF-4 kit-compiler (Gate-2, KIT-FIDELITY)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** INFO (overall PASS-WITH-NOTES)
**Target:** engine `06ec241` (math note) + `b0684d4` (compiler module); collab `3694f2fc` (assert SQL); live `corpus.db`
**Developer:** gamora (`rule_owner` + simulation seam)
**Conductor:** gandalf (RUN-CONDUCTOR); charter law "jack-ryan Gate-2 BLOCK on any engine diff (KF-5, and any KF-4 engine touch)"
**Principles applied:** Disciplines #1 (math-before-code), #2 (smoke vs full-regen), #8 (schema/eval boundary), #11 (empirical inspection), #12 (semantic-shift / attribution); Review Principles #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #5 (severity)

## Overall Gate-2 verdict: PASS-WITH-NOTES (no BLOCK)

KF-5 may proceed to build atop this engine diff. All 6 readiness items verified on evidence
(byte-level trace / DB probe / smoke re-run), not on the report's word. The RED (cyclone) is the
fidelity gauge working as designed, not a compiler failure. Two INFO notes + one WARN-adjacent
naming-drift note recorded for the record; none block. The 2-entry mirror-sync is a legitimate
follow-on (mirror-consistency fix, in-scope) — recommendation below.

## Per-item verdict table

| # | Item | Verdict | Load-bearing evidence |
|---|------|---------|----------------------|
| 1 | Zero-engine-change | **PASS** | `git diff 06ec241~1..b0684d4 --name-status` = 7 files, all `A` (added), all under `kit_compiler/` + math note. ZERO `M`. `git diff 2f43045..b0684d4` on `damage_resolver.py`/`spatial_engine.py`/`combatant.py` (the 3 named) = **empty across the whole run**. No existing module imports `kit_compiler` (grep empty) → no hidden coupling. |
| 2 | Mirror-drift finding + bypass | **PASS** | Bypass is real: `spatial_engine._determine_geometry_type_with_source` Path 1 (`spatial_engine.py:823-826`) reads explicit `spatial_geometry_type` and returns immediately before Path 2 ever touches the stale local `_RICH_TO_SPATIAL`. Compiler sets `spatial_geometry_type` explicitly per skill (`kit_compiler.py:531`). Drift confirmed: engine-local table (`spatial_engine.py:752-777`, 24 entries) MISSING `orbit`+`placed_lane`; authoritative `geometry_derivation._RICH_TO_SPATIAL` (`:477-509`, 26 entries) HAS them (`orbit→circle` :485, `placed_lane→line` :495). Smoke: firewall `primary_geometry=='line'` GREEN via `placed_lane`. |
| 3 | Semantic-shift (Disc #12) dual population | **PASS** | Table = 347 rows: 310 dated `2026-07-22` (KF-1) + 37 dated `2026-07-23` (KF-4). Distinguishable by `created_date` AND by the in-row `[KF-4-compiled]` marker on every KF-4 `expected_state` (DB-verified). Reinterpretation documented in 3 places a future reader hits: math note §4.3 Disc-#12 flag, both commit messages, and the in-row provenance marker. Idempotent DELETE keys on the marker, leaves KF-1 rows untouched (`emit_assert_sql.py:9,64`). |
| 4 | Legacy-flat-path injection | **PASS** | Compiler sets `damage_scaling_type=None` + `scaling_attribute=""` (`kit_compiler.py:534-535`). Resolver dispatch (`damage_resolver.py:855`) `_scaling_type = getattr(skill,"damage_scaling_type",None)` → falsy → `if not _scaling_type:` (`:879`) selects the legacy flat path (`:881`): `magnitude = effect.params.get("magnitude",0.0) × skill.damage_multiplier`. Typed physical/magical/hybrid path (which reads `scaling_stat`) is fully skipped; `scaling_attribute=""` further forces `scaling_stat=0` (`:811-813`). RDR leaf enters as `magnitude`, NOT double-scaled. Identity seam preserved. (Math-note line ref "95-97" is stale; actual path is ~879-881 — mechanism correct, cite stale.) |
| 5 | Cyclone RED disposition | **PASS** | Docket `176` (`mechanic_gap_docket`, DB-probed): `mechanism_class=poe1_cyclone_base_weapon_dps_build_point_gap`, `status=open`, full `spec_text_or_path` (VALUE-harvest gap, explicitly NOT engine-mechanic gap), `disposition=reported_for_swap_decision` with options A/B/C deferred to Conductor/Matt, `provenance_json.kind=value_gap`. Compiler refusal path (`acceptance.py:159-161` → `evaluate_asserts:196-200`) reports RED→docket, never swaps/fabricates. RED assert row `routed_docket_id=176`. Smoke: exactly 1 RED = `poe1-cyclone has_damage_base`. |
| 6 | Build-point selector + `_v327_context` fence | **PASS** | The fence catches the trap: 6 `basedmg_pct_gem*_v327ctx` rows (rule `R-CTX-BP`) hold the post-3.27 150% values; compiler selects `effectiveness_pct_gem20_bp=59.0` (rule `R-K4`, the 3.15 build point). Selector skips any key with `v327_context`/`_ctx` OR `rule_id=='R-CTX-BP'` (`kit_compiler.py:167,348`). Matches manifest R-K4 ("`_v327_context` rows CONTEXT-ONLY — must NOT consume as build point"). `_BUILD_POINT_LEVEL={d2:20,poe1:20,poe2:20,gd:None}` matches slvl20/gem20 pins. PIN-N10 n_shards=10 (`n_shards_expected_pin`) → smoke `projectiles_per_cast==10` GREEN. |

## Smoke re-run (self-executed, Discipline #2)

`cd .../reincarnated-engine/src && python3 -m reincarnated.simulation.kit_compiler.smoke_kf4_compiler`
→ **35 GREEN · 1 RED · 1 GAP/untested**, matching the charter's KFL-11a expectation exactly.
RED = `poe1-cyclone: primary_has_damage_base == True (actual=False)` → docket 176 (correct per §4.3).
GAP = `gd-flames-of-ignaffar-purifier` HELD (untested, not red — value un-harvestable, not falsified;
correct disposition). All 4 pilots compile to valid `class_dict` shape + run through the EXISTING
`run_spatial_fight` projection path (finite damage, HP resolves, no crash). `SMOKE PASS`.

## Determinism risk: NIL — byte-identical trace check NOT needed

The additive-only structure IS the determinism proof. A trace-diff would be theater. Rationale:
determinism drift requires either (a) an existing code path changed, or (b) a new import mutated
shared state. Neither exists: KF-4 diff = 7 `A`-only files; zero diff to any existing combat/geometry/
resolver file across the whole run; no production module imports `kit_compiler` (leaf module). The
compiler is a pure function of read-only DB rows → `class_dict`; fight RNG is seeded separately at run
time. Existing paths are bit-for-bit unchanged ⇒ same seed → same trace by construction.

## Additional verifications (beyond the 6 items)

- **DB byte-rebuildability + idempotency (Disc #11):** re-ran the committed `.sql` twice against a DB
  copy — asserts stable at 347→347→347; KF-4-compiler docket stays at exactly 1 (no accumulation).
  DELETE-then-INSERT in a transaction; `routed_docket_id` resolves docket via subquery so it survives
  auto-increment-id shifts on rebuild. Robust.
- **READ-ONLY compliance (charter + my own constraint):** `kit_reader` opens `mode=ro` — no write can
  occur; reads `rdr_value` only, never `source_value` for damage (dual-column law; `kit_reader.py:5-6,187`).
  The one `file:` use is a sqlite ACCESS-MODE URI (`mode=ro`), explicitly distinguished from the banned
  corpus `file:` addressing convention (`:117-119`); DB path validated as PLAIN.
- **Discipline #8 (no arbitrary code from data):** assert evaluator is a restricted dispatch over
  `_OPS`={==,!=,>=,<=} against an allow-list `_FIELD_READERS` (`acceptance.py:41-58`) — NOT `eval()`.
- **Scope-attribution catch (Disc #12):** `git diff 2f43045..b0684d4` shows `spatial_engine.py` +98
  lines — but that is entirely from the PRIOR commit `1564e2f` (REPLICA-1 emitter, already Gate-2
  PASSED 2026-07-22), NOT KF-4. The KF-4 range touches `spatial_engine.py` for zero lines. Confirmed
  the emitter change is out of this review's scope.

## Notes for the record (INFO — none block)

- **INFO-1 (math-note cite staleness):** the math note §0 / §6 item 2 cite `damage_resolver.py:96` /
  `:95-97`. The real legacy-flat path is `damage_resolver.py:879-881`, and `spatial_engine.py` lives at
  `simulation/spatial_gauntlet/spatial_engine.py` (note references it unqualified). The MECHANISM
  described is correct and correctly targeted; only the line/path citations drifted (the resolver has
  grown since the reference was written). No code impact. Developer may refresh the cites opportunistically.
- **INFO-2 (manifest key-name descriptor drift, item 6):** manifest R-K4 names the cyclone build-point
  leaf `poe1_effectiveness_pct_v315`/`poe1_base_damage_pct_v315`; the emitted DB keys are
  `effectiveness_pct_gem20_bp`/`base_damage_pct_gem20_bp` (same value 59.0, same rule R-K4). Prose-vs-key
  descriptor drift only; the selector matches the actual `_bp` suffix, so correctness is unaffected.
- **INFO-3 (PIN-C3 conflict, on gamora's list):** D2 life-coefficients use maxroll primary
  (`life_per_level=1.0`, `life_per_vit=2.0`, rule R-A1); manifest R-A1 carries the fextralife
  alternative (+2/level,+3/vit) as a dual-anchored annotation. This affects HP-pool identity ONLY —
  the compiler sets `scaling_stat=0`, so stats never amplify damage (`kit_compiler.py:447,534-535`).
  Zero effect on the damage-fidelity gauge. The maxroll choice is a sound curation call, correctly
  surfaced as Gate-2-reviewable; I concur with maxroll-primary (D2R-platform precedence, PIN-C3).

## Mirror-sync follow-on disposition (the 2-entry recommendation)

**Verdict: IN-SCOPE mirror-consistency fix, NOT a mechanic change. Recommend as a follow-on — I approve
the change-class; the edit itself is a separate engine diff that rides its own Gate-2.**

gamora's recommendation is to add `placed_lane→line` and `orbit→circle` to
`spatial_engine._RICH_TO_SPATIAL` (`:752-777`) so the engine-local mirror matches the authoritative
`generation.geometry_derivation._RICH_TO_SPATIAL` (`:477-509`). Assessment:
- It is a **mirror-consistency fix**, not a mechanic change. The two Wave-C entries already exist in the
  authoritative table (which passed Gate-2 at Wave-C 2026-07-17) and in the compiler's own copy. The
  engine-local table is simply stale — the file's own comments (`:751`) declare it "mirrors
  geometry_derivation._RICH_TO_SPATIAL." A stale mirror against a passed authoritative source is a bug,
  and syncing 2 entries to match is a consistency repair.
- **Byte-neutrality argument holds:** both entries only fire for skills carrying `placed_lane`/`orbit`
  rich geometry with NO explicit `spatial_geometry_type`. Today the ONLY producers of those rich values
  are (a) the KF-4 compiler, which sets `spatial_geometry_type` explicitly and so never reaches the
  mirror, and (b) Wave-C generation, which sets it via `derive_spatial_geometry_type`. So syncing the 2
  entries changes NO current trace — it removes a latent Path-2 landmine for any future producer that
  emits rich `placed_lane`/`orbit` WITHOUT the explicit spatial field (which would currently fall to
  the Path-3 name-keyword heuristic and mis-derive).
- **Under ADR-002 this is a within-seam refactor with no API change to consumers** (the value returned
  for existing inputs is unchanged; only previously-heuristic inputs now resolve correctly). It is
  rocket's or gamora's to author in the `spatial_gauntlet` seam. Because charter law makes ANY engine
  diff Gate-2-gated, the 2-line sync gets its own Gate-2 pass — but it is INFO-severity and I pre-approve
  the change-class here.
- **This finding does NOT require the sync to unblock KF-5.** The compiler's explicit-field bypass makes
  KF-4/KF-5 correct today regardless of the mirror. The sync is hygiene (close the latent drift), not a
  precondition.

## Action

- [x] Developer (gamora): no fix-forward required for KF-4. All 6 items PASS. KF-5 unblocked.
- [ ] Developer (gamora/rocket, follow-on, INFO): author the 2-entry `spatial_engine._RICH_TO_SPATIAL`
      mirror-sync (`placed_lane→line`, `orbit→circle`) as its own additive engine diff; it rides a
      separate Gate-2 (pre-approved change-class). Byte-neutral to all current traces. Non-blocking.
- [ ] Developer (gamora, opportunistic, INFO): refresh math-note line/path cites (§0/§6) —
      `damage_resolver.py:879-881`, `simulation/spatial_gauntlet/spatial_engine.py`.
- [x] Conductor (gandalf): Gate-2 returns PASS-WITH-NOTES → KF-5 may proceed per KFL-11c. Cyclone RED
      remains the A-path fork (KFL-11b) — a value-harvest gap, not a compiler defect; roster untouched
      pending the 3.15 weapon-DPS harvest verdict.
- [ ] Matt: no decision needed from this Gate-2 (no BLOCK, no locked-decision conflict). The cyclone
      B-vs-C escalation (accept-partial vs §5 swap) reaches you only IF the 3.15 weapon DPS proves
      unanchorable (per KFL-11b), which is a separate lane.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/kit_compiler/` — kit_reader.py, kit_compiler.py, acceptance.py, emit_assert_sql.py, smoke_kf4_compiler.py, __init__.py
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/kf4-kit-compiler-2026-07-23.md`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:855,879-881,811-813`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:752-777,823-838`
- `~/Games/reincarnated-engine/src/reincarnated/generation/geometry_derivation.py:477-509`
- `~/Games/reincarnated-collaboration/agentic_orchestration/research/scripts/catalogue_migrations/corpus_kf4_acceptance_asserts.sql`
- `~/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db` (READ-ONLY probes: docket 176, kit_acceptance_assert dual population, kit_numeric v327 fence)
- `~/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-07-23-kf23-rules-needed-manifest.md` (R-K4, R-M3, R-A1 pins)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-charter.md` (§KF-4, §5, §8, KFL-9..KFL-11)
