#!/usr/bin/env python3
"""KC2-PM4 Lap G shared library -- THE PLAYER'S OWN KIT (I-2 / I-3 substrate).

READ-ONLY on the vendor corpus, on `/Volumes/reincarnated/`, and on every prior lap's emission.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE QUESTION (charter L-6, Lap G)
═══════════════════════════════════════════════════════════════════════════════════════════════

T4b -- the terminal mechanism -- has MISSED twice and is unreachable by any board-side fold.  The
sim's player models the EoR channel ONLY: no movement skill, no secondary actives, no potions, no
circuit-breaker.  On wave 160 he walks into 20,861 damage in 6.69 s with ZERO player damage rows
and zero counterplay.  Matt's testimony (PM-2 L-10, banked): he *"did ALOT of dashing"*, used the
build-guide skills, played with potions, and died to poison/DoT *"in a major way."*

This lap decodes the PLAYER SIDE.  Five questions, all MEASURED or explicitly DECLARED (GL-12).

═══════════════════════════════════════════════════════════════════════════════════════════════
⚑ G0 -- THE SOURCE MOVED.  Lap A read the PRISTINE download; this lap reads the SAVE MATT PLAYED
═══════════════════════════════════════════════════════════════════════════════════════════════

Lap A (2026-08-12) parsed `gdc/_EoRWarlGuts/player.gdc` (sha256 `c8738da3…`) -- the 2022 forum
download, extracted from the pristine zip, BEFORE first load.  It is v1.1.9-era.

**Matt's actually-played save exists on the share and had never been read.**  Two byte-identical
copies:

    /Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc
    /Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/player.gdc
    sha256  b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5   98,101 bytes

It is the migrated, played, 1.3.0.0-era file (`expansion_status = 7` = AoM|FG|FoA, against the
pristine's `3` = AoM|FG).  **The played save is the source of record for "the kit as PLAYED"; the
pristine is retained as the CROSS-CHECK.**  Both are parsed by this lap and diffed field by field.

═══════════════════════════════════════════════════════════════════════════════════════════════
⚑ G1 -- LAP A's CLIFF C-3 BIT, AND IS NOW CLOSED.  The real .gdc stream cipher, decoded here
═══════════════════════════════════════════════════════════════════════════════════════════════

Lap A's parser handled only the PLAINTEXT case: the pristine file's seed *is* `0x55555555`, so
`seed ^ 0x55555555 == 0`, the key table is all zeros, and the XOR stream is the identity.  Lap A
named this as cliff C-3 and did not implement the real schedule because it was not needed.

**The played save's seed is `0x5298565B`.  The cliff bit.**  The schedule, established here from
first principles against the file (never spelled from memory, every step falsified against the
bytes):

    seed  = uint32 @0  XOR  0x55555555
    key   = seed
    table[i] for i in 0..255:      k = rotate_right_1(k) ;  k = (k * 39916801) mod 2^32
                                   table[i] = k                      # ONE round per entry
    read_u8 :  v = raw   ^ (key & 0xFF) ;  key ^= table[raw]
    read_u32:  v = raw32 ^  key         ;  key ^= table[b] for each of the 4 RAW bytes

  ⚑ THE ROUND COUNT WAS MEASURED, NOT ASSUMED.  4 candidate schedules (1/2/3/4 rotate+multiply
    rounds per table entry) were run; all four decode the magic (the first int uses the initial
    key, so the table is irrelevant there), but only **rounds = 1** decodes `header_version = 2`
    and the wide-string name `EoRWarlGuts`.  The other three desync inside the name length.

  ⚑ THREE POSITIONS CONSUME BYTES WITHOUT UPDATING THE KEY.  Found by solving, not by guessing:
    the key error `D = true_key XOR my_key` is CONSTANT once introduced (both sides update by the
    same `^= table[raw]`), so a run of known plaintext pins `D` exactly.  A 16-byte run of zeros
    at file offset 78..93 decoded to a constant `0xd8`, which pins `D`; searching every 1/4/5/8
    byte window in 64..78 for `XOR table[b] == D` returned EXACTLY ONE candidate: **bytes 70..73.**
    That is the post-header `uint32` (Lap A's plaintext read called it `expansion_status`; it is
    really `expansion_status` as a BYTE at 69 followed by a raw-read `uint32`).  The same rule
    then holds for **block lengths** and **block end-markers**: both consume 4 bytes with NO key
    update.  All three were established by requiring the file to parse to its last byte.

  VERIFICATION, and it is total: with these three rules the played save walks **15/15 blocks,
  every end-marker decodes to 0, and the walk terminates at byte 98,101 of 98,101** -- and the
  SAME code walks the pristine plaintext save to 87,820/87,820 with 15/15 zero markers, so the
  reader is not tuned to one file.

  ⚑ TWO BLOCKS NEED A RESYNC AND THEY NAME THEMSELVES.  Blocks 3 (inventory) and 4 (stash) carry
  NESTED length ints, so a blanket "bump the key over the whole payload" over-bumps.  Because the
  end-marker's plaintext is 0, the TRUE key at the marker is exactly the raw marker bytes -- so
  the walker resyncs there, and reports per block whether the blanket skip was `clean`.  **Blocks
  1, 2, 5, 6, 7, 17, 8, 12, 13, 14, 15, 16, 10 are all `clean = True` on the played save** --
  i.e. every block this lap actually reads (8 = skills, 14 = UI settings) verified its own key
  state independently.  Only 3 and 4 are `clean = False`, and neither is read.

═══════════════════════════════════════════════════════════════════════════════════════════════
⚑ G2 -- BLOCK 14 IS THE HOTBAR, AND THE CORPUS CONFIRMS IT
═══════════════════════════════════════════════════════════════════════════════════════════════

Lap A walked block 14 by (id, length) only.  It is the UI-settings block.  Two independent
confirmations, neither of them assumed:

  (a) it carries exactly the skill records a player binds, in a fixed array, with an item-skill
      flag and an equip-location index;
  (b) its LAST four bytes on the pristine save decode to the float **48.0**, and
      `records/game/gameengine.dbr : CameraDistanceMax = 48.0`.  The block ends with the camera
      zoom setting.  That is a UI-settings block.

  ⚑ WHAT THIS LAP DOES **NOT** CLAIM.  The per-slot trailer is NOT a fixed-width record: it is
  13 bytes on most entries but 17 or 21 on others (`ascension1`, `eyeofreckoning1`, the rune),
  with runs of `0xFFFFFFFF` whose length varies per entry.  Four fixed-grammar hypotheses were
  built and all four were falsified against those trailers.  **Therefore the mapping
  ordinal -> physical key / mouse button is DECLARED-GAP.**  What IS emitted is directly read and
  is not in dispute: the skill record, the array ORDINAL, the item-skill byte, the item record,
  and the equip-location int.  (`14` = medal on the rune, `11` = relic on the relic skill, `10` =
  the component slot -- all three agree with Lap A's independently-recovered equipment array.)

═══════════════════════════════════════════════════════════════════════════════════════════════
⚑ G3 -- THE 1.3.0.0 SKILL-BLOCK LAYOUT GAINED ONE BYTE, AND THE POSITION IS AMBIGUOUS
═══════════════════════════════════════════════════════════════════════════════════════════════

Block 8's per-entry stride after the record path is **27 bytes on the pristine save and 28 on the
played save**.  Every one of the 10 possible insertion points for a single `u8` was tried; exactly
TWO parse all 367 entries with in-range values and land exactly on the item-skill section
(positions 1 and 2 -- i.e. the new byte sits immediately BEFORE or immediately AFTER the existing
`enabled` byte).  They are structurally indistinguishable (two adjacent bytes).  **This lap emits
both as `b1` / `b2` and asserts nothing about which is `enabled`.**  Neither is load-bearing: rank,
devotion level and the autocast pair are unaffected and are read identically under both.

═══════════════════════════════════════════════════════════════════════════════════════════════
UNITS -- inherited from Lap F (R-PM4-7 lineage), not re-derived
═══════════════════════════════════════════════════════════════════════════════════════════════

`resources/Text_EN.arc -> tags_ui.txt : SkillDistanceFormat={%.1f0 {^E}Meter %s1}` -- the game
prints a RAW DB length followed by the literal word "Meter", no conversion factor.  One DB length
unit IS one metre.  The sim already rides this identity twice unconverted
(`meleeTargetDistance 2.4 -> D_ENGAGE_M`, EoR `skillTargetRadius 3.0 -> EOR_RADIUS_M`).
Times are seconds (`skill_activated.tpl : skillCooldownTime  desc="Seconds"`).  Sim tick =
0.08163 s.  **Nothing in this lap is rescaled.**

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap G.
"""
from __future__ import annotations

import csv
import hashlib
import pathlib
import re
import struct
import sys
from typing import Dict, List, Optional, Sequence, Tuple

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")

sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4d_lib_2026_08_13 import E3, sha256_of                 # noqa: E402  (the ruled .arz reader)
from pm4f_lib_2026_08_13 import Templates                     # noqa: E402  (templates.arc reader)
from gd_arc_reader_2026_07_26 import ArcArchive               # noqa: E402

# ── THE TWO SAVES ───────────────────────────────────────────────────────────────────────────────
PLAYED_SAVE = pathlib.Path(
    "/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc")
PLAYED_SAVE_MIRROR = pathlib.Path(
    "/Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/player.gdc")
PRISTINE_SAVE = (META / "agentic_orchestration" / "legolas" / "notes"
                 / "2026-08-12-kc2-pm2-lap-a-player-sheet" / "gdc" / "_EoRWarlGuts" / "player.gdc")

LAP_A_SHEET = (META / "agentic_orchestration" / "legolas" / "notes"
               / "2026-08-12-kc2-pm2-lap-a-player-sheet" / "measured-player-sheet.csv")

TEXT_ARCS = ["resources/Text_EN.arc", "gdx1/resources/Text_EN.arc", "gdx2/resources/Text_EN.arc",
             "gdx3/resources/Text_EN.arc", "mods/survivalmode/resources/Text_EN.arc"]

GAMEENGINE = "records/game/gameengine.dbr"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# G1 -- THE .gdc READER
# ══════════════════════════════════════════════════════════════════════════════════════════════

class GDC:
    """Grim Dawn `player.gdc` stream reader.  Handles the plaintext AND obfuscated cases with one
    code path (the plaintext file is just the key==0 degenerate case of the same schedule)."""

    ROUNDS = 1  # MEASURED (see module docstring G1), not assumed

    def __init__(self, buf: bytes) -> None:
        self.b = buf
        seed = (struct.unpack_from("<I", buf, 0)[0] ^ 0x55555555) & 0xFFFFFFFF
        t: List[int] = []
        k = seed
        for _ in range(256):
            for _r in range(self.ROUNDS):
                k = ((k >> 1) | (k << 31)) & 0xFFFFFFFF
                k = (k * 39916801) & 0xFFFFFFFF
            t.append(k)
        self.t = t
        self.key = seed
        self.seed_raw = struct.unpack_from("<I", buf, 0)[0]
        self.p = 4

    def _bump(self, raw: bytes) -> None:
        for by in raw:
            self.key = (self.key ^ self.t[by]) & 0xFFFFFFFF

    def u8(self) -> int:
        raw = self.b[self.p]
        self.p += 1
        v = raw ^ (self.key & 0xFF)
        self.key = (self.key ^ self.t[raw]) & 0xFFFFFFFF
        return v

    def u32(self) -> int:
        raw = self.b[self.p:self.p + 4]
        self.p += 4
        v = (struct.unpack("<I", raw)[0] ^ self.key) & 0xFFFFFFFF
        self._bump(raw)
        return v

    def u32_nobump(self) -> int:
        """Decoded, but the 4 bytes do NOT advance the key.  Block lengths + the header int."""
        raw = self.b[self.p:self.p + 4]
        self.p += 4
        return (struct.unpack("<I", raw)[0] ^ self.key) & 0xFFFFFFFF

    def raw32(self) -> int:
        v = struct.unpack_from("<I", self.b, self.p)[0]
        self.p += 4
        return v

    def f32(self) -> float:
        return struct.unpack("<f", struct.pack("<I", self.u32()))[0]

    def s(self) -> str:
        n = self.u32()
        if n > 4096:
            raise ValueError(f"string length {n} at {self.p}")
        return bytes(self.u8() for _ in range(n)).decode("latin-1")

    def ws(self) -> str:
        n = self.u32()
        if n > 4096:
            raise ValueError(f"wstring length {n} at {self.p}")
        return bytes(self.u8() for _ in range(n * 2)).decode("utf-16-le", "replace")


def parse_header(g: GDC) -> Dict[str, object]:
    h: Dict[str, object] = {}
    h["seed_raw"] = f"0x{g.seed_raw:08X}"
    h["obfuscated"] = g.seed_raw != 0x55555555
    h["magic"] = struct.pack("<I", g.u32()).decode("latin-1")
    if h["magic"] != "GDCX":
        raise ValueError(f"not a GDC file (magic={h['magic']!r})")
    h["header_version"] = g.u32()
    h["name"] = g.ws()
    h["sex"] = g.u8()
    h["class_tag"] = g.s()
    h["level"] = g.u32()
    h["hardcore"] = g.u8()
    h["expansion_status"] = g.u8()          # 3 = AoM|FG (pristine) · 7 = AoM|FG|FoA (played)
    h["post_header_int_raw"] = g.raw32()    # consumed, key NOT advanced -- G1
    h["data_version"] = g.u32()
    h["mystery16"] = bytes(g.u8() for _ in range(16)).hex()
    return h


def walk_blocks(buf: bytes) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    """Walk every block.  Each entry carries the key state at its payload start, so any block can
    be re-read independently.  `clean` says whether the blanket payload skip reproduced the
    block's own zero end-marker (i.e. whether the block contains nested no-bump length ints)."""
    g = GDC(buf)
    h = parse_header(g)
    out: List[Dict[str, object]] = []
    while g.p + 8 <= len(buf):
        bid = g.u32()
        blen = g.u32_nobump()
        if blen == 0 or g.p + blen + 4 > len(buf):
            break
        rec = {"id": bid, "len": blen, "payload": g.p, "key": g.key}
        rawp = buf[g.p:g.p + blen]
        g.p += blen
        g._bump(rawp)
        rawm = buf[g.p:g.p + 4]
        rec["clean"] = ((struct.unpack("<I", rawm)[0] ^ g.key) & 0xFFFFFFFF) == 0
        g.key = struct.unpack("<I", rawm)[0]     # resync on the known-zero marker
        g.p += 4
        out.append(rec)
    h["bytes_walked"] = g.p
    h["bytes_total"] = len(buf)
    return h, out


def reader_at(buf: bytes, blk: Dict[str, object]) -> GDC:
    g = GDC(buf)
    g.p = int(blk["payload"])
    g.key = int(blk["key"])
    return g


def read_skill_block(path: pathlib.Path):
    """Block 8 -- skill + devotion allocation, and the autocast (devotion-proc) bindings."""
    buf = path.read_bytes()
    h, bl = walk_blocks(buf)
    b8 = [b for b in bl if b["id"] == 8][0]
    g = reader_at(buf, b8)
    end = int(b8["payload"]) + int(b8["len"])
    ver = g.u32()
    n = g.u32()
    extra_byte = bool(int(h["expansion_status"]) & 4)     # FoA-era layout -- G3
    rows = []
    for _ in range(n):
        e = {"record": g.s(), "rank_allocated": g.u32(), "b1": g.u8()}
        e["b2"] = g.u8() if extra_byte else None
        e["devotion_level"] = g.u32()
        e["experience"] = g.u32()
        e["f_active"] = g.u32()
        e["u8a"] = g.u8()
        e["u8b"] = g.u8()
        e["autocast_skill"] = g.s()
        e["autocast_controller"] = g.s()
        if not e["record"].startswith("records/"):
            raise ValueError(f"skill-block desync at {e['record'][:40]!r}")
        rows.append(e)
    item_skill_count = g.u32()
    tail = bytes(g.u8() for _ in range(end - g.p))
    return h, b8, ver, n, rows, item_skill_count, tail


_SKILL_RE = re.compile(rb"records/skills/[a-z0-9_/\.\-]{5,90}\.dbr")
_ITEM_RE = re.compile(rb"records/items/[a-z0-9_/\.\-]{5,90}\.dbr")


def read_ui_bindings(path: pathlib.Path):
    """Block 14 -- the bound-skill array.  Emits ONLY directly-read fields (see G2)."""
    buf = path.read_bytes()
    h, bl = walk_blocks(buf)
    b14 = [b for b in bl if b["id"] == 14][0]
    g = reader_at(buf, b14)
    end = int(b14["payload"]) + int(b14["len"])
    dec = bytearray()
    while g.p < end:
        dec.append(g.u8())
    s = bytes(dec)
    out = []
    for m in _SKILL_RE.finditer(s):
        rec = m.group().decode()
        after = m.start() + len(rec)
        is_item = bool(s[after] == 1) if after < len(s) else False
        item = equip = None
        if is_item:
            m2 = _ITEM_RE.match(s, after + 5)
            if m2:
                item = m2.group().decode()
                equip = s[after + 5 + len(item)]
        out.append({"binding_ordinal": len(out), "skill_record": rec,
                    "is_item_skill": is_item, "item_record": item, "equip_location": equip})
    return h, b14, out, s


# ══════════════════════════════════════════════════════════════════════════════════════════════
# TEXT TAGS
# ══════════════════════════════════════════════════════════════════════════════════════════════

_TAGS: Optional[Dict[str, str]] = None


def tags() -> Dict[str, str]:
    global _TAGS
    if _TAGS is None:
        d: Dict[str, str] = {}
        for rel in TEXT_ARCS:
            p = VENDOR / rel
            if not p.exists():
                continue
            a = ArcArchive(p)
            for n in a.names():
                try:
                    raw = a.read_file(n).decode("utf-8", "replace")
                except Exception:
                    continue
                for line in raw.splitlines():
                    if "=" in line and not line.startswith("//"):
                        k, _, v = line.partition("=")
                        d[k.strip()] = v.strip()
        _TAGS = d
    return _TAGS


def name_of(rec: dict) -> str:
    return tags().get(str(rec.get("skillDisplayName", "")), "")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# RANK ALGEBRA -- allocated (MEASURED) vs effective (DERIVED, basis named)
# ══════════════════════════════════════════════════════════════════════════════════════════════

def sheet_skill_bonuses() -> Dict[str, int]:
    """From Lap A's `measured-player-sheet.csv` (camera-measured, frame 512).  NOT re-measured."""
    out: Dict[str, int] = {}
    with LAP_A_SHEET.open() as f:
        for row in csv.reader(f):
            if row and row[0].startswith("bonus_") and row[0].endswith("_skills"):
                out[row[0]] = int(row[1])
    return out


#: `playerclass01` = Soldier, `playerclass09` = Oathkeeper (from the class tag
#: `tagSkillClassName0109`, cross-checked at Lap A).
MASTERY_OF_DIR = {"playerclass01": ("Soldier", "bonus_soldier_skills"),
                  "playerclass09": ("Oathkeeper", "bonus_oathkeeper_skills")}


def effective_rank(record: str, allocated: int, bonuses: Dict[str, int]) -> Tuple[int, str]:
    """DERIVED.  +all-skills and +mastery-skills apply to MASTERY skills only.  Item-granted and
    devotion skills take NO rank bonus in GD, so they are returned unchanged with the basis said
    out loud rather than silently applied."""
    seg = record.split("/")
    d = seg[2] if len(seg) > 2 else ""
    if d in MASTERY_OF_DIR:
        mastery, key = MASTERY_OF_DIR[d]
        add = bonuses.get("bonus_all_skills", 0) + bonuses.get(key, 0)
        return allocated + add, f"DERIVED: allocated+{add} (+all {bonuses.get('bonus_all_skills',0)}, +{mastery} {bonuses.get(key,0)}; sheet frame 512)"
    return allocated, "MEASURED: no rank bonus applies (item-granted / devotion / default skill)"


def at_rank(v, rank: int):
    """Index a per-rank array at `rank` (1-based).  Scalars pass through.  Over-range clamps to the
    last authored cell and the caller is told, never silently."""
    if not isinstance(v, list):
        return v, "scalar"
    if not v:
        return None, "empty"
    i = max(0, min(rank - 1, len(v) - 1))
    return v[i], ("exact" if i == rank - 1 else f"CLAMPED to len {len(v)}")


def rec(path: str) -> dict:
    r, _arc = E3.winner(path)
    return r or {}


def arc_of(path: str) -> Optional[str]:
    _r, a = E3.winner(path)
    return a


def dump_csv(path: pathlib.Path, rows: Sequence[dict], cols: Sequence[str]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return hashlib.sha256(path.read_bytes()).hexdigest()
