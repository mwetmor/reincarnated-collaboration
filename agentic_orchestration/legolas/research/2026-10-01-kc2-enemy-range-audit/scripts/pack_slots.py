import json,collections
P='/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/'
w=json.load(open(P+'waves.json'))['pools']
ws=[r for r in w['wave_spawn'] if 151<=r['global_wave']<=160]
pools=set(r['pool_record'] for r in ws)
members=collections.defaultdict(set)
for r in w['pool_member']:
    if r['pool_record'] in pools: members[r['member_record']].add(r['family'])
print('members reachable w151-160:',len(members))
o=json.load(open(P+'monster_offense.json'))
rows=[]
for rs,name in [('⚑ v3p3_rows','v20_monster_attack_slot'),('⚑ v3p4p1_rows','y1_nine_winner_slot_constructed'),('⚑ v3p5_rows','u1_pool_attack_slot')]:
    for r in o[rs][name]:
        v=r['value']; rows.append(dict(rowset=name.split('_')[0],id=r['id'],record=r['record_path'],slot=v['slot'],skill=v['skill'],reach_m=v['reach_m'],extent_m=v.get('extent_m'),extent_carrier=v.get('extent_carrier'),range_band=v.get('range_band'),kind=v.get('kind'),is_weapon_swing=v.get('is_weapon_swing')))
sup=o['⚑ v3p4_superseded_rows']
print('superseded ids', len(sup))
recs=collections.Counter(r['record'] for r in rows)
print('records with slot rows', len(recs), collections.Counter(r['rowset'] for r in rows))
inpop=[r for r in rows if r['record'] in members]
print('slot rows in pop', len(inpop), 'records', len(set(r['record'] for r in inpop)))
missing=[m for m in members if m not in recs]
print('pop members without slot rows', len(missing), missing[:10])
# duplicates across rowsets
by=collections.defaultdict(set)
for r in rows: by[r['record']].add(r['rowset'])
print(collections.Counter(tuple(sorted(v)) for v in by.values()))
json.dump(dict(rows=rows,members={k:sorted(v) for k,v in members.items()},superseded=list(sup.keys())),open('pack_slots.json','w'))
