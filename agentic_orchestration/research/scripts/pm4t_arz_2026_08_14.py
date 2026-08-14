#!/usr/bin/env python3
"""
pm4t_arz_2026_08_14.py — RUN KC2-PM4 LAP T. Multi-archive GD `.arz` record reader.

WHY THIS EXISTS
    Lap T must walk `records/creatures/traps/spawnbeacon.dbr` and its FULL aura/skill/template
    chain, plus the tier-16 monster rosters' movement chain. Records live spread across EIGHT
    `.arz` archives with expansion-override semantics. The existing
    `gd_arz_adapter_2026_07_24.py` reads ONE archive for ONE record; this generalises it to a
    layered corpus index with override order, plus a reverse index (which records reference X).

    FORMAT TRUTH is UNCHANGED from the legolas probe `2026-07-23-gd-arz-extraction-probe.md` §0
    and is re-implemented here verbatim so this module stands alone (read-only, vendor tree never
    written).

READ-ONLY. Never writes to the vendor tree.
"""
import struct
import pathlib
import hashlib

import lz4.block

CORPUS = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")

# Override order: later entries WIN on identical record paths.
# Base game -> expansions in release order -> the Crucible (survivalmode) layers.
# NOTE: the override order itself is an ASSUMPTION about the engine's mod-stacking; every
# finding that depends on it says so, and § "which archive" is reported per record.
ARCHIVE_ORDER = [
    ("database.arz", CORPUS / "database" / "database.arz"),
    ("GDX1.arz", CORPUS / "gdx1" / "database" / "GDX1.arz"),
    ("GDX2.arz", CORPUS / "gdx2" / "database" / "GDX2.arz"),
    ("GDX3.arz", CORPUS / "gdx3" / "database" / "GDX3.arz"),
    ("SurvivalMode.arz", CORPUS / "mods" / "survivalmode" / "database" / "SurvivalMode.arz"),
    ("SurvivalMode1.arz", CORPUS / "survivalmode1" / "database" / "SurvivalMode1.arz"),
    ("SurvivalMode2.arz", CORPUS / "survivalmode2" / "database" / "SurvivalMode2.arz"),
    ("SurvivalMode3.arz", CORPUS / "survivalmode3" / "database" / "SurvivalMode3.arz"),
]

FIELD_TYPE_INT = 0
FIELD_TYPE_FLOAT = 1
FIELD_TYPE_STR = 2
FIELD_TYPE_BOOL = 3


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Arz:
    """One `.arz` archive. TQIT variant (magic=2)."""

    def __init__(self, path, label=None):
        self.path = pathlib.Path(path)
        self.label = label or self.path.name
        self.blob = self.path.read_bytes()
        self._parse_header()
        self._parse_string_table()
        self._parse_record_table()

    def _parse_header(self):
        (self.magic, self.version, self.rt_offset, self.rt_size,
         self.rt_count, self.st_offset, self.st_size) = struct.unpack_from("<HHiiiii", self.blob, 0)
        if self.magic != 2:
            raise ValueError(f"{self.label}: unexpected magic {self.magic}")

    def _parse_string_table(self):
        buf = self.blob[self.st_offset:self.st_offset + self.st_size]
        pos = 0
        n = struct.unpack_from("<i", buf, pos)[0]
        pos += 4
        out = []
        for _ in range(n):
            ln = struct.unpack_from("<i", buf, pos)[0]
            pos += 4
            out.append(buf[pos:pos + ln].decode("latin-1"))
            pos += ln
        self.strings = out

    def _parse_record_table(self):
        buf = self.blob
        pos = self.rt_offset
        self.index = {}
        for _ in range(self.rt_count):
            name_id = struct.unpack_from("<i", buf, pos)[0]
            pos += 4
            tlen = struct.unpack_from("<i", buf, pos)[0]
            pos += 4
            rtype = buf[pos:pos + tlen].decode("latin-1")
            pos += tlen
            off, comp, decomp = struct.unpack_from("<iii", buf, pos)
            pos += 12
            pos += 8  # timestamp i64
            self.index[self.strings[name_id].lower()] = (rtype, off, comp, decomp)

    def has(self, rec_path):
        return rec_path.lower().replace("\\", "/") in self.index

    def record_type(self, rec_path):
        return self.index[rec_path.lower().replace("\\", "/")][0]

    def read(self, rec_path):
        key = rec_path.lower().replace("\\", "/")
        rtype, off, comp, decomp = self.index[key]
        blob = self.blob[24 + off:24 + off + comp]
        dec = lz4.block.decompress(blob, uncompressed_size=decomp)
        return self._decode_fields(dec)

    def _decode_fields(self, dec):
        out = {}
        pos = 0
        n = len(dec)
        while pos + 8 <= n:
            ftype, count, key_id = struct.unpack_from("<HHI", dec, pos)
            pos += 8
            vals = []
            for i in range(count):
                raw = dec[pos:pos + 4]
                pos += 4
                if len(raw) < 4:
                    break
                if ftype == FIELD_TYPE_INT:
                    vals.append(struct.unpack("<i", raw)[0])
                elif ftype == FIELD_TYPE_FLOAT:
                    vals.append(struct.unpack("<f", raw)[0])
                elif ftype == FIELD_TYPE_STR:
                    idx = struct.unpack("<I", raw)[0]
                    vals.append(self.strings[idx] if idx < len(self.strings) else f"<oob:{idx}>")
                elif ftype == FIELD_TYPE_BOOL:
                    vals.append(bool(struct.unpack("<I", raw)[0]))
                else:
                    vals.append(struct.unpack("<I", raw)[0])
            if key_id < len(self.strings):
                out[self.strings[key_id]] = vals[0] if len(vals) == 1 else vals
        return out


class Corpus:
    """Layered index across the eight archives. Later archives override earlier ones."""

    def __init__(self, order=None):
        self.archives = []
        self.digests = {}
        for label, p in (order or ARCHIVE_ORDER):
            if not p.exists():
                continue
            self.archives.append(Arz(p, label))
            self.digests[label] = sha256(p)
        # resolution map: record path -> (archive_label, archive_object)
        self.resolve = {}
        self.all_layers = {}
        for a in self.archives:
            for k in a.index:
                self.resolve[k] = a
                self.all_layers.setdefault(k, []).append(a.label)

    def has(self, rec_path):
        return rec_path.lower().replace("\\", "/") in self.resolve

    def owner(self, rec_path):
        return self.resolve[rec_path.lower().replace("\\", "/")].label

    def layers(self, rec_path):
        return self.all_layers.get(rec_path.lower().replace("\\", "/"), [])

    def read(self, rec_path):
        key = rec_path.lower().replace("\\", "/")
        return self.resolve[key].read(key)

    def record_type(self, rec_path):
        key = rec_path.lower().replace("\\", "/")
        return self.resolve[key].record_type(key)

    def paths(self):
        return list(self.resolve.keys())

    def find(self, *substrings):
        subs = [s.lower() for s in substrings]
        return sorted(p for p in self.resolve if all(s in p for s in subs))


def walk_chain(corpus, root, max_depth=6, dbr_only=True):
    """BFS the record graph from `root` following every field value that ends in `.dbr`.

    Returns dict: record_path -> {"depth", "owner", "type", "fields", "parents"}
    """
    seen = {}
    frontier = [(root.lower(), 0, None, None)]
    while frontier:
        path, depth, parent, via = frontier.pop(0)
        path = path.replace("\\", "/")
        if path in seen:
            seen[path]["parents"].append((parent, via))
            continue
        if not corpus.has(path):
            seen[path] = {"depth": depth, "owner": None, "type": None,
                          "fields": None, "parents": [(parent, via)], "missing": True}
            continue
        fields = corpus.read(path)
        seen[path] = {"depth": depth, "owner": corpus.owner(path),
                      "type": corpus.record_type(path), "fields": fields,
                      "parents": [(parent, via)], "missing": False}
        if depth >= max_depth:
            continue
        for k, v in fields.items():
            vals = v if isinstance(v, list) else [v]
            for x in vals:
                if isinstance(x, str) and x.lower().endswith(".dbr"):
                    frontier.append((x.lower(), depth + 1, path, k))
    return seen
