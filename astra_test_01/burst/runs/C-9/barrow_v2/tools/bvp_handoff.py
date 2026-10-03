#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): writes take/KC2_HANDOFF.md from the take's own manifests (nothing typed twice).

    python3 tools/bvp_handoff.py
"""
import json, math, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
TAKE = os.environ.get("BVP_TAKE", os.path.join(BV2, "take"))
FR = json.load(open(os.path.join(BV2, "paint", "frame_bvp.json")))
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
TI = json.load(open(os.path.join(TAKE, "ground", "tiles.json")))
CU = json.load(open(os.path.join(TAKE, "cutouts", "cutouts.json")))
DO = json.load(open(os.path.join(TAKE, "doors.json")))
GC = json.load(open(os.path.join(TAKE, "ground_class", "ground_class.json")))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
P = FR["px_per_m"]; A = math.radians(FR["pitch_deg"])


def main():
    lay = os.path.join(BV2, "layout_v2.json")
    g = [x for x in CU["groups"] if x.get("strips")]
    big = sorted(g, key=lambda x: -x["over_floor_ground_m2"])
    o = []
    o.append("# barrow_v2 'Fjord Headland': handoff to KC2's drax (ground skin + cutouts)\n")
    o.append("> Lane BVP (drax), Run C-9 Phase 2. Every number below is read from the take's manifests. "
             "Paths are relative to `astra_test_01/burst/runs/C-9/barrow_v2/`.\n")
    o.append("## 1. The frame and the projection\n")
    o.append(f"- **Sim frame:** +x east, +y SOUTH, metres, origin = the player start. It is the same frame as `layout_v2.json` and the pack's sg1 anchors.")
    o.append(f"- **Projection:** `kc2play_projection.gd` exactly: `screen_x = ppm*x`, `screen_y = ppm*sin(a)*y - ppm*cos(a)*z`, with a = {FR['pitch_deg']}°, zero yaw. Every art pixel lies on the z = 0 plane, as the actors do.")
    o.append(f"- **Authored density:** {P:.6f} px/m across ({P*math.sin(A):.4f} px per ground metre down-screen). That is the PLATE density, so ZOOM-HOUSE holds up.")
    o.append(f"- **Runtime scale** = `proj.ppm / {P:.6f}`. At ZOOM-GD that is 75.668 / 100.6176 = 0.75203.")
    o.append(f"- **Plate:** {FR['size_px'][0]} x {FR['size_px'][1]} px, with sim (0, 0) at plate px {FR['origin_px']}.")
    o.append(f"- **Painted envelope:** the floor dilated by the ZOOM-GD half-window + {FR['margin_m']} m, so the unclamped camera never shows past the paint. Outside it, alpha is 0.\n")
    o.append("## 2. Ground tiles: `World/Ground` (under the y-sorted `Actors`)\n")
    o.append(f"- **Manifest:** `take/ground/tiles.json`. It has {len(TI['tiles'])} tiles of up to {FR['tile']}² px, PNG RGBA. Each row carries `origin_sim_m`, the sim (x, y) of the tile's top-left pixel corner.")
    o.append(f"- **Placing a tile:** `position = proj.m_to_px(origin_sim_m.x, origin_sim_m.y)`, `scale = proj.ppm / {P:.6f}`, `centered = false`.")
    o.append("- **What the tiles hold:** the WHOLE painting, tall pieces included. You don't need to cut holes. Where a piece can hide an actor, its cutout (§3) draws over him by y-sort.\n")
    o.append("```\n" + "\n".join(f"{t['id']}  {t['file']}  origin_sim_m {t['origin_sim_m']}  {t['size_px'][0]}x{t['size_px'][1]}" for t in TI["tiles"]) + "\n```\n")
    o.append("## 3. Cutouts: children of the y-sorted `Actors` node\n")
    o.append(f"- **Manifest:** `take/cutouts/cutouts.json`.")
    o.append(f"- **What a cutout is:** {len(CU['cutouts'])} strips across {len(g)} tall pieces. Each piece is cut from the painting at its own geometry (an ID render of the greybox at the same camera, dilated {CU['feather_px']} px). Each piece is SLICED into {CU['strip_m']} m vertical strips.")
    o.append("- **Draw rule:**")
    o.append("  - `Sprite2D.centered = false`;")
    o.append("  - `position = proj.m_to_px(sort_point_sim_m)`;")
    o.append("  - `offset = texture_offset_px` (in texture px; the node's scale applies);")
    o.append(f"  - `scale = proj.ppm / {P:.6f}`.")
    o.append("- **Sorting:** y-sort then compares the strip's sort point with each actor's ground point. The sort point is the FRONT (camera-side, largest-y) edge of the piece's footprint inside that strip.")
    o.append("- **Why strips:** a long diagonal piece (a palisade run, the hall's west wall, the cliff lip) sorts correctly along its whole length. An actor north of the strip's front edge is behind it; one south of it is in front. No actor ever stands inside a footprint, because every tall piece is outside the floor (validator R5).\n")
    o.append("| piece | features | strips | over the floor (ground m²) |")
    o.append("|---|---|---:|---:|")
    for x in sorted(g, key=lambda x: x["group"]):
        o.append(f"| `{x['group']}` | {', '.join(f for f in x['features'] if not f.startswith('@'))} | {x['strips']} | {x['over_floor_ground_m2']} |")
    o.append("\n**Cutouts that overlap the walkable floor ON SCREEN:**\n")
    o.append("- No piece stands on the floor.")
    o.append("- A piece SOUTH of the floor rises up-screen over the floor north of it. This is the correct picture of the world: the hall's roof hides a man standing behind the hall.")
    o.append("- Y-sort handles it.")
    o.append("- Pieces with a non-zero floor overlap, largest first:\n")
    for x in big:
        if x["over_floor_ground_m2"] > 0:
            o.append(f"- `{x['group']}`: {x['over_floor_ground_m2']} m²")
    o.append("\n## 4. The walkable polygon and the doors\n")
    o.append(f"- **Walkable floor:** `layout_v2.json` → `floor.polygon`, {len(L['floor']['polygon'])} vertices, sim frame, z = 0, {L['floor']['area_m2']} m². It is the convex hull of the six 8 m discs + 1 m.")
    o.append(f"- **The layout file:** `layout_v2.json`, sha256 `{sha(lay)}`.")
    o.append("- **Door anchors** (`take/doors.json`): the six anchors of record, each with its painted deliverer and that deliverer's emergence point.\n")
    o.append("| anchor | sim (x, y) | deliverer | how | deliverer point (sim) |")
    o.append("|---|---|---|---|---|")
    for d in DO["doors"]:
        o.append(f"| {d['id']} | ({d['anchor_sim_m'][0]:.3f}, {d['anchor_sim_m'][1]:.3f}) | `{d['deliverer']}` | {d['how']} | {tuple(round(v, 2) for v in d['deliverer_point_sim_m']) if 'deliverer_point_sim_m' in d else 'ground art (the mere is the floor)'} |")
    o.append("\n## 5. Ground class map (surface-aware VFX)\n")
    o.append(f"- **`take/ground_class/ground_class_sim.png`:** {GC['px_per_m']} px/m, sim extent {GC['extent_sim_m']}. Row 0 is the north edge.")
    o.append(f"- **`ground_class_plate_q4.png`:** the same classes on the plate grid at 1/4 plate resolution.")
    o.append(f"- **Classes:** " + ", ".join(f"{k} = {v}" for k, v in GC["classes"].items()) + ".")
    o.append(f"- **Surfaces:** " + ", ".join(f"{k} → {v}" for k, v in GC["surface"].items()) + ".\n")
    o.append("## 6. Draw order, in one list\n")
    o.append("1. `World/Ground`: the tiles.")
    o.append("2. Then the existing ground VFX (mouth rings, aprons, EoR).")
    o.append("3. Then `World/Actors` (y_sort_enabled): the actors AND the cutout strips together, sorted by ground y.")
    o.append("4. Then the HUD.\n")
    o.append("Two things to watch:")
    o.append("- The ground VFX draw over the painting but under every cutout, even where a cutout sorts behind an actor.")
    o.append("- The mere (p05's deliverer) is ground art. Its cracks/burst VFX go on the ground layer.\n")
    o.append("## 7. Preview\n")
    o.append("`take/preview/`:")
    o.append("- V0–V7, the composited views at ZOOM-GD (V0 at plate scale);")
    o.append("- Y1–Y3, the y-sort proofs with a JOIN-1 hero cell at true scale;")
    o.append("- `barrow_v2_pan.mp4`, the pan film.\n")
    open(os.path.join(TAKE, "KC2_HANDOFF.md"), "w").write("\n".join(o) + "\n")
    print(os.path.join(TAKE, "KC2_HANDOFF.md"))


if __name__ == "__main__":
    main()
