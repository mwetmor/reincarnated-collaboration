# D7 assembly: her body with its clips and painted texture, plus every gear piece fitted,
# skinned and exported -- D2's sequence (15_export_scene), without the barbarian-specific
# morphs, carry poses and shield work.
#
#   blender -b -noaudio --python scripts/s9_assemble.py -- <body.glb> <tex.png> <outdir> [--json f]
#
#   deforming  robe, mantle, belt   isolated -> decimated -> pushed off the body -> skinned
#                                   (weights transferred from the nearest body point)
#   rigid      bracers              isolated -> bound to the forearms, one bone per side
#              circlet              PROCEDURAL, see below -> bound to Head
#   weapon     staff                socketed to RightHand, shaft centred through the fist;
#                                   52_weapon_bones later rebinds it to weapon_r
#
# LAYER OFFSETS are measured off the BODY, as D2's were. The belt goes on at 12 mm so it sits
# OUTSIDE the robe at the waist, where a belted robe is cinched to within about a centimetre.
#
# THE CIRCLET IS PROCEDURAL. It is part of the approved costume, and its Tripo isolation did
# not separate: a ~1 cm band pressed to the scalp came out either with her whole face attached
# (24,726 verts) or in fragments (1,455 verts, 3 components). At the play camera, 100.6 px/m,
# a 1 cm band is about ONE PIXEL. So it is realised directly -- a bronze band fitted to the
# MEASURED head cross-section at brow height, and a small ember stone at the front -- and the
# manifest says so. It is the one gear piece not built by the stated method.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s9_assemble.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODYGLB, TEX, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ROOT = os.path.dirname(HERE)
PIECES = a[a.index('--pieces') + 1] if '--pieces' in a else os.path.join(ROOT, "pieces")
os.makedirs(OUT, exist_ok=True)
rep = dict(pieces={})

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODYGLB)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
for o in body:
    for s_ in o.material_slots:
        if s_.material and s_.material.node_tree:
            for nd in s_.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img
                    nd.image.colorspace_settings.name = 'sRGB'
# REST before fitting: bone heads are read POSED, and an import leaves an action active
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0])
H = float(BV[:, 2].max() - BV[:, 2].min())
print("body %.4f m, %d clips" % (H, len(bpy.data.actions)))
made = []

def extend_boundary(pc, dist):
    """HEM OVERLAP: move every boundary vertex `dist` outward ALONG THE SURFACE, perpendicular to
    its boundary. The last white speckles were a 1-px crack of linen down the top of the robe's
    front split, where the two panels converge to a hairline instead of meeting -- two edges that
    do not overlap, which no closing of the isolation can fix because nothing lies between them.
    Overlapping the edges closes the hairline and covers any notch left on any hem. Runs BEFORE
    clear_body, so the body push still corrects anything this tips inward."""
    import bmesh
    bm = bmesh.new(); bm.from_mesh(pc.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.verts.ensure_lookup_table(); bm.normal_update()
    move = {}
    for e in bm.edges:
        if not e.is_boundary or not e.link_faces:
            continue
        f = e.link_faces[0]
        a_, b_ = e.verts[0].co, e.verts[1].co
        t = (b_ - a_).normalized()
        n = f.normal
        o = t.cross(n).normalized()
        mid = (a_ + b_) * 0.5
        if (f.calc_center_median() - mid).dot(o) > 0:      # point AWAY from the garment interior
            o = -o
        for v in e.verts:
            move.setdefault(v.index, Vector((0, 0, 0)))
            move[v.index] += o
    for vi, o in move.items():
        if o.length > 1e-9:
            bm.verts[vi].co += o.normalized() * dist
    bm.to_mesh(pc.data); bm.free(); pc.data.update()
    return len(move)


DEFORM = [("robe", 30000, 0.006), ("mantle", 22000, 0.010), ("belt", 14000, 0.012)]
# per-piece face targets are overridable for the decimation experiment: ROBE_FACES=90000 etc.
DEFORM = [(nm, int(os.environ.get(nm.upper() + "_FACES", f)), o) for nm, f, o in DEFORM]
for nm, faces, offs in DEFORM:
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(PIECES, "%s.glb" % nm), before)
    f0 = len(pc.data.polygons)
    # WELD THE UV SEAMS BEFORE DECIMATING (pass 2). glTF stores a vertex once per UV island, so an
    # imported piece is cut along every seam, and the collapse decimator then thins each side of a
    # seam INDEPENDENTLY: the two edges stop coinciding and a hairline crack opens along the seam.
    # The 6 mm hem overlap was hiding most of those (it extends every boundary, seams included);
    # at the true play scale the fireball's back view still showed one (3 px at 2x, 20 cm of air
    # behind it). Welding co-located vertices joins the islands -- UVs are per face-corner, so each
    # face keeps its own -- and the decimator keeps the seams as seams. WELD=0 restores the old path.
    if os.environ.get("WELD", "1") != "0":
        _bm = bmesh.new(); _bm.from_mesh(pc.data)
        _n0 = len(_bm.verts)
        bmesh.ops.remove_doubles(_bm, verts=_bm.verts, dist=1e-5)
        _n1 = len(_bm.verts)
        _bm.to_mesh(pc.data); _bm.free(); pc.data.update()
        rep.setdefault("welded", {})[nm] = dict(verts_before=_n0, verts_after=_n1)
        print("  %-8s welded %d -> %d verts before decimation" % (nm, _n0, _n1))
    G.decimate(pc, faces)
    HEM = {"robe": 0.006, "mantle": 0.004, "belt": 0.004}
    nb = extend_boundary(pc, float(os.environ.get(nm.upper() + "_HEM", HEM.get(nm, 0.004))))
    P, pushed = G.clear_body(pc, tree, offs)
    ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
    G.align_space(pc, body[0])
    pc.name = nm
    made.append((nm, [pc]))
    rep["pieces"][nm] = dict(mode="skin", faces=[f0, len(pc.data.polygons)], offset_m=offs,
                             hem_overlap_m=HEM.get(nm, 0.004), boundary_verts_extended=int(nb),
                             pushed=int(pushed), skinned_verts=int(ok))
    print("  %-8s skinned: %d -> %d faces, pushed %d verts off the body by %.3f m"
          % (nm, f0, len(pc.data.polygons), pushed, offs))

before = set(sc.objects)
pc = G.import_piece(os.path.join(PIECES, "bracers.glb"), before)
G.decimate(pc, 10000)
P, pushed = G.clear_body(pc, tree, 0.003)
parts = G.bone_bind(pc, arm, ["RightForeArm", "LeftForeArm"], True)
for o, _ in parts:
    G.align_space(o, body[0])
made.append(("bracers", [o for o, _ in parts]))
rep["pieces"]["bracers"] = dict(mode="bone", bones=["RightForeArm", "LeftForeArm"],
                                objects=[o.name for o, _ in parts])
print("  bracers  bound: %s" % [(o.name, b) for o, b in parts])

# ---- the circlet, procedural, fitted to the MEASURED head -------------------------
hb = arm.pose.bones["Head"]
hh = np.array(arm.matrix_world @ hb.head); ht = np.array(arm.matrix_world @ hb.tail)
zb = float(BV[:, 2].min()) + 0.955 * H                      # brow band, above the eyebrows
ax = np.array([hh[0], hh[1]])
near = (np.abs(BV[:, 2] - zb) < 0.006) & (np.linalg.norm(BV[:, :2] - ax, axis=1) < 0.16)
Rh = float(np.percentile(np.linalg.norm(BV[near][:, :2] - ax, axis=1), 85)) if near.sum() > 20 else 0.095
ctr = np.array([np.median(BV[near][:, 0]), np.median(BV[near][:, 1])]) if near.sum() > 20 else ax
# THE BAND FOLLOWS THE HEAD'S OUTLINE, not a circle. The first fit took ONE radius -- the 85th
# percentile of scalp distance at brow height, 0.1226 m -- and the band floated 2-4 cm clear of her
# head all round: a halo. A head is longer than it is wide and her hair bulks it unevenly, so no
# single radius fits. Here, for each of 64 directions, the OUTERMOST scalp/hair point at brow
# height (within +/-4 deg of that direction), smoothed round the loop, plus 4 mm.
slab = BV[near][:, :2] - ctr
ang = np.arctan2(slab[:, 1], slab[:, 0]); rad = np.linalg.norm(slab, axis=1)
N = 64; th = np.linspace(-np.pi, np.pi, N, endpoint=False); rr = np.zeros(N)
for k, t in enumerate(th):
    d = np.abs((ang - t + np.pi) % (2 * np.pi) - np.pi)
    m = d < np.radians(4)
    rr[k] = rad[m].max() if m.sum() else np.nan
ok_ = ~np.isnan(rr)
rr = np.interp(th, th[ok_], rr[ok_], period=2 * np.pi)
rr = np.convolve(np.r_[rr[-3:], rr, rr[:3]], np.ones(7) / 7, mode="valid")   # smooth, circular
rr = rr + 0.004
pts = [Vector((float(ctr[0] + r_ * math.cos(t)), float(ctr[1] + r_ * math.sin(t)), zb)) for t, r_ in zip(th, rr)]
me_c = bpy.data.meshes.new("circlet")
me_c.from_pydata(pts, [(i, (i + 1) % N) for i in range(N)], [])
ob_c = bpy.data.objects.new("circlet", me_c); sc.collection.objects.link(ob_c)
bpy.context.view_layer.objects.active = ob_c
mod = ob_c.modifiers.new("skin", 'SKIN')
for v in me_c.skin_vertices[0].data:
    v.radius = (0.0045, 0.0045)
bpy.ops.object.select_all(action='DESELECT'); ob_c.select_set(True)
bpy.ops.object.modifier_apply(modifier="skin")
Rh = float(np.median(rr))
_front = float(rr[np.argmin(np.abs(th - (-np.pi / 2)))])     # -Y is her front
# the ember stone at the front of the brow (she faces -Y)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.011,
                                      location=(float(ctr[0]), float(ctr[1]) - (_front + 0.006), zb))
stone = bpy.context.active_object; stone.name = "circlet_stone"
for o, col, em in ((ob_c, (0.62, 0.42, 0.20, 1), 0.0), (stone, (0.95, 0.30, 0.08, 1), 2.5)):
    m = bpy.data.materials.new(o.name + "_mat"); m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = col
    bs.inputs["Metallic"].default_value = 0.85 if o is ob_c else 0.0
    bs.inputs["Roughness"].default_value = 0.35
    if em:
        bs.inputs["Emission Color"].default_value = col; bs.inputs["Emission Strength"].default_value = em
    o.data.materials.append(m)
bpy.ops.object.select_all(action='DESELECT'); ob_c.select_set(True); stone.select_set(True)
bpy.context.view_layer.objects.active = ob_c
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
g = ob_c.vertex_groups.new(name="Head")
g.add(list(range(len(ob_c.data.vertices))), 1.0, 'REPLACE')
mm = ob_c.modifiers.new('arm', 'ARMATURE'); mm.object = arm
G.align_space(ob_c, body[0])
made.append(("circlet", [ob_c]))
rep["pieces"]["circlet"] = dict(mode="bone", bones=["Head"], method="PROCEDURAL",
    band_height_m=round(zb, 4), band_radius_m=[round(float(rr.min()), 4), round(float(rr.max()), 4)],
    fit="the head's outline at brow height, 64 directions, +4 mm -- a single radius floated it as a halo",
    verts_in_slab=int(near.sum()),
    why=("Tripo isolation did not separate a ~1 cm band from the scalp: 24,726 verts with the whole "
         "face attached, or 1,455 verts in 3 fragments. At 100.6 px/m it is ~1 px in play."))
print("  circlet  PROCEDURAL: band at %.3f m following the head outline, radius %.4f-%.4f m (median %.4f), front %.4f, from %d scalp verts"
      % (zb, rr.min(), rr.max(), Rh, _front, near.sum()))

# ---- the staff ------------------------------------------------------------------
before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "builds", "staff.glb"), before)
G.decimate(pc, 9000)
info = G.socket_weapon2(pc, arm, "RightHand", 1.75, 0.55, axis_world=(0, 0, 1), face_world=(0, -1, 0))
moved = G.centre_shaft_on_fist(pc, body[0], arm, "RightHand")
G.align_space(pc, body[0])
pc.name = "staff"
made.append(("staff", [pc]))

# ---- grips: close the hands round the staff (the barbarian's method) -------------
# The rig has no finger bones, so the hands are closed with MORPHS, driven by the equipment.
# The channel comes from the HAND (gearlib.hand_frame): the across-palm axis a fist closes
# round -- which is also the axis 52_weapon_bones --roll seats the shaft onto, so the grip and
# the mount agree by construction. Radius: the staff's own shaft at the grip (thin core, 25th
# percentile), clamped as the barbarian's was, +10 mm for the fingers' thickness.
_r, _ = G.shaft_radius(pc, arm, "RightHand")
_r = float(min(max(_r, 0.012), 0.028))
rep["grips"] = {}
for _key, _bone in (("grip_R", "RightHand"), ("grip_L", "LeftHand")):
    _c, _chan, _al, _pal = G.hand_frame(body[0], arm, _bone)
    _k, _mv, _mx = G.grip_key(body[0], arm, _bone, _c, _chan, _r + 0.010, _key)
    if _k:
        _k.value = 0.0                      # OFF by default; the scene drives it
    rep["grips"][_key] = dict(bone=_bone, closes_to_m=round(_r + 0.010, 4), verts_moved=int(_mv),
                              max_travel_m=round(float(_mx), 4))
    print("  %s: closes to %.4f m, %d verts moved, max %.4f m" % (_key, _r + 0.010, _mv, _mx))

# ---- under-garment keys: pull the HIDDEN body in where the clips push it through the cloth ----
# The pass-2 speckle stills (five clips, posed through the staff layer) found 6 pale dots at 1x and
# 3 at 2x, and the Godot ID pass with the body HIDDEN showed garment BEHIND every one of them: the
# BODY in front of the cloth, not a hole. scripts/s14_poke.py measures it per body vertex as the
# clearance to the very garment point that covered it at rest, over every frame of every shipped
# clip, and dumps the worst depth per vertex (--dump). Given that file (--under), each garment gets a
# MORPH on the body, `under_<garment>`, that moves the vertices IT covers inward along their rest
# normals by that depth + MARGIN, spread over DILATE rings (decaying) so the dent has no rim, tapered
# to zero over TAPER rings at the edge of the covered region (a vertex no garment covers never moves).
# A morph, not an edit: the gear stack can show her without the robe, and the body must be whole
# then. The scene sets under_<g> = 1 while garment g is worn, as it sets grip_R with the staff.
UNDER = a[a.index('--under') + 1] if '--under' in a else None
if UNDER:
    from mathutils.kdtree import KDTree
    MARGIN, DILATE, DECAY, TAPER, CAP = 0.004, 6, 0.85, 2, 0.045
    U = np.load(UNDER)
    rp, dep, cvr = U["rest_pos"], U["depth"], U["cover"]
    gnames = [str(x) for x in U["garments"]]
    kd = KDTree(len(rp))
    for i, q in enumerate(rp):
        kd.insert(Vector(q.tolist()), i)
    kd.balance()
    bo = body[0]
    Mb = np.array(bo.matrix_world)
    nv = len(bo.data.vertices)
    co = np.empty(nv * 3); bo.data.vertices.foreach_get("co", co)
    nr = np.empty(nv * 3); bo.data.vertices.foreach_get("normal", nr)
    Wv = co.reshape(-1, 3) @ Mb[:3, :3].T + Mb[:3, 3]
    Nw = nr.reshape(-1, 3) @ np.linalg.inv(Mb[:3, :3]); Nw /= np.linalg.norm(Nw, axis=1, keepdims=True) + 1e-12
    D0 = np.zeros(nv); CV = np.full(nv, -1); matched = 0
    for i in range(nv):
        hits = kd.find_range(Vector(Wv[i].tolist()), 0.0005)
        if not hits:
            continue
        matched += 1
        ids = [h[1] for h in hits]
        D0[i] = float(dep[ids].max())
        cs = [int(cvr[j]) for j in ids if cvr[j] >= 0]
        if cs:
            CV[i] = max(set(cs), key=cs.count)
    e = np.empty(len(bo.data.edges) * 2, dtype=np.int64); bo.data.edges.foreach_get("vertices", e)
    e = e.reshape(-1, 2); e0, e1 = e[:, 0], e[:, 1]
    covd = CV >= 0
    D = np.where(D0 > 0, D0 + MARGIN, 0.0)
    for _ in range(DILATE):
        nb = np.zeros(nv)
        np.maximum.at(nb, e0, D[e1]); np.maximum.at(nb, e1, D[e0])
        D = np.where(covd, np.maximum(D, DECAY * nb), 0.0)
    ring = np.where(covd, np.inf, 0.0)
    for r_ in range(1, TAPER + 1):
        nb = np.full(nv, np.inf)
        np.minimum.at(nb, e0, ring[e1]); np.minimum.at(nb, e1, ring[e0])
        ring = np.minimum(ring, nb + 1)
    taper = np.clip(ring / float(TAPER), 0.0, 1.0)
    SH = np.minimum(D * taper, CAP)
    if not bo.data.shape_keys:
        bo.shape_key_add(name="Basis", from_mix=False)
    Mi = np.linalg.inv(Mb)
    rep["under_keys"] = dict(source=os.path.basename(UNDER), margin_m=MARGIN, dilate_rings=DILATE, decay=DECAY,
                             taper_rings=TAPER, cap_m=CAP, body_verts=int(nv), matched_to_dump=int(matched), keys={})
    # ONE key per garment NAME: the bracers are two objects (one per forearm) in the dump
    for gname_ in sorted(set(gnames)):
        gks = [k for k, g_ in enumerate(gnames) if g_ == gname_]
        sel = np.nonzero(np.isin(CV, gks) & (SH > 1e-5))[0]
        key = bo.shape_key_add(name="under_" + gname_, from_mix=False)
        key.value = 0.0                                # OFF by default; the scene drives it
        newp = Wv[sel] - Nw[sel] * SH[sel, None]
        loc = newp @ Mi[:3, :3].T + Mi[:3, 3]
        for vi, q in zip(sel, loc):
            key.data[int(vi)].co = Vector(q.tolist())
        rep["under_keys"]["under_" + gname_] = dict(verts_moved=int(len(sel)),
                                                     max_m=round(float(SH[sel].max()) if len(sel) else 0.0, 4),
                                                     median_m=round(float(np.median(SH[sel])) if len(sel) else 0.0, 4),
                                                     poke_verts=int((np.isin(CV, gks) & (D0 > 0)).sum()))
        print("  under_%-8s %6d verts in, max %.4f m, median %.4f m (%d measured pokes)"
              % (gname_, len(sel), rep["under_keys"]["under_" + gname_]["max_m"],
                 rep["under_keys"]["under_" + gname_]["median_m"], rep["under_keys"]["under_" + gname_]["poke_verts"]))
    print("  under keys: %d of %d body verts matched to the dump within 0.5 mm" % (matched, nv))

# ---- the staff carry layer: spine up + staff arm, from work/staff_carry.json -------
# Authored against the SEATED staff (scripts/s12_carry.py). Shipped the way shield_carry_L was:
# a two-frame pose clip plus the filter list, for the scene's filtered Blend2.
CP = os.path.join(ROOT, "work", "staff_carry.json")
assert os.path.exists(CP), "work/staff_carry.json missing -- run s12_carry first"
cp = json.load(open(CP))
act = bpy.data.actions.new("staff_carry_R")
arm.animation_data.action = act
for f in (0, 1):
    sc.frame_set(f)
    for bn, flat in cp["bones"].items():
        pbx = arm.pose.bones[bn]
        pbx.matrix_basis = Matrix([flat[i * 4:(i + 1) * 4] for i in range(4)])
        pbx.rotation_mode = 'QUATERNION'
        pbx.keyframe_insert("rotation_quaternion", frame=f)
        pbx.keyframe_insert("location", frame=f)
act.use_fake_user = True
arm.animation_data.action = None
for pbx in arm.pose.bones:
    pbx.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
tr = arm.animation_data.nla_tracks.new(); tr.name = "staff_carry_R"
tr.strips.new("staff_carry_R", 0, act)
rep["staff_carry_R"] = dict(filter_bones=cp["filter_bones"], authored=cp["measured"])
print("  staff_carry_R: %d bones, authored tilt %.2f deg" % (len(cp["bones"]), cp["measured"]["tilt_deg"]))
rep["pieces"]["staff"] = dict(mode="socket", bone="RightHand", length_m=1.75, grip=0.55,
                              socket=info, shaft_centred_m=moved)
print("  staff    socketed to RightHand: %s; shaft centred %s" % (info.get("span_scaled_m"), moved))


def export(objs, path, anim=False):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
                              export_animations=anim, export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
rep["files"] = {"so-body.glb": export(body, os.path.join(OUT, "so-body.glb"), anim=True)}
for nm, objs in made:
    rep["files"]["%s.glb" % nm] = export(objs, os.path.join(OUT, "%s.glb" % nm))
for k, v in rep["files"].items():
    print("wrote %-14s %6.2f MB" % (k, v))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
