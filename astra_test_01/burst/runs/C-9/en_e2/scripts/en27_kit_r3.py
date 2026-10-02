# EN-E2 round 3 -> JOIN-1: clip manifest + renderer kit for the WRAITH (w) and the REVENANT (r) (en20's shape; numbers re-read from the
# shipped body's own measure (en09), the hover record (en24), the death ground track and the VFX frame tables; nothing typed except the
# roster facts, which are quoted with their source).
#   python3 scripts/en27_kit_r3.py <w|r>  -> join1_render/manifests/<kid>_clips.json + join1_render/kits/<kid>.json
import json, os, sys, hashlib
import numpy as np
g = sys.argv[1]; E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J = os.path.join(os.path.dirname(E), 'join1_render')
sys.path.insert(0, os.path.join(E, 'scripts')); C = __import__('s17_loop_closure')
KID = dict(w='en-wraith', r='en-revenant')[g]
body = os.path.join(E, 'export/final_%s/en_%s_body.glb' % (g, g))
M = json.load(open(os.path.join(E, 'export/final_%s/en_%s_measure.json' % (g, g))))
H = json.load(open(os.path.join(E, 'export/final_%s/height.json' % g)))
GR = json.load(open(os.path.join(E, 'work/%s_graft.json' % g)))['clips']
TIP = dict(w=0.2722, r=0.2391)[g]; TIPL = dict(w=0.2645, r=0.2317)[g]   # farthest hand vertex weighted > 0.5 to the hand, along its +Y, at rest (measured)
VIDS = dict(w=['en_w_spirit'], r=['en_r_frost', 'en_r_flame', 'en_r_storm'])[g]
sha16 = hashlib.sha256(open(body, 'rb').read()).hexdigest()[:16]
m = C.model(body); hi = [i for i in m['joints'] if m['nodes'][i].get('name') == 'Hips'][0]
ts = sorted({float(t) for v in m['anims']['death'].values() for t in v[0]}); P = np.array([C.globals_at(m, 'death', t)[hi][:3, 3] for t in ts])
dtrack = np.hypot(P[:, 0], P[:, 2])
def src(c):
    if c in GR: return os.path.basename(GR[c]['source']).replace('.glb', '').replace('_', ' ') + ' (Mixamo Pro Magic Pack)'
    return dict(glide='built from idle by en24 (lean 14 deg forward, hover bob), in place', emerge='built by en24 (unfold up from the floor, 0.8667 s = the roster spawn clip)')[c]
def vfx(vid):
    V = json.load(open(os.path.join(E, 'vfx/%s_frames.json' % vid)))
    return dict(atlas=os.path.join(E, 'vfx', V['atlas']), frames=os.path.join(E, 'vfx/%s_frames.json' % vid), atlas_px=V['atlas_size'], atlas_sha256=V['sha256'],
                baked_px_per_m=V['px_per_m'], blend=V['blend'], sizes_m=V['params'],
                phases={k: dict(fps=v['fps'], frames=v['n'], plane=v['plane'], loop=v['loop'], px_per_m=v.get('px_per_m', V['px_per_m']),
                                max_frame_px=[max(f['rect'][2] for f in v['frames']), max(f['rect'][3] for f in v['frames'])]) for k, v in V['phases'].items()},
                telegraph_lead_s=round(V['phases']['ring_tele']['n'] / V['phases']['ring_tele']['fps'], 4))
casts = {c: dict(release_s=v['release_s'], hand=v['hand'], definition='%s, the key that ENDS the fastest interval, on the clip\'s own 30 fps key %d' % (v['rule'], v['key']))
         for c, v in M['release'].items()}
if g == 'w':
    HV = json.load(open(os.path.join(E, 'work/w_hover.json')))
    loco = dict(glide=dict(speed_m_s=2.889, **{'from': 'roster: the lead Wraith record (wraith_a01) characterRunSpeed 0.9 x K4-0 = 2.889 m/s; its walk and run are BOTH the glide clip; in place, the runtime translates'}))
    extra = dict(hover=dict(lift_m=HV['lift_m'], bob_m=HV['bob_m'], glide_lean_deg=HV['lean_deg'], legs='rest inside the shroud (leg channels dropped)',
                            note='the cells show it FLOATING: the shroud tail tips ~0.15 m above the anchor in idle (the anchor is still the ground origin)'),
                 emerge=dict(clip='emerge', seconds=M['clip_len_s']['emerge'], roster='p05 hero members 1.49 bodies; spawn clip wraith_spawn_a01 27 frames 0.8667 s (DATAMINED)',
                             method='unfolds UP from the floor (no floor crossing; cells have no floor to hide one); the fade-in is the runtime\'s'),
                 death_dissipate='the death sinks the hips to 0.40 m and crumples; DISSIPATE = the runtime fades the held last frame (alpha ramp), nothing baked')
else:
    loco = {c: dict(speed_m_s=M['speeds'][c]['m_per_s'], **{'from': 'en09: the Mixamo source root travel x the export scale / the shipped clip length (in place at source)'}) for c in ('walk', 'run')}
    extra = dict(elements=dict(note='ONE base mesh. The storm / flame / frost revenants differ by the RUNTIME: the element VFX atlas (vfx_runtime[element]) and a sprite '
                                    'MODULATE on the cell (suggested, not rendered): frost (0.88, 0.94, 1.0), flame (1.0, 0.90, 0.80), storm (0.92, 0.89, 1.0)',
                               roster='Storm / Flame / Frost Revenant: skeleton_01a (5.03 bodies), the lead Storm Revenant; projectile 63 % / aoe 22 % / aura 14 %'))
man = dict(what='JOIN-1 clip manifest for the %s (crucible, roster rig %s) -- lane EN-E2 round 3 (drax, R-C9-132/133), read off en_e2/export/final_%s'
           % (dict(w='WRAITH', r='REVENANT')[g], dict(w='wraith', r='skeleton_01a')[g], g),
           body=dict(file=body, sha256_16=sha16, height_m=H['target_m']),
           clips={c: dict(seconds=M['clip_len_s'][c], source=src(c)) for c in M['clip_len_s']},
           locomotion_in_place=loco, casts=casts,
           death=dict(root='de-rooted at source (+deroot); hips ground track max %.3f m from the origin, ends %.3f m' % (dtrack.max(), dtrack[-1])),
           vfx_runtime={vid.split('_')[-1]: vfx(vid) for vid in VIDS}, **extra)
for v in man['vfx_runtime'].values():
    v['note'] = 'RUNTIME effects, NOT in the cells (contract 2.2). For the KC2 drax.'
mp = os.path.join(J, 'manifests', '%s_clips.json' % KID); json.dump(man, open(mp, 'w'), indent=1)
st = lambda clip, kind, role, n, samp, **kw: dict(clip=clip, kind=kind, role=role, frames=n, sampling=samp, **kw)
if g == 'w':
    states = dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
                  walk=st('glide', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.glide', stride_from='locomotion_in_place.glide',
                          skill='the glide (the roster walk = its run clip)'),
                  run=st('glide', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.glide', stride_from='locomotion_in_place.glide'),
                  claw=st('claw', 'oneshot', 'oneshot_release', 12, 'release', release_from='casts.claw.release_s', release_socket='cast_hand',
                          manifest_entry='casts.claw', skill='the roster melee (49 %): the clawing lunge'),
                  aura=st('aura', 'oneshot', 'oneshot_release', 16, 'release', release_from='casts.aura.release_s', release_socket='chest',
                          manifest_entry='casts.aura', skill='the roster aura (19 %) / nova (14 %): arms out; the ground ring is the runtime atlas'),
                  cast_bolt=st('cast_bolt', 'oneshot', 'oneshot_release', 12, 'release', release_from='casts.cast_bolt.release_s', release_socket='cast_hand',
                               manifest_entry='casts.cast_bolt', skill='the roster projectile (12 %)'),
                  hit=st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit'),
                  death=st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death'),
                  emerge=st('emerge', 'oneshot', 'oneshot', 12, 'ends', manifest_entry='clips.emerge', skill='p05 emergence (roster spawn clip 0.8667 s)'))
else:
    states = dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
                  walk=st('walk', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.walk', stride_from='locomotion_in_place.walk'),
                  run=st('run', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.run', stride_from='locomotion_in_place.run'),
                  cast_bolt=st('cast_bolt', 'oneshot', 'oneshot_release', 12, 'release', release_from='casts.cast_bolt.release_s', release_socket='cast_hand',
                               manifest_entry='casts.cast_bolt', skill='the roster projectile (63 %)'),
                  cast_area=st('cast_area', 'oneshot', 'oneshot_release', 16, 'release', release_from='casts.cast_area.release_s', release_socket='cast_hand',
                               manifest_entry='casts.cast_area', skill='the roster AoE (22 %) / aura (14 %)'),
                  hit=st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit'),
                  death=st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death'))
sockets = dict(cast_hand=dict(bone='RightHand', along_bone_m=TIP, _what='the right hand\'s TIP (+%.4f m along +Y, measured); every release in this kit is right-handed (en09)' % TIP),
               chest=dict(bone='Spine', _what='the chest: Meshy\'s "Spine" is the TOP spine joint (Spine02 is the lowest)'),
               head_top=dict(bone='head_end', _what='the top of the head'))
if g == 'w':
    sockets['off_hand'] = dict(bone='LeftHand', along_bone_m=TIPL, _what='the left claw tip (+%.4f m along +Y): the claw lunge strikes with both hands' % TIPL)
kit = dict(kit=KID, _what='Per-kit config for the JOIN-1 sprite-cell renderer: the %s (crucible; lane EN-E2 round 3, R-C9-132/133), one body, no gear, %.2f m. No layers, no morphs.'
           % (dict(w='WRAITH (floats; legs at rest inside the shroud)', r='REVENANT skeleton (one base mesh; elements are runtime tints + VFX)')[g], H['target_m']),
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=body, pieces=[], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh (char1) skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres', mesh_name_contains='char1'),
           camera={}, morphs={}, states=states, sockets=sockets,
           vfx_runtime={k: dict(atlas=v['atlas'], frames=v['frames'], atlas_px=v['atlas_px'], sizes_m=v['sizes_m']) for k, v in man['vfx_runtime'].items()},
           watchdog_s=2400)
kp = os.path.join(J, 'kits', '%s.json' % KID); json.dump(kit, open(kp, 'w'), indent=1); print('wrote', mp, kp)
