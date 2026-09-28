#!/usr/bin/env python3
"""C-9 R-C9-61: add the character toggle's skins to the ORIGINAL cliffside scene.

IDEMPOTENT.  Strips anything it wrote before and writes a fresh block, so re-measuring
and re-running is the whole loop and the scene cannot drift from the numbers.

WHAT IT ADDS, all as siblings of the Keeper's own AnimatedSprite2D, inside the one
scene that is already running -- no new scene, nothing swapped at the scene level:

  KnightSprite   AnimatedSprite2D on frames/knight_test.tres, hidden by default.
                 It takes the KEEPER'S OWN transform -- centered=false, offset
                 (-256,-400), scale 0.629167 -- because both sets are 512x512 cells
                 rendered with the sole on the same ground row (Keeper 394-400,
                 Meshy 398-405).  Registering it any other way would be inventing a
                 correction for a difference that is not there.

  Knight3D       a SubViewport carrying the real-time 3D knight, composited back into
                 the 2D scene through a Sprite2D with that same transform.  Sized and
                 aimed to match the sprite pipeline exactly (117.5 px/m, 19.77 deg),
                 so the two knights can be toggled between without the figure moving.

  CharacterSkin  the Node that owns the toggle.

The Keeper's own nodes are not touched.
"""
import argparse
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent / "godot"
SCENE = PROJ / "scenes" / "cliffside.tscn"
BEGIN = "; --- C-9 R-C9-61 character toggle (written by tools/patch_scene.py) ---"
END = "; --- end C-9 R-C9-61 character toggle ---"

# The Keeper's own visual transform, copied so the skins land on the same feet.
OFFSET = "Vector2(-256, -400)"
SCALE = "Vector2(0.629166666667, 0.629166666667)"
VIEW = 512               # SubViewport is square, like the sprite cells


def strip(t):
    t = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", t, flags=re.S)
    for rid in ("KnightFrames", "Knight3DScene", "CharSkinScript", "Knight3DScript"):
        t = re.sub(r'\[ext_resource [^\]]*id="%s"\]\n' % rid, "", t)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-3d", action="store_true",
                    help="also add the Knight3D SubViewport (needs the merged GLB)")
    a = ap.parse_args()

    t = SCENE.read_text()
    before = len(t)
    t = strip(t)
    print("stripped %d bytes of any previous toggle block" % (before - len(t)))

    ext = ['[ext_resource type="SpriteFrames" path="res://frames/knight_test.tres" id="KnightFrames"]',
           '[ext_resource type="Script" path="res://scripts/character_skin.gd" id="CharSkinScript"]']
    nodes = [
        '[node name="KnightSprite" type="AnimatedSprite2D" parent="Actors/Keeper"]',
        'visible = false',
        'sprite_frames = ExtResource("KnightFrames")',
        'centered = false',
        'offset = %s' % OFFSET,
        'scale = %s' % SCALE,
        'animation = &"idle_S"',
        '',
    ]
    if a.with_3d:
        ext.append('[ext_resource type="Script" path="res://scripts/knight3d.gd" id="Knight3DScript"]')
        nodes += [
            '[node name="Knight3D" type="Node2D" parent="Actors/Keeper"]',
            'visible = false',
            'script = ExtResource("Knight3DScript")',
            '',
            # The Sprite2D that shows the viewport. Its texture is assigned at runtime
            # from the SubViewport, because a ViewportTexture's path is resolved against
            # the scene it is saved in and is brittle to write by hand.
            '[node name="View" type="Sprite2D" parent="Actors/Keeper/Knight3D"]',
            'centered = false',
            'offset = %s' % OFFSET,
            'scale = %s' % SCALE,
            '',
            '[node name="VP" type="SubViewport" parent="Actors/Keeper/Knight3D"]',
            'disable_3d = false',
            'transparent_bg = true',
            'handle_input_locally = false',
            'size = Vector2i(%d, %d)' % (VIEW, VIEW),
            'render_target_update_mode = 4',
            '',
        ]
    nodes += [
        '[node name="CharacterSkin" type="Node" parent="Actors/Keeper"]',
        'script = ExtResource("CharSkinScript")',
        '',
    ]

    # nodes go straight after the Keeper's own subtree; ext_resources with the others
    anchor = '[node name="Camera2D" type="Camera2D" parent="Actors/Keeper"]'
    i = t.index(anchor)
    j = t.index("\n[node ", i + len(anchor)) + 1
    t = t[:j] + BEGIN + "\n" + "\n".join(nodes) + END + "\n" + t[j:]

    last = t.rindex("[ext_resource ")
    k = t.index("\n", last) + 1
    t = t[:k] + "\n".join(ext) + "\n" + t[k:]

    SCENE.write_text(t)
    print("wrote %s  (%s)" % (SCENE, "with 3D" if a.with_3d else "2D skin only"))


if __name__ == "__main__":
    sys.exit(main())
