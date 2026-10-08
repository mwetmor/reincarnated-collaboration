# Finding — 2026-10-08 — JOIN-1 J3a rulebook delta (guard → PACK_PIN v2 → tally → AMENDMENT-4), Gate-2, and KP-379

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: drax may re-pin at `ea28195a`; the KP-379 population must be widened before sourcing)
**Target:** engine `e124242f`, `cf1a3ef9`, `77ef4962`, `5f7d62fd`, `3627ab62`, `3653a70c`, `615f886e`, `06d6db42`, `baec5c0d`, `ea28195a` (MIGRATION `15bf0b6d`); collab `ac39190d2`, `1a467f8f6`, `d8838a895`, `cee0a5a56`
**Developer:** gamora · conductor gandalf (KP-379)
**Principles applied:** 1, 2, 3, 5 · Disciplines #10, #12

## (1) Certification: HOLDS for every rulebook commit

| Rulebook commit | P-J2-9 | GM | § 4.7 v4 (HEAD start = end, kc2 tree `7496a28a` unchanged) | Evidence |
|---|---|---|---|---|
| `cf1a3ef9` guard + v1 re-cut | 30/30 | 7/7 FILE-equal (run 1's instrument defect kept, not quoted) | BYTE-IDENTICAL at `cc875bb9` (later instrument-only commit; rulebook worktree `cf1a3ef9`) | `ac39190d2` |
| `5f7d62fd` PACK_PIN v2 + 4 `_FIELDS` | 30/30 | 7/7 | BYTE-IDENTICAL at `5f7d62fd` | `1a467f8f6` (not on the conductor's list; it exists and passes) |
| `615f886e` tier tally | 30/30 | 7/7, 0 JOIN draws, tripwire 0 | BYTE-IDENTICAL, start = end = `615f886e` | `d8838a895` |
| `ea28195a` AMENDMENT-4 counters + anchor | 30/30 | 7/7, `row33_stash_mismatch` 0 | BYTE-IDENTICAL, start = end = `ea28195a` | `cee0a5a56` |

- The remaining commits (`e124242f`, `77ef4962`, `3627ab62`, `3653a70c`, `06d6db42`, `baec5c0d`, `15bf0b6d`) are instrument, test or doc changes. Each lies before a certified rulebook HEAD.
- `git diff c850a0e7 15bf0b6d -- src/reincarnated/simulation/kc2` is **empty**. Oracle exposure: none.

## (2) G-D4 reading: SOUND, with two conditions (INFO-1)

- KP-356 sets X = max(kit AS, 196). With no joined kit, the G-D4 baseline **is** `gd-decoded @ 196`, in the same configuration and on the same clock. A separate emission would be byte-redundant.
- **Condition 1:** the row of record is the **post-sourcing G-D3 re-run (25/25 unrefused)**, not `d8838a895`. That emission has a 4/25 hole.
- **Condition 2:** re-emit at any rulebook move that touches the `gd-decoded` path, and at X > 196 when a faster kit is named (J3b).

## (3) D-1 and D-4 reported FALSE, not re-scored: CORRECT. Anchor fix: ADEQUATE (INFO-2)

- Both predictions are false as preregistered, and are reported that way with their causes: refusals plus the `id()` anchor for D-1; 17/25 against ≥ 20 for D-4. Re-scoring after the fact is exactly what a prereg forbids.
- **Note on D-4:** the 4 refused cells stop early, so they count as "fewer ticks" trivially (17 − 13 = 4). Reporting **13/21** beside 17/25 is the honest figure, and she does.
- **The fix.** `note_sf_rows` holds a weakref per instance. Its callback retires the last count at dealloc, before the id can be freed for reuse. This is sound under CPython refcounting and gc, and `SecondaryStreams` has a `__dict__`, so it supports weakrefs.
- **The test discriminates:** `baec5c0d` asserts that id reuse actually occurred (`len(ids) < 200`) **and** that the totals match.
- **Validation owed:** D-1 is re-tested as a fresh prediction on the G-D3 re-run.

## (4) KP-379 population: WRONG AS WORDED (WARN-1)

**The body that refused is not in the line-up roster.**
- `records/creatures/enemies/ghost_a01_summon.dbr` does not occur in `referent_lineup.py` or its CSV.
- It is a **monster-spawned pet**: `pm2_tg2_pet_chain.csv` rows 70, 114 and 115 show it spawned by Ilgorr's `ilgorr_ghostgenerator` and Grum's `skeletalgolem_summonghosts01`, among others.
- So "every (record, wave) the line-up can spawn" would source everything **except** the bodies that refused.

**Ruled population:** the line-up roster (pins plus every alternative's roster minus footage absences, w151–160), **unioned with its transitive pet closure** from `pm2_tg2_pet_chain.csv`, at the parent's wave.

**What escapes and what does not:**
- **Waves > 160 do not escape:** every G-D3 terminal row reads wave 160 (`survived_window` / `player_death`).
- **Also verify:** whether any body can be struck at a wave other than the one it spawned in (carry-over or deferred arrival). If it can, key coverage on every wave the body can be alive in.
- **Required:** a **closure test**. Count the bodies the guard actually looks up in a `gd-decoded` run that fall outside the sourced set; it must read 0. This replaces any argument from enumeration.

## (5) Survival 13/21 vs 16/21: HONEST (INFO-3)

- There are 6 discordant pairs (5 survived → died, 1 died → survived). The exact sign test gives p = 2·7/64 = **0.219**. It is stated as not significant, and the referent's crit constant (12) is disclosed.
- **Wording:** "buys no measurable survival gain" should read **"no detectable gain at n = 21 (6 discordant pairs; low power); the observed direction is adverse"**. A non-significant result is not evidence of no effect.
- The 4 refused cells are excluded non-randomly: they are exactly the trajectories that reached the pet. Say so.

## Action
- [ ] conductor: amend KP-379's population to roster ∪ transitive pet closure, plus the closure test (WARN-1).
- [ ] gamora: re-run G-D3 after sourcing, with D-1 as a fresh prediction; that run is the G-D4 row of record (INFO-1, INFO-2). Fix the survival wording (INFO-3).
- [ ] drax: re-pin at `ea28195a` may proceed.
- [ ] Matt: none.

## References
- engine `src/join2_rulebook/{crit.py, forms.py}` at `ea28195a`; `tests/test_join3a_crit.py` at `baec5c0d`
- `src/reincarnated/simulation/kc2/referent_lineup.py` (read-only); `data/kc2/pm2_tg2_pet_chain.csv` (rows 70, 114, 115)
- engine `3627ab62` § 5; collab `agentic_orchestration/gamora/analyses/2026-10-08-join1-{guard,pinv2,gd3,amd4}/`
