import json, csv, math, collections, sys
OUT=sys.argv[1]
R=json.load(open('compare.json')); roll=json.load(open('rollup.json')); S=json.load(open('summary.json'))
names={}
for f in ['/Users/admin/Games/reincarnated-engine/data/kc2/pm2_tg2_attack_slots.csv']:
    for r in csv.DictReader(open(f)): names[r['record']]=r['display_name']
HALF_W = 960/75.668; HALF_H = 540/(75.668*math.sin(math.radians(52.9535411256029)))
def j(x): return json.dumps(x) if isinstance(x,list) else x
cols=[('pack_row_id','PACK'),('pack_rowset','PACK'),('record','PACK'),('display_name','PACK-substrate (pm2_tg2_attack_slots.csv)'),('kind','PACK'),
 ('in_w151_160_pool','PACK (waves.json pool_member x wave_spawn 151-160)'),('slot','PACK'),('pack_skill','PACK'),('pack_reach_m','PACK'),('pack_range_band','PACK'),
 ('pack_reach_source','INFERRED (reproduces threat._reach_for over the pinned CSVs; 2181/2181 attributed)'),('pack_reach_source_skill','PACK-substrate'),('pack_reach_source_projectile','PACK-substrate'),
 ('delivery_class','INFERRED (slot/class classification)'),('ai_root_skill','DATAMINED (creature slot field, Ed IV CRUCIBLE winner)'),('skill_class','DATAMINED'),
 ('gd_distanceProfile','DATAMINED'),('gd_profile_src','DATAMINED [bin] ctor default'),('gd_GetRange_m','DATAMINED (gameengine.dbr ladder via Skill::GetRange)'),
 ('actorRadius_m','DATAMINED'),('scale','DATAMINED'),('r_player_lo_m','DATAMINED (pc01 actorRadius)'),('r_player_hi_m','DATAMINED x scale (limb INFERRED)'),
 ('gd_use_range_centre_m_HI','DATAMINED formula [bin] + record values; radius x scale limb INFERRED'),('gd_use_range_centre_m_LO','DATAMINED formula [bin] + record values; radius limb LO'),
 ('gd_range_band','DATAMINED'),('gd_band_min_m','DATAMINED'),('gd_band_max_m','DATAMINED'),('gd_band_minmax_src','DATAMINED'),('gd_band_max_centre_m_HI','DATAMINED formula [bin] + record values; HI limb'),
 ('gd_skillTargetRadius_m','DATAMINED (rank array printed whole)'),('gd_projectile','DATAMINED'),('gd_projectileDistance_m','DATAMINED (projectile entity flight cap)'),('gd_projectileVelocity_mps','DATAMINED'),
 ('unit_conversion','DATAMINED (GD DB length unit = metre; x1.0)'),('gd_reference_reach_m','DATAMINED-derived (see gd_reference_basis)'),('gd_reference_basis','-'),
 ('diff_m','INFERRED arithmetic: pack - gd_reference'),('ratio','INFERRED arithmetic'),('FLAG_pack_exceeds_gd','INFERRED'),
 ('FLAG_pack_beyond_half_width_12.69m','INFERRED (port ZOOM-GD, 1920x1080)'),('FLAG_pack_beyond_half_height_8.94m','INFERRED'),('FLAG_gd_beyond_half_width_12.69m','INFERRED')]
with open(f'{OUT}/range_audit_per_attack.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow([c for c,_ in cols])
    for r in sorted(R, key=lambda r:(r['record'], r['slot'], r['skill'])):
        g=r.get('gd_reference_reach_m')
        row=dict(pack_row_id=r['row_id'],pack_rowset=r['rowset'],record=r['record'],display_name=names.get(r['record'],''),kind=r['kind'],in_w151_160_pool=r['in_w151_160_pool'],
            slot=r['slot'],pack_skill=r['skill'],pack_reach_m=r['pack_reach_m'],pack_range_band=r['pack_range_band'],pack_reach_source=r['pack_reach_source'],
            pack_reach_source_skill=r.get('pack_reach_source_skill',''),pack_reach_source_projectile=r.get('pack_reach_source_projectile',''),delivery_class=r['delivery_class'],
            ai_root_skill=r.get('ai_root_skill'),skill_class=r.get('skill_class'),gd_distanceProfile=r.get('gd_distanceProfile'),gd_profile_src=r.get('gd_profile_src'),gd_GetRange_m=r.get('gd_GetRange_m'),
            actorRadius_m=r.get('actorRadius'),scale=r.get('scale'),r_player_lo_m=0.32,r_player_hi_m=round(0.3199999928474426*1.0499999523162842,4),
            gd_use_range_centre_m_HI=r.get('gd_use_range_centre_m_HI'),gd_use_range_centre_m_LO=r.get('gd_use_range_centre_m_LO'),gd_range_band=r.get('gd_range_band',''),
            gd_band_min_m=r.get('gd_band_min_m'),gd_band_max_m=r.get('gd_band_max_m'),gd_band_minmax_src=r.get('gd_band_minmax_src',''),gd_band_max_centre_m_HI=r.get('gd_band_max_centre_m_HI'),
            gd_skillTargetRadius_m=j(r.get('gd_skillTargetRadius')),gd_projectile=r.get('projectile',''),gd_projectileDistance_m=j(r.get('gd_projectileDistance')),gd_projectileVelocity_mps=j(r.get('gd_projectileVelocity')),
            unit_conversion='x1.0 (m->m)',gd_reference_reach_m=g,gd_reference_basis=r.get('gd_reference_basis'),diff_m=r.get('diff_m'),ratio=r.get('ratio'),
            FLAG_pack_exceeds_gd=r.get('FLAG_pack_exceeds_gd'),**{'FLAG_pack_beyond_half_width_12.69m':r['pack_reach_m']>HALF_W,'FLAG_pack_beyond_half_height_8.94m':r['pack_reach_m']>HALF_H,
            'FLAG_gd_beyond_half_width_12.69m':(g or 0)>HALF_W})
        w.writerow([row[c] for c,_ in cols])
json.dump({c:g for c,g in cols}, open(f'{OUT}/range_audit_per_attack.grades.json','w'), indent=1)
with open(f'{OUT}/range_audit_per_monster.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['record','display_name','kind','in_w151_160_pool','pack_max_reach_m (PACK; = oracle max_reach_m over slots, dying excluded)','gd_max_ai_reach_m (DATAMINED-derived, HI limb)','diff_m','FLAG_pack_max_exceeds_gd','FLAG_pack_max_beyond_half_width_12.69m','FLAG_gd_max_beyond_half_width_12.69m'])
    for x in sorted(roll,key=lambda x:-x['diff_m']):
        w.writerow([x['record'],names.get(x['record'],''),x['kind'],x['in_pop'],x['pack_max_reach_m'],x['gd_max_ai_reach_m'],x['diff_m'],x['diff_m']>1e-6,x['pack_max_reach_m']>HALF_W,x['gd_max_ai_reach_m']>HALF_W])
p=json.load(open('p05_spawn.json'))
with open(f'{OUT}/p05_spawn_activation.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['record','display_name','pack_max_reach_m (PACK)','gd_max_ai_reach_m (DATAMINED-derived)','pack_reach_ge_7.159m','gd_reach_ge_7.159m','gd_spawn_anim (DATAMINED anim table)','gd_spawn_anim_s (DATAMINED Ed III .anm header, (frames-1)/30, speed 1.0)','gd_special_slots [slot,Timeout s,Delay s,Range] (DATAMINED)'])
    for r in p['rows']:
        w.writerow([r['record'],names.get(r['record'],''),r['pack_max_reach_m'],r['gd_max_ai_reach_m'],r['pack_reach_ge_p05_dist'],r['gd_reach_ge_p05_dist'],r['gd_spawn_anim'],r['gd_spawn_anim_s'],json.dumps([[s['slot'],s['timeout_s'],s['delay_s'],s['range']] for s in r['gd_special_slots']])])
print('written')
