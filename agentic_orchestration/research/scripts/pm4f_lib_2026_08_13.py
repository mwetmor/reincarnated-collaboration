#!/usr/bin/env python3
"""KC2-PM4 Lap F shared library -- GIVE THE BODIES THEIR SPACE BACK (per-record collision radii).

READ-ONLY on the vendor corpus, the engine tree, every baton, and every emission of every prior lap.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE QUESTION (charter L-4, Iteration 3)
═══════════════════════════════════════════════════════════════════════════════════════════════

The sim's player-weapon hit-test treats every body as a POINT (`entity_radius_m = None` on all 188
baton actors).  gamora's I-2 landing note § 5.3 measured the consequence: the 3.0 m EoR disc holds
up to **54 co-resident bodies** where hexagonal packing of half-metre bodies caps ~32, and 8.3 % of
the reference cell's kill work happens above that ceiling.  The conductor ruled Iteration 3 =
"occupancy -- give the bodies their space back", bounded by MEASURED geometry.

THIS LAP SUPPLIES THE GEOMETRY.  It answers four questions, and it answers two of them by DECLARING
a dead end rather than by estimating past it (GL-12).

═══════════════════════════════════════════════════════════════════════════════════════════════
THE DECODE, LINK BY LINK -- every citation checked first-hand, none adopted
═══════════════════════════════════════════════════════════════════════════════════════════════

F1. ⚑ THE FIELD EXISTS, AND IT IS ON EVERY BODY.  `database/templates.arc -> actor.tpl` declares
    FOUR co-located geometry variables in one template:

        actorRadius     real     defaultValue "0"                    <- THE RADIUS
        actorHeight     real     defaultValue "0"
        collisionShape  picklist defaultValue "Box;Sphere;Cylinder;Capsule"
        scale           real     defaultValue "1"

    `collisionShape` is the decisive co-location: `actorRadius`/`actorHeight` are the parameters of
    a collision PRIMITIVE, not an aggro/audio/light radius.  The corpus keeps those separate and
    suffixed -- `MonsterMusicRadius`, `characterLightRadius`, `npcAlertRadius`, `npcSocialRadius`,
    `skillTargetRadius`.  `actorRadius` is the un-suffixed geometric radius of the actor itself.

    THE INCLUDE CHAIN, walked from the templates (not assumed):
        monster.tpl -> Character.tpl -> Actor.tpl        (14-template closure)
        pet.tpl     -> Monster.tpl -> ...                (15-template closure)
        player.tpl  -> ... -> Actor.tpl
    so every body on this board inherits the four fields.  MEASURED: present on 297/297 board
    records AND on the player record.

F2. THE SECOND, INDEPENDENT SIZE SURFACE -- `character.tpl` declares

        pathingSize   picklist  defaultValue "Small;Medium;Large"
        pathMass      real      defaultValue "1.0"

    the navmesh footprint CLASS.  It is not a length, so it cannot be the radius; it CORROBORATES
    `actorRadius` -- over the 297 board records the class medians are Small 0.400 / Medium 0.750 /
    Large 1.000, and over all 3,070 corpus `Class = Monster` records 0.400 / 0.700 / 1.000.

F3. ⚑ THE UNIT, PROVED FROM THE GAME'S OWN UI STRINGS -- NOT ASSERTED.
    `resources/Text_EN.arc -> tags_ui.txt` carries

        SkillDistanceFormat={%.1f0 {^E}Meter %s1}
        TargetRadius=Target Area

    i.e. the game prints a RAW DB length scalar, to one decimal, immediately followed by the
    literal word "Meter", with NO conversion factor anywhere in the format string.  A skill whose
    `skillTargetRadius` is 2.5 renders as "2.5 Meter Target Area".  ⇒ **one DB length unit is one
    metre, by the game's own display contract.**

    The sim already rides this identity twice, 1:1 and unconverted:
        gameengine.dbr `meleeTargetDistance` = 2.4000000953674316  ->  locomotion.D_ENGAGE_M = 2.4
        EoR skill      `skillTargetRadius`   = 3.0                  ->  fixture.EOR_RADIUS_M = 3.0
    so `actorRadius` -- a `real` in the same corpus, on the same template family -- is
    COMMENSURABLE WITH THE DISC RADIUS WITHOUT CONVERSION.  Nothing is rescaled in this lap.

F4. ⚑ `scale` -- THE ONE LIMB THIS LAP CANNOT DECIDE, AND IT IS DECLARED, NOT ESTIMATED.
    `actor.tpl:scale` has an EMPTY description.  Two readings survive every test I could build:

      (i)  world radius = actorRadius            (`scale` is mesh/render scale only)
      (ii) world radius = actorRadius x scale    (the engine scales the collision primitive)

    FOUR discriminators were built and run.  Reported in full, including the two that FAILED to
    discriminate and the one whose counter-evidence I went looking for and found:

      D1  AUTHORING INVARIANCE.  Over 189 mesh-groups (>=3 records, varying `scale`):
          104 hold `actorRadius` CONSTANT while `scale` varies; **ZERO** hold `actorRadius/scale`
          constant.  ⇒ `actorRadius` is authored PER-MESH, never re-authored per scale.  This
          EXCLUDES "actorRadius is a hand-authored world-space radius", but does NOT choose between
          (i) and (ii).

      D2  MESH BOUNDING BOX.  First-of-kind here: `resources/Creatures.arc -> *.msh` is an
          8-byte-header chunk container (`MSH\\x03` + [chunkID u32][len u32][payload]); chunk **10**
          is 24 bytes = 6 floats = the mesh AABB (min xyz, max xyz).  Walked cleanly on 278/297
          board meshes with exact byte coverage.  **INCONCLUSIVE**: `actorRadius / mesh_half_Z` has
          median 0.499 and IQR 0.275-1.169; multiplying by `scale` moves it to 0.666 / 0.309-1.443.
          Neither lands on 1.0, because the bind-pose AABB includes arms, wings and weapons.  ⚑ The
          mesh AABB DOES NOT DISCRIMINATE, and it is reported as a failed discriminator, not
          quietly dropped.

      D3  pathingSize CONCORDANCE over 3,070 corpus monsters.  Goodman-Kruskal gamma against the
          ordinal class: raw **0.5413**, scaled **0.5516**.  A 0.010 difference.  **INCONCLUSIVE.**

      D4  ⚑ pathingSize AT CONSTANT (mesh, actorRadius) -- the one that produced a signal, AND the
          counter-evidence that kills it.  Only TWO such groups vary in `pathingSize`, and on both
          the LARGER `scale` carries the LARGER class (5/5 cross-class pairs agree, 0 disagree):
              raptorwinged01.msh, actorRadius 0.55: scale 0.40 juvenile -> Small;
                                                    scale 0.65/0.90/1.00 -> Medium
              possessedstatue_m_01a.msh, actorRadius 0.75: scale 2.5 -> Medium; scale 3.0 -> Large
          **BUT** 545 groups hold `pathingSize` CONSTANT, and **37 of them span >= 1.5x in `scale`**
          (max 3.87x, `prawnb01.msh`).  So the authors' own class does NOT reliably track `scale`.
          **5 agreeing pairs against 37 disagreeing groups is not a decode.  DECLARED.**

    ⇒ THIS LAP EMITS BOTH LIMBS AND RULES NEITHER, exactly as Lap D/E emitted LO/HI:
          radius_m     = actorRadius            grade MEASURED   (LO limb)
          radius_m_hi  = actorRadius * scale    grade DERIVED    (HI limb)
    **The conductor rules which limb Iteration 3 runs.**  Both are in the CSV, by explicit column,
    never by row order (R-PM4-2's law, carried).

F5. COLLISION SEMANTICS -- PARTIALLY DECODABLE, AND THE UNDECODABLE PART IS NAMED.
    `monster.tpl` declares exactly two collision fields, and their DESCRIPTIONS are the finding:

        forceCollision    bool  "force collision (ignores hostility)"
        forceNoCollision  bool  "force no collision (ignores hostility)"

    ⚑ Both descriptions say **"ignores hostility"**, which is the template corpus telling us that
    the BASE character-vs-character collision rule is a function of the HOSTILITY RELATION between
    the two bodies.  These two fields are the OVERRIDES.  **The base rule itself is engine-internal:
    there is no hostility->collision table, no collision-category field, and no collision-layer
    record anywhere in the corpus.**  DECLARED-GAP with the dead end named.  Per-record override
    flags ARE decodable and are emitted.

    `collisionShape` is set on **0 of the 297** board records (1,004 corpus records DO set it --
    Box 583 / Sphere 392 / Capsule 11 / Cylinder 9), so all 297 take an engine default whose value
    is likewise not in the data: a picklist `defaultValue` enumerates the OPTIONS, it does not name
    a default.  DECLARED, second dead end named.

F6. NO WAVE / DIFFICULTY / CHAMPION MODIFIER SCALES BODY SIZE ON THIS BOARD -- MEASURED ABSENCE.
      * `attributepak.tpl` carries 11 declared names, ZERO geometric.
      * `gameadjustment.tpl` (the Crucible survival term's own template) = attributepak +
        `spawnMinAdj` / `spawnMaxAdj` / `spawnChampionMinAdj` / `spawnChampionMaxAdj` -- four spawn
        **COUNT** fields.  ZERO geometric.
      * Across all **819** templates the ONLY runtime body-scale field pair is `actorScale` /
        `actorScaleTime` on **`skill_buffselfcolossus.tpl`** (`Class = Skill_BuffSelfColossus`).
        Corpus-wide it is carried by exactly **4** records (salazar_possession1 1.20,
        cultist_possession1 1.20, theforsaken_overflowingrage 1.50, and the base template 1.80),
        and **ZERO of the 297 board bodies carries any of them.**
      * Champion / hero bodies are SEPARATE `.dbr` records with their OWN `actorRadius` and `scale`
        (they are already rows in this table), so the champion limb needs no multiplier.
    ⇒ Q2 = MEASURED-ABSENT.  Body size on the E-s09-cp150 board is a pure per-record constant.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, iteration I-3, Lap F.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import pathlib
import re
import struct
import sys
from typing import Dict, List, Optional, Sequence, Set, Tuple

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

# Lap D's library (which imports band A's chain) and Lap E's population closure. RE-IMPLEMENTS
# NOTHING: same reader (`E3.winner`, whole-record replacement), same populations, same basis names.
from pm4d_lib_2026_08_13 import E3, rolled_records, sha256_of              # noqa: E402
from pm4e_lib_2026_08_13 import summon_only_bodies                          # noqa: E402
from gd_arc_reader_2026_07_26 import ArcArchive                             # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")

BAND_B_FIRST_W, BAND_B_LAST_W = 151, 170

# ── the template + text containers (READ from bytes, never extracted into the vendor tree) ──────
TEMPLATES_ARC = VENDOR / "database" / "templates.arc"
TEXT_ARCS = ["resources/Text_EN.arc", "gdx1/resources/Text_EN.arc",
             "gdx2/resources/Text_EN.arc", "gdx3/resources/Text_EN.arc",
             "mods/survivalmode/resources/Text_EN.arc"]
CREATURE_ARCS = ["resources/Creatures.arc", "gdx1/resources/Creatures.arc",
                 "gdx2/resources/Creatures.arc", "gdx3/resources/Creatures.arc",
                 "mods/survivalmode/resources/Creatures.arc"]

#: F1 -- the four `actor.tpl` geometry variables and the two `character.tpl` footprint variables.
GEOM_FIELDS = ("actorRadius", "actorHeight", "collisionShape", "scale")
FOOTPRINT_FIELDS = ("pathingSize", "pathMass", "physicsMass", "physicsFriction")
#: F5 -- the two `monster.tpl` collision overrides.
COLLISION_FIELDS = ("forceCollision", "forceNoCollision")

#: F3 -- the unit proof.
UNIT_TAG_FILE = "tags_ui.txt"
UNIT_TAG_KEYS = ("SkillDistanceFormat", "SkillDistanceFormatMod", "TargetRadius")

#: F6 -- the only runtime body-scale template in the corpus.
COLOSSUS_CLASS = "Skill_BuffSelfColossus"

#: Q4 -- the player.  Both sexes are read; they are identical on every geometry field (asserted).
PLAYER_RECORDS = ("records/creatures/pc/malepc01.dbr", "records/creatures/pc/femalepc01.dbr")
#: Which one the fixture runs.  DECLARED: the two are byte-identical on all six geometry fields,
#: so the choice is immaterial and is recorded rather than hidden.
PLAYER_RECORD_OF_RECORD = "records/creatures/pc/malepc01.dbr"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F1 -- THE TEMPLATE SURFACE, DECODED FROM `templates.arc` (never spelled from memory)
# ══════════════════════════════════════════════════════════════════════════════════════════════

_VAR_RE = re.compile(r"Variable\s*\{[^{}]*\}", re.S)
_KV_RE = re.compile(r'(\w[\w ]*)\s*=\s*"([^"]*)"')


class Templates:
    """`templates.arc` reader.  Decodes Variable blocks and the `Include File` graph."""

    def __init__(self, path: pathlib.Path = TEMPLATES_ARC) -> None:
        self.arc = ArcArchive(path)
        self._raw: Dict[str, str] = {}
        self.failed: List[str] = []
        for n in self.arc.names():
            try:
                self._raw[self._key(n)] = self.arc.read_file(n).decode("utf-8", "replace")
            except Exception:
                self.failed.append(n)

    @staticmethod
    def _key(name: str) -> str:
        """`templatebase/foo.tpl` and `database\\Templates\\TemplateBase\\Foo.tpl` -> one key."""
        p = str(name).replace("\\", "/").lower().split("/")
        if len(p) >= 2 and p[-2] in ("templatebase", "backup", "engine", "menu"):
            return p[-2] + "/" + p[-1]
        return p[-1]

    def has(self, tpl: str) -> bool:
        return self._key(tpl) in self._raw

    def variables(self, tpl: str) -> List[Dict[str, str]]:
        t = self._raw.get(self._key(tpl), "")
        out = []
        for m in _VAR_RE.finditer(t):
            out.append({k.strip(): v for k, v in _KV_RE.findall(m.group(0))})
        return out

    def declare(self, tpl: str, field: str) -> Optional[Dict[str, str]]:
        for v in self.variables(tpl):
            if v.get("name") == field:
                return v
        return None

    def includes(self, tpl: str) -> List[str]:
        return [self._key(v["defaultValue"]) for v in self.variables(tpl)
                if v.get("type") == "include" and v.get("defaultValue")]

    def closure(self, root: str) -> List[str]:
        """Breadth-first `Include File` closure.  Order is the walk order, deterministic."""
        seen: List[str] = []
        stack = [self._key(root)]
        while stack:
            f = stack.pop(0)
            if f in seen or f not in self._raw:
                continue
            seen.append(f)
            stack.extend(self.includes(f))
        return seen

    def declaring_templates(self, field: str) -> List[str]:
        return sorted(k for k in self._raw if self.declare(k, field) is not None)

    def all_field_names(self) -> Set[str]:
        out: Set[str] = set()
        for k in self._raw:
            for v in self.variables(k):
                if v.get("name"):
                    out.add(v["name"])
        return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F3 -- THE UNIT PROOF, read out of the game's own UI strings
# ══════════════════════════════════════════════════════════════════════════════════════════════

def unit_format_strings() -> List[Tuple[str, str, str]]:
    """`[(arc, tag, value)]` for the tags that prove a raw DB length scalar prints as metres."""
    out: List[Tuple[str, str, str]] = []
    for rel in TEXT_ARCS:
        p = VENDOR / rel
        if not p.exists():
            continue
        arc = ArcArchive(p)
        for n in arc.names():
            if pathlib.Path(n).name.lower() != UNIT_TAG_FILE:
                continue
            try:
                body = arc.read_file(n).decode("utf-8-sig", "replace")
            except Exception:
                continue
            for line in body.splitlines():
                if "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() in UNIT_TAG_KEYS:
                    out.append((rel, k.strip(), v.strip()))
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F4 / D2 -- THE MESH AABB.  First-of-kind `.msh` chunk decode in this lineage.
# ══════════════════════════════════════════════════════════════════════════════════════════════

MSH_MAGIC = b"MSH\x03"
MSH_BBOX_CHUNK_ID = 10
MSH_BBOX_CHUNK_LEN = 24


class MeshIndex:
    """`creatures/<path>.msh -> AABB`, over the five `Creatures.arc` containers.

    ⚑ FORMAT, SOLVED HERE, NOT ADOPTED.  `MSH\\x03` magic, then a flat chunk list:
    `[chunkID u32][payloadLen u32][payload]`.  Chunk **10** is 24 bytes = 6 little-endian floats,
    `(minX, minY, minZ, maxX, maxY, maxZ)` in MESH space, Y up.  Verified by exact byte coverage:
    the walk consumes every byte of every file it reads with no residue.

    ⚑ AND IT DID NOT ANSWER THE QUESTION (F4 / D2).  The bind-pose AABB includes arms, wings and
    weapons, so it is not a body-width proxy.  It is emitted because a failed discriminator that is
    published is evidence, and one that is deleted is a silent estimate.
    """

    def __init__(self) -> None:
        self._idx: Dict[str, Tuple[str, ArcArchive, str]] = {}
        self.arc_counts: Dict[str, int] = {}
        for rel in CREATURE_ARCS:
            p = VENDOR / rel
            if not p.exists():
                continue
            arc = ArcArchive(p)
            n_msh = 0
            for n in arc.names():
                if n.lower().endswith(".msh"):
                    # the .dbr `mesh` field is rooted at `creatures/`; the arc is rooted inside it
                    self._idx["creatures/" + n.replace("\\", "/").lower()] = (rel, arc, n)
                    n_msh += 1
            self.arc_counts[rel] = n_msh

    def __len__(self) -> int:
        return len(self._idx)

    @staticmethod
    def _chunks(d: bytes) -> Tuple[List[Tuple[int, int, int]], bool]:
        """`([(chunkID, len, payload_offset)], exact_byte_coverage)`."""
        if d[:4] != MSH_MAGIC:
            return [], False
        off, out = 4, []
        while off + 8 <= len(d):
            cid, ln = struct.unpack_from("<II", d, off)
            out.append((cid, ln, off + 8))
            off += 8 + ln
        return out, off == len(d)

    def aabb(self, mesh: str) -> Optional[Tuple[Tuple[float, ...], str, bool]]:
        """`((minx,miny,minz,maxx,maxy,maxz), arc, exact_coverage)` or None."""
        e = self._idx.get(str(mesh).replace("\\", "/").lower())
        if not e:
            return None
        rel, arc, name = e
        try:
            d = arc.read_file(name)
        except Exception:
            return None
        chunks, exact = self._chunks(d)
        for cid, ln, o in chunks:
            if cid == MSH_BBOX_CHUNK_ID and ln == MSH_BBOX_CHUNK_LEN:
                return struct.unpack_from("<6f", d, o), rel, exact
        return None


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE POPULATIONS -- NOTE-9: every count names what it counts over
# ══════════════════════════════════════════════════════════════════════════════════════════════

def populations() -> Tuple[List[str], List[str], List[str]]:
    """`(P-ROLLED-20 records, P-SUMMON-128, the union)`.

    Both are IMPORTED, not re-derived: `P-ROLLED-20` is Lap D's frozen-baton roll over waves
    151-170 (169 records / 344 actors) and `P-SUMMON-128` is Lap E's summon-only closure.  A third
    population definition is a third thing that can drift.
    """
    roster = sorted(rolled_records(first=BAND_B_FIRST_W, last=BAND_B_LAST_W).keys())
    summon, _missed = summon_only_bodies()
    return roster, sorted(summon), sorted(set(roster) | set(summon))


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE ROW -- one body's geometry, MEASURED
# ══════════════════════════════════════════════════════════════════════════════════════════════

BODY_COLS = (
    "record", "population", "radius_m", "radius_m_hi", "radius_source_field",
    "radius_source_template", "grade", "grade_hi", "collision_flag", "body_kind",
    "actor_radius_raw", "actor_scale", "actor_height", "collision_shape",
    "pathing_size", "path_mass", "physics_mass",
    "force_collision", "force_no_collision", "monster_class", "template_name", "archive",
    "mesh", "mesh_aabb_half_x", "mesh_aabb_half_z", "mesh_aabb_height", "mesh_arc",
    "basis",
)


def body_row(record: str, population: str, meshes: MeshIndex) -> Dict[str, object]:
    r, arc = E3.winner(record)
    if r is None:
        return dict(record=record, population=population, radius_m="", radius_m_hi="",
                    radius_source_field="", radius_source_template="",
                    grade="DECLARED-GAP", grade_hi="DECLARED-GAP",
                    collision_flag="", body_kind="",
                    basis="GAP:RECORD-ABSENT-FROM-EDITION-III")

    def num(f):
        v = r.get(f)
        return None if v is None else float(v)

    ar, sc, ah = num("actorRadius"), num("scale"), num("actorHeight")
    fc, fnc = r.get("forceCollision"), r.get("forceNoCollision")
    shape = r.get("collisionShape")

    if ar is None:
        grade, basis = "DECLARED-GAP", "GAP:NO-actorRadius-ON-RECORD"
        lo = hi = ""
    else:
        grade = "MEASURED"
        # ⚑ NO ROUNDING.  The corpus stores float32 (`0.3499999940395355`); rounding it to a
        # pretty 0.35 is a modification of a measured quantity, and the no-estimate audit is
        # written to catch exactly that.  The pretty value is the reader's job, not the file's.
        lo = repr(ar)
        hi = repr(ar * (sc if sc is not None else 1.0))
        basis = ("MEASURED:actor.tpl actorRadius @Edition-III/%s"
                 " | HI = x scale (DERIVED, F4 undecided)" % (arc or "?"))

    # F5 -- the per-record override, and the base rule DECLARED as engine-internal.
    if str(fnc) == "True":
        flag = "FORCE-NO-COLLISION"
    elif str(fc) == "True":
        flag = "FORCE-COLLISION"
    else:
        flag = "DEFAULT-HOSTILITY-DEPENDENT-UNDECODABLE"

    # A MEASURED zero is a measurement, not a hole -- and it must be loud, because a zero-radius
    # body is exactly the point-body the occupancy fold exists to retire.
    kind = "ZERO-RADIUS-DECLARED" if (ar is not None and ar == 0.0) else "PHYSICAL"

    mesh = str(r.get("mesh") or "")
    hx = hz = hy = marc = ""
    got = meshes.aabb(mesh) if mesh else None
    if got:
        bb, marc, _exact = got
        hx, hz, hy = round((bb[3] - bb[0]) / 2, 5), round((bb[5] - bb[2]) / 2, 5), round(bb[4] - bb[1], 5)

    return dict(
        record=record, population=population, radius_m=lo, radius_m_hi=hi,
        radius_source_field="actorRadius", radius_source_template="database/templates/actor.tpl",
        grade=grade, grade_hi="DERIVED" if grade == "MEASURED" else grade,
        collision_flag=flag, body_kind=kind,
        actor_radius_raw="" if ar is None else repr(ar),
        actor_scale="" if sc is None else repr(sc),
        actor_height="" if ah is None else repr(ah),
        collision_shape="" if shape is None else str(shape),
        pathing_size=str(r.get("pathingSize") or ""),
        path_mass="" if num("pathMass") is None else num("pathMass"),
        physics_mass="" if num("physicsMass") is None else num("physicsMass"),
        force_collision="" if fc is None else str(fc),
        force_no_collision="" if fnc is None else str(fnc),
        monster_class=str(r.get("Class") or ""), template_name=str(r.get("templateName") or ""),
        archive=arc or "", mesh=mesh,
        mesh_aabb_half_x=hx, mesh_aabb_half_z=hz, mesh_aabb_height=hy, mesh_arc=marc,
        basis=basis,
    )


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F4 -- THE FOUR DISCRIMINATORS, run over the CORPUS (not over the board), so the answer is not
#       a property of 297 records
# ══════════════════════════════════════════════════════════════════════════════════════════════

def corpus_monsters() -> List[Tuple[str, str, float, float, str]]:
    """`[(record, mesh, actorRadius, scale, pathingSize)]` over every `Class = Monster` creature."""
    out = []
    for p in E3.idx:
        if not p.startswith("records/creatures"):
            continue
        r, _ = E3.winner(p)
        if not r or str(r.get("Class")) != "Monster":
            continue
        m, ar, sc, ps = r.get("mesh"), r.get("actorRadius"), r.get("scale"), r.get("pathingSize")
        if None in (m, ar, sc, ps):
            continue
        out.append((p, str(m).lower(), float(ar), float(sc), str(ps)))
    return out


PATHING_ORD = {"Small": 0, "Medium": 1, "Large": 2}


def d1_authoring_invariance(rows: Sequence[Tuple[str, str, float, float, str]]) -> Dict[str, int]:
    """Within mesh-groups whose `scale` varies: is `actorRadius` constant, or `actorRadius/scale`?"""
    g: Dict[str, List[Tuple[float, float]]] = collections.defaultdict(list)
    for _p, m, ar, sc, _ps in rows:
        g[m].append((ar, sc))
    const_r = prop_r = neither = n_groups = 0
    for _m, v in g.items():
        if len(v) < 3 or len({round(s, 4) for _a, s in v}) < 2:
            continue
        n_groups += 1
        if len({round(a, 4) for a, _s in v}) == 1:
            const_r += 1
        elif len({round(a / s, 4) for a, s in v if s}) == 1:
            prop_r += 1
        else:
            neither += 1
    return dict(groups=n_groups, actor_radius_constant=const_r,
                radius_over_scale_constant=prop_r, neither=neither)


def d3_gamma(rows: Sequence[Tuple[str, str, float, float, str]], scaled: bool) -> Dict[str, float]:
    """Goodman-Kruskal gamma of a size measure against the ordinal `pathingSize` class.

    Deterministic: the full pair set is streamed by class-bucket sort, no sampling, no RNG.
    """
    buckets: Dict[int, List[float]] = collections.defaultdict(list)
    for _p, _m, ar, sc, ps in rows:
        if ps in PATHING_ORD:
            buckets[PATHING_ORD[ps]].append(ar * sc if scaled else ar)
    conc = disc = tie = 0
    ks = sorted(buckets)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            lo_v = sorted(buckets[ks[i]])
            for x in buckets[ks[j]]:
                import bisect
                conc += bisect.bisect_left(lo_v, x)
                tie += bisect.bisect_right(lo_v, x) - bisect.bisect_left(lo_v, x)
                disc += len(lo_v) - bisect.bisect_right(lo_v, x)
    tot = conc + disc
    return dict(concordant=conc, discordant=disc, tied=tie,
                gamma=round((conc - disc) / tot, 6) if tot else 0.0)


def d4_pathing_at_constant_geometry(rows: Sequence[Tuple[str, str, float, float, str]]):
    """Groups sharing (mesh, actorRadius). Does `pathingSize` track `scale`?  AND the reverse."""
    g: Dict[Tuple[str, float], List[Tuple[str, float, str]]] = collections.defaultdict(list)
    for p, m, ar, sc, ps in rows:
        g[(m, round(ar, 4))].append((p, sc, ps))
    agree = disagree = tied = 0
    varying: List[Tuple[str, float, List[Tuple[str, float, str]]]] = []
    const_groups = 0
    const_wide = 0
    widest = (0.0, "")
    for (m, ar), v in g.items():
        if len(v) < 2:
            continue
        classes = {ps for _p, _s, ps in v}
        scales = [s for _p, s, _ps in v]
        ratio = (max(scales) / min(scales)) if min(scales) > 0 else 0.0
        if len(classes) > 1:
            varying.append((m, ar, v))
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    a, b = v[i], v[j]
                    if a[2] == b[2]:
                        continue
                    ds = a[1] - b[1]
                    dc = PATHING_ORD.get(a[2], 0) - PATHING_ORD.get(b[2], 0)
                    if ds == 0:
                        tied += 1
                    elif ds * dc > 0:
                        agree += 1
                    else:
                        disagree += 1
        else:
            const_groups += 1
            if ratio >= 1.5:
                const_wide += 1
            if ratio > widest[0]:
                widest = (ratio, m)
    return dict(varying_groups=len(varying), pairs_agree=agree, pairs_disagree=disagree,
                pairs_tied=tied, constant_groups=const_groups,
                constant_groups_scale_spread_ge_1_5x=const_wide,
                widest_constant_group_ratio=round(widest[0], 4),
                widest_constant_group_mesh=widest[1],
                varying_detail=[(m, ar, sorted(v, key=lambda x: x[1])) for m, ar, v in varying])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F6 -- the wave / difficulty / champion scale-modifier census
# ══════════════════════════════════════════════════════════════════════════════════════════════

def colossus_records() -> List[Tuple[str, float, float]]:
    """Every `Skill_BuffSelfColossus` record in the corpus: `(record, actorScale, actorScaleTime)`."""
    out = []
    for p in E3.idx:
        r, _ = E3.winner(p)
        if r and str(r.get("Class")) == COLOSSUS_CLASS:
            out.append((p, float(r.get("actorScale") or 0.0), float(r.get("actorScaleTime") or 0.0)))
    return sorted(out)


def bodies_carrying(records: Sequence[str], skill_paths: Set[str]) -> List[Tuple[str, str, str]]:
    """`[(body, skillName field, skill)]` for any body that references one of `skill_paths`."""
    out = []
    for rec in records:
        r, _ = E3.winner(rec)
        if not r:
            continue
        for k, v in r.items():
            if k.startswith("skillName") and str(v).lower().replace("\\", "/") in skill_paths:
                out.append((rec, k, str(v)))
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# emission helpers
# ══════════════════════════════════════════════════════════════════════════════════════════════

def dump(path: pathlib.Path, cols: Sequence[str], rows: Sequence[Dict[str, object]]) -> str:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return sha256_of(path)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()
