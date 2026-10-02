# DEFECT FIX (stage K): Godot builds each GLB's Skeleton3D in that FILE's node order, and binds a skin by bone INDEX; a piece
# exported by Blender and a body written by Meshy + binary patches order their joint nodes differently (rig 3: completely), so
# every piece rode the wrong bones in Godot while Blender (which binds by vertex-group NAME) showed it right. This rewrites a
# piece's node array so its joint nodes appear in EXACTLY the body's joint-node order (all indices remapped: children, skins,
# skeleton, mesh nodes, scenes, animations). Geometry, weights and IBMs are untouched.
#   python3 e47_node_order.py <body.glb> <piece.glb> [<piece.glb> ...]   (in place)
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
body = sys.argv[1]; jb, _ = L.load_glb(body)
border = [jb['nodes'][i]['name'] for i in range(len(jb['nodes'])) if i in set(jb['skins'][0]['joints'])]
for p in sys.argv[2:]:
    js, b = L.load_glb(p); nodes = js['nodes']; jset = set(js['skins'][0]['joints'])
    name = {i: nodes[i].get('name') for i in range(len(nodes))}
    jidx = {name[i]: i for i in jset}
    extra = [n for n in [name[i] for i in sorted(jset)] if n not in border]
    assert set(border) <= set(jidx) and all(n.startswith('cape_') for n in extra), "%s: joint set differs from the body's (extras must be cape_*)" % p
    others = [i for i in range(len(nodes)) if i not in jset]
    # keep non-joint nodes in their relative order, joints in the body's order, joints placed where the first joint was
    first = min(jset); newold = [i for i in others if i < first] + [jidx[n] for n in border] + [jidx[n] for n in extra] + [i for i in others if i > first]
    o2n = {o: n for n, o in enumerate(newold)}
    js['nodes'] = [nodes[o] for o in newold]
    for nd in js['nodes']:
        if 'children' in nd: nd['children'] = [o2n[c] for c in nd['children']]
    for sk in js['skins']:
        sk['joints'] = [o2n[j] for j in sk['joints']]
        if 'skeleton' in sk: sk['skeleton'] = o2n[sk['skeleton']]
    for sc in js['scenes']: sc['nodes'] = [o2n[n] for n in sc['nodes']]
    for an in js.get('animations', []):
        for ch in an['channels']: ch['target']['node'] = o2n[ch['target']['node']]
    R_.write_glb(p, js, bytearray(b))
    js2, _ = L.load_glb(p); after = [js2['nodes'][i]['name'] for i in range(len(js2['nodes'])) if i in set(js2['skins'][0]['joints'])]
    r = L.lint(p); print(os.path.basename(p), 'joint node order == body:', after[:len(border)] == border, 'extras', len(after) - len(border), '| lint', r['verdict'], r['fails'][:2])
