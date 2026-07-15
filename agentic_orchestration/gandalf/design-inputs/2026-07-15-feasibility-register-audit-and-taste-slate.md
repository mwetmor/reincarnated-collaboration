# Feasibility-Cuts Register v1 — gandalf Audit + Taste-Slate Surface (Q30)

> **STATUS:** CURRENT (load-bearing as of 2026-07-15) — the charter-mandated audit of elrond's register (charter: *"elrond executes; gandalf audits; Matt ratifies taste cuts"*) + the taste-cut decision surface.

**Date:** 2026-07-15 · **Author:** gandalf (`▶ ROLE: DRIFT-CRITIC` for §§1–3 audit · `SPEC-AUTHOR` for §4 leans)
**Audits:** `agentic_orchestration/research/curated/atlas/feasibility-cuts-register-v1.md` (elrond, commit `d5cf6a5a`)
**Verification method:** independent re-derivation of every count (block-factorization arithmetic, separate script); **occupancy test** — every cut predicate checked against the real corpus (469 active + 37 corpse `cell_key`s in `corpus.db`); legolas findings.jsonl structure + evidence spot-check.
**Companion:** `2026-07-14-gate-b-diagnosis-and-proposed-ruling.md` (F-1); `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §2/§4; `gaps-kpis-direction-analysis.md` §A.4 (the red laws).

---

## 1. Audit verdict — split verdict

| Dimension | Verdict |
|---|---|
| **Arithmetic as-built** | ✅ **VERIFIED EXACT** — every number re-derived independently and matched to the digit: raw box 900,169,200; post-logical 461,515,320; post-red-law 422,445,240; all four logical marginals; RED-3 marginal 76,204,800 + composed 39,070,080; all five taste counts + percentages. Zero arithmetic errors in the ladder. |
| **RED-1 / RED-2 honesty exclusion** | ✅ **RIGHT CALL** — key-invisible relational properties kept off the lattice as generation/curation filters. Exactly the no-force-fit discipline the brief demanded. |
| **Cut predicates vs the real corpus** | ⚠ **THREE FALSIFIED BY INHABITED CELLS** (§2). The register never ran the occupancy test — do real kits sit in "logically impossible" ground? 149 active kits do. |
| **Two mechanical slips** | ⚠ T5 meso footprint wrong in generator (3,780 → should be 3,240 under v1's own L1; propagated to .csv/.json/§2 footnote); §2 prose says RED-3 removes "~8.5% of the naive box" — it is 8.5% of the *post-logical survivors* (4.3% of naive). |

The falsifications are **not** arithmetic errors — they are predicate over-reach, and the register's own caveats half-anticipated one of them (the RED-3 binding flag). The audit turns flags into evidence.

---

## 2. Three falsifications (with the kits that falsify them)

### A1 — L1 over-cuts: `damage ⟺ function=none` is contradicted by 30% of the living corpus

The active treatment×function joint: **damage×hard-stop 33 · damage×stun 26 · damage×hex 24 · damage×knockback 16 · damage×expose 11 · damage×taunt 10 · damage×blind 7 · damage×fear 3 = 130 living kits** with damage treatment AND a control function. Frozen-Orb-class kits — damage primaries carrying a kit-designed control **rider** — are bedrock genre, and the curation ontology assigns them exactly that way. The coordinate register (§2 row 5, §6.1) never states one-concept exclusivity; L1 over-formalized it.

**Amendment L1′:** incoherent pairs are only **`{control, hybrid} × none`** (a control/hybrid kit must HAVE a function). Coherent pairs: 30 − 2 = **28** (was 19).
**Curation debt surfaced:** 9 active `control×none` rows sit in even-L1′-cut ground — function unassigned at crawl; elrond review.

### A2 — RED-3 mis-specified twice: it misses its own motivating corpses and seals living ground

Pulled every movement-verb-geometry kit in the corpus (19 active, dash_attack/teleport):

- **All 19 living movement kits are `commit=instant`** — tempo spans low (d2-charger), med (×9: d3-leapquake, d3-raekor-boulder, gd-shadow-strike-infiltrator, tq-shield-charge-conqueror…), high (×9: poe1-flicker, hades1-athena-dash…). The `instant∧high` consequent seals ground where **10 living kits stand** — Leapquake and Shield Charge are not dead ground.
- **The law's own corpses aren't in the predicate's reach:** d2-leap-attack-barb (`commit=wind-up`) and poe1-charged-dash (`commit=channel`) — both intrinsic-red — have **`geometry=blank`** (masked at crawl), so the geometry-keyed antecedent never fires on them. The predicate as operationalized catches zero of the deaths it encodes.
- **What actually separates dead from living in the data is COMMIT, not tempo:** both intrinsic-red movement corpses are non-instant; every living movement kit is instant. d4-blade-shift (instant+high, dash) died **extrinsic-itemization** (legolas verdict — no Aspect written for it), which the law should NOT seal.

**Amendment RED-3′ (law-text amendment — Matt ratifies):** *"Movement verbs as damage loops only at **instant commit**"* — drop the tempo conjunct. Predicate: `geometry∈{movement-verb} ∧ commit≠instant ⟹ SEAL`.
**Three-way concordance check:** RED-3′ seals exactly the two intrinsic-red movement corpses (wind-up, channel), spares the extrinsic-itemization corpse and all 19 living kits. The law text, the corpus occupancy, and legolas's independent death-class re-crawl now agree perfectly.
**Binding caveat stands** (elrond's flag, sharpened): the movement-verb geometry class is curation-bound {dash_attack, teleport}; the two motivating corpses need geometry re-keyed (blank → dash_attack) so the law's evidence lives inside its own predicate.

### A3 — L4 over-cuts: the flamethrower corner is inhabited

`BEAM×melee`: **d3-arachyr-firebats is ACTIVE there** (rooted point-blank channel-beam — the flamethrower archetype; d2-inferno-sorc is its corpse-twin, dead of tuning lore, not impossibility). `ORBIT×melee`: **8 active kits** (whirling-blades-class). Both cells have referents → not logically incoherent.

**Amendment L4″:** `delivery=PROJECTILE ⟹ range≠melee` only (projectile⊗melee: zero referents — a payload that travels cannot have pure-melee reach). BEAM and ORBITAL drop out of the cut.

**L2 and L3 STAND** — zero active or corpse referents in summon⊗solo or melee⊗ranged. ✅

---

## 3. Corrected ladder (provisional-for-decision; elrond regenerates the authoritative artifacts)

| stage | exact | meso |
|---|---|---|
| raw naive box | 900,169,200 | 11,340 |
| post-logical (L1′ + L2 + L3 + L4″) | **740,139,120** | **10,080** |
| post-red-law (RED-3′) | **693,146,160** | 10,080 |

Coverage denominator grows 422.4M → **693.1M** (the honest direction: we were over-claiming exploration by over-cutting the space). 469 active kits ≈ 6.8×10⁻⁵ % of exact grain. Meso ghost field = **10,080 cells** (still trivially renderable).

## 4. Taste slate against the corrected lattice — my leans (`SPEC-AUTHOR`)

Recomputed on the corrected survivors. **My lean: ratify ZERO taste cuts.** The seal bar is "we would NEVER ship this"; every candidate contains a shipped-or-shippable fantasy. Sealing is what red laws are for — none of these are red.

| id | predicate | removes | % | lean | why |
|---|---|---|---|---|---|
| **T5** hybrid-treatment plane | `treatment=hybrid` | 222,796,980 | 32.1% | **KEEP** | The engine's own ratified role taxonomy (2026-05-08, amended 2026-07-12) is **damage / control / hybrid** — hybrid is first-class in OUR generator. Cutting it seals the one region our engine explicitly intends to explore beyond genre (the corpus is hybrid-empty — that makes it the flagship frontier, not dead ground). Counter noted honestly: corpus curation has never assigned hybrid → **curation debt: define hybrid-assignment criteria before first engine-hybrid ingestion.** Cut-then-reopen would churn the devlog denominator. |
| **T2** triggered + wind-up | 111,608,280 | 16.1% | **KEEP** | Double-latency is unexplored, not dead — the parry-counter fantasy (condition fires → telegraphed heavy answer) lives here; genre-rare because genre engines are poor at telegraphs, not because it feels bad. Frontier means exactly this. |
| **T3** self-cost + heavy proxy | 34,791,120 | 5.0% | **KEEP** | The blood-summoner is a **proven signature archetype** — Last Epoch's Acolyte bleeds HP to sustain her army as class identity. Sealing a corner a competitor ships as a flagship would be self-blinding. |
| **T4** flat + low + channel | 24,801,840 | 3.6% | **KEEP** | The drain-life channel (WoW Warlock's Drain Life, V Rising's blood drain) is iconic. Weakest keep on the slate — but "inert as primary" is a tuning risk the balance loop prices, not an impossibility. |
| **T1** glass + rooted + channel | 14,881,104 | 2.1% | **KEEP** | The maximal-risk contract — huge damage if you dare stand still — is a genre staple. d4-incinerate died here of **D4's content mix** (mobile endgame; legolas verdict), while PoE1's rooted channels thrived in theirs: the cell is content-mix-dependent, NOT intrinsically dead. We control our own content mix; this is the balance loop's showcase corner. |

If Matt ratifies zero cuts: denominator stays 693,146,160 / meso 10,080; SEALED ground on the ghost field = logical + RED-3′ only.

## 5. Curation-debt list (elrond, no Matt gate)

1. Generator fix: T5 meso footprint bug (marginal-on-raw used where composed-on-survivors needed) + §2 prose slip; **regenerate register v1.1 under the ratified amendments** (one command, per its own provenance design).
2. 9 active `control×none` kits — assign functions.
3. Corpse geometry re-keys: d2-leap-attack-barb, poe1-charged-dash (+ d4-blade-shift check) blank → movement-verb geometry.
4. Ingest legolas re-crawl: 12 death_class verdicts + 32 tranche-1 mech_notes (proposed-value pattern honored — elrond writes, legolas never did).
5. Hybrid-assignment criteria memo (gates first engine-hybrid ingestion; from T5 ruling).

## 6. Legolas re-crawl relay (spot-checked ✅)

All 12 unknown corpses got verdicts, **zero researched-no-verdict**; 8/12 intrinsic-red — the unknowns skewed to design-level failures because tuning fixes would have been documented events; absence of documentation was itself signal. Record structure verified (kit_id / field / proposed_value / evidence_summary / sources / confidence); Grim Ward evidence trail cites the patch-2.4/2.5 lineage precisely. d4-incinerate → intrinsic-red (root-channel in mobile endgame) and d4-blade-shift → extrinsic-itemization both **cross-validate §2's amendments** from an independent evidence stream.

---

## Cross-references

Register: `research/curated/atlas/feasibility-cuts-register-v1.md` · legolas: `agentic_orchestration/legolas/research/census-recrawl-2026-07-14/findings.jsonl` (commit `c906a039`) · Q30 row: `canonical/matt_decision_needed/README.md` · charter §2/§4.

Tracker-delta: engine tracker SESSION-DELTA — register landed + audited (3 predicate amendments proposed, Matt-gated as Q30a); taste slate surfaced (Q30b); legolas verdicts in, elrond ingestion queued; ghost field gated on Q30.

---

**Signed:** gandalf
**For:** turning the register's flags into evidence, the evidence into amendments, and the slate into a decision Matt can rule in one line.
