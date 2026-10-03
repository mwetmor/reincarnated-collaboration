# EN-E4: the true_size block (conductor rulings on R-C9-137 open items; KC2 relay 2026-10-02) + the breath's extra bursts.
#   python3 work/patch_kit_en4.py <coilseer|gloamwing>
# shipped = the pack's measured body (n12 h_model_m / length_m, re-read from the GLB); designed = the brief's size at the reference record.
# Radii are the oracle's monster_actor_radius_m, READ (not written) from reincarnated-engine
# output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model/monster_offense.json (gr2_gd_fire_range rows, per record_path).
import json, sys
C9 = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9'
N = sys.argv[1]; K = 'en-' + N
kp = '%s/join1_render/kits/%s.json' % (C9, K); mp = '%s/join1_render/manifests/%s_clips.json' % (C9, K)
cm = json.load(open('%s/en_e4/export/%s/%s_clips.json' % (C9, N, N)))
kit = json.load(open(kp)); man = json.load(open(mp))
PACK = 'reincarnated-engine src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model/monster_offense.json (read-only)'
NOTE = ('conductor size call: one shipped base mesh; the runtime scales each record by factor = true/shipped when the per-kit ppm allows '
        '(KC2 side, KP-222). true = designed x scale(record) / scale(reference record): the roster SCALE is DATAMINED; the roster mesh sizes '
        'are not usable as world size (Lap F).')
if N == 'coilseer':
    sh = cm['h_model_m']; des = 2.2; ref = 1.2
    rows = [('dc_bounty08 (bounty, lead record)', 1.2, 0.72), ('slith_h01/h02/h04/h05/h06 (devotion hero)', 1.05, 0.72),
            ('slith_h03 (devotion hero)', 1.05, 0.9), ('slith_h07/h08 (devotion hero)', 1.2, 0.45)]
    ts = dict(base_height_m=sh, designed_height_m=des, reference_record='dc_bounty08.dbr', reference_scale=ref,
              basis='height, ground to crown (upright upper body); the serpent body lies ~2.3 m behind the torso base', note=NOTE,
              radius_source=PACK, records={})
    for r, s, rad in rows:
        t = round(des * s / ref, 3)
        ts['records'][r] = dict(scale=s, true_height_m=t, factor=round(t / sh, 3), monster_actor_radius_m=rad)
    ts['radius_check'] = ('INFO, no large mismatch: the 0.72 m radius (1.44 m circle) covers the upright torso and the arms (half-width 0.85 m at '
                          'rest); the serpent body extends ~2.3 m behind it outside the circle by design (a tail, like the void drone). '
                          'slith_h07/h08 carry radius 0.45 at the SAME scale 1.2 as dc_bounty08 (0.72): the same sprite, a smaller collision '
                          'circle -- record data, flagged so KC2 does not read it as a size difference.')
else:
    ln = cm['length_m']; ms = 0.68; sh_btr = round(3.6 * ms, 4)
    ts = dict(basis='length, beak tip to rump (the tail feathers extend beyond)', designed_length_m=3.6, reference_record='hypporaven_h03.dbr (lead)',
              reference_scale=1.15, base_length_m=sh_btr, base_length_note='shipped beak-to-rump = 3.6 x 0.68 (max-fit: the mesh was built at '
              '5.6 m beak-to-tail-tip and re-prepped at x0.68 to clear the canvas with margin; motion_scale 0.68); the shipped GLB AABB length '
              'including the tail is %s m' % ln, note=NOTE, radius_source=PACK, records={})
    for r in ('hypporaven_h01', 'hypporaven_h02', 'hypporaven_h03', 'hypporaven_h04'):
        ts['records'][r + ' (hero, w158 p05)'] = dict(scale=1.15, true_length_m=3.6, factor=round(3.6 / sh_btr, 3), monster_actor_radius_m=1.0)
    ts['primary'] = 'designed (KC2 relay: designed size primary; the AABB basis kept as a labelled alternate)'
    aabb = round(2 * 3.90963 * 1.15, 2)
    ts['alternate_aabb'] = dict(roster_mesh_aabb_half_xz_meshspace=[7.26681, 3.90963], roster_mesh_aabb_height_meshspace=3.7255,
                                true_length_m_at_1_15=aabb, factor=round(aabb / sh_btr, 3),
                                note='ALTERNATE ONLY: the bind-box depth x scale (the void drone rule) gives ~9.0 m; the Lap F mesh units are '
                                     'unreliable as world size, so this is not the basis of record. KC2 owns the final scaling ruling (KP-222).')
    ts['radius_check'] = ('INFO, no large mismatch: radius 1.0 m (2.0 m circle) against the designed 3.6 m beak-to-rump and ~1.6 m width with '
                          'the wings folded; the head and tail overhang the circle front and back, as a horse-sized quadruped does. '
                          'Under the AABB alternate (~9 m) the circle would be badly undersized -- one more reason the designed basis is primary.')
    # the breath: one declared release (contract: release_index = one exact sample), the later bursts listed (conductor ruling 3; KC2: visual only)
    c = man['casts']['cast_breath']
    c['additional_bursts'] = [dict(frame=50, s=round(50 / 30, 4)), dict(frame=70, s=round(70 / 30, 4))]
    c['additional_bursts_note'] = ('the record fires three bursts (*Hit f26 / f50 / f70); release_index declares f26; f50 and f70 are VISUAL '
                                   'bursts (KC2 confirmed), spawned by the runtime off the same maw socket at these clip times')
    man['vfx_runtime']['aura_note'] = ('gloamwing_dark_aura + gloamwing_dark_wisps are a RUNTIME-LOOPED atlas (ground haze + wisps), never baked into '
                                       'the cells (conductor ruling 4, KC2 confirmed); on from spawn / cast_roar release')
    json.dump(man, open(mp, 'w'), indent=1)
kit['true_size'] = ts
json.dump(kit, open(kp, 'w'), indent=1)
print(K, json.dumps({k: v for k, v in ts.items() if k == 'records'})[:600])
