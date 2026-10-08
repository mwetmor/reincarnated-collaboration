# JOIN-1 · J3b controls at rulebook `9047b515` (L-01 / L-04 / L-05): first pass, and the L-01 (ii) HALT

**gamora, 2026-10-08.**
- **Prereg:** engine `9bd4e840`, AMENDMENT-1 `a2a8099e`.
- **Instrument:** `gamora_join3b_controls_2026_10_08.py`, with fixes at `1ec7c776` (None-tolerant J-S8 compare) and `732b8d1f` (validity requires 25/25 sim terminals).
- **Rulebook `9047b515` is certified at defaults** (`../2026-10-08-join1-j3b-cert/`: P-J2-9 30/30; GM 7/7 FILE-equal, 0 draws, `n_outside` 0, `acc_bound` empty; § 4.7 v4 ORACLE BYTE-IDENTICAL). It is **NOT the J3b rulebook of record** (KP-388).
- **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/j3b-9047b515-<RUN>`.

**INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Visor alone), not 57 or 69.

## ⚑ FINDING → HALT (ruled KP-388): KP-356 (ii) coupled the Warlord's energy drain to the WORLD clock

**What happened.** At world AS 300, **ORACLE-TWIN@300, NC-J3-L01-W (world = kit = 300) and NC-J3-L01-P (world 300, kit 196) all end after wave 151 in 25/25 cells**, with `harness_error:TruncatedSalt` (the OBS-1 guard). The composition outcome is `dry_out`.

**Why.**
- The sealed drain is `cost · world_tps · factor` (PER_TICK, L-22): 14.4 per world tick at every AS, so 176.4/s at 196 and 270/s at 300.
- At kit = world this is the oracle's own law (the twin dries out too).
- At kit < world the Warlord pays per world tick while attacking at 196.

**Ruled (KP-388): a JOIN-only charge per KIT pulse** (engine AMENDMENT-2 `463342a2`).

**Two instrument notes:**
- At world 300 the frozen emitter writes one G4 row per cell with `n_bodies_in_disc = None` (tick 314). The b0n J-S8 summary then raised; ORACLE-TWIN@300 attempt 1 is kept in bulk (`j3b-ORACLE-TWIN@300-attempt1-compare-crash`). I worked around it in my script; the frozen harness is not edited.
- My first-pass screen read L01-W / L01-P as PASS: it caught `raised:*` but not `harness_error:*`. Fixed and declared at `732b8d1f`. **L01-W, L01-P and the twin are INVALID as control evidence.**

## Results under the `732b8d1f` validity screen

| Run | Verdict | Detail |
|---|---|---|
| ORACLE-TWIN@300 / NC-J3-L01-W / NC-J3-L01-P | **INVALID** (25/25 TruncatedSalt) | Their limbs were formally true on one truncated wave. They are re-designed or re-run under AMENDMENT-2 (L01-W at X = 200; L01-P under the per-kit-pulse charge) |
| NC-J3-L01-1 (frame-breakpoint, effective 156.8 at world 196) | PASS, **superseded** | Period bit-equal; `acc_bound` {156.8/196}; ticks 124,756 vs 117,695 (23 up / 2 down, p 1.9e-5); leech per tick 0.391 vs 0.454 (25/0). Charged per world tick, so it is re-run under the AMENDMENT-2 law |
| NC-J3-L04-1 (intake floor 5) | **PASS** | 7/7 FILE-equal (REACHED-INSENSITIVE), re-confirmed under the new screen |
| NC-J3-L04-2 (intake floor 90) | **NO VERDICT** (HEAD moved under it at `732b8d1f`) | Limbs held: law check 0 violations; first divergence 25/25; `pth_effective` 90.0 on every row below 90; intake paired total 23.08 M > 22.28 M (sign p 0.108). **Re-run at the record commit** |
| NC-J3-L05-1 (intake ceiling 95) | **PASS** | Law check 0 violations; first divergence 25/25. Intake paired total 22.24 M vs 22.28 M, reported (direction not predicted; sign p 0.035) |
| NC-J3-L05-2 (summon ceiling 95) | **PASS** | Law check 0 violations; first divergence 25/25; ticks paired total 119,111 > 117,695 (sign p 0.25) |
