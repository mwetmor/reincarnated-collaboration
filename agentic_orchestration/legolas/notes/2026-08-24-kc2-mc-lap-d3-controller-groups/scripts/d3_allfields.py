#!/usr/bin/env python3
"""D-3 STEP 6 — EVERY record field ControllerMonster::Load actually consumes.

Not "every field the .tpl exposes" — every field name literal PUSHED as an argument inside
ControllerMonster::Load.  Diffed against the template surface in both directions:
  * template-but-not-binary  => the editor exposes a field the engine ignores (DEAD FIELD)
  * binary-but-not-template  => the engine reads a field the editor never shows (HIDDEN FIELD)
READ-ONLY."""
from __future__ import annotations
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L, d3_binary as B
from d3_picklist import RAW, cstr_at
OUT = pathlib.Path(__file__).resolve().parent

VTBL = {0x14: "GetString", 0x18: "GetBool?", 0x1c: "GetInt", 0x20: "GetIntArray?",
        0x24: "GetFloat", 0x28: "GetFloatArray?"}


def main():
    pe = L.PE.PE32(L.PE.GD / "Game.dll")
    ins = []
    for line in open(OUT / "d3_ctrlmonster_load.asm"):
        m = RAW.match(line.rstrip("\n").replace("\t", " "))
        if m:
            ins.append((int(m.group(1), 16), " ".join(m.group(3).split())))

    seen = []
    for i, (a, t) in enumerate(ins):
        m = re.match(r"push (0x1[0-9a-f]{7})$", t)
        if not m:
            continue
        s = cstr_at(pe, int(m.group(1), 16))
        if not s or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,}", s):
            continue
        # the CALL that consumes it, within 12 instructions
        call = None
        for j in range(i + 1, min(i + 14, len(ins))):
            c = re.match(r"call (?:dword ptr )?\[e[a-z]{2} \+ (0x[0-9a-f]+)\]$", ins[j][1])
            if c:
                call = VTBL.get(int(c.group(1), 16), f"vtbl+{c.group(1)}")
                break
            if re.match(r"call dword ptr \[eax \+ (0x[0-9a-f]+)\]$", ins[j][1]):
                pass
        seen.append((hex(a), s, call))

    tpl = {r["name"] for r in L.template_surface()}
    # a pushed literal is either a FIELD NAME (consumed by a Get*) or a picklist TOKEN/default
    field_names, tokens = [], []
    for a, s, call in seen:
        (field_names if call else tokens).append((a, s, call))

    fn = sorted({s for _, s, _ in field_names})
    print(f"ControllerMonster::Load pushes {len(fn)} distinct literals that reach a LoadTable::Get*")
    print("\n--- BINARY-CONSUMED, NOT IN THE TEMPLATE (hidden fields) ---")
    hidden = [s for s in fn if s not in tpl]
    for s in hidden:
        calls = sorted({c for _, x, c in field_names if x == s})
        print(f"  {s:34s} {calls}")
    print("\n--- TEMPLATE-EXPOSED, NEVER PUSHED IN Load (dead fields) ---")
    dead = sorted(tpl - set(fn))
    for s in dead:
        print(f"  {s}")
    json.dump(dict(consumed=fn, hidden=hidden, dead=dead,
                   all_push_sites=seen), open(OUT / "d3_allfields.json", "w"), indent=2)


if __name__ == "__main__":
    main()
