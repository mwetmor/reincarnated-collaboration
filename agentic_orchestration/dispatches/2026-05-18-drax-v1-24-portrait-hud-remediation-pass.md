# 2026-05-18 — drax — v1.24 portrait HUD remediation pass (galadriel-diagnosed)

**Authority:** Matt directive 2026-05-18 evening: *"help drax fix the portrait HUD clipping"* + *"tell drax to start"*. Per hive-mind § 6.1 cross-seam coordination + agent-definition § Cross-seam coordination (drax-galadriel critique-pair pattern). Knight-rider may amend if needed; the dispatch is dropped in by galadriel because the diagnosis is galadriel-authored evidence and Matt directed direct routing.
**Type:** Pattern B; ~90 min total wall-clock if all 4 land in one pass; each independent + pickable subset.
**Predecessor:** galadriel handoff brief (`agentic_orchestration/galadriel/reports/2026-05-18-drax-portrait-hud-handoff-brief.md`) — landed at commit `0be487e`; hive-log HANDOFF entry posted.
**Status:** 🟢 **ACTIVE — drax: START.**
**Tag intent:** `drax/v1.24-portrait-hud-remediation-pass-1` (local; ADR-006 honored by drax).

---

## TL;DR

The benchmark report (`canonical/story/visual-benchmark-vs2a-2026-05-18.md`) § 5.1 rank-1 dissonance is "portrait viewport CLIPS the demo's actual HUD." Galadriel's diagnosis decomposes this into **three independent, mechanically fixable root causes** + one bonus audit. The work is not a redesign — it's surgical fixes to existing render bugs.

Read the brief in full for context. The capsule:

| # | File | Symptom | Fix path | Effort |
|---|---|---|---|---|
| 1 | `src/ui/diabloHud.ts:11-16` | Resource globe off-canvas; HP globe mid-screen-not-bottom | Live-binding positions (pattern at `potionHud.ts:311-312`) | ~30 min |
| 2 | `src/ui/combatHud.ts:830-840` | "Wave 1 of 11" jagged double-strike | Y-spacing proportional to font height | ~15 min |
| 3 | `src/mobile/touchHotbar.ts:90-94` | Ability buttons "invisible" against dark scene | Lighter+more-opaque BG + thicker accent outline | ~15 min |
| 4 (bonus) | `src/ui/seasonSelector.ts` (suspected) | Menu-surface portrait rendering anomaly (rubric § 6.3) | Single-file audit; same root cause family as #2 likely | ~30 min |

---

## Why this is a galadriel→drax dispatch (not knight-rider→drax)

Per hive-mind mode (operating mode change § 2.1): "Knight-rider authors a scope-of-work document; specialists execute against it continuously; per-task dispatches become check-in markers rather than authorization gates." Galadriel-authored evidence + Matt-directed routing converts a brief into a check-in dispatch directly. Knight-rider's role is observed but not blocked-on; knight-rider may amend if a different sequencing is needed.

Per agent-definition § Cross-seam coordination: *"With drax: evidence supply. When galadriel surfaces a visible dissonance, drax decides whether and how to address it in implementation. Drax may consult galadriel on technical render details."*

The brief is the evidence. The dispatch is the start signal.

---

## Required reading (in order)

1. **`agentic_orchestration/galadriel/reports/2026-05-18-drax-portrait-hud-handoff-brief.md`** — full diagnosis + remediation paths + verification protocol. Drax reads this in full. Everything below is meta.
2. `canonical/story/visual-benchmark-vs2a-2026-05-18.md` § 5.1 — the rank-1 dissonance the work closes
3. `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/capture.png` — the broken picture
4. `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/desktop-1920x1080/capture.png` — the working picture (same demo, same SHA — proves the HUD architecture is sound)

---

## Sequencing recommendation (drax's call)

Galadriel recommends the order in § 5 of the brief (DiabloHud → CombatStatus → TouchHotbar → audit). Rationale: globe-coords is the highest visual leverage (the resource globe is COMPLETELY MISSING currently); wave header is the next-loudest broken element; touchHotbar visibility is the third. The audit is cleanup. But drax may reorder per implementation logic (e.g., if the typography helper change for #2 affects more files than expected, do it last so the diff is contained).

---

## Out of scope

- Atmospheric layer dissonance (rank-2 of benchmark report § 5.2). Separate diagnosis path; galadriel offers a second brief if drax wants. **Do not address in this pass.**
- Color register dissonance (rank-3 § 5.3). Gandalf design-direction call pending; drax should NOT pre-emptively warm the scene palette without that resolution.
- Town surfaces (§ 6.1). L3-RESOLVED to (a) — Phase-2+ scope. Not this pass.
- Capture-timing artifact (§ 6.4). Future D11.5 v2 work for `combat-midfight-paused` variant. Not this pass.
- Engine code (any path in `reincarnated-engine/`). Drax stays demo-side.
- The full v1.7 § 3.5 portrait remap — already shipped at drax/v1.21. This pass corrects three specific render bugs in that remap's wake.

---

## HARD NOs (per overnight sprint § 6 still in effect)

- No `git push --force`
- No vendor acquisitions
- No CLAUDE.md / AGENTS.md modifications
- No Phase-1 P1 scope changes

---

## Completion handoff (drax)

When the pass completes (one fix or all four):

1. Append completion record to this dispatch
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline) recording which root causes were addressed + smoke-test notes + new demo SHA
3. Local tag: `drax/v1.24-portrait-hud-remediation-pass-1`
4. Galadriel discovers the new SHA via normal hive-scan; re-captures + re-scores axis 3.4 asynchronously (non-blocking; ~10s capture + ~30 min re-score)
5. Updated benchmark report § 4.1 + scoring.json land via galadriel commit; no drax action required for re-score

---

## Open consult points (drax → galadriel mid-fix)

Per § 7 of the brief — drax may ping galadriel for:

- **Mid-fix render check.** After fixing #1 globes, galadriel can re-capture and confirm positioning before #2 + #3 land. Useful if drax wants to validate position guesses against the actual rendered output before continuing.
- **A/B color choice for #3.** If `0x1a2530` doesn't read well, galadriel can test 3–5 candidate colors and visually rank them.

Galadriel is continuously available per hive-mind protocol § 3.3 spirit. Drax does not file a request-and-wait; drax pings in the hive log; galadriel responds in real-time when present.

---

## Verification (galadriel-side, async, non-blocking)

When new demo SHA lands:
- `node capture.mjs --state combat-midfight --viewport mobile-portrait-1290x2796` (~10s)
- Side-by-side: new PNG vs prior PNG vs DoE reference
- Re-apply rubric axis 3.4 (typography + UI register) scoring
- Update `scoring.json` + benchmark report § 4.1 + hive-log STATE
- If aggregate moves materially, update report § 0 TL;DR

Galadriel does NOT block drax's pivot to next work; re-score lands when it lands.

---

*Dispatched 2026-05-18 evening by galadriel per Matt directive. Diagnosis: galadriel. Implementation: drax. Re-score: galadriel. The Mirror has named what it saw; the smith works the iron now.*
