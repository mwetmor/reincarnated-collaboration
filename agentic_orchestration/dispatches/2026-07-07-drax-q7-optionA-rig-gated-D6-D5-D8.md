# Dispatch — 2026-07-07 — drax — Q7 RULED (Option A): rig-gated demo layers D6 + D5 + D8

**From:** knight-rider
**To:** drax (presentation seam — `reincarnated-godot/`, `reincarnated-demo/`)
**Approved by:** Matt 2026-07-07 — **Q7 RULED: OPTION A** (authored per-variant BoneMaps → GeneralSkeleton). drax UNBLOCKED immediately into the rig-gated layers.
**Estimated effort:** large / multi-session (three demo layers). Pattern B — own session.

## Q7 ruling (verbatim, load-bearing)
**OPTION A: authored per-variant BoneMaps → GeneralSkeleton.**
- **Formalize `apply_hero_retarget.py` + the per-family `.tres` files (`sidekick_bone_map` + `goblin_bone_map`) as the v2 demo's canonical retargeting contract.**
- **Superset nuance adopted as written:** where a future pack's rig auto-maps cleanly, verify by **eye-check and skip the bespoke `.tres`** — author a map only where the rig needs one. (Do NOT pre-author maps for rigs that don't need them.)

## Unblocked scope — three rig-gated layers (all under FIXED Camera B)
**Camera B is FIXED and NOT re-litigated:** FOV 40 / pitch −55° / yaw 47° / dist 34m. Author + capture everything under it.

1. **D6 — three-beat floor authoring + capture.** The three-beat floor layout + its capture pass, now that the retargeting contract is ruled.
2. **D5 — verb VFX + summon meshes.** The verb-level VFX and the summon meshes (rig-gated on the retarget contract for the summoned bodies).
3. **D8 — grimoire portraits.** The grimoire portrait set.

*(You authored the Q7 recommendation and hold the D6/D5/D8 layer detail in your AGENT_STATE + prior held-work notes — this dispatch is the GO + the ruling context, not a re-spec. Pull your own layer notes for the per-beat/per-mesh/per-portrait specifics.)*

## Contract to formalize (Option A deliverable)
- `apply_hero_retarget.py` — canonical retargeting entry point for the v2 demo.
- Per-family `.tres`: `sidekick_bone_map`, `goblin_bone_map` — the bespoke maps where the rig needs one.
- Document the eye-check-and-skip rule for future auto-mapping rigs so the contract is self-describing (a map exists ONLY where a rig needed it).

## Required reading before starting
- Your own AGENT_STATE.md (`reincarnated-godot/AGENT_STATE.md` and/or `reincarnated-demo/AGENT_STATE.md`) — the D6/D5/D8 held-work detail + your Q7 recommendation writeup.
- Camera B params above (FIXED).
- Any prior capture-harness notes for the MP4 walkthrough harness.

## Scope / acceptance
- [ ] `apply_hero_retarget.py` + `sidekick_bone_map.tres` + `goblin_bone_map.tres` formalized as the canonical retarget contract; eye-check-skip rule documented.
- [ ] D6 three-beat floor authored + captured under Camera B.
- [ ] D5 verb VFX + summon meshes authored (summoned bodies retargeted via the contract).
- [ ] D8 grimoire portraits authored.
- [ ] AGENT_STATE.md updated (which layers complete, which capture artifacts produced).
- [ ] Tag(s) per seam convention: `drax/v-...`.
- [ ] Commit per established pattern (presentation-seam auto-commit); push is Matt-gated unless a cycle push-pattern is set.

## Out of scope
- NO engine-repo touches (`reincarnated-engine/` is off-limits per seam boundary).
- NO Camera B re-litigation (FIXED).
- NO pre-authoring `.tres` maps for rigs that auto-map cleanly (eye-check + skip).

## References
- Q7 ruling (Matt 2026-07-07, Option A); decisions-log entry filed by jack-ryan.
- ADR-004 (MIGRATION if any cross-surface contract), presentation-seam scope amendment 2026-06-21 (drax owns `reincarnated-godot/`).

## Completion record
*(appended by drax on completion)*
