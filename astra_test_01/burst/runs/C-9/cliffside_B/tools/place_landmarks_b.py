#!/usr/bin/env python3
"""C-9 R-C9-42: the burning cathedral and the burning tower as SPRITES, staggered in
depth, instead of painted into the far layer.

WHY THEY LEFT THE LAYER.  Painted in, the two landmarks stood 500-580 px above the far
layer's own ridge, so framing the layer by its horizon put them off the top of the
screen and framing them put the ridge 598 px down the frame -- which is the "horizon far
too large" Matt saw.  One layer cannot be framed twice.  Cut out, each landmark is
placed on its own, the layer goes back on the plain horizon rule, and the two can be
STAGGERED the way A's far layer staggers its own: a big one down in the land band and a
small one up under the horizon, which is what reads as depth.

WHERE THEY GO.  Children of the Layer_far_ruins Parallax2D, so they scroll with the far
layer and need no parallax maths of their own -- drawn over the far layer's own sprite
and under the forest by z_index (the layer is z=-30, the forest z=-20, and z_index on a
child is relative, so +2 and +3 land at -28 and -27, between them).

COORDINATES ARE LAYER-LOCAL, AND THE HORIZON IS THE DATUM.  build_b_assets.py gives the
B far layer a vertical offset that lands its ridge on the row A's ridge occupies, so
layer-local y 690 is the horizon in BOTH registers.  Everything here is stated as a
distance from that row, which is why these numbers survive a re-render of the layer.

B ONLY.  scripts/style_toggle.gd hides them in A.  They carry no collision -- they are
background a mile away -- so `visible` is the whole of it, unlike the still figures,
which had to take a StaticBody2D down with them.

IDEMPOTENT: strips any block it wrote before and writes a fresh one, so re-measuring
and re-running is the whole loop and the scene cannot drift from the numbers.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
ART = PROJ.parent / "artifacts" / "CS9-assembly"
OUT_SPR = PROJ / "sprites_landmarks"
SCENE = PROJ / "scenes" / "cliffside.tscn"
REPORT = PROJ / "frames" / "landmarks_b.json"

BEGIN = "; --- C-9 R-C9-42 far-layer landmarks (written by tools/place_landmarks_b.py) ---"
END = "; --- end C-9 R-C9-42 far-layer landmarks ---"

# The far layer's horizon, in layer-local px. build_b_assets.py aligns B's ridge onto
# A's row, so this one number is the datum for both registers.
HORIZON_Y = 690.0

# Per landmark: the source, the BUILDING's own x span in the source (masonry only --
# the fire licking to the right and the plume are not the building and must not set its
# width), and the placement, stated as the conductor framed it.
LANDMARKS = {
    "cathedral": {
        "src": "L12_sprite_cathedral.png",
        "building_x": (25, 420),          # conductor's measurement of the masonry
        # NEARER / LARGER, in the land band, west of the bridge. Scale is set by the
        # target on-screen building width, not typed in.
        "target_building_w": 300.0,
        "below_horizon": 588.0,           # masonry base, px below the ridge row
        "centre_x": 630.0,                # layer-local x of the building's centre
        "z": 3,
    },
    "tower": {
        "src": "L12_sprite_tower.png",
        "building_x": (20, 310),
        # FURTHER BACK / SMALLER, just under the ridge near the horizon, east of the
        # cathedral and still west of the bridge.
        "target_building_w": 102.0,
        "below_horizon": 210.0,
        "centre_x": 1300.0,
        "z": 2,
    },
}


def masonry(path, bx):
    """The building's own box in source px: base row, spire row, and the centre of the
    masonry span the conductor measured.

    The largest fully-opaque component is NOT the building -- the fire is opaque too and
    runs 100 px past the stonework, so measuring the width from it would make every
    landmark a sixth too small for its stated scale. The component gives the BASE and
    the SPIRE (vertical extent is not confused by the fire); the WIDTH comes from the
    conductor's own masonry span.
    """
    a = np.asarray(Image.open(path))
    solid = a[..., 3] > 240
    lab, k = ndimage.label(solid)
    sizes = ndimage.sum(solid, lab, range(1, k + 1))
    m = (lab == int(np.argmax(sizes)) + 1)
    ys, xs = np.nonzero(m)
    feather_bottom = int(np.nonzero((a[..., 3] > 8).any(1))[0].max())
    return {"base_row": int(ys.max()), "spire_row": int(ys.min()),
            "centre_col": (bx[0] + bx[1]) / 2.0,
            "building_w": float(bx[1] - bx[0]),
            "component_x": [int(xs.min()), int(xs.max())],
            "feather_bottom_row": feather_bottom,
            "size": [int(a.shape[1]), int(a.shape[0])]}


def strip_previous(t):
    t = re.sub(r'\[ext_resource type="Texture2D" path="res://sprites_landmarks/[^"]+" id="[^"]+"\]\n', "", t)
    for name in ("Landmark_cathedral", "Landmark_tower"):
        t = re.sub(r'\[node name="%s" type="Sprite2D" parent="Layer_far_ruins"\]\n[^\[]*' % name, "", t)
    t = re.sub(re.escape(BEGIN) + r"\n", "", t)
    t = re.sub(re.escape(END) + r"\n", "", t)
    return t


def main():
    OUT_SPR.mkdir(exist_ok=True)
    t = SCENE.read_text()
    before = len(t)
    t = strip_previous(t)
    print("stripped %d bytes of any previous landmark block" % (before - len(t)))

    report = {"note": "C-9 R-C9-42: the two far-layer landmarks as sprites. Layer-local "
                      "coordinates; y is stated as a distance below the far layer's "
                      "horizon row (%d), which build_b_assets.py aligns between A and B."
                      % HORIZON_Y,
              "horizon_layer_y": HORIZON_Y, "landmarks": {}}
    ext, nodes = [], []
    for name, cfg in LANDMARKS.items():
        src = ART / cfg["src"]
        dst = OUT_SPR / (name + ".png")
        shutil.copyfile(src, dst)
        m = masonry(src, cfg["building_x"])
        s = cfg["target_building_w"] / m["building_w"]
        base_y = HORIZON_Y + cfg["below_horizon"]
        # centered = false, so position is the texture's own origin in layer px
        px = cfg["centre_x"] - m["centre_col"] * s
        py = base_y - m["base_row"] * s
        spire_y = py + m["spire_row"] * s
        foot_y = py + m["feather_bottom_row"] * s
        ext.append('[ext_resource type="Texture2D" path="res://sprites_landmarks/%s.png" id="LM_%s"]'
                   % (name, name))
        nodes.append(
            '[node name="Landmark_%s" type="Sprite2D" parent="Layer_far_ruins"]\n'
            'z_index = %d\n'
            'centered = false\n'
            'position = Vector2(%.3f, %.3f)\n'
            'scale = Vector2(%.6f, %.6f)\n'
            'texture = ExtResource("LM_%s")\n' % (name, cfg["z"], px, py, s, s, name))
        report["landmarks"][name] = {
            "source": cfg["src"], "scale": round(s, 5),
            "building_w_source_px": m["building_w"],
            "building_w_layer_px": round(m["building_w"] * s, 1),
            "building_h_layer_px": round((m["base_row"] - m["spire_row"]) * s, 1),
            "layer_position": [round(px, 2), round(py, 2)],
            "masonry_base_layer_y": round(base_y, 1),
            "masonry_base_below_horizon": cfg["below_horizon"],
            "spire_layer_y": round(spire_y, 1),
            "spire_above_horizon": round(HORIZON_Y - spire_y, 1),
            "feather_foot_layer_y": round(foot_y, 1),
            "centre_layer_x": cfg["centre_x"], "z_index_relative": cfg["z"],
            "measured": m,
        }
        print("  %-10s scale %.4f -> building %.0fx%.0f layer px   base y %.0f (%.0f "
              "below the ridge)   spire y %.0f (%.0f %s the ridge)   x %.0f..%.0f"
              % (name, s, m["building_w"] * s, (m["base_row"] - m["spire_row"]) * s,
                 base_y, cfg["below_horizon"], spire_y, abs(HORIZON_Y - spire_y),
                 "above" if spire_y < HORIZON_Y else "below",
                 px, px + m["size"][0] * s))

    # ext_resources go with the other layer textures; nodes go straight after the far
    # layer's own sprite, so they are that layer's children in file order too.
    anchor = '[node name="Sprite2D" type="Sprite2D" parent="Layer_far_ruins"]'
    i = t.index(anchor)
    j = t.index("[node ", i + len(anchor))
    t = t[:j] + BEGIN + "\n" + "\n".join(nodes) + END + "\n" + t[j:]

    last_ext = t.rindex("[ext_resource ")
    k = t.index("\n", last_ext) + 1
    t = t[:k] + "\n".join(ext) + "\n" + t[k:]

    SCENE.write_text(t)
    REPORT.write_text(json.dumps(report, indent=1))
    print("wrote", SCENE, "and", REPORT)


if __name__ == "__main__":
    sys.exit(main())
