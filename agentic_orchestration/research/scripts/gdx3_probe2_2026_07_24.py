#!/usr/bin/env python3
"""
gdx3_probe2_2026_07_24.py — Follow-up probe: playerclass10 identity + spatial outliers.

Q2b: playerclass10 — is this a genuine new player mastery or something else?
     - List all 40 record paths in records/skills/playerclass10/
     - Sample-decode a few to see skillDisplayName / skillBitmapName / templateName
Q3b: Identify which specific controller records have MaxPursuitDistance > 600 or PursuitTime > 90000
     (the out-of-envelope values). Name the paths and values.
"""
import io
import struct
import pathlib
import sys
import lz4.block

EDITION_II = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
GDX3_ARZ   = EDITION_II / "gdx3/database/GDX3.arz"

TYPE_INT32, TYPE_FLOAT32, TYPE_STRIDX, TYPE_BOOL = 0, 1, 2, 3


class ArzArchive:
    def __init__(self, path: pathlib.Path, label: str = ""):
        self.path = path
        self.label = label or path.name
        self.raw = path.read_bytes()
        self._parse_header()
        self._parse_string_table()
        self._parse_record_table()

    def _parse_header(self):
        b = self.raw
        (self.magic, self.version, self.rt_offset, self.rt_size,
         self.rt_count, self.st_offset, self.st_size) = struct.unpack_from("<HHiiiii", b, 0)
        if self.magic != 2:
            raise ValueError(f"magic={self.magic}, expected 2")

    def _parse_string_table(self):
        self.strings = []
        b = self.raw
        pos = self.st_offset
        (self.st_count,) = struct.unpack_from("<I", b, pos); pos += 4
        for _ in range(self.st_count):
            (slen,) = struct.unpack_from("<i", b, pos); pos += 4
            s = b[pos:pos + slen].decode("latin-1"); pos += slen
            self.strings.append(s)

    def _parse_record_table(self):
        self.records = {}
        pos = self.rt_offset
        end = self.rt_offset + self.rt_size
        b = self.raw
        for _ in range(self.rt_count):
            if pos >= end: break
            (name_id,) = struct.unpack_from("<i", b, pos); pos += 4
            (rt_len,) = struct.unpack_from("<i", b, pos); pos += 4
            rtype = b[pos:pos + rt_len].decode("latin-1"); pos += rt_len
            (data_offset,) = struct.unpack_from("<i", b, pos); pos += 4
            (comp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (decomp_size,) = struct.unpack_from("<i", b, pos); pos += 4
            (timestamp,) = struct.unpack_from("<q", b, pos); pos += 8
            rec_path = self.strings[name_id]
            self.records[rec_path] = dict(rtype=rtype, data_offset=data_offset,
                                          comp_size=comp_size, decomp_size=decomp_size)

    def read_record(self, rec_path: str) -> dict:
        meta = self.records[rec_path]
        base = 24 + meta["data_offset"]
        blob = self.raw[base: base + meta["comp_size"]]
        dec = lz4.block.decompress(blob, uncompressed_size=meta["decomp_size"])
        return self._decode_fields(dec)

    def _decode_fields(self, dec: bytes) -> dict:
        out = {}
        stream = io.BytesIO(dec)
        while True:
            head = stream.read(8)
            if len(head) < 8: break
            ftype, count, key_id = struct.unpack("<HHI", head)
            payload = stream.read(count * 4)
            if len(payload) < count * 4: break
            field_name = self.strings[key_id]
            vals = []
            for i in range(count):
                chunk = payload[i * 4:(i + 1) * 4]
                if ftype == TYPE_FLOAT32:
                    vals.append(struct.unpack("<f", chunk)[0])
                elif ftype == TYPE_INT32:
                    vals.append(struct.unpack("<i", chunk)[0])
                elif ftype == TYPE_BOOL:
                    vals.append(bool(struct.unpack("<I", chunk)[0]))
                elif ftype == TYPE_STRIDX:
                    vals.append(self.strings[struct.unpack("<I", chunk)[0]])
                else:
                    vals.append(struct.unpack("<i", chunk)[0])
            out[field_name] = vals[0] if count == 1 else vals
        return out


def main():
    gdx3 = ArzArchive(GDX3_ARZ, "GDX3")

    # ---- Q2b: playerclass10 identity ----
    print("=" * 70)
    print("Q2b — playerclass10 records (all 40)")
    print("=" * 70)
    pc10_paths = sorted(p for p in gdx3.records if "skills/playerclass10/" in p)
    print(f"Total: {len(pc10_paths)}")
    for p in pc10_paths:
        rtype = gdx3.records[p]["rtype"]
        print(f"  [{rtype}] {p}")

    # Sample-decode a few for skill metadata
    print("\nSample decode of first 5 playerclass10 records:")
    for path in pc10_paths[:5]:
        try:
            rec = gdx3.read_record(path)
            keys_of_interest = ["skillDisplayName", "skillBitmapName", "templateName",
                                 "skillMaxLevel", "skillUltimateLevel", "Class"]
            print(f"\n  {path}")
            for k in keys_of_interest:
                if k in rec:
                    print(f"    {k}: {rec[k]!r}")
            # also show all keys to spot new/interesting ones
            all_keys = list(rec.keys())
            print(f"    field count: {len(all_keys)}")
            # show first 10 fields not in keys_of_interest
            extra = [k for k in all_keys if k not in keys_of_interest][:10]
            print(f"    other fields (first 10): {extra}")
        except Exception as e:
            print(f"  ERROR: {path}: {e!r}")

    # ---- Q3b: spatial outliers ----
    print("\n" + "=" * 70)
    print("Q3b — GDX3 controller records with out-of-prior-envelope spatial values")
    print("      Prior envelope: MaxPursuitDistance [0, 600]; PursuitTime [0, 90000]")
    print("=" * 70)
    ctrl_paths = [p for p in gdx3.records if "controller" in p.lower()]
    outliers = []
    for path in ctrl_paths:
        try:
            rec = gdx3.read_record(path)
            mpd = rec.get("MaxPursuitDistance")
            pt = rec.get("PursuitTime")
            flags = []
            if mpd is not None and mpd > 600:
                flags.append(f"MaxPursuitDistance={mpd}")
            if pt is not None and pt > 90000:
                flags.append(f"PursuitTime={pt}")
            if flags:
                outliers.append((path, flags, rec))
        except Exception as e:
            print(f"  DECODE ERROR {path}: {e!r}")

    print(f"\nOutlier controller records: {len(outliers)}")
    for path, flags, rec in sorted(outliers):
        rtype = gdx3.records[path]["rtype"]
        print(f"\n  [{rtype}] {path}")
        for f in flags:
            print(f"    *** {f}")
        # Show all spatial fields for context
        for sf in ["ViewDistance", "InnerViewDistance", "MaxPursuitDistance", "PursuitTime",
                   "fleeDistance", "WanderDistance", "RoamDistance"]:
            if sf in rec:
                print(f"    {sf}: {rec[sf]}")

    # ---- Also: check if any base template records reference playerclass10 ----
    print("\n" + "=" * 70)
    print("playerclass10 — cross-reference: does any other GDX3 record reference 'playerclass10'?")
    print("=" * 70)
    refs = []
    for path in list(gdx3.records.keys())[:500]:  # sample check
        try:
            rec = gdx3.read_record(path)
            for k, v in rec.items():
                if isinstance(v, str) and "playerclass10" in v.lower():
                    refs.append((path, k, v))
        except Exception:
            pass
    print(f"References to 'playerclass10' in first 500 records: {len(refs)}")
    for path, k, v in refs[:10]:
        print(f"  {path}  [{k}] = {v!r}")

    # ---- Show top-level paths within playerclass10 to understand structure ----
    print("\nplayerclass10 path structure:")
    subdirs = set()
    for p in pc10_paths:
        parts = p.split("/")
        # depth-4 prefix: records/skills/playerclass10/<subdir>
        if len(parts) >= 4:
            subdirs.add(parts[3])
        else:
            subdirs.add("<root>")
    print(f"  Subdirectory names: {sorted(subdirs)}")

    # Show record type breakdown for playerclass10
    from collections import Counter
    pc10_rtypes = Counter(gdx3.records[p]["rtype"] for p in pc10_paths)
    print(f"  Record types: {dict(pc10_rtypes)}")


if __name__ == "__main__":
    main()
