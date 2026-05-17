#!/usr/bin/env python3
"""
Build the VS2a Pimen subset manifest.

Consumes:
    agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl

Produces:
    agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl

Subset selection follows the gandalf 8-pack design-ordering from
`canonical/story/vs2a-vfx-scene-needs.md` § 3.3 with elrond-side cost-optimization:

  1. mega-pack-elemental-spell-effects (bundle: closes fire/water/earth/wind/thunder/holy/dark/ice in one purchase at $12.75 — supersedes individual purchase of element-spell-effect-3 packs #1-#4 in gandalf ordering)
  2. earth-spell-effect-03::enemy-elemental (bundled split row — Earth Elemental sprite for enemy embodiment trial)
  3. battle-vfx-hit-spark ($4.25 — Slot C physical impact)
  4. battle-vfx-projectile ($4.25 — Slot B physical projectile + Slot C impact backup)
  5. pixel-battle-effects (CC-BY $0 — fallback physical-slash + hit-effect; FLAG: CC-BY attribution risk per Gap G4)
  6. buff-n-debuff-vfx-pack-01 ($2.55 — Slot D status-apply + Slot E status-ambient)
  7. buff-n-debuff-vfx-pack-02 ($2.55 — Slot D status-apply + Slot E status-ambient, distinct visual register)

Each row in the manifest represents a (pack × substrate_tag × slot) assignment.
A single pack may produce multiple manifest rows when its animation set spans
multiple slots (e.g., fire-spell-effect-3 contributes to A, B, C, D, E).

Schema per row (drax-consumable; references pack by `source_asset_id` =
pack_slug used by `scripts/pimen-ingest/`):

    {
      "asset_id": "<pack_slug>.<substrate_tag>.<slot>",  # composite key
      "pack_slug": "<source_asset_id>",                  # drax ingest key
      "vendor": "pimen",
      "substrate_tag": "<element>-<slot-suffix>",
      "slot": "A" | "B" | "C" | "D" | "E" | "F",
      "encounter_compatibility": [...],
      "attribution_class": "commercial-license" | "cc-by" | "cc-0",
      "pack_origin": "pimen-9" | "pimen-step-b" | "pimen-bundle-mega-01",
      "animations_in_pack_for_slot": [...],
      "render_notes": "<drax § 2 layering / sub-container hint>",
      "spec_ref": "vs2a-vfx-scene-needs.md § <ref>",
      "source_url": "...",
      "cost_usd_attributed": <float>,  # bundle cost amortized OR pack cost
      "curated_row_ref": "pimen-catalogue-curated-2026-05-16.jsonl::<source_asset_id>"
    }

This manifest is the INPUT to drax's VS2a first VFX integration (4-step chain
step 3). Drax's existing ingest pipeline (`scripts/pimen-ingest/`) processes
each `pack_slug` independently; this manifest tells drax *which packs to
ingest* and *what substrate-tag × slot each pack covers*.
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

CURATED_PATH = Path(
    "/Users/admin/Games/reincarnated-collaboration/"
    "agentic_orchestration/research/curated/"
    "pimen-catalogue-curated-2026-05-16.jsonl"
)
OUT_PATH = Path(
    "/Users/admin/Games/reincarnated-collaboration/"
    "agentic_orchestration/research/curated/"
    "pimen-subset-vs2a-2026-05-17.jsonl"
)

# Encounter-type compatibility from spec § 1.2 — derived per substrate-tag
# Spec § 1.2 encounter types: swarm / trash / magic / pack / elite / mini-boss / boss
ALL_ENCOUNTERS = ["swarm", "trash", "magic", "pack", "elite", "mini-boss", "boss"]
COMBAT_ENCOUNTERS = ["trash", "magic", "pack", "elite", "mini-boss", "boss"]  # swarm = pack-rendering subset

# --- Pack-level VS2a coverage map ---
# Each entry describes a curated pack's substrate-tag × slot deployment for
# VS2a. The map below is the operational subset selection (elrond curation
# layer on top of gandalf design ordering).

# Element-pack template — element-spell-effect-3 packs contribute to Slots A/B/C
# (per Pimen's "Spell Effect 03" structure: cast-charge startup frames +
# projectile/beam mid-frames + impact peak frames). The buff/debuff packs cover
# Slots D/E separately.

ELEMENT_PACK_VS2A_DEPLOY = {
    # Fire — fire-spell-effect-3 (paid, bundled via mega-pack-01)
    "fire-spell-effect-3": {
        "element": "fire",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,  # 12.75 / 8 element packs in bundle
        "slots": {
            "A": {"substrate_tag": "fire-cast-charge",
                  "animations_in_pack_for_slot": [
                      "Fire Shield (9 startup frames)",
                      "Fire Combo 3-hit (startup frames per hit)"],
                  "render_notes": "Loop startup frames behind caster (particlesUnder). Procedural fallback OK per drax § 2.2 Slot A."},
            "B": {"substrate_tag": "fire-projectile",
                  "animations_in_pack_for_slot": [
                      "Fire Beam (10f loop)",
                      "Mini Fireball (16x16 sustained)"],
                  "render_notes": "particlesMid layer; sprite-track from caster to target per drax § 2.2 Slot B."},
            "C": {"substrate_tag": "fire-impact",
                  "animations_in_pack_for_slot": [
                      "Fire Bite (17f peak at frame 1-2)",
                      "Fire Claw (9f)",
                      "Hit Effects x4 (~5f each)"],
                  "render_notes": "particlesOver at peak frame; verify frame-1-peak discipline per drax § 2.2 Slot C."},
            # D/E covered separately by buff/debuff packs; fire DoT ambient
            # would need buff-pack burn-aura or fire-spell-effect aura subset.
        }
    },
    "water-spell-effect-03": {
        "element": "water",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "water-cast-charge",
                  "animations_in_pack_for_slot": ["spell-startup-subset"],
                  "render_notes": "Loop startup frames behind caster. Procedural fallback OK."},
            "B": {"substrate_tag": "water-projectile",
                  "animations_in_pack_for_slot": ["water-spell-projectile-subset"],
                  "render_notes": "particlesMid; sprite-track caster-to-target."},
            "C": {"substrate_tag": "water-impact",
                  "animations_in_pack_for_slot": ["water-spell-impact-subset"],
                  "render_notes": "particlesOver at peak."},
        }
    },
    "earth-spell-effect-03": {
        "element": "earth",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "earth-cast-charge",
                  "animations_in_pack_for_slot": ["earth-spell-startup-subset"],
                  "render_notes": "Ground-anchored startup glow. particlesUnder."},
            "C": {"substrate_tag": "earth-impact",
                  "animations_in_pack_for_slot": ["earth-spell-slam-subset"],
                  "render_notes": "ground_slam_directional + impact_burst. particlesOver peak; sustained debris frames drop to particlesUnder."},
            # B: earth typically instant AOE, no projectile slot
        }
    },
    "wind-spell-effect-03": {
        "element": "wind",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "wind-cast-charge",
                  "animations_in_pack_for_slot": ["wind-spell-startup-subset"],
                  "render_notes": "Swirl-around-caster startup. particlesUnder."},
            "B": {"substrate_tag": "wind-projectile",
                  "animations_in_pack_for_slot": ["wind-spell-projectile-subset"],
                  "render_notes": "particlesMid travel."},
            "C": {"substrate_tag": "wind-impact",
                  "animations_in_pack_for_slot": ["wind-spell-impact-subset"],
                  "render_notes": "particlesOver peak; brief ambient swirl can spill to particlesUnder."},
        }
    },
    # Thunder — substrate-name = lightning per substrate-expansion-decision
    "thunder-spell-effect-03": {
        "element": "lightning",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "lightning-cast-charge",
                  "animations_in_pack_for_slot": ["thunder-spell-startup-subset"],
                  "render_notes": "Crackle-around-caster startup. particlesUnder + occasional particlesOver flash."},
            "B": {"substrate_tag": "lightning-projectile",
                  "animations_in_pack_for_slot": ["thunder-spell-bolt-subset"],
                  "render_notes": "particlesMid (or particlesOver for forked-bolt overhead reads)."},
            "C": {"substrate_tag": "lightning-impact",
                  "animations_in_pack_for_slot": ["thunder-spell-strike-subset"],
                  "render_notes": "particlesOver peak; brief afterglow drops to particlesMid."},
        }
    },
    "ice-spell-effect-02": {
        "element": "water",  # ice as water-substrate variant per canonical-7
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "C": {"substrate_tag": "water-impact-ice-variant",
                  "animations_in_pack_for_slot": ["ice-spell-impact-subset"],
                  "render_notes": "Ice flavor variant for water-impact when skill is cold-flavored. particlesOver."},
            "E": {"substrate_tag": "water-slow-ambient",
                  "animations_in_pack_for_slot": ["ice-spell-frozen-loop-subset"],
                  "render_notes": "Sustained frost overlay above entity. particlesOver for legibility."},
        }
    },
    "holy-spell-effect": {
        "element": "holy",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "holy-cast-charge",
                  "animations_in_pack_for_slot": ["holy-spell-startup-subset"],
                  "render_notes": "Radiant-ring-around-caster. particlesUnder + particlesOver halo."},
            "C": {"substrate_tag": "holy-impact",
                  "animations_in_pack_for_slot": ["holy-spell-burst-subset"],
                  "render_notes": "Bright burst. particlesOver peak; verify peak-on-frame-1 per drax § 2.2 Slot C."},
            "E": {"substrate_tag": "holy-debuff-ambient",
                  "animations_in_pack_for_slot": ["holy-spell-glow-loop-subset"],
                  "render_notes": "Sustained holy-tint loop. particlesOver overlay."},
        }
    },
    "dark-spell-effect": {
        "element": "shadow",  # canonical-7 name; pimen 'dark' = shadow
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 1.59,
        "slots": {
            "A": {"substrate_tag": "shadow-cast-charge",
                  "animations_in_pack_for_slot": ["dark-spell-startup-subset"],
                  "render_notes": "Inky-pulse-around-caster. particlesUnder."},
            "C": {"substrate_tag": "shadow-impact",
                  "animations_in_pack_for_slot": ["dark-spell-burst-subset"],
                  "render_notes": "Dark void burst. particlesOver peak."},
            "E": {"substrate_tag": "shadow-curse-ambient",
                  "animations_in_pack_for_slot": ["dark-spell-aura-loop-subset"],
                  "render_notes": "Sustained shadow-overlay loop. particlesOver."},
        }
    },
}

# Earth Elemental enemy sprite (bundled split row)
EARTH_ELEMENTAL = {
    "earth-spell-effect-03::enemy-elemental": {
        "element": "earth",
        "pack_origin": "pimen-bundle-mega-01",
        "cost_attribution": 0.0,  # bundled with earth-spell-effect-03 purchase
        "category": "enemy-sprite",
        "slots": {},  # NOT a VFX-slot asset; reserved for embodiment trial
        "render_notes": "Enemy-sprite bundled with earth-spell-effect-03. NOT VFX; reserved for embodiment trial scope (out of VS2a slot wiring). Flag for future embodiment-asset dispatch.",
    }
}

# Physical / kinetic packs
PHYSICAL_PACK_VS2A_DEPLOY = {
    "battle-vfx-hit-spark": {
        "element": "physical",
        "pack_origin": "pimen-step-b",
        "cost_attribution": 4.25,
        "slots": {
            "C": {"substrate_tag": "physical-impact",
                  "animations_in_pack_for_slot": ["hit-spark-burst-subset"],
                  "render_notes": "Sprite-required for Slot C per drax § 2.2; particlesOver peak. Aseprite source available — palette-shift capable per § 2.5."},
        }
    },
    "battle-vfx-projectile": {
        "element": "physical",
        "pack_origin": "pimen-step-b",
        "cost_attribution": 4.25,
        "slots": {
            "B": {"substrate_tag": "physical-projectile",
                  "animations_in_pack_for_slot": ["arrow-bolt-trail-subset"],
                  "render_notes": "Hunter projectile sprite + muzzle-flash. particlesMid travel."},
            "C": {"substrate_tag": "physical-impact",
                  "animations_in_pack_for_slot": ["projectile-impact-subset"],
                  "render_notes": "Backup Slot C for projectile-arrival impact. particlesOver peak."},
        }
    },
    # CC-BY — attribution risk per Gap G4
    "pixel-battle-effects": {
        "element": "physical",
        "pack_origin": "pimen-9",
        "cost_attribution": 0.0,
        "attribution_class": "cc-by",  # override default
        "slots": {
            "C": {"substrate_tag": "physical-slash",
                  "animations_in_pack_for_slot": ["cutting-slash-arc-subset"],
                  "render_notes": "CC-BY ATTRIBUTION REQUIRED. particlesOver peak. Fallback only if drax filter-includes CC-BY OR awaiting CodeManu acquisition."},
        }
    },
}

# Buff/debuff packs — Slot D (status-apply) + Slot E (status-ambient)
# Two packs from the 9 available is sufficient per gandalf § 3.3 ordering #8.
# Selection criteria: hand-drawn-pixel + aseprite-source-included = palette-shift
# capable (per drax § 2.5 + spec § 1.3) for substrate-modulated rendering.
BUFF_DEBUFF_PACKS_VS2A_DEPLOY = {
    "buff-n-debuff-vfx-pack-01": {
        "element": "substrate-modulated",  # buff/debuff applies across all 7 elements via tint
        "pack_origin": "pimen-step-b",
        "cost_attribution": 2.55,
        "slots": {
            "D": {"substrate_tag": "status-apply-generic",
                  "animations_in_pack_for_slot": ["status-apply-burst-subset"],
                  "render_notes": "One-shot status-apply ring. particlesOver. Tint per element substrate at runtime (drax composes element-color onto pack frames)."},
            "E": {"substrate_tag": "status-ambient-generic",
                  "animations_in_pack_for_slot": ["status-ambient-loop-subset"],
                  "render_notes": "Sustained ailment overlay. particlesOver for over-entity reads; particlesUnder for ground-aura reads. Tint per element."},
        }
    },
    "buff-n-debuff-vfx-pack-02": {
        "element": "substrate-modulated",
        "pack_origin": "pimen-step-b",
        "cost_attribution": 2.55,
        "slots": {
            "D": {"substrate_tag": "status-apply-generic-variant",
                  "animations_in_pack_for_slot": ["status-apply-ring-subset"],
                  "render_notes": "Distinct visual register from pack-01 — multi-ailment legibility per drax § 2.2 Slot D concurrency note (8px radial jitter when stacked). Aseprite source available."},
            "E": {"substrate_tag": "status-ambient-generic-variant",
                  "animations_in_pack_for_slot": ["status-ambient-loop-subset"],
                  "render_notes": "Alternative sustained loop for distinct ailment families. Distinguishable from pack-01 when 3+ ailments stacked."},
        }
    },
}


def build_manifest_rows(curated_records: list[dict]) -> list[dict]:
    """Build manifest rows by joining VS2a deploy maps against curated records."""
    curated_by_id = {r["source_asset_id"]: r for r in curated_records}

    # Merge all deploy maps
    all_deploy = {**ELEMENT_PACK_VS2A_DEPLOY,
                  **EARTH_ELEMENTAL,
                  **PHYSICAL_PACK_VS2A_DEPLOY,
                  **BUFF_DEBUFF_PACKS_VS2A_DEPLOY}

    rows = []
    for pack_slug, deploy in all_deploy.items():
        curated = curated_by_id.get(pack_slug)
        if curated is None:
            raise SystemExit(f"FATAL: pack_slug '{pack_slug}' not found in curated catalogue")

        # Earth Elemental special case — no VFX slots; produce a single
        # reference row for tracking + embodiment-trial-deferred routing.
        if not deploy.get("slots"):
            rows.append({
                "asset_id": f"{pack_slug}.embodiment-reserved.NA",
                "pack_slug": pack_slug,
                "vendor": "pimen",
                "substrate_tag": "earth-enemy-sprite-embodiment-reserved",
                "slot": "N/A",
                "encounter_compatibility": ["elite", "mini-boss", "boss"],
                "attribution_class": "commercial-license",
                "pack_origin": deploy["pack_origin"],
                "animations_in_pack_for_slot": [],
                "render_notes": deploy.get("render_notes", ""),
                "spec_ref": "vs2a-vfx-scene-needs.md § 1.3 (embodiment matrix) + § 3.3 Gap G3",
                "source_url": curated.get("source_url"),
                "cost_usd_attributed": deploy["cost_attribution"],
                "curated_row_ref": f"pimen-catalogue-curated-2026-05-16.jsonl::{pack_slug}",
                "vs2a_status": "deferred-embodiment-trial-scope",
            })
            continue

        # Default attribution class from curated license
        default_attr = "commercial-license"
        if curated.get("license") == "CC-BY":
            default_attr = "cc-by"

        for slot_letter, slot_info in deploy["slots"].items():
            attr = deploy.get("attribution_class", default_attr)
            rows.append({
                "asset_id": f"{pack_slug}.{slot_info['substrate_tag']}.{slot_letter}",
                "pack_slug": pack_slug,
                "vendor": "pimen",
                "substrate_tag": slot_info["substrate_tag"],
                "slot": slot_letter,
                "encounter_compatibility": COMBAT_ENCOUNTERS,
                "attribution_class": attr,
                "pack_origin": deploy["pack_origin"],
                "animations_in_pack_for_slot": slot_info["animations_in_pack_for_slot"],
                "render_notes": slot_info["render_notes"],
                "spec_ref": f"vs2a-vfx-scene-needs.md § 2.2 Slot {slot_letter} + § 3.3 design-ordering",
                "source_url": curated.get("source_url"),
                "cost_usd_attributed": deploy["cost_attribution"],
                "curated_row_ref": f"pimen-catalogue-curated-2026-05-16.jsonl::{pack_slug}",
                "vs2a_status": "active",
            })

    return rows


def main():
    curated = []
    with open(CURATED_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                curated.append(json.loads(line))

    rows = build_manifest_rows(curated)

    # Header row — manifest provenance
    header = {
        "_manifest_kind": "pimen-subset-vs2a",
        "_manifest_version": "1.0",
        "_generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "_generated_by": "elrond+build_pimen_subset_vs2a_2026_05_17.py",
        "_spec_ref": "canonical/story/vs2a-vfx-scene-needs.md (commit 43396bb)",
        "_dispatch_ref": "agentic_orchestration/dispatches/2026-05-17-elrond-pimen-subset-selection-vs2a.md",
        "_curated_source": "agentic_orchestration/research/curated/pimen-catalogue-curated-2026-05-16.jsonl",
        "_row_count": len(rows),
        "_distinct_pack_count": len({r["pack_slug"] for r in rows}),
        "_total_cost_usd_attributed": round(sum(r["cost_usd_attributed"] for r in rows), 2),
        "_attribution_classes": sorted(set(r["attribution_class"] for r in rows)),
        "_slot_coverage": sorted(set(r["slot"] for r in rows)),
        "_substrate_tags": sorted(set(r["substrate_tag"] for r in rows)),
    }

    with open(OUT_PATH, "w") as f:
        f.write(json.dumps(header) + "\n")
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"Wrote manifest: {OUT_PATH}")
    print(f"  manifest rows (data): {len(rows)}")
    print(f"  distinct packs: {header['_distinct_pack_count']}")
    print(f"  total cost attributed: ${header['_total_cost_usd_attributed']}")
    print(f"  attribution classes: {header['_attribution_classes']}")
    print(f"  slots covered: {header['_slot_coverage']}")
    print(f"  substrate-tag count: {len(header['_substrate_tags'])}")


if __name__ == "__main__":
    main()
