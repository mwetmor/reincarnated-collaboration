#!/usr/bin/env python3
"""ui_settings v7 — solved layout.

Drift vs the 1.1.9.1 (v5) reference is confined to the preamble, which gains
three int words after the five (str,str,byte) groups:

    unknown_a(int)   hotslotCount(int) = 47   unknown_c(int) = 0

NAMING CAUTION. Only the SECOND word is established: it is the hotslot count. That
is confirmed independently by the 2026-08-05 prior solve in
legolas/scratch/2026-08-05-eorwarlguts-parse/gdc2.py, which also records that the
FoA community-tooling fork hard-codes 95 hotslots for v>=7 and thereby overruns a
block written by GD 1.3.0.5.

This module reads unknown_a as a PAGE COUNT (pages * hotslotCount slots). That is a
HYPOTHESIS, not a result. It reconciles both fixture files, and is suggestive on
_Fresh Character 01 -- which reads 2 and carries a Werewolf transform, i.e. a second
action bar -- but the same bytes also parse as a flat 95 slots and I cannot separate
the two readings. For _EoRWarlGuts (unknown_a == 1) the distinction does not arise:
47 slots consume the block exactly under either reading.

The slot struct itself is UNCHANGED. Proof of the slot struct: the gap between
the end of one skill record-path and the start of the next is invariantly 17
bytes across all ten populated slots, which is exactly
isItemSkill(1) + itemLen(4) + equipLocation(4) + nextType(4) + nextSkillLen(4).

Empty slots carry type == 0xFFFFFFFF (-1).

Oracle satisfied on _EoRWarlGuts: pageCount*slotsPerPage slots consume the block
to exactly end-4, the trailing float is a plausible cameraDistance (48.0), and
the end-of-block sentinel decrypts to 0. Preamble size 63 is the ONLY value in
0..99 that satisfies the oracle on both _EoRWarlGuts and _Fresh Character 01.
"""
import json
import sys

import gdc_parse as G

EMPTY = 0xFFFFFFFF


def parse_ui(path):
    r, bid, blen, end = G.parse(path, stop_before="ui_settings")
    ver = r.read_int()
    base = r.p
    out = {"file": path, "version": ver, "payload_bytes": end - base}
    out["unknown1"] = r.read_byte()
    out["unknown2"] = r.read_int()
    out["unknown3"] = r.read_byte()
    out["groups"] = [[r.read_string(), r.read_string(), r.read_byte()]
                     for _ in range(5)]
    out["pageCount"] = r.read_int()
    out["slotsPerPage"] = r.read_int()
    out["v7_unknown"] = r.read_int()

    pages = []
    for pg in range(out["pageCount"]):
        slots = []
        for i in range(out["slotsPerPage"]):
            off = r.p - base
            t = r.read_int()
            s = {"slot": i, "offset": off,
                 "type": (-1 if t == EMPTY else t)}
            if t == 0:
                s["skill"] = r.read_string()
                s["isItemSkill"] = r.read_byte()
                s["item"] = r.read_string()
                s["equipLocation"] = r.read_int()
            elif t == 4:
                s["item"] = r.read_string()
                s["bitmapUp"] = r.read_string()
                s["bitmapDown"] = r.read_string()
                s["label"] = r.read_wstring()
            slots.append(s)
        pages.append(slots)
    out["pages"] = pages

    tail = []
    while end - r.p > 4:
        tail.append(r.read_int())
    out["tail"] = tail
    out["cameraDistance"] = r.read_float() if end - r.p == 4 else None
    out["cursor_at_end"] = (r.p == end)
    out["sentinel_ok"] = r.peek_key_sync()
    return out


if __name__ == "__main__":
    res = parse_ui(sys.argv[1])
    print(f"version={res['version']} pageCount={res['pageCount']} "
          f"slotsPerPage={res['slotsPerPage']} v7_unknown={res['v7_unknown']}")
    print(f"cameraDistance={res['cameraDistance']} tail={res['tail']}")
    print(f"ORACLE: cursor_at_end={res['cursor_at_end']} "
          f"sentinel_ok={res['sentinel_ok']}")
    for pg, slots in enumerate(res["pages"]):
        print(f"\n--- page {pg} ---")
        for s in slots:
            if s["type"] == -1:
                continue
            extra = ""
            if s["type"] == 0:
                extra = (f" skill={s['skill']!r} isItemSkill={s['isItemSkill']}"
                         f" equipLocation={s['equipLocation']}")
                if s["item"]:
                    extra += f" item={s['item']!r}"
            print(f"  slot[{s['slot']:2d}] @{s['offset']:4d} type={s['type']}{extra}")
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], "w"), indent=1)
