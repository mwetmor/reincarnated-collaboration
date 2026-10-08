# JOIN-1 · P-J2-5 step 2: HALTED at the source pre-check (KP-364)

gamora, 2026-10-08. Prereg engine `756f1098`; instrument `410493bc`.

## Result: nothing computed

Lap O's library reads Grim Dawn **edition III** (2026-08-08) at fixed paths, and both are **absent** from disk:

- `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/database/database.arz`
- `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/resources/Text_EN.arc`

`/Users/admin/Games/vendor/` holds only edition II (2026-07-24) and edition IV (2026-09-29). The directory was last modified on 2026-10-01. The extra `.arz` at `/Users/admin/depots/219991/24346246/` is of unrecorded edition.

- **No edition was substituted** (GL-12; conductor KP-364: route, don't substitute).
- **S2-CAL-1 did not run,** so no verdict counts and no E_L exist yet.
- `s2_precheck.json` records the missing paths, the three library FILE sha256s and the table pin (OK).

## Routed to the conductor (for elrond / legolas)

Either **(a)** restore edition III at its path, or **(b)** rule which edition the library reads instead.

Under (b), S2-CAL-1 is exactly the check that detects drift: the library must reproduce Lap O's 2026-08-14 table on 74/74, or step 2 HALTs. Edition IV is newer than the sealed oracle's data, so a game-data change since 2026-08-08 would show there.

---

## Run of record on EDITION IV (conductor KP-366, option (b)): PASS, all CERTAIN

- **Instrument:** engine `20158959`. The edition is a recorded parameter (`--edition IV`), not a silent path swap.
  - Root: `/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929`.
  - Steam buildid `24825149`, checked against its appmanifest.
  - The closure reader's `E3` is rebound to edition IV before Lap O's libraries bind it. Lap O's library files are unchanged.
  - Every vendor file opened was recorded: only edition IV's, and **0 files of any other edition**.
- **Sealed kc2** was bound first.
- **Evidence:** `run-edition-IV/` (`s2_precheck.json`, `s2_cal.json`, `s2_apply.json`, `s2_child.log`).

| Check | Result |
|---|---|
| **S2-CAL-1, the drift gate:** Lap O's library at the table's own L, from edition IV, against the 2026-08-14 table | **74/74 within `B_row`; max \|Δ\| = 0.0** (bit-exact). Edition IV reproduces Lap O's table: no drift on these records |
| **S2-CAL-2, the level rule:** board `level` vs the table's `spawn_level` | same L on 35/74, and those reproduce within bound (as predicted). Different L on **39/74**, where table L − board L is 2 to 7 levels. **E_L = 130.368 DA** |
| **§ 3 on the unmeasured path pairs:** 122 pairs, 114 records (the 112 never tabled, plus 2 tabled at other waves only) | **CERTAIN 122 · UNDECIDED 0 · BELOW 0 · UNSOURCEABLE 0** |
| the tightest sourced body | `boss&quest/humanascendant_mindthief_01` @ w155: DA 2675.165, p 106.18; at DA + E_L, p 102.55 |
| margin | DA\* − (max sourced DA + E_L) = **91.7 DA** |
| **whole-path minimum p** (74 measured + 122 sourced) | **105.98**, on the measured `hero/springscrab_h01` @ w152 (unchanged from J2) |

**Verdict:** no BELOW, UNDECIDED or UNSOURCEABLE body is on the J-S8 path, so **this is not a Matt finding.** `HIT_CHANCE = 1.0` is now a theorem on **196/196** path pairs, robust to the level-rule error.

**What it rests on, stated:**
- Lap O's law and decomposition (step 1);
- edition IV's records, which reproduce edition III's table bit-exact on the 74;
- the level rule of record, L-RULE-B (board level), with its 39/74 disagreement carried as E_L.

**Next, per the prereg's § 4:** star-lord's sourced-DA pack member (provenance `SOURCED (step 2; L-RULE-B; E_L; edition IV)`), then the `OffenseHitUndecided` guard with NC-S2-G1. At GD on J-S8 the guard is predicted never to fire.
