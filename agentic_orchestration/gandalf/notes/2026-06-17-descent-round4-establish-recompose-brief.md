# Round-4 Establish RECOMPOSE Brief — Descent Scene (drax)

**STATUS:** GO — fires now. The 6 chambers are GREEN (galadriel iter6 re-score, commit `3b679cb`: 6/6 pass both gates). **Establish ×3 is the ONLY remaining non-green still** — gated on COMPOSITION, not light. This is the last piece to close the run-to-green.
**Author:** gandalf (design steward, run-to-green orchestrator). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md` (the run-to-green tracker; Round-3 establish DESIGN DIRECTION section is the authority for this — read it).
**Scope:** **CAMERA-ONLY.** Do NOT touch the chamber lighting rig — it just landed GREEN; perturbing it re-opens a closed gate.

---

## 0. The problem (galadriel + gandalf both confirm, independent eyes)

The establish shot fails on COMPOSITION. Its light improved (+5 LDR from the global rig) but three residuals remain, and one DOMINATES:

1. **★ THE DOMINANT FAILURE — a wall of flat saturated BLUE slabs** across the left/center band. These are the per-zone **cool** CombatFills grazing the tall stacked deep chamber walls; in the across-spine angle the deep walls present FACE-ON and read as bright flat blue cardboard. They are the single most eye-catching element and pull the eye hard-left, away from the descent. (galadriel: "the blue deep-wall panels DOMINATE the across-spine left band.")
2. Cool spine floor (warmCool 0.988 — faintly cool, not warm-dominant).
3. No focal payoff anchoring the deep end.

**Note the irony:** the same ACES-contrast + ambient-0.17 global rig that FIXED the chambers SHARPENED this — a deeper surround makes the cool blue slabs pop harder. The fix is NOT to undo the rig (the chambers need it); it is to RECOMPOSE the camera so the blue walls stop presenting face-on.

---

## 1. The design direction — katabasis (the WHY, so your camera judgment is grounded)

An establishing shot for a DESCENT is *katabasis* — the oldest journey-pattern. **Its power is mystery + downward-pull, NOT a full-map reveal.** You descend INTO the unknown; you do not see the bottom from the top. This dissolves the geometry conflict you correctly named (across-spine = blue deep-walls; down-spine = magenta-but-worse-blue):

- **DROP the "plant the magenta focal payoff" ask entirely.** The magenta sanctum is the DESTINATION — a destination revealed from the threshold is robbed of arrival. It already reads premium in its OWN zone cam (where the player arrives). Showing it in the overview deflates the descent. **Residual #3 is therefore not a defect to fix — it's a reveal we deliberately withhold.** Do not frame the deep end to show the sanctum.
- **The hero of the establish is the WARM NEAR-CLUSTER + the felt downward step,** not the deep end. Gold braziers large in the foreground; the spine recedes into green-fog mystery with warm brazier-points as breadcrumbs trailing into the dark.

## 2. The fix — Option 1, CAMERA-ONLY (chosen; lowest risk)

Recompose `_build_establishing_camera` (~line 2100-2150) so:

- **(a) Deep walls rake EDGE-ON, not face-on.** Drop the camera lower and rotate/offset so the tall deep chamber walls present at a GRAZING angle and recede into the green fog — they only read as flat blue SLABS when face-on. Edge-on + fog-veiled, they become atmospheric depth, not cardboard. This is the single highest-leverage change — it kills the dominant failure.
- **(b) Warm near-cluster LARGE in the foreground.** Frame so the nearest 2-3 chambers' gold braziers fill the foreground as the hero element; the rest steps down and recedes. This is the original code-comment intent (`:2028-2037`: "intimate 3/4 of the upper 2-3 chambers... rest receding into fog") — push it the rest of the way.
- **(c) The spine descends into fog-mystery.** Let depth dissolve into green-fog with warm breadcrumb-points; do NOT light the deep end to a destination.
- **warmCool should improve as a SIDE EFFECT of (b)** — more warm braziers + fewer cool deep-walls in frame raises the warm fraction without adding a single light. If it doesn't fully warm, that's secondary; the blue-slab kill + the felt descent are primary.

**Do NOT:** add wall-wash/deep-wall lights (rejected Option 2 — perturbs the combat look + the landed rig); build a down-spine deep-look cam (rejected Option 3 — worse blue + robs arrival). Camera position/rotation/FOV/framing ONLY. (A modest establish-specific fog tweak is acceptable IF needed to veil the deep walls — but prefer pure camera.)

**The 3 establish views:** galadriel reports establish_01/02/03 are currently CV-identical (one framing applied to all three). Your call on the camera architecture: either make them 3 genuinely distinct descent-views (e.g., high-threshold-down / mid-spine / low-near-cluster — a sequence that itself tells the descent) OR consolidate to one canonical establish if 3 identical views are redundant. Whatever reads best as "the wow that sells the descent."

## 3. Process

- **CAMERA-ONLY.** No chamber lighting changes, no geometry, no spawn changes. Parity 35/35 + Gate B hold trivially (camera doesn't touch them) — but confirm.
- **Self-measure** the iter7 establish frames against galadriel's scorer (LDR off the 102 floor; warmCool toward warm). But the PRIMARY gate is COMPOSITION — your eye: do the blue slabs stop dominating? Is the warm foreground the hero? Does it read as a felt downward descent into mystery?
- **Auto-commit** your iter7 work-products (the .gd camera change) with the `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` trailer; **do NOT push** (Matt-gated). Captures git-ignored (Synty-derivative), local only.

## 4. Acceptance (the establish gate — the last gate)

- **Composition (primary):** reads as a felt DOWNWARD descent into fog-mystery; warm-foreground-dominant; **NO blue-slab focus-pull** (deep walls edge-on + fog-veiled, reading as atmospheric depth not flat panels); magenta sanctum NOT shown (deliberate withhold). gandalf rules composition on the rendered iter7 stills; galadriel gives the independent perception read.
- **Light (secondary):** LDR off the 102 floor; warmCool improved toward warm-dominant (≥1.0) via the framing shift.
- **Gate B:** held (camera-only).

## 5. Output

1. iter7 establish captures (×3 or consolidated; local, git-ignored).
2. The camera recipe (position/rotation/FOV that landed it).
3. Your eyes-on read: blue-slab dominance killed? warm-foreground hero? felt-descent? + self-measured LDR/warmCool.
4. Your call on the 3-view architecture (distinct sequence vs consolidated) + why.

---

**Signed:** gandalf, 2026-06-17. Round-4 establish RECOMPOSE — the last non-green still. Camera-only katabasis recompose: rake the dominant blue deep-wall slabs edge-on into fog, warm-near-cluster as the foreground hero, spine into fog-mystery, magenta withheld (destination revealed on arrival, not at the threshold). Chamber rig is GREEN — do NOT touch it. Closes the run-to-green on approval. GO.
