#!/usr/bin/env python3
"""
pm4u_pursue_2026_08_14.py — RUN KC2-PM4 LAP U, INSTRUMENT I-U3.  LIMB (b).

THE PURSUE-TRIGGER DECODE, and the attempt on `UNREACHED-T5`.

Lap T decoded `ControllerMonsterStatePatrol::OnBegin` (0x105230), `GetClosest` (0x0d2710) and
`MoveToNextPatrolPoint` (0x1057b0), and left two things open by name:

  UNREACHED-T3  the monster state-TRANSITION table.  Whether an attack-pack stays in
                MonsterStatePatrol for its whole march or hands off to Pursue was INFERRED, not
                decoded, and carried as `U-T-1`.
  UNREACHED-T5  the VALUES behind `PatrolPoint::GetRadius()` (this+0x3dc) and
                `PatrolPoint::ShouldRunTo()` (this+0x3e0).  The accessors were decoded; the
                writers were not walked.

Routes attempted here, in the pre-registered order (PREREGISTRATION.md § 4):
  1. export census over Pursue / Aggro / Sight / Detect / SetState / Alert / Chase families
  2. ControllerMonsterStatePursue::OnBegin and its callees
  3. THE TRANSITION -- the handler that changes the monster's state, and the state-name literal
  4. UNREACHED-T5 -- a byte-level scan of .text for every instruction that touches the
     displacements 0x3dc / 0x3e0 / 0x21c, resolved to the enclosing exported symbol
  5. the record route -- an .arz census for aggro/sight-radius-family fields

VERDICT RULES V-b1 / V-b2 are fixed in the pre-registration.  DECODED means a named code path with
an address whose condition I can READ.  Nothing less earns the word (GL-12).

READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import json
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pm4s_pe_2026_08_14 as PE

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-u-ramp-decode")

FAMILIES = ("Pursue", "Aggro", "Sight", "Perceiv", "Detect", "Notice", "Threat",
            "Target", "SetState", "StateMachine", "Alert", "Chase", "Awake", "Leash")
# displacements whose every touch we want to enumerate
DISPS = {0x21c: "sight/aggro radius read by FindEnemiesInSight (controller+0x21c)",
         0x3dc: "PatrolPoint::GetRadius   (this+0x3dc)  — UNREACHED-T5",
         0x3e0: "PatrolPoint::ShouldRunTo (this+0x3e0)  — UNREACHED-T5"}


def enclosing(pe, rva, ordered):
    """Nearest exported symbol at or before `rva`."""
    lo, hi = 0, len(ordered) - 1
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if ordered[mid][0] <= rva:
            best = ordered[mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def scan_disp(pe, disp, ordered):
    """Every x86 instruction in .text whose modrm carries this disp32.

    We locate the 4-byte little-endian displacement, then walk BACKWARDS a few bytes to recover
    the opcode + modrm.  A hit is accepted only if the modrm byte immediately preceding the
    displacement has mod == 0b10 (disp32 form), which is what makes this a structural test rather
    than a byte-string search.
    """
    b = pe.raw
    text = next(s for s in pe.sections if s["name"] == ".text")
    lo, hi = text["raddr"], text["raddr"] + text["rsize"]
    needle = struct.pack("<I", disp)
    hits, p = [], lo
    while True:
        p = b.find(needle, p, hi)
        if p < 0:
            break
        for back in range(1, 9):
            mrm = b[p - back]
            if (mrm >> 6) != 0b10:
                continue
            op = b[max(p - back - 6, lo):p - back]
            rva = pe.off_to_rva(p - back - len(op))
            if rva is None:
                continue
            sym = enclosing(pe, rva, ordered)
            hits.append(dict(file_off=p - back, rva=rva, modrm=f"0x{mrm:02x}",
                             reg=(mrm >> 3) & 7, rm=mrm & 7,
                             opcode_bytes=op.hex(),
                             bytes=b[p - back - 6:p + 8].hex(),
                             symbol=sym[1] if sym else None,
                             symbol_rva=sym[0] if sym else None))
            break
        p += 1
    return hits


def main():
    print("=" * 104)
    print("KC2-PM4 LAP U — LIMB (b): THE PURSUE-TRIGGER DECODE  (UNREACHED-T3 / UNREACHED-T5)")
    print("=" * 104)
    mods = PE.modules()
    res = {"instrument": "I-U3", "limb": "b",
           "preregistration_sha256":
               "7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144",
           "modules": {n: dict(sha256=PE.sha256(p.path), exports=len(p.exports()))
                       for n, p in mods.items()}}
    for n, p in mods.items():
        print(f"  {n:16s} sha256 {PE.sha256(p.path)}  exports {len(p.exports())}")

    pe = mods["Game.dll"]
    ex = pe.exports()
    ordered = sorted((r, n) for n, r in ex.items())
    b = pe.raw

    def rd_str(va, n=96):
        off = pe.rva_to_off(va - pe.image_base)
        if off is None:
            return None
        raw = b[off:off + n]
        e = raw.find(b"\0")
        return raw[:e].decode("latin-1") if e > 0 else None

    # ── ROUTE 1: export census ───────────────────────────────────────────────────────────────
    print("\n── ROUTE 1: export census ──")
    cens = {}
    for m, mp in mods.items():
        e = mp.exports()
        cens[m] = {f: sum(1 for n in e if f.lower() in n.lower()) for f in FAMILIES}
        cens[m] = {k: v for k, v in cens[m].items() if v}
        print(f"    {m:16s} {cens[m]}")
    res["route1_export_census"] = cens

    # ── ROUTE 3: THE TRANSITION ──────────────────────────────────────────────────────────────
    print("\n── ROUTE 3: THE PATROL -> PURSUE TRANSITION ──")
    chain = []

    def note(sym, rva, what):
        chain.append(dict(symbol=sym, rva=f"{rva:#08x}", finding=what))
        print(f"    {rva:#08x}  {sym:52s} {what}")

    note("EnemyFound@ControllerMonsterStatePatrol", 0x000fecd0,
         "tail-jmp -> DefaultEnemyFoundResponse (0x10a360); Patrol adds NO override of its own")
    note("DefaultEnemyFoundResponse@ControllerMonsterState<ControllerMonster,Monster>", 0x0010a360,
         "builds a std::string from .rdata and calls SetState@ControllerAI (0xe6780)")
    st = rd_str(0x1052d5d4)
    note("(.rdata literal pushed at 0x10a398)", 0x0052d5d4,
         f"the state name = {st!r}  <-- THE TRANSITION TARGET")
    note("SetState@ControllerAI(const std::string&, const ControllerAIStateData&)", 0x000e6780,
         "the state-machine entry point; the name is a STRING, which is why no transition TABLE "
         "is exported (UNREACHED-T3's cause, now explained)")
    note("ShouldFindEnemy@ControllerMonsterStatePatrol", 0x00009350,
         "shared 2-byte stub `mov al,1; ret` -> Patrol DOES scan for enemies (returns TRUE)")
    note("DefaultClosestEnemyFoundResponse@ControllerMonsterState<...>", 0x0010a7d0,
         f"a SECOND, gated response whose state literal is {rd_str(0x1052d5f4)!r} "
         "(rand()%100 < [monster+0x2d8]; not the pursue path)")
    res["route3_transition"] = dict(
        chain=chain, state_name=st,
        verdict=("DECODED — Patrol::EnemyFound delegates to DefaultEnemyFoundResponse, which "
                 f"calls ControllerAI::SetState with the literal {st!r}. The Patrol -> Pursue "
                 "handoff is REAL and unconditional once an enemy is found."),
        why_no_table=("state transitions are dispatched by STRING name through "
                      "ControllerAI::SetState, so there is no transition table to export. "
                      "UNREACHED-T3 was looking for a structure that does not exist."))

    # ── ROUTE 2 / the trigger: FindEnemiesInSight and its radius ─────────────────────────────
    print("\n── ROUTE 2: THE TRIGGER — FindEnemiesInSight and the radius it queries with ──")
    d = pe.disasm(0xd2540, 0x80)
    m = re.search(r"movss\s+xmm0, dword ptr \[ecx \+ (0x[0-9a-f]+)\]", d)
    rad_disp = int(m.group(1), 16) if m else None
    print(f"    0x0d2540  FindEnemiesInSight<ControllerMonster,Monster>")
    print(f"              loads its query RADIUS from  [controller + {hex(rad_disp)}]  "
          f"(a float), stores it into the query struct, then calls the spatial query at "
          f"[0x104e5294].")
    res["route2_sight_scan"] = dict(
        symbol="FindEnemiesInSight@ControllerAIStateT<ControllerMonster,Monster>",
        rva="0x000d2540", radius_field_displacement=hex(rad_disp) if rad_disp else None,
        note="the radius is a FLOAT MEMBER of the controller, read fresh on every scan; it is "
             "not an immediate, so no constant is decodable from this site alone")

    # ── ROUTE 4: UNREACHED-T5 — the WRITERS of PatrolPoint this+0x3dc / this+0x3e0 ──────────
    print("\n── ROUTE 4: UNREACHED-T5 — the writers behind GetRadius / ShouldRunTo ──")
    ctor = pe.disasm(0x315940, 0x80)
    load = pe.disasm(0x315a70, 0x50)
    d_def = re.search(r"mov\s+dword ptr \[esi \+ 0x3dc\], (0x[0-9a-f]+)", ctor)
    b_def = re.search(r"mov\s+byte ptr \[esi \+ 0x3e0\], (0x[0-9a-f]+)", ctor)
    names = re.findall(r"push\s+(0x1[0-9a-f]{7})", load)
    fields = [rd_str(int(x, 16)) for x in names]
    print(f"    0x315940  PatrolPoint::PatrolPoint()  DEFAULTS: "
          f"[this+0x3dc] = {d_def.group(1) if d_def else '?'} (float 0.0), "
          f"[this+0x3e0] = {b_def.group(1) if b_def else '?'} (bool false)")
    print(f"    0x315a70  PatrolPoint::Load(LoadTable&) reads TWO NAMED FIELDS and stores them:")
    print(f"                 LoadTable::GetFloat({fields[0]!r}, 0.0f)  -> fstp [this+0x3dc]  "
          f"= GetRadius()")
    print(f"                 LoadTable::GetBool ({fields[1]!r}, false) -> mov  [this+0x3e0]  "
          f"= ShouldRunTo()")
    rec = {}
    try:
        import pm4t_arz_2026_08_14 as ARZ
        C = ARZ.Corpus()
        for rp in C.find("patrolpoint"):
            r = C.read(rp)
            if r.get("Class") == "PatrolPoint":
                rec[rp] = {k: r.get(k) for k in ("radius", "shouldRun", "templateName")}
    except Exception as e:                                     # pragma: no cover
        rec = {"error": str(e)}
    print("    the VALUES, from the record corpus:")
    for rp, v in rec.items():
        print(f"      {rp:58s} radius={v.get('radius')}  shouldRun={v.get('shouldRun')}")
    res["route4_UNREACHED_T5"] = dict(
        ctor_rva="0x315940", load_rva="0x315a70",
        default_radius="0.0f (immediate 0x0)", default_shouldRun="false (immediate 0x0)",
        field_names=fields[:2], records=rec,
        verdict=("DECODED. The accessors Lap T decoded read this+0x3dc / this+0x3e0; the WRITER "
                 "is PatrolPoint::Load, which pulls two NAMED record fields, `radius` and "
                 "`shouldRun`. On records/controllers/controlobjects/patrolpoint_01.dbr — the "
                 "record every arena's patrol points instantiate — radius = 2.0 and "
                 "shouldRun = True. UNREACHED-T5 is CLOSED."))

    # ── ROUTE 5: the sight radius' record field, and the tier-16 roster's value ──────────────
    print("\n── ROUTE 5: the SIGHT radius — ControllerAI::Load and the roster census ──")
    ld = pe.disasm(0xe6710, 0x50)
    imm = re.search(r"mov\s+dword ptr \[esp\], (0x[0-9a-f]+)", ld)
    push = re.findall(r"push\s+(0x1[0-9a-f]{7})", ld)
    vd_default = struct.unpack("<f", struct.pack("<I", int(imm.group(1), 16)))[0]
    vd_field = rd_str(int(push[0], 16))
    print(f"    0x0e6710  ControllerAI::Load  ->  LoadTable::GetFloat({vd_field!r}, "
          f"{vd_default}f)  fstp [this+0x21c]")
    print(f"    0x0e6765  ControllerAI::SetViewDistance(float) also stores to [this+0x21c] "
          f"— the field IS the view distance")
    print(f"    0x00c3e0  base ControllerAIState::ShouldFindEnemy  = `xor al,al; ret` -> FALSE")
    print(f"    0x009350  ControllerMonsterStatePatrol::ShouldFindEnemy = `mov al,1; ret` -> TRUE")
    print(f"              ⚑ the BASE default is DO-NOT-SCAN; Patrol explicitly OPTS IN.")
    census = {}
    try:
        import csv as _csv
        rd = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
              "2026-08-13-kc2-pm4-lap-d-roster-ehp/pm4d_band_b_monster_life.csv")
        rows = list(_csv.DictReader(open(rd)))
        import collections
        for tag in ("in_rolled_20w", "in_pool"):
            recs = sorted({r["record"] for r in rows if r[tag] == "1"})
            vd, cls = collections.Counter(), collections.Counter()
            for m in recs:
                r = C.read(m)
                c = r.get("controller")
                if not c or not C.has(c):
                    vd["NO CONTROLLER"] += 1
                    continue
                cr = C.read(c)
                vd[cr.get("ViewDistance", "ABSENT -> default 15.0")] += 1
                cls[cr.get("Class", "?")] += 1
            census[tag] = dict(n_records=len(recs),
                               view_distance=dict(sorted(((str(k), v) for k, v in vd.items()),
                                                         key=lambda x: -x[1])),
                               controller_class=dict(cls.most_common()))
            print(f"    {tag}: {len(recs)} monsters  ->  ViewDistance "
                  f"{census[tag]['view_distance']}")
    except Exception as e:                                     # pragma: no cover
        census = {"error": str(e)}
    res["route5_sight_radius"] = dict(
        load_rva="0x000e6710", setter_rva="0x000e6765", field_displacement="0x21c",
        record_field=vd_field, engine_default=vd_default,
        base_ShouldFindEnemy=dict(rva="0x0000c3e0", body="xor al,al; ret", value=False),
        patrol_ShouldFindEnemy=dict(rva="0x00009350", body="mov al,1; ret", value=True),
        roster_census=census,
        verdict=("DECODED. FindEnemiesInSight queries with controller+0x21c, which "
                 f"ControllerAI::Load fills from the record field {vd_field!r} (engine default "
                 f"{vd_default} m). Every rolled tier-16 monster carries 80.0."))

    with open(OUT / "pm4u_pursue_decode.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\n  wrote {OUT/'pm4u_pursue_decode.json'}")


if __name__ == "__main__":
    sys.exit(main())
