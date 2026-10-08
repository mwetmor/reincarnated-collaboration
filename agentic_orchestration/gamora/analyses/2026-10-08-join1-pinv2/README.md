# JOIN-1: rulebook `5f7d62fd` (PACK_PIN → pack v2 + the 4 PACK-ONLY gd-decoded operands; KP-378), evidence

**gamora, 2026-10-08.** The rulebook worktree was at `5f7d62fd` (engine HEAD `5f7d62fd`, quiet) for every run here.

**PACK_PIN:**
- pack `kc2-rulebook-pack-v2`, digest `95e9c600de4eb215fae8547285e750bfae2de9fe1e492bcc89b29d15cb7ea73e`;
- manifest `c4760fde1a919f0a822db912c9f77777f93c7b70344a988b1f528e51d6b053b4`;
- `cut_commit 02bff63f`.

These were copied programmatically and asserted against star-lord's MIGRATION `0469d403`.

**`_FIELDS` +4 (PACK_ONLY, no ORACLE-CONST source):**
- `pth_roll_span_floor` (LAW, 100.0);
- `crit_damage_pct_eor` (KIT:warlord, 69.0);
- `crit_damage_pct_soulfire` (KIT:warlord, 57.0);
- `crit_model_player_stream_gd_decoded` (KIT:warlord, `"pth-coupled"`).

**INFO-V2-2:** the v2 pack dir and `export/kc2_rulebook_pack_v2.py` are in B′ `forbidden_dirs` and the witness `FORBIDDEN_DIRS` (engine `e124242f`).

| Dir / file | What | Result |
|---|---|---|
| `pj29.json` | P-J2-9 operand bit-equality | **30/30 bit-equal** (ORACLE-CONST + PACK); the PACK-ONLY rows equal their declared values; NC-E5-1..4 true |
| `golden-master/` | J-S8 golden master, profile `gd` | **7/7 ROWSET-equal and all 7 grain FILEs byte-equal** to the J-S8 fixture (sha256 per file). 25 cells, HEAD fixed, instrument pinned, no foreign reads, join records pass, 0 JOIN draws in 26/26 records, intake tripwire 0. Bulk is at `/Users/admin/Games/join3a-bulk-evidence/pinv2-golden-master-5f7d62fd` (`bulk_manifest.json`). |
| `s47v4/`, `s47v4.stdout.txt` | § 4.7 v4 | **ORACLE BYTE-IDENTICAL** (HEAD fixed; A, B and B′ pass) |

**INFO-V2-3:** the sealed referent's crit-damage constant `fixture.CRIT_DAMAGE_PCT` is **12** (the Warborn Visor alone; sealed `fixture.py:219`). It never fires, because CritLimb is LO. Any referent-vs-JOIN crit comparison must say the referent carries 12, not 57 or 69.

**Superseded as the rulebook of record by `615f886e`** (the G-D3 tally). See `../2026-10-08-join1-gd3/`.
