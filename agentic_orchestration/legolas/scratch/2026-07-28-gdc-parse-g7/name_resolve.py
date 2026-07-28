#!/usr/bin/env python3
"""SCRATCH (G-7) — bridge measured gear/skill/monster tags to English display names.

Loads every Text_EN.arc in the Edition-II corpus (base + gdx1/2/3, expansion
tags override base per GD precedence) and joins:
  * equipped gear   prefix + base + suffix  -> the full item name a player sees
  * allocated skills                        -> mastery + skill display names
  * greatestMonsterKilledName               -> boss display name
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arc_text import load_tags  # noqa: E402

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive  # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS = ["resources/Text_EN.arc", "gdx1/resources/Text_EN.arc",
        "gdx2/resources/Text_EN.arc", "gdx3/resources/Text_EN.arc"]
ARZS = ["database/database.arz", "gdx1/database/GDX1.arz",
        "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]

HERE = pathlib.Path(__file__).parent


def main():
    tags = load_tags([VENDOR / a for a in ARCS])
    print(f"tags loaded: {len(tags)}\n")

    arzs = []
    for rel in ARZS:
        p = VENDOR / rel
        if p.exists():
            arzs.append((rel, ArzArchive(p)))

    def rec(path):
        for rel, a in arzs:
            try:
                r = a.read_record(path)
            except Exception:
                continue
            if r:
                return rel, r
        return None, None

    def t(tag):
        return tags.get(tag)

    # ---- gear -------------------------------------------------------------
    gear = json.load(open(HERE / "gear_resolved.json"))
    print("=" * 78)
    print("EQUIPPED GEAR — English names")
    print("=" * 78)
    out_gear = []
    for row in gear:
        parts, dbg = [], {}
        for role, key in (("prefixName", "lootRandomizerName"),
                          ("baseName", "itemNameTag"),
                          ("suffixName", "lootRandomizerName")):
            r = row[role]
            res = r.get("resolved") or {}
            tag = res.get(key) or res.get("itemNameTag") or res.get("lootRandomizerName")
            if not r["record"]:
                dbg[role] = None
                continue
            eng = t(tag) if tag else None
            dbg[role] = {"record": r["record"], "tag": tag, "english": eng,
                         "src": res.get("_source"),
                         "class": res.get("itemClassification"),
                         "style_tag": res.get("itemStyleTag"),
                         "style_english": t(res["itemStyleTag"]) if res.get("itemStyleTag") else None}
            if eng:
                parts.append(eng)
            elif tag:
                parts.append(f"<{tag}?>")
        # GD renders style tag for common-base gear as part of the base name
        base = dbg.get("baseName") or {}
        full = " ".join(parts)
        if base.get("style_english"):
            # style precedes the base noun, after the prefix
            pre = [dbg["prefixName"]["english"]] if dbg.get("prefixName") and dbg["prefixName"]["english"] else []
            mid = [base["style_english"], base["english"]]
            suf = [dbg["suffixName"]["english"]] if dbg.get("suffixName") and dbg["suffixName"]["english"] else []
            full = " ".join(x for x in pre + mid + suf if x)
        print(f"\n{row['group']}[{row['slot']}]  seed={row['seed']}")
        print(f"   NAME: {full}")
        for role in ("prefixName", "baseName", "suffixName"):
            d = dbg.get(role)
            if d:
                print(f"     {role:<11} {d['record']}")
                print(f"     {'':11} tag={d['tag']} eng={d['english']!r} "
                      f"style={d['style_tag']}/{d['style_english']!r} src={d['src']} class={d['class']}")
        out_gear.append({"group": row["group"], "slot": row["slot"],
                         "seed": row["seed"], "name": full, "parts": dbg})
    json.dump(out_gear, open(HERE / "gear_named.json", "w"), indent=1)

    # ---- skills -----------------------------------------------------------
    parsed = json.load(open(HERE / "parsed.json"))
    print("\n" + "=" * 78)
    print("ALLOCATED SKILLS — .arz records + English")
    print("=" * 78)
    print(f"header tag tagSkillClassName10 -> {t('tagSkillClassName10')!r}")
    out_sk = []
    for s in parsed["blocks"]["character_skills"]["skills"]:
        p = s["name"]
        if "/playerclass" not in p:
            continue
        src, r = rec(p)
        st = (r or {}).get("skillDisplayName")
        row = {"record": p, "level": s["level"], "enabled": s["enabled"],
               "devotionLevel": s["devotionLevel"], "src": src,
               "skillDisplayName": st, "english": t(st) if st else None,
               "maxLevel": (r or {}).get("skillMaxLevel"),
               "ultimateLevel": (r or {}).get("skillUltimateLevel"),
               "tier": (r or {}).get("skillTier"),
               "Class": (r or {}).get("Class"),
               "FileDescription": (r or {}).get("FileDescription"),
               "skillBaseDescription": t((r or {}).get("skillBaseDescription") or "") if r else None,
               "buffSkillName": (r or {}).get("buffSkillName"),
               "petSkillName": (r or {}).get("petSkillName"),
               "skillDependancy": (r or {}).get("skillDependancy"),
               "skillMasteryLevelRequired": (r or {}).get("skillMasteryLevelRequired"),
               "skillConnectionOff": (r or {}).get("skillConnectionOff"),
               "keys": sorted((r or {}).keys())}
        out_sk.append(row)
        print(f"\n{p}  lvl={s['level']} enabled={s['enabled']}  src={src}")
        print(f"   displayTag={st} -> {row['english']!r}")
        print(f"   Class={row['Class']} FileDescription={row['FileDescription']!r}")
        print(f"   maxLevel={row['maxLevel']} ultimate={row['ultimateLevel']} tier={row['tier']} "
              f"masteryReq={row['skillMasteryLevelRequired']} dependancy={row['skillDependancy']}")
    json.dump(out_sk, open(HERE / "skills_named.json", "w"), indent=1)

    # ---- boss -------------------------------------------------------------
    print("\n" + "=" * 78)
    print("MONSTER TAGS")
    print("=" * 78)
    for pd in parsed["blocks"]["play_stats"]["perDifficulty"]:
        for k in ("greatestMonsterKilledName", "lastMonsterHit", "lastMonsterHitBy"):
            if pd[k]:
                print(f"  {k:<26} {pd[k]:<28} -> {t(pd[k])!r}")


if __name__ == "__main__":
    main()
