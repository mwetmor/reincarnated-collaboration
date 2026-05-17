# 2026-05-17 — drax-demo — Follow-up UI cleanup + demo-only dodge primitive

**Authority:** Matt L3 disposition 2026-05-17 (focused playtest follow-up after v0.25 polish bundle passed steps 1-5; step 6 surfaced 4 additional asks).
**Type:** Pattern B (long task) — ~1-2 hours estimated (4 small-to-medium items).
**Predecessor:** `drax/v0.25-playtest-ux-polish-bundle-1` (just shipped; all 4 items + Item 5 audit complete).
**Seam:** reincarnated-demo (Pixi.js) — all 4 items are demo-side; no engine, simulation, or loadout work.

---

## Why these matter

Focused playtest 1-5 PASSED with v0.25 polish landed. Step 6 (son's qualitative read) came back **"OK"** with three positive observations (character height vs monsters: much better; movement speed: much better) and three forward asks:

1. **UI text under class name is too crowded.** Archetype + energy-type subtitles are visual noise; remove them. Class name alone is sufficient identity.
2. **HP/energy bars under feet are too prominent.** Shrink them.
3. **No dodge mechanic.** Need a way to evade attacks with VFX (roll/strafe/sprint — Matt is flexible on the exact verb).

Items 1-3 are pure UX. Item 4 (dodge) is a **demo-only quick-win primitive** — the input binding + animation gives son the dodge feel for next playtest. The full engine-side dodge mechanic (i-frames? distance-based? class-coupled?) is a separate canonical design question for gandalf + gamora, deferred to Phase-2 or scope-extended if Matt wants it sooner.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.25 ship STATE + Item 5 OBSERVATION (most recent)
2. `reincarnated-demo/src/visuals/sprites.ts` — your v0.25 changes (DEBUG_DRAW + label y-offsets); Items 1-3 touch this file
3. `reincarnated-demo/src/main.ts` — your v0.25 `_syncUiToScreen()` + the existing Phase 9.3 LMB handler (`_handleLmbClick()` etc.); Item 4 dodge binds alongside LMB
4. `reincarnated-demo/AGENT_STATE.md` — your seam's current state

---

## Scope

### Item 1 (LOW) — Remove archetype text under class name

**Symptom:** subtitleLabel currently renders archetype name (e.g., "fire_mage") below the class name. Matt says this is redundant noise.

**Fix:**
- Locate the `subtitleLabel` (likely in `sprites.ts` per your v0.25 y-offset work)
- Remove the archetype-portion of the subtitle rendering OR remove the subtitleLabel entirely if it serves no other purpose
- **CRITICAL — Pattern P7 preservation:** verify `?mode=perception_test` still suppresses any remaining identity-leak text. If subtitleLabel is removed entirely, perception_test mode behavior is moot (nothing to suppress). If subtitleLabel retains another purpose, ensure P7 still applies.
- Verify in normal mode: class name visible cleanly; no archetype text below

### Item 2 (LOW) — Remove energy type text under class name

**Symptom:** energy-type indicator (e.g., "fire", "lightning") renders below class name as separate text. Matt wants it gone.

**Fix:**
- Locate the energy-type label (may be the same subtitleLabel structure or a separate `energyTypeLabel`)
- Remove it
- Energy type identity is implicitly carried by the class name (which often includes the substrate, e.g., "fire_mage") and by VFX color/sprite — explicit text label is redundant
- Verify in normal mode: only class name visible above character

**Combined Item 1+2 outcome:** above the character, only the class name floats. Nothing else.

### Item 3 (LOW) — Shrink HP + energy bars under feet

**Symptom:** HP/energy bars below character's feet are too prominent; visually noisy.

**Fix:**
- Locate the HP bar + energy bar rendering (likely in `sprites.ts` or a dedicated bar-renderer module)
- Reduce bar dimensions by ~30-50%:
  - Width: ~70% of previous (e.g., if currently 60px, try 40-42px)
  - Height: ~60% of previous (e.g., if currently 6px, try 3-4px)
  - Tune visually until they read as informational but not dominant
- Maintain readability:
  - HP bar still visibly fills/depletes
  - Energy bar still visibly fills/depletes
  - Color contrast preserved
- Verify across chierit characters (sprite size varies; bars should look right on all 10 entity packs)

### Item 4 (MEDIUM) — Demo-only dodge primitive (cosmetic-only)

**Cosmological framing:** ARPG canon includes evasion verbs — D3 evade, D4 dodge roll, PoE flame dash + dash, Last Epoch movement skills, Grim Dawn dash, Lost Ark sidestep, etc. Matt's request ("roll/strafe/sprint whatever") signals flexibility on the exact verb; the gameplay primitive is the load-bearing surface.

**Scope guardrails for this dispatch (HARD):**
- This is **cosmetic-only at the demo layer.** No engine-side mechanic.
- No i-frames (no damage prevention from the dodge)
- No interaction with skill/cooldown system
- No telemetry emission
- No class-coupling, no substrate-coupling, no role-coupling
- Just: input → brief player movement burst → VFX

The engine-side dodge mechanic (i-frames, distance-based, class-coupled, etc.) is a separate canonical design question being routed to gandalf for cosmological framing + gamora for mechanical design. That work happens later (Phase-2 or scope-extension TBD). Do NOT pre-empt that work in this dispatch.

**Fix:**
- Bind input: **Space bar** OR **Right mouse button** OR **Shift+direction** — pick whatever feels most natural alongside the existing Phase 9.3 LMB-click-to-move and any existing keyboard inputs. Avoid binding-collision with hotbar (1-9 keys) or LMB.
  - Recommended: Space bar (universal "do the movement thing" verb in ARPGs; explicit; no chord)
- On dodge input:
  - If player has a current move direction (recent LMB destination, or keyboard direction held): dodge moves the character ~1.5-2x normal-movement-distance in that direction over ~150-250ms (faster than normal walk)
  - If player has no current move direction: dodge in the player's current facing direction
- Cooldown: ~0.5-1.0 seconds (cosmetic-only; no engine validation). Prevents spam without being punitive.
- VFX:
  - **Placeholder is acceptable** — a simple white/colored streak particle trail, a brief sprite-stretch animation, or a Graphics-drawn dash arc. Whatever your seam can ship in <30 minutes.
  - The VFX serves the playtest "this feels good" signal, not visual polish
  - Mark the placeholder VFX as `TODO(drax) — replace with proper dodge VFX after canonical dodge design lands (gandalf/gamora L3)`
- Edge cases:
  - Dodge during cast: **default — interrupt the cast** (cast cancels, dodge happens). Note this is opposite to v0.25's LMB-during-cast behavior; dodge specifically interrupts because it's an evasion verb. If this feels wrong in playtest, surface for revision.
  - Dodge while on cooldown: input ignored (no animation; subtle is fine)
  - Dodge against a wall / out-of-bounds: cap movement at wall; play dodge animation in place (no teleport through geometry)

---

## Out of scope (DO NOT)

- ❌ DO NOT implement engine-side i-frames, damage prevention, or skill/cooldown integration for the dodge — that's a separate larger design question
- ❌ DO NOT modify engine, simulation, or loadout files (this is demo-side only)
- ❌ DO NOT design the canonical dodge mechanic (cosmology, class/substrate coupling, balance) — that's gandalf + gamora
- ❌ DO NOT add monster-density tuning or AOE distribution adjustments — that's a post-D10 regen concern (gamora-side, not demo-side)
- ❌ DO NOT touch the season-pointer update micro-task (`SEASON_IDS` in `src/data/loader.ts`) — that's the next drax-demo dispatch after gamora's pre-D10 regen lands
- ❌ DO NOT extend scope to other UX bugs you notice. Surface as OBSERVATION for the next dispatch.

---

## Acceptance criteria

- [ ] Archetype text under class name removed
- [ ] Energy type text under class name removed
- [ ] Only class name floats above character in normal mode
- [ ] Perception_test mode (`?mode=perception_test`) still suppresses any remaining identity text (P7 verified)
- [ ] HP + energy bars under feet shrunk by ~30-50%; still readable
- [ ] Dodge input bound (Space or your choice); brief movement burst + placeholder VFX on dodge
- [ ] Dodge has ~0.5-1.0s cooldown; no engine integration
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag: `drax/v0.26-followup-ui-cleanup-and-dodge-primitive-1`
- [ ] Hive-log STATE entry + OBSERVATION (any adjacent issues noticed)

---

## Smoke test expectation

Manual visual + interaction smoke:
1. Load demo → class name floats above character; no archetype or energy-type text below
2. HP + energy bars under feet are noticeably smaller; still readable
3. Space (or your dodge-bind key): player does a brief dash with VFX in current direction
4. Spam dodge → cooldown kicks in; no spam
5. Dodge during LMB-move: dodge happens in move direction; movement order canceled
6. Dodge during cast: cast interrupted; dodge happens (opposite to LMB v0.25 behavior; intentional)
7. `?mode=perception_test`: still no identity leak

---

## Math-before-code requirements

N/A — UI cleanup + demo-only cosmetic dodge; no engine math involved.

---

## Tag intent

`drax/v0.26-followup-ui-cleanup-and-dodge-primitive-1` — single-commit ship preferred (one tag for the whole bundle).

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 race-condition discipline gandalf authored). `git fetch origin` first; conflict-check; pull-rebase if concurrent commits.

---

## Follow-up coordination (post-this-dispatch)

When this lands:
- **Drax season-pointer update** is queued for after gamora pre-D10 regen ships (separate later micro-task; ~30 min)
- **Canonical dodge design** is queued for gandalf L3 (Phase-2 or scope-extension TBD)
- **Monster-density + AOE tuning** is queued for post-D10 regen (gamora-side)

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 disposition + Path C sequencing. Estimated 1-2 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-18 by drax
**Commit:** `8fa7573` in reincarnated-demo
**Tag:** `drax/v0.26-followup-ui-cleanup-and-dodge-primitive-1`

### Acceptance criteria status

- [x] Archetype text under class name removed (`_playerSubtitle` now always `''`)
- [x] Energy type text under class name removed (same change — was part of same subtitle string)
- [x] Only class name floats above character in normal mode
- [x] Perception_test mode (`?mode=perception_test`) still suppresses identity text — trivially (subtitle is empty in all modes; P7 satisfied)
- [x] HP + energy bars shrunk ~40-42%; still readable (BAR_WIDTH 160→96, BAR_HEIGHT 12→7, RES_HEIGHT 7→4)
- [x] Dodge input bound (Shift key); brief movement burst + particle trail VFX on dodge
- [x] Dodge has 0.75s cooldown; no engine integration
- [x] Demo build clean (`npm run build`); tsc + vite 520 modules, 0 errors
- [x] Tag `drax/v0.26-followup-ui-cleanup-and-dodge-primitive-1` cut
- [x] Hive-log STATE entry + OBSERVATION appended

### Implementation notes

- Dodge key: Shift (not Space — Space is already hotbar slot 0 via `getAbilitySlotPressed()`)
- Direction priority: lmbMoveTarget vector → WASD-held → face-toward-primary-actor → east fallback
- Cast interrupt: `playerSprite.animState = 'idle'` reset (opposite to LMB v0.25 behavior; intentional)
- VFX: 5 fading circle particles per dodge frame, element-color tinted; TODO(drax) annotated for replacement
- `clearUI()` resets dodge state and destroys trail Graphics objects cleanly

### Follow-up open items (tracked in AGENT_STATE.md)

- Season-pointer update: queued for after gamora pre-D10 regen ships (separate micro-task)
- Canonical dodge VFX + mechanic: queued for gandalf/gamora L3 (Phase-2 or scope-extension TBD)
