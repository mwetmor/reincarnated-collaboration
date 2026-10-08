# JOIN-1 · J3a: build evidence so far (KP-367 → KP-370)

gamora, 2026-10-08. **Engine commits, each ALONE:**

| Commit | What |
|---|---|
| `68186bde` | prereg AMENDMENT-1 (WARN-P1, INFO-P1, INFO-P3) |
| `80350db0` | instrument + fail-first tests (12 FAILED against `547ac177`) |
| **`47c5c94e`** | **rulebook** (tree `88ac456d…`): L-06 per lane, the crit streams, the lane walk, rows 32/33/34 |
| `1200ee19` | prereg AMENDMENT-2 (the decoded rule; M2 retired; `gd-judged` renamed `gd-decoded`) |

**The rulebook worktree is at `47c5c94e`.** `47c5c94e` landed before KP-369. **It committed no M2 value:** `gd-judged` refuses at bind for lack of pack rows. Its `m2_band` and `independent-proc` model are dispositioned in AMENDMENT-2 § 1.

## Results

**GM-0 at `47c5c94e`** (`GM-0/`, run under the C-9 courtesy gate):
- J-S8 7/7 ROWSET-equal; **all 7 grain FILEs byte-equal to the fixture**.
- TA-X equal; 26 records; tree ok; 0 hits.
- **0 JOIN-stream draws in 26/26 records** (`crit_counters.draws == {}`).
- Lane census: intake 43,790, summon 28,671, `None` 0.

**The LANE-0 prediction was false as written.**
- The census counts every `resolve_hit` call. G1 records only the emitter's recorded attempts (35,165 / 21,346).
- It is restated in AMENDMENT-2 § 5: `None` = 0, with the census equal to the parity profiler's sealed-caller counts.
- **Found here, before LANE-0 was run.**

**nc8k** (`s47-nc8k/`), as predicted:
- B′ RED;
- census differs exactly `['player_offense.PlayerOffense.crit_mult']`;
- path check GREEN;
- one witness fingerprint hit, on the HEAD pid, for that key only.

**§ 4.7 v4 at `47c5c94e`** (`s47v4/`, `s47v4.stdout.txt`): **NO VERDICT.** HEAD moved during the run (`47c5c94e` → `2318cd4b`, star-lord's pack v1 commits). It is re-run at the next quiet HEAD.

**Bulk:** `GM-0/{emission,records}` moved to `/Users/admin/Games/join3a-bulk-evidence/GM-0/`, with manifests.

---

## `pth-coupled` / `gd-decoded` (AMENDMENT-2/-3; KP-373/374)

**Engine commits, each ALONE:**

| Commit | What |
|---|---|
| `84cc0633` | AMENDMENT-3 |
| `f1d8fe38` | fail-first tests (5 FAILED against `47c5c94e`) |
| **`5655123c`** | **rulebook** (tree `facf986c…`) |
| `c850a0e7` | AMENDMENT-3 corrigendum 1 (level margins) |

**The rulebook worktree is at `5655123c`.**

**G-D1 and G-D2 (form level; `tests/test_join3a_crit.py`, 15/15 pass):**
- **G-D1(a), 57 %:** E = **1.0875983921933081** at DA 2770.09 and **1.207005003536779** at DA 2011.53. Bit-exact with legolas's `worked_example.py`.
- **G-D1(b), 69 %:** E = **1.1032876564667364** / **1.2405273953024458**. Bit-exact.
- PTH = 103.53680208248068 / 124.88782033303511, bit-exact.
- **G-D2:** `gd-decoded` refuses at bind with `GdDecodedValueAbsent`, because the pinned pack has no v2 rows. `gd-judged` is refused as "renamed gd-decoded". M2 survives only as `bracket_sealed_d100`, labelled contradicted.
- **The WARN-3 assertion holds:** no `p2m_*` crit, tier or E column is named in the rulebook.

**GM-0 at `5655123c`** (`GM-0-5655123c/`, under the courtesy gate):
- J-S8 7/7, **all 7 grain FILEs byte-equal**;
- 26 records, tree ok, 0 hits;
- **0 JOIN-stream draws** (26/26);
- **J3-INTAKE-ROLL tripwire `intake_pth_ge_100` = 0**, as predicted;
- lane `None` = 0.

**§ 4.7 v4:**
- My run at `5655123c` reads NO VERDICT, because HEAD moved under it (`5655123c` → `06d00fb6`, star-lord's MIGRATION). It is kept in `s47v4-5655123c/`.
- **The covering run is star-lord's:** ORACLE BYTE-IDENTICAL at the quiet HEAD `5655123c`, per conductor KP-374.

**Bulk:** `/Users/admin/Games/join3a-bulk-evidence/GM-0-5655123c/`.
