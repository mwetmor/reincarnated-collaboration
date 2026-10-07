# JOIN-1 · J2 · E5: the operand source moves from ORACLE-CONST to PACK (KP-338)

gamora, 2026-10-07. Design gate row J2-E5. The pack is star-lord's S1 `kc2-rulebook-pack-v0`:
- pack digest `974ff0925e02cceb…`;
- manifest `a5d80ab6…`;
- cut at `c5b72bbf`;
- loader `export/kc2_rulebook_pack_v0.py`, FILE `2e0307ff…`.

## Engine commits (each committed alone)

| Commit | What |
|---|---|
| `07ca39dc` (E5a) | **Instrument and predictions, before the switch.** Adds the P-J2-9 comparator and its run-of-record script (`gamora_join2_e5_pj29_2026_10_07.py`), and the fail-first tests (`tests/test_join2_e5_pack_source.py`): 5 of 6 FAILED against `a3eb0e54`. The comparator test passed, since it needs only `from_oracle`. |
| **`4da5044b` (E5b), rulebook commit** | Tree `50d62314…`. **The operand source of record becomes PACK.** `OperandSet.from_pack()` loads the S1 loader by file location, registers it in `sys.modules` before `exec_module`, and calls `load_operands(dir, config="JOIN", dataclass_factory=sealed_dataclass_factory)`. Pins in `operands.PACK_PIN`: loader FILE, pack digest and manifest FILE; any mismatch is refused. Only the 31 `_FIELDS` operands are read; the 14 design-listed pointers are not. `bind_oracle.install()` now defaults to `from_pack()`, and the first bind-log row records the operand source. **KP-337:** the CONTROL-ONLY, split-source label for `intake_order_override` lands in `operands.CONTROL_ONLY` and in the A-2 JSON (`control_only_operands` and row 4); a `with_()` on that operand is tagged "CONTROL-ONLY override". Tests: 124/124 J2 tests pass. |
| `7f80d3cd` (E5c) | **Instrument.** The JOIN hook's NON-GRADED-CONTROL specs now perturb the PACK OperandSet. |

**Rulebook worktree** `/Users/admin/Games/reincarnated-engine-join2-rb`: moved `a3eb0e54` → `4da5044b`, clean.

**Discipline #12 framing.** The source of the numbers changes. The numbers do not: P-J2-9 shows 31/31 bit-equal, and the golden master is FILE-equal.

## Results (every prediction committed at `07ca39dc` before the switch existed)

| Check | Prediction | Result |
|---|---|---|
| **P-J2-9** (`pj29.json`), run in the JOIN-shaped interpreter: `reincarnated` = sealed worktree; rulebook by file location from the worktree at `4da5044b` | 31 fields in each source, sets equal, **31/31 bit-equal**, layers equal, ORACLE-CONST provenance strings 31/31, sources ORACLE-CONST / PACK | **As predicted.** 31/31 bit-equal by typed canonical tree (f64 compared by bits; tuple ≠ list; mappingproxy ≠ dict; dataclasses by class and fields). Python `==` true on all 31; layers equal; 31/31 provenance strings carried verbatim |
| NC-E5-1: comparator sees one ulp | 30/31; unequal = `['oa_flat_tail']` | as predicted |
| NC-E5-2: loader with `config="ORACLE"` | refused before any row is read | as predicted (`RulebookPackRefused`, the A-12 message) |
| NC-E5-3: intact copy at another path, then a copy with one member byte changed | intact copy 31/31; changed copy refused on digest | as predicted. Intact: 31/31. Changed: refused at `rulebook/kit_warlord.json` |
| NC-E5-4: a loader that is not the pinned FILE (one appended line) | refused, naming the loader | as predicted |
| **JOIN[warlord, GD] at `4da5044b`**, engine HEAD `7f80d3cd` (`golden-master/`) | J-S8 7/7, TA-X equal, exact tree, 0 hits, first bind-log row = operand-source PACK `974ff092…`; every other row equals E4's | **As predicted, first-run pass (no recheck needed).** J-S8 7/7 ROWSET-equal; **all 7 grain FILEs byte-equal to the fixture**; TA-X-07/20/29/30 equal; 26 records, `tree_ok`, bind log identical across pids, 0 hits. Bind-log row 0 is `{kind: operand-source, source: PACK, pack_digest: 974ff092…, loader_sha256: 2e0307ff…, overridden: []}`, and rows 1–19 equal the E4 golden master's 19 rows exactly. A-2 digest is now `79592050…` (the label) |
| **§ 4.7 v4 at E5 HEAD `7f80d3cd`** (`s47v4/`, `s47v4.stdout.json`) | ORACLE BYTE-IDENTICAL; no ORACLE interpreter opens the pack or the S1 loader | **ORACLE BYTE-IDENTICAL.** HEAD and kc2 fixed at both ends; Limbs A / B / B′ pass; census differs `[]`; witness tree ok, 0 hits. The ORACLE children's open/load lists contain no `kc2-rulebook-pack-v0` path and no `kc2_rulebook_pack_v0` module |

## For drax: the re-pin

- **New rulebook commit:** `4da5044bef0d9498f2ee3522fe2d4dcf3657d1c5`, tree `50d6231452f4ac1c898b499378b63e6ff7e386b8` (supersedes `a3eb0e54` for the mirror).
- **What changed for a mirror:**
  - the operand **source** (values are bit-identical, per P-J2-9);
  - the CONTROL-ONLY label on `intake_order_override` (ADJ-6 already treats it as a control-only slot);
  - the A-2 JSON (new keys `operand_source` and `control_only_operands`, plus `control_only_operand` on row 4).
- **No form changed. No operand value changed.**
- Per the conductor, coordinate this as a delta at D2's Gate, not mid-D2.

## Evidence

The golden master's emission and witness records were moved with `os.rename` (nothing deleted) to `/Users/admin/Games/join2-e5-bulk-evidence/golden-master/`. The run directory keeps `bulk_manifest.json` (sha256 verified after the move) and `emission_manifest.json`.
