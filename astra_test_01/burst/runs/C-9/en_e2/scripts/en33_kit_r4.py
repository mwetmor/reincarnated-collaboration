# EN-E2 round 4 -> JOIN-1: clip manifest + renderer kit for the BRUTE (b), the BOG-WRETCH (c) and the IMP (i) (en27's shape; numbers
# re-read from the shipped body's measure (en09), its death ground track and the VFX frame table; roster facts quoted with their source).
#   python3 scripts/en33_kit_r4.py <b|c|i>
import json, os, sys, hashlib
import numpy as np
g = sys.argv[1]; E = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J = os.path.join(os.path.dirname(E), 'join1_render')
sys.path.insert(0, os.path.join(E, 'scripts')); C = __import__('s17_loop_closure')
KID = dict(b='en-brute', c='en-wretch', i='en-imp', g='en-golem', n='en-gaunt', y='en-icebrute', v='en-voidlord', s='en-statue', o='en-bonegolem', d='en-fleshhulk', e='en-colossus')[g]
VID = dict(b='en_b_blight', c='en_c_blood', i='en_i_aether', g='en_g_mud', n='en_n_frost', y='en_y_frost', v='en_v_void', s='en_s_stone', o='en_o_bone', d='en_d_aether', e='en_e_aether')[g]
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
           style='melee 91 %', p05_bodies=1.01, spawn='aetherialimp_spawn_a01, 47 frames', spawn_clip_frames=47),
    g=dict(rig='golemswamp_phase01', tier1_rank=5, bodies=9.03, lead='Ugdenbog Golem (scale 1.0, actorRadius 0.5 -> 0.5 m; range 0.5-0.99)', run_m_per_s=[3.851, 4.975],
           style='aoe 66 % / melee 17 % / projectile 17 %', p05_bodies=3.12, spawn='golemswamp_phase01_appearance_a01, 108 frames', spawn_clip_frames=108,
           summons='the carnivorous plant (our ossuary bloom)', roster_projectile=dict(row='swampgolem_vinenova', speed_mps=11.0, body_r_m=0.5, explosion_r_m=2.0)),
    n=dict(rig='wendigo', tier1_rank=8, bodies=6.04, lead='Wendigo (scale 1.0, actorRadius 0.75 -> 0.75 m; range 0.75-0.98)', run_m_per_s=[2.889, 3.209],
           style='melee 55 % / projectile 26 % / aura 17 %', p05_bodies=0.0),
    y=dict(rig='yeti', tier1_rank=19, bodies=3.04, lead='Diremane Brute (scale 0.8, actorRadius 1.3 -> 1.04 m; range 1.04-1.62)', run_m_per_s=[2.247, 3.691],
           style='projectile 39 % / aoe 37 % / aura 14 %', p05_bodies=0.0),
    v=dict(rig='chthonianrylok', tier1_rank=17, bodies=3.48, lead='Ekket\'Zul, Progenitor of Darkness (BOSS; scale 1.6, actorRadius 0.8 -> 1.28 m; range 0.8-1.575)',
           run_m_per_s=[2.889, 3.53], style='melee 42 % / projectile 28 % / aoe 27 %', p05_bodies=1.0, spawn='chthonianrylok_spawn_c01_fire, 106 frames', spawn_clip_frames=106,
           roles='trash 1.51 / boss 1.50 / champion-hero 0.27 / nemesis 0.20'),
    s=dict(rig='possessedstatue', referent_rank=2, bodies='2.4 referent (w156, 4 raw)', lead='The Steward (BOSS; scale 3.0, actorRadius 0.75 -> 2.25 m) / statue_a01-b02 trash; range 0.6-2.25',
           run_m_per_s=[3.209, 3.53], style='melee 49 % / aoe 38 % / projectile 13 %', p05_bodies=0.0, weapon='Spear2h (a prop: join1 piece spear3.glb on weapon_r)'),
    o=dict(rig='golembone_phase01', referent_rank=10, bodies='1.0 referent (w158 hero)', lead='Skeletal Monstrosity (scale 1.4, actorRadius 0.75 -> 1.05 m; range 0.9-1.125)',
           run_m_per_s=[4.33, 4.97], style='aoe 46 % / buff 45 % (bone prison) / summons on 22 %', p05_bodies=0.0),
    d=dict(rig='fleshhulk_unarmed', referent_rank=9, bodies='1.0 referent (w159 quest boss)', lead='the w159 quest boss (scale 1.52, actorRadius 0.75 -> 1.14 m; heroes 1.45)',
           style='aoe 44 % / melee 26 % / projectile 22 % (charge -> aether stomp r 9 m; aether smash; aether field aura; dying explosion r 3 m)', p05_bodies=0.0, box='H/D 3.2 (BUILD_PRIORITY.md)'),
    e=dict(rig='aetherialcolossus', referent_rank=8, bodies='1.0 referent (w160 quest boss)', lead='the w160 quest boss (scale 1.8, actorRadius 0.75 -> 1.35 m; heroes 1.6)',
           style='projectile 56 % / melee 18 % / aoe 14 % (grenade burst r 2.5 m @ 16 m/s; slam r 8 m; roar r 8 m; charge; strike)', p05_bodies=0.0, box='H/D 2.5 (BUILD_PRIORITY.md)'))[g]
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
           use=dict(d='slash = the aether smash / charge; ring_* (r 4.5 m) = the aether stomp; bolt + burst = the lobbed aether glob; aura (r 7 m) = the aether field',
                    e='bolt + burst (r 2.5 m) = the crystal grenade lob (projectile 56 %); slash = the strike; ring_* (r 4.0 m) = the slam / roar',
                    s='slash = the sweep / strike arcs; ring_* (r 4.5 m) = the thrust impact (mega-punch row); burst = the strike impact',
                    o='slash = the heavy swing; ring_* (r 3.0 m) = the slam / bone prison; aura (r 4.0 m) = the disease cloud (hero rows)',
                    v='slash = the claw sweep; bolt + burst (r 1.8 m) = the chaos bolt; ring_* (r 4.0 m) = the eruption; aura (r 8.0 m) = the dying chaos blast (roster r 8-9 m)',
                    g='slash = the heavy swing; ring_* = the SLAM shock ring (r 4.0 m); bolt + burst (r 2.0 m) = the mud lob (the vine nova row: see roster_projectile)',
                    n='slash = the lunging claw; bolt = the ice shard; aura = the chilling howl (soul-siphon row r 7.0 m)',
                    y='bolt + burst (r 2.4 m) = the boulder/ice throw; ring_* = the ground pound (r 4.0 m); aura = the roar (ice howl row r 8.0 m)',
                    b='slash = the heavy swing (attack) arc; bolt/burst = the HURL (overhead throw, projectile 31 %); ring_* = the roar nova (poison projectile nova, r 3.5 m rot-skin aura)',
                    c='slash = the swipe; bolt + burst (r 2.4 m) = the lobbed blood-pool throw (projectile 40 %); ring_* = the blood pool / leeching presence',
                    i='slash = the claw; burst (r 3.0 m) = its fire-strike explosion; ring_burst (r 2.5 m) = its dying eruption')[g])
man = dict(what='JOIN-1 clip manifest for the %s (crucible, roster rig %s) -- lane EN-E2 round 4 (drax, R-C9-132/133), read off en_e2/export/final_%s' % (KID, ROSTER['rig'], g),
           body=dict(file=body, sha256_16=sha16, height_m=H['target_m']), roster=ROSTER,
           clips={c: dict(seconds=M['clip_len_s'][c], source=src(c)) for c in M['clip_len_s']},
           locomotion_in_place={c: dict(speed_m_s=M['speeds'][c]['m_per_s'], **{'from': 'en09: the Mixamo source root travel x the export scale / the shipped clip length (in place at source)'}) for c in ('walk', 'run')},
           casts=casts, death=dict(root='de-rooted at source (+deroot); hips ground track max %.3f m from the origin, ends %.3f m' % (dtr.max(), dtr[-1])),
           vfx_runtime={VID.split('_')[-1]: vfx})
if g == 's':
    man['weapon'] = dict(piece=os.path.join(E, 'export/final_s/spear3.glb'), bone='weapon_r', length_m=round(1.55 * H['factor'], 4), right_fist_from_butt_m=round(0.74 * H['factor'], 4),
                         mount='e10 (the two-hand grip from the great-sword idle) + en45 (wl_e1 e12 with LEN from env): weapon_r carries a channel on every clip laying the shaft through both fists',
                         mount_record=os.path.join(E, 'export/final_s/weapon_mount.json'))
if g in ('c', 'n'):
    man['hunch'] = json.load(open(os.path.join(E, 'work/%s_hunch.json' % g)))
    man['hunch']['note'] = 'the named edit en31 (the conductor: a hunched feral carriage) is IN every clip of the shipped body'
if 'emerge' in M['clip_len_s']:
    man['emerge'] = dict(clip='emerge', seconds=M['clip_len_s']['emerge'], roster='p05 %.2f bodies; %s (DATAMINED)' % (ROSTER['p05_bodies'], ROSTER['spawn']),
                         method='unfolds UP from a crouch (no floor crossing; cells have no floor); the fade-in and any duration warp are the runtime\'s')
SIZE_CALLS = dict(
    s=dict(designed_height_m=2.30, shipped_height_m=H['target_m'], factor=round(H['target_m'] / 2.30, 4),
           why='at 2.30 m with a 2.50 m spear the strikes cleared the 768 canvas; the spear was shortened (2.50 -> 2.10 m at 2.30, the same ratio now 1.87 m), '
               'the great-sword HIGH SPIN (a full-length spinning reach) replaced by the leaping slam, and the body shipped at 2.05 m (tightest 45 px = 5.9 %). '
               'The CONDUCTOR\'s size call (5 % working margin).'),
    o=dict(designed_height_m=2.60, shipped_height_m=H['target_m'], factor=round(H['target_m'] / 2.60, 4),
           why='at 2.60 m the swing and the death fall cleared the canvas; the death fall centred (en42) and the body shipped at 2.20 m (tightest 45 px = 5.9 %). '
               'The CONDUCTOR\'s size call.'))
if g in SIZE_CALLS: man['size_call'] = SIZE_CALLS[g]
SCJ = os.path.join(E, 'work/%s_size_call.json' % g)          # C-9 Phase 2: a max-fit size call recorded as JSON (d, e)
if os.path.exists(SCJ): man['size_call'] = json.load(open(SCJ))
PJ = os.path.join(E, 'work/%s_paint.json' % g)              # C-9 Phase 2: the D7 paint record
if os.path.exists(PJ) and g in 'de': man['painted_texture'] = dict(status='PAINTED (D7 method)', **json.load(open(PJ)))
if g == 'y':
    man['size_call'] = dict(designed_height_m=2.80, shipped_height_m=H['target_m'], factor=round(H['target_m'] / 2.80, 4),
                            why='at 2.80 m the overhead throw and the ground pound cleared the 768 x 768 canvas (edge touch on 8 cells); the 5 % margin gate (38.4 px) '
                                'allows at most ~2.26 m; shipped at 2.20 m (margin 53 px = 6.9 %). The CONDUCTOR\'s size call (round 5 brief), not the art\'s.',
                            roster_radius_x_scale_m=[1.04, 1.625])
TS = os.path.join(E, 'work/%s_true_size.json' % g)          # KP-222: the en46 true-size block, in the manifest AND the kit
if os.path.exists(TS): man['true_size'] = json.load(open(TS))
mp = os.path.join(J, 'manifests', '%s_clips.json' % KID); json.dump(man, open(mp, 'w'), indent=1)
st = lambda clip, kind, role, n, samp, **kw: dict(clip=clip, kind=kind, role=role, frames=n, sampling=samp, **kw)
states = dict(idle=st('idle', 'loop', 'locomotion_idle', 12, 'loop', manifest_entry='clips.idle'),
              walk=st('walk', 'loop', 'locomotion_walk', 12, 'loop', manifest_entry='clips.walk', stride_from='locomotion_in_place.walk'),
              run=st('run', 'loop', 'locomotion_run', 12, 'loop', manifest_entry='clips.run', stride_from='locomotion_in_place.run'))
ONE = dict(b=[('attack', 12, 'the heavy unarmed swing (melee 59 %)'), ('hurl', 12, 'the overhead hurl (projectile 31 %)'), ('roar', 16, 'the roar (the poison nova / rot skin)')],
           c=[('swipe', 12, 'the swipe (melee 44 %)'), ('throw', 12, 'the throw (projectile 40 %: the blood pool)'), ('buff', 12, 'the chest-thump buff (12 %)')],
           i=[('attack', 12, 'the claw swipe (melee 91 %)')],
           g=[('slam', 12, 'the ground slam + shock ring (aoe 66 %)'), ('attack', 12, 'the heavy swing (melee 17 %)'), ('lob', 12, 'the mud lob (projectile 17 %)'),
              ('summon', 12, 'the summon gesture (the ossuary bloom)')],
           n=[('claw', 12, 'the lunging claw (melee 55 %)'), ('throw', 12, 'the ice-shard throw (projectile 26 %)'), ('aura', 16, 'the chilling howl (aura 17 %)')],
           y=[('throw', 12, 'the boulder / ice throw (projectile 39 %)'), ('pound', 16, 'the ground pound (aoe 37 %)'), ('roar', 16, 'the roar (aura 14 %)')],
           s=[('attack', 12, 'the overwhelming two-handed strike (melee 49 %)'), ('thrust', 12, 'the spear thrust (the mega-punch row, r 4.5 m)'),
              ('sweep', 16, 'the leaping slam (aoe 38 %: double swipe; the spin attack cleared the canvas)')],
           d=[('slam', 12, 'the aether stomp / smash (aoe 44 %)'), ('attack', 12, 'the charging swing (melee 26 %)'), ('lob', 12, 'the lobbed aether glob (projectile 22 %)')],
           e=[('lob', 12, 'the crystal grenade lob (projectile 56 %)'), ('attack', 12, 'the strike (melee 18 %)'), ('slam', 12, 'the slam (aoe 14 %)'), ('roar', 16, 'the roar (r 8 m)')],
           o=[('slam', 12, 'the double strike slam (aoe 46 %)'), ('attack', 12, 'the heavy swing'), ('buff', 16, 'the bone prison call (buff 45 %)')],
           v=[('attack', 12, 'the brutal downward strike (melee 42 %)'), ('sweep', 12, 'the chaos claw sweep (aoe swipe)'), ('cast_bolt', 12, 'the chaos bolt (projectile 28 %)'),
              ('cast_area', 16, 'the eruption (aoe 27 %)')])[g]
for c, n, sk in ONE:
    states[c] = st(c, 'oneshot', 'oneshot_release', n, 'release', release_from='casts.%s.release_s' % c,
                   release_socket=('main_tip' if g == 's' and c != 'sweep' else 'chest') if (c in ('roar', 'buff', 'aura', 'summon') or (g == 's' and c != 'sweep')) else ('main_hand' if M['release'][c]['hand'] == 'RightHand' else 'off_hand'), manifest_entry='casts.%s' % c, skill=sk)
states['hit'] = st('hit', 'oneshot', 'oneshot', 8, 'ends', manifest_entry='clips.hit')
states['death'] = st('death', 'oneshot', 'oneshot_hold', 16, 'ends', hold_last=True, manifest_entry='clips.death')
if 'emerge' in M['clip_len_s']:
    states['emerge'] = st('emerge', 'oneshot', 'oneshot', 16 if M['clip_len_s']['emerge'] > 3 else 12, 'ends', manifest_entry='clips.emerge', skill='p05 emergence (the unfold-up approach)')
sockets = dict(main_hand=dict(bone='RightHand', along_bone_m=TIP['RightHand'], _what='the right hand\'s TIP (+%.4f m along +Y, measured): the strike / throw hand (en09)%s'
                              % (TIP['RightHand'], '; the brute\'s HUGE right fist' if g == 'b' else '')),
               off_hand=dict(bone='LeftHand', along_bone_m=TIP['LeftHand'], _what='the left hand\'s tip (+%.4f m)' % TIP['LeftHand']),
               chest=dict(bone='Spine', _what='the chest (Meshy "Spine" = the top spine joint)'), head_top=dict(bone='head_end', _what='the top of the head'))
if g == 's':
    sockets['main_grip'] = dict(bone='weapon_r', _what='the spear grip (the right fist on the shaft)')
    sockets['main_tip'] = dict(bone='weapon_r', along_bone_m=round((1.55 - 0.74) * H['factor'], 4), _what='the spear BLADE TIP: weapon_r + (length - grip) along +Y')
kit = dict(kit=KID, **({'size_call': 'DOWNSCALED %.2f -> %.2f m to fit the 768 canvas with a >= 5 %% margin; see the manifest size_call (the conductor\'s call)' % (man['size_call']['designed_height_m'], man['size_call']['shipped_height_m'])} if 'size_call' in man else {}), _what='Per-kit config for the JOIN-1 sprite-cell renderer: the %s (crucible; lane EN-E2 round 4, R-C9-132/133), one body, no gear, %.2f m. No layers, no morphs.' % (KID, H['target_m']),
           contract=dict(doc='reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md', commit='d95e1df', schema='join1-sprite-cells/1'),
           source=dict(body=body, pieces=[os.path.join(E, 'export/final_s/spear3.glb')] if g == 's' else [], clip_manifest=mp, loadout=dict(main_hand=None, main_side='R', off_hand=None, weapsel=0)),
           h_model=dict(method='rest pose, the body mesh (char1) skinned at rest by the runtime importer: crown (max up) minus sole (min up), metres', mesh_name_contains='char1'),
           camera={}, morphs={}, states=states, sockets=sockets,
           **({'true_size': man['true_size']} if 'true_size' in man else {}), **({'painted_texture': man['painted_texture']} if 'painted_texture' in man else {}),
           vfx_runtime={VID.split('_')[-1]: dict(atlas=vfx['atlas'], frames=vfx['frames'], atlas_px=vfx['atlas_px'], sizes_m=vfx['sizes_m'])}, watchdog_s=2400)
kp = os.path.join(J, 'kits', '%s.json' % KID); json.dump(kit, open(kp, 'w'), indent=1); print('wrote', mp, kp)
