# VDM-2 COMPENDIUM — the enriched one-representation render

> **STATUS:** CURRENT (v2.0). Generated 2026-07-22T09:46:42Z FROM the `corpus.db` `kit_master` view (574) ENRICHED live with the six VDM-2 side-car blocks + two registries. **db md5 `bebc933b0bf9bcab5988bbc16bcc55b4`.**

**Authority:** post-VDM-2, `corpus.db` + this compendium GOVERN. This is the v2.0 successor to the VDM-1 compendium (`research/vdm1/compendium/`, `v1.1-verified`, which stays recoverable in git + on disk). The VDM-2 lap re-emitted all 267 record-class kits into six per-kit/per-skill side-car blocks + 2 registries; this render surfaces that structure per-kit alongside the VDM-1 identity/mapping/citation/verify surface.

**Mechanism (Approach B — freeze-cleanest):** the six-side-car joins happen in the RENDER LAYER (this gen script), NOT in the DB. `corpus.db` is never mutated — no view redef, no DDL, no data touch. The multi-row-per-kit side-cars are aggregated via correlated subqueries + `json_group_array` (the same pattern `kit_master` already uses for citations), so the surface stays EXACTLY 574 rows with no per-skill explosion. canon_corpus data columns stay frozen.

**Freeze proof (measured at gen time):** full-585 fingerprint `38823f2fee619cb856c342f2abd10c15` (expected `38823f2fee619cb856c342f2abd10c15`) · 584-differential `d5a9a8e04d585a610b214c674830289a` (expected `d5a9a8e04d585a610b214c674830289a`) · corpus.db md5 `bebc933b0bf9bcab5988bbc16bcc55b4` (expected `bebc933b0bf9bcab5988bbc16bcc55b4`) · **freeze held: True**.

**Invariants (measured):** canon_corpus 585 / kit_master 574 / is_system 19 · skill_geometry_band 490 / kit_deviation 259 / recognition_hook 441 / kit_acceptance_assert 310 / kit_delta_t4 267 / kit_numeric 2 · kit_door_arg 0 (carved out — untouched) · verify_ledger 2577 · door_registry 28 / motion_signature_registry 18.

**Contents:** 574 kits · 21 games · per-game `.md` + `vdm2-compendium.jsonl` (machine render) + `registries.md` (the two global reference tables).

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
| **TOTAL** | **574** | `vdm2-compendium.jsonl` |

**Regeneration:** `python3 research/scripts/vdm2_compendium_gen_2026_07_22.py` (read-only on `corpus.db`; re-stamps the md5).

**Provenance-cleanliness:** `court` (reconciled, enum-checked) is the surfaced element field; `original_element` carries raw provenance (reversibility). Raw mobile-era descriptors (`elem_raw`, suffix raws) are NOT exposed (provenance-only, VDM-1 law held). `kit_citations` is the sole citation authority (`canon_corpus.source_urls` DEPRECATED-frozen).
