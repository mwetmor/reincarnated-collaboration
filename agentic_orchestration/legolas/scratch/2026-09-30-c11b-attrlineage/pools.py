import arz, re, collections
# Build: for every tier16 wave proxy (w01..w10 = waves 151..160), walk pool1..poolN
# and record (creature_record -> set of levelVarianceEquation dbr)
MODS=["SurvivalMode.arz","SurvivalMode1.arz","SurvivalMode2.arz","SurvivalMode3.arz"]
def findmod(rec):
    hit=(None,None)
    for n in arz.PRECEDENCE+MODS:
        a=arz.arz(n)
        if rec in a.records: hit=(n,a.get(rec))
    return hit

def all_records():
    s=set()
    for n in arz.PRECEDENCE+MODS: s|=set(arz.arz(n).records)
    return s

ALL=all_records()
lvcache={}
def lv(rec):
    if rec not in lvcache: lvcache[rec]=findmod(rec)[1]
    return lvcache[rec]

def wave_proxies(wave):
    t = (wave-1)//10 + 1
    w = wave - (t-1)*10
    pre = "records/proxies/tier%02dwaves/proxy_w%02d_" % (t, w)
    return sorted(r for r in ALL if r.startswith(pre))

def pool_entries(pool_rec):
    d = lv(pool_rec)
    if d is None: return []
    out=[]
    for i in range(1,13):
        nm = d.get("name%d"%i)
        if not nm: continue
        out.append((nm, d.get("levelVarianceEquation%d"%i), d.get("championChance",0.0)))
    return out

