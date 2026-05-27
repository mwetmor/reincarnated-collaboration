# Scaffold-Drift Recognition + Three-Part Corrective Package

> **STATUS:** CURRENT — gandalf-authored; Matt 2026-05-27 ratified the three-fix substrate recommendation inline, ratified the recognition that 16-character cohort + 12-skill 3-chain grid are real drift cases (not false patterns), and authorized this consolidated package. Routes to knight-rider for dispatch packaging + jack-ryan for discipline ratification.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "Agree with #5 recommendation of Three discrete fixes (layered). Please author the side-car." + "author all three as one consolidated document" (re-package directive after recognition of skill-tree drift and 16-char drift)
**Supersedes:** `agentic_orchestration/gandalf/notes/2026-05-27-substrate-weapon-family-balance-sidecar-request.md` (folded into § 2 of this doc)
**Companion docs:**
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains AMENDED 2026-05-27)
- `canonical/41-progression-framework-2026-05-27.md` § 2-3 (L50 hybrid progression)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (per-attribute weapon profile)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md`

---

## 0. TL;DR

Three concrete drift cases surfaced on 2026-05-27, all sharing one failure mode: **scaffold values from a fast-shipped predecessor calcifying into "this is what the system does."**

| # | Drift case | Scaffold source | Calcified into | Corrective |
|---|---|---|---|---|
| 1 | Substrate weapon family imbalance + ammo contamination | SC-6b enrichment landed unfiltered; gear gen samples uniform | Production weapon binding for Wave 5 cohort | **Part 1** — three-fix substrate sidecar (rocket + elrond) |
| 2 | 16-character cohort | Cycle 13 gauntlet test cohort size | De facto season cardinality | **Part 2** — explicit season-cardinality canonical decision (bundled into Wave 1.5) |
| 3 | 12-skill 3-chain 4-tier grid emission | Wave 0.5 Track D minimum-viable per-skill emission | De facto skill-tree architecture | **Part 2** — Wave 1.5 skill-tree-architecture scope (rocket; ~1 week) |

Plus a meta-corrective:

| # | Meta-corrective | Owner |
|---|---|---|
| 4 | **Discipline #40 candidate** — scaffold values that ship to production-output paths require canonical decision before next wave fires | **Part 3** — routes to jack-ryan for engineering-disciplines.md canonical-write |

**Sequencing:**
- Part 1 Fix A (hygiene filter): folds into Wave 1 closure window
- Part 1 Fix B + Fix C: pre-Wave-2; math-note required
- Part 2 (Wave 1.5 + season cardinality): inserts BEFORE Wave 2 (Layers 5+8+9 depend on it; Wave 5 production season depends on it)
- Part 3 (Discipline #40): jack-ryan canonical-write parallel; not gating

---

## 1. Recognition — the scaffold-drift meta-pattern

### 1.1 The pattern

A wave ships a **scaffold value** to unblock immediate downstream consumption. The scaffold is:
- Pragmatic — solves the immediate need with minimum machinery
- Functional — works correctly for the test case in front of it
- Documented as scaffold — usually noted in math-notes or commit messages as "v1; refines later"

Then the wave closes Gate-2 PASS. The scaffold survives. The next wave consumes it as input. By the time someone notices, the scaffold has become load-bearing infrastructure for three downstream systems, and the canonical design intent is silently contradicted.

**This is Discipline #13 implicit-pillar drift in its purest mechanical form.** Discipline #13 was authored thinking about CONCEPTUAL drift — design pillars that nobody re-anchored. The mechanical analog — SCAFFOLD VALUES that nobody re-decided — is the same failure mode.

### 1.2 Three concrete instances surfaced today

**Instance 1 — Substrate weapon family imbalance** (Matt's question that surfaced everything):
- SC-6b enrichment landed `weapon_type_family` column populated correctly
- Gear gen `substrate_weapon_binding.py` samples `rng.choice` uniform across `primary_stat`-filtered rows
- No family-balancing logic; no `weapon_kind` filter
- Result: STR characters 90% heavy-melee; arrows/bolts/shields/banners eligible as main weapons
- Empirically: STR is functionally a heavy-melee gallery; ammo contamination latent in Wave 5 cohort

**Instance 2 — 16-character cohort**:
- `bc_target_subspace_generator.py` L173: `def generate(self, n_kits: int = 22)` — DEFAULT IS 22, NOT 16
- Multi-fire extension supports up to 50 (L213-225)
- Cycle 13 output directory `cycle-13-mechanical-season-001/characters/` has 16 character JSONs
- The 16 came from gauntlet sim PASS criteria (`simulation/MIGRATION.md` L566: "all 16 kits"; `cycle-13-option-a-remediation-root-cause-2026-05-27.md` L124: "16 of 18 kits have generation_shipped=True")
- NO canonical doc locks 16 as season cardinality — not doc 29, not doc 41, not doc 46, not doc 47
- Matt's stated intent (verbatim): "maximal quantity of characters who are unique/playable/balanced/thematically coherent to faction and season"
- Drift: 16 is creeping in as the de facto season size by inertia

**Instance 3 — 12-skill 3-chain 4-tier grid**:
- `per_skill_emitter.py` L151-152: chains hardcoded to `["chain_A", "chain_B", "chain_C"]`; tiers hardcoded `[1,2,3,4]`
- L130-134: chain_A = primary T1-T4; chain_B = secondary T1-T4; chain_C = control T1+T2 / support T3+T4
- Emits flat 3×4 = 12 grid; T4 on every chain; no supporting chain; no branching
- Canonical state (doc 40 § 8.3 AS AMENDED 2026-05-27 + D69 + D83 + D66 + roadmap):
  - Variable 3-or-4 chains per class
  - T4 count = chain count − 1 (3-chain → 2 T4; 4-chain → 3 T4)
  - Supporting chain (T3-cap, class-intrinsic, every class has one)
  - Branching gated by chain depth ≥4
  - ONE T4 unlocked at a time (active identity discipline)
- Drift: scaffold contradicts six locked architectural commitments

### 1.3 Why this matters for Cycle 14 deliverable

Wave 5 produces the "initial mechanical+cohesion season" — the **first production output that Matt's stated quality bar applies to.** Per framing brief Q10: "the goal is not to ship something but to ship a game (playable characters that run the gauntlet in band)."

If three scaffold values are load-bearing at Wave 5 firing time, the production season inherits:
- STR-cohort heavy-melee monoculture (Instance 1)
- 16-character output size regardless of canonical intent (Instance 2)
- 12-skill 3-chain grids on every character regardless of class architecture (Instance 3)

This produces a "playable but not as designed" season output. The corrective package below addresses all three before Wave 5 fires.

---

## 2. Corrective Part 1 — Substrate Weapon Family Balance Sidecar

### 2.1 Diagnosis (empirical state)

**Substrate composition (2,293 v1_scope rows in `weapon_sim_props`):**

By `weapon_type_family`:

| Family | Count | % | Routes from |
|---|---|---|---|
| martial-heavy | 801 | 34.9% | STR |
| ranged | 796 | 34.7% | DEX (706) + STR (90) |
| martial-light | 369 | 16.1% | DEX |
| caster-faith | 167 | 7.3% | WIS |
| caster-arcane | 160 | 7.0% | INT |

By `primary_stat`:

| Stat | Count | % |
|---|---|---|
| DEX | 1,075 | 46.9% |
| STR | 891 | 38.8% |
| WIS | 167 | 7.3% |
| INT | 160 | 7.0% |

By `weapon_kind`:

| Kind | Count | Concern |
|---|---|---|
| category | 1,139 | Clean |
| named_template | 927 | Clean |
| **ammo_or_consumable** | **148** | **Arrows/bolts eligible as main weapon** |
| unique | 42 | OK |
| shield/talisman/banner/horn | 36 | Off-hand items leaking |

**Selection algorithm (`substrate_weapon_binding.py:_query_substrate_weapon` L238-269):**

```sql
SELECT ... FROM weapon_knowledge_entries wke
JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id
WHERE wke.v1_scope = 1 AND wsp.primary_stat = ?  -- bc_attribute only

rng = random.Random(seed)
selected = rng.choice(rows)  -- UNIFORM
```

**No family-balancing. No weapon_kind filter. No weighting.**

**Within-attribute family routing produced:**

| BC attribute | Family options | Lock effect |
|---|---|---|
| STR | martial-heavy 90% / ranged 10% | **Heavy-melee dominant — variety floor ~10%** |
| DEX | ranged 66% / martial-light 34% | Moderately balanced |
| INT | caster-arcane 100% | Single-family lock (by design — caster routing) |
| WIS | caster-faith 100% | Single-family lock (by design — caster routing) |

**Variety problem concentrated in STR** — Diablo II "every barbarian carries a two-hander" pattern. The 90:10 split is too steep without intervention.

### 2.2 Fix A — Hygiene filter (no design call; pure correctness)

**Add `wke.weapon_kind IN ('category', 'named_template', 'unique')` to the substrate query.**

- Eliminates 185 contamination rows (148 ammo + 36 shield/talisman/banner/horn + 1 unknown)
- Reduces draw pool from 2,293 → 2,108 (still abundant per attribute)
- Trivial code change; module-load assertion verifies count
- **Owner:** rocket
- **Sequencing:** fold into Wave 1 closure window OR fire as small follow-on dispatch
- **Risk:** none — pure correctness

### 2.3 Fix B — Within-STR family rebalancing (design call ratified)

**Re-weight STR draws to 70% martial-heavy / 30% ranged (from current 90/10).**

Adds a `WITHIN_ATTRIBUTE_FAMILY_WEIGHT` table to `substrate_weapon_binding.py`:

```python
WITHIN_ATTRIBUTE_FAMILY_WEIGHT: dict[str, dict[str, float]] = {
    "STR": {"martial-heavy": 0.70, "ranged": 0.30},
    "DEX": {"ranged": 0.60, "martial-light": 0.40},   # mild rebalance from 66/34
    "INT": {"caster-arcane": 1.00},                    # single-family by design
    "WIS": {"caster-faith": 1.00},                     # single-family by design
}
```

Query stays the same; selection becomes two-step:
1. Sample `weapon_type_family` per attribute's weight table
2. `rng.choice` uniform within the sampled family's rows

**Effect on 4-STR cohort:** expected ~2.8 heavy-melee + ~1.2 ranged STR characters (from current ~3.6 + ~0.4). Produces "STR archer" / "STR crossbowman" archetypes at meaningful frequency.

- **Owner:** rocket
- **Sequencing:** Wave 2 candidate (alongside Layer 8 set keying — both touch substrate sampling logic)
- **Math note required:** Discipline #1 — `within-attribute-family-weight-math.md` documenting the 70/30 / 60/40 derivation + variance implications
- **Decision before:** Wave 5 gauntlet

### 2.4 Fix C — Within-caster weapon_kind variety audit (substrate-first)

**Audit caster-arcane (160) and caster-faith (167) for `weapon_kind` distribution.**

The within-caster identity beat comes from kind variety (orb vs tome vs wand vs staff vs scepter vs focus), not family. Need empirical answer:

- Are casters 90% staves? → need within-family kind rebalancing
- Are casters already diverse? → no action needed
- Are some kinds (banner, horn) miscategorized? → curation pass

**Empirical audit query (elrond):**

```sql
SELECT wsp.weapon_type_family, wke.weapon_kind, COUNT(*) AS n
FROM weapon_sim_props wsp JOIN weapon_knowledge_entries wke ON wke.id = wsp.weapon_id
WHERE wke.v1_scope = 1 AND wsp.weapon_type_family IN ('caster-arcane', 'caster-faith')
GROUP BY wsp.weapon_type_family, wke.weapon_kind ORDER BY n DESC;
```

Plus drill into sub-categories if `category` dominates (likely): `canonical_name` keyword analysis for "staff" / "wand" / "orb" / "tome" / "scepter" / "focus".

- **Owner:** elrond (audit) → gandalf (design call if remediation needed)
- **Sequencing:** can fire anytime; not gating
- **Output:** brief findings note at `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md`

### 2.5 Sidecar dispatch package proposal

KR drafts as ONE bundled sidecar dispatch:

Title: `2026-05-27-substrate-weapon-family-balance-sidecar.md`
Items: A (rocket) + B (rocket math-note + impl) + C (elrond audit)
Sequence: A fires Wave 1 window; B math-note fires now, impl Wave 2; C audit fires now

---

## 3. Corrective Part 2 — Wave 1.5 Skill-Tree Architecture + Season Cardinality Canonical Decision

### 3.1 The drift (rocket Wave 0.5 emission vs canonical state)

**What `per_skill_emitter.py` actually emits:**

```python
# L151-152
chains: list[str] = field(default_factory=lambda: ["chain_A", "chain_B", "chain_C"])
tiers_per_chain: list[int] = field(default_factory=lambda: [1, 2, 3, 4])

# L130-134
_CHAIN_ROLE: dict[str, dict[int, str]] = {
    "chain_A": {1: "primary_attack", 2: "primary_attack", 3: "primary_attack", 4: "primary_attack"},
    "chain_B": {1: "secondary_attack", 2: "secondary_attack", 3: "secondary_attack", 4: "secondary_attack"},
    "chain_C": {1: "control", 2: "control", 3: "support", 4: "support"},
}
```

→ Flat 3×4 = 12 grid. T4 on every chain. No supporting chain. No branching. No depth variability.

**What doc 40 § 8.3 (AS AMENDED 2026-05-27 closeout § 1.4) + D69 + D83 + D66 says:**

| Class chain count | T4 count | Architecture |
|---|---|---|
| **3 chains** | **2 T4** | 2 T4 chains × ~5 nodes (branching-eligible) + 1 supporting chain × ~3 nodes |
| **4 chains** | **3 T4** | 3 T4 chains × ~3-4 nodes (linear) + 1 supporting chain × ~3 nodes |

Plus:
- **D69:** Branching gated by chain depth ≥4 nodes — wide-vs-tall lever
- **D83:** T4 count per class = chain count − 1
- **D66 SHARPENED:** ONE T4 unlocked at a time (active identity discipline)
- **Supporting chain (Option C):** every class has one; T3-cap; absorbs class-intrinsic passives

**Drift matrix:**

| Canonical | Rocket Wave 0.5 | Drift |
|---|---|---|
| Variable 3-or-4 chains | Hardcoded 3 chains | YES |
| T4 count = chain count − 1 (3 chains → 2 T4) | T4 on all 3 chains | YES |
| Supporting chain (T3-cap, class-intrinsic) | No supporting chain | YES |
| Branching gated by depth ≥4 | No branching | YES |
| ONE T4 unlocked at a time | All 3 T4s emitted as equivalent skills | Architectural intent obscured |
| Off-shoot branches for wide trees | Not implemented | YES |

### 3.2 Season cardinality drift (companion to skill-tree drift)

**Canonical state:**
- `bc_target_subspace_generator.py` L173: `n_kits: int = 22` (one per BC-cell base enumeration)
- L213-225: multi-fire extension supports up to 50 base kits
- `cycle-13-wave-2-t4-algorithm-math-2026-05-27.md` L354: "Per cohort per BC-target cell: generate N=10-20 kits"

**Cycle 13 actual output:** 16 characters in `cycle-13-mechanical-season-001/characters/`

**No canonical doc locks 16.** The 16 came from gauntlet PASS criteria scope (16 of 18 cells passed synthetic_mode bypass). With synthetic_mode RETIRED (Discipline #39), the gauntlet PASS count is empirical, not pre-determined.

**Matt's stated intent (verbatim):** "maximal quantity of characters who are unique/playable/balanced/thematically coherent to faction and season."

**Decision required:** explicit season cardinality target — three options:

| Option | Cardinality | Trade-off |
|---|---|---|
| **Option 1** — Match BC-cell base enumeration | 22 base, ~16-22 surviving | One-per-cell coverage; minimal but clean |
| **Option 2** — Multi-fire extension | 30-50 base, ~25-40 surviving | Within-cell variety; preferred for "maximal quantity" |
| **Option 3** — Open-ended (faction-driven) | N per faction × M factions | Production scale; depends on faction count |

**gandalf recommendation: Option 2 for Cycle 14 Wave 5 production season; Option 3 deferred until faction-architecture decisions land.** Option 2 surfaces within-cell variety and gives the gauntlet a meaningful filter to do.

### 3.3 Wave 1.5 — Skill-Tree Architecture (scope)

**Position:** inserts BEFORE Wave 2 (Layers 5+8+9). Rationale:
- Wave 2 set-keying and class-agnostic drops depend on knowing per-class chain structure (which chain is the supporting chain? which T4s are unlocked?)
- Wave 5 gauntlet needs real chain architecture to validate cohort KPM bands
- Without Wave 1.5, Wave 5's "production season" produces 12-skill 3-chain monocultures regardless of canonical state

**Owner:** rocket (primary implementer); gandalf design-call partner on class-roster decisions; jack-ryan Gate-1 + Gate-2

**Estimated effort:** ~1 week anchor (per framing brief Q10 quality > timeline)

**Scope items:**

#### Item 1 — Per-class chain count (3 or 4) sampled from class metadata

- Replace `SkillEmissionConfig.chains` hardcoded default with **per-class chain_count derived from class metadata**
- Class metadata source: kit candidate's `class_archetype` field or a class-roster registry (TBD per Wave 1.5 design call)
- Acceptance: 16-character test season produces a mix of 3-chain and 4-chain classes (not all 3-chain)

#### Item 2 — T4-count = chain_count − 1 rule

- Implement D83 — a 3-chain class has 2 T4-capable chains + 1 supporting (T3-cap) chain; a 4-chain class has 3 T4-capable chains + 1 supporting chain
- The supporting chain is **identified per class** (not random) — substrate-led: which chain absorbs the class-intrinsic passives?
- Acceptance: no 3-chain class emits 3 T4s; no 4-chain class emits 4 T4s

#### Item 3 — Supporting chain (T3-cap, class-intrinsic)

- Supporting chain caps at T3 (no T4 capstone)
- Carries class-intrinsic passives (per doc 40 § 6.6.1 Option C)
- Visually + mechanically distinct from T4 chains (different node art? different unlock semantics? — Wave 1.5 design call)
- Acceptance: every class has exactly one supporting chain; supporting chain's max tier = 3

#### Item 4 — Depth-≥4 branching (wide-vs-tall lever per D69)

- Chains with depth ≥4 nodes can have **branch points** — T2 or T3 splits into two parallel sub-paths
- Branch points consume the same T-tier but offer alternative skill effects
- Wide vs tall: a 3-chain class with depth-6 chains has more wide-vs-tall lever than a 4-chain class with depth-3 chains
- Acceptance: at least one test class demonstrates a branched chain; branch consumption rules clear in math-note

#### Item 5 — ONE T4 unlocked at a time (D66 active identity discipline)

- Of the 2-3 T4-capable chains per class, ONLY ONE has its T4 capstone unlocked at any given time
- Switching T4 capstones is the respec-with-legendary-trigger mechanism (D65)
- This is a RUNTIME-ACTIVE marker (`active_t4_chain: str`), not a generation-time fixed property
- Acceptance: kit JSON has explicit `active_t4_chain` field; gauntlet sim consumes this for damage routing

**Math notes required (Discipline #1):**
1. `wave-1-5-class-chain-architecture-math.md` — per-class chain count + T4 count + supporting chain identification rules
2. `wave-1-5-branching-math.md` — depth-≥4 branching rules; branch consumption; node-count accounting
3. `wave-1-5-active-t4-runtime-math.md` — runtime-active T4 marker; respec mechanism

### 3.4 Season cardinality canonical decision (bundled into Wave 1.5)

Wave 1.5 scope ALSO ratifies:

- **Season cardinality:** Option 2 (multi-fire extension to 30-50 base kits) for Cycle 14 Wave 5
- **Default `n_kits`:** changes from current 22 to **40** (within multi-fire extension's 50-cap) — gives gauntlet meaningful filter
- **Gauntlet PASS rate target:** ~70-80% pass through (so 40 base → ~28-32 surviving)
- **Output documented** as canonical decision in doc 41 § 4 (progression framework — production season cardinality)

**Owner:** gandalf authors the doc 41 § 4 amendment as part of Wave 1.5 close; rocket implements the n_kits=40 default

### 3.5 Class roster scoping question (gating Wave 1.5)

Per doc 40 § 8.3 amendment: "First-pass class roster DEFERRED — substrate-evidence follow-on (Wave 1 BC-target review surfaces substrate vote)."

**Wave 1.5 cannot fire without resolving:** which classes exist? Per-class chain count? Per-class supporting-chain identity?

**Three sub-options:**

| Option | Approach | Trade-off |
|---|---|---|
| **A** — Use Cycle 13 16-archetype list as v1 class roster | Existing `S1_endgame_dex_01_dagger_assassin` etc. names map to classes | Fast; biased by gauntlet-test cohort selection |
| **B** — gandalf authors first-pass class roster (3-4 weeks design call) | Bottom-up design from BC-cell coverage + archetype-vocabulary | Slow; canonical-quality |
| **C** — Substrate-evidence audit (elrond) → gandalf design call | Wave 1 BC-target review pulls archetype-vocabulary from substrate; gandalf curates class list | Substrate-led; defensible |

**gandalf recommendation: Option C.** Composes with Path A substrate-led discipline + Wave 1 BC-target review already in flight. Surface the question to KR — Wave 1.5 gates on this sub-decision landing.

### 3.6 Cross-seam impact

- **gamora damage_resolver:** consumes `active_t4_chain` field; needs MIGRATION.md entry
- **star-lord Track C transform:** character JSON shape adds `active_t4_chain` + `supporting_chain` fields; ingest schema extension
- **elrond:** class roster substrate audit (Item 3.5 Option C) generates input data for Wave 1.5
- **drax:** loadout app skill-tree rendering needs updating — supporting chain visually distinct; branch points renderable; active T4 marker visible

---

## 4. Corrective Part 3 — Discipline #40 Candidate (for jack-ryan)

### 4.1 Statement

**Discipline #40 — Scaffold values shipped to production-output paths require canonical decision before next wave fires.**

When a Wave-N implementation introduces a hardcoded default (cohort size, chain count, tier count, per-class architecture, sampling distribution, etc.) into a code path that feeds production output artifacts, that default MUST either:

- **(a)** be ratified as a canonical design lock in the appropriate canonical doc with explicit STATUS update, OR
- **(b)** be flagged as `SCAFFOLD-WITH-PENDING-DECISION` in:
  - the introducing wave's MIGRATION.md entry
  - the roadmap (`canonical/02-roadmap.md` § 3 or equivalent)
  - the next wave's dispatch as a gating decision

**No "we shipped it so it's the design" inertia permitted.** A scaffold value passing Gate-2 does NOT ratify it as canonical.

### 4.2 Why this discipline is needed

**Three concrete drift cases on 2026-05-27** (this doc § 1.2) demonstrate the failure mode:

1. SC-6b enrichment + uniform substrate sampling → STR heavy-melee monoculture; ammo as main weapons
2. Cycle 13 gauntlet PASS criteria (16 of 18 cells) → 16-character de facto season size
3. Wave 0.5 Track D minimum-viable per-skill emission → 12-skill 3-chain grid contradicting six canonical commitments

Each scaffold WAS appropriate at scaffold time. Each became drift because nobody re-decided when production consumption began.

### 4.3 Operational hook

**When this discipline fires:**

- **At dispatch authoring** (KR): the "out-of-scope" section of a dispatch must explicitly enumerate scaffold values introduced in this wave AND name the decision-required-before for each
- **At Gate-2 review** (jack-ryan): one verification item — "scaffold values in this wave: are they flagged per Discipline #40?" — added to Gate-2 checklist
- **At wave close** (KR): MIGRATION.md entry for the wave must list scaffold values with one of two STATUSES: RATIFIED-AS-CANONICAL or SCAFFOLD-WITH-PENDING-DECISION
- **At roadmap update** (KR): § 3 production progress tracker shows scaffold-pending items as ⚠ visual flag

### 4.4 Cross-references to existing disciplines

- **Discipline #11 (empirical inspection over assumption):** Discipline #40 is the temporal-axis composition — assumption that "scaffold becomes canonical by default" must be empirically tested at every wave-close
- **Discipline #13 (implicit-pillar drift):** Discipline #40 is the mechanical-value analog of #13's conceptual-pillar focus
- **Discipline #18 (math-before-code at hotspots):** Discipline #40 composes — math-notes that introduce scaffold values must include "this is scaffold; canonical decision required by Wave N" provenance
- **Discipline #39 (no-synthetic-stub-as-permanent-fallback):** Discipline #40 is the broader generalization — #39 covers the specific synthetic_mode case; #40 covers the general scaffold-as-drift pattern

### 4.5 Canonical-write target

**Author:** jack-ryan (engineering-disciplines.md is jack-ryan's territory)
**Target file:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #40
**Sequencing:** parallel to KR Wave 1.5 dispatch authoring; not gating Cycle 14 substantive work
**Authority:** Matt 2026-05-27 ratified the recognition; jack-ryan ratifies the discipline-form

---

## 5. Sequencing + Routing Summary

### 5.1 Routing table

| Item | Owner | Sequencing | Gates |
|---|---|---|---|
| Part 1 Fix A — hygiene filter | rocket | Wave 1 closure window OR small follow-on | jack-ryan Gate-2 PASS |
| Part 1 Fix B — STR family rebalancing | rocket | Wave 2 (math-note now; impl Wave 2) | Discipline #1 math-note; Gate-1 + Gate-2 |
| Part 1 Fix C — caster kind audit | elrond | Non-gating; fire anytime | elrond completes; gandalf design-call follow-on if needed |
| Part 2 — Wave 1.5 skill-tree architecture | rocket | INSERT BEFORE Wave 2 | 3 math-notes; Class roster sub-decision (3.5 Option C); jack-ryan Gate-1 + Gate-2 |
| Part 2 — Season cardinality canonical | gandalf (doc 41 § 4 amendment) | Bundled into Wave 1.5 close | Matt ratification of Option 2 default n_kits=40 |
| Part 3 — Discipline #40 ratification | jack-ryan | Parallel to KR Wave 1.5; non-gating | jack-ryan engineering-disciplines.md canonical-write |

### 5.2 KR dispatch packaging recommendation

**Three dispatches:**

1. **Substrate sidecar** (Part 1) — single bundled dispatch with three items (Fix A + Fix B + Fix C)
2. **Wave 1.5 — Skill-Tree Architecture** (Part 2) — substantive rocket dispatch ~1 week scope; gates on class-roster sub-decision (3.5 Option C)
3. **Discipline #40 ratification** (Part 3) — small jack-ryan canonical-write dispatch; parallel

### 5.3 Pre-Wave-5 prerequisite assertion

**Before Wave 5 (production gauntlet sim) fires, ALL of the following must close:**

- [ ] Part 1 Fix A — hygiene filter applied
- [ ] Part 1 Fix B — STR family rebalancing landed
- [ ] Part 2 — Wave 1.5 skill-tree architecture landed (per-class chain count + supporting chain + branching + active T4 marker)
- [ ] Part 2 — Season cardinality canonical decision ratified (Option 2 n_kits=40 default)
- [ ] Part 3 — Discipline #40 canonical-write landed (so Wave 5's MIGRATION.md entry can use the discipline)

Part 1 Fix C is non-gating (audit-first; remediation only if needed).

---

## 6. Cross-references

### 6.1 Canonical docs (consumed)

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 (variable 3-or-4 chains AMENDED 2026-05-27 closeout § 1.4) + D66 + D69 + D83
- `canonical/41-progression-framework-2026-05-27.md` § 2-3 (L50 hybrid; § 4 will receive season cardinality amendment)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 per-attribute weapon profile

### 6.2 Operational + agent docs (consumed)

- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md`
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.3-1.4 (D66 sharpened + variable 3-or-4 chains)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § Q10 (quality > timeline)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` (Wave 2 + Wave 5 dependency naming)

### 6.3 Engine code (referenced)

- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` L238-269 (Fix A + Fix B target)
- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` L130-152 (Wave 1.5 target)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_subspace_generator.py` L173-225 (season cardinality target)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #40 target)

### 6.4 Supersedes

- `agentic_orchestration/gandalf/notes/2026-05-27-substrate-weapon-family-balance-sidecar-request.md` — folded into § 2 of this doc; superseded note marked accordingly

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — consolidated recognition + three-part corrective package
**Authority:** Matt 2026-05-27 ratified (a) three-fix substrate recommendation inline, (b) recognition that 16-char + 12-skill are real drift cases, (c) "author all three as one consolidated document" directive
**Composition:** with doc 40 § 8.3 + § 6.6.1 (variable chain count + supporting chain Option C) + doc 41 § 2-4 (L50 hybrid; § 4 receives season cardinality amendment per Wave 1.5 close) + doc 47 § 3 (per-attribute weapon profile, Fix B aligned) + framing brief Q10 (quality > timeline; supports Wave 1.5 insertion before Wave 2)

**For:** the consolidated corrective package addressing three concrete scaffold-drift instances surfaced 2026-05-27 (substrate weapon family imbalance + 16-character cohort drift + 12-skill 3-chain grid drift), plus meta-corrective Discipline #40 candidate. Routes Part 1 to KR for sidecar dispatch packaging; routes Part 2 to KR for Wave 1.5 scope-doc + dispatch authoring (gates on class-roster sub-decision Option C); routes Part 3 to jack-ryan for engineering-disciplines.md canonical-write. All three parts must close before Wave 5 production gauntlet fires per § 5.3 prerequisite assertion.

**Signed:** gandalf (story-and-design steward)
