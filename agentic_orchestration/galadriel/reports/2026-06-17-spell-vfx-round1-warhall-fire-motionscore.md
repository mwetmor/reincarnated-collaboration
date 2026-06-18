# Spell-VFX Round-1 — war_hall FIRE cast — galadriel motion-score (Gate A, INDEPENDENT)

**Scorer:** galadriel (visual perception). **Date:** 2026-06-17. **godot commit:** `3b1daa2`.
**Authority:** `agentic_orchestration/gandalf/notes/2026-06-17-spell-vfx-round1-galadriel-motionscore-request.md`
**Tracker:** `agentic_orchestration/gandalf/notes/2026-06-17-spell-vfx-runtogreen-log.md` (§2.4 criteria, §3 dual gate).
**Instrument:** `agentic_orchestration/galadriel/pipeline/spell-motion-score.mjs` → `.json` + `spell-motion-trajectory.png`.
**Mask diagnostic:** floor-wash vs bright-core separation confirmed via mask-viz (see § methodology).

**Discipline note:** scored INDEPENDENTLY before consuming gandalf's eyes-on. gandalf's read + drax self-assess named two residuals; my metrics 1/4/5 were tasked to confirm-or-refute. They are confirmed below, quantified. This is the cross-check working, not anchoring.

---

## 0. Capture integrity — PASS

- 7 frames, 1152×648, t = 0.08/0.18/0.30/0.47/0.63/0.74/0.92 (charge → charge-peak → release → mid-travel → impact-onset → impact → fade).
- **md5-distinctness: PASS — 7 unique hashes, zero repeats.** The descent "cam1 grabbed six times" false-read is ruled out; the frames are genuinely a time sequence with motion.

---

## 1. Why a new instrument + the methodology crux

A spell is a VERB; the static register-2 scorer (LDR/SHF/warmCool) cannot score a verb. New instrument = a **time-sequence motion scorer**.

**The crux (no-silent-transformation):** the naive "warm-energy centroid over the whole frame" is the WRONG instrument and I proved it on this strip — a whole-frame warm centroid barely moves (48%→46% x) because it is SWAMPED by the static warm chamber backdrop (torchlit walls, braziers, warm floor). Same trap the blue-slab diagnostic warned of. The spell is ADDITIVE light on a STATIC (GREEN-locked) rig, so the correct isolation is an **additive-floor subtraction**:

```
backdrop_floor(x,y) = MIN over all 7 frames of warm-luma(x,y)        [the static warm field]
spell_energy(x,y,t) = max(0, warm-luma(x,y,t) - backdrop_floor(x,y)) [the transient cast]
```

The static walls/braziers have ~0 excess (warm in every frame → floor eats them). The KEEP-locked pale `CombatFill` disc under the caster is cool-pale + static → excluded twice (warm gate + floor subtraction). **Spell-mask = spell_energy ≥ 28.**

**Refinement (mask-viz-corroborated):** the full-mask (e≥28) is contaminated in the charge frames (F01–F03) by a diffuse warm FLOOR-WASH the min-subtraction under-cancels. The mask-viz shows it plainly: F01–F03 = a broad red floor blob; F04–F07 = a tight bright bloom that marches right. So the **headline track is the BRIGHT-CORE centroid (e≥90)** — the bolt the eye follows — reported alongside the full-mask for transparency. Both are in the JSON.

**Caster/threat geometry — grounded by pixel-probe, not assumed:** caster = (34,72)% (F01 brightest-pixel origin, the hero center-bottom); threat = (53,57)% (F06 impact-burst centroid, the mob cluster screen-right). Caster→threat vector points right + slightly up.

---

## 2. Per-metric report

### Metric 1 ★ ENERGY-TRAVEL (headline) — PASS

Bright-core centroid axis-fraction (0 = caster, 1 = threat):

| frame | beat | CORE (x%,y%) | CORE axis | full axis |
|---|---|---|---|---|
| F01 | charge | (76.2, 88.2) | 1.034 ⚠ | 0.53 |
| F02 | charge-peak | (41.9, 81.6) | **0.028** (at caster) | 0.028 |
| F03 | release | (51.7, 86.7) | 0.236 | 0.177 |
| F04 | mid-travel | (60.1, 75.7) | 0.799 | 0.758 |
| F05 | impact-onset | (60.4, 71.7) | 0.907 | 0.948 |
| F06 | impact | (61.5, 68.0) | **1.040** (at threat) | 1.048 |
| F07 | fade | (70.6, 72.5) | 1.236 | 1.178 |

**HEADLINE: from the first formed-core frame (F02, AT the caster, axis 0.028) to impact (F06, AT the threat, axis 1.04) = +1.012 caster→threat axis-march; +19.6% frame-width rightward.** This is a textbook caster→threat travel signature — the energy EMANATES from the caster and TRAVELS to the threat. **PASS.**

The F01 axis=1.034 is a charge-frame artifact (bright pixels present but not yet a coherent bolt — mask-viz proves F01 is floor-wash, not a formed core). It is the reason a naive "first-to-last net" misleads; the coherent-bolt window F02→F06 is the honest headline.

### Metric 2 INTER-FRAME MOTION-PRESENCE — PASS

Mean inter-frame delta in the spell region peaks at the release→travel beat (60.3 at F03→F04, 47.7 at F04→F05) and the high-delta band's centroid SPANS 22% of frame-width across the strip (47.7% → 69.7%). The leading edge **propagates** across frames; it does not pulse in one place. **PASS** — there is genuine inter-frame motion and it advances spatially.

### Metric 3 FIRE-HUE LEGIBILITY — PASS

| frame | dom hue | fire-band frac (0–50°) | mean RGB |
|---|---|---|---|
| F01–F04 (charge→travel) | 350–360° (deep red) | 0.30–0.45 | R>G>B, warm |
| F05–F07 (impact→fade) | 50–60° (amber/gold) | 0.42–0.51 | R>G>B, hot |

Dominant hue is **deep-red in charge/travel (350–360°), shifting to amber/gold (50–60°) at impact** — a physically-correct fire lifecycle (cooler red ember → hot amber flash). Mean RGB is R>G>B throughout (warm-dominant, B always lowest). Fire-band fraction 0.30–0.51. **PASS — reads unambiguously as fire**, no element-ambiguous mush, no non-fire cast hue. (Note: the charge red at 350–360° is the slightly-magenta-leaning red gandalf's eye flagged — it sits at the red/magenta boundary, not in the orange core. Minor, cosmetic.)

### Metric 4 PREMIUM-LAYERING — PASS at impact, MARGINAL at mid-travel (CONFIRMS residual a)

Mean local-luma-std inside the mask (blue-slab flat-cardboard line = ≤9.0):

| frame | beat | mean local-std | read |
|---|---|---|---|
| F01 | charge | 7.38 | below flat line (diffuse charge wash) |
| F02 | charge-peak | 8.27 | below flat line |
| F03 | release | 7.53 | below flat line |
| **F04** | **mid-travel** | **8.55** | **AT the flat-cardboard boundary — soft, low internal structure** |
| F05 | impact-onset | 11.79 | clear of flat — layered burst |
| F06 | impact | 10.37 | clear of flat — layered |
| F07 | fade | 10.90 | clear of flat — layered |

**The impact (F05–F06) is genuinely premium-layered (10.4–11.8, well clear of the 9.0 flat line). But the mid-travel bolt (F04) sits at 8.55 — right at the flat-cardboard boundary.** The traveling bolt has LOW internal layering: it is a soft bloom, not a structured core+glow+particle projectile. **This CONFIRMS residual (a): the mid-travel bolt reads SOFT** — quantified, F04 layering 8.55 vs the impact's 10.4–11.8, a ~25% structure deficit at the travel beat.

### Metric 5 DIRECTIONALITY / PRINCIPAL-AXIS — PARTIAL (CONFIRMS residual b)

| frame | elongation (1=round) | axis-align cos (1=at threat) | princ axis° | c→t axis° |
|---|---|---|---|---|
| F01 | 3.59 | 0.918 | 0.9 | -22.5 |
| F02 | 2.28 | 0.940 | -2.5 | -22.5 |
| F03 | 3.83 | 0.897 | 3.7 | -22.5 |
| F04 | 3.48 | 0.855 | 8.8 | -22.5 |
| F05 | 3.26 | 0.826 | 11.8 | -22.5 |
| F06 | 3.34 | 0.812 | 13.2 | -22.5 |
| F07 | 3.96 | 0.738 | 19.9 | -22.5 |

**Elongation 2.3–3.9 throughout — the spell IS shaped, NOT a radially-symmetric ground-glow** (a glyph would be ~1.0). So it is not decoration; it points somewhere. **BUT the principal axis is near-horizontal (0–13°) while the caster→threat axis is -22.5° (down-and-right), and the alignment DEGRADES across the lifecycle (cos 0.92 charge → 0.81 impact → 0.74 fade).** The bolt elongates **horizontally-rightward** but the threat is **down-and-to-the-right** — so the aim is good-not-crisp (cos 0.81 at impact ≈ 30–35° off the true threat-line) and drifts further off-axis as it travels. **This CONFIRMS residual (b): directionality reads as "fire migrates rightward" more than "a crisp bolt aimed at the specific marquee point"** — the aim-axis is horizontal and loosens as the spell travels, rather than holding a locked line to the threat.

### Backdrop-invariance (Gate-B-adjacent) — PASS

OUTSIDE the union spell-mask, drift vs F01: max luma-drift = **1.276** (tol 4.0), max warmbias-drift = 1.93. Both well within tolerance. **The chamber backdrop is INVARIANT frame-to-frame except where the spell is — the cast is purely additive; the GREEN-locked rig did NOT move.** Gate-B holds on the rig-stability axis. (The small residual drift is the spell's additive bloom bleeding a few px past the mask edge — expected, not a rig change.)

---

## 3. Independent PASS/FAIL read

**Does the sequence read as a character-driven FIRE spell emanating caster→threat, or still a static summon-glyph?**

**It reads as a character-driven FIRE cast emanating caster→threat. NOT a static summon-glyph.** The transformation LANDED. Five-metric scorecard:

| metric | verdict | evidence |
|---|---|---|
| 1 ★ energy-travel | **PASS** | +1.012 axis-march F02→F06 (caster→threat); +19.6% frame-width |
| 2 motion-presence | **PASS** | high-delta band propagates 22% frame-width; not a pulse-in-place |
| 3 fire-hue | **PASS** | deep-red→amber fire lifecycle, R>G>B throughout, fire-band 0.30–0.51 |
| 4 premium-layering | **PASS (impact) / MARGINAL (mid-travel)** | impact 10.4–11.8 layered; **F04 mid-travel 8.55 at the flat-cardboard line** |
| 5 directionality | **PARTIAL** | elongated 2.3–3.9 (shaped, not radial), but axis horizontal/loosening, cos 0.81 at impact (~30° off the threat-line) |
| backdrop-invariance | **PASS** | max drift 1.28 vs tol 4.0; rig untouched, additive cast |

**No metric exposes a static-glyph failure.** The glyph→cast transformation is real and measured. The two residuals are crispness/polish, not a fundamental failure — exactly the disposition gandalf's eye + drax self-assess called.

**My numbers CONFIRM both named residuals** (they do not refute them — I looked for cleaner-than-the-eye and did not find it; if anything metric 4 puts a hard number on the soft-bolt and metric 5 quantifies the aim-drift):
- **(a) soft mid-travel bolt** — metric 4: F04 layering 8.55, at the flat-cardboard boundary, vs impact 10.4–11.8. The travel beat lacks core+glow+particle structure; it is a bloom.
- **(b) directionality migrates-rightward not crisply-aimed** — metric 5: principal axis horizontal (0–13°) vs threat-line -22.5°; alignment loosens 0.92→0.74 across the lifecycle. Shaped but not threat-locked.

---

## 4. One-line verdict + precise residual (for a targeted Round-2)

**VERDICT: PASS-with-residual.** The war_hall FIRE cast reads as a character-driven spell emanating caster→threat (headline metric 1: +1.012 axis-march, confirmed by motion-presence, fire-hue, impact-layering, and an invariant backdrop) — the summon-glyph is genuinely replaced by a cast verb. **Two convergent residuals are confirmed and quantified, both at the mid-travel/aim layer:**

> **Residual (a) — soft mid-travel bolt: metric 4, frame F04 (t=0.47), layering 8.55 sits AT the 9.0 flat-cardboard line vs the impact's 10.4–11.8 — a ~25% internal-structure deficit at the travel beat. The bolt is a soft bloom, not a layered projectile.**
>
> **Residual (b) — aim migrates rightward not threat-locked: metric 5, frames F04–F07, principal axis stays near-horizontal (8–20°) while the caster→threat line is -22.5°; alignment loosens cos 0.86→0.74 across travel→fade (~30–35° off the threat-line at impact). The bolt is shaped and rightward but does not hold a locked aim-line to the marquee point.**

**Round-2 is targetable not blind:** sharpen the F04–F05 mid-travel silhouette (raise internal luma-variance — tighter core + crisper glow falloff + particle scatter, push F04 layering from 8.55 toward the impact's 10+) AND tilt/lock the projection axis down-and-right onto the caster→threat vector (-22.5°) so elongation aligns (target cos ≥ 0.90 held across travel, not loosening to 0.74). The charge→impact emanation, fire-legibility, and rig-invariance are PROVEN — Round-2 touches only the bolt's mid-travel crispness + aim-lock, nothing upstream.

**Dual-gate handoff:** my photometry/motion numbers OWN the above (authoritative). gandalf OWNS the composition ruling on CONVERGENCE — and my numbers CONVERGE with his recorded eyes-on (transformation landed; same two residuals, now quantified). The cross-check agrees: targeted drax Round-2 on (a)+(b), not a re-architecture.

---

**Artifacts:**
- Instrument: `agentic_orchestration/galadriel/pipeline/spell-motion-score.mjs`
- Scores: `agentic_orchestration/galadriel/pipeline/spell-motion-score.json`
- Trajectory strip (centroid-annotated): `agentic_orchestration/galadriel/pipeline/spell-motion-trajectory.png`
- Captures (local, git-ignored, Synty-derivative): `reincarnated-godot/harness_logs/descent_spellfx_warhall_seq_01..07.png`

**Signed:** galadriel, 2026-06-17. Gate A — NEW time-sequence motion-score instrument (a spell is a verb; the static scorer can't score it). Headline = energy-travel caster→threat, confirmed +1.012 axis-march. PASS-with-residual; both named residuals confirmed + quantified (metric 4 soft-bolt F04, metric 5 aim-drift F04–F07). Independent of gandalf's eye; converges with it.
