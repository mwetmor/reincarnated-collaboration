# Scaffold-Drift Case #7 — Cell-Label Class-Concept Leak (Inspection Verdict)

> **STATUS:** URGENT — scaffold-drift case caught BEFORE Wave 5 production season fires. Class concept leaks from engine to player-facing display despite 2026-05-27 no-classes recommitment.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-28
**Trigger:** Matt-requested inspection ("fire the inspection now") of bc_cell ID surfacing in player-facing exports
**Scope:** Inspection only; ratification + remediation requires Matt Pattern-B call
**Authority:** This verdict is a finding artifact; architectural remediation requires Matt + KR + rocket + drax coordination

---

## 0. TL;DR

**The no-classes recommitment (2026-05-27) was incomplete.** The class concept survives architecturally — not in canonical docs (those were redacted) or in math notes (also redacted) or in gandalf notes (redacted) — but in **engine code** that pre-dates the recommitment AND in **drax loadout app code** that surfaces engine labels directly to the player.

Concretely:
- `reincarnated-engine/src/reincarnated/generation/bc_target_cell_sampler.py` defines **25 hand-authored `CellDef` entries with class-archetype labels** (Heavy Barbarian, Dagger Assassin, Standard Wizard, Channeling Cleric, etc.) — these are NOT substrate-emergent
- `reincarnated-loadout/src/data/cycle13Types.ts` has `deriveCharacterDisplayName()` that extracts the label from `character_id` and **surfaces it as the player-facing display name**
- `reincarnated-loadout/src/components/Cycle13/Cycle13CharacterHeader.tsx` + `Cycle13SampleSection.tsx` render the derived name to the player
- `reincarnated-loadout/src/__tests__/cycle13-db-integration.test.ts` asserts this behavior as **canonical** (e.g., `expect(deriveCharacterDisplayName('S1_endgame_str_01_heavy_barbarian')).toBe('Heavy Barbarian')`)
- LLM uniform-naming layer (per D-Sharpened spec) exists in `reincarnated-engine/src/reincarnated/llm/naming.py` but is **NOT in the player-facing display name pipeline** for kits/characters

**The player sees engineer-authored class archetype names directly.** Heavy Barbarian, Dagger Assassin, Standard Wizard — a 25-class roster encoded as engineering labels and surfaced to the player without an LLM uniform-naming buffer.

This is **scaffold-drift case #7** in Cycle 14. The framing-audit (Discipline #42) predicted this kind of catch but the no-classes recommitment redaction inventory MISSED the engine + loadout surfaces.

---

## 1. Evidence chain

### 1.1 Engine — hand-authored 25-class roster in cell sampler

`/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_cell_sampler.py` (created `9597084` cycle-12-layer-2):

```python
CellDef(
    cell_id=1,
    label="Heavy Barbarian",
    mechanical_cell="str_heavy_barbarian_pair",
    bc_target=BcTargetCell(range="melee", tempo="low", amplitude="spiky", attribute="STR", proxy_density="none"),
    ...
)
```

**25 CellDef entries with class-archetype labels** (lines 85-400):

| Attribute | Labels |
|---|---|
| STR | Heavy Barbarian, Light Fighter, Polearm Soldier, Thrown-Heavy/Atlatl, Ancestor-Warrior |
| DEX | Dagger Assassin, Archer, Crossbow Sniper, Twin-Blade Fencer, Falconer/Pet-Archer, Trap Assassin/Mine-Mercenary |
| INT | Standard Wizard, Artillery Mage, Pyromantic Caster, Red Mage/Spellsword, Arcane-Familiar Mage, Necromancer Summoner, Totem Hierophant |
| WIS | Channeling Cleric, Holy Knight/Paladin, Ritual Mage/Oracle, Storm Caller/Druid, Monk-archetype, Druid Beastmaster, Witch Doctor Petmaster |

This is a **25-class roster** encoded as engineering labels in the BC cell sampler. Not substrate-emergent. Hand-authored by rocket in cycle-12-layer-2.

### 1.2 Engine — character_id schema embeds the label

`/Users/admin/Games/reincarnated-engine/src/reincarnated/export/cycle13_loadout_ingest.py` line 126:

```sql
character_id  TEXT PRIMARY KEY NOT NULL,  -- e.g. "S1_endgame_str_01_heavy_barbarian"
```

`/Users/admin/Games/reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export.py` lines 296-312:

```
Source: char_id like "S1_endgame_str_01_heavy_barbarian"
...
Source: "S1_endgame_str_01_heavy_barbarian"
Target: "endgame_str_01_heavy_barbarian" (strip the S1_ season prefix)
```

The character_id format `S{season}_endgame_{attr}_{nn}_{cell_label_snake_case}` embeds the hand-authored label as the load-bearing identifier across the entire engine + export pipeline.

### 1.3 Loadout — player-facing name derived from engineer ID

`/Users/admin/Games/reincarnated-loadout/src/data/cycle13Types.ts` (line 239+):

```typescript
/** Derive human-readable display name from character_id */
export function deriveCharacterDisplayName(characterId: string): string {
  // e.g. "S1_endgame_str_01_heavy_barbarian" → "Heavy Barbarian"
  const parts = characterId.split('_');
  const indexIdx = parts.findIndex((p) => /^\d{2}$/.test(p));
  if (indexIdx >= 0 && indexIdx < parts.length - 1) {
    return parts
      .slice(indexIdx + 1)
      .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
      .join(' ');
  }
  return characterId;
}
```

**The loadout app extracts the engineer-authored label and surfaces it directly as the player-facing display name.** No LLM uniform-naming layer in this path.

### 1.4 Loadout — player-facing rendering

`/Users/admin/Games/reincarnated-loadout/src/components/Cycle13/Cycle13CharacterHeader.tsx` line 53:

```typescript
const displayName = deriveCharacterDisplayName(char.character_id);
```

`/Users/admin/Games/reincarnated-loadout/src/components/Cycle13/Cycle13SampleSection.tsx` line 79:

```typescript
<span>{deriveCharacterDisplayName(c.character_id)}</span>
```

The player sees "Heavy Barbarian" / "Dagger Assassin" / etc. — directly from the engineer label, no LLM intermediation.

### 1.5 Loadout — leak asserted as canonical behavior in tests

`/Users/admin/Games/reincarnated-loadout/src/__tests__/cycle13-db-integration.test.ts` lines 241-251:

```typescript
describe('deriveCharacterDisplayName — ID to human label', () => {
  it('converts heavy_barbarian to Heavy Barbarian', () => {
    expect(deriveCharacterDisplayName('S1_endgame_str_01_heavy_barbarian')).toBe('Heavy Barbarian');
  });
  it('converts dagger_assassin to Dagger Assassin', () => {
    expect(deriveCharacterDisplayName('S1_endgame_dex_01_dagger_assassin')).toBe('Dagger Assassin');
  });
  it('converts standard_wizard to Standard Wizard', () => {
    expect(deriveCharacterDisplayName('S1_endgame_int_01_standard_wizard')).toBe('Standard Wizard');
  });
```

The leak is **explicitly canonicalized in the test suite.** This is not accidental drift — this is documented expected behavior.

### 1.6 LLM uniform-naming layer exists but is OUT-OF-PATH

`/Users/admin/Games/reincarnated-engine/src/reincarnated/llm/naming.py`:

```python
"""
LLM naming layers.
Layer One: skill naming (from mechanical context bundle).
Layer Two: class and monster naming (from gestalt of skills + stats + theme).
All functions mutate and return the entity with name/flavor attached.
"""
```

**Notes:**
- The naming module ITSELF is still framed around "class and monster naming" — vocabulary lock incomplete here too
- The naming module IS in the player-facing pipeline for SKILLS (per existing infrastructure)
- The naming module is **NOT in the player-facing pipeline for KIT/CHARACTER DISPLAY NAMES** — character display name is derived from the engineer ID in the loadout app, not from any LLM-generated name

---

## 2. Architectural implication

### 2.1 What the no-classes recommitment caught (correctly)

Per `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` § 3 redaction inventory:

- ✅ `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + § 6.6.1 (per-class chains → per-kit)
- ✅ Option α math notes (5 notes) — terminology redacted
- ✅ gandalf-authored notes — terminology redacted
- ✅ `canonical/48-cycle-14-class-roster-2026-05-27.md` — VESTIGIAL status
- ✅ `_SyntheticPlayerClass` retired at Wave 0.5

### 2.2 What the recommitment MISSED

- ❌ `bc_target_cell_sampler.py` — 25 hand-authored CellDef labels constituting a class roster
- ❌ `character_id` schema — embeds the label as load-bearing identifier in engine + export + loadout
- ❌ `deriveCharacterDisplayName` in loadout — surfaces engineer label directly as player-facing name
- ❌ Loadout components — render engineer label to player
- ❌ Loadout test suite — asserts the leak as canonical
- ❌ `llm/naming.py` module framing — still calls itself "class and monster naming"

### 2.3 Why this is scaffold-drift case #7

Pattern: the no-classes recommitment caught the class concept where it was VISIBLE (canonical docs, math notes, gandalf-authored notes) but missed where it was INVISIBLE (engineering code authored in earlier cycles, technical ID schemas, downstream consumers).

The 6 prior scaffold-drift cases (doc 48 + Phase 7 SPEC/IMPL + _SyntheticPlayerClass + BASE_SPELL_DAMAGE_L50 + GAUNTLET_ENCOUNTER_PASS_FLOOR + engine KPM ceiling 600.0) were caught BEFORE production fired. This case is being caught BEFORE Wave 5 production season fires — same pattern, same window.

### 2.4 What the framework says about this

- **D-Sharpened (locked):** substrate-anchor metadata hidden engine-layer; LLM uniform player-facing names. Currently VIOLATED for kit/character display names.
- **Discipline #41 (pre-authored taxonomy interrogation):** 25 hand-authored CellDef labels = pre-authored taxonomy. Substrate vote is being bypassed at the labeling layer.
- **Discipline #42 (framing-audit at sub-agent dispatch consumption):** the recommitment redaction inventory needed a framing-audit that asked "what player-facing surfaces inherit class taxonomy that aren't in the redaction inventory?" — this would have caught the loadout surfaces.
- **D7 AI-tell line:** the player-facing display name is engineer-authored prose, not LLM-curated. Honors D7 spec ironically — but in a way that hardcodes the pre-imposed taxonomy.

### 2.5 The honest read

The 25 cell labels may have been authored with **real design intuition** about ARPG archetypes — Heavy Barbarian, Standard Wizard, etc. are recognizable genre patterns. The substrate clustering (PM-1) might converge on similar shapes (this is the D6 A/B comparison hypothesis). But by **hardcoding** the labels at the cell-sampler layer AND surfacing them to the player WITHOUT an LLM uniform-naming buffer, the architecture pre-imposes the taxonomy rather than letting the substrate vote.

**Even if substrate clusters happen to converge on similar archetypes, the player should see LLM-generated uniform names, not engineer labels.** Otherwise we can never know whether the player is responding to substrate-emergent identity or to engineer-imposed labels.

---

## 3. Remediation options

### Option R1 — Full vocabulary scrub + LLM uniform-naming integration (~3-5 days)

- Redact `bc_target_cell_sampler.py` CellDef labels to substrate-coordinate descriptors (e.g., "Cell-1 STR-melee-low-spiky-pair-A" instead of "Heavy Barbarian")
- Update `character_id` schema to remove embedded class label (e.g., `S1_endgame_str_01_cell01` instead of `S1_endgame_str_01_heavy_barbarian`)
- Integrate LLM uniform-naming layer (per D-Sharpened) into character display name pipeline
- Update loadout app: `deriveCharacterDisplayName` consumes LLM-generated display name from JSON, not from character_id
- Update test suite to assert LLM-name pathway, not label-derivation pathway
- Pros: full no-classes architectural integrity; substrate-led discipline preserved at player-facing surface
- Cons: ~3-5 days; touches engine + export + loadout + tests; could delay Cycle 14 close

### Option R2 — Partial scrub: rename labels to non-class-coded descriptors (~1-2 days)

- Redact `bc_target_cell_sampler.py` CellDef labels to substrate-coordinate descriptors
- Update `character_id` schema accordingly
- DEFER LLM uniform-naming layer integration to Cycle 15
- Loadout `deriveCharacterDisplayName` continues to derive from ID, but ID now contains substrate-coordinate descriptor (e.g., "STR Melee Low Spiky" instead of "Heavy Barbarian")
- Pros: no-classes vocabulary respected; substrate-led at display layer (substrate coordinates ARE the descriptor)
- Cons: player sees less evocative names; LLM uniform-naming deferred

### Option R3 — Minimal scrub: redact only `bc_target_cell_sampler.py` label strings (~half day)

- Redact CellDef labels to substrate-coordinate descriptors
- LEAVE existing kit_archive.db data with old labels (smoke data only; will regenerate at Wave 5)
- Update `character_id` schema for new generations
- Cycle 15 picks up LLM uniform-naming integration + loadout deeper refactor
- Pros: fastest unblock; Wave 5 production season fires under clean architecture
- Cons: partial; loadout still uses label-derivation pattern (legacy behavior); player UX experience deferred

### Option R4 — Defer to Cycle 15 entirely with explicit acknowledgment (~0 days; risky)

- Accept 25-label leak for Cycle 14 v1
- Add explicit Discipline #39 scaffold-with-pending-decision marker
- Cycle 15 picks up full Option R1 work
- Pros: zero Cycle 14 impact
- Cons: Cycle 14 v1 ships with class taxonomy visible to player; A/B comparison (D6) becomes bias-loaded because player UX inherits pre-imposed labels; the no-classes recommitment is functionally undone for the player surface

### Option R5 — Hybrid: Option R3 now + Cycle 15 commitment to Option R1 (~half day Cycle 14 + Cycle 15 scope)

- Cycle 14: minimal scrub of `bc_target_cell_sampler.py` label strings to substrate-coordinate descriptors
- Update character_id schema for Wave 5 production season
- Update loadout `deriveCharacterDisplayName` to handle new ID format (no behavioral change for player; cleaner ID)
- Cycle 15: full LLM uniform-naming integration per D-Sharpened
- Pros: substrate-led discipline restored at engine; player sees neutral substrate-coordinate names instead of class labels; LLM uniform-naming work scoped to Cycle 15 where it belongs
- Cons: ~half-day Cycle 14 work; defers richer naming UX to Cycle 15

---

## 4. Recommendation

**gandalf-recommend Option R5 (Hybrid).**

Rationale:
1. **Substrate-led discipline restoration is non-negotiable.** Allowing class labels to surface to the player AT ALL undoes the no-classes recommitment in practice. Wave 5 production season cannot ship with this leak intact without contradicting the architecture's stated commitments.
2. **Option R1 full work is correctly Cycle 15 scope.** LLM uniform-naming integration requires Phase 5 cohesion-judge LLM to mature + D-Sharpened spec to operationalize + naming prompt template authoring. That's Cycle 15 work; doesn't fit Cycle 14 close.
3. **Option R3/R5 minimal scrub is ~half day.** Acceptable Cycle 14 cost. Doesn't delay Wave 5 production fire materially (composes with Phase 7 IMPL bridge ~1-2 weeks; minimal scrub fires during Phase 7 IMPL work).
4. **Option R5 vs R3:** R5 explicitly commits Cycle 15 to LLM uniform-naming work, which scopes the architectural close. R3 leaves the deeper UX work unclaimed.
5. **Option R4 (defer entirely) is unacceptable** because A/B comparison (D6) becomes bias-loaded: if the player sees "Heavy Barbarian" labels, the A/B comparison cannot honestly distinguish "substrate clusters converged on archetypes" from "we pre-imposed archetypes and called them substrate clusters."

### 4.1 Scope of Cycle 14 minimal scrub (Option R5 part 1)

| Item | Change | Owner | Effort |
|---|---|---|---|
| `bc_target_cell_sampler.py` 25 CellDef labels | Replace class-archetype labels with substrate-coordinate descriptors (e.g., "STR Melee Low Spiky A" instead of "Heavy Barbarian") | rocket | ~0.25d |
| `mechanical_cell` strings (25 cells) | Audit + redact class-coded substrings (e.g., `str_heavy_barbarian_pair` → `str_melee_low_spiky_pair_a`) | rocket | ~0.1d |
| `character_id` schema | Update embedded label format to use substrate-coordinate descriptor | star-lord (export seam) | ~0.1d |
| `deriveCharacterDisplayName` in loadout | Update to parse new format; player sees substrate-coordinate descriptor | drax | ~0.05d |
| Loadout tests | Update integration tests to match new format | drax | ~0.05d |
| `llm/naming.py` module docstring | Update "class and monster naming" framing → "kit and monster naming" | star-lord | ~0.02d |
| Wave 5 production season | Fires UNDER the scrubbed architecture | gamora + cascade | already scoped |

**Total minimal scrub:** ~half day; can fire in parallel with Phase 7 IMPL bridge.

### 4.2 Cycle 15 scope (Option R5 part 2)

| Item | Change |
|---|---|
| LLM uniform-naming layer integration | Per D-Sharpened spec; LLM generates kit/character display name from cluster context + substrate identity |
| Loadout display name source | Consume LLM-generated `display_name` field from JSON, not from character_id derivation |
| `llm/naming.py` "Layer Two" | Implements kit/character naming function (replaces existing "class naming" framing) |
| Loadout tests | Assert LLM-name pathway |

---

## 5. Pre-Wave-5 framing-audit recommendation

Per Discipline #42 framing-audit three-question protocol, applied to the Wave 5 production season dispatch:

**Q1 — What load-bearing framing assumptions does Wave 5 depend on?**

(1) Substrate-led discipline is intact across the engine + player-facing pipeline; (2) Character display names reflect substrate identity, not pre-imposed taxonomy; (3) A/B comparison (D6) can honestly distinguish substrate convergence from pre-imposition.

**Q2 — What evidence currently in hand could refute these assumptions?**

This inspection. The 25 hand-authored CellDef labels + the loadout `deriveCharacterDisplayName` surface-leak refute assumption (1) and (2). Assumption (3) becomes bias-loaded.

**Q3 — If refutation evidence exists, is the right move to refine the framing rather than execute the work as-framed?**

Yes. Wave 5 production season should NOT fire until the cell-label scrub lands. The architectural commitment fails its own stated goals otherwise.

---

## 6. KR coordination

This finding requires:
1. Matt Pattern-B ratification of Option R5 (or alternative)
2. KR routes minimal scrub as parallel work to Phase 7 IMPL bridge
3. rocket + star-lord + drax coordinate the scrub (~half day)
4. Wave 5 production season fires UNDER the scrubbed architecture (acceptance criterion: no class-coded labels surface to player)
5. Cycle 15 scope commits to LLM uniform-naming integration (Option R5 part 2)

---

## 7. The bigger pattern

7 scaffold-drift cases caught in Cycle 14 now:

1. doc 48 class roster (caught at canonical lock)
2. Phase 7 SPEC/IMPL ambiguity (caught at gamora Pattern-A)
3. `_SyntheticPlayerClass` (caught at Wave 5 Phase 3 attempt)
4. `BASE_SPELL_DAMAGE_L50` "STARTING ESTIMATE" (caught at rocket Phase 3 re-impl)
5. `GAUNTLET_ENCOUNTER_PASS_FLOOR=14` (caught at gamora SC-7 calibration)
6. Engine KPM ceiling 600.0 (caught at jack-ryan Gate-3 SC7-F1)
7. **Cell-label class-concept leak (this verdict; caught at Matt-requested inspection 2026-05-28)**

Each case found pre-imposed structure that the substrate then refuted (or would have refuted at full scale). The discipline framework is operating as designed. The pattern suggests:

- **Engineer-authored code from prior cycles needs framing-audit re-application** when major architectural recommitments fire. Redaction inventory should explicitly enumerate code surfaces, not just doc + note surfaces.
- **Player-facing surfaces specifically need explicit audit** because they are downstream of the engine + export layers where drift commonly hides.
- **Discipline #42 framing-audit applies to architectural recommitments, not just sub-agent dispatch consumption.** This is a candidate amendment for jack-ryan (engineering-disciplines.md territory).

---

## 8. Sign-off

**Author:** gandalf
**Status:** Inspection complete; finding captured; remediation recommendation = Option R5 (Hybrid).
**For:** Matt Pattern-B ratification + KR scrub coordination + rocket + star-lord + drax minimal scrub implementation.
**Composes with:** D6 A/B comparison success criteria (bias-guard intact only if scrub lands); D13 parallel-fire authorization (scrub fires parallel to Phase 7 IMPL bridge).
**Sequencing:** scrub MUST land before Wave 5 production season fires.

Signed: gandalf
