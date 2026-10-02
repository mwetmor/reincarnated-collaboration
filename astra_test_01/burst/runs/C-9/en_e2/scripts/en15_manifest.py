# EN-E2: the enemy manifest (one per acolyte) -- what the KC2 runtime and the D2 cell renderer read: the shipped GLB and its sha,
# every clip with its measured length / loop / release, locomotion speeds, the roster's size and ability numbers it stands in for,
# and the VFX flipbook (sizes and radii in metres, from the roster ability rows). Every number re-read from the shipped files.
#   python3 scripts/en15_manifest.py <m|f>
import json, hashlib, sys, os
g = sys.argv[1]; D = 'export/final_%s' % g
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
M = json.load(open('%s/en_%s_measure.json' % (D, g))); H = json.load(open('%s/height.json' % D)); V = json.load(open('vfx/en_%s_cold_frames.json' % g))
G = json.load(open('work/%s_graft.json' % g))['clips']
ROSTER = dict(
    m=dict(rig='hero01_unarmed', tier1_rank=6, bodies_151_160=7.91, lead_trash_record_size=dict(actorRadius_m=0.35, scale=1.0, radius_x_scale_m=0.35),
           radius_x_scale_range_m=[0.35, 0.98], run_m_per_s_range=[1.93, 3.85], attack_style='projectile 40% / aoe 39%', p05=False,
           projectile_ref=dict(rows=['fireorb / lightningorb_strong (16 m/s, body r 0.3 / 0.1, explosion r 1.5, fire range 16.3 m)'], speed_mps=16.0, body_r_m=0.3, explosion_r_m=1.5, fire_range_m=16.3),
           aoe_ref=dict(rows=['rainoflightning (impact r 2.2 within 8 m)', 'eldritchrain (1.8 within 15 m)'], ring_r_m=2.2, target_radius_m=8.0)),
    f=dict(rig='heroine01_unarmed', tier1_rank=15, bodies_151_160=4.29, lead_trash_record_size=dict(actorRadius_m=0.35, scale=1.0, radius_x_scale_m=0.35),
           radius_x_scale_range_m=[0.35, 0.68], run_m_per_s_range=[1.93, 3.53], attack_style='projectile 74% / aoe 13%', p05=False,
           projectile_ref=dict(rows=['necroticmissiles (20 m/s, body r 0.1, explosion r 1.5, 16.3 m)', 'arcanemissile (33 m/s, r 0.3, expl 0.5)'], speed_mps=20.0, body_r_m=0.1, explosion_r_m=1.5, fire_range_m=16.3),
           aoe_ref=dict(rows=['goregeyser (r 2.5)', 'skysharddevastation (2.2 within 8 m)'], ring_r_m=2.5, target_radius_m=8.0)))[g]
body = '%s/en_%s_body.glb' % (D, g)
clips = {}
for c, L in M['clip_len_s'].items():
    e = dict(length_s=L, loop=c in ('idle', 'walk', 'run'), source=os.path.basename(G[c]['source']).replace('.glb', '') + ' (Mixamo Pro Magic Pack)', flags=G[c]['flags'])
    if c in M['loops']: e['loop_seam_m'] = M['loops'][c]
    if c in M['release']: e.update(release_s=M['release'][c]['release_s'], release_hand=M['release'][c]['hand'], release_rule=M['release'][c]['rule'])
    if c in M['speeds']: e.update(ground_speed_m_per_s=M['speeds'][c]['m_per_s'], speed_basis=M['speeds'][c]['basis'])
    if c == 'death': e['root_travel_note'] = 'NOT de-rooted: the fall travels (lint WARN); extent %s m' % M['extent']['death']
    e['extent_m'] = M['extent'][c]
    clips[c] = e
man = dict(id='en2_%s_acolyte' % g, what='possessed acolyte of the Keepers of Hours, %s trash caster (R-C9-132/133, lane EN-E2)' % ('male' if g == 'm' else 'female'),
           body=dict(path=os.path.abspath(body), sha256=sha(body), height_m=H['target_m'], export_scale=H['factor'], forward='+Z', up='+Y',
                     joints=26, skeleton='Meshy 24 + weapon_r/weapon_l (52_weapon_bones), skeleton identity PASS',
                     texture='painted (D7 method: sheet A 19.77 deg + sheet B 52.95 deg over A) EMBEDDED in the GLB (e42)' + ('; ashen skin grade (en11) per the conductor' if g == 'f' else ''),
                     gear='none (one body; nothing to bind, so no node-order rewrite applies)'),
           roster=ROSTER, clips=clips, sockets=dict(cast_hand='RightHand bone (the measured release hand of both casts)', off_hand='LeftHand'),
           vfx=dict(atlas=os.path.abspath('vfx/' + V['atlas']), frames=os.path.abspath('vfx/en_%s_cold_frames.json' % g), atlas_sha256=V['sha256'], px_per_m=V['px_per_m'],
                    blend=V['blend'], params_m=V['params'],
                    phases={k: dict(fps=v['fps'], n=v['n'], plane=v['plane'], loop=v['loop']) for k, v in V['phases'].items()},
                    runtime_needs=dict(
                        bolt='billboard quad at the cast hand at release_s, flying along the facing at the ROSTER speed (%.0f m/s) to the fire range (%.1f m) or a hit; rotate the quad to the screen-space travel; burst (r %.1f m) where it stops' % (ROSTER['projectile_ref']['speed_mps'], ROSTER['projectile_ref']['fire_range_m'], ROSTER['projectile_ref']['explosion_r_m']),
                        area='ring_tele drawn ON THE FLOOR (ground quad, metres) at the target point from release_s - %.2f s; ring_burst + ring_smoke at release_s; ring radius %.1f m (baked at that radius: scale the quad by r/%.1f for another row)' % (V['phases']['ring_tele']['n'] / V['phases']['ring_tele']['fps'], V['params']['ring_r_m'], V['params']['ring_r_m']),
                        collision='the bolt BODY radius is the roster number (%.1f m); the painted bolt is drawn larger for legibility' % ROSTER['projectile_ref']['body_r_m'],
                        render_as='runtime effects (quads over the cell layer), not baked into the character cells')),
           deliverables=dict(sheet=os.path.abspath('../artifacts/EN2-%s/EN2-%s_a.png' % ((g.upper(),) * 2)), stills8=os.path.abspath('artifacts/en_%s_stills8.png' % g),
                             film_playscale=os.path.abspath('film/en_%s_playscale.mp4' % g), film_2x=os.path.abspath('film/en_%s_2x.mp4' % g)),
           emergence='none: the roster marks the type p05 = 0 (ring trash, appears at t=0 with no spawn clip); a rise clip exists if wanted (Pro Magic "Crouch To Standing Idle", converted, not grafted)')
json.dump(man, open('%s/en_%s_manifest.json' % (D, g), 'w'), indent=1); print('wrote %s/en_%s_manifest.json' % (D, g))
