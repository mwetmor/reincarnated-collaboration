#!/usr/bin/env python3
"""SCRATCH (U-1) — full rolled-stat extraction for EVERY equipped slot.

Input : the G-7 gear_resolved.json (record paths + per-item seeds from the .gdc)
Output: per-slot base/prefix/suffix stat tables with lootRandomizerJitter ranges.
Read-only.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import u1_lib as U  # noqa: E402

G7 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration"
                  "/legolas/scratch/2026-07-28-gdc-parse-g7/gear_resolved.json")

# fields that are never a player-facing stat
NOISE = {
    "Class", "templateName", "ActorName", "FileDescription", "characterBaseAttackSpeedTag",
    "bitmap", "mesh", "baseTexture", "bumpTexture", "armorMaleMesh", "armorFemaleMesh",
    "dropSound", "dropSound3D", "dropSoundWater", "hitSound", "swipeSound", "weaponTrail",
    "maxTransparency", "outlineThickness", "physicsFriction", "physicsMass", "scale",
    "actorHeight", "actorRadius", "castsShadows", "itemCostName", "itemNameTag",
    "itemStyleTag", "itemText", "lootRandomizerName", "lootRandomizerCost",
    "marketAdjustmentPercent", "itemSkillAutoController", "shieldBlockAnimation",
    "attackSoundName", "itemClassification", "lootRandomizerJitter", "roundBitmap",
    "itemSetName", "useAnimation",
}
META = {"itemLevel", "levelRequirement", "attributeScalePercent", "armorClassification",
        "itemClassification", "lootRandomizerJitter", "characterBaseAttackSpeed"}

SLOTNAME = {0: "head", 1: "amulet", 2: "torso", 3: "legs", 4: "feet", 5: "hands",
            6: "ring1", 7: "ring2", 8: "waist", 9: "shoulders", 10: "medal", 11: "relic"}


def stats(path):
    tag, rel, rtype, f = U.rec(path)
    if f is None:
        return None
    jit = f.get("lootRandomizerJitter", 0.0) or 0.0
    out, meta = {}, {"_src": rel, "_recordType": rtype, "_jitter": jit}
    for k in META:
        if k in f and f[k] not in (0, 0.0, ""):
            meta[k] = f[k]
    for k, v in f.items():
        if k in NOISE or k.startswith("skillConnection"):
            continue
        if isinstance(v, list):
            if not any(x not in (0, 0.0, "") for x in v):
                continue
            out[k] = v
        else:
            if v in (0, 0.0, ""):
                continue
            if isinstance(v, str) and ("/" in v or "." in v and v.endswith(".tex")):
                continue
            out[k] = v
    return meta, out


def rng(v, jit):
    if not isinstance(v, (int, float)) or jit == 0:
        return None
    return (round(v * (1 - jit / 100), 2), round(v * (1 + jit / 100), 2))


def main():
    gear = json.load(open(G7))
    rows = []
    for g in gear:
        label = f"{g['group']}[{g['slot']}]"
        if g["group"] == "equipment":
            label += f" {SLOTNAME.get(g['slot'], '?')}"
        print("=" * 100)
        print(f"{label}   seed={g['seed']}")
        entry = {"label": label, "seed": g["seed"], "parts": {}}
        for role in ("baseName", "prefixName", "suffixName", "componentName", "augmentName"):
            p = g[role]["record"]
            if not p:
                continue
            r = stats(p)
            if r is None:
                print(f"  !! {role} NOT FOUND {p}")
                continue
            meta, st = r
            print(f"  -- {role:<11} {p}")
            print(f"     {meta}")
            for k in sorted(st):
                v = st[k]
                rr = rng(v, meta["_jitter"])
                print(f"       {k:<42} = {v}" + (f"   roll-range {rr}" if rr else ""))
            entry["parts"][role] = {"record": p, "meta": meta, "stats": st}
        rows.append(entry)
    json.dump(rows, open(pathlib.Path(__file__).parent / "gear_stats.json", "w"), indent=1)


if __name__ == "__main__":
    main()
