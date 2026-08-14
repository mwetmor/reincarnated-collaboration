#!/usr/bin/env python3
"""KC2-PM4 Lap S — minimal, dependency-free PE32 export-table reader + objdump bridge.

WHY THIS EXISTS
    Lap J (`pathMass`, 2026-08-14) proved the method: the shipped Grim Dawn modules are PE32
    (`coff-i386`) with FULL MSVC-decorated export tables, so a named C++ member function can be
    located by RVA and disassembled directly out of the shipped bytes with `objdump`.  Lap J's
    parser lived in `/tmp` scratch and did not survive; this file is the durable version, so
    Lap S's `characterRunSpeedJitter` decode is reproducible.

    RE-IMPLEMENTS NOTHING ELSE: the ARC/ARZ readers are imported where needed, never copied.

READ-ONLY on `/Users/admin/Games/vendor/grim-dawn/`.  Never writes to the vendor tree.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap S.
"""
from __future__ import annotations

import hashlib
import pathlib
import struct
import subprocess
from typing import Dict, List, Optional, Tuple

GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class PE32:
    """Just enough PE32 to map RVA<->file offset and read the export directory."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.raw = self.path.read_bytes()
        b = self.raw
        if b[:2] != b"MZ":
            raise ValueError(f"BLOCKED-FORMAT: not MZ ({path})")
        pe_off = struct.unpack_from("<I", b, 0x3C)[0]
        if b[pe_off:pe_off + 4] != b"PE\0\0":
            raise ValueError(f"BLOCKED-FORMAT: no PE signature ({path})")
        self.pe_off = pe_off
        (self.machine, self.n_sections, _, _, _, self.opt_size,
         self.characteristics) = struct.unpack_from("<HHIIIHH", b, pe_off + 4)
        opt = pe_off + 24
        self.magic = struct.unpack_from("<H", b, opt)[0]
        if self.magic != 0x10B:
            raise ValueError(f"BLOCKED-FORMAT: only PE32 (0x10B) mapped, got {self.magic:#x}")
        self.image_base = struct.unpack_from("<I", b, opt + 28)[0]
        n_dirs = struct.unpack_from("<I", b, opt + 92)[0]
        self.dirs = []
        for i in range(n_dirs):
            self.dirs.append(struct.unpack_from("<II", b, opt + 96 + 8 * i))
        sec = opt + self.opt_size
        self.sections = []
        for i in range(self.n_sections):
            name, vsize, vaddr, rsize, raddr = struct.unpack_from("<8sIIII", b, sec + 40 * i)
            self.sections.append(dict(name=name.rstrip(b"\0").decode("latin-1"),
                                      vsize=vsize, vaddr=vaddr, rsize=rsize, raddr=raddr))

    # ---------------------------------------------------------------- addressing
    def rva_to_off(self, rva: int) -> Optional[int]:
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
                d = rva - s["vaddr"]
                if d < s["rsize"]:
                    return s["raddr"] + d
                return None
        return None

    def off_to_rva(self, off: int) -> Optional[int]:
        for s in self.sections:
            if s["raddr"] <= off < s["raddr"] + s["rsize"]:
                return s["vaddr"] + (off - s["raddr"])
        return None

    def section_of_rva(self, rva: int) -> Optional[dict]:
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
                return s
        return None

    # ---------------------------------------------------------------- exports
    def exports(self) -> Dict[str, int]:
        """decorated-name -> RVA."""
        if hasattr(self, "_exp"):
            return self._exp
        out: Dict[str, int] = {}
        if not self.dirs or self.dirs[0][1] == 0:
            self._exp = out
            return out
        d_rva, _ = self.dirs[0]
        off = self.rva_to_off(d_rva)
        if off is None:                       # e.g. `Grim Dawn.exe` — no export directory
            self._exp = out
            return out
        b = self.raw
        # Export Directory Table is 40 bytes / 11 fields.  The `Name RVA` at +12 is easy to drop
        # by miscount, which silently yields name pointers that resolve into .text — self-caught
        # here on the first run (the "exports" came back as raw x86 byte strings).
        (_char, _ts, _maj, _min, _name_rva, ordinal_base, n_funcs, n_names,
         addr_funcs, addr_names, addr_ords) = struct.unpack_from("<IIHHIIIIIII", b, off)
        f_off = self.rva_to_off(addr_funcs)
        n_off = self.rva_to_off(addr_names)
        o_off = self.rva_to_off(addr_ords)
        if None in (f_off, n_off, o_off):     # malformed/absent table (`Grim Dawn.exe`)
            self._exp = out
            return out
        for i in range(n_names):
            name_rva = struct.unpack_from("<I", b, n_off + 4 * i)[0]
            no = self.rva_to_off(name_rva)
            end = b.index(b"\0", no)
            name = b[no:end].decode("latin-1")
            ordv = struct.unpack_from("<H", b, o_off + 2 * i)[0]
            frva = struct.unpack_from("<I", b, f_off + 4 * ordv)[0]
            out[name] = frva
        self._exp = out
        return out

    def find(self, needle: str) -> List[Tuple[str, int]]:
        return sorted((n, r) for n, r in self.exports().items() if needle in n)

    # ---------------------------------------------------------------- disassembly
    def disasm(self, rva: int, nbytes: int = 0x200) -> str:
        """objdump the byte range at `rva`, VMA-corrected so branch targets read as RVAs."""
        off = self.rva_to_off(rva)
        if off is None:
            raise ValueError(f"rva {rva:#x} is not file-backed")
        cmd = ["objdump", "-d", "--x86-asm-syntax=intel",
               f"--start-address={hex(self.image_base + rva)}",
               f"--stop-address={hex(self.image_base + rva + nbytes)}",
               str(self.path)]
        return subprocess.run(cmd, capture_output=True, text=True).stdout

    def sym_at(self, rva: int) -> Optional[str]:
        """Reverse lookup: which exported symbol starts at this RVA."""
        if not hasattr(self, "_rev"):
            self._rev = {}
            for n, r in self.exports().items():
                self._rev.setdefault(r, n)
        return self._rev.get(rva)


def modules() -> Dict[str, PE32]:
    return {n: PE32(GD / n) for n in ("Game.dll", "Engine.dll", "Grim Dawn.exe")}


if __name__ == "__main__":
    import sys
    for name, pe in modules().items():
        print(f"{name}: machine={pe.machine:#x} base={pe.image_base:#x} "
              f"sections={pe.n_sections} exports={len(pe.exports())} sha256={sha256(pe.path)}")
    if len(sys.argv) > 1:
        for name, pe in modules().items():
            for n, r in pe.find(sys.argv[1]):
                print(f"  {name}  {r:#010x}  {n}")
