# R-C9-98: drop the weapon_r channels of ONE clip in the battle mage's own body copy (binary glTF patch).
#   python3 s37_drop_weapon_track.py <in.glb> <out.glb> <clip> [--json f]
# WHY: D7 baked a weapon_r track into cast_meteor for the 1.75 m STAFF (a rotation + a ground slide that plants the butt in
# the snow). The wand rides the same bone, so in frames 42-60 that track carried it up to 0.55 m out of her fist
# (work/clearance_wand_v7.json). With the channels gone, weapon_r holds its rest under the hand and the wand stays gripped.
# Only this file changes (body/so-body_battlemage_*.glb, the battle mage's model); so_d7's staff body is untouched.
# Every other clip is verified byte-identical in its sampler data.
import json, sys
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
a = sys.argv[1:]; IN, OUT, CLIP = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '_drop.json')
js, b = L.load_glb(IN)
wr = next(i for i, n in enumerate(js['nodes']) if n.get('name') == 'weapon_r')
other_before = json.dumps([an for an in js['animations'] if an.get('name') != CLIP], sort_keys=True)
an = next(x for x in js['animations'] if x.get('name') == CLIP)
drop = [c for c in an['channels'] if c['target'].get('node') == wr]
keep = [c for c in an['channels'] if c['target'].get('node') != wr]
used = sorted({c['sampler'] for c in keep}); smap = {s: i for i, s in enumerate(used)}
an['samplers'] = [an['samplers'][s] for s in used]
for c in keep:
    c['sampler'] = smap[c['sampler']]
an['channels'] = keep
assert json.dumps([x for x in js['animations'] if x.get('name') != CLIP], sort_keys=True) == other_before
R_.write_glb(OUT, js, bytes(b))
rep = dict(input=IN, out=OUT, clip=CLIP, weapon_r_node=wr, channels_dropped=[c['target']['path'] for c in drop],
           channels_left=len(keep), other_clips_identical=True)
json.dump(rep, open(OUTJ, 'w'), indent=1); print(json.dumps(rep))
