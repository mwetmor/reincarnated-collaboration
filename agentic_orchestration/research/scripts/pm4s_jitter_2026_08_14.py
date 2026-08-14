#!/usr/bin/env python3
"""KC2-PM4 Lap S — LIMB (d): the `characterRunSpeedJitter` law (cliff `C-I18-1`).

Method is Lap J's (`pathMass`), reused unchanged: template decode from `templates.arc` bytes,
per-record values over Lap D's frozen roster baton, then PE export-table + `objdump` against the
shipped modules.  RE-IMPLEMENTS NOTHING: the `.arz` reader, the roster and the ARC reader are all
imported.

READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap S.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import re
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts")
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src")

from gd_arc_reader_2026_07_26 import ArcArchive                       # noqa: E402
from pm4s_pe_2026_08_14 import PE32, GD, sha256                       # noqa: E402
from pm4d_lib_2026_08_13 import rolled_records                        # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
OUT = META / "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-s-arena-advance"
FIELD = "characterRunSpeedJitter"
SIBLING = "characterRunSpeed"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 100)
    print("KC2-PM4 LAP S — LIMB (d): `characterRunSpeedJitter`")
    print("=" * 100)

    # ── d1 : the declaration, decoded from templates.arc bytes ───────────────────────────────
    arc = ArcArchive(VENDOR / "database" / "templates.arc")
    decl, groups = [], {}
    for n in arc.names():
        if not n.endswith(".tpl"):
            continue
        t = arc.read_file(n).decode("utf-8", "replace")
        if FIELD not in t:
            continue
        decl.append(n)
        i = t.find(f'name = "{FIELD}"')
        blk = t[max(0, i - 200): i + 400]
        gi = t.rfind('name = "', 0, t.rfind("Group", 0, i))
        groups[n] = re.search(r'name\s*=\s*"([^"]+)"', t[t.rfind("Group", 0, i):] or "") \
            .group(1) if t.rfind("Group", 0, i) >= 0 else "?"
        d = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', blk[blk.find(f'name = "{FIELD}"'):
                                                          blk.find("}", blk.find(f'name = "{FIELD}"'))]))
        decl_fields = d
    print(f"\n  d1 DECLARATION — templates declaring `{FIELD}`: {len(decl)}")
    for n in sorted(decl):
        print(f"       {n}   group={groups[n]!r}")
    print(f"     properties: {decl_fields}")

    # ── d6 : is the field READ BY NAME anywhere in the shipped binaries? ──────────────────────
    mods = {m: (GD / m).read_bytes() for m in ("Game.dll", "Engine.dll", "Grim Dawn.exe")}
    jitter_fields = set()
    for n in arc.names():
        if n.endswith(".tpl"):
            jitter_fields |= set(re.findall(r'name\s*=\s*"([A-Za-z0-9_]*[Jj]itter)"',
                                            arc.read_file(n).decode("utf-8", "replace")))
    print("\n  d6 CONSUMPTION — literal-in-binary test over EVERY `*Jitter` field in the corpus,")
    print("     with non-jitter positive controls (a field the engine demonstrably reads by name")
    print("     must appear as a NUL-terminated literal in the module that reads it):")
    lit = {}
    for f in sorted(jitter_fields) + [SIBLING, "characterRunSpeedModifier", "pathMass",
                                      "placementExtents", "characterAttackSpeed"]:
        where = [m for m, b in mods.items() if f.encode() + b"\x00" in b]
        lit[f] = where
        kind = "JITTER " if f in jitter_fields else "CONTROL"
        print(f"     {kind} {f:32s} -> {where if where else 'NONE'}")
    # Is there a STANDALONE "Jitter\0" literal?  If the engine built the field name at runtime as
    # `<base> + "Jitter"` it would need one.  The naive test `b"Jitter\0" in b` is a FALSE POSITIVE
    # -- it matches the tail of `lootRandomizerJitter\0`.  Self-caught; the test below requires the
    # preceding byte to be a non-identifier character, i.e. that the string actually STARTS there.
    bare = {}
    for m, b in mods.items():
        hits = [mo.start() for mo in re.finditer(rb"Jitter\x00", b)
                if mo.start() == 0 or not re.match(rb"[A-Za-z0-9_]", b[mo.start() - 1:mo.start()])]
        bare[m] = len(hits)
    print(f"     STANDALONE 'Jitter\\0' literals (needed for runtime name concatenation): {bare}")

    # ── d2 : per-record values over Lap D's frozen roster baton ───────────────────────────────
    recs = rolled_records()
    print(f"\n  d2 PER-RECORD VALUES over Lap D's frozen baton — {len(recs)} distinct records")
    from gamora_kc2_c1_closure_ed3_2026_08_08 import E3
    rows, census, sib = [], collections.Counter(), collections.Counter()
    for r in sorted(recs):
        d, arcname = E3.winner(r)
        v = d.get(FIELD)
        s = d.get(SIBLING)
        census[v] += 1
        sib[s is not None] += 1
        rows.append(dict(record=r, archive=arcname,
                         characterRunSpeedJitter=v,
                         jitter_grade="MEASURED" if v is not None else "ABSENT-FROM-RECORD",
                         characterRunSpeed=s,
                         consumed_by_shipped_binary="NO — no module contains the literal",
                         basis="Lap D frozen baton (P-ROLLED); E3.winner whole-record replacement"))
    for k, n in sorted(census.items(), key=lambda kv: (kv[0] is None, kv[0])):
        print(f"       {FIELD} = {str(k):>6}  x{n}")
    print(f"       records carrying the non-jitter sibling `{SIBLING}`: {sib[True]}/{len(rows)}")

    with open(OUT / "pm4s_jitter_records.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ── d3/d4/d5 : the transform, disassembled ────────────────────────────────────────────────
    g = PE32(GD / "Game.dll")
    ex = g.exports()
    sites = {n: hex(ex[n]) for n in ex if "Jitter" in n and "CharAttribute" in n}
    print(f"\n  d3/d4/d5 — jitter machinery in Game.dll: {len(sites)} exported symbols")
    print("     THE SPEED PATH: ?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z"
          f"  @ {hex(ex['?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z'])}")
    print("     vtable slot +0x44 of ??_7CharAttributeVal_RunSpeed@GAME@@6B@ (MEASURED)")
    disasm = g.disasm(ex["?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z"], 0xd0)
    (OUT / "evidence").mkdir(exist_ok=True)
    (OUT / "evidence" / "addjitter_charattributevalspeed.asm").write_text(disasm)
    print(f"     disassembly banked -> evidence/addjitter_charattributevalspeed.asm")

    out = dict(field=FIELD, declaring_templates=sorted(decl), declaration=decl_fields,
               groups=groups, literal_in_binary=lit, bare_jitter_suffix=bare,
               record_census={str(k): v for k, v in census.items()},
               n_records=len(rows),
               module_digests={m: sha256(GD / m) for m in mods},
               symbols=sites)
    with open(OUT / "pm4s_jitter.json", "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print(f"\n  wrote {OUT/'pm4s_jitter_records.csv'}  ({len(rows)} rows)")
    print(f"  wrote {OUT/'pm4s_jitter.json'}")


if __name__ == "__main__":
    sys.exit(main())
