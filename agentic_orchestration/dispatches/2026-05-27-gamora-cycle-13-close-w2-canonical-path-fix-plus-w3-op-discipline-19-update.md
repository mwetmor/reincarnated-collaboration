# Dispatch — gamora — Cycle 13 Close W2 + W3 Bundled Amendment

**Date authored:** 2026-05-27
**Authored by:** knight-rider (per jack-ryan PASS-with-WARN verdict `482801c`)
**Status:** PENDING
**Cycle:** 13 (post-close non-blocking remediation)
**Scope:** BUNDLED W2 (canonical-path-overwrite fix) + W3 (Discipline #19 OP amendment)

---

## 0. Context

Jack-ryan PASS-with-WARN verdict at `agentic_orchestration/qa/findings/2026-05-27-cycle-13-close-gate-2-re-verification.md` flagged two non-blocking gamora-seam WARNs requiring amendment:

- **W2 — canonical-path-overwrite:** the dispatch-named canonical path `cycle-13-gauntlet-sim-results-2026-05-27.json` was overwritten during subsequent smoke iterations + now contains 5-kit / 1,500-fight smoke data instead of the 16-kit / 27,360-fight full-empirical-run truth. The truth lives at the timestamped variant `cycle-13-gauntlet-sim-results-20260527_144454.json` (620,907 bytes; 10:44).
- **W3 — Discipline #19 violation:** during Track A execution, gamora fired 9 concurrent pytest shells against the engine repo (3 partition-parallel + 6 zombie full-suite invocations) without serializing test runs. No work-product corruption observed; resource cost only. Operating-procedure update recommended.

Both seam-internal to gamora. Bundled for efficiency. Non-blocking — Cycle 13 close PASSes with these WARNs in flight.

---

## 1. Required reading

1. **`agentic_orchestration/qa/findings/2026-05-27-cycle-13-close-gate-2-re-verification.md`** — jack-ryan verdict (§ "Adjudication on canonical-path-overwrite" + § "WARN W3" specifically)
2. **`agentic_orchestration/dispatches/2026-05-27-jack-ryan-cycle-13-close-re-verification-bundled-track-a-plus-track-b.md`** § 3 + § 4 — KR forensic finding + Discipline #19 violation flag
3. **`reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260527_144454.json`** — the 620K truth file
4. **`reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json`** — the canonical-named path now containing smoke data
5. **`reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`** § v1.31 — your prior remediation MIGRATION entry; amend with W2 + W3 follow-on entries
6. **`reincarnated-engine/.claude/skills/`** (if a gamora operating-procedure skill is installed there) OR **`reincarnated-collaboration/.claude/skills/`** (meta-repo equivalent) — locate gamora's operating-procedure for W3 amendment
7. **`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — Discipline #19 verbatim

---

## 2. Scope — sequential steps

### Step 1 — W2 canonical-path-overwrite fix

**Action:** copy the 620K full-empirical-truth file to the canonical dispatch-named path, overwriting the smoke data.

```
cp reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260527_144454.json \
   reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json
```

**Verification step (Discipline #11):** after copy, read the canonical path + verify it now contains:
- `total_kits_validated: 16`
- `kits_season_emit: 16`
- `season_emit_rate: 1.0`
- `total_fights_run: 27360`
- `mean_encounters_passed_per_kit: 14.25`
- `kit_results` count: 16
- `encounter_results` count: 912

**Optional defensive step:** consider whether the gauntlet sim's output-write path should be amended to use an atomic rename pattern (write to temp file + rename), preventing future smoke-overwrites of canonical paths. If yes, document in the math note + MIGRATION.md as an additional discipline-improvement. Out-of-scope for this dispatch's required acceptance criteria, but a logical W2-companion change you may choose to author.

### Step 2 — W3 OP amendment for Discipline #19

**Action:** locate the gamora operating-procedure skill (or equivalent runbook) + add explicit pytest-serialization constraint.

If gamora has an installed operating-procedure skill at `.claude/skills/reincarnated-gamora-operating-procedure/SKILL.md` (or similar — model on the existing `reincarnated-knight-rider-operating-procedure` skill at `~/Games/reincarnated-collaboration/.claude/skills/reincarnated-knight-rider-operating-procedure/SKILL.md`), amend with a section roughly:

```markdown
### 3.X — Pytest-serialization (Discipline #19 reinforcement)

**Anti-pattern observed Cycle 13 Track A:** firing concurrent full-suite pytest runs against the engine repo while prior runs are still in flight. Causes SQLite lock contention on telemetry.db, zombie processes consuming CPU/memory, and ambiguous test results.

**Rule:** serialize pytest runs. Wait for one to complete before firing the next. If parallel-partition test execution is desired, use pytest-xdist (`pytest -n auto`) within a SINGLE invocation — do not fire multiple pytest shells in parallel.

**Composition with Discipline #19:** the broader Agent-tool-not-for-waiting discipline forbids sleep-polling; this addendum constrains pytest-firing pattern within the same spirit.
```

If no installed skill exists, author the W3 amendment directly in `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` as a "behavioral discipline note" section, OR add to the engine-wide `engineering-disciplines.md` as a #19.x sub-discipline (jack-ryan owns engineering-disciplines.md per role authority — if you choose this path, flag for KR to route jack-ryan dispatch instead of writing directly).

**Recommended:** amend installed skill if one exists; otherwise amend AGENT_STATE.md (gamora's seam-owned file). Do NOT write to engineering-disciplines.md directly (jack-ryan's authority).

### Step 3 — MIGRATION.md entries

Amend `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`:

- New § (next version after v1.31) — W2 canonical-path-overwrite fix + (if you chose) atomic-rename pattern adoption
- New § — W3 Discipline #19 OP amendment cross-reference

Per ADR-004.

### Step 4 — Test suite verification

Run engine pytest suite **serially** (single invocation; do not fire multiple) to verify no regressions from Step 1/2 work. Quick spot-check only:

```
cd /Users/admin/Games/reincarnated-engine && PYTHONPATH=src python3 -m pytest tests/simulation/ -q 2>&1 | tail -10
```

Expected: no new failures.

---

## 3. Acceptance criteria

- [x] Canonical path `cycle-13-gauntlet-sim-results-2026-05-27.json` contains the 16-kit / 27,360-fight full-empirical-run data (verified via Discipline #11 spot-check)
- [x] W3 OP amendment lands (skill amendment OR AGENT_STATE.md addition) with pytest-serialization rule
- [x] MIGRATION.md § v1.32 (or next) documents W2 + W3 amendments
- [x] No test-suite regressions
- [x] (Optional) atomic-rename pattern for canonical output writes — if you adopt, document in math note + MIGRATION

---

## 4. Out-of-scope

- **Do NOT** modify gauntlet sim simulation logic itself — W2 is path-write hygiene only
- **Do NOT** modify the 620K timestamped variant — it's the source of truth being copied FROM
- **Do NOT** write directly to engineering-disciplines.md (jack-ryan's authority); flag KR if disciplines-amendment is your preferred W3 path
- **Do NOT** re-run the full gauntlet — the empirical truth already exists; W2 is path-correction only

---

## 5. Completion record protocol

Append a completion record to this dispatch file with:

- **Status:** COMPLETE
- **W2 verification:** canonical path now contains 27,360 fights / 16/16 kits (spot-checked)
- **W3 amendment:** path of skill OR AGENT_STATE.md amended; brief summary of constraint added
- **Atomic-rename adoption:** yes/no; if yes, brief description
- **MIGRATION.md § version**
- **Test suite spot-check result**
- **Commit SHA(s)**

KR will pick up + close W2 + W3 tasks. After all 4 WARNs are remediated (W2, W3, W4 by rocket, and implicit W1 if any), KR updates the wind-down summary for Matt's ratification surface.

---

**Authority:** knight-rider per Matt Option A authorization + jack-ryan verdict `482801c` + ratified framing brief § 4.1 autonomous scope + Matt per-cycle-push authorization.

---

## Completion record

**Status:** COMPLETE
**Completed:** 2026-05-27
**Completed by:** gamora

### W2 verification

Canonical path `cycle-13-gauntlet-sim-results-2026-05-27.json` now contains the full 16-kit / 27,360-fight empirical-run truth. Discipline #11 spot-check results:

```
total_kits_validated: 16        (was 5 in smoke data)
kits_season_emit: 16            (was 0)
season_emit_rate: 1.0           (was 0.0)
total_fights_run: 27360         (was 1500)
mean_encounters_passed_per_kit: 14.25  (was 2.5)
kit_results count: 16           (was 5)
encounter_results count: 912    (was 50)
file size: 620,907 bytes        (was 35,771 bytes)
```

All 7 acceptance criteria from dispatch § 2 Step 1 verified.

### Atomic-rename adoption

**YES** — adopted as W2 companion structural fix in `gauntlet_sim.py`.

Two changes landed:
1. **Smoke-guard:** canonical path NOT written when `smoke=True` (new parameter on `w5g2_pass_verification_and_result_authoring`; threaded from `run_gauntlet_sim`). Log message explicitly states "canonical path NOT overwritten" on smoke runs.
2. **Atomic-rename:** canonical write on full runs (`smoke=False`) uses temp file + `Path.replace()` — POSIX-atomic; prevents partial-write corruption.

Test `test_smoke_output_json_valid` updated to assert canonical path ABSENT on smoke run and validate timestamped output instead.

### W3 amendment

**Path:** `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` § "Behavioral Discipline Notes" — "Pytest-serialization (Discipline #19 reinforcement)" section.

Added rule: serialize pytest runs; wait for one to complete before firing next; single-invocation per verification step; `pytest -n auto` for parallel partitions within a single shell.

Operating-procedure skill (`reincarnated-gamora-operating-procedure/SKILL.md`) targeted for § 3.5c amendment but blocked by file-write permission policy on meta-repo skill files. AGENT_STATE.md capture is the seam-internal fallback per OP § 3.7 file-write constraint pattern.

Flag to KR: if project-wide Discipline #19 sub-operationalization (pytest-specific) is desired in engineering-disciplines.md, route a jack-ryan dispatch — gamora does not write engineering-disciplines.md directly.

### MIGRATION.md version

**§ v1.32** — W2 canonical-path smoke-guard + atomic-rename + W3 Discipline #19 OP amendment cross-reference.

### Test spot-check result

190 passed, 0 failed — single serial invocation (Discipline #19 self-applied):
- `tests/test_cycle13_wave5_gauntlet_sim.py` (includes updated smoke-guard test)
- `tests/test_cycle13_wave4_sim_cycling.py`
- `tests/test_cycle12_wave5_sim_combatant_integration.py`

### Commit SHA

`37f6fff` — pushed to `main` at `reincarnated-engine`.
