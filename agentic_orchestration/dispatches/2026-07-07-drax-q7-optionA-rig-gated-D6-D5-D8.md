# Dispatch — 2026-07-07 — drax — Q7 RULED (Option A): rig-gated demo layers D6 + D5 + D8

**From:** knight-rider
**To:** drax (presentation seam — `reincarnated-godot/`, `reincarnated-demo/`)
**Approved by:** Matt 2026-07-07 — **Q7 RULED: OPTION A** (authored per-variant BoneMaps → GeneralSkeleton). drax UNBLOCKED immediately into the rig-gated layers.
**Estimated effort:** large / multi-session (three demo layers). Pattern B — own session.

## Q7 ruling (verbatim, load-bearing)
**OPTION A: authored per-variant BoneMaps → GeneralSkeleton.**
- **Formalize `apply_hero_retarget.py` + the per-family `.tres` files (`sidekick_bone_map` + `goblin_bone_map`) as the v2 demo's canonical retargeting contract.**
- **Superset nuance adopted as written:** where a future pack's rig auto-maps cleanly, verify by **eye-check and skip the bespoke `.tres`** — author a map only where the rig needs one. (Do NOT pre-author maps for rigs that don't need them.)

## Unblocked scope — three rig-gated layers (all under CAMERA B′, dist 20m)
**⚠️ CAMERA B′ — Matt-ruled 2026-07-07 (supersedes the dist-34 language everywhere):** FOV 40 / pitch −55° / yaw 47° / **dist 20m** (hero fraction 8.02% geometric, D3 register). This is a **dist-only** revision of the Q8-ratified Camera B (34→20); **FOV/pitch/yaw were NOT re-opened and stay closed.** Landed in code: godot `67e128e` (`scripts/playshell.gd`, `CAM_DIST 34.0→20.0`). Decisions-log `a0bf7fd`; re-ratification artifact `agentic_orchestration/qa/2026-07-07-camera-Bprime-re-ratification.md`. **Author + capture everything under B′ (dist 20).**

1. **D6 — three-beat floor authoring + capture.** The three-beat floor layout + its capture pass, now that the retargeting contract is ruled.
2. **D5 — verb VFX + summon meshes.** The verb-level VFX and the summon meshes (rig-gated on the retarget contract for the summoned bodies).
3. **D8 — grimoire portraits.** The grimoire portrait set.

## Binding constraints (Matt/gandalf relay 2026-07-07 — fold into every lane)
- **HARNESS LAW (capture template):** SHOOT-mode frame grabs run `--rendering-driver metal` **WITHOUT `--headless`** — `--headless` forces the Dummy rasterizer → null framebuffer → every `save_png` errors. NEVER pair `--headless` with SHOOT captures. (`--headless` is fine for the min-spec CPU sim-loop probe, which grabs no frames.)
- **D6-AUTHORING VISIBLE-BAND CONSTRAINT (consumption-time law):** at B′ the visible band ≈**29m**, near-edge ≈**24m**. **No encounter/AI config or roster-shopped kit bound for a player surface may carry engagement range beyond the visible band** (specimen: gravecaller archer 38.9m = off-screen-capable at B′). Binds at **D6 encounter authoring + roster shopping**; NEVER at emission; sim gauntlet unaffected.
- **REGISTER-SEQUENCING INSURANCE:** dist 20 HOLDS (Matt-confirmed; the side-by-side concern was diagnosed as a resolution artifact — SHOOT renders 1920×1080 vs the old 1152×648 live window). Register re-opens ONLY on new empirical evidence (named HIGH-confidence path = galadriel pixel-benchmark vs real D3/D4; not scheduled — escalate to Matt only if a lane surfaces a register problem). **Cheap insurance: within each lane, sequence authoring/wiring AHEAD of final captures** so a register revision (if ever) is one constant + capture re-runs only.
- **HOUSEKEEPING (first entry):** the godot working tree carries a PRE-EXISTING unstaged deletion of `[rendering] mesh_lod/lod_change/threshold_pixels=1.0` (prior-session residue, kept out of `aa8b0ae`). **Disposition commit-or-revert on your first entry.**
- **Matched-media (already landed):** `project.godot [display]` run-window is now 1920×1080 (drax `aa8b0ae`, Metal/M2) — live eyeballing during authoring is no longer undersampled.

*(You authored the Q7 recommendation and hold the D6/D5/D8 layer detail in your AGENT_STATE + prior held-work notes — this dispatch is the GO + the ruling context, not a re-spec. Pull your own layer notes for the per-beat/per-mesh/per-portrait specifics.)*

## Contract to formalize (Option A deliverable)
- `apply_hero_retarget.py` — canonical retargeting entry point for the v2 demo.
- Per-family `.tres`: `sidekick_bone_map`, `goblin_bone_map` — the bespoke maps where the rig needs one.
- Document the eye-check-and-skip rule for future auto-mapping rigs so the contract is self-describing (a map exists ONLY where a rig needed it).

## Required reading before starting
- Your own AGENT_STATE.md (`reincarnated-godot/AGENT_STATE.md` and/or `reincarnated-demo/AGENT_STATE.md`) — the D6/D5/D8 held-work detail + your Q7 recommendation writeup.
- Camera B′ params above (dist 20m); re-ratification artifact `agentic_orchestration/qa/2026-07-07-camera-Bprime-re-ratification.md`; decisions-log `a0bf7fd`.
- Any prior capture-harness notes for the MP4 walkthrough harness (apply the HARNESS LAW above).

## Scope / acceptance
- [ ] `apply_hero_retarget.py` + `sidekick_bone_map.tres` + `goblin_bone_map.tres` formalized as the canonical retarget contract; eye-check-skip rule documented.
- [ ] First-entry housekeeping: dispose the mesh_lod `threshold_pixels=1.0` unstaged deletion (commit-or-revert).
- [ ] D6 three-beat floor authored + captured **under Camera B′ (dist 20)**; encounter/roster ranges respect the ≈29m visible band.
- [ ] D5 verb VFX + summon meshes authored (summoned bodies retargeted via the contract).
- [ ] D8 grimoire portraits authored.
- [ ] All SHOOT captures fire per the HARNESS LAW (`metal`, no `--headless`); authoring/wiring sequenced ahead of final captures (register insurance).
- [ ] AGENT_STATE.md updated (which layers complete, which capture artifacts produced).
- [ ] Tag(s) per seam convention: `drax/v-...`.
- [ ] Commit per established pattern (presentation-seam auto-commit); push is Matt-gated unless a cycle push-pattern is set.

## Out of scope
- NO engine-repo touches (`reincarnated-engine/` is off-limits per seam boundary).
- NO Camera B′ re-litigation — FOV/pitch/yaw closed; dist 20 HOLDS (register re-opens only on new empirical evidence, escalate to Matt).
- NO pre-authoring `.tres` maps for rigs that auto-map cleanly (eye-check + skip).

## References
- Q7 ruling (Matt 2026-07-07, Option A) + Camera B′ ruling (Matt 2026-07-07, dist 20); decisions-log entries `8f1a5a1` (Q7) + `a0bf7fd` (B′).
- Presentation-lane GO relay (Matt/gandalf 2026-07-07): harness law, D6 visible-band constraint, register-sequencing insurance, mesh_lod housekeeping.
- ADR-004 (MIGRATION if any cross-surface contract), presentation-seam scope amendment 2026-06-21 (drax owns `reincarnated-godot/`).

## Completion record
*(appended by drax on completion)*
