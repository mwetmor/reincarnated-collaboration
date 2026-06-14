# Stage-3 BC-coordinate-cutover scoping ruling — narrow deletion + Stage 3b

**Type:** scoping ruling (gandalf seam) — the §7 prove-then-delete gate applied at PATH granularity to the irreversible Stage-3 deletion.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-ruled 2026-06-14 (Pattern-B): "delete the start-of-pipe archetype tag... but hold the physical portion."
**Companion docs:**
- KR Stage-2-closure report 2026-06-14 (both gate-halves PASS; Stage 2 closed; behavior-identical).
- jack-ryan Gate-2 finding (smuggling-trap closed in code — `bc_target_role_priority` takes only the 8-tuple; tables demoted, not deleted).
- gandalf §7 prove-then-delete gate (the BC-cutover design gate this ruling instantiates).

---

## 0. TL;DR — the ruling

Stage 3 is **NARROW + an explicit Stage 3b**:

- **Stage 3 (now, gated):** physically delete the start-of-pipe archetype-tag machinery that the ELEMENTAL (coordinate-composed) path has abandoned — the subset of KR's full-deletion list the physical fallback does NOT touch. Makes the **elemental-path lock structural** (nothing to revert to).
- **Stage 3b (deferred):** delete the physical fallback (at minimum `ARCHETYPE_ROLE_PRIORITY` + `legacy_archetype_shim` + any physical templates). **Re-open criterion: physical-pool expansion landing** (moves physical kits onto the coordinate, making the fallback truly inert).

**The irreversible cut fires only AFTER** both read-only prereqs clear (§3) AND gamora's reference-audit pins the exact elemental-only deletion set (§2). Prove, THEN delete. KR brings the final go back to Matt.

## 1. Why narrow on the merits (not just caution)

The cutover's irreversibility payoff = permanently closing the label-as-input smuggling trap. That payoff is earned **per-path, and only on a path proven to no longer need the label.**

- **Elemental path: PROVEN.** Stage 2 — 16/16 PASS, L1=0.000, zero label-input in the live path; jack-ryan verified the code takes only the 8-tuple. The payoff is earned → make it structural.
- **Physical path: NOT proven inert + deliberately deferred.** Physical kits still ride the legacy fallback; the physical-pool expansion that would move them onto the coordinate is the work Matt *chose* to defer. The payoff isn't earned there yet, and the fallback may still be load-bearing.

Deleting a still-live, deliberately-deferred path now to chase completeness-of-deletion would fight the deferral decision made on purpose. Same logic as the earth_caster cut: delete the over-claim that fires at frequency 0.0000, never the path still firing.

## 2. The carve — principle, not blind enumeration

The exact deletion set is a **gamora/rocket reference-audit**, held to this principle:

- **DELETE:** symbols referenced ONLY by the elemental/coordinate path (the elemental `ARCHETYPE_TEMPLATES`, the elemental-only `V-D1..V-D6` deprecated-residents, `_PLAYER_CONTROLLER_ARCHETYPES` *if* elemental-only).
- **HOLD (→ Stage 3b):** anything the physical fallback still touches — at minimum `ARCHETYPE_ROLE_PRIORITY` (the demoted table physical still keys against) and `legacy_archetype_shim` (the bridge physical kits use), plus any physical templates.

I do NOT enumerate the exact set blind. gamora's reference-audit determines which symbols are elemental-only vs. physical-shared. **Design gives the principle; the audit gives the list.** (Note: `ARCHETYPE_ROLE_PRIORITY` is shared — elemental demoted it in Stage 2, physical still keys against it — so it is HELD, not deleted, under the narrow scope.)

## 3. The two prereqs that gate the irreversible cut (prove-then-delete)

1. **Full-season elemental zero-label proof run** (read-only, non-destructive). Pass criterion: across a full season, **zero label-input firing attributable to any elemental/coordinate-composed kit.** Physical-fallback kits firing label-input is EXPECTED and does not fail the proof — but the instrumentation must **attribute** firing to elemental-vs-physical so an elemental leak cannot hide behind expected physical firing (discrimination-law-at-the-instrument; same discipline as M1.3.5). Side benefit: reveals whether current seasons generate any live physical kits — informs when Stage 3b can fire.
2. **drax demo-VFX coupling pre-check** (read-only). The Pixi.js demo may key class VFX overlays on the legacy label (`main.ts` 1509 / 2108 / 2243). Sweep before deletion — **the Pixi demo is still the live surface (Godot is a spike, not a commit).** If the demo reads a to-be-deleted symbol, re-point it to the coordinate first.

The deletion fires only after BOTH clear and the §2 reference-audit pins the set.

## 4. drax co-brief (Pixi sweep + Godot coordinate-clean)

The drax demo-VFX pre-check (sweep the Pixi label-coupling) and the Godot vertical-slice spike are the SAME underlying move: VFX keys on the **coordinate, never the label.** Co-brief them so the Godot build starts coordinate-clean from the first frame and never re-imports the trap we are spending three stages to delete. This also resolves the drax-queue collision: the tiny Pixi sweep + the larger Godot spike, one agent, one brief.

## 5. Disposition / routing

- **KR:** commission the two read-only prereqs (§3) now; HOLD the irreversible cut for Matt's final go post-proof; sequence the drax co-brief (§4).
- **gamora (with rocket for generation-side symbols):** the reference-audit (§2 carve) + the full-season elemental zero-label proof run (§3.1, attribution-instrumented).
- **drax:** the demo-VFX coupling sweep (§3.2), co-briefed with the Godot spike.
- **Stage 3b:** parked; re-open criterion = physical-pool expansion landing.

---

**Signed:** gandalf, 2026-06-14
**For:** the Stage-3 scoping ruling — narrow the irreversible deletion to the elemental-abandoned start-of-pipe archetype-tag machinery (the §7 prove-then-delete gate at path granularity), hold the physical fallback to an explicit Stage 3b gated on physical-pool expansion, and fire the cut only after the full-season elemental zero-label proof + the drax demo-VFX sweep clear and gamora's reference-audit pins the exact elemental-only set.
