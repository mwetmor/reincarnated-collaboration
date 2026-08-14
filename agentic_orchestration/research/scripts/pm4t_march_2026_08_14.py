#!/usr/bin/env python3
"""
pm4t_march_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T2.

LIMB (b): MARCH-SPEED PRICING for the tier-16 waves 151-160 roster.

Decodes the movement-rate chain for all 790 roster bodies:
  * per-record `characterRunSpeed` / `characterRunSpeedModifier` / `characterRunSpeedJitter`
    / `pathMass` / `pathingSize` / `monsterClassification`   (control against Lap R)
  * the SKILL/AURA/CONTROLLER chain of every roster record, searched for permanent movement
    modifiers vs transient movement skills                    (P-B3)
  * the engine caps                                           (`records/game/gameengine.dbr`)
  * the Crucible scaling surface                              (`records/game/survivalinfo.dbr`
    and every survival-archive record) searched for ANY run-speed term   (P-B2)

Emits:
    pm4t_march_speed.csv       one row per roster record
    pm4t_march_summary.json    the aggregate table + the modifier-search results

READ-ONLY.
"""
import csv
import json
import pathlib
import statistics as st
import sys
import collections

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pm4t_arz_2026_08_14 as M

LAPS = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes")
ROSTER = LAPS / "2026-08-14-kc2-pm4-lap-p-sustain-engine" / "pm4p_leech_resistance.csv"
OUT = LAPS / "2026-08-14-kc2-pm4-lap-t-arrival-decode"

EXPAND = {"initialskillname", "buffskillname", "controller", "petskillname",
          "modifierskillname", "skillsecondaryname", "auraskillname", "passiveskillname"}
EXPAND |= {f"skillname{i}" for i in range(1, 18)}

SPEED_FIELDS = ["characterRunSpeed", "characterRunSpeedModifier", "characterRunSpeedMaxModifier",
                "characterRunSpeedJitter", "walkSpeed", "pathMass", "pathingSize",
                "maxRotationSpeed", "minRotationSpeed", "avoidForce"]


def is_neutral(v):
    vals = v if isinstance(v, list) else [v]
    return all((isinstance(x, (int, float)) and x in (0, 0.0)) or x in ("", None, False)
               for x in vals)


def chain_of(corpus, root, max_depth=3):
    seen, frontier = {}, [(root.lower(), 0)]
    while frontier:
        p, d = frontier.pop(0)
        if p in seen or not corpus.has(p):
            continue
        f = corpus.read(p)
        seen[p] = (d, corpus.record_type(p), f)
        if d >= max_depth:
            continue
        for k, v in f.items():
            if k.lower() not in EXPAND:
                continue
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str) and x.lower().endswith(".dbr"):
                    frontier.append((x.lower(), d + 1))
    return seen


def main():
    corpus = M.Corpus()

    # ---------- engine caps
    caps = corpus.read("records/game/gameengine.dbr")
    cap_terms = {k: v for k, v in caps.items() if "RunSpeed" in k or "Speed" in k}

    # ---------- Crucible scaling surface (P-B2)
    survival_speed_hits = []
    survival_archives = {"SurvivalMode.arz", "SurvivalMode1.arz",
                         "SurvivalMode2.arz", "SurvivalMode3.arz"}
    for a in corpus.archives:
        if a.label not in survival_archives:
            continue
        for path in a.index:
            try:
                f = a.read(path)
            except Exception:
                continue
            for k, v in f.items():
                if "RunSpeed" in k and not is_neutral(v):
                    survival_speed_hits.append({"archive": a.label, "record": path,
                                                "field": k, "value": v})
    survivalinfo = corpus.read("records/game/survivalinfo.dbr") if corpus.has(
        "records/game/survivalinfo.dbr") else {}

    # ---------- the roster
    rows = list(csv.DictReader(open(ROSTER)))
    records = {}
    for r in rows:
        records.setdefault(r["record"], r)

    out_rows, missing = [], []
    chain_movement = []
    for rec, meta in sorted(records.items()):
        if not corpus.has(rec):
            missing.append(rec)
            continue
        f = corpus.read(rec)
        row = {"record": rec, "archive": corpus.owner(rec), "class": corpus.record_type(rec),
               "monster_classification": meta.get("monster_classification", ""),
               "display_name": meta.get("display_name", ""),
               "level": meta.get("level", "")}
        for fld in SPEED_FIELDS:
            v = f.get(fld, "")
            row[fld] = json.dumps(v) if isinstance(v, list) else v
        # walk the record's own mechanical chain for movement modifiers
        ch = chain_of(corpus, rec)
        perm, transient = [], []
        for p, (d, cls, ff) in ch.items():
            if p == rec.lower():
                continue
            for k, v in ff.items():
                if "RunSpeed" not in k or is_neutral(v):
                    continue
                entry = {"root": rec, "sub_record": p, "sub_class": cls, "depth": d,
                         "field": k, "value": v}
                # a term is PERMANENT only if it lives on a passive/aura buff class
                if cls and ("Passive" in cls or "Aura" in cls or "Toggled" in cls):
                    perm.append(entry)
                else:
                    transient.append(entry)
                chain_movement.append({**entry, "kind": "permanent" if entry in perm else "transient"})
        row["chain_perm_speed_terms"] = len(perm)
        row["chain_transient_speed_terms"] = len(transient)
        row["chain_size"] = len(ch)
        out_rows.append(row)

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_march_speed.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    # ---------- aggregate
    def nums(field, subset=None):
        return [float(r[field]) for r in (subset or out_rows)
                if r[field] not in ("", None) and not isinstance(r[field], str) or
                (isinstance(r[field], str) and r[field] not in ("",) and
                 r[field].replace(".", "", 1).replace("-", "", 1).isdigit())]

    def fnums(field, subset=None):
        out = []
        for r in (subset or out_rows):
            v = r.get(field, "")
            try:
                out.append(float(v))
            except (TypeError, ValueError):
                pass
        return out

    by_class = {}
    for cls in sorted(set(r["monster_classification"] for r in out_rows)):
        sub = [r for r in out_rows if r["monster_classification"] == cls]
        vals = fnums("characterRunSpeed", sub)
        by_class[cls] = {
            "n_records": len(sub),
            "characterRunSpeed": {
                "n": len(vals), "min": min(vals), "median": st.median(vals),
                "mean": round(st.mean(vals), 6), "max": max(vals),
                "distinct": sorted(set(round(v, 6) for v in vals)),
            },
            "runSpeedModifier_nonzero": sum(1 for r in sub if fnums("characterRunSpeedModifier", [r]) and fnums("characterRunSpeedModifier", [r])[0] != 0),
            "jitter_distinct": sorted(set(fnums("characterRunSpeedJitter", sub))),
            "pathingSize": dict(collections.Counter(r["pathingSize"] for r in sub)),
        }

    allv = fnums("characterRunSpeed")
    summary = {
        "instrument": "I-T2",
        "roster_source": str(ROSTER),
        "roster_records": len(records),
        "records_resolved": len(out_rows),
        "records_missing_from_corpus": missing,
        "engine_caps": cap_terms,
        "survivalinfo_fields": {k: v for k, v in survivalinfo.items()},
        "P_B2_survival_archive_runspeed_hits": survival_speed_hits,
        "P_B3_chain_movement_terms": chain_movement,
        "characterRunSpeed_pooled": {
            "n": len(allv), "min": min(allv), "median": st.median(allv),
            "mean": round(st.mean(allv), 6), "max": max(allv),
            "distinct_count": len(set(round(v, 6) for v in allv)),
        },
        "characterRunSpeedModifier_nonzero_records": [
            {"record": r["record"], "value": r["characterRunSpeedModifier"]}
            for r in out_rows
            if fnums("characterRunSpeedModifier", [r]) and fnums("characterRunSpeedModifier", [r])[0] != 0
        ],
        "by_classification": by_class,
        "archive_digests": corpus.digests,
    }
    with open(OUT / "pm4t_march_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    print(f"roster records {len(records)} | resolved {len(out_rows)} | missing {len(missing)}")
    print("\n--- ENGINE CAPS (records/game/gameengine.dbr)")
    for k, v in sorted(cap_terms.items()):
        print(f"    {k} = {v!r}")
    print("\n--- P-B2: run-speed terms anywhere in the FOUR SURVIVAL archives")
    print(f"    non-neutral hits: {len(survival_speed_hits)}")
    for h in survival_speed_hits[:40]:
        print(f"      {h['archive']} {h['record']} :: {h['field']} = {h['value']!r}")
    print("\n--- P-B3: movement terms in roster records' skill chains")
    print(f"    hits: {len(chain_movement)}")
    for h in chain_movement[:30]:
        print(f"      [{h['kind']}] {h['sub_record']} [{h['sub_class']}] :: {h['field']} = {h['value']!r}")
    print("\n--- characterRunSpeed POOLED")
    print("   ", json.dumps(summary["characterRunSpeed_pooled"]))
    print("\n--- BY CLASSIFICATION")
    for cls, d in by_class.items():
        c = d["characterRunSpeed"]
        print(f"    {cls:10s} n={d['n_records']:4d}  runSpeed min {c['min']:.4f} "
              f"med {c['median']:.4f} mean {c['mean']:.4f} max {c['max']:.4f}  "
              f"distinct={len(c['distinct'])}  modNZ={d['runSpeedModifier_nonzero']}  "
              f"jitter={d['jitter_distinct']}")
    print(f"\n--- characterRunSpeedModifier non-zero roster records: "
          f"{len(summary['characterRunSpeedModifier_nonzero_records'])}")
    for r in summary["characterRunSpeedModifier_nonzero_records"][:20]:
        print(f"      {r['record']} = {r['value']}")


if __name__ == "__main__":
    main()
