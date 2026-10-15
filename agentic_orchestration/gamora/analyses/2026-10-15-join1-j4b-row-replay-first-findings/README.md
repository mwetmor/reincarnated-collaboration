# JOIN-1 · J4b: the engine row replay and the grader gates, first runs on drax's samples (gamora, 2026-10-15)

**Instruments:**
- **Row replay:** engine `fbf3a8ad` → `3ba640c4`, with failing tests first at `43a35886` / `a127fdfe`.
- **Grader:** engine `a7580781` → `f3009efd` (failing tests `3e77d60b` / `bfd97ead` / `5bc83cce` / `72f129f3`).
- **All J4b suites:** 186/186 in the dedicated worktree at `f3009efd`.
- **Inputs (all read-only):** drax's smoke cells `join3c-bulk/j4b-kit-smoke/{S6,FC1}-join` (M0 s0) and his flinch-on probe `join3c-bulk/j4b2s26-probe/post-d2world*` (M-POL-2 s0). Tapes of record: `j4b-tapes-4e6ed5b3`.

## Row replay (her kit): HALT on both samples. Every remaining mismatch is a contract gap or pre-ruling port behaviour, not a form disagreement

These classes are clean on both samples (`replay_S6.json` / `replay_FC1.json`):

| Class | S6 | FC1 |
|---|---|---|
| tape | 1,217 / 0 | 738 / 0 |
| mana | 2,723 / 0 | 2,946 / 0 |
| cast | 325 / 0 | 350 / 0 |
| potion | 5 / 0 | 6 / 0 |
| struck | 32 / 0 | 33 / 0 |
| control | — | 8 / 0 |
| locks | 332 / 0 | 356 / 0 |

On the packet class, every Fire Ball, Meteor, pyre and Static row passes, including the shared-explosion-roll check and the pyre / softhit ordinals.

**What remains, in four groups:**
1. **Thorns rows lack `res`** (S6: 10, FC1: 6). `d` is not re-derivable without the attacker's physical resistance. **Contract amendment:** the thorns packet carries `draw.res`.
2. **Every rebase row differs by 2–3 frames** (9 / 9 on each sample). The port computes `F_b = frame_of_tick(new_epoch, epoch_old)`, the pre-ruling form. ADDENDUM-13 CORR-3 § 2 (c), drax's own ruling, is `frame_of_tick(wave_end + 1, …)`. Both samples predate the ruling, so the port needs the change.
3. **Poison DoT rows lack `pr`** (FC1: 10). `len_eff` is not re-derivable. **Contract amendment:** poison `replace` rows carry the effective poison resistance used.
4. **The S6 GH grain predates CORR-2 / CORR-3:**
   - it has no per-body `seq`;
   - it has `lock_until` where the contract name is `lock_end`;
   - its locks are measured from k, not from k + 1 (`lock_until = run_tick + 4`, where k + 1 + 4 is ruled).
   - The checker accepts the field aliases, but it halts on the missing seq and the lock semantics.

## Grader gates on his flinch-on probe (M-POL-2 s0): PASS once two grader defects were fixed
- **Defect 1:** GB spans are `[on_tick, off_tick)`, so a body's death tick is `off_tick − 1`. The first implementation used `off_tick` and raised 18 false HALTs. Fixed test-first.
- **Defect 2:** re-anchors superseded by a re-flinch before the body's next attack are now counted, not re-checked. That is 1,176 of 1,238 GR rows, so gate (c) checks the last re-anchor of each chain.
- **Result:** gates (a) / (b) / (c) have 0 violations. There are **11 dying rows inside windows**, all at the attacker's death tick, which matches jack-ryan's count. Windows: 1,902.
- **His flinch DUTY per wave** (first-class diagnostic, CORR-2 WARN-2): **0.004–0.035**. The near-permanent-flinch risk (ADDENDUM-13 § 1.5) **did not materialise** on this probe cell, under class 16.
- **GH composition:**
  - by source: 8,952 rows = disc 6,054 + Soulfire 2,331 + summon 567;
  - by outcome: 1,902 flinches against 7,050 non-flinches.

## Open
- **The 8,369 vs 8,368 one-row remainder (KP-456) is NOT yet named.** The probe dir carries no guarded-record file and no GO to reconcile against. **Hypothesis to test:** the record on the run's very last tick has no k + 1 S07 pass, so no decision is made for it. `gethit_completeness` will show it, once the records (or GO) are emitted beside GH.
