# Does "crossing 3D scenes off the plan" also retire the 3D character/gear mannequin route?

> **STATUS:** OPEN — filed by gandalf (ARCHITECT) 2026-09-15 at the scene-builder canonization (`canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md § 1`). Blocks: the reconciliation sweep of Synty/3D-register text across `style-register.md`, the game tracker (PART A4 / B1 / B2 / B4 / C), `ensemble-asset-pipeline-spec.md`, `pipeline-game.md` and several engine-spec docs.

**The question.** R-C3-102 says: *"We are leaving Synty behind and crossing 3D scenes off our project plan."* It names **scenes** and **Synty**. The ensemble asset spec still carries a **3D character/gear mannequin route** (rig → render → sprite) as a candidate for the character matrix. Run C-3 built the character matrix by a different method (Astra stills → Grok clips → cycle cut → matte). Is the 3D mannequin route also retired, kept as a fallback, or kept as a *motion source* only?

**Recommendation (one):** **Retire it as an ASSET route; keep a plain Godot mannequin as a MOTION SOURCE only.** Characters are painted (the C-3 matrix stands); but the video-generation findings put pose-driven transfer first (route R1: a mannequin walk cycle rendered in Godot at all 8 directions drives every gear-tier still, giving identical timing/silhouette across gear). That needs a mannequin rig for *motion*, never for rendering the character. So: no 3D character/gear assets, no Synty; yes to a grey mannequin as a driving-video source.

**Options:**
- **A. Retire the 3D mannequin route entirely** — clean; loses the free driving-video source for R1 (a motion source would then have to come from video or mocap libraries).
- **B (recommended). Retire as asset route; keep as motion source** — matches the C-3 matrix method and the R1 plan; the mannequin never appears in art.
- **C. Keep the full 3D mannequin route as a fallback** — keeps old tracker items alive and the register ambiguity that the canon doc had to flag.

**Consequence of the ruling:** the reconciliation sweep (in place, never amputate) rewrites each Synty/3D clause to the ruled scope; the tracker's 3D items close or are rescoped accordingly.
