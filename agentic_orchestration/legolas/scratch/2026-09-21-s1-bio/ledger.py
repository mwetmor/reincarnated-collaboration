#!/usr/bin/env python3
"""S-1 probe: full ATTRIBUTE ledger for the referent save. READ-ONLY.
Sums characterStrength / Dexterity / Intelligence (+ their Modifier %) over
bio + every allocated skill/devotion record (and its buff chain) at its rank
+ every equipped item and its affix chain."""
import sys, json, re; sys.path.insert(0,'.')
import gdcg7 as G, arz

SAVE="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/player.gdc"
FLAT = ("characterStrength","characterDexterity","characterIntelligence",
        "characterLife","characterMana","characterManaRegen","characterLifeRegen")
PCT  = ("characterStrengthModifier","characterDexterityModifier","characterIntelligenceModifier",
        "characterLifeModifier","characterManaModifier","characterManaRegenModifier","characterLifeRegenModifier")

res = G.parse(SAVE)
rows = []

def take(label, rec, rank=None, arch=None, d=None):
    if d is None:
        arch, d = arz.find(rec)
    if d is None:
        rows.append((label, rec, rank, "NOT-FOUND", {})); return None
    vals = {}
    for k in FLAT+PCT:
        v = d.get(k)
        if v is None: continue
        if isinstance(v, list):
            if rank is None: continue
            i = min(rank, len(v)) - 1
            if i < 0: continue
            v = v[i]
        if v: vals[k] = float(v)
    if vals: rows.append((label, rec, rank, arch, vals))
    return d

# ---- 1. bio
bio = res["blocks"]["character_bio"]
rows.append(("BIO", "player.gdc::character_bio", None, "save",
             {"characterStrength": bio["physique"], "characterDexterity": bio["cunning"],
              "characterIntelligence": bio["spirit"], "characterLife": bio["health"],
              "characterMana": bio["energy"]}))

# ---- 2. allocated skills & devotions (walk buff chain)
CHAIN = ("buffSkillName","petSkillName","skillName","modifierSkillName","passiveSkillName")
seen = set()
def walk(label, rec, rank, depth=0):
    key=(rec,rank)
    if key in seen or depth>3: return
    seen.add(key)
    a,d = arz.find(rec)
    if d is None: return
    take(label + ("" if depth==0 else f" >{depth}"), rec, rank, a, d)
    for c in CHAIN:
        nxt = d.get(c)
        if isinstance(nxt,str) and nxt.endswith(".dbr"):
            walk(label, nxt, rank, depth+1)

# ⚑ ALLOCATION PREDICATE. `devotionLevel` is NON-ZERO ON ALL 285 devotion records
# in the file -- it is NOT the allocation flag. `level > 0` gives exactly 55,
# which is what the bio block's `totalDevotionUnlocked` says. Using
# max(level, devotionLevel) sums the WHOLE devotion tree.
for s in res["blocks"]["character_skills"]["skills"]:
    r = s.get("level") or 0
    if r <= 0: continue
    nm = s["name"]
    kind = "DEVOTION" if "/devotion/" in nm else "SKILL"
    walk(f"{kind} r{r}", nm, r)

# ---- 3. equipped items + affix chain
inv = res["blocks"]["inventory"]
for grp in ("equipment","weapon1","weapon2"):
    for it in inv.get(grp,[]):
        if not it.get("baseName"): continue
        take(f"ITEM[{grp}]", it["baseName"])
        for f in ("prefixName","suffixName","modifierName","transmuteName",
                  "componentName","augmentName","relicBonus"):
            x = it.get(f)
            if x: take(f"ITEM[{grp}].{f}", x)

tot = {}
for label, rec, rank, arch, vals in rows:
    for k,v in vals.items(): tot[k] = tot.get(k,0.0)+v

print(f"{'source':26s} {'rank':>4s}  STR    DEX    INT    LIFE    MANA   MREG  LREG   %STR %DEX %INT %LIFE %MANA %MREG")
for label, rec, rank, arch, vals in rows:
    if not any(vals.get(k) for k in ("characterStrength","characterDexterity","characterIntelligence",
                                     "characterLife","characterMana","characterManaRegen",
                                     "characterStrengthModifier","characterDexterityModifier",
                                     "characterIntelligenceModifier","characterManaModifier",
                                     "characterManaRegenModifier","characterLifeModifier")): continue
    g=lambda k: vals.get(k,0.0)
    print(f"{label:26s} {str(rank or ''):>4s}  "
          f"{g('characterStrength'):6.1f} {g('characterDexterity'):6.1f} {g('characterIntelligence'):6.1f} "
          f"{g('characterLife'):7.1f} {g('characterMana'):7.1f} {g('characterManaRegen'):5.2f} {g('characterLifeRegen'):5.2f}  "
          f"{g('characterStrengthModifier'):4.0f} {g('characterDexterityModifier'):4.0f} {g('characterIntelligenceModifier'):4.0f} "
          f"{g('characterLifeModifier'):5.0f} {g('characterManaModifier'):5.0f} {g('characterManaRegenModifier'):5.0f}   <- {rec.replace('records/','')}")
print()
print("TOTALS:", json.dumps({k:round(v,3) for k,v in sorted(tot.items())}, indent=1))
