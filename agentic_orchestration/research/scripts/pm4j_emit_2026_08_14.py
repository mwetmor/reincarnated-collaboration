#!/usr/bin/env python3
"""LAP J (RUN KC2-PM4) -- decode `pathMass` (cliff C-F6).

Emits `pm4j_pathmass.csv`: one row per body on the E-s09-cp150 board (P-ROLLED-20 roster +
P-SUMMON-128) plus the two player records, carrying the MEASURED `pathMass` field verbatim from
the Edition-III `.arz` corpus, its siblings, and the runtime-effective values implied by the
`Character::GetPathMass()` transform decoded from `Game.dll`.

RE-IMPLEMENTS NOTHING.  Populations, the record reader and the digest helper are imported from
Lap D / Lap F.  A second population definition is a second thing that can drift.

GL-12: every value is read from bytes.  NOTE-9: every row names the basis it was measured on.
No value is rounded -- float32 is emitted verbatim.
"""
import collections
import csv
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pm4d_lib_2026_08_13 import E3, rolled_records                      # noqa: E402
from pm4f_lib_2026_08_13 import populations, PLAYER_RECORDS             # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-j-pathmass")

BAND_B_FIRST_W, BAND_B_LAST_W = 151, 170

#: MEASURED from `Game.dll` `?GetPathMass@Character@GAME@@QBEMXZ` (rva 0x59850), disassembled.
#: The five `Character_ActionState` values that take the x1.0 arm; every other state takes x2.0.
#: Names decoded from the `?GetActionStateAsText@...` jump table at rva 0x471a8.
LOCOMOTION_STATES = {5: "Move", 6: "Walk", 19: "Jump", 20: "Illegal", 21: "Evade"}
MULT_LOCOMOTING = 1.0
MULT_STATIC = 2.0

COLS = (
    "record", "population", "n_actors",
    "path_mass", "path_mass_grade",
    "path_mass_effective_locomoting", "path_mass_effective_static",
    "avoid_force", "pathing_size", "actor_radius",
    "physics_mass", "physics_friction", "physics_restitution",
    "monster_class", "template_name", "archive", "basis",
)

FLOAT_FIELDS = ("pathMass", "avoidForce", "actorRadius",
                "physicsMass", "physicsFriction", "physicsRestitution")


def _raw(r, key):
    """The field VERBATIM -- no rounding, no coercion to a pretty number."""
    v = r.get(key)
    return "" if v is None else repr(float(v)) if key in FLOAT_FIELDS else str(v)


def row(record, population, n_actors):
    r, arc = E3.winner(record)
    if r is None:
        return dict(record=record, population=population, n_actors=n_actors,
                    path_mass="", path_mass_grade="DECLARED-GAP",
                    path_mass_effective_locomoting="", path_mass_effective_static="",
                    avoid_force="", pathing_size="", actor_radius="",
                    physics_mass="", physics_friction="", physics_restitution="",
                    monster_class="", template_name="", archive="",
                    basis="GAP:RECORD-ABSENT-FROM-EDITION-III")
    pm = r.get("pathMass")
    if pm is None:
        grade, eff_lo, eff_hi, basis = ("DECLARED-GAP", "", "",
                                        "GAP:FIELD-ABSENT-FROM-RECORD")
        pm_s = ""
    else:
        pm = float(pm)
        pm_s = repr(pm)
        grade = "MEASURED"
        eff_lo, eff_hi = repr(pm * MULT_LOCOMOTING), repr(pm * MULT_STATIC)
        basis = ("MEASURED:arz-record-field:pathMass|"
                 "effective=DERIVED:Game.dll!Character::GetPathMass@rva0x59850")
    return dict(record=record, population=population, n_actors=n_actors,
                path_mass=pm_s, path_mass_grade=grade,
                path_mass_effective_locomoting=eff_lo,
                path_mass_effective_static=eff_hi,
                avoid_force=_raw(r, "avoidForce"),
                pathing_size=_raw(r, "pathingSize"),
                actor_radius=_raw(r, "actorRadius"),
                physics_mass=_raw(r, "physicsMass"),
                physics_friction=_raw(r, "physicsFriction"),
                physics_restitution=_raw(r, "physicsRestitution"),
                monster_class=_raw(r, "monsterClassification"),
                template_name=_raw(r, "templateName"),
                archive=arc, basis=basis)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    roster, summon, _union = populations()
    agg = rolled_records(first=BAND_B_FIRST_W, last=BAND_B_LAST_W)

    rows = []
    for rec in roster:
        rows.append(row(rec, "P-ROLLED-20", agg[rec]["n_actors"]))
    for rec in summon:
        rows.append(row(rec, "P-SUMMON-128", ""))
    for rec in PLAYER_RECORDS:
        rows.append(row(rec, "P-PLAYER-2", ""))

    path = OUT / "pm4j_pathmass.csv"
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    digest = hashlib.sha256(path.read_bytes()).hexdigest()

    # ---- the census, printed so the note never quotes a number the emitter did not produce ----
    print("rows: %d  (roster %d + summon %d + player %d)"
          % (len(rows), len(roster), len(summon), len(PLAYER_RECORDS)))
    print("roster actor-instances (waves 151-170): %d"
          % sum(agg[r]["n_actors"] for r in roster))
    print("sha256(pm4j_pathmass.csv) = %s" % digest)
    for pop in ("P-ROLLED-20", "P-SUMMON-128", "P-PLAYER-2"):
        c = collections.Counter(r["path_mass"] for r in rows if r["population"] == pop)
        print("  %-13s pathMass census: %s" % (pop, dict(sorted(c.items()))))
    allc = collections.Counter(r["path_mass"] for r in rows)
    print("  BOARD+PLAYER   pathMass census: %s" % dict(sorted(allc.items())))
    print("  grades: %s" % dict(collections.Counter(r["path_mass_grade"] for r in rows)))
    # actor-weighted, because the solver acts on instances, not on records
    aw = collections.Counter()
    for r in rows:
        if r["population"] == "P-ROLLED-20" and r["path_mass"]:
            aw[r["path_mass"]] += int(r["n_actors"])
    print("  roster ACTOR-weighted pathMass census: %s" % dict(sorted(aw.items())))


if __name__ == "__main__":
    main()
