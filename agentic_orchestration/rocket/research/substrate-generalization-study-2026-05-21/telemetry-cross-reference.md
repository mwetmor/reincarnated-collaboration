# Track B — Telemetry Cross-Reference

**Date:** 2026-05-21
**Author:** rocket

---

## B.1 Telemetry sources consulted

| Source | Path | Coverage |
|---|---|---|
| Main telemetry DB | `/Users/admin/Games/reincarnated-engine/data/telemetry.db` | 39 seasons (fire/water/earth/wind/physical only) |
| P2 diagnostic regen output | `/Users/admin/Games/reincarnated-engine/output/p2-fresh-diagnostic-regen-2026-05-19/` | season_100005, all 7 substrates present |
| R1 kit-redesign queue | `canonical/story/r1-kit-redesign-queue-2026-05-19.md` | 51-class catalogue, shadow/holy/lightning explicit entries |

---

## B.2 Main telemetry DB — structure and element coverage

The `class_balance_results` table contains per-tier win rates (swarm/magic/elite/mini_boss/boss) for **104 class-season pairs** across **14 seasons** with schema versions 2.10-2.13.

**Element coverage in per-tier data:**

| Element | N class-season pairs | Boss WR mean | Boss WR zero % | Pattern-A % |
|---|---|---|---|---|
| fire | 24 | 0.385 | 25% | 25% |
| water | 20 | 0.448 | 15% | 15% |
| earth | 20 | 0.242 | 40% | 40% |
| wind | 20 | 0.320 | 40% | 40% |
| physical | 20 | 0.000 | 100% | 100% |
| **lightning** | **0** | **N/A** | **N/A** | **N/A** |
| **holy** | **0** | **N/A** | **N/A** | **N/A** |
| **shadow** | **0** | **N/A** | **N/A** | **N/A** |

Lightning, holy, and shadow have zero representation in the main telemetry DB's per-tier balance data. These substrates were not in the canonical 5-element rotating generation set prior to P2.

**Calibration note:** All historical per-tier data in the main telemetry DB was generated under pre-disposition-3 calibration (the older aggregate-WR convergence gate with different encounter parameters). This calibration is materially different from P2's disposition-3 (boss_HP × 0.40, armor × 0.45, swarm_HP × 3.5, boss_timeout=240s, mini_boss_timeout=150s). Direct numerical comparison of boss WR values between historical and P2 is NOT valid without controlling for calibration.

---

## B.3 Calibration gap significance

The telemetry gap between historical (pre-disposition-3) and P2 (disposition-3) is load-bearing for interpreting the Track B findings.

**Historical data (pre-disposition-3):**
- Best seasons show fire/water achieving boss_wr ≈ 0.4-1.0 (season_099001)
- Pattern-A rate varied: fire 25%, water 15%, earth 40%, wind 40%
- Physical: 100% Pattern-A throughout (structural; no boss kills in 20 class-season pairs)

**P2 season_100005 (disposition-3):**
- ALL classes across ALL 7 substrates: boss_wr = 0.0
- Pattern-A rate: 100% regardless of substrate, kit size, or element

The change from ~60% kit-acceptable in best historical seasons to 0% under disposition-3 is explained by the encounter calibration change (harder bosses + per-tier WR gate vs old aggregate-WR gate), NOT by substrate-specific pathology emerging for shadow/lightning/holy.

---

## B.4 R1 kit-redesign queue cross-reference

The `canonical/story/r1-kit-redesign-queue-2026-05-19.md` documents 51-class catalogue analysis from R1 sprint v2. Shadow and holy appear explicitly in the modifier-saturation table:

- `class_0018` (shadow_mage): modifier=4.0, WR=0.0 across ALL tiers — "totally broken kit"
- `class_0045` (shadow_mage): modifier=4.0, same
- `class_0033` (holy_caster): modifier=1.43, mini_boss passes but boss=0.0
- `class_0044` (holy_caster): similar
- `class_0060` (holy_controller): modifier=4.0, boss=0.0
- `class_0016` (lightning_mage): range_profile="close", 5 melee-range skills — archetypal mismatch

This corroborates that shadow and holy pathology was visible in the pre-P2 catalogue. However, the pathology was ALSO present for fire (class_0002: fire_mage with boss_wr=0.0), water, earth, and wind in the P2 season_100005 data. The shadow/holy entries are not more pathological than the canonical-four on a kit-architectural basis — they appear in the modifier-saturation table because the older catalogue had specific poorly-composed instances, not because shadow/holy substrate systematically generates worse kits.

---

## B.5 Lightning-specific note

Lightning's `chain_lightning` geometry (preferred per substrate_identity.yaml) is the one geometry in the P2 kit analysis that shows multi-target hit capability on a boss entity (each chain hop could hit the same boss multiple times depending on sim implementation). class_0006 (lightning_mage) in P2 has 4 chain_lightning skills — the highest burst potential among the 7 substrates in that season. Yet boss_wr=0.0 for lightning_mage as well. This is consistent with the P2 finding that the pathology is shared.

---

## B.6 Track B verdict

Track B confirms: the pathology is present for shadow and holy even in the pre-P2 catalogue. Track B cannot produce calibration-controlled comparisons between shadow/lightning/holy vs canonical-four because those substrates were never in the same generation run under the same calibration. The P2 data provides the only cross-substrate, same-calibration snapshot, and it shows complete boss-kill collapse for all 7 substrates simultaneously.
