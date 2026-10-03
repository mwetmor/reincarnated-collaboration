# EN-E2 round 7 group 2 -> JOIN-1: clip manifest + renderer kit for the four BOSS MESHES on the hero01 / heroine01 rigs
# (h WARDEN, k ARCH-MAGISTER on hero01_unarmed; j BETRAYER WITCH, q MIND-TAKER on heroine01_unarmed). en27's revenant shape (caster
# clip set: idle, walk, run, cast_bolt, cast_area, hit, death), numbers re-read from the shipped body (en09 measure, en34 tips, the
# death ground track, the VFX frame table). Every pack is PROVISIONAL TEXTURE: Tripo's own texture, embedded, until the Astra reset.
#   python3 scripts/en52_kit_r7g2.py <h|k|j|q>  -> join1_render/manifests/<kid>_clips.json + join1_render/kits/<kid>.json
#   python3 scripts/en52_kit_r7g2.py <h|k|j|q> --painted [--paint-json work/<g>_paint.json]
#     C-9 Phase 2: the D7 PAINT PASS. A NEW pack root <kid>_p (pack roots are immutable; the provisional root is superseded, its
#     source body snapshotted at export/final_<g>_v1). The provisional block is replaced by a painted_texture record.
import json, os, sys, hashlib
import numpy as np
g = sys.argv[1]; E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J = os.path.join(os.path.dirname(E), 'join1_render')
sys.path.insert(0, os.path.join(E, 'scripts')); C = __import__('s17_loop_closure')
NEW = g in 'lux'                                   # C-9 Phase 2 new casters: painted from birth, no provisional root to supersede
PAINTED = '--painted' in sys.argv or NEW
KID0 = dict(h='en-warden', k='en-magister', j='en-witch', q='en-mindtaker', l='en-fleshshaper', u='en-ascended', x='en-vigillord')[g]; KID = KID0 + ('_p' if PAINTED and not NEW else '')
WHO = dict(h='the WARDEN (armoured champion of the order; the clock-face shield is costume, rigged unarmed)',
           k='the ARCH-MAGISTER (scholar-mage; the robe is weighted to the thighs and shins and travels as a skirt)',
           j='the BETRAYER WITCH (the two w156 witches share this mesh; the bone-hand pauldron is costume)',
           q='the MIND-TAKER (gaunt sorceress; the needle bracelet is costume)',
           l='the FLESH-SHAPER (w152 quest boss: aether caster; the grafted left forearm is costume)',
           u='the ASCENDED ZEALOT (w154 quest boss: fire caster; may hover in the source, built standing; the sun-disc pauldron is costume)',
           x='the VIGIL-LORD (w160 nemesis + its revenant summon + the w153 bounty hero: skeletal caster; the wrist lantern is costume, standing in for the record\'s off-hand focus)')[g]
RIG = dict(h='hero01_unarmed', k='hero01_unarmed', j='heroine01_unarmed', q='heroine01_unarmed', l='aetherialfleshshaper', u='korvaaksascended01a', x='skeleton_01a_b')[g]
MIX = dict(hero01_unarmed='projectile 44 % / aoe 24 % / melee 24 % (the rig, BUILD_PRIORITY.md)',
           heroine01_unarmed='projectile 65 % / aura 12 % / melee 12 % (the rig, BUILD_PRIORITY.md)',
           aetherialfleshshaper='aoe 45 % / projectile 39 % / aura 14 % (BUILD_PRIORITY.md)', korvaaksascended01a='projectile 62 % / aoe 25 % / melee 12 % (BUILD_PRIORITY.md)',
           skeleton_01a_b='projectile 60 % / aoe 20 % / buff 10 % (BUILD_PRIORITY.md)')[RIG]
VID = dict(h='en_h_pale', k='en_k_aether', j='en_j_blight', q='en_q_storm', l='en_l_aether', u='en_u_flame', x='en_x_pale')[g]
SHEET = dict(h='artifacts/EN2-H1/EN2-H1_a.png', k='artifacts/EN2-H2/EN2-H2_a.png', j='artifacts/EN2-W1/EN2-W1_a.png', q='artifacts/EN2-W2/EN2-W2_a_r1.png', l='artifacts/EN2-L/EN2-L_a_r1.png', u='artifacts/EN2-U/EN2-U_a_r1.png', x='artifacts/EN2-X/EN2-X_a_r1.png')[g]
body = os.path.join(E, 'export/final_%s/en_%s_body.glb' % (g, g))
M = json.load(open(os.path.join(E, 'export/final_%s/en_%s_measure.json' % (g, g))))
H = json.load(open(os.path.join(E, 'export/final_%s/height.json' % g)))
GR = json.load(open(os.path.join(E, 'work/%s_graft.json' % g)))['clips']
TIPS = json.load(open(os.path.join(E, 'work/%s_tips.json' % g))); TIP = TIPS['RightHand']
sha16 = hashlib.sha256(open(body, 'rb').read()).hexdigest()[:16]
m = C.model(body); hi = [i for i in m['joints'] if m['nodes'][i].get('name') == 'Hips'][0]
ts = sorted({float(t) for v in m['anims']['death'].values() for t in v[0]}); P = np.array([C.globals_at(m, 'death', t)[hi][:3, 3] for t in ts])
dtrack = np.hypot(P[:, 0], P[:, 2])
if g == 'x':
    WT = json.load(open(os.path.join(E, 'work/wt_x.json')))
    rig = dict(method='FREE weight transfer (en49, no Meshy credit) from the REVENANT\'s Meshy rig (builds/en_r_rigged.glb) onto this mesh: k=%d inverse-distance weights, leg side rule (midline gap %.2f), joints refit by the displacement field' % (WT['k'], WT['side_gap']),
               why='the conductor\'s route for the skeleton nemesis (same skeleton family as the built revenant; the roster: same clip directory and 39-bone count)',
               report=os.path.join(E, 'work/wt_x.json'))
    if os.path.exists(os.path.join(E, 'work/x_bridge_cut.json')):
        BC = json.load(open(os.path.join(E, 'work/x_bridge_cut.json'))); rig['bridge_cut'] = dict(tool='en55 (after en10_final)', faces_removed=BC['cut'], vertices_unblended=BC['verts_unblended'])
elif g == 'q':
    WT = json.load(open(os.path.join(E, 'work/wt_q.json')))
    rig = dict(method='FREE weight transfer (en49, no Meshy credit) from the female acolyte\'s Meshy rig (builds/en_f_rigged.glb, heroine01 skeleton) '
                      'onto this mesh: k=%d inverse-distance weights, leg side rule (midline gap %.2f), joints refit by the displacement field' % (WT['k'], WT['side_gap']),
               why='Meshy stopped at 25/30 by the ledger\'s own 10-credit reservation for a 5-credit rig; not worked around',
               validation='en49 self-test exact (weights 0 disagreement, joints 0 m); cross-body f -> witch scored against the witch\'s Meshy rig: '
                          'joint error mean 0.029 / max 0.047 (mesh units, 1.70 tall); limb girth minima in line with the Meshy-rigged witch',
               report=os.path.join(E, 'work/wt_q.json'))
    BC = json.load(open(os.path.join(E, 'work/q_bridge_cut.json')))
    rig['bridge_cut'] = dict(tool='en55 (after en10_final)', faces_removed=BC['cut'], vertices_unblended=BC['verts_unblended'],
                             why='Tripo fused the hanging hands and wrap-strap ends to the thighs; a lifted arm pulled them into a bar (0.94 m at walk 0.3). '
                                 'After the cut the longest torn sliver is 0.27 m (the Meshy-rigged witch: 0.43 m)')
else:
    RR = json.load(open(os.path.join(E, 'work/res_rig_%s.json' % g)))
    rig = dict(method='Meshy auto-rig (5 credits, %s ledger)' % ('the R-C9-135' if NEW else 'round-7'), task=RR['id'])
prov = dict(status='PROVISIONAL TEXTURE', texture='Tripo H3.1 own texture (work/%s_tripo_tex.png), embedded; no paint pass, no grade' % g,
            why='the Astra image limit: the D7 paint (sheets A/B, register, region grade) waits for the reset, 2026-10-03 20:32 local',
            replace='paint A/B (en08 + en32 bake) -> en17/en19 grade -> en10_final -> en21 cells -> index; geometry, rig and clips stay')
if PAINTED:
    PJ = json.load(open(os.path.join(E, 'work/%s_paint.json' % g)))
    prov = None
    painted = dict(status='PAINTED (D7 method)', **({} if NEW else dict(supersedes='join1_pack/%s (provisional Tripo texture; source body kept at export/final_%s_v1)' % (KID0, g))), **PJ)
casts = {c: dict(release_s=v['release_s'], hand=v['hand'], definition='%s, the key that ENDS the fastest interval, on the clip\'s own 30 fps key %d' % (v['rule'], v['key']))
         for c, v in M['release'].items()}
def src(c):
    b = os.path.basename(GR[c]['source']).replace('.glb', '')
    return (b[4:] if b.startswith('axe_') else b).replace('_', ' ') + (' (Mixamo Pro Melee Axe Pack, unarmed)' if b.startswith('axe_') else ' (Mixamo Pro Magic Pack)')
def vfx(vid):
    V = json.load(open(os.path.join(E, 'vfx/%s_frames.json' % vid)))
    return dict(atlas=os.path.join(E, 'vfx', V['atlas']), frames=os.path.join(E, 'vfx/%s_frames.json' % vid), atlas_px=V['atlas_size'], atlas_sha256=V['sha256'],
                baked_px_per_m=V['px_per_m'], blend=V['blend'], sizes_m=V['params'],
                phases={k: dict(fps=v['fps'], frames=v['n'], plane=v['plane'], loop=v['loop'], px_per_m=v.get('px_per_m', V['px_per_m']),
                                max_frame_px=[max(f['rect'][2] for f in v['frames']), max(f['rect'][3] for f in v['frames'])]) for k, v in V['phases'].items()},
                telegraph_lead_s=round(V['phases']['ring_tele']['n'] / V['phases']['ring_tele']['fps'], 4),
                note='RUNTIME effects, NOT in the cells (contract 2.2). For the KC2 drax.')
loco = {c: dict(speed_m_s=M['speeds'][c]['m_per_s'], **{'from': 'en09: the Mixamo source root travel x the export scale / the shipped clip length (in place at source)'}) for c in ('walk', 'run')}
man = dict(what='JOIN-1 clip manifest for %s (crucible boss mesh, roster rig %s) -- lane EN-E2 round 7 group 2 (drax, R-C9-132/133)%s, read off en_e2/export/final_%s' % (WHO, RIG, ' + C-9 Phase 2 paint pass' if PAINTED else '', g),
           **(dict(painted_texture=painted) if PAINTED else dict(provisional_texture=prov)), rig=rig, sheet=os.path.join(os.path.dirname(E), SHEET),
           body=dict(file=body, sha256_16=sha16, height_m=H['target_m']),
           clips={c: dict(seconds=M['clip_len_s'][c], source=src(c)) for c in M['clip_len_s']},
           locomotion_in_place=loco, casts=casts,
           death=dict(root='de-rooted at source (+deroot); hips ground track max %.3f m from the origin, ends %.3f m' % (dtrack.max(), dtrack[-1])),
           roster=dict(rig=RIG, attack_mix=MIX, melee='the rig\'s melee share has no clip in this caster set (as the acolytes); the runtime may play cast_bolt'),
           vfx_runtime={VID.split('_')[-1]: vfx(VID)})
TS = os.path.join(E, 'work/%s_true_size.json' % g)
if os.path.exists(TS): man['true_size'] = json.load(open(TS))
SC = os.path.join(E, 'work/%s_size_call.json' % g)
if os.path.exists(SC): man['size_call'] = json.load(open(SC))
mp = os.path.join(J, 'manifests', '%s_clips.json' % KID); json.dump(man, open(mp, 'w'), indent=1)
st = lambda clip, kind, role, n, samp, **kw: dict(clip=clip, kind=kind, role=role, frames=n, sampling=samp, **kw)
states = dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
              walk=st('walk', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.walk', stride_from='locomotion_in_place.walk'),
              run=st('run', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.run', stride_from='locomotion_in_place.run'),
              cast_bolt=st('cast_bolt', 'oneshot', 'oneshot_release', 12, 'release', release_from='casts.cast_bolt.release_s', release_socket='cast_hand',
                           manifest_entry='casts.cast_bolt', skill='the roster projectile'),
              cast_area=st('cast_area', 'oneshot', 'oneshot_release', 16, 'release', release_from='casts.cast_area.release_s', release_socket='cast_hand',
                           manifest_entry='casts.cast_area', skill='the roster AoE / aura'),
              hit=st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit'),
              death=st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death'))
sockets = dict(cast_hand=dict(bone='RightHand', along_bone_m=TIP, _what='the right hand\'s TIP (+%.4f m along +Y, measured, en34); every release in this kit is right-handed (en09)' % TIP),
               chest=dict(bone='Spine', _what='the chest: Meshy\'s "Spine" is the TOP spine joint (Spine02 is the lowest)'),
               head_top=dict(bone='head_end', _what='the top of the head'))
kit = dict(kit=KID, _what='Per-kit config for the JOIN-1 sprite-cell renderer: %s; one body, no gear, %.2f m. No layers, no morphs. %s'
           % (WHO, H['target_m'], ('PAINTED (D7 paint pass, C-9 Phase 2).' if NEW else 'PAINTED (D7 paint pass, C-9 Phase 2); supersedes %s.' % KID0) if PAINTED else 'PROVISIONAL TEXTURE (Tripo\'s own) until the Astra reset.'),
           **(dict(painted_texture=painted) if PAINTED else dict(provisional_texture=prov)),
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=body, pieces=[], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh (char1) skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres', mesh_name_contains='char1'),
           camera={}, morphs={}, states=states, sockets=sockets,
           vfx_runtime={k: dict(atlas=v['atlas'], frames=v['frames'], atlas_px=v['atlas_px'], sizes_m=v['sizes_m']) for k, v in man['vfx_runtime'].items()},
           watchdog_s=2400, **({'true_size': man['true_size']} if 'true_size' in man else {}), **({'size_call': man['size_call']} if 'size_call' in man else {}))
kp = os.path.join(J, 'kits', '%s.json' % KID); json.dump(kit, open(kp, 'w'), indent=1); print('wrote', mp, kp)
