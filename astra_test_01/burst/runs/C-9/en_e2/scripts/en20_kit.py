# EN-E2 -> JOIN-1: the clip manifest + the renderer kit for one acolyte (templates: join1_render/kits/gd-eor-warlord.json and
# its manifest -- a kit without layers, so join1_render/scripts/validate_sockets.py applies). Every number is re-read from the
# shipped body's own measure (en09, on the GLB) and the VFX frame tables; nothing typed.
#   python3 scripts/en20_kit.py <m|f>   -> join1_render/manifests/en-acolyte-<g>_clips.json + join1_render/kits/en-acolyte-<g>.json
import json, os, sys, hashlib
g = sys.argv[1]; E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J = os.path.join(os.path.dirname(E), 'join1_render')
KID = 'en-acolyte-%s' % g
body = os.path.join(E, 'export/final_%s/en_%s_body.glb' % (g, g))
M = json.load(open(os.path.join(E, 'export/final_%s/en_%s_measure.json' % (g, g))))
H = json.load(open(os.path.join(E, 'export/final_%s/height.json' % g)))
G = json.load(open(os.path.join(E, 'work/%s_graft.json' % g)))['clips']
V = json.load(open(os.path.join(E, 'vfx/en_%s_cold_frames.json' % g)))
TIP = dict(m=0.2397, f=0.2186)[g]      # the right hand's farthest vertex weighted > 0.5 to RightHand, along the bone's +Y, at rest, metres (measured)
sha16 = hashlib.sha256(open(body, 'rb').read()).hexdigest()[:16]
src = lambda c: os.path.basename(G[c]['source']).replace('.glb', '').replace('_', ' ') + ' (Mixamo Pro Magic Pack)'
man = dict(what='JOIN-1 clip manifest for the %s possessed acolyte (crucible trash caster, roster rig %s) -- lane EN-E2 (drax, R-C9-132/133), read off en_e2/export/final_%s'
           % ('male' if g == 'm' else 'female', 'hero01_unarmed' if g == 'm' else 'heroine01_unarmed', g),
           body=dict(file=body, sha256_16=sha16, height_m=H['target_m']),
           clips={c: dict(seconds=M['clip_len_s'][c], source=src(c)) for c in M['clip_len_s']},
           locomotion_in_place={c: dict(speed_m_s=M['speeds'][c]['m_per_s'], **{'from': 'en09: the Mixamo source root travel over the clip x the export scale / the shipped clip length (in place at source; root stripped by the graft)'})
                                for c in ('walk', 'run')},
           casts={c: dict(release_s=M['release'][c]['release_s'], hand=M['release'][c]['hand'],
                          definition=('the THROW: the leading hand\'s peak FORWARD speed, the key that ENDS the fastest interval (s18 rule), on the clip\'s own 30 fps key %d'
                                      if c == 'cast_bolt' else 'the area PUSH: the peak 3D hand speed, the key that ends the fastest interval, on the clip\'s own 30 fps key %d') % M['release'][c]['key'])
                  for c in ('cast_bolt', 'cast_area')},
           death=dict(root='de-rooted at source (the graft\'s +deroot: the hips\' first-to-last ground line removed, the fall kept); hips ground track max %s m from the origin'
                           % dict(m='0.299', f='0.448')[g]),
           vfx_runtime=dict(note='RUNTIME effects, NOT in the cells (contract 2.2: no VFX baked). For the KC2 drax.',
                            atlas=os.path.join(E, 'vfx', V['atlas']), frames=os.path.join(E, 'vfx/en_%s_cold_frames.json' % g),
                            atlas_px=V['atlas_size'], atlas_sha256=V['sha256'], baked_px_per_m=V['px_per_m'], blend=V['blend'], sizes_m=V['params'],
                            phases={k: dict(fps=v['fps'], frames=v['n'], plane=v['plane'], loop=v['loop'],
                                            max_frame_px=[max(f['rect'][2] for f in v['frames']), max(f['rect'][3] for f in v['frames'])]) for k, v in V['phases'].items()},
                            bolt='spawn at cell socket cast_hand at the release frame; flies at the roster speed; burst where it stops',
                            area='ring_tele on the floor at the target, starting telegraph_lead_s before release_s; ring_burst and ring_smoke at release_s',
                            telegraph_lead_s=round(V['phases']['ring_tele']['n'] / V['phases']['ring_tele']['fps'], 4)))
mp = os.path.join(J, 'manifests', '%s_clips.json' % KID); json.dump(man, open(mp, 'w'), indent=1)
st = lambda clip, kind, role, n, samp, **kw: dict(clip=clip, kind=kind, role=role, frames=n, sampling=samp, **kw)
kit = dict(kit=KID,
           _what='Per-kit config for the JOIN-1 sprite-cell renderer: the %s POSSESSED ACOLYTE (crucible trash caster; lane EN-E2, R-C9-132/133), one body, no gear, %.2f m. No layers, no morphs.'
                 % ('male' if g == 'm' else 'female', H['target_m']),
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=body, pieces=[], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh (char1) skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres', mesh_name_contains='char1'),
           camera={}, morphs={},
           states=dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
                       walk=st('walk', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.walk', stride_from='locomotion_in_place.walk'),
                       run=st('run', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.run', stride_from='locomotion_in_place.run'),
                       cast_bolt=st('cast_bolt', 'oneshot', 'oneshot_release', 12, 'release', release_from='casts.cast_bolt.release_s', release_socket='cast_hand',
                                    manifest_entry='casts.cast_bolt', skill='the roster\'s projectile row (the cold bolt)'),
                       cast_area=st('cast_area', 'oneshot', 'oneshot_release', 16, 'release', release_from='casts.cast_area.release_s', release_socket='cast_hand',
                                    manifest_entry='casts.cast_area', skill='the roster\'s AoE row (the cold ring)'),
                       hit=st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit'),
                       death=st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death')),
           sockets=dict(cast_hand=dict(bone='RightHand', along_bone_m=TIP, _what='the casting hand\'s TIP: RightHand + %.4f m along +Y (the farthest hand vertex at rest, measured) -- the bolt spawn; both casts release from the right hand (en09)' % TIP),
                        chest=dict(bone='Spine', _what='the chest: Meshy\'s "Spine" is the TOP spine joint (parent of neck and both shoulders; Spine02 is the LOWEST, child of Hips)'),
                        head_top=dict(bone='head_end', _what='the top of the head')),
           vfx_runtime=dict(manifest_block='vfx_runtime', atlas=man['vfx_runtime']['atlas'], frames=man['vfx_runtime']['frames'], atlas_px=V['atlas_size'], sizes_m=V['params']),
           watchdog_s=2400)
kp = os.path.join(J, 'kits', '%s.json' % KID); json.dump(kit, open(kp, 'w'), indent=1); print('wrote', mp, kp)
