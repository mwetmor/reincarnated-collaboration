"""DATAMINED per-record tables for the reposition / jostle counterfactual (legolas, 2026-10-02). READ-ONLY.

For every creature record in the oracle's fire-range CSV (the v3.8/v3.9 roster + pets) this reads, from the
Edition II database (the referent era; Edition IV is cross-checked and reported):

  controller.randomRepositionChance  -> ControllerMonster+0x2e0 (Load 0x0f7cd5); Attack's per-completion roll
  controller.RepositionChance        -> ControllerMonster+0x3b0 (Load 0x0f7cc1); Attack::ProjectileCollisionCallback
  pathingSize                        -> Character+0x1dd8 (Load 0x0421a6); GetExtents() Small 0.5 / Medium 1.0 / Large 1.75
  monsterClassification              -> Monster+0x3798; Boss(3)/Quest(4)/SuperBoss(5) force +0x3abc
  forceCollision / forceNoCollision  -> Monster+0x3abc / +0x3abd (Load 0x2d59b0 / 0x2d59e2)

and per (record, slot, skill) the skill's distanceProfile (the fire-range CSV column; ABSENT => Melee, range audit L6),
because GD requests an ATTACK SLOT only for distanceProfile Melee (`Skill::NeedsAttackSlot` 0x3c7800 = [skill+0x8c]==0).

Also the player record's numAttackSlots (malepc01/femalepc01).

usage: python3 rj_tables.py <out.json>
"""
import csv
import json
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/"
                   "2026-10-01-kc2-enemy-range-audit/scripts")
import gdlib  # noqa: E402

FR = "/Users/admin/Games/reincarnated-engine/data/kc2/kc2_gd_fire_range_v3p8.csv"
PROBE = ("/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/"
         "scratchpad/hunt2/out/probe_s0.pkl")
EXT = {"Small": 0.5, "Medium": 1.0, "Large": 1.75}
IMMOVABLE_CLASSES = {"Boss", "Quest", "SuperBoss"}


def main(outp: str) -> None:
    rows = list(csv.DictReader(open(FR)))
    recs = {r["record"] for r in rows}
    # the seed-9 boards' own roster + pet records (incl. records with no attack rows in the fire-range CSV),
    # from the residual hunt's board probe (same engine_seed(9, w) line-up)
    import pickle
    probe = pickle.load(open(PROBE, "rb"))
    for w, dd in probe.items():
        recs |= {a["record_path"] for a in dd["actors"]}
        recs |= {p["record_path"] for p in (dd["wave"].get("pets") or [])}
    recs = sorted(recs)
    out = {"source": "Edition II database (referent era), CRUCIBLE precedence (last archive wins); "
                     "Edition IV cross-checked", "records": {}, "skill_profile": {}, "player": {}}
    eds = {e: gdlib.Edition(e) for e in ("II", "IV")}
    n_diff = 0
    for rec in recs:
        row = {}
        for e, ed in eds.items():
            arc, r = ed.winner(rec)
            if r is None:
                row[e] = None
                continue
            ctrl = r.get("controller")
            c = ed.winner(ctrl)[1] if ctrl else None
            cls = r.get("monsterClassification")
            fc = int(r.get("forceCollision") or 0)
            row[e] = {
                "controller": ctrl,
                "randomRepositionChance": (c or {}).get("randomRepositionChance"),
                "RepositionChance": (c or {}).get("RepositionChance"),
                "pathingSize": r.get("pathingSize") or "Small",
                "extents_m": EXT.get(r.get("pathingSize") or "Small", 0.5),
                "monsterClassification": cls,
                "forceCollision": fc,
                "forceNoCollision": int(r.get("forceNoCollision") or 0),
                "immovable": bool(fc or cls in IMMOVABLE_CLASSES),
            }
        if row["II"] != row["IV"]:
            n_diff += 1
        out["records"][rec] = {"II": row["II"], "IV_differs": row["II"] != row["IV"]}
    for r in rows:
        prof = r["distance_profile"]
        key = f'{r["record"]}|{r["slot"]}|{r["skill"]}'
        out["skill_profile"][key] = ("Melee" if prof in ("Melee", "ABSENT") else (prof or None))
    for pc in ("records/creatures/pc/malepc01.dbr", "records/creatures/pc/femalepc01.dbr"):
        for e, ed in eds.items():
            arc, r = ed.winner(pc)
            out["player"][f"{e}:{pc}"] = {"archive": arc, "numAttackSlots": r.get("numAttackSlots"),
                                         "numDefenseSlots": r.get("numDefenseSlots"),
                                         "actorRadius": r.get("actorRadius"), "scale": r.get("scale")}
    out["n_records"] = len(recs)
    out["n_records_II_vs_IV_differ"] = n_diff
    json.dump(out, open(outp, "w"), indent=1, sort_keys=True)
    rr = [v["II"] for v in out["records"].values() if v["II"]]
    print(len(recs), "records;", n_diff, "differ II/IV;",
          sum(1 for v in rr if v["randomRepositionChance"]), "with randomRepositionChance>0;",
          sum(1 for v in rr if v["immovable"]), "immovable")


if __name__ == "__main__":
    main(sys.argv[1])
