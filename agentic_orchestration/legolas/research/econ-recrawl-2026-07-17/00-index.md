# Econ Re-crawl — 8-kit Evidence Batch — 2026-07-17

**Mode:** B (targeted re-crawl)
**Commissioner:** gandalf-prime (autonomous atlas-parity run, Matt authorization 2026-07-17)
**Scope:** 8 econ:UNKNOWN residual kits after Census V10 landing (97.5% expressible, 551/565)
**Charge reference:** single largest residual bucket after Wave-C landing; Elrond mechanical application; corpus.db
**Precedent:** `agentic_orchestration/legolas/research/econ-recrawl-2026-07-16/` (20-kit, 17 classified / 3 unverifiable, commit 4abe140f)
**Wave-B spec reference:** `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md`
**Wave-C landed:** LC (life-cost, hp_cost_scale ≤ 0.30), TH (damage-taken-converts), BT (block-trigger), SU (summon-economy) as of engine `941dbbf`. DR (drain) NOT landed — WC-19 deferred; any DR finding = Wave-D scope input.

## Output files

- `00-index.md` — this file
- `application-sheet-2026-07-17.md` — per-kit disposition rows; Elrond applies mechanically

## Summary counts

**Econ batch (8 kits):**
- Classified: 7
- Unverifiable: 1 (`d2-wl-void-rift`)

**Grand total:** 8 kits — 7 classified, 1 UNVERIFIABLE

**Row-count verification:** application-sheet has exactly 8 rows. Summary block counts reconcile with row-level `**disposition**` markers: 7 rows marked `**classify**`, 1 row marked `**unverifiable**`. No discrepancy.

## Landed-vocab distribution (7 classified)

- `spend` (conventional mana-cost): 5 — `d2-bowazon`, `d2-fireclaw-wolf`, `d2-fury-wolf`, `d2-kicksin`, `d2-rabies-wolf`
- `spend` w/ cooldown-gate rider: 1 — `poe1-whispering-ice` (Icestorm — mana + hard 6.50s CD)
- `NR` (near-zero / auto-fire): 1 — `vs-phieraggi` (survivor-genre passive auto-cast, Revival-count multiplier)

## NOTABLE finds flagged for elrond / gandalf

**1. `d2-wl-void-rift` — CORPUS PROVENANCE FINDING (not classifier gap).** Two independent skill-tree enumerations (rpgstash Chaos/Demon/Eldritch guide + fextralife wiki) confirm no D2R Warlock skill named "Void Rift" exists across all 30 skills. Google searches for "Void Rift Warlock" return DESTINY 2 Voidwalker Warlock builds. This suggests "D2" ambiguity between Diablo 2 and Destiny 2 during corpus harvest produced a phantom kit. Not resolvable by Wave-B/C spec; this is a **provenance-integrity finding** for elrond / jack-ryan. Recommended action: consider negative-corpus flag (kit_id retained, negative=1) OR delete row. Mob-harvest v3 tag warrants a broader audit for other "D2" collisions.

**2. Shapeshift form-lock as secondary economy overlay (persistent-form buff).** All three D2 Druid werewolf kits (`d2-fireclaw-wolf`, `d2-fury-wolf`, `d2-rabies-wolf`) have PRIMARY econ = spend (mana per attack: Fire Claws 4, Fury 4, Rabies 10), with a SECONDARY layer: Werewolf form is a **cast-once persistent-form buff** (15 mana cast, base 40s duration extended by Lycanthropy passive; re-cast when timer expires). This is neither RS (no pool reservation) nor PC (not a toggle-drain — it's a durationed buff like an aura-cast). It matches the `SS` sketch-family from prior d2-wl audit (see 07-16 sheet §8 `d4-rabies-lacerate` note). **Not a new-shape finding requiring Wave-D spec — the form-lock is descriptive lineage / gx metadata, not a bin.** Primary econ classification stands. Flagged for elrond's awareness that all three werewolf kits carry the same SS overlay pattern.

**3. `poe1-whispering-ice` — cooldown-gated spend, not stat-to-damage-as-economy.** Classifier's `resource_verbatim=stat→damage` captured Int-scaling but missed the ECONOMY layer. Actual economy: (a) mana cost per Icestorm cast (unspecified base, offset by Inspiration Support in most builds) + (b) hard 6.50s Cooldown Time gating cast rate + (c) Cast while Channelling frequently used to trigger it near-free. The Int-per-10 mechanic scales DAMAGE, not resource. Bin = `spend` with cooldown-rider descriptor. Not a new-shape.

**4. `vs-phieraggi` — genre-native NR (Survivor auto-fire).** Vampire Survivors weapons have no player-controlled cast; they auto-fire on a cooldown timer (1.4s here). Revival-count is a passive damage/amount multiplier (+1 per Revival, cap +10 each), not a spend/reservation/charge. This fits the landed `NR` bin (near-zero / steady auto-fire) and is genre-typical for VS / bullet-heavens generally. `resource_verbatim=revive-stock-as-power` is accurate flavor but the mechanic is passive multiplier, not consumable — Revival is spent when the player DIES (Awake Arcana lets it un-cap), not by weapon use. No Wave-D need.

## No DR / no NEW-SHAPE findings

All 7 classified kits fit landed Wave-B/C vocabulary (`spend` + `NR` with descriptor riders). Zero DR (drain) findings — no drain-scope input for Wave-D from this batch. Zero unmapped shapes.
