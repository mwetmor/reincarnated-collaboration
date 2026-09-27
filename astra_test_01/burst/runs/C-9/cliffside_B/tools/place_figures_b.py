#!/usr/bin/env python3
"""C-9 scene v3: put the angel and the demon into scenes/cliffside.tscn.

Reads frames/figures_b.json (written by tools/build_figures_b.py) and rewrites the two
figure nodes in the scene from it.  IDEMPOTENT: it strips any block it wrote before and
writes a fresh one, so re-running the measurement and re-running this is the whole loop
and the scene can never drift from the numbers that justify it.

They go in as DIRECT CHILDREN of Actors/, beside the Keeper, rather than inside a
wrapper node.  Actors/ is the y_sort_enabled node; a wrapper would sort as ONE unit
against the knight and both figures would flip in front of or behind him together,
which is not what "y-sorted with the knight" means.

The collision is the Keeper's own feet-ellipse, scaled: a 32-gon ConvexPolygonShape2D,
semi-axes in the same 16.61 : 6.04 ratio the Keeper uses, so a figure occupies the
ground the same way the player does and he walks around it rather than into it.
"""
import json
import math
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
SCENE = PROJ / "scenes" / "cliffside.tscn"
FIG_JSON = PROJ / "frames" / "figures_b.json"

BEGIN = "; --- C-9 v3 still figures (written by tools/place_figures_b.py) ---"
END = "; --- end C-9 v3 still figures ---"


def ellipse(rx, ry, n=32):
    pts = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        pts.append("%.6f, %.6f" % (rx * math.cos(t), ry * math.sin(t)))
    return ", ".join(pts)


def strip_previous(t):
    """Remove every node, ext_resource and sub_resource this tool wrote before."""
    t = re.sub(r'\[ext_resource type="Texture2D" path="res://sprites_figures/[^"]+" id="[^"]+"\]\n', "", t)
    t = re.sub(r'\[ext_resource type="Script" path="res://scripts/still_figure\.gd" id="[^"]+"\]\n', "", t)
    t = re.sub(r'\[sub_resource type="ConvexPolygonShape2D" id="Feet_(?:Angel|Demon)"\]\n[^\[]*', "", t)
    for name in ("Angel", "Demon"):
        t = re.sub(r'\[node name="%s" type="StaticBody2D" parent="Actors"\]\n[^\[]*' % name, "", t)
        t = re.sub(r'\[node name="\w+" type="\w+" parent="Actors/%s"\]\n[^\[]*' % name, "", t)
    return t


def main():
    fig = json.loads(FIG_JSON.read_text())
    t = SCENE.read_text()
    before = len(t)
    t = strip_previous(t)
    print("stripped %d bytes of any previous figure block" % (before - len(t)))

    # ---- ext_resources, after the Keeper script line -----------------------
    anchor = '[ext_resource type="Script" path="res://scripts/keeper.gd" id="Keeper"]'
    if anchor not in t:
        raise SystemExit("cliffside.tscn: Keeper script ext_resource not found")
    ext = [anchor, '[ext_resource type="Script" path="res://scripts/still_figure.gd" id="StillFigure"]']
    for name in fig["figures"]:
        ext.append('[ext_resource type="Texture2D" path="res://sprites_figures/%s.png" id="Tex%s"]'
                   % (name, name.capitalize()))
    t = t.replace(anchor, "\n".join(ext), 1)

    # ---- sub_resources: one feet ellipse each ------------------------------
    sub = []
    for name, f in fig["figures"].items():
        rx, ry = f["collision_ellipse_rx_ry"]
        sub.append('[sub_resource type="ConvexPolygonShape2D" id="Feet_%s"]\npoints = PackedVector2Array(%s)\n'
                   % (name.capitalize(), ellipse(rx, ry)))
    first_node = t.index("[node name=")
    t = t[:first_node] + "\n".join(sub) + "\n" + t[first_node:]

    # ---- the nodes, appended after the last Actors/ child ------------------
    nodes = [BEGIN]
    for name, f in fig["figures"].items():
        cap = name.capitalize()
        ox, oy = f["offset"]
        s = f["scale"]
        x, y = f["world_pos"]
        if not f["walkable"]:
            raise SystemExit("%s at %s is not on walkable ground -- fix FIGURES[] in "
                             "tools/build_figures_b.py and re-measure" % (name, (x, y)))
        nodes.append(
            '[node name="%s" type="StaticBody2D" parent="Actors"]\n'
            'position = Vector2(%.4f, %.4f)\n'
            'collision_layer = 1\ncollision_mask = 0\n'
            'script = ExtResource("StillFigure")\n'
            'figure_name = "%s"\n' % (cap, x, y, name))
        nodes.append(
            '[node name="Sprite2D" type="Sprite2D" parent="Actors/%s"]\n'
            'centered = false\noffset = Vector2(%.4f, %.4f)\n'
            'scale = Vector2(%.9f, %.9f)\n'
            'texture = ExtResource("Tex%s")\n' % (cap, ox, oy, s, s, cap))
        nodes.append(
            '[node name="CollisionShape2D" type="CollisionShape2D" parent="Actors/%s"]\n'
            'shape = SubResource("Feet_%s")\n' % (cap, cap))
    nodes.append(END + "\n")
    t = t.rstrip("\n") + "\n\n" + "\n".join(nodes)

    # ---- load_steps ---------------------------------------------------------
    n = len(re.findall(r'^\[ext_resource ', t, re.M)) + len(re.findall(r'^\[sub_resource ', t, re.M)) + 1
    t = re.sub(r"load_steps=\d+", "load_steps=%d" % n, t, count=1)

    SCENE.write_text(t)
    print("wrote %s  (load_steps=%d)" % (SCENE, n))
    for name, f in fig["figures"].items():
        print("  %-6s at %s  scale %.5f  offset %s  ellipse %s  walkable=%s"
              % (name, f["world_pos"], f["scale"], f["offset"],
                 f["collision_ellipse_rx_ry"], f["walkable"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
