# JOIN-1 · J2-E3 evidence: the binder, the golden master, the witness on emitter children

gamora, 2026-10-07. Conductor KP-329. This covers jack-ryan's E2b Gate-2 § 4 list (collab `5312a8852`), the E2c/E2e Gate-2 delta items (`f24a93b93`), and INFO-1 / INFO-5. **E3 is ready for Gate-2.**

## Engine commits (each ALONE, in A-9 order)

| commit | what |
|---|---|
| `6626f664` · `b5a01125` | the pre-E3 INSTRUMENT and FORMS commits (BLOCK-1, WARN-E2e-1, WARN-E2c-1); evidence in collab `ac6d565b6` |
| `fa3d0716` **E2d** | the JOIN hook (loader, provenance, per-pid record) · witness `install_recorder` · the runner (inert profile only). Fail-first 5F → 5 passed |
| (R-7) | sparse rulebook worktree `/Users/admin/Games/reincarnated-engine-join2-rb` (cone `src/join2_rulebook`, 108 KB), first at `fa3d0716`, then **`5779b342`** |
| `5779b342` **E3a** | `bind_oracle.py` (the binder) · `a2_table.json` (real class names + the ADDENDUM-E1 corrigenda; INFO-1, INFO-5) · the D-1 operand. Fail-first 6F → 6 passed |
| `e5aad629` **E3b** | instrument: the fingerprint classifier (E2d checker defect, below) · shallow witness closures · the `NO VERDICT` label carries its reason · NC-J2-8 with the binder of record · the P-J2-7 corpus script. Fail-first 5F → 5 passed |
| `4211bb8f` **E3c** | instrument: nested emitter wrappers described through their closures. Fail-first 1F → passes |

Every run below ran at engine HEAD **`4211bb8f`**, with the rulebook worktree at **`5779b342`** (tree OID `src/join2_rulebook` recorded in each `JOIN-PROVENANCE.json`). HEAD, the kc2 tree, and the instrument pin (tracked, clean, committed blob) were each checked at **both ends** and held. Disk stayed at ≥ 31 GiB free.

**Bulk per-pid records and emitted grains were moved out of the repo** to `/Users/admin/Games/join2-e3-bulk-evidence/<run>/` (643 MB). Each run's `bulk_manifest.json` pins every moved file by FILE sha256, and `emission_manifest.json` is the emitter's own manifest. Nothing was deleted.

## § 4 item 1–3 · ORACLE half under the witness (`oracle-witness/`): **PASS, as predicted**

- **J-S8:** 7/7 ROWSET-equal to `f82807fb`. This is witness inertness: the witness changes nothing in the fight.
- **Cells:** 25/25 reported, `foreign_reads = 0` in every cell.
- **Exact tree:** 1 emitter (ppid = launcher) + 25 cells; grid-exact; no extra, missing, duplicate or orphan pids.
- **Record hits:** 0. Every fingerprint is either equal to the sealed census or an emitter wrapper of a sealed kc2 object.
- **Ends:** HEAD fixed; instrument pinned.

## § 4 item 4 · coverage negative control (`oracle-witness-displace-W1-NULL-4/`): **RED, as predicted**

- **Tree RED:** `n_cells` 24 of 25; `missing` exactly `[('W1-NULL','4','0')]`; nothing unexpected; `tree_ok` false.
- **J-S8:** still 7/7. The displacer changes nothing in the fight.
- **Declared confound, also predicted:** each of the 25 recorded pids carries "customize module other than the pinned witness". The displacer is itself a sitecustomize.

## § 4 item 5 · THE GOLDEN MASTER, JOIN[warlord, GD] (`join-gd/`): **PASS, as predicted (P-J2-2)**

- **J-S8:** 7/7 ROWSET-equal to `f82807fb`, with the rulebook installed at GD. That **includes the D-1 binding**: the Soulfire period is ONE operand under RB-REPR-F32, bound to both oracle consumers. So **C-1(a) = R3-F32 through the rulebook, reproduced**. C-1(b) did not arise: no oracle edit.
- **A-10:** TA-X-07 / 20 / 29 / 30 reported beside the diff: all equal.
- **Cells:** 25/25, `foreign_reads = 0`.
- **Exact tree:** 26 `join-hook` records (1 emitter + 25 cells).
- **Bind log:** identical in every pid. It installs **13 rows**, plus rows 24/25 with the read-back `interval_s = 0x3fc99999a0000000`.
- **Record hits:** 0.
  - Every substituted symbol present in a cell is rulebook-owned, or an emitter wrapper of a rulebook object. In one cell checked by hand: `threat.mitigate`, `resolve_hit` and `physical_applied` are emitter-wrapper(rulebook); `applied_damage`, `applied_for`, row 16 and `soulfire_applied` are rulebook. **The forms ARE on the path.**
  - Every non-substituted symbol (e.g. `armour_branch`, `probability_to_hit`) is an emitter wrapper of a sealed kc2 object.
- **`JOIN-PROVENANCE.json`** carries: rulebook worktree / commit / tree OID, profile, A-2 digest, JOIN hook sha256, every per-pid record's sha256, and the env keys set. The emitter's `ORACLE` label on this emission is never quoted.

## § 4 item 6 · controls with the real binder (`s47-controls/`, § 4.7 v4)

| control | observed | as predicted |
|---|---|---|
| nc8f | census differs `['threat.resolve_hit']`; witness fingerprint hit | yes |
| nc8g | census differs `['threat.probability_to_hit']`; witness fingerprint hit | yes |
| nc8h (BLOCK-1) | census differs `['threat.mitigate']`; witness fingerprint hit | yes |
| **nc8a-rb** (NC-J2-8(a), binder of record under `reincarnated.simulation.join2_ctl`) | B′ RED: 22 path hits; census differs exactly **17** (the 15 substituted keys + `energy.SoulfireCostTerm.interval_s (default)` + `fixture.SOULFIRE_PERIOD_S`); witness fingerprint + path hits | yes |
| **nc8b-rb** (NC-J2-8(b), binder of record as `join2_rulebook`) | B′ RED: 22 path hits incl. names; census differs the same 17; witness name, import-event and fingerprint hits | yes |

## § 4.7 at `4211bb8f` (`s47v4/`): **ORACLE BYTE-IDENTICAL**

- HEAD fixed and instrument pinned.
- Limb A: `f04ef6d0…` equal.
- Limbs B and B′: pass.

## P-J2-7 at corpus level (`pj27_corpus.json`): **PASS**

- **J-S4b ROWSET:** `c96d8975ca4d5e0511174c2ba5d6560329b1e049749e49137f7f45ab592ad0e9`, recomputed under elrond's law.
- **Reader input:** reads `rdr_value` only. No conversion row is unstamped.
- **Reader result:** `eor_fire_to_physical_conversion_pct` = 100.0 → **Physical**, scope `eyeofreckoning1.dbr` via the declared `eor_` prefix. The Gutsmasher rows are not consulted.

## The E2d dry run (`e2d-join-inert/`) and a named checker defect

**What the predicted clauses showed:** every one held. J-S8 7/7, 25 cells with `foreign_reads = 0`, exact tree of 26 join-hook records, `bind_log []` identical, every rulebook file under the worktree.

**What the checker reported:** RED on 400 rows. **Cause:** the checker compared do-not-substitute fingerprints with the sealed census. But the J-S8 emitter **wraps 19 symbols in every cell**, so a cell's exit fingerprint of those symbols is the emitter's wrapper, in ORACLE and JOIN alike. **This is a checker defect, not a behaviour difference.** It was fixed in E3b by `classify()`, and the oracle-witness and join-gd predictions were amended before their runs.

**The offline re-check** (`recheck.json`) leaves 50 rows unresolved: `run.simulate_wave` and `threat.mitigate` × 25. Those two are double-wrapped by the emitter, and the E2d record format could not describe the inner layer. E3c fixed the format. Every E3 run above resolves them. The E2d run is kept, not re-labelled, and was **not** re-run, because its fight result was already 7/7.

## Owed / open

- **E4** (A-9): A-5 parity probes (call-count parity, read-back), the remaining controls (NC-J2-1…11b, A-13 equivalences) and per-site perturbations.
- **Port side (drax):** D1, then D2 under a KP-312 Matt ruling with the enumerated site list.
- **Ratification:** L-08 at J3; L-17 at J4b.
