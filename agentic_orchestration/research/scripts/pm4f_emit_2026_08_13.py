#!/usr/bin/env python3
"""KC2-PM4 Lap F emitter -- per-record body radii for the 169 roster + 128 summon records + player.

Emits FIVE files into `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-f-body-radii/`:

  1. `pm4f_body_radii.csv`        THE SIM-CONSUMABLE.  298 rows = 169 roster + 128 summon + player,
                                  de-duplicated on `record` with `population` naming the membership.
  2. `pm4f_field_evidence.csv`    the template declaration surface -- every geometry/collision field,
                                  where it is declared, its description, its default, its coverage.
  3. `pm4f_scale_modifier_scan.csv`  Q2's census: every place in the corpus that could scale a body.
  4. `pm4f_discriminators.csv`    F4's four `scale` tests, INCLUDING the two that failed and the
                                  counter-evidence to the one that produced a signal.
  5. `pm4f_mesh_aabb.csv`         the first-of-kind `.msh` chunk-10 AABB decode (corroboration).

READ-ONLY on the vendor corpus, the engine tree and every prior emission.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, iteration I-3, Lap F.
"""
from __future__ import annotations

import collections
import json
import pathlib
import statistics
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4f_lib_2026_08_13 import (  # noqa: E402
    BODY_COLS, COLLISION_FIELDS, FOOTPRINT_FIELDS, GEOM_FIELDS, MeshIndex,
    PLAYER_RECORDS, PLAYER_RECORD_OF_RECORD, Templates, E3,
    body_row, bodies_carrying, colossus_records, corpus_monsters,
    d1_authoring_invariance, d3_gamma, d4_pathing_at_constant_geometry,
    dump, populations, unit_format_strings,
)

OUT = META / "agentic_orchestration" / "legolas" / "notes" / "2026-08-13-kc2-pm4-lap-f-body-radii"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict = {"lap": "KC2-PM4 / I-3 / Lap F", "author": "legolas", "date": "2026-08-13"}

    # ── F1: the template surface ───────────────────────────────────────────────────────────────
    print("[1] templates.arc -- the declaration surface")
    T = Templates()
    summary["templates"] = {"extracted": len(T._raw), "failed": T.failed}
    closures = {r: T.closure(r) for r in ("monster.tpl", "pet.tpl", "player.tpl", "character.tpl")}
    summary["include_closures"] = {k: v for k, v in closures.items()}
    for k, v in closures.items():
        print(f"    {k:14s} closure {len(v):2d}  actor.tpl in chain: {'actor.tpl' in v}")

    field_rows = []
    for field, group in ([(f, "actor.tpl geometry") for f in GEOM_FIELDS]
                         + [(f, "character.tpl footprint") for f in FOOTPRINT_FIELDS]
                         + [(f, "monster.tpl collision") for f in COLLISION_FIELDS]):
        decls = T.declaring_templates(field)
        primary = decls[0] if decls else ""
        d = T.declare(primary, field) if primary else None
        field_rows.append(dict(
            field=field, group=group, declaring_templates=";".join(decls),
            n_declaring=len(decls), primary_template=primary,
            var_class=(d or {}).get("class", ""), var_type=(d or {}).get("type", ""),
            description=(d or {}).get("description", ""),
            default_value=(d or {}).get("defaultValue", ""),
        ))

    # ── F3: the unit proof ─────────────────────────────────────────────────────────────────────
    print("[2] Text_EN.arc -- the unit proof")
    units = unit_format_strings()
    for a, k, v in units:
        print(f"    [{a}] {k} = {v}")
    summary["unit_proof"] = [{"arc": a, "tag": k, "value": v} for a, k, v in units]
    ge, _ = E3.winner("records/game/gameengine.dbr")
    summary["unit_anchors"] = {
        "gameengine.dbr:meleeTargetDistance": float(ge["meleeTargetDistance"]),
        "gameengine.dbr:meleeAutoTargetDistance": float(ge["meleeAutoTargetDistance"]),
        "gameengine.dbr:meleeRange": float(ge["meleeRange"]),
        "sim locomotion.D_ENGAGE_M": 2.4,
        "sim fixture.EOR_RADIUS_M": 3.0,
    }

    # ── populations ────────────────────────────────────────────────────────────────────────────
    print("[3] populations")
    roster, summon, union = populations()
    both = sorted(set(roster) & set(summon))
    print(f"    P-ROLLED-20 {len(roster)}  P-SUMMON-128 {len(summon)}  union {len(union)}  overlap {len(both)}")
    summary["populations"] = {"P-ROLLED-20": len(roster), "P-SUMMON-128": len(summon),
                              "union": len(union), "overlap": len(both), "overlap_records": both}

    # ── the mesh index (D2) ────────────────────────────────────────────────────────────────────
    print("[4] Creatures.arc -- mesh AABB index")
    meshes = MeshIndex()
    print(f"    {len(meshes)} meshes over {len(meshes.arc_counts)} arcs: {meshes.arc_counts}")
    summary["mesh_index"] = {"total": len(meshes), "per_arc": meshes.arc_counts}

    # ── THE BODY TABLE ─────────────────────────────────────────────────────────────────────────
    print("[5] body radii")
    rows = []
    for rec in union:
        pop = ("ROSTER-169+SUMMON-128" if rec in both
               else ("ROSTER-169" if rec in set(roster) else "SUMMON-128"))
        rows.append(body_row(rec, pop, meshes))
    for rec in PLAYER_RECORDS:
        r = body_row(rec, "PLAYER", meshes)
        r["basis"] = r["basis"] + " | Class=Player, templateName=player.tpl"
        rows.append(r)
    # the two player records must agree on every geometry field, or the "player radius" is a choice
    pl = {r["record"]: r for r in rows if r["population"] == "PLAYER"}
    agree = all(pl[PLAYER_RECORDS[0]][k] == pl[PLAYER_RECORDS[1]][k]
                for k in ("radius_m", "radius_m_hi", "actor_scale", "actor_height",
                          "pathing_size", "path_mass", "collision_flag"))
    print(f"    player male/female geometry identical: {agree}")
    summary["player"] = {
        "record_of_record": PLAYER_RECORD_OF_RECORD,
        "male_female_geometry_identical": agree,
        "radius_m": pl[PLAYER_RECORD_OF_RECORD]["radius_m"],
        "radius_m_hi": pl[PLAYER_RECORD_OF_RECORD]["radius_m_hi"],
        "actor_height": pl[PLAYER_RECORD_OF_RECORD]["actor_height"],
        "actor_scale": pl[PLAYER_RECORD_OF_RECORD]["actor_scale"],
        "pathing_size": pl[PLAYER_RECORD_OF_RECORD]["pathing_size"],
        "path_mass": pl[PLAYER_RECORD_OF_RECORD]["path_mass"],
    }

    # ── Q2: the scale-modifier census ──────────────────────────────────────────────────────────
    print("[6] Q2 -- wave / difficulty / champion body-scale modifiers")
    scan_rows = []
    for tpl in ("attributepak.tpl", "gameadjustment.tpl"):
        names = sorted({v["name"] for v in T.variables(tpl) if v.get("name")})
        geo = [n for n in names if any(t in n.lower() for t in
                                       ("size", "scale", "radius", "height", "collis", "bound"))]
        scan_rows.append(dict(surface=tpl, kind="template", n_fields=len(names),
                              geometric_fields=";".join(geo) or "(none)",
                              detail=";".join(names), verdict="NO-GEOMETRIC-FIELD"))
        print(f"    {tpl:22s} fields {len(names):3d}  geometric {geo or '(none)'}")

    colossus = colossus_records()
    colossus_paths = {p for p, _s, _t in colossus}
    carriers = bodies_carrying(union, colossus_paths)
    for p, s, t in colossus:
        scan_rows.append(dict(surface=p, kind="Skill_BuffSelfColossus record", n_fields=2,
                              geometric_fields="actorScale;actorScaleTime",
                              detail=f"actorScale={s};actorScaleTime={t}",
                              verdict="RUNTIME-BODY-SCALE-EXISTS"))
    scan_rows.append(dict(surface="union(297) x skillName*", kind="board census",
                          n_fields=len(union), geometric_fields="actorScale",
                          detail=";".join(f"{a}|{b}|{c}" for a, b, c in carriers) or "(none)",
                          verdict="ZERO-BOARD-BODIES-CARRY-A-BODY-SCALE-SKILL"
                                  if not carriers else "BOARD-BODY-CARRIES-ONE"))
    all_names = T.all_field_names()
    scale_like = sorted(n for n in all_names if n in ("actorScale", "actorScaleTime"))
    scan_rows.append(dict(surface="ALL 819 templates", kind="corpus template sweep",
                          n_fields=len(all_names), geometric_fields=";".join(scale_like),
                          detail="only skill_buffselfcolossus.tpl declares a runtime body scale",
                          verdict="SOLE-RUNTIME-BODY-SCALE-SURFACE"))
    print(f"    Skill_BuffSelfColossus records: {len(colossus)}; board bodies carrying one: {len(carriers)}")
    summary["q2"] = {"colossus_records": colossus, "board_carriers": carriers,
                     "attributepak_geometric_fields": 0, "gameadjustment_geometric_fields": 0}

    # ── F4: the four discriminators ────────────────────────────────────────────────────────────
    print("[7] F4 -- the four `scale` discriminators, over the CORPUS")
    cm = corpus_monsters()
    d1 = d1_authoring_invariance(cm)
    g_raw, g_scl = d3_gamma(cm, False), d3_gamma(cm, True)
    d4 = d4_pathing_at_constant_geometry(cm)
    print(f"    corpus Class=Monster creature records: {len(cm)}")
    print(f"    D1 {d1}")
    print(f"    D3 gamma raw {g_raw['gamma']} vs scaled {g_scl['gamma']}")
    print(f"    D4 varying groups {d4['varying_groups']} agree {d4['pairs_agree']} "
          f"disagree {d4['pairs_disagree']} | constant groups {d4['constant_groups']} "
          f"of which >=1.5x spread {d4['constant_groups_scale_spread_ge_1_5x']}")

    # D2 -- the mesh ratio spread, over the board
    def spread(vals):
        vals = sorted(v for v in vals if v is not None)
        if not vals:
            return {}
        q = statistics.quantiles(vals, n=4) if len(vals) > 3 else [vals[0], vals[0], vals[-1]]
        return dict(n=len(vals), min=round(min(vals), 4), p25=round(q[0], 4),
                    median=round(statistics.median(vals), 4), p75=round(q[2], 4),
                    max=round(max(vals), 4))
    board = [r for r in rows if r["population"] != "PLAYER"]
    r_over_z = [float(r["radius_m"]) / float(r["mesh_aabb_half_z"])
                for r in board if r["mesh_aabb_half_z"] not in ("", None)
                and float(r["mesh_aabb_half_z"]) > 0.01 and r["radius_m"] != ""]
    rs_over_z = [float(r["radius_m_hi"]) / float(r["mesh_aabb_half_z"])
                 for r in board if r["mesh_aabb_half_z"] not in ("", None)
                 and float(r["mesh_aabb_half_z"]) > 0.01 and r["radius_m_hi"] != ""]
    d2 = {"actorRadius/mesh_half_Z": spread(r_over_z),
          "actorRadius*scale/mesh_half_Z": spread(rs_over_z)}
    print(f"    D2 {d2}")

    disc_rows = [
        dict(test="D1-authoring-invariance", basis="corpus Class=Monster mesh-groups, >=3 recs, varying scale",
             n=d1["groups"], result=json.dumps(d1), verdict="EXCLUDES-HAND-AUTHORED-WORLD-RADIUS",
             discriminates="NO"),
        dict(test="D2-mesh-AABB", basis="board records with a resolvable .msh chunk-10 AABB",
             n=len(r_over_z), result=json.dumps(d2),
             verdict="INCONCLUSIVE-bind-pose-AABB-includes-limbs-and-weapons", discriminates="NO"),
        dict(test="D3-pathingSize-gamma", basis="3,070 corpus Class=Monster creature records",
             n=len(cm), result=json.dumps({"gamma_raw": g_raw, "gamma_scaled": g_scl}),
             verdict="INCONCLUSIVE-gamma-moves-0.010", discriminates="NO"),
        dict(test="D4-pathingSize-at-constant-geometry",
             basis="corpus groups sharing (mesh, actorRadius)", n=d4["constant_groups"] + d4["varying_groups"],
             result=json.dumps({k: v for k, v in d4.items() if k != "varying_detail"}),
             verdict="SIGNAL-5/0-BUT-COUNTER-EVIDENCE-37-CONSTANT-GROUPS-SPAN->=1.5x",
             discriminates="NO"),
    ]
    summary["f4_discriminators"] = {"D1": d1, "D2": d2, "D3": {"raw": g_raw, "scaled": g_scl},
                                    "D4": {k: v for k, v in d4.items() if k != "varying_detail"},
                                    "D4_varying_detail": d4["varying_detail"],
                                    "verdict": "scale-applies-to-collision: DECLARED-GAP"}

    # ── mesh AABB table ────────────────────────────────────────────────────────────────────────
    mesh_rows = [dict(record=r["record"], mesh=r["mesh"], mesh_arc=r["mesh_arc"],
                      half_x=r["mesh_aabb_half_x"], half_z=r["mesh_aabb_half_z"],
                      height=r["mesh_aabb_height"], actor_radius=r["radius_m"],
                      actor_scale=r["actor_scale"])
                 for r in rows if r["mesh_aabb_half_z"] not in ("", None)]

    # ── write ──────────────────────────────────────────────────────────────────────────────────
    print("[8] emit")
    digests = {}
    digests["pm4f_body_radii.csv"] = dump(OUT / "pm4f_body_radii.csv", BODY_COLS, rows)
    digests["pm4f_field_evidence.csv"] = dump(
        OUT / "pm4f_field_evidence.csv",
        ("field", "group", "n_declaring", "primary_template", "var_class", "var_type",
         "description", "default_value", "declaring_templates"), field_rows)
    digests["pm4f_scale_modifier_scan.csv"] = dump(
        OUT / "pm4f_scale_modifier_scan.csv",
        ("surface", "kind", "n_fields", "geometric_fields", "verdict", "detail"), scan_rows)
    digests["pm4f_discriminators.csv"] = dump(
        OUT / "pm4f_discriminators.csv",
        ("test", "basis", "n", "discriminates", "verdict", "result"), disc_rows)
    digests["pm4f_mesh_aabb.csv"] = dump(
        OUT / "pm4f_mesh_aabb.csv",
        ("record", "mesh", "mesh_arc", "half_x", "half_z", "height", "actor_radius", "actor_scale"),
        mesh_rows)
    for k, v in digests.items():
        print(f"    {k:32s} {v}")
    summary["digests"] = digests

    # ── the distribution + coverage statements the conductor pre-named ─────────────────────────
    lo = [float(r["radius_m"]) for r in board if r["radius_m"] != ""]
    hi = [float(r["radius_m_hi"]) for r in board if r["radius_m_hi"] != ""]
    by_pathing = collections.defaultdict(list)
    for r in board:
        if r["radius_m"] != "":
            by_pathing[r["pathing_size"]].append(float(r["radius_m"]))
    argmin = min((r for r in board if r["radius_m"] != "" and r["body_kind"] == "PHYSICAL"),
                 key=lambda r: float(r["radius_m"]))
    argmax = max((r for r in board if r["radius_m"] != ""), key=lambda r: float(r["radius_m"]))
    summary["coverage"] = {
        "board_records": len(board),
        "with_actorRadius": sum(1 for r in board if r["radius_m"] != ""),
        "grade_MEASURED": sum(1 for r in board if r["grade"] == "MEASURED"),
        "grade_DECLARED_GAP": sum(1 for r in board if r["grade"] == "DECLARED-GAP"),
        "zero_radius_declared": sum(1 for r in board if r["body_kind"] == "ZERO-RADIUS-DECLARED"),
        "mesh_aabb_resolved": len(mesh_rows),
        "player_rows": 2,
    }
    summary["distribution_lo"] = spread(lo)
    summary["distribution_hi"] = spread(hi)
    summary["by_pathing_size"] = {k: spread(v) for k, v in sorted(by_pathing.items())}
    summary["argmin_physical"] = {k: argmin[k] for k in ("record", "radius_m", "pathing_size")}
    summary["argmax"] = {k: argmax[k] for k in ("record", "radius_m", "pathing_size")}
    summary["collision_flag_census"] = dict(
        collections.Counter(r["collision_flag"] for r in board))
    summary["collision_shape_set_on_board"] = sum(1 for r in board if r["collision_shape"])

    # ── the wave-160 spot check ────────────────────────────────────────────────────────────────
    W160_ROSTER = ["records/creatures/enemies/nemesis/nemesis_kymon_01.dbr",
                   "records/creatures/enemies/nemesis/nemesis_wendigo_01.dbr",
                   "records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
                   "records/creatures/enemies/boss&quest/statue_korvaaktombguardian.dbr"]
    W160_PETS = ["records/creatures/enemies/wraith_b01_summon.dbr",
                 "records/creatures/enemies/wraith_c01_summon.dbr",
                 "records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr"]
    idx = {r["record"]: r for r in rows}
    summary["wave160_spot_check"] = {
        "roster": [{k: idx[r][k] for k in ("record", "radius_m", "radius_m_hi", "actor_scale",
                                           "pathing_size", "grade")} for r in W160_ROSTER],
        "pets": [{k: idx[r][k] for k in ("record", "radius_m", "radius_m_hi", "actor_scale",
                                         "pathing_size", "grade")} for r in W160_PETS],
    }

    (OUT / "pm4f_emit_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(f"[9] summary -> {OUT/'pm4f_emit_summary.json'}")
    print("\nDISTRIBUTION (LO limb, board 297):", summary["distribution_lo"])
    print("DISTRIBUTION (HI limb, board 297):", summary["distribution_hi"])
    print("by pathingSize:", {k: v["median"] for k, v in summary["by_pathing_size"].items()})
    print("collision flags:", summary["collision_flag_census"])


if __name__ == "__main__":
    main()
