# JOIN-1 · J1 — the self-join (B0), oracle side, deconfounded first

**NOT-A-GRADED-RUN. Read-only. No oracle code changed. No binder invented. Nothing tuned.**
gamora, 2026-10-02, Run JOIN-1 (charter v0.6, KC2 KP-229). Gate: jack-ryan Gate-2 on the schema-gap list (charter § 4.2).

- Pre-registration (committed alone first): engine `0a3e0a0e`, `simulation/math/kc2-join1-j0-ablation-j1-selfjoin-prereg-2026-10-02.md` § 5
- Harness: engine `6227374a`, `simulation/scripts/gamora_join1_j1_selfjoin_b0_2026_10_02.py`
- Emitted table: `b0_selfjoin.json` (this directory). Every value in it is read from its source when the harness runs. FILE digests are printed in its `pins` block: kit JSON `b82c9a0f…`, corpus.db `dffad643…`, kit_compiler.py `eef2dd4c…`, pm4g_played_kit.csv `2fd5a347…`.

## The verdict

**B0 does not reproduce the referent.** Zero of the four `EXECUTES-THE-BOUNDARY-RULEBOOK` rows (J-P2 § 2.1: TA-X-07, 20, 29, 30) can be reproduced numerically, because **the corpus path never reaches the arena**. `compile_kit` emits a class_dict for the spatial engine (`run_spatial_fight`). Nothing under `simulation/kc2/`, and no oracle script, consumes it.

**There are three divergent rows, and each has a PROPOSED disposition.** The pass rule (charter § 4.2) therefore resolves as follows: **B0 = PASS-BY-DISPOSITION if, and only if, jack-ryan's Gate-2 accepts the three dispositions. Until then B0 is UNGRADED, not PASS.**

**The APPROX ceiling applies to every B0 figure.** The corpus record is APPROX by its own deviation note, and it describes a different Warlord build from the referent save (Layer R).

### The differing-mechanism list (the rulebook's to-do)

| row | boundary | what differs | kind | proposed disposition |
|---|---|---|---|---|
| **B-BIND** | the corpus path reaching the arena | no consumer of the compiled kit in kc2. The kc2 player is assembled from the pack: PlayerOffense, SecondaryStreams, PlayerSustainFold, PlayerKitResidualFold, DefenceField, SummonFold, channel policy, P-MOVE | contract gap, compiler ↔ arena | `closes-in-J2`. J2's FORM/OPERAND split names the operand interface a compiled kit must fill; the binder itself is the J4 adapter piece |
| **TA-X-07** | hit resolution + monster→player mitigation (conservation) | the received-side defence operand (armour, resists): referent = the MEASURED defence sheet; corpus = `defense: {riders: []}` (R-G5 GAP) | the operand is absent; carried from C/R. Not a boundary-rule difference: the conservation identity holds for any operands | `schema-change-owed` (→ J-L4): received-side mitigation rows on the record, plus a defence field on the compiled contract |
| **TA-X-20** | hit-test predicate + target multiplicity | **the FORM agrees** (circle, no arc gate, no target cap). **The OPERAND is absent:** the EoR radius is 3.0 m on the referent (DB-CITED) and `geometry_params: {}` on the corpus | carried from R7 + C6 | `schema-change-owed` (→ J-L4): a DATAMINED radius row on the record, carried into `geometry_params` |
| TA-X-29 | global-magnitude fold | none. The fold reads monster records and wave modifiers only | kit-independent | none owed (conditional on B-BIND) |
| TA-X-30 | pursuit halt | none in form. `d_engage_m` = 2.4 is arena-side; the values depend on the pilot's trajectory | kit-independent in form | none owed (conditional on B-BIND) |

**What deconfounding shows.** None of the three divergences is a difference between the corpus path's boundary rules and the referent's. Two are kit operands the record does not carry and the compiler does not flag (TA-X-07, TA-X-20). The third is a contract that does not connect the two paths (B-BIND). **The two rows that exercise only world-side rules (TA-X-29, TA-X-30) take no kit operand, so a bound corpus kit would meet the same boundary rules as the referent.** That is the structural precondition B0 exists to establish, and it holds.

⚑ **Caveat (#86):** J-P2 classified the four EXECUTES rows against prereg v1.6 (v3.4.2). The v3.11 oracle adds folds on top of that configuration, but none of them is the kit↔world operand path these four rows consume. Their kit-dependence is carried by structure, not re-derived by a fixture on v3.11 (the J-S8 fixture is cut at star-lord's closure commit, per charter v0.6).

## Layer R: the record against the pack (the APPROX ceiling)

| id | field | record (`gd-eor-warlord.json`) | pack of record | verdict |
|---|---|---|---|---|
| R1 | castable skills | Eye of Reckoning, Judgment | EoR, Vire's Might, War Cry, Ascension, Blitz, Violent Delights, Weapon Attack, Guardian of Empyrion, Deathstalker; **Judgment: 0 of 324 rows** | DIFFERS. A different build; EoR is the only shared skill |
| R2 | element | `element_primary` null + `ELEMENT_CONVERSION_PHYSICAL`; corpus.db `original_element` = `court` = **fire** | EoR Fire→Physical 100 % (Gutsmasher), weapon Chaos/Lightning→Physical 50 %, Aether→Physical 25 % | the physical-converted identity AGREES. The conversion source differs. The record's raw element field says fire |
| R3 | resource | "energy-hungry channel + Beronath aura upkeep", no number | 13 mana/tick at rank 20; 0.16 s period at 100 % AS | qualitative only. The aura is not in the referent kit |
| R4 | devotion procs | Maul (Bear) on Judgment; payload unfetched | seven bindings on the referent's own bar (incl. Ulzaad's Decree, Shifting Sands, Turtle Shell, Arcane Barrier, Tip the Scales) | DIFFERS |
| R5 | key items | Korvan Spaulders, Beronath aura, Kaisan's Eldritch Eye, Conduit of Divine Whispers | Gutsmasher, Warborn Visor/Chestguard, Sandreaver Bracers, Kaisan's Burning Eye | DIFFERS. No item in common by name |
| R6 | pets | none | Guardian of Empyrion, Deathstalker | DIFFERS (the record is silent) |
| R7 | EoR radius | "small radius", no number | 3.0 m, DB-CITED | the record lacks the operand |
| R8 | numeric rows | 0 numerics, 0 composition factors | MEASURED save + DATAMINED rows | the record has none |

Consistency check: the compiler reads corpus.db, while the charter names the JSON export. The two agree on skills and geometry, but the JSON does not surface `original_element`/`court`, which are the fields the compiler actually consumes (finding EL-2).

## Layer C: the compiler against the record

| id | field | compiled | verdict |
|---|---|---|---|
| C1 | element | `dominant_element` = fire; both skills `canonical_element` = fire | **contradicts the record.** A null `element_primary` (element-neutral under the PHYSICAL RULE) falls through to the raw `original_element`. `t4_doors` is never read |
| C2 | magnitude | 0.0 on both skills; gap = `base_foi_damage (R-K5 GAP, T4 pending)`; `held=False`, `notes=[]` | **GAP carried, mislabelled, unannounced.** Every `gd` kit takes the level-None branch and gets a Flames-of-Ignaffar label, and the HELD note is not emitted |
| C3 | energy_cost | 10.0 on both skills | default, unflagged |
| C4 | resource_economy | `{}` | dropped. A level-less kit loses even the provenance tags a levelled kit keeps |
| C5 | movement / stats | 5.75; STR 10, VIT 54 | projection defaults, unflagged |
| C6 | geometry operand | `geometry_params: {}` | GAP, unflagged. The wide-zone flag fires only for cone/ground circle with a `wide` band |
| C7 | trigger grammar / doors / support lanes | no field | dropped (the KF-4 contract has no proc/aura/leech slot) |
| C8 | output contract | spatial-engine class_dict | **does not reach the arena** (= B-BIND) |

## Findings

### For the kit-compiler owner (`simulation/kit_compiler/`). Findings only; nothing edited
- **KC-1 (C1):** element resolution ignores the record's PHYSICAL RULE. A null `element_primary` should mean element-neutral, or the `ELEMENT_CONVERSION_PHYSICAL` door should resolve it to physical; it should never fall through to `original_element`. Today a physical-converted kit compiles as fire, which feeds the damage-family registry the wrong family. That is the exact path the charter's `KeyError` discipline guards on the rulebook side.
- **KC-2 (C2):** the gap label for level-less `gd` kits is the FoI label ("R-K5, T4 pending"), and the HELD note is keyed on `HELD_KITS` membership rather than on the branch actually taken. The fix is a per-kit gap reason, plus emitting the note whenever the GAP branch fires.
- **KC-3 (C3, C5, C6):** defaults (energy 10.0, movement 5.75, VIT 54, empty geometry) enter `class_dict` with no entry in `notes`/`gap_excluded`. They should be named on the artifact's face, as the wide-zone default already is.
- **KC-4 (C4):** `resource_economy` is `{}` whenever `level is None`. The mapping's qualitative tags should be carried regardless of level.
- **KC-5 (C8 / B-BIND):** the KF-4 contract targets the spatial engine, so there is no path from a compiled kit to the kc2 arena. For JOIN, the compiler needs a second emission target shaped by J2's operand interface. This is the J2/J4 design item, recorded here so it is not discovered at J4a.

### For elrond (the corpus kit record). Findings only; the record is not edited
- **EL-1 (R1, R4, R5, R6):** `gd-eor-warlord` describes a different build (forum SSF EoR + Judgment/Maul) from the REFERENT-v1 Warlord (the measured save: EoR + Vire's Might/War Cry/Blitz/Ascension + two summons + Gutsmasher). As a self-join referent it is a sibling build, not the same one. Either a record for the referent build is minted, or the self-join is declared a sibling-join on its face.
- **EL-2 (R2):** corpus.db `canon_corpus.original_element` = `court` = fire, while the mapping's own fidelity note rules physical. The JSON export does not surface these two fields, so a reader of the JSON cannot see the value the compiler consumes.
- **EL-3 (R7, R8):** the record carries no numeric rows, although DATAMINED values exist for at least the EoR radius (3.0 m), channel period (0.16 s @ 100 % AS) and mana cost (pack `pe1` / `pm4l`). These are the operands TA-X-20 needs. Proposed route: J-L4 (`magnitude_grade` / `mechanism_grade` columns).

## Halt check
No ORACLE behaviour change: `simulation/kc2/` is imported only to read two constants (`fixture.EOR_RADIUS_M`, `locomotion.D_ENGAGE_M`), nothing is executed, and no oracle file is edited. No lever moved. No write outside gamora's trees. Nothing halts to Matt from J1.
