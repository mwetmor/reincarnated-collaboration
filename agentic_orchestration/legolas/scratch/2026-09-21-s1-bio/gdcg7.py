#!/usr/bin/env python3
"""
NON-PRODUCTION SCRATCH TOOLING — legolas / KIT-CAL-1 pass G-7 / 2026-07-28

Grim Dawn .gdc character-save reader. READ-ONLY. Never writes to the input.

Port of AaronHutchinson/Grim-Dawn-Save-Decryption (decrypt-player.cpp @ GD 1.1.9.1)
with two deliberate deviations required by the commission:

  1. LOG-DON'T-THROW on every struct-version assert. Edition-II / Fangs-of-Asterkarn
     is expected to have bumped versions past the 1.1.9.1 reference. Observed-vs-
     expected pairs are recorded, not fatal.
  2. PER-BLOCK BANKING. Each top-level block is parsed inside a checkpoint; a block
     that fails does not lose the blocks already banked.

Resync note: update_key() mixes only *ciphertext* bytes, so the key state can be
replayed over a skipped span without decrypting it. Block-end sentinels are
written as literal 0, so the stored raw word equals the key at that point -- a
free 32-bit sync check. That makes skip-and-resync possible after a bad block.
"""

import json
import struct
import sys

MAGIC = 0x58434447  # "GDCX" LE


class Reader:
    def __init__(self, data):
        self.d = data
        self.p = 0
        self.key = 0
        self.table = [0] * 256
        self.notes = []

    # --- cipher ---------------------------------------------------------
    def read_key(self):
        k = struct.unpack_from("<I", self.d, self.p)[0]
        self.p += 4
        k ^= 0x55555555
        self.key = k
        for i in range(256):
            k = ((k >> 1) | (k << 31)) & 0xFFFFFFFF
            k = (k * 39916801) & 0xFFFFFFFF
            self.table[i] = k

    def _advance(self, raw_bytes):
        for b in raw_bytes:
            self.key ^= self.table[b]
        self.key &= 0xFFFFFFFF

    def next_int(self):
        """Decrypt 4 bytes WITHOUT advancing the key (block lengths, sentinels)."""
        v = struct.unpack_from("<I", self.d, self.p)[0]
        self.p += 4
        return v ^ self.key

    def peek_key_sync(self):
        """True if the 4 bytes at cursor decrypt to 0 under the current key."""
        if self.p + 4 > len(self.d):
            return False
        return struct.unpack_from("<I", self.d, self.p)[0] == self.key

    def read_int(self):
        raw = self.d[self.p:self.p + 4]
        v = struct.unpack("<I", raw)[0]
        self.p += 4
        ret = v ^ self.key
        self._advance(raw)
        return ret & 0xFFFFFFFF

    def read_byte(self):
        raw = self.d[self.p:self.p + 1]
        v = raw[0]
        self.p += 1
        ret = (v ^ self.key) & 0xFF
        self._advance(raw)
        return ret

    def read_float(self):
        return struct.unpack("<f", struct.pack("<I", self.read_int()))[0]

    def read_string(self):
        n = self.read_int()
        if n > 4096:
            raise ValueError(f"string length {n} implausible at 0x{self.p:x}")
        return bytes(self.read_byte() for _ in range(n)).decode("latin-1")

    def read_wstring(self):
        n = self.read_int()
        if n > 4096:
            raise ValueError(f"wstring length {n} implausible at 0x{self.p:x}")
        out = []
        for _ in range(n):
            lo = self.read_byte()
            hi = self.read_byte()
            out.append(chr(lo | (hi << 8)))
        return "".join(out)

    def read_uid(self):
        return bytes(self.read_byte() for _ in range(16)).hex()

    # --- blocks ---------------------------------------------------------
    def block_start(self):
        bid = self.read_int()
        blen = self.next_int()
        return bid, blen, self.p + blen

    def block_end(self, end, label):
        if self.p != end:
            raise ValueError(
                f"{label}: cursor 0x{self.p:x} != block end 0x{end:x} "
                f"(delta {self.p - end:+d})")
        if self.next_int() != 0:
            raise ValueError(f"{label}: end-of-block sentinel non-zero")

    def expect_version(self, got, want, label):
        if got != want:
            self.notes.append(
                f"VERSION DRIFT: {label} version={got} (reference expects {want})")
        return got

    def resync_to(self, end, label):
        """Replay key over the unparsed span, then validate the sentinel."""
        span = self.d[self.p:end]
        self._advance(span)
        self.p = end
        ok = self.peek_key_sync()
        self.next_int()
        self.notes.append(
            f"RESYNC after {label}: skipped {len(span)} bytes, "
            f"sentinel {'OK' if ok else 'FAILED'}")
        return ok


def read_item(r):
    it = {
        "baseName": r.read_string(),
        "prefixName": r.read_string(),
        "suffixName": r.read_string(),
        "modifierName": r.read_string(),
        "transmuteName": r.read_string(),
    }
    it["seed"] = r.read_int()
    it["componentName"] = r.read_string()
    it["relicBonus"] = r.read_string()
    it["componentSeed"] = r.read_int()
    it["augmentName"] = r.read_string()
    it["unknown"] = r.read_int()
    it["augmentSeed"] = r.read_int()
    it["var1"] = r.read_int()
    it["stackCount"] = r.read_int()
    # inventory v11 (Edition-II / FoA) drift: four additional 4-byte words per
    # item, not present in the 1.1.9.1 reference. Solved by brute force against
    # the block-end + sentinel oracle (see solve_inventory.py). Their exact slot
    # between transmuteName and end-of-struct is UNDETERMINED for this save --
    # every intervening field is zero here, so five placements parse identically.
    # Observed value in every item: [0, 1, 0, 0]. Names unknown.
    it["_v11_extra"] = [r.read_int() for _ in range(4)]
    return it


def read_equipment(r):
    it = read_item(r)
    it["attached"] = r.read_byte()
    return it


def parse(path, stop_before=None):
    """If stop_before is a block name, return the Reader parked just after that
    block's id/length words and version int -- i.e. at its first content byte.
    Used by the layout-solver scripts to reach a drifted block with correct key
    state without duplicating the preceding sequence."""
    with open(path, "rb") as f:
        data = f.read()
    r = Reader(data)
    out = {"file_size": len(data), "blocks": {}, "offsets": {}, "notes": r.notes}

    r.read_key()
    magic = r.read_int()
    out["magic_ok"] = (magic == MAGIC)
    if not out["magic_ok"]:
        raise SystemExit(f"bad magic 0x{magic:08x}")
    r.expect_version(r.read_int(), 2, "file.preheader")

    # --- header (not a block) ---
    off = r.p
    hdr = {
        "name": r.read_wstring(),
        "sex": r.read_byte(),
        "tag": r.read_string(),
        "level": r.read_int(),
        "hardcore": r.read_byte(),
    }
    hdr["_offset"] = f"0x{off:x}"
    out["header"] = hdr

    b3 = r.read_byte()
    if b3 != 3:
        r.notes.append(f"post-header byte = {b3} (expected 3)")
    z = r.next_int()
    if z != 0:
        r.notes.append(f"post-header next_int = {z} (expected 0)")
    out["file_version"] = r.expect_version(r.read_int(), 8, "gdc_file")

    out["offsets"]["uid"] = f"0x{r.p:x}"
    out["uid"] = r.read_uid()

    # --- top-level blocks, banked individually ---
    plan = [
        ("character_info", 1, 5, blk_character_info),
        ("character_bio", 2, 8, blk_character_bio),
        ("inventory", 3, 4, blk_inventory),
        ("character_stash", 4, 6, blk_stash),
        ("respawn_list", 5, 1, blk_uidlists(3, True)),
        ("teleport_list", 6, 1, blk_uidlists(3, False)),
        ("marker_list", 7, 1, blk_uidlists(3, False)),
        ("shrine_list", 17, 2, blk_uidlists(6, False)),
        ("character_skills", 8, 5, blk_skills),
        ("lore_notes", 12, 1, blk_lore),
        ("faction_pack", 13, 5, blk_factions),
        ("ui_settings", 14, 5, blk_ui),
        ("tutorial_pages", 15, 1, blk_tutorial),
        ("play_stats", 16, 11, blk_playstats),
        ("trigger_tokens", 10, 2, blk_tokens),
    ]

    for name, want_id, want_ver, fn in plan:
        start = r.p
        try:
            bid, blen, end = r.block_start()
        except Exception as exc:
            r.notes.append(f"FATAL: cannot read block header for {name}: {exc}")
            break
        if bid != want_id:
            r.notes.append(
                f"BLOCK ID MISMATCH at {name}: got {bid}, expected {want_id} "
                f"(offset 0x{start:x}) -- ABORTING sequence")
            break
        out["offsets"][name] = f"0x{start:x}"
        if name == stop_before:
            return r, bid, blen, end
        try:
            ver = r.expect_version(r.read_int(), want_ver, name)
            res = fn(r, end)
            res["_version"] = ver
            r.block_end(end, name)
            out["blocks"][name] = res
        except Exception as exc:
            r.notes.append(f"BLOCK FAILED: {name}: {type(exc).__name__}: {exc}")
            if not r.resync_to(end, name):
                r.notes.append("resync failed -- stopping")
                break

    out["trailing_bytes"] = len(data) - r.p
    return out


def blk_character_info(r, end):
    d = {}
    d["isInMainQuest"] = r.read_byte()
    d["hasBeenInGame"] = r.read_byte()
    d["difficulty"] = r.read_byte()
    d["greatestDifficulty"] = r.read_byte()
    d["money"] = r.read_int()
    d["greatestSurvivalDifficulty"] = r.read_byte()
    d["currentTribute"] = r.read_int()
    d["compassState"] = r.read_byte()
    d["skillWindowShowHelp"] = r.read_byte()
    d["weaponSwapActive"] = r.read_byte()
    d["weaponSwapEnabled"] = r.read_byte()
    d["texture"] = r.read_string()
    d["unknown"] = r.read_int()
    d["lootMode_bytes_consumed"] = 0
    n = 0
    while r.p < end:
        r.read_byte()
        n += 1
    d["lootMode_bytes_consumed"] = n
    return d


def blk_character_bio(r, end):
    d = {}
    d["_field_offsets"] = {}
    for f in ("level", "experience", "attributePointsUnspent", "skillPointsUnspent",
              "devotionPointsUnspent", "totalDevotionUnlocked"):
        d["_field_offsets"][f] = f"0x{r.p:x}"
        d[f] = r.read_int()
    for f in ("physique", "cunning", "spirit", "health", "energy"):
        d["_field_offsets"][f] = f"0x{r.p:x}"
        d[f] = r.read_float()
    return d


def blk_inventory(r, end):
    d = {"sacks": [], "equipment": [], "weapon1": [], "weapon2": []}
    d["flag"] = r.read_byte()
    if d["flag"]:
        d["numBags"] = r.read_int()
        d["focused"] = r.read_int()
        d["selected"] = r.read_int()
        for _ in range(d["numBags"]):
            bid, blen, sack_end = r.block_start()
            tempBool = r.read_byte()
            n = r.read_int()
            items = [dict(read_item(r), x=r.read_int(), y=r.read_int()) for _ in range(n)]
            r.block_end(sack_end, "inventory_sack")
            d["sacks"].append({"tempBool": tempBool, "items": items})
        d["useAlternate"] = r.read_byte()
        for i in range(12):
            off = r.p
            e = read_equipment(r)
            e["_slot"] = i
            e["_offset"] = f"0x{off:x}"
            d["equipment"].append(e)
        d["alternate1"] = r.read_byte()
        for i in range(2):
            off = r.p
            e = read_equipment(r)
            e["_slot"] = i
            e["_offset"] = f"0x{off:x}"
            d["weapon1"].append(e)
        d["alternate2"] = r.read_byte()
        for i in range(2):
            off = r.p
            e = read_equipment(r)
            e["_slot"] = i
            e["_offset"] = f"0x{off:x}"
            d["weapon2"].append(e)
    return d


def blk_stash(r, end):
    d = {"tabs": []}
    d["stashTabsPurchased"] = r.read_int()
    for _ in range(d["stashTabsPurchased"]):
        bid, blen, tab_end = r.block_start()
        w = r.read_int()
        h = r.read_int()
        n = r.read_int()
        items = [dict(read_item(r), x=r.read_float(), y=r.read_float()) for _ in range(n)]
        # stash_tab v11 drift: trailing fields absent from the 1.1.9.1 reference.
        # Drained rather than guessed; values recorded so the drift is visible.
        tail = []
        while r.p + 4 <= tab_end:
            tail.append(r.read_int())
        while r.p < tab_end:
            tail.append(r.read_byte())
        if tail:
            r.notes.append(f"stash_tab v11: {len(tail)} trailing word(s) drained: {tail}")
        r.block_end(tab_end, "stash_tab")
        d["tabs"].append({"width": w, "height": h, "items": items, "_tail": tail})
    return d


def blk_uidlists(count, with_spawn):
    def fn(r, end):
        d = {"uids": []}
        for _ in range(count):
            n = r.read_int()
            d["uids"].append([r.read_uid() for _ in range(n)])
        if with_spawn:
            d["spawn"] = [r.read_uid() for _ in range(3)]
        return d
    return fn


def blk_skills(r, end):
    d = {"skills": [], "itemSkills": []}
    n = r.read_int()
    for _ in range(n):
        off = r.p
        s = {"_offset": f"0x{off:x}", "name": r.read_string()}
        s["level"] = r.read_int()
        s["enabled"] = r.read_byte()
        # character_skills v8 (Edition-II / FoA) drift: exactly one byte added
        # to the skill struct, positioned between `enabled` and `devotionLevel`.
        # Placement fixed empirically -- of the five ways to distribute the
        # 4 byte-fields around the 3 int-fields, only this one makes all
        # 62x3 = 186 int fields read as 0; every other placement yields
        # uniformly random values. See solve_skills.py.
        s["_v8_newbyte"] = r.read_byte()
        s["devotionLevel"] = r.read_int()
        s["experience"] = r.read_int()
        s["active"] = r.read_int()
        s["unknown1"] = r.read_byte()
        s["unknown2"] = r.read_byte()
        s["autoCastSkill"] = r.read_string()
        s["autoCastController"] = r.read_string()
        d["skills"].append(s)
    d["masteriesAllowed"] = r.read_int()
    d["skillReclamationPointsUsed"] = r.read_int()
    d["_devotionReclamation_offset"] = f"0x{r.p:x}"
    d["devotionReclamationPointsUsed"] = r.read_int()
    # v8 adds one further word here; all three trailing words read 0, so the
    # exact ordering is undetermined but devotionReclamationPointsUsed == 0
    # holds under every candidate ordering.
    d["_v8_trailing"] = r.read_int()
    m = r.read_int()
    for _ in range(m):
        d["itemSkills"].append({
            "name": r.read_string(),
            "autoCastSkill": r.read_string(),
            "autoCastController": r.read_string(),
            "itemSlot": r.read_int(),
            "itemName": r.read_string(),
        })
    return d


def blk_lore(r, end):
    n = r.read_int()
    return {"names": [r.read_string() for _ in range(n)]}


def blk_factions(r, end):
    d = {"faction": r.read_int(), "factions": []}
    n = r.read_int()
    for _ in range(n):
        d["factions"].append({
            "modified": r.read_byte(), "unlocked": r.read_byte(),
            "value": r.read_float(), "positiveBoost": r.read_float(),
            "negativeBoost": r.read_float(),
        })
    return d


def blk_ui(r, end):
    d = {"slots": []}
    d["unknown1"] = r.read_byte()
    d["unknown2"] = r.read_int()
    d["unknown3"] = r.read_byte()
    for _ in range(5):
        r.read_string()
        r.read_string()
        r.read_byte()
    for i in range(46):
        t = r.read_int()
        slot = {"slot": i, "type": t}
        if t == 0:
            slot["skill"] = r.read_string()
            slot["isItemSkill"] = r.read_byte()
            slot["item"] = r.read_string()
            slot["equipLocation"] = r.read_int()
        elif t == 4:
            slot["item"] = r.read_string()
            slot["bitmapUp"] = r.read_string()
            slot["bitmapDown"] = r.read_string()
            slot["label"] = r.read_wstring()
        d["slots"].append(slot)
    d["cameraDistance"] = r.read_float()
    return d


def blk_tutorial(r, end):
    n = r.read_int()
    return {"pages": [r.read_int() for _ in range(n)]}


def blk_playstats(r, end):
    d = {"_field_offsets": {}}

    def i32(name):
        d["_field_offsets"][name] = f"0x{r.p:x}"
        d[name] = r.read_int()

    def f32(name):
        d["_field_offsets"][name] = f"0x{r.p:x}"
        d[name] = r.read_float()

    for f in ("playTime", "deaths", "kills", "experienceFromKills",
              "healthPotionsUsed", "manaPotionsUsed", "maxLevel",
              "hitsReceived", "hitsInflicted", "criticalHitsInflicted",
              "criticalHitsReceived"):
        i32(f)
    f32("greatestDamageInflicted")
    d["perDifficulty"] = []
    for _ in range(3):
        d["perDifficulty"].append({
            "greatestMonsterKilledName": r.read_string(),
            "greatestMonsterKilledLevel": r.read_int(),
            "greatestMonsterKilledLifeAndMana": r.read_int(),
            "lastMonsterHit": r.read_string(),
            "lastMonsterHitBy": r.read_string(),
        })
    i32("championKills")
    f32("lastHit")
    f32("lastHitBy")
    f32("greatestDamageReceived")
    for f in ("heroKills", "itemsCrafted", "relicsCrafted",
              "transcendentRelicsCrafted", "mythicalRelicsCrafted",
              "shrinesRestored", "oneShotChestsOpened", "loreNotesCollected"):
        i32(f)
    d["bossKills"] = [r.read_int() for _ in range(3)]
    for f in ("survivalWaveTier", "greatestSurvivalScore",
              "cooldownRemaining", "cooldownTotal"):
        i32(f)
    d["_field_offsets"]["v"] = f"0x{r.p:x}"
    vn = r.read_int()
    d["v_length"] = vn
    d["v"] = [{"str": r.read_string(), "num": r.read_int()} for _ in range(vn)]
    for f in ("shatteredRealmSouls", "shatteredRealmEssence"):
        i32(f)
    d["difficultySkip"] = r.read_byte()
    d["tail"] = []
    while r.p + 4 <= end:
        d["tail"].append(r.read_int())
    while r.p < end:
        d["tail"].append(r.read_byte())
    return d


def blk_tokens(r, end):
    d = {"tokens": []}
    for _ in range(3):
        n = r.read_int()
        d["tokens"].append([r.read_string() for _ in range(n)])
    return d


if __name__ == "__main__":
    result = parse(sys.argv[1])
    json.dump(result, open(sys.argv[2], "w"), indent=1)
    print(f"notes ({len(result['notes'])}):")
    for n in result["notes"]:
        print("  " + n)
    print("blocks parsed:", ", ".join(result["blocks"].keys()))
    print("trailing bytes:", result["trailing_bytes"])
