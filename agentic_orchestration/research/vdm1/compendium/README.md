# VDM-1 COMPENDIUM — the one-representation render

> **STATUS:** CURRENT (v1.1-verified). Generated 2026-07-19T20:04:46Z FROM the `corpus.db` `kit_master` view. **db md5 `c7886250e92d80c9014890a58b0b0cc3`.**

**Authority (D-11a / D-11f inversion):** post-v1.1, `corpus.db` + this compendium GOVERN. This compendium is the ONE-per-kit representation Matt asked for — the most complete version with URL + authorship citations attached — assembled live from the `kit_master` view (identity ⋈ mapping ⋈ citation-aggregate ⋈ verify-tally ⋈ dossier-count). It **supersedes** the four review rosters (`REVIEW-BOOK-ROSTER-{EXACT,CLOSE,APPROX,GAPPED}.md`), which carry no citations; those retire to git as the review artifact.

**Contents:** 574 kits · 21 games · per-game `.md` + one `vdm1-compendium.jsonl` (machine render).

| game | kits | file |
|---|---|---|
| poe1 | 94 | [`kits-poe1.md`](kits-poe1.md) |
| d2 | 60 | [`kits-d2.md`](kits-d2.md) |
| la | 52 | [`kits-la.md`](kits-la.md) |
| d3 | 49 | [`kits-d3.md`](kits-d3.md) |
| d4 | 46 | [`kits-d4.md`](kits-d4.md) |
| gd | 41 | [`kits-gd.md`](kits-gd.md) |
| poe2 | 38 | [`kits-poe2.md`](kits-poe2.md) |
| le | 37 | [`kits-le.md`](kits-le.md) |
| di | 24 | [`kits-di.md`](kits-di.md) |
| vs | 23 | [`kits-vs.md`](kits-vs.md) |
| tq | 21 | [`kits-tq.md`](kits-tq.md) |
| hot | 17 | [`kits-hot.md`](kits-hot.md) |
| chronicon | 16 | [`kits-chronicon.md`](kits-chronicon.md) |
| undecember | 12 | [`kits-undecember.md`](kits-undecember.md) |
| tl2 | 11 | [`kits-tl2.md`](kits-tl2.md) |
| tli | 9 | [`kits-tli.md`](kits-tli.md) |
| hades1 | 7 | [`kits-hades1.md`](kits-hades1.md) |
| hades2 | 5 | [`kits-hades2.md`](kits-hades2.md) |
| mcd | 5 | [`kits-mcd.md`](kits-mcd.md) |
| tq2 | 5 | [`kits-tq2.md`](kits-tq2.md) |
| tl1 | 2 | [`kits-tl1.md`](kits-tl1.md) |
| **TOTAL** | **574** | `vdm1-compendium.jsonl` |

**Regeneration:** `python3 research/scripts/vdm1_compendium_gen_2026_07_19.py` (read-only on `corpus.db`; re-stamps the md5). Cheap to re-run if a trailing citation lands (e.g. the `ud-snowstorm-frost` citation-pending residue closing 573→574).

**Provenance-cleanliness:** the `kit_master` view exposes NO mobile-era raw descriptors (`elem_raw`, suffix raws); those remain provenance-only in `canon_corpus`. `kit_citations` is the sole citation authority (`canon_corpus.source_urls` is DEPRECATED-frozen per D-11c).
