# Gate 3 — Verdict 1 (calibration capture): crypt-vault clear-room node

**Status:** ACTIVE — Matt's first live-editor walk-through verdict on the crypt-vault clear-room node PoC, captured verbatim as calibration data.
**Author:** gandalf (design steward), 2026-06-19, Pattern B dialogue with Matt.
**Parent instrument:** `agentic_orchestration/gandalf/notes/2026-06-19-crypt-vault-node-gate3-coherence-capture.md`
**Why this exists:** brief § 4 — "Matt's verdict + REASONS are calibration samples for the eventual automated coherence judge — this is the HITL investment that removes HITL later." This is the first real corpus of triples.

---

## Verdict: FAIL-WITH-REASONS — but the FOUNDATION PASSED (iterate, do NOT restart)

The structural foundation the PoC was built to prove is **confirmed good by Matt's eye**. The failures are (1) a real F3-class stair failure that is also a Gate-1 escape, and (2) a rich architecture/dressing iteration list. This is "iterate in-loop, re-render, re-judge," NOT "method invalid."

## Confirmed wins (validated negative → positive)

- **F1 (overlapping/copy-paste crypts) — CONFIRMED FIXED.** Matt: *"Nothing is overlapping incorrectly is the biggest win."* The structure-first / locked-grid thesis is validated by the human eye. This was the worst prior failure.
- **F2 (half-hidden doors) — CONFIRMED FIXED.** Matt: *"The open doorways can be entered."*
- **Bonus:** *"The windows are a nice touch."*

## Two governing principles Matt set (these reframe everything)

### Principle 1 — Intent: this is a CLEAR-ROOM (pack/elite, connects rooms)
Matt's question: boss / mini-boss / trash-pack-connector? **Answer (from brief § 3 + the `elite_pack` shell): clear-room — an elite-pack room that stitches to neighbors via entrance+exit sockets.** Therefore Matt's conditional FIRES: *"choose one angle to be the direction that the player camera will face (2.5D diagonal) and then place the second level (gargoyle + stair destination) across from the camera."*

### Principle 2 — Author + judge ONLY what the 2.5D ARPG camera sees (CRITICAL method change)
Matt, verbatim: *"we should only take pictures of what the ARPG 2.5D diagonal 'top-down' camera will see, otherwise we are optimizing for a game the player will never experience - and that's the wrong game."*
- **Adopted.** The acceptance unit collapses from the 15-frame orbit to **the player's committed 2.5D camera** (+ any allowed in-game rotations).
- **Reconciliation with the anti-single-angle-trap rule:** the orbit existed (pre-Gate-1) to stop a single hero shot hiding breakage. Gate 1 (engine-truth, camera-independent) now owns breakage detection — so Gate 2 (register) and Gate 3 (coherence) can and should collapse to the player camera. Audit/orbit angles survive ONLY as internal debug instruments, never the acceptance unit.
- **Evidence the orbit was the wrong acceptance unit:** the orbit set + Gate 1 BOTH passed the broken stairs (A/B/C). Matt's eye caught them. The orbit cost 15 frames and did not catch the real failure.
- **This is likely THE project ARPG camera convention, not just this room's** — set deliberately.

## The triples — (criterion, specific element, what Matt wants instead)

| # | Criterion | Element | What Matt wants |
|---|---|---|---|
| A | F3 (structure) | the stairs | floating in mid-air + facing wrong direction → ground them + correct orientation |
| B | F3/coherence | stair top landing | currently lands at a railing → open the balustrade at the landing |
| C | F4 (support reason) | storey piers under deck | only 1 level tall, reach halfway → must reach the 6 m deck (stack/taller piers) |
| D | coherence | mezzanine ↔ wall intersection | passes through wall, appears other side → CLIP at the wall; AND remove 3 tiles of dead space beyond that wall |
| E | VFX | brazier flames | change shape with camera, too wide/detached → tighten range tightly atop the brazier |
| F | P3 (playable read) | battle area vs walls | battle area stops before walls → fill the gap (annulus) with scene-appropriate scattered LARGER objects to keep combatants in the fighting space |
| G | architecture | the gallery (2nd level) | extend across the MAJORITY of its wall, stop a fair bit before the next wall, end in a railing |
| H | F4 (structure reason) | beneath the gallery | add ARCHES column-to-column as an arcade (self-justifying architecture) |
| I | P1/P2 (life/age) | walls + 2nd-level architecture | dungeon plants, moss, vines — especially around the arches |
| J | wayfinding + theme | floor | carpet running roughly door-to-door (confirms clear-room traversal) |
| K | annulus soft-boundary | non-stair side | slightly raised + railing + a small step you "might try to climb" BUT a fallen column blocks it; raised coffins behind it |

## Gate-1 escape finding (stairs A/B/C) — strengthen criterion 4

Gate-1 crit 4 ("vertical both-ends-land") PASSED (foot y=-0.33, top y=6.99, deck y=6.00) yet the stair is visibly broken. The criterion checks ENDPOINT PROXIES (AABB foot/top y, deck-tile proximity) but NOT: (1) stair ORIENTATION (orthogonal index — climbable face direction), (2) visual GROUNDING (mesh sits on floor vs floats — Synty prefab pivot), (3) landing CLEAR (no railing blocking), (4) SUPPORT reaches the supported deck (piers → 6 m). **gandalf flagged exactly this proxy-vs-reality gap in the Gate-3 package; Matt's walk confirmed it.** Crit 4 must grow these checks. The mezzanine remains BACKDROP (combatants never go up) — but backdrop must be architecturally honest; K's "climbable-looking but blocked" is the correct no-false-affordance handling.

## Sequence Matt set
Camera direction FIRST (Principle 1 conditional) → then solve stairs/2nd-level/supports → then the architecture extensions (G–K). Don't fire piecemeal; lock the camera frame, then commission one coherent rebuild.

## Deferred (recognition → validate → commit; gated on this node passing Matt)
Method canonicalization; render-harness → player-camera-only; Gate-1 crit-4 strengthening canonical write (jack-ryan); the Godot-single-occupant operating discipline (knight-rider sequencing); collider-strip optimization (drax follow-on).
