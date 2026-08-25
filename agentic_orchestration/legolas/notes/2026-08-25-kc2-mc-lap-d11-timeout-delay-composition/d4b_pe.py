"""Minimal READ-ONLY PE32 reader: sections + export directory. Hand-rolled (no pefile dependency)
so nothing is installed into the environment and nothing is written to the vendor tree."""
import struct, pathlib

class PE32:
    def __init__(self, path):
        self.path = pathlib.Path(path); self.raw = self.path.read_bytes()
        b = self.raw
        e_lfanew = struct.unpack_from('<I', b, 0x3C)[0]
        assert b[e_lfanew:e_lfanew+4] == b'PE\0\0', 'not PE'
        coff = e_lfanew + 4
        (self.machine, self.nsec, _, _, _, self.opt_size, _) = struct.unpack_from('<HHIIIHH', b, coff)
        opt = coff + 20
        self.magic = struct.unpack_from('<H', b, opt)[0]
        assert self.magic == 0x10b, f'not PE32 (magic={self.magic:#x})'
        self.image_base = struct.unpack_from('<I', b, opt+28)[0]
        nrva = struct.unpack_from('<I', b, opt+92)[0]
        self.dirs = [struct.unpack_from('<II', b, opt+96+8*i) for i in range(nrva)]
        sh = opt + self.opt_size
        self.sections = []
        for i in range(self.nsec):
            o = sh + 40*i
            name = b[o:o+8].rstrip(b'\0').decode('latin-1')
            vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', b, o+8)
            self.sections.append(dict(name=name, vaddr=vaddr, vsize=vsize, raddr=raddr, rsize=rsize))

    def rva2off(self, rva):
        for s in self.sections:
            if s['vaddr'] <= rva < s['vaddr'] + max(s['vsize'], s['rsize']):
                return s['raddr'] + (rva - s['vaddr'])
        return None

    def at(self, rva, n):
        o = self.rva2off(rva)
        return None if o is None else self.raw[o:o+n]

    def cstr(self, rva):
        o = self.rva2off(rva); e = self.raw.index(b'\0', o)
        return self.raw[o:e].decode('latin-1')

    def exports(self):
        """name -> rva  (and ordinal -> rva)."""
        erva, esz = self.dirs[0]
        if not erva: return {}, {}
        o = self.rva2off(erva)
        # IMAGE_EXPORT_DIRECTORY = Characteristics, TimeDateStamp, MajorVer(H), MinorVer(H),
        # Name, Base, NumberOfFunctions, NumberOfNames, AddressOfFunctions, AddressOfNames,
        # AddressOfNameOrdinals -> ELEVEN fields (the first bring-up dropped MinorVersion and
        # shifted every subsequent RVA by one slot; recorded so the next reader does not repeat it).
        (_, _, _, _, name_rva, ordbase, naddr, nnames,
         addr_rva, names_rva, ord_rva) = struct.unpack_from('<IIHHIIIIIII', self.raw, o)
        self.dll_name = self.cstr(name_rva)
        addrs = struct.unpack_from(f'<{naddr}I', self.raw, self.rva2off(addr_rva))
        npt   = struct.unpack_from(f'<{nnames}I', self.raw, self.rva2off(names_rva))
        ords  = struct.unpack_from(f'<{nnames}H', self.raw, self.rva2off(ord_rva))
        byname = {}
        for i in range(nnames):
            byname[self.cstr(npt[i])] = addrs[ords[i]]
        return byname, dict(export_dir=(erva, esz), n_addr=naddr, n_names=nnames, ordbase=ordbase)
