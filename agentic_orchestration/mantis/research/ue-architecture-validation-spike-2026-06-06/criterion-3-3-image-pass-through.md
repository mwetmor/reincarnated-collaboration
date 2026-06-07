# Criterion 3.3 — Image-Pass-Through-to-Meshy Validation

**Verdict:** BLOCKED (Meshy API key required)
**Date:** 2026-06-06 Session 1

---

## Blocking gate

Same as criterion 3.1 — Meshy API key required.

---

## Pre-work: weapon selection and path protocol

Per dispatch § 4 test pattern: select 3-5 weapons from museum-tier substrate subset.

### Routing protocol (from canonical/story/asset-pipeline-meshy-swap-2026-05-22.md)

- **Path 1 (direct pass-through):** substrate image URL → fetch + cache → quality-score gate → Meshy 6
- **Path 2 (ChatGPT-gen intermediate):** image description → ChatGPT (gpt-image-1) → coherence gate → Meshy 6
- **Pass condition:** Path 1 equal-or-better on ≥4/5 weapons → lock direct-pass-through as production default

### 5 weapon nominations (ready for execution when unblocked)

Selected from known museum-tier substrate sources (Royal Armouries + Met Museum, Tier-1 per canonical/story/asset-pipeline-meshy-swap-2026-05-22.md § 3.6.4):

| # | Type | Source | Notes |
|---|---|---|---|
| W1 | Standard sword (claymore type) | Royal Armouries | Tier-1, landscape format, prior Sidecar A confirmed PASS for Path 1 |
| W2 | Crossbow | Met Museum | Tier-1, compound object (crossbow + cranequin), Sidecar A N=1 PASS |
| W3 | Polearm / halberd | Royal Armouries | **Tier-1 EXCEPTION — portrait format** → routes to Path 2 per canonical interim policy |
| W4 | Katana or Japanese sword | Met Museum or Royal Armouries | Tier-1 but different cultural register from W1; tests cultural diversity of Path 1 |
| W5 | Bow or ranged weapon | Museum source | Tests non-weapon_form_physical substrate path |

Note: W3 is assigned to Path 2 per the interim polearm-portrait policy. This weapon validates the policy correctly identifies and routes the exception. It does NOT count against Path 1 acceptance score per the policy.

### Sidecar A prior work composition

`agentic_orchestration/star-lord/research/image-pass-through-vs-llm-gen-meshy-comparison-2026-05-23/comparison.md` contains prior Sidecar A findings (MIXED verdict, 5 weapons × 2 paths). This criterion 3.3 is effectively Sidecar A.2 — extending the sample to confirm stability of Tier-2 verdict and further characterize the polearm exception.

Key Sidecar A findings (already established, do not re-test):
- Claymore (Tier-1, standard): Path 1 SUPERIOR ✅
- Crossbow (Tier-1, compound object N=1): Path 1 CONFIRMED ✅
- Halberd (Tier-1, portrait polearm): Path 1 FAIL → Path 2 mandatory ✅
- Barrett M82 (Tier-2, ~700px): Path 1 PARITY (N=1, not yet stable)
- Yellow Quartz Longsword (Tier-3, game-render, 99×134px): Path 2 mandatory ✅

---

## Does NOT affect criterion 3.2 verdict

Criterion 3.3 validates the image-pass-through pipeline, not the UE import pipeline. 3.2 uses Meshy output regardless of which input path was used. 3.3 PASS strengthens the case for production-path viability; 3.3 RED changes the Meshy input path but not the UE side.

---

*Criterion 3.3 status: BLOCKED — same gate as 3.1. Weapon nominees ready; execution within one session of unblocking.*
