# Pool × VFX Catalogue Mapping Audit — 2026-05-19

**Mode:** A (analytical — audit-and-refinement)
**Commissioner:** knight-rider / gandalf (F5 dispatch 2026-05-19)
**Owner:** legolas
**F3 upstream gate:** `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-19.md`
**Dispatch:** `agentic_orchestration/dispatches/2026-05-19-legolas-plus-gandalf-vs2a-F5-drift14-pool-vfx-catalogue-audit.md`
**Sources consulted:** `data/seasonal_elements/vfx_coverage_manifest.json` (156-entry manifest); `data/seasonal_elements/pool.json` (156-entry pool); `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (Step B Tier-1 VFX inventory)
**Status:** COMPLETE — Track A delivered; readiness signal for gandalf Track B at § 6

---

## § 0 — Scope summary

This is a **verification + refinement pass** on the existing 156-entry manifest at `data/seasonal_elements/vfx_coverage_manifest.json`, not a greenfield audit. The substantial 2026-05-17 implementation cascade (legolas inline annotations + gandalf cull-decisions + rocket auto-demote logic + schema) already assigned Tier A–E annotations to all 156 entries. Per F3 framework § 4.2, F5 scope is:

1. Verify all 156 tier annotations are consistent with the F3 framework Tier A–E definitions
2. Surface borderline-disputable tier cases for gandalf re-scoring adjudication
3. Annotate `canonical_pair_leak` coverage completeness (field is present; audit confirms no gaps)
4. Confirm auto-demote ground-truth: which allow-list entries carry `vfx_catalogue_mapping_clean = False` and therefore get auto-demoted at pool-load

---

## § 1 — Summary (4 sentences)

All 156 manifest entries have been verified against the F3 framework Tier A–E methodology. The manifest is structurally consistent: 86 entries are `vfx_catalogue_mapping_clean = True` (Tier A or B); 70 are `False` (Tier C, D, or E); all 21 `canonical_pair_leak = True` entries are correctly identified. Three allow-list entries (`lantern`, `torch`, `tinder`) carry `vfx_catalogue_mapping_clean = False` (Tier C) and will auto-demote at pool-load, yielding a post-demote effective allow-list of **57 entries** against the rocket math note § 2.4 target of ~55 — within acceptable variance. Six borderline cases require gandalf adjudication: `fume` (Tier-C vs Tier-E ambiguity), `miasma` (Tier-C vs Tier-E), `bone` (Tier-C vs Tier-D biological-organic), `blood` (Tier-C vs Tier-D liquid-register severity), `web` (Tier-C depth-of-VFX-analog), and `thorn` (Tier-B clean but culled-plant-anatomical; status already correct as eligible).

---

## § 2 — Catalogue coverage baseline (operational VFX catalogue state)

### § 2.1 Catalogue state at audit date (2026-05-19)

Per `cross-vendor-substrate-inventory-2026-05-16.jsonl` and F3 framework § 4.1: **no catalogue changes since 2026-05-17**. Pimen GREEN-list at 11/13 elements (unchanged). CreativeKind palette-shift coverage unchanged. Tier-2 vendors (Fellor, Frostwindz, Ansimuz, CraftPix) unchanged. The audit operates against the same catalogue state the 2026-05-17 annotations were authored against.

### § 2.2 Canonical-slot VFX coverage map

For reference: which substance-concept families the catalogue directly supports at each canonical slot:

| Canonical slot | Direct (Tier A) coverage | Palette-shift (Tier B) family |
|---|---|---|
| **fire** | Combustion-particles (ember/spark/cinder/blaze/scorch/brand/flare); Pimen fire-spell-effect-3 + CreativeKind fire-spells | Darkened-carbon variants (coal/soot/char/charcoal/pitch/tar); warm-diffuse (glow); transitional (ash/flicker); hard-sparking (flint/steam) |
| **wind** | Pimen wind VFX + CraftPix topdown-wind-lightning; covers sustained-force (gale/plume/dust) + cold-crystal (frost/hail) | Obscuring-diffuse (mist/fog/vapor/cloud/billow/draft); cold-wet (sleet); cutting-force (shear); demoted-cluster (gust) |
| **water** | Pimen magical-water-effect + CreativeKind water-spells; direct: tide/rain/ice/snow/wake/wave/brine | Flowing/surface/crystal water variants: salt/glacier/marsh/spring/stream/ripple/eddy/foam/current/slick |
| **earth** | Pimen earth-spell-effect-02 + Fellor earth-vfx + CreativeKind earth-spells; direct: stone/granite/sand/ore/iron/gold/gem/crystal | Geological-mineral spectrum: slate/basalt/limestone/marble/chalk/clay/mud + metal-family: copper/bronze/silver/lead/rust/obsidian/amber/quartz/geode; plant-family via CraftPix bamboo-wall: root/bark/wood/vine/thorn/peat/soil |

### § 2.3 Findings-blocker status

**No findings-blockers.** Pimen + CreativeKind coverage data is sufficient for all 156-entry tier determinations. The Step B Tier-1 inventory (29 substrate rows) provides comprehensive anchor evidence. No entries require Tier-2 vendor acquisition to resolve their tier — all Tier-D/E annotations are grounded in catalogue absence, and all Tier-A/B/C annotations are grounded in catalogue presence at the appropriate abstraction level.

---

## § 3 — Tier distribution and operational ground-truth

### § 3.1 Tier distribution (all 156 entries)

| Tier | Count | Definition | `vfx_catalogue_mapping_clean` |
|---|---|---|---|
| **A — Direct** | 29 | Direct vendor catalogue coverage; no modification | True |
| **B — Palette-shift** | 57 | Palette change only achievable | True |
| **C — Composite** | 41 | Palette + compositing required | False |
| **D — Custom-required** | 21 | No clean catalogue mapping; bespoke VFX needed | False |
| **E — Non-visual** | 8 | Cannot render as visual VFX | False |

**Total clean (Tier A+B):** 86 entries. **Total blocked (Tier C+D+E):** 70 entries.

### § 3.2 Auto-demote ground-truth

Pool loader auto-demote logic fires for entries where `d1_status == "allow-list"` AND `vfx_catalogue_mapping_clean == False`. Three entries qualify:

| id | primary_slot | d1_total | tier | rationale |
|---|---|---|---|---|
| `lantern` | fire | 9 | C | Object framing (carried vessel); composite fire+container required; not a substance |
| `torch` | fire | 9 | C | Object framing (handheld torch); composite fire+stick required; not a substance |
| `tinder` | fire | 8 | C | Dry-preparatory fuel; no standalone substance-VFX; composite required |

All three have Tier-C rationales grounded in object/process framing rather than substance-shape — the canonical fire-slot VFX (combustion particles, fire-spell direct) does not render "lantern," "torch," or "tinder" coherently. Auto-demote outcome for all three: `eligible`. No dispute on any of these three; Tier-C is correct.

### § 3.3 Post-auto-demote effective pool composition

| Status | Pre-demote | Post-auto-demote (at load) |
|---|---|---|
| allow-list (vfx-clean) | 60 | **57** |
| eligible (vfx-acceptable) | 50 | **53** (50 native + 3 auto-demoted) |
| quarantine (vfx-blocked) | 46 | **46** (Tier-E entries already in quarantine; no net change) |
| **Total** | **156** | **156** |

**Rocket math note § 2.4 target: ~55 post-auto-demote allow-list.** Empirical result: **57**. Delta: +2 vs target. Within acceptable variance — no adjustment required. The 2026-05-17 cull cascade + auto-demote logic yields a post-cull allow-list within 4% of target.

### § 3.4 Tier-E quarantine auto-demote

Eight Tier-E entries (`breath`, `sigh`, `whisper`, `whistle`, `howl`, `hum`, `thrum`, `exhalation`) are all in `d1_status == "quarantine"` already. The pool loader's Tier-E auto-demote-to-quarantine rule fires conservatively but produces no net status change for any of these entries. Quarantine-correct confirmed for all eight.

---

## § 4 — Per-slot verification tables

Key: **T** = True, **F** = False. Columns: `id | d1_total | d1_status | tier | clean | leak | audit_verdict | flags`

Flags: `AUTO-DEMOTE` = allow-list + clean=False (auto-demoted at load); `BORDERLINE` = surfaced for gandalf adjudication; `TIER-E-CORRECT` = auditory/non-visual, quarantine-correct; `CULLED-PLANT-ANAT` = culled per plant-anatomical cull, pool status=eligible (correct).

### § 4.1 FIRE (32 entries)

| id | d1_total | d1_status | tier | clean | leak | audit_verdict | flags |
|---|---|---|---|---|---|---|---|
| brand | 11 | allow-list | A | T | F | CONFIRMED | |
| cinder | 11 | allow-list | A | T | T | CONFIRMED | |
| magma | 11 | allow-list | A | T | T | CONFIRMED | |
| blaze | 10 | allow-list | A | T | T | CONFIRMED | |
| char | 10 | allow-list | B | T | T | CONFIRMED | |
| coal | 10 | allow-list | B | T | F | CONFIRMED | |
| ember | 10 | allow-list | A | T | T | CONFIRMED | |
| lava | 10 | allow-list | A | T | T | CONFIRMED | |
| pitch | 10 | allow-list | B | T | F | CONFIRMED | |
| scorch | 10 | allow-list | A | T | T | CONFIRMED | |
| spark | 10 | allow-list | A | T | T | CONFIRMED | |
| ash | 9 | allow-list | B | T | T | CONFIRMED | |
| charcoal | 9 | allow-list | B | T | F | CONFIRMED | |
| flint | 9 | allow-list | B | T | F | CONFIRMED | |
| lantern | 9 | allow-list | C | F | F | CONFIRMED | AUTO-DEMOTE |
| tar | 9 | allow-list | B | T | F | CONFIRMED | |
| torch | 9 | allow-list | C | F | F | CONFIRMED | AUTO-DEMOTE |
| flare | 8 | allow-list | A | T | F | CONFIRMED | |
| soot | 8 | allow-list | B | T | F | CONFIRMED | |
| tinder | 8 | allow-list | C | F | F | CONFIRMED | AUTO-DEMOTE |
| brazier | 7 | eligible | C | F | F | CONFIRMED | |
| flicker | 6 | eligible | B | T | T | CONFIRMED | |
| kindling | 6 | eligible | C | F | F | CONFIRMED | |
| oil | 6 | eligible | B | T | F | CONFIRMED | |
| smoke | 6 | eligible | B | T | T | CONFIRMED | |
| candle | 5 | eligible | C | F | F | CONFIRMED | |
| fume | 5 | eligible | C | F | F | CONFIRMED | BORDERLINE |
| glow | 5 | eligible | B | T | F | CONFIRMED | |
| hearth | 5 | eligible | C | F | F | CONFIRMED | |
| ignition | 5 | eligible | C | F | T | CONFIRMED | |
| steam | 5 | eligible | B | T | F | CONFIRMED | |
| wax | 4 | quarantine | C | F | F | CONFIRMED | |

**Fire slot summary:** 20 allow-list (17 confirmed vfx-clean; 3 AUTO-DEMOTE); 11 eligible; 1 quarantine. No D or E entries. 12 `canonical_pair_leak = True` entries (all core-combustion vocabulary: ember/spark/cinder/lava/magma/blaze/char/scorch/ash/flicker/smoke/ignition). Note: `smoke` is eligible (d1=6) — pair-leak flag correct; already not on allow-list.

### § 4.2 WIND (38 entries)

| id | d1_total | d1_status | tier | clean | leak | audit_verdict | flags |
|---|---|---|---|---|---|---|---|
| frost | 11 | allow-list | A | T | F | CONFIRMED | |
| hail | 11 | allow-list | A | T | F | CONFIRMED | |
| hurricane | 11 | eligible | C | F | T | CONFIRMED | |
| rime | 11 | eligible | B | T | F | CONFIRMED | |
| cyclone | 10 | eligible | C | F | T | CONFIRMED | |
| gale | 10 | allow-list | A | T | T | CONFIRMED | |
| shear | 10 | eligible | B | T | F | CONFIRMED | |
| tempest | 10 | eligible | C | F | T | CONFIRMED | |
| gust | 9 | eligible | B | T | T | CONFIRMED | |
| howl | 9 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| miasma | 9 | eligible | C | F | F | CONFIRMED | BORDERLINE |
| pall | 9 | eligible | C | F | F | CONFIRMED | |
| sleet | 9 | allow-list | B | T | F | CONFIRMED | |
| squall | 9 | eligible | C | F | T | CONFIRMED | |
| typhoon | 9 | eligible | C | F | T | CONFIRMED | |
| billow | 8 | eligible | B | T | F | CONFIRMED | |
| dust | 8 | allow-list | A | T | F | CONFIRMED | |
| plume | 8 | allow-list | A | T | F | CONFIRMED | |
| spore | 7 | eligible | C | F | F | CONFIRMED | |
| cloud | 5 | allow-list | B | T | F | CONFIRMED | |
| draft | 5 | eligible | B | T | F | CONFIRMED | |
| fog | 5 | eligible | B | T | F | CONFIRMED | |
| mist | 5 | eligible | B | T | F | CONFIRMED | |
| vapor | 5 | eligible | B | T | F | CONFIRMED | |
| veil | 5 | eligible | C | F | F | CONFIRMED | |
| feather | 4 | quarantine | C | F | F | CONFIRMED | |
| pollen | 4 | quarantine | C | F | F | CONFIRMED | |
| seed | 4 | quarantine | C | F | F | CONFIRMED | |
| gauze | 3 | quarantine | C | F | F | CONFIRMED | |
| silk | 3 | quarantine | C | F | F | CONFIRMED | |
| breath | 2 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| gossamer | 2 | quarantine | C | F | F | CONFIRMED | |
| exhalation | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| hum | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| sigh | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| thrum | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| whisper | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |
| whistle | 0 | quarantine | E | F | F | CONFIRMED | TIER-E-CORRECT |

**Wind slot summary:** 7 allow-list (all vfx-clean; 0 auto-demote); 15 eligible; 16 quarantine (8 Tier-E auditory + 8 Tier-C/D biological/textural). No auto-demote fires in wind slot. Storm-cluster cull (`hurricane/cyclone/tempest/typhoon/squall`) confirmed at eligible; all 5 carry `canonical_pair_leak = True`. 1 `canonical_pair_leak` in allow-list: `gale` (cluster representative KEPT per drift-14-wind-storm-cluster decision). Wind allow-list is notably thin (7 entries) relative to other slots; this reflects the storm-cluster cull + auditory cull landing correctly.

### § 4.3 WATER (33 entries)

| id | d1_total | d1_status | tier | clean | leak | audit_verdict | flags |
|---|---|---|---|---|---|---|---|
| blood | 11 | eligible | C | F | F | CONFIRMED | BORDERLINE |
| brine | 11 | allow-list | A | T | F | CONFIRMED | |
| glacier | 11 | allow-list | B | T | F | CONFIRMED | |
| ice | 11 | allow-list | A | T | F | CONFIRMED | |
| mercury | 11 | eligible | B | T | F | CONFIRMED | |
| salt | 10 | allow-list | B | T | F | CONFIRMED | |
| tide | 10 | allow-list | A | T | T | CONFIRMED | |
| wake | 10 | allow-list | A | T | F | CONFIRMED | |
| wave | 10 | allow-list | A | T | F | CONFIRMED | |
| rain | 9 | allow-list | A | T | F | CONFIRMED | |
| slick | 9 | allow-list | B | T | F | CONFIRMED | |
| marsh | 8 | allow-list | B | T | F | CONFIRMED | |
| pearl | 8 | quarantine | D | F | F | CONFIRMED | |
| snow | 8 | allow-list | A | T | F | CONFIRMED | |
| foam | 7 | eligible | B | T | F | CONFIRMED | |
| current | 5 | eligible | B | T | F | CONFIRMED | |
| droplet | 5 | eligible | C | F | F | CONFIRMED | |
| eddy | 5 | eligible | B | T | F | CONFIRMED | |
| ripple | 5 | eligible | B | T | F | CONFIRMED | |
| spring | 5 | eligible | B | T | F | CONFIRMED | |
| stream | 5 | eligible | B | T | F | CONFIRMED | |
| bubble | 3 | quarantine | C | F | F | CONFIRMED | |
| dew | 3 | quarantine | C | F | F | CONFIRMED | |
| honey | 3 | quarantine | D | F | F | CONFIRMED | |
| jelly | 3 | quarantine | D | F | F | CONFIRMED | |
| milk | 3 | quarantine | D | F | F | CONFIRMED | |
| nectar | 3 | quarantine | D | F | F | CONFIRMED | |
| sap | 3 | quarantine | C | F | F | CONFIRMED | |
| slush | 3 | quarantine | C | F | F | CONFIRMED | |
| sweat | 3 | quarantine | D | F | F | CONFIRMED | |
| lather | 2 | quarantine | D | F | F | CONFIRMED | |
| suds | 2 | quarantine | D | F | F | CONFIRMED | |
| tear | 2 | quarantine | D | F | F | CONFIRMED | |

**Water slot summary:** 11 allow-list (all vfx-clean; 0 auto-demote); 8 eligible; 14 quarantine (9 Tier-D domestic/biological + 5 Tier-C composite-specific). Only 1 `canonical_pair_leak = True` entry (`tide`) — water slot has the lowest pair-leak density (1/33 = 3%). Note: `mercury` is Tier-B vfx-clean but eligible (cultural-register concern per drift-14-alternative-liquid cull overrides clean VFX — correctly not allow-list); `blood` is Tier-C borderline (flagged below).

### § 4.4 EARTH (53 entries)

| id | d1_total | d1_status | tier | clean | leak | audit_verdict | flags |
|---|---|---|---|---|---|---|---|
| bone | 11 | eligible | C | F | F | CONFIRMED | BORDERLINE |
| chitin | 11 | quarantine | D | F | F | CONFIRMED | |
| claw | 11 | quarantine | D | F | F | CONFIRMED | |
| crystal | 11 | allow-list | A | T | F | CONFIRMED | |
| gem | 11 | allow-list | A | T | F | CONFIRMED | |
| gold | 11 | allow-list | A | T | F | CONFIRMED | |
| granite | 11 | allow-list | A | T | F | CONFIRMED | |
| horn | 11 | quarantine | D | F | F | CONFIRMED | |
| iron | 11 | allow-list | A | T | F | CONFIRMED | |
| obsidian | 11 | allow-list | B | T | F | CONFIRMED | |
| ore | 11 | allow-list | A | T | F | CONFIRMED | |
| scale | 11 | quarantine | D | F | F | CONFIRMED | |
| silver | 11 | allow-list | B | T | F | CONFIRMED | |
| stone | 11 | allow-list | A | T | T | CONFIRMED | |
| thorn | 11 | eligible | B | T | F | CONFIRMED | CULLED-PLANT-ANAT |
| throne | 11 | quarantine | D | F | F | CONFIRMED | |
| tooth | 11 | quarantine | D | F | F | CONFIRMED | |
| amber | 10 | allow-list | B | T | F | CONFIRMED | |
| basalt | 10 | allow-list | B | T | F | CONFIRMED | |
| bronze | 10 | allow-list | B | T | F | CONFIRMED | |
| copper | 10 | allow-list | B | T | F | CONFIRMED | |
| marble | 10 | allow-list | B | T | F | CONFIRMED | |
| quartz | 10 | allow-list | B | T | F | CONFIRMED | |
| slate | 10 | allow-list | B | T | F | CONFIRMED | |
| clay | 9 | allow-list | B | T | F | CONFIRMED | |
| geode | 9 | allow-list | B | T | F | CONFIRMED | |
| lead | 9 | allow-list | B | T | F | CONFIRMED | |
| marrow | 9 | quarantine | D | F | F | CONFIRMED | |
| sand | 9 | allow-list | A | T | F | CONFIRMED | |
| husk | 8 | quarantine | D | F | F | CONFIRMED | |
| limestone | 8 | allow-list | B | T | F | CONFIRMED | |
| rust | 8 | allow-list | B | T | F | CONFIRMED | |
| shell | 8 | quarantine | D | F | F | CONFIRMED | |
| bark | 7 | eligible | B | T | F | CONFIRMED | |
| peat | 7 | eligible | B | T | F | CONFIRMED | |
| root | 7 | eligible | B | T | F | CONFIRMED | |
| web | 7 | eligible | C | F | F | CONFIRMED | BORDERLINE |
| wood | 7 | eligible | B | T | F | CONFIRMED | |
| vine | 6 | eligible | B | T | F | CONFIRMED | |
| chalk | 5 | eligible | B | T | F | CONFIRMED | |
| mold | 5 | eligible | C | F | F | CONFIRMED | |
| mud | 5 | eligible | B | T | F | CONFIRMED | |
| rot | 5 | eligible | C | F | F | CONFIRMED | |
| soil | 5 | eligible | B | T | F | CONFIRMED | |
| gravel | 4 | quarantine | C | F | F | CONFIRMED | |
| leaf | 4 | quarantine | C | F | F | CONFIRMED | |
| lichen | 4 | quarantine | C | F | F | CONFIRMED | |
| moss | 4 | quarantine | C | F | F | CONFIRMED | |
| pebble | 4 | quarantine | C | F | F | CONFIRMED | |
| silt | 4 | quarantine | C | F | F | CONFIRMED | |
| threshold | 4 | quarantine | D | F | F | CONFIRMED | |
| flower | 3 | quarantine | D | F | F | CONFIRMED | |
| petal | 3 | quarantine | D | F | F | CONFIRMED | |

**Earth slot summary:** 22 allow-list (all vfx-clean; 0 auto-demote); 13 eligible; 18 quarantine (12 Tier-D biological-organic/conceptual + 6 Tier-C quarantine). Only 1 `canonical_pair_leak = True` entry (`stone`) — earth slot has lowest pair-leak count in absolute terms. The biological-organic cull cluster (`chitin/claw/horn/scale/shell/tooth/marrow/husk/bone`) is correctly distributed: most are Tier-D quarantine; `bone` alone is Tier-C eligible (borderline — flagged below). Earth slot has the richest mineral-geological vocabulary and the deepest allow-list (22 entries, 39% of earth pool).

---

## § 5 — Borderline cases for gandalf adjudication

Six entries require gandalf Track B re-scoring adjudication. None of these change the auto-demote outcome (all are in `eligible` or `quarantine` already, not `allow-list`). The question in each case is whether the tier assignment should shift — which affects the `vfx_catalogue_mapping_clean` boolean and the `d1_status` floor, but not the current allow-list/eligible/quarantine binary (since all six are already below allow-list).

### § 5.1 `fume` — Tier-C vs Tier-E question

**Current:** Tier-C, `vfx_catalogue_mapping_clean = False`, `d1_status = eligible`
**Rationale filed:** "invisible-toxic gas; no visual register"
**Audit read:** The rationale text leans toward Tier-E ("no visual register") but the tier is assigned as C. This is internally inconsistent. `fume` is fire-primary with tags `[toxic, rising, invisible]`. Two reads are defensible:
- **Tier-C (current):** Fume CAN be rendered via smoke-VFX + color-tint (greenish-grey particle for toxic-fire-gas); Fellor smoke-vfx or Ansimuz explosion-smoke are viable composite substrates; renders incoherently against plain fire-VFX but achievable with compositing.
- **Tier-E (alternative):** `invisible` is in the entry's own tags; the word's primary semantic register is the toxic-gas-you-can't-see quality; rendering as visible-particle would misrepresent the concept.

**Legolas read:** Tier-C is more defensible. `fume` in fantasy-combat contexts renders as a visible gas-cloud effect (analogous to poison-cloud); the `invisible` tag reflects mundane chemistry but the combat-register is visual. Tier-E is reserved for fundamentally auditory/textural entries where no combat-visual rendering makes sense. However, the rationale text should be corrected to align with the Tier-C assignment ("composite smoke-particle VFX achievable via palette-shift on Fellor smoke-vfx" rather than "no visual register").

**Route to gandalf:** Tier-C confirmed or Tier-E upgrade — whichever, rationale text needs correction.

### § 5.2 `miasma` — Tier-C vs Tier-E question

**Current:** Tier-C, `vfx_catalogue_mapping_clean = False`, `d1_status = eligible`
**Rationale filed:** "toxic-choking-atmospheric; composite VFX required; vocab-obscure"
**Audit read:** `miasma` is wind-primary with tags implying atmospheric toxic cloud. Unlike `fume`, `miasma` has a clear fantasy visual register (poisonous cloud of air; visible miasmatic fog). Fellor smoke-vfx (10 animations, multi-phase) + Ansimuz Vapor/Smoke Column provide composite substrates. Tier-C is correct. No Tier-E argument is supportable — miasma is visually representable as a colored atmospheric cloud even if the word's etymology is obscure. The `vocab-obscure` flag is a D1 concern (already in eligible d1=9 via manual override for vocab-obscure), not a VFX-mapping concern.

**Route to gandalf:** Tier-C confirmed; no change recommended. Noting only for completeness as the rationale's "vocab-obscure" tag could be misread as a VFX-mapping concern.

### § 5.3 `bone` — Tier-C vs Tier-D biological-organic question

**Current:** Tier-C, `vfx_catalogue_mapping_clean = False`, `d1_status = eligible`, rationale: "biological-organic renders distinct from mineral earth; Tier C borderline"
**Audit read:** `bone` is the hardest biological-organic case. The manifest explicitly notes "Tier C borderline." Under Tier-C, the claim is: bone CAN be composited from earth-VFX with pale-white palette-shift + hard-angular fragment modification. Under Tier-D, the claim is: bone's visual register (white-calcified biological fragments) is so distinct from mineral-earth (grey-brown stone particles) that rendering bone-VFX as modified earth-VFX would produce the same cognitive dissonance as throne-VFX (the motivating Drift-14 example).

**Legolas read:** This is a genuine C-vs-D borderline. `bone` as a combat substance (bone-shards, bone-armor, bone-fragments flying) IS representable in an ARPG register — the Frostwindz Necromancer pack ships bone-raise-undead VFX that reads as pale-white fragments. However, this is a **separate substrate** (death-necrotic) not the earth-mineral substrate. The question is whether a season selecting `bone` as an earth-slot element would render coherently via earth-VFX + palette-shift, or whether it requires commission of a distinct VFX. The `biological-organic` sub-category flag applies. The existing Tier-C annotation is defensible if gandalf adjudicates that earth-VFX+white-palette reads as bone in combat context; Tier-D is defensible if the white-fragment rendering requires the death-necrotic substrate.

**Route to gandalf:** Adjudicate: would "bone-strike with white-shifted earth-particle VFX" produce player-visible cognitive dissonance? If yes → Tier-D (no change to auto-demote outcome; already eligible). If no → Tier-C confirmed.

### § 5.4 `blood` — Tier-C vs Tier-D liquid-register severity question

**Current:** Tier-C, `vfx_catalogue_mapping_clean = False`, `d1_status = eligible`, rationale: "red-palette creates cultural-register mismatch; Tier C; demoted to eligible"
**Audit read:** `blood` is water-primary. The existing rationale grounds the demotion in "cultural-register mismatch" (red-liquid vs canonical blue/cyan water-VFX). The question is whether this mismatch is a Tier-C (achievable with palette-shift despite mismatch) or Tier-D (palette-shift is technically possible but the register mismatch is severe enough to produce cognitive dissonance). CodeManu `blood-effects-vol1` ships 180 blood-VFX animations — so a dedicated blood-VFX DOES exist in the catalogue. If that pack were acquired, `blood` would be Tier-A direct. The current Tier-C annotation assumes we don't have that pack licensed; the question is whether water-VFX + red-palette achieves acceptable rendering.

**Legolas read:** Tier-C is correct under the current catalogue state (CodeManu blood-effects-vol1 not yet acquired). The red-palette issue is real but water-VFX + saturated-red palette produces a blood-like liquid-particle effect that is commercially standard in ARPG combat. However: the `blood` cull rationale from 2026-05-17 emphasizes the "cultural-register mismatch" as the demotion reason, which suggests the motivation was design-level (not wanting blood-themed seasons in a certain direction) rather than VFX-technical. That's a gandalf-track adjudication, not a VFX-mapping question.

**Route to gandalf:** Two-question adjudication: (a) confirm Tier-C is correct for VFX-mapping purposes (achievable with palette-shift even if not catalog-direct); (b) confirm eligible status is the correct permanent home for design reasons (blood-themed season decision), not just VFX-mapping reasons.

### § 5.5 `web` — Tier-C depth-of-VFX-analog question

**Current:** Tier-C, `vfx_catalogue_mapping_clean = False`, `d1_status = eligible`, rationale: "fine-catching-suspended; composite VFX required; flex earth+wind"
**Audit read:** `web` (spider-web) is earth-primary. The question is whether "composite VFX required" achieves a coherent rendering. The earth-VFX catalogue (stone particles, mineral debris) has no natural analog for spider-web's fine-linear-strand structure. A "web" combat-VFX would require string-particle compositing distinctly different from stone-or-sand particle animation. This is Tier-C at the lower end — possible but requires substantial compositing work, not just palette adjustment. No sub-category flag is applied in the manifest; this could be tagged `biological-organic` (spider anatomy) or left as general-composite.

**Legolas read:** Tier-C is defensible but near the C/D boundary. The distinguishing factor: "composite VFX required" for web means adding a distinct visual motif (strands/threads), not just adjusting particle color. For reference, Tier-C threshold per F3 framework is "palette + minor compositing (e.g., adding sparkle overlay; texture-replacement)." Web-strand rendering goes beyond sparkle overlay — it's a structural motif change. Borderline.

**Route to gandalf:** Adjudicate whether web's rendering requirement (strand-structure, not particle) crosses from Tier-C into Tier-D. No auto-demote impact either way (already eligible).

### § 5.6 `thorn` — Culled status verification (no tier change needed)

**Current:** Tier-B, `vfx_catalogue_mapping_clean = True`, `d1_status = eligible`, rationale: "CULLED drift-14-plant-anatomical; CraftPix bamboo-wall covers plant register; Tier B for wood-nature coverage but demoted to eligible per plant-anatomical cull"
**Audit read:** `thorn` has Tier-B `vfx_catalogue_mapping_clean = True` — meaning the VFX IS achievable via palette-shift on CraftPix bamboo-wall/nature VFX. The `eligible` status does NOT come from the VFX-mapping tier but from the plant-anatomical cull decision. This is an unusual case: VFX-clean=True but not allow-list. This is correct behavior — the F3 framework allows eligible entries to be VFX-clean (the `vfx-acceptable` category covers `d1_total >= 5` AND `vfx_catalogue_mapping_clean = True`). `thorn` sits at d1=11, eligible (culled), Tier-B, clean=True — it is a `vfx-acceptable` entry per F3 § 3.3 definition.

**Route to gandalf:** No tier change needed. Verification note: `thorn`'s `d1_status = eligible` is the result of the plant-anatomical cull, not the VFX-mapping gate. The auto-demote logic does NOT fire (auto-demote requires `d1_status == allow-list AND clean == False`; thorn is eligible+clean=True). Pool loader behavior is correct as-is.

---

## § 6 — Canonical pair-leak coverage assessment

The `canonical_pair_leak` boolean is populated on all 156 manifest entries. Coverage is complete.

**Distribution: 21 entries with `canonical_pair_leak = True`** (13.5% of pool).

By slot:
- Fire: 12/32 (37.5%) — dominated by core-combustion vocabulary: ember/spark/cinder/lava/magma/blaze/char/scorch/ash + eligible (flicker/smoke/ignition)
- Wind: 7/38 (18.4%) — storm-cluster group (hurricane/cyclone/tempest/typhoon/squall) + gale (allow-list representative) + gust (eligible)
- Water: 1/33 (3.0%) — tide only
- Earth: 1/53 (1.9%) — stone only

**Interpretation:** Fire has the highest canonical_pair_leak density because fire-vocabulary is inherently substance-coherent with fire-VFX — the words ARE the canonical element. Wind's 7-entry cluster is the storm-weather sub-register the 2026-05-17 cull addressed. Water and earth entries have been effectively de-biased by the cull cascade (only canonical anchors `tide` and `stone` remain at True). The fire density (12 entries) is not a problem operationally because those entries are not falsely on allow-list from a VFX-mapping perspective — they ARE coherent with fire-VFX. The pair-leak flag is informational for cluster-collapse logic (Track 3, deferred post-VS2a), not an automatic demotion trigger.

---

## § 7 — Reclassification summary

**No reclassifications recommended.** All 156 existing tier annotations are confirmed as correct or confirmed as valid within their tolerance range. The manifest as filed 2026-05-17 is structurally sound.

**Rationale text corrections recommended (not tier changes):**
- `fume`: rationale says "no visual register" but tier is C — rationale should be corrected to acknowledge composite achievability ("grey-green smoke-particle composite achievable via Fellor smoke-vfx palette-shift; rationale note: fire-primary, toxic-atmospheric rendering is combat-viable").

**Borderline cases for gandalf adjudication (tier MAY shift; pool status does NOT shift — all already below allow-list):**
1. `fume` — Tier-C confirmed but rationale text correction needed; OR upgrade to Tier-E if gandalf reads `invisible` tag as definitional
2. `bone` — Tier-C confirmed or Tier-D upgrade; biological-organic register question
3. `blood` — Tier-C confirmed; design-intent question for gandalf about `eligible` permanence
4. `web` — Tier-C confirmed or Tier-D upgrade; strand-vs-particle compositing depth question
5. `miasma` — Tier-C confirmed; no change recommended; noting for completeness

None of the borderline cases change the **auto-demote outcome** (all are already below allow-list). The only potential auto-demote impact would be if a currently-non-allow-list Tier-C entry were upgraded to Tier-A or Tier-B AND its d1_total were ≥ 8 — but none of the borderline cases are upgrade candidates toward vfx-clean status.

---

## § 8 — Readiness signal for gandalf Track B re-scoring pass

**Track A is COMPLETE.** Manifest verified. 156/156 entries covered. Auto-demote ground-truth confirmed (3 entries: lantern/torch/tinder). Canonical pair-leak coverage complete. Effective allow-list post-demote: 57 entries (target ~55; +2 variance acceptable).

**gandalf Track B scope (per F3 § 5; revised per F5 confirmation):**

1. **Pass 1 — Auto-demote verification:** Confirm the 3 auto-demote entries (`lantern`, `torch`, `tinder`) are acceptable at `eligible` status post-demote. No re-annotation needed; these are confirmed Tier-C.

2. **Pass 2 — Borderline adjudication:** Adjudicate 4 genuine borderline cases:
   - `fume` (Tier-C correct but rationale text fix needed; or Tier-E if gandalf reads `invisible` as definitional)
   - `bone` (Tier-C vs Tier-D biological-organic; VFX register question)
   - `blood` (Tier-C vs Tier-D; design-intent permanence question for eligible status)
   - `web` (Tier-C vs Tier-D; strand-structure compositing depth question)

3. **Pass 3 — Culled-pool summary:** Per F3 § 5.3, if material changes land (i.e., any borderline case shifts from Tier-C to Tier-D and the entry currently has `vfx_catalogue_mapping_clean = False` — no change in auto-demote because all are already below allow-list), document in `canonical/story/pool-vfx-mapping-culled-2026-05-19.md`. If no material changes, the 2026-05-17 cull-decisions doc remains the canonical reference.

**gandalf estimated effort: 2–3h.** The 156-entry manifest is verified. Track B is adjudication of 4–5 borderline cases, not a full re-scoring pass.

**Tag fire: `vs2a/v0.10-drift14-audit-complete` — ready to fire when both Track A (this doc) + Track B (gandalf re-scoring pass) are complete.**

---

## § 9 — Source list

| Source | Path | Role |
|---|---|---|
| F3 framework (F5 commission criteria) | `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-19.md` | Tier A–E definitions; audit methodology |
| F5 dispatch | `agentic_orchestration/dispatches/2026-05-19-legolas-plus-gandalf-vs2a-F5-drift14-pool-vfx-catalogue-audit.md` | Commission scope + acceptance criteria |
| VFX coverage manifest | `data/seasonal_elements/vfx_coverage_manifest.json` (reincarnated-engine repo) | 156-entry manifest being audited |
| Pool data | `data/seasonal_elements/pool.json` (reincarnated-engine repo) | d1_status + d1_total per entry |
| Tier-1 VFX inventory | `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` | Catalogue coverage evidence (29 substrate rows) |
| Drift-14 entry | `canonical/story/drift-audit.md` § Drift-14 | Problem statement + closure mechanism |
| Cull decisions | `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` | 2026-05-17 Track B decisions; baseline for audit |

---

## § 10 — Completion record

**Track A complete.** Filed at `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-19.md`.

- 156/156 entries verified
- 0 reclassifications (tier annotations confirmed as-is)
- 3 auto-demote confirmations (lantern/torch/tinder → eligible at load)
- 5 borderline cases surfaced for gandalf Track B (fume/bone/blood/web/miasma)
- 21/21 `canonical_pair_leak` entries confirmed; coverage complete
- Post-auto-demote allow-list: 57 (target ~55; +2 acceptable)
- No findings-blockers; catalogue data sufficient
- No reclassification surface requiring Tier-2 vendor acquisition routing

*Filed 2026-05-19 by legolas under autonomous-operation authority (VS2a hive-mind protocol § 4.0). F5 Track A deliverable. Readiness signal for gandalf Track B re-scoring pass issued at § 8.*
