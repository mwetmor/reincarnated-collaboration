# Phase E-2 Gate-2 Findings Record — 2026-05-23

**Author:** knight-rider
**For:** durable record of Gate-2 critique-pair returns on legolas Phase E-1 frame-revision output (commit `080c7bf`, tag `legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23`); anchors the Phase E-2 dispatch authoring
**Reviewers:** jack-ryan (DEV-MODE Pattern-A-light) + gandalf (Pattern-A-deep framing-audit per § 9.5)

---

## 1. Jack-ryan Gate-2 (process side) — verbatim

### Finding 1 — Gate-1 fold-in compliance [INFO]

All five Gate-1 findings honored:

- **BLOCK Finding 2 (acceptance gate verbatim):** Completion summary gates table states "≥ 50 emergent clusters" and "≥ 0.70 per-lineage purity." Bis-disposition section cites "125 clusters ≥ 50 threshold" and "Purity 0.9444 ≥ 0.70 threshold" explicitly. Wording matches dispatch §B.6. RESOLVED.
- **WARN Finding 1 (stratification floor + per-lineage table pre-fire):** Math note §3.1 commits all parameters and §3.2 provides the complete 14-lineage table. File mtime 12:22; pipeline fired 12:26:48 — 4-minute gap confirms code-after-math. Discipline #1 honored. RESOLVED.
- **WARN Finding 3 (MIGRATION.md native-vs-nearest split):** §4 of MIGRATION.md is explicit, includes SQL patterns, carries ADR-004 + Discipline #8 citation, and names Phase E-2/E-3/E-4 consumers individually. RESOLVED.
- **WARN Finding 5 (no full-pool bootstrap re-fire):** D2 was re-fired as a minimal TruncatedSVD(k=3) on full X_weighted to extract axes — this is axis recomputation for projection, not a bootstrap re-fire. Math note §3.1 and completion summary §D1/D2 document the choice. Bootstrap stability itself was not re-run; the full-pool 10-resample result from Option-A was treated as authoritative. This is within dispatch scope and correctly justified. RESOLVED.
- **WARN Finding 6 (Discipline #19 candidate operationalization):** Substrate-voting-is-binding is fully operationalized in math note §2 as a binding gate. RESOLVED.

### Finding 2 — psutil RSS-guard absent at HDBSCAN.fit [WARN]

Run log line 48: `psutil not available — skipping RSS guard (not installed; pip install psutil to enable)`. Math note §1 committed this guard as a discipline-compliant safety belt. Guard was coded correctly but psutil was not installed at runtime — silent drop.

Materiality: low (peak memory ~600-700 MB on 8 GiB at k=3; guard would not have triggered). Forward concern: Phase E-1.5 sensitivity sweep or any future subsample-scale re-run on this machine without psutil leaves the safety belt missing. **Action:** queue `pip install psutil` as preflight for Phase E-1.5 dispatch (sub-carry 9.10-G.1).

### Finding 3 — D1 features.md overwrite discrepancy [INFO]

Math note §3.1 committed "skip overwriting features.md." Run log shows D1 completion with features.md write path (line 14) then "D1 already computed above; X is in memory. Skipping features.md overwrite" (line 25). Completion summary §Artifacts lists features.md as "Overwritten (identical content)." These statements are in tension; data integrity unaffected (content identical). Action: documentation inaccuracy; no rework needed.

### Finding 4 — Tag protocol, bis-disposition, D2 re-fire scope, idempotent ALTER TABLE [INFO]

All clean. Tag seam-prefix per ADR-001. Bis-disposition gates unambiguous. D2 minimal re-fire bit-for-bit identical (RANDOM_STATE=42). `assignment_method` column added idempotently with error-catch.

**Jack-ryan verdict: Gate-2 ratification PASS.** Phase E-2 unblocked from process side. WARN (psutil) is non-blocking; surfaced for Phase E-1.5 preflight.

---

## 2. Gandalf Gate-2 (design-coherence framing-audit per § 9.5) — verbatim

### Question A — Substrate-led or stratification/parameter-manufactured? [WARN]

Cluster roster shows substrate-led structure on the *whole* — but two specific cluster shapes need calling out before Phase E-2 inherits them as canonical.

**(1) Cluster 90 (N=10,087, east_asian/unknown-period/rifle) is suspicious by sheer mass.** 10,087 rows ≈ 77% of the entire east_asian pool (13,080) packed into one cluster — and the dominant period is `unknown` with `register=historical`, top-3 representatives include `H/AKJ-16`, `Q132210441`, `Teppô`. That mix (alphanumeric catalog IDs + romaji `Teppô` for matchlock firearm) reads like an east_asian metadata-floor / unknown-period bucket, not a coherent weapon-design cluster. This is the axis-1+axis-2 corner where `period_unknown` (negative-loading on axis-2) collapses with `lineage_east_asian` and surfaces in axis-3 as `lineage_east_asian (-0.1876)`. It's the dual of fantasy_generic — but where fantasy_generic clustered *by weapon-type* (Cluster 62 axe, Cluster 52 spear, etc.), east_asian collapsed into a single metadata-unknown mega-bucket. **Likely cause:** the `period_unknown` flag is doing too much work on east_asian rows whose periods weren't curated in Phase D cleaning.

**(2) Cluster 50 (N=1,907, european/contemporary/bow)** — top-3 representatives are `zweihänder` (×2) and `hardened steel kriegsmesser`. These are two-handed swords, not bows. The "bow" top-weapon-type label is a labeling artifact of the provisional-description code, but the underlying mix (military_modern register + contemporary + european + two-handed) is real and coherent. This is a **labeling-pipeline bug** more than a clustering bug, but Phase E-2 will inherit garbled provisional descriptions.

Neither is a stratification-floor artifact. The 125 count is substrate-led. But Cluster 90 needs design-side recognition that it's a metadata-bucket cluster, not a weapon-design cluster.

### Question B — Does k=3 give Phase E-2 enough resolution? [INFO with mild WARN]

Axes 1-3 = (fantasy-register, military-modern/contemporary, one-hand/two-hand) is a sensible *coarse* spine. Cluster 62 (fantasy_generic axe, N=4,807) bundles `Abyssal Bane Chakram`, `Abyssal Bane Knuckle Duster (rare variant)`, `Abyssal Bane Knuckle Duster (very rare variant)` together with "axe" as the dominant top weapon-type — i.e., the "Abyssal Bane" item-template family collapses across weapon types into one cluster because axis 1 (`kind_named_template`) dominates over weapon-shape signal at this k. **For canonical labeling that respects weapon-form fantasy, axes 1-3 are too coarse on the fantasy_generic side.** Phase E-2 can label "Abyssal Bane family" sensibly, but cannot label "fantasy axes vs fantasy chakrams" — they're in the same cluster.

Acceptable for Phase E-2 as **coarse spine canonical labels**, NOT acceptable as final taxonomy. Phase E-1.5 sensitivity sweep (queued, not executed) is the natural follow-on.

### Question C — Rare-lineage representation [INFO]

Mostly genuine. Cluster 23 (arctic_circumpolar/contemporary/lance, N=34, purity 0.88) and Cluster 86 (south_american_indigenous/contemporary/shotgun, N=36) show rare lineages forming their own clusters where the substrate supports it. Cluster 68 (cross_cultural/contemporary/shotgun, N=502) absorbing some oceanic rows is plausible — oceanic at 39 total is genuinely sparse. **Not pathological.**

**Caveat:** n.am.indigenous has its dominant cluster (Cluster 69) at only 7 rows (`european/contemporary/rifle` dominant) — the lineage is spread across 15 clusters with no real home. Substrate-honest (29 total rows can't form a coherent cluster at mcs=10) but Phase E-2 should NOT attempt to canonically label n.am.indigenous via cluster — it doesn't have one.

### Question D — Native-vs-nearest split [WARN]

The 10K-native / 38K-nearest asymmetry is methodologically honest *if* Phase E-2 treats it as a label-confidence weight. MIGRATION.md § 4 documents the requirement explicitly. But "must not assume equal density-based confidence" is a discipline imposed on downstream consumers — it doesn't yet exist as a Phase E-2 dispatch directive. **Methodology debt risk:** Phase E-2 authors canonical labels, those labels propagate to engine/loadout, the 38K nearest-centroid rows inherit labels with no confidence flag visible to engine consumers. **Mitigation needed:** Phase E-2 dispatch must require that cluster-representative sampling for labeling pull preferentially from `hdbscan_native` rows.

### Question E — Phase E-2 readiness verdict — CONDITIONAL PASS

Three conditions for the Phase E-2 dispatch:

1. **Cluster 90 flagged as metadata-bucket cluster.** Phase E-2 labels it honestly (e.g., "East Asian Uncurated-Period Pool" or equivalent) rather than retro-fitting a weapon-design narrative onto a 10K-row metadata residue. Knight-rider documents this in the Phase E-2 dispatch.
2. **Cluster representatives sampled from `hdbscan_native` only.** Per MIGRATION § 4. Phase E-2 dispatch makes this explicit; gandalf labels using top-3 reps drawn from N=10K, not the full 48K.
3. **Phase E-1.5 sensitivity sweep queued as immediate follow-on after Phase E-2, not deferred indefinitely.** k=3 is acceptable as coarse spine for THIS labeling pass; the question of whether weapon-form distinctions (axe vs chakram within fantasy_generic) deserve substrate-distinct treatment is deferred to E-1.5 + a future re-labeling pass. Phase E-2 canonical labels should be authored with the explicit acknowledgement that they are coarse-spine, not weapon-form-resolution-final.

**Gandalf verdict: Design-coherence Gate-2 ratification CONDITIONAL PASS** — conditions 1, 2, 3 above must appear in the Phase E-2 dispatch authored by knight-rider.

---

## 3. Synthesis for Phase E-2 dispatch authoring

| Fold-in source | Required dispatch directive |
|---|---|
| Gandalf condition 1 | Cluster 90 metadata-bucket labeling protocol |
| Gandalf condition 2 | hdbscan_native-only representative sampling for labeling |
| Gandalf condition 3 | Phase E-1.5 sensitivity sweep as immediate-follow-on carry |
| Gandalf Question A.2 (Cluster 50) | Provisional-description override protocol when top-reps contradict description |
| Gandalf Question C (n.am.indigenous) | Non-cluster canonical disposition for n.am.indigenous |
| Jack-ryan Finding 2 (psutil) | Sub-carry 9.10-G.1 (psutil preflight for E-1.5) |

---

**Signed:** knight-rider, post-Gate-2 critique-pair synthesis 2026-05-23 ~12:35 EDT. Phase E-2 dispatch authoring follows this record.
