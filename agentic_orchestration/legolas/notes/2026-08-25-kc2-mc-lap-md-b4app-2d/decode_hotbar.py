#!/usr/bin/env python3
"""
decode_hotbar.py — READ-ONLY. Block-index + hot-bar / skills / play-stats decode
for Fangs-of-Asterkarn-era player.gdc, where several block INTERIORS have drifted
past the community reference but the block FRAME has not.

Method (lap MD-B4app-2d): the top-level block ID sequence is fixed and known, and
the first word of every block is `read_int()` of that ID. Known plaintext ⇒ the
XOR key is recoverable at every block boundary independently. Walking the declared
block lengths therefore yields a complete block index without parsing any interior,
and the index is SELF-VERIFYING: it must land exactly on EOF.

Drifted interiors (inventory v11 vs reference v4) are skipped, not guessed.

NO WRITE PATH. Files are opened 'rb'.
"""

import json
import struct
import sys

import gdc_read

# fixed top-level order, from gdc_file::read() in decrypt-player.cpp
BLOCK_ORDER = [
    (1, "character_info"), (2, "character_bio"), (3, "inventory"),
    (4, "character_stash"), (5, "respawn_list"), (6, "teleport_list"),
    (7, "marker_list"), (17, "shrine_list"), (8, "character_skills"),
    (12, "lore_notes"), (13, "faction_pack"), (14, "ui_settings"),
    (15, "tutorial_pages"), (16, "play_stats"), (10, "trigger_tokens"),
]


def header_and_index(path):
    data = open(path, "rb").read()
    r = gdc_read.Reader(data)
    hdr = {"file": path, "size": len(data)}
    hdr["magic_ok"] = (r.read_int() == 0x58434447)
    r.read_int()
    hdr["name"] = r.read_wstr()
    hdr["sex"] = r.read_byte()
    hdr["tag"] = r.read_str()
    hdr["level"] = r.read_int()
    hdr["hardcore"] = r.read_byte()
    r.read_byte()
    r.next_int()
    hdr["file_version"] = r.read_int()
    hdr["uid"] = "".join("%02x" % r.read_byte() for _ in range(16))

    pos = r.p
    index = {}
    for bid, name in BLOCK_ORDER:
        b = r.seek_block(pos, bid, name)
        index[name] = {"start": pos, "len": b["len"], "end": b["end"]}
        pos = b["end"] + 4          # +4 = the end-of-block sentinel word
    hdr["index_lands_on_eof"] = (pos == len(data))
    hdr["index_final_pos"] = pos
    return data, r, hdr, index


def _walk_slots(bytev, ints, start, body_len):
    """Chain hot_slot records from `start`. Returns (slots, end_offset)."""
    def rstr(p):
        n = ints[p]
        if n > 4096:
            raise ValueError("bad string length %d at %d" % (n, p))
        return bytev[p + 4:p + 4 + n].decode("latin1"), p + 4 + n

    slots = []
    p = start
    while p < body_len - 4:
        t = ints[p]
        q = p + 4
        s = {"index": len(slots), "type": t}
        if t == 0:
            s["skill"], q = rstr(q)
            s["isItemSkill"] = bytev[q]
            q += 1
            s["item"], q = rstr(q)
            s["equipLocation"] = ints[q]
            q += 4
        elif t == 4:
            s["item"], q = rstr(q)
            s["bitmapUp"], q = rstr(q)
            s["bitmapDown"], q = rstr(q)
            n = ints[q]
            q += 4 + 2 * n
        s["position"] = gdc_read.SLOT_POSITION.get(
            s["index"], "unmapped index %d" % s["index"])
        s["type_name"] = gdc_read.TYPE_NAME.get(t, "type=%d" % t)
        slots.append(s)
        p = q
    return slots, p


def read_ui_settings(path):
    """Decode block 14 without assuming the reference preamble size.

    The Fangs-era block is version 7 and carries ~12 bytes of preamble the
    reference (v5) does not know about, so the slot-array start is UNKNOWN.
    Rather than guess it, every plausible start is tried and accepted only if
    the resulting chain satisfies three INDEPENDENT structural anchors:

      (1) the chain lands exactly on the trailing cameraDistance float;
      (2) slot 24 decodes as type 2  (health potion);
      (3) slot 25 decodes as type 3  (energy potion).

    A wrong start cannot satisfy all three; this is a validation, not a guess.
    """
    import dump_block
    data, hdr, index, bs, bl, bytev, ints = dump_block.block_views(
        path, 14, "ui_settings")
    ui = {"block_version": ints[0], "body_start": bs, "body_len": bl}
    accepted = None
    for start in range(10, 200):
        try:
            slots, end = _walk_slots(bytev, ints, start, bl)
        except Exception:
            continue
        if end != bl - 4 or len(slots) < 26:
            continue
        if slots[24]["type"] == 2 and slots[25]["type"] == 3:
            accepted = (start, slots)
            break
    if accepted is None:
        ui["error"] = "no slot-array start satisfies the three anchors"
        return ui
    ui["slot_array_start"] = accepted[0]
    ui["slots"] = accepted[1]
    ui["slot_count"] = len(accepted[1])
    ui["anchors_ok"] = True
    ui["cameraDistance"] = struct.unpack(
        "<f", struct.pack("<I", ints[bl - 4]))[0]
    return ui


def read_skills(r, index):
    b = r.seek_block(index["character_skills"]["start"], 8, "character_skills")
    out = {"block_version": r.read_int()}
    n = r.read_int()
    skills = []
    for _ in range(n):
        s = {"name": r.read_str(), "level": r.read_int(),
             "enabled": r.read_byte(), "devotionLevel": r.read_int(),
             "experience": r.read_int(), "active": r.read_int()}
        r.read_byte()
        r.read_byte()
        s["autoCastSkill"] = r.read_str()
        s["autoCastController"] = r.read_str()
        skills.append(s)
    out["skills"] = skills
    out["masteriesAllowed"] = r.read_int()
    out["skillReclamationPointsUsed"] = r.read_int()
    out["devotionReclamationPointsUsed"] = r.read_int()
    n = r.read_int()
    out["itemSkills"] = [{"name": r.read_str(), "autoCastSkill": r.read_str(),
                          "autoCastController": r.read_str(),
                          "itemSlot": r.read_int(), "itemName": r.read_str()}
                         for _ in range(n)]
    out["landed_on_block_end"] = (r.p == b["end"])
    out["residual_bytes"] = b["end"] - r.p
    return out


def read_bio(r, index):
    r.seek_block(index["character_bio"]["start"], 2, "character_bio")
    out = {"block_version": r.read_int()}
    for f in ("level", "experience", "attributePointsUnspent",
              "skillPointsUnspent", "devotionPointsUnspent",
              "totalDevotionUnlocked"):
        out[f] = r.read_int()
    for f in ("physique", "cunning", "spirit", "health", "energy"):
        out[f] = r.read_float()
    return out


def read_play_stats(r, index):
    b = r.seek_block(index["play_stats"]["start"], 16, "play_stats")
    ps = {"block_version": r.read_int()}
    for f in ("playTime", "deaths", "kills", "experienceFromKills",
              "healthPotionsUsed", "manaPotionsUsed", "maxLevel",
              "hitsReceived", "hitsInflicted", "criticalHitsInflicted",
              "criticalHitsReceived"):
        ps[f] = r.read_int()
    ps["greatestDamageInflicted"] = r.read_float()
    ps["perDifficulty"] = [
        {"greatestMonsterKilledName": r.read_str(),
         "greatestMonsterKilledLevel": r.read_int(),
         "greatestMonsterKilledLifeAndMana": r.read_int(),
         "lastMonsterHit": r.read_str(),
         "lastMonsterHitBy": r.read_str()} for _ in range(3)]
    ps["championKills"] = r.read_int()
    ps["lastHit"] = r.read_float()
    ps["lastHitBy"] = r.read_float()
    ps["greatestDamageReceived"] = r.read_float()
    for f in ("heroKills", "itemsCrafted", "relicsCrafted",
              "transcendentRelicsCrafted", "mythicalRelicsCrafted",
              "shrinesRestored", "oneShotChestsOpened", "loreNotesCollected"):
        ps[f] = r.read_int()
    ps["bossKills"] = [r.read_int() for _ in range(3)]
    ps["survivalWaveTier"] = r.read_int()
    ps["greatestSurvivalScore"] = r.read_int()
    ps["cooldownRemaining"] = r.read_int()
    ps["cooldownTotal"] = r.read_int()
    n = r.read_int()
    ps["v"] = [[r.read_str(), r.read_int()] for _ in range(n)]
    ps["residual_bytes"] = b["end"] - r.p
    return ps


def decode(path):
    data, r, hdr, index = header_and_index(path)
    res = {"header": hdr, "index": index, "errors": {}}
    for key, fn in (("character_bio", read_bio),
                    ("character_skills", read_skills),
                    ("play_stats", read_play_stats)):
        try:
            res[key] = fn(r, index)
        except Exception as exc:
            res["errors"][key] = "%s: %s" % (type(exc).__name__, exc)
    try:
        res["ui_settings"] = read_ui_settings(path)
    except Exception as exc:
        res["errors"]["ui_settings"] = "%s: %s" % (type(exc).__name__, exc)
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(decode(p), indent=1, ensure_ascii=False))
