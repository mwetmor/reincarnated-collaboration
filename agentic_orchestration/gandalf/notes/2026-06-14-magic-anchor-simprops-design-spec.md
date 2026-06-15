# magic-anchor caster sim_props — design-spec hand-off to elrond

**Type:** design-spec-as-math hand-off (gandalf seam → elrond, catalogue/substrate seam).
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (Pattern-B) — "Author the sim_props pass for these 102 in elrond's seam."
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` — the weapon-as-identity model these rows must satisfy (selected weapon's `weapon_type_family` = the kit-identity root).
- `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/MIGRATION.md` — the 206-row caster enrichment precedent; this pass uses the SAME mechanics (source-tagged ingest, sim_props authoring, v1_scope membership).
- `agentic_orchestration/elrond/notes/2026-05-27-caster-weapon-kind-audit.md` — the caster-faith mace-domination finding (62%) this pass partially remediates by adding staff/censer/reliquary/ritual faith-forms.

---

## 0. TL;DR — what + why

102 `gandalf-authored-magic-anchor-*` rows (24 classical + 29 medieval + 49 contemporary) are **knowledge-only**: `v1_scope=0`, ZERO `weapon_sim_props`, ZERO `weapon_type_family`, `quality_tier` null. The content is high-coherence caster material (gandalf review 2026-06-14: classical deity-foci excellent; medieval arcane/folk-caster + reliquary-faith both coherent; contemporary tech-casters mostly strong, five gun-casters flagged). **They cannot be selected as weapon-as-identity roots until sim_props exist.** This pass authors the sim_props + family + primary_stat that lift them from reserve to selectable, using the existing pool's proven conventions so they sit coherently beside the 2,499 `v1_scope=1` rows.

**One-line move:** map each row to one of six archetype sim-profiles (grounded in real pool exemplars below), assign family + primary_stat per the resolution rule, quality-score to the pool standard, and document the v1_scope-flip pool-growth as a Matt-reversible deployment step.

---

## 1. The 102 rows — current state (live-verified 2026-06-14)

| source_library | rows | period bucket |
|---|---|---|
| `gandalf-authored-magic-anchor-ancient-2026-06-01` | 24 | classical |
| `gandalf-authored-magic-anchor-medieval-2026-06-01` | 29 | medieval |
| `gandalf-authored-magic-anchor-modern-2026-06-01` | 49 | contemporary |

All 102: `v1_scope=0`, no `weapon_sim_props` row, no `weapon_type_family`, `quality_tier` null. `proxy_attribute_class` distribution (already authored, use as the family-resolution input): **INT 7 · INT_or_WIS 81 · WIS 6 · STR_or_WIS 6 · STR 2.**

---

## 2. Family + primary_stat assignment rule (the design call)

The pool is **single-stat-per-caster-family**: `caster-arcane → INT` (235/235), `caster-faith → WIS` (228/228), `hybrid → mixed`. So every row resolves to exactly one (family, primary_stat) pair:

| proxy_attribute_class | Resolution |
|---|---|
| `INT` (7) | → **caster-arcane / INT** |
| `WIS` (6) | → **caster-faith / WIS** |
| `INT_or_WIS` (81) | **Per-row discriminator** (canonical_name + register): channels **arcane-cosmic-elemental** power → caster-arcane / INT; channels **devotional-divine-holy** power → caster-faith / WIS. **Default leans:** deity-anchored *elemental* foci (Aeolus' wind-pipes, Hades' bident, Quetzalcoatl staff) → **caster-arcane** (they wield element/cosmos, not devotion); censers, reliquaries, prayer/relic implements, crusader/saint items → **caster-faith**. |
| `STR_or_WIS` (6) | Faith-melee channels (reliquary-swords). Faith-dominant → **caster-faith / WIS** (melee profile, template C); martial-dominant → **hybrid / STR** (template F). |
| `STR` (2) | Legendary swords with a faith overlay (e.g. Joyeuse — canonically STR-coded named sword). → **hybrid / STR** (template F). |

**You (elrond) own the per-row call** — you hold these rows. The rule above is the design intent; canonical_name + register are the discriminators. Flag any row where the lean is genuinely 50/50 and I'll adjudicate.

---

## 3. The six archetype sim-profile templates (grounded in real pool exemplars)

Map every row to ONE template. Values are the proven sibling-row conventions (pulled live from the pool 2026-06-14), not invented. Tune within the listed bands to fit the specific weapon; do not exceed the family's pool band (arcane range_max ≤22, faith range_max ≤18; both charge ≤1.2; both amp ≤3.75).

| # | Archetype | family / stat | range_min–max | atk_speed | charge_s | hits | aoe | amp_min–max | spellmod | pool exemplar |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | Arcane single-target (staff/rod/wand/focus/sceptre) | caster-arcane / INT | 5.0–18.0 | 1.5 | 0.0 | 1 | 0.0 | 0.84–2.4 | ~64–100 | Flutterby Rod |
| **B** | Arcane area (projector/diffuser/emitter/orb) | caster-arcane / INT | 5.0–18.0 | 0.7 | 1.2 | 1 | 3.5 | 0.48–3.0 | ~50–86 | (Censer pattern, arcane-coded) |
| **C** | Faith melee channel (reliquary-sword/brand/faith-mace) | caster-faith / WIS | 0.5–2.5 | 1.5 | 0.0 | 1 | 0.0 | 0.84–2.4 | ~55–70 | Mace of Nova Scotia |
| **D** | Faith ritual implement (censer/distaff/pestle/sigil/broom/vajra) | caster-faith / WIS | 2.5–7.0 | 0.7 | 1.2 | 1 | 3.5 | 0.48–3.0 | ~80–90 | vajra |
| **E** | Faith long-range area (high censer / area-faith) | caster-faith / WIS | 5.0–18.0 | 0.7 | 1.2 | 1 | 3.5 | 0.48–3.0 | ~37–60 | Censer of Righteousness |
| **F** | Martial-faith hybrid (STR-coded sword + faith overlay) | hybrid / STR | 0.5–2.5 | 1.2 | 0.0 | 1 | 0.0 | 0.84–2.4 | ~30–50 | (hybrid STR convention) |

**Spell-glove / gauntlet forms** (contemporary `*Glove` / `*Gauntlet`): template **A** at the **short** end (range_min 2.5, range_max ~10) — close-mid hand-caster; keep arcane/INT unless register is explicitly devotional.

---

## 4. Per-row archetype mapping (keyword → template)

Discriminate on the weapon-form noun in `canonical_name`:

- `staff / rod / wand / focus / sceptre / pipes / quill / lance` + arcane → **A**
- `projector / diffuser / emitter / channeler / orb / mirror` (area/sci-fi vessel) → **B** (arcane) or **E** (faith) by stat
- `sword / brand / reliquary-sword / cleaver / mace` + faith → **C**
- `censer / distaff / pestle / sigil / broom / athame / ladle / vajra / bident-as-ritual` → **D**
- `banner / standard / oriflamme / tug` (faith-standard, long projection) → **E**
- `glove / gauntlet` → **A-short**
- STR-coded named swords (Joyeuse, Durendal-if-martial) → **F**

This is guidance, not a lookup — the canonical_name + description carry the intent; you arbitrate edge cases.

---

## 5. The five gun-caster soft-spot (explicit design flag — Matt-visible)

`Coilgun Caster Pistol`, `Railgun Caster Rod`, `Antimatter Channeler Rifle-Caster`, `Ion Pulse Carbine-Caster`, `Thermal Channeler Carbine-Pistol`. The underlying form is a **gun**; "Caster/Channeler" is asserted by name. Under weapon-as-identity this is genuinely ambiguous (INT spell-projector vs DEX ranged-physical).

**Ruling:** assign **caster-arcane / INT, template A at extended range** (range_max up to 22) — honors the asserted caster identity AND the purpose these were authored for (filling the near-zero modern-caster axis). **Tag them** `gun_caster_identity_forced` in `sim_viability_notes` so the call is greppable and Matt can veto to ranged-DEX if the gun-form should win. Do NOT silently route them to `ranged`.

---

## 6. Mechanics, acceptance, and the v1_scope-flip consequence

**Author to the 206-row enrichment precedent:**
- New `weapon_sim_props` row per entry (FK `weapon_id → weapon_knowledge_entries.id`); `secondary_stat='none'` unless a clear dual-scaling case; `hits_per_attack=1` (these are single-hit casters); `sim_viable=1` (they map onto proven-viable templates — inherit the presumption); `sim_viability_notes` records the template letter + any flag; `sim_verified_date` = authoring date.
- Quality-score to the pool standard so `quality_tier` is non-null (selection coherence — unscored rows create selection artifacts).
- New source-tag `legolas_crawl_substrate_enrichment` analog or `gandalf_magic_anchor_simprops_v1_2026_06_14`; write a `MIGRATION.md` in your seam documenting before/after family counts.

**Acceptance criteria:**
1. All 102 carry a `weapon_sim_props` row with `weapon_type_family ∈ {caster-arcane, caster-faith, hybrid}` + a non-null `primary_stat`.
2. Family split honors § 2; the five gun-casters carry the § 5 flag.
3. `quality_tier` non-null on all 102.
4. Pool family counts re-reported (expected ≈ caster-arcane 235→~300, caster-faith 228→~290, hybrid 70→~80).

**The v1_scope-flip = the one Matt-reversible deployment step (FLAG, do not bury):**
Flipping `v1_scope=0→1` grows the live cycle-14 BALANCED pool **2,499 → ~2,601** and shifts caster/hybrid share **21.3% → ~24%**. This is *directionally aligned* with the deliberate caster-enrichment trajectory (the pool was 85.8% martial pre-206-enrichment) — GOOD, not a violation. **Default: set `v1_scope=1`** (honoring "make these selectable"), and document the growth in MIGRATION so it is one-UPDATE reversible. **If Matt prefers cycle-14 frozen,** hold the flip at `v1_scope=0` (rows stay ready-but-staged for the next pool re-snapshot) — author everything else regardless. Surface this choice to Matt at hand-back; do not let it block the sim_props authoring.

---

## 7. Routing

- **elrond:** execute §§ 2–6; author sim_props + family + primary_stat + quality; write the seam MIGRATION; report family counts + the v1_scope decision back.
- **gandalf:** review the family assignments (esp. the 81 INT_or_WIS resolutions + the 5 gun-casters); adjudicate any 50/50 flags; relay the v1_scope choice to Matt.
- **gamora (downstream, optional):** a confirmatory sim-viability batch on the 102 once selectable — not blocking; the templates are proven-viable siblings.
- **KR:** aware of the pool-growth consequence (weapon-as-identity spec roots on this pool; +102 rows shifts its anchor counts, not its family-aware logic).

---

**Signed:** gandalf, 2026-06-14
**For:** lifting the 102 magic-anchor caster rows from knowledge-only reserve to selectable weapon-as-identity roots — six pool-grounded archetype sim-profiles, a single-stat family-resolution rule, the gun-caster identity-forcing ruling, and the v1_scope-flip surfaced as a Matt-reversible deployment decision.
