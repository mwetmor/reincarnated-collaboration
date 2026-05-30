# Phase 5 element_distribution aggregator forensics
**Date:** 2026-05-29
**Author:** rocket (forensic query; Pattern-A)
**Scope:** Read-only investigation; no code changes.

---

## Aggregator location

Primary computation:
`reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py`
Function `_compute_cluster_reps()`, lines 635-736.
Specifically lines 678-688 (element decode + Counter accumulation + normalisation).

`_ELEMENT_MAP` (the element encoding table): same file, lines 310-313.

Invocation chain (for Path X re-fire):
1. `wave5_season_orchestrator.py:2334` — `_run_pm1_on_phase4_archive()`
2. `phase5_pm1_multimodal_clustering.py:run_pm1_clustering()` — calls `_compute_cluster_reps()` per cluster
3. `phase5_orchestrator.py:pm1_result_to_faction_clusters_input():3121` — passes `cluster.element_distribution` directly into the faction_clusters_input dict
4. `phase5_orchestrator.py:run_phase5_wave_a_sync()` — LLM Wave A receives `element_distribution` as input

---

## Q1: Data source

The aggregator does NOT operate at chain level. It operates at **kit level, via a single ordinal-encoded float per kit** (`element_encoded` in `PM1KitVector`).

The data source path:
1. `_build_pm1_kit_data()` (`wave5_season_orchestrator.py:322-348`) reads `kit.element` (a string, e.g. `"physical"`) and passes it as `"element": element` in the kit_data dict.
2. `build_kit_feature_vector()` (`phase5_pm1_multimodal_clustering.py:382-383`) encodes it: `element_encoded = encode_categorical(kit_data.get("element", "fire"), _ELEMENT_MAP)`.
3. `_compute_cluster_reps()` (lines 678-685) reverse-decodes each kit's `element_encoded` float back to an element name using `min(_ELEMENT_MAP, key=lambda k: abs(_ELEMENT_MAP[k] - kv.element_encoded))`, then builds a Counter over those decoded names.

Matt's working hypothesis (chain-level aggregation) is incorrect. The actual mechanism is simpler and more direct: single kit-primary-element encoded as float then decoded. The chain-level framing does not apply.

---

## Q2: Physical handling

**Physical is entirely absent from `_ELEMENT_MAP`** (line 310-313):

```python
_ELEMENT_MAP = {
    "fire": 0.0, "water": 0.143, "earth": 0.286, "wind": 0.429,
    "lightning": 0.571, "holy": 0.714, "shadow": 0.857,
}
```

Seven elements only. No physical.

When a physical-primary kit is encoded at line 382-383:
`encode_categorical("physical", _ELEMENT_MAP)` → key `"physical"` not in map → returns `default=0.5`.

When that `element_encoded=0.5` is later decoded in `_compute_cluster_reps` (line 681):
`min(_ELEMENT_MAP, key=lambda k: abs(_ELEMENT_MAP[k] - 0.5))`

The two nearest entries are wind (0.429, dist=0.071) and lightning (0.571, dist=0.071). Due to floating-point arithmetic under CPython 3.12, `abs(0.571 - 0.5)` evaluates to a value slightly less than `abs(0.5 - 0.429)`, making lightning the tie-break winner:

```
wind:      abs(0.429 - 0.5) = 0.07100000000000001
lightning: abs(0.571 - 0.5) = 0.07099999999999995   <- wins by FP epsilon
```

**Empirical verification**: 

Simulating season_001 C1 (earth=5, physical=3, fire=2, wind=1, lightning=1, holy=1; n=13):
- 3 physical kits each encode to 0.5, each decode to "lightning"
- Final Counter: earth=5, lightning=4, fire=2, wind=1, holy=1
- Normalised: earth=38%, lightning=31%, fire=15%, wind=8%, holy=8%

This matches Matt's reported output exactly. Physical disappears; lightning absorbs all 3 physical votes.

The same arithmetic applies consistently across all STR-primary kits in C2 and C3 (and 002/003), producing the systematic 3-4x lightning over-representation Matt observed.

**Physical-handling conclusion**: Physical is not excluded, re-routed to a substitute, or suppressed in output. It is encoded as the sentinel default (0.5) and then decoded as lightning via floating-point tie-break. It is a silent map-miss bug, not an intentional exclusion.

---

## Q3: Stale-cache concern

**No stale-cache concern.** There is no `cluster_aggregate_log` that gets written and re-read on Path X re-fire.

The full re-computation path on Path X re-fire (`start_from_phase=5`):
1. `_load_phase4_archive_for_pm1()` — reads `kit_archive.db` + `phase2_kit_candidates.json` fresh (lines 2326-2329)
2. `_run_pm1_on_phase4_archive()` — calls `run_pm1_clustering()` fresh; builds new `PM1ClusteringResult` in memory (line 2334)
3. `pm1_result_to_faction_clusters_input()` — reads `cluster.element_distribution` from the freshly-computed result (line 2370)
4. `run_phase5_cohesion_judge()` — calls LLM Wave A with the fresh (but still buggy) input (line 2399)

The bug is structural (missing map entry), not cached. Every fresh Path X re-fire produces the same skewed output as long as `_ELEMENT_MAP` excludes physical. No retroactive stale data concern.

One nuance: the existing `phase5_faction_clusters.json` files (seasons 001/002/003) were written with the buggy aggregator output. They are not stale in the sense of being read back during re-fire — they are overwritten by each re-fire. The bug will persist in any re-fire until `_ELEMENT_MAP` is corrected.

---

## Hypothesis verification

Matt's working hypothesis (chain-level aggregation + physical exclusion + lightning-fallback or re-normalization) is **partially correct in outcome but incorrect in mechanism**.

Correct: physical is absorbed into lightning, and physical shows 0% in output.
Incorrect: the mechanism is not chain-level. It is kit-level float encoding with a missing map entry.

The numbers reconcile under the following model:
- **Kit-level encoding with physical→default(0.5)→lightning decode via FP tie-break**
- All 3 reconciliation models in the dispatch framing (chain-level variants) are superseded by this simpler explanation

Numerical confirmation run:
- C1 n=13 input: earth=5, physical=3, fire=2, wind=1, lightning=1, holy=1
- Aggregator output: `{'earth': 0.385, 'lightning': 0.308, 'fire': 0.154, 'wind': 0.077, 'holy': 0.077}`
- Matt reported: `earth 38%, lightning 31%, fire 15%, wind 8%, holy 8%`
- Match: exact (within rounding)

---

## Remediation scope

**Small. Single-line fix in `_ELEMENT_MAP` plus one-character default change.**

The fix has two parts:

**Part 1 — Add physical to `_ELEMENT_MAP`** (`phase5_pm1_multimodal_clustering.py` line 310-313).

Physical needs an ordinal position. Options:
- Append at end: `"physical": 1.0` (pushes shadow to 0.857, fine — shadow already at 0.857; physical at 1.0)
- Insert at ordinal position appropriate to design intent

The encoding value doesn't need to be "correct" in any semantic sense — it just needs to be distinct from all other values so the round-trip encode→decode produces "physical" not "lightning".

Suggested: insert `"physical": 1.0` as 8th entry. This is a 1-line add.

**Part 2 — Update `element_attr` comment on line 150** (cosmetic; `PM1KitVector.element_encoded` docstring says "fire/water/earth/wind/lightning/holy/shadow" — add physical).

No changes required in:
- `_build_pm1_kit_data()` — already passes `element="physical"` correctly (line 344)
- `pm1_result_to_faction_clusters_input()` — pass-through
- `phase5_orchestrator.py` — reads `element_distribution` as-is; no filter on physical

**Retroactive re-fire impact:** after the fix, existing seasons 001/002/003 need Phase 5+ re-fire to correct faction names + Wave-S names. Matt-estimated ~$0.20 across 3 seasons per hive-mind-state § 5405. Rocket retroactive re-fire dispatch is a sequential follow-on (per hive-mind-state routing § 4-5).

**Design question for gandalf (not blocking remediation):** should physical be included in the element_distribution LLM prompt at all, or filtered pre-LLM with a note about STR-physical faction composition? The fix above (include physical) is correct and minimal; gandalf may want to add framing context in the Wave A prompt about what physical means thematically. This is a gandalf coordination question surfaced post-fix.

---

## Instance 6 composition note

This finding is **Instance 6 #7** (candidate per hive-mind-state § 5377). Jack-ryan is running parallel Disc #42a framing-audit.

Family classification: **substrate-led discipline drift at aggregator/encoding layer**. The substrate pipeline correctly emits `element="physical"` for STR kits (Amendment 7 operationalizes this canonically). The PM-1 encoding map is a downstream consumer that was never updated to include physical when physical was added as a canonical element (LC-012 fix 2026-05-21 per MEMORY.md). The LLM (Wave A) receives biased input and names factions accordingly — it is behaving correctly given what it receives. Substrate-led discipline intact at substrate + generation layer; broken at encoding-layer consumer.

This is structurally parallel to Amendment 7a (per-chain element wiring fix): in both cases the per-kit or per-chain physical wiring is set correctly at the source, but a downstream layer (PM-1 encoding vs skill emitter) drops or mis-routes physical. Same family of bug; different layer.
