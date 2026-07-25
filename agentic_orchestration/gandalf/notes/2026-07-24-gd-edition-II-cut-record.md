# GD Edition-II — Cut Record + Edition-I Delta

**Date:** 2026-07-24
**Authorized by:** Matt ("snapshot with editions — cut Edition II, co-pinning ruled")
**Conductor:** gandalf (RUN-CONDUCTOR)
**Fetch:** Matt, interactive authenticated DepotDownloader session. Transcript at
`matt_notes_handoff_docs/fetch-logs`.
**Assembly:** gandalf, from `/Users/admin/depots/` → `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`

---

## 1. The fetch — succeeded; the verification step is what failed

Matt reported the fetch as failed because the closing `find "$DST" -name "*.arz" | sort`
returned `find: : No such file or directory`.

**Root cause:** `DST=…` and `mkdir -p "$DST"` were typed into the login `zsh` while `bash`
was still starting. The `bash-3.2$` subshell that ran the downloads never had `DST` set, so
every `-dir "$DST"` was `-dir ""` and the closing `find` was handed an empty path argument
(`find: :` — the colon with nothing before it is the tell).

DepotDownloader treated the empty `-dir` as "not supplied" and fell back to its default
`depots/<depot_id>/<build_id>/…` layout under the shell's cwd, `/Users/admin`. **All 190 MB
arrived correctly.** Nothing was lost; nothing needed re-fetching.

Recorded because the failure mode is worth recognizing on sight: *a command that reports a
path error on an empty argument is a variable-scope failure, not a download failure.*

## 2. Manifest pins — the finding

Every depot the account owns was re-enumerated at current manifests. Comparing against the
Edition-I pin table:

| depot_id | Edition-I manifest | Edition-II manifest | Δ |
|---|---|---|---|
| 219991 (base) | 8006922163969537169 | 8006922163969537169 | **unchanged** |
| 483840 (survivalmode) | 4219096235914851781 | 4219096235914851781 | **unchanged** |
| 642280 (gdx1 / Ashes of Malmouth) | 2275863479823292335 | 2275863479823292335 | **unchanged** |
| 642281 (survivalmode1) | 1006721765621603920 | 1006721765621603920 | **unchanged** |
| 897670 (gdx2 / Forgotten Gods) | 4804720554373426689 | 4804720554373426689 | **unchanged** |
| 897671 (survivalmode2 / FG Crucible) | 2984427886892515994 | 2984427886892515994 | **unchanged** |
| 228983/4/5/6, 228990, 229003 | unchanged | unchanged | non-data; 0 bytes |
| **2699230 (gdx3 / Fangs of Asterkarn)** | — | **1575323658468418166** | **NEW** (07/23 03:00:32) |
| **2699231 (survivalmode3)** | — | **2924790412415164930** | **NEW** (07/23 03:01:19) |

**Edition-I was already a post-Asterkarn-patch build.** The base manifest carries a
07/23/2026 02:59:09 timestamp — that *is* the expansion patch. Our Edition-I fetch ran
07/23 22:38, roughly twenty hours downstream of it. The freeze captured post-patch base
bytes without anyone realizing it.

**Edition II is therefore purely ADDITIVE.** It is Edition-I plus two archives.

## 3. Byte-level verification — the pinning premise, live-tested

Manifest IDs are advertised as immutable content identifiers. That is a *claim about the
world*, and we had been treating it as load-bearing without ever testing it. Identical
manifests predict identical bytes. The prediction was registered before the diff was run.

**Result: 11/11 IDENTICAL.** Every `.arz` and `.arc` shared between the two editions
byte-matches, independently confirmed by SHA-256 against the Edition-I freeze table.

```
database/database.arz                          IDENTICAL
gdx1/database/GDX1.arz                         IDENTICAL
gdx1/resources/Text_EN.arc                     IDENTICAL
gdx2/database/GDX2.arz                         IDENTICAL
gdx2/resources/Text_EN.arc                     IDENTICAL
mods/survivalmode/database/SurvivalMode.arz    IDENTICAL
mods/survivalmode/resources/Text_EN.arc        IDENTICAL
resources/Text_EN.arc                          IDENTICAL
survivalmode1/database/SurvivalMode1.arz       IDENTICAL
survivalmode1/resources/Text_EN.arc            IDENTICAL
survivalmode2/database/SurvivalMode2.arz       IDENTICAL
```

The manifest pin is now an *empirically validated* version key, not an assumed one. This is
the single most useful by-product of the run: `source_version` can carry a manifest ID and
that ID means what we need it to mean.

## 4. New in Edition-II

| path | bytes | sha256 |
|---|---|---|
| `gdx3/database/GDX3.arz` | 47,334,429 | `1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0` |
| `gdx3/resources/Text_EN.arc` | 191,313 | `d6e7f7810ab251e3ad9e0dcf87e22d0af8f7d1611c02e1be4d431c44fd0d1f18` |
| `survivalmode3/database/SurvivalMode3.arz` | 3,919,713 | `b4aa2d78675c4f05f92988e5c524ff9874a13984700484656a10b0578b03af7e` |
| `survivalmode3/resources/Text_EN.arc` | 2,219 | `6336cde2568712253eb21020732421a4a8d417fd92eab60a2f6f86c606927524` |
| `survivalmode2/resources/text_en.arc` | 2,048 | `8269f89cc6eda34847e8839722767f11a3ac66210a198bc5b82e65823a3c824f` |

GDX3 at 47 MB sits in the same weight class as GDX1 (42 MB) and GDX2 (33 MB) — this is a
full expansion's worth of records, not a patch payload.

## 5. A coverage gap in our own freeze — found by the diff

`survivalmode2/resources/text_en.arc` shows as "new in Edition-II." **It is not new.** It
exists in the Edition-I source directory (2,048 bytes, 2026-07-23 22:53) and was **missed by
the Edition-I freeze**, because the freeze's `find` used case-sensitive `-name "Text_EN.arc"`
and this one file ships lowercase.

The content is a 2 KB stub; the practical loss is nil. **The class of error is the point.**
The Edition-I freeze record asserts "All `Text_EN.arc` (5 files)" and that assertion was
false — it was 5 of 6. Nothing in the freeze verification could have caught it: all 11 hashes
matched, because the check verified *the files we collected*, not *the files that exist*.

That is precisely the hazard the TRUE-SOURCES canon-change proposal names as **D-a
(coverage-boundary declaration)** — a value-level check passing cleanly over an
undeclared missing population — and we committed it in our own artifact, in the same
session in which we wrote the discipline. It is now the discipline's best worked example,
and the second-best argument for it: it is not a hazard that happens to sloppy outsiders.

Edition-II carries the file. Edition-I's record is annotated below rather than re-cut.

## 6. Consequences for banked work

- **The FoI 22-row byte-match certificate SURVIVES unchanged.** Flames of Ignaffar lives in
  gdx2; `GDX2.arz` is byte-identical across editions.
- **The controller spatial fields survive** (`ViewDistance`, `SightAngerRate`,
  `MaxPursuitDistance`, `fleeDistance`) — same archives, same bytes. TSF6/VDM work is not
  version-skewed.
- **The co-pinning risk I raised is narrower than I claimed.** I warned that Matt's Asterkarn
  playtest observations would be version-skewed against Edition-I rows. For anything sourced
  from base/gdx1/gdx2 they are not — the bytes are the same build he is playing. The
  co-pinning rule still stands and should still be enforced, but the specific alarm was
  louder than the fact. Recorded because a warning that turns out overstated should be marked
  as such, not quietly retired.
- **Edition-I is not deprecated.** It is a strict subset of Edition-II and remains valid for
  every row derived from it. `source_version` backfill (elrond, owed) should carry the
  Edition-I pin as recorded, and only gdx3-derived rows need the Edition-II pin.

## 7. Owed follow-ups

1. `source_version` backfill on Edition-I rows, **before** any gdx3 row lands. — **elrond**
2. gdx3 adapter lap: does `GDX3.arz` parse under the existing TQIT reader, and does it
   introduce new `playerclass<NN>/` namespaces (new masteries) or only records? — **legolas**
3. Annotate the Edition-I freeze record's § 2 file-count claim. — **gandalf** (done, see that file)
4. Ratify the disposition ruling + the manifest-pin validation into decisions-log. — **jack-ryan**

## 8. Locations

- **Edition-I:** `/Users/admin/Games/vendor/grim-dawn-edition-I-20260723/` — 11 files, unchanged, re-verified 11/11 this session
- **Edition-II:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` — 16 data files + `depot.config.edition-II`, 189 MB
- **Raw fetch (may be deleted once Edition-II is trusted):** `/Users/admin/depots/`
- **Live source (Edition-I era):** `/Users/admin/Games/vendor/grim-dawn/` — untouched

**Note:** Edition-II carries no `.DepotDownloader/*.manifest` binaries — this DepotDownloader
run did not retain them. The manifest pins in § 2 are sourced from the fetch transcript, which
is the primary record of the run. Retained at `matt_notes_handoff_docs/fetch-logs`; do not
delete it, as it is currently the only Edition-II version pin.
