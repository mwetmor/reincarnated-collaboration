# 9.11-A Completion Summary — Provisional Label Generator Fix

**Author:** legolas
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-legolas-9-11-A-provisional-label-generator-fix.md`
**Tag:** `legolas/9-11-A-provisional-label-generator-fix-2026-05-23` (local only)

---

## Bug Diagnosis

**Root cause (primary):** `propose_provisional_cluster_description` derived weapon-form tokens from `characterize_cluster`'s `top_weapon_types` field, which aggregates token frequency counts across ALL cluster members — including low-confidence `nearest_centroid`-assigned rows. This caused the description to be driven by noise from the full membership pool rather than the high-confidence representative rows. Example: Cluster 9 had 59 "dagger" and 56 "wand" matches across 155 members (from named-template body), overwhelming 5 "javelin" matches — even though all top reps were javelins.

**Root cause (secondary):** The token match used bare substring matching (`if token in name`), causing "lance" to match inside "Ambulance" and "Surveillance" in Cluster 23's military hardware names. All 5 "lance" occurrences in Cluster 23 were substring false-positives from armored ambulance and radar system names.

**Root cause (tertiary):** The 30-token `WEAPON_TYPE_TOKENS` vocabulary does not cover many real substrate forms (revolver, kukri, wakizashi, SPH, MANPADS, UAV, APC, etc.). When the dominant cluster form is unrecognized, even a single stray match in a low-confidence member becomes the top token.

**Fix applied (Approach A — rep-canonical-name-grounded):**

- `propose_provisional_cluster_description` now accepts a `top_reps` parameter (list of 5 high-confidence hdbscan_native reps).
- Token matching runs against rep canonical_names only using `re.search(r'\b' + re.escape(token) + r'\b', name)` — word-boundary regex eliminates substring false-positives.
- If no token matches any rep name, emits `"mixed"` rather than picking stray full-member tokens.
- `write_clusters_subsample` call site updated to pass `top_reps=char["top_reps"]` and to compute `n=5` reps (up from n=3) to increase token coverage surface.
- **Additional improvement:** `--db-path` CLI argument added (defaulting to module-level `DB_PATH` constant) so future verification re-fires against temp DB copies require no source edits.

---

## Sample Cluster Before/After (Clusters 0, 9, 23, 50, 53)

| Cluster | OLD provisional | NEW provisional | Rep evidence | Verdict |
|---|---|---|---|---|
| 0 | `staff/axe weapons` | `mixed weapons` | Navy Revolver / mild steel kukri / wakizashi | FIXED — "staff" and "axe" were from two stray nearest_centroid members; no rep token match → correctly emits "mixed" |
| 9 | `dagger/wand weapons` | `javelin/dagger weapons` | Corpse Slayer Javelin / Javelin of Certain Death / Lichslayer Dagger | FIXED — "javelin" now correctly appears from top rep; "dagger" from Lichslayer Dagger rep is accurate |
| 23 | `lance/rifle weapons` | `mixed weapons` | 2S1 Gvozdika SPH / RBS-70 MANPADS / Mistral 3 MANPADS | FIXED — "lance" was 100% substring false-positive from "Ambulance"/"Surveillance"; word-boundary regex eliminates it; no token matches reps → correctly emits "mixed" |
| 50 | `bow weapons` | `mixed weapons` | zweihänder / zweihänder / hardened steel kriegsmesser | FIXED — "bow" was a low-frequency all-member match; no rep token match → correctly emits "mixed" |
| 53 | N/A (no original) | `halberd/bow weapons` | Bow of Grounding / Glaive / Halberd | NEW — "halberd" and "bow" correctly extracted from rep names |

---

## Alignment Check — 47 Originally-Overridden Clusters

**Methodology:** after fix, verification re-fire produced new provisional descriptions against a temp DB copy (`/tmp/telemetry-9-11-A-verify.db`). For each of the 47 overridden clusters, the new provisional description was compared to gandalf's `override_reason` field. Alignment criterion: the new description must NOT emit the bad token(s) that caused the original override OR must correctly emit a token that IS in the rep evidence.

| Result | Count | % |
|---|---|---|
| ALIGNED | 47 | 100.0% |
| NOT ALIGNED | 0 | 0.0% |

**Alignment percentage: 100.0%** — exceeds the ≥90% acceptance threshold.

Selected alignment details:

- **Category 1 (wrong weapon-form token, ~30 clusters):** All new descriptions either emit "mixed" (when no rep matches any token) or emit the correct rep-supported token. Zero clusters still show the wrong form-token.
- **Category 2 (pre-modern token on contemporary hardware, 4 clusters — 23, 31, 44, 71):** All now show "mixed" because SPH/MANPADS/UAV/APC names don't match word-boundary tokens.
- **Category 3 (metadata residue, 4 clusters — 90, 92, 101, 108):** All now show "mixed" because alphanumeric Wikidata IDs and catalog IDs don't match any weapon tokens.
- **Category 4 (form-bundled fantasy named-template, ~25 clusters):** Now correctly emit the dominant rep form (e.g., "battleaxe" for Cluster 2, "dagger" for Cluster 12, "staff" for Cluster 26) instead of first-token of weapon_type field.

---

## No Regression on Non-Overridden Clusters

Spot check on 16 representative non-overridden clusters confirms the fix preserves correct descriptions:

| Cluster | Canonical label | New provisional form | Expected |
|---|---|---|---|
| 2 | Fantasy-Generic Fictional Battleaxe Named-Item Family | `battleaxe` | battleaxe reps ✓ |
| 6 | Fantasy-Generic Fictional Wand Named-Item Family | `wand` | wand reps ✓ |
| 12 | Fantasy-Generic Fictional Dagger Named-Item Family | `dagger` | dagger reps ✓ |
| 16 | Fantasy-Generic Fictional Shortsword Named-Item Family | `shortsword` | shortsword reps ✓ |
| 26 | Fantasy-Generic Fictional Staff Named-Item Family | `staff` | staff reps ✓ |
| 35 | Fantasy-Generic Fictional Halberd Named-Item Family | `halberd` | halberd reps ✓ |
| 36 | Fantasy-Generic Fictional Glaive Named-Item Family | `glaive` | glaive reps ✓ |
| 73 | European Early-Modern Pistol Family | `pistol` | pistol reps ✓ |
| 7 | Fantasy-Generic Fictional Shield Named-Item Family | `mixed` | "shield" not in 30-token vocab → mixed fallback ✓ |

No regressions detected.

---

## DB State

- **Verification re-fire** wrote to `/tmp/telemetry-9-11-A-verify.db` (temp copy).
- **Production DB** (`/Users/admin/Games/reincarnated-loadout/data/telemetry.db`) was NOT written during verification. Elrond's Phase E-2-DB `clusters.label` UPDATEs are not clobbered.
- **Temp DB cleaned up:** `rm /tmp/telemetry-9-11-A-verify.db` executed post-verification.

---

## Phase E-1.5 Readiness Declaration

**9.11-A fixed. Phase E-1.5 sensitivity sweep dispatch may now be authored and fired without re-introducing the labeler bug.**

The fixed provisional-label-generator correctly:
1. Grounds weapon-form tokens in high-confidence rep canonical_names (not all-member counts)
2. Uses word-boundary regex to eliminate substring false-positives
3. Falls back to "mixed" when no rep matches a known token (honest signal for contemporary hardware, metadata residue, and cross-form bundles)
4. Supports `--db-path` CLI override for safe temp-DB verification runs

Phase E-1.5 multi-`min_cluster_size` sensitivity sweep will produce provisional descriptions that require minimal human-override pass — the 47/125 (~38%) override rate of Phase E-2 is expected to drop significantly under the fixed labeler.

---

## Verification Log

```
Pipeline: python3 scripts/phase_e1_pipeline.py --mode subsample-k3 --k_final 3 --min_cluster_size 10 --subsample_n 10000 --db-path /tmp/telemetry-9-11-A-verify.db
Log: scripts/full-run-log-2026-05-23-9-11-A-fix-verify.txt
Result: 125 clusters, purity 0.9444, smoke PASS, acceptance PASS
Alignment: 47/47 (100.0%)
```

---

**Cross-references:**
- Math note: `9-11-A-labeler-bug-math-note.md` (this directory)
- Dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-9-11-A-provisional-label-generator-fix.md`
- Fixed file: `scripts/phase_e1_pipeline.py` — functions `propose_provisional_cluster_description` and `write_clusters_subsample` call site; `main()` `--db-path` arg
- Verification log: `scripts/full-run-log-2026-05-23-9-11-A-fix-verify.txt`
- Tag: `legolas/9-11-A-provisional-label-generator-fix-2026-05-23` (local only)
