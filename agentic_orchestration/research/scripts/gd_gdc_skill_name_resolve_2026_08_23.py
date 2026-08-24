#!/usr/bin/env python3
"""Resolve allocated skill + devotion record paths from a parsed .gdc to English
display names, using the Edition-II GD corpus (base + gdx1/2/3).

READ-ONLY. Reuses legolas prior art: arc_text.load_tags (G-7 scratch) and
gd_arz_adapter_2026_07_24.ArzArchive (research/scripts).
"""
import json
import pathlib
import sys

G7 = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7"
SCRIPTS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts"
sys.path.insert(0, G7)
sys.path.insert(0, SCRIPTS)
from arc_text import load_tags  # noqa: E402
from gd_arz_adapter_2026_07_24 import ArzArchive  # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS = ["resources/Text_EN.arc", "gdx1/resources/Text_EN.arc",
        "gdx2/resources/Text_EN.arc", "gdx3/resources/Text_EN.arc"]
ARZS = ["database/database.arz", "gdx1/database/GDX1.arz",
        "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]

# fields that speak to VFX geometry / cadence — the question behind the question
GEOM = ["Class", "FileDescription", "skillDisplayName", "skillMaxLevel",
        "skillCooldownTime", "skillActiveDuration", "skillTargetRadius",
        "skillTargetAngle", "skillTargetNumber", "skillWeaponTargetNumber",
        "skillProjectileNumber", "targetAngle", "radius", "skillChanceWeight",
        "buffSkillName", "petSkillName", "spawnObjects", "skillTier",
        "skillMasteryLevelRequired", "skillDependancy", "conversionInType"]


def main():
    tags = load_tags([VENDOR / a for a in ARCS])
    arzs = [(rel, ArzArchive(VENDOR / rel)) for rel in ARZS if (VENDOR / rel).exists()]
    sys.stderr.write(f"tags={len(tags)} arz={[r for r, _ in arzs]}\n")

    def rec(path):
        # later archives (expansions) win, matching GD precedence
        found = (None, None)
        for rel, a in arzs:
            try:
                r = a.read_record(path)
            except Exception:
                continue
            if r:
                found = (rel, r)
        return found

    parsed = json.load(open(sys.argv[1]))
    skills = parsed["blocks"]["character_skills"]["skills"]
    alloc = [s for s in skills if s["level"] > 0]

    out = []
    for s in alloc:
        src, r = rec(s["name"])
        r = r or {}
        dn = r.get("skillDisplayName")
        eng = tags.get(dn) if dn else None
        # devotion stars often carry the constellation name on the parent record
        row = {"record": s["name"], "level": s["level"], "enabled": s["enabled"],
               "src": src, "displayTag": dn, "english": eng,
               "desc": tags.get(r.get("skillBaseDescription") or "", None)}
        for k in GEOM:
            if k in r:
                row[k] = r[k]
        # follow buffSkillName / petSkillName one hop for geometry
        for hop in ("buffSkillName", "petSkillName"):
            hp = r.get(hop)
            if hp:
                hsrc, hr = rec(hp)
                if hr:
                    row[hop + "_resolved"] = {
                        k: hr[k] for k in GEOM + ["skillDisplayName"] if k in hr}
                    hdn = hr.get("skillDisplayName")
                    if hdn:
                        row[hop + "_english"] = tags.get(hdn)
        out.append(row)

    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(f"resolved {len(out)} allocated skills -> {sys.argv[2]}")
    named = sum(1 for r in out if r["english"])
    print(f"  with English display name: {named}/{len(out)}")


if __name__ == "__main__":
    main()
