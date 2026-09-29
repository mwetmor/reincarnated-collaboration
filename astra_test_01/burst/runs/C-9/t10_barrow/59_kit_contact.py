"""C-9 T10-1b: render the six kit props at the play camera, beside the barbarian for scale.

    blender --background --python 59_kit_contact.py -- <kitdir> <bodyglb> <out.png> <meta.json>

The camera is the one the scene is played at: orthographic, pitch 52.95354112560294, yaw 47
-- the same basis the props' yaw was baked against, so what this shows IS the face each prop
presents in the barrow.

THE BARBARIAN'S GLB CARRIES A STRAY. `nb-body.glb` holds `char1` (289,469 tris, 1.557 units
tall) AND an 80-triangle `Icosphere` of size 1.9 x 2.0 x 2.0 centred on the origin. Taking
the file's AABB as the figure's height makes him 2.5645 units, so scaling that to 1.85 m
would have put the actual man at 1.12 m -- and the scale reference, which is the whole point
of standing him next to the props, would have been quietly 40% wrong while looking fine.
Only `char1` is imported.

Positions are computed, not eyeballed: with an orthographic camera the ground's screen-right
axis is exactly (cos A, sin A, 0), so laying the props along it spaces them horizontally in
frame and one metre on that axis is exactly `resolution_x / ortho_scale` pixels -- which is
what the scale bar in the annotation pass is drawn from.
"""
import json
import math
import os
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
KIT, BODY, OUT, META = argv[0], argv[1], argv[2], argv[3]
ORDER = ["rocks", "stump", "cairn", "log", "skull", "shield"]
YAW, PITCH = 47.0, 52.95354112560294
GAP = 0.55
BODY_H = 1.85
W, H = 2800, 900

bpy.ops.wm.read_factory_settings(use_empty=True)


def bounds(objs):
    lo, hi = [1e9] * 3, [-1e9] * 3
    for o in objs:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                lo[i] = min(lo[i], w[i])
                hi[i] = max(hi[i], w[i])
    return lo, hi


def load(path, keep=None):
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.context.scene.objects if o not in before]
    bpy.ops.object.select_all(action="DESELECT")
    for o in new:
        o.select_set(True)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    ms = []
    for o in new:
        if o.type != "MESH" or (keep and o.name.split(".")[0] not in keep):
            bpy.data.objects.remove(o, do_unlink=True)
        else:
            ms.append(o)
    return ms


items = []
for nm in ORDER:
    ms = load(os.path.join(KIT, "%s.glb" % nm))
    lo, hi = bounds(ms)
    items.append({"name": nm, "meshes": ms, "half": max(hi[0] - lo[0], hi[1] - lo[1]) / 2,
                  "h": hi[2] - lo[2]})

body = load(BODY, keep={"char1"})
lo, hi = bounds(body)
s = BODY_H / (hi[2] - lo[2])
for o in body:
    o.matrix_world = mathutils.Matrix.Diagonal((s, s, s, 1.0)) @ o.matrix_world
lo, hi = bounds(body)
for o in body:
    o.matrix_world = mathutils.Matrix.Translation(
        (-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2])) @ o.matrix_world
lo, hi = bounds(body)
items.insert(0, {"name": "barbarian", "meshes": body,
                 "half": max(hi[0] - lo[0], hi[1] - lo[1]) / 2, "h": hi[2] - lo[2]})

A = math.radians(YAW)
P = math.radians(PITCH)
right = mathutils.Vector((math.cos(A), math.sin(A), 0.0))
t, span = 0.0, []
for it in items:
    t += it["half"]
    span.append(t)
    t += it["half"] + GAP
total = t - GAP
mid = total / 2 - items[0]["half"] + items[0]["half"]
centre = (span[0] - items[0]["half"] + span[-1] + items[-1]["half"]) / 2
for it, x in zip(items, span):
    d = right * (x - centre)
    for o in it["meshes"]:
        o.matrix_world = mathutils.Matrix.Translation(d) @ o.matrix_world
    it["t"] = x - centre

gnd = bpy.data.meshes.new("gnd")
gnd.from_pydata([(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)])
gobj = bpy.data.objects.new("gnd", gnd)
bpy.context.scene.collection.objects.link(gobj)
gm = bpy.data.materials.new("gm")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (.80, .82, .85, 1)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
gobj.data.materials.append(gm)

sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("w")
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (.72, .76, .82, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.1

sun_d = bpy.data.lights.new("sun", "SUN")
sun_d.energy = 3.2
sun_d.angle = math.radians(3.0)
sun_d.color = (1.0, 0.97, 0.92)
sun = bpy.data.objects.new("sun", sun_d)
sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(52.0), 0.0, math.radians(47.0 + 130.0))

hi_z = max(it["h"] for it in items)
ortho = total + GAP * 1.4
cd = bpy.data.cameras.new("cam")
cd.type = "ORTHO"
cd.ortho_scale = ortho
cam = bpy.data.objects.new("cam", cd)
sc.collection.objects.link(cam)
sc.camera = cam
target = mathutils.Vector((0, 0, hi_z * 0.42))
back = mathutils.Vector((math.sin(A) * math.cos(P), -math.cos(A) * math.cos(P), math.sin(P)))
cam.location = target + back * 80.0
cam.rotation_euler = (math.pi / 2 - P, 0.0, A)
cd.clip_start, cd.clip_end = 1.0, 200.0
sc.render.filepath = OUT
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)

# A second pass with the ground hidden and the film transparent, so the annotation step can
# CROP TO THE CONTENT instead of to a number somebody read off a preview. Same camera, same
# frame, so the alpha lines up pixel for pixel with the render above.
gobj.hide_render = True
sc.render.film_transparent = True
sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = os.path.splitext(OUT)[0] + "_alpha.png"
bpy.ops.render.render(write_still=True)

with open(META, "w") as f:
    json.dump({"width": W, "height": H, "ortho_scale": ortho,
               "px_per_m": W / ortho, "yaw_deg": YAW, "pitch_deg": PITCH,
               "items": [{"name": it["name"], "t_m": round(it["t"], 4),
                          "screen_x_px": round(W / 2 + it["t"] * W / ortho, 1),
                          "height_m": round(it["h"], 4),
                          "footprint_half_m": round(it["half"], 4)} for it in items]}, f, indent=1)
print("[contact] %s  %dx%d  %.1f px/m" % (OUT, W, H, W / ortho))
