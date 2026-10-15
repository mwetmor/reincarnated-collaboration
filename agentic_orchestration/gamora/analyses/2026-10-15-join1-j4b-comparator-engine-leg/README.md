# JOIN-1 · J4b · comparator re-emission, ENGINE leg (gamora, 2026-10-15)

`JOIN[warlord, gd-decoded @ 196]` was re-emitted with the KP-386 instrument as committed, plus the additive GO sidecar (ADDENDUM-A CORRIGENDUM-1 § 2, CORRIGENDUM-2, and the conductor's 1e-9 gate on jack-ryan INFO-1/2/3, collab `390806fde`).
- **Worktree:** the dedicated one, `reincarnated-engine-j4b-cert`.
- **Bulk:** stays in `/Users/admin/Games/join3a-bulk-evidence/j4b-comparator-engine-leg/`. `bulk_sha256.txt` holds the digests.
- **Provenance:** no emission of her kit was read.

## (i) Instrument G1–G7 vs `4c30b0d64`: 7/7 ROWSET and 7/7 FILE sha256 EQUAL (`compare_vs_4c30b0d64.json`)
- **Run:** `gamora_join3a_gd3_2026_10_08.py emit`, at engine HEAD `9b98db4e`.
  - The instrument file is unchanged since KP-386.
  - Oracle `969fbd8d`; rulebook worktree `3eefaa2e`, the J3c pin, unmoved.
  - head_fixed true; instrument_pinned true; 25 cells; 0 foreign reads; join_records PASS.
- **`compare_vs_JS8.json` reports 6/7 FALSE vs J-S8. That is expected**, because the instrument's own PREDICTION says "7/7 vs J-S8 PREDICTED FALSE (crits move damage)". It is the KP-384 result, reproduced.

## (ii) The sidecar's G1–G7 equal the instrument's row for row on 25/25 cells, and the identity holds on 25/25 (`sidecar/sidecar_report.json`)
- **Sidecar:** engine `da29f39b`.
- **Identity, leech-reconciled:**
  - 0 off-ledger HP falls;
  - Σ applied = Σ (initial − REAL final HP) + Σ leech_heal_hp. The maximum relative residual is **5.3e-14**, against a 1e-9 gate;
  - the observed per-body heal equals the fold's telemetry;
  - the heal on bodies he never hit is 0.
- **The identity as CORRIGENDUM-1 registered it (no heal term) fails, as CORRIGENDUM-2 predicted.** It is reported and does not gate.
- **History, recorded rather than buried:** the first 25-cell sidecar run (`2bd18836`, set aside as `sidecar_at_2bd18836_superseded/` in bulk) failed the identity on W1-NULL s0 and s2, at relative residuals −6.9e-5 and −2.7e-4, with 0 chain breaks.
  - **Cause:** a body that survives the wave can keep leeching after its last hit. "Final HP" read as the last `hp_after` was the wrong measurement.
  - **Fix:** `da29f39b` reads the body's real final HP from the oracle's own state dict, through a pass-through observer on `MutatorFold.leech_heal`.
  - **Effect:** it was a measurement fix, not a semantic change. G1–G7 were unaffected; they were equal on both runs.
- **GO volume:** 324,563 rows. Families: physical (EoR disc) / lightning (Soulfire) / bleeding / summon.
- **His M-c (information, not a prediction):** Σ applied / Σ ticks = 4,292,184,298 / 113,051 = **37,966.8 per tick**. Without summons it is 37,961.7; the summons give 576,800 HP in total.

## (iii) PREREG-ADDENDUM-B input (`prereg_b.json`)
- **Instrument:** engine `d5a217ba`.
- **Reads:** his G7, GS and GO, plus `prereg_a.json` (collab `d11ce3a12`, unchanged).
- **The registered reading of last_arrival (the Mover.spawn_t_s schedule)** gives a median tail_share of 0.82–1.00 on every wave, so all 10 waves are KILL-LIMITED.
- **A measured-arrival reading (the latest first-hit tick over roster bodies)** gives 0.026–0.37, so only waves 159 and 160 are KILL-LIMITED.
- **The registration is in PREREG-ADDENDUM-B** (engine).
