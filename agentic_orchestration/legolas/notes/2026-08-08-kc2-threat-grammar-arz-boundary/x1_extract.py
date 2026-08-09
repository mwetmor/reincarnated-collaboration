#!/usr/bin/env python3
"""Threat-grammar extraction — Edition-III .arz + .anm, keyed to t22 roster basis. READ-ONLY."""
import json,csv,re,collections
from tg_lib import E3, roster

ANM=json.load(open("anm_index.json"))
FPS=30.0
PFX=("unarmed","sHanded","dHanded","dualRanged","staff","ranged1h","ranged2h","axe2h","mace2h","sword2h","spear2h")

def akey(ref):
    r=(ref or "").lower().replace("\\","/")
    return r[len("creatures/"):] if r.startswith("creatures/") else r

def frames(ref):
    e=ANM.get(akey(ref))
    return e["frames"] if e else None

def num(v,d=None):
    return v if isinstance(v,(int,float)) and not isinstance(v,bool) else d

rows=roster()
mon_rows=[]; slot_rows=[]
stat=collections.Counter()

for r in rows:
    rp=r["record"]
    rec,own=E3.merged(rp)
    if rec is None:
        stat["record_unresolved"]+=1
        mon_rows.append({"record":rp,"status":"NOT-FOUND-IN-ARZ"}); continue
    tblp=rec.get("charAnimationTableName")
    trec,_=E3.merged(tblp) if tblp else (None,None)
    if trec is None: stat["no_anim_table"]+=1
    ctrlp=rec.get("controller"); crec,_=E3.merged(ctrlp) if ctrlp else (None,None)

    # ---- basic (unarmed) attack animation: weighted duration over Anim1..3
    dur=[];wt=[];spd=[];names=[]
    if trec:
        for i in (1,2,3):
            a=trec.get(f"unarmedAttackAnim{i}")
            if isinstance(a,str) and a.lower().endswith(".anm"):
                f=frames(a)
                s=num(rec.get(f"unarmedAttackAnimSpeed{i}"),1.0) or 1.0
                w=num(rec.get(f"unarmedAttackAnimWeight{i}"),0.0) or 0.0
                if f: dur.append(f/FPS/s); wt.append(w); spd.append(s); names.append(a.rsplit("/",1)[-1])
    wsum=sum(wt) or 0
    basic_dur = sum(d*w for d,w in zip(dur,wt))/wsum if wsum else (sum(dur)/len(dur) if dur else None)
    # effective swing period: anim duration / characterAttackSpeed
    cas=num(rec.get("characterAttackSpeed"),1.0) or 1.0
    swing = basic_dur/cas if basic_dur else None
    if basic_dur: stat["basic_anim_measured"]+=1
    else: stat["basic_anim_NOTFOUND"]+=1

    # ---- alt animation classes present (equip-roll dependent)
    alt=[p for p in PFX if p!="unarmed" and trec and isinstance(trec.get(p+"AttackAnim1"),str)]

    # ---- special anim ref map, per prefix
    refmap={}
    if trec:
        for k,v in trec.items():
            m=re.match(r'^([A-Za-z0-9]+?)SpecialAnimRef(\d+)$',k)
            if m and isinstance(v,str):
                an=trec.get(f"{m.group(1)}SpecialAnim{m.group(2)}")
                if isinstance(an,str) and an.lower().endswith(".anm"):
                    refmap.setdefault(v,{}).setdefault(m.group(1),an)
        for p in PFX:
            for nm,fld in (("__spell__",p+"SpellAttackAnim"),("__buffself__",p+"BuffSelfAnim1"),
                           ("__buffother__",p+"BuffOtherAnim1"),("__channel__",p+"ChannelAnim")):
                an=trec.get(fld)
                if isinstance(an,str): refmap.setdefault(nm,{}).setdefault(p,an)

    mon_rows.append(dict(
        record=rp, status="OK", arz_owners="|".join(own),
        anim_table=tblp or "", controller=ctrlp or "",
        monster_classification=rec.get("monsterClassification",""),
        character_attack_speed=cas,
        character_attack_speed_tag=rec.get("characterBaseAttackSpeedTag",""),
        character_spellcast_speed=num(rec.get("characterSpellCastSpeed")),
        character_run_speed=num(rec.get("characterRunSpeed")),
        walk_speed=num(rec.get("walkSpeed")),
        run_speed_jitter=num(rec.get("characterRunSpeedJitter")),
        min_rotation_speed=num(rec.get("minRotationSpeed")),
        max_rotation_speed=num(rec.get("maxRotationSpeed")),
        num_attack_slots=num(rec.get("numAttackSlots")),
        waiting_anim_delay_ms=num(rec.get("waitingAnimDelay")),
        death_anim_blend_time=num(rec.get("deathAnimBlendTime")),
        basic_attack_anims="|".join(names),
        basic_attack_anim_weights="|".join(str(x) for x in wt),
        basic_attack_anim_speeds="|".join(str(x) for x in spd),
        basic_attack_anim_durs_s="|".join(f"{d:.4f}" for d in dur),
        basic_attack_dur_s=round(basic_dur,4) if basic_dur else "",
        basic_swing_period_s=round(swing,4) if swing else "",
        anim_classes_alt="|".join(alt),
        ctrl_max_swing_pause=num(crec.get("maxSwingPause")) if crec else None,
        ctrl_reposition_chance=num(crec.get("RepositionChance")) if crec else None,
        ctrl_dodge_chance=num(crec.get("DodgeChance")) if crec else None,
        ctrl_dodge_delay=num(crec.get("DodgeDelay")) if crec else None,
        ctrl_pursuit_time_ms=num(crec.get("PursuitTime")) if crec else None,
        ctrl_view_distance=num(crec.get("ViewDistance")) if crec else None,
        ctrl_inner_view_distance=num(crec.get("InnerViewDistance")) if crec else None,
        ctrl_flee_behavior=(crec or {}).get("FleeBehavior",""),
        ctrl_enemy_too_close=num(crec.get("enemyTooClose")) if crec else None,
    ))

    # ---- attack slots
    SLOTS=[("basic","attackSkillName",None,None,None,None)]
    for n in ("","2","3","4","5"):
        SLOTS.append((f"special{n or '1'}", f"specialAttack{n}SkillName", f"specialAttack{n}Chance",
                      f"specialAttack{n}Delay", f"specialAttack{n}Timeout", f"specialAttack{n}Range"))
    SLOTS.append(("initial","initialSkillName",None,None,None,None))
    SLOTS.append(("dying","dyingSkillName",None,None,None,None))
    for slot,fs,fc_,fd,ft,fr in SLOTS:
        sp=rec.get(fs)
        if not (isinstance(sp,str) and sp.lower().endswith(".dbr")): continue
        s,_=E3.merged(sp)
        if s is None: stat["skill_unresolved"]+=1; s={}
        san=s.get("skillSpecialAnimationName")
        anmref=None; anmfr=None; grade=""
        if isinstance(san,str) and san:
            m=refmap.get(san)
            if m:
                anmref=m.get("unarmed") or list(m.values())[0]; anmfr=frames(anmref)
                grade="DIRECT-REF" if anmfr else "REF-RESOLVED-ANM-MISSING"
            else:
                grade="REF-UNSATISFIED-BY-TABLE"
        else:
            grade="NO-REF"
        # labelled fallback (NOT a measurement of the bound clip; engine-default assumption)
        fbref=None
        if anmfr is None:
            cls=s.get("Class","")
            fam="__spell__" if not cls.startswith(("Skill_AttackWeapon","Skill_WPAttack","Skill_WeaponPool")) else None
            m=refmap.get(fam) if fam else None
            if m: fbref=m.get("unarmed") or list(m.values())[0]
        fbfr=frames(fbref) if fbref else None
        pn=s.get("skillProjectileName"); pv=pd=la=None
        if isinstance(pn,str) and pn.lower().endswith(".dbr"):
            pr,_=E3.merged(pn)
            if pr: pv=num(pr.get("projectileVelocity")); pd=num(pr.get("projectileDistance")); la=num(pr.get("launchAngle"))
        stat["slot_"+grade]+=1
        slot_rows.append(dict(
            record=rp, slot=slot, skill=sp, skill_class=s.get("Class",""),
            chance_pct=num(rec.get(fc_)) if fc_ else None,
            delay_s=num(rec.get(fd)) if fd else None,
            timeout_s=num(rec.get(ft)) if ft else None,
            range_band=rec.get(fr,"") if fr else "",
            skill_cooldown_s=num(s.get("skillCooldownTime")),
            skill_active_duration_s=num(s.get("skillActiveDuration")),
            skill_charge_duration_s=num(s.get("skillChargeDuration")),
            instant_cast=s.get("instantCast",""),
            allows_warmup=s.get("skillAllowsWarmUp",""),
            warmup_effect=s.get("warmUpEffectName",""),
            wave_time_s=num(s.get("waveTime")), wave_distance=num(s.get("waveDistance")),
            camera_shake_dur_s=num(s.get("cameraShakeDurationSecs")),
            time_between_attacks_ms=num(s.get("timeBetweenAttacks")),
            target_interval_s=num(s.get("skillTargetInterval")),
            distance_profile=s.get("distanceProfile",""),
            anim_binding_grade=grade,
            special_anim_ref=san if isinstance(san,str) else "",
            fallback_anm=(fbref or "").rsplit("/",1)[-1],
            fallback_anm_dur_s=round(fbfr/FPS,4) if fbfr else "",
            special_anm=(anmref or "").rsplit("/",1)[-1],
            special_anm_frames=anmfr if anmfr else "",
            special_anm_dur_s=round(anmfr/FPS,4) if anmfr else "",
            projectile=pn if isinstance(pn,str) else "",
            projectile_velocity=pv, projectile_distance=pd, projectile_launch_angle=la,
        ))

def dump(fn,rws):
    keys=[]
    for r in rws:
        for k in r:
            if k not in keys: keys.append(k)
    with open(fn,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader()
        for r in rws: w.writerow({k:("" if r.get(k) is None else r.get(k)) for k in keys})
    print(fn,len(rws),"rows,",len(keys),"cols")

dump("tg_monster_timing.csv",mon_rows)
dump("tg_attack_slots.csv",slot_rows)
print("stats:",dict(stat))
