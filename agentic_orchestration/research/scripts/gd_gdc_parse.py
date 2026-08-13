#!/usr/bin/env python3
"""Minimal Grim Dawn player.gdc parser — written from scratch for KC2-PM2 Lap A.

Scope: the fields the PM-2 fight sim cross-check needs — header identity, the
character-bio block (level / experience / unspent points / total devotion /
the five stored float attributes), the skill+devotion allocation block, and the
equipped-item block. Everything else is walked and reported by (id, length) only.

Format notes established empirically against `_EoRWarlGuts/player.gdc`
(sha256 c8738da3…):
  * uint32 @0 is the obfuscation seed. GD's stream cipher derives its key table
    from `seed ^ 0x55555555`; when that is 0 the whole table is 0 and the XOR
    stream is the identity, i.e. the file is PLAINTEXT. This save has
    seed == 0x55555555, so no decryption layer is needed. A save with any other
    seed would need the CRC-style key schedule and is OUT OF SCOPE here
    (documented cliff).
  * header: seed, magic "GDCX", version, wname, sex byte, class-tag string,
    level u32, hardcore byte, u32, dataVersion u32, 16 zero bytes.
  * blocks: u32 id, u32 length, <length bytes of payload>, u32 zero end-marker.

No third-party code was used; GDStash / gd-edit were consulted as prose
reference for field ORDER only.
"""
import argparse
import json
import struct
import sys


class R:
    def __init__(self, buf):
        self.b = buf
        self.p = 0

    def u32(self):
        v = struct.unpack_from("<I", self.b, self.p)[0]
        self.p += 4
        return v

    def u8(self):
        v = self.b[self.p]
        self.p += 1
        return v

    def f32(self):
        v = struct.unpack_from("<f", self.b, self.p)[0]
        self.p += 4
        return v

    def s(self):
        n = self.u32()
        v = self.b[self.p:self.p + n].decode("latin-1")
        self.p += n
        return v

    def ws(self):
        n = self.u32()
        v = self.b[self.p:self.p + n * 2].decode("utf-16-le")
        self.p += n * 2
        return v


def parse_header(r):
    seed = r.u32()
    magic = r.b[r.p:r.p + 4].decode("latin-1")
    r.p += 4
    if magic != "GDCX":
        raise ValueError(f"not a GDC file (magic={magic!r})")
    if seed != 0x55555555:
        raise ValueError(
            f"seed 0x{seed:08X} != 0x55555555 -> stream is obfuscated; "
            "this parser only handles the plaintext (key==0) case"
        )
    h = {"seed": f"0x{seed:08X}", "magic": magic, "file_version": r.u32()}
    h["name"] = r.ws()
    h["sex"] = r.u8()
    h["class_tag"] = r.s()
    h["level_header"] = r.u32()
    h["hardcore"] = r.u8()
    # empirically: u32 == 3 (expansion status: AoM + FG) then a single pad byte,
    # then the data version (8 for the v1.2-era format).
    h["expansion_status"] = r.u32()
    h["pad_u8"] = r.u8()
    h["data_version"] = r.u32()
    h["mystery16"] = r.b[r.p:r.p + 16].hex()
    r.p += 16
    return h


def walk_blocks(r):
    """Yield (id, start_of_payload, length) and leave the reader past each block."""
    out = []
    while r.p + 8 <= len(r.b):
        start = r.p
        bid = r.u32()
        blen = r.u32()
        payload = r.p
        end = payload + blen
        if blen == 0 or end + 4 > len(r.b):
            break
        marker = struct.unpack_from("<I", r.b, end)[0]
        if marker != 0:
            out.append({"id": bid, "offset": start, "length": blen, "ok": False})
            break
        out.append({"id": bid, "offset": start, "payload": payload,
                    "length": blen, "ok": True})
        r.p = end + 4
    return out


def parse_bio(buf, payload):
    r = R(buf)
    r.p = payload
    d = {"block_version_raw": r.u32()}
    d["level"] = r.u32()
    d["experience"] = r.u32()
    d["attribute_points_unspent"] = r.u32()
    d["skill_points_unspent"] = r.u32()
    d["devotion_points_unspent"] = r.u32()
    d["devotion_points_total_spent"] = r.u32()
    for k in ("physique", "cunning", "spirit", "health", "energy"):
        d[k + "_stored_float"] = round(r.f32(), 3)
    return d


def parse_skills(buf, payload, blen):
    """Skill block: u32 version, u32 count, then per entry
    name(str) level(u32) enabled(u8) devotion_level(u32) experience(u32)
    active(u32) u8 u8 autocast_skill(str) autocast_controller(str).
    Followed by a second (item-skill) list. Parsed defensively."""
    r = R(buf)
    r.p = payload
    end = payload + blen
    out = {"block_version_raw": r.u32(), "skills": [], "item_skills": []}
    n = r.u32()
    out["declared_count"] = n
    for i in range(n):
        if r.p >= end:
            out["desync_at_index"] = i
            break
        try:
            e = {"name": r.s(), "level": r.u32(), "enabled": r.u8(),
                 "devotion_level": r.u32(), "experience": r.u32(),
                 "active": r.u32(), "u8a": r.u8(), "u8b": r.u8(),
                 "autocast_skill": r.s(), "autocast_controller": r.s()}
        except Exception as exc:
            out["desync_at_index"] = i
            out["desync_error"] = repr(exc)
            break
        if not e["name"].startswith("records/"):
            out["desync_at_index"] = i
            out["desync_name"] = e["name"][:60]
            break
        out["skills"].append(e)
    if r.p + 4 <= end and "desync_at_index" not in out:
        m = r.u32()
        out["item_skill_declared_count"] = m
        for i in range(m):
            if r.p >= end:
                break
            try:
                out["item_skills"].append({
                    "name": r.s(), "autocast_skill": r.s(),
                    "autocast_controller": r.s(), "item_slot": r.u32(),
                    "item_name": r.s(), "u32": r.u32()})
            except Exception as exc:
                out["item_skill_desync_at_index"] = i
                out["item_skill_desync_error"] = repr(exc)
                break
    return out


def scan_records(buf, prefixes):
    """Length-prefixed ASCII record paths anywhere in the file. Robust against
    unparsed block internals — used to enumerate equipped gear when the strict
    inventory walk is not attempted."""
    hits = []
    i = 0
    n = len(buf)
    while i < n - 8:
        ln = struct.unpack_from("<I", buf, i)[0]
        if 8 <= ln <= 200 and i + 4 + ln <= n:
            try:
                s = buf[i + 4:i + 4 + ln].decode("ascii")
            except UnicodeDecodeError:
                i += 1
                continue
            if any(s.startswith(p) for p in prefixes) and s.endswith(".dbr"):
                hits.append((i, s))
                i += 4 + ln
                continue
        i += 1
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", help="write full result here")
    a = ap.parse_args()
    buf = open(a.path, "rb").read()
    r = R(buf)
    res = {"file": a.path, "size": len(buf)}
    res["header"] = parse_header(r)
    blocks = walk_blocks(r)
    res["blocks"] = [{k: v for k, v in b.items() if k != "payload"} for b in blocks]

    for b in blocks:
        if not b.get("ok"):
            continue
        if b["id"] == 2:
            try:
                res["bio"] = parse_bio(buf, b["payload"])
            except Exception as e:  # documented cliff, never a guess
                res["bio_error"] = repr(e)
        if b["id"] == 8:
            try:
                res["skills_block"] = parse_skills(buf, b["payload"], b["length"])
            except Exception as e:
                res["skills_error"] = repr(e)

    recs = scan_records(buf, ("records/items/", "records/skills/"))
    res["record_scan"] = {
        "items": sorted({s for _, s in recs if s.startswith("records/items/")}),
        "skills": sorted({s for _, s in recs if s.startswith("records/skills/")}),
    }
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=2)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("record_scan",)}, indent=2)[:6000])
    print("\nitems:", len(res["record_scan"]["items"]),
          "skills:", len(res["record_scan"]["skills"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
