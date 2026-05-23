# Mobile feel target — Dungeon of Exile (DoE) anchor

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authored:** 2026-05-17 by gandalf, immediately following Matt's 15-minute play session of Dungeon of Exile and gameplay screenshot capture.

**Status:** Canonical reference for mobile feel; amendable as Matt plays more DoE (or other cluster titles) and reports new observations.

**Companion artifacts:**
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — sizing-ratio canon
- `canonical/story/arpg-map-overlay-research-2026-05-17.md` — map overlay design (PC-anchored)
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — drax v1.6 execution plan (now amendment-pending per § 7)
- `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — narrow-slice combat model
- `canonical/story/vs2a-vfx-scene-needs.md` — locked visual register (HYBRID a3)
- `../DOE.png` — gameplay screenshot (Matt 2026-05-17 15:56)

---

## § 0 — TL;DR

Dungeon of Exile (DoE) is the closest mobile-ARPG cluster reference for what Reincarnated mobile should feel like. Matt's 15-minute play session + the gameplay screenshot together identify **five design principles** the genre-cluster has converged on for mobile and that Reincarnated should adopt:

1. **Combat is positioning + dodge, not input frequency.** Skills are cooldown-driven; auto-attack handles most damage output; player skill = movement and threat-reading.
2. **Loot flows through the player, not into them.** Auto-pickup, auto-compare, one-tap equip. Inventory management is a *between-combat* surface, not a *during-combat* surface.
3. **React-or-auto interaction.** Environmental interactions surface as pop-up affordances with auto-completion fallback if the player doesn't react fast enough.
4. **Single healing affordance, cooldown-based.** No potion inventory; one large "Healing" button on cooldown.
5. **UI is sparse during combat; surfaces only the things the player must read.** Inventory hidden; chat hidden; resource bars where they're glanceable; objective counter visible.

**Locked decisions confirmed via this doc:**
- Mobile orientation = **portrait primary** (DoE is portrait-only).
- Healing potions = **cooldown ability on both PC and mobile** (consistency).
- Inventory modal serves **inspect-and-equip**, not active management (per § 6 of decision-batch 2026-05-17).
- Telegraphed AOE + dodge narrow-slice direction = **strongly validated** (DoE uses near-identical rectangular telegraphs).

**Forward-flagged design questions** (not blocking; surface in mobile commission):
- HP placement: minimap-anchored (DoE pattern) vs separate HP globe (D-series)
- Touch-targeting design (replaces retired enemy-cycle)
- Skill auto-cast vs tap-cast split (which of our skills are manual?)
- React-or-auto affordance pattern specification
- Trial-room "X killed" objective-counter UI pattern

---

## § 1 — Sources

### § 1.1 — Matt's play-session paragraph (verbatim)

> DOE is not played wide-screen (horizontal), it is played vertically. It understands that you can't really press a lot of buttons on mobile, so everything is auto-attack with cooldowns. The game is all about building the right skill and gear combinations and finding loot. The gameplay is ultra-fast and the on-the-battlefield skill is dodging and avoiding telegraphed attacks and not getting boxed into monster swarms. You don't click and interact with anything. Even the gear pops up automatically if it is a higher power level and you just click to add it to your character without losing a beat during battle. I should say you do interact with some elements of the battlefield but it is with a pop-up hand/finger button and it auto-clicks if you don't click it faster than it auto-opens the chest for you. Maybe some of the skills are on-click, but I did not run into any within 15 minutes of play. Also, the health potions are on cooldown so you don't have to worry about managing tons of inventory items.

### § 1.2 — Screenshot (`../DOE.png`)

Portrait-orientation gameplay screenshot. Scene: rift content (`[EASY] Whisper Rift 2`); 5+ enemies visible; player mid-combat with cape/shield warrior class; telegraphed AOE rectangle on ground; damage numbers floating; "55 killed" objective counter; healing potion bottom-right.

---

## § 2 — Screen anatomy (from screenshot, annotated)

### § 2.1 — Top-of-screen region

| Element | Position | Function | Reincarnated-relevant |
|---|---|---|---|
| Rift name banner | Top-left | `[EASY] Whisper Rift 2` — difficulty + zone label | Yes — trial-room naming pattern; our `season_NNNNNN` ID is internal, player-facing name should match this energy ("Whisper Rift" >> "Season 1005") |
| Corner minimap (route preview) | Top-left, attached to rift banner | Shows path-from-here to objective + player position marker | Yes — confirms DoE bundles map + objective navigation in one corner module |
| Timer | Below minimap | `00:41` elapsed time | Yes — trial-room timer is genre-canonical for rift content |
| HP bar | Below timer (part of rift module) | Player HP rendered horizontally, attached to minimap module | **Notable departure from D-series.** HP is part of the navigation module, NOT a separate globe. Forward-flagged as mobile design question. |
| Boss skull icon | Right of HP bar | Indicates a boss/elite is in-zone | Yes — affordance for "there is a boss here; track it" |
| Return-to-city portal | Top-right | Large circular icon, "Return to City" label | Yes — single-tap recall affordance |

### § 2.2 — Mid-screen / combat region

| Element | Visual signature | Function |
|---|---|---|
| Player character | Centered, ~1/8 viewport tall, painterly | Cape, shield, white-hair — paladin-class shape; raster-painterly visual register (matches our HYBRID a3 lock) |
| Enemies | Top of frame, 5+ visible | Wolves + armored humanoids + (off-left) shadow-substrate cluster with purple smoke; thin red HP bars above each |
| Telegraphed AOE | Red rectangle on ground, right of player | Hard-edged red fill; rectangular geometry; identical to our engine's `geometry_type: rectangular_aoe` |
| Damage numbers | Floating in scene | `22` orange (large), `15` white (smaller), `-3` red (player taking damage); color-coded by source/type |
| Status text | Below damage cluster | `Slow` in blue — status-effect surface |
| Resource bar (player) | Above player sprite | Green/blue horizontal bar — mana/resource overhead-attached, NOT in HUD |
| Movement reticle | Below player, large grey circle | Just-tapped move-target indicator (tap-to-move confirmed); fades after arrival |
| Blood splatter | Ground around combat | Visceral combat-aftermath VFX; persists ~2-5 seconds |

### § 2.3 — Bottom region

| Element | Position | Function | Reincarnated-relevant |
|---|---|---|---|
| Character portrait | Bottom-left corner | Lv 5 player avatar, circular frame, **red-dot notification** | The red-dot is the "loot/level-up available" affordance — Matt's "click to add it to your character without losing a beat" |
| Chat bubble | Above portrait | System messages | Minimal — no chat input field visible during combat |
| Compass triangle | Above chat bubble | Directional/recall affordance | Lower-priority UI |
| Currency display | Bottom-center-left | `3` (red gem) + `165` (green gem) — premium + soft currency | Small, non-intrusive |
| Skill bar | Bottom-center | 5 numbered slots; only slots 1 + 2 filled (icy + wind skill icons) | **Confirms most damage is auto-attack; few manual skills.** |
| Ultimate / special button | Bottom-right-of-skillbar | Large blue/gold circular spell icon | The "high-commitment skill" Matt called out |
| Healing potion | Bottom-right corner | Large red potion bottle, **"Healing" label**, single button | **Single potion, cooldown-based.** No row of potion types. |
| "55 killed" counter | Bottom-mid, above skill bar | Objective progress + horizontal rope/progress bar | Trial-room objective UI |
| XP bar | Full-width bottom edge | `Level 5` left, `Lv.5` center marker, `79%` right | Persistent progression visibility |

### § 2.4 — Notable absences

- **No virtual joystick.** Movement is tap-to-move (Diablo-canonical).
- **No inventory icon during combat.** Loot equipping is a red-dot-on-portrait affordance, not a dedicated button.
- **No party UI.** Solo confirmed.
- **No chat input field.** System-message-only.
- **No HP/MP globes in the bottom-corner Diablo-canonical positions.** HP is top-left; mana is overhead-on-player.
- **No targeting reticle on enemies.** Auto-target (or positioning-IS-targeting per Matt's paragraph).

---

## § 3 — Combat loop pattern

Synthesizing Matt's paragraph + screenshot evidence:

### § 3.1 — Input vocabulary

| Action | Input |
|---|---|
| Move | Tap on ground (move-to-target) |
| Auto-attack | Continuous on nearest enemy; player does not initiate |
| Skill 1 / 2 | Tap skill icon (when filled and off cooldown) |
| Ultimate | Tap right-side big button |
| Heal | Tap healing-potion button (cooldown-gated) |
| Equip loot | Tap red-dot character portrait |
| Environmental interact | React to pop-up hand-button OR auto-completes |

**Total input frequency:** Very low. Player taps movement most; skills tap rarely; heal taps when needed; equip taps when red-dot appears.

### § 3.2 — Threat model

The player's during-combat cognitive load is:

1. **Read terrain + enemy positioning** ("don't get boxed into monster swarms" — Matt)
2. **Read telegraphed AOE indicators** ("dodging and avoiding telegraphed attacks" — Matt; see red rectangle in screenshot)
3. **Path movement to safe ground** (tap-to-move; auto-attack handles damage)
4. **Tap skill on cooldown** when offensive-window opens (skills 1-2 + ultimate)
5. **Tap heal** when HP threatens
6. **Tap red-dot on portrait** when loot upgrades available (between dodges)

The **highest-frequency, highest-skill-ceiling action is movement.** Everything else is opportunistic taps.

### § 3.3 — Pace

Matt: "ultra-fast." Screenshot supports: 5+ enemies converging on player; multiple damage numbers overlapping; red AOE telegraph in-frame; "55 killed" in ~41 seconds = ~1.3 kills/second clear rate. This is **higher pace than D2/D3/D4 PC pace**, comparable to **Diablo Immortal's rift pace.**

### § 3.4 — Implication for Reincarnated

Our current combat-pace lock from the AOE-tuning briefing is **medium-to-high**. DoE confirms the mobile pacing target should be **high-end medium**, with positioning as the primary skill expression. The narrow-slice dodge + telegraphed-AOE work is exactly tuned for this.

---

## § 4 — Loot and progression flow

Matt's paragraph contains a complete loot-flow specification we should adopt as canonical:

### § 4.1 — Auto-pickup

- All ground drops auto-pickup as the player moves over them.
- **Triggering criteria for surface-to-player:** "higher power level than currently equipped."
- Lower-power-level drops: filtered silently; do not interrupt the player.

### § 4.2 — Auto-compare

- Newly-acquired upgrades trigger a "click to add" affordance (per Matt: red-dot on portrait in screenshot).
- The comparison is pre-computed; the player does not browse inventory mid-combat to decide.

### § 4.3 — One-tap equip

- Tap red-dot → item equips → red-dot clears.
- Player loses no beat in combat.
- Old item is auto-vended or auto-vault'd (DoE behavior unclear from 15-min session; **forward-flag for follow-up**).

### § 4.4 — Inventory as inspect-surface

- The player visits inventory between combats to:
  - Inspect equipped gear in detail (affixes, set bonuses)
  - Manually swap to alternate builds
  - Compare currently-stored items for build-crafting decisions
- The player **never** visits inventory mid-combat. Inventory is not a combat surface.

### § 4.5 — Implication for Reincarnated

- **Validates `project_pet_system.md`** strongly. Pet auto-pickup is the right answer.
- **Validates D17 Court of Forms browser** — Court is the between-combat inspect-and-decide surface.
- **Re-shapes the mobile inventory modal decision (decision-batch 2026-05-17 #6).** Modal is correct; its *contents* should prioritize:
  1. Equipped gear visualization
  2. Comparison-pane affordance
  3. Set-bonus / affix detail
  4. Loadout-swap shortcut
  - Inventory grid sorting / management is **secondary** to these.

---

## § 5 — Five extracted design principles (canonical for Reincarnated mobile)

These are the design primitives DoE has converged on and that Reincarnated should adopt. Each gets a name we can reference in future docs.

### § 5.1 — Principle 1: **Positioning IS the skill ceiling**

Combat skill expression is movement + threat-reading, NOT input frequency. Auto-attack handles damage output; skills are cooldown-driven taps; the player's hands are mostly on the move-to-target gesture.

**Reincarnated application:** Our cooldown-based skill system already aligns. The narrow-slice dodge work is the right investment. **Do not add input-frequency-rewarding mechanics** (e.g., combo chains, attack-canceling, action-game-style timing) without explicit Matt approval — they would fight this principle.

### § 5.2 — Principle 2: **Loot flows through, not into**

Loot pipeline is auto-pickup → auto-compare → one-tap-equip. The player never browses inventory mid-combat. Inventory is a between-combat inspect-surface.

**Reincarnated application:** Pet auto-pickup + Court of Forms as inspect surface = correct architecture. Forward-flag the **old-item auto-vend/auto-vault** behavior — Matt to observe DoE more or we observe genre cluster.

### § 5.3 — Principle 3: **React-or-auto affordances**

Environmental interactions (chests, doors, levers, NPC dialogue triggers) surface as pop-up hand-button affordances. If the player taps fast enough, they activate intentionally. If they don't, the game auto-completes the interaction.

**Reincarnated application:** New design primitive for canonical-32 amendment. Specifies: every battlefield interaction has an `auto_complete_window` (e.g., 0.8-1.5s); player tap during window = intentional activation; window expiry = auto-completion. Reduces decision fatigue; preserves agency. **Forward-flag for canonical-32 § 13 (new section authoring).**

### § 5.4 — Principle 4: **Single healing affordance, cooldown-gated**

One large heal button (DoE's "Healing"), cooldown-based, no inventory of potion types. No "potion of greater healing vs potion of lesser healing" — just one heal, one cooldown.

**Reincarnated application:** **Locked per Matt 2026-05-17:** PC + mobile both use cooldown-based heal. Canonical-32 § (TBD) amendment needed: retire potion-inventory mechanic; replace with cooldown ability. Inventory slots freed for build-crafting items only.

### § 5.5 — Principle 5: **Combat-UI sparseness**

During combat, only surfaces visible are: rift HUD (top-left), portal (top-right), skill bar + ultimate + heal (bottom), objective counter + XP (bottom edge), character portrait + currency (bottom-left). Hidden: inventory icon, full character sheet, social UI, chat input, advanced minimap controls.

**Reincarnated application:** Mobile UI must follow the same hide-during-combat rule. Our PC HUD has more elements visible by default; mobile must aggressively prune. The full set of combat-visible elements should be a canonical-32 enumeration. **Forward-flag for canonical-32 § (TBD).**

---

## § 6 — Validations: what DoE confirms about current Reincarnated direction

| Reincarnated decision / design | DoE evidence | Confidence |
|---|---|---|
| Telegraphed AOE + dodge (narrow slice) | Red rectangular AOE telegraph visible in screenshot; identical geometry to our `rectangular_aoe`; player's "dodging" is the skill | **High** |
| Cooldown-driven skills | Skill bar with cooldown gating; no input-frequency reward | **High** |
| Trial-room / boss-gallery content model (canonical-32) | `[EASY] Whisper Rift 2` with timer + "55 killed" counter = trial-room model | **High** |
| Pet auto-pickup (`project_pet_system.md`) | DoE auto-pickup confirms direction | **High** |
| HYBRID a3 visual register (VS2a) | DoE's HD-raster-painterly art = same cluster | **High** |
| Solo-only gameplay (project_design_intent.md) | No party UI, no chat input, no friend list | **High** |
| Substrate-coherent enemies (canonical-32) | Off-left enemy cluster with purple smoke suggests shadow-substrate signature | **Medium** (genre-typical; not unique) |
| Court of Forms as inspect surface (D17) | DoE's inspect-vs-management split validates the architecture | **High** |
| Objective-counter trial framing | "55 killed" UI = trial-room objective canon | **High** |

---

## § 7 — Pivots / amendments needed in current docs

### § 7.1 — Mobile orientation: portrait-primary (LOCKED 2026-05-17)

**Amendment scope:**
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` (drax v1.6) — currently assumes both portrait and landscape; amend to portrait-primary, landscape-secondary.
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — § 3.5 minimap-positioning specifies portrait/landscape symmetry; amend to portrait-primary tuning with landscape-fallback notes.
- Drax mobile commission (forward) — should explicitly target portrait viewport first; landscape support is a polish-phase item, not a v1 requirement.

### § 7.2 — Healing potions: cooldown on PC + mobile (LOCKED 2026-05-17)

**Amendment scope:**
- `canonical/32-progression-design.md` — potion mechanic needs new section or section-amendment: retire potion-inventory; replace with cooldown ability ("Healing"). Specify cooldown duration (recommend 8-12s baseline; gear/trait modifiable).
- `canonical/17-gear-and-spirit-guide-design.md` — gear-affix system: retire affixes that interact with potion-inventory; add affixes that modify heal cooldown or heal magnitude.
- `reincarnated-engine/src/reincarnated/simulation/combatant.py` — `STAMINA_POTION_USE` or equivalent fields: refactor to cooldown-gated `heal_ability`. **Star-lord/gamora coordination at implementation time.**

### § 7.3 — Inventory modal: inspect-and-equip surface (clarification of #6 decision-batch lock)

**Amendment scope:**
- Mobile inventory modal (drax mobile commission) — design specifies:
  - Equipped gear visualization (primary)
  - Comparison-pane affordance (primary)
  - Affix + set-bonus detail (primary)
  - Loadout-swap shortcut (primary)
  - Inventory grid sorting / management (secondary)

### § 7.4 — HP placement on mobile (forward-flagged; no lock yet)

DoE puts HP in the rift-HUD module top-left, not as a bottom-corner globe. **Open design question:** Reincarnated mobile — match DoE (HP top-left, attached to navigation) or D-series (HP globe bottom-left)?

**Recommend:** Match DoE for mobile (top-left, attached to minimap module); keep globe pattern on PC. Reasons:
- DoE-pattern frees bottom-corner real estate for the heal cooldown + skill bar
- Top-left is glanceable during movement (thumb is bottom-right; eye drifts up)
- Globe pattern is desktop-canonical; mobile players have less screen budget to spare on large HP affordance

**Not locked.** Surface in mobile commission.

### § 7.5 — Skill auto-cast vs tap-cast split (forward-flagged)

DoE: most damage = auto-attack; 2 of 5 skill slots filled (tap-cast); 1 ultimate (tap-cast). The split is approximately **3-5 manual skill slots out of total kit; rest is auto.**

For Reincarnated's larger kit (per canonical-32 progression), this implies:
- 3-5 skills are tap-cast (player chooses which ones in build-crafting)
- All other skills proc automatically on attack-cycle or off cooldown

**Not locked.** Surface in mobile commission and canonical-32 § 12.5 amendment.

### § 7.6 — React-or-auto interaction primitive (new canonical-32 section)

New design primitive (per § 5.3). Gandalf to author canonical-32 amendment when scoped.

---

## § 8 — Forward-flagged for mobile commission

When the mobile commission spawns (likely post-VS2a, possibly VS2b territory), the following questions surface:

1. **Touch-targeting design** (replaces retired enemy-cycle from decision-batch 2026-05-17 #4)
2. **HP placement** (per § 7.4)
3. **Skill auto-vs-tap split** (per § 7.5)
4. **React-or-auto specification** (per § 7.6 + § 5.3)
5. **Trial-room "X killed" objective-counter UI** (DoE-pattern; adopt as-is?)
6. **Movement reticle visualization** (DoE shows a large grey circle on tap-to-move target; our PC demo has cursor pointer — what's mobile equivalent?)
7. **Old-item auto-vend / auto-vault behavior** after equip (DoE behavior unclear from 15-min session)
8. **Currency display position** (DoE: bottom-center-left, small, dual-currency; our currency model is TBD)
9. **Red-dot notification model** (where do we surface "tap me" affordances besides character portrait?)
10. **Visual register cluster confirmation** (DoE = HD-raster-painterly, aligned with HYBRID a3 lock; legolas catalog crawl should weight this cluster heavily)

---

## § 9 — Open questions for Matt (post-doc, non-urgent)

**Most decisions from the DoE paragraph are now locked. Remaining open:**

1. **DoE skill 1 vs skill 2 — both visible in screenshot (icy + wind icons), both partially-charged in cooldown rings.** Did you observe whether these are auto-cast or tap-cast? The screenshot suggests tap-cast (otherwise why surface them in a player-tappable slot?), but Matt's paragraph implies most skills are auto. **Worth clarifying on next play session.**

2. **Movement reticle on ground (large grey circle south of player in screenshot) — is it persistent (always visible at tap-target) or only flashes on tap?** Affects our movement-feedback UI design.

3. **DoE's auto-vend / auto-vault behavior — what happens to old items when you tap red-dot to equip new?** Affects pet-system + loot-flow design.

4. **DoE potion cooldown duration?** Affects our balance baseline. (Recommend Matt note timer on next session.)

5. **Did you observe substrate-coherent enemy behaviors in DoE?** (Off-left purple-smoke cluster looks shadow-substrate.) Affects whether DoE's enemy taxonomy matches our substrate model.

---

## § 10 — Amendment policy

This doc captures a **single-session observation**. It will likely amend as Matt:

- Plays more DoE (different builds, different content tiers, different sessions)
- Plays other cluster titles (Diablo Immortal, Torchlight Infinite, Eternium, Anima ARPG)
- Tests Reincarnated mobile prototypes against the DoE feel-target

**Amendment policy:**
- New observations append as `## § N — Amendment YYYY-MM-DD` sections
- Locked decisions (per § 0 TL;DR) require explicit Matt re-approval to amend
- Forward-flagged items (§ 8) resolve into locked decisions when the mobile commission addresses them
- Cross-references update as new canonical docs land

---

## § 11 — Cross-references

- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — sizing canon; **§ 3.5 portrait-primary tuning LANDED 2026-05-17** (Path A doc-cascade dispatch)
- `canonical/story/arpg-map-overlay-research-2026-05-17.md` — overlay design (PC-anchored; mobile portions consistent with this doc)
- `canonical/story/mobile-ux-execution-plan-2026-05-17.md` — drax v1.6 plan; **§ 4.3 portrait-primary amendment LANDED 2026-05-17** (Path A doc-cascade dispatch); § 4.2 portrait-diagram TBD pointer landed; § 7 portrait-primary preamble landed
- `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — narrow-slice combat; § 6 validations
- `canonical/story/vs2a-vfx-scene-needs.md` — visual register; § 6 alignment confirmed
- `canonical/32-progression-design.md` — **§ 13 (NEW) react-or-auto + cooldown-heal LANDED 2026-05-17** (Path A doc-cascade dispatch); § 13.1 retires potion-inventory; § 13.2 react-or-auto primitive; § 13.4 portrait-primary mobile-orientation note
- `canonical/17-gear-and-spirit-guide-design.md` — **heal-cooldown affix family LANDED 2026-05-17** (Path A doc-cascade dispatch); retires potion-interaction affixes
- `canonical/16-project-roadmap.md` — mobile-commission slot to be defined
- `agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md` — **this dispatch** that landed the four amendments above
- `agentic_orchestration/AGENTS.md` — drax mobile commission scope reference
- `project_pet_system.md` (Matt memory) — § 6 strong validation
- `project_design_intent.md` (Matt memory) — § 6 validation (solo confirmed)
- `../DOE.png` — gameplay screenshot, Matt 2026-05-17 15:56
- **§ 12 below** — DoE as canonical reference experience (Matt L3 Path A lock 2026-05-17; codified Q5 2026-05-18)

---

## § 12 — DoE as canonical reference experience (Matt L3 Path A lock 2026-05-17; codified Q5 2026-05-18)

**Status:** **LOCKED** per Matt L3 yes-batch 2026-05-18 Tier 1.5 Q5. This section codifies DoE's role as the locked reference experience that future agents anchor mobile-UX decisions against. Earlier sections of this doc (§ 0 - § 10) capture the *observations* from Matt's 15-minute play session; this section names DoE itself as the canon.

### § 12.1 — What DoE is, in canonical terms

Dungeon of Exile (DoE) is the **validated reference experience** for Reincarnated mobile feel + UX patterns. Not an inspiration. Not one influence among many. The reference. When a designer, engineer, or agent asks "what should this mobile UX feel like?" the answer is DoE unless and until this canon is amended.

The lock landed via Matt L3 Path A authorization 2026-05-17 (decisions-log entry 2026-05-17: *Heal mechanic + heal-affix family canonicalization*). The Path A doc-cascade was executed the same day — canonical-17 + canonical-32 portrait-primary amendments + heal-cooldown affix family + react-or-auto primitive — under that single authorization. This Q5 paragraph (2026-05-18) is the back-fill that names DoE itself, not just its consequences, as canon.

### § 12.2 — What DoE establishes for Reincarnated

The DoE reference locks the following baseline as canonical mobile-feel for the project. Each item is sourced from § 2 - § 6 above; this section restates them as a single-glance reference list for future agents:

- **Portrait-primary orientation.** Mobile play is portrait. Landscape is fallback-only, polish-phase. (§ 7.1)
- **Cooldown-based heal.** Single "Healing" button, cooldown-gated. Drax v1.18.5 hotfix landed the demo-side parameters: 10s cooldown; 35% max-HP; 50 HP floor; 0s cast; no invuln window. No potion inventory. (§ 5.4, § 7.2; decisions-log 2026-05-17 heal canonicalization entry)
- **Auto-cast skill rotation with manual target override.** Most skills proc automatically on cooldown / attack-cycle; player retains manual targeting agency. Reincarnated Option A locked 2026-05-18. Skill bar surfaces ~3-5 manual slots; remainder is auto. (§ 7.5)
- **Cooldown-based potions.** Mirrors DoE's heal pattern — no inventory of consumable potion variants; potion is a cooldown ability (15s baseline per drax v1.18.5 hotfix). (§ 5.4)
- **Touch-first input design.** Tap-to-move; tap-to-cast; tap-to-equip via red-dot affordance. No virtual joystick; no enemy-cycle reticle; positioning IS targeting. (§ 3.1, § 5.1)
- **HUD density appropriate for portrait + finger-touch precision.** Touch-target sizing 88-125px per `mobile-pc-pixel-sizing-ratios-2026-05-17.md` (gandalf v1.7); combat-UI sparseness per § 5.5; inventory hidden during combat; map + HP module top-left; skill bar + heal bottom.

### § 12.3 — Departure rule: when Reincarnated may deviate from DoE canon

DoE is the reference; it is not a contract. Reincarnated-specific mechanics — Spirit Guide, Earth-Self meta-layer, 6-archetype kit shape, substrate-coherent enemies, trial-room boss-gallery model — may force departures the genre-cluster reference cannot anticipate.

**Departure rule (locked):**

1. **Any deviation from DoE-canon mobile-UX requires an explicit canon-doc note.** The deviation must be authored into the relevant canonical doc (this one, or canonical-17 / canonical-32, or a successor) with:
   - Statement of what DoE-canon prescribes
   - Statement of what Reincarnated does instead
   - Reasoning grounded in a Reincarnated-specific mechanic (not "designer preference" and not "we think this is better generally")
2. **Departure requires Matt L3 sign-off.** Not L1, not implicit through implementation. The explicit canon-doc note routes through a yes-batch question. Agents may *propose* departures via Q-batch surfacing; only Matt locks them.
3. **Default is fidelity.** When a mobile-UX question arises and DoE has a clear answer, the default is to match DoE. The burden of justification rests with the departure, not with the fidelity.

This rule protects against the pattern where projects with strong reference targets drift through accumulated micro-departures, each individually justified, until the cumulative result no longer feels like the reference. Diablo Immortal's pre-launch beta drift away from its mobile-feel-target back toward D3-PC patterns is the cautionary tale; the post-launch corrections were expensive.

### § 12.4 — Forward-looking: when to reselect the canonical reference

DoE is canon **through VS2a + VS2b**. Beyond that, the canonical reference may need reselection if Reincarnated-specific mechanics push the demo away from DoE-pattern fidelity.

**Triggers for canon reselection (any one is sufficient to surface a Matt L3 question):**

- **Earth meta-layer surfaces a UX paradigm DoE doesn't model.** If the persistent-Earth-Self loop requires a UI shell (gacha-style form library, MOBA-arena lobby, Pokemon-style collection screen) that DoE has no analogue for, the reference may need extension via a second cluster title (e.g., a gacha-strong title for the form-library surface; a hub-MMO title for the rift-event surface).
- **PVP/PVE rift events introduce multi-actor UX demands.** DoE is solo-only (validated § 6). If rift events introduce party, raid, or arena UX, the solo-only reference is insufficient; a multi-actor reference is needed.
- **Spirit Guide interaction depth exceeds DoE's auto-cast paradigm.** If Spirit Guide gameplay surfaces as a *during-combat* surface with its own input vocabulary (rather than its current between-combat narration / guidance role), DoE's "low input frequency" principle may no longer match.
- **Substrate-coherent enemies require enemy-readability UX DoE doesn't have.** If the player needs to read substrate signatures (shadow / verdant / ember / etc.) at a glance to choose tactics, and DoE's enemy-tells are too generic to model that, an alternate reference may be needed.
- **Visual register diverges from DoE's HD-raster-painterly cluster.** The HYBRID a3 lock currently aligns (§ 6); a future register pivot would break the alignment and force reselection.

**When a trigger fires:** gandalf authors a canon-reselection-question for the next yes-batch, surfacing the candidate alternate reference(s) and the specific Reincarnated mechanic forcing the departure. Matt L3 selects the new canon (or extends DoE with a secondary reference for the divergent surface). Default behavior, absent trigger, is **DoE remains canon.**

### § 12.5 — Cross-references for § 12

- `canonical/17-gear-and-spirit-guide-design.md` — portrait-primary amendments (Path A doc-cascade 2026-05-17); heal-cooldown affix family
- `canonical/32-progression-design.md` — § 13 (NEW) react-or-auto primitive + cooldown-heal + portrait-primary mobile-orientation note (Path A doc-cascade 2026-05-17)
- `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (gandalf v1.7) — sizing-ratio + 88-125px touch-target canon
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-17 entry — *Heal mechanic + heal-affix family canonicalization (DoE feel-target lock)*; jack-ryan DoE Path A entry
- `agentic_orchestration/dispatches/2026-05-18-gandalf-q5-doe-paragraph-mobile-feel-canon.md` — this dispatch (Matt L3 Tier 1.5 Q5 authorization)
- Earlier sections of this doc: § 0 TL;DR (locked decisions), § 5 (five design principles), § 6 (validations), § 7 (pivots / amendments executed)

---

*Authored 2026-05-17 by gandalf, immediately following Matt's DoE play session + screenshot. This doc is the canonical feel-target reference for Reincarnated mobile design. § 12 appended 2026-05-18 per Matt L3 Tier 1.5 Q5 yes-batch (codifies DoE as the canonical reference; departure rule + canon-reselection triggers). Future amendments append per § 10.*
