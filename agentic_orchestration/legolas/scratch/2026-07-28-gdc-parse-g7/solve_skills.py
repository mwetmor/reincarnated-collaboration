#!/usr/bin/env python3
"""SCRATCH — brute-force the drifted character_skills v8 skill struct.

Reference (1.1.9.1, v5):
    name(s) level(i) enabled(b) devotionLevel(i) experience(i) active(i)
    unknown1(b) unknown2(b) autoCastSkill(s) autoCastController(s)

Search: number of int words after `enabled` (A), byte fields after those (B),
trailing int words after the two autocast strings (C), trailing words after
devotionReclamationPointsUsed (D), and extra words on item_skill (E).

Oracle: all 62 skill entries parse, the block is consumed to exactly its
declared end, and the end-of-block sentinel decrypts to 0.
"""
import itertools
import sys

import gdc_parse as G


def try_layout(path, A, B, C, D, E, enabled_byte=True):
    r, bid, blen, end = G.parse(path, stop_before="character_skills")
    ver = r.read_int()
    n = r.read_int()
    if n > 400:
        return None
    skills = []
    for _ in range(n):
        off = r.p
        s = {"_offset": f"0x{off:x}", "name": r.read_string()}
        s["level"] = r.read_int()
        s["enabled"] = r.read_byte() if enabled_byte else r.read_int()
        s["_ints"] = [r.read_int() for _ in range(A)]
        s["_bytes"] = [r.read_byte() for _ in range(B)]
        s["autoCastSkill"] = r.read_string()
        s["autoCastController"] = r.read_string()
        s["_tail"] = [r.read_int() for _ in range(C)]
        skills.append(s)
    d = {"_version": ver, "skills": skills}
    d["masteriesAllowed"] = r.read_int()
    d["skillReclamationPointsUsed"] = r.read_int()
    d["_devRec_offset"] = f"0x{r.p:x}"
    d["devotionReclamationPointsUsed"] = r.read_int()
    d["_after_devrec"] = [r.read_int() for _ in range(D)]
    m = r.read_int()
    if m > 200:
        return None
    isk = []
    for _ in range(m):
        e = {"name": r.read_string(),
             "autoCastSkill": r.read_string(),
             "autoCastController": r.read_string(),
             "itemSlot": r.read_int(),
             "itemName": r.read_string(),
             "_extra": [r.read_int() for _ in range(E)]}
        isk.append(e)
    d["itemSkills"] = isk
    if r.p != end or not r.peek_key_sync():
        return None
    return d


if __name__ == "__main__":
    path = sys.argv[1]
    hits = []
    for A, B, C, D, E in itertools.product(range(9), range(5), range(5),
                                           range(4), range(3)):
        for eb in (True, False):
            try:
                res = try_layout(path, A, B, C, D, E, eb)
            except Exception:
                continue
            if res:
                hits.append((A, B, C, D, E, eb))
                print(f"HIT A={A} B={B} C={C} D={D} E={E} enabled_byte={eb} "
                      f"skills={len(res['skills'])} itemSkills={len(res['itemSkills'])}")
    print(f"{len(hits)} layout(s) pass the oracle")
