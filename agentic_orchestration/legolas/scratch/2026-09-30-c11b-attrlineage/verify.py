import arz, csv, re
MODS=["SurvivalMode.arz","SurvivalMode1.arz","SurvivalMode2.arz","SurvivalMode3.arz"]
def findmod(rec):
    hit=(None,None)
    for n in arz.PRECEDENCE+MODS:
        a=arz.arz(n)
        if rec in a.records: hit=(n,a.get(rec))
    return hit
def ev(eq, charLevel):
    return eval(eq, {"charLevel": float(charLevel)})
def attrs(rec, level):
    n,d = findmod(rec)
    if d is None: return None
    cl_eq = d.get("charLevel") or "charLevel*1"
    cl = ev(cl_eq, level)
    bio = d.get("characterAttributeEquations")
    if not bio: return None
    bn,bd = findmod(bio)
    dex = ev(bd["characterDexterity"], cl) + float(d.get("characterDexterity") or 0.0)
    itl = ev(bd["characterIntelligence"], cl) + float(d.get("characterIntelligence") or 0.0)
    return dict(archive=n, bio=bio, bio_archive=bn, charlevel_eq=cl_eq, charLevel=cl,
                dex_eq=bd["characterDexterity"], int_eq=bd["characterIntelligence"],
                dex=dex, intl=itl,
                rec_dexmod=float(d.get("characterDexterityModifier") or 0.0),
                rec_intmod=float(d.get("characterIntelligenceModifier") or 0.0),
                cls=d.get("monsterClassification"))
