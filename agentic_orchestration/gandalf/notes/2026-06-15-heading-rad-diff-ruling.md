# heading_rad diff — RULING: presentation-lever, loader-ignore is correct (closes star-lord emitter carry)

**Type:** design ruling (gandalf seam) — resolves the ⚠ callout from star-lord's `arena_scenario_emitter` session.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-conduit 2026-06-15. star-lord routed the `heading_rad` value-correction (`0.0` → `−π/2`) for a design call on whether drax's ArenaRoom loader must consume it.
**Parent:**
- star-lord emitter (engine commit `4b3c1df`; godot `5df86fb`; `MIGRATION.md § v1.77`). jack-ryan Gate-1 CLEAR.
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-parametric-arenaroom-refactor.md` — the parity contract this applies: **spawn POSITIONS sacrosanct; figure facing/scale/dressing/camera are presentation levers.**

---

## 0. The ruling

`heading_rad` is a **presentation-lever field, NOT parity-critical.** The emitter correctly carries the canonical `−π/2` in the JSON (data fidelity); drax's loader correctly **ignores** it and derives facing from a readability rule. **Both are right; no conflict; no loader change needed.** The carry CLOSES — drax need not spend a verification cycle; the answer is confirmed in code below.

## 1. Evidence (code-cited)

1. **Uniform default, not tactical signal.** `heading_rad = −π/2` across all 6 scenarios (`arena.py:179` dataclass default + `:293/428/483/569/651/726` — every entity "facing south toward [mobs/boss/elite]"). A single starting-orientation default, identical everywhere.
2. **The sim overrides it immediately.** Player heading is reset to face the primary target at fight-start (`spatial_engine.py:1132/1139`); every entity re-faces its target each step (`:676/691/743`). The spawn heading lives ~one frame before the AI turns everyone to engage → **essentially zero fight-outcome signal.** Heading *is* read for cone/line/flanking geometry (`:538/566/812`) — but on the **dynamic** heading the AI computes, not the spawn default.
3. **The loader already ignores it.** `_world()` reads only `x`/`y` (`render_arena_room.gd:164`); `_build_combatants` sets facing via `_face()` with rule-derived targets — boss/mini-boss→player, retinue→arena-center, player→marquee (`:349-362`). `heading_rad` is loaded-but-unread.
4. **The rule is MORE faithful than the spec field would be.** Drax's facing rule reproduces the sim's **fight-start** state (everyone turned to engage) — which is exactly the moment galadriel scores (a fight-in-progress tableau across the VFX lifecycle). The literal pre-fight spawn heading (a uniform "everyone facing south") would render a lineup, not a battle — worse for readability *and* less faithful to the scored moment.

## 2. Why the JSON still carries −π/2 (and should)

The JSON is a faithful mirror of `arena.py` — that fidelity is the emitter's entire purpose (parity-by-construction). **Data layer faithful; consumption layer applies presentation rules.** The JSON carrying the true value while the consumer ignores a presentation-lever field is the correct separation, not a contradiction. Drax's bootstrap `0.0` was a hand-typed placeholder; the emitter's `−π/2` is the correction. Good hygiene; inert for the current consumer. star-lord did this right.

## 3. Forward caveat (flag, do NOT act now)

At the **live-combat milestone** — when the room stops being a scored tableau and becomes a playable fight that initializes entity STATE from the spec — reconsider whether entities should initialize facing from `heading_rad` for exact spawn-instant state-parity. Even then it is marginal (the sim overrides at fight-start regardless). Inert now; trivially revisitable then. **Not a dispatch.**

## 4. The other diff rows (not gandalf-gating — noted for completeness)

- **Wrapper rename** (`schema_version`/`__bootstrap_note__` → `_schema_version`/`_generated_from`/`_emitted_at`/`_do_not_hand_edit`): cosmetic provenance; fine.
- **`leash_distance_override_m`, `suppress_leash_hp_reset`, `description`**: additive engine geometry/telemetry/informational params the JSON faithfully carries and the Layer-1 room ignores safely. Correct separation (the room consumes Layer-1 geometry; engine-internal params ride along inert).
- **CI regen-guard (backlog):** endorsed as the right hardening — it makes the parity-audit-trail discipline automatic (a `--diff` in CI catches any future `arena.py` change that doesn't re-run the emitter, i.e. the exact drift the emitter prevents). Correctly backlogged; non-urgent (manual regen + commit-as-contract already delivers most of the value). star-lord/jack-ryan's call to schedule; not a design gate.

---

**Signed:** gandalf, 2026-06-15
**For:** ruling `heading_rad` a presentation-lever field — the emitter carries the canonical `−π/2` (faithful data mirror), drax's loader ignores it and derives facing from a readability rule that reproduces the sim's fight-start state (more faithful to the galadriel-scored moment than the uniform pre-fight spawn heading would be), closing star-lord's routed ⚠ carry without a drax verification cycle; revisit only at the live-combat milestone, where it remains marginal because the sim overrides spawn heading at fight-start regardless.
