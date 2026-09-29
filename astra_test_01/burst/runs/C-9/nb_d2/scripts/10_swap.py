# D2 step 6: THE SWAP TEST -- one body, one texture, gear stacked on, nothing
# about the body repainted between stacks.
#
#   blender -b -noaudio --python scripts/10_swap.py -- <clip.glb> <bodytex.png>
#     <outdir> --gear "helmet:bone:Head,bracers:bone:LeftForeArm|RightForeArm:split"
#     [--elev 52.95] [--res 300] [--poke]
#
# Pieces are fitted INLINE here, from pieces/*.glb, for the reason in gearlib:
# a skinned glTF round trip collapsed every one of them.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("10_swap.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
CLIP, TEX, OUT = a[0], a[1], a[2]
SPEC = a[a.index("--gear") + 1] if "--gear" in a else ""
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 300
POKE = "--poke" in a or "--pokeonly" in a
ACTION = a[a.index("--action") + 1] if "--action" in a else None
ONLY = int(a[a.index("--only-frame") + 1]) if "--only-frame" in a else None
ROOT = os.path.dirname(HERE)


def unlit(objs, img=None):
    for o in objs:
        for s in o.material_slots:
            m = s.material
            if not m or not m.node_tree:
                continue
            nt = m.node_tree
            if img:
                for nd in nt.nodes:
                    if nd.type == 'TEX_IMAGE':
                        nd.image = img
                        nd.image.colorspace_settings.name = 'sRGB'
            b = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
            out = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            L = b.inputs['Base Color'].links if b else []
            if L:
                nt.links.new(L[0].from_socket, em.inputs['Color'])
            nt.links.new(em.outputs['Emission'], out.inputs['Surface'])


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
unlit(body, img)
BV, BT, names, W, tree = G.body_sampler(body[0])
worn, fitinfo = [], []
for item in [s for s in SPEC.split(",") if s]:
    parts = item.split(":")
    nm, mode = parts[0], parts[1]
    bones = parts[2].split("|") if len(parts) > 2 and parts[2] else []
    split = len(parts) > 3 and parts[3] == "split"
    faces = dict(helmet=12000, bracers=12000, byrnie=26000, mantle=24000,
                 axe=9000, shield=9000).get(nm, 16000)
    # A helmet is WORN OVER HAIR, so pushing it out of the body pushes it out
    # of the braid and flattens it onto the scalp: 5021 of its 6000 vertices
    # read as "inside" purely because the base build's hair is a solid volume.
    # Rigid pieces that sit on top of something are not offset; the garments,
    # which must not show skin through them in motion, are.
    offs = dict(helmet=0.0, bracers=0.002, byrnie=0.005, mantle=0.008,
                axe=0.0, shield=0.0).get(nm, 0.004)
    before = set(sc.objects)
    srcdir = "builds" if mode == "socket" else "pieces"
    pc = G.import_piece(os.path.join(ROOT, srcdir, "%s.glb" % nm), before)
    n0, n1 = G.decimate(pc, faces)
    if offs > 0:
        P, pushed = G.clear_body(pc, tree, offs)
    else:
        co = np.empty(len(pc.data.vertices) * 3)
        pc.data.vertices.foreach_get("co", co)
        P, pushed = co.reshape(-1, 3), 0
    if mode == "socket":
        ln = float(parts[3]) if len(parts) > 3 else 0.82
        gr = float(parts[4]) if len(parts) > 4 else 0.3
        # AXE: haft up so the head rides high, cutting edge forward (-Y) so it
        # leads a forward swing. SHIELD: the disc's NORMAL outward on his left
        # (+X), boss forward, sitting on the outside of the forearm.
        SPECS = dict(
            axe=dict(axis_world=(0, 0, 1), face_world=(0, -1, 0),
                     offset_world=(0, 0, 0), anchor="head"),
            shield=dict(axis_world=(1, 0.70, 0), face_world=(0, -1, 0),
                        offset_world=(0.20, -0.18, -0.13), anchor="normal"))
        sp = SPECS.get(nm, dict(axis_world=(0, 0, 1), face_world=(0, -1, 0),
                                offset_world=(0, 0, 0), anchor="head"))
        info = G.socket_weapon2(pc, arm, bones[0], ln, gr, **sp)
        G.align_space(pc, body[0])
        made = [(pc, bones[0])]
        ok = len(pc.data.vertices)
        print("      socket %s: %s" % (nm, info))
    elif mode == "skin":
        ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
        G.align_space(pc, body[0])
        made = [(pc, "skinned")]
    else:
        made = G.bone_bind(pc, arm, bones, split)
        for o, _ in made:
            G.align_space(o, body[0])
        ok = len(pc.data.vertices)
    unlit([o for o, _ in made])
    worn += [o for o, _ in made]
    fitinfo.append(dict(piece=nm, mode=mode, faces_in=n0, faces_out=n1,
                        pushed_out=pushed, bound=ok,
                        bones=[b for _, b in made]))
    print("  + %-8s %-5s %6d -> %5d faces, %d pushed out, bound to %s"
          % (nm, mode, n0, n1, pushed, [b for _, b in made]))
    if nm == "helmet":
        mv, ca, kk = G.helmet_on_key(body[0], made[0][0], arm)
        kk.value = 1.0
        print("      helmet_on shape key: %d of %d candidate head vertices "
              "pulled under the dome" % (mv, ca))
        fitinfo[-1]["helmet_on_moved"] = mv
        fitinfo[-1]["helmet_on_candidates"] = ca

if ACTION:
    acts = {x.name: x for x in bpy.data.actions}
    assert ACTION in acts, "no action %s in %s" % (ACTION, list(acts))
    arm.animation_data.action = acts[ACTION]
act = arm.animation_data.action if arm.animation_data else None
f0, f1 = (int(v) for v in act.frame_range) if act else (1, 2)
nfr = max(1, f1 - f0)
if ONLY is not None:
    f0, nfr = f0 + ONLY, 1
V = []
for o in body:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); lo, hi = V.min(0), V.max(0); H = float(hi[2] - lo[2])
ctr = Vector((0.0, 0.0, float(lo[2] + hi[2]) * 0.5))

poke = None
if POKE and worn:
    # poke-through: a worn vertex that ends up INSIDE the posed body
    dg = bpy.context.evaluated_depsgraph_get()
    worst = (-1, -1.0, 0)
    per = []
    for i in range(nfr):
        sc.frame_set(f0 + i)
        dg = bpy.context.evaluated_depsgraph_get()
        eb = body[0].evaluated_get(dg)
        bt = BVHTree.FromObject(eb, dg)
        inv = eb.matrix_world.inverted()
        n_in = 0; tot = 0
        for o in worn:
            eo = o.evaluated_get(dg); me = eo.to_mesh()
            cv = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", cv)
            pts = (cv.reshape(-1, 3) @ np.array(eo.matrix_world.to_3x3()).T
                   + np.array(eo.matrix_world.translation))
            tot += len(pts)
            for p in pts[::3]:
                hit = bt.find_nearest(inv @ Vector(p.tolist()))
                if hit[0] is None:
                    continue
                if (Vector(p.tolist()) - (eb.matrix_world @ hit[0])).dot(
                        eb.matrix_world.to_3x3() @ hit[1]) < 0:
                    n_in += 1
            eo.to_mesh_clear()
        frac = 100.0 * n_in / max(tot / 3.0, 1)
        per.append(round(frac, 3))
        if frac > worst[1]:
            worst = (i, frac, n_in)
    poke = dict(per_frame_pct=per, worst_frame=worst[0],
                worst_pct=round(worst[1], 3), worst_verts=worst[2])
    print("  poke-through: worst frame %d at %.2f%% of sampled gear vertices "
          "inside the body (mean %.2f%%)" % (worst[0], worst[1], float(np.mean(per))))

if "--pokeonly" in a:
    json.dump(dict(clip=os.path.basename(CLIP), gear=SPEC, fit=fitinfo, poke=poke),
              open(os.path.join(OUT, "info.json"), "w") if os.path.isdir(OUT)
              else open(OUT, "w"), indent=1)
    print("poke only; no render")
    raise SystemExit(0)
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = H * 1.40
FAC = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
el = math.radians(EL)
os.makedirs(OUT, exist_ok=True)
for f in FAC:
    az = math.radians((360 - FAC[f]) % 360)
    pos = ctr + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                        math.sin(el))) * (10 * H)
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    for i in range(nfr):
        sc.frame_set(f0 + i)
        sc.render.filepath = os.path.join(OUT, "%s_%03d.png" % (f, i))
        bpy.ops.render.render(write_still=True)
json.dump(dict(clip=os.path.basename(CLIP), gear=SPEC, frames=nfr, fps=sc.render.fps,
               elev=EL, res=RES, facings=list(FAC), fit=fitinfo, poke=poke),
          open(os.path.join(OUT, "info.json"), "w"), indent=1)
print("rendered %d facings x %d frames" % (len(FAC), nfr))
