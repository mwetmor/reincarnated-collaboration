# EN-E2 round 4 -> JOIN-1: clip manifest + renderer kit for the BRUTE (b), the BOG-WRETCH (c) and the IMP (i) (en27's shape; numbers
# re-read from the shipped body's measure (en09), its death ground track and the VFX frame table; roster facts quoted with their source).
#   python3 scripts/en33_kit_r4.py <b|c|i>
import json, os, sys, hashlib
import numpy as np
g = sys.argv[1]; E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J = os.path.join(os.path.dirname(E), 'join1_render')
sys.path.insert(0, os.path.join(E, 'scripts')); C = __import__('s17_loop_closure')
KID = dict(b='en-brute', c='en-wretch', i='en-imp')[g]
VID = dict(b='en_b_blight', c='en_c_blood', i='en_i_aether')[g]
body = os.path.join(E, 'export/final_%s/en_%s_body.glb' % (g, g))
M = json.load(open(os.path.join(E, 'export/final_%s/en_%s_measure.json' % (g, g))))
H = json.load(open(os.path.join(E, 'export/final_%s/height.json' % g)))
GR = json.load(open(os.path.join(E, 'work/%s_graft.json' % g)))['clips']
TIP = json.load(open(os.path.join(E, 'work/%s_tips.json' % g)))
V = json.load(open(os.path.join(E, 'vfx/%s_frames.json' % VID)))
sha16 = hashlib.sha256(open(body, 'rb').read()).hexdigest()[:16]
m = C.model(body); hi = [i for i in m['joints'] if m['nodes'][i].get('name') == 'Hips'][0]
ts = sorted({float(t) for v in m['anims']['death'].values() for t in v[0]}); P = np.array([C.globals_at(m, 'death', t)[hi][:3, 3] for t in ts]); dtr = np.hypot(P[:, 0], P[:, 2])
ROSTER = dict(
    b=dict(rig='aetherialcorruption', tier1_rank=1, bodies=17.78, lead='Fleshwarped Aberration (aetherialcorruption_a01: scale 1.6, actorRadius 0.45 -> radius x scale 0.72 m; range 0.56-0.92)',
           run_m_per_s=[3.691, 4.012], style='melee 59 % / projectile 31 %', p05_bodies=10.99, spawn='aetherialcorruption_spawn_a01, 148 frames', spawn_clip_frames=148),
    c=dict(rig='cannibal', tier1_rank=12, bodies=5.65, lead='Ugdenbog Wretch (scale 0.9, actorRadius 0.8 -> 0.72 m; range 0.72-1.0)', run_m_per_s=[3.209, 3.53],
           style='melee 44 % / projectile 40 % / buff 12 %', p05_bodies=0.0),
    i=dict(rig='aetherialimp', tier1_rank=9, bodies=5.98, lead='Aetherial Scamp (scale 0.65, actorRadius 0.8 -> 0.52 m; range 0.52-0.68)', run_m_per_s=[3.209, 3.209],
           style='melee 91 %', p05_bodies=1.01, spawn='aetherialimp_spawn_a01, 47 frames', spawn_clip_frames=47))[g]
def src(c):
    if c in GR: return os.path.basename(GR[c]['source']).replace('.glb', '').replace('_', ' ') + ' (Mixamo)'
    return dict(emerge='en29: crouch idle (its first 31 keys) then crouch to standing idle (Pro Melee Axe), first 4 keys cross-faded')[c]
casts = {c: dict(release_s=v['release_s'], hand=v['hand'], definition='%s, the key that ENDS the fastest interval, on the clip\'s own 30 fps key %d' % (v['rule'], v['key']))
         for c, v in M['release'].items()}
vfx = dict(atlas=os.path.join(E, 'vfx', V['atlas']), frames=os.path.join(E, 'vfx/%s_frames.json' % VID), atlas_px=V['atlas_size'], atlas_sha256=V['sha256'],
           baked_px_per_m=V['px_per_m'], blend=V['blend'], sizes_m=V['params'], note='RUNTIME effects, NOT in the cells (contract 2.2). For the KC2 drax.',
           phases={k: dict(fps=v['fps'], frames=v['n'], plane=v['plane'], loop=v['loop'], px_per_m=v.get('px_per_m', V['px_per_m']),
                           max_frame_px=[max(f['rect'][2] for f in v['frames']), max(f['rect'][3] for f in v['frames'])]) for k, v in V['phases'].items()},
           telegraph_lead_s=round(V['phases']['ring_tele']['n'] / V['phases']['ring_tele']['fps'], 4),
           use=dict(b='slash = the heavy swing (attack) arc; bolt/burst = the HURL (overhead throw, projectile 31 %); ring_* = the roar nova (poison projectile nova, r 3.5 m rot-skin aura)',
                    c='slash = the swipe; bolt + burst (r 2.4 m) = the lobbed blood-pool throw (projectile 40 %); ring_* = the blood pool / leeching presence',
                    i='slash = the claw; burst (r 3.0 m) = its fire-strike explosion; ring_burst (r 2.5 m) = its dying eruption')[g])
man = dict(what='JOIN-1 clip manifest for the %s (crucible, roster rig %s) -- lane EN-E2 round 4 (drax, R-C9-132/133), read off en_e2/export/final_%s' % (KID, ROSTER['rig'], g),
           body=dict(file=body, sha256_16=sha16, height_m=H['target_m']), roster=ROSTER,
           clips={c: dict(seconds=M['clip_len_s'][c], source=src(c)) for c in M['clip_len_s']},
           locomotion_in_place={c: dict(speed_m_s=M['speeds'][c]['m_per_s'], **{'from': 'en09: the Mixamo source root travel x the export scale / the shipped clip length (in place at source)'}) for c in ('walk', 'run')},
           casts=casts, death=dict(root='de-rooted at source (+deroot); hips ground track max %.3f m from the origin, ends %.3f m' % (dtr.max(), dtr[-1])),
           vfx_runtime={VID.split('_')[-1]: vfx})
if g == 'c':
    man['hunch'] = json.load(open(os.path.join(E, 'work/c_hunch.json')))
    man['hunch']['note'] = 'the named edit en31 (the conductor: a hunched feral carriage) is IN every clip of the shipped body'
if 'emerge' in M['clip_len_s']:
    man['emerge'] = dict(clip='emerge', seconds=M['clip_len_s']['emerge'], roster='p05 %.2f bodies; %s (DATAMINED)' % (ROSTER['p05_bodies'], ROSTER['spawn']),
                         method='unfolds UP from a crouch (no floor crossing; cells have no floor); the fade-in and any duration warp are the runtime\'s')
mp = os.path.join(J, 'manifests', '%s_clips.json' % KID); json.dump(man, open(mp, 'w'), indent=1)
st = lambda clip, kind, role, n, samp, **kw: dict(clip=clip, kind=kind, role=role, frames=n, sampling=samp, **kw)
states = dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
              walk=st('walk', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.walk', stride_from='locomotion_in_place.walk'),
              run=st('run', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.run', stride_from='locomotion_in_place.run'))
ONE = dict(b=[('attack', 12, 'the heavy unarmed swing (melee 59 %)'), ('hurl', 12, 'the overhead hurl (projectile 31 %)'), ('roar', 16, 'the roar (the poison nova / rot skin)')],
           c=[('swipe', 12, 'the swipe (melee 44 %)'), ('throw', 12, 'the throw (projectile 40 %: the blood pool)'), ('buff', 12, 'the chest-thump buff (12 %)')],
           i=[('attack', 12, 'the claw swipe (melee 91 %)')])[g]
for c, n, sk in ONE:
    states[c] = st(c, 'oneshot', 'oneshot_release', n, 'release', release_from='casts.%s.release_s' % c,
                   release_socket='chest' if c in ('roar', 'buff') else ('main_hand' if M['release'][c]['hand'] == 'RightHand' else 'off_hand'), manifest_entry='casts.%s' % c, skill=sk)
states['hit'] = st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit')
states['death'] = st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death')
if 'emerge' in M['clip_len_s']:
    states['emerge'] = st('emerge', 'oneshot', 'oneshot', 12, 'ends', manifest_entry='clips.emerge', skill='p05 emergence (the unfold-up approach)')
sockets = dict(main_hand=dict(bone='RightHand', along_bone_m=TIP['RightHand'], _what='the right hand\'s TIP (+%.4f m along +Y, measured): the strike / throw hand (en09)%s'
                              % (TIP['RightHand'], '; the brute\'s HUGE right fist' if g == 'b' else '')),
               off_hand=dict(bone='LeftHand', along_bone_m=TIP['LeftHand'], _what='the left hand\'s tip (+%.4f m)' % TIP['LeftHand']),
               chest=dict(bone='Spine', _what='the chest (Meshy "Spine" = the top spine joint)'), head_top=dict(bone='head_end', _what='the top of the head'))
kit = dict(kit=KID, _what='Per-kit config for the JOIN-1 sprite-cell renderer: the %s (crucible; lane EN-E2 round 4, R-C9-132/133), one body, no gear, %.2f m. No layers, no morphs.' % (KID, H['target_m']),
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=body, pieces=[], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh (char1) skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres', mesh_name_contains='char1'),
           camera={}, morphs={}, states=states, sockets=sockets,
           vfx_runtime={VID.split('_')[-1]: dict(atlas=vfx['atlas'], frames=vfx['frames'], atlas_px=vfx['atlas_px'], sizes_m=vfx['sizes_m'])}, watchdog_s=2400)
kp = os.path.join(J, 'kits', '%s.json' % KID); json.dump(kit, open(kp, 'w'), indent=1); print('wrote', mp, kp)
