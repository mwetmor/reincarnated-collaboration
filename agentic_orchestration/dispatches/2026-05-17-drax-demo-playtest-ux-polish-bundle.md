# 2026-05-17 — drax-demo — Playtest UX polish bundle (4 fixes + 1 investigation)

**Authority:** Matt L3 disposition 2026-05-17 — playtest-blocking UX bugs + season-data-staleness audit surfaced during pre-perception-test smoke.
**Type:** Pattern B (long task) — ~2-4 hours estimated, depending on what discovery surfaces in items 1 + 3 + 5.
**Seam:** reincarnated-demo (Pixi.js) — all 5 items are demo-side; no engine or loadout work.
**Cross-seam impact:** Item 5 audit may trigger a downstream gamora dispatch for fresh standard-demo season regen.

---

## Why these matter

Matt is preparing to run live playtests (perception-test sessions + general demo runs). The 4 items below are surface-level bugs that interfere with **his and his son's ability to actually play the build.** Without these fixes:
- Skill hotbar (Item 1) becomes invisible on map transitions → player can't see cooldowns/skills
- Missing LMB movement (Item 2) → every ARPG player's muscle memory is broken; movement requires non-standard input
- Vestigial debug geometry (Item 3) → visual noise on character; perception-test risk (substrate-coherence reads less clean)
- Archetype text overlapping character (Item 4) → readability + visual polish

These do NOT block the D27 perception-test runner infrastructure (already shipped); they make the *underlying demo* usable for testing.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — most recent STATE entries (your D27 final integration entry + post-D3 hive state)
2. `reincarnated-demo/AGENT_STATE.md` — your seam's current state (v0.23 perception-test integration + v0.23 sub-phase A extraction)
3. `reincarnated-demo/scripts/perception-test-runner/README.md` — the `?mode=perception_test` Pattern-P7 substrate-suppression wiring you authored in D27 (Item 4 must not break this)
4. `reincarnated-demo/src/main.ts` — bootstrap; you added the perception_test mode wiring here in D27
5. Whatever PIXI scene-graph / UI-overlay / input-handler modules are conventional in your repo (you know your seam; this dispatch doesn't prescribe file paths)

---

## Items (4)

### Item 1 (HIGH) — Skill hotbar must always stay pinned to the screen bottom

**Symptom Matt reports:**
> *"Skill hotbar locks in place on map 1 and then goes out of screen so I cannot see the skills."*

**Likely root cause:** Hotbar rendered as a world-coordinate child of a scene/map container rather than as a UI overlay anchored to the viewport. When the camera follows the player across map transitions, the hotbar stays at world position (0,0)-ish and scrolls off-screen.

**Fix:**
- Move the skill hotbar into a screen-space UI layer (typically a Pixi `Container` that is NOT a child of the world/camera container — instead a sibling at the stage root, with absolute screen-position).
- Anchor the hotbar to viewport bottom (typically `app.screen.height - hotbarHeight - padding`).
- Re-anchor on `resize` events (handle browser-window resize gracefully).
- Verify the hotbar renders consistently across:
  - Map 1 boot state (immediately visible)
  - Map 1 movement (does not scroll off)
  - Any map transitions (if multi-map exists)
  - Window resize

### Item 2 (HIGH) — Left mouse button: click-to-move + click-enemy-to-attack

**Symptom Matt reports:**
> *"Please add left mouse button click for movement (or lowest cooldown attack if clicking an enemy)."*

**Cosmological framing:** ARPG canon (D2 / D3 / D4 / PoE / Last Epoch / Grim Dawn). Left-click is the universal "interact with where I just pointed" verb. On empty ground = move. On enemy = primary attack.

**Fix:**
- Add a global LMB input handler scoped to the world-canvas (NOT to UI elements — don't intercept hotbar clicks, skill-button clicks, or dialog clicks).
- LMB on empty ground tile:
  - Issue a move-to-position order. Use whatever pathfinding/move-target system already exists (your seam knows its mover; this dispatch doesn't prescribe).
- LMB on enemy entity:
  - Identify the player's lowest-cooldown attack skill (typically index 0 of the hotbar, or whatever convention the demo uses for "primary"). If multiple skills are tied for lowest CD, pick the first.
  - Issue an attack-target order with that skill.
- Coexistence guarantees:
  - Existing keyboard movement (WASD or arrow keys, if present) must continue to work
  - Existing skill hotbar bindings (1-9 keys or whatever) must continue to work
  - LMB on UI elements (hotbar buttons, menu items) must remain UI-clicks, not world-clicks
- Edge cases to handle:
  - LMB held / dragged → continuous-move? **Default:** treat as click-to-point (release-on-up = re-issue order). Do not implement hold-to-move unless the existing input system already does so.
  - LMB while player is mid-cast → queue the new order vs interrupt? **Default:** finish the current cast, then issue the new order (no interrupt). If existing system has different convention, match it.
  - LMB on an out-of-range enemy → move toward the enemy, then attack when in range. **Default:** if your existing mover supports "approach then act," use it; if not, ship as "move to enemy position; player must click again when in range."

### Item 3 (MEDIUM) — Remove vestigial debug-drawn aura circle + weapon

**Symptom Matt reports:**
> *"Please remove vestigial geometrically drawn aura circle around character and geometrically drawn weapon."*

**Root cause:** Pre-VFX-pipeline placeholder shapes from early dev. Both are `Graphics`-drawn primitives (circle around feet for "aura"; some geometric shape for "weapon" attached to character). They predate the chierit character-sprite ingestion (v0.18+) and the v0.23 perception-test integration.

**Fix:**
- Locate the Graphics-drawn aura circle (likely in `Character` / `Player` / `Entity` render code; look for `.drawCircle()` or `.beginFill()` / `.endFill()` calls around character spawn or render-update)
- Locate the Graphics-drawn weapon (likely a child sprite/graphics attached to the character; may be conditional on `weapon_type` or `archetype`)
- Remove both. Either delete the code paths cleanly OR gate them behind a `DEBUG_DRAW = false` constant for easy reactivation if needed for diagnostics
- Verify character renders cleanly with only the sprite (chierit or otherwise) + any planned VFX overlay
- Confirm no test or perception-test runner code references these primitives

### Item 4 (MEDIUM) — Archetype text floats above character, not on top

**Symptom Matt reports:**
> *"Ensure class name/archetype text floats above character and not on top of character."*

**Likely root cause:** Text sprite is positioned at character's anchor point or center, instead of with a y-offset above the sprite's top.

**Fix:**
- Locate the archetype/class-name text rendering (often labeled `subtitle`, `nameplate`, `archetype_label`, or similar)
- Apply y-offset so text renders above the character sprite's top edge:
  - Typical offset: 8-16 pixels above sprite top (depending on sprite size)
  - Center horizontally on the character (text anchor 0.5)
  - Account for sprite height variation across chierit characters (use the sprite's actual rendered height, not a hardcoded constant)
- **CRITICAL — Pattern P7 substrate-suppression preservation:** In D27 you wired `?mode=perception_test` to suppress this text to empty string. **DO NOT** un-suppress it when fixing positioning — the suppression must remain when perception_test mode is active. The positioning fix applies to **normal mode** (subtitle visible); in perception_test mode the subtitle stays empty regardless of position.
- Verify in both modes:
  - Normal mode: text visible, floats above character
  - Perception-test mode: text remains empty (substrate not leaked to subject)

### Item 5 (HIGH-priority investigation; not a code fix) — Season-data freshness audit

**Symptom Matt reports:**
> *"Am I supposed to see the old archetypes and old classes/abilities? Or the new archetypes from the new engine and new skills? It looks like I still see wind-caster, hybrid mage, rogue. I didn't expect to see those old substrates and structures."*

**Knight-rider hypothesis (high confidence):** The demo is loading season data produced by a **pre-D3 engine snapshot** (i.e., a season JSON generated before commit `048611a` landed on engine main). Gamora D3 shipped the canonical-7 substrate expansion + Path-a archetype composition refactor today — 11 new substrate-role tags landed (`lightning_mage`/`lightning_caster`/`lightning_controller`, `holy_mage`/etc., `shadow_mage`/etc., plus `earth_burst` + `wind_burst`). These will NOT appear in Matt's current demo session because the season JSON predates them.

Separately, `hybrid_mage` and `rogue` are **PRESERVED by D3 design** — they live in `_HYBRID_ARCHETYPE_TEMPLATES` + `PHYSICAL_ARCHETYPE_TEMPLATES` and are explicitly retained. They will continue appearing in post-D3 seasons too. That preservation behavior is correct per the math contract; Matt may want gandalf to weigh in on whether `hybrid_mage` should be retired cosmologically, but that's a separate L3 question outside this dispatch.

**Investigation actions (NO CODE CHANGES in Item 5):**

- Identify the exact file path(s) the demo loads season data from at boot (likely a JSON at `public/data/`, `public/seasons/`, `src/assets/`, or similar — your seam knows)
- Inspect the season JSON file's metadata for any of:
  - `engine_version` field
  - `engine_git_sha` field
  - `generated_at` timestamp
  - Any other provenance markers
- Enumerate the full archetype roster present in the current season:
  - List every `archetype_tag` value found in the season's class/character entries
  - Highlight any of: `lightning_*`, `holy_*`, `shadow_*`, `earth_burst`, `wind_burst` → present or absent?
  - Note any `hybrid_*` or physical archetypes (`rogue`, `warrior`, `knight`, etc.) present
- Cross-reference against the post-D3 archetype set (per gamora's D3 HANDOFF: 21 substrate-role pairs + 5 physical + hybrid = 25 templates; 18 distinct elemental tags after burst/area alias collapse):
  - Expected post-D3 elemental tags: `fire_mage`, `fire_caster`, `fire_controller`, `water_mage`, `water_caster`, `water_controller`, `earth_burst` (was `earth_mage`), `earth_caster`, `earth_controller`, `wind_burst` (was `wind_mage`), `wind_caster`, `wind_controller`, `lightning_mage`, `lightning_caster`, `lightning_controller`, `holy_mage`, `holy_caster`, `holy_controller`, `shadow_mage`, `shadow_caster`, `shadow_controller`
  - Expected preserved: `hybrid_mage` + physical archetypes
- Author findings as STATE entry in hive log AND as `OBSERVATION — drax-demo → knight-rider — season data freshness audit` block answering:
  - **Q1:** What season file is the demo loading? (path + size + timestamp)
  - **Q2:** What engine version/SHA produced it? (from metadata, or "unknown / no provenance markers")
  - **Q3:** Are any post-D3-introduced archetype tags present? (binary yes/no per tag)
  - **Q4:** What's the path forward for the demo to consume a fresh post-D3 season? (e.g., "demo loads `public/data/season_XYZ.json`; needs gamora to regen + drax to update pointer" OR "demo loads live from engine API; needs engine update")

**Out of scope for Item 5:** Do NOT generate a new season yourself (that's gamora's seam). Do NOT update the season-pointer file (that's a follow-up dispatch after gamora regens). Investigation + reporting only.

**Why this is HIGH-priority:** Matt is preparing to play the build now. If the demo is on stale content, he's testing the wrong engine snapshot — perception-test results would be meaningless, and his impressions of "do the new substrates feel right" would be answered by absent evidence. Item 5 unblocks the next decision (do we need a fresh full-season regen now, or is the demo already on post-D3 data and Matt's confusion is about preserved templates?).

---

## Out of scope (DO NOT)

- ❌ DO NOT modify engine or loadout files (this is demo-side only)
- ❌ DO NOT modify D27 perception-test runner's `ARCHETYPE_SLOTS`, `runner.html`, or `runner.js` (Item 4 must preserve the existing P7 wiring; touching the runner itself is out of scope)
- ❌ DO NOT wire holy combat VFX from the newly-on-disk CreativeKind Holy Spell Effects pack (that's a separate VFX-wiring dispatch; here you're only removing vestigial debug-drawn primitives, not adding new VFX)
- ❌ DO NOT add NEW gameplay systems (e.g., do not add hold-to-move, force-attack modifier, or any input pattern beyond Item 2 spec). Match existing conventions or default to the dispatch's specified behavior.
- ❌ DO NOT extend scope to other UX bugs you notice during this work. Surface them as OBSERVATION entries in hive log for the next dispatch. Single-purpose ship.

---

## Acceptance criteria

- [ ] Skill hotbar always visible at viewport bottom; survives map transitions + window resize
- [ ] LMB on empty ground = move-to; LMB on enemy = lowest-CD primary attack; existing keyboard inputs continue to work
- [ ] Vestigial debug aura circle removed; vestigial debug weapon removed; character renders with sprite only (+ planned VFX overlay if any active)
- [ ] Archetype text floats above character with appropriate y-offset; perception_test mode P7 suppression preserved
- [ ] `npm run build` clean (tsc + vite); existing demo tests pass
- [ ] No console errors on demo boot or during typical play (move, attack, map transition, window resize)
- [ ] Tag: `drax/v0.25-playtest-ux-polish-bundle-1` (seam-prefixed; intermediate)
- [ ] Hive-log STATE entry appended summarizing all 4 fixes + any OBSERVATION entries for adjacent bugs you noticed but left out of scope

---

## Smoke test expectation

Manual visual smoke against a running demo session. Operator script:

1. `npm run dev` (or your seam's dev-server command)
2. Open browser → demo loads
3. **Hotbar check:** hotbar visible at bottom; move player around; hotbar stays put
4. **LMB check:** LMB on empty space → character moves there; LMB on enemy → character attacks with primary; both work alongside any existing keyboard inputs
5. **Vestigial-geometry check:** no aura circle around character; no geometric weapon shape; character is clean sprite
6. **Archetype-text check:** in normal mode, text floats above character; in `?mode=perception_test`, text is empty (P7 preserved)
7. Window resize → hotbar re-anchors correctly; no layout break
8. Browser console: no errors

Record findings in hive-log STATE entry.

---

## Math-before-code requirements

N/A — UI/UX work; no engine math involved.

---

## Tag intent

`drax/v0.25-playtest-ux-polish-bundle-1` — single-commit ship preferred (one tag for the whole bundle). If item-level commits land separately, tag the final one.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 race-condition discipline gandalf authored this session). `git fetch origin` first; conflict-check; pull-rebase if concurrent commits.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 disposition. Estimated 2-4 hours. Append completion record when done.*
