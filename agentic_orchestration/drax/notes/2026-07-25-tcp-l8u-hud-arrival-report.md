# TCP-L8-U — mode (ii) HUD ARRIVAL: the combat HUD for *Reap. Die. Rise.*

**From:** drax (presentation seam) · **To:** gandalf (`RUN-CONDUCTOR`), Matt
**Date:** 2026-07-25 · **Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l8u-hud-arrival.md`
**Floor:** `~/Games/mcp-lab/l8ui/` (created this cell; **stays** — it is the (i) cells' floor)
**Verdict:** **PASS** — design delivered, judged over real gameplay at two aspects, exit predicate met.
Includes one **ceiling-finding (L-G PASS)** that materially weakens L8's premise, and **two items
flagged to Matt**.

---

## §0 — Clock, banked honestly (TCP-32)

| | |
|---|---|
| FIRST_INTENT banked | `2026-07-25T22:30:31Z`, **before** any reading or work — `l8ui/FIRST_INTENT.md` |
| Clock start / close | `22:30:31Z` → `22:59:05Z` |
| **Total** | **28m 34s** |
| **Execution** (every Godot invocation: 1 import, 75 renders, 1 census) | **~86 s = 5.0%** |
| **Authoring** (reading, deciding, typing, looking, judging) | **95.0%** |

Consistent with TCP-32's finding that authoring dominates. Slightly below the "~99%" of prior
cells because this lap is render-heavy — it still never approached parity.

---

## §1 — Read-list, declared (§4.4; mode (ii) is not blind)

**Canon — meta-repo.** `reap-die-rise-story/00-index.md` · `story-keystone.md` (§14–§20, incl. the
LOCKED reap beat) · `gameplay-loop-design.md` (all §, esp. §5 enemy ontology, §9 Goldilocks, §16,
§23 run model) · `style-register.md` · `reap-die-rise-game/one-realm-mvp-scope.md` ·
`reap-die-rise-engine/`: `attribute-system-2026-05-24.md`, `skill-system-2026-05-24.md`,
`40-gear-balance-guide-architecture` §8.4.4, `46-concentration-architecture`,
`49-loadout-sample-player-surface-design`, `ailment-layer-engine-spec.md`,
`telegraph-dodge-temporal-decoupling-2026-06-15.md`, `coordinate-register-2026-07-13.md` ·
`current-to-end-state-{story,game}.md`.

**Engine source (read, not assumed — TCP-30 applied to my own reading).**
`reincarnated-engine/src/reincarnated/simulation/combatant.py` — `_ENERGY_CONFIGS` and the mana
branch, which is where the six-economy finding actually comes from; the docs alone would not have
given it.

**Real engine output (my own repo).** `reincarnated-loadout/data/season_002328/classes/*.json`
— 10 gauntlet-passed kits, inspected for skill count, roles, chains, elements, energy types.
`reincarnated-loadout/src/data/serializedLoadout.ts` (the 10-slot gear contract).

**Reference only, not modified.** `reincarnated-godot/scenes/arena_room.tscn` — I took the
established 2.5D camera register (fov 44, shallow ARPG pitch) rather than inventing an angle.

---

## §2 — What the ancestry actually said, and why it changed the design

Five findings did real work. Four are only visible if you read the engine and its output rather
than imagining an ARPG.

**(a) Max 8 active skills, flat. Exactly ONE T4.** Doc-40 §8.4.4 (*"Maximum 8 active skills. Flat 8"*)
and doc-49/D66. This is the single most layout-critical number in a HUD and it is already ruled.
No invention required.

**(b) Real kits carry 10–14 skills.** Measured across all ten emitted kits in `season_002328`
(chains of 2–7, tiers 1–4). So **the bar is a chosen subset, not the kit** — which is why unfilled
slots must read as *unmade decisions*, not as locked-out controls.

**(c) There are SIX energy economies, with opposite dynamics.** From `_ENERGY_CONFIGS`:
`mana` (starts full, passive regen) · `rage` (100, starts **empty**, no regen) · `combo` (**5,
discrete**) · `focus` (100, starts full, **−5/s decay**) · `stamina-as-resource` (150, +20/s) ·
`charge-stack` (**10, discrete**, hold-then-release). A single blue orb is correct for exactly one
of the six. This produced R-6, the design's most consequential ruling.

**(d) Kits are element-MIXED.** `class_0001` is `dominant_element=fire` and its `primary_attack`
is `canonical_element=earth`. A per-kit "your element" readout would therefore be **wrong on real
data**. Element belongs per-skill. (R-8.)

**(e) The project has a stated meter-avoidance discipline**, loop-doc §16: *"more elegant than a
meter (and consistent with our meter-avoidance elsewhere)"* — composed with keystone §19.3's
LOCKED requirement that the god stay unreadable and non-triggerable. This directly forbids things
a generic ARPG HUD would happily add. (R-13.)

Also load-bearing: style-register.md §"Scope honesty" states **"UI / HUD layer not evidenced —
the UI chrome is a separate, not-yet-evidenced surface."** This cell fills a gap canon names.

---

## §3 — The design

**Name:** the **Reliquary HUD**. The game's objective is literally a *conduit* — "the realm's
soul-vessel." The player is a soul wearing a stolen body. So the organising metaphor is **vessels
holding soul-stuff**, which is the game's own central object rather than a borrowed one.

```
┌──────────────────────────────────────────────────────────────┐
│ ●○ STRUCTURE II          OSSUARY WARDEN            ┌────────┐│
│ grimoire · page 12/400+   ◤ TOO HOT ◥              │minimap ││
│                           ▬▬▬▬▬▬▬▬▬▬                │ glyphs ││
│                                                    └────────┘│
│                      ( play space — clear )                  │
│                                                              │
│              ┌──┐┌─┐  ▣ ▣ ▣ ▣ ▣ ▣ ▣ ▢   ◈             │
│              │HP││E│  1 2 3 4 5 Q E R   T4              │
│              └──┘└─┘                                         │
└──────────────────────────────────────────────────────────────┘
```

### The rulings (veto-open; Matt may overturn any)

**R-1 — "Am I about to die, and what can I do about it" is ONE question, so it gets ONE place.**
Life, energy, ailments, the 8 skills and the T4 are a single **Combat Cluster**. Almost every
shipped ARPG splits survival (corner) from action (centre), forcing two saccades to answer one
question. *Reasoning:* the second clause of gandalf's own criterion — "what can I do about it" — is
answered by *how many slots are lit*, so it must be adjacent to the thing that says you're dying.

**R-2 — Ambient vs survival is the anchoring split.** Corner-anchored = ambient, consulted
deliberately (minimap, conduits, run beat). Centre-anchored = survival, read peripherally. This is
the whole anchoring story and it is what makes 21:9 work rather than merely not-crash.

**R-3 — Named champions get a target frame; fodder never does.** Loop-doc §5 makes the
monster/champion split load-bearing; nameplating fodder would flood the frame and destroy the
scarcity that makes a champion land.

**R-4 — The Combat Cluster anchors bottom-CENTRE, not bottom-left.** *Reasoning:* a corner-pinned
survival readout drifts ~320 px further into the periphery at 21:9 than at 16:9 — the ergonomics
silently degrade with monitor width. Anchoring to centre holds the read at a fixed distance from
the character at any aspect. Only genuinely ambient things get true corners.

**R-5 — VOID-FILLS-BRIGHT. The danger signal is the EMPTY space, and it grows in area AND
luminance as life falls.** This is the core of the design and it inverts the genre. A conventional
bar makes the danger state *smaller and dimmer* — at 10% HP you are looking for a shrinking dark
sliver, in a dark crypt. Mine makes it *larger and brighter*: at 13% HP the vessel is a large hot
orange block, the loudest thing in the cluster. Peripheral vision detects area and luminance
change well and glyphs badly, so the signal should grow along the axes the periphery can actually
see. **Measured:** the life vessel is the highest-contrast element in the HUD at every background.

**R-5a — Straight-sided vessel, not an orb.** I take the *shape* principle and reject the *orb
geometry*. An orb is a circle: near empty, the remaining liquid is a thin lens and the surface
barely moves for a large HP loss, so **the orb is least sensitive exactly where the player needs
it most.** Same liquid affordance, honest linear geometry. This is the deliberate divergence §2
invited.

**R-6 — The energy readout is POLYMORPHIC over the six engine economies.** Continuous vessel for
`mana` / `rage` / `stamina-as-resource` / `focus`; **discrete pips** for `combo` (5) and
`charge-stack` (10). *Reasoning:* a continuous fill reading "3.4 of 5 combo points" is a lie about
the mechanic. Colour additionally encodes valence, because `rage` starting empty and filling is a
*reward* signal while `mana` draining is a *danger* signal — the same widget with opposite meaning.
**Evidence:** `l8ui/out/SHEET_economies.png` shows all six side by side.

**R-6b — `focus` is deliberately denied the Void-Fills-Bright treatment.** `focus` starts full and
decays; giving it the life vessel's bright-void treatment would put two bright emptying vessels
side by side and read as *two things killing you*. Bright-void is reserved for life alone.

**R-7 — Player ailments live WITH the life vessel.** A burn ticking on you is part of "am I about
to die," not a separate bookkeeping surface. Capped at 5 + "+N" (registry is 8 live + 4 spec'd, so
icon-soup is a real hazard). Target-side ailments belong on the target, not here.

**R-8 — Element tint is per SKILL, not per kit** — forced by real data (§2d).

**R-9 — Cooldown and unaffordability use two never-confusable channels.** Cooldown = a radial
sweep (a *moving shape*, time-coded). Unaffordable = a flat veil (a *static wash*, quantity-coded).
**R-9b:** the veil is tinted with the active economy's colour, so an unaffordable slot visually
points at the vessel it is short of.

**R-10 — At the reap beat the HUD RECEDES and the verb owns the centre.** Keystone §19.1/§20.2
stages this as sudden, visceral, camera-taking-over. A polite prompt line at the top of the screen
is the wrong register for the most important beat in the game. The cluster/minimap/run-state drop
to 30–38% opacity, `R E A P` takes the centre with the creed *Mete · Morere · Resurge* beneath it
(keystone §18: inscription register only, never the primary title).

**R-11 — Every element carries its own contrast floor, via a two-polarity keyline.** A dark outer
edge AND a light inner edge on every element, plus bounded gradient scrims. Whatever the
background does, one of the two edges holds contrast. **This is the ruling §3.2 exists to test and
it is the one I measured hardest** — see §4.

**R-12 — The escape clock renders as rising edge-bleed, NOT a countdown.** *Reasoning:* canon says
"generous-but-urgent," and a precise number makes a generous clock computable, which kills the
tension it exists to create; it also collides with the §16 meter-avoidance discipline.
**⚠ This one is flagged to Matt — see §7.**

**R-13 — What is deliberately NOT on the HUD, and why.** No god-mood / appeasement meter (keystone
§19.3 LOCKED: triggers must be non-patternable; a meter *is* a pattern and would resolve the
Rorschach). No cult-standing meter (§16 meter-avoidance; it is a hub surface). No XP bar (level
numeral only). No currency. No uncapped buff-icon soup.

**R-14 — Method: H (hand-authored `.tscn` + headless capture loop). W-MUR deliberately NOT used.**
*Reasoning:* this is the ARRIVAL. Its job is to produce the contract and the authoring datum every
later cell is measured against. Using the wire here would contaminate that datum with
wire-learning cost, and comparing instruments is precisely the (i) cells' job, not mine. L-J
respected: W-PRO untouched, its swap directory never opened.

---

## §4 — Legibility, argued and measured (§4.2)

**The dispatch's instruction was the important one:** *"contrast failures live in exactly the
places a hand-picked screenshot avoids."* So I did not pick an angle. I rendered candidate
framings without the HUD and **measured Rec.709 relative luminance inside each HUD region**
(`l8ui/analyse_bg.py`), then chose the extremes.

That immediately caught a failure in my own test rig: **at the ARPG camera the crypt does not fill
the frame, and every HUD region measured 0.0000 luminance** — the HUD was floating over black
void. A legibility test over black is worthless, and I would have shipped it if I had trusted the
picture instead of the numbers.

Three MEASURED background cases were then established:

| case | framing | scene luminance under the HUD |
|---|---|---|
| **DARK** | d=15, aim (−5,−5) | mean 0.082 – 0.133, p05 **0.0003** |
| **STONE** | d=9, aim (0,0) | mean 0.155 – 0.221 — *the "disappears over stone" case* |
| **BLOOM** | d=11, `--torch=140` | mean 0.502 – 0.784, max **0.99** |

> **The BLOOM case is a declared stress, and I want it on the record why it exists.** The crypt
> as-shipped tops out near 0.40 luminance — **it has no genuinely bright region.** The LOCKED style
> register, by contrast, ships dramatic lighting (galadriel measured LDR 231.6, glow threshold
> 1.25). Judging the HUD only against the flat substrate would **under-test** it. `--torch` boosts
> the crypt's `InteriorPool` **at runtime only**; the substrate file is 0444 and byte-identical.

### Results (`l8ui/legibility.py`)

| region | worst contrast | verdict | scene Y behind it |
|---|---|---|---|
| life_vessel | **10.21 : 1** | PASS | 0.095 → 0.554 |
| energy_vessel | 7.58 : 1 | PASS | 0.133 → 0.590 |
| skill_bar | 12.00 : 1 | PASS | 0.121 → 0.653 |
| t4_slot | 6.37 : 1 | PASS | 0.133 → 0.536 |
| target_frame | 6.97 : 1 | PASS | 0.082 → 0.784 |
| minimap | 4.78 : 1 | PASS | 0.088 → 0.606 |
| ailments | 13.84 : 1 | PASS | 0.087 → 0.591 |

**All regions clear WCAG 3.0:1 at every measured background.**

### The number the design actually stands on — background independence

| region | HUD's own luminance span | scene's span | **isolation** |
|---|---|---|---|
| life_vessel | 0.213 → 0.219 (**1.03×**) | 0.095 → 0.554 (5.83×) | **5.7×** |
| energy_vessel | 0.079 → 0.089 (1.12×) | 0.133 → 0.590 (4.43×) | 4.0× |
| ailments | 0.189 → 0.337 (1.79×) | 0.087 → 0.591 (6.78×) | 3.8× |
| t4_slot | 0.095 → 0.103 (1.09×) | 0.133 → 0.536 (4.04×) | 3.7× |
| skill_bar | 0.070 → 0.127 (1.80×) | 0.121 → 0.653 (5.41×) | 3.0× |
| minimap | 0.014 → 0.034 (2.44×) | 0.088 → 0.606 (6.88×) | 2.8× |
| **target_frame** | 0.044 → 0.217 (**4.94×**) | 0.082 → 0.784 (9.56×) | **1.9× ← weakest** |

**The life vessel's own luminance moves 3% while the scene behind it moves 5.8×.** That is R-11
working: the HUD carries its own contrast floor and cannot disappear over stone.

**Attributed weakness (L-F).** `target_frame` is the least isolated element at 1.9× — it is mostly
text over a gradient scrim with no solid bed. It still passes at 6.97:1, but it is the element that
would fail first if the register got brighter than the stress case. Named, not hidden.

### A near-miss worth reporting (TCP-30, in miniature)

My first metric run **convicted the minimap at 1.26:1 — a FAIL.** Before accepting it I checked:
the minimap rect is ~97% flat panel with a handful of small glyphs, so p95 landed on the bed and
measured the bed against itself. At p99.5 the same region is **9.08:1**, and the glyphs are plainly
legible by eye. **The instrument was wrong, not the design.** I made the metric ink-coverage-aware
and re-ran. This is the third-hand version of the defect TCP-30 says this program has committed
three times, and it took one deliberate check to avoid.

---

## §5 — Census (§4.3), exact

Counted from the live instantiated tree (`l8ui/census.gd`), not estimated.

| | |
|---|---|
| **Hand-authored node writes** | **66** (57 `hud.tscn` + 9 `skill_slot.tscn`) |
| Hand-authored sub-resources | 28 (21 + 7) |
| **Runtime nodes, authored tree** | **129** (128 Control-derived) |
| Runtime nodes, populated with a real state | **144** |
| Runtime nodes, worst case (charge-stack, 10 pips) | **154** |
| **Player-facing controls** | **17** (+2 conditional overlays) |
| Shaders / scripts | 1 / 2 |

> **The 66 → 129 gap is the single most useful number here for the (i) comparison.** A `.tscn`
> author writes 66 nodes because the slot component is authored once and instanced nine times. An
> instrument that creates nodes one at a time must produce **129** — a ~2× penalty before a single
> layout nudge. **Any (i) cell reporting a node count must state which of the two it produced**,
> or the comparison is meaningless. Full contract: `l8ui/CONTRACT.md`.

---

## §6 — ★ THE ITERATION LOG, and the ceiling it finds (§4.5)

Full table: `l8ui/ITERATION_LOG.md`. Summary:

| Measure | Value |
|---|---|
| Total numbered passes | **12** |
| **Layout passes** (edit-batch → render → look) | **5** |
| Substrate/framing passes | 5 |
| Correctness passes (my own code errors) | 1 |
| Measurement-instrument passes | 1 |
| **Discrete layout edits** | **~16** |
| Edits per look | **≈3.2** |
| Median single-still render | **1.19 s** |
| Full 10–12 still set | 12–15 s |
| Regressions I introduced fixing my own defects | **1** |
| Defects visible ONLY at the second aspect ratio | **1** |

### ⚑ Ceiling-finding (L-G = PASS): L8's premise does not survive measurement

§0 hypothesised **N≈12 controls, ~40 layout iterations, ~150 ms wire nudge vs a 15–30 s script
edit → relaunch → screenshot cycle.** The control count was right (17). The rest was not:

1. **The script cycle is 1.19 s, not 15–30 s** — 10–25× cheaper than assumed. A headless
   one-frame capture is not an editor round-trip. **The denominator of the wire's advantage is
   wrong by an order of magnitude.**
2. **Layout iterations were 5, not 40** — and discrete edits ~16.
3. **Edits batch** (≈3.2 per render), so per-edit render cost amortises to ~0.37 s.
4. Being generous to the wire: 16 nudges × 150 ms = **2.4 s** vs 5 renders × 1.2 s = **6 s**.
   The wire's saving on this lap is **~3.6 seconds against a 28m34s clock — 0.2%.**
5. **The dominant cost was neither editing nor rendering. It was LOOKING and DECIDING.** One 1:1
   crop inspection produced ten findings. Reading the frame and judging it is the bottleneck, and
   **no wire addresses it** — the agent must look either way.

**Stated in the wire's favour, because it deserves it:** this is an ARRIVAL, where most passes
create things that do not yet exist — text's strongest case. A pure *tuning* cell ("take this exact
tree, move twelve things four pixels") has a different profile. The (i) cells should measure that
separately rather than inherit this conclusion. But **L8 was nominated as the wire's strongest
untested case, and on the arrival cell's numbers the case is far weaker than hypothesised.**

---

## §7 — HALT items for Matt

Neither blocked me from producing an answer, so I did not stop the cell. But the dispatch says
inventing a game-systems decision silently commits the project, so here are the forks. **I have
stopped on branch (a) and made a reversible call on (b).**

### (a) ⚠ HALT — the escape clock is a design fork I should not close alone (R-12)

Canon says the escape clock is **"generous-but-urgent"** and that *"a competent player escapes
with a thrilling margin; only a fumbling one fails."* It never says whether the player can **see**
it. That is not a presentation detail — it decides what the escape *is*:

- **Fork A — no numeric clock** (what I built): rising edge-bleed pressure only. Preserves the
  dread, obeys §16 meter-avoidance, keeps the escape a *feeling*. **Cost:** a player who fails has
  no way to know they were behind, which is the classic unfair-death complaint.
- **Fork B — a visible timer**: fair, learnable, streamable, and it makes the escape a *skill
  test*. **Cost:** a generous clock rendered as a number becomes computable, and players will
  optimise the margin to zero — the tension the beat exists to create evaporates.

**This is a story/design ruling about what the crescendo of every run is, and it is yours.** My
implementation is one node (`EscapePressure`) and is trivially swappable either way. One-Realm §8
lists the escape clock's band as something the demo is meant to *empirically validate* — which
argues for shipping Fork A into playtest and letting the data rule. I lean that way, but I am
naming the fork rather than banking it.

### (b) Flagged dependency — B1 / Q2 (run-persistence) tunes a threshold I had to pick

`current-to-end-state-story.md` B1 is **OPEN** (LAUNCH-GATE), and `story-expansion.md:175` says
explicitly: ***"Do not harden possession-surface UI/scenes until B1 is ruled."***

My HUD touches that surface twice: the grimoire page counter ("page 12 of 400+", demo-critical per
One-Realm §4) and — less obviously — **R-5's danger thresholds**. How loud the death warning
should be is a function of *what death costs*, and that is exactly what B1 rules. I set
VOID_CRIT at <25%; if death forfeits volatile grimoire pages that is right, and if death is cheap
it is over-dramatic. **Not hardened, reversible, one constant.** Demo is explicitly unaffected
("a demo banks trivially or not at all", One-Realm §9).

### (c) Observation, not a HALT — some kits have no basic attack

Across the ten emitted kits, `primary_attack` appears **7 times for 10 kits** — several kits have
none. So the bar cannot assume a free left-click attack, and a resource-starved player of such a
kit may have *nothing to press*. That is an engine/design question, not a HUD one, and I flag it
to gandalf rather than paper over it in presentation.

---

## §8 — Exit predicate (§5)

| Predicate | Status |
|---|---|
| §4.1 FIRST_INTENT verbatim + clock start before work | ✅ `l8ui/FIRST_INTENT.md`, 22:30:31Z |
| §4.2 Stills at both resolutions + defensible legibility argument | ✅ 12 FINAL stills; measured, brightest AND darkest |
| §4.3 Exact control + node census | ✅ 17 controls; 66 authored / 129 / 144 / 154 |
| §4.4 Rulings veto-open with reasoning; read-list declared | ✅ R-1…R-14; §1 |
| §4.5 ITERATION LOG | ✅ `l8ui/ITERATION_LOG.md` + §6 |
| §4.6 Clock closed, authoring separate from execution | ✅ 28m34s / 5.0% execution |
| §5.2 Substrate sha + 0444 at start AND end | ✅ `d45db0f5…6a1966`, mode 444, both ends |
| §5.3 `mcp-lab/project/` and `l7vfx/` demonstrably untouched | ✅ see below |
| §5.4 `user://` clean; project stays | ✅ shader_cache only; no logs, no artifacts |

**On §5.3, precisely.** `scene_before.tscn` is byte-identical and still 0444 — verified at start
and end. Every command I ran against `project/` was a read (`ls`/`stat`/`shasum`/`grep`/`find`, and
`cp` *from* it). **I never wrote to either floor, and never opened W-PRO's swap directory.**

My start-of-cell directory-listing hashes did move, and I want that explained rather than glossed:
`project/`'s directory mtime advanced to 18:41 and `l7vfx/` **did not exist** when I snapshotted at
18:31 (it appears at 18:49 with its own `stage.tscn`). Both are the **concurrent L5a and L7 cells
working in their own floors** — my snapshot was taken against a moving target, which makes the
listing hash the wrong instrument. The per-file sha of the substrate is the right one, and it holds
exactly.

**Assets.** The crypt has 6 external deps (3 PNG + 3 `.gdshader`). I copied those out read-only
alongside the scene so the composite renders in *my* project; the source directory was not modified.

---

## §9 — What steered me (asked directly, answered directly)

**Yes — §2's Diablo II sentence steered me, and in an identifiable way.**

The **physiological** half — peripheral vision reads area/motion/luminance, not glyphs — did **not**
steer me. It is in my FIRST_INTENT, written before I read the dispatch's reasoning, and it is
physics.

The **exemplar** half did. *"Diablo II's orbs are readable as shape"* anchored me inside the
**"liquid in a container"** solution family. I diverged on the geometry (R-5a rejects the circle)
and inverted the signal (R-5), but I never left the vessel. **I did not seriously evaluate the
non-vessel branch:** a character-anchored diegetic ring, a screen-edge vignette that reddens, an
armour/silhouette damage state on the model itself, or an audio-first survival signal.

That matters because **the screen-edge vignette is arguably stronger on gandalf's own criterion.**
It is the most peripheral thing that exists, needs zero saccade, and it is where shooters
converged. The tell that the branch was live: **I reached for exactly that solution for the escape
pressure (R-12)** — so I had it available and only spent it on a secondary signal, because the
primary slot was already occupied by an orb-shaped assumption.

**The defect, generalised:** naming an exemplar imports its *solution space*, not just its
*principle*. Had §2 stated the peripheral-vision principle and stopped, the answer would have been
genuinely open. Recommendation for future mode-(ii) dispatches: state the criterion, name no
exemplar. If an exemplar is needed to make the criterion concrete, give **two from different
families** so neither becomes the default.

**Two further steers, smaller but real:**

1. **§0's "~40 layout iterations."** I quoted that number back in my own FIRST_INTENT prediction
   ("below the ~40 the dispatch hypothesizes") — it anchored my expectation before I measured
   anything. The measured figure was 5. Since the iteration count is *the very quantity the lap
   asked me to measure*, stating an estimate for it in the brief is a live anchoring hazard. **Put
   the hypothesis in a sealed section the measurer reads only afterwards.**
2. **§3.2's "the crypt is available."** Naming the substrate made me use it, and the crypt turned
   out to be a poor legibility instrument — no genuinely bright region, and at the ARPG camera
   every HUD region initially measured **0.0000** luminance. I recovered (measure-then-choose
   framings, plus a declared bloom stress), but a purpose-built frame with a real torch pool and a
   character in it would have been a better test and cost less. **The convenience of an available
   substrate quietly substituted for the right one.**

---

## §10 — Artefacts

**Floor (stays — it is the (i) cells' floor):** `/Users/admin/Games/mcp-lab/l8ui/`

| Path | What |
|---|---|
| `FIRST_INTENT.md` | banked verbatim before work |
| `CONTRACT.md` | **the spec the (i) cells build against** |
| `ITERATION_LOG.md` | ★ the lap's payload |
| `ui/hud.tscn` | the HUD (57 authored nodes) |
| `ui/skill_slot.tscn` | slot component (9 nodes, instanced ×9) |
| `ui/palette.gd` | colour + metric tokens, each with its reason |
| `ui/hud.gd` | state driver (renders what it is handed; invents nothing) |
| `ui/cooldown_wipe.gdshader` | radial cooldown sweep |
| `capture.gd` / `capture.tscn` / `shoot.sh` | over-gameplay capture harness |
| `analyse_bg.py` / `legibility.py` / `crop.py` / `census.gd` | the measurement instruments |
| `crypt_substrate.tscn` | 0444, sha-verified copy |
| `out/FINAL_*.png` | 12 stills (9× 16:9, 3× 21:9) |
| `out/SHEET_economies.png` | all six energy economies side by side |

**Signed:** drax, presentation seam, 2026-07-25.
*The engine emits; I render it faithfully. Where the engine had not decided, I said so instead of
deciding for it.*
