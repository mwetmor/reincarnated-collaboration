# JOIN-1 · J3b CLOSE-OUT evidence: the J3b rulebook of record `d5384b4b951092911cf75a05103987ab772f6343`

**gamora, 2026-10-08.**

**Prereg trail (engine):**
- `9bd4e840` (prereg);
- `a2a8099e` (AMENDMENT-1);
- `463342a2` (AMENDMENT-2: the channel energy charge per KIT pulse, KP-388), with its § 5 append (KP-390).

**Rulebook trail:**
- `9047b515`: L-01 (KP-356 (ii) refusal, frame-breakpoint, `acc_bound`), L-04 (lane floor + row 35), L-05 (lane ceiling);
- **`d5384b4b`**: A-2 row 36, `run.charge_per_tick` rebound to sealed × h, plus `charge_bound`.

Every run is courtesy-gated with engine HEAD = `d5384b4b`, fixed throughout. **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/j3b-record-<RUN>`.

**INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Visor alone), not 57 or 69.

## Certification of `d5384b4b` (defaults)

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| `golden-master/` | 7/7 FILE-equal (sha256 per grain); 0 JOIN draws; `n_outside` 0; `acc_bound` and `charge_bound` empty in 26/26 |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |
| `s47-nc8n/` | **RED exactly as predicted:** census differs `['run.charge_per_tick']`; path check GREEN on both children; one witness hit on the HEAD pid for that key |
| `info3_rulebook_diff_9047b515_d5384b4b.patch` | **INFO-3:** the rulebook diff is ONLY the row-36 form, its A-2 entry (plus the JSON comma after row 35) and `charge_bound`. So **L04-1, L05-1 and L05-2 at `9047b515` stand** (collab `5c0203328`) |

## Controls at `d5384b4b` (`controls/`; directions are paired totals, sign test reported only)

Every run below is **valid**: HEAD fixed, pinned, 25 cells, 0 foreign reads, join records pass, closure 0, **25/25 sim terminals**.

| Run | Verdict | Detail |
|---|---|---|
| ORACLE-TWIN@200 | valid | In-process child override; **reach, not GD-at-200 fidelity**; never the fixture or the GM |
| **NC-J3-L01-W** (world = kit = 200) | **PASS** | 7/7 ROWSET-equal to the twin; period == `tick_period_s(200)` on every row; `acc_bound` and `charge_bound` empty. Per-tick cost **0.96×** the 196 GM (1.215 vs 1.268 ms wall per G7 tick); Σ ticks 121,814 vs 117,695 |
| **NC-J3-L01-P = NC-J3-E-1** (world 300, kit 196, GD) | **PASS** | Period == `tick_period_s(300)` on every row; `acc_bound` {repr(196/300)}; **`charge_bound` {"9.408"} on all 400 `simulate_wave` calls**; row-32 calls per world tick 1.094 vs J-S8 1.708 (lower in 25/25). **The 300 % dry-out is cured** (it was 25/25 TruncatedSalt at `9047b515`). **Reported, not predicted:** survival 17/25 vs 20/25; Σ ticks 174,419 vs 117,695 (×1.48 on the finer clock); Σ intake 22.58 M vs 22.28 M (+1.3 %) |
| **NC-J3-L01-1** (frame-breakpoint, effective 156.8 at world 196) | **PASS** | Period bit-equal to J-S8; `acc_bound` {repr(156.8/196)}; `charge_bound` {"11.520000000000001"} on 400 calls; ticks 124,756 > 117,695 (23 up / 2 down, p 1.9e-5); leech per tick 0.391 < 0.454 (25/0). Outcomes are identical to the `9047b515` run: at world 196 no cell neared dry-out under either charge |
| **NC-J3-L04-2** (intake floor 90) | **PASS** (was NO VERDICT) | Law check 0 violations; first divergence 25/25; `pth_effective` 90.0 on every monster row below 90; intake 23.08 M > 22.28 M (sign p 0.108) |
| **NC-J3-RT** | **PASS** | 7/7 FILE-equal to J-S8 at `d5384b4b`, after the controls |

**Refusal controls** (form tests, `tests/test_join3b_levers.py`, green at `d5384b4b`): L01-K (`KitAboveWorldClock`); L04-3 (`OffenseFloorUnbuilt`); L04-4 (`SplitRecordRefused`); L05-3 (`FloorAboveCeiling`); two-lane floors (`BindRefused`); `UnknownLaneCaller`.

## For J3c (drax) and J4
- **J3c pins `d5384b4b951092911cf75a05103987ab772f6343`.** The port must mirror **row 36** (the charge per kit pulse) and **row 35** (the G1 floor record).
- **Until S-7 lands** in the KP-312 change set, the port **refuses `hits_per_tick < 1`**: that covers L01-1, L01-P, every kit < world comparison, and G-D4 @ X. L01-W at kit = world is port-safe.
- **J4 (INFO-2):** row 36 is the Warlord's resource law (Eye of Reckoning channel cost). Each joined kit needs its own.
