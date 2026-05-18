# Galadriel Capture Set — 2026-05-18

**Author:** galadriel (visual-perception steward).
**Pipeline:** `agentic_orchestration/galadriel/pipeline/` v0.1.0 (Playwright 1.49.0; headless Chromium 131.0.6778.33).
**Demo SHA at capture:** `59b9330` drax/v1.23 (D11.5 at `c039184` drax/v1.22 + R2/Vercel hybrid at v1.23).
**Dev server:** `http://localhost:5173` (Vite v?; HMR-current).
**Reference set:** `../reference-images/MANIFEST.md` (7 Matt-captured DoE frames).
**Rubric:** `../rubrics/2026-05-18-rubric-doe-comparison-v1.md` (v1-DRAFT).

---

## What this set is

Nine captures across three states × four viewports. Every capture has a JSON sidecar at `<state>/<viewport>/capture.json` with full provenance (demo SHA, console log tail, friction notes, wait_for diagnostics).

| State | Viewport | DoE ref | Comparison-grade? | Friction |
|---|---|---|---|---|
| `combat-midfight` | `mobile-portrait-1290x2796` | `DOE-combat-whisper-rift-2-2026-05-17.png` | **YES — PRIMARY** | none — `wait_for_satisfied: true` |
| `combat-midfight` | `mobile-portrait-390x844` | (cross-viewport check) | secondary | none |
| `combat-midfight` | `mobile-portrait-375x667` | (cross-viewport check) | secondary | none |
| `combat-midfight` | `desktop-1920x1080` | (non-DoE context) | secondary | none |
| `combat-empty-room` | `mobile-portrait-1290x2796` | (HUD-isolated cross-check vs DoE HUD modules) | HUD-only | none |
| `combat-empty-room` | `mobile-portrait-390x844` | (HUD-isolated cross-check) | HUD-only | none |
| `landing` | `mobile-portrait-1290x2796` | none (no DoE menu ref) | finding-only | none |
| `landing` | `mobile-portrait-390x844` | none | finding-only | none |
| `landing` | `desktop-1920x1080` | none | finding-only | none |

`inventory-open` state captures were NOT produced tonight — no DoE inventory reference in current 7-image set; defer to Phase-2 when reference is added.

---

## Demo state at capture time

Per D11.5 determinism contract (`src/debug/debugStates.ts`):

- **Season:** `season_002011` (first in SEASON_IDS)
- **Class:** `Wall-Shocked Smuggler` (lightning_mage, mana-resource) — first playable class for the season
- **Wave:** 1 of 11 (label: "Swarm — Vanguard"; 8 Pitchwall Crusher monsters in pack)
- **HP/Mana:** 16890 / 16890 HP; mana segmented
- **Aggro:** activated before first tick per spec
- **Atmospheric pack:** `clima_niebla_espesa` loaded for season_002011
- **Floor tileset:** `plates.png` (P1 swap; 104 floor tile variants)
- **Stair texture:** loaded from Objects.png (P2 primary)
- **Frostwindz physical:** 5 slashes + 5 impacts prewarmed
- **Pimen VFX:** 6 element-specific spell-effect packs loaded (fire / water / wind / earth / thunder / ice)

**Capture-timing observation (Discipline #8 surface):** The lightning_mage class is **fast-clearing** on wave 1 — by the `warmup_ms: 2500` capture moment, the wave has progressed from 8 alive to 1 alive (`alive=1 dead=7` in the wave:diag log). Captures land in **late-midfight**, not early-midfight. This is a deterministic outcome of the class+wave matchup, not a randomness issue. Surfacing as advisory to drax/D11.5 spec: future state design might consider reducing class DPS in debug-state init, OR spawning a slower-clearing enemy class for combat-midfight, OR adding a `combat-midfight-paused` variant for capture-stable scenes. Not a sprint-night blocker; rubric scoring proceeds with late-midfight captures.

---

## Per-capture observations (descriptive; not scored)

Survey-mode observations only — per agent-definition § Cross-cutting rules, descriptive findings are separated from scored axes (which live in the rubric scoring artifacts).

### combat-midfight × mobile-portrait-1290×2796 (PRIMARY)

What the picture shows:
- Top: 2 small circular HUD icons top-left (gold-bordered avatar + blue-bordered icon), "Wave 1 of 11" centered (text rendering with jagged overlap / double-strike artifact), top-right circular icon (gold-bordered)
- Mid-band upper: 2 tiny monster sprites (gold + red small figures, possibly off-camera tier indicators)
- Mid-band: player avatar (small, blue/yellow robed figure, lightning_mage), "-Shocked Smuggler" floating label **clipped on left edge**, "16890 / 16890 HP" numeric stack with red horizontal bar + cyan-green segmented bar below
- Mid-band lower-right: one enemy with red HP-ring + blue particle aura, second enemy with red HP-ring directly below
- Lower-right: cluster of floating numbers `6.2 / 5 / 11.9 / 6.1 / 8.0 / 0.3` (these are skill-cooldown countdowns visible because the portrait viewport is clipping the skill rail to a vertical sliver at the right edge)
- Vertical red and blue rectangles (potions; bottom-right area)
- Bottom: gray joystick circle (left), small "C" indicator (mid), red+blue potion pair + "[Q]E" hotkey label (bottom-left)
- Background: dark navy-to-black; subtle floor texture barely visible; minimal atmospheric-layer presence despite `clima_niebla_espesa` loading per console
- NO visible AOE telegraph; NO objective banner; NO minimap; NO "killed counter"; NO level XP bar; NO healing button

### combat-midfight × desktop-1920×1080 (context capture)

What the picture shows — markedly different framing:
- Top-left: 3 icons (INVENTORY, character-sheet, etc.) with hotkey labels visible (`[B]`, `[V]`, `[I]` or similar)
- Top-center: "Wave 1 of 11" + subtitle (faintly visible: "Swarm — Vanguard"?)
- Top-right: horizontal slim indicator
- Mid: player (lightning_mage with staff, blue/yellow robes), "Wall-Shocked Smuggler" name label LEFT of player, HP/mana bars BELOW player
- Mid-right: 7-8 enemy sprites in curved arc formation with HP rings (Pitchwall Crushers visible); pink/magenta impact effect mid-scene
- Bottom-left: 3 round status icons (red HP orb with `16890 / 16890`, blue potion, gray)
- Bottom-center: **6 skill cooldown slots in a horizontal rail** numbered 2-6 + "SPC" key, with countdown numbers visible: `0.3 / 8.1 / 6.3 / 11.9 / 9.6 / 6.2`
- Bottom-right: blue orb with `90 / 270` (mana)
- The demo has substantially more HUD architecture than the portrait viewport reveals — the portrait viewport is **clipping the skill rail + side orbs**

### combat-empty-room × mobile-portrait-1290×2796

What the picture shows:
- Same top HUD as combat-midfight (HUD modules consistent)
- Mid: player + "-Shocked Smuggler" label + HP/MP — same as combat-midfight
- Lower-right: floating element-name labels with cooldown numbers visible (`LIG 19 / LIG 22 / WIN 23 / LIG 29 / LIG 18 / LIG 13`) — these are skill cooldown indicators after spell casts; element-prefixed
- NO visible enemies (room is genuinely empty)
- NO visible AOE telegraph; no combat effects
- The "empty room" delivers what its name says — useful for typography/UI register HUD-isolated comparison

### landing × all viewports

See rubric v1-DRAFT § 6.3 finding — menu surface renders clean at desktop, breaks at portrait phone aspect with tile-overlap artifacts. Pre-D11.5 captures; included for completeness.

---

## Key descriptive observations across the set

1. **Demo HUD architecture is substantial — but portrait phone viewport clips it.** The desktop 1920×1080 capture reveals 6 skill cooldown slots + HP/mana orbs + inventory buttons. The portrait 1290×2796 capture clips most of this. This is **its own finding** — not a register dissonance but a **viewport-fit issue** at the DoE-matched aspect.

2. **Text rendering at portrait phone viewport shows artifacts.** The "Wave 1 of 11" header renders with jagged overlap / double-strike (also observed at the season-selector menu — same bug family). The "-Shocked Smuggler" name label clips on the left edge. Pre-D11.5 landing-state finding (§ 6.3 of rubric) extends into the combat state.

3. **Atmospheric layer loaded but not visibly contributing.** Console logs confirm `clima_niebla_espesa` loaded (and 6 other atmospheric packs prewarmed). The captures show a near-empty dark background with no visible mist/fog/atmospheric haze. Either the layer renders at very low alpha, or it's behind another layer, or it's not in the viewport's coverage area. Surface as drax-actionable.

4. **Floor tileset (plates.png) barely visible.** Console confirms `104 floor tile variants` loaded. The mid-band shows extremely subtle floor texture; the rest of the scene is near-black. Drax's v1.18.6 disabled decorative props per Matt L3 ("DoE has decorative-free dungeons"); the resulting scene is comparably sparse but **also lacks DoE's ground detail** (blood, debris, crimson texture).

5. **Color register is COOL not WARM.** DoE combat ref reads dark-brown + crimson + warm-red-orange. Demo combat reads dark-navy/black + cool-blue particles + white text. The demo is *cold lit volume* vs DoE's *warm lit volume*. This is the loudest single dissonance and merits drax + gandalf interpretation.

6. **Fast-clearing capture-timing issue.** Lightning_mage at wave 1 = capture lands at late-midfight (1 of 8 enemies remaining). Future iterations might want a `combat-midfight-paused` debug-state variant for capture-stable comparison scenes.

---

## Cross-reference

- Rubric: `../rubrics/2026-05-18-rubric-doe-comparison-v1.md`
- Reference manifest: `../reference-images/MANIFEST.md`
- Dispatch (capture pipeline): `agentic_orchestration/dispatches/2026-05-18-galadriel-capture-pipeline-and-state-matched-captures.md`
- Dispatch (benchmark report): `agentic_orchestration/dispatches/2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md`
- DoE feel-target canon: `canonical/story/mobile-feel-target-doe-2026-05-17.md`
- D11.5 spec: `~/Games/reincarnated-demo/src/debug/debugStates.ts`

---

*Authored 2026-05-18 by galadriel after D11.5 gate opened (drax/v1.22 + v1.23). The Mirror has captured the picture. Scoring follows.*
