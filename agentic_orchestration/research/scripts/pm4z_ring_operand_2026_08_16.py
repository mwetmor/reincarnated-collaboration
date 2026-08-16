#!/usr/bin/env python3
"""KC2-PM4 · Lap Z · THE RING-OPERAND FORK PAIR   (ruling `R-PM4-65 part 3`)

TWO questions, from `UNREACHED-I24D-1` (gamora, I-24-D § 10; root defect `D-I24D-1`):

  (a) is the engine's `meleeTargetDistance` operand the float32 the DB stores, promoted
      (`2.4000000953674316`), or the DB-cited decimal `2.4`?
  (b) does the engine's contact/range test compare SQUARED distances, or take a root first?

READ-ONLY on every source.  OUTCOME-FIREWALLED: reads no sim outcome, touches no baton, runs no
simulation, writes nothing outside this lap's notes directory.  Law 3: gamora's 0.234/0.372
occupancy pair is CONTEXT (prereg § 0.1) and is never consulted during grading.  `R-PM4-27 part 3`:
no limb is designated by which one grades better.

`NOTE D-V2-1` honoured.  The defect was that *vtable* data symbols (`??_7X@...@6B@`) collide on
RVAs in the export table, so vtable bases read from exports are unreliable.  This lap reads NO
vtable base.  It resolves exactly one FUNCTION export by name, and it discharges D-V2-1 explicitly
by (i) asserting the name's RVA is not shared with any other exported name, (ii) asserting the RVA
lands in `.text`, and (iii) asserting the RVA is the START of a `.pdata` RUNTIME_FUNCTION.  Every
other code site is reached by a byte-cited rip-relative / absolute reference, never by a symbol.

Evidence classes are those declared closed in `prereg.md § 2`:
  EC-1 compiled-record byte read · EC-2 template declaration · EC-3 format type-system census
  EC-4 squared-distance field sweep · EC-5 string residency · EC-6 targeted instruction-stream read
  EC-7 IEEE-754 boundary arithmetic · EC-8 TQ/GD lineage (shipped-corpus attestation)

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import math
import pathlib
import re
import struct
import sys
from decimal import Decimal, getcontext

import capstone
import lz4.block

getcontext().prec = 60

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GDBIN = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
SCRIPTS = META / "agentic_orchestration/research/scripts"
OUT = META / "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-z-ring-operand"

sys.path.insert(0, str(SCRIPTS))
from gd_arz_adapter_2026_07_24 import ArzArchive                            # noqa: E402
from gd_arc_reader_2026_07_26 import ArcArchive                             # noqa: E402

log_lines: list[str] = []


def L(msg: str = "") -> None:
    print(msg)
    log_lines.append(msg)


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 0 — THE PINS.  HALT on the first mismatch.  (prereg.md § 1)
# ══════════════════════════════════════════════════════════════════════════════════════════════

PINS = {
    VENDOR / "database/database.arz": "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    VENDOR / "gdx1/database/GDX1.arz": "431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292",
    VENDOR / "gdx2/database/GDX2.arz": "13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072",
    VENDOR / "gdx3/database/GDX3.arz": "e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4",
    VENDOR / "database/templates.arc": "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
    GDBIN / "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    GDBIN / "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
    GDBIN / "Grim Dawn.exe": "1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4",
    GDBIN / "x64/Game.dll": "7c62f1aa8b32ce3dbfb5a640b7af280203d28016b8f9e39225e36028136b26eb",
    GDBIN / "x64/Engine.dll": "d6df581038af18184ce7f63d75ecbe56f350d12e49d396064445bda3a6650a2c",
    GDBIN / "x64/Grim Dawn.exe": "82c42980a194e152bd91092461198e0d04d8e47aea14701d3a997d2e238691e3",
    GDBIN / "DBREditor.exe": "4d11ae30b4c0faca7d8e4a2f410e023cd22bcc9cfad20a3a1598a5777794d93a",
    GDBIN / "ArchiveTool.exe": "fae1c6ec40a6beeb3968ad15a10e7345ef025f47f552d002952b4f3a6c0cce0a",
    GDBIN / "AssetManager.exe": "7e84db3f26adf9f18376251baa26c5450d7875ec5a54fd95487116f288a23aa3",
    SCRIPTS / "gd_arz_adapter_2026_07_24.py": "040bd078a73f81ed7b839820fcfc15af1e74beba81a930fc147f1080bb317266",
    SCRIPTS / "gd_arc_reader_2026_07_26.py": "a5def5a669270f6362f96dfcb932d0ba8a77b689919086675b97b95fa16f7597",
}

# survivalmode overlays: pinned in Lap Y, re-verified here for the override sweep only
OVERLAYS = [
    ("SurvivalMode.arz", VENDOR / "mods/survivalmode/database/SurvivalMode.arz",
     "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6"),
    ("SurvivalMode1.arz", VENDOR / "survivalmode1/database/SurvivalMode1.arz",
     "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252"),
    ("SurvivalMode2.arz", VENDOR / "survivalmode2/database/SurvivalMode2.arz",
     "940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95"),
    ("SurvivalMode3.arz", VENDOR / "survivalmode3/database/SurvivalMode3.arz",
     "e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a"),
]


def verify_pins() -> dict:
    L("§ 0  PINS — re-verified before any read.  HALT on first mismatch.")
    got = {}
    for p, want in list(PINS.items()) + [(pp, ww) for _, pp, ww in OVERLAYS]:
        h = sha(p)
        got[str(p)] = h
        state = "OK " if h == want else "DRIFT"
        L(f"   [{state}] {h}  {p.name}")
        if h != want:
            raise SystemExit(f"HALT-PIN-DRIFT: {p} expected {want} got {h}")
    L(f"   {len(got)} pins verified EXACT.")
    L()
    return got


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 1 — MINIMAL PE READER (PE32 + PE32+).  No vtable reads anywhere.
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PEX:
    def __init__(self, path: pathlib.Path):
        self.path = pathlib.Path(path)
        self.B = B = self.path.read_bytes()
        pe = struct.unpack_from("<I", B, 0x3C)[0]
        if B[pe:pe + 4] != b"PE\0\0":
            raise ValueError(f"BLOCKED-FORMAT: no PE signature ({path})")
        self.opt = opt = pe + 24
        self.opt_size = struct.unpack_from("<H", B, pe + 20)[0]
        self.magic = struct.unpack_from("<H", B, opt)[0]
        self.p64 = self.magic == 0x20B
        self.image_base = (struct.unpack_from("<Q", B, opt + 24)[0] if self.p64
                           else struct.unpack_from("<I", B, opt + 28)[0])
        nd_off = opt + (108 if self.p64 else 92)
        n = struct.unpack_from("<I", B, nd_off)[0]
        self.dirs = [struct.unpack_from("<II", B, nd_off + 4 + 8 * i) for i in range(n)]
        sec = opt + self.opt_size
        self.secs = {}
        for i in range(struct.unpack_from("<H", B, pe + 6)[0]):
            nm, vs, va, rs, ra = struct.unpack_from("<8sIIII", B, sec + 40 * i)
            self.secs[nm.rstrip(b"\0").decode("latin-1")] = (vs, va, rs, ra)
        self.md = capstone.Cs(capstone.CS_ARCH_X86,
                              capstone.CS_MODE_64 if self.p64 else capstone.CS_MODE_32)

    def rva2off(self, rva):
        for _n, (vs, va, rs, ra) in self.secs.items():
            if va <= rva < va + max(vs, rs):
                d = rva - va
                if d < rs:
                    return ra + d
        return None

    def off2rva(self, off):
        for _n, (vs, va, rs, ra) in self.secs.items():
            if ra <= off < ra + rs:
                return va + (off - ra)
        return None

    def section_of(self, rva):
        for n, (vs, va, rs, ra) in self.secs.items():
            if va <= rva < va + max(vs, rs):
                return n
        return None

    def cstr(self, rva):
        o = self.rva2off(rva)
        e = self.B.index(b"\0", o)
        return self.B[o:e].decode("latin-1")

    def exports(self):
        """decorated-name -> RVA.  FUNCTION exports only are used by this lap; see D-V2-1 guard."""
        er, _es = self.dirs[0]
        o = self.rva2off(er)
        (_c, _t, _M, _m, _nm, _ordbase, _nfuncs, nnames,
         eat, enpt, eot) = struct.unpack_from("<IIHHIIIIIII", self.B, o)
        eat_o, enpt_o, eot_o = self.rva2off(eat), self.rva2off(enpt), self.rva2off(eot)
        out = {}
        for i in range(nnames):
            nr = struct.unpack_from("<I", self.B, enpt_o + 4 * i)[0]
            ordi = struct.unpack_from("<H", self.B, eot_o + 2 * i)[0]
            out[self.cstr(nr)] = struct.unpack_from("<I", self.B, eat_o + 4 * ordi)[0]
        return out

    def imports(self):
        """IAT-slot-RVA -> (dll, symbol)."""
        imp_rva, _sz = self.dirs[1]
        p = self.rva2off(imp_rva)
        out = {}
        while True:
            olt, _ts, _fc, name_rva, iat_rva = struct.unpack_from("<IIIII", self.B, p)
            if name_rva == 0:
                break
            dll = self.cstr(name_rva)
            t = olt if olt else iat_rva
            step = 8 if self.p64 else 4
            fmt = "<Q" if self.p64 else "<I"
            k = 0
            while True:
                ent = struct.unpack_from(fmt, self.B, self.rva2off(t) + step * k)[0]
                if ent == 0:
                    break
                hi = (1 << 63) if self.p64 else (1 << 31)
                nm = f"ORDINAL#{ent & 0xffff}" if ent & hi else self.cstr((ent & 0x7fffffff) + 2)
                out[iat_rva + step * k] = (dll, nm)
                k += 1
            p += 20
        return out

    def pdata(self):
        vs, va, rs, ra = self.secs[".pdata"]
        out = []
        for i in range(ra, ra + rs, 12):
            b_, e_, _u = struct.unpack_from("<III", self.B, i)
            if b_ or e_:
                out.append((b_, e_))
        return out

    def fnbounds(self, rva):
        for b_, e_ in self.pdata():
            if b_ <= rva < e_:
                return b_, e_
        return None

    def dis(self, beg, end):
        o = self.rva2off(beg)
        code = self.B[o:o + (end - beg)]
        return [(i.address - self.image_base, i.mnemonic, i.op_str)
                for i in self.md.disasm(code, self.image_base + beg)]

    def bytes_at(self, rva, n):
        o = self.rva2off(rva)
        return self.B[o:o + n]


def f32_of(b4: bytes) -> float:
    return struct.unpack("<f", b4)[0]


def to_f32(x: float) -> float:
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 2 — EC-1  COMPILED-RECORD BYTE READ
# ══════════════════════════════════════════════════════════════════════════════════════════════

REC = "records/game/gameengine.dbr"
FIELDS = ("meleeTargetDistance", "meleeAutoTargetDistance", "meleeRange")


def ec1():
    L("═" * 100)
    L("EC-1  COMPILED-RECORD BYTE READ — what does the shipped DB literally store?")
    L("═" * 100)
    out = {"record": REC, "fields": {}, "overlay_overrides": [], "substring_decoys": []}
    a = ArzArchive(VENDOR / "database/database.arz")

    # ⚑ D-Z-1 GUARD: name the record EXACTLY.  A substring match on 'gameengine' returns 7 records,
    # six of which are dev-sandbox archives carrying DIFFERENT values.  Enumerate them so the
    # decoy set is on the record, not merely avoided.
    decoys = sorted(r for r in a.records if "gameengine" in r.lower() and r != REC)
    for d in decoys:
        m = a.records[d]
        dec = lz4.block.decompress(a.raw[24 + m["data_offset"]:24 + m["data_offset"] + m["comp_size"]],
                                   uncompressed_size=m["decomp_size"])
        pos = 0
        val = None
        while pos + 8 <= len(dec):
            ft, c, k = struct.unpack_from("<HHI", dec, pos)
            if a.strings[k] == "meleeTargetDistance":
                val = (ft, dec[pos + 8:pos + 8 + 4].hex())
            pos += 8 + c * 4
        out["substring_decoys"].append({"record": d, "meleeTargetDistance": val})
    L(f"   ⚑ D-Z-1 GUARD: {len(decoys)} decoy records substring-match 'gameengine'; all enumerated.")
    for d in out["substring_decoys"]:
        if d["meleeTargetDistance"]:
            L(f"       DECOY {d['record']}  type={d['meleeTargetDistance'][0]} "
              f"hex={d['meleeTargetDistance'][1]} f32={f32_of(bytes.fromhex(d['meleeTargetDistance'][1]))!r}")

    m = a.records[REC]
    base = 24 + m["data_offset"]
    dec = lz4.block.decompress(a.raw[base:base + m["comp_size"]], uncompressed_size=m["decomp_size"])
    pos = 0
    while pos + 8 <= len(dec):
        ft, c, k = struct.unpack_from("<HHI", dec, pos)
        nm = a.strings[k]
        payload = dec[pos + 8:pos + 8 + c * 4]
        if nm in FIELDS:
            u32 = struct.unpack("<I", payload)[0]
            fv = f32_of(payload)
            out["fields"][nm] = {
                "record_stream_offset": f"0x{pos:04x}", "type_tag": ft, "value_count": c,
                "payload_bytes_hex": payload.hex(), "payload_u32_hex": f"0x{u32:08x}",
                "payload_width_bytes": len(payload),
                "as_float32_promoted_to_double": repr(fv),
                "exact_decimal": str(Decimal(fv)),
            }
            L(f"   {REC} @0x{pos:04x}  {nm}")
            L(f"       type_tag={ft} (1 = float32)   count={c}   payload={payload.hex()} "
              f"= 0x{u32:08x}   width={len(payload)} B")
            L(f"       as double: {fv!r}   exact: {Decimal(fv)}")
        pos += 8 + c * 4
    out["field_stream_residue_bytes"] = len(dec) - pos
    L(f"   field-stream residue for this record: {len(dec) - pos} bytes")

    for lbl, p, _w in OVERLAYS + [("GDX1.arz", VENDOR / "gdx1/database/GDX1.arz", ""),
                                  ("GDX2.arz", VENDOR / "gdx2/database/GDX2.arz", ""),
                                  ("GDX3.arz", VENDOR / "gdx3/database/GDX3.arz", "")]:
        ov = ArzArchive(p)
        present = REC in ov.records
        out["overlay_overrides"].append({"archive": lbl, "record_present": present})
        L(f"   overlay {lbl:18} {REC} present: {present}")
    L()
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 3 — EC-2 / EC-3 / EC-4 / EC-8  TEMPLATE + FORMAT TYPE SYSTEM
# ══════════════════════════════════════════════════════════════════════════════════════════════

def ec234():
    L("═" * 100)
    L("EC-2 / EC-3 / EC-4 / EC-8  TEMPLATE DECLARATION · FORMAT TYPE SYSTEM · SQUARED SWEEP")
    L("═" * 100)
    arc = ArcArchive(VENDOR / "database/templates.arc")
    names = list(arc.names())
    types = collections.Counter()
    varnames = set()
    tq = []
    sq = []
    decls = {}
    fails = []
    for n in names:
        try:
            t = arc.read_file(n).decode("latin-1")
        except Exception as ex:
            e = arc.entries[n]
            fails.append({"name": n, "error": type(ex).__name__, "entry_type": e["entry_type"],
                          "comp_size": e["comp_size"], "decomp_size": e["decomp_size"]})
            continue
        for mm in re.finditer(r'type\s*=\s*"([^"]*)"', t):
            types[mm.group(1)] += 1
        for mm in re.finditer(r"Variable\s*\{(.*?)\}", t, re.S):
            blk = mm.group(1)
            g = lambda k: (re.search(k + r'\s*=\s*"([^"]*)"', blk).group(1)
                           if re.search(k + r'\s*=\s*"([^"]*)"', blk) else "")
            nm = g("name")
            if not nm:
                continue
            varnames.add(nm)
            ty, de, dv = g("type"), g("description"), g("defaultValue")
            if re.search(r"\bTQ\b", de):
                tq.append({"template": n, "name": nm, "type": ty, "description": de,
                           "defaultValue": dv})
            low = nm.lower()
            if "squared" in low or low.endswith("sq") or "sqr" in low:
                sq.append({"template": n, "name": nm, "type": ty})
            if nm in FIELDS and n == "gameengine.tpl":
                decls[nm] = {"template": n, "class": g("class"), "type": ty,
                             "description": de, "defaultValue": dv}
    L(f"   templates parsed OK: {len(names) - len(fails)}/{len(names)}   failed: {len(fails)}")
    for f in fails:
        L(f"       FAIL {f}")
    L(f"   distinct Variable names across the corpus: {len(varnames)}")
    L("   EC-2  gameengine.tpl declarations:")
    for k, v in decls.items():
        L(f"       {k}: class={v['class']!r} type={v['type']!r} "
          f"description={v['description']!r} defaultValue={v['defaultValue']!r}")
    L("   EC-3  distinct type= strings (the format's entire declared type alphabet):")
    for k, v in sorted(types.items(), key=lambda x: -x[1]):
        L(f"       {k!r:22} x{v}")
    L(f"   EC-3  any 'double'-class type declared anywhere: "
      f"{[k for k in types if 'double' in k.lower()] or 'NONE'}")
    L(f"   EC-4  Variable names matching squared/sq/sqr: {sq or 'NONE (decoded-absent)'}")
    L(f"   EC-8  Variables whose description names Titan Quest: {len(tq)}")
    for r in tq:
        L(f"       {r}")
    L()
    return {"template_type_strings": dict(types), "declarations": decls,
            "distinct_variable_names": len(varnames), "squared_field_matches": sq,
            "tq_lineage_attestations": tq, "template_parse_failures": fails,
            "templates_total": len(names)}


ARCHIVES = [("database.arz", VENDOR / "database/database.arz"),
            ("GDX1.arz", VENDOR / "gdx1/database/GDX1.arz"),
            ("GDX2.arz", VENDOR / "gdx2/database/GDX2.arz"),
            ("GDX3.arz", VENDOR / "gdx3/database/GDX3.arz")] + \
           [(lbl, p) for lbl, p, _ in OVERLAYS]


def ec3_typetags():
    L("═" * 100)
    L("EC-3  COMPILED-FORMAT TYPE-TAG CENSUS — the falsifiable width test")
    L("═" * 100)
    L("   The reader assumes a 4-byte stride per value.  If ANY type tag carried an 8-byte payload,")
    L("   the field stream would desync and leave residue.  Residue is therefore the falsifier for")
    L("   'the compiled format has no double-width numeric type'.")
    grand = collections.Counter()
    rows = []
    tot_rec = tot_res = 0
    for lbl, p in ARCHIVES:
        a = ArzArchive(p)
        tc = collections.Counter()
        n = res = 0
        for _rec, m in a.records.items():
            base = 24 + m["data_offset"]
            dec = lz4.block.decompress(a.raw[base:base + m["comp_size"]],
                                       uncompressed_size=m["decomp_size"])
            pos = 0
            while pos + 8 <= len(dec):
                ft, c, _k = struct.unpack_from("<HHI", dec, pos)
                tc[ft] += 1
                pos += 8 + c * 4
            if pos != len(dec):
                res += 1
            n += 1
        grand += tc
        tot_rec += n
        tot_res += res
        rows.append({"archive": lbl, "records": n, "field_entries": sum(tc.values()),
                     "type_tags": json.dumps(dict(sorted(tc.items()))),
                     "records_with_stream_residue": res})
        L(f"   {lbl:18} records={n:6}  tags={dict(sorted(tc.items()))}  residue_records={res}")
    L(f"   GRAND: records={tot_rec}  field_entries={sum(grand.values())}  "
      f"distinct_type_tags={sorted(grand)}  records_with_residue={tot_res}")
    L()
    return {"per_archive": rows, "grand_records": tot_rec,
            "grand_field_entries": sum(grand.values()),
            "distinct_type_tags": sorted(grand), "records_with_stream_residue": tot_res}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 4 — EC-5  STRING RESIDENCY (CORROBORATION ONLY)
# ══════════════════════════════════════════════════════════════════════════════════════════════

MODULES = [("x86/Game.dll", GDBIN / "Game.dll"), ("x86/Engine.dll", GDBIN / "Engine.dll"),
           ("x86/Grim Dawn.exe", GDBIN / "Grim Dawn.exe"),
           ("x64/Game.dll", GDBIN / "x64/Game.dll"), ("x64/Engine.dll", GDBIN / "x64/Engine.dll"),
           ("x64/Grim Dawn.exe", GDBIN / "x64/Grim Dawn.exe"),
           ("DBREditor.exe", GDBIN / "DBREditor.exe"),
           ("ArchiveTool.exe", GDBIN / "ArchiveTool.exe"),
           ("AssetManager.exe", GDBIN / "AssetManager.exe")]

NEEDLES = [b"meleeTargetDistance", b"GetEntitiesInCone", b"GetEntitiesInSphere",
           b"GetDistanceSquared", b"LengthSquared", b"SqrDist", b"DistanceSq"]


def ec5():
    L("═" * 100)
    L("EC-5  STRING RESIDENCY — CORROBORATION GRADE ONLY (D-V2-1: names a vocabulary, not a caller)")
    L("═" * 100)
    rows = []
    for lbl, p in MODULES:
        b = p.read_bytes()
        r = {"module": lbl}
        for n in NEEDLES:
            r[n.decode()] = b.count(n)
        rows.append(r)
        L(f"   {lbl:20} " + "  ".join(f"{n.decode()}={r[n.decode()]}" for n in NEEDLES))
    L()
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 5 — EC-6  TARGETED INSTRUCTION-STREAM READ.  Every link cited by file + RVA + bytes.
# ══════════════════════════════════════════════════════════════════════════════════════════════

CONE_SYM = ("?GetEntitiesInCone@World@GAME@@QEAAXAEAV?$vector@PEAVEntity@GAME@@@mem@@"
            "AEBVWorldVec3@2@AEBVVec3@2@MM_NW4EntityListType@2@@Z")


def ec6():
    L("═" * 100)
    L("EC-6  TARGETED INSTRUCTION-STREAM READ — the anchor chain, link by link")
    L("═" * 100)
    A = {}

    # ---- LINK 1: the field-name string in x64/Game.dll -----------------------------------------
    g = PEX(GDBIN / "x64/Game.dll")
    off = g.B.find(b"meleeTargetDistance\x00")
    srva = g.off2rva(off)
    A["link1_string"] = {"module": "x64/Game.dll", "file_offset": f"0x{off:x}",
                         "rva": f"0x{srva:x}", "section": g.section_of(srva),
                         "bytes": g.bytes_at(srva, 20).hex(),
                         "occurrences_in_module": g.B.count(b"meleeTargetDistance\x00")}
    L(f"   L1  'meleeTargetDistance\\0' @ x64/Game.dll rva 0x{srva:x} ({g.section_of(srva)}), "
      f"{A['link1_string']['occurrences_in_module']} occurrence(s)")

    # ---- LINK 2: every rip-relative reference to it in .text -----------------------------------
    vs, va, rs, ra = g.secs[".text"]
    refs = []
    for o in range(ra, ra + rs - 4):
        disp = struct.unpack_from("<i", g.B, o)[0]
        if va + (o - ra) + 4 + disp == srva:
            refs.append(va + (o - ra))
    A["link2_refs"] = [{"disp_rva": f"0x{r:x}", "lea_rva": f"0x{r - 3:x}",
                        "lea_bytes": g.bytes_at(r - 3, 7).hex()} for r in refs]
    L(f"   L2  rip-relative references in .text: {len(refs)} -> "
      f"{[hex(r - 3) for r in refs]}  (opcode 48 8D 15 = lea rdx,[rip+d32])")

    # ---- LINK 3: the load site and its float-width store ---------------------------------------
    load_fn = g.fnbounds(refs[0])
    load = g.dis(0x2B3D66, 0x2B3DAA)
    A["link3_load_site"] = {
        "module": "x64/Game.dll",
        "runtime_function": [f"0x{load_fn[0]:x}", f"0x{load_fn[1]:x}"],
        "listing": [f"0x{a:08x}  {m} {o}" for a, m, o in load],
        "store_instruction": next(f"0x{a:08x}  {m} {o}" for a, m, o in load
                                  if m == "movss" and o.startswith("dword ptr [r13 + 0x13a4]")),
        "field_slot": "gameengine-config + 0x13a4",
        "store_width_bytes": 4,
    }
    L(f"   L3  load site inside RUNTIME_FUNCTION 0x{load_fn[0]:x}..0x{load_fn[1]:x}:")
    for a, m, o in load:
        L(f"          0x{a:08x}  {m:<8} {o}")
    L("       ⇒ the DB accessor's return is stored by `movss` (4-byte single) into slot +0x13a4.")

    # ---- LINK 4: the C++ constructor default at the same slot (independent slot-width witness) --
    ctor = g.dis(0x2AC150, 0x2AC18C)
    A["link4_ctor_defaults"] = [f"0x{a:08x}  {m} {o}" for a, m, o in ctor]
    L("   L4  constructor defaults at the same slot family (independent width witness):")
    for a, m, o in ctor:
        imm = re.search(r"0x([0-9a-f]{8})$", o)
        fv = f"  = {f32_of(struct.pack('<I', int(imm.group(1), 16)))!r}f" if imm else ""
        L(f"          0x{a:08x}  {m:<8} {o}{fv}")

    # ---- LINK 5: the SOLE reader of slot +0x13a4 across the whole module -----------------------
    md = g.md
    readers = []
    for beg, end in g.pdata():
        o = g.rva2off(beg)
        if o is None:
            continue
        for i in md.disasm(g.B[o:o + (end - beg)], g.image_base + beg):
            if "0x13a4" in i.op_str:
                readers.append({"fn": f"0x{beg:x}", "rva": f"0x{i.address - g.image_base:x}",
                                "mnemonic": i.mnemonic, "op_str": i.op_str})
    A["link5_slot_refs"] = readers
    L(f"   L5  ALL instructions in x64/Game.dll referencing displacement 0x13a4: {len(readers)}")
    for r in readers:
        L(f"          fn={r['fn']:>10} @{r['rva']:>10}  {r['mnemonic']:<8} {r['op_str']}")

    # ---- LINK 6: the consumer passes it as the cone radius, via a NAMED IMPORT -----------------
    cons = g.dis(0x501343, 0x501362) + g.dis(0x5015E8, 0x501621)
    imp = g.imports()
    call_slot = 0x5F1950
    A["link6_consumer"] = {
        "module": "x64/Game.dll", "runtime_function": "0x5012d0",
        "listing": [f"0x{a:08x}  {m} {o}" for a, m, o in cons],
        "iat_slot_rva": f"0x{call_slot:x}", "import": list(imp[call_slot]),
    }
    L("   L6  the consumer (RUNTIME_FUNCTION 0x5012d0) passes the value as a call argument:")
    for a, m, o in cons:
        L(f"          0x{a:08x}  {m:<8} {o}")
    L(f"       IAT slot 0x{call_slot:x} resolves by the IMPORT DIRECTORY to:")
    L(f"          {imp[call_slot][0]} :: {imp[call_slot][1]}")

    # ---- LINK 7: D-V2-1-guarded export resolution in Engine.dll --------------------------------
    e = PEX(GDBIN / "x64/Engine.dll")
    ex = e.exports()
    cone = ex[CONE_SYM]
    shared = [k for k, v in ex.items() if v == cone]
    fb = e.fnbounds(cone)
    A["link7_export_guard"] = {
        "module": "x64/Engine.dll", "symbol": CONE_SYM, "rva": f"0x{cone:x}",
        "exports_sharing_this_rva": shared, "section": e.section_of(cone),
        "pdata_bounds": [f"0x{fb[0]:x}", f"0x{fb[1]:x}"],
        "rva_is_function_start": fb[0] == cone, "total_exports": len(ex),
    }
    L("   L7  D-V2-1 GUARD on the one export this lap resolves by name:")
    L(f"          rva 0x{cone:x}   names sharing this rva: {len(shared)} ({shared == [CONE_SYM]})")
    L(f"          section={e.section_of(cone)}   .pdata bounds 0x{fb[0]:x}..0x{fb[1]:x}   "
      f"rva==function-start: {fb[0] == cone}")

    # ---- LINK 8: the Sphere is built with a 4-byte radius, then delegated ----------------------
    build = e.dis(0x21DCD7, 0x21DD1D)
    A["link8_sphere_build"] = [f"0x{a:08x}  {m} {o}" for a, m, o in build]
    L("   L8  GetEntitiesInCone builds a Sphere {float x,y,z; float radius} and delegates:")
    for a, m, o in build:
        L(f"          0x{a:08x}  {m:<8} {o}")
    inv = {}
    for k, v in ex.items():
        inv.setdefault(v, []).append(k)
    A["link8_delegate"] = inv.get(0x21E3A0)
    L(f"          call 0x21e3a0 -> {inv.get(0x21E3A0)}")

    # ---- LINK 9: the per-entity test site inside the quadtree walk -----------------------------
    walk = e.dis(0x134110, 0x134134)
    A["link9_walk"] = [f"0x{a:08x}  {m} {o}" for a, m, o in walk]
    L("   L9  per-entity test site inside the sphere gather (0x134080):")
    for a, m, o in walk:
        L(f"          0x{a:08x}  {m:<8} {o}")

    # ---- LINK 10: THE COMPARISON ITSELF --------------------------------------------------------
    prim = e.dis(0x27CFF0, 0x27D0DF)
    A["link10_primitive_x64"] = {
        "module": "x64/Engine.dll", "rva": "0x27cff0",
        "pdata_bounds": [f"0x{e.fnbounds(0x27CFF0)[0]:x}", f"0x{e.fnbounds(0x27CFF0)[1]:x}"],
        "listing": [f"0x{a:08x}  {m} {o}" for a, m, o in prim],
        "sqrt_instructions": [f"0x{a:08x} {m} {o}" for a, m, o in prim if m.startswith("sqrt")],
        "double_precision_arithmetic": [f"0x{a:08x} {m} {o}" for a, m, o in prim
                                        if m in ("mulsd", "addsd", "subsd", "comisd", "ucomisd",
                                                 "divsd", "sqrtsd")],
        "radius_square": [f"0x{a:08x} {m} {o}" for a, m, o in prim
                          if m == "mulss" and o == "xmm0, xmm0"],
        "compare": [f"0x{a:08x} {m} {o}" for a, m, o in prim if m == "comiss"][-1],
    }
    L("   L10 THE COMPARISON — x64/Engine.dll 0x27cff0 (box-vs-sphere; rcx=ABBox, rdx=Sphere):")
    for a, m, o in prim:
        L(f"          0x{a:08x}  {m:<8} {o}")
    L(f"       sqrt instructions in this function: "
      f"{A['link10_primitive_x64']['sqrt_instructions'] or 'NONE'}")
    L(f"       double-precision arithmetic in this function: "
      f"{A['link10_primitive_x64']['double_precision_arithmetic'] or 'NONE'}")

    # ---- LINK 11: the independent node-level primitive agrees ----------------------------------
    node = e.dis(0x134B50, 0x134C22)
    A["link11_primitive_node"] = {
        "module": "x64/Engine.dll", "rva": "0x134b50",
        "listing": [f"0x{a:08x}  {m} {o}" for a, m, o in node],
        "sqrt_instructions": [f"0x{a:08x} {m} {o}" for a, m, o in node if m.startswith("sqrt")],
        "double_precision_arithmetic": [f"0x{a:08x} {m} {o}" for a, m, o in node
                                        if m in ("mulsd", "addsd", "subsd", "comisd", "ucomisd")],
    }
    L(f"   L11 second, independent primitive at 0x134b50 (node-vs-sphere): "
      f"sqrt={A['link11_primitive_node']['sqrt_instructions'] or 'NONE'}, "
      f"double={A['link11_primitive_node']['double_precision_arithmetic'] or 'NONE'}")

    # ---- LINK 12: the x86 shipped build, independently -----------------------------------------
    g32 = PEX(GDBIN / "Game.dll")
    off32 = g32.B.find(b"meleeTargetDistance\x00")
    srva32 = g32.off2rva(off32)
    va32 = g32.image_base + srva32
    vs, va, rs, ra = g32.secs[".text"]
    refs32 = [va + (o - ra) for o in range(ra, ra + rs - 4)
              if struct.unpack_from("<I", g32.B, o)[0] == va32]
    # ⚑ D-Z-3.  PE32 has no .pdata, so an x86 disassembly start is a MANUAL byte anchor and a
    # linear sweep from an arbitrary offset can desync mid-instruction.  Guard: decode from THREE
    # independent start offsets and require the store instruction to agree in all three.  If they
    # disagree, the listing is not cited.
    starts = [refs32[0] - 0x40, refs32[0] - 0x3C, refs32[0] - 0x2E]
    legs = [g32.dis(s, refs32[0] + 0x14) for s in starts]
    store_claims = []
    for lg in legs:
        hit = [f"0x{a:08x}  {m} {o}" for a, m, o in lg
               if m == "fstp" and o == "dword ptr [edi + 0xc7c]"]
        store_claims.append(hit)
    x86_converged = len({tuple(c) for c in store_claims}) == 1 and all(store_claims)
    x86load = legs[0]
    e32 = PEX(GDBIN / "Engine.dll")
    vs, va, rs, ra = e32.secs[".text"]
    pat = re.compile(rb"\xf3\x0f\x59\xc0.{0,12}?\x0f\x2f.{1,6}?\x0f[\x93\x97]\xc0", re.S)
    sites = [va + m.start() for m in pat.finditer(e32.B[ra:ra + rs])]
    x86prim = e32.dis(sites[-1] - 0x30, sites[-1] + 0x12)
    A["link12_x86"] = {
        "game_dll_string_rva": f"0x{srva32:x}", "game_dll_abs_refs": [f"0x{r:x}" for r in refs32],
        "game_dll_store_listing": [f"0x{a:08x}  {m} {o}" for a, m, o in x86load],
        "d_z_3_three_start_convergence": x86_converged,
        "d_z_3_start_offsets": [f"0x{s:x}" for s in starts],
        "d_z_3_store_claim_per_start": store_claims,
        "engine_dll_signature_sites": [f"0x{s:x}" for s in sites],
        "engine_dll_primitive_listing": [f"0x{a:08x}  {m} {o}" for a, m, o in x86prim],
    }
    L("   L12 x86 shipped build, independently:")
    L(f"       ⚑ D-Z-3 three-start convergence on the store instruction: {x86_converged} "
      f"(starts {[hex(s) for s in starts]})")
    for a, m, o in x86load:
        L(f"          [Game.dll]   0x{a:08x}  {m:<8} {o}")
    for a, m, o in x86prim:
        L(f"          [Engine.dll] 0x{a:08x}  {m:<8} {o}")
    L()
    return A


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 6 — EC-7  IEEE-754 BOUNDARY ARITHMETIC
# ══════════════════════════════════════════════════════════════════════════════════════════════

def ec7():
    L("═" * 100)
    L("EC-7  IEEE-754 BOUNDARY ARITHMETIC — what each limb is worth, in metres")
    L("═" * 100)
    r32 = f32_of(bytes.fromhex("9a991940"))
    d24 = 2.4
    sq64 = r32 * r32
    sq32 = to_f32(r32 * r32)
    eng = math.sqrt(sq32)
    rows = [
        {"id": "A2/B2", "limb_a": "decimal 2.4", "limb_b": "rooted", "arith": "double",
         "threshold_m": repr(d24), "exact_decimal": str(Decimal(d24))},
        {"id": "A1/B2", "limb_a": "stored float32", "limb_b": "rooted", "arith": "double",
         "threshold_m": repr(r32), "exact_decimal": str(Decimal(r32))},
        {"id": "A2/B1", "limb_a": "decimal 2.4", "limb_b": "squared", "arith": "double",
         "threshold_m": repr(math.sqrt(d24 * d24)), "exact_decimal": str(Decimal(math.sqrt(d24 * d24)))},
        {"id": "A1/B1", "limb_a": "stored float32", "limb_b": "squared", "arith": "double",
         "threshold_m": repr(math.sqrt(sq64)), "exact_decimal": str(Decimal(math.sqrt(sq64)))},
        {"id": "ENGINE", "limb_a": "stored float32", "limb_b": "squared", "arith": "float32",
         "threshold_m": repr(eng), "exact_decimal": str(Decimal(eng))},
    ]
    for r in rows:
        r["delta_vs_engine_m"] = f"{Decimal(float(r['threshold_m'])) - Decimal(eng):+.6E}"
    out = {
        "r32_bit_pattern": "0x4019999A",
        "r32_as_double": repr(r32), "r32_exact_decimal": str(Decimal(r32)),
        "decimal_2p4_as_double": repr(d24), "decimal_2p4_exact": str(Decimal(d24)),
        "fork_a_window_m": str(Decimal(r32) - Decimal(d24)),
        "r32_squared_double": repr(sq64), "r32_squared_double_is_exact": Decimal(sq64) == Decimal(r32) * Decimal(r32),
        "fl32_r32_squared": repr(sq32), "fl32_r32_squared_exact": str(Decimal(sq32)),
        "fl32_r32_squared_hex": struct.pack("<f", sq32).hex(),
        "engine_effective_radius_m": repr(eng), "engine_effective_radius_exact": str(Decimal(eng)),
        "engine_minus_r32_m": str(Decimal(eng) - Decimal(r32)),
        "engine_minus_2p4_m": str(Decimal(eng) - Decimal(d24)),
        "fork_b_inert_at_double_precision": Decimal(math.sqrt(sq64)) == Decimal(r32),
        "table": rows,
    }
    L(f"   r32 = float32(2.4) = 0x4019999A = {r32!r}   exact {Decimal(r32)}")
    L(f"   decimal 2.4 as double            = {d24!r}   exact {Decimal(d24)}")
    L(f"   FORK-(a) WINDOW                  = {Decimal(r32) - Decimal(d24)} m")
    L(f"   r32^2 in double is EXACT (48-bit product in a 53-bit significand): "
      f"{out['r32_squared_double_is_exact']}")
    L(f"      ⇒ at DOUBLE precision, squared and rooted give the SAME threshold: fork (b) INERT")
    L(f"   fl32(r32^2) = {sq32!r} = 0x{struct.pack('<f', sq32).hex()}   exact {Decimal(sq32)}")
    L(f"   ENGINE effective boundary radius = sqrt(fl32(r32^2)) = {eng!r}")
    L(f"      engine - r32  = {Decimal(eng) - Decimal(r32)} m")
    L(f"      engine - 2.4  = {Decimal(eng) - Decimal(d24)} m")
    L("   ⇒ the engine's threshold sits at the MIDPOINT of the fork-(a) window, "
      "4.768e-8 m from EACH limb.")
    L()
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════════════════════

def main():
    L("KC2-PM4 · LAP Z · RING-OPERAND FORK PAIR — instrument run")
    L("legolas (UNKNOWN-RESEARCHER) · 2026-08-16 · read-only · outcome-firewalled")
    L()
    digests = verify_pins()
    res = {
        "lap": "KC2-PM4 Lap Z", "commission": "R-PM4-65 part 3",
        "provenance": "UNREACHED-I24D-1 (gamora I-24-D § 10); root defect D-I24D-1",
        "ec1_compiled_record": ec1(),
        "ec2_ec4_ec8_templates": ec234(),
        "ec3_type_tag_census": ec3_typetags(),
        "ec5_string_residency": ec5(),
        "ec6_instruction_stream": ec6(),
        "ec7_boundary_arithmetic": ec7(),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pm4z_operand.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    (OUT / "pm4z_binary_anchors.json").write_text(
        json.dumps(res["ec6_instruction_stream"], indent=2, sort_keys=True) + "\n")

    with (OUT / "pm4z_type_system.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["layer", "key", "count_or_value", "basis"])
        for k, v in sorted(res["ec2_ec4_ec8_templates"]["template_type_strings"].items()):
            w.writerow(["templates.arc type= string", k, v, "819 shipped .tpl files"])
        for r in res["ec3_type_tag_census"]["per_archive"]:
            w.writerow(["arz type-tag census", r["archive"], r["type_tags"],
                        f"records={r['records']} entries={r['field_entries']} "
                        f"residue_records={r['records_with_stream_residue']}"])
        w.writerow(["arz type-tag census", "GRAND", json.dumps(res["ec3_type_tag_census"]["distinct_type_tags"]),
                    f"records={res['ec3_type_tag_census']['grand_records']} "
                    f"entries={res['ec3_type_tag_census']['grand_field_entries']} "
                    f"residue_records={res['ec3_type_tag_census']['records_with_stream_residue']}"])

    with (OUT / "pm4z_boundary_arithmetic.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "limb_a", "limb_b", "arith", "threshold_m",
                                           "exact_decimal", "delta_vs_engine_m"])
        w.writeheader()
        for r in res["ec7_boundary_arithmetic"]["table"]:
            w.writerow(r)

    (OUT / "pm4z_digests.json").write_text(json.dumps({
        "pinned_inputs": digests,
        "instrument": {str(pathlib.Path(__file__).resolve()): sha(pathlib.Path(__file__).resolve())},
    }, indent=2, sort_keys=True) + "\n")
    (OUT / "decode.log").write_text("\n".join(log_lines) + "\n")

    emitted = {}
    for n in ("pm4z_operand.json", "pm4z_binary_anchors.json", "pm4z_type_system.csv",
              "pm4z_boundary_arithmetic.csv", "pm4z_digests.json"):
        emitted[n] = sha(OUT / n)
    print()
    print("EMITTED (sha256, full 64 hex):")
    for k, v in emitted.items():
        print(f"   {v}  {k}")


if __name__ == "__main__":
    main()
