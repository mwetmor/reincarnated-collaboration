# Holes in an isolated garment = small BOUNDARY LOOPS. A garment has a few long loops (neck,
# hem, cuffs, front opening); a hole left by an isolation predicate is a short loop inside it.
#   blender -b -noaudio --python scripts/s11_holes.py -- <piece.glb> [...]
import bpy, bmesh, sys, json
import numpy as np
res = {}
for p in sys.argv[sys.argv.index('--') + 1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=p)
    obs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and len(o.data.vertices) > 200]
    loops_all = []
    for ob in obs:
        bm = bmesh.new(); bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)     # weld UV-seam splits first
        bd = [e for e in bm.edges if e.is_boundary]
        seen = set()
        for e in bd:
            if e.index in seen:
                continue
            # walk the loop
            n, stack = 0, [e]
            while stack:
                x = stack.pop()
                if x.index in seen:
                    continue
                seen.add(x.index); n += 1
                for v in x.verts:
                    for y in v.link_edges:
                        if y.is_boundary and y.index not in seen:
                            stack.append(y)
            loops_all.append(n)
        bm.free()
    L = np.array(sorted(loops_all, reverse=True))
    small = int((L <= 40).sum())
    res[p.split('/')[-1]] = dict(loops=len(L), longest=L[:5].tolist(), small_loops_le_40_edges=small,
                                 edges_in_small_loops=int(L[L <= 40].sum()))
    print("%-12s %5d boundary loops; longest %s; SMALL (<=40 edges): %5d loops, %6d edges"
          % (p.split('/')[-1], len(L), L[:5].tolist(), small, int(L[L <= 40].sum())))
