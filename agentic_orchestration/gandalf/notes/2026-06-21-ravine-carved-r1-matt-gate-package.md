# Carved Ravine — Revision 1 — Matt Gate Package

**Status:** TRIPOD COMPLETE — awaiting the Matt Gate. The carve + Matt's two R1 corrections are built, rendered, and scored on all three tripod legs. Two items need Matt's adjudication before (or at) the gate; both are batched with all other build refinements into ONE post-decision drax round to avoid re-render churn.
**Author:** gandalf (design steward), 2026-06-21.
**Build:** `reincarnated-godot` `d0b7191` (carve + R1), held — NO push. galadriel scorecard `155cdac`. Carve-spec `3dc3372` + Revision-1 amendment (this session).
**Parents:** `2026-06-21-ravine-carve-and-sculpt-spec.md` (the build contract incl. the Revision-1 section); `2026-06-20-ravine-atgrade-matt-gate-package.md` (the prior gate this transforms from); `2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (scoring target).

---

## 1. What you're gating

The approved flat at-grade scene, CARVED into a sculpted gorge (`scenes/ravine_carved.tscn`, a NEW scene — the approved `ravine_atgrade.tscn` is untouched), then revised per your two corrections after you viewed the first carve:

- **Carve:** footprint dropped below grade; footprint boundary → tapered-overhang `Dirt_Cliff` wall line (smooth rounded rock, wider at bottom = lean-in overhangs); cross-log raised overhead; rim forest stays at grade as the genuine massive-zone illusion above. Dressing: fern-topped outcrops, vine-wrapped log bridge, leaf-pile rim, intermittent magical green current in the trough, moss+leaf rock caps, corner ferns, downward roots, and small blue/cyan bioluminescent mushrooms at the base + sides (the §3 CRITICAL signature the at-grade scene under-served).
- **R1-A (your correction):** added a slightly-blue **sky sliver** at the top of the rim trees + a **sun FILL** light so more light reaches the gorge floor — held to the emissive-led register.
- **R1-B (your correction):** replaced the uniform 8 m depth with a shallower **variable** profile (see §3 — this is one of the two items needing your call).

Frames (local, gitignored — your eye): `/Users/admin/Games/reincarnated-godot/harness_logs/ravine_carved_2026-06-21/` (`00_committed`, `01_pool1`, `02_reveal`, `03_pool2`, `04_downgorge`, `05_lookback`, `10_carve_floor_downgorge`; up-shaft diagnostics `06`/`07`; MP4 `ravine_carved_walkthrough.mp4`).

## 2. The tripod verdict (all three legs)

| Reviewer | Result | Note |
|---|---|---|
| **drax (builder self-score)** | ~0.95 | gameplay frames median value 0.12–0.15 (5–20% band), emissive p99 0.54–0.73; §6 = 0; builder bias acknowledged |
| **galadriel (CV)** | **0.85 composite · 0 / 10 §6 auto-fails · register SURVIVED** | clears threshold (≥0.75 + zero auto-fails). Base median 0.096 (dark-first), glow p99 0.698, daylight-spike 0.0003%, enchanted-family 99.9%, neutral-gray 0.007%. Scorecard: `agentic_orchestration/galadriel/reports/2026-06-21-enchanted-forest-ravine-carved-r1-cv-scorecard.md` |
| **gandalf (§1/§4 human read)** | **PASS-with-held-items** | both your corrections landed and READ correct — see §3/§4 |

**The carve traded breadth for depth, as designed** (galadriel vs the 0.94 at-grade baseline): won ravine-layering 0.70→0.92, enclosure 0.90→0.96, fog-depth 0.72→0.80; paid emissive-multi-hue 0.90→0.80, mushroom-variety 0.95→0.85, warm-cool contrast 0.88→0.74. All liftable, none an auto-fail. The emissive *character* softened (punchy lime caps → diffuse cooler teal/cyan glow off the trough); register survived, glow is still the apex on every hero frame.

## 3. My §1/§4 judgment — your corrections landed

**R1-A (sky/sun): PASS.** Frame `06` (look up the wall) was a pure-black void; now a blue sky band + warm sun disc above the rim silhouettes — light reaches in, depth-hierarchy framing restored. Frame `10` (down-gorge floor) was murky-dark; now legible — deck, enemies, blue cliff-base mushrooms, the bright-green trough current — and the register survives by eye (green current is the brightest thing, base dark-teal). galadriel confirms quantitatively: not daylit, dark-first intact.

**R1-B (depth): reads correct in frame `10`** — a proper enclosing gorge, not a deep slot, not a shallow scratch.

## 4. The two items I held for YOUR call (not defects — adjudication)

1. **The depth number — needs your reference.** drax measured the hero mushrooms at **10.24 m** — ~2× my spec's estimate. Taken literally, "1–1.5 large mushrooms" = 10–15 m, *deeper* than the 8 m you called too deep. drax correctly treated your binding intent ("shallower / more light to the floor") as governing and set a **variable 4.0–6.5 m** profile (shallow at entry → deepening to the Pool-2 climax → easing back at exit; all through-axis slopes < 10°, combat floor stays flat-walkable). At 4–6.5 m the gorge is ~half a hero-mushroom deep, so the giant mushrooms stand taller than the rim. **Frame `10` is the cleanest depth read — does that match what you pictured, or set a different absolute against the frame?** ("1 mushroom" and the 10 m measurement can't both hold; I'd rather you anchor the number than I guess.)
2. **Frame `01` (pool1) occlusion.** A large dark overhang rock eats the right ~40% of that frame — the camera station collides with the new lean-in overhang geometry (same family as the earlier burial problem). A camera-station pass fixes it without touching the build. Most significant of the composition residuals.

## 5. Batched-next-round items (after your depth call — do NOT fire piecemeal)

A depth change forces a full re-render, so all build refinements batch into ONE drax round after you rule on depth:
- **(if depth changes)** re-profile `_carve_d(z)` to your number + re-render.
- **galadriel's top dissonance:** warm-vs-cool contrast collapsed (warm 0.0004% — every amber cap fell outside the gorge framings). **One in-frame warm amber mushroom cap restores the §3 amber-against-teal pop** — the cheapest single lift on the board.
- **Frame `01` camera-station** fix (§4.2).
- **Frame `03` pool water** reads loud/saturated cyan — minor, carried WATCH; dial if it bothers you.

## 6. The gate decision in front of you

- **PASS as-is** (accept the 4–6.5 m depth) → I fire ONE drax round for the §5 polish items (warm cap + frame-01 camera + optional water dial), re-run the tripod, final gate.
- **ADJUST depth** → name the absolute against frame `10`; I fold it into the §5 batch round and re-gate.
- **HOLD on anything your eye catches** → name it; targeted round.

Nothing pushed — carve held at `d0b7191`, galadriel scorecard at `155cdac`, awaiting your authorization.

## Sign-off
gandalf, 2026-06-21. Tripod complete (drax ~0.95 · galadriel 0.85 / 0 auto-fails / register SURVIVED · gandalf §1/§4 PASS-with-held-items). Your two corrections landed; two items await your adjudication (depth number, frame-01 occlusion); all build refinements batched into one post-decision round to avoid re-render churn. The human gate is yours.
