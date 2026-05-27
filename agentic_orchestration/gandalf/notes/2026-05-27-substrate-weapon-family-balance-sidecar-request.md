# Substrate Weapon Family Balance — Sidecar Request

> **STATUS:** SUPERSEDED 2026-05-27 — folded into `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` § 2 (Corrective Part 1). Matt 2026-05-27 verbatim "author all three as one consolidated document" directive packaged this sidecar with the Wave 1.5 skill-tree-architecture corrective + Discipline #40 candidate into one consolidated recognition + corrective document. Refer to the consolidated doc for the authoritative routing + sequencing.
>
> _Original STATUS (now superseded):_ CURRENT — gandalf-authored design recognition + sidecar request. Matt 2026-05-27 approved three-fix recommendation per design-call inline response. Routes to knight-rider for dispatch packaging.

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "Agree with #5 recommendation of Three discrete fixes (layered). Please author the side-car."
**Target seams:** rocket (Fix A + Fix B implementation) + elrond (Fix C substrate audit)
**Sequencing target:** Fix A folds into Wave 1 closure window (small); Fix B Wave 2 candidate; Fix C audit-first, evidence-gated remediation

---

## 1. Diagnosis (empirical state)

### 1.1 Substrate composition (2,293 v1_scope rows in `weapon_sim_props`)

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

By `weapon_kind` (contamination surface):

| Kind | Count | Concern |
|---|---|---|
| category | 1,139 | Clean |
| named_template | 927 | Clean |
| **ammo_or_consumable** | **148** | **Arrows/bolts eligible as main weapon** |
| unique | 42 | OK |
| shield/talisman/banner/horn | 36 | Off-hand items leaking |

### 1.2 Selection algorithm (`substrate_weapon_binding.py:_query_substrate_weapon` L238-269)

```sql
SELECT ... FROM weapon_knowledge_entries wke
JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id
WHERE wke.v1_scope = 1 AND wsp.primary_stat = ?  -- bc_attribute only

rng = random.Random(seed)
selected = rng.choice(rows)  -- UNIFORM
```

**No family-balancing. No weapon_kind filter. No weighting.**

### 1.3 Within-attribute family routing produced

| BC attribute | Family options | Lock effect |
|---|---|---|
| STR | martial-heavy 90% / ranged 10% | **Heavy-melee dominant — variety floor ~10%** |
| DEX | ranged 66% / martial-light 34% | Moderately balanced |
| INT | caster-arcane 100% | Single-family lock (by design — caster routing) |
| WIS | caster-faith 100% | Single-family lock (by design — caster routing) |

**Variety problem concentrated in STR** — Diablo II "every barbarian carries a two-hander" pattern. The 90:10 split is too steep without intervention.

---

## 2. Three-fix recommendation (Matt 2026-05-27 ratified)

### Fix A — Hygiene filter (no design call; pure correctness)

**Add `wke.weapon_kind IN ('category', 'named_template', 'unique')` to the substrate query.**

- Eliminates 185 contamination rows (148 ammo + 36 shield/talisman/banner/horn + 1 unknown)
- Reduces draw pool from 2,293 → 2,108 (still abundant per attribute)
- Trivial code change; module-load assertion verifies count
- **Owner:** rocket
- **Sequencing:** fold into Wave 1 closure window OR fire as small follow-on dispatch
- **Risk:** none — pure correctness

### Fix B — Within-STR family rebalancing (design call ratified)

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

**Effect on 4-STR cohort:** expected ~2.8 heavy-melee + ~1.2 ranged STR characters (from current ~3.6 + ~0.4). Produces "STR archer" / "STR crossbowman" archetypes at meaningful frequency — composes with the cohort-archetype filename pattern (`S1_endgame_str_03_polearm_soldier.json` already names a family-specific archetype; STR-ranged would map to `S1_endgame_str_NN_archer_warrior.json`).

- **Owner:** rocket
- **Sequencing:** Wave 2 candidate (alongside Layer 8 set keying — both touch substrate sampling logic)
- **Math note required:** Discipline #1 — `within-attribute-family-weight-math.md` documenting the 70/30 / 60/40 derivation + variance implications
- **Decision before:** Wave 5 gauntlet (cohort outputs depend on STR-family distribution)

### Fix C — Within-caster weapon_kind variety audit (substrate-first)

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

---

## 3. Sidecar dispatch package proposal (for KR)

KR drafts as ONE bundled sidecar dispatch or splits per owner — KR's call.

### Option 1 — Single sidecar dispatch (recommended)
Title: `2026-05-27-substrate-weapon-family-balance-sidecar.md`
Items: A (rocket) + B (rocket math-note + impl) + C (elrond audit)
Sequence: A fires immediately (Wave 1 window); B math-note fires now, impl Wave 2; C audit fires now

### Option 2 — Split per owner
- `2026-05-27-rocket-substrate-hygiene-filter.md` (Fix A small)
- `2026-05-27-rocket-substrate-family-rebalance.md` (Fix B Wave 2)
- `2026-05-27-elrond-caster-kind-audit.md` (Fix C audit)

**Recommendation: Option 1 — single dispatch with three items.** Keeps the design intent unified; sub-agents read one doc; KR closes one dispatch with three completion records.

---

## 4. Cross-references

- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 — per-attribute weapon profile (Fix B preserves attribute routing)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 — substrate-led discipline (Fix B aligns substrate sampling with cohort-archetype intent)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` — SC-6 substrate audit (Fix A directly remediates contamination surface noted there)
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md` — SC-6b Path A landed (Fixes consume the `weapon_type_family` column SC-6b added)

---

## 5. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — sidecar request authored; routes to knight-rider for dispatch packaging
**Authority:** Matt 2026-05-27 ratified three-fix recommendation
**Composition:** with doc 47 § 3 per-attribute weapon profile + doc 40 § 8 substrate-led discipline + SC-6 audit (contamination surface) + SC-6b enrichment (Path A schema)

**For:** the Matt 2026-05-27 ratification of the three-discrete-fix recommendation — Fix A hygiene filter (eliminate 185 ammo/off-hand contamination rows; rocket; Wave 1 window) + Fix B within-STR family rebalancing (70/30 heavy/ranged; rocket; Wave 2; math-note required) + Fix C caster weapon_kind audit (elrond; non-gating). Routes to knight-rider for dispatch packaging — recommend single bundled dispatch.

**Signed:** gandalf (story-and-design steward)
