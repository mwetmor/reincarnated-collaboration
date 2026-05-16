# Dispatch — 2026-05-16 — star-lord — Investigate Tier-1 column coverage gap

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 (after drax surfaced the coverage finding during v0.7.1 work)
**Status:** COMPLETE
**Estimated effort:** 1 session (~60-120 min depending on what the investigation surfaces)
**Acceptance:** Root cause identified; mitigation path proposed (with explicit math-before-code per Discipline #1); findings filed; if a code fix is the right answer, it's in scope to ship in the same session subject to standard smoke-test discipline.

## Context — the finding

Drax's v0.7.1 work (commit `68dfceb`, deploy `odfuct08x`) included a coverage assessment on the Tier-1 telemetry columns in `season_001005`. Numbers:

| Field | Population | Population fraction |
|---|---|---|
| Total fight rows | 1,541,700 | 100% |
| Rows with `duration_seconds` non-null | 52,800 | ~3.4% |
| Rows with `a_heals_received` non-null | 52,800 | ~3.4% |
| Rows with `a_potions_used` non-null | 52,800 | ~3.4% |
| (class × monster) pairs with any Tier-1 data | 120 / 242 | ~49.6% |

Drax's analysis: those 52,800 rows correspond to **the first 6 balance loop iterations only.** Coverage is sparse AND uneven (half the encounter pairs have nothing).

Operational consequence: drax pivoted v0.7's encounter-analytics projection from the *intended* `Damage × Time-to-Kill` back to `Damage × Win Rate` because Tier-1 data was too sparse for per-pair averaging. The viz is now stable but the intended-richer projection is blocked.

## What contradicts what

Your telemetry-tier1 dispatch (`2026-05-14-star-lord-telemetry-tier1.md`) completed 2026-05-16 with:

> **Smoke status: PASSED.** End-to-end verified: balance_loop produces fight_log entries with non-NULL `a_heals_received`, `a_potions_used`, `duration_seconds`; recorder persists them to an in-memory DB; columns present with correct REAL/INTEGER types.

So the verification path worked. But drax's empirical query on `data/telemetry.db` for season_001005 shows ~3% coverage. The verification didn't catch the gap.

Gamora's B10.4 Option 2 regen (commits `b15ecb2` + `540160c`, intermediate tag `gamora/v1.3-b10-4-option-2-impl`, milestone `v1.3-b10-4-swarm-calibration`) ran AFTER your telemetry-tier1 landed (`baa3bed` came before `b15ecb2` chronologically). So gamora's regen SHOULD have produced rows with Tier-1 populated. But drax's analysis suggests those new rows ALSO don't have the fields populated.

## Drax's leading hypothesis (worth testing, not assumed)

> "The fight sim apparently still doesn't write them."

In other words: there's a code path in `fight_engine.py` (or upstream in `balance_loop.py`) that is being exercised in production runs but does NOT write the Tier-1 fields. Your smoke test verified one path; the regen path may be a different one.

## What to do — math-before-code (Discipline #1)

This is a math-before-code investigation. Do NOT modify code until you have the empirical picture.

### Step 1 — Empirical: verify drax's coverage numbers

Query `data/telemetry.db` directly. Confirm:
- Total fight rows for season_001005
- Tier-1 column non-null counts
- WHICH balance_loop_iteration values are represented in the 52,800 rows (drax said "first 6 iterations only" — confirm)
- WHICH classes / monsters have Tier-1 data vs not

If drax's numbers reproduce, you have an authoritative finding. If they don't, that's data-freshness or query-divergence — different problem.

### Step 2 — Code-path inventory

Read every code path that writes to `class_fight_loadouts`. Specifically:
- `src/reincarnated/telemetry/recorder.py` — the `record_class_fight_loadouts` function
- All callers of that function in `src/reincarnated/`

For each caller, document:
- Where the fight_log dict comes from
- Whether the fight_log dict has the Tier-1 fields populated at that point
- Whether the fight_log fields propagate to the `class_fight_loadouts` INSERT correctly

The hypothesis to test: are there callers passing fight_log dicts that DON'T have Tier-1 fields, resulting in NULL writes? If so, where do those fight_log dicts originate?

### Step 3 — Cross-check with gamora's regen path

`balance_loop.py` has multiple code paths (recompose loop, convergence binary search, rejection gate). Trace which path produces fight_log entries that get written to `class_fight_loadouts` AND verify the Tier-1 fields are populated on the fight_log dict at the write moment.

If you find a path that produces fight_log dicts missing the Tier-1 fields, that's the root cause. If all paths produce them correctly, the root cause is elsewhere (e.g., a transactional issue, a recorder bug, a different writer, or the data being old).

### Step 4 — Reconcile vs the historical timeline

Per drax's analysis "those 52,800 rows come from the first 6 balance loop iterations only" — this implies the rows that DO have Tier-1 data are from an EARLIER regen, not gamora's recent Option 2 regen. Verify this with a query on row-creation timestamp or some other temporal signal in the DB. If true, the question becomes: why didn't gamora's Option 2 regen write Tier-1 data on the rows it touched?

### Step 5 — Propose mitigation

Once root cause is identified, propose a fix path:
- **(a)** Pure code fix — patch the path that bypasses Tier-1 writes, then a new regen produces clean data
- **(b)** Backfill — write a one-time migration script that re-computes Tier-1 fields for existing rows (probably impossible since the fight sim is the source of truth for those values — but worth naming as the rejected option with reasoning)
- **(c)** Schema-level fix — make Tier-1 fields NOT NULL with defaults, forcing the issue at insert time
- **(d)** Other path you surface during investigation

If the answer is (a) and the fix is small enough to ship in-session, ship it. Standard discipline: math note → code → smoke test → tag. Otherwise file findings and queue follow-on dispatch.

## Cross-seam considerations

- **Gamora's seam touch:** If the investigation surfaces a bug in `balance_loop.py` (which is gamora's), DO NOT modify `balance_loop.py` directly. File the finding; knight-rider authors a gamora dispatch for the code fix. You can investigate the code (read-only); the boundary is the write.
- **MIGRATION.md:** If a schema-level fix is the right answer, MIGRATION.md needs an entry per ADR-004.

## Out of scope

- The other telemetry gaps (`engine_version`, `seasonal_element_name`, `convergence_wall_time_seconds`) — these are pre-existing flagged items requiring Matt approval per ADR-006. This dispatch is Tier-1 only.
- A full regen of any season. Investigation only; regens get authorized separately.
- Any drax-side change. Drax has already shipped the v0.7 viz fallback (Damage × WR projection). When the Tier-1 fix lands, drax authors a follow-on dispatch to update the encounter_analytics generation + switch projection.

## Required reading

- `agentic_orchestration/dispatches/2026-05-14-star-lord-telemetry-tier1.md` (your own dispatch + completion record)
- `src/reincarnated/telemetry/recorder.py`
- `src/reincarnated/telemetry/migrations.py` (V2.0 entry)
- `src/reincarnated/simulation/balance_loop.py` (gamora's seam — read-only)
- `src/reincarnated/simulation/fight_engine.py` (gamora's seam — read-only)
- `src/reincarnated/simulation/fight_result.py` (gamora's seam — read-only)
- Drax's v0.7.1 completion record (commit message of `68dfceb` + AGENT_STATE.md update from drax's recent session)
- `agentic_orchestration/skill_handoff_2026-05-16.md` § cross-seam items for context
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #11 (attribution), #12 (semantic shifting)

## Acceptance criteria

- [ ] Empirical reproduction of drax's coverage numbers (or correction with new authoritative figures)
- [ ] Code-path inventory documenting where `class_fight_loadouts` writes happen and which paths populate Tier-1
- [ ] Root cause identified with named diagnostic evidence
- [ ] Mitigation proposed with rationale; if shipping in-session, smoke-tested + tagged + MIGRATION.md if cross-seam
- [ ] Findings filed at `agentic_orchestration/qa/findings/2026-05-16-star-lord-tier1-coverage-rootcause.md`
- [ ] Knight-rider notified at completion with root cause + mitigation status

---

## Completion record

**Completed:** 2026-05-16  
**Findings file:** `agentic_orchestration/qa/findings/2026-05-16-star-lord-tier1-coverage-rootcause.md`  
**Root cause:** Two data-timing factors, NO code bug. (1) 1,488,900 rows are pre-V2.0-migration → NULL columns expected, unfixable without regen. (2) B10.4 Option 2 regen generated 10 classes (not 11) for seed 1005 due to CLASS_COUNT_RANGE RNG variance; class_0011 simply wasn't in that run. All 52,800 post-migration rows correctly have Tier-1 data. Drax's "fight sim doesn't write them" hypothesis is incorrect.  
**Mitigation shipped (yes/no):** No — code is correct, no fix needed. Mitigation path is next authorized full regen; findings file recommends passing n_classes=11 explicitly.  
**Tag (if any):** None (no code changes)  
**Notes for knight-rider:** The 3.4% Tier-1 coverage is a data-timing artifact. Code is correct across all three write paths (balance_loop, recorder, orchestrator). The intended `Damage × Time-to-Kill` encounter analytics projection in drax remains blocked on a full regen. Recommend Matt authorize a full regen for season_001005 with n_classes=11 to populate complete Tier-1 data. Until then, drax's fallback viz (Damage × Win Rate) is correct. No gamora dispatch needed — no code bug in gamora's seam found.
