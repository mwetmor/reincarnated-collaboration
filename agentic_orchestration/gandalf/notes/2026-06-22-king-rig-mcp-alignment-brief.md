# King-Rig MCP Alignment Brief — hair snap + sword grip

**Author:** gandalf (design steward), 2026-06-22
**For:** a fresh `claude --agent drax` session launched IN `~/Games/reincarnated-godot`
(so it loads `.mcp.json` at startup and connects to the live editor on WS:6550)
**Workflow:** MCP-priority (Matt directive 2026-06-22) — use engine-truth transforms,
not compute-blind-then-render. This is the first king-rig task on the MCP workflow.

---

## Why MCP for this

Two defects are precise ALIGNMENT problems where reading the actual mesh/bone
transforms live beats guessing-then-rendering:

1. **Hair mis-snapped.** Matt: "the hair is not snapped to the head correctly (it is
   so low that the scalp is showing through)." The hair mesh `Chr_Hair_Short_01`
   (assembled in `scripts/king_rig.gd` `_attach_hair`) sits TOO LOW — the bald-skin
   skull shows through the open gold crown ring, and the dark-brown low-poly dome
   reads as a leather cap/helmet rather than hair. (There is NO separate helmet — a
   prior pass confirmed the head is one bald-skin surface; the "helmet" IS this hair.)
2. **Sword grip read.** Matt earlier: "the sword is snapped to the wrist." The forward
   angle is now correct (`_seat_sword`, pitch 75 / yaw-left 12, committed 7e9e9ac),
   but verify the HILT actually seats in the PALM, not floating at the wrist.

## Engine-truth to read via MCP (don't guess these)

Instantiate / run the king so the rig exists, then read:
- **Head mesh AABB** (the bald-skin head surface) — its top-Y and crown-of-skull
  extent. `godot_scene3d get_spatial_info` with a `type_filter`/`within_aabb` (NEVER
  an unbounded `get_scene_tree` — friction #6: it dumps the whole tree).
- **Hair node current transform** — `godot_node_read get_properties` on the hair
  MeshInstance: its current position/scale/basis relative to the head bone.
- **Crown ring inner extent** — so the hair fills the ring opening (no scalp gap).
- **RightHand bone socket world position** + the **sword node global transform** —
  to confirm the hilt origin coincides with the palm, not the wrist joint.

## Target

- Raise (and scale if needed) the hair so it COVERS the scalp inside the crown ring —
  no skin visible through the opening — and the silhouette reads as HAIR.
- Warm/lighten the hair tint enough that the low-poly dome reads as chestnut hair,
  not a dark cap (Matt wants "only hair and the crown"). Tune against the render.
- Confirm the sword hilt sits in the palm; nudge the grip-drop if it reads as wrist.

## Frictions to respect (from the 2026-06-19 smoke-test)

- **#7 port 6550 is a hard singleton** — ONE MCP client. Don't open a 2nd.
- **#2 lazy connection w/ backoff** — gate the first real call on a cheap
  `godot_project get_info` poll.
- **#6** prefer `godot_scene3d get_spatial_info` (filtered) over `get_scene_tree`.
- The king is **runtime-built** in `king_rig.gd`; you edit the SCRIPT (a file), then
  re-verify. Don't mutate / persist changes into Matt's open editor scene.

## Deliverables (don't commit — gandalf eye-verifies + commits)

- `harness_logs/king_rig_mcp_2026-06-22/head_hair_fixed.png` — head close-up: hair
  covers the scalp, reads as hair, crown + hair only, no dark-cap read.
- `.../sword_grip.png` — close on the right hand: hilt in the palm.
- Report the engine-truth numbers you read (head top-Y, old vs new hair offset/scale,
  hand socket vs hilt origin) so the fix is grounded, not eyeballed.

## Scope guard

Only `scripts/king_rig.gd` (+ new `shoot_*`/`probe_*` harnesses). Do NOT touch the
occlusion files (`walltop_*`), the catalogue, or `project.godot` (leave its
auto-stripped LOD line for gandalf to restore). Do NOT commit.
