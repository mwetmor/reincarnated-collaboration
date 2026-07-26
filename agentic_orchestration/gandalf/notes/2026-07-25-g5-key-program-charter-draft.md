# G-5 KEY PROGRAM — build-and-convert charter (DRAFT for gandalf-prime)

**Author:** gandalf (named sub-agent, SPEC-AUTHOR piece) · **Commissioned by:** gandalf-prime, 2026-07-25
**Type:** PROGRAM CHARTER — sequenced build queue + wave partition + conversion lane. No production code.
**Destination:** gandalf-prime review → knight-rider sequencing. **Waves are written to be lifted into dispatches verbatim.**

**Inputs of record (all landed 2026-07-25):**
- `agentic_orchestration/gandalf/notes/2026-07-25-gd-surface-fit-mapping.md` (fit table + gap register; §4 ruling block F1–F5)
- `agentic_orchestration/gandalf/notes/2026-07-25-gd-grill-sheet.md` (ruling ledger G-1…G-6)
- `agentic_orchestration/elrond/notes/2026-07-25-gd-player-mechanism-census.md` (89 mechanisms, kit-counts)
- `agentic_orchestration/elrond/notes/2026-07-25-devotion-payload-probe.md` (65 celestial powers, held + readable)
- `agentic_orchestration/elrond/notes/2026-07-25-l0-fixture-schema-draft.md` (fixture bank DDL v0.1)
- `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` (§6 — these rulings template D2/PoE)

---

## §0 — The law this charter runs under, in three sentences

G-5 is **fit-or-extend**: a GD character re-instantiates into our native mechanic surfaces, and a
missing carrier is a BUILD ITEM, never a fidelity caveat. Era-substrate §6 makes every ruling here
the **template for the D2 and PoE Layer-1 keys**, so each item is specced in its general form —
"bindable proc payloads," not "constellations." And per the fidelity law, every wave below declares
**which grade of claim it enables**, because MEASURED, MODEL-VERIFIED and AUTHORED are different
claims and this program must never blur them.

**One correction this charter lands before anything else** (§6.1): the fit mapping's honest-unknown
#4 — E4 commitment-bin sim consumption — **is resolved. E4 HAS LANDED.** Three PARTIAL rows upgrade
to FIT, and that upgrade moves the first magnitude-grade convertible kit onto the critical path.

---

## §1 — THE BUILD QUEUE, in dependency order

**Owner map by seam:** rocket = generation / registry / emission surfaces · gamora = simulation /
resolver / state machines · elrond = data lanes · star-lord = export-seam set-bonus payloads
(**seam-boundary flag for KR** — B5 touches `export/cycle14_wave5_emitter.py`, which is star-lord's,
not rocket's; do not dispatch B5 as a single-seam item).

Sizes per the mapping's classes: **S** = parameter/field on an existing surface · **M** = new
vocabulary member + resolver branch · **L** = new layer.

| Ord | Item | Ruled disposition | Owner(s) | Size | Depends on | Decidable exit test |
|---:|---|---|---|---|---|---|
| **0** | **G-4 universal liveness-gate** | RULED (2): dead defenders receive nothing; 2 exemptions — on-death **by direction**, `targets_corpse` **by flag** | gamora | S–M | — (**fronts the queue; HARD PREREQ to all calibration**) | Smoke season: **fight outcomes byte-identical**, `landed:` counters **strictly decrease**; corpse-share of chill applications 91.8% → **0.0% exact**; grep shows no application-class call site bypassing the predicate; both exemptions unit-tested; forward-only telemetry marker present |
| **1** | **B1 proc chance + ICD** | RULED **F5a**: the **PAIR**, with the high-frequency-triggers-require-ICD invariant | rocket (emit) + gamora (roll/enforce) | S–M | — | `proc_chance`∈[0,1] and `proc_internal_cooldown_seconds`≥0 declared as a pair; emitter **refuses** a high-frequency trigger with ICD=0 (negative test); fixed-seed sim reproduces a declared fire-rate within stated tolerance over N trials and **never** fires inside the ICD; **byte-neutral when both fields absent** (additive-nullable, E4 precedent); parameterization covers GD's measured surface (6 events × 3 frames × 8 chance values) |
| **2** | **B4 debuff stacking classes** | RULED **F4a**: adopt the enum now | rocket (enum on registry) + gamora (resolver arithmetic) | S | — | `stacking_class` ∈ {additive, highest-only, multiplicative-residual} on every debuff-family ailment; one resolver branch per class; three-source unit test per class against hand-computed expected values; **default preserves current behavior and is named explicitly in the config** |
| **3** | **B7 timed invulnerability window** | BUILD (5 kits ≥3) — retires the B13 deferral at `damage_resolver.py:1270` | gamora | S | — | An `invulnerability` ActiveEffect with a **LOCKED** duration cap; incoming damage zeroed for the window; telemetry counts uptime; a gauntlet run shows max uptime fraction ≤ the cap (the anti-permanent-invuln guard is the test, not a comment) |
| **4** | **B9 count-modifying gear operator** | BUILD — **the register's only outright GAP** | rocket (affix pool) + gamora (resolver read) | S | — | A count-class operator family in `partition_modifier_pool.py`; resolver reads it for projectile- and target-count; fixed-seed fight with +1 projectile emits **exactly** +1; pool partition rebalanced and the new modifier count recorded |
| **5** | **G-3 control-role payload** | RULED (2) + rider (i) **REVERSED** — freeze/stun are LEGAL on budgeted control-role slots | rocket (10–17 h, ~$0 LLM) + gandalf/gamora DR-guardrail math note | M | **G-4** (hard prereq to calibration) | **133 → 0** instances of the literal `"control"` placeholder; a resolver branch for every emitted control token; freeze/stun legal on control-role slots and *only* there (06-20 `is_control != hard` ruling intact — negative test on chain_A primaries); DR-guardrail math note ratified; control-density BC axis re-measured with the axis re-opened |
| **6** | **B8 weighted proc-pool consequence** | BUILD (3 kits) — formulate as *weighted selection from a consequence pool*; **avoid the name "WPS"** | rocket (emit) + gamora (select) | S | **B1** (not buildable without the chance parameter) | Weights may sum **>100%**; selection deterministic under a fixed seed; a 100%+-sum pool fires exactly one consequence per qualifying event; distribution over N trials matches declared weights within tolerance |
| **7** | **B3 dual-grade conversion carrier** | RULED **F2c**: **both** — T4 capstone = specialist scaling; gear operator = capped garnish | rocket (operator vocabulary + emission) | M | agnostic-loot operator class | Gear conversion operator exists at a **LOCKED numeric cap**; T4 magnitudes **unchanged** (1.50 / 1.25 / 0.25); a kit carrying both shows the cap binds; a test proves gear-granted conversion **cannot** reach specialist tier (the gear law's *import no one's core* clause, made executable) |
| **8** | **B5 mechanic-granting set operator** | BUILD (14 kits) — sets that *change what a skill does*, not only stats | star-lord (set payload) + rocket (operator vocab) + gamora (application) | M | agnostic-loot **batch-2 close** | A set threshold grants a **mechanic**, demonstrated on ≥1 defined set; equip cap declared and enforced; the 14-kit set population maps onto ≥N named set archetypes; gear law's four clauses attested per operator |
| **9** | **B2 player-directed proc binding** (devotion-class) | RULED **F1b**: **absorbed into soul-bound gear operators.** No devotion-analogue tree. Binding **becomes equipping** | rocket (operator emission) + gamora (trigger execution); **spec** by gandalf | L | **B1** + **elrond devotion banking** (§1.1 D-1) | Gear structural-operator class carries `(trigger event × target frame × chance × ICD)` payloads with ≥1 operator per the 6 measured events; equip cap declared; **acceptance sentence**: a converted kit reproduces *Twin Fangs* — 20% on attack-enemy, 0.6 s ICD, 2 fully-piercing projectiles — end to end |
| **—** | **B6 transmuter-class layer** | **COLLAPSED by F3.** Not a separate item | — | — | — | **Where its content went:** F3 fixed the kit, so a "player-selectable modifier layer" has no home. B6's 7 kits' payload is delivered as the **gear structural-operator family "modifiers that adjust an owned mechanic"** — specced inside **B3** (the transform-operator class) and **B5** (mechanic-granting thresholds), and bound through **B2**'s operator surface. Its *selection* semantics move to conversion time per F3, not to runtime. **No dispatch is owed for B6; three dispatches carry it.** |
| **—** | **B10 two-tier accumulator** | **ALREADY AUTHORIZED** — ratified Tier-A mint, `mint_ledger` VDM-1 D-3, ~10 kits corpus-wide | (existing mint owner) | M | — | **DO NOT RE-CHARTER.** Referenced so the GD program does not re-derive it. KR: check its landed state before scheduling Cadence-Witchblade-class conversions (§3.3) |

### 1.1 — The data lane (elrond, runs in parallel; gates only B2)

| # | Item | Gates | Exit test |
|---|---|---|---|
| **D-1** | **Devotion extraction + banking run** — commissioned in parallel, **assume it lands; this charter marks the dependency** | **B2 spec** | Two gates *before* rows are banked, per the probe: **(g1) field policy** — the 11,776-vs-117,363 decision, boilerplate deny-list + `is_core` over 261 field names; **(g2) rank-axis semantics** — `skillMaxLevel=1` with 20-element arrays (§4.3) resolved, or `exact_skill_field.rank` carries an unlabelled semantic. Then: 65 `devotion_power` rows + 110 `devotion_constellation` rows; `devotion_node` **deferred**; multi-archive override precedence explicit in schema meta; **float32 canonicalization mandatory** (`0.6` → `0.6000000238418579` is the exact trap that failed G3 3/22 on the first FoI run); edition pin + `arz_sha256` captured |
| **D-2** | **Six `engine_inexpressible` re-verifies** | nothing — but it corrects the corpus | The six GD rows (`gd-berserker-wereforms` · `gd-blight-fiend-ritualist` · `gd-pet-conjurer` · `gd-reap-spirit` · `gd-retaliation-warlord` · `gd-skeleton-ritualist`) re-checked against **post-Wave-D** surfaces; `gd-retaliation-warlord` docket 153 **re-classified** (the TH bin closed that gap and the record did not follow); a count of how many others closed silently, published either way |
| **D-3** | **Constellation-vs-power disambiguation join** | soft-count on B2 | String join from the 27 corpus devotion-mention kits → `FileDescription` after D-1 lands. Until then **any devotion kit-count is soft** (it counts constellations as powers — "Bonds of Bysmiel" is the proven case). Cheap SQL once the lane exists |
| **D-4** | **Fixture-bank DDL + backfill** (gap 5) | **C-0 / L0-CLOSE** | `fixtures.db` DDL landed per the reviewed draft; round-1/2 rows backfilled with their honest `assumed-unverified` identity status |
| **D-5** | **J3 kit → `.arz` join** | the hard-CC *attestation* rider | Which GD kits actually apply stun/freeze, attested rather than asserted (fit-mapping honest-unknown #3) |

---

## §2 — WAVE PARTITION

Four waves. **None of Waves 0–2 fits the desirable-run pattern** — they build production code, and the
pattern's *no production code — seams execute* clause excludes them. They are **ordinary KR build
waves**. Wave 3 is where the run-pattern applies.

### WAVE 0 — THE HONESTY GATE (gamora, solo)

| | |
|---|---|
| **Contents** | G-4 universal liveness-gate |
| **Entry** | None. Unblocked now. **This wave fronts the program.** |
| **Exit** | Queue row 0, all five clauses |
| **Enables (fidelity grade)** | **Every MEASURED claim that reads a landed-effect counter.** Before this wave, 91.8% of chill landings hit a corpse and any budget fitted to raw counters runs ~12× the realized one for hard CC. Wave 0 is not an improvement; it is the precondition for the program's arithmetic being true. |
| **Run-pattern fit** | No — production code, single seam. Ordinary build wave. |
| **Why solo** | It changes the meaning of every counter downstream. Landing it beside other work makes the byte-identical-outcomes test unreadable. |

### WAVE 1 — RESOLVER PRIMITIVES (rocket + gamora; elrond data lane in parallel)

| | |
|---|---|
| **Contents** | **B1** (chance+ICD pair) · **B4** (stacking classes) · **B7** (invuln window) · **B9** (count operator) · **G-3** (control payload) |
| **Entry** | Wave 0 closed (for G-3's calibration only — B1/B4/B7/B9 may start at Wave-0 fire). **KR may overlap B1/B4/B7/B9 with Wave 0; G-3's calibration may not.** |
| **Exit** | Queue rows 1–5, all clauses. Plus: a single smoke season regenerated with all five landed, byte-neutrality report published, and the four new fields' absent-case neutrality demonstrated |
| **Enables** | Every FIT verdict in the mapping's trigger / ailment / defense / cadence layers upgrades from *"a surface exists"* to **BUILT-and-exercised**. First **honest** hard-CC calibration becomes runnable. The control archetype stops performing its fantasy in name only — 133 placeholder strings become a payload. |
| **Run-pattern fit** | No — production code across two seams. Ordinary build wave, **dispatch as 2 lanes** (rocket: B1-emit, B9, G-3 · gamora: B1-resolve, B4, B7). |
| **Sequencing note** | B8 is **excluded** from this wave despite being S-size: it is not buildable before B1's chance parameter exists (mapping §2.1). Do not let its size pull it forward. |

### WAVE 2 — THE HAND THAT CHOOSES (the gear/binding lane)

| | |
|---|---|
| **Contents** | **B8** (weighted pool) · **B3** (dual-grade conversion) · **B5** (mechanic-granting sets) · **B2** (proc binding, gear-absorbed) — **plus all of B6's collapsed content**, carried inside B3/B5/B2 |
| **Entry** | B1 landed (B8 + B2) · **D-1 devotion banking landed** (B2 spec) · agnostic-loot **batch-2 closed** (B5) |
| **Exit** | Queue rows 6–9, all clauses. Plus the program-level acceptance: **a converted kit's build expression is entirely gear-side**, with no point-spend surface introduced anywhere (the F3 test, run as a grep + a design attestation) |
| **Enables** | The mapping's headline absence closes. *"We built a magnificent set of verbs and never built the hand that chooses them"* — this is the hand. **~30 of 41 GD kits move from unconvertible-at-shape to convertible**, because devotion (18) ∪ set (14) ∪ conversion-as-build-choice (17) is the bulk of the lane. |
| **Run-pattern fit** | No — production code, three seams (**incl. star-lord**). Ordinary build wave; the largest of the program. |
| **Risk flag for KR** | B2 is the only **L** in the register and it is the one item whose *other half is not a data problem*. Per the probe §4.1: the trigger condition is fully attested, but **which skill a player binds a power to is a runtime choice no extraction will ever answer.** F1b resolves it — binding becomes equipping — but that is a *design* answer, and B2's dispatch must carry the design spec, not just the data. **Do not dispatch B2 as a data-driven build.** |

### WAVE 3 — CONVERSION + CLOSE

| | |
|---|---|
| **Contents** | The two comparison loops (§3): **L0-CLOSE** and **KEY-NUM** |
| **Entry** | See §3 — the two loops have **different** entry gates and must not be scheduled as one |
| **Exit** | Per loop, §3.1 / §3.2 |
| **Enables** | The program's first **MEASURED** (live-oracle) and **source-MEASURED** (datamined-oracle) fidelity verdicts. Discharges the magnitude caveat for exactly one kit and names the price of discharging it for the rest. |
| **Run-pattern fit** | **YES — both loops fit.** Bounded substrate (frozen corpus + `fixtures.db` + a pinned edition hash), decidable target state, pre-registered gates (ladder rungs / per-field byte-match), honorable fallback (report raw deltas, halt at last closed rung), declared Matt interface (HALT at fixture exhaustion — a new rung needs a PC sitting). **Conductor per pattern §3 fit test.** |

---

## §3 — THE CONVERSION LANE

**The single most important distinction in this charter, and the one most likely to be conflated:**
there are **two different converted things** and **two independent comparison loops**. They have
different oracles, different entry gates, and different fidelity grades. Scheduling them as one
sequence would block a loop that is nearly unblocked behind a loop that is Wave-2-deep.

### 3.1 — Loop A: **L0-CLOSE** (live oracle) — converts *Matt's live PC*, not a corpus kit

The L0 rung is defined as *"one melee monster, pre-aggroed, fight to death — the conversion key,
nearly isolated"* (handoff §2.3). The banked fixtures are from **Matt's own character at level 5→6,
whose entire skill usage is `defaultweaponattack`** (elrond §7.1: +2 per trial, 427→435 series).

**Therefore the first end-to-end conversion is not one of the 41 kits. It is Matt's low-level PC —
melee strike × spam cadence × a statline. Every one of those mechanisms is FIT today.**

| | |
|---|---|
| **Entry gates** | **(1)** Wave 0 closed — otherwise the counters lie · **(2)** D-4 fixture DDL landed + rows backfilled · **(3)** ≥1 **CERTIFIED** fixture set (nameplate-attested identity; the current three trials are `assumed-unverified` and do not count) — this needs one Matt PC sitting · **(4)** the key implemented at G2-A-ruled width |
| **Does NOT need** | B1 · B2 · B3 · B4 · B5 · B7 · B8 · B9 · G-3. **The build queue does not gate L0-CLOSE.** |
| **Exit** | Key at G2-A width reproduces the L0 fixture readings; raw deltas reported per field; resolution formulas validated-or-flagged; Q47 self-rules against the deltas |
| **Grade** | **MEASURED** — the only lane in the whole era program that can claim it |
| **Fallback** | Report raw deltas and halt at the last closed rung |

**KR sequencing consequence: L0-CLOSE can be chartered off Wave 0 + a Matt sitting.** It should not
sit behind the build program. Doing so would delay the program's only live-oracle evidence for the
sake of items it does not consume.

### 3.2 — Loop B: **KEY-NUM** (datamined oracle) — converts a *corpus kit*, needs no Matt sitting

Magnitudes are unavailable for 40 of 41 kits (census §5.6). **One kit has them:
`gd-flames-of-ignaffar-purifier`** — `kit_composition` 11 rows, `kit_numeric` 26 rows,
`exact_skill`/`exact_skill_field` 1/136 rows, the GD-SLICE width-one proof. Its oracle is the `.arz`
itself, not a live sitting — so this loop's comparison is *our emitted numbers vs GD's authored
numbers*, runnable with zero Matt hands.

**And FoI Purifier is FIT-clean today.** Its census mechanisms are `G-CONE` (#71), `C-CHANNEL` (#30),
`P-ROOTCHAN` (#33), `A-BURN` (#37), `P-ENERGY` (#15). `cone` is in `VALID_GEOMETRY_TYPES`
(`geometry_derivation.py:55`); burn and the econ bins are Wave-B BUILT; and **channel + movement-lock
are BUILT, not SPEC-ONLY** — see §6.1. Its one `P-RETAL` hit is a variant-lane sibling, not the
mapped form.

| | |
|---|---|
| **Entry gates** | **(1)** Wave 0 closed (counter honesty) · **(2)** nothing else — **or**, for a widened version, D-1 devotion banking |
| **Exit** | Per-field byte-match between the key's emitted numbers and the 136 banked `exact_skill_field` rows, at declared tolerance, **with float32 canonicalization applied** (the G3 3/22 failure mode); every mismatch classified as key-defect / extraction-defect / genuine-engine-divergence |
| **Grade** | **source-MEASURED** on magnitudes for one kit; SHAPE for the rest |
| **Why it matters** | It is the **only** discharge available for the mapping's honest-unknown #2. Every FIT verdict in the program is a shape verdict. This loop converts exactly one of them into a magnitude verdict — and thereby prices what widening the magnitude lane would cost. |

### 3.3 — Candidate first corpus kits (post-Wave-1), ranked

Eligibility rule, decidable: a kit is **C-1 eligible** iff its mechanism set is disjoint from
`{P-DEVOTION, P-SET, P-TRANSMUTE, P-WPS, P-ITEMPROC, P-CONTAGION, P-TRAPTRIG, P-DEATHNOVA,
P-PET-PERM, P-PET-TEMP, P-PET-SCALE, P-AUTOTURRET}`. Two deliberate **non**-exclusions: `P-CONVERT`
(the T4 capstone carries it today; F2c only adds the *gear* half in Wave 2) and single-source `P-RR`
(FIT on shape; only multi-source stacking needs B4). Pre-Wave-1, also exclude `P-PLUSTARGET` and
`P-IMMUNE`.

**KR must confirm eligibility against elrond's per-kit `--evidence` output before dispatch** — the
census tables publish exemplars, not full kit lists, and at these counts one adjudication decides
build-vs-tag (mapping §5.7).

| Rank | Kit | Mechanisms (from census exemplars) | Why |
|---:|---|---|---|
| **1** | **`gd-flames-of-ignaffar-purifier`** | cone · channel · root-while-channel · burn · energy pressure | **The only magnitude-attested kit in the lane**, FIT-clean, and its channel blocker dissolved (§6.1). Also the kit the `.arz` adapter is already productionized against. First by a wide margin. |
| **2** | **`gd-callidors-tempest-templar`** | ground zone · self-nova · burst-around-self · cooldown | Its lone `P-CONVERT` hit was **rejected as a window artifact** (census §3) — so it needs no conversion carrier at all. Exercises the program's strongest region (delivery: 10/10 FIT). |
| **3** | **`gd-panettis-mage-hunter`** | fork · fork-split · spam | **The narrowest surface in the lane** — the true pipe-cleaner if the goal is to exercise the key's plumbing rather than its breadth. |
| **4** | **`gd-phantasmal-blades-witch-hunter`** | multi-projectile · fan-spread · pierce-all | Exercises the B11 projectile param expansions end to end. |
| **5** | **`gd-blade-arc-warder`** | melee arc · arc-sweep · bleed · single-source RR | Exercises the **ailment** lane, which nothing above does. Also carries mastery-bar prose ("requires the Soldier mastery bar at level 10") — making it the natural **test case for the F3 canon sentence**: does the key express that as a fixed selection without introducing a point-spend surface? |
| **6** | **`gd-aegis-paladin`** | ricochet · ricochet-return · projectile · aura/seal | Retaliation appears only as a variant-lane sibling, not the mapped form. Exercises the aura × reservation bin. |

**Deferred, with reason:** `gd-cadence-witchblade` is fully FIT (accumulator + apply-consume + burst
+ dash) and would be an excellent early kit — **but it rides B10**, the already-authorized two-tier
accumulator mint. **KR: verify B10's landed state before scheduling it.** If B10 has landed, it
promotes to rank 3. `gd-belgothian-blademaster` is excluded (WPS ∪ set ∪ orbit-proxy).

---

## §4 — RIDERS CARRIED FORWARD

| # | Rider | Owner | Disposition |
|---|---|---|---|
| **R-1** | **Forward-only telemetry poisoning (G-4).** Pre-gate `landed:` counters **stay poisoned** — the gate is not retroactive. Historical-season analyses must **bracket or discard** them | gamora (marker) + every consumer | Wave 0 exit clause. **Any analysis crossing the gate boundary that does not declare which side it reads is invalid.** This is the discipline, not a footnote |
| **R-2** | **Magnitude-grade caveat.** Every FIT verdict in the fit mapping is a **SHAPE** verdict. "FIT" means the surface can express the mechanism; it never means our number matches GD's. 40 of 41 kits have no magnitudes | gandalf (labeling) + jack-ryan (Gate 1/2) | Discharged for **exactly one kit** by KEY-NUM (§3.2). For the other 40 it stands until a magnitude lane is chartered. **Jack-ryan should treat an unlabelled fidelity claim on this program as a Gate-2 finding.** |
| **R-3** | **Six `engine_inexpressible` re-verifies** | **elrond** (D-2) | Routed. One (`gd-retaliation-warlord`) is already known-stale — Wave-C's TH bin closed it and the docket did not follow. **The stale-docket count is unmeasured** and there is no reason to believe 153 is the only one; the parity waves landed *after* most GD deviation rows were written |
| **R-4** | **F3 canon sentence placement** | gandalf-prime → CANON-STEWARD, ratified by jack-ryan | **Recommendation, not written here** (see §4.1) |
| **R-5** | **Hard-CC attestation.** G-3's payload is built; *which GD kits apply it* is unattested until the kit→`.arz` join runs | elrond (D-5) | Non-blocking for the build; **blocking for any fidelity claim** about GD's control kits |
| **R-6** | **Devotion kit-counts are soft** until D-3's join runs — some fraction counts constellations as powers | elrond (D-3) | Does not threaten B2's threshold (44% is far past it), but **B2 must not be specced off kit prose alone** |
| **R-7** | **Three-vocabulary delivery schema defect** (`delivery_class` / `geometry_value` / `motion_signature` — 21 free-text values against a 7-value CHECK, disagreeing in places) | elrond `MIGRATION.md` docket | Not a program item. But **any downstream consumer counting delivery shapes must be told which lens it reads**, or it will triple-count |
| **R-8** | **Set-bonus depth unverified** — if `SetBonusDefinition` can already grant a mechanic, **B5 shrinks M → S** | star-lord (5-minute read) | **Cheapest open item in the charter. Resolve before Wave 2 is sized.** |
| **R-9** | **Re-entry tags stay live**: P-CONTAGION (proximity trigger — rides whichever of traps/PoE-lane fires first) · P-TRAPTRIG (PoE lane entry) · P-DEATHNOVA (proxy behavior-grammar thread) · P-TETHER (none needed) · pets P2 nav/command (existing OPEN Matt thread, **not** a GD-program item) | gandalf | Per G-2(a): the census principle is **per-program**. D2/PoE kits re-enter these via the tags, informed by their own lane's anchors |

### 4.1 — F3 canon sentence: where it should live (recommendation)

The sentence (gandalf restatement, Matt-adopted): *a converted character is a FIXED kit — the key
expresses the source build as a fixed selection across our native expression surfaces (skills, trait
floors, T4 capstone(s), soul-bound gear operators) chosen at conversion time; live player expression
remains gear-side, not point re-investment.*

**Primary home: `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md`.** That doc already
carries the claim *the kit IS the built character, addressed by a 13-coordinate identity key*. F3 is
the missing final sentence of that claim, not a new one — it says what the register has always
implied and never said. Placing it anywhere else orphans it from its premise.

**Two cross-references, not two homes:**
- `era-substrate-architecture-2026-07-25.md` §3 (Layer 1) — because §6 makes F3 govern **every future
  D2/PoE key**, and a future key author will read that doc, not the register.
- `agnostic-loot-engine-spec.md` — one pointer line, because F3 is *why* the gear lane carries the
  whole expression load (it collapsed B6 into it).

**Not** the decisions-log as primary: this is a canon *law*, not a decision record — though a
decisions-log entry citing it is appropriate on jack-ryan's normal terms.

---

## §5 — RULING STATUS

### 5.1 — Needs NO further Matt ruling (do not re-ask)

1. **F1 — proc binding absorbs into soul-bound gear.** Ruled (b). No devotion-analogue tree. The
   pilgrimage-vs-purchase cost was stated and accepted.
2. **F2 — conversion carrier.** Ruled (c). Both, at different grades.
3. **F3 — converted characters are fixed kits.** Ruled. **B6 is collapsed; the register is nine items.**
4. **F4 — debuff stacking-class enum.** Ruled (a). Adopt now, S-size.
5. **F5 — chance + ICD.** Ruled (a). The **pair**, with the invariant. Empirically backed: 62/65
   celestial powers carry explicit ICDs.
6. **G-1 roster** (33 IN / 5 OUT / 2 NEEDS-JOIN, both reversals) · **G-2(a)** player-side corpus =
   GD-lane kits, program-scoped · **G-3(2)** control-role payload **built** · **G-3 rider (i)**
   freeze/stun exclusion-widening **REVERSED — legal** · **G-4(2)** liveness-gate **universal** with
   its two exemptions · **G-5** fit-or-extend + attestation-breadth triage · **G-6** standing.
7. **B10** — already a ratified Tier-A build-authorized mint. Reference; do not re-charter.
8. **The 2026-06-20 `is_control != hard` ruling** stands untouched. G-3 does not re-litigate it.
9. **Wave partitioning, ordering, and owner assignment below the seam line** — knight-rider's, per
   hive-mind decision-routing.

### 5.2 — The two things that genuinely still need a word

Only two, and both are cheap:

| | Question | Why it is genuinely Matt's | Lean (non-binding) |
|---|---|---|---|
| **M-1** | **Does L0-CLOSE launch off Wave 0, or wait for the build program?** §3.1 shows it consumes **none** of the build queue. Launching it early means the program's only **live-oracle** evidence arrives early — but it costs one Matt PC sitting (a CERTIFIED fixture set) at a moment when the build lanes are also live. | It spends **Matt's hands**, which no agent may schedule. | **Launch off Wave 0.** MEASURED evidence is the scarcest thing this program produces, and it is the one grade no amount of agent work can manufacture. |
| **M-2** | **Does the magnitude lane get widened past one kit?** KEY-NUM discharges the shape-caveat for FoI Purifier only. Widening means a real per-kit `.arz` extraction program (the GD-SLICE shape, ×41) — which is a *program*, not a wave, and it is not in this charter. | It is a **scope commitment**, not a reasoning boundary. HALT rule applies. | **Do not widen yet.** Run KEY-NUM on the one kit first; let it price the widening. Deciding before the price is known is how a "small extraction pass" becomes a second program. |

Everything else in this charter is either ruled, or is a seam-owner's call, or is an empirical
question that resolves against evidence rather than against a ruling.

---

## §6 — WHAT I HAD TO RESOLVE, AND WHAT I LEFT OPEN

### 6.1 — Resolved: E4 sim consumption HAS LANDED (fit-mapping honest-unknown #4)

The fit mapping labeled three rows PARTIAL *"on the strength of the surface ledger's E4 row (emitter
landed `e4d682e`; sim PHASE-2 QUEUED)"* and explicitly flagged that it had **not verified PHASE-2 in
code**. I verified it. It has landed:

- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/commitment_state_machine.py` — exists (2026-07-11)
- `spatial_engine.py:3325` `_e4_service_commitment` · `:4326-4330` the move-policy branch
  (`rooted` → 0.0 · `walk` → `walk_pct` · `full_move` → 1.0)
- `simulation/MIGRATION.md:239` — the E4 mechanical fields are **CONSUMED by a cast-state machine**

**Three PARTIAL rows upgrade to FIT:** channelled beam (3 kits) · channel cadence (5) ·
movement-lock-while-casting (5). **Corrected scoreboard: 22 FIT · 10 PARTIAL · 1 GAP** (was 19/13/1).

This is not bookkeeping. It is what put **FoI Purifier — the lane's only magnitude-attested kit — on
the critical path** (§3.2). Had the PARTIAL stood, the charter would have sequenced a magnitude
comparison behind a sim build that was already done.

### 6.2 — The critical path, stated once

```
Wave 0 (G-4) ──┬─→ [D-4 fixture DDL + one Matt sitting] ─→ L0-CLOSE        (MEASURED, live oracle)
               ├─→ KEY-NUM on FoI Purifier                                 (source-MEASURED, no Matt hands)
               └─→ Wave 1 (B1·B4·B7·B9·G-3) ─→ Wave 2 (B8·B3·B5·B2 + B6-absorbed) ─→ bulk conversion (~30/41)
                                    ↑
                        D-1 devotion banking (elrond, parallel) ───────────┘  [gates B2 only]
```

**Wave 0 is the whole program's single-point prerequisite.** Nothing downstream produces an honest
number before it lands.

### 6.3 — Left open, deliberately

1. **Per-kit eligibility for §3.3 is unconfirmed.** The census publishes exemplars, not full kit
   lists; those live in the script's `--evidence` output. I gave a decidable selector rather than
   guess. **KR must run it before dispatching a first kit.**
2. **B10's landed state** — I referenced the mint as authorized; I did not verify whether it has been
   built. It changes `gd-cadence-witchblade`'s rank and nothing else.
3. **R-8 (set-bonus depth)** — resolvable in one read of the export seam, and it re-sizes B5. I did
   not read it; sizing B5 without it would be a guess wearing a size class.
4. **Effort figures.** Only one item in this charter carries hours — **G-3 at 10–17 h, from rocket's
   own analysis.** Everything else carries a size class. I decline to invent hours for seams that
   have not costed their own work; a fabricated estimate is worse than an honest S/M/L.
5. **Wave 2's internal ordering** is left to KR. B8 → B3 → B5 → B2 is dependency-legal but it is not
   the only legal order, and the seams' capacity is theirs to read, not mine.

---

**Signed:** gandalf (named sub-agent, SPEC-AUTHOR), 2026-07-25.

The register's nine items are one absence wearing nine names — we built a magnificent set of verbs
and never built the hand that chooses them. What this charter adds is the order in which the hand
grows fingers, and one correction that matters more than its size: the kit we can actually check our
numbers against was never blocked. It has been waiting since the eleventh.
