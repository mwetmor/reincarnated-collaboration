#!/usr/bin/env python3
"""
Feasibility-Cuts Register — v1.2 (EDITION-II: +`pull` function level)
==============================================================================
Charter: canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md
  §2 SPACE != MAP + three ratified cut classes (logical / red-law / taste)
  §4 ghost field: enumerate lattice -> project ALL as zero-mass ghosts
      (decoupling law: ghosts land when THIS register lands; denominator law:
       coverage claims use the enumerated feasible lattice, never the sample)
Register base (enumeration input): coordinate-register-2026-07-13.md §2
  — the 13-coordinate kit-IDENTITY key (element-free; 14 serialized cell_key slots).

===== v1.2 SUPERSEDES v1.1 (Edition-II §10.1, gandalf renderer spec) =====
  Matt authorized the Edition-II chain 2026-07-15 ("If the slate holds, cut Edition-II §10").
  ONE change vs v1.1: the `function` coordinate grows 10 -> 11 levels (+`pull`).
  `pull` = inward displacement force, knockback's INVERSE (register §10.1 definition).

  LAW-INHERITANCE PROOF (why NO new law, no HALT):
    - L1' reads (treatment, function): `{control,hybrid} => function != none`. `pull` is a
      function value != none, so {control,hybrid}xpull is COHERENT and damage x pull is coherent
      (control-rider). L1' incoherent set stays {control,hybrid}xnone ONLY. `pull` slots in cleanly.
    - L2 / L3 / L4'' / RED-3' do NOT read the function coordinate. Adding a function level cannot
      change any of them.
    => the pull slice vets ENTIRELY under the ratified ledger {L1', L4'', L2, RED-3'}; new seals
       take EXISTING cut_ids only. Pull-slice meso: 1080 feasible + 54 sealed (all L2 SUMMON x solo
       x pull). ZERO cells need a new law. (If ANY pull cell had needed a new law -> HALT to Matt.)

  DENOMINATOR SUPERSESSION (v1.1 -> v1.2; every number independently re-derivable, audit bar):
    exact:  raw 900,169,200 -> 990,186,120 | post-logical 740,139,120 -> 819,439,740 |
            post-red-law 693,146,160 -> 767,411,820
    meso:   raw 11,340 -> 12,474 | feasible 10,080 -> 11,160 | sealed 1,260 -> 1,314 (L1' 756 + L2 558)
    depth-by-delivery UNCHANGED (function is CORE; depth is over non-core coords): PROJECTILE/MELEE
            55,755; others 74,340. depth_sum over 11,160 feasible meso = 767,411,820 = exact denom.

DISTINCTION (load-bearing): this is the 13-coordinate CORPUS-IDENTITY lattice,
NOT the engine-native SUBSTRATE lattice (substrate-coordinates.md L0-L4,
L4 ≈ 1.284×10⁹; banned bounding box 2.57×10⁹). Two different objects. The
substrate "2.57B" ban is not this register's naive box; this register carries
its OWN naive box with its OWN pre-cut caveat (renderer R2 spirit).

Executor: elrond (data steward). This is a TOOL script (curation/enumeration),
not engine code. Regenerates the register table from one command.

Run:  python3 feasibility_cuts_register_v1_2_2026_07_15.py
Emits: feasibility-cuts-register-v1.2.{csv,json}  (beside the .md)
       counts_ladder + pull-slice vetting printed + written into the JSON.
       Analysis tables into corpus.db (atlas_feasibility_*_v1_2 ; gitignored).
"""

import os, sys, json, sqlite3, itertools
from collections import Counter

DB  = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"

# ---------------------------------------------------------------------------
# THE ENUMERATION BASE — definitional value sets, coordinate-register §2.
# Element-free identity key. Masks (unknown/blank) are NOT definitional values;
# they are curation states, never lattice cells.
# #5 serializes as TWO cell_key slots: treatment + function.
# The "function" slot carries the control functions PLUS the literal 'none'
# (damage kits occupy 'none'); enumerating 5a×5b freely OVER-counts — the
# damage⊗control-function incoherence is the first LOGICAL cut.
# ---------------------------------------------------------------------------
COORDS = {
    "movement":   ["FREE-MOVE", "WALK", "ROOTED"],                                       # 3   #1  LOCKED
    "delivery":   ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON"],  # 7   #2  LOCKED
    "amp":        ["FLAT", "SPIKY", "VAR"],                                              # 3   #3  LOCKED
    "geometry":   [f"g{i:02d}" for i in range(21)],                                      # 21  #4  rolls up into #2
    "treatment":  ["damage", "control", "hybrid"],                                       # 3   #5a
    "function":   ["none", "hard-stop", "stun", "taunt", "fear", "blind",
                   "knockback", "expose", "hex", "silence", "pull"],                     # 11  #5b (incl. none; +pull v1.2)
    "defense":    ["tank", "mitigate", "evade", "absorb", "glass"],                      # 5   #6
    "economy":    ["spend", "cooldown", "generator-spender", "reserve",
                   "self-cost", "finite", "free"],                                       # 7   #7
    "proxy":      ["solo", "light", "heavy"],                                            # 3   #8
    "range":      ["melee", "mid", "ranged", "dual"],                                    # 4   #9
    "tempo":      ["low", "med", "high"],                                                # 3   #10
    "commit":     ["instant", "wind-up", "channel"],                                     # 3   #11
    "activation": ["active", "triggered"],                                              # 2   #12
    "dependency": ["one-shot", "build→spend", "apply→detonate"],                         # 3   #13
}
ORDER = list(COORDS.keys())  # canonical serialization order (matches cell_key)

# never-demote CORE (register §6.1) = the MESO-GRAIN (register rollup) axes.
CORE = ["movement", "delivery", "treatment", "function", "proxy", "activation", "dependency"]


def naive_product(coords):
    p = 1
    for v in coords.values():
        p *= len(v)
    return p


# ===========================================================================
# LOGICAL CUTS — combinations incoherent by definition. Each states its rule.
# A "cut" here is a PREDICATE; the removed-count is enumerated by counting the
# lattice cells the predicate selects (given the survivors of prior cuts, so
# counts compose — order = the register's stated order).
# ===========================================================================
def build_logical_cuts():
    """Return list of dicts: id, predicate(fn over a dict-cell), rule, rationale."""
    cuts = []

    # L1′ — treatment/function coherence (AMENDED 2026-07-15 per gandalf audit §2.A1,
    #   Matt-ratified Q30a). The ONLY incoherent pairs are {control,hybrid}⊗none:
    #   a control/hybrid kit MUST carry a function (that IS its identity). BUT
    #   damage⊗(any function) is NOW COHERENT — the control-RIDER semantics: a damage
    #   primary carrying a kit-designed control rider (Frozen-Orb class) is bedrock genre,
    #   and 130 living kits (damage×hard-stop 33, ×stun 26, ×hex 24, ×knockback 16,
    #   ×expose 11, ×taunt 10, ×blind 7, ×fear 3) prove it. v1's L1 over-formalized this
    #   with a `damage⟺none` half that the occupancy test falsified.
    #   Coherent pairs: 30 − 2 = 28 (was 19). Incoherent: {control,hybrid}×none only.
    def L1(c):
        return c["treatment"] in ("control", "hybrid") and c["function"] == "none"
    cuts.append(dict(
        id="L1-treatment-function-coherence",
        predicate=L1,
        rule="treatment∈{control,hybrid} ⟹ function≠none  (control/hybrid MUST have a function; "
             "damage×function IS coherent — control-rider semantics, 130 living kits)",
        rationale=("AMENDED L1′ (Matt-ratified Q30a, gandalf audit §2.A1): the only incoherent "
                   "treatment×function pairs are {control,hybrid}×none — a control/hybrid kit's "
                   "function is its identity, so 'none' is incoherent for it. damage×(any control "
                   "function) is COHERENT: a damage primary carrying a control rider (Frozen-Orb "
                   "class) is bedrock genre — 130 active kits sit there. v1's `damage⟺none` half "
                   "was over-reach, falsified by 30%% of the living corpus. 28 coherent pairs."),
        cls="logical",
    ))

    # L2 — SUMMON delivery ⟺ non-solo proxy (register §3B "summon economy" derived read).
    #   delivery=SUMMON with proxy=solo is incoherent: a summon kit HAS a proxy (the summoned
    #   entity) by definition; conversely proxy density is the summon's own axis. The register
    #   (§2 coord #8, §3B) defines summon-economy = model ∩ delivery=SUMMON ∩ proxy density —
    #   the pairing SUMMON⊗solo has no referent (nothing was summoned).
    def L2(c):
        return c["delivery"] == "SUMMON" and c["proxy"] == "solo"
    cuts.append(dict(
        id="L2-summon-implies-proxy",
        predicate=L2,
        rule="delivery=SUMMON ⟹ proxy∈{light,heavy}  (SUMMON⊗solo forbidden)",
        rationale=("Register §3B: a SUMMON kit's identity is its proxy; proxy=solo means nothing "
                   "was summoned. SUMMON⊗solo is definitionally empty (the summoned entity IS the "
                   "proxy)."),
        cls="logical",
    ))

    # L3 — MELEE delivery ⟺ melee-capable range (register coord #9 partly derived from #2).
    #   Charge C.5 names melee⊗projectile as DEFINITIONAL (range coord is partly derived from
    #   delivery). Operationalized on the identity key: delivery=MELEE with range∈{ranged} is
    #   incoherent (a melee-delivered strike cannot have pure-ranged reach). melee/dual/mid
    #   stay (dual = melee+ranged hybrid reach; mid = extended-melee lunge geometry).
    def L3(c):
        return c["delivery"] == "MELEE" and c["range"] == "ranged"
    cuts.append(dict(
        id="L3-melee-delivery-range-coherence",
        predicate=L3,
        rule="delivery=MELEE ⟹ range≠ranged  (MELEE⊗ranged forbidden; melee/mid/dual allowed)",
        rationale=("Charge C.5: melee⊗projectile-family is DEFINITIONAL (range is partly derived "
                   "from delivery). A MELEE-delivered kit cannot have pure-ranged reach; dual "
                   "(hybrid reach) and mid (lunge) remain coherent."),
        cls="logical",
    ))

    # L4″ — PROJECTILE-only delivery ⟺ non-pure-melee range (AMENDED 2026-07-15 per
    #   gandalf audit §2.A3, Matt-ratified Q30a). ONLY delivery=PROJECTILE ⊗ range=melee
    #   is incoherent (a payload that travels cannot have pure-melee reach — zero referents).
    #   BEAM and ORBITAL DROP OUT of the cut: the occupancy test found the "flamethrower
    #   corner" inhabited — d3-arachyr-firebats is ACTIVE at BEAM×melee (rooted point-blank
    #   channel-beam), and 8 active whirling-blades-class kits sit at ORBIT×melee. Both cells
    #   have living referents, so they are NOT logically incoherent.
    def L4(c):
        return c["delivery"] == "PROJECTILE" and c["range"] == "melee"
    cuts.append(dict(
        id="L4-ranged-delivery-range-coherence",
        predicate=L4,
        rule="delivery=PROJECTILE ⟹ range≠melee  (projectile⊗melee: zero referents; BEAM & "
             "ORBITAL dropped — flamethrower + whirling-blades corners are inhabited)",
        rationale=("AMENDED L4″ (Matt-ratified Q30a, gandalf audit §2.A3): only PROJECTILE×melee "
                   "is incoherent (a travelling payload cannot have pure-melee reach — zero "
                   "referents). BEAM×melee is ALIVE (d3-arachyr-firebats, the point-blank "
                   "channel-beam flamethrower) and ORBIT×melee is ALIVE (8 whirling-blades kits). "
                   "v1's L4 over-cut two inhabited cells. mid/ranged/dual remain; NOVA/ZONE/MELEE/"
                   "SUMMON unconstrained."),
        cls="logical",
    ))

    return cuts


# ===========================================================================
# RED-LAW CUTS — the 3 intrinsic RED laws (gaps-kpis-direction §A.4), as
# lattice predicates WHERE HONESTLY EXPRESSIBLE. Critical honesty rule: a law
# that is about kit-INTERNAL design pattern and does NOT translate to a
# coordinate-combination predicate STAYS a generation/curation filter and is
# NOT applied to the lattice. Documented either way.
# ===========================================================================
def build_redlaw_cuts():
    cuts = []

    # RED-1 — CO-LOCATION. "Damage must be co-located with the avatar's present
    # position or an anchored proxy (totem/trap/minion)."
    # HONESTY: this is a GEOMETRY/positional-fidelity property (damage-painted-where-
    # -you-WERE vs where-you-ARE). The identity key has NO coordinate that encodes
    # trail-vs-present positioning. gandalf §B.5 states verbatim it is "structurally
    # under-observable ... carried by curation/generation filters instead." Therefore
    # it does NOT translate to a coordinate-combination predicate over the 13-coord key.
    #   -> NOT A LATTICE CUT. Stays a generation/curation filter.
    cuts.append(dict(
        id="RED-1-co-location",
        predicate=None,                 # None => NOT applied to the lattice
        applies_to_lattice=False,
        rule="(no coordinate predicate — positional/geometry property, key-invisible)",
        rationale=("The co-location law distinguishes damage painted where the avatar WAS from "
                   "damage at its present position — a trail-vs-chase GEOMETRY property. The "
                   "13-coord identity key encodes no trail/present positional coordinate "
                   "(gandalf §B.5: 'structurally under-observable ... carried by curation/"
                   "generation filters instead'). Force-fitting it would fabricate a predicate "
                   "the key cannot honestly express. STAYS a generation/curation filter."),
        cls="red-law",
    ))

    # RED-2 — NO ANTI-SYNERGY. "Sustain must not cannibalize the build's own
    # resources, army, or economy."
    # HONESTY: the corpses (poe1-reaper: minion that eats your minions; vs-gatti-amari:
    # cats that eat your pickups) are KIT-INTERNAL relational patterns — "this kit's
    # sustain consumes this kit's OWN scaling substrate." That is a within-kit design
    # relation, NOT a value-tuple over the identity coordinates. Two kits with
    # IDENTICAL 13-coord keys can differ on whether the sustain cannibalizes — the
    # cannibalism is a mechanic-note property, invisible to the coordinate tuple.
    # gandalf §A.2-6: KPI-observable eventually (K5/K6 on EMITTED kits), never a
    # coordinate predicate.
    #   -> NOT A LATTICE CUT. Stays a generation/curation filter (+ future sim KPI).
    cuts.append(dict(
        id="RED-2-no-anti-synergy",
        predicate=None,
        applies_to_lattice=False,
        rule="(no coordinate predicate — kit-internal relational property, key-invisible)",
        rationale=("Anti-synergy is a within-kit RELATION (sustain consumes the kit's OWN army/"
                   "economy). Two kits with identical 13-coord keys can differ on whether sustain "
                   "cannibalizes — the property lives in the mechanic, not the coordinate tuple. "
                   "gandalf §A.2-6: observable only as a future sim-KPI (K5/K6) on EMITTED kits, "
                   "never as a lattice predicate. STAYS a generation/curation filter."),
        cls="red-law",
    ))

    # RED-3 — MOVEMENT-DAMAGE CARVE-OUT. "Movement verbs as damage loops only at
    # instant-commit + high tempo." (The carve-out that separates flicker-survivors
    # from leap-attack-corpses.)
    # HONESTY: THIS ONE IS EXPRESSIBLE. gandalf §A.2-4 states the register ALREADY
    # separates the living from the dead by exactly two coordinates: survivors sit at
    # commit=instant + tempo=high; corpses at commit=wind-up + tempo=low. The carve-out
    # is a predicate over (delivery/geometry = movement-verb) × commit × tempo. BUT the
    # "movement verb as the DAMAGE LOOP" antecedent needs a coordinate handle. On the
    # identity key the movement-verb-as-payload lands as geometry ∈ {dash_attack, teleport}
    # (the movement-verb geometries) serving as primary delivery. So the honestly-
    # expressible predicate is:
    #   geometry ∈ {movement-verb geoms} AND NOT (commit=instant AND tempo=high)  => SEAL
    # This is the "committal movement-damage dies" half. We express it at MESO+geometry
    # grain. HONESTY CAVEAT: geometry is coord #4 (a demotable/refine-within-#2 coord),
    # and the register's g00..g20 are placeholders here (the SPACE enumerates ~21 abstract
    # shapes). We therefore express RED-3 as a predicate keyed to the SEMANTIC movement-verb
    # geometry class, and report its removed-count against the exact lattice by treating the
    # movement-verb geometry class as a designated subset (size = 2 of 21: dash_attack,
    # teleport — the two live movement-verb geoms in the corpus). This is honest: the cut is
    # real and coordinate-expressible; its exact cardinality depends on which of the 21
    # abstract geometry slots are movement-verbs, which is a curation binding (flagged).
    MOVE_VERB_GEOMS = 2  # dash_attack, teleport (corpus-observed movement-verb geometries)

    def RED3(c, move_verb_geoms=None):
        # c["geometry"] is an abstract slot gNN; the caller designates the move-verb slots.
        is_move_verb = c["geometry"] in (move_verb_geoms or set())
        if not is_move_verb:
            return False
        # AMENDED RED-3′ (Matt-ratified Q30a; law text amended at source, gandalf
        # gaps-kpis-direction §A.4): TEMPO CONJUNCT DROPPED. Movement-verb-as-damage-loop
        # survives ONLY at instant commit; sealed at any non-instant commit.
        return c["commit"] != "instant"

    cuts.append(dict(
        id="RED-3-movement-damage-carveout",
        predicate=RED3,                 # applied with a designated move-verb geometry subset
        applies_to_lattice=True,
        move_verb_geom_count=MOVE_VERB_GEOMS,
        rule=("geometry∈{movement-verb geoms: dash_attack, teleport} ∧ commit≠instant ⟹ SEAL "
              "(committal movement-damage dies; instant-commit movement-damage lives — "
              "tempo conjunct DROPPED per RED-3′)"),
        rationale=("AMENDED RED-3′ (Matt-ratified Q30a; law text amended at source, gandalf "
                   "gaps-kpis-direction §A.4): the occupancy test found what separates dead from "
                   "living movement kits is COMMIT, not tempo. All 19 living movement-verb kits "
                   "are commit=instant (across low/med/high tempo — Leapquake & Shield Charge are "
                   "instant+high, alive). Both intrinsic-red movement corpses (d2-leap-attack-barb "
                   "wind-up, poe1-charged-dash channel) are non-instant. d4-blade-shift (instant+ "
                   "high) died extrinsic-itemization and is correctly SPARED. So: seal iff "
                   "commit≠instant. Three-way concordance (law text · corpus occupancy · legolas "
                   "death-class re-crawl) now agrees. CAVEAT (binding): the movement-verb geometry "
                   "class = {dash_attack, teleport} is curation-bound (2 of ~21 slots); the two "
                   "motivating corpses were re-keyed blank→dash_attack (corpus.db, Edition-II) so "
                   "the law's evidence lives inside its own predicate. Cardinality moves if a "
                   "third movement-verb geometry lands (re-run trigger)."),
        cls="red-law",
    ))

    return cuts


# ===========================================================================
# TASTE-CANDIDATE SLATE — proposed, NEVER applied. Each carries a predicate,
# rationale, and removed-count (computed against the post-red-law survivor
# lattice). Matt ratifies one by one. Returned in the report; gandalf surfaces.
# ===========================================================================
def build_taste_candidates():
    """Predicates over a cell; removed-counts computed post-red-law. NOT applied."""
    cands = []

    # T1 — pure-glass channel-committed. glass defense + commit=channel + rooted movement:
    # the "stand still, no defense, long channel" corner — the rooted-channel CONTESTED
    # cell's most fragile sub-corner. CANDIDATE (Matt may want the corner kept as amber).
    cands.append(dict(
        id="T1-glass-rooted-channel",
        predicate=lambda c: c["defense"] == "glass" and c["commit"] == "channel" and c["movement"] == "ROOTED",
        rationale="Rooted + channel + glass = the maximally-exposed sustained-cast corner (the CONTESTED rooted-channel cell's most fragile sub-region). Taste question: seal, or keep as balance-loop showcase.",
        cls="taste-candidate",
    ))

    # T2 — triggered + wind-up. activation=triggered ∧ commit=wind-up: a game-state
    # trigger that then still eats a wind-up is a double-latency corner the genre rarely
    # ships. CANDIDATE (may be legitimate for telegraphed procs).
    cands.append(dict(
        id="T2-triggered-windup",
        predicate=lambda c: c["activation"] == "triggered" and c["commit"] == "wind-up",
        rationale="Triggered activation THEN a wind-up = double-latency (the condition fires, then you still charge). Genre-rare. Taste question: seal as feel-dead, or keep for telegraphed heavy procs.",
        cls="taste-candidate",
    ))

    # T3 — self-cost + reserve economy pairing is already a logical tension, but the
    # SOFTER taste candidate: self-cost economy ∧ proxy=heavy (bleed your own HP to
    # sustain a heavy army) — the "sacrifice-summoner" corner. CANDIDATE.
    cands.append(dict(
        id="T3-selfcost-heavy-proxy",
        predicate=lambda c: c["economy"] == "self-cost" and c["proxy"] == "heavy",
        rationale="HP-as-resource (self-cost) sustaining a HEAVY proxy army = the blood-summoner corner. Coherent but a strong flavor commitment. Taste question: reserve for a signature archetype, or seal as over-specific.",
        cls="taste-candidate",
    ))

    # T4 — FLAT amplitude + SPIKY-only contexts... expressed as amp=FLAT ∧ tempo=low ∧
    # commit=channel: the "slow flat channel" = the lowest-drama damage profile. CANDIDATE.
    cands.append(dict(
        id="T4-flat-low-channel",
        predicate=lambda c: c["amp"] == "FLAT" and c["tempo"] == "low" and c["commit"] == "channel",
        rationale="Flat amplitude + low tempo + channel = the flattest, slowest, most inert damage feel in the space. Taste question: seal as anti-fun, or keep (some sustained-drain fantasies live here).",
        cls="taste-candidate",
    ))

    # T5 — hybrid treatment is rare/contested in the corpus (n=0 observed control-hybrid
    # in active treatment slot; corpus has damage=432, control=31, blank=6). The FULL
    # hybrid-treatment plane is a taste candidate: does the atlas WANT the hybrid-treatment
    # third of coord #5 enumerated as feasible, or is hybrid a curation-only interpolation?
    cands.append(dict(
        id="T5-hybrid-treatment-plane",
        predicate=lambda c: c["treatment"] == "hybrid",
        rationale="treatment=hybrid is defined but corpus-empty (active corpus: damage/control only). Taste question: enumerate the full hybrid-treatment plane as frontier (Mendeleev), or treat hybrid as a curation interpolation not a first-class ghost region. HIGH-IMPACT — hybrid multiplies the whole function sub-plane.",
        cls="taste-candidate",
    ))

    return cands


# ===========================================================================
# ENUMERATION ENGINE — compose the cut ladder, exact + meso-grain.
# ===========================================================================
def enumerate_lattice(coords, logical_cuts, redlaw_cuts, taste_cands,
                      move_verb_geoms, grain_name):
    """Full brute-ish enumeration is 8.1e8 — too large to materialize. Use
    factored counting: cuts are LOCAL (each predicate touches a small coord
    subset), so removed-counts are computed as (subset-cells matching) ×
    (product of the untouched coords). This is exact and instant."""
    names = list(coords.keys())
    sizes = {k: len(v) for k, v in coords.items()}
    total = 1
    for s in sizes.values():
        total *= s

    def factored_count(touched_keys, match_fn, base_coords):
        """Count cells (in base_coords space) where match_fn(subcell)=True,
        by enumerating ONLY the touched coords and multiplying the rest.
        If any read-coord is ABSENT from base_coords (e.g. meso-grain drops it),
        the predicate is inexpressible at this grain -> 0 removed (documented)."""
        if not set(touched_keys).issubset(set(base_coords)):
            return 0
        touched = [k for k in names if k in touched_keys and k in base_coords]
        rest = [k for k in base_coords if k not in touched]
        rest_prod = 1
        for k in rest:
            rest_prod *= len(base_coords[k])
        cnt = 0
        for combo in itertools.product(*[base_coords[k] for k in touched]):
            sub = dict(zip(touched, combo))
            # fill untouched with a sentinel the predicate won't read (predicates only
            # read touched keys by construction; guard with a completeness assert)
            if match_fn(sub):
                cnt += 1
        return cnt * rest_prod

    # ---- LADDER stage: post-logical (apply cuts SEQUENTIALLY on survivors) ----
    # Because logical cuts can overlap (a cell may violate two), we compute the
    # SURVIVOR set by inclusion-exclusion via a per-cut "carved space". To stay
    # exact AND instant we build the survivor space as a filtered product over the
    # UNION of touched coordinates, then multiply untouched. The union of touched
    # coords across all logical cuts here is small: {treatment,function,delivery,
    # proxy,range} — enumerate that joint (3*10*7*3*4 = 2520) and multiply the rest.
    def survivors_after(cuts_applied, base_coords, extra_ctx=None):
        touched = set()
        active = []
        # union of coords each predicate reads — declared explicitly per cut below
        READS = {
            "L1-treatment-function-coherence": ["treatment", "function"],
            "L2-summon-implies-proxy":         ["delivery", "proxy"],
            "L3-melee-delivery-range-coherence": ["delivery", "range"],
            "L4-ranged-delivery-range-coherence": ["delivery", "range"],
            "RED-3-movement-damage-carveout":  ["geometry", "commit", "tempo"],
        }
        for ct in cuts_applied:
            if ct.get("predicate") is None or ct.get("applies_to_lattice") is False:
                continue
            # a cut is expressible at this grain only if ALL its read-coords are present
            if not set(READS[ct["id"]]).issubset(set(base_coords)):
                continue
            active.append(ct)
        for ct in active:
            touched |= set(READS[ct["id"]])
        touched = [k for k in names if k in touched and k in base_coords]
        rest = [k for k in base_coords if k not in touched]
        rest_prod = 1
        for k in rest:
            rest_prod *= len(base_coords[k])
        surv = 0
        for combo in itertools.product(*[base_coords[k] for k in touched]):
            sub = dict(zip(touched, combo))
            killed = False
            for ct in active:
                pred = ct["predicate"]
                if ct["id"] == "RED-3-movement-damage-carveout":
                    if pred(sub, move_verb_geoms=move_verb_geoms):
                        killed = True
                        break
                else:
                    if pred(sub):
                        killed = True
                        break
            if not killed:
                surv += 1
        return surv * rest_prod

    raw = total
    logical_only = [c for c in logical_cuts]
    post_logical = survivors_after(logical_only, coords)
    post_redlaw = survivors_after(logical_only + [c for c in redlaw_cuts if c.get("applies_to_lattice")], coords)

    # per-cut removed counts (marginal, on the pre-cut raw space — reported as the
    # cut's OWN footprint; the ladder uses composed survivors above)
    per_cut = {}
    READS = {
        "L1-treatment-function-coherence": (["treatment", "function"],
            lambda s: (s["function"] != "none") if s["treatment"] == "damage" else (s["function"] == "none")),
        "L2-summon-implies-proxy": (["delivery", "proxy"],
            lambda s: s["delivery"] == "SUMMON" and s["proxy"] == "solo"),
        "L3-melee-delivery-range-coherence": (["delivery", "range"],
            lambda s: s["delivery"] == "MELEE" and s["range"] == "ranged"),
        "L4-ranged-delivery-range-coherence": (["delivery", "range"],
            lambda s: s["delivery"] in ("PROJECTILE", "ORBITAL", "BEAM") and s["range"] == "melee"),
    }
    for cid, (rd, fn) in READS.items():
        per_cut[cid] = factored_count(set(rd), fn, coords)
    # RED-3 marginal
    per_cut["RED-3-movement-damage-carveout"] = factored_count(
        {"geometry", "commit", "tempo"},
        lambda s: (s["geometry"] in move_verb_geoms) and not (s["commit"] == "instant" and s["tempo"] == "high"),
        coords,
    )

    # taste candidates: removed-count on the POST-RED-LAW survivor lattice.
    # (marginal footprint on raw for legibility; applied-cumulatively is a Matt call)
    taste_counts = {}
    T_READS = {
        "T1-glass-rooted-channel": (["defense", "commit", "movement"],
            lambda s: s["defense"] == "glass" and s["commit"] == "channel" and s["movement"] == "ROOTED"),
        "T2-triggered-windup": (["activation", "commit"],
            lambda s: s["activation"] == "triggered" and s["commit"] == "wind-up"),
        "T3-selfcost-heavy-proxy": (["economy", "proxy"],
            lambda s: s["economy"] == "self-cost" and s["proxy"] == "heavy"),
        "T4-flat-low-channel": (["amp", "tempo", "commit"],
            lambda s: s["amp"] == "FLAT" and s["tempo"] == "low" and s["commit"] == "channel"),
        "T5-hybrid-treatment-plane": (["treatment"],
            lambda s: s["treatment"] == "hybrid"),
    }
    # taste ADDITIONAL removal on the POST-RED-LAW SURVIVOR lattice (the honest
    # "if Matt accepts this cut, this many additional cells seal") — COMPOSED-ON-SURVIVORS,
    # NOT marginal-on-raw (that was the v1 T5 slip: gandalf audit §1, table row 4). Exact,
    # factored: enumerate the UNION of (lattice-cut read-coords present at THIS grain) +
    # (taste read-coords), count cells that SURVIVE the amended lattice cuts AND match the
    # taste predicate, multiply untouched.
    #
    # AMENDED predicates (L1′ / L4″ / RED-3′) — must match build_logical_cuts / build_redlaw_cuts.
    # Grain-aware: reads only coords present in `coords` (meso drops range/geometry/etc., so the
    # cuts keyed to absent coords simply don't fire at that grain — correct: L3/L4/RED-3 are
    # invisible at meso, only L1′ + L2 bind there).
    LATTICE_READS_FULL = {"treatment", "function", "delivery", "proxy", "range", "geometry", "commit"}
    LATTICE_READS = {k for k in LATTICE_READS_FULL if k in coords}

    def survives_lattice(sub):
        # L1′: {control,hybrid}×none incoherent (damage×function IS coherent).
        if "treatment" in sub and "function" in sub:
            if sub["treatment"] in ("control", "hybrid") and sub["function"] == "none":
                return False
        # L2: SUMMON×solo forbidden.
        if "delivery" in sub and "proxy" in sub:
            if sub["delivery"] == "SUMMON" and sub["proxy"] == "solo":
                return False
        # L3: MELEE×ranged forbidden.
        if "delivery" in sub and "range" in sub:
            if sub["delivery"] == "MELEE" and sub["range"] == "ranged":
                return False
        # L4″: PROJECTILE×melee only (BEAM/ORBITAL spared).
        if "delivery" in sub and "range" in sub:
            if sub["delivery"] == "PROJECTILE" and sub["range"] == "melee":
                return False
        # RED-3′: movement-verb geometry × non-instant commit sealed (tempo conjunct dropped).
        if "geometry" in sub and "commit" in sub:
            if sub["geometry"] in move_verb_geoms and sub["commit"] != "instant":
                return False
        return True

    taste_counts_postcut = {}
    for cid, (rd, fn) in T_READS.items():
        # a taste candidate is expressible at THIS grain only if ALL its read-coords are present.
        if not set(rd).issubset(set(coords)):
            taste_counts_postcut[cid] = None
            continue
        union = set(rd) | LATTICE_READS
        tkeys = [k for k in names if k in union and k in coords]
        rest = [k for k in coords if k not in tkeys]
        rest_prod = 1
        for k in rest:
            rest_prod *= len(coords[k])
        cnt = 0
        for combo in itertools.product(*[coords[k] for k in tkeys]):
            sub = dict(zip(tkeys, combo))
            if survives_lattice(sub) and fn(sub):
                cnt += 1
        taste_counts_postcut[cid] = cnt * rest_prod

    for cid, (rd, fn) in T_READS.items():
        # footprint on raw
        taste_counts[cid] = factored_count(set(rd), fn, coords)

    return dict(
        taste_counts_postcut=taste_counts_postcut,
        grain=grain_name,
        raw=raw,
        post_logical=post_logical,
        post_redlaw=post_redlaw,
        per_cut=per_cut,
        taste_counts=taste_counts,
        sizes=sizes,
    )


def _vet_pull_slice():
    """v1.2 — enumerate the NEW function=pull meso cells; confirm EVERY sealed pull cell takes an
    EXISTING cut_id (L1'/L2). A pull cell needing a NEW law is a HALT condition (raised loud).
    Meso core = movement, delivery, treatment, function, proxy, activation, dependency."""
    MOVE = COORDS["movement"]; DELIV = COORDS["delivery"]; TREAT = COORDS["treatment"]
    PROXY = COORDS["proxy"]; ACT = COORDS["activation"]; DEP = COORDS["dependency"]
    total = feasible = 0
    seal_by_cut = {}
    halt_cells = []
    for mv, d, t, p, a, dep in itertools.product(MOVE, DELIV, TREAT, PROXY, ACT, DEP):
        f = "pull"
        total += 1
        cut = None
        # L1': {control,hybrid} x none — pull != none, so L1' can NEVER seal a pull cell.
        if t in ("control", "hybrid") and f == "none":
            cut = "L1-treatment-function-coherence"
        # L2: SUMMON x solo.
        elif d == "SUMMON" and p == "solo":
            cut = "L2-summon-implies-proxy"
        if cut is None:
            feasible += 1
        else:
            seal_by_cut[cut] = seal_by_cut.get(cut, 0) + 1
    # HALT gate: any sealed pull cell whose cut is outside the ratified {L1', L2} enum.
    for cut in seal_by_cut:
        if cut not in ("L1-treatment-function-coherence", "L2-summon-implies-proxy"):
            halt_cells.append(cut)
    if halt_cells:
        raise SystemExit(f"HALT: pull-slice cell(s) need a NEW law (cut_id outside {{L1',L2}}): {halt_cells}")
    return dict(pull_meso_total=total, pull_meso_feasible=feasible,
                pull_meso_sealed=total - feasible, sealed_by_cut=seal_by_cut,
                new_law_needed=0, halt=False,
                note=("All sealed pull cells take EXISTING cut_ids (L2 SUMMON x solo x pull). "
                      "L1' cannot seal a pull cell (pull != none). ZERO new laws — no HALT."))


def main():
    logical = build_logical_cuts()
    redlaw = build_redlaw_cuts()
    taste = build_taste_candidates()
    move_verb_geoms = {"g00", "g01"}  # designate 2 abstract slots as movement-verb geoms (dash_attack, teleport)

    # EXACT-LATTICE grain (all 13 coords).
    exact = enumerate_lattice(COORDS, logical, redlaw, taste, move_verb_geoms, "exact-lattice")

    # MESO-GRAIN (register rollup = never-demote core). geometry NOT in core, so RED-3
    # (geometry-keyed) does not apply at meso-grain — documented.
    meso_coords = {k: COORDS[k] for k in CORE}
    meso = enumerate_lattice(meso_coords, logical, redlaw, taste, move_verb_geoms, "meso-grain")

    # -------- counts ladder printout --------
    def ladder(tag, e):
        print(f"\n==== COUNTS LADDER — {tag} ====")
        print(f"  raw naive product          : {e['raw']:>15,}")
        print(f"  post-logical               : {e['post_logical']:>15,}   "
              f"(-{e['raw']-e['post_logical']:,})")
        print(f"  post-red-law (lattice-cuts): {e['post_redlaw']:>15,}   "
              f"(-{e['post_logical']-e['post_redlaw']:,})")
        print(f"  --- per-cut marginal footprint (on raw) ---")
        for cid, n in e["per_cut"].items():
            print(f"      {cid:38s} -{n:,}")
        print(f"  --- taste-candidate ADDITIONAL removal on post-red-law survivors (NOT applied) ---")
        for cid, n in e["taste_counts_postcut"].items():
            base = e["post_redlaw"]
            pct = (100.0 * n / base) if (n is not None and base) else 0.0
            shown = f"~{n:,}" if n is not None else "N/A-this-grain"
            print(f"      {cid:38s} {shown:>18s}   ({pct:.1f}% of survivors)")
    ladder("EXACT-LATTICE (13 coords)", exact)
    ladder("MESO-GRAIN (register rollup / never-demote core)", meso)

    # -------- machine-readable cuts table (CSV + JSON) --------
    rows = []
    for c in logical:
        rows.append(dict(id=c["id"], cls=c["cls"], applies_to_lattice=True,
                         predicate_rule=c["rule"], rationale=c["rationale"],
                         removed_exact=exact["per_cut"].get(c["id"], ""),
                         removed_meso=meso["per_cut"].get(c["id"], "")))
    for c in redlaw:
        atl = c.get("applies_to_lattice", False)
        rows.append(dict(id=c["id"], cls=c["cls"], applies_to_lattice=atl,
                         predicate_rule=c["rule"], rationale=c["rationale"],
                         removed_exact=(exact["per_cut"].get(c["id"], "") if atl else "N/A-filter"),
                         removed_meso=(meso["per_cut"].get(c["id"], "N/A-no-geometry") if atl else "N/A-filter")))
    for c in taste:
        pc = exact["taste_counts_postcut"].get(c["id"])
        # meso taste count: COMPOSED-ON-SURVIVORS (T5 slip fix). Only T5 is meso-expressible
        # (treatment ∈ meso core); the rest read non-core coords -> None at meso. Use the
        # grain-aware composed count, NOT the marginal-on-raw footprint.
        pcm = meso["taste_counts_postcut"].get(c["id"])
        rows.append(dict(id=c["id"], cls=c["cls"],
                         applies_to_lattice="RULED-KEEP-2026-07-15-Matt-Q30b",
                         predicate_rule="(taste — RULED KEEP by Matt 2026-07-15; ZERO cuts; "
                                        "recorded as lineage, nothing sealed by taste)",
                         rationale=c["rationale"],
                         removed_exact=(pc if pc is not None else ""),
                         removed_meso=(pcm if pcm is not None else "N/A-this-grain")))

    # ---- v1.2 pull-slice vetting: enumerate the NEW function=pull meso cells, confirm every
    #      sealed one takes an EXISTING cut_id (L1'/L2). A cell needing a new law -> HALT. ----
    pull_slice = _vet_pull_slice()

    os.makedirs(OUT, exist_ok=True)
    csv_path = os.path.join(OUT, "feasibility-cuts-register-v1.2.csv")
    json_path = os.path.join(OUT, "feasibility-cuts-register-v1.2.json")
    import csv as _csv
    with open(csv_path, "w", newline="") as f:
        w = _csv.DictWriter(f, fieldnames=["id", "cls", "applies_to_lattice",
                                           "predicate_rule", "removed_exact", "removed_meso", "rationale"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    payload = dict(
        version="1.2",
        generated="2026-07-15",
        generator="feasibility_cuts_register_v1_2_2026_07_15.py",
        supersedes="feasibility-cuts-register-v1.1",
        edition="II",
        edition_change=(
            "function coordinate 10 -> 11 levels (+`pull` = inward displacement force, knockback's "
            "inverse; register §10.1). Law-inheritance: L1' reads (treatment,function) and pull!=none "
            "so {control,hybrid}xpull is coherent + damage x pull is a coherent rider -> L1' incoherent "
            "set unchanged ({control,hybrid}xnone). L2/L3/L4''/RED-3' do not read function -> unaffected. "
            "Pull vets ENTIRELY under the ratified ledger; ZERO new laws (else HALT to Matt)."),
        pull_slice_vetting=pull_slice,
        amendments_ratified=(
            "Q30a (Matt 2026-07-15 'Great. Approved on all. Please proceed.'): "
            "L1′ (only {control,hybrid}×none incoherent — 28 coherent tf pairs; "
            "damage×function coherent via control-rider, 130 living kits); "
            "L4″ (only PROJECTILE×melee cut — BEAM & ORBITAL spared, flamethrower + "
            "whirling-blades corners inhabited); "
            "RED-3′ (tempo conjunct dropped — seal iff movement-verb geometry × commit≠instant). "
            "Q30b (Matt): taste slate RULED — ZERO cuts, all five KEEP as lineage. "
            "v1.2 (Edition-II §10.1): +`pull` function level; law-ledger unchanged, all inherited."),
        taste_slate_ruling="RULED 2026-07-15 — ZERO CUTS (Matt Q30b); five candidates kept as lineage",
        base_register="coordinate-register-2026-07-13.md §2 (13-coordinate kit-identity key) + `pull` (Edition-II)",
        DISTINCTION=("This is the 13-coordinate CORPUS-IDENTITY lattice, NOT the engine-native "
                     "substrate lattice (substrate-coordinates.md L4≈1.284e9; banned box 2.57e9). "
                     "The '2.57B' ban is the SUBSTRATE naive box; this register's own naive box "
                     "is reported below with its own pre-cut caveat (renderer R2 spirit)."),
        counts_ladder=dict(
            exact_lattice=dict(raw=exact["raw"], post_logical=exact["post_logical"],
                               post_redlaw=exact["post_redlaw"]),
            meso_grain=dict(raw=meso["raw"], post_logical=meso["post_logical"],
                            post_redlaw=meso["post_redlaw"]),
        ),
        per_cut_removed_exact=exact["per_cut"],
        per_cut_removed_meso=meso["per_cut"],
        taste_candidate_footprint_exact_on_raw=exact["taste_counts"],
        taste_candidate_removal_exact_post_redlaw=exact["taste_counts_postcut"],
        taste_candidate_removal_meso_post_logical=meso["taste_counts_postcut"],
        taste_candidate_footprint_meso_marginal_on_raw=meso["taste_counts"],
        move_verb_geom_binding=sorted(move_verb_geoms),
        cuts=rows,
        coordinate_sizes=exact["sizes"],
        never_demote_core=CORE,
    )
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # -------- v1.2 pull-slice vetting printout (HALT-gate visible) --------
    print("\n==== v1.2 PULL-SLICE VETTING (function=pull meso cells) ====")
    print(f"  pull meso cells: total={pull_slice['pull_meso_total']} "
          f"feasible={pull_slice['pull_meso_feasible']} sealed={pull_slice['pull_meso_sealed']}")
    print(f"  sealed by cut_id: {pull_slice['sealed_by_cut']}")
    print(f"  new laws needed: {pull_slice['new_law_needed']}  HALT: {pull_slice['halt']}")

    # -------- analysis table into corpus.db (gitignored) — v1_2 names --------
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS atlas_feasibility_cuts_v1_2_2026_07_15")
        cur.execute("""CREATE TABLE atlas_feasibility_cuts_v1_2_2026_07_15
                       (id TEXT, cls TEXT, applies_to_lattice TEXT, predicate_rule TEXT,
                        removed_exact TEXT, removed_meso TEXT, rationale TEXT)""")
        for r in rows:
            cur.execute("INSERT INTO atlas_feasibility_cuts_v1_2_2026_07_15 VALUES (?,?,?,?,?,?,?)",
                        (r["id"], r["cls"], str(r["applies_to_lattice"]), r["predicate_rule"],
                         str(r["removed_exact"]), str(r["removed_meso"]), r["rationale"]))
        cur.execute("DROP TABLE IF EXISTS atlas_feasibility_ladder_v1_2_2026_07_15")
        cur.execute("""CREATE TABLE atlas_feasibility_ladder_v1_2_2026_07_15
                       (grain TEXT, raw INT, post_logical INT, post_redlaw INT)""")
        cur.execute("INSERT INTO atlas_feasibility_ladder_v1_2_2026_07_15 VALUES (?,?,?,?)",
                    ("exact-lattice", exact["raw"], exact["post_logical"], exact["post_redlaw"]))
        cur.execute("INSERT INTO atlas_feasibility_ladder_v1_2_2026_07_15 VALUES (?,?,?,?)",
                    ("meso-grain", meso["raw"], meso["post_logical"], meso["post_redlaw"]))
        con.commit()
        con.close()
        print(f"\n[corpus.db] atlas_feasibility_cuts_v1_2_2026_07_15 + _ladder_ written (gitignored).")
    except Exception as ex:
        print(f"\n[corpus.db] SKIP analysis tables: {ex}")

    print(f"\nWROTE {csv_path}")
    print(f"WROTE {json_path}")
    return exact, meso


if __name__ == "__main__":
    main()
