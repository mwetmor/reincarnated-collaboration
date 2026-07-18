# VDM-1 Stage 0 — Stale-Flag Inventory: `mobile_blocking_mechanics`

**Date:** 2026-07-18
**Author:** legolas (Mode A, Stage 0b — local work, no DB writes)
**Source for wave-landing state:** `canonical/current-to-end-state/current-to-end-state-engine.md` (census trajectory V7→V13; Wave-A/B/C/D gate records)
**Source for flag taxonomy:** `SELECT DISTINCT mobile_blocking_mechanics FROM canon_corpus` — 24 distinct values across 515 flagged rows
**DB authority:** read-only; elrond is sole writer
**Purpose:** identify which `mobile_blocking_mechanics` flags claim mechanisms that have since landed (Waves A/B/C/D) vs still-open ones — output is a refresh-candidates list for the probe-backfill lane

---

## Background

`mobile_blocking_mechanics` was set at 2026-07-12 snapshot. Since then:
- **Wave-A** (proxy-AI, turret/pet/summon economy A3, summon-as-troop-command geometry, nav slice-1/2): LANDED
- **Wave-B** (resource economies: PC persistent-charges, RS reservation/aura toggles, AM accumulate-meter, RC rack-consume, charge-stack): LANDED
- **Wave-C** (mark/consume triggers, ailments blind/curse/fear/deflect, orbit geometry, placed-lane geometry, TH damage-taken-converts): LANDED
- **Wave-D** (fidelity items: fear flee-AI model-1, decrepify movement, orbit analytic model-1, placed-lane LOS model-B; vocab-loader restore; econ:DR resolved as non-bin): LANDED
- **GX-02 shapeshift docket:** OPEN (3 kits; Matt forks A–E unruled); form-swap NOT landed
- **di-spiritform-druid-pvp:** resolved as phantom (no real "spirit form" mechanic); row `negative=1` per run ruling 16
- **Census V13:** 560/563 = 99.47%; residual tail 3 = all mechanic:shapeshift

---

## Flag-by-Flag Analysis

### 1. `direct-hit instant verbs native` — 193 kits
**Status: LANDED (Wave-A/sim baseline)**
These flags assert the kit requires only instantaneous single-hit projectile/melee/AoE delivery, which was the foundational sim capability.
**All 193 are STALE-LANDED.** Flag is no longer a blocker; these kits should be expressible-now.
**Refresh action:** elrond probe-backfill pass should confirm expressibility and clear this flag (or reclassify if a secondary blocker exists).

---

### 2. `soul-control troop command exists; turret/pet AI variants + summon economy needed` — 66 kits
**Status: LANDED (Wave-A + Wave-B)**
Wave-A delivered A3 summon economy + turret/pet AI basis. Wave-B delivered RS (reservation/aura/summon-slot economy), PC (persistent-charge), AM (accumulate-meter), RC. The summon economy family is fully specified and built.
**All 66 are STALE-LANDED.** Summon economy (Wave-A A3 + Wave-B RS) covers the troop-command surface.
**Refresh action:** elrond probe-backfill should reclassify against the landed Wave-A/B vocabulary.

---

### 3. `no rule matched — Mac pass to classify` — 45 kits
**Status: PARTIALLY STALE — classification-pending, not mechanism-blocked**
This flag marks kits that didn't match any economy/mechanic rule at harvest time and were queued for a Mac-session classification pass. Waves A/B/C/D have since expanded the vocabulary substantially. Many of these will now classify against landed rules.
**Stale:** to the extent the vocabulary gap they represented has closed (most will land post-reclassification).
**Still-open:** a small subset may remain unclassified if they map to genuinely novel mechanisms. Requires per-kit reclassification pass against the current spec — NOT a mechanism gap; a classification-workflow artifact.
**Refresh action:** per-kit reclassification pass against Wave-A/B/C/D vocabulary by elrond. Expected outcome: most land; residue surfaces as new docket items if genuine gaps.

---

### 4. `sustained-stream/channel verb + movement-tax tuning` — 39 kits
**Status: LANDED (Wave-B charge-stack + Wave-C mark/consume primitives)**
Channeling verbs (Cyclone, Incinerate, Scourge Arrow, Blade Flurry, etc.) require the `persistent_trigger` + `commitment_state_machine` surface, which landed in Wave-B. The movement-tax (Cyclone's full-move-during commit) was specified and built.
**All 39 are STALE-LANDED.** The `channel` commit-type in the Wave-B spec covers this family.
**Caveat:** Cyclone-style full-move-during channeling has the `sustained-stream/channel verb + movement-tax tuning` flag explicitly because of the movement-while-channeling interaction. The movement-tax tuning component (balancing channeling-while-moving damage) is in the spec; whether the tuning parameters are fully dialed is a balance question, not an expressibility gap.
**Refresh action:** elrond probe-backfill reclassify to `channel` commit-type / expressible-now.

---

### 5. `mark/tag ledger + consume-trigger operators` — 32 kits
**Status: LANDED (Wave-C)**
Wave-C delivered the mark/consume trigger family: `ActiveEffect("mark:<identity>")` on defender, +5 trigger events including `on-block-successful`, 6 consequence types, `MAX_CHAIN_DEPTH=1` locked. This is the exact mechanism this flag identified as needed.
**All 32 are STALE-LANDED.**
**Refresh action:** elrond probe-backfill reclassify to expressible-now.

---

### 6. `rotational/orbital substrate addendum — build pending` — 18 kits
**Status: LANDED (Wave-C orbit geometry)**
Wave-C landed orbit as the 25th `geometry_value` (analytic, zero-RNG). These 18 kits required orbit-geometry expression which is now in the spec and built.
**All 18 are STALE-LANDED.**
**Note:** Wave-C gate-2 deferred orbit 2D sub-projectile motion to Wave-D fidelity ledger (MVP-deferral). Wave-D landed orbit analytic Model-1. The residue (orbit sub-projectile motion) is in the Wave-D fidelity items, which are registered open. However, for expressibility-now purposes, kits using orbit geometry ARE now expressible — the sub-projectile motion is a fidelity enhancement, not a structural blocker.
**Refresh action:** elrond probe-backfill reclassify to expressible-now (orbit geometry landed).

---

### 7. `evidence record — see harvest report` — 18 kits
**Status: CLASSIFICATION-ARTIFACT, not a mechanism flag**
This value marks kits where the blocking classification was deferred to a harvest report. It is a workflow-tracking note, not a mechanism descriptor. The underlying mechanism may or may not be expressible-now depending on the kit.
**Cannot bulk-classify:** requires per-kit lookup of the harvest report finding.
**Refresh action:** per-kit audit against current spec vocabulary. Cannot stale-flag en masse.

---

### 8. `dash/blink verb — sim support verify; deflect riders new` — 17 kits
**Status: PARTIALLY LANDED**
- Dash/blink verbs: built in Wave-A nav (blink/teleport as instant movement verb) and the committed-movement grammar.
- Deflect: Wave-C spec defined deflect as a `def-bin rider` (not ailment). Wave-C gate-2 deferred deflect conditions to Wave-D fidelity ledger. Wave-D landed primitives; deflect conditions are registered as Wave-D fidelity items (open).
**Stale for dash/blink portion:** movement verbs are in-spec and built.
**Still-open for deflect portion:** deflect-condition primitives are in the Wave-D fidelity ledger (registered open, not yet built). However deflect is a rare mechanism; most of the 17 kits in this bucket likely require only the dash/blink verb, not deflect.
**Refresh action:** per-kit split — reclassify dash/blink component as expressible; flag deflect-dependent kits for Wave-E or fidelity-ledger tracking.

---

### 9. `thorns/stat-retaliation channel` — 11 kits
**Status: LANDED (Wave-C TH damage-taken-converts bin)**
Wave-C delivered the `damage_taken_converts` bin for thorns/retaliation mechanics: POST-mitigation reflect ≤1.00, reflect chain-depth 0. The TH family (3 confirmed members: gd-retaliation-warlord, d4-thorns-barb, d3-invoker-thorns) was corrected from 0 to 3 at Wave-B Gate-1 and landed in Wave-C.
**All 11 are STALE-LANDED.** The thorns/retaliation surface is now expressible.
**Refresh action:** elrond probe-backfill reclassify to expressible-now.

---

### 10. `form-swap stat-block hotswap` — 10 kits
**Status: STILL OPEN (GX-02 shapeshift docket — Matt forks A–E unruled)**
Shapeshift / form-swap is the remaining non-engineering-blocked tail (3 kits in residual tail per V13). The 10 kits with this flag include the 3 shapeshift-docket kits plus 7 additional kits that presumably have a form-swap element as secondary mechanic.
**Still-open:** form-swap stat-block hotswap has NOT landed. GX-02 docket is open; Matt forks A (one-vs-two families), B (persistence), C (slot-semantics), D (entry economy), E (commit-grammar) are unruled.
**Refresh action:** these 10 kits are correctly flagged as blocked. No refresh needed. They ARE the probe-backfill lane's target for form-swap evidence collection.

**Kit list (from DB query):**
```
SELECT kit_id, folk_name, game FROM canon_corpus 
WHERE mobile_blocking_mechanics = 'form-swap stat-block hotswap'
```
(Run against DB for exact list — not reproduced here to avoid stale enumeration risk.)

---

### 11. `echo/clone actors — troop-command adjacent` — 9 kits
**Status: LARGELY LANDED (Wave-A proxy-AI + troop-command + Wave-B RS)**
Echo/clone actor patterns (mirror images, spectral clones) are covered by the summon-economy + troop-command family from Wave-A, with RS reservation-slot economics from Wave-B. The "troop-command adjacent" note is accurate — these use the same proxy-actor framework.
**Stale-landed for the proxy-actor/economy surface.** Whether individual kits are fully expressible depends on whether their specific clone-behavior (e.g., clones that mirror player input vs autonomous actors) maps to the A3 summon grammar.
**Refresh action:** per-kit reclassification pass. Most will land; any that require true player-input mirroring may surface a fidelity note.

---

### 12. `self-cost contract operators` — 8 kits
**Status: LANDED (Wave-B LC self-cost bins + Wave-C hp_cost_scale)**
Wave-C landed LC (life-cost) as `hp_cost_scale ≤ 0.30` with `reservation +hp`. Self-cost contract mechanics (pay life to deal damage, forbidden-rite-style) are now in the spec.
**All 8 are STALE-LANDED.**
**Refresh action:** elrond probe-backfill reclassify to expressible-now.

---

### 13. `battle-sim auto-aim native` — 8 kits
**Status: LANDED (Wave-A nav + proxy-AI)**
Battle-sim auto-aim targeting was delivered by Wave-A slice-1/2 (a)-only nav. These kits required basic targeting policy from the sim, which is now in.
**All 8 are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 14. `return-path/carom projectile solver` — 7 kits
**Status: LANDED (Wave-C placed-lane + return-path spec)**
Return-path and carom (bouncing, returning) projectile mechanics were addressed by Wave-C's `placed-lane` (26th geometry_value, static line collider, blocks projectiles — creates the carom surface) and the return-path solver entries. The placed-lane is built (Wave-C Gate-2 PASS).
**Stale-landed.** However, Wave-C gate-2 deferred placed-lane persistent collider/LOS to Wave-D fidelity ledger. Wave-D landed placed-lane LOS Model-B. These kits are now expressible.
**Refresh action:** reclassify to expressible-now.

---

### 15. `reservation/aura toggles — loot-operator extension` — 7 kits
**Status: LANDED (Wave-B RS reservation-aura bin)**
Wave-B delivered the RS (reservation/aura) bin explicitly. Aura toggles with `persistent_toggle` commitment-state are in the Wave-B spec.
**All 7 are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 16. `union/recipe evolution system (pair-grain authoring)` — 6 kits
**Status: STILL OPEN**
This flag describes kits built around recipe/union mechanics (crafting evolution, pairing synergies at the meta-layer level). This mechanism was not addressed by Waves A/B/C/D. It is not in the current engine spec as an implemented surface.
**Still-open.** These kits likely require a Wave-E or separate docket entry.
**Refresh action:** these kits remain correctly flagged. Probe-backfill should document the exact union/recipe mechanic per kit as evidence for docket authoring.

---

### 17. `persistent/mobile zone entities — VFX slot model adjacent; follow-zones new` — 5 kits
**Status: PARTIALLY LANDED**
- Persistent zones (static): covered by Wave-C `placed-lane` (static zone collider).
- Mobile follow-zones (zones that track the player): the "follow-zones new" sub-note indicates this was NOT in the placed-lane spec (which is static). Mobile follow-zones are not in the current engine spec.
**Stale for static persistent zones; still-open for mobile follow-zones.**
**Refresh action:** per-kit split — static-zone kits reclassify as expressible; mobile-follow-zone kits remain flagged for Wave-E.

---

### 18. `stochastic ops in loot-operator framework — per-cast roll verify` — 3 kits
**Status: LARGELY LANDED**
The loot-operator framework is built (Wave-A/B). Per-cast stochastic rolls (random element hits, elemental hit archetype) are native to the engagement loop's RNG resolution. The loot-operator's per-kill and per-cast roll surfaces are both specified.
**Stale-landed for most patterns.** Verify per-kit that the specific stochastic surface is in-spec.
**Refresh action:** per-kit reclassification pass; most will land.

---

### 19. `on-kill resource-spawn economy (corpse/soul ammo)` — 3 kits
**Status: LANDED (Wave-B RS + corpse/soul surface)**
On-kill resource economies (corpses spawning ammo, soul energy on kill) are addressed by the Wave-B economy spec (on-kill resource-spawn is in the RS/econ vocabulary). The `on-kill` trigger is a native sim event.
**All 3 are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 20. `finite-ammo/consumable economy` — 3 kits
**Status: LANDED (Wave-B PC persistent-charge bin)**
Finite-ammo and consumable-charge mechanics (e.g., flasks as ammo, potion charges) are covered by the PC (persistent-charge) bin from Wave-B.
**All 3 are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 21. `element-application addendum covers hybrid caps — status-gate ops verify` — 3 kits
**Status: LANDED (Wave-C ailment layer + element-application spec)**
Wave-C delivered the ailment layer (sunder, freeze, stun, poison, taunt, blind, curse, fear) with interaction matrix and runaway guards. Hybrid element-cap mechanics and status-gate operations are in the Wave-C ailment spec.
**All 3 are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 22. `lodge/retrieve ammo economy + return-path solver` — 2 kits
**Status: LANDED (Wave-B PC + Wave-C return-path)**
Lodge (projectile embeds) + retrieve (player pulls back, regains charge) economy is a sub-pattern of PC (persistent-charge) combined with the return-path solver from Wave-C.
**Both are STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

### 23. `reap/possession is RDR-native` — 1 kit
**Status: LANDED (native to RDR sim)**
This flag asserts the mechanic (reap/possession) is native to the Reincarnated sim design. No external wave needed.
**STALE (was never actually a blocker).**
**Refresh action:** reclassify as expressible-now (was native all along).

---

### 24. `default-attack scaling native to sim` — 1 kit
**Status: LANDED (Wave-A sim baseline)**
Default-attack scaling is the foundational sim capability (Wave-A sim baseline).
**STALE-LANDED.**
**Refresh action:** reclassify to expressible-now.

---

## Consolidated Stale/Open Register

| Status | Flag | Kit count |
|---|---|---|
| **STALE-LANDED** | direct-hit instant verbs native | 193 |
| **STALE-LANDED** | soul-control troop command exists; turret/pet AI variants + summon economy needed | 66 |
| **STALE-PARTIALLY** | no rule matched — Mac pass to classify | 45 |
| **STALE-LANDED** | sustained-stream/channel verb + movement-tax tuning | 39 |
| **STALE-LANDED** | mark/tag ledger + consume-trigger operators | 32 |
| **STALE-LANDED** | rotational/orbital substrate addendum — build pending | 18 |
| **CLASSIFY-ARTIFACT** | evidence record — see harvest report | 18 |
| **STALE-PARTIALLY** | dash/blink verb — sim support verify; deflect riders new | 17 |
| **STALE-LANDED** | thorns/stat-retaliation channel | 11 |
| **STILL-OPEN** | form-swap stat-block hotswap | 10 |
| **STALE-LARGELY** | echo/clone actors — troop-command adjacent | 9 |
| **STALE-LANDED** | self-cost contract operators | 8 |
| **STALE-LANDED** | battle-sim auto-aim native | 8 |
| **STALE-LANDED** | return-path/carom projectile solver | 7 |
| **STALE-LANDED** | reservation/aura toggles — loot-operator extension | 7 |
| **STILL-OPEN** | union/recipe evolution system (pair-grain authoring) | 6 |
| **STALE-PARTIALLY** | persistent/mobile zone entities — VFX slot model adjacent; follow-zones new | 5 |
| **STALE-LARGELY** | stochastic ops in loot-operator framework — per-cast roll verify | 3 |
| **STALE-LANDED** | on-kill resource-spawn economy (corpse/soul ammo) | 3 |
| **STALE-LANDED** | finite-ammo/consumable economy | 3 |
| **STALE-LANDED** | element-application addendum covers hybrid caps — status-gate ops verify | 3 |
| **STALE-LANDED** | lodge/retrieve ammo economy + return-path solver | 2 |
| **STALE-LANDED** | reap/possession is RDR-native | 1 |
| **STALE-LANDED** | default-attack scaling native to sim | 1 |
| **TOTAL flagged rows** | | **515** |

---

## Summary Counts

| Category | Kit count |
|---|---|
| **STALE-LANDED** (flags that describe mechanisms now fully in engine) | ~397 |
| **STALE-PARTIALLY / STALE-LARGELY** (mostly landed; per-kit audit needed) | ~74 |
| **CLASSIFY-ARTIFACT** (not mechanism flags; workflow-tracking) | 18 |
| **STILL-OPEN** (mechanisms genuinely not yet landed) | ~16 |

**Total STALE-LANDED (bulk-reclassifiable):** approximately 397 rows across 14 flag values. These are the highest-priority probe-backfill candidates — a single elrond pass with the Wave-A/B/C/D vocabulary can reclassify them to expressible-now.

**STILL-OPEN (correctly flagged, require probe-backfill evidence):**
- `form-swap stat-block hotswap` — 10 kits (GX-02 docket; Matt-gated)
- `union/recipe evolution system (pair-grain authoring)` — 6 kits (no wave coverage)

**Fidelity-deferred (Wave-D open items, expressible-now but not EXACT):**
- Orbit 2D sub-projectile motion (Wave-D fidelity ledger)
- Placed-lane persistent collider/LOS (landed Wave-D Model-B — expressible)
- Fear flee-AI model-1 (Wave-D landed primitive §5.c — expressible as primitive)
- Decrepify movement (Wave-D landed §5.d — expressible as primitive)
- Deflect conditions (Wave-D fidelity ledger — still-open)

**Note for probe-backfill lane:** the `no rule matched — Mac pass to classify` 45 kits are a classification-workflow artifact, not a mechanism gap. Reclassification against Wave-A/B/C/D vocabulary will resolve most. Those that don't resolve surface as novel docket candidates requiring ≥3-build evidence per the parsimony ladder (R-7).

---

## Refresh-Candidates List for Probe-Backfill Lane

**Highest priority (bulk reclassify, no per-kit judgment needed):**
1. `direct-hit instant verbs native` — 193 kits → reclassify to expressible-now
2. `soul-control troop command exists; turret/pet AI variants + summon economy needed` — 66 kits → reclassify to expressible-now (Wave-A A3 + Wave-B RS)
3. `mark/tag ledger + consume-trigger operators` — 32 kits → reclassify to expressible-now (Wave-C)
4. `sustained-stream/channel verb + movement-tax tuning` — 39 kits → reclassify to expressible-now (Wave-B `channel` commit-type)
5. `rotational/orbital substrate addendum — build pending` — 18 kits → reclassify (Wave-C orbit geometry landed)
6. `thorns/stat-retaliation channel` — 11 kits → reclassify (Wave-C TH bin)
7. `reservation/aura toggles — loot-operator extension` — 7 kits → reclassify (Wave-B RS)
8. `self-cost contract operators` — 8 kits → reclassify (Wave-C hp_cost_scale)
9. `battle-sim auto-aim native` — 8 kits → reclassify (Wave-A nav)
10. `return-path/carom projectile solver` — 7 kits → reclassify (Wave-C placed-lane + Wave-D LOS)
11. `on-kill resource-spawn economy (corpse/soul ammo)` — 3 kits → reclassify (Wave-B RS)
12. `finite-ammo/consumable economy` — 3 kits → reclassify (Wave-B PC)
13. `element-application addendum covers hybrid caps — status-gate ops verify` — 3 kits → reclassify (Wave-C ailment)
14. `lodge/retrieve ammo economy + return-path solver` — 2 kits → reclassify (Wave-B PC + Wave-C return-path)
15. `reap/possession is RDR-native` — 1 kit → reclassify (native)
16. `default-attack scaling native to sim` — 1 kit → reclassify (Wave-A)

**Per-kit audit needed:**
- `no rule matched — Mac pass to classify` — 45 kits
- `evidence record — see harvest report` — 18 kits
- `dash/blink verb — sim support verify; deflect riders new` — 17 kits (split dash from deflect)
- `echo/clone actors — troop-command adjacent` — 9 kits
- `persistent/mobile zone entities — VFX slot model adjacent; follow-zones new` — 5 kits
- `stochastic ops in loot-operator framework — per-cast roll verify` — 3 kits

**Do NOT refresh (correctly open):**
- `form-swap stat-block hotswap` — 10 kits (GX-02 docket; Matt-gated)
- `union/recipe evolution system (pair-grain authoring)` — 6 kits (no wave coverage; docket candidate)
