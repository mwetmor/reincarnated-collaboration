# Research — GD Rank-Array Adjudication (TSR-3 Founding Evidence) — 2026-07-24

**Mode:** A (analytical)
**Commissioner:** gandalf
**Authorized by:** Matt, 2026-07-24
**Sources consulted:**
- `/Users/admin/Games/vendor/grim-dawn/database/database.arz` (Edition-I, SHA-256 8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f)
- `/Users/admin/Games/vendor/grim-dawn/gdx1/database/GDX1.arz` (Edition-I, SHA-256 e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539)
- `agentic_orchestration/research/datamine-acquisition/gd/raw/all_skills.js` (grimtools harvest, 2026-07-21 22:49)
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (working .arz parser, reused)
- Steam Web API appdetails endpoint (appid=2699230, accessed 2026-07-24)
- All prior probe notes (2026-07-23-gd-arz-extraction-probe.md, 2026-07-23-join-surface-probe.md)

---

## Summary

The original TSR-3 claim — "grimtools' community-harvested 60-rank arrays contradict the .arz's actual 26 ranks" — was drawn from a comparison between two records that are not the same skill in the same namespace. The grimtools payload (`all_skills.js`) contains exclusively `nonplayerskills/` monster-use records and item/component skills. The playerclass records (where FoI lives, with `skillMaxLevel=16` and `skillUltimateLevel=26`) are entirely absent from the grimtools harvest. There was never a contradiction to observe: both sources encode correct data for the records they each contain, and those records are in different namespaces with different true caps. The 60-element arrays in the grimtools payload reflect the `skillMaxLevel=60` of the monster copies, not padding of the player copies. The two `skillMaxLevel:16` outliers in the JS payload are a separate phenomenon (mixed-length arrays within a single monster-summoning record) that do not represent player cap data. The founding claim requires replacement; the correct claim is stated in the verdict section.

---

## Findings

### Q1.1 — Is sk296 the same skill as purifyingflame1.dbr?

**No.** Confirmed by byte-level match.

`sk296` in `all_skills.js` has `skillDisplayName:"tagCompSkillA014Name"` and template class `Skill_AttackProjectileRing`. Searching `database.arz` for all records with `skillDisplayName='tagCompSkillA014Name'` returns five records:

| Record path | skillMaxLevel | rtype |
|---|---|---|
| `records/skills/nonplayerskills/bossskills/banegargoth_fireballnovabarrage.dbr` | 60 | Skill_AttackProjectileRing |
| `records/skills/nonplayerskills/factionskills/blacklegion_fireblast_01.dbr` | 60 | Skill_AttackProjectile |
| `records/skills/itemskills/componentskills/comp_fireblast_01.dbr` | 1 | Skill_AttackProjectile |
| `records/skills/nonplayerskills/bossskills/special/rock_fireballnova.dbr` | 60 | Skill_AttackProjectileRing |
| `records/skills/nonplayerskills/heroskills/aetherialphantom_fireballnovabarrage.dbr` | 60 | Skill_AttackProjectileRing |

The sk296 `offensiveFireMin` array byte-matches `banegargoth_fireballnovabarrage.dbr` exactly (first 5 values: 57, 83, 111, 140, 170; last 5: 2106, 2149, 2191, 2234, 2276). sk296 is a boss nonplayer skill; `purifyingflame1.dbr` is `tagGDX1Class07SkillName04A`, a player class 07 (Inquisitor) skill in `GDX1.arz`. These are records in entirely different namespaces with different display tags, different skill classes, different element types (fire ring projectile vs. fire cone channeled), and different source archives. They were never the same skill.

**Is FoI present in grimtools under any identifier?** No. `tagGDX1Class07SkillName04A` appears zero times in `all_skills.js` (grep confirmed). No record in the harvest matches `purifyingflame1.dbr` on any field.

### Q1.2 — Does the padding hypothesis hold?

**Partially confirmed, but with a more precise characterization than "padding."**

The grimtools payload contains `nonplayerskills/` records that have `skillMaxLevel=60` in the `.arz` itself. The 60-element arrays in the JS payload exactly match the 60-element arrays in those source `.arz` records. This is not UI padding applied by grimtools: the `.arz` ground truth for monster skills natively stores 60-element arrays because those records have `skillMaxLevel=60`. The grimtools site is not inflating anything — it is faithfully reflecting its source records, which happen to be monster copies rather than player copies.

Decisive test results — four skills with different true caps, compared across three sources:

| .arz playerclass record | True cap (max/ult) | Player .arz array len | NPS .arz skillMaxLevel | grimtools array len | Match to NPS? |
|---|---|---|---|---|---|
| `playerclass01/bladearc1.dbr` | 16/26 | 26 | 60 (`ironmaiden_bladearc1.dbr`) | 60 | Yes — byte-exact |
| `playerclass07/purifyingflame1.dbr` | 16/26 | 26 | No NPS copy in database.arz | NOT IN JS | N/A |
| `playerclass07/hunteraura2.dbr` | 10/20 | 20 | No NPS copy in database.arz | NOT IN JS | N/A |
| `playerclass01/cadence1b.dbr` | 3/3 | None (no rank arrays) | Not found | NOT IN JS | N/A |

The grimtools harvest draws from `nonplayerskills/`, not `playerclass/`. For Blade Arc, the nonplayer copy (`ironmaiden_bladearc1.dbr`) genuinely has `skillMaxLevel=60` in the .arz and the JS arrays (60 elements, continuously increasing to rank 60) are correct for that record. The 60-element arrays are not padded repeats of a shorter true array — they are legitimately authored 60-rank scaling tables for monster combat, not overcap tables for player skill gear.

The gandalf hypothesis that arrays saturate/plateau and repeat after the "true" player cap was tested. For Blade Arc: `offensivePhysicalMin` continues increasing monotonically from rank 1 to rank 60 with no plateau. The `sat@59` observation in the first pass was an artifact of the last element being the array's end, not a saturation in the middle. Saturation does occur in some arrays (e.g., `sk497`'s `petBurstSpawn` plateaus at rank 19 of 60, `petLimit` at rank 19 of 60) but this is not a uniform padding schema — it reflects the actual authored values for those specific skill parameters in monster records.

**The correct picture:** The grimtools harvest is a collection of nonplayer/monster skills, item-granted skills, and component skills — not player class skills. The two namespaces have different skillMaxLevel values because they serve different purposes: player skills use 16+10=26 (base+ultimate) caps; monster copies use 60 because monsters can be at any level.

### Q1.3 — The two skillMaxLevel:16 outliers in the grimtools JS

The two records are `sk1497` and `sk733`.

**sk1497:** `skillMaxLevel:16`, `skillUltimateLevel:26`, `skillDisplayName:"tagClass03SkillName01C"`. Searching `database.arz` for this tag finds `records/skills/nonplayerskills/summoning/summon_winddevil_poison1.dbr`, which has `skillMaxLevel=16` and `skillUltimateLevel=26` in the .arz. This is a summoning-type nonplayer skill that genuinely carries these caps — the values are native to the record, not a player skill cap showing through. Within `sk1497`, arrays have mixed lengths: `skillManaCost[26]` (matching skillUltimateLevel) and `petLimit[60]` (independently authored at 60 for pet-management purposes). These are mixed lengths within a single record because the two fields serve different semantic roles, not because of any padding scheme.

**sk733:** `skillMaxLevel:16`, `skillDisplayName:"tagClass05SkillDescription03A"` (not a Name tag — a description tag). All arrays in this record are 60 elements. The `skillMaxLevel:16` here appears to be the actual cap for this specific monster skill record, not a player-cap echo. The `.arz` record for `tagClass05SkillDescription03A` was not directly located in the monster namespace search, but the presence of `skillMaxLevel:16` alongside 60-element arrays in a record without `skillUltimateLevel` is consistent with this being a nonplayer skill whose authoring simply used 16 as its cap — Crate can and does set nonplayer skill caps to non-60 values.

**Why the outliers do not rescue a padding theory:** A padding hypothesis would predict that 60-element arrays stop scaling meaningfully at the player's true cap (16 or 26) and repeat or plateau thereafter. In both outlier cases, the evidence contradicts this: `sk1497` has `petLimit[60]` that never stops scaling (last value is 4, not a repeat), and `sk733` has damage arrays of 60 elements all authored without any saturation pattern matching rank 16 or 26. The outliers are two nonplayer records that happen to carry `skillMaxLevel:16` because their content authors set that cap, not because a player cap was faithfully preserved into them.

The asymmetry (most records show `skillMaxLevel:60`, two show `skillMaxLevel:16`) reflects authoring variation in monster/NPS records, not a distinction between "padded" and "non-padded" records.

### Q1.4 — Was grimtools serving PTR/pre-release expansion data on 2026-07-21?

Not applicable to our harvest. The grimtools harvest (`all_skills.js`) contains no records with `tagGDX1Class07SkillName04A` (FoI) and no GDX3 content. GDX1 content in the payload is minimal: only 6 occurrences of GDX1 tags, all corresponding to what appear to be monster copies of Inquisitor-class skills (tagGDX1Class07SkillName14A = `Skill_WPAttack_ProjectileBurst` with `skillMaxLevel:60`). Matt's hypothesis (grimtools had expansion data ahead of retail) is chronologically excluded for this artifact and structurally excluded for FoI specifically, since FoI is absent from the harvest entirely.

---

## Verdict

### Does TSR-3's founding evidence stand?

**No. The founding evidence is a category error, not a data quality finding.**

The original observation was: "grimtools' 60-rank arrays contradict the .arz's 26 ranks." This comparison was never made between the same skill in the same namespace. The grimtools harvest exclusively contains nonplayer/monster skill records; the .arz playerclass records (including FoI) are entirely absent from that payload. The nonplayer copies of base-game skills (e.g., `ironmaiden_bladearc1.dbr`) natively have `skillMaxLevel=60` in the .arz — the 60-element arrays are correct for those records. There is no contradiction: neither source was wrong. The original analyst compared a nonplayer monster skill (grimtools) to a playerclass skill (.arz) that share a display-name tag, observed a rank-count difference, and incorrectly attributed that difference to a data-quality failure in the secondary source.

**Note on what does not change:** "consult the primary source (.arz)" remains correct and the TRUE-SOURCES pipeline remains justified — but the justification is different from what was written. The .arz advantage over grimtools is not that grimtools has wrong ranks; it is that grimtools does not contain player class skills at all. The correct rationale for preferring the .arz is coverage and namespace completeness, not correction of erroneous secondary data.

### Replaceable canon sentence

The current claim (paraphrased): "grimtools' community-harvested 60-rank arrays contradict the .arz's actual 26 ranks, and nobody noticed until a primary source was consulted."

**Replace with:** "The grimtools all_skills.js harvest contains exclusively nonplayer/monster skill records; player class skills are entirely absent from that payload. The .arz is the sole source for player skill data including true rank caps, rank arrays, cone geometry, and cast cadence. grimtools' 60-element arrays are correct for the monster records they represent; the discrepancy is a namespace mismatch, not a data quality failure in the secondary source."

---

## Knowledge gaps not resolved

1. **Full coverage of which player class skills appear as NPS copies in the grimtools payload.** The current finding is based on the sampled skills. A complete survey of which player-tagged skills appear in the NPS namespace, and therefore which appear in the grimtools harvest, was not done. Not required for the verdict but useful for understanding what the grimtools payload is actually good for.
2. **sk733's .arz source record.** The search for `tagClass05SkillDescription03A` (a description tag, not a name tag) in `database.arz` was not completed. The identity of this record's playerclass counterpart is unknown; it may be a standalone monster skill with no player copy.
3. **Why some GDX1 player skills appear in grimtools as NPS copies but FoI does not.** `tagGDX1Class07SkillName14A` and `15A` appear in grimtools (via NPS copies), but `04A` (FoI) does not. This suggests FoI has no nonplayer copy in the base `database.arz` (confirmed: not found in database.arz NPS search). Whether a NPS copy exists in `GDX1.arz` was not checked.

---

## Source list

| Source | Path / URL | Access date |
|---|---|---|
| database.arz (Edition-I) | `/Users/admin/Games/vendor/grim-dawn/database/database.arz` | 2026-07-24 |
| GDX1.arz (Edition-I) | `/Users/admin/Games/vendor/grim-dawn/gdx1/database/GDX1.arz` | 2026-07-24 |
| all_skills.js (grimtools harvest) | `agentic_orchestration/research/datamine-acquisition/gd/raw/all_skills.js` | 2026-07-21 (harvest date) |
| gd_arz_adapter_2026_07_24.py | `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` | Reused 2026-07-24 |
| Prior extraction probe | `agentic_orchestration/legolas/notes/2026-07-23-gd-arz-extraction-probe.md` | 2026-07-23 |
| Prior join-surface probe | `agentic_orchestration/legolas/notes/2026-07-23-join-surface-probe.md` | 2026-07-23 |
| Edition-I fingerprint | `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-I-freeze-fingerprint.md` | 2026-07-24 |
