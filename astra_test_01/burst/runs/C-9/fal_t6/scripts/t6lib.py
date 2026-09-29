# C-9 T6 bake-off shared primitives (drax).
#
# ONE camera convention for the whole test, and it is NOT the sprite pipeline's.
# Matt ruling R-C9-68: characters are seen at the world camera's REAL angle,
# orthographic, 52.95354112560294 deg elevation -- not the 19.77 deg of the old
# sprite convention. Every T6 render uses ELEV below unless a call passes 0.0
# explicitly (the side-on geometry read, and the silhouette-IoU pass which must
# match the painted input views' flat elevation).
#
# Canonical frame, same as meshy_t2/scripts/t6lib: Z up, character faces +Y,
# feet on z = 0, midline x = 0, metres. Camera azimuth 0 ("S") sits at +Y and
# looks back down -Y, so azimuth 0 sees the FACE.
import math
import numpy as np
from mathutils import Vector, Matrix

ELEV = 52.95354112560294          # Matt R-C9-68, the world camera's real angle
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
# The four painted input views, as azimuths in THIS frame. Derived, not guessed:
# a camera at az 90 (+X) looking at a model facing +Y has world -Y on its screen
# right, so the model's nose points screen-RIGHT -- which is the painted "right"
# view. Az 270 mirrors it and is "left". Checked against the sheets: the
# manticore's "left" plate has its head at screen left.
INPUT_AZI = {"front": 0, "right": 90, "back": 180, "left": 270}


def mesh_objects(sc):
    return [o for o in sc.objects if o.type == 'MESH' and len(o.data.vertices)]


def verts_world(objs):
    out = []
    for o in objs:
        M = o.matrix_world
        co = np.empty(len(o.data.vertices) * 3)
        o.data.vertices.foreach_get("co", co)
        out.append(co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation))
    return np.vstack(out)


def apply_world(sc, M):
    """Left-multiply every root object's world matrix. Roots only, so parented
    children and armature-skinned meshes ride along instead of being moved twice.

    The view_layer.update() is NOT optional. A child's matrix_world is CACHED;
    moving its parent does not refresh it until the depsgraph is evaluated. Four
    of the twelve models (both Trellis 2 and both Hi3D) ship the mesh under a
    parent node, so without this every later verts_world() read the PRE-
    transform positions -- and read them silently, returning a clean array of
    plausible numbers. The renders came out right (the depsgraph had caught up
    by render time) while the measurements did not, which is the worst possible
    split: the head close-ups were aimed at the chest and the recorded bounding
    boxes were the delivered ones wearing the normalised ones' name."""
    import bpy
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = M @ o.matrix_world
    bpy.context.view_layer.update()


def normalise(sc, objs, yaw_deg=0.0, flip_x=False, target_h=1.0):
    """Put the model in the canonical frame.

    yaw_deg  rotation about Z applied FIRST, to bring the model's own front
             round to +Y. Measured per generator, not assumed -- see
             fal_t6/compare/orientation.json for what each one needed.
    flip_x   mirror across the midline, for a model that came out handed wrong.
    target_h uniform scale so the figure's overall height is target_h metres,
             then feet to z = 0 and midline x = 0.
    """
    if flip_x:
        apply_world(sc, Matrix.Scale(-1.0, 4, Vector((1, 0, 0))))
        for o in objs:
            o.data.flip_normals()
    if yaw_deg:
        apply_world(sc, Matrix.Rotation(math.radians(yaw_deg), 4, 'Z'))
    P = verts_world(objs)
    h = float(P[:, 2].max() - P[:, 2].min())
    S = target_h / h
    apply_world(sc, Matrix.Scale(S, 4))
    P = verts_world(objs)
    T = Matrix.Translation(Vector((-float(np.median(P[:, 0])), 0.0, -float(P[:, 2].min()))))
    apply_world(sc, T)
    P = verts_world(objs)
    mn, mx = P.min(0), P.max(0)
    # Check the transform actually landed. A normalise that quietly no-ops
    # returns the delivered mesh wearing the normalised mesh's name, and every
    # number downstream inherits that without a single error.
    assert abs(float(mx[2] - mn[2]) - target_h) < 1e-3, \
        f'height {float(mx[2]-mn[2]):.4f} != target {target_h}'
    assert abs(float(mn[2])) < 1e-3, f'feet at z={float(mn[2]):.4f}, not 0'
    return dict(scale=round(S, 6), yaw_deg=yaw_deg, flip_x=flip_x,
                bbox_min=[round(v, 4) for v in mn.tolist()],
                bbox_max=[round(v, 4) for v in mx.tolist()])


def unlit(objs):
    """Emission = the material's colour map. Judges the texture as PAINT, with
    no lighting term to flatter or hide it.

    NOT just Base Color. Rodin v2.5 with material="Shaded" delivers a BLACK
    Base Color and routes its 2K map into Emission Color at strength 1 -- so the
    naive base-colour-only version of this helper rendered Rodin as a pure black
    silhouette, four times, and the instrument looked like it was working. Take
    Base Color when it is linked, Emission Color when it is not, and record
    which was used per model so the difference is on the sheet, not hidden.
    Returns e.g. {'Material_0': 'base_color'}."""
    used = {}
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.node_tree:
                continue
            nt = m.node_tree
            out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None)
            b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if out is None or b is None:
                continue
            em = nt.nodes.new('ShaderNodeEmission')
            if b.inputs['Base Color'].links:
                nt.links.new(b.inputs['Base Color'].links[0].from_socket, em.inputs['Color'])
                used[m.name] = 'base_color'
            elif 'Emission Color' in b.inputs and b.inputs['Emission Color'].links:
                nt.links.new(b.inputs['Emission Color'].links[0].from_socket, em.inputs['Color'])
                used[m.name] = 'emission'          # Rodin "Shaded": baked light
            else:
                em.inputs['Color'].default_value = b.inputs['Base Color'].default_value
                used[m.name] = 'flat_base_color'
            nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    return used


def clay(objs):
    """Strip every material to one neutral diffuse grey, so the LIT pass reads
    geometry only. Texture cannot flatter a lumpy surface or hide a seam."""
    import bpy
    m = bpy.data.materials.new('t6_clay')
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (0.62, 0.60, 0.58, 1.0)
    b.inputs['Roughness'].default_value = 0.62
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.35
    elif 'Specular' in b.inputs:
        b.inputs['Specular'].default_value = 0.35
    for o in objs:
        o.data.materials.clear()
        o.data.materials.append(m)
    return m


def key_light(sc, aim, h):
    """One soft key from screen upper-left plus a low ambient fill. The key is
    parented to nothing and lives in world space at azimuth -45 from the camera
    ring's S, which puts it upper-left for the S/SE views and keeps a consistent
    read across the four clay directions."""
    import bpy
    d = bpy.data.lights.new('key', 'AREA')
    d.energy = 900.0
    d.size = 3.0 * h
    ob = bpy.data.objects.new('key', d)
    sc.collection.objects.link(ob)
    a, el = math.radians(-38), math.radians(40)
    pos = Vector(aim) + Vector((math.sin(a) * math.cos(el), math.cos(a) * math.cos(el),
                                math.sin(el))) * (6.0 * h)
    ob.location = pos
    ob.rotation_euler = (Vector(aim) - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.world = bpy.data.worlds.new('w')
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.30, 0.32, 0.36, 1.0)
    bg.inputs['Strength'].default_value = 0.55
    return ob


def setup_scene(res=512, transparent=True):
    import bpy
    sc = bpy.context.scene
    eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
    sc.render.resolution_x = res
    sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    return sc


def make_camera(sc, ortho_scale):
    import bpy
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ortho_scale
    cam.data.clip_start = 0.001
    return cam


def place_camera(cam, az_deg, aim, dist, elev=ELEV):
    A, el = math.radians(az_deg), math.radians(elev)
    aim = Vector(aim)
    pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                        math.sin(el))) * dist
    cam.location = pos
    cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    return pos
