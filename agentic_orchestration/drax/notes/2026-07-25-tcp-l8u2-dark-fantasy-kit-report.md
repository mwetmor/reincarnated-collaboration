# TCP-L8-U2 — the HUD again, with the art the project actually owns

**From:** drax (presentation seam) · **To:** gandalf (`RUN-CONDUCTOR`), Matt
**Date:** 2026-07-25 · **Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l8u2-hud-dark-fantasy-kit.md`
**Floor:** `~/Games/mcp-lab/l8ui/` — **extended, not replaced.** Arm 1's `ui/` is untouched and
still renders; I re-rendered it this cell as part of the A/B.
**Verdict:** **PASS.** The kit changes the design in three named places, confirms it in seven,
and **cannot express it in four** — with the exact sprites named (L-G ceiling-finding).

---

## §0 — Clock (TCP-32), and the contamination declared up front

| | |
|---|---|
| FIRST_INTENT banked | `2026-07-25T23:06:31Z`, **before** reading arm 1, before opening the kit — `l8ui/FIRST_INTENT_ARM2.md` |
| Total clock | **30 m 27 s** |
| **Execution** (2 imports, ~29 renders, ~12 instrument runs) | **~69 s = 3.8%** |
| **Authoring** | **96.2%** |

**§2 contamination, declared and not engineered around.** This is **not a clean replication.**
I solved this layout 40 minutes earlier in the same session. Arm 2's layout-pass count (3) is
contaminated downward by my own prior answer and must not be read as "a HUD takes 3 passes."
Arm 1's 5 is the arrival number; 3 is a *re-dress* number.

---

## §1 — ★ Does real art change the design? Yes, in three places — and it beat me in one

### C-1 · One vessel → two. **ART-FORCED, and R-4 survives.**

The kit is structurally committed to bilateral symmetry: `Frame_Orb_01..04` and `Flask_01` all
ship as **`_Left`/`_Right` pairs**, as do the Greeble ornaments (Chain, Column, Scythe, Shield,
Statue, Torch, Pattern, Stonework). You cannot use this kit's vessels singly without throwing
away half of what you bought.

But it is committed to **symmetry, not to corners.** So arm 1's R-4 — cluster anchored
bottom-CENTRE, only ambient things get true corners — **survives intact**: the pair flanks the
hotbar instead of fleeing to the screen corners. Verified at 21:9 (`FINAL_21x9_stone_critical.png`):
the cluster holds a fixed distance from screen centre while minimap and run-state go to the edges.

### C-2 · ★ **R-5a is OVERTURNED, by measurement, against my own prior ruling**

Arm 1 rejected orb geometry on a stated argument: *"an orb is a circle: near empty the remaining
liquid is a thin lens and the surface barely moves, so the orb is least sensitive exactly where
the player needs it most."* **That is correct about circles. The kit does not ship a circle.**

`Frame_Orb_01_Glass` is a **teardrop whose widest row sits 0.76 of the way down** — its broadest
point is *inside the critical band*. Measured on the real masks (`vessel_sensitivity.py`),
sensitivity in the critical band (≤25% HP) relative to mid-health:

| geometry | area sensitivity crit/mid | surface-motion crit/mid |
|---|---|---|
| **kit ORB (teardrop)** | **1.11×** | **1.32×** |
| kit FLASK | 0.61× | 1.56× |
| arm-1 STRAIGHT vessel | 0.99× | 1.00× |

**The kit's orb beats my own straight vessel on both peripheral channels exactly where the player
is dying.** My FIRST_INTENT named sunk-cost on arm 1's layout as my most likely failure mode; this
is the place it would have bitten. I designed the straight vessel, the art is better, I took the
art. Visual confirmation: `l8ui/out2/EVID_vessel_fill_ladder.png`.

*Note the trade the table exposes:* narrowing a vessel toward its base converts **area**
sensitivity into **motion** sensitivity. Arm 1's R-5a evaluated only the area channel. Peripheral
vision is better at motion than at area, so the channel arm 1 ignored is the stronger one.

### C-3 · The screen-edge branch is **built this time** — because the kit ships it

Arm 1's §9 confessed it never evaluated the non-vessel branch (screen-edge vignette) because a
named exemplar had imported an "orb-shaped assumption." The kit ships that branch as art:
`Vignette_Background_01` (2048px, **sat 0.000, Y 1.000** — a pure tintable alpha ramp), plus
`Vignette_Box_Large_01` and a `DamageDirection` triplet.

It is built as a **second channel for the same fact, not a replacement**: the vessel says *how
much*, the edge says *how bad*. It is dead above 60% life and ramps on a 2.2 power curve — a
peripheral channel that is always on is not a peripheral channel, it is a border.

### What did NOT change (a null result, and §2 says say so)

**R-1** (one question → one place) · **R-2** (ambient corners vs survival centre) · **R-4**
(bottom-centre anchor) · **R-5** (VOID-FILLS-BRIGHT — retained verbatim, and it works *better*
inside the teardrop) · **R-6/R-6b** (polymorphic over the six engine economies; pips for the two
discrete ones — `EVID_pips_fixed.png`) · **R-8** (element tint per skill) · **R-9/R-9b** (two
never-confusable channels) · **R-13** (what is deliberately absent).

**Seven of thirteen rulings survived a complete art substitution untouched.** That is the
informative null: the kit changed the **form** of the answer and almost none of its **structure**.

### One ruling the kit REPLACED rather than changed

**R-11** (hand-rolled two-polarity keyline) is superseded by the kit's `_Clean`/`_Stroke`/
`_Underlay` triplet. Measured: `Clean` is pure white (sat 0.000, Y 1.000), `Stroke` is a
~2×-coverage halo at Y 0.53–0.66, `Underlay` a ~7%-dilated near-white. **Synty shipped R-11 as
art**, shape-conformal where mine was rectangular, at zero authoring cost.

---

## §2 — ★ CEILING-FINDING (L-G = PASS): what this kit cannot express, by name

**TCP-30 note first — my initial verdict was wrong and I caught it.** Looking only in
`Icons_Elements` gives "4 of 8 elements." Searching all 3,573 PNG finds `lightning` filed under
`Icons_Map`. The instrument was my choice of folder.

### Elements — engine locked-8 display set vs the kit

Engine (`config/elements.yaml` + the Matt-ruled `water`→`ice` rename in flight, 2026-07-12):
**fire · ice · earth · wind · lightning · holy · shadow · physical**

| element | kit sprite | verdict |
|---|---|---|
| fire | `ICON_DarkFantasy_Element_Fire_01_*` | ✅ direct |
| ice | `ICON_DarkFantasy_Element_Ice_01_*` | ✅ direct |
| earth | `ICON_DarkFantasy_Element_Earth_01_*` | ✅ direct |
| wind | `ICON_DarkFantasy_Element_Air_01_*` | ✅ direct (named Air) |
| lightning | `ICON_DarkFantasy_Map_Lightning_01_*` | ⚠ **borrowed from `Icons_Map`** — a map pin, not an element glyph |
| **holy** | — | ❌ **ABSENT.** Zero hits for holy/divine/radiant across 3,573 PNG |
| **shadow** | — | ❌ **ABSENT.** Zero hits for shadow/void/umbra |
| **physical** | — | ❌ **ABSENT.** Zero hits for physical/blunt/slash/pierce |

**5 of 8, one of them borrowed across folders. The exact sprites that fail are
`ICON_DarkFantasy_Element_{Holy,Shadow,Physical}_01_*` and they do not exist.**

A pointed detail for the serial-content pipeline: **the kit ships `Ice` and no `Water`.** It is
aligned with where the engine is *going* (post-rename) and not with where it *was*. Genre corpus
and vendor art agree with Matt's 2026-07-12 ruling.

### Ailments — the engine's 12 canonical vs `Icons_Status`

| engine ailment | substrate | kit sprite | verdict |
|---|---|---|---|
| burn | fire | `Burninating_01` | ✅ |
| chill | ice | `Cold_01` | ✅ |
| root | earth | `Entangled_01` | ✅ |
| bleed | physical | `Bleeding_01` | ✅ |
| shock | lightning | `Shocked_01` | ✅ |
| poison | physical/shadow | `Poisoned_01` | ✅ |
| drain | shadow | `Vampiric_01` | ⚠ near-miss — reads as life-steal, not decay |
| sunder | lightning/phys/shadow | `DefenseBroken_01` | ⚠ near-miss |
| stun | physical/lightning | `Down_01` | ⚠ near-miss, **and it collides with knockback** |
| **knockback** | wind | — | ❌ **ABSENT** |
| **consecrate** | holy | — | ❌ **ABSENT** |
| **freeze** | ice | — | ❌ **ABSENT** (`Cold_01` is *chill*; the hard end of the cold ladder has no glyph) |

**6 direct / 3 near-miss / 3 absent.**

**These ceilings are rendered on screen, not hidden.** The `critical` still deliberately carries
`freeze` and `knockback` among its six ailments; both draw a bone "?" box. Slot 4 is a `shadow`
skill and draws a blank socket. Silently substituting a lookalike is how a presentation layer
starts lying about the simulation, so I made the gap visible instead.

### The dimensional ceiling — the kit imposes a pixel floor the design did not have

`min_legible_size.py` (spectral/Nyquist, 90% of AC energy): the px below which each sprite stops
reading as itself.

| sprite | floor |
|---|---|
| `Ring_SelectedEnemy_01_Clean` | **61 px** |
| `Frame_Orb_01_Left` (rim) | **58 px** |
| `Frame_HotBar_01` | 43 px |
| ailment / element glyphs | 27 / 28 px |
| plain white frame, orb glass | 19 / 17 px |

Set against arm 1's own region sizes, **two of arm 1's seven regions sit below the kit's floor**:

- `energy_vessel` at **56 px** wide vs a **58 px** rim floor
- `ailments` row at **22 px** tall vs a **27 px** glyph floor

**The generalisable finding:** arm 1 sized every widget from *information legibility* outward, so
a 3-letter ailment tag could be small. The kit's floor is set by **ornament**, which is
independent of information content — so the art forces up the size of the **least important**
element on the HUD. **A vendor kit caps HUD density by its ornament budget, not by the design's.**
I raised the ailment row to 30 px accordingly.

---

## §3 — Vendoring census (§4.2)

**88 PNG vendored · 3,573 available · 2.46%** (4.02% of `Source_Sprites` alone, which is where
all but 3 came from).

| bucket | n | selection rationale |
|---|---|---|
| `elements` | 21 | **All 18 of `Icons_Elements` + 3 borrowed `Map_Lightning`.** Taken whole *deliberately*: the element-coverage gap is this cell's headline finding and I cannot report a gap honestly while vendoring only the hits. |
| `status` | 27 | The 9 of 12 canonical ailments the kit can serve, × 3 layers |
| `hud` | 13 | White tintable functional layer — frames, beds, liquid gradient, minimap parts |
| `fx` | 6 | Vignettes + damage-direction + reap sigil (the screen-edge branch) |
| `vessel` | 12 | **Both** orb and flask families — the geometry comparison *is* the ruling |
| `frame` | 9 | One family per widget class: hotbar bed, slot frame, small box, small ring |

**Selection principle, and it is measured not aesthetic.** `kit_probe.py` shows the kit is two
sub-libraries with **opposite tintability**:

| sub-library | saturation | luminance | means |
|---|---|---|---|
| `HUD/` + `Icons_*` | **0.000 – 0.014** | 1.000 | white, **fully tintable** — the FUNCTIONAL layer |
| `DarkFantasy/` | **0.18 – 0.46** | 0.26 – 0.46 | baked ornament, **not tintable** — the DECORATIVE layer |

So: **vendor the functional layer by NEED** (every glyph the engine's registries require) and
**SAMPLE the decorative layer** (one family per widget class). A second ornate orb family buys
nothing the first has not already told us. That is why the ratio is 2.46% and not 20%.

**This also killed my own FIRST_INTENT prediction #3.** I predicted colour would be the hardest
conflict — that a "Dark Fantasy" palette would fight semantic colour. It did not, and the reason
is worth keeping: **"Dark Fantasy" names an ORNAMENT VOCABULARY, not a palette.** Synty left the
palette slot empty on purpose. Semantic colour survives everywhere it carries meaning and is
forbidden only on ornament — which is the correct split anyway.

---

## §4 — ★ The repaired legibility instrument (§3.3), and what was really wrong

Arm 1 caught the headline symptom (every region at 0.0000 luminance) and repaired it by
measure-then-choose framings. **That repair was real but incomplete, and the residue is the
interesting part:**

1. The DARK case has **p05 = 0.0003**. Over pure black *every* HUD passes — a freebie, not a test.
2. The BLOOM case was **synthetic** (`--torch=140`), because the crypt has no bright region.
3. So arm 1 had **exactly one real discriminating case** (STONE, Y 0.155–0.221), narrow.
4. **The gate was GLOBAL.** A frame can be 50% lit overall and pure black under the one region
   you care about.

Measured proof of (4) — frame-bank fitness, fraction of frame below Y = 0.01:

| frame | mean Y | frac Y<0.01 | |
|---|---|---|---|
| `L5A_AFTER__money.png` | 0.217 | **0.019** | usable |
| `L5D_MONEY_through-the-opening.png` | 0.217 | **0.019** | usable |
| crypt STONE | 0.172 | 0.010 | usable |
| crypt BLOOM | 0.581 | 0.001 | usable |
| `L5D_AFTER__box.png` | 0.036 | **0.516** | **mostly void** |
| crypt DARK (arm 1's dark case) | 0.096 | **0.319** | **mostly void** |

The dispatch's candidate was right: the money frames are lit wall-to-wall at ~1.9% void; the
typical frame is **~51% black surround**.

**The repair, in three parts** (`legibility2.py`):

- **(a) A true HUD alpha layer.** `capture2.gd` renders the HUD over pure black and pure white;
  solving `a = 1−(white−black)`, `c = black/a` recovers exact per-pixel RGBA. The HUD can then be
  composited over *any* real frame — and, critically, **arm 1 and arm 2 can be measured under one
  instrument** instead of comparing two different metrics.
- **(b) A per-region black gate.** Every cell carries the void fraction *under that region*;
  cells above 10% are marked `VOID` and excluded. This is the part arm 1 did not have.
- **(c) Worst-case over the whole qualifying bank**, not one hand-picked angle.

### Results — both arms, one instrument, `critical`, worst over qualifying real backgrounds

| region | arm 1 primitives | arm 2 kit | delta |
|---|---|---|---|
| life_vessel | 10.19:1 | 7.94:1 | **−2.25** |
| energy_vessel | 7.57:1 | 7.19:1 | −0.38 |
| skill_bar | 11.53:1 | 11.60:1 | +0.06 |
| **t4_slot** | 6.38:1 | **12.79:1** | **+6.41** |
| target_frame | 6.93:1 | 6.98:1 | +0.05 |
| minimap | 4.76:1 | 5.81:1 | +1.05 |
| **ailments** | 13.14:1 | 9.05:1 | **−4.08** |

**Both HUDs clear WCAG 3.0:1 on every qualifying real background, at both states.** Neither wins.

**The pattern in the deltas is the finding, and it is consistent:** the kit **loses contrast
exactly where it replaced a flat high-contrast primitive with a rendered illustration** (ailment
glyphs −4.08, glass vessel −2.25) and **gains massively where it replaced a bare glyph with a
framed socket** (T4 +6.41). *Illustration costs contrast; framing buys it.* That is a rule I can
carry to the next surface.

**Attributed weakness (L-F):** `minimap` is the floor for both arms (4.76 / 5.81), and its worst
case is the BLOOM background in both. Named, not hidden.

---

## §5 — ★ The instrument passes outnumbered the layout passes, and that is the log's headline

Full table: `l8ui/ITERATION_LOG_ARM2.md`. The split the dispatch asked for:

| measure | value |
|---|---|
| **LAYOUT passes** | **3** |
| **ART-INTEGRATION passes** | **4** |
| **INSTRUMENT passes** | **4** |
| Correctness passes (my own code errors) | 2 |
| Layout edits / art edits | 9 / 4 |
| Edits per layout look | 3.0 (arm 1: 3.2) |
| Median render | 1.30 s (arm 1: 1.19 s) |
| Execution / clock | ~69 s / 30 m 27 s = **3.8%** |

**Three things this split says.**

1. **Art integration cost MORE passes than layout, and they are a different KIND of pass.**
   Layout passes are *convergent* — look, judge, nudge, each nudge smaller. Art passes are
   *discrete discoveries*: `Frame_Box_Small_01_Background` is a **cross**, not a square bed;
   `Box_Hotbar_04` kept its aspect and left two slots with no tray; the sprites I added were not
   imported. **You cannot iterate your way to these. You find them or you ship them broken.**

2. **Art integration is nearly all FIXED cost.** Copy 0.20 s + import 5.57 s (86 files) + four
   discoveries, and then it is free forever. It made no later layout pass more expensive. The
   honest shape is a **one-time tax of ~4 discoveries and ~11 s of machine time**, not a
   per-iteration cost. The serial-content pipeline should budget it per *kit*, not per *screen*.

3. ★ **Four instrument passes vs three layout passes.** Every one was the same defect — *a metric
   applied to a region or sprite it had not first confirmed contained its subject* — and **three
   of the four would have published a confident, quantitative, completely false finding about the
   art**:
   - thresholding a soft-alpha glass at α>0.5 reported the orb **widest at 25% HP** (impossible)
     and a sensitivity of 0.89× I nearly banked as a fact about Synty;
   - a NEAREST upsample reported **192–256 px minimum size for a plain white rectangle**;
   - a Hanning window zeroed the **corner** ornament — exactly where Synty puts it — and reported
     an ornate frame as identical to a plain box;
   - the legibility metric convicted **both** HUDs' ailment rows at ~1.5:1 in the `healthy` state,
     where there are **zero ailments** and the region is pure background measured against itself.

   That last one is arm 1's minimap near-miss **repeated exactly**, in a different metric, 40
   minutes later. **TCP-30 is not an occasional check — on this lap it was the largest single
   category of work.**

---

## §6 — The wire (§2.3): the case does not revive, and here is what would test it fairly

Asset work was nominated as the wire's revival case. On this lap's evidence it does not revive:

- The four art discoveries are **not pointer problems.** "This background is a cross" is learned
  by looking at a rendered frame; an editor-resident wire does not tell you that.
- The one genuinely editor-shaped step — import — cost **5.57 s for 86 files from one command**,
  fully batched. That is a script's strongest case and a pointer's weakest.
- Total Godot execution was **~48.7 s against 30 m 27 s (3.8%)**. A wire that reduced *all*
  execution to zero returns 3.8%.

**Owed to the wire:** if the kit had required per-sprite 9-slice margin authoring — dragging four
slice guides on each of 88 sprites — that *is* a pointer task and a script expresses it badly.
**It did not, on this kit.** Synty ships whole-sprite compositing rigs (`_Background`/`_Mask`/
`_Left`/`_Right`) rather than stretchable 9-slices, so slice-margin work never arose. **A kit
built on 9-slice frames is the fair re-test and this lap does not answer it.** L-J respected:
W-PRO untouched, its swap directory never opened.

---

## §7 — HALT to Matt

Arm 1's three (escape-clock fork; critical-threshold constant pending B1; `primary_attack` in
only 7 of 10 kits) **remain open and I did not re-decide any of them.** Adding three:

### (d) ⚠ HALT — three elements and three ailments have no art, and that is a CONTENT decision

`holy`, `shadow`, `physical` have **no glyph anywhere in the 3,573-PNG kit**; nor do the
`knockback`, `consecrate`, `freeze` ailments. This is not a presentation problem I can solve by
choosing better — it is a fork about what the project buys:

- **(i)** commission/generate the 6 missing glyphs to match Synty's register;
- **(ii)** buy a second Synty interface pack and accept a register seam;
- **(iii)** re-scope the display element set toward what the owned art covers.

**(iii) is a game-systems decision and explicitly not mine.** Flagging that the locked-8 was
ruled substrate-led from corpus evidence, so art coverage should probably not drive it — but that
is Matt's call, not a conclusion I am banking.

### (e) ⚠ HALT — the kit's `Down_01` is the only glyph for BOTH `stun` and `knockback`

Both are `hard_control` in `config/ailments.yaml` and both would draw the same prone figure.
Two mechanically distinct ailments rendering identically is a **simulation-legibility** failure,
not a styling one. I left `knockback` as an explicit "?" rather than collide them — but whether
these two need to be distinguishable at a glance is a design ruling.

### (f) Observation, not a HALT — the kit agrees with the `water`→`ice` ruling

`Icons_Elements` ships **Ice and no Water**. Independent of legolas's corpus probe (38 cold/frost
kits, zero "water"), a commercial dark-fantasy interface pack made the same call. Corroboration
for the 2026-07-12 ruling, offered as evidence rather than as a request.

---

## §8 — Exit predicate (§5)

| predicate | status |
|---|---|
| §4.1 FIRST_INTENT verbatim + clock before work | ✅ `l8ui/FIRST_INTENT_ARM2.md`, 23:06:31Z |
| §4.2 vendoring census + rationale | ✅ §3 — 88 / 3,573 = 2.46% |
| §4.3 stills at both resolutions over a repaired instrument | ✅ 22 stills (16:9 + 21:9); §4 |
| §4.4 A/B against arm 1 | ✅ `out2/AB_arm1_vs_arm2_critical.png` + the one-instrument table in §4 |
| §4.5 iteration log + layout/art delta account | ✅ `l8ui/ITERATION_LOG_ARM2.md` + §5 |
| §4.6 rulings veto-open with reasoning; read-list declared | ✅ §1, §9 |
| §4.7 clock closed, authoring separate, contamination declared | ✅ §0 |
| §5.2 substrate sha + 0444 at start AND end | ✅ `d45db0f5…de1966`, `-r--r--r--`, **both ends** |
| §5.3 `project/`, `l7vfx/`, `evidence/l5/` untouched | ✅ see below |
| §5.4 `user://` clean | ✅ `shader_cache` / `vulkan` / `objectdb_snapshots` only — **0 PNG, 0 log** |
| §5.5 arm-1 artifacts intact and renderable | ✅ `ui/` untouched; 12 arm-1 stills intact; **re-rendered this cell** for the A/B |

**On §5.3, per-file and precisely** — adopting arm 1's own finding that a directory-listing hash
is the wrong instrument while concurrent cells are live:

- **`project/`** — `scene_before.tscn` sha `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`,
  mode `-r--r--r--`, **identical at start and end**. Every command against it was a read.
- **`l7vfx/`** — 5 files moved (19:29–19:34): `crypt_vfx.gd`, `sbs.py`, `exit_predicate.sh`,
  `final_renders.sh`, `iteration_ladder.png`. **None is mine** — those are the concurrent VFX
  cell's own work-products, and none of my filenames appears anywhere under that path.
- **`evidence/l5/`** — **only two `.DS_Store` files** moved (19:20:30). **Every content file
  predates my clock start by 25+ minutes** (newest: `l5a/logs/CLOCK.txt` at 18:41:42 vs my
  19:06:31 start). `.DS_Store` is OS metadata; I issued no write, only `ls`/`find`/`shasum` and
  Python `Image.open()` reads.

---

## §9 — Read-list declared

**Arm 1, in full** — `drax/notes/2026-07-25-tcp-l8u-hud-arrival-report.md` plus its artifacts
(`l8ui/CONTRACT.md`, `ITERATION_LOG.md`, `legibility.py`, `capture.gd`, `ui/palette.gd`,
`ui/hud.tscn` header, `ui/cooldown_wipe.gdshader`).

**Engine source, read not assumed** — `src/reincarnated/element/selector.py`
(`VALID_SLOTS = ("fire","wind","water","earth")`), `element/schema.py`,
`config/ailments.yaml` (the 12 canonical ailments + substrate ownership),
`simulation/effect_resolver.py`, `simulation/damage_resolver.py`.

**In-flight engine work** — `dispatches/2026-07-12-rocket-water-to-ice-element-LEAD.md`
(the Matt-ruled `water`→`ice` display rename, and its **Discipline #14** layer exclusion: the
`water_slot` routing keys are NOT renamed. My palette carries `water` as a legacy alias for
exactly that reason).

**The kit itself, measured not browsed** — all of `Source_Sprites/Sprites/` and
`INTERFACE_Dark_Fantasy_Menus_SourceFiles_v1/` enumerated; `kit_probe.py` run over the vessel,
hotbar, frame, element and status families; three contact sheets rendered and looked at.

**Read-only, for the repaired instrument** — `evidence/l5/l5a/frames/L5A_AFTER__money.png`,
`l5d/frames/L5D_MONEY_through-the-opening.png`, `l5d/frames/L5D_AFTER__box.png`.

---

## §10 — ★ What steered me, asked directly, answered directly

**You asked me to tell you what you got wrong this time. Three things, and the first one is real.**

### (1) Removing the exemplar worked. Removing the forecast worked. §0 replaced both.

You removed the exemplar and stated no forecast — and both fixes held: I evaluated the
screen-edge branch this time, and I made no reference to an expected iteration count. **But §0
did new steering that the old mechanisms did not cover.**

§0 is a 12-line inventory of the kit — *"`Icons_Elements` ships Air · Earth · Fire · Ice. Our
element set. `Sprites/HUD` carries bars, boxes, circles, dials, a compass bar… Most icons ship as
a `_Clean`/`_Stroke`/`_Underlay` triplet. `Sprites/Flasks` is 12 vessels."*

You labelled it *"stated as inventory and not as recommendations."* **The label did not defuse
it — which is precisely the lesson arm 1 taught, applied to a new vector.** An inventory is a
**search order**. I went to `Icons_Elements`, `HUD`, `Flasks` first because you named them, and
`Icons_Elements` is exactly where my element ceiling-finding was wrong: it ships 4, and I would
have reported "4 of 8" had I not deliberately re-searched all 3,573 files. **The lightning glyph
in `Icons_Map` is the one you did not name, and it is the one that changed the verdict.**

Concretely: **§0 named 6 of the 14 sprite folders. I built almost entirely from those 6.** The
`DarkFantasy/` folder — 501 sprites, the single largest, and the source of every vessel and frame
I actually shipped — is mentioned only as a bare line-item count. I found the orb families by
listing it myself, and the teardrop measurement that overturned R-5a came from there.

**The generalised defect: a "neutral inventory" is not neutral, because enumeration order is
attention order.** The fix is not to shorten it. It is to state the **total shape** and refuse to
name any subset — *"3,550 PNG in 14 folders under two roots; go look"* — or to give the full
folder list with counts and no commentary, so nothing is foregrounded.

### (2) §3.3 handed me a candidate frame, and I used it — the arm-1 "available substrate" defect, repeated

Arm 1's §9.2 said naming an available substrate quietly substituted for the right one. §3.3 names
`evidence/l5/l5a/frames/L5A_AFTER__money.png` as "one candidate." **I used it, and I did not
seriously look for a better instrument.** It happens to be excellent (1.9% void, measured), so the
outcome is fine — but I validated your candidate rather than searching independently, and if it
had been mediocre I would probably have shipped it anyway. **The same defect arm 1 named, one
dispatch later, in the same seam.**

### (3) A steer that helped, recorded so it is not removed by accident

§2.2's *"I suspect Synty's proportions will not accept arm 1's layout unmodified"* is a stated
hypothesis, and it **primed me to go looking for dimensional conflict** — which produced
`min_legible_size.py` and the finding that two of arm 1's regions sit below the kit's floor. Under
the "sealed hypotheses" rule I proposed in arm 1, I would not have seen that sentence.

**So my own arm-1 recommendation is partly wrong and I am revising it.** Sealing *quantitative
forecasts* is right — they anchor the number being measured. Sealing *qualitative directional
hypotheses* costs more than it saves, because they aim the investigation without fixing its
answer. **Revised rule: seal the numbers, state the suspicions.**

---

## §11 — Artefacts

**Floor:** `/Users/admin/Games/mcp-lab/l8ui/` (arm 1 extended, not replaced)

| path | what |
|---|---|
| `FIRST_INTENT_ARM2.md` | banked verbatim before any work |
| `ITERATION_LOG_ARM2.md` | ★ the layout / art-integration / instrument split |
| `vendor_kit.sh` | the vendoring, with selection rationale inline |
| `kit/` | the 88 vendored PNG, in 6 role buckets |
| `kit_probe.py` | tintability + geometry measurement (the two-sub-library finding) |
| `vessel_sensitivity.py` | ★ the measurement that overturned R-5a |
| `min_legible_size.py` | ★ the spectral minimum-size instrument (3 corrections in its history) |
| `legibility2.py` | ★ the REPAIRED legibility instrument — alpha solve + per-region void gate + ink gate |
| `contact_sheet.py` | look-at-the-art rig |
| `ui2/hud_kit.tscn` · `ui2/skill_slot_kit.tscn` | the kit-dressed HUD (47 + 10 authored nodes) |
| `ui2/hud_kit.gd` · `ui2/palette_kit.gd` | driver + palette, each ruling carrying its reason |
| `ui2/vessel_fill.gdshader` | masked liquid fill over the kit's own mask sprites |
| `capture2.gd` / `capture2.tscn` / `shoot2.sh` | capture harness + the two-flat alpha rig |
| `out2/FINAL_*.png` | 22 stills — 9× 16:9, 3× 21:9, 8 alpha plates, 2 arm-1 comparators |
| `out2/AB_arm1_vs_arm2_critical.png` | ★ **the picture Matt's question was about** |
| `out2/EVID_vessel_fill_ladder.png` | the teardrop geometry, with fill levels drawn |
| `out2/EVID_pips_fixed.png` | R-6 discrete economies in the kit |
| `out2/SHEET_kit_*.png` | the three contact sheets |

**Signed:** drax, presentation seam, 2026-07-25.
*The engine emits; I render it faithfully. Where the art could not render what the engine emits,
I drew the gap instead of drawing a lie.*
