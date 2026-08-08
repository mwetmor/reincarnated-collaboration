#!/usr/bin/env python3
"""C-1 / C-3(a) — band-A per-record eHP INPUTS + characterRunSpeed census.

Band A := distinct monster records reachable in Crucible waves 1..93 (the s1 ramp), p06 EXCLUDED
(S1_BONUS_SPAWNS_ENABLED = False).  Reproduces gamora's 466 regular / 434 champion / 896 union.

Emits INPUTS, not a summary total: the amended sim composes the § 6.2b four-link chain per-record.
WINNER-ONLY overlay semantics (whole-record replacement, L-33 C-9) throughout.  READ-ONLY.
"""
import sys, pathlib, csv, json, math, collections
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from t0_lib import read, owners

PE6 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/scratch/2026-08-07-pe6-crucible/pe6_crucible_wave_pools.csv")
TAGS = json.load(open(HERE.parent / "2026-08-08-kc2-ehp-composition/t23_tags.json"))

BAND_LO, BAND_HI, APL = 1, 93, 100          # fixture is L100 for the whole s1 sitting
OFFSET = 3                                   # L-33: MEASURED +3, DB-source NAMED-ABSENT, DECLARED
APL_ALT = APL + OFFSET                       # the non-discriminable reading (b): apl = 103

# ── the two global multiplier terms ────────────────────────────────────────────────────────────
ULT_REC = "records/game/balancingadjustment_mp+difficulty_enemies01.dbr"
GLAD_REC = "records/game/balancingadjustment_survivalmode_enemies03.dbr"
_ult, ULT_ARCH = read(ULT_REC)
ULT = _ult["characterLifeModifier"][8]                      # Ultimate, 1 player = +580
_glad, GLAD_ARCH = read(GLAD_REC)
GLAD_ARR = _glad["characterLifeModifier"]
def G_of(wave):                                             # L-33 C-4: fighting w reads index w-1
    return GLAD_ARR[wave - 1]

_ab_cache = {}
def armorbase_array(path):
    if path not in _ab_cache:
        r, a = read(path)
        _ab_cache[path] = (r["characterLifeModifier"], a) if r else (None, None)
    return _ab_cache[path]

def evaleq(eq, **vars):
    return eval(str(eq).replace("^", "**"), {"__builtins__": {}}, dict(vars))

def life_at(eq, L):
    return evaleq(str(eq).replace("charLevel", f"({L})"))

# ── 1. band-A membership from the PE-6 emission ────────────────────────────────────────────────
pool_slots = collections.defaultdict(set)     # pool_record -> set of waves in band
rec_pools  = collections.defaultdict(set)     # record -> set of (pool_record, kind)
rec_waves  = collections.defaultdict(set)
rec_kinds  = collections.defaultdict(set)
pool_meta  = {}
for r in csv.DictReader(open(PE6)):
    w = int(r["global_wave"])
    if not (BAND_LO <= w <= BAND_HI):     continue
    if int(r["spawn_point"]) == 6:        continue      # p06 OFF for the s1 band
    pool = r["pool_record"].lower()
    pool_slots[pool].add(w)
    pool_meta.setdefault(pool, dict(archive=r["pool_archive"], kind=r["pool_kind"],
                                    spawn_min=r["spawn_min"], spawn_max=r["spawn_max"],
                                    champion_chance=r["champion_chance"],
                                    champion_min=r["champion_min"], champion_max=r["champion_max"]))
    for fld, kind in (("roster_records", "regular"), ("champ_records", "champion")):
        for rec in (r[fld] or "").split(" | "):
            rec = rec.strip().lower()
            if not rec: continue
            rec_pools[rec].add((pool, kind)); rec_waves[rec].add(w); rec_kinds[rec].add(kind)

BAND = sorted(rec_waves)
print(f"band A: waves {BAND_LO}..{BAND_HI}, p06 OFF -> {len(BAND)} distinct records "
      f"({sum(1 for r in BAND if 'regular' in rec_kinds[r])} regular / "
      f"{sum(1 for r in BAND if 'champion' in rec_kinds[r])} champion), {len(pool_slots)} pools")

# ── 2. per-(pool, slot) level-variance binding ─────────────────────────────────────────────────
LV_CACHE = {}
def lv_band(lvpath):
    """(min,max) at apl=APL under reading (a) [+OFFSET applied later], and under reading (b)."""
    if lvpath not in LV_CACHE:
        r, a = read(lvpath)
        if not r:
            LV_CACHE[lvpath] = None
        else:
            mn, mx = r.get("minVarianceEquationNormal"), r.get("maxVarianceEquationNormal")
            LV_CACHE[lvpath] = dict(
                archive=a, min_eq=mn, max_eq=mx,
                min_a=evaleq(mn, averagePlayerLevel=APL),     max_a=evaleq(mx, averagePlayerLevel=APL),
                min_b=evaleq(mn, averagePlayerLevel=APL_ALT), max_b=evaleq(mx, averagePlayerLevel=APL_ALT))
    return LV_CACHE[lvpath]

placements = []      # (pool, slot_kind, slot_idx, record, weight, minPL, limit, lv_record)
pool_rows  = {}
for pool in sorted(pool_slots):
    pr, parch = read(pool)
    if not pr:
        print(f"  !! POOL MISSING: {pool}"); continue
    pool_rows[pool] = (pr, parch)
    for j in range(1, 41):
        for pfx, kind in (("", "regular"), ("Champion", "champion")):
            n = pr.get(f"name{pfx}{j}")
            if not n: continue
            placements.append(dict(
                pool_record=pool, pool_archive=parch, pool_kind=pool_meta[pool]["kind"],
                slot_kind=kind, slot_index=j, record=str(n).lower(),
                slot_weight=pr.get(f"weight{pfx}{j}"), slot_min_player_level=pr.get(f"minPlayerLevel{pfx}{j}"),
                slot_limit=pr.get(f"limit{pfx}{j}"),
                lv_record=str(pr.get(f"levelVarianceEquation{pfx}{j}") or "")))
print(f"placements (pool x slot) in band A: {len(placements)}")

# ── 3. per-record intrinsic inputs ─────────────────────────────────────────────────────────────
def armorbase_of(rec):
    for i in range(1, 41):
        s = rec.get(f"skillName{i}")
        if s and "armorbase" in str(s).lower():
            return str(s), rec.get(f"skillLevel{i}")
    return None, None

# Task 2b/C-3: the ControllerMonster locomotion + aggro surface, per-record via `controller`.
CTRL_FIELDS = ["MaxPursuitDistance", "PursuitTime", "ViewDistance", "InnerViewDistance",
               "MaxYViewDistance", "RoamBehavior", "RoamDistance", "MinRoamDistance",
               "MinTimeBeforeRoam", "MaxTimeBeforeRoam", "ChanceToIdleOnPatrol",
               "MinPatrolIdleTime", "MaxPatrolIdleTime", "WanderDistance", "MinWanderDistance",
               "TeleportToLeaderDistance", "fleeDistance", "FleeBehavior", "FleeChance",
               "DodgeChance", "DodgeDistance", "MinDodgeDistance", "enemyTooClose",
               "EmoteBeforePursuingChance", "ChanceToRespondToDistressCall",
               "minSwingPause", "maxSwingPause"]
_ctrl_cache = {}
def controller_of(path):
    if path not in _ctrl_cache:
        r, a = read(path) if path else (None, None)
        _ctrl_cache[path] = (r, a)
    return _ctrl_cache[path]

REC = {}
missing, no_bio, no_ab = [], [], []
for path in BAND:
    r, arch = read(path)
    if not r:
        missing.append(path); continue
    tag = r.get("description", "")
    bio = r.get("characterAttributeEquations")
    brec, barch, life_eq = None, None, None
    if bio:
        brec, barch = read(str(bio))
        if brec: life_eq = brec.get("characterLife")
    if not life_eq: no_bio.append(path)
    abp, ablv = armorbase_of(r)
    if not abp: no_ab.append(path)
    REC[path] = dict(
        record=path, winner_archive=arch, name_tag=tag, body=TAGS.get(tag, tag),
        monster_class=r.get("monsterClassification"),
        bio_record=str(bio) if bio else "", bio_archive=barch or "", life_equation=life_eq or "",
        own_characterLifeModifier=r.get("characterLifeModifier") or 0.0,
        own_characterLife=r.get("characterLife") or 0.0,
        own_charLevel_equation=r.get("charLevel") or "",
        armorbase_record=abp or "", armorbase_skill_level_eq=ablv or "",
        armorbase_archive=(armorbase_array(abp)[1] if abp else ""),
        # --- Task 2a: locomotion terms, all dimensionless ---
        characterRunSpeed=r.get("characterRunSpeed"),
        characterRunSpeedModifier=r.get("characterRunSpeedModifier"),
        characterRunSpeedJitter=r.get("characterRunSpeedJitter"),
        walkSpeed=r.get("walkSpeed"),
        minRotationSpeed=r.get("minRotationSpeed"), maxRotationSpeed=r.get("maxRotationSpeed"),
        characterAttackSpeed=r.get("characterAttackSpeed"),
        walkDistance=r.get("walkDistance"), walkUsesRun=r.get("walkUsesRun"),
        disableMovement=r.get("disableMovement"),
        distressCall=r.get("distressCall"), distressCallRange=r.get("distressCallRange"),
        distressCallTime=r.get("distressCallTime"),
        minLevel=r.get("minLevel"), maxLevel=r.get("maxLevel"), lifeTime=r.get("lifeTime"),
        n_fields=len(r), overlay_owners="+".join(owners(path)))
    ctrl_path = str(r.get("controller") or "")
    crec, carch = controller_of(ctrl_path)
    REC[path]["controller_record"] = ctrl_path
    REC[path]["controller_archive"] = carch or ""
    REC[path]["controller_class"] = (crec or {}).get("Class", "")
    for f in CTRL_FIELDS:
        REC[path]["ctrl_" + f] = (crec or {}).get(f)
print(f"resolved {len(REC)}/{len(BAND)}  | MISSING {len(missing)} | no bio-life {len(no_bio)} | "
      f"no armorbase skill {len(no_ab)}")

# ── 4. placement rows: resolve L under BOTH readings; compute the chain inputs ─────────────────
prow = []
lv_divergence = collections.Counter()
for p in placements:
    if p["record"] not in REC: continue
    lv = lv_band(p["lv_record"]) if p["lv_record"] else None
    d = dict(p)
    R = REC[p["record"]]
    d.update(body=R["body"], monster_class=R["monster_class"], winner_archive=R["winner_archive"])
    if lv:
        d.update(lv_archive=lv["archive"], lv_min_equation=lv["min_eq"], lv_max_equation=lv["max_eq"])
        # reading (a): evaluate at apl=100, floor, then add the MEASURED +3
        a_lo, a_hi = math.floor(lv["min_a"]) + OFFSET, math.floor(lv["max_a"]) + OFFSET
        # reading (b): evaluate at apl=103, floor, no offset
        b_lo, b_hi = math.floor(lv["min_b"]), math.floor(lv["max_b"])
        d.update(charLevel_min_readingA=a_lo, charLevel_max_readingA=a_hi,
                 charLevel_min_readingB=b_lo, charLevel_max_readingB=b_hi,
                 readings_agree=(a_lo == b_lo and a_hi == b_hi))
        lv_divergence[(p["lv_record"], a_lo, a_hi, b_lo, b_hi)] += 1
        L = a_lo                                     # the sim's operative reading (a), band floor
        d["charLevel_used"] = L
        d["charLevel_grade"] = ("DERIVED (proxy levelVarianceEquation at apl=100, floor, + the "
                                "MEASURED +3; DB-source of the +3 NAMED-ABSENT — DECLARED sim input)")
        arr, aarch = armorbase_array(R["armorbase_record"]) if R["armorbase_record"] else (None, None)
        d["armorbase_record"] = R["armorbase_record"]
        d["armorbase_index"] = L - 1 if arr else ""
        d["armorbase_pct"] = arr[L - 1] if arr and 0 <= L - 1 < len(arr) else ""
        d["bio_record"], d["life_equation"] = R["bio_record"], R["life_equation"]
        d["base_life_at_charLevel"] = round(life_at(R["life_equation"], L), 4) if R["life_equation"] else ""
    else:
        d.update(lv_archive="", lv_min_equation="", lv_max_equation="",
                 charLevel_min_readingA="", charLevel_max_readingA="",
                 charLevel_min_readingB="", charLevel_max_readingB="", readings_agree="",
                 charLevel_used="", charLevel_grade="NO levelVarianceEquation on this slot",
                 armorbase_record=R["armorbase_record"], armorbase_index="", armorbase_pct="",
                 bio_record=R["bio_record"], life_equation=R["life_equation"],
                 base_life_at_charLevel="")
    d["ultimate_pct"] = ULT
    d["own_characterLifeModifier"] = R["own_characterLifeModifier"]
    d["own_applied"] = "NO (L-33 C-5: falsified; Bileeater +50 breaks its own exact closure +4.41%)"
    d["characterRunSpeed"] = R["characterRunSpeed"]
    d["waves_in_band"] = len(pool_slots[p["pool_record"]])
    d["first_wave"] = min(pool_slots[p["pool_record"]]); d["last_wave"] = max(pool_slots[p["pool_record"]])
    prow.append(d)

# ── 5. roll up per-record level bands across all placements ────────────────────────────────────
by_rec = collections.defaultdict(list)
for d in prow: by_rec[d["record"]].append(d)

out1 = []
for path in BAND:
    if path not in REC: continue
    R = dict(REC[path]); ds = by_rec.get(path, [])
    Ls = [d["charLevel_used"] for d in ds if d["charLevel_used"] != ""]
    lvs = sorted({d["lv_record"] for d in ds if d["lv_record"]})
    R.update(
        in_band_as="+".join(sorted(rec_kinds[path])),
        n_pools=len({p for p, _ in rec_pools[path]}), n_placements=len(ds),
        n_waves_in_band=len(rec_waves[path]),
        first_wave=min(rec_waves[path]), last_wave=max(rec_waves[path]),
        level_variance_records="|".join(lvs),
        charLevel_min=min(Ls) if Ls else "", charLevel_max=max(Ls) if Ls else "",
        charLevel_grade=("DERIVED (proxy levelVarianceEquation at apl=100, floor, + the MEASURED +3; "
                         "the +3's DB source is NAMED-ABSENT — DECLARED sim input)" if Ls else "NO-LEVEL-BINDING"),
        readings_agree_all=all(d["readings_agree"] for d in ds if d["readings_agree"] != "") if ds else "",
        ultimate_pct=ULT, ultimate_record=ULT_REC, ultimate_archive=ULT_ARCH,
        gladiator_record=GLAD_REC, gladiator_archive=GLAD_ARCH,
        gladiator_lookup_law="G(wave) = characterLifeModifier[wave-1] = the cell LABELED wave (L-33 C-4)",
        own_applied="NO (L-33 C-5 falsified)",
        chain="eHP = floor( characterLife(bio, L) * (1 + ultimate_pct/100 + G(wave)/100 + armorbase[L-1]/100) )",
        run_speed_kind="DIMENSIONLESS MULTIPLIER (HALT-2 CLOSED-BY-TYPE); engine m/s reference NAMED-ABSENT",
    )
    # base life at the band's min/max level, so the sim can sanity-check its own evaluation
    if R["life_equation"] and Ls:
        R["base_life_at_charLevel_min"] = round(life_at(R["life_equation"], min(Ls)), 4)
        R["base_life_at_charLevel_max"] = round(life_at(R["life_equation"], max(Ls)), 4)
        arr, _ = armorbase_array(R["armorbase_record"]) if R["armorbase_record"] else (None, None)
        R["armorbase_pct_at_charLevel_min"] = arr[min(Ls) - 1] if arr else ""
        R["armorbase_pct_at_charLevel_max"] = arr[max(Ls) - 1] if arr else ""
    else:
        R["base_life_at_charLevel_min"] = R["base_life_at_charLevel_max"] = ""
        R["armorbase_pct_at_charLevel_min"] = R["armorbase_pct_at_charLevel_max"] = ""
    out1.append(R)

C1 = HERE / "kc2_s1_banda_record_inputs.csv"
cols1 = ["record", "body", "name_tag", "winner_archive", "overlay_owners", "monster_class",
         "in_band_as", "n_pools", "n_placements", "n_waves_in_band", "first_wave", "last_wave",
         "level_variance_records", "charLevel_min", "charLevel_max", "charLevel_grade",
         "readings_agree_all",
         "bio_record", "bio_archive", "life_equation",
         "base_life_at_charLevel_min", "base_life_at_charLevel_max",
         "armorbase_record", "armorbase_archive", "armorbase_skill_level_eq",
         "armorbase_pct_at_charLevel_min", "armorbase_pct_at_charLevel_max",
         "own_characterLifeModifier", "own_characterLife", "own_charLevel_equation", "own_applied",
         "ultimate_pct", "ultimate_record", "ultimate_archive",
         "gladiator_record", "gladiator_archive", "gladiator_lookup_law", "chain",
         "characterRunSpeed", "characterRunSpeedModifier", "characterRunSpeedJitter", "walkSpeed",
         "walkDistance", "walkUsesRun", "disableMovement",
         "minRotationSpeed", "maxRotationSpeed", "characterAttackSpeed", "run_speed_kind",
         "controller_record", "controller_archive", "controller_class"] + \
        ["ctrl_" + f for f in CTRL_FIELDS] + \
        ["distressCall", "distressCallRange", "distressCallTime",
         "minLevel", "maxLevel", "lifeTime", "n_fields"]
with open(C1, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols1, extrasaction="ignore"); w.writeheader(); w.writerows(out1)
print(f"[wrote] {C1.name}  {len(out1)} rows x {len(cols1)} cols")

C2 = HERE / "kc2_s1_banda_placement_inputs.csv"
cols2 = ["pool_record", "pool_archive", "pool_kind", "slot_kind", "slot_index", "record", "body",
         "monster_class", "winner_archive", "slot_weight", "slot_min_player_level", "slot_limit",
         "lv_record", "lv_archive", "lv_min_equation", "lv_max_equation",
         "charLevel_min_readingA", "charLevel_max_readingA",
         "charLevel_min_readingB", "charLevel_max_readingB", "readings_agree",
         "charLevel_used", "charLevel_grade",
         "bio_record", "life_equation", "base_life_at_charLevel",
         "armorbase_record", "armorbase_index", "armorbase_pct",
         "ultimate_pct", "own_characterLifeModifier", "own_applied",
         "characterRunSpeed", "waves_in_band", "first_wave", "last_wave"]
with open(C2, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols2, extrasaction="ignore"); w.writeheader(); w.writerows(prow)
print(f"[wrote] {C2.name}  {len(prow)} rows x {len(cols2)} cols")

C3 = HERE / "kc2_s1_banda_wave_cells.csv"
scal = {k: _glad[k] for k in _glad if isinstance(_glad[k], list)}
with open(C3, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["wave_fought", "gladiator_array_index", "characterLifeModifier_pct",
                "lookup_law", "record", "archive"])
    for wv in range(BAND_LO, BAND_HI + 1):
        w.writerow([wv, wv - 1, G_of(wv),
                    "fighting wave w reads 0-based index w-1 = the cell LABELED w (L-33 C-4)",
                    GLAD_REC, GLAD_ARCH])
print(f"[wrote] {C3.name}  {BAND_HI - BAND_LO + 1} rows")

# ── 6. diagnostics the note needs ──────────────────────────────────────────────────────────────
print("\n== level-variance proxies used in band A (reading A vs reading B) ==")
seen = {}
for (lvp, a_lo, a_hi, b_lo, b_hi), n in sorted(lv_divergence.items()):
    seen.setdefault(lvp, (a_lo, a_hi, b_lo, b_hi, 0))
    t = seen[lvp]; seen[lvp] = (a_lo, a_hi, b_lo, b_hi, t[4] + n)
for lvp, (a_lo, a_hi, b_lo, b_hi, n) in sorted(seen.items()):
    flag = "AGREE" if (a_lo, a_hi) == (b_lo, b_hi) else "*** DIVERGE ***"
    print(f"  {lvp:42s} A=[{a_lo},{a_hi}] B=[{b_lo},{b_hi}]  {flag:16s} ({n} placements)")

print("\n== characterRunSpeed census over band A ==")
rs = collections.Counter(R["characterRunSpeed"] for R in out1)
tot = sum(rs.values())
for v, n in sorted(rs.items(), key=lambda kv: (-kv[1], kv[0] if kv[0] is not None else -1)):
    print(f"  {str(v):>8s}  n={n:4d}  ({100*n/tot:5.1f} %)")
vals = sorted(v for v in (R["characterRunSpeed"] for R in out1) if v is not None)
if vals:
    print(f"  n={len(vals)}  min={min(vals)}  max={max(vals)}  "
          f"median={vals[len(vals)//2]}  mean={sum(vals)/len(vals):.4f}")
print("\n== characterRunSpeedJitter census ==")
for v, n in sorted(collections.Counter(R["characterRunSpeedJitter"] for R in out1).items(),
                   key=lambda kv: -kv[1])[:8]:
    print(f"  {str(v):>8s}  n={n}")
print("\n== walkSpeed census (top 10) ==")
for v, n in sorted(collections.Counter(R["walkSpeed"] for R in out1).items(), key=lambda kv: -kv[1])[:10]:
    print(f"  {str(v):>8s}  n={n}")
print("\n== CONTROLLER locomotion census over band A (C-3 surface) ==")
print(f"  distinct controller records: {len({R['controller_record'] for R in out1})}  "
      f"| records with NO controller: {sum(1 for R in out1 if not R['controller_record'])}")
for f in ("ctrl_MaxPursuitDistance", "ctrl_PursuitTime", "ctrl_ViewDistance",
          "ctrl_InnerViewDistance", "ctrl_RoamBehavior", "ctrl_RoamDistance",
          "ctrl_ChanceToIdleOnPatrol", "ctrl_MinPatrolIdleTime", "ctrl_MaxPatrolIdleTime",
          "ctrl_EmoteBeforePursuingChance", "ctrl_enemyTooClose", "walkDistance",
          "ctrl_minSwingPause", "ctrl_maxSwingPause", "disableMovement"):
    c = collections.Counter(R.get(f) for R in out1)
    nums = sorted(v for v in (R.get(f) for R in out1) if isinstance(v, (int, float)))
    top = ", ".join(f"{k}×{n}" for k, n in c.most_common(5))
    rng = (f"  [n={len(nums)} min={min(nums)} med={nums[len(nums)//2]} max={max(nums)}]"
           if nums else "")
    print(f"  {f:32s} {top}{rng}")

print("\n== monsterClassification census ==")
for v, n in sorted(collections.Counter(R["monster_class"] for R in out1).items(), key=lambda kv: -kv[1]):
    print(f"  {str(v):>12s}  n={n}")
print("\n== armorbase records used ==")
for v, n in sorted(collections.Counter(R["armorbase_record"] for R in out1).items()):
    print(f"  {v or '(NONE)':60s} n={n}")
print("\n== bio curves (top 12 of %d distinct) ==" % len({R['bio_record'] for R in out1}))
for v, n in sorted(collections.Counter(R["bio_record"] for R in out1).items(), key=lambda kv: -kv[1])[:12]:
    print(f"  {v or '(NONE)':64s} n={n}")
print(f"\nMISSING records ({len(missing)}): " + ", ".join(missing[:12]))
print(f"no-bio-life ({len(no_bio)}): " + ", ".join(no_bio[:12]))
print(f"no-armorbase ({len(no_ab)}): " + ", ".join(no_ab[:12]))
print(f"\nG cells across band A: wave 1 -> {G_of(1)}, wave 93 -> {G_of(93)}, "
      f"min {min(G_of(w) for w in range(1,94))}, max {max(G_of(w) for w in range(1,94))}")
json.dump(dict(missing=missing, no_bio=no_bio, no_armorbase=no_ab),
          open(HERE / "c1_gaps.json", "w"), indent=1)
