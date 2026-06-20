# At-Grade Ravine — Matt Gate Package (FRESH-START build, pre-carve)

**Status:** READY FOR THE MATT GATE. This is the flat, fully-walkable patterned combat scene built on the REAL POLYGON Enchanted Forest assets. **No carve until you pass it** (carve = drop the channel 7-10 modules + raise cross-log, a post-gate transform).
**Author:** gandalf (design steward), 2026-06-20.
**Parents:** `2026-06-20-ravine-cutout-pattern-spec.md` (the build contract); `2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (the GPT-5.4 scoring target); the burn-down + fresh-import + at-grade-first dialogue this session.

---

## 1. What you're gating

A single Godot scene laid out FLAT AT GRADE per the locked pattern: `entry-pinch → POOL 1 (8 goblin grunts) → connector-pinch (quasi-snake, hides Pool 2) → POOL 2 (Troll_01 boss + 3 elites) → exit-pinch`, ~80m × ~40m. Everything walkable. Built 100% from real Synty POLYGON meshes (enchanted-forest biome + goblin-war-camp roster skinned green + Troll_01). **Zero SIMPLE assets** (mechanical guard PASS, re-verified by me: 28,201 paths scanned, zero).

Frames (local, gitignored — your eye): `/Users/admin/Games/reincarnated-godot/harness_logs/ravine_atgrade_2026-06-20/` (00_committed, 01_pool1, 02_reveal, 03_pool2, 04_downgorge, 05_lookback).

## 2. The tripod verdict (all three legs)

| Reviewer | Result | Note |
|---|---|---|
| **galadriel (CV)** | **0.94 composite · 0 / 10 §6 auto-fails** | clears threshold (≥0.75 + zero auto-fails) with margin; 95.7% enchanted-family pixels, 0.0002% neutral-gray, emissive in the 5-15% band, dark-first/lit-from-within. Scorecard: `agentic_orchestration/galadriel/reports/2026-06-20-enchanted-forest-ravine-atgrade-cv-scorecard.md` |
| **drax (builder self-score)** | ~0.78 (conservative) | honest below-1.0 flags on density (combat islands deliberately sparse for telegraph clarity) and ravine-layering (flat by design pre-carve) |
| **gandalf (§1/§4 human read)** | PASS-with-held-taste | the enchanted read genuinely LANDS — see §3 |

## 3. My §1/§4 judgment (mood / enclosure / depth hierarchy)

**It reads as the target.** Emissive-led enchanted register over a dark teal base — glowing amber + cyan mushroom caps, calm cyan/green water pools as primary light, framing trunks, real fog depth. This is a different universe from the prior fake-prism run. **Frame 01_pool1 is the exemplar:** a matte combat island ringed by a calm glowing cyan pool, amber hero focal, dark enclosure — exactly the "magic pops because the base is dark" read the rubric demands.

**Two defects I caught and fixed autonomously this round (NOT held — resolved):**
1. **Water read as shattered cyan glass shards** (jittered overlapping tiles) → rebuilt as coherent calm sheets, one still-water level per pool. The core fix. (A real CCW-winding/back-face-cull bug surfaced behind the rewrite; also fixed.)
2. **Cyan caps white-clipped + a rim trunk bisected the downgorge sightline** → both resolved.

## 4. Held for YOUR taste (register-tier, not defects — I did NOT spin more rounds)

1. **Pool edges are faintly rectangular** — the water flood follows the footprint rectangle rather than an organic shoreline. Naturalness refinement; one build-tuning pass if it bothers you.
2. **03_pool2 is the weakest framing** — its camera looks steeply down, so the calm-water read goes subordinate to the island deck (galadriel: this one frame drags density + depth; the other 5 carry the set). Camera-station taste.
3. **03_pool2 has a dark-quad billboard upper-right** — a `Background_Trees` mesh lacking alpha transparency renders opaque. Fixing it is a project-wide foliage-alpha change that risks regressing the other 5 frames; deliberately not chased. Decide if it's worth the risk.

## 5. The gate decision in front of you

**PASS** → I authorize drax to carve: drop the channel 7-10 `Dirt_Cliff` modules, the at-grade rim forest becomes the genuine massive-zone illusion above, raise the pre-placed `Log_01` to span the gorge as the cross-log. The footprint mechanism is unchanged by the carve — it's a transform on this approved surface.
**HOLD** → name which of §4 (or anything your eye catches) you want resolved first; I fire a targeted round and re-gate.

No push has happened — everything is committed local, awaiting your authorization (the build commits + galadriel scorecard + this package).

## Sign-off
gandalf, 2026-06-20. Tripod PASS on the CV + builder + design legs; the human gate is yours. No carve until you pass the flat patterned scene.
