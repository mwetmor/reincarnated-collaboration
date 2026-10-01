import json, collections, math, csv
d = json.load(open("gd_ranges.json")); L = d["ladder"]
P_LO = 0.3199999928474426; P_HI = P_LO * 1.0499999523162842; TOL = 0.5
HALF_W = 960/75.668; HALF_H = 540/(75.668*math.sin(math.radians(52.9535411256029)))
def mx(x):
    if x is None: return None
    if isinstance(x, list):
        v=[float(a) for a in x if a is not None]; return max(v) if v else None
    return float(x)
def eq(a,b): return a is not None and b is not None and abs(a-b) < 1e-3
AI_SLOTS = ("basic","special1","special2","special3","special4","special5","chain_initial","chain_next","tree_attack")
rows=[]
for o in d["rows"]:
    if o["superseded_in_pack"]: continue
    pr = o["pack_reach_m"]
    pd = mx(o.get("gd_projectileDistance")); str_root = mx(o.get("gd_skillTargetRadius")); str_pack = mx(o.get("pack_skill_skillTargetRadius"))
    if eq(pr,pd): carrier="projectile_distance (GD projectileDistance, the projectile's flight cap)"
    elif eq(pr,str_pack) or eq(pr,str_root): carrier="skill_radius (GD skillTargetRadius, the effect radius)"
    elif eq(pr,o.get("pack_extent_m")) and o.get("pack_extent_carrier"): carrier="extent:"+o["pack_extent_carrier"]
    elif eq(pr,2.4): carrier="MELEE_REACH_M fallback (D_ENGAGE_M = meleeTargetDistance 2.4)"
    else: carrier="other (damage-row carrier; see pack row)"
    ar = o.get("actorRadius"); sc = o.get("scale") or 1.0
    rm_lo = ar if ar is not None else None; rm_hi = ar*sc if ar is not None else None
    g = o.get("gd_GetRange_m")
    cls = o.get("skill_class") or ""
    slot = o["slot"]
    if slot == "dying": kind="DYING (not AI-gated; fires at death)"
    elif slot in ("initial","toggled_aura") or (cls.startswith(("Skill_Buff","SkillBuff")) and slot not in AI_SLOTS): kind="AURA/INITIAL (radius around caster)"
    else: kind="AI-INITIATED (CloseEnoughToUseSkill"+(" + IsSkillInProperRange" if slot.startswith("special") else "")+")"
    r = dict(o)
    r["pack_reach_carrier"] = carrier; r["delivery_class"] = kind
    if g is not None and rm_hi is not None:
        r["gd_use_range_centre_m_HI"] = round(g + rm_hi + P_HI + TOL, 3)
        r["gd_use_range_centre_m_LO"] = round(g + rm_lo + P_LO + TOL, 3)
    bmax = o.get("gd_band_max_m"); bmin=o.get("gd_band_min_m")
    if slot.startswith("special") and bmax is not None and rm_hi is not None:
        r["gd_band_max_centre_m_HI"] = round(bmax + rm_hi + P_HI, 3)
        r["gd_band_min_centre_m_HI"] = round(max(bmin,0.5) + rm_hi + P_HI, 3) if bmin is not None else None
    # GD reference reach for the comparison
    if kind.startswith("AI"):
        cands = [x for x in (r.get("gd_use_range_centre_m_HI"), r.get("gd_band_max_centre_m_HI")) if x is not None]
        gref = min(cands) if cands else None; gsrc = "min(GetRange(distanceProfile)+r_m+r_p+0.5, band max+r_m+r_p)" if len(cands)==2 else "GetRange(distanceProfile)+r_m+r_p+0.5"
    elif kind.startswith("AURA"):
        gref = str_pack if str_pack is not None else str_root; gsrc = "skillTargetRadius (aura radius, centre; radii NOT added)"
    else:
        isproj = "Projectile" in cls
        gref = pd if (isproj and pd is not None) else (str_root if str_root is not None else str_pack); gsrc = "projectileDistance (geometric flight cap)" if (isproj and pd is not None) else "skillTargetRadius"
    r["gd_reference_reach_m"] = gref; r["gd_reference_basis"] = gsrc
    if gref is not None:
        r["diff_m"] = round(pr - gref, 3); r["ratio"] = round(pr / gref, 3) if gref else None
        r["FLAG_pack_exceeds_gd"] = pr > gref + 1e-6
    r["FLAG_beyond_screen_half_height_8.94m"] = pr > HALF_H
    r["FLAG_beyond_screen_half_width_12.69m"] = pr > HALF_W
    rows.append(r)
json.dump(rows, open("compare.json","w"), indent=0)
print("screen half w/h", round(HALF_W,3), round(HALF_H,3))
print("rows", len(rows))
for k in ("delivery_class","pack_reach_carrier"):
    print(collections.Counter(r[k] for r in rows))
ai=[r for r in rows if r["delivery_class"].startswith("AI")]
print("AI rows", len(ai), "exceed", sum(1 for r in ai if r.get("FLAG_pack_exceeds_gd")), "no gref", sum(1 for r in ai if r.get("gd_reference_reach_m") is None))
for k in ("AURA","DYING"):
    sub=[r for r in rows if r["delivery_class"].startswith(k)]
    print(k, len(sub), "exceed", sum(1 for r in sub if r.get("FLAG_pack_exceeds_gd")), "no gref", sum(1 for r in sub if r.get("gd_reference_reach_m") is None))
print("AI exceed by carrier", collections.Counter(r["pack_reach_carrier"] for r in ai if r.get("FLAG_pack_exceeds_gd")))
print("AI beyond half-height", sum(1 for r in ai if r["FLAG_beyond_screen_half_height_8.94m"]), "beyond half-width", sum(1 for r in ai if r["FLAG_beyond_screen_half_width_12.69m"]))
print("GD AI ref beyond half-width", sum(1 for r in ai if (r.get('gd_reference_reach_m') or 0) > HALF_W))
