#!/usr/bin/env python3
"""
d3_lib.py — KC2 MODEL-COMPLETION RUN, piece D-3.  Shared library.  READ-ONLY.

Decodes the remaining ControllerMonster field GROUPS against:
  (1) the shipped TEMPLATE  (database/templates.arc -> controllermonster.tpl / controllerai.tpl)
      — field name, type, group, engine-side default, and Crate's own description string
  (2) the RECORD corpus     (8-archive layered .arz, override order per pm4t_arz)
      — the values actually carried by THIS fight's roster's controllers
  (3) the BINARY            (Game.dll) — which code reads the field, i.e. the SEMANTICS

Roster basis: `pm4d_band_b_monster_life.csv` (Lap D), columns `in_rolled_20w` / `in_pool`.
Controller join: monster record field `controller` -> controller .dbr  (the Lap U join, verbatim).

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-24.
"""
from __future__ import annotations

import collections
import csv
import pathlib
import re
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
SCRIPTS = META / "agentic_orchestration" / "research" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import pm4t_arz_2026_08_14 as ARZ            # noqa: E402
import pm4s_pe_2026_08_14 as PE              # noqa: E402

TPL_DIR = (META / "agentic_orchestration" / "legolas" / "scratch"
           / "2026-08-08-kc2-halt-bundle" / "tpl")
ROSTER = (META / "agentic_orchestration" / "legolas" / "notes"
          / "2026-08-13-kc2-pm4-lap-d-roster-ehp" / "pm4d_band_b_monster_life.csv")
OUT = (META / "agentic_orchestration" / "legolas" / "notes"
       / "2026-08-24-kc2-mc-lap-d3-controller-groups")

# The D-3 target groups (charter).  Senses / AngerManagement / DistressCalls / Pursuit are
# ALREADY DECODED (WR3-W2, Lap U) and are NOT redone; they appear only as context columns.
TARGET_GROUPS = ["SkillUsage", "Attacking", "Dodging", "Fleeing", "PetBehaviour",
                 "Roaming", "Patrolling", "Emote", "Sleep", "Loot", "Dying", "RandomAnger"]
DONE_GROUPS = ["Senses", "AngerManagement", "DistressCalls", "Pursuit"]


# ─────────────────────────────────────────────────────────────────── template parsing
_VAR = re.compile(
    r'Variable\s*\{(.*?)\}', re.S)
_KV = re.compile(r'(\w+)\s*=\s*"(.*?)"', re.S)


def parse_tpl(path: pathlib.Path):
    """Return [(group, name, class, type, description, defaultValue)] in file order.

    The .tpl grammar is brace-nested `Group { name=... Variable { ... } ... }`.  We track the
    innermost enclosing Group name by a single-pass brace walk — no regex nesting games.
    """
    txt = path.read_text(errors="replace")
    out, stack, i = [], [], 0
    while i < len(txt):
        m = re.compile(r'\b(Group|Variable)\s*\{', re.S).search(txt, i)
        if not m:
            break
        kind = m.group(1)
        # find matching close brace
        depth, j = 1, m.end()
        while j < len(txt) and depth:
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
            j += 1
        body = txt[m.end():j - 1]
        if kind == "Group":
            gname = re.search(r'name\s*=\s*"(.*?)"', body)
            stack.append(gname.group(1) if gname else "?")
            i = m.end()                      # descend
        else:
            kv = dict(_KV.findall(body))
            out.append(dict(group=stack[-1] if stack else "?",
                            name=kv.get("name", "?"),
                            vclass=kv.get("class", ""),
                            vtype=kv.get("type", ""),
                            description=kv.get("description", ""),
                            default=kv.get("defaultValue", "")))
            i = j
        # pop groups whose closing brace we have passed
        while stack:
            break
    return out


def parse_tpl_ordered(path: pathlib.Path):
    """Correct brace-aware walk producing (group, variable) pairs."""
    txt = path.read_text(errors="replace")
    toks = list(re.finditer(r'\b(Group|Variable)\s*\{|\}', txt))
    out, stack = [], []
    for t in toks:
        if t.group(0) == "}":
            if stack:
                stack.pop()
            continue
        kind = t.group(1)
        # body = up to the matching close, computed lazily for the name only
        depth, j = 1, t.end()
        while j < len(txt) and depth:
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
            j += 1
        body = txt[t.end():j - 1]
        if kind == "Group":
            gname = re.search(r'name\s*=\s*"(.*?)"', body)
            stack.append(gname.group(1) if gname else "?")
        else:
            kv = dict(_KV.findall(body))
            out.append(dict(group=stack[-1] if stack else "?",
                            name=kv.get("name", "?"),
                            vclass=kv.get("class", ""),
                            vtype=kv.get("type", ""),
                            description=kv.get("description", ""),
                            default=kv.get("defaultValue", "")))
            stack.append("__VAR__")          # so the closing } pops the var, not the group
    return out


def template_surface():
    """Full ControllerMonster field surface = controllerai.tpl (base) + controllermonster.tpl."""
    base = parse_tpl_ordered(TPL_DIR / "controllerai.tpl")
    derived = parse_tpl_ordered(TPL_DIR / "controllermonster.tpl")
    seen, out = set(), []
    for src, rows in (("controllerai.tpl", base), ("controllermonster.tpl", derived)):
        for r in rows:
            if r["name"] in ("ActorName", "Class", "FileDescription", "Include File"):
                continue
            if r["name"] in seen:
                continue
            seen.add(r["name"])
            r = dict(r)
            r["tpl"] = src
            out.append(r)
    return out


# ─────────────────────────────────────────────────────────────────── roster / corpus
def roster(flag="in_rolled_20w"):
    rows = list(csv.DictReader(open(ROSTER)))
    return sorted({r["record"] for r in rows if r[flag] == "1"})


def controller_join(C, monsters):
    """monster .dbr -> controller .dbr.  Returns (mapping, unresolved)."""
    mp, bad = {}, []
    for m in monsters:
        if not C.has(m):
            bad.append((m, "monster record ABSENT"))
            continue
        r = C.read(m)
        c = r.get("controller")
        if isinstance(c, list):
            c = c[0] if c else None
        if not c or not C.has(c):
            bad.append((m, f"controller {c!r} absent"))
            continue
        mp[m] = c
    return mp, bad


def census(C, controllers, fields):
    """{field: Counter(value)} over the given controller record set, ABSENT counted."""
    out = {f: collections.Counter() for f in fields}
    cls = collections.Counter()
    for c in controllers:
        r = C.read(c)
        cls[r.get("Class", "?")] += 1
        for f in fields:
            v = r.get(f, "__ABSENT__")
            if isinstance(v, list):
                v = ";".join(str(x) for x in v) if v else "__EMPTY__"
            out[f][str(v)] += 1
    return out, cls


def all_controllermonster_records(C):
    """Every record in the layered corpus whose winning Class is ControllerMonster."""
    out = []
    for p in C.paths():
        if not p.startswith("records/controllers"):
            continue
        try:
            r = C.read(p)
        except Exception:
            continue
        if r.get("Class") == "ControllerMonster":
            out.append(p)
    return sorted(out)
