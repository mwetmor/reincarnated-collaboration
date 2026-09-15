# Request → knight-rider — reconcile drax's two charters before the VFX fixture is dispatched

**From:** gandalf (ARCHITECT), 2026-09-15. **Occasioned by:** jack-ryan Gate-1 BLOCK-5, `agentic_orchestration/qa/findings/2026-09-15-vfx-architecture-gate1.md`.

**The conflict (Principle 3 / ADR-004):** `.claude/agents/drax.md` + `AGENTS.md:140-157` charter drax into `reincarnated-demo/`, `reincarnated-loadout/`, `reincarnated-godot/` (*"Forward+/Metal renderer"*) and never mention `astra_test_01/`. `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md § 2` (CANON per R-C3-116/119) charters him into the painted-2D lane (grey rooms, web export, deploy-truth). A cold `--agent drax` session reads the former. The VFX proposal (`gandalf/notes/2026-09-15-vfx-workflow-architecture/03-architecture.md` § 3 P-0, V10) asks him to hand-author a G1 event-driven component + deterministic fixture host on the **Compatibility** renderer.

**Conductor lean (for KR to ratify or amend, not Matt's):** the fixture and component live in **`reincarnated-godot/vfx_fixture/`** (drax's repo; Compatibility; hand-authored; *not* inside the exporter-generated `astra_test_01/burst/runs/C-3/cliffside_*` trees, which the next PACK regenerates); the lane's exporter later imports the component as a dependency. `reincarnated-godot/project.godot` is Forward+ on `sidekick_test.tscn` — the fixture project sets Compatibility explicitly.

**Asks:** (1) amend `drax.md` / `AGENTS.md` to name the painted-2D lane + Compatibility; (2) a MIGRATION note for the exporter↔hand-authored boundary; (3) the "grey room" word now means two things (drax's static terrain guide vs the VFX **motion fixture**) — the dispatch vocabulary must use *motion fixture* for the latter.

Blocks nothing until Matt rules Q79 V10/V17; then it blocks the P-0 dispatch.


**⟲ NARROWED 2026-09-15 (Matt V10):** the fixture is the *current cliffside scene* in the Astra lane; the monster pack is Astra-painted; the G1 component / targeting / replay land in the exporter (Astra TOOLING); **drax assists on grey-box and Godot systems as needed** — no drax-owned fixture repo. Asks (1) and (3) stand (name the lane in drax's charter; "motion fixture" vocabulary); ask (2) reduces to: drax edits inside exporter-generated trees must be handed back as exporter changes, never left as hand-edits the next PACK overwrites.
