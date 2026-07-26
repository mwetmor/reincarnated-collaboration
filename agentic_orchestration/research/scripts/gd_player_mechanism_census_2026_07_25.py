#!/usr/bin/env python3
"""
GD player-side mechanism census (2026-07-25) — elrond.

READ-ONLY over agentic_orchestration/research/curated/corpus.db.
Enumerates the distinct player-side mechanisms the 41 GD-lane kits exercise,
with per-mechanism kit-count, exemplars, provenance table, and attestation grade.

Two attestation grades, never blurred:
  STRUCTURED  — read from a typed column or a typed JSON field. Measured.
  PROSE       — regex over curated prose (dossier payloads, mapping delivery/fidelity
                notes, verify_ledger claim/anchor text). Each hit carries its
                evidence snippet so it is hand-checkable.

Usage:  python3 gd_player_mechanism_census_2026_07_25.py [--evidence]
"""
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

DB = (Path(__file__).resolve().parents[1] / "curated" / "corpus.db")
LANE = "gd-%"

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row


def q(sql, params=()):
    return con.execute(sql, params).fetchall()


KITS = [r["kit_id"] for r in q(
    "SELECT kit_id FROM kit_master WHERE game='gd' ORDER BY kit_id")]
NAME = {r["kit_id"]: r["folk_name"] for r in q(
    "SELECT kit_id, folk_name FROM kit_master WHERE game='gd'")}
N = len(KITS)

# mechanism_id -> dict(label, family, grade, provenance, kits:set, evidence:{kit:snippet})
MECH = {}


def add(mid, label, family, grade, provenance, kit, snippet):
    m = MECH.setdefault(mid, dict(label=label, family=family, grade=grade,
                                  provenance=provenance, kits=set(), ev={}))
    m["kits"].add(kit)
    m["ev"].setdefault(kit, snippet)


# ---------------------------------------------------------------- STRUCTURED
# (1) skill_geometry_band — typed delivery / cadence / pierce / chain / motion
SGB_DELIVERY = {
    "zone":            ("D-ZONE",  "Ground-placed zone / persistent ground effect"),
    "projectile":      ("D-PROJ",  "Projectile delivery"),
    "melee_arc":       ("D-MELEE", "Melee arc / sweep"),
    "summon_delegate": ("D-DELEG", "Delegated actor delivery (pet / totem / turret)"),
    "aura":            ("D-AURA",  "Aura / persistent self-field"),
    "motion":          ("D-MOTION", "Motion-fused attack (dash / spin / charge)"),
    "beam":            ("D-BEAM",  "Channeled beam"),
}
for r in q("SELECT kit_id, source_skill, delivery_class, cadence_class, pierce, chain, "
           "motion_signature, range_band, width_band, speed_band "
           "FROM skill_geometry_band WHERE kit_id LIKE ?", (LANE,)):
    k, sk = r["kit_id"], r["source_skill"] or "?"
    if r["delivery_class"] in SGB_DELIVERY:
        mid, lbl = SGB_DELIVERY[r["delivery_class"]]
        add(mid, lbl, "delivery shape", "STRUCTURED",
            "skill_geometry_band.delivery_class", k, f"{sk} -> {r['delivery_class']}")
    if r["cadence_class"]:
        add(f"C-{r['cadence_class'].upper()}",
            {"cooldown": "Cooldown-gated cadence", "spam": "Spam cadence",
             "channel": "Channel cadence",
             "builder_spender": "Builder/spender cadence"}[r["cadence_class"]],
            "cadence", "STRUCTURED", "skill_geometry_band.cadence_class", k,
            f"{sk} -> {r['cadence_class']}")
    if r["pierce"] == "all":
        add("G-PIERCE", "Pierce-all projectile", "delivery shape", "STRUCTURED",
            "skill_geometry_band.pierce", k, f"{sk} -> pierce=all")
    if r["chain"]:
        add("G-CHAIN", "Chain / hop to additional targets", "delivery shape",
            "STRUCTURED", "skill_geometry_band.chain", k, f"{sk} -> chain={r['chain']}")
    ms = r["motion_signature"]
    if ms:
        add(f"M-{ms.upper()}", f"Motion signature: {ms.replace('_',' ')}",
            "motion signature", "STRUCTURED",
            "skill_geometry_band.motion_signature", k, f"{sk} -> {ms}")

# (2) kit_mapping JSON — geometry_value / ailments / trigger_grammar / t4_doors / elements
GEOM_ROLL = {
    "ground_targeted_circle": ("G-GROUND", "Ground-targeted circle placement"),
    "totem":        ("G-TOTEM",  "Placed autonomous emitter (totem / trap / turret)"),
    "melee_strike": ("G-MSTRIKE", "Melee point strike"),
    "self_buff":    ("G-SELFBUF", "Self-buff (non-aura)"),
    "single_target": ("G-SINGLE", "Single-target payload"),
    "multi_projectile": ("G-MULTIP", "Multi-projectile / fan spread"),
    "circle":       ("G-NOVA",  "Self-centred circle / nova"),
    "ring":         ("G-NOVA",  "Self-centred circle / nova"),
    "whirlwind":    ("G-SPIN",  "Sustained spin / whirlwind"),
    "melee_arc":    ("G-MARC",  "Melee arc sweep"),
    "line":         ("G-LINE",  "Line / lane payload"),
    "dash_attack":  ("G-DASH",  "Dash / charge attack"),
    "beam_channel": ("G-BEAM",  "Channelled beam"),
    "aura":         ("G-AURA",  "Aura"),
    "teleport":     ("G-BLINK", "Teleport / blink strike"),
    "ricochet_bounce": ("G-RICO", "Ricochet / bounce"),
    "orbit":        ("G-ORBIT", "Orbiting proxy"),
    "fork":         ("G-FORK",  "Fork / split projectile"),
    "cone":         ("G-CONE",  "Cone"),
    "chain":        ("G-CHAINH", "Chain-hop between targets"),
}
AIL_LABEL = {
    "burn": "Burn DoT", "bleed": "Bleed DoT", "poison": "Poison/acid DoT",
    "curse:sap": "Sap / weaken curse (debuff)", "drain": "Drain (life/resource siphon)",
    "root": "Root / immobilize (hard CC)", "blind": "Blind / fumble (soft CC)",
}
for r in q("SELECT kit_id, mapping_json FROM kit_mapping WHERE kit_id LIKE ?", (LANE,)):
    k = r["kit_id"]
    mj = json.loads(r["mapping_json"]) if r["mapping_json"] else {}
    for s in mj.get("skills", []):
        gv = s.get("geometry_value")
        sk = s.get("source_skill", "?")
        if gv in GEOM_ROLL:
            mid, lbl = GEOM_ROLL[gv]
            add(mid, lbl, "delivery shape", "STRUCTURED",
                "kit_mapping.mapping_json$.skills[].geometry_value", k, f"{sk} -> {gv}")
        for a in (s.get("ailments") or []):
            add(f"A-{a.upper().replace(':','_')}", AIL_LABEL.get(a, a),
                "ailment / status", "STRUCTURED",
                "kit_mapping.mapping_json$.skills[].ailments[]", k, f"{sk} -> {a}")
    tg = mj.get("trigger_grammar") or {}
    if tg.get("proc_trigger_condition"):
        v = tg["proc_trigger_condition"]
        add(f"T-{v.upper()}", f"Proc trigger: {v}", "trigger machinery", "STRUCTURED",
            "kit_mapping.mapping_json$.trigger_grammar.proc_trigger_condition", k, v)
    if tg.get("consequence_type"):
        v = tg["consequence_type"]
        add(f"T-CONS-{v.upper()}", f"Proc consequence: {v}", "trigger machinery",
            "STRUCTURED",
            "kit_mapping.mapping_json$.trigger_grammar.consequence_type", k, v)
    if tg.get("mark_identity"):
        add("T-ACCUM", "Swing-count accumulator (every-Nth-swing)", "trigger machinery",
            "STRUCTURED", "kit_mapping.mapping_json$.trigger_grammar.mark_identity", k,
            tg["mark_identity"])
    if tg.get("trigger_chain_shape") == "apply-consume-pair":
        add("T-APPLYCONSUME", "Apply-then-consume pair (detonator)", "trigger machinery",
            "STRUCTURED", "kit_mapping.mapping_json$.trigger_grammar.trigger_chain_shape",
            k, "apply-consume-pair")

# ---------------------------------------------------------------- PROSE CORPUS
PROSE = defaultdict(list)   # kit -> [(table.field, text)]
for r in q("SELECT kit_id, family, payload_json FROM kit_dossier "
           "WHERE kit_id LIKE ? AND abstained=0 AND payload_json IS NOT NULL", (LANE,)):
    PROSE[r["kit_id"]].append((f"kit_dossier[{r['family']}]", r["payload_json"]))
for r in q("SELECT kit_id, mapping_json FROM kit_mapping WHERE kit_id LIKE ?", (LANE,)):
    mj = json.loads(r["mapping_json"]) if r["mapping_json"] else {}
    for s in mj.get("skills", []):
        if s.get("delivery_notes"):
            PROSE[r["kit_id"]].append(
                ("kit_mapping$.skills[].delivery_notes", s["delivery_notes"]))
    for fld in ("fidelity_notes", "motion_frame"):
        if mj.get(fld):
            PROSE[r["kit_id"]].append((f"kit_mapping$.{fld}", mj[fld]))
    if mj.get("resource_economy"):
        PROSE[r["kit_id"]].append(
            ("kit_mapping$.resource_economy", json.dumps(mj["resource_economy"])))
    if mj.get("scaffold"):
        PROSE[r["kit_id"]].append(
            ("kit_mapping$.scaffold", json.dumps(mj["scaffold"])))
for r in q("SELECT kit_id, claim_text, anchor_quote FROM verify_ledger "
           "WHERE kit_id LIKE ? AND verdict='CONFIRMED'", (LANE,)):
    for fld, v in (("verify_ledger.claim_text", r["claim_text"]),
                   ("verify_ledger.anchor_quote", r["anchor_quote"])):
        if v:
            PROSE[r["kit_id"]].append((fld, v))
for r in q("SELECT kit_id, missing_expression, source_anchor FROM kit_deviation "
           "WHERE kit_id LIKE ?", (LANE,)):
    for fld, v in (("kit_deviation.missing_expression", r["missing_expression"]),
                   ("kit_deviation.source_anchor", r["source_anchor"])):
        if v:
            PROSE[r["kit_id"]].append((fld, v))

# (mid, label, family, regex)
PROSE_RULES = [
    ("P-CONVERT",  "Damage-type conversion (item/set/skill-mod granted)", "gear-borne",
     r"conver(t|sion|ts|ted)\b|pass-?through conversion|to[- ]fire\b|to[- ]cold\b|to[- ]acid\b"),
    ("P-SET",      "Item-set threshold bonus as build enabler", "gear-borne",
     r"\b\d[- ]?piece\b|\bset bonus\b|\bkey_set\b|\bset\":|\bset_function\b|Set \(|\bset is\b"),
    ("P-DEVOTION", "Devotion / constellation proc binding", "trigger machinery",
     r"devotion|constellation"),
    ("P-TRANSMUTE", "Transmuter / skill modifier that changes skill behaviour", "passive/tree",
     r"transmuter|skill_mod|Quick Jack|Tremor|Volcanic Stride|Nightfall|Unstable Anomaly|modifier\b"),
    ("P-RR",       "Resistance reduction (RR / shred)", "buff-debuff",
     r"resistance reduction|resist(ance)? shred|reduces? enemy .{0,25}resist|\bRR\b|"
     r"reduce vitality resistance|reduces? .{0,20}resistance by"),
    ("P-CDR",      "Cooldown reduction as a scaling lever", "gear-borne",
     r"cooldown reduction|\bCDR\b"),
    ("P-LEECH",    "Life leech / attack-damage-converted-to-health", "buff-debuff",
     r"life leech|\bleech(es|ing)?\b|\bADCtH\b|life-?drinking|lifesteal|sustains? survivability"),
    ("P-PET-PERM", "Persistent pet / summoned combatant", "pets-summons",
     r"persist until death|permanent[- ]fiend|pets? fight autonomously|"
     r"skeleton army|Raise Skeletons|Summon Blight Fiend|Briarthorn|Familiar\b|"
     r"autonomous pets?|summoned combatant|pet wall|menagerie"),
    ("P-PET-TEMP", "Temporary / duration-limited summon", "pets-summons",
     r"lasts only \d+ seconds|temporary (wendigo )?spirits?|short duration|Primal Spirit|"
     r"temporary pet|10s duration"),
    ("P-PET-SCALE", "Pet-scaling stat lane (pet% damage, pet OA/DA)", "pets-summons",
     r"pet-scaling|pet% damage|pet OA/DA|pet bonuses|pet-only stats|Player stats irrelevant"),
    ("P-WPS",      "Weapon-pool proc suite (on-attack proc pool)", "trigger machinery",
     r"\bWPS\b|Weapon Pool Skills"),
    ("P-REPLACER", "Default-attack replacer", "delivery shape",
     r"replaces default weapon attack|default-?attack repla|auto-?attack replacer|"
     r"Default-attack replacement|attack-replacer"),
    ("P-STACKMETER", "Charge / stack accumulator meter", "passive/tree",
     r"charges? stack|stack(s|ing)? charges|charge-stacking|max stacks|fervor meter|"
     r"stacks? per swing"),
    ("P-RETAL",    "Retaliation / damage-return (thorns)", "buff-debuff",
     r"retaliation|damage return|returns damage to attacker|Counter Strike"),
    ("P-ABSORB",   "Damage absorption / shield layer", "buff-debuff",
     r"absorption stacking|Blast Shield|damage absorption|absorb\w*\b"),
    ("P-ENERGY",   "Energy / mana economy pressure as a build constraint", "resource economy",
     r"energy[- ]hungry|energy management|energy sustain|energy regen|heavy energy drain|"
     r"energy consumption|mana reserve|energy managed"),
    ("P-ROOTCHAN", "Movement lock while casting / channelling", "delivery shape",
     r"rooted while channel|rooted or slow-moving|briefly rooted|cast-root|rooted but can kite"),
    ("P-MOVEATK",  "Movement skill fused with attack / gap-close", "delivery shape",
     r"gap-close|movement and nuke fused|movement skill IS the primary attack|"
     r"movement-attack|charge/dash through|teleports player to target|Blitz charge"),
    ("P-ITEMPROC", "Skill-granting item proc (weapon/amulet procs a skill)", "gear-borne",
     r"weapon procs|procs Tainted Eruption|item proc|grants? .{0,20}skill|Beronath conversion aura"),
    ("P-PLUSTARGET", "Affix that adds targets / projectiles to a skill", "gear-borne",
     r"\+\d+ extra targets|adds? \+?\d+ projectile|increases projectile count|"
     r"extra targets to|adds 100% pass-through"),
    ("P-STUN",     "Hard CC — stun / daze", "ailment / status",
     r"\bstun(s|ned|-lock|locks?)\b|daze|Flashbang"),
    ("P-SLOW",     "Soft CC — slow / chill", "ailment / status",
     r"\bslow(s|ed|ing) (enem|target|the pack)|\bchill(s|ed|ing)? (enem|target)"),
    ("P-FREEZE",   "Hard CC — freeze / petrify", "ailment / status",
     r"\bfreez(e|es|ing|ed)\b|petrif"),
    ("P-HEALZONE", "Healing / sustain zone or totem", "buff-debuff",
     r"passive healing|Wendigo Totem|Word of Renewal|HP sustain|healing and stat buffer|"
     r"leech vitality from all nearby"),
    ("P-IMMUNE",   "Timed defensive cooldown / immunity window", "buff-debuff",
     r"Mirror of Ereoctes|Mark of Torment|timed immunity|panic defensive|defensive cooldown|"
     r"Nullification"),
    ("P-CONTAGION", "Contagion / proximity spread between enemies", "delivery shape",
     r"spreads? to nearby|spread(s)? body-to-body|contagion|plague JUMPING|infects one target"),
    ("P-TETHER",   "Enemy-attached tether / beacon", "delivery shape",
     r"tether|attached to target enemy|beacon"),
    ("P-DEATHNOVA", "Explosion-on-death (proxy / corpse)", "pets-summons",
     r"explo(de|sion) on death|explosion-on-death|walking bombs?|mobile bomb"),
    ("P-ASPEED",   "Attack-speed / cast-speed as the scaling lever", "resource economy",
     r"attack speed maximized|attack-speed-governed|casting speed gear|cast speed|"
     r"Fast attack speed|casting-speed tempo|attack speed stacks"),
    ("P-AURA-EX",  "Persistent support field (seal / aura / toggle)", "passive/tree",
     r"Inquisitor Seal|Ascension toggles|toggle|aura requires mana|Night's Chill|"
     r"Primal Bond aura|Celestial Presence"),
    ("P-TRAPTRIG", "Contact-triggered placed trap (arms on enemy contact)", "trigger machinery",
     r"burst when enemies step on it|arms on enemy contact|trap arms|steps? on it"),
    ("P-AUTOTURRET", "Autonomous placed turret with own targeting", "pets-summons",
     r"fires? shells autonomously|fire autonomously|mortars fire|aggro-targeting autonomy|"
     r"turret aggro"),
]
COMPILED = [(m, l, f, re.compile(rx, re.I)) for m, l, f, rx in PROSE_RULES]

# HAND-ADJUDICATED EXCLUSIONS. Every regex hit below was read in context and
# rejected. Reasons are load-bearing: the corpus records NEGATIVE tokens in the
# same prose fields it records positive ones, so a naive scan over-counts.
EXCLUDE = {
    ("P-CONVERT", "gd-aar-spellbinder"):
        "NEGATION — fidelity_notes: 'no conversion/propagation capstone attested'",
    ("P-CONVERT", "gd-forcewave-warlord"):
        "NEGATION — fidelity_notes: 'NO conversion attested -> no ELEMENT_CONVERSION_PHYSICAL door'",
    ("P-CONVERT", "gd-callidors-tempest-templar"):
        "WINDOW ARTIFACT — matched 'compressed to fire-primary', not a conversion mechanic",
    ("P-DEVOTION", "gd-belgothian-blademaster"):
        "CROSS-REFERENCE — 'sibling of devotion-proc row' names an engine mapping row, "
        "not a devotion this kit takes; kit's own capstone_alterations ABSTAINED",
    ("P-RR", "gd-pet-conjurer"):
        "NEGATION + CROSS-KIT — 'not attestable HERE -- contrast gd-doom-bolt-sentinel where "
        "CoF's resistance reduction WAS fetched'",
    ("P-TRANSMUTE", "gd-bwc-demolitionist"):
        "STRUCK ANCHOR — the 'fumble transmuters' line is recorded as INADMISSIBLE per §0.2",
    ("P-TRANSMUTE", "gd-drain-essence-spellbinder"):
        "RECLASSIFIED — '+2 extra targets via item modifier' is a gear affix; counted at P-PLUSTARGET",
    ("P-ITEMPROC", "gd-belgothian-blademaster"):
        "RECLASSIFIED — 'weapon procs firing every swing' is the WPS pool; counted at P-WPS",
    ("P-RETAL", "gd-aegis-paladin"):
        "VARIANT-LANE — 'Retaliation Warlord Aegis' names a sibling kit in known_variants, "
        "not this kit's mapped form",
    ("P-RETAL", "gd-flames-of-ignaffar-purifier"):
        "VARIANT-LANE — 'FoI retaliation Purifier (Hybris set)' is a listed variant, not the mapped form",
    ("P-STUN", "gd-canister-saboteur"):
        "STRUCK BY CORPUS — kit_deviation: 'the engine emits NO CC token for it because the fetched "
        "anchor names only debuff; stun/blind live in probe/claim-paraphrase, both inadmissible'",
    ("P-FREEZE", "gd-aar-spellbinder"):
        "FOLK-NAME ARTIFACT — 'Albrecht the Freezer' is a variant nickname, no freeze status attested",
    ("P-FREEZE", "gd-roh-infiltrator"):
        "NEGATION — fidelity_notes: 'NO freeze/chill token — cold shards is element flavor only'",
    ("P-FREEZE", "gd-shadow-strike-infiltrator"):
        "NEGATION — fidelity_notes: 'NO chill/freeze token — cold is element flavor only'",
    ("P-FREEZE", "gd-trozan-druid"):
        "NEGATION — fidelity_notes: 'NO chill/freeze token: cold is element-flavor only'",
}
REJECTED = []

for k, rows in PROSE.items():
    for mid, lbl, fam, rx in COMPILED:
        for fld, text in rows:
            mo = rx.search(text)
            if mo:
                if (mid, k) in EXCLUDE:
                    REJECTED.append((mid, k, EXCLUDE[(mid, k)]))
                    break
                s = max(0, mo.start() - 60)
                add(mid, lbl, fam, "PROSE", f"{fld} (regex)", k,
                    f"[{fld}] ...{text[s:mo.end()+60].strip()}...")
                break

# mechanisms whose every hit was adjudicated away still deserve a zero row
for (mid, _k) in list(EXCLUDE):
    if mid not in MECH:
        lbl = next(l for m, l, f, _ in PROSE_RULES if m == mid)
        fam = next(f for m, l, f, _ in PROSE_RULES if m == mid)
        MECH[mid] = dict(label=lbl, family=fam, grade="PROSE-ZEROED",
                         provenance="all hits hand-rejected — see REJECTED ledger",
                         kits=set(), ev={})

# ---------------------------------------------------------------- REPORT
rows = sorted(MECH.items(), key=lambda kv: (-len(kv[1]["kits"]), kv[1]["family"], kv[0]))
print(f"# GD player-side mechanism census — N = {N} kits\n")
print(f"# distinct mechanisms enumerated: {len(rows)}")
print(f"# STRUCTURED: {sum(1 for _, m in rows if m['grade']=='STRUCTURED')}  "
      f"PROSE: {sum(1 for _, m in rows if m['grade']=='PROSE')}\n")
print("| id | mechanism | family | kits | % | grade | provenance | exemplars |")
print("|---|---|---|---|---|---|---|---|")
for mid, m in rows:
    ks = sorted(m["kits"])
    ex = "; ".join(NAME.get(x, x) for x in ks[:3])
    print(f"| {mid} | {m['label']} | {m['family']} | {len(ks)} | "
          f"{100*len(ks)/N:.0f}% | {m['grade']} | `{m['provenance']}` | {ex} |")

# ------------------------------------------------------- ZERO PROBES
# Seed-list mechanism families searched for and NOT found. Printed so the
# absence claims in the note are reproducible rather than assertions.
ZERO_PROBES = [
    ("knockdown / knockback",     r"knock ?down|knockback"),
    ("soft CC: slow / chill applied to enemies",
     r"\bslow(s|ed|ing) (enem|target|the pack)|\bchill(s|ed|ing)? (enem|target)"),
    ("% current-HP or % max-HP damage",
     r"% (of )?(current|max(imum)?) (health|hp|life)|percent.{0,12}health"),
    ("on-block proc / block chance", r"\bon[- ]block\b|block chance|blocked attack"),
    ("internal cooldown on a proc",  r"internal cooldown|\bICD\b|proc cooldown|cooldown per proc"),
    ("exclusive-skill constraint",   r"exclusive skill|exclusive aura|mutually exclusive"),
    ("+N to skill affix",            r"\+\d+ to (all )?(skills|.{0,25}skill)|\+skill\b"),
    ("health / energy regeneration stat", r"health regen|hp regen|energy regen(eration)?\b"),
    ("reflect (distinct from retaliation)", r"\breflect"),
    ("taunt / threat manipulation",  r"\btaunt"),
]
print("\n## ZERO PROBES — seed families searched, kits matched\n")
for lbl, rx in ZERO_PROBES:
    rr = re.compile(rx, re.I)
    hits = sorted({k for k, rows in PROSE.items()
                   for _f, t in rows if t and rr.search(t)})
    print(f"  {len(hits):2d}  {lbl}" + (f"   -> {hits}" if hits else ""))

print(f"\n## REJECTED HITS (hand-adjudicated) — {len(REJECTED)}\n")
for mid, k, why in sorted(REJECTED):
    print(f"  {mid:14s} {k:34s} {why}")

if "--evidence" in sys.argv:
    print("\n\n## EVIDENCE APPENDIX\n")
    for mid, m in rows:
        print(f"\n### {mid} — {m['label']} ({len(m['kits'])} kits, {m['grade']})")
        for k in sorted(m["kits"]):
            print(f"  - {k}: {m['ev'][k][:220]}")

# coverage per kit
print("\n\n## PER-KIT MECHANISM COUNT\n")
percount = defaultdict(int)
for _, m in rows:
    for k in m["kits"]:
        percount[k] += 1
for k in sorted(KITS, key=lambda x: -percount[x]):
    print(f"  {percount[k]:>3}  {k}")
con.close()
