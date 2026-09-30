#!/usr/bin/env python3
"""Minimal PE/COFF reader: sections, string->VA, RIP-relative LEA xref scan. READ-ONLY."""
import struct, sys, pathlib

class PE:
    def __init__(self, path):
        self.d = pathlib.Path(path).read_bytes()
        e_lfanew = struct.unpack_from('<I', self.d, 0x3c)[0]
        assert self.d[e_lfanew:e_lfanew+4] == b'PE\0\0'
        coff = e_lfanew + 4
        machine, nsec, _, _, _, optsz, _ = struct.unpack_from('<HHIIIHH', self.d, coff)
        self.machine = machine
        opt = coff + 20
        magic = struct.unpack_from('<H', self.d, opt)[0]
        self.pe32p = (magic == 0x20b)
        self.imagebase = struct.unpack_from('<Q' if self.pe32p else '<I', self.d, opt + (24 if self.pe32p else 28))[0]
        self.sections = []
        p = opt + optsz
        for _ in range(nsec):
            name = self.d[p:p+8].rstrip(b'\0').decode('latin-1')
            vsz, va, rsz, roff = struct.unpack_from('<IIII', self.d, p+8)
            self.sections.append((name, va, vsz, roff, rsz)); p += 40
    def off2va(self, off):
        for name, va, vsz, roff, rsz in self.sections:
            if roff <= off < roff + rsz: return self.imagebase + va + (off - roff)
        return None
    def va2off(self, va):
        r = va - self.imagebase
        for name, sva, vsz, roff, rsz in self.sections:
            if sva <= r < sva + max(vsz, rsz): return roff + (r - sva)
        return None
    def sec_of_va(self, va):
        r = va - self.imagebase
        for name, sva, vsz, roff, rsz in self.sections:
            if sva <= r < sva + max(vsz, rsz): return name
        return None
    def find_cstr(self, s):
        """all file offsets where NUL-terminated ASCII string s begins (preceded by NUL)."""
        b = s.encode() + b'\0'
        out, i = [], 0
        while True:
            i = self.d.find(b, i)
            if i < 0: break
            if i == 0 or self.d[i-1] == 0: out.append(i)
            i += 1
        return out
    def lea_xrefs(self, target_va):
        """scan executable sections for `lea reg,[rip+disp32]` resolving to target_va.
        also catches mov reg,[rip+disp32] style 8b/8d with REX."""
        hits = []
        for name, sva, vsz, roff, rsz in self.sections:
            if name not in ('.text', 'text', '.code'): continue
            blob = self.d[roff:roff+rsz]
            base = self.imagebase + sva
            for i in range(len(blob) - 7):
                b0 = blob[i]
                if not (0x48 <= b0 <= 0x4f): continue
                if blob[i+1] != 0x8d: continue
                modrm = blob[i+2]
                if (modrm & 0xc7) != 0x05: continue   # mod=00 rm=101 -> RIP-rel
                disp = struct.unpack_from('<i', blob, i+3)[0]
                nxt = base + i + 7
                if nxt + disp == target_va:
                    hits.append(base + i)
        return hits
