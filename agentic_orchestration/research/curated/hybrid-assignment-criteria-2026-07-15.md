# Hybrid-Assignment Criteria — the decision procedure for `treatment=hybrid`

> **STATUS:** CURRENT (load-bearing as of 2026-07-15). The assignment procedure elrond
> applies whenever a tranche or re-key PROPOSES `treatment=hybrid`. Gates the FIRST
> engine-hybrid ingestion ever (Edition-II §10, `la-destroyer-vortex-gravity` +
> `di-cyclone-strike-monk-base`). This memo is the operational form of gandalf's
> taxonomy line; it does not re-decide the taxonomy, it makes it a repeatable ruling.

**Author:** elrond (data steward) · **Date:** 2026-07-15
**Consumes:** gandalf treatment=hybrid taxonomy line (`agentic_orchestration/gandalf/notes/2026-07-15-treatment-hybrid-taxonomy-line.md`, `3f20f738`) — the 4-probe deletion test is gandalf's; this doc operationalizes it as elrond's keying criteria.
**Lineage:** legolas defended-zero red-team (`research/knowledge/mcd-pull-mechanic/2026-07-15-hybrid-wedge-defended-zero.md`); Matt's MCD gravity-assembly signal.
**Governs:** the `canon_engine_key.ctrl_treatment` value (`damage`/`control`/`hybrid`) on any kit whose source or tranche proposes hybrid. Reversible, C3-style: the assignment is a stated verdict on stated evidence; the raw tranche claim is preserved.

---

## 0. The bar (why this exists)

`treatment=hybrid` is a first-class engine role (damage/control/hybrid — ratified taxonomy). The corpus is hybrid-EMPTY at the active grain — that emptiness is the flagship FRONTIER (T5 KEEP ruling), NOT a bucket to fill loosely. So the bar to assign hybrid must be high enough that the emptiness stays honest: a kit keys hybrid **only when the genre genuinely hardlocks two co-equal halves.** Everything short of that keys to its primary treatment + a rider annotation. This memo is that bar, as a procedure.

## 1. The four-probe deletion test (ALL FOUR must PASS)

A kit is `treatment=hybrid` **only if all four probes pass.** Asymmetry on ANY probe → assign the **primary treatment** (the half that survives) + annotate the other half as a rider. This is gandalf's deletion test, keyed to what elrond can read off a tranche/source row.

| # | Probe | PASS condition (hybrid survives) | FAIL → verdict |
|---|---|---|---|
| **P1** | **Damage-removal** | Remove the damage half. The remaining CONTROL is a viable standalone role **for THIS kit as designed** (not as a party-support reconfiguration). | If the control alone is vestigial/party-only → **damage-primary** + control rider. |
| **P2** | **Control-removal** | Remove the control half. The kit STILL functions as a damage kit — but hybrid requires the removal to break it. So PASS = removing control **collapses** the kit (it cannot operate as designed). | If the kit still operates as a damage kit (even degraded) → **damage-primary** + control rider. *Degraded-but-operable FAILS the collapse bar.* |
| **P3** | **Configuration** | NO sanctioned variant of the same kit de-emphasizes either half. | If a sanctioned variant removes/de-emphasizes a half (essence swap, gear path, engraving) → hybrid is a **player option, not kit identity** → primary + rider. |
| **P4** | **Assembly** | Both halves are intrinsic to the kit's class/skill identity. | If the control half is assembled via items/enchants/affixes/boons/runes-in-a-classless-game → **rider-proc lineage** → primary treatment; control documented, never keyed as a hybrid half. |

**Composition rule.** hybrid ⟺ (P1 ∧ P2 ∧ P3 ∧ P4). Any single FAIL → NOT hybrid.

## 2. The four escape doors (name the FAIL when you record it)

Every genre near-miss escapes the wedge through exactly one door. When a probe fails, record WHICH door — it is the reversible-verdict rationale:

- **VESTIGIAL** (fails P1): the non-primary half is trivial/inverted (zMonk's trivial damage).
- **SUPPRESSED-BY-DESIGN** (fails P1 or P2 asymmetrically): the kit gears AGAINST one half (zBarb suppresses its own damage → control-primary, not hybrid).
- **CONFIGURABLE-OUT** (fails P3): a sanctioned variant removes a half (DI Storm Spirit removes Cyclone Strike's pull).
- **GEAR-ASSEMBLED** (fails P4): an enchant/affix/item/rune-economy supplies the control half (MCD Gravity; Ranslor's Folly; Empire's Grasp).

## 3. Rider-annotation form (what a FAIL produces instead of hybrid)

A near-miss keys as: **`ctrl_treatment` = the surviving primary**, and the rider is recorded — NOT invented, NOT silently dropped:

- `ctrl_treatment` = `damage` (or `control`) — the half that survives the deletion.
- `ctrl_function` = the rider's control function level (e.g. `pull`, `knockback`) when the rider is a real control effect.
- Rider provenance in `flags` / mech_note: the door that disqualified hybrid + the source's own framing.

This keeps the kit's real dual character legible (the pull IS there) while refusing the hybrid over-claim (the pull is not a co-equal hardlocked half).

## 4. Two documented calls this memo GATES (Edition-II §10 first ingestion)

Both are PROPOSED `treatment=hybrid` in the pull tranche (`b7f773d3`). Verdicts under §1:

### `la-destroyer-vortex-gravity` — VERDICT: **damage-primary + pull rider** (NOT hybrid)

| probe | reading (from tranche + Lost Ark source) | pass? |
|---|---|---|
| P1 damage-removal | Remove damage → the 6 m pull + High-Stagger remains; but Stagger is a raid-mechanic contribution, and Vortex Gravity's designed role in Hypergravity Mode is the burst-damage identity skill. Control-alone is not this kit's standalone designed role. | **borderline** |
| P2 control-removal | Remove the pull → Vortex Gravity is still a High-Stagger hammer-slam damage burst. It **operates degraded, does not collapse**. Degraded-but-operable FAILS the collapse bar. | **FAIL** |
| P3 configuration | The **Rage Hammer engraving path** is a sanctioned Destroyer variant that de-emphasizes the Hypergravity/gravity stance in favor of Rage-Hammer normal-mode burst. A sanctioned variant de-emphasizes the gravity half → hybrid is a build option, not kit identity. | **FAIL** |
| P4 assembly | The pull is intrinsic (class skill), so P4 passes — but P2/P3 already disqualify. | pass |

**Door: SUPPRESSED-not; the disqualifier is P2 (degraded-but-operable) + P3 (configurable — Rage Hammer path).** Hypergravity is a damage stance; the sanctioned engraving variant de-emphasizes it. **Key `ctrl_treatment=damage`, `ctrl_function=pull` (rider).** Matches gandalf's read (flag b): "Vortex Gravity likely fails probe 2 or 3 → damage-primary + rider."

### `di-cyclone-strike-monk-base` — VERDICT: **damage-primary + pull rider** (NOT hybrid), on the KIT-LEVEL door

| probe | reading (from tranche + DI source) | pass? |
|---|---|---|
| P1 damage-removal | Remove damage → pull-only Gather remains, a real utility role. | pass (skill-level) |
| P2 control-removal | Remove pull → still a wind-up Holy/Physical nova damage skill. Operates degraded. | **borderline→FAIL** |
| P3 configuration | **Storm Spirit essence removes the pull → DPS-only.** A sanctioned variant de-emphasizes the control half. This is the decisive FAIL — the base skill's co-equal pull+damage is REAL at SKILL level, but the KIT-level configurability door (gear-assembled essences: Storm Spirit, Driven Thunder, Frigid Cyclone) means the hybrid is a player option. | **FAIL** |
| P4 assembly | The BASE pull is intrinsic (no Legendary required) → P4 passes at base grain. | pass |

**Door: CONFIGURABLE-OUT (P3) — Storm Spirit removes the pull.** gandalf's taxonomy line grants this the one-paragraph acknowledgment: **skill-level co-equal pull+damage is REAL in canon; the hardlock fails only at kit level.** This is the genuine boundary case. Elrond keys the kit at the KIT grain (the grain the atlas records) → **`ctrl_treatment=damage`, `ctrl_function=pull` (rider)**, WITH the acknowledgment recorded that at pure-skill grain this is the closest hybrid in the genre. Matches gandalf's read (flag b): "DI base is the genuine skill-level hybrid but the kit-level configurability door holds."

## 5. Consequence for the corpus (the honesty that this preserves)

Both proposed hybrids resolve to **damage-primary + pull rider.** Therefore:
- The active corpus stays **hybrid-EMPTY** after Edition-II §10 ingestion — the T5 frontier is intact, honestly.
- No engine-hybrid is force-keyed on degraded-but-operable or configurable-out evidence.
- The pull is fully legible on both rows (via `ctrl_function=pull`), so nothing is lost — the dual character is recorded, the over-claim is refused.
- When a genuinely-hardlocked hybrid IS eventually found (a kit where removing EITHER half collapses it AND no sanctioned variant de-emphasizes either AND both are intrinsic), it keys hybrid under this same procedure — and the frontier's first real inhabitant is recorded on evidence, not on optimism.

---

**Signed:** elrond (data steward) — for a hybrid bar high enough that an empty frontier stays an honest frontier. The procedure refuses the over-claim (degraded ≠ collapsed; configurable ≠ hardlocked; assembled ≠ intrinsic) while keeping every real rider legible.
