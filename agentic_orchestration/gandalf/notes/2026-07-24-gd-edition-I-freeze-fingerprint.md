# GD Edition-I — Freeze + Fingerprint Record

**Date:** 2026-07-24
**Authorized by:** Matt ("go — freeze and fingerprint first")
**Conductor:** gandalf (RUN-CONDUCTOR)
**Trigger:** a Grim Dawn expansion landed 2026-07-23. Re-fetching the Steam depot would
overwrite our primary source in place, destroying the ability to diff old against new.
The diff is the deliverable, so the old bytes had to be preserved before anything moved.

---

## 1. What this is

`hashing is the fingerprint; copying is the freeze.` Hashes alone prove that something
changed but leave us unable to diff *content*. Both were done.

**Frozen snapshot:** `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/`
**Source:** `/Users/admin/Games/vendor/grim-dawn/` (DepotDownloader fetch, 2026-07-23 22:38–22:53)
**Size:** 140 MB

The source directory is **untouched** — this is an additive copy, not a move.

## 2. Freeze scope and why

| Included | Size | Why |
|---|---|---|
| All `*.arz` (6 files) | 139 MB | The primary source. Everything the GD adapter consumes. |
| All `Text_EN.arc` (5 files) | 900 KB | Localization tag-bridge. Currently PENDING in the adapter (`name_provenance` flag) — skill display names are localization tags in the `.arz`, resolvable only here. Frozen now so the bridge can be built later against the same edition. |
| `.DepotDownloader/` manifests | ~1 MB | The version pin. See § 4. |

**Excluded:** ~9.7 GB of art/asset `.arc` archives and the Windows binaries. Nothing in
our pipeline consumes them, and they dominate the depot's size. If a future need arises
they are re-fetchable at the same manifest IDs recorded below — which is precisely what
makes the exclusion safe.

**Relative directory structure preserved**, so the existing adapter can be repointed at
the frozen tree by changing only its root path.

## 3. Verified inventory — SHA-256

All 11 files verified byte-identical against source at freeze time (11/11 OK).

```
8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f  database/database.arz
e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539  gdx1/database/GDX1.arz
85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a  gdx1/resources/Text_EN.arc
f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985  gdx2/database/GDX2.arz
8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1  gdx2/resources/Text_EN.arc
e55b760f36ab80a6ad16fd34f3f8ca76e1cde55ee6160d72eb574c01221405f2  mods/survivalmode/database/SurvivalMode.arz
fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e  mods/survivalmode/resources/Text_EN.arc
613457c8df72fe5a16de88def05dd00f518cf4e61c14cf375ef2ccab6dbd6e01  resources/Text_EN.arc
6df94d3be33e600c737634bc8fcf1949a4b51d349677c7404b98c44ce2da6e5a  survivalmode1/database/SurvivalMode1.arz
af9d87ce5cc72629ffb970aa8e6a06e2cdf1b0fd0bf6dd0dcd3e32244430a694  survivalmode1/resources/Text_EN.arc
940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95  survivalmode2/database/SurvivalMode2.arz
```

**Note:** `database.arz` here is 58,338,379 bytes. The 2026-07-23 probe note records it as
"55.6 MB, 34114 records" — the same file, MiB vs MB. Not a discrepancy.

## 4. The version pin — depot / manifest IDs

Steam manifest IDs are immutable content identifiers. They are a **better** version pin
than a marketing patch number, because they name exact bytes rather than a label the
publisher can reuse. This table is what `source_version` should carry.

| depot_id | manifest_id | manifest SHA-1 |
|---|---|---|
| 219991 | 8006922163969537169 | 69cbd1d16014a37263bfb6a83bfb9d55e9e2880d |
| 228983 | 8124929965194586177 | d3ac038d8d7c2e6a75ca410598a5a1a9ee5050c0 |
| 228984 | 2547553897526095397 | 0eb2146a7f22464cf06a5577c25232516d914f9a |
| 228985 | 3966345552745568756 | 2b510f9a1f9eda3ca593017ab489189170af1047 |
| 228986 | 8782296191957114623 | 0e9f4b037462df803197b3fddeca0c99001b6ec2 |
| 228990 | 1829726630299308803 | b78bd741f53fdd76c5a5618038c5d8172b67b812 |
| 229003 | 8740933542064151477 | 122ae492dc56bfcd567d8fa3535481a24798bd86 |
| 483840 | 4219096235914851781 | 11cd7cac9874a45eb2138d8d3c04ff8586d6e2c8 |
| 642280 | 2275863479823292335 | 5145baa2f0943a2d8338289d7d04e824a27031c1 |
| 642281 | 1006721765621603920 | c9becf65f08c2eaf9848e07719b8a3722f94c3c6 |
| 897670 | 4804720554373426689 | 93f9ccdafb98eba572c27f587e7ecfcf5681193a |
| 897671 | 2984427886892515994 | 8bec4377487689362252459009f848efc1bf6560 |

219991 = base-game Windows content. 642280/642281 = Ashes of Malmouth (gdx1).
897670/897671 = presumed Forgotten Gods (gdx2) — **not verified**, inferred from the
presence of `GDX2.arz` in this fetch. Legolas verifies against SteamDB; it is not banked.

## 5. Known gaps in this edition (recorded, not fixed)

- **`templates/` absent.** Zero `.tpl` files in the depot. The 2026-07-23 probe expected
  them "alongside `database/`". Every `.arz` record references a template by path via
  `templateName`, so template semantics are currently unresolvable from what we hold.
  Either the depot list omitted a depot, or templates ship elsewhere. Open question.
- **Localization bridge unbuilt.** `Text_EN.arc` is frozen but not parsed. Skill display
  names remain localization tags (`tagGDX1Class07SkillName04A`). `name_provenance` is
  flagged PENDING in the adapter.
- **No gdx3 content.** This edition predates the 2026-07-23 expansion. Confirmed by
  directory inventory (gdx1, gdx2, survivalmode1/2 only).
- **`Asterkarn` strings in the base archive are NOT expansion content.** Asterkarn Valley,
  Asterkarn Road, and the Asterkarn Mountains yeti boss are pre-existing base-game Act-4
  locations. The expansion is named after an existing region. Recorded because these
  strings read at first glance as evidence the expansion is present. It is not.
- **`records/fx/skillsothergdx3/...` appears exactly once** in `database.arz`, as a single
  FX path. Weak signal, unexplained. Not evidence of expansion content; flagged for legolas.

## 6. The rule this establishes

**Corpus disposition: snapshot with editions** (gandalf lean, pending Matt ruling).
Every banked row carries the manifest pin of the edition it was derived from. Expansions
produce *new* editions alongside old ones; they do not overwrite.

**Co-pinning corollary:** the playtest build and the corpus edition must be co-pinned, or
every human-oracle observation must be labeled with the build it came from. Matt is the
oracle for everything the `.arz` is silent about — notably aggro onset, which TSF6-TRACK-A
established the sim has no concept of at all. An observation learned on Asterkarn and
banked against Edition-I controller values is a version-skewed row wearing the badge of
human-validated ground truth. That is worse than an unpinned row.

Consequence: **Edition II should be cut promptly**, because the oracle has already moved
to it. An edition nobody plays is a museum piece.

## 7. Owed follow-ups

1. `source_version` is empty on the one banked `exact_skill` row
   (`gd-flames-of-ignaffar-purifier`). Backfill with the Edition-I pin **before** any
   Edition-II row lands. Mixed populated/blank version columns are worse than uniformly
   blank, because the blanks start reading as "same as the others." — **elrond**
2. Edition-II lane establishment + delta report. — **legolas** (commissioned 2026-07-24)
3. Re-adjudication of the 60-vs-26 grimtools contradiction. — **legolas** (same commission)

## 8. Ownership

This record was produced by gandalf under an emergency freeze authorization and lives in
gandalf's notes for unambiguous provenance. **It is evidence, not canon.** Downstream
ownership: legolas consumes it for the delta run; elrond owns any corpus-schema
consequence and the `source_version` backfill.
