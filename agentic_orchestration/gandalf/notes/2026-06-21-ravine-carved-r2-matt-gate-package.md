# Carved Ravine — Revision 2 — Matt Gate Package

**Status:** BUILT + VERIFIED BY EYE — awaiting the Matt Gate. R2 is committed (`reincarnated-godot 7cad6fd`, NOT pushed — push HELD per directive). My §1/§4 read is **MIXED**: your brightness/wall/overhang/water/card directives LANDED, but R2-C (hide-the-floor dense forest) and R2-D (pull the camera back) collided into a composition regression I will not rubber-stamp. Your eye is the R2 gate; this package gives you the honest read + the options.
**Author:** gandalf (design steward), 2026-06-21.
**Build:** `reincarnated-godot 7cad6fd` (R2 — height/light/forest/camera), held. galadriel CV NOT RUN this round (rubric stale, see §2).
**Parents:** `2026-06-21-ravine-carve-and-sculpt-spec.md` (Revision-2 section = the build contract); `2026-06-21-ravine-carved-r1-matt-gate-package.md` (the gate this transforms from); `2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (the now-advisory dark-first scoring target).

---

## 1. What you're gating

The R1 carve, revised per your six R2 corrections:
- **R2-A** overhang → ~10% of prior (1.5–2.8° lean, was 12–26°); walls topped at `RIM_TOP_Y = 5.5 m` — just above the 10.24 m hero-mushroom's world-top (~+3.74 m at the Pool-2 floor). The towering R1 slot is gone.
- **R2-B** brighter hazy green-blue sky (zenith `(0.40,0.66,0.78)`, sky_energy 1.35; ambient 0.24→0.82, key 0.44→1.05, sun 0.30→0.70); `ACCENT_BOOST=1.7` + glow `hdr_threshold=1.65` craft-guard so emissive still pops against the brighter base.
- **R2-C** dense above-ground forest (3 rings + ~300-item undergrowth carpet) to hide the floor. **Palm divergence:** no palm asset exists in the pack — slim solid trees (`Tree_Small/Medium`) stand in to avoid card artifacts.
- **R2-D** camera back+up to mid ravine↔cathedral (follow-cam 5.5→6.5 back / 6.5→7.0 up; in-scene station eyes ~6.5 m above the gorge floor).
- **R2-E** rock-top leaves lifted to the surface; definitive water-coherence (one calm strip per pool, no qstep quad grid); foliage cards root-caused (`TRANSPARENCY_ALPHA_SCISSOR` raw-loaded TGAs; garbage tex=none cards dropped).

Frames (local, gitignored — your eye): `/Users/admin/Games/reincarnated-godot/harness_logs/ravine_walkthrough_carved_2026-06-21/` — stations `ravine_carved_00..11_*.png`, walk beats `walk_beat_000XX.png`, MP4 `ravine_walkthrough_carved_R2.mp4`.

## 2. The verdict legs

| Reviewer | Result | Note |
|---|---|---|
| **drax (builder self-score)** | YES on combat frames, with 2 flagged soft spots | (a) dense rim carpet → green-plateau foreground in over-rim/far framings; (b) connector pinch hard to frame. no-SIMPLE exit 0; scene load-clean PASS. |
| **galadriel (CV)** | **NOT RUN** | the GPT-5.4 rubric is dark-first; R2 is an intentional bright register shift (spec flag). Scoring against the stale rubric would mislead. CV is advisory until the hazy-bright rubric re-baseline. |
| **gandalf (§1/§4 human read)** | **MIXED — register WIN + composition REGRESSION** | see §3. The static climax (`03`) is genuinely strong; most other framings are fouled by the foreground green carpet. |

## 3. My §1/§4 judgment — what landed, what broke

**LANDED (your directives are real on the hero frame):**
- **Brightness (R2-B):** `03_pool2` is no longer a dark cave. Bright hazy teal-green base, player + Troll + goblins readable, green current + glowing focal still pop. The register shift you asked for is genuine.
- **Wall height + overhang (R2-A):** walls sit just above the mushroom tops; near-vertical rocky lip, not a cantilever. The R1 towering-slot problem is solved.
- **Water (R2-E):** `03` shows continuous calm strips — the blocky cyan tiles are gone.
- **Cards (R2-E):** largely resolved on the hero frames.

**BROKE (a composition regression — NOT a soft spot):**
- `01_pool1` — a **static station** (drax's report claims in-gorge eyes avoid the carpet; they do NOT here) — a flat bright-green mass eats ~70% of the frame and shoves the goblin fight into a small distant aperture.
- Every **follow-cam** walk beat (`00080 / 00440 / 01140 / 01520`) repeats the failure: smooth featureless bright-green foreground humps dominate; the playable gorge is small and distant beyond them. The follow-cam IS the play view — this is the read that matters.
- `00_committed` (entry) reads as bland flat-green floor + dark teal rock, no enchanted character.

**Root cause — a tension between two of YOUR R2 directives:**
R2-C ("we really do not want to see much of the forest floor" → dense carpet) + R2-D ("camera back to see the ambiance above the ravine") composed into the opposite of the intent: the dense-forest carpet rendered as a smooth bright-green **skin** rather than packed foliage, and the pulled-back camera now shoots *across* that skin into a distant slot. We see a LOT of flat floor, just a green one. The two directives pull against each other and need your adjudication on which dominates.

**One defect to fix regardless:** `walk_beat_01520` has a **red/magenta region upper-left** — consistent with the safety-net material flagging an untextured asset. drax should confirm + clear it in whatever round you authorize.

## 4. The design tension to resolve (your call)

The green-carpet foreground is not a bug to patch blind — it's the visible result of R2-C × R2-D. Resolving it is a design choice between three readings, and I want your eye on it rather than guessing:

- **(i) Camera dominates** — bring the follow-cam back down/in (closer to the original ravine cam) so it sits *inside* the gorge looking along it; accept seeing less over-rim ambiance. The combat reads clean; the "deep forest above" becomes a backdrop band, not the foreground.
- **(ii) Floor-treatment dominates** — keep the pulled-back camera but replace the smooth green carpet with genuinely packed, broken-up foliage (clustered ferns/mushrooms/rocks with dark gaps) so the foreground reads as dense forest texture, not a flat green skin. More build cost; honors both directives if it works.
- **(iii) Hybrid** — pulled-back camera at the static climax stations only (where `03` already works), follow-cam rides lower during traversal. Different cameras for different beats.

## 5. The gate decision in front of you

- **PASS the register, ADJUST the composition** → tell me which of §4 (i/ii/iii) you want; I fold it + the red-artifact fix into ONE drax round and re-gate.
- **PASS as-is** (accept the green-carpet framings as the traversal look; `03` is the money shot) → I fire ONE drax round for just the red-artifact fix + re-gate.
- **HOLD on anything your eye catches** in the MP4 or frames → name it; targeted round.

Nothing pushed — R2 held at `7cad6fd`, no galadriel leg this round (rubric re-baseline pending), awaiting your adjudication.

## Sign-off
gandalf, 2026-06-21. R2 built + verified by eye. The brightness/wall/overhang/water/card directives LANDED on the hero frame; the R2-C × R2-D combination produced a foreground green-carpet regression across the traversal + pool1 framings that I will not rubber-stamp. Your two directives are in tension; §4 is the design call. The human gate is yours.
