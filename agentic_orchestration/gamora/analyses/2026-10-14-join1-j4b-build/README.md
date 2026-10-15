# JOIN-1 · J4b BUILD (engine side): `join2_rulebook/d2/`, grids, tables, certification

**Engine commits, in order:**
- `c9a6cd47` ADDENDUM-10 (design of record);
- `ced19966` the build prereg;
- `1829ecd8` fail-first, 29 RED;
- `ec5a8ed7` the d2 rulebook, 29 / 29 GREEN;
- `0c30456f` → `4d5d4611` the `hero` alias (fail-first, then code);
- `270407d7` the grids instrument;
- `9de6f9ad` ADDENDUM-11 (tier chain);
- `55882da1` → `84f5498f` the tier chain (fail-first, then code);
- `15890543` the grids patch;
- **`833fee62` the table emitter: the certified HEAD.**

Each is committed alone, and none is pushed. The kc2 tree OID is `7496a28a` throughout, and `join2_rulebook/__init__.py` is unchanged: `d2/` is loaded by no existing path.

| File | What |
|---|---|
| `grids.json` | the prereg § 4 grids at `833fee62`: **ALL PASS, every negative control RED** |
| `tables/` | the bind-time tables at `833fee62`, plus `manifest.json` (input and output sha256; HEAD and kc2 bound at both ends). Re-emitted byte-identical on a second run |
| `pj29.json` | P-J2-9 at `833fee62` |
| `golden-master/`, `golden-master.stdout.txt` | GM 7/7 (JOIN[Warlord]) at `833fee62`. The emission and records are in bulk `/Users/admin/Games/join3a-bulk-evidence/j4b-build-golden-master-833fee62/` (`bulk_manifest.json`: 34 files, sha256) |
| `s47v4/`, `s47v4.stdout.txt` | § 4.7 v4 at `833fee62`, run from the dedicated worktree `reincarnated-engine-j4b-cert` |
| `s47v4-attempt1-no-verdict-head-moved/` | attempt 1, run from the main repo: **NO VERDICT** because main's HEAD moved during the run (`833fee62` → `216bf806`, a concurrent commit). The instrument refused correctly |

## Grids (`grids.json`)

| Grid | Rows | Result |
|---|---|---|
| G-LVL (Fire Ball / Meteor / Fire Bolt mana, min, max; pyre bit rate and frames; Fire Mastery; Warmth; slvl 1–60, against legolas `primary_rows.json`) | 600 | 0 bad; NC RED |
| G-H1-C13 (279 rolled + 108 caster + 3 null refusals + 186 unique / ES) | 576 | 0 bad; NC RED |
| G-H1-C14 (FA primary, 372 rolled; unique / ES checked against stage-3 per-attack rows AND its summaries, 54 / 64) | 372 | 0 bad; summaries reproduced; NC RED |
| G-FREEZE (stage-4 rounding table) | 22 | 0 bad; NC RED |
| G-SKILLS-TXT (every transcribed parameter against 1.13 Skills.txt) | 85 cells | 0 bad |
| G-REGEN | 5 | 0 bad (base refill 3,003 frames ≈ 120.1 s) |
| G-TIME (frame ↔ tick, m = 1…20,000) | 20,000 | 0 bad |
| G-ABS-DOT | 1 | pass |
| G-REFUSE (AttackerTierUnresolved, IntakeFamilyUnmapped, ControlFamilyUnmapped, DotFamilyUnmapped, PortOnlyKit) | 5 | all refuse |

## Tables (`tables/manifest.json`)
- **`anchor_ar_eq_table.json`:** boss / nemesis on unique + Extra Strong, the JUDGED UPPER ARM.
- **`anchor_ar_eq_table_unique.json`:** the plain-unique companion.
- **Coverage:** roster 507 (with the pool lift) + pets 68, × w151–160 = **5,750 rows**. The ECDF is weighted on **P′ = 243** (step-2b P minus its 5 depth-2 pets).
- **Tiers, by the ADDENDUM-11 chain:** step 1: 91; step 2: 121; step 3: 349; step 4: 6; step 5: 8.
  - Totals: trash 188, champion-hero 311, boss 57, nemesis 19.
  - P′ tiers: trash 108, champion-hero 111, boss 20, nemesis 4.
- **Construction marginal on P′ at the FA Defence (3,017, clvl 99):**
  - trash: **52 [49–59] (40–72)**, equal to stage 3's D2 target 52 [49–59] (40–72);
  - champion-hero: 61 (51–78);
  - boss upper / unique: 64 / 52;
  - nemesis upper / unique: 71 / 62.
- **`physical_contact_table.json`,** keyed `record|slot|skill`: 2,187 slots, **800 contact** (swing 521, Physical 270, Pierce 9), Pierce-only 13, Bleeding-only 0. Every slot's skill class is joined by skill path; 0 unmatched.

## Certification at `833fee62`

| Check | Result |
|---|---|
| **P-J2-9** | **30 / 30 bit-equal** (sources ORACLE-CONST and PACK); NC-E5-1…4 pass |
| **GM 7/7** (JOIN[Warlord], `gamora_join2_e3_run … join gd`) | **G1–G7 all true**: 25 cells, head fixed, instrument pinned, 0 foreign reads, 26 JOIN records with an identical bind log; `rulebook_commit` 833fee62 in the provenance |
| **§ 4.7 v4** | **ORACLE BYTE-IDENTICAL**: "HEAD fixed; A and B and B' pass" (attempt 2, dedicated worktree) |

**How the rulebook worktree was used:**
- For GM, the shared rulebook worktree `reincarnated-engine-join2-rb` was checked out at `833fee62` from about 23:15 to 23:22 EDT.
- It was **restored to the J3c pin `3eefaa2e` at 2026-10-15T03:22:53Z** and is clean.
- From now on, J4b checks run in the dedicated worktree `/Users/admin/Games/reincarnated-engine-j4b-cert` (conductor instruction), never in the shared pin.

**Not in this build:** the B0-N numeric re-run, which needs pack v4 and the re-minted J-S4b.
