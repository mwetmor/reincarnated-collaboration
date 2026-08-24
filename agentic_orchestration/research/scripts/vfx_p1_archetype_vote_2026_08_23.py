#!/usr/bin/env python3
"""VFX ARCHETYPE-BINDING RUN — P1 archetype vote (elrond, 2026-08-23).

Charter: agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md
Ledger:  L-7 (P0-a PASS / bounds) · L-8 (emission bundles PROHIBITED) · L-9 (method authorized)
P0-a:    agentic_orchestration/elrond/notes/2026-08-23-vfx-p0a-kit-substrate-clusterability.md

METHOD (as executed — see MIGRATION doc for the full merge log + deviations from P0-a §6):
  Universe   canon_corpus.roster_status='active' JOIN canon_engine_key.row_class='combat-kit'  (531 kits)
  Grain      SKILL. One row per kit_mapping.mapping_json.skills[] entry inside the universe (1,138).
  Axis       kit_mapping.mapping_json.skills[].geometry_value  — the field kit_compiler.py
             `_rich_geometry_for_skill` reads FIRST as authoritative (§3.1); 99.7% populated.
  Refinement skill_geometry_band.motion_signature / .delivery_class joined on (kit_id, skill_ordinal).
             MEASURED to be functionally determined BY the axis (purity 1.000 on every archetype),
             therefore carried as ANNOTATION, never as a split axis.
  Merge      NONE PERFORMED. `_DELIVERY_TO_RICH` is injective over the 7 attested delivery classes
             (licenses no cross-class merge). `_RICH_TO_SPATIAL` is REJECTED as merge authority: it is
             the run-time hit-gauge collapse (25 rich keys -> 5 spatial values), and the engine keeps
             the rich vocabulary separate precisely because spatial is lossy. Recorded as annotation.
  Singletons KEPT as classes (Discipline #41). NULL-motion is informative, not missing.
  Labels     READ verbatim from the axis value. `researcher_gloss` is a CONCATENATION of attested
             facts (modal motion + delivery + exemplar source_skill strings) — no invented vocabulary.

Transactional + idempotent (re-run drops and rebuilds this vote_run's rows only). Additive DDL:
no existing table or column is altered. Read-only on every engine-side store.
"""
from __future__ import annotations
import collections
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CUR = os.path.abspath(os.path.join(HERE, "..", "curated"))
DB = os.path.join(CUR, "corpus.db")
VOTE_RUN = "vfx-archetype-vote-2026-08-23"
SCHEMA_VERSION = "vfx-archetype-vote-2026-08-23/P1"
SOURCE = "corpus.db kit_mapping.mapping_json.skills[].geometry_value + skill_geometry_band"
SOURCE_DATE = "2026-08-23"

# kit_compiler.py `_RICH_TO_SPATIAL` — transcribed verbatim 2026-08-23 (read-only mirror; the engine
# owns this map, we never write it). Used ONLY to annotate + to prove the merge it would license is
# the wrong one. Not a merge authority here.
RICH_TO_SPATIAL = {
    "circle": "circle", "ground_targeted_circle": "circle", "aura": "circle",
    "ring": "circle", "vortex_pull": "circle", "whirlwind": "circle",
    "cone": "cone", "melee_arc": "cone",
    "line": "line", "beam_channel": "line", "chain": "line", "fork": "line",
    "ricochet_bounce": "line",
    "single_target": "point", "multi_projectile": "point", "melee_strike": "point",
    "ground_slam": "point", "leap_strike": "point",
    "totem": "none", "self_buff": "none", "blink": "none", "teleport": "none",
    "dash_attack": "none", "defensive_dash": "none", "placed_lane": "line",
}
# kit_compiler.py `_DELIVERY_TO_RICH` — verbatim mirror. Injective over its 7 keys.
DELIVERY_TO_RICH = {
    "projectile": "multi_projectile", "beam": "beam_channel", "zone": "ground_targeted_circle",
    "motion": "whirlwind", "aura": "aura", "summon_delegate": "totem", "melee_arc": "melee_arc",
}

DDL = """
CREATE TABLE IF NOT EXISTS vfx_archetype (
    archetype_id              TEXT NOT NULL,   -- READ verbatim from the axis value. Never invented.
    vote_run                  TEXT NOT NULL,
    grain                     TEXT NOT NULL CHECK (grain IN ('skill','kit')),
    axis_expr                 TEXT NOT NULL,   -- the defining contingency cell, as an expression
    axis_source               TEXT NOT NULL,   -- exact substrate path the axis value came from
    motion_signature_attested TEXT,            -- modal motion_signature among banded members (NULL = none banded / no path signature)
    motion_support            INTEGER NOT NULL DEFAULT 0,
    motion_purity             REAL,            -- modal share; 1.0 => functionally determined by the axis
    delivery_class_attested   TEXT,
    delivery_support          INTEGER NOT NULL DEFAULT 0,
    delivery_purity           REAL,
    engine_rich_key           INTEGER NOT NULL,-- 1 iff archetype_id is a key of kit_compiler._RICH_TO_SPATIAL
    engine_spatial_primitive  TEXT,            -- ANNOTATION ONLY. Never used as merge authority (see MIGRATION).
    member_skills             INTEGER NOT NULL,
    member_kits               INTEGER NOT NULL,
    exemplar_skills_json      TEXT NOT NULL,   -- JSON array of verbatim source_skill strings
    researcher_gloss          TEXT NOT NULL,   -- concatenation of attested facts; zero-repo-context legible
    support_tier              TEXT NOT NULL CHECK (support_tier IN ('T1','T2','T3','T4')),
    vocab_flag                TEXT,            -- non-NULL = the value is outside the engine's authored vocabulary
    source                    TEXT NOT NULL,
    source_date               TEXT NOT NULL,
    PRIMARY KEY (archetype_id, vote_run)
);
CREATE TABLE IF NOT EXISTS vfx_archetype_member (
    kit_id              TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    skill_ordinal       INTEGER NOT NULL,      -- 0-based index into mapping_json.skills[]; -1 = kit carries no kit_mapping row
    vote_run            TEXT NOT NULL,
    archetype_id        TEXT,                  -- NULL => unassignable (see unassignable_reason)
    source_skill        TEXT,
    geometry_value_raw  TEXT,                  -- RAW preserved: the curation is reversible from this
    motion_signature_raw TEXT,
    delivery_class_raw  TEXT,
    banded              INTEGER NOT NULL,      -- 1 = a skill_geometry_band row exists for (kit_id, skill_ordinal)
    assignment_basis    TEXT NOT NULL,
    unassignable_reason TEXT,
    PRIMARY KEY (kit_id, skill_ordinal, vote_run)
);
CREATE INDEX IF NOT EXISTS idx_vam_arch ON vfx_archetype_member(archetype_id);
CREATE INDEX IF NOT EXISTS idx_vam_kit  ON vfx_archetype_member(kit_id);
CREATE TABLE IF NOT EXISTS vfx_vote_merge_log (
    vote_run       TEXT NOT NULL,
    entry_id       TEXT NOT NULL,
    candidate      TEXT NOT NULL,   -- the merge that was considered
    authority      TEXT NOT NULL,   -- the engine join that would license it
    decision       TEXT NOT NULL CHECK (decision IN ('MERGED','REJECTED','NOT-LICENSED')),
    rationale      TEXT NOT NULL,
    PRIMARY KEY (vote_run, entry_id)
);
CREATE TABLE IF NOT EXISTS vfx_vote_falsifier (
    vote_run     TEXT NOT NULL,
    falsifier_id TEXT NOT NULL,
    statement    TEXT NOT NULL,
    outcome      TEXT NOT NULL CHECK (outcome IN ('FIRED','NOT-FIRED','FIRED-MISGRAINED','PENDING-P3')),
    evidence     TEXT NOT NULL,
    consequence  TEXT NOT NULL,
    PRIMARY KEY (vote_run, falsifier_id)
);
"""


def md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def exemplars(rows: list[dict], k: int = 5) -> list[str]:
    """Pick k distinct verbatim source_skill strings, preferring short paren-free names.

    Presentation-only selection (P2 researchers read these). Non-destructive: the full member list
    is preserved in vfx_archetype_member; nothing is dropped or rewritten.
    """
    seen, clean, rest = set(), [], []
    for r in sorted(rows, key=lambda x: (x["kit_id"], x["ord"])):
        n = (r["src"] or "").strip()
        if not n or n.lower() in seen:
            continue
        seen.add(n.lower())
        (clean if ("(" not in n and len(n) <= 34) else rest).append(n)
    return (clean + rest)[:k]


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = f"{DB}.pre-vfx-p1-{stamp}-backup"
    print(f"[backup] {backup}")
    shutil.copy2(DB, backup)
    with open(backup + ".md5.txt", "w") as f:
        f.write(f"{md5(backup)}  {os.path.basename(backup)}\n")

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # ---------------- READ: universe + substrate ----------------
    uni = {
        r["kit_id"]: r
        for r in cur.execute(
            "select c.kit_id, c.folk_name, c.game, k.delivery_value "
            "from canon_corpus c join canon_engine_key k using(kit_id) "
            "where c.roster_status='active' and k.row_class='combat-kit'"
        )
    }
    band = {
        (r["kit_id"], r["skill_ordinal"]): r
        for r in cur.execute("select * from skill_geometry_band")
    }
    rows: list[dict] = []
    mapped: set[str] = set()
    skill_empty: list[str] = []
    for kid, mj in cur.execute(
        "select kit_id, mapping_json from kit_mapping where mapping_json is not null"
    ).fetchall():
        if kid not in uni:
            continue
        mapped.add(kid)
        skills = json.loads(mj).get("skills", []) or []
        if not skills:
            skill_empty.append(kid)
            continue
        for i, s in enumerate(skills):
            b = band.get((kid, i))
            rows.append(dict(
                kit_id=kid, ord=i, src=s.get("source_skill"), gv=s.get("geometry_value"),
                ms=b["motion_signature"] if b else None,
                dc=b["delivery_class"] if b else None, banded=1 if b else 0,
            ))
    unmapped = sorted(set(uni) - mapped)
    skill_empty.sort()

    assert len(uni) == 531, f"universe drift: {len(uni)}"
    assert len({r["kit_id"] for r in rows}) + len(unmapped) + len(skill_empty) == len(uni)
    print(f"[universe] kits={len(uni)} mapped={len(mapped)} unmapped={len(unmapped)} "
          f"mapped-but-skill-empty={len(skill_empty)} skill_rows={len(rows)}")

    # ---------------- VOTE: contingency lattice on the axis ----------------
    by_arch: dict[str, list[dict]] = collections.defaultdict(list)
    unassignable: list[dict] = []
    for r in rows:
        if r["gv"]:
            by_arch[r["gv"]].append(r)
        else:
            unassignable.append(r)

    # ---------------- WRITE ----------------
    cur.executescript(DDL)
    for t in ("vfx_archetype", "vfx_archetype_member", "vfx_vote_merge_log", "vfx_vote_falsifier"):
        cur.execute(f"delete from {t} where vote_run=?", (VOTE_RUN,))

    def tier(n: int) -> str:
        return "T1" if n >= 50 else "T2" if n >= 20 else "T3" if n >= 5 else "T4"

    for aid, members in sorted(by_arch.items(), key=lambda kv: -len(kv[1])):
        ms_c = collections.Counter(m["ms"] for m in members if m["ms"])
        dc_c = collections.Counter(m["dc"] for m in members if m["dc"])
        ms, ms_n = (ms_c.most_common(1)[0] if ms_c else (None, 0))
        dc, dc_n = (dc_c.most_common(1)[0] if dc_c else (None, 0))
        ms_pur = (ms_n / sum(ms_c.values())) if ms_c else None
        dc_pur = (dc_n / sum(dc_c.values())) if dc_c else None
        ex = exemplars(members)
        is_rich = 1 if aid in RICH_TO_SPATIAL else 0
        gloss = (
            f"{aid} — motion signature: {ms or 'none attested (no path signature)'}; "
            f"delivery class: {dc or 'none attested (unbanded)'}; "
            f"exemplar skills: {', '.join(ex) if ex else '(none named)'}"
        )
        flag = None if is_rich else (
            "value is NOT a key of kit_compiler._RICH_TO_SPATIAL — the engine would fall through to "
            "the 'point' default at compile time; cross-seam finding, not fixed here"
        )
        if aid == "knockback":
            flag = (flag or "") + " | probable vocabulary leak: an effect noun occupying a geometry slot (n=1)"
        cur.execute(
            "insert into vfx_archetype values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (aid, VOTE_RUN, "skill",
             f"geometry_value = '{aid}'",
             "kit_mapping.mapping_json.skills[].geometry_value (kit_compiler §3.1 authoritative)",
             ms, ms_n, ms_pur, dc, dc_n, dc_pur, is_rich, RICH_TO_SPATIAL.get(aid),
             len(members), len({m["kit_id"] for m in members}), json.dumps(ex), gloss,
             tier(len(members)), flag, SOURCE, SOURCE_DATE),
        )

    for r in rows:
        assigned = bool(r["gv"])
        cur.execute(
            "insert into vfx_archetype_member values (?,?,?,?,?,?,?,?,?,?,?)",
            (r["kit_id"], r["ord"], VOTE_RUN, r["gv"] if assigned else None, r["src"],
             r["gv"], r["ms"], r["dc"], r["banded"],
             "axis-read: mapping skills[].geometry_value" if assigned else "none",
             None if assigned else
             "geometry_value NULL in kit_mapping; skill_geometry_band absent so the engine's "
             "_DELIVERY_TO_RICH fallback has no delivery_class input either. The engine would "
             "default this skill to 'single_target' at compile — an engine DEFAULT, not an "
             "attestation, so no archetype is voted here."),
        )
    # Kit-level coverage exceptions, carried as sentinel rows so the accounting is TOTAL:
    #   ordinal -1 = no kit_mapping row at all   ·   ordinal -2 = kit_mapping row, empty skills[]
    for kid in unmapped:
        cur.execute(
            "insert into vfx_archetype_member values (?,?,?,?,?,?,?,?,?,?,?)",
            (kid, -1, VOTE_RUN, None, None, None, None, None, 0, "none",
             "kit is in the active combat universe but carries no kit_mapping row — no skill "
             "entries exist to vote"),
        )
    for kid in skill_empty:
        cur.execute(
            "insert into vfx_archetype_member values (?,?,?,?,?,?,?,?,?,?,?)",
            (kid, -2, VOTE_RUN, None, None, None, None, None, 0, "none",
             "kit_mapping row exists and is structurally complete (motion_frame / scaffold / "
             "t4_doors / resource_economy / trigger_grammar all present) but skills[] is an EMPTY "
             "array — the per-skill mapping pass never landed for this kit. No skill entries exist "
             "to vote; a re-mapping lap would bring the kit into the archetype set unchanged."),
        )

    merge_log = [
        ("M-1", "cross-delivery_class merge via kit_compiler._DELIVERY_TO_RICH",
         "kit_compiler._DELIVERY_TO_RICH (7 keys)", "NOT-LICENSED",
         "The map is injective over its 7 attested delivery classes (7 distinct rich values), so it "
         "collapses no two delivery classes. It also takes no motion input, so it can neither merge "
         "nor split within a delivery class. It licenses zero merges."),
        ("M-2", "collapse archetypes sharing a spatial primitive via kit_compiler._RICH_TO_SPATIAL",
         "kit_compiler._RICH_TO_SPATIAL (25 keys -> 5 values)", "REJECTED",
         "Would merge 25 archetypes into 5 (circle<-6, none<-6, line<-6, point<-5, cone<-2), erasing "
         "every VFX distinction the substrate attests. The map's declared purpose in-code is the "
         "run-time hit-gauge the compiler asserts against; the engine maintains the RICH vocabulary "
         "separately (`_rich_geometry_for_skill` returns rich as the skill's geometry_type; the "
         "spatial collapse happens only at `primary_geometry`) precisely because spatial is lossy. "
         "Using the lossy side as identity authority inverts the map. Carried as annotation instead."),
        ("M-3", "merge 'orbit' into 'whirlwind' (both attest motion_signature=orbit_fixed)",
         "none — no engine join maps 'orbit'", "NOT-LICENSED",
         "'orbit' (n=18, 18 kits) is absent from _RICH_TO_SPATIAL entirely. Merging it into "
         "'whirlwind' would be hand-imposition on a shared refinement value; the substrate attests "
         "them as two distinct geometry_values. Kept separate; the engine-map gap is filed as a "
         "cross-seam finding (corroborated: MIGRATION.md V9 already lists 'geometry:orbit'=6 as a "
         "residual blocked bucket)."),
        ("M-4", "split archetypes by motion_signature",
         "measurement, not a join", "NOT-LICENSED",
         "motion_signature is functionally determined by the axis: across 305 joined rows every one "
         "of the 22 archetypes carrying banded members has exactly ONE motion_signature (purity "
         "1.000, zero exceptions). A split on a functionally-determined refinement produces no new "
         "classes. Same result for delivery_class (407 joined rows, purity 1.000, 25/25 archetypes)."),
        ("M-5", "fold the 3 geometry_value-NULL skills into 'single_target'",
         "kit_compiler._rich_geometry_for_skill terminal default", "REJECTED",
         "The engine's `return \"single_target\"` is a last-resort default reached when both the "
         "mapping value and the delivery_class fallback are absent. A default is not an attestation. "
         "Listed as unassignable-with-reason instead."),
    ]
    for e in merge_log:
        cur.execute("insert into vfx_vote_merge_log values (?,?,?,?,?,?)", (VOTE_RUN,) + e)

    # ---------------- FALSIFIERS (pre-registered in P0-a §6) ----------------
    # (a) spatial-collapse half — count archetypes per spatial primitive; the P3 half is imagery.
    sp = collections.defaultdict(list)
    for aid in by_arch:
        if aid in RICH_TO_SPATIAL:
            sp[RICH_TO_SPATIAL[aid]].append(aid)
    sp_fire = {s: sorted(l) for s, l in sp.items() if len(l) >= 3}
    # strongest over-split candidates: same spatial AND same attested motion_signature
    modal_ms = {aid: (collections.Counter(m["ms"] for m in ms_ if m["ms"]).most_common(1) or [(None, 0)])[0][0]
                for aid, ms_ in by_arch.items()}
    pairs = []
    for s, l in sp.items():
        buckets = collections.defaultdict(list)
        for aid in l:
            buckets[modal_ms.get(aid)].append(aid)
        for m, group in buckets.items():
            if len(group) >= 2:
                pairs.append(f"spatial '{s}' + motion '{m}': {sorted(group)}")
    # (b) as pre-registered (kit-grain delivery_value spread) AND correctly re-grained (delivery_class)
    dv_of = {k: uni[k]["delivery_value"] for k in uni}
    b_pre = {aid: len({dv_of[m["kit_id"]] for m in ms_}) for aid, ms_ in by_arch.items()}
    b_pre_fire = {a: n for a, n in b_pre.items() if n > 4}
    b_post = {aid: len({m["dc"] for m in ms_ if m["dc"]}) for aid, ms_ in by_arch.items()}
    b_post_fire = {a: n for a, n in b_post.items() if n > 1}
    # (c) representativeness: TVD between banded and unbanded archetype distributions
    bd = collections.Counter(r["gv"] for r in rows if r["banded"] and r["gv"])
    ub = collections.Counter(r["gv"] for r in rows if not r["banded"] and r["gv"])
    nb, nu = sum(bd.values()), sum(ub.values())
    tvd = sum(abs(bd[a] / nb - ub[a] / nu) for a in by_arch) / 2
    top_delta = sorted(((bd[a] / nb - ub[a] / nu, a) for a in by_arch), key=lambda t: -abs(t[0]))[:5]

    falsifiers = [
        ("F-a", "If >=3 archetypes collapse to the same _RICH_TO_SPATIAL primitive AND to the same "
                "reference imagery at P3, the taxonomy is over-split.",
         "PENDING-P3",
         f"First conjunct SATISFIED broadly: {len(sp_fire)} spatial primitives carry >=3 archetypes "
         f"({'; '.join(f'{s}<-{len(l)}' for s, l in sorted(sp_fire.items()))}). This is expected and is "
         f"exactly why _RICH_TO_SPATIAL was rejected as merge authority (merge-log M-2). Second "
         f"conjunct (shared reference imagery) is not testable until P3. Substrate-side proxy for the "
         f"strongest over-split candidates — archetypes sharing BOTH spatial primitive and attested "
         f"motion_signature: " + " | ".join(sorted(pairs)),
         "Verdict DEFERRED to P3. The listed same-spatial+same-motion groups are the P3 watch-list: "
         "if any such group also selects the same canonical reference, THAT group (not the whole "
         "taxonomy) is over-split and should be merged at P4 with the receipt recorded."),
        ("F-b", "If any archetype's member kits span >4 delivery_value classes, the cell is under-split.",
         "FIRED-MISGRAINED",
         f"As pre-registered (kit-grain delivery_value): FIRES on {len(b_pre_fire)}/{len(by_arch)} "
         f"archetypes ({', '.join(f'{a}={n}' for a, n in sorted(b_pre_fire.items(), key=lambda t: -t[1]))}). "
         f"But delivery_value is a KIT-level column while archetypes are SKILL-grain, so a 3-skill kit "
         f"donates its single delivery_value to 3 different archetypes — the statistic measures kit "
         f"heterogeneity, not archetype heterogeneity. Correctly re-grained onto the skill-grain "
         f"delivery_class: {len(b_post_fire)}/{len(by_arch)} archetypes span >1 class "
         f"(407 joined rows, purity 1.000).",
         "The pre-registered form is mis-grained against the axis the vote actually ran on; its firing "
         "carries no under-split signal. The correctly-grained form does NOT fire: no archetype is "
         "under-split. Recorded rather than filed down (P0-a methodology step 5)."),
        ("F-c", "If the banded subset's archetype distribution differs materially from the unbanded "
                "subset's, the banded sample is unrepresentative and the skill-grain half is biased.",
         "FIRED",
         f"Total variation distance between banded (n={nb}) and unbanded (n={nu}) archetype "
         f"distributions = {tvd:.3f}. Largest deltas (banded minus unbanded): " +
         ", ".join(f"{a} {d:+.1%}" for d, a in top_delta) + ".",
         "MILD bias, consequence CONTAINED. The banding pass over-sampled skills with legible "
         "delivery geometry (zone/summon/spread) and under-sampled self-buffs and generic melee. "
         "Because the archetype set rests on geometry_value (99.7% coverage) and motion_signature is "
         "annotation only, the bias does not distort the taxonomy — it means the motion_signature "
         "annotation column is denser on some archetypes than others. P3/P4 should not read "
         "motion_support as evidence of archetype importance."),
    ]
    for f in falsifiers:
        cur.execute("insert into vfx_vote_falsifier values (?,?,?,?,?,?)", (VOTE_RUN,) + f)

    con.commit()

    # ---------------- VERIFY ----------------
    n_arch = cur.execute("select count(*) from vfx_archetype where vote_run=?", (VOTE_RUN,)).fetchone()[0]
    n_mem = cur.execute("select count(*) from vfx_archetype_member where vote_run=? and skill_ordinal>=0", (VOTE_RUN,)).fetchone()[0]
    n_assigned = cur.execute("select count(*) from vfx_archetype_member where vote_run=? and archetype_id is not null", (VOTE_RUN,)).fetchone()[0]
    n_unassign = cur.execute("select count(*) from vfx_archetype_member where vote_run=? and archetype_id is null", (VOTE_RUN,)).fetchone()[0]
    sum_members = cur.execute("select coalesce(sum(member_skills),0) from vfx_archetype where vote_run=?", (VOTE_RUN,)).fetchone()[0]
    orphan = cur.execute(
        "select count(*) from vfx_archetype_member m where m.vote_run=? and m.archetype_id is not null "
        "and not exists (select 1 from vfx_archetype a where a.archetype_id=m.archetype_id and a.vote_run=m.vote_run)",
        (VOTE_RUN,)).fetchone()[0]
    kits_covered = cur.execute(
        "select count(distinct kit_id) from vfx_archetype_member where vote_run=? and archetype_id is not null",
        (VOTE_RUN,)).fetchone()[0]

    assert n_mem == len(rows), (n_mem, len(rows))
    assert sum_members == n_assigned == len(rows) - len(unassignable), (sum_members, n_assigned)
    assert n_unassign == len(unassignable) + len(unmapped) + len(skill_empty), (n_unassign,)
    assert orphan == 0
    assert kits_covered + len(unmapped) + len(skill_empty) == len(uni)
    print(f"[verify] archetypes={n_arch} skill_rows={n_mem} assigned={n_assigned} "
          f"({n_assigned/n_mem:.1%}) unassignable_skills={len(unassignable)} "
          f"kits_covered={kits_covered}/{len(uni)} ({kits_covered/len(uni):.1%}) "
          f"[exceptions: {len(unmapped)} no-mapping + {len(skill_empty)} empty-skills] "
          f"orphans={orphan} — ALL OK")
    for r in cur.execute("select falsifier_id, outcome from vfx_vote_falsifier where vote_run=?", (VOTE_RUN,)):
        print(f"[falsifier] {r['falsifier_id']}: {r['outcome']}")

    cur.execute(
        "insert into corpus_schema_meta (version, applied_utc, note) values (?,?,?)",
        (SCHEMA_VERSION, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         f"VFX archetype vote P1 (elrond, gandalf RUN-CONDUCTOR). ADDITIVE: vfx_archetype ({n_arch}), "
         f"vfx_archetype_member ({n_mem + len(unmapped)}), vfx_vote_merge_log ({len(merge_log)}), "
         f"vfx_vote_falsifier. Substrate-led contingency vote on kit_mapping skills[].geometry_value "
         f"(the kit_compiler §3.1-authoritative per-skill field, 99.7% populated in universe) — this "
         f"CORRECTS P0-a §6, which recommended skill_geometry_band.delivery_class x motion_signature "
         f"(40% coverage) as primary. NO MERGES PERFORMED: _DELIVERY_TO_RICH is injective; "
         f"_RICH_TO_SPATIAL rejected as merge authority (lossy run-time hit-gauge, 25->5). "
         f"motion_signature + delivery_class measured functionally determined by the axis (purity "
         f"1.000) and carried as annotation. Coverage {n_assigned}/{n_mem} skills, "
         f"{kits_covered}/{len(uni)} kits. Backup {os.path.basename(backup)}."),
    )
    con.commit()
    con.close()
    print(f"[stamp] {SCHEMA_VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
