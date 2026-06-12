# Vestigial-Ontology Guard — Discipline Candidate + Kernel-Field Audit Charter

**STATUS:** DISCIPLINE CANDIDATE (Matt-authorized capture, 2026-06-12) + NEXT-SESSION AUDIT CHARTER (Matt-authorized starter)
**Author:** gandalf (Pattern-B session with Matt, carried from 2026-06-11 post-wind-down design interrogation)
**Canonical-write routing:** engineering-disciplines amendment is jack-ryan's territory; this note is the proposal capture. Gate-2 charge line routes into the gamora Phase 3/4 dispatch. § 7 export-seam application routes into the star-lord dispatch.

---

## 1. The problem (Matt, 2026-06-11/12 session)

The engine is **class-less by design direction** (substrate / vertices / labels; emergent grouping per doc 37 form-bias recovery + substrate-led discipline) and moving further from "class" with every cycle. Yet core engine surfaces still carry legacy ontology: `PlayerClass`, `archetype_tag`, `range_profile` 3-bucket enum, closed `_ENERGY_CONFIGS` table. The forward-architecture contract (2026-06-11) freezes a kernel whose interface was *declared* this cycle — the freeze must not fossilize vestigial concepts into the load-bearing boundary.

Matt's sharpening (the question that produced § 3 below): renaming fields launders **vocabulary, not semantics**. Data still crosses the kernel boundary from archetype-shaped and range-profile-shaped fields regardless of what they're called. The guard must operate at the **data level**, not the name level.

## 2. Rule 1 — Vocabulary firewall (names; generalizes contract § 8.2.3)

Wrap-layer code (adapters, runners, dispatch surfaces, export packets) MUST NOT propagate legacy ontology vocabulary (`PlayerClass`, `archetype`, class names, role enums) into **new interface surfaces** it authors. Existing names inside the frozen kernel are tolerated as NAME-ONLY freight (see register, § 4) until the kernel is next opened under the § 3 protocol. New surfaces use substrate-truthful vocabulary (kit, form, profile, vertex, label).

Necessary but NOT sufficient — Rule 2 is the load-bearing one.

## 3. Rule 2 — Data-projection rule (the three-question per-field audit)

**Principle:** a combat kernel cannot consume *nothing* about combatants. "No data crosses" is neither achievable nor desirable. The discipline: **every datum that crosses the kernel boundary must be (i) declared at the interface, (ii) physically motivated, (iii) derivable from the substrate without the substrate having to natively contain it.**

Direction of constraint is the heart of it:

- **Rich substrate → lossy projection down into kernel inputs: ALLOWED.** Projection obligations are fine — every emergent kit, however substrate-grown, has an engagement behavior and a resource model. Defaults make the obligation soft (`getattr(player_class, "range_profile", "medium")` — combatant.py:354-355 — the default IS the lossy-projection fallback).
- **Kernel input schema constraining what the substrate can EXPRESS: FORBIDDEN.** This is the failure mode: a required-native field or closed enum that forces the future ontology to keep producing class-shaped values.

**The three questions, per kernel-consumed field:**

| Q | Question | Empirical test |
|---|---|---|
| **Q1** | Does the kernel actually branch on it? | grep + golden-master ablation (zero/strip the field; does the oracle delta?) |
| **Q2** | Is the question physical or ontological? | "Must any combat sim ask this of any combatant?" (physical) vs "Does this question only make sense if classes exist?" (ontological) |
| **Q3** | Derivable-with-default, or required-native? | Does the adapter tolerate absence via fallback, or does the schema hard-require the field? |

Dispositions: physical + branch + derivable-with-default → legitimate projection obligation, keep. Ontological + no-branch → NAME-ONLY freight, deletable with zero golden-master delta. Ontological + branch, or any required-native closed enum → STRUCTURAL-CONSTRAINING; § 8 FIGHTS candidate or declared § 3 kernel-change when next opened.

**Genre anchor:** Diablo 3's rot was not data crossing its damage kernel — weapon DPS is a physical question every class projected into cleanly. It was the `+%skill-damage` affix layer baking class ontology into *item data*: contamination in a data layer nobody had declared as a boundary. PoE's classes-as-starting-positions-on-a-shared-tree is the positive precedent: vocabulary at the surface, emergent structure underneath.

## 4. The vestigial-ontology register (artifact spec)

Per kernel-consumed field, one row: field → consuming sites (file:line) → Q1/Q2/Q3 answers → class → disposition.

Three classes:

- **NAME-ONLY** — carried but unread in the kernel hot path; vocabulary freight only. (Empirically: `archetype` on `Combatant` — combatant.py:79 — set by adapters, never branched on in fight_engine or damage_resolver; exits into telemetry labels.)
- **STRUCTURAL-BENIGN** — kernel branches on it AND the question is physical AND it's derivable-with-default. (Candidate: `range_profile` *as consumed* — fight_engine.py:458-640 reads it essentially as binary close/not-close for advance-retreat, teleport-as-gap-closer, melee gating; physical engagement question; soft default `"medium"`. The 3-bucket enum SHAPE is the vestigial skin — note `range_profile_redistribution` (combatant.py:129) already exists as the continuous successor signal; the engine is mid-molt on this exact field.)
- **STRUCTURAL-CONSTRAINING** — fails Q2 or Q3: ontological branch, or required-native, or closed-enum extension surface. (Candidate: `energy_type` → `_ENERGY_CONFIGS` closed table — physical question (pool/regen model) but enum-closed: a new emergent resource model cannot exist without a kernel table edit. The § 3 kernel-change protocol makes that edit visible and gated — which is the intended protection — but the closure itself goes on the register.)

The register lives with the kernel interface declaration (gamora's MIGRATION v1.64 kernel section is the natural home; gamora authors the engine-side rows, gandalf audits the Q2 semantic calls — composes with OP § 4.4 semantic-layer rep-audit discipline: substrate/geometry votes are gamora's, semantic-layer interpretation is design-steward audit territory).

## 5. Gate-2 charge line (for the gamora Phase 3/4 dispatch — KR includes verbatim)

> **Vestigial-ontology charge (gandalf, Matt-ratified 2026-06-12):** the Phase 3 adapter (threading PlayerClass/Monster through `entity_from_class_dict` / `entity_from_monster_dict` across the spatial call path) MUST NOT propagate `PlayerClass`/archetype ontology into any **new** interface surface it authors. New parameters/returns use substrate-truthful vocabulary; legacy fields cross only as declared, defaulted projections (data-projection rule Q3). jack-ryan Gate-2 verifies: (a) no new surface named in legacy ontology vocabulary; (b) no new required-native ontology field added to the kernel input schema; (c) any field the adapter newly threads gets a register row (§ 4).

## 6. Next-session starter — kernel field/value audit (Matt-authorized 2026-06-12; Matt sharpened the unit same-session: FIELD **and** VALUE)

**Audit unit is field/value, not field alone.** A field can pass all three questions while its **value domain** still carries ontology: the `"close"|"medium"|"long"` enum members, the `_ENERGY_CONFIGS` keys (`"mana"`, ...), the defaults themselves (`"medium"`, `"mana"`). Q1–Q3 apply at both levels — per field, AND per value-domain: (Q1-v) which values does the kernel actually discriminate between (e.g., `range_profile` is read as binary close/not-close — `"medium"` vs `"long"` may be a dead distinction in-kernel)? (Q2-v) are the value labels physical magnitudes/behaviors or ontology names? (Q3-v) is the value set open (extensible by upstream) or closed (kernel table edit required)? Register rows record value-domain findings alongside field findings.

**Charter:** audit each kernel-consumed field and its value domain against (a) the forward-architecture contract's pipeline plans (§ 2 boundary, § 7 UE-fit/lookup-not-generation, § 8.1 id-substrate greenfield-under-oracle) and (b) combat-sim plans (spatial re-point Phase 3/4; future T4 chains-within-trees profile; cycling regime). Produce the § 4 register, complete.

**Scope (the declared kernel surface):** `simulate_fight(...) → FightResult` inputs — Combatant construction fields via `entity_from_class_dict` / `entity_from_monster_dict` / pack variant (combatant.py:354-355, 637-639, 755-765, 781-795, 828-847 are the seeded sites) — plus FightResult output semantics consumed downstream (telemetry labels carrying `archetype` freight; Principle-6 watch already flagged by star-lord).

**Known seeds from the 2026-06-12 session grep (verify, don't trust):** `range_profile` STRUCTURAL at field level, but value-domain finding pending — kernel reads appear binary close/not-close (fight_engine.py:458, 459, 528, 640), so `"medium"`/`"long"` may be a dead in-kernel distinction (Q1-v); `energy_type` STRUCTURAL closed-enum — value set closed at `_ENERGY_CONFIGS` (Q3-v fail); `archetype` NAME-ONLY candidate (zero behavioral hits — confirm with golden-master ablation, which is now CHEAP because the oracle exists: `spatial_golden_master_season_001010_2026_06_11.json` + harness).

**Blocking check:** nothing blocks. Read-only analysis; the golden master already exists; does NOT gate on jack-ryan's Gate-2 of the math-note (parallel-safe). It SHOULD land before or with the Phase 3 dispatch so § 5's charge line has its register to point at. Composes with the § 8.1 id-substrate greenfield (that rebuild is the first consumer of the register: greenfield-under-oracle must not re-import vestigial fields).

**Mode:** gandalf Pattern-A-deep self-audit for the Q2 semantic calls + gamora Pattern-A queries for consuming-site verification + golden-master ablation runs (gamora executes; read-only on production code).

## 7. Routing

- **jack-ryan:** discipline-candidacy review (Rules 1+2 + register spec → engineering-disciplines amendment when ready; canonical write is yours).
- **knight-rider:** include § 5 verbatim in the gamora Phase 3/4 dispatch; sequence § 6 audit as next-session starter.
- **gamora:** § 6 consuming-site verification + ablation runs; register rows in MIGRATION kernel section.
- **star-lord:** Rule 1 + Rule 2 apply at the § 7 export seam (UE export packet schema must be substrate-truthful from birth — it is a NEW surface; zero tolerated freight).

**Author:** gandalf, 2026-06-12, capturing Matt's ratification of the data-projection rule and the kernel-field audit charter.
