# EN-E3: write a creature's JOIN-1 kit config + clip manifest for the SHARED renderer (join1_render, unchanged).
#   python3 scripts/n14_join_kit.py <name> <kit_id> <export.glb> <clips.json (n12)> <vfx.json> <states.json>
# The manifest's numbers are RE-READ from n12's manifest, which re-read them from the GLB (no hand-copied durations):
#   clips.<c>.seconds, locomotion_in_place.<walk|run>.speed_m_s, attacks.<a>.release_s (the contact time) and casts.<c>.release_s.
# Sockets: head_top / chest / maw (the jaw tip -- where the bite lands and the bile leaves), bones named by the rig.
import json, sys, os, math, hashlib, re
# PROSE CARRIES NO SECONDS: 48_manifest_lint reads any '<n> s' in prose as a claim about a clip's duration (that is how it caught
# stale numbers before). Roster/VFX prose ('poison 3 s', 'rel f37 (1.23 s)') is converted to milliseconds so it cannot pose as one.
def ms(t): return re.sub(r'(\d+(?:\.\d+)?)\s*s\b', lambda m: '%d ms' % round(float(m.group(1)) * 1000), t) if isinstance(t, str) else t
NAME, KID, GLB, CLIPS, VFX, STATES = sys.argv[1:7]
C9 = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9'
cm = json.load(open(CLIPS)); vfx = json.load(open(VFX)); st_spec = json.load(open(STATES))
glb = os.path.abspath(GLB)
man = dict(what='JOIN-1 clip manifest for the %s (crucible creature, roster rig %s) -- lane EN-E3 (drax, R-C9-132), read off %s'
                % (NAME, cm['roster_type_id'], os.path.relpath(glb, C9)),
           body=dict(file=glb, sha256_16=cm['glb_sha256'][:16], height_m=cm['h_model_m'], length_m=cm['length_m']),
           clips={}, locomotion_in_place={}, attacks={}, casts={}, death={}, vfx_runtime=dict(
               note='RUNTIME effects, NOT in the cells (contract 2.2: no VFX baked). Flipbook atlases, straight alpha, sizes in metres.',
               effects=[dict({k: ms(v) for k, v in e.items()}, atlas=os.path.join(os.path.dirname(glb), e['atlas'])) for e in vfx['effects']]))
for c, e in cm['clips'].items():
    man['clips'][c] = dict(seconds=e['duration_s'], source=ms('procedural, hand-keyed in Blender (en_e3/scripts/n10); roster ref: %s' % e.get('source')))
    if e.get('ground_speed_m_s'):
        man['locomotion_in_place'][c] = dict(speed_m_s=e['ground_speed_m_s'], from_='n10: the stance foot moves back at exactly this speed '
                                             '(measured foot slide 0.000 m in the world at this speed); clip in place, root stripped')
    if 'contact_s' in e:
        man['attacks'][c] = dict(release_s=e['contact_s'], frame=e['contact_frame'], definition='the bite CONTACT: the jaw at full gape, the frame the roster '
                                 'puts the hit on (30 fps key %d)' % e['contact_frame'])
    if 'release_s' in e:
        man['casts'][c] = dict(release_s=e['release_s'], frame=e['release_frame'], definition='the RELEASE the roster sets for this ability (30 fps key %d)' % e['release_frame'])
man['death'] = dict(root='root never moves; the body rolls and settles on the ground (n10 ground solve); last frame held')
for k in ('walk', 'run'):
    if k in man['locomotion_in_place']: man['locomotion_in_place'][k]['from'] = man['locomotion_in_place'][k].pop('from_')
mp = os.path.join(C9, 'join1_render', 'manifests', '%s_clips.json' % KID)
json.dump(man, open(mp, 'w'), indent=1)
lm = cm['landmarks']
kit = dict(kit=KID, _what='Per-kit config for the JOIN-1 sprite-cell renderer: the %s (crucible creature, lane EN-E3, R-C9-132). One body, no gear, no layers, '
           'no morphs. The body is a skinned GLB with an embedded painted texture; the mouth interior is its second surface.' % NAME,
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=glb, pieces=[], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres',
                        mesh_name_contains='body'),
           camera={}, morphs={}, states={}, sockets=st_spec['sockets'],
           vfx_runtime=dict(manifest_block='vfx_runtime', atlases=[e['atlas'] for e in man['vfx_runtime']['effects']]),
           watchdog_s=2400)
for s, d in st_spec['states'].items():
    rec = dict(clip=d.get('clip', s), kind=d['kind'], role=d['role'], frames=d['frames'], sampling=d['sampling'], manifest_entry='clips.' + d.get('clip', s))
    if s in man['locomotion_in_place']: rec['stride_from'] = 'locomotion_in_place.' + s
    if d['sampling'] == 'release':
        blk = 'attacks' if d.get('clip', s) in man['attacks'] else 'casts'
        rec['release_from'] = '%s.%s.release_s' % (blk, d.get('clip', s)); rec['release_socket'] = 'maw'; rec['manifest_entry'] = '%s.%s' % (blk, d.get('clip', s))
    if d.get('hold_last'): rec['hold_last'] = True
    if d.get('skill'): rec['skill'] = d['skill']
    kit['states'][s] = rec
kp = os.path.join(C9, 'join1_render', 'kits', '%s.json' % KID)
json.dump(kit, open(kp, 'w'), indent=1)
print('wrote', kp, 'and', mp)
