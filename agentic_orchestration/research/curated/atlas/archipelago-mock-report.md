# Archipelago MOCK — Edition-I 469 kits — ashore/at-sea census + territory surface

**Status:** MOCK · **ratified:** FALSE · **Date:** 2026-07-16 · **Author:** elrond (data steward)
**Charge:** `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-grain-law-and-archipelago-mock-brief.md` (Part B)
**Authority:** Matt 2026-07-16 — *"I do approve of the archipelago strategy."* (strategy approved sight-unseen; this mock buys the census with real numbers.)
**Generator:** `agentic_orchestration/research/scripts/atlas_archipelago_mock_2026_07_16.py` · **Seed:** 20260716

> **THROWAWAY-CLASS EXHIBIT — NOTHING SERVED, NOTHING VENDORED.** Memberships are **computed** (clustering + label propagation in full 14-dim MCA space). Island **seating is designed-for-legibility** (MDS on cluster centroids), **not a measured coordinate** — disclosed as such in the JSON. **G1/G2/G3 ratification gates are NOT run** in this mock (they are charter-run + pre-registered, later). Do not read this mock as ratified.

> **⚠ SHELVED 2026-07-16 (Matt wave-4 ruling) — RECOGNITION RECORD.** The archipelago **territory-map surface is shelved**; Edition IV proceeds as anchored-E3 (see decision file `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § WAVE 4). **Re-entry criterion (empirical):** a per-sub-cluster-τ propagation passing names-level design review at ≥80% precision over ≥20 proposals. **Census caveat (post-mortem):** the "core" counts below CONFLATE gateA-ratified members with τ-propagated proposals — ratified truth is WHIRLWIND 15+0 · CHANNELED-BEAM 9+0 · MINION-PET 7+0 · AURA 8+2 · TOTEM-SENTRY 24+**22** · TRAP-MINE 23+**20**, and the 44 proposals ran ~1/3 precision (global-τ umbrella defect over multi-cluster families). The full-space **derivation layer survives unserved** (Leiden, U-n queue, ghost affinity, propagation-as-queue).

## 1. ASHORE / AT-SEA CENSUS (the answer to Matt's membership question)

| stratum | count | of 469 |
|---|---:|---:|
| **Islands (named six) — cores ashore** | 130 | 27.7% |
| **Islets (U-n, unnamed)** | 213 | 45.4% |
| **Straits (split family affinity)** | 0 | 0.0% |
| **Drifters (at sea — below-tau, no family)** | 126 | 26.9% |
| **TOTAL** | 469 | 100% |

**Per-family CORE sizes (the six named islands):**

| island (family) | core size |
|---|---:|
| TOTEM-SENTRY | 46 |
| TRAP-MINE | 43 |
| WHIRLWIND | 15 |
| CHANNELED-BEAM | 9 |
| AURA | 10 |
| MINION-PET | 7 |
| **named-island cores total** | 130 |

**Ghost cells (frontier, family-affinity shaded — MOCK approximation):**

| ghost stratum | cells |
|---|---:|
| shallows (within a family affinity radius) | 76 |
| deep (beyond ALL family radii — the true frontier) | 263 |
| frontier cells total (drifter+islet footprint) | 339 |

## 2. What the numbers say (survey-mode: what IS)

- **The named six are minority coasts, not the mainland.** 130 of 469 kits (28%) sit on a named family island as tau-confident cores; the bulk (126 drifters, 27%) is the mechanically-generic mainland at sea — kits that resemble no gateA family strongly. This is the honest shape of the corpus: the distinctive families are peripheral minorities around a dense generic core.
- **Some families are archipelagos, some are single islands.** Measured by how many distinct Leiden clusters each family's gateA seeds span: TOTEM-SENTRY=6, TRAP-MINE=7, WHIRLWIND=1, CHANNELED-BEAM=2, AURA=1, MINION-PET=2. The archipelagic families (TRAP-MINE(7), TOTEM-SENTRY(6)) scatter their seeds across multiple sub-islands under one named territory; the single-island families (CHANNELED-BEAM(2), MINION-PET(2), WHIRLWIND(1), AURA(1)) concentrate in one (or nearly one) cluster.
- **No straits (0).** At margin m=0.15, no kit sits between two families (2nd-nearest family within 15% of the nearest, both within tau). The six gateA families are **mechanically well-separated** in MCA space — kits commit cleanly to one family. (Note: the gateA seeds of TOTEM-SENTRY and MINION-PET do share one Leiden cluster, so a *cluster-level* strait notion would fire there; but at *kit-level affinity* each kit is clearly closer to one family. The mock reports the kit-level result honestly rather than manufacture a strait.)
- **213 islets (U-n)** in 27 coherent unseeded clusters (size>=3) carry no gateA seed and no tau-core — unnamed territory the gateA labeling never reached (largest: U-1, 20 kits). They are the concrete candidates for the next round of family naming.

## 3. Method (disclosed)

**Corpus (Stage 0, fail-loud):** the mock corpus is Edition-I's 469 active kits, exactly the `atlas-coordinates-active.csv` membership. Asserted (via Part A's ratified `grain` column): all 469 `grain='kit'`; **zero mcd rows**; **LA composition = 0** (expected 0 — the 62 LA rows are post-E1 growth). Kit-grain-clean by construction; no HALT.

**Clustering (Stage 1):** full **14-dim MCA space** (`dim1..dim14` — the retained-dims space, NOT the 2D plane). Method: **Leiden-CPM consensus** on a kNN(k=10) graph, 60 seeds @ resolution 0.3 (the existing `atlas_derivation_2026_07_14.leiden_consensus` machinery). **66 clusters**, biggest 4.5% (no degeneracy). Resolution profile:

| resolution | clusters | biggest | biggest %% |
|---:|---:|---:|---:|
| 0.2 | 45 | 24 | 5.1% |
| 0.3 **(chosen)** | 60 | 24 | 5.1% |
| 0.5 | 95 | 16 | 3.4% |
| 0.8 | 182 | 12 | 2.6% |
| 1.0 | 469 | 1 | 0.2% |

> **HDBSCAN was tried and REJECTED.** On the same 14-dim space it produced a **degenerate giant cluster (65-72%% of kits** at min_cluster_size 5-10), because the dense MCA core lumps into one blob and everything else becomes noise. That would trip the mock's own >60%% HALT. Leiden-CPM partitions the dense core into resolvable communities, which is what an archipelago needs. Disclosed per the brief.

**Family labels + tau (Stage 2):** seeded from the **86 gateA ratified labels** (6 families). A kit's family = its nearest gateA seed by family; **tau is an ABSOLUTE affinity threshold** — distance in MCA space to the nearest same-family seed — so the mechanically-generic mainland (far from every family) is **abstained as drifters, not force-assigned** (this was the key fix: a vote-share tau admitted everything and flooded two families to 130-160 members; an absolute-distance tau produces a real archipelago). **tau calibrated on a stratified 20% gateA holdout** (18 of 86 seeds): tau maximizes accuracy x coverage x (1 - mainland-admit-rate) — the third factor is the false-core penalty that makes tau discriminating. **Chosen tau = 0.80**, holdout accuracy **1.000**, coverage **0.889**, mainland-admit-rate **0.094**.

| tau | admit/holdout | accuracy | coverage | mainland-admit | score |
|---:|---:|---:|---:|---:|---:|
| 0.30 | 2/18 | 1.000 | 0.111 | 0.000 | 0.111 |
| 0.40 | 3/18 | 1.000 | 0.167 | 0.003 | 0.166 |
| 0.50 | 6/18 | 1.000 | 0.333 | 0.018 | 0.327 |
| 0.60 | 10/18 | 1.000 | 0.556 | 0.023 | 0.543 |
| 0.70 | 12/18 | 1.000 | 0.667 | 0.065 | 0.623 |
| 0.80 | 16/18 | 1.000 | 0.889 | 0.094 | 0.805 **<-- chosen** |
| 0.90 | 16/18 | 1.000 | 0.889 | 0.144 | 0.761 |
| 1.00 | 16/18 | 1.000 | 0.889 | 0.211 | 0.701 |
| 1.10 | 17/18 | 1.000 | 0.944 | 0.324 | 0.639 |
| 1.20 | 17/18 | 1.000 | 0.944 | 0.507 | 0.466 |
| 1.30 | 17/18 | 1.000 | 0.944 | 0.653 | 0.328 |
| 1.40 | 17/18 | 1.000 | 0.944 | 0.749 | 0.237 |
| 1.50 | 17/18 | 1.000 | 0.944 | 0.825 | 0.165 |
| 1.60 | 17/18 | 1.000 | 0.944 | 0.903 | 0.091 |
| 1.70 | 18/18 | 1.000 | 1.000 | 0.916 | 0.084 |
| 1.80 | 18/18 | 1.000 | 1.000 | 0.948 | 0.052 |
| 1.90 | 18/18 | 1.000 | 1.000 | 0.963 | 0.037 |
| 2.00 | 18/18 | 1.000 | 1.000 | 0.974 | 0.026 |

**Five strata (Stage 3):** core (affinity<=tau) / islet (coherent unseeded cluster, size>=3, U-n) / strait (two families within m=0.15 AND both within tau) / drifter (below-tau, no family — the mainland) / ghost (frontier). Islet discipline: an unseeded cluster is demoted to drifter if it gained tau-cores (a family **fringe**, not a pure islet — 90 members) or is below size 3 (a lone/tiny fragment adrift is a **drifter**, not land — 14 members). U-n therefore means genuinely-unclaimed coherent territory; U-1 is the largest islet.

**Ghost cells (Stage 3b, MOCK):** MOCK approximation over the 469 kits' own unclaimed (drifter+islet) footprint; NOT the charter 11,160-cell meso ghost-field projection (that is Edition-scoped + read-only). Shallows=76 (within a family affinity radius, 90th-percentile intra-family), deep=263 (beyond all — the true frontier).

**Seating (Stage 4):** MDS(2D) on cluster centroids (full-space euclidean) + within-island local MDS layout + water by fiat. MDS stress 609.0437 over 66 cluster centroids. Islands seat at the mean of their cores; islets at the mean of their members; water by fiat between islands; local island radius ~6 units. **Tombstones:** E1-469 has **0 negative kits** — Finding F-1 (tombstones on their HOME island; kit death is not geography) is honored **vacuously**; the placement mechanism is disclosed but no tombstone needs seating.

## 4. Gates NOT run (say so plainly)

**G1/G2/G3 ratification gates are NOT run in this mock.** They are charter-run and pre-registered, to fire later against a real (non-mock) archipelago derivation. This exhibit answers the *census* question with real numbers and shows the *shape* of the territory surface; it does **not** ratify anything. The seating is designed-for-legibility, not measured. Nothing here is served or vendored.

## 5. Residual framings embedded for Matt to rule on concretely

- **Two-surfaces identity:** memberships (computed, defensible) vs seating (designed, legibility-only). The mock keeps them separate and stamped; a ratified atlas would need to decide whether the archipelago *replaces* or *overlays* the plane surface.
- **Five-strata membership:** the census above is the concrete instance. Matt can now see whether core/islet/strait/drifter/ghost is the right vocabulary against real counts, or whether (e.g.) drifters at 27% argue for a coarser family net or more seed labels.

**Artifacts:** `atlas-archipelago-mock.json` (this dir) · this report. Both stamped `mock:true, ratified:false`.
