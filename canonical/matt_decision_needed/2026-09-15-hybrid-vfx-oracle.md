# Adopt a hybrid VFX outcome oracle (Hades timing + Children of Morta / Slormancer legibility)?

> **STATUS:** OPEN — filed by gandalf (ARCHITECT) 2026-09-15, fork R-C3-118; Matt deferred the ruling until a VFX built to the spec is seen (R-C3-120) and then to the VFX session's size step (R-C3-123). Blocks: the oracle reference file the sheets are measured against (`oracle/vfx_reference_hades.json` today).

**Recommendation (one): adopt the hybrid** — Hades keeps the *timing* bands (strike rise 0–1 frames, decay curve, half-life; the only measured flipbook timing we have); Children of Morta + The Slormancer supply the *legibility* bands measured on painted-pixel ground (near-white ≤ 2 %, halo +.16–.41 over ground, floor light +.07–.09, burst extent 3–6 BH, saturated banded cores, S median ≥ .5). Take the ruling **after the size/timing clips exist** (VFX session step 2) so the extent band is set against our own screen scale, and give `holy` / `field` classes their own band set (T3v `element_class`).

**Options:** A. Hades-only as today (keeps a white-core target the painted-pixel evidence contradicts). **B. Hybrid (recommended).** C. CoM/Slormancer only (loses the only timing numbers).

**Evidence:** `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md`; `…/2026-09-15-chronicon-com-slormancer-vfx/findings.md`; style card v0.2.
