# J-S7: the D2 frontier tables, pinned by FILE digest (JOIN-1, RC-W4)

> **STATUS:** CURRENT. JOIN-1 charter v0.5 § 1 row **J-S7** (`gandalf/notes/2026-09-29-join-1-run-charter.md`): *"these files are GITIGNORED, so git cannot pin them; they are pinned by a committed manifest of FILE sha256s derived at launch."* Seat elrond, J0, 2026-10-01.
> **Machine-checkable manifest:** `J-S7-frontier-tables-2026-10-01.sha256`, in this directory and `shasum -c` compatible.
> **Scope:** the frontier TABLES only: the charter's three (`MonStats.txt`, `MonLvl.txt`, `Levels.txt`) **plus `DifficultyLevels.txt`, added on the conductor's instruction (gandalf, 2026-10-01)**. legolas's J4a formula leg uses it for F07 (difficulty resist penalty 0/−40/−100) and F13 (leech divisors 1/2/3). See `legolas/research/2026-10-01-join1-j4a-d2-ww-barb/README.md` Q12. **The frontier POINT** (which area and difficulty is a kit's home frontier) **is not pinned here.** It is commission C-12 / C-12b at J4.

## Digests: every one is a **FILE** digest (sha256 of the file's bytes as they sit on disk), not a ROWSET digest

| File (repo: `reincarnated-collaboration`) | Bytes | Lines | **FILE sha256** | git blob id (local = upstream @ pin) |
|---|---|---|---|---|
| `agentic_orchestration/research/datamine-acquisition/d2/raw/MonStats.txt` | 431,898 | 736 | **FILE** `973eedacd121f724f6dca1c7201750f6a4e60480c3d536ef5a9cb36853d38193` | `4cf7a87f9bb4108b9da7da6896404e92e64920be` ✓ |
| `agentic_orchestration/research/datamine-acquisition/d2/raw/MonLvl.txt` | 14,595 | 112 | **FILE** `7624abe33673f8bf4f243de141fb387a1d78f1192466ace49ac8b3c175fa4df8` | `b1dbc101278e17ef6c5076455e70a41e96fcd263` ✓ |
| `agentic_orchestration/research/datamine-acquisition/d2/raw/Levels.txt` | 66,476 | 139 | **FILE** `3163b66ea391b1e51a4ead54d7f3465d7fdc4fe6f3385f098826c9bb6cca837b` | `b3b93fd1dbf92f1d3881d9ecad75902ae70ef648` ✓ |
| `agentic_orchestration/research/datamine-acquisition/d2/raw/DifficultyLevels.txt` | 582 | 4 | **FILE** `aaa1a5d93df8c62707cf05308d82418ae7058ac1ac15ac768331f2abe440ff88` | `46e61f9865138081d5b33cd891fbeb8531db656a` ✓ |

**Derivation (re-runnable; nothing was retyped):**
```
cd ~/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2
(cd raw && shasum -a 256 MonStats.txt MonLvl.txt Levels.txt DifficultyLevels.txt) | sed 's#  #  raw/#' > J-S7-frontier-tables-2026-10-01.sha256
shasum -a 256 -c J-S7-frontier-tables-2026-10-01.sha256        # verify: four lines "OK"
```

**Provenance check, beyond the FILE digest.** For each file, `git hash-object raw/<file>` equals the blob id that GitHub reports for `code/d2_113_data/<file>` in `fabd/diablo2` at commit **`45112569deb9384738ccafe5c24ebbb71f41c7c9`** (`gh api repos/fabd/diablo2/contents/code/d2_113_data?ref=45112569…`, run 2026-10-01). The upstream sizes match too. So the local bytes **are** the pinned upstream commit's bytes, not merely bytes of the same size as the `MANIFEST.md` inventory. On-disk mtimes for the first three are 2026-07-21, the acquisition date in `MANIFEST.md`.

**`DifficultyLevels.txt`: how it reached `raw/`.** It was not part of the 2026-07-21 acquisition, so `MANIFEST.md`'s inventory still lists 34 files and `raw/` now holds 35. That inventory is legolas's acquisition record and is not edited here.
- legolas fetched the file for J4a from `https://raw.githubusercontent.com/fabd/diablo2/45112569deb9384738ccafe5c24ebbb71f41c7c9/code/d2_113_data/DifficultyLevels.txt` and recorded its sha256 in `legolas/research/2026-10-01-join1-j4a-d2-ww-barb/primary_rows.json` (`aaa1a5d9…ff88`).
- The bytes were in the session scratchpad. elrond copied them byte-for-byte (`cp -p`) into `raw/` on 2026-10-01 and derived the digest from the copy.
- The digest equals legolas's recorded value, and the file's git blob id equals the upstream blob at the pin. Grade: DATAMINED, D2 1.13 classic (not D2R: a named version skew; see `MANIFEST.md`).

**What breaks this pin:** any edit, re-fetch or re-encoding of the four files (line endings included). A `shasum -c` failure means the J-S7 substrate moved, which is a named finding under charter § 1. Never re-derive the manifest silently.

**Signed:** elrond, 2026-10-01.
