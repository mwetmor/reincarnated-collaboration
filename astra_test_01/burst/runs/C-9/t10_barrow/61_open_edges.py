"""C-9 T10-1c: gandalf's instrument -- weld by position, count edges used by ONE triangle.

    blender --background --python 61_open_edges.py -- <glb> [glb ...]

Written to his definition rather than to mine, and run first on the files he measured, so
that a disagreement shows up as a disagreement instead of as a conclusion. My own probe
counted `not is_manifold`, which lumps a 1-face edge together with a 3-face edge; his
counts only the 1-face ones, and on these meshes those are two different populations of
identical size, so the two instruments differ by exactly 2x and neither is wrong. His is
the one that means "hole".

Also reported, because the distinction decides whether a mesh is worth re-reducing:

    pieces      connected components AFTER the weld. Many pieces is a SHATTER.
    open_edges  edges with one triangle. Many of these with ONE piece is a mesh that is
                still in one piece and cracked along its seams -- which is the barrow
                stones, and is a different defect with a different severity.
    edges_3     edges with three or more triangles: the other half of a T-junction, and
                the reason a weld can close a crack and still not leave a closed surface.
"""
import json
import os
import sys

import bmesh
import bpy

paths = sys.argv[sys.argv.index("--") + 1:]
WELD = 1e-5
out = []
for src in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    # A rigged glTF makes Blender GENERATE a bone display mesh ("Icosphere", 80 tris, in a
    # collection called glTF_not_exported) that is not in the file. Anything that counts
    # meshes after an import has to drop it or it counts the importer.
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"
              and not any(c.name == "glTF_not_exported" for c in o.users_collection)]
    bm = bmesh.new()
    for o in meshes:
        m = o.data.copy()
        m.transform(o.matrix_world)
        bm.from_mesh(m)
        bpy.data.meshes.remove(m)
    for o in meshes:
        o.data.calc_loop_triangles()
    tris = sum(len(o.data.loop_triangles) for o in meshes)
    v0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=WELD)
    bm.verts.ensure_lookup_table()
    openv = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    e3 = sum(1 for e in bm.edges if len(e.link_faces) > 2)
    wire = sum(1 for e in bm.edges if len(e.link_faces) == 0)
    seen, pieces = set(), 0
    for v in bm.verts:
        if v.index in seen:
            continue
        pieces += 1
        st = [v]
        seen.add(v.index)
        while st:
            c = st.pop()
            for e in c.link_edges:
                o2 = e.other_vert(c)
                if o2.index not in seen:
                    seen.add(o2.index)
                    st.append(o2)
    lo = [min(v.co[i] for v in bm.verts) for i in range(3)]
    hi = [max(v.co[i] for v in bm.verts) for i in range(3)]
    r = {"file": src, "tris": tris, "verts_raw": v0, "verts_welded": len(bm.verts),
         "edges": len(bm.edges), "open_edges": openv, "edges_3plus": e3, "wire_edges": wire,
         "pieces": pieces,
         # report in glTF axes: Blender (X, Y, Z) came from glTF (x, z, -y)
         "aabb_min_gltf": [round(lo[0], 6), round(lo[2], 6), round(-hi[1], 6)],
         "aabb_max_gltf": [round(hi[0], 6), round(hi[2], 6), round(-lo[1], 6)],
         "size_gltf": [round(hi[0] - lo[0], 6), round(hi[2] - lo[2], 6), round(hi[1] - lo[1], 6)]}
    bm.free()
    out.append(r)
    print("[open] %-46s tris %8d  open %6d  e3+ %6d  pieces %5d  size %s"
          % (os.path.basename(src), tris, openv, e3, pieces, r["size_gltf"]))
print("[openjson] %s" % json.dumps(out))
