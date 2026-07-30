# AMBIENT-REFIT fold-in — Matt directive (LR/presentation session, 2026-07-30)

> **Authorization:** Matt, in-session: *"Ok, I like it… Can we fold in the particle refit?"* — after
> approving the SCENEWRIGHT recipe (2026-07-30). Matt also declared session intent: the baton is
> nearly ready; the presentation session begins preparing its work here. Reference watch he is
> reviewing: `reincarnated-godot/tmp/wr2/wr3_after_pre_boss_B_74000802.mp4`, which he is
> *"very ready to see fully baked."*
> **Conductor for this cell:** gandalf (LR/presentation session). This is presentation-seam work
> Matt allocated here directly; it does not touch WR3 run conduction (charter session). Recorded
> so the charter session's ledger can cross-reference; zero WR1/WR2/WR3 ruling numbers consumed.

## The cell (drax): AMB-REFIT

Discharges the OWED item drax named twice (WR1-ROOMS §7.3; WR2 after-baton render note ~line 201):
the promoted ambient's emission extents are authored for the 17.5 m race stage; in the 37.5 m room
it dresses the middle and not the edges (0.50% vs 3.02% in-room coverage, ratio = 17.5²/37.5²).

**Matt's design intent (the acceptance standard, his words):** lessen the ambient's prominence in
the bright center, and use that lessened center as the sample extended across the room generally —
today it is distracting in the center and relatively absent outside it.

**Recipe (Matt-approved):**
1. Emission extents ×k (k = 37.5/17.5 = 2.143) in the `vfx/ambient/pp/*.tres` process materials,
   **counts HELD, sprite scale HELD** — the per-area dilution to ~0.22× IS the lessening; no
   sample-then-tile second step needed. Count trim only after the eye sees it.
2. `L5_CentrePool` quieted specifically (count/albedo) until the lit center matches the room-wide
   read — prominence is density × illumination; quiet the one layer living in the bright spot.
3. FORBIDDEN: scaling the `GPUParticles3D` node (2.14× sprites — drax's own prior refusal stands).

**Verification riders:** VOID-1 re-fires WITH the leak control (extents now approach walls; zeros
count only if the control still bleeds) · LSTAT-2 stage datum stationary · M-EYE: verdict
deliverable is MOTION — the WR3 watch re-rendered same seed/leg/tier/arm/camera with the refit
ambient in the room the fight renders in, plus before/after plates.

## Scope 2 (same cell, Matt follow-up directive): overhead AI-STATE tags on enemy combatants

**Matt verbatim:** *"I think maybe the only thing missing is the AI state that we are planning to
put above the enemy combatant NPCs."*

- Billboard state tag above each ENEMY combatant, driven ONLY from what the trace states — never
  an invented label. Sources on `replica-frame/v1` (+WR3 additions): `commit_state` (idle /
  wind-up / recovery once Mechanism C2 emits them), movement `intent`, `decision` events,
  `telegraph` (tell-in-progress). Missing/dark fields print as absent, not as a default state —
  the drax §0 discipline (a missing conditional key and a zero are different statements).
- Presentation: short word + color chip, legible at 720p from the `arena_full` camera stand-off;
  consistent anchor height above the capsule; declared an INSTRUMENT OVERLAY (owner-eye
  legibility layer), not final game UI — same class as the existing frame banners/readouts.
- Player gets NO tag in this pass (Matt named enemy combatants only).

**Guards:** traces READ-ONLY · race-lineage `tmp/vmur*` untouched (evidence) · frozen
`kit_replica_level.gd` discipline per WR1-ROOMS §7.1 · collision check at cell start (`git status`
on reincarnated-godot; HALT if another cell's uncommitted work sits on ambient/playback surfaces) ·
godot repo commits local, NOT pushed (conductor pushes after Matt's eye) · presentation-layer
change ONLY — zero fight/trace semantics.
