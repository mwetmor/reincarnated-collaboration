# Dispatch — 2026-07-08 — rocket — pilot precondition: catalog extension + feed dedup

**From:** knight-rider
**To:** rocket
**Approved by:** Matt (two-leg pilot process ratified 2026-07-08, "wholeheartedly agree"); commissioned via gandalf transmission `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
**Estimated effort:** ~2–4 h (two beats, one seam + one MIGRATION)
**Acceptance:** catalog carries ≥1 `escape_lane` room (+ `dense_cell`); MIGRATION.md hands the count/band contract to gamora; feed submits distinct `legendary_id`s only, guarded by a halt-loud byte-identity assert.

## Context

The 1800-candidate emission run was Matt-killed 2026-07-08 as **mis-instrumented**. The same-day forensic correction (§8 of `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md` — **§8 governs**) established the true mechanism: `season_emit ≡ 0 by construction`. The four-family gate is LIVE and correct (R4 flip 2026-07-07), but the fought encounter catalog (`endgame_encounter_catalog.py`) contains **zero `escape_lane` rooms** — F4's sole member shell. The criterion was registered in the judge (`_shell_result_passed`), but nobody ever added the room to the rotation. F4 = False for every kit → the four-family conjunction is unsatisfiable regardless of kit quality. The JUDGE was armed; the ROOM never landed.

This is the first of two precondition dispatches (rocket + gamora) that must land before the stratified re-fire pilot can fire. Your work makes the conjunction *reachable*; it does not fire any run.

Verified at authoring (this session): `grep escape_lane endgame_encounter_catalog.py` → 0 hits; `grep dense_cell` → 0 hits. Catalog is currently 18 encounters (`boss_with_adds ×3 · chokepoint_corridor ×3 · elite_pack ×4 · magic_pack ×3 · mini_boss ×1 · open_arena ×4`).

## Required reading before starting

- **Post-mortem §8** (governs): `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md` — §8.2 (zero escape_lane → season_emit≡0), §8.3 (dedup finding), §8.5 (revised pilot).
- **Commissioning transmission:** `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md` — Unit 1 (your unit) + the gandalf design rider on the per-family room roster.
- `src/reincarnated/simulation/gauntlet_sim.py:217-234` (escape_lane F4 criterion registration + density-verification note), `:264-274` (`_FAMILY_SHELLS`), `:875-881` (escape_lane KPM handling).
- `src/reincarnated/generation/season_generation_pipeline.py:1705-1726` (cell-grain contract comment + the unconditional-append feed).
- engineering-disciplines.md: **#1** (math-before-code), **#2 / #2-FF** (smoke + full-fire rider), **#11** (empirical inspection over comment-claims), **#12** (semantic-shift honesty).

## Math-before-code

- **Beat (a) escape_lane:** its F4 criterion (exit-within-window ≥0.80 + KPM band [60,150]) is ALREADY REGISTERED and density-verified against spawn arithmetic (`gauntlet_sim.py:217-234`; math note §4 falsifier named). This is a **wiring check, not a re-derivation** — the room's spawn/geometry parameters must match the arithmetic the registered criterion already assumes. Document that match; do NOT re-derive the band.
- **Beat (a) dense_cell:** an F1 member (F1 = `{dense_cell, chokepoint_corridor, magic_pack}`). It has NO existing band entry. Its band is gamora's to derive (per the w-alpha-6 methodology) — you supply the room + declare the band-key need in MIGRATION; you do not author the band.
- **Beat (b) dedup:** no math; it enforces the existing documented cell-grain contract (`:1710-1714`). The volume claim to verify empirically: submitted-config count drops from ~2,422 to the number of *distinct* legendary_ids (~20–70).

## Cross-seam contract change? (Principle 6 gate — completed by knight-rider at authoring)

**Beat (a): YES — cross-seam contract change (ADR-004 trigger).** Adding rooms moves the catalog from 18 → 19 or 20 encounters. The count invariant and band tables live in **gamora's seam**, guarded by **SIX count-guard sites across TWO files** (five in `gauntlet_sim.py` fire at import; one in `t4_sim_cycling.py` is a runtime guard):
- `gauntlet_sim.py`: `GAUNTLET_ENCOUNTER_COUNT_EXPECTED = 18` (`:109`); module-level asserts at `:667` and `:1884`; runtime check at `:1203`; `_W5G_ENCOUNTER_COUNT_EXPECTED = 18` (`:1871`).
- `t4_sim_cycling.py:617-620`: independent hard-coded `if encounter_count != 18: raise RuntimeError("... SC-6 substrate integrity failure")` — **a separate file, a RUNTIME guard** (won't trip on a bare import; only when the catalog-load path runs). The commissioning transmission named this (`t4_sim_cycling.py:620`); do not lose it.
- Band tables: `ENCOUNTER_COHORT_KPM_BAND` (`:323`), `SPATIAL_ENCOUNTER_KPM_BAND` (`:611`, with the keys=={"balanced"} assert at `:625`).

**You do NOT touch `gauntlet_sim.py`** (gamora's seam). You **write a MIGRATION.md** handing the contract to gamora (see Scope). This is the ADR-004 split KR owns; gamora's companion dispatch consumes it.

**Sequencing + expected transient:** rocket lands FIRST. The moment your catalog holds 20 encounters, `import gauntlet_sim` raises `AssertionError` (18≠20) — this breakage is **confined to gamora's seam** and is the expected hand-off window, resolved by gamora's consuming beat. Your OWN catalog smoke must **not** import `gauntlet_sim`; validate the catalog's structure standalone. Do NOT tag any milestone while the window is open; intermediate seam-prefixed tag only.

**Round-trip completion** for beat (a) is completed across the rocket+gamora pair and verified by gamora's gauntlet smoke (per-family verdicts emit, including F4/escape_lane + F1/dense_cell). State this in MIGRATION.md as the round-trip contract.

**Beat (b): NO cross-seam contract change.** The dedup changes the *volume* of configs submitted to the gauntlet; it adds/modifies/renames **no dict field** on any inter-seam fixture (season_emit shape unchanged; the result stays cell-grain by the existing `:1710` contract). Round-trip: not applicable — no cross-seam contract change in beat (b). The halt-loud byte-identity assert (below) is the safety, not a schema change.

## Scope

**Beat (a) — encounter-catalog extension** (`generation/endgame_encounter_catalog.py`):
- [ ] Add **≥1 `escape_lane` encounter (MANDATORY)** — parameters matching the registered F4 criterion's spawn arithmetic (wiring check per math note; cite the arithmetic).
- [ ] Add **≥1 `dense_cell` encounter (RECOMMENDED — F1 rigor parity)** — gandalf's design rider rules the per-family roster at Gate-1; dense_cell closes the emission-vs-pilot F1 rigor mismatch (§8.2: emission judges F1 without its hardest member).
- [ ] Write **MIGRATION.md** (`generation/` → `simulation/` boundary) declaring: shells added; new expected count (state exact N: 19 if escape_lane only, 20 with dense_cell); **all SIX count-guard sites gamora must update — five in `gauntlet_sim.py` (`:109`, `:667`, `:1203`, `:1871`, `:1884`) plus `t4_sim_cycling.py:617-620` (the runtime SC-6 guard — do NOT omit; it lives in a second file and fails only when the catalog-load path runs)**; band-key needs (escape_lane → wiring per existing registration; dense_cell → new band, gamora derives); and the round-trip contract (gamora's gauntlet smoke emits per-family verdicts over the extended catalog AND exercises the t4 catalog-load path).
- [ ] Catalog structure smoke (standalone; does NOT import gauntlet_sim).

**Beat (b) — feed dedup** (`generation/season_generation_pipeline.py:~1717`):
- [ ] Submit **distinct `legendary_id`s only** to `run_gauntlet_sim` (currently `all_configs.append(cfg)` is unconditional → ~100× redundant fights of the same cell-config).
- [ ] **MANDATORY halt-loud byte-identity assert:** before deduping, assert that all configs sharing a `legendary_id` are byte-identical. If `_build_legendary_config` leaks any sample-derived field, the `:1710-1714` contract comment lies — **die loud, do not certify quiet** (Discipline #11: comments are claims, not proof; we were just burned by a stale docstring at `w3_emission_driver.py:505`).
- [ ] Smoke: log line `[W5R.2] Submitting N ...` shows N = distinct-lid count (~20–70), not 2,422.

**Common:**
- [ ] Smoke-test passes (each beat)
- [ ] MIGRATION.md written (beat a) — affects gamora `gauntlet_sim.py`
- [ ] Round-trip smoke (beat a, completed via gamora) / not-applicable justified (beat b) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag (intermediate, seam-prefixed): e.g. `rocket/v-pilot-precond-catalog-dedup-1`

## Acceptance criteria

- [ ] `grep -c escape_lane src/reincarnated/generation/endgame_encounter_catalog.py` ≥ 1
- [ ] `grep -c dense_cell src/reincarnated/generation/endgame_encounter_catalog.py` ≥ 1 (if dense_cell included per Gate-1 roster ruling)
- [ ] Catalog structure smoke first-log-line names N encounters (19 or 20) and lists the new shell(s)
- [ ] Feed-dedup smoke: `[W5R.2] Submitting N ...` with N ≈ distinct-lid count (≪ 2,422)
- [ ] Halt-loud byte-identity assert present and exercised (a deliberate divergence injection trips it)
- [ ] MIGRATION.md handed to gamora, naming all SIX count-guard sites (five in `gauntlet_sim.py` + `t4_sim_cycling.py:617-620`) + band-key needs + round-trip contract
- [ ] Round-trip smoke: beat (a) round-trip completes across the rocket+gamora pair, verified by gamora's gauntlet smoke emitting per-family verdicts over the 20-encounter catalog. Beat (b): Round-trip not applicable — no cross-seam contract change (volume-only, no dict field touched).

## #2-FF pre-fire verification (eat our own cooking — this dispatch names its instruments)

- **Beat (a) instrument:** catalog structure smoke. **Pre-fire one-command check:** `grep -c escape_lane src/reincarnated/generation/endgame_encounter_catalog.py` returns ≥1 AFTER edit; first-log-line expectation: `catalog: N=20 encounters | shells include escape_lane, dense_cell`.
- **Beat (b) instrument:** the `[W5R.2] Submitting %d legendary configs` log line + the byte-identity assert. **Pre-fire expectation:** post-dedup N ∈ [~20, ~70]; assert fires loud on injected divergence.
- **Precondition state this dispatch stands on:** four-family gate LIVE (R4 flip 2026-07-07, `gauntlet_sim.py:1023-1026`); escape_lane criterion registered (`:217-234`); catalog currently 18 with zero escape_lane/dense_cell (verified this session).

## Out of scope (explicit non-goals)

- **Do NOT touch `gauntlet_sim.py`** or any file in `simulation/` — the count asserts + band tables are gamora's seam. Hand them over via MIGRATION.md.
- Do NOT fire any emission run of any size. This dispatch makes the conjunction reachable; it does not harvest.
- Do NOT re-derive the escape_lane band (registered + density-verified; wiring check only).
- Do NOT derive the dense_cell band (gamora's math-before-code beat).
- Do NOT change the season_emit result grain or any inter-seam dict field (dedup is volume-only).
- Flavor, resource_model, Glance — all out of scope (post-mortem §6 "out of scope for the pilot").

## Open questions for the agent to resolve (document your calls)

- Exact spawn/geometry parameters of the new escape_lane room such that its exit-window arithmetic satisfies the registered ≥0.80 criterion — cite the math-note arithmetic you matched against.
- Whether dense_cell lands in this dispatch (default: YES per gandalf rider + F1 rigor parity). If Gate-1 roster ruling drops it, N=19 and MIGRATION reflects escape_lane only.
- Whether `_build_legendary_config` leaks any sample-derived field (the byte-identity assert answers this empirically — if it trips, escalate; the cell-grain contract comment is then false and the pilot grain assumption needs review).

## References

- Post-mortem §8 (governs): `agentic_orchestration/gandalf/notes/2026-07-08-1800-run-postmortem-misinstrumented-emission-fire.md`
- Commissioning transmission (Unit 1): `agentic_orchestration/gandalf/notes/2026-07-08-kr-commissioning-transmission-pilot-preconditions.md`
- `gauntlet_sim.py:217-234, 264-274, 875-881` (escape_lane registration + family shells) — READ ONLY, gamora's seam
- `season_generation_pipeline.py:1705-1726` (cell-grain contract + unconditional feed)
- Discipline #2-FF proposal (in jack-ryan ratification queue): `agentic_orchestration/gandalf/notes/2026-07-08-discipline-2-amendment-full-fire-rider-proposal.md`
- Companion dispatch (gamora): `2026-07-08-gamora-pilot-precondition-f3-assertions-legii.md`
