import json, collections, re, gdlib, csv, sys
LADDER_FIELDS = ["meleeRange","shortRange","moderateRange","longRange","maximumRange","bossRange"]
DP_ENUM = {"Melee":0,"Short":1,"Moderate":2,"Long":3,"Maximum":4,"Boss":5}
BAND_ENUM = {"ShortRange":1,"MediumRange":2,"LongRange":3}
BAND_DEF = {1:(0.0,4.0),2:(4.0,8.0),3:(8.0,16.0)}   # Game.dll binary defaults (InitSkillsInController)
BAND_FIELDS = {1:("shortRangeMin","shortRangeMax"),2:("mediumRangeMin","mediumRangeMax"),3:("longRangeMin","longRangeMax")}
TOL = 0.5     # GetSkillUseTolerance, Game.dll 0x62230
P_RADIUS_LO = 0.3199999928474426; P_SCALE = 1.0499999523162842
P_RADIUS_HI = P_RADIUS_LO * P_SCALE
d = json.load(open("pack_slots.json"))
rows = d["rows"]; sup = set(d["superseded"]); members = d["members"]
E = {"IV": gdlib.Edition("IV"), "II": gdlib.Edition("II")}
ge = E["IV"].winner("records/game/gameengine.dbr")[1]
LADDER = [ge[f] for f in LADDER_FIELDS]
def num(x):
    if isinstance(x, list): return x
    try: return float(x)
    except: return None
def first(x):
    if isinstance(x, list): return x[0] if x else None
    return x
def slot_field(slot):
    if slot == "basic": return "attackSkillName", None
    m = re.match(r"special(\d)$", slot)
    if m:
        n = int(m.group(1)); p = "specialAttack" if n == 1 else f"specialAttack{n}"
        return p + "SkillName", p + "Range"
    return {"initial":("initialSkillName",None),"dying":("dyingSkillName",None),
            "chain_initial":("chainInitialSkill",None),"chain_next":("chainNextSkill",None)}.get(slot,(None,None))
out = []
for r in rows:
    rec = r["record"]; ed = "IV"
    k, c = E[ed].winner(rec)
    c2k, c2 = E["II"].winner(rec)
    sf, bf = slot_field(r["slot"])
    root = r["skill"]
    if c and sf and isinstance(c.get(sf), str) and c.get(sf):
        root = c.get(sf)
    sk_k, sk = E[ed].winner(root) if root else (None, None)
    sk2_k, sk2 = E["II"].winner(root) if root else (None, None)
    pk_k, pksk = E[ed].winner(r["skill"]) if r["skill"] else (None, None)
    o = dict(row_id=r["id"], rowset=r["rowset"], superseded_in_pack=r["id"] in sup, kind=r["kind"],
             record=rec, in_w151_160_pool=rec in members, slot=r["slot"], skill=r["skill"],
             pack_reach_m=r["reach_m"], pack_range_band=r["range_band"] or "",
             pack_extent_m=r["extent_m"], pack_extent_carrier=r["extent_carrier"] or "",
             creature_archive_IV=k, creature_archive_II=c2k, skill_archive_IV=sk_k,
             ai_root_skill=root, root_differs_from_pack_skill=(root or "").lower()!=(r["skill"] or "").lower(),
             pack_skill_distanceProfile=(pksk or {}).get("distanceProfile","") if pksk else None,
             pack_skill_skillTargetRadius=num((pksk or {}).get("skillTargetRadius")) if pksk else None)
    # creature-side
    if c:
        o["actorRadius"] = num(c.get("actorRadius")); o["scale"] = num(c.get("scale")) or 1.0
        if sf:
            o["creature_slot_field"] = sf; o["creature_slot_skill"] = (c.get(sf) or "")
        if bf:
            band = c.get(bf) or ""
            o["gd_range_band"] = band; be = BAND_ENUM.get(band, 0)
            if be:
                fmin, fmax = BAND_FIELDS[be]
                o["gd_band_min_m"] = num(c.get(fmin)) if c.get(fmin) is not None else BAND_DEF[be][0]
                o["gd_band_max_m"] = num(c.get(fmax)) if c.get(fmax) is not None else BAND_DEF[be][1]
                o["gd_band_minmax_src"] = "record" if c.get(fmax) is not None else "Game.dll default"
    # skill-side
    if sk:
        o["skill_class"] = sk.get("Class", "")
        dp = sk.get("distanceProfile", "")
        o["gd_distanceProfile"] = dp
        o["gd_distanceProfile_II"] = (sk2 or {}).get("distanceProfile", "") if sk2 else None
        child = sk.get("buffSkillName")
        if isinstance(child, str) and child:
            ck, cs = E[ed].winner(child)
            o["child_skill"] = child; o["child_distanceProfile"] = (cs or {}).get("distanceProfile", "")
        idx = DP_ENUM.get(dp, 0)   # Skill ctor default +0x8c = 0 (Melee) when absent/unrecognised
        o["gd_profile_enum"] = idx; o["gd_profile_src"] = "record" if dp in DP_ENUM else "ABSENT->Melee (ctor default 0)"
        o["gd_GetRange_m"] = LADDER[idx]
        o["gd_skillTargetRadius"] = num(sk.get("skillTargetRadius"))
        pn = sk.get("skillProjectileName") or (pksk or {}).get("skillProjectileName")
        if isinstance(pn, list): pn = pn[0]
        if isinstance(pn, str) and pn:
            pk, pr = E[ed].winner(pn)
            o["projectile"] = pn
            if pr:
                o["gd_projectileDistance"] = num(pr.get("projectileDistance"))
                o["gd_projectileVelocity"] = num(pr.get("projectileVelocity"))
                o["gd_projectile_distanceProfile"] = pr.get("distanceProfile", "")
                o["gd_projectile_class"] = pr.get("Class", "")
    out.append(o)
json.dump(dict(ladder=dict(zip(LADDER_FIELDS, LADDER)), rows=out), open("gd_ranges.json", "w"), indent=0)
print(len(out))
print(collections.Counter(o.get("gd_distanceProfile") for o in out))
print(collections.Counter(o.get("gd_profile_src") for o in out))
print(collections.Counter(o.get("gd_range_band") for o in out))
print(sum(1 for o in out if o.get("creature_slot_skill") and o["creature_slot_skill"].lower()!=o["skill"].lower()), "slot-skill mismatches")
print(sum(1 for o in out if o.get("gd_distanceProfile_II") is not None and o.get("gd_distanceProfile_II")!=o.get("gd_distanceProfile")), "dp IV vs II diffs")
