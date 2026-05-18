# Galadriel → Drax Handoff Brief — Portrait HUD Visibility Issues

**Author:** galadriel (visual-perception steward).
**Type:** evidence-anchored handoff brief — drax-consumable.
**Authority:** Matt directive 2026-05-18 evening (*"help drax fix the portrait HUD clipping"*); per hive-mind protocol § 6.1 cross-seam coordination + agent-definition § Cross-seam coordination ("Drax may consult galadriel on technical render details").
**Source captures:** `agentic_orchestration/galadriel/captures/2026-05-18/`
**Source rubric:** `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1.md`
**Source report:** `canonical/story/visual-benchmark-vs2a-2026-05-18.md` §§ 4.1 axis 3.4 + 5.1
**Demo SHA at diagnosis:** `59b9330` drax/v1.23

The Mirror does not implement; the Mirror sees. This brief surfaces three diagnoses with file:line pointers for drax-side remediation. The work is drax's; the evidence is galadriel's. Drax may consult galadriel on render details mid-fix; galadriel will re-capture and re-score after fix lands.

---

## § 0 — TL;DR

The benchmark report's "portrait viewport CLIPS the demo's actual HUD" (§ 5.1 dissonance, rank 1) decomposes into **three distinct root causes**, each with a specific remediation focus. They are independently fixable; fixing all three would close the rank-1 dissonance.

| # | Symptom | Root cause | File | Severity |
|---|---|---|---|---|
| 1 | Resource (mana) globe invisible; HP globe in mid-screen-left (not bottom-left) | `DiabloHud` uses hardcoded landscape coords captured at module-load before `Mobile.init()` remaps canvas | `src/ui/diabloHud.ts:11-16` | **HIGH** |
| 2 | "Wave 1 of 11" header renders with jagged double-strike | `CombatStatus` places waveLabel (font 13→62pt) and phaseLabel (font 10→48pt) only 17px apart in Y — lines overlap dramatically at mobile font scale | `src/ui/combatHud.ts:830-840` | **HIGH** |
| 3 | TouchHotbar ability buttons "missing" (only cooldown text labels visible) | BG circle fill `0x0a1018` at `0.78` alpha is near-black on near-black scene — circles disappear into background | `src/mobile/touchHotbar.ts:90-94` | **MEDIUM** |

Bonus finding: same `MOBILE_FONT_SCALE` text-overlap pattern as combatHud likely affects the season-selector menu rendering anomaly (§ 6.3 of the benchmark report). Worth checking if `seasonSelector.ts` uses similar tight y-spacing with `font()`.

---

## § 1 — The picture

Three captures bound this diagnosis:

| Capture | What it shows | Relevance |
|---|---|---|
| `captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/capture.png` | Primary state-matched comparison-grade capture at DoE aspect. HP indicator mid-left, NO mana globe visible, "Wave 1 of 11" jagged, ability arc darkness | The eyes that the player sees |
| `captures/2026-05-18/combat-midfight/desktop-1920x1080/capture.png` | Desktop landscape — full 6-skill rail visible, HP+mana orbs at bottom-corners, clean wave header | Reveals the demo's actual HUD architecture |
| `captures/2026-05-18/combat-empty-room/mobile-portrait-1290x2796/capture.png` | Mobile portrait with no enemies — HUD-isolated; element-prefixed cooldown labels ("LIG 19 / WIN 23 …") visible after spells cast | Confirms touchHotbar IS instantiated; cooldown labels readable; BG circles not |

**Comparing primary vs desktop side-by-side:**

The desktop capture shows the demo HAS a substantial, well-designed HUD. The mobile portrait capture is the SAME demo at the SAME SHA but the HUD architecture is materially different — not because of layout intent, but because:

1. One HUD module renders at the wrong coords (the globes — § 2 below)
2. One HUD module overlaps itself (the wave header — § 3 below)
3. One HUD module is visually invisible (the ability arc BG — § 4 below)

The combined effect is that the **portrait-phone player sees a fraction of what the desktop player sees**, even though most of it is already wired and rendering — just rendering wrong.

---

## § 2 — Root cause #1: DiabloHud hardcoded landscape coords

### § 2.1 — The diagnosis

`src/ui/diabloHud.ts:11-16`:

```typescript
const GLOBE_RADIUS = 58;
const GLOBE_Y      = 880;  // center Y for both globes

// HP globe: left side;  Resource globe: right side
const HP_X  = 76;
const RES_X = 1724; // CANVAS_WIDTH - 76
```

These are module-load-time constants. The comment `// CANVAS_WIDTH - 76` is misleading: the value is computed at module evaluation, NOT at construction. At module-load time `CANVAS_WIDTH = 1800` (landscape default) per `src/rendering/stage.ts:11`, even on mobile, because `Mobile.init()` runs **after** import resolution.

After `Mobile.init()` calls `initCanvasDimensions()` (`stage.ts:13-22`), the live-binding `CANVAS_WIDTH` flips to `944`. But `RES_X` is already `1724` — it captured the desktop value.

### § 2.2 — Symptom in capture

At portrait canvas 944×1800:

| Variable | Value | Effect |
|---|---|---|
| `HP_X = 76` | Left edge | ✓ HP globe at x=76 is OK (still within 944px canvas) |
| `RES_X = 1724` | Far right of LANDSCAPE | ✗ **Off-canvas by 780px** (1724 > 944) — resource globe completely invisible |
| `GLOBE_Y = 880` | Bottom of LANDSCAPE | ✗ **Mid-vertical of portrait** (880 / 1800 = 49% from top) — HP globe appears mid-screen, not bottom |

The primary capture shows exactly this: "16890 / 16890 HP" with red bar at mid-screen-left at canvas-y ≈ 880 (scales to viewport-y ≈ 1200 in the 2796-tall 1290 capture). Resource globe nowhere visible.

### § 2.3 — Drax-actionable remediation paths

**Path A — Make positions live-binding (recommended; minimal surface area):**

Change the constants to a getter or to recompute-at-construction:

```typescript
// src/ui/diabloHud.ts
import { CANVAS_WIDTH, CANVAS_HEIGHT } from '../rendering/stage';

// Per gandalf v1.7 § 3.5 guidance for portrait positions (TBD — drax authors):
function hudPositions() {
  const portrait = CANVAS_WIDTH < CANVAS_HEIGHT;
  return portrait
    ? { HP_X: 76, RES_X: CANVAS_WIDTH - 76, GLOBE_Y: CANVAS_HEIGHT - 105 }
    : { HP_X: 76, RES_X: CANVAS_WIDTH - 76, GLOBE_Y: 880 };
}

// In constructor (instead of module constants):
const { HP_X, RES_X, GLOBE_Y } = hudPositions();
```

Effect at portrait (CANVAS_WIDTH=944, CANVAS_HEIGHT=1800):
- HP_X = 76 (unchanged)
- RES_X = 944 − 76 = 868 (now visible at right edge of portrait canvas)
- GLOBE_Y = 1800 − 105 = 1695 (now bottom of portrait canvas, where DoE puts its globes)

**Path B — Pattern-match PotionHud's live-binding approach:**

PotionHud already does this correctly at `src/ui/potionHud.ts:311-312`:

```typescript
this.container.x = 155;
this.container.y = CANVAS_HEIGHT - 105;  // live-binding at construction
```

Adopt the same pattern in DiabloHud.

**Path C — Larger refactor (defer to v2):**

Move all HUD position constants to a centralized `src/ui/hudLayout.ts` keyed on orientation. Higher cost; better long-term coherence; not needed for v1.24 fix.

### § 2.4 — Estimated effort

~20–40 minutes (Path A or B). Single file. Adjacent already-working pattern (PotionHud) to copy.

### § 2.5 — Open question for drax

The gandalf v1.7 § 3.5 portrait guidance defines specific positions for mobile-touch elements (joystick, touchPotions, touchHotbar, etc.). Does it specify where the HP/resource globes should sit in portrait? If so, use those positions verbatim. If not, the bottom-corners convention (x=76/868, y=1695) matches DoE's bottom-corners HP/mana globes register.

---

## § 3 — Root cause #2: CombatStatus wave-header line-overlap at mobile font scale

### § 3.1 — The diagnosis

`src/ui/combatHud.ts:830-840`:

```typescript
constructor(parent: Container) {
  this.container = new Container();
  this.waveLabel = new Text('', new TextStyle({ fill: 0xaabbcc, fontSize: font(13), fontFamily: 'monospace' }));
  this.waveLabel.anchor.set(0.5, 0);
  this.waveLabel.x = CANVAS_WIDTH / 2;
  this.waveLabel.y = 8;

  this.phaseLabel = new Text('', new TextStyle({ fill: 0x556677, fontSize: font(10), fontFamily: 'monospace' }));
  this.phaseLabel.anchor.set(0.5, 0);
  this.phaseLabel.x = CANVAS_WIDTH / 2;
  this.phaseLabel.y = 25;
  ...
}
```

`font(N)` from `src/ui/typography.ts:18`:

```typescript
export function font(N: number): number {
  return Mobile.isActive ? N * MOBILE_FONT_SCALE : N;  // MOBILE_FONT_SCALE = 4.8
}
```

Mobile font sizes:
- `waveLabel`: `font(13) = 62.4pt`
- `phaseLabel`: `font(10) = 48pt`

Y positions:
- `waveLabel.y = 8`
- `phaseLabel.y = 25`

**Spacing between y=8 and y=25 is only 17px**, but the waveLabel's font height alone is ~62pt. The two lines overlap dramatically — the waveLabel renders FROM y=8 down to y~70, and the phaseLabel renders FROM y=25 down to y~73. They cohabit the same vertical band.

This is the "jagged double-strike" artifact in the capture: "Wave 1 of 11" (waveLabel) and "Swarm — Vanguard" (phaseLabel) drawn on top of each other.

### § 3.2 — Symptom in capture

Primary capture shows "Wave 1 of 11" with what appears to be italic-style ghost text drawn through it. That's the phaseLabel ("Swarm — Vanguard" subtitle, fainter color 0x556677) drawn at near-identical Y to the waveLabel.

The desktop capture shows the same modules rendering cleanly: at desktop `font(13) = 13pt` and `font(10) = 10pt`, with 17px Y-spacing they don't overlap.

### § 3.3 — Drax-actionable remediation paths

**Path A — Increase Y spacing on mobile (recommended; minimal surface area):**

Make `phaseLabel.y` proportional to the actual rendered font height:

```typescript
// Use Y-spacing proportional to font size + small gap
const WAVE_FONT  = font(13);
const PHASE_FONT = font(10);
this.waveLabel.y  = 8;
this.phaseLabel.y = 8 + WAVE_FONT + 4;  // wave-font-height + 4px gap
```

At desktop: phaseLabel.y = 8 + 13 + 4 = 25 (current behavior preserved).
At mobile: phaseLabel.y = 8 + 62.4 + 4 ≈ 74 (clears the waveLabel).

**Path B — Use `Mobile.isActive` to branch Y positions explicitly:**

```typescript
this.phaseLabel.y = Mobile.isActive ? 76 : 25;
```

Less elegant; equivalent effect.

**Path C — Reduce font size on mobile for these specific labels:**

The current `MOBILE_FONT_SCALE = 4.8` "compensates canvas-CSS downscale" (typography.ts:11 comment). The scale is correct for *readability* but is too aggressive for the wave-header *layout* given the tight Y-spacing originally designed for desktop. Could expose a `compactFont(N)` variant with reduced scale (e.g., 3.0× instead of 4.8×) for tight-layout labels. Higher complexity; not needed for v1.24.

### § 3.4 — Estimated effort

~10–20 minutes (Path A). Single function. The fix changes Y-positions only; doesn't touch the font-rendering pipeline.

### § 3.5 — Audit recommendation

The same pattern likely affects other tight-spacing UI modules. Galadriel's structured finding § 6.3 (menu-surface rendering anomaly at portrait phone aspect with tile-bleed artifacts) is a strong candidate — `seasonSelector.ts:54` is referenced in the demo's console log on landing (per `landing/mobile-portrait-390x844/capture.json` console_log_tail). Worth a single-file audit: does seasonSelector use `font()` with tight intra-tile Y-spacing? If yes, same root cause.

Audit script suggestion (read-only; drax-runnable):

```bash
grep -n "font(\|MOBILE_FONT_SCALE" src/ui/*.ts | grep -E "font\([0-9]+\)"
# Then for each hit, check the surrounding Y-position assignments
```

This would inventory all font() usages and flag candidates where the gap between adjacent Y-positions is less than the rendered font height.

---

## § 4 — Root cause #3: TouchHotbar background circles disappear into dark scene

### § 4.1 — The diagnosis

`src/mobile/touchHotbar.ts:90-94`:

```typescript
const bg = new Graphics();
bg.beginFill(0x0a1018, 0.78);
bg.lineStyle(isPrimary ? 2 : 1.5, elemColor, isPrimary ? 0.9 : 0.6);
bg.drawCircle(0, 0, BTN_R);
bg.endFill();
ctr.addChild(bg);
```

The BG fill is `0x0a1018` (very dark navy, RGB ≈ 10/16/24) at alpha 0.78. The combat scene's background register is also very dark navy (per benchmark report § 4.1 axis 3.2 — color register cool-cold-in-dark). The two colors are too close in value; against the dark scene, the button BGs are nearly invisible.

The outline (`lineStyle` colored by element) is more visible at 0.6–0.9 alpha but is only 1.5–2px wide. At the BTN_R=42 circle radius, an outline that thin doesn't read as a button-affordance from a viewing distance.

The cooldown labels (white text with high contrast against the dark BG) DO read — which is why the lower-right cluster looks like "floating cooldown numbers" rather than "ability buttons."

### § 4.2 — Symptom in capture

Lower-right number cluster (6.2 / 5 / 11.9 / 6.1 / 8.0 / 0.3) is visible. Looking closely at the arc pattern, the numbers ARE arranged in the touchHotbar arc (slot 0 at bottom-right, slot 5 upper-left of the arc) per `BTN_POS_PORTRAIT` at `touchHotbar.ts:18-25`. But without visible BG circles, the cluster reads as floating text, not button affordances.

### § 4.3 — Drax-actionable remediation paths

**Path A — Increase BG alpha + lighten BG color (recommended):**

```typescript
const bg = new Graphics();
bg.beginFill(0x1a2530, 0.92);  // lighter navy + more opaque
bg.lineStyle(isPrimary ? 3 : 2.5, elemColor, isPrimary ? 1.0 : 0.85);  // thicker outline at higher alpha
bg.drawCircle(0, 0, BTN_R);
bg.endFill();
```

At BTN_R=42, the 92%-opaque larger circle with a thicker accent-colored outline reads cleanly against any background. Element-colored outline (per `ELEMENT_COLORS` map) makes each slot identifiable.

**Path B — Add a subtle drop-shadow / outer halo:**

DoE's bottom skill rail uses a slight outer glow per icon — this is a common ARPG-UI convention that resolves "button on dark scene" visibility. PixiJS has `DropShadowFilter` or a manual halo Graphics layer could add a 4–6px white-low-alpha ring outside the BG circle.

Higher complexity; visual polish. Defer to v2 unless Path A is insufficient.

**Path C — Active/inactive distinction:**

Currently the BG is the same when ability is on cooldown vs ready. DoE convention dims the icon when on cooldown and brightens it when ready. The cooldown overlay (`Graphics`) is present in the code (line 47 `cooldownOverlay`) — it likely handles this already; verify it does, and tune if not.

### § 4.4 — Estimated effort

~10–15 minutes (Path A). Single-file two-line change. Easy to A/B test (just toggle the constants and re-capture).

---

## § 5 — Suggested remediation sequence (drax's call)

For a v1.24 portrait-HUD pass that closes the rank-1 dissonance:

1. **§ 2 DiabloHud globe coords (~30 min)** — highest leverage; the resource globe is currently invisible, the HP globe is mid-screen instead of bottom. Path B (PotionHud pattern) is the cleanest.
2. **§ 3 CombatStatus wave header (~15 min)** — second highest leverage; the wave header is a primary HUD module rendering incoherently. Path A (Y-spacing proportional to font-height) is the cleanest.
3. **§ 4 TouchHotbar BG visibility (~15 min)** — third; cooldown text is readable but button-as-affordance reads better with proper BG contrast. Path A is sufficient.
4. **§ 3.5 audit recommendation (~30 min if action taken)** — single grep + visual scan of seasonSelector.ts and other tight-layout UI modules. May surface the menu-surface rendering anomaly (rubric § 6.3) as the same root cause.

Total estimated wall-clock: **~90 minutes** if all four land in one pass. Each fix is independent — drax can pick subset based on priority.

---

## § 6 — Verification protocol (galadriel side)

After drax's fix lands and a new demo SHA exists:

1. Galadriel re-runs: `node capture.mjs --state combat-midfight --viewport mobile-portrait-1290x2796` (~10s)
2. Galadriel inspects the new PNG side-by-side with both the prior capture and the DoE reference
3. Galadriel re-applies rubric axis 3.4 scoring (typography + UI register); writes updated `scoring.json` at the new demo SHA
4. Galadriel updates the benchmark report's § 4.1 axis 3.4 row to reflect the new score + appends a "remediation pass" note recording the fix
5. Galadriel posts hive log STATE: "axis 3.4 re-scored after drax v1.24 portrait HUD pass; new score=X / aggregate updated"

Drax does NOT need to wait for galadriel re-score before moving on. Galadriel re-scores asynchronously when the new SHA lands; the verification is non-blocking.

---

## § 7 — Open consult points (drax → galadriel)

If drax wants galadriel's eye while implementing:

- **Mid-fix render check.** After fixing § 2 globes, drax can ping galadriel; galadriel re-captures and confirms positioning before § 3 + § 4 land. Useful if drax wants to validate position guesses against the actual rendered output.
- **A/B color choice for § 4 BG.** If Path A's `0x1a2530` doesn't read well, galadriel can test 3–5 candidate colors and visually rank them.
- **Atmospheric layer follow-up.** Rank-2 dissonance from report (§ 5.2 — atmospheric layer loaded but not visibly contributing) is a separate diagnosis path; galadriel can author a second brief if drax wants. Cross-references: `[atmospheric] wired for season=season_002011` console log present at every combat capture's `capture.json`; visible alpha contribution missing. Suspect z-order or alpha tuning.

---

## § 8 — Cross-references

**Galadriel artifacts:**
- Capture set: `agentic_orchestration/galadriel/captures/2026-05-18/`
- Primary scoring: `captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/scoring.json`
- Rubric: `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1.md`
- Report: `canonical/story/visual-benchmark-vs2a-2026-05-18.md` § 4.1 axis 3.4 + § 5.1
- Pipeline: `agentic_orchestration/galadriel/pipeline/` (re-capture in ~10s)

**Demo files referenced (READ-ONLY by galadriel):**
- `src/ui/diabloHud.ts:11-16` — root cause #1
- `src/ui/combatHud.ts:830-840` — root cause #2
- `src/mobile/touchHotbar.ts:90-94` — root cause #3
- `src/ui/typography.ts:11-18` — `MOBILE_FONT_SCALE = 4.8`; `font()` helper
- `src/rendering/stage.ts:10-22` — `CANVAS_WIDTH`/`CANVAS_HEIGHT` live-binding + `initCanvasDimensions()`
- `src/ui/potionHud.ts:311-312` — adjacent already-working live-binding pattern (PotionHud) to copy in § 2 fix

**Demo D11.5 spec:** `src/debug/debugStates.ts` (commit `c039184` drax/v1.22) — galadriel's capture pipeline depends on this; remediation pass should not change the determinism contract.

**Hive-mind protocol:**
- § 6.1 cross-seam coordination
- § 14.1.1 PRE-SIGNAL discipline (galadriel-side commit pattern)

**Agent definition (galadriel):** `.claude/agents/galadriel.md` § Cross-seam coordination — drax-galadriel critique-pair pattern.

---

*Authored 2026-05-18 evening by galadriel per Matt L3 directive. Source-code references are READ-ONLY observations; remediation is drax's seam. Galadriel will re-capture + re-score asynchronously when the new demo SHA lands. The Mirror sees; the smith works the iron.*
