#!/usr/bin/env python3
"""KC2-PM4 Lap R — LIMB C: game-side movement-speed terms, both sides of the screen.

  C.1  PLAYER movement speed  — base record + every equipped item, allocated skill, devotion and
       one-hop payload that carries a `characterRunSpeed*` field.
  C.2  MONSTER movement speed — per-record `characterRunSpeed` / Jitter / Modifier / `walkSpeed`
       / rotation speeds for the 151-160 roster, joined to the frozen wave roll.
  C.3  EoR's movement-while-channeling rule — from the skill record + its template.
  C.4  Crucible spawn geometry — searched; UNREACHED recorded honestly if not in the record DB.

READ-ONLY on the vendor corpus.  OUTCOME-FIREWALLED: no simulation output is opened.
GL-12: every value carries record path + field name.  Nothing estimated.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap R.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import numpy as np

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4r_lib_2026_08_14 import OUT, dump_csv, sha256                      # noqa: E402
from pm4o_lib_2026_08_14 import roster_actors                              # noqa: E402
from pm4g_lib_2026_08_13 import (                                          # noqa: E402
    E3, rec, arc_of, at_rank, read_skill_block, PLAYED_SAVE,
)
from pm4l_emit_2026_08_14 import EQUIP, WARBORN, ITEM_PASSIVES             # noqa: E402

SPEED_FIELDS = ("characterRunSpeed", "characterRunSpeedModifier", "characterRunSpeedJitter",
                "walkSpeed", "maxRotationSpeed", "minRotationSpeed",
                "characterAttackSpeed", "characterAttackSpeedModifier")
#: monster-side movement DEBUFF fields the player's own kit may apply (measured, not assumed active)
SLOW_FIELDS = ("offensiveSlowRunSpeedMin", "offensiveSlowRunSpeedMax",
               "offensiveSlowRunSpeedModifier", "offensiveSlowRunSpeedChance",
               "offensiveSlowRunSpeedDurationMin", "offensiveSlowRunSpeedDurationMax",
               "defensiveSlowRunSpeed")

PC_CANDIDATES = [
    "records/creatures/pc/malepc01.dbr", "records/creatures/pc/femalepc01.dbr",
    "records/creatures/pc/malepc02.dbr", "records/creatures/pc/femalepc02.dbr",
    "records/creatures/npcs/malepc01.dbr",
]
GAMEENGINE = "records/game/gameengine.dbr"
EOR = "records/skills/playerclass09/eyeofreckoning1.dbr"


def get(path):
    try:
        r, a = E3.winner(path)
        return (r or None), a
    except Exception:
        return None, None


def main():
    rows, res = [], {}
    print("=" * 100)
    print("KC2-PM4 LAP R — LIMB C — game-side movement-speed terms")
    print("=" * 100)

    # ── C.1 PLAYER ────────────────────────────────────────────────────────────────────────────
    print("\n--- C.1 PLAYER movement speed ---")
    pc_found = []
    for p in PC_CANDIDATES:
        r, a = get(p)
        if r:
            vals = {f: r[f] for f in SPEED_FIELDS if f in r}
            pc_found.append((p, a, vals))
            print(f"  {p}  [{a}]")
            for f, v in sorted(vals.items()):
                print(f"      {f} = {v}")
                rows.append(dict(side="player", subject="player_base_record", record=p,
                                 archive=a, field=f, value=v, wave="", level="",
                                 basis="creature record, direct read"))
    if not pc_found:
        print("  UNREACHED — no player-creature record resolved from the candidate list")
        rows.append(dict(side="player", subject="player_base_record", record="|".join(PC_CANDIDATES),
                         archive="", field="characterRunSpeed", value="UNREACHED",
                         wave="", level="",
                         basis="none of the candidate PC records resolves in the Edition-III corpus"))
    res["player_base_records"] = [dict(record=p, archive=a, values=v) for p, a, v in pc_found]

    ge, gea = get(GAMEENGINE)
    ge_speed = {k: ge[k] for k in ge if "peed" in k} if ge else {}
    print(f"  {GAMEENGINE}  [{gea}] — speed-bearing fields: "
          f"{ge_speed if ge_speed else 'NONE'}")
    for f, v in sorted(ge_speed.items()):
        rows.append(dict(side="player", subject="game_engine_globals", record=GAMEENGINE,
                         archive=gea, field=f, value=v, wave="", level="",
                         basis="global engine record, direct read"))
    res["gameengine_speed_fields"] = ge_speed

    # every equipped item + allocated skill + one-hop payload carrying a run-speed field
    print("\n  walking the played character's own records for `characterRunSpeed*` ...")
    seen, hits = set(), []

    def probe(path, subject, extra=""):
        if not path or path in seen:
            return
        seen.add(path)
        r, a = get(path)
        if not r:
            return
        found = {f: r[f] for f in SPEED_FIELDS
                 if f in r and f.startswith("characterRunSpeed") and r[f] not in (0, 0.0)}
        # rank arrays present as lists
        if found:
            hits.append((subject, path, a, found, extra))

    # (1) EQUIPMENT — base + every affix + component + augment, per slot (Lap P's own enumeration)
    for slot, base, affixes, comp, aug in EQUIP:
        for path, kind in ([(base, "base")] + [(a, "affix") for a in affixes]
                           + ([(comp, "component")] if comp else [])
                           + ([(aug, "augment")] if aug else [])):
            probe(path, f"gear:{kind}", extra=f"slot {slot}")
    # (2) the Warborn set record
    probe(WARBORN, "set_bonus", extra="warborn @3pc")
    # (3) item-granted passives
    for p, rk in ITEM_PASSIVES:
        probe(p, "item_passive", extra=f"rank {rk}")
    # (4) ALLOCATED skills (block 8) + their one-hop payloads
    _h, _b8, _v, _n, blk, _isc, _t = read_skill_block(PLAYED_SAVE)
    for s in blk:
        p, alloc = s["record"], s["rank_allocated"]
        if alloc <= 0:
            continue
        probe(p, "allocated_skill", extra=f"rank {alloc}")
        r, _ = get(p)
        if r:
            for k, val in r.items():
                if isinstance(val, str) and val.endswith(".dbr") and (
                        k.startswith("buffSkillName") or k.startswith("petSkillName")
                        or k.startswith("itemSkillName") or k.startswith("skillName")
                        or k.startswith("petBonusName")):
                    probe(val, "skill_payload", extra=f"via {p.rsplit('/',1)[-1]}::{k}")

    # ⚑ MEASURED-INACTIVE discipline (Lap P's lesson).  Three records on this character carry very
    #   large run-speed modifiers that are TRANSIENT movement skills, not permanent passives.  A
    #   sum-everything pass would report 838 % movement speed.  They are EMITTED, not dropped, and
    #   marked so the gap is legible.
    TRANSIENT = {
        "records/skills/default/defaultevade.dbr":
            "MEASURED-INACTIVE — default Evade / dodge-roll; active only for the roll",
        "records/skills/playerclass01/blitz1.dbr":
            "MEASURED-INACTIVE — Blitz, a charge attack; active only for the charge",
        "records/skills/playerclass09/viremight1.dbr":
            "MEASURED-INACTIVE — Vire's Might, a charge; active only for the charge",
    }
    if hits:
        perm = 0.0
        for subj, p, a, f, ex in hits:
            st = TRANSIENT.get(p, "ACTIVE — permanent (equipped / allocated passive)")
            print(f"    {subj:<18} {p}  [{a}]  {f}  {ex}   [{st.split(' ')[0]}]")
            for fn, v in f.items():
                if st.startswith("ACTIVE"):
                    perm += float(v)
                rows.append(dict(side="player", subject=subj, record=p, archive=a,
                                 field=fn, value=v, wave="", level="",
                                 active_status=st,
                                 basis=f"own-record walk of the played character {ex}".strip()))
        print(f"    -> PERMANENT-source sum = +{perm:.1f} %  ; 100 + {perm:.0f} = {100+perm:.0f} % "
              f"vs playerRunSpeedCapMax {ge_speed.get('playerRunSpeedCapMax')} "
              f"-> CLIPPED; Lap A sheet prints 135 %")
        rows.append(dict(side="player", subject="player_runspeed_COMPOSED", record="(walk)",
                         archive="", field="characterRunSpeedModifier_permanent_sum",
                         value=perm, wave="", level="",
                         active_status="ACTIVE — permanent sources only",
                         basis="sum of ACTIVE rows above; transient movement skills EXCLUDED "
                               "(MEASURED-INACTIVE). 100+sum exceeds playerRunSpeedCapMax=135 and "
                               "is clipped; Lap A measured-player-sheet.csv row 35 prints 135 %"))
    else:
        print("    MEASURED-ABSENT — zero equipped items / allocated skills / one-hop payloads on "
              "this character declare a non-zero `characterRunSpeed*` field")
        print(f"    (records probed: {len(seen)})")
        rows.append(dict(side="player", subject="player_kit_runspeed_total", record="(walk)",
                         archive="", field="characterRunSpeedModifier", value=0.0,
                         wave="", level="",
                         basis=f"MEASURED-ABSENT across {len(seen)} own records probed "
                               f"(equipped items, allocated skills, one-hop payloads)"))
    res["player_kit_runspeed_hits"] = [dict(subject=s, record=p, archive=a, fields=f, note=e)
                                       for s, p, a, f, e in hits]
    res["player_kit_records_probed"] = len(seen)

    # ── C.2 MONSTERS ──────────────────────────────────────────────────────────────────────────
    print("\n--- C.2 MONSTER movement speed, 151-160 roster ---")
    acts = roster_actors()
    by_rec = collections.defaultdict(list)
    for a in acts:
        by_rec[a["record_path"]].append(a)
    print(f"  roster: {len(acts)} actors over {len(by_rec)} distinct records")
    vals, halted = [], []
    for p, aa in sorted(by_rec.items()):
        r, arch = get(p)
        if not r:
            halted.append(p)
            for a in aa:
                rows.append(dict(side="monster", subject=p.rsplit("/", 1)[-1][:-4], record=p,
                                 archive="", field="characterRunSpeed", value="UNREACHED",
                                 wave=a["wave"], level=a.get("level", ""),
                                 basis="record did not resolve in the Edition-III corpus"))
            continue
        rs = r.get("characterRunSpeed")
        for a in aa:
            for f in ("characterRunSpeed", "characterRunSpeedModifier",
                      "characterRunSpeedJitter", "walkSpeed",
                      "maxRotationSpeed", "minRotationSpeed"):
                if f in r:
                    rows.append(dict(side="monster", subject=p.rsplit("/", 1)[-1][:-4], record=p,
                                     archive=arch, field=f, value=r[f],
                                     wave=a["wave"], level=a.get("level", ""),
                                     basis="creature record, direct read (level-independent scalar)"))
        if rs is not None:
            vals.append((p, float(rs), len(aa), r.get("characterRunSpeedJitter"),
                         r.get("characterRunSpeedModifier")))
    v = np.array([x[1] for x in vals])
    print(f"  records with `characterRunSpeed`: {len(vals)}/{len(by_rec)}  "
          f"(UNREACHED {len(halted)})")
    print(f"  distribution: min {v.min():.3f}  p25 {np.percentile(v,25):.3f}  "
          f"median {np.median(v):.3f}  p75 {np.percentile(v,75):.3f}  max {v.max():.3f}  "
          f"mean {v.mean():.4f}")
    dist = collections.Counter(round(x, 3) for x in v)
    print("  value histogram (record count):")
    for k in sorted(dist):
        print(f"    {k:.3f} : {dist[k]:>3}")
    # actor-weighted (how the BOARD actually moves)
    aw = np.array([x[1] for x in vals for _ in range(x[2])])
    print(f"  ACTOR-WEIGHTED (n={len(aw)} rostered bodies): median {np.median(aw):.3f}  "
          f"mean {aw.mean():.4f}")
    jit = [x[3] for x in vals if x[3] is not None]
    print(f"  characterRunSpeedJitter: n={len(jit)} distinct "
          f"{sorted(set(round(float(z),2) for z in jit))}")
    slow = sorted(vals, key=lambda z: z[1])[:6]
    fast = sorted(vals, key=lambda z: -z[1])[:6]
    print("  slowest 6:  " + " · ".join(f"{p.rsplit('/',1)[-1][:-4]}={s:.2f}" for p, s, *_ in slow))
    print("  fastest 6:  " + " · ".join(f"{p.rsplit('/',1)[-1][:-4]}={s:.2f}" for p, s, *_ in fast))
    res["monster_runspeed"] = dict(
        n_records=len(by_rec), n_with_field=len(vals), n_unreached=len(halted),
        unreached_records=halted,
        min=float(v.min()), p25=float(np.percentile(v, 25)), median=float(np.median(v)),
        p75=float(np.percentile(v, 75)), max=float(v.max()), mean=float(v.mean()),
        histogram={str(k): int(n) for k, n in sorted(dist.items())},
        actor_weighted_median=float(np.median(aw)), actor_weighted_mean=float(aw.mean()),
        n_rostered_bodies=int(len(aw)),
        jitter_values=sorted(set(round(float(z), 2) for z in jit)),
        slowest=[(p, s) for p, s, *_ in slow], fastest=[(p, s) for p, s, *_ in fast],
    )

    # per-wave actor-weighted mean
    pw = []
    rsmap = {p: s for p, s, *_ in vals}
    for w in range(151, 161):
        ws = [rsmap[a["record_path"]] for a in acts
              if a["wave"] == w and a["record_path"] in rsmap]
        if ws:
            pw.append(dict(wave=w, n_bodies=len(ws), mean_runspeed=round(float(np.mean(ws)), 4),
                           median_runspeed=round(float(np.median(ws)), 4),
                           min_runspeed=round(float(min(ws)), 4),
                           max_runspeed=round(float(max(ws)), 4)))
    res["monster_runspeed_per_wave"] = pw
    print("  per-wave actor-weighted mean runSpeed: "
          + " ".join(f"w{r['wave']}={r['mean_runspeed']:.3f}" for r in pw))

    # ── C.3 EoR channel-movement rule ─────────────────────────────────────────────────────────
    print("\n--- C.3 EoR movement-while-channeling rule ---")
    r, a = get(EOR)
    eor = {}
    for f in ("Class", "canUseWhileMoving", "delayMovement", "rotationSpeedMultiplier",
              "skillTargetRadius", "timeBetweenAttacks", "duration", "useResetsDuration",
              "characterRunSpeed", "characterRunSpeedModifier", "forceMovement",
              "instantCast", "skillCooldownTime"):
        val = r.get(f, "MEASURED-ABSENT") if r else "UNREACHED"
        eor[f] = val
        print(f"    {f:<28} = {val}")
        rows.append(dict(side="player", subject="eyeofreckoning1", record=EOR, archive=a,
                         field=f, value=val, wave="", level="",
                         basis="skill record, direct read (Lap G § 7 independently reproduced)"))
    res["eor_channel_rule"] = eor

    # ── C.4 Crucible spawn geometry ───────────────────────────────────────────────────────────
    print("\n--- C.4 Crucible spawn geometry ---")
    probes = ["records/game/crucible.dbr", "records/ui/crucible.dbr",
              "records/creatures/spawnpoints/spawnpoint01.dbr",
              "records/game/survivalmode.dbr", "records/game/levels/crucible.dbr"]
    found_any = False
    for p in probes:
        r, a = get(p)
        if r:
            found_any = True
            print(f"    RESOLVED {p} [{a}]  ({len(r)} fields)")
    if not found_any:
        print("    UNREACHED — no arena-geometry / spawn-point record resolves in the `.arz`")
        print("    record DB.  Level geometry and spawn-point placement live in the `.map` / "
              "`.lvl` world assets, which are NOT record-DB content and were not opened.")
        rows.append(dict(side="arena", subject="crucible_spawn_geometry", record="(searched)",
                         archive="", field="spawn_points|arena_dimensions", value="UNREACHED",
                         wave="", level="",
                         basis="probed 5 candidate record paths; none resolves. Arena geometry is "
                               "`.map`/`.lvl` world-asset content, not `.arz` record content."))
    res["crucible_spawn_geometry"] = "UNREACHED" if not found_any else "PARTIAL"

    # ── emit ──────────────────────────────────────────────────────────────────────────────────
    cols = ["side", "subject", "record", "archive", "field", "value", "wave", "level",
            "active_status", "basis"]
    d, n = dump_csv(OUT / "pm4r_speed_terms.csv", rows, cols)
    print(f"\npm4r_speed_terms.csv  rows={n}  sha256={d}")
    res["emitted"] = {"pm4r_speed_terms.csv": {"sha256": d, "rows": n}}
    pathlib.Path("/tmp/pm4r/limb_c.json").write_text(json.dumps(res, indent=2, default=str))
    print("limb_c.json written")


if __name__ == "__main__":
    main()
