#!/usr/bin/env python3
"""
gdc_read.py — READ-ONLY Grim Dawn player.gdc parser.

Lap MD-B4app-2d (KC2 MODEL-COMPLETION run). Purpose: recover the hot-bar
bindings (block 14 `ui_settings`) plus skill ranks (block 8) and playtime
(block 16) from Matt's referent EoR-Warlord save.

Format reference: AaronHutchinson/Grim-Dawn-Save-Decryption (decrypt-player.cpp),
mapped in agentic_orchestration/legolas/notes/2026-07-28-gd-gdc-save-probe.md § 3.

NO WRITE PATH EXISTS IN THIS FILE. It opens files 'rb' and never writes bytes.

Per probe § 4 mitigation 1: version asserts are LOGGED, not thrown. The
block-length + end-sentinel machinery is the real integrity check and stays ON.
Per mitigation 2: blocks are banked as they complete, so a late drift does not
cost the early reads.
"""

import json
import struct
import sys


class Reader:
    def __init__(self, data):
        self.d = data
        self.p = 0
        self.key = 0
        self.table = []
        self.version_notes = []
        self._read_key()

    # ---- cipher -------------------------------------------------------
    def _read_key(self):
        k = struct.unpack_from("<I", self.d, 0)[0]
        self.p = 4
        k ^= 0x55555555
        self.key = k
        t = []
        for _ in range(256):
            k = ((k >> 1) | (k << 31)) & 0xFFFFFFFF
            k = (k * 39916801) & 0xFFFFFFFF
            t.append(k)
        self.table = t

    def _advance(self, raw_bytes):
        for b in raw_bytes:
            self.key ^= self.table[b]

    # ---- primitives ---------------------------------------------------
    def next_int(self):
        """4 bytes, XOR with key, key NOT advanced. Block lengths + sentinels."""
        raw = struct.unpack_from("<I", self.d, self.p)[0]
        self.p += 4
        return raw ^ self.key

    def read_int(self):
        raw = self.d[self.p:self.p + 4]
        self.p += 4
        val = struct.unpack("<I", raw)[0] ^ self.key
        self._advance(raw)
        return val

    def read_byte(self):
        raw = self.d[self.p:self.p + 1]
        self.p += 1
        val = raw[0] ^ (self.key & 0xFF)
        self._advance(raw)
        return val

    def read_float(self):
        return struct.unpack("<f", struct.pack("<I", self.read_int()))[0]

    def read_str(self):
        n = self.read_int()
        if n > 0x100000:
            raise ValueError("implausible string length %d at 0x%x" % (n, self.p))
        return "".join(chr(self.read_byte()) for _ in range(n))

    def read_wstr(self):
        n = self.read_int()
        if n > 0x100000:
            raise ValueError("implausible wstring length %d at 0x%x" % (n, self.p))
        out = []
        for _ in range(n):
            c = self.read_byte()
            c |= self.read_byte() << 8
            out.append(chr(c))
        return "".join(out)

    # ---- blocks -------------------------------------------------------
    def block_start(self, expect_id, name):
        bid = self.read_int()
        blen = self.next_int()
        end = self.p + blen
        if bid != expect_id:
            raise ValueError("%s: block id %d != expected %d" % (name, bid, expect_id))
        return {"id": bid, "end": end, "name": name}

    def block_end(self, b):
        if self.p != b["end"]:
            raise ValueError("%s: cursor 0x%x != block end 0x%x (delta %d)"
                             % (b["name"], self.p, b["end"], self.p - b["end"]))
        sent = self.next_int()
        if sent != 0:
            raise ValueError("%s: end sentinel %d != 0" % (b["name"], sent))

    def seek_block(self, pos, block_id, name):
        """Re-synchronise at a known block boundary.

        The key is RECOVERABLE at every block start without having parsed
        anything before it: the first word of a block is `read_int()` of the
        block ID, which is KNOWN PLAINTEXT, so key = ciphertext XOR id. This
        makes every block independently readable and lets a version-drifted
        block (e.g. Fangs-era `inventory`) be skipped rather than guessed at.
        """
        raw = self.d[pos:pos + 4]
        self.key = struct.unpack("<I", raw)[0] ^ block_id
        self.p = pos + 4
        self._advance(raw)
        blen = self.next_int()
        return {"id": block_id, "end": self.p + blen, "name": name, "len": blen}

    def version(self, name, expected):
        v = self.read_int()
        if v != expected:
            self.version_notes.append(
                {"block": name, "observed": v, "reference_expected": expected})
        return v

    # ---- composites ---------------------------------------------------
    def read_item(self):
        it = {
            "baseName": self.read_str(),
            "prefixName": self.read_str(),
            "suffixName": self.read_str(),
            "modifierName": self.read_str(),
            "transmuteName": self.read_str(),
        }
        it["seed"] = self.read_int()
        it["componentName"] = self.read_str()
        it["relicBonus"] = self.read_str()
        it["componentSeed"] = self.read_int()
        it["augmentName"] = self.read_str()
        it["unknown"] = self.read_int()
        it["augmentSeed"] = self.read_int()
        it["var1"] = self.read_int()
        it["stackCount"] = self.read_int()
        return it

    def read_hot_slot(self):
        s = {"type": self.read_int()}
        if s["type"] == 0:
            s["skill"] = self.read_str()
            s["isItemSkill"] = self.read_byte()
            s["item"] = self.read_str()
            s["equipLocation"] = self.read_int()
        elif s["type"] == 4:
            s["item"] = self.read_str()
            s["bitmapUp"] = self.read_str()
            s["bitmapDown"] = self.read_str()
            s["label"] = self.read_wstr()
        return s


# slot index -> screen position, per decrypt-player.cpp hot_slot::read comment
SLOT_POSITION = {}
for i in range(10):
    SLOT_POSITION[i] = "primary action bar #%d" % (i + 1)
SLOT_POSITION[10] = "weapon-set-1 LEFT click"
SLOT_POSITION[11] = "weapon-set-2 LEFT click"
SLOT_POSITION[12] = "weapon-set-1 RIGHT click"
SLOT_POSITION[13] = "weapon-set-2 RIGHT click"
for i in range(14, 24):
    SLOT_POSITION[i] = "secondary action bar #%d" % (i - 13)
SLOT_POSITION[24] = "health potion"
SLOT_POSITION[25] = "energy potion"
SLOT_POSITION[26] = "stationary attack (?)"

TYPE_NAME = {0: "skill", 2: "health potion", 3: "energy potion",
             4: "item", 0xFFFFFFFF: "EMPTY"}


def parse(path):
    data = open(path, "rb").read()
    r = Reader(data)
    out = {"file": path, "size": len(data), "blocks_ok": [], "error": None}

    magic = r.read_int()
    out["magic_ok"] = (magic == 0x58434447)
    r.read_int()                      # constant 2
    out["name"] = r.read_wstr()
    out["sex"] = r.read_byte()
    out["tag"] = r.read_str()
    out["level_header"] = r.read_int()
    out["hardcore"] = r.read_byte()
    r.read_byte()                     # constant 3
    r.next_int()                      # constant 0
    out["file_version"] = r.read_int()

    try:
        out["uid"] = "".join("%02x" % r.read_byte() for _ in range(16))
        out["blocks_ok"].append("uid")

        b = r.block_start(1, "character_info")
        r.version("character_info", 5)
        info = {}
        info["isInMainQuest"] = r.read_byte()
        info["hasBeenInGame"] = r.read_byte()
        info["difficulty"] = r.read_byte()
        info["greatestDifficulty"] = r.read_byte()
        info["money"] = r.read_int()
        info["greatestSurvivalDifficulty"] = r.read_byte()
        info["currentTribute"] = r.read_int()
        info["compassState"] = r.read_byte()
        info["skillWindowShowHelp"] = r.read_byte()
        info["weaponSwapActive"] = r.read_byte()
        info["weaponSwapEnabled"] = r.read_byte()
        info["texture"] = r.read_str()
        r.read_int()
        # Reference reads exactly 39 loot-filter bytes (GD 1.1.9.1). Newer builds
        # append filter options without bumping the block version, so size this
        # from the block length rather than from the reference constant. The
        # end-sentinel check below still proves the read landed correctly.
        info["lootMode"] = [r.read_byte() for _ in range(b["end"] - r.p)]
        info["lootMode_count"] = len(info["lootMode"])
        r.block_end(b)
        out["character_info"] = info
        out["blocks_ok"].append("character_info")

        b = r.block_start(2, "character_bio")
        r.version("character_bio", 8)
        bio = {}
        for f in ("level", "experience", "attributePointsUnspent",
                  "skillPointsUnspent", "devotionPointsUnspent",
                  "totalDevotionUnlocked"):
            bio[f] = r.read_int()
        for f in ("physique", "cunning", "spirit", "health", "energy"):
            bio[f] = r.read_float()
        r.block_end(b)
        out["character_bio"] = bio
        out["blocks_ok"].append("character_bio")

        b = r.block_start(3, "inventory")
        r.version("inventory", 4)
        inv = {}
        flag = r.read_byte()
        inv["flag"] = flag
        if flag:
            numBags = r.read_int()
            inv["numBags"] = numBags
            r.read_int()  # focused
            r.read_int()  # selected
            inv["sacks"] = []
            for _ in range(numBags):
                sb = r.block_start(0, "inventory_sack")
                r.read_byte()
                n = r.read_int()
                sack = []
                for _ in range(n):
                    it = r.read_item()
                    it["x"] = r.read_int()
                    it["y"] = r.read_int()
                    sack.append(it)
                r.block_end(sb)
                inv["sacks"].append(sack)
            r.read_byte()  # useAlternate
            eq = []
            for _ in range(12):
                it = r.read_item()
                it["attached"] = r.read_byte()
                eq.append(it)
            inv["equipment"] = eq
            r.read_byte()
            w1 = []
            for _ in range(2):
                it = r.read_item()
                it["attached"] = r.read_byte()
                w1.append(it)
            inv["weapon1"] = w1
            r.read_byte()
            w2 = []
            for _ in range(2):
                it = r.read_item()
                it["attached"] = r.read_byte()
                w2.append(it)
            inv["weapon2"] = w2
        r.block_end(b)
        out["inventory"] = inv
        out["blocks_ok"].append("inventory")

        b = r.block_start(4, "character_stash")
        r.version("character_stash", 6)
        ntabs = r.read_int()
        out["stashTabsPurchased"] = ntabs
        for _ in range(ntabs):
            tb = r.block_start(0, "stash_tab")
            r.read_int()
            r.read_int()
            n = r.read_int()
            for _ in range(n):
                r.read_item()
                r.read_float()
                r.read_float()
            r.block_end(tb)
        r.block_end(b)
        out["blocks_ok"].append("character_stash")

        for bid, name, ver, nuid in ((5, "respawn_list", 1, 6),
                                     (6, "teleport_list", 1, 3),
                                     (7, "marker_list", 1, 3),
                                     (17, "shrine_list", 2, 6)):
            b = r.block_start(bid, name)
            r.version(name, ver)
            if name == "respawn_list":
                for _ in range(3):
                    n = r.read_int()
                    for _ in range(n):
                        for _ in range(16):
                            r.read_byte()
                for _ in range(3):
                    r.read_str()
            else:
                for _ in range(nuid):
                    n = r.read_int()
                    for _ in range(n):
                        for _ in range(16):
                            r.read_byte()
            r.block_end(b)
            out["blocks_ok"].append(name)

        b = r.block_start(8, "character_skills")
        r.version("character_skills", 5)
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
        itemSkills = []
        for _ in range(n):
            isk = {"name": r.read_str(), "autoCastSkill": r.read_str(),
                   "autoCastController": r.read_str(),
                   "itemSlot": r.read_int(), "itemName": r.read_str()}
            itemSkills.append(isk)
        out["itemSkills"] = itemSkills
        r.block_end(b)
        out["blocks_ok"].append("character_skills")

        b = r.block_start(12, "lore_notes")
        r.version("lore_notes", 1)
        n = r.read_int()
        for _ in range(n):
            r.read_str()
        r.block_end(b)
        out["blocks_ok"].append("lore_notes")

        b = r.block_start(13, "faction_pack")
        r.version("faction_pack", 5)
        r.read_int()
        n = r.read_int()
        for _ in range(n):
            r.read_byte()
            r.read_byte()
            r.read_float()
            r.read_float()
            r.read_float()
        r.block_end(b)
        out["blocks_ok"].append("faction_pack")

        # ---- THE TARGET -------------------------------------------------
        b = r.block_start(14, "ui_settings")
        r.version("ui_settings", 5)
        ui = {}
        ui["unknown1"] = r.read_byte()
        ui["unknown2"] = r.read_int()
        ui["unknown3"] = r.read_byte()
        ui["unknown45"] = []
        for _ in range(5):
            ui["unknown45"].append([r.read_str(), r.read_str(), r.read_byte()])
        slots = []
        for i in range(46):
            s = r.read_hot_slot()
            s["index"] = i
            s["position"] = SLOT_POSITION.get(i, "unmapped index %d" % i)
            s["type_name"] = TYPE_NAME.get(s["type"], "type=%d" % s["type"])
            slots.append(s)
        ui["slots"] = slots
        ui["cameraDistance"] = r.read_float()
        r.block_end(b)
        out["ui_settings"] = ui
        out["blocks_ok"].append("ui_settings")

        b = r.block_start(15, "tutorial_pages")
        r.version("tutorial_pages", 1)
        n = r.read_int()
        for _ in range(n):
            r.read_int()
        r.block_end(b)
        out["blocks_ok"].append("tutorial_pages")

        b = r.block_start(16, "play_stats")
        r.version("play_stats", 11)
        ps = {}
        for f in ("playTime", "deaths", "kills", "experienceFromKills",
                  "healthPotionsUsed", "manaPotionsUsed", "maxLevel",
                  "hitsReceived", "hitsInflicted", "criticalHitsInflicted",
                  "criticalHitsReceived"):
            ps[f] = r.read_int()
        ps["greatestDamageInflicted"] = r.read_float()
        ps["perDifficulty"] = []
        for _ in range(3):
            row = {"greatestMonsterKilledName": r.read_str(),
                   "greatestMonsterKilledLevel": r.read_int(),
                   "greatestMonsterKilledLifeAndMana": r.read_int(),
                   "lastMonsterHit": r.read_str(),
                   "lastMonsterHitBy": r.read_str()}
            ps["perDifficulty"].append(row)
        ps["championKills"] = r.read_int()
        ps["lastHit"] = r.read_float()
        ps["lastHitBy"] = r.read_float()
        ps["greatestDamageReceived"] = r.read_float()
        for f in ("heroKills", "itemsCrafted", "relicsCrafted",
                  "transcendentRelicsCrafted", "mythicalRelicsCrafted",
                  "shrinesRestored", "oneShotChestsOpened",
                  "loreNotesCollected"):
            ps[f] = r.read_int()
        ps["bossKills"] = [r.read_int() for _ in range(3)]
        ps["survivalWaveTier"] = r.read_int()
        ps["greatestSurvivalScore"] = r.read_int()
        ps["cooldownRemaining"] = r.read_int()
        ps["cooldownTotal"] = r.read_int()
        n = r.read_int()
        ps["v"] = [[r.read_str(), r.read_int()] for _ in range(n)]
        ps["shatteredRealmSouls"] = r.read_int()
        ps["shatteredRealmEssence"] = r.read_int()
        ps["difficultySkip"] = r.read_byte()
        r.read_int()
        r.read_int()
        r.block_end(b)
        out["play_stats"] = ps
        out["blocks_ok"].append("play_stats")

        b = r.block_start(10, "trigger_tokens")
        r.version("trigger_tokens", 2)
        for _ in range(3):
            n = r.read_int()
            for _ in range(n):
                r.read_str()
        r.block_end(b)
        out["blocks_ok"].append("trigger_tokens")

        out["eof_clean"] = (r.p == len(data))
    except Exception as exc:  # bank what completed; never improvise past it
        out["error"] = "%s: %s (cursor 0x%x)" % (type(exc).__name__, exc, r.p)

    out["version_drift"] = r.version_notes
    return out


if __name__ == "__main__":
    for path in sys.argv[1:]:
        res = parse(path)
        print(json.dumps(res, indent=1, ensure_ascii=False))
