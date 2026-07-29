#!/usr/bin/env python3
"""probe9 (WR1 E-3) — the seconds-per-swing chain.
(a) player character record base attack-speed fields
(b) any Skill_Attack* template/base record carrying timeBetweenAttacks
(c) controller swing-pause fields for the KC1 opposition roster
(d) monster characterAttackSpeed census. Read-only."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
archives=[(p.name,ArzArchive(p)) for p in ARZS]
db=dict(archives)['database.arz']

print("### (a) player record attack-speed / cadence fields")
for t in ["records/creatures/pc/malepc01.dbr","records/creatures/pc/femalepc01.dbr"]:
    for name,a in archives:
        if t in a.records:
            rec=a.read_record(t)
            print(f"  --- {t} [{name}]")
            for k in sorted(rec):
                if re.search(r'attackspeed|swing|timeBetween|characterAttackRadius|weaponSpeed|animSpeed$', k, re.I):
                    print(f"    {k:40s} {rec[k]!r}")
            break

print("\n### (b) base_template skills: timeBetweenAttacks + related")
for name,a in archives:
    for rp in a.records:
        if 'base_template skills' not in rp: continue
        rec=a.read_record(rp)
        tb = rec.get('timeBetweenAttacks')
        if tb is not None:
            print(f"  [{name}] {rp:70s} timeBetweenAttacks={tb!r} class={rec.get('Class')}")
    break

print("\n### (b2) census of timeBetweenAttacks values on ALL skill records (database.arz)")
c=collections.Counter(); ex={}
for rp in db.records:
    if not rp.startswith('records/skills/'): continue
    rec=db.read_record(rp)
    tb=rec.get('timeBetweenAttacks')
    if tb is None: continue
    key=(db.record_type(rp), tb if not isinstance(tb,list) else tuple(tb)[:1])
    c[key]+=1; ex.setdefault(key,rp)
for k,n in sorted(c.items(), key=lambda x:-x[1])[:25]:
    print(f"  {str(k[0]):34s} tba={k[1]!r:16s} n={n:4d}  e.g. {ex[k]}")

print("\n### (c) controllers: swing-pause fields")
for name,a in archives:
    if name!='database.arz': continue
    seen=collections.Counter()
    for rp in a.records:
        if not rp.startswith('records/controllers/'): continue
        rec=a.read_record(rp)
        mn,mx=rec.get('minSwingPause'),rec.get('maxSwingPause')
        if mn is None and mx is None: continue
        seen[(mn,mx)]+=1
    for k,n in sorted(seen.items(), key=lambda x:-x[1])[:20]:
        print(f"  minSwingPause={k[0]!r:10s} maxSwingPause={k[1]!r:10s} n={n}")

print("\n### (d) KC1 roster: characterAttackSpeed / controller / weaponScale")
ROSTER=["zombie_a01","zombie_b02h","zombie_g01","zombie_soldiera01","zombiehound_a01","gazer_a01",
        "ghoul_a01","boar_a01","boar_a02","scavenger_a01","rifthound_swamp_a01","humanoutlaw_melee_a01",
        "humanoutlaw_ranged_a01","humanchthonic_cultist_a01","prawn_a01","spidergianta_a01",
        "bonerat_meleea01","skeleton_a01","zombiemutated_a01","zombie_c01","boar_b01",
        "hero/boar_h01","hero/zombie_h01","hero/rifthound_h01","boss&quest/warden01","boss&quest/warden02",
        "boss&quest/slith_wightmirecave01","slitha_melee_b01","slitha_shaman_c01","hero/slith_h01"]
for name,a in archives:
    if name!='database.arz': continue
    for stem in ROSTER:
        cands=[rp for rp in a.records if rp.startswith('records/creatures/enemies/') and rp.endswith('/'+stem+'.dbr' if '/' not in stem else stem+'.dbr')]
        cands=[c for c in cands if c.endswith(stem+'.dbr')]
        for rp in cands[:1]:
            rec=a.read_record(rp)
            ctrl=rec.get('controller')
            crec=a.read_record(ctrl) if ctrl and ctrl in a.records else {}
            print(f"  {stem:36s} aspd={rec.get('characterAttackSpeed')!r:6s} aspdMod={rec.get('characterAttackSpeedModifier')!r:6s} "
                  f"wpnScale={rec.get('weaponScale')!r:6s} swingPause={crec.get('minSwingPause')!r}/{crec.get('maxSwingPause')!r} ctrl={(ctrl or '').rsplit('/',1)[-1]}")
