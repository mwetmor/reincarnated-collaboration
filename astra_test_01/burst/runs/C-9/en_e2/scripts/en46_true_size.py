# EN-E2 TRUE SIZE (the conductor, after group 1; the KC2 drax's contract ruling KP-222): for a kit whose body ships smaller than its true
# size (a canvas size call), each roster record's factor from the SHIPPED height to its TRUE height, so the runtime can scale the cells back
# when its per-kit ppm allows. EN-E3's en-voiddrone block is the format.
# BASIS (stated, because the roster's own mesh heights cannot be used: field_grades -- "mesh_aabb_*_meshspace ... Lap F ruled it a FAILED
# body-size discriminator ... Do not use as a world height"): the roster's per-record SCALE is DATAMINED and is the game's own size ratio
# between records of one rig. The absolute anchor is OUR designed height for the reference record (the art call made on the model sheet:
# the height the body was built and rigged at). So: true_height(rec) = designed_height x scale(rec) / scale(ref); factor = true / shipped.
#   python3 scripts/en46_true_size.py <g> <type_id> <designed_m> <ref record substring> [--only rec1,rec2]
# --only (round 7 group 2): a BOSS MESH on a shared rig serves only its own records; the block lists just those (the reference
# record may be outside the list: it anchors the scale, e.g. the acolyte at scale 1.0 for the hero01/heroine01 boss meshes).
import json, os, sys
g, TID, DES, REF = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-02-crucible-enemy-roster-packet/roster.json'
d = json.load(open(R)); t = next(x for x in d['types'] if x['type_id'] == TID)
H = json.load(open(os.path.join(E, 'export/final_%s/height.json' % g))); SHIP = float(H['target_m'])
ref = next(m for m in t['members_detail'] if REF in m['record'] or REF in m['display_name'])
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
groups = {}
for m in t['members_detail']:
    if ONLY and os.path.basename(m['record']).replace('.dbr', '') not in ONLY: continue
    key = (round(float(m['scale']), 4))
    groups.setdefault(key, []).append(m)
recs = {}
for sc, ms in sorted(groups.items()):
    roles = sorted({m['role'] for m in ms}); names = sorted({os.path.basename(m['record']).replace('.dbr', '') for m in ms})
    true = DES * sc / float(ref['scale'])
    label = '%s (%s)' % ('/'.join(names[:4]) + ('/...' if len(names) > 4 else ''), '/'.join(roles))
    recs[label] = dict(scale=sc, true_height_m=round(true, 3), factor=round(true / SHIP, 3), e_bodies=round(sum(m['e_bodies_151_160_p06_off'] for m in ms), 3))
out = dict(base_height_m=SHIP, designed_height_m=DES, reference_record=os.path.basename(ref['record']), reference_scale=float(ref['scale']),
           note='conductor size call: one shipped base mesh; the runtime scales each record by factor = true/shipped when the per-kit ppm allows (KC2 side, KP-222). '
                'true = designed height x scale(record) / scale(reference record): the roster SCALE is DATAMINED; the roster mesh heights are not usable (Lap F).',
           records=recs)
p = os.path.join(E, 'work/%s_true_size.json' % g); json.dump(out, open(p, 'w'), indent=1)
print('TRUE_SIZE', g, SHIP, {k: v['factor'] for k, v in recs.items()})
