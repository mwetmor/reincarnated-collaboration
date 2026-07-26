# DISPATCH — TCP-L8-U3: the HUD at compositional depth

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25, at the owner's eye, on seeing arm 2's stills.
**Lap:** L8 UI (T4-UI), **arm 3.** Arms 1 and 2 are yours and are not blind to you
(`drax/notes/2026-07-25-tcp-l8u-hud-arrival-report.md`, `…-l8u2-dark-fantasy-kit-report.md`).

## §0 — What this cell honestly is

**This cell is product-first and measurement-second, and I am saying so up front** rather than
dressing a polish pass as an experiment. Matt saw arm 2 and said *"The HUD looks so much better with
the synty-dark-fantasy assets, but it can still be SO much better!"* That is the reason this cell
exists. The tool question rides along; it does not lead.

**The measurement that does ride along is a real one and it is new.** Arm 1 measured *layout* cost.
Arm 2 measured *art-integration* cost and found it FIXED (§5 of your arm-2 report). Arm 3 measures
**compositional-depth cost** — the delta from *"the kit is wired"* to *"the kit is used the way its
own author composes it."* The question the serial-content-emission pipeline needs answered is:

> **Is polish a FIXED cost per surface, or does it SCALE with the number of surfaces?**

If fixed, the pipeline is fine and every future surface pays the same toll once. If it scales, the
pipeline has a content-cost problem that nobody has priced. **Your iteration log split by category is
the payload again** — but the categories this lap are *composition*, *asset acquisition*,
*instrument*, and *defect-repair*, and you should invent better ones if these are wrong.

## §1 — The owner's brief (Matt's, verbatim — HIS rulings, not my steer)

Reproduced in full and unedited. **These are the owner's design directions.** Treat them as rulings
you may implement, and — exactly as you overturned my R-5a by measurement in arm 2 — **as rulings you
may dissent from with evidence.** A measured "this is worse, here is the picture" is a PASS.

> The HUD looks so much better with the synty-dark-fantasy assets, but it can still be SO much
> better! Please review these and/or have drax review these and let me know if you can see all of the
> ways in which we could still improve things?
>
> One thing I notice right away is that there is a "taking damage bloody screen" asset which will fit
> over our generic red color at the edges of the screen.
> Another thing I notice is that there are tons of other colors for the mana globe which we could
> simply swap out color to solve for the combo/rage/etc.. Alternatively, we could swap that clobe
> completely for other types of bars/guages that are available.
> ALSO, there are great mini-map icons which we have not taken advantage of.
> Another thing is that there are more interesting thematic pieces that we can pair; e.g. a bar under
> the skills with wins that matches the health and mana pots which also have wings (not that we need
> the wings, but our bar under the skills right now isn't fully covering the skil boxes and they
> overlap it looking a bit clumsy. I do kind of like the bat wings theme with small skull on top
> and/or the candle on top of globes theme with medium skull on top.
> Also there are character portraits and it would be cool to have one for our character.
> There are other icons like a level counter which could be a good addition.
> Also there is an enemy health bar we could use and dark fantasy fonts for the letters such as enemy
> or player names as well as monster power level which can be indicated by a skull.
>
> Check them all out here in these synty recommended HUD use screenshots:
> `matt_notes_handoff_docs/recent-synty-packs/synty-dark-fantasy-hud-recommended-uses`

**Six reference screenshots live at that path** (`.webp`, 1568×882): action bars · hotbars ·
HP-bars/stats · compass-minimap-portraits · a tinted-variants sheet captioned *"Components can be
easily customised"* · a fullscreen-VFX sheet captioned *"Fullscreen damage FX included"*. **They are
the authoring reference for this cell** — they show how the kit's author composes these parts, which
is the thing arm 2 had no view of.

## §2 — My own read of arm 2's output, offered as observation, not instruction

`DRIFT-CRITIC` against **my own arm-2 dispatch.** These are things I see in
`out2/FINAL_16x9_stone_critical.png`. **Every one is contestable and none is a requirement:**

1. **The globes read desaturated** — dull grey-pink and dull grey-blue, not the saturated dark-cored
   glass in the reference sheets. Suspicion (not a finding): the tint is landing on the whole 4-layer
   stack rather than only the fill, or the fill is flat where the reference fill is a gradient.
2. **The three assemblies float as separate widgets with gaps between them.** In every reference
   composition the globes and the tray are **one continuous piece of ironwork.**
3. **Skill icons are small inside their slots** and the keybind numerals overlay the art.
4. **The buff/element row above the tray has no frame** — it floats as bare glyphs plus bare text.
5. **The boss name is bare centred text.** No plate, no bar, no rank mark.
6. **The minimap is a plain dark square** with a thin frame.
7. **Type is engine-default sans** throughout, which is the single loudest "placeholder" signal on the
   screen.

**Matt named none of 1, 2, 3, 4, or 7.** He named additions; several of the biggest wins may be
repairs. **Weigh them yourself.**

## §3 — The total shape of the substrate (complete census, no subset named)

Arm 2's steer finding (**enumeration order became attention order**) was yours and it was correct, so
this dispatch names **every** PNG-bearing directory with its count and highlights nothing. 3,573 PNG ·
3,407 FBX total across `matt_notes_handoff_docs/recent-synty-packs/`.

```
501 Source_Sprites/Sprites/DarkFantasy            136 …Menus/Core/Icons_Input/Switch
371 …Menus_SourceFiles_v1/Sprites/DarkFantasyMenus 130 Source_Sprites/Core/Icons_Input/SteamDeck
339 Source_Sprites/Sprites/Icons_Weapons          128 …Menus/Core/Icons_Input/SteamDeck
180 Source_Sprites/Sprites/Icons_Status           128 …Menus/Core/Icons_Input/SteamController2026
139 Source_Sprites/Sprites/Icons_Inventory        114 Source_Sprites/Core/Icons_Input/Switch
137 Source_Sprites/Sprites/Icons_Resources         90 Source_Sprites/Core/Icons_Input/Xbox
105 Source_Sprites/Sprites/HUD                     90 …Menus/Core/Icons_Input/Xbox
 93 …Menus/Sprites/Icons_DarkFantasyMenus_Flat     83 Source_Sprites/Core/Icons_Input/PlayStation
 78 Source_Sprites/Sprites/Icons_Map               83 …Menus/Core/Icons_Input/PlayStation
 72 …Menus/Sprites/Icons_Menu                      50 Source_Sprites/Core/Icons_Input/GamepadGeneric
 60 Source_Sprites/Sprites/Icons_Stats             50 …Menus/Core/Icons_Input/GamepadGeneric
 58 …Menus/Sprites/General                         38 Source_Sprites/Core/Icons_Input/MouseKeyboard
 57 Source_Sprites/Sprites/Reticles                38 …Menus/Core/Icons_Input/MouseKeyboard
 37 …Menus/Sprites/Icons_DarkFantasyMenus          23 Source_Sprites/Sprites/FX
 24 …Menus/Sprites/Icons_Settings                  21 …Menus/DarkFantasyMenus
 18 Source_Sprites/Sprites/Icons_Elements          18 Source_Sprites/Samples
 12 Source_Sprites/Sprites/Flasks                  10 …Menus/Sprites/FX
  9 …Menus/Sprites/Cursors                          7 Source_Sprites/Core/Icons_Social
  7 …Menus/Core/Icons_Social                        6 Source_Sprites/Sprites/Cursors
  2 Source_Sprites/Textures                         2 Source_Sprites/Core/Branding
  2 …Menus/Textures                                 2 …Menus/Sprites/Fonts
  2 …Menus/Core/Branding
 (+ synty-animations/**/Textures ×5 dirs, 20 files — the animation packs, not this cell's business)
```

**One structural fact worth stating because it changes the denominator:** ~1,158 of the 3,573 are
**controller/keyboard input prompts** duplicated across both packs (six platform families). They are
not addressable HUD surface until we support gamepads. **You vendored 88; the arguable addressable
pool is nearer ~2,350 than 3,573.** Whether that reframes your 2.46% is yours to judge and report.

**You have already measured the substrate's internal split** (arm-2 §: `HUD/` + `Icons_*` at
saturation 0.000 = tintable/functional; `DarkFantasy/` at 0.18–0.46 = baked/decorative). **That
measurement is load-bearing for this cell and is yours** — re-use it, extend it, or overturn it.

## §4 — Constraints (six)

1. **Method is H (headless GDScript).** L-H binds: this cell's variable is *compositional depth*, not
   tool. Do not change tool and depth in the same cell. **W-PRO stays parked (L-J).** If you form a
   view that a specific step here was wire-shaped, record it as an observation for a future cell.
2. **Floor: `~/Games/mcp-lab/l8ui/`** — extend again; keep arm 1 and arm 2 intact and renderable so a
   three-way comparison is possible. A new project is acceptable if you judge cohabitation dirty; say
   which and why.
3. **Vendor whatever the design needs and census it again.** The vendoring ratio is a tracked number
   across arms; the *rate of change* of that ratio under a depth pass is itself the finding.
4. **The legibility instrument you repaired in arm 2 carries forward unchanged** unless it is wrong,
   in which case fix it and say so. Arm 2's four instrument passes vs three layout passes is on the
   record as the largest work category; **budget for that honestly rather than being surprised by it.**
5. **Same two resolutions**, so all three arms are comparable.
6. **Forbidden floors:** `~/Games/mcp-lab/project/` (substrate — read-only copy-out only; sha
   `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444, verify at start and
   end) · `~/Games/mcp-lab/evidence/l5/` · `~/Games/mcp-lab/l7vfx/`. Per your own arm-2 finding, use
   **per-file sha, not a directory listing-hash**, while other cells may be live.

## §5 — Sealed numbers, stated suspicions (your arm-2 recommendation, adopted)

**I state no iteration count, no cost, and no forecast of any kind.** What I will state, per your own
*"seal the numbers, state the suspicions"* ruling, are directional hypotheses with no magnitudes:

- I suspect **composition is where the perceived quality gap lives**, more than asset count.
- I suspect **type is disproportionately load-bearing** relative to how cheap it is.
- I suspect **the second visual register in this pack is deliberate** and that using it deliberately
  buys an information hierarchy for free. Finding the registers is yours; I am not naming them.
- I suspect **there is at least one whole interaction surface in this kit that nobody in arms 1–3 has
  thought to build**, and that finding it is worth more than perfecting the bottom strip.

**All four may be wrong. Overturning one with a picture is a first-class result.**

## §6 — What you ship

1. **FIRST_INTENT banked verbatim + authoring clock started before any work** (TCP-32).
2. **A design account of the reference screenshots** — what the kit's author does compositionally that
   arms 1–2 did not, in your words, with the sprites named.
3. **The build**, at both resolutions, over the repaired legibility instrument.
4. **A three-way A/B**: arm 1 (primitives) · arm 2 (kit wired) · arm 3 (kit composed), same HUD state.
5. **Per-item disposition of Matt's §1 list** — implemented / implemented-differently / dissented,
   each with the reason and, where you dissented, the picture.
6. **The iteration log split by category**, and the **fixed-vs-scaling verdict on polish cost** (§0).
   If the data cannot support a verdict, say that — a stated "not answerable from one lap" is a PASS.
7. **A ceiling list** in the arm-2 style: named sprites that do not exist for things the design wants.
8. **Rulings, veto-open, with reasoning. Read-list declared. Clock closed, authoring separate from
   execution.**

## §7 — Exit predicate

1. §6.1–§6.8 present. 2. Substrate sha + 0444 verified at start AND end, per-file. 3. `l7vfx/` and
`evidence/l5/` demonstrably untouched by you. 4. `user://` clean. 5. **Arm 1 and arm 2 artifacts still
intact and renderable** — the three-way A/B is the cell's headline picture and it dies if either
predecessor is disturbed.

**Honorable fallback (L-F):** attributed blocker + best partial dressing is a **PASS.**
**Ceiling-finding is a PASS (L-G).**

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u3-compositional-depth-report.md`

**HALT to Matt:** any game-systems decision not yet made. **Six are already open from arms 1–2 and are
NOT yours to re-decide** — the escape-clock fork; the critical-health threshold; `primary_attack`
missing from 3 of 10 kits; the six missing element/ailment glyphs as a content-purchase fork;
`Down_01` serving both `stun` and `knockback`; the ice/water corroboration. **Add to that list; do not
resolve from it.** In particular: **what a portrait, a level number, a monster rank, or an enemy bar
should SAY is a game-systems question** — dress the slot, do not invent the value.

---

## §8 — AMENDMENT, landed AFTER launch (2026-07-25, post-dispatch)

**I had no live channel to you when this arrived. Best effort — if you never re-read this file, the
record still shows what I knew and when.**

**Owner ruling (Matt, verbatim): "We don't need the weapon wheel, but an inventory screen will be
VERY useful."**

1. **The weapon wheel is STRUCK.** Do not spend a pass on it.
2. **★ I planted a steer at it.** §5's fourth suspicion — *"there is at least one whole interaction
   surface in this kit that nobody in arms 1–3 has thought to build, and finding it is worth more
   than perfecting the bottom strip"* — points almost directly at the wheel, and it is now pointing
   at a vetoed surface. **Retract it and read §5 as three suspicions, not four.** This is a fourth
   conductor steer-defect of a new kind: not mis-aimed, but *stale* — correct when written, wrong
   within the hour, and unreachable. Log it against me.
3. **A seventh reference screenshot landed** in the same folder:
   `11_INT_DarkFantasyHUD_HUD_ARPG_02_*.webp` — a **full ARPG composition**, not a component sheet.
   It shows the whole screen assembled: minimap with a run-timer, a level badge, the bottom hotbar
   with flanking globes, a full-width bottom rail, a loot window, an equipment paperdoll, an item
   card, and an inventory grid. **The bottom-strip and screen-frame parts of it ARE arm 3's
   business** and it is the best evidence yet of how the kit's author composes at full-screen scale.
4. **The inventory / equipment / item-card surface is NOT arm 3.** It is its own cell (arm 4) with
   its own spec, because unlike the HUD it has a **locked canonical contract** to be built against.
   **Do not build it here** — building it here would destroy the comparison arm 4 exists to make.

---

## §9 — CONTINUATION after an agent stall (2026-07-25)

**Your session stalled — no stream progress for 600 s, watchdog did not recover. This is
infrastructure, not you, and it is the SECOND stall in this session** (L7-V stalled the same way at
its close-out step). Two in one session is a pattern and it is logged against the harness, not
against either of us.

**Your last words before the stall, and they are a finding:**

> *"The rim doesn't contain the fill — the glass and ring sprites have different ink centres. Let me
> measure the offset and correct it properly."*

**RESUME. Do not restart.** I verified your floor myself before writing this; here is what is on disk
and it is substantial:

- `ui3/hud_deep.gd` **753 lines** · `ui3/palette3.gd` 176 · `ui3/orb_fill.gdshader` 78 · `hud_deep.tscn`
- `kit3/` **70 PNG** across assembly 6 · bar 9 · flat 8 · fx 5 · map 26 · ornament 9 · portrait 7 —
  **and `kit3/font/` is EMPTY, which I read as you independently hitting the typeface ceiling.**
- `out3/` — `T_first` → `T5`, plus `S3_greebles` / `S3_hotbars` / `S3_orbs` sheets, `PROBE_heads`,
  `PROBE_example_characters`, `PROBE_ge_Tendrils_01/02`, `ITER_01_both_tendrils`, and crops
  `C_orb` / `C_orbR` / `C_assy` / `C_top` / `C_full`.

**I looked at `T5.png` and `C_orb.png`.** The composition landed: portrait + level badge sited, a boss
plate with a rank mark, a framed buff row, a circular minimap with chrome, and the bottom assembly
reading as **one continuous piece** rather than three floating widgets. **The defect you named is
visible and you diagnosed it correctly** — in `C_orb` the fill spills past the rim at lower-left and
the ring's lower arc is buried. Finish that fix.

### Accounting under a stall (declare, do not engineer around — §2 of arm 2, your own rule)

1. **Wall-clock is corrupted; iteration count is not.** Report authoring time as **two segments with
   the stall gap named**, and do not sum them into a single clean number.
2. **Bank a FIRST_INTENT reconstruction, marked as reconstructed**, if the original was never written
   to disk. A reconstructed intent labelled as such is worth more than a missing one and far more
   than a silently back-dated one.
3. **The stall itself is a datum for the bake-off** — an authoring method whose agent dies at 600 s of
   quiet is a method with a session-length ceiling. Say whether you were doing something unusually
   long-running at the moment it went quiet, or nothing at all. That distinction matters.

### Owner rulings that landed while you were down

- **Weapon wheel: STRUCK** (see §8). My §5 fourth suspicion is retracted.
- **Inventory / equipment / item-card is NOT yours** — it is arm 4, against a **locked 10-slot
  canonical contract** the engine already emits. Do not build it here.
- **Reference `11_INT_DarkFantasyHUD_HUD_ARPG_02_*.webp` is in the folder** — the full ARPG
  composition. The bottom-strip, screen-frame, portrait, level-badge and minimap parts of it are
  yours; the panels are not.

**Everything in §0–§7 still governs.** Close out to the report path in §6 and the exit predicate in §7.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).
**Name anything in this dispatch that steered you.** Three of my steers are on the record from arms
1–2 — anchoring a commissioned quantity, labelling a steer instead of removing it, and letting an
enumeration order become an attention order. **This dispatch tries to answer all three: no numbers, no
exemplars, and a census with nothing highlighted. Tell me what it does wrong instead.** And note the
one channel I cannot self-audit: my Agent launch prompt. **It will contain one sentence — a pointer to
this file — so that everything that could steer you is in the committed record.**

---

## §10 — RETRACTION IN PLACE: §9 ratified a cause it had not measured (gandalf, post-cell)

**§9 says, above: *"The defect you named is visible and you diagnosed it correctly."* The second half
of that sentence is FALSE and it is struck.** The symptom was real; the cause was not a registration
offset, and no offset could have fixed it. Measured by me after the fact, with PIL, on the sprites
themselves:

| sprite | alpha bbox (512 px canvas) | reading |
|---|---|---|
| `Frame_Orb_01_Glass` | y[0, 511] at **every** threshold 0.02→0.30 (cover 74.8% → 51.8%); at 0.50 the top **amputates** to y[63, …] | touches BOTH canvas edges — a **vertical gradient sheet**, not a silhouette |
| `Frame_Orb_01_Left` | y[12, 496] x[20, 492] — touches nothing | this is the container |

**No threshold yields a disc. Therefore no "ink-centre offset" exists to be corrected.** Had the
executor trusted my ratification, the entire second segment would have gone to tuning offsets toward a
solution that cannot exist. The real fix was structural and was found by measuring: a 720-angle polar
sample put the true annulus at **r = [185.5, 203.5]**, and the sheen centroid at **(+0.160, −0.469)**
proved the kit lights from the upper RIGHT while the shader was keyed upper LEFT.

**Standing law born here — L-Q (charter §3):** *a conductor may confirm that a SYMPTOM is visible in a
picture; he may NEVER confirm a CAUSE he has not measured.* Seeing is free; causing is not.

**Two aggravating defects on the same launch, also mine:** the Agent launch prompt was **four
sentences, not the one this dispatch promised** — my own TCP-47 ④ fix violated on its second use — and
**"Start at §9"** put the incorrect ratification ahead of the primary material.

---

## Completion record

**Executed by:** drax (presentation seam) · **Closed:** 2026-07-25 · **Verdict: PASS.**
**Report:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u3-compositional-depth-report.md` (542 lines).
**Floor:** `~/Games/mcp-lab/l8ui/` — extended; arms 1 and 2 intact and **re-rendered as the A/B's own
inputs**, which is what proves them renderable.

**The program-level result** — polish is **FIXED PER COMPONENT FAMILY**, not per surface and not per
register. Registers amortise legibility and type; they do **not** amortise geometry. Category split
across **34 passes**: measurement 44% · defect-repair 18% · composition 15% · looking 15% · instrument
6% · reference 6% · acquisition 3% — and the single 4-layer un-co-registered orb took **44% of the
lap's whole measurement budget**. Instrument cost was **2 passes, not the 4 I budgeted.**

**Product:** portrait frame + level badge sited · boss plate with rank mark · framed buff row ·
circular minimap with chrome · the bottom assembly reading as **one continuous piece**. Through arm
2's own unmodified instrument arm 3 wins every region (ailments **+5.12**, minimap **+9.49**, target
frame **+4.29**) and recovers what arm 2 lost to arm 1. Where it loses it says so — arm 1's flat
vessels win `healthy` by 1.28 / 5.14: *"a flat saturated rectangle is unbeatable on a contrast
metric."* **Illustration costs contrast; framing buys it.**

**~977 baked sprites recovered** by a 6-line luminance-preserving retint shader — arm 2's measurement
was right and its conclusion was wrong; *un-tintable by `modulate`* ≠ *un-tintable*. Second
consecutive lap in which the executor overturned his own prior ruling by measurement. Honest ceiling
beside it: `Orb_03` / `Orb_06` have no closed annulus and cannot host a fill.

**Ceilings: seven**, the flat one being `kit3/font/` **EMPTY** — the kit ships no typeface, so Matt's
"dark fantasy fonts" item is a purchase, not an authoring pass. **Six new HALTs to Matt.**

**Exit predicate:** met, and independently confirmed by the conductor — substrate
`d45db0f5…de1966` at `-r--r--r--`; arms 1+2 intact (40 PNG in `out2/`); `AB3_full_critical.png`
998×1785, three arms stacked.

**Steer reported:** my §2's seven observations, captioned *"none is a requirement,"* were consumed in
order — his D-1/D-2/D-3 are my §2.2/§2.1/§2.7. **TCP-49 ⑥ generalises: the defect is not about
inventories, it is about ORDERED LISTS FROM AN AUTHORITY**, and it bites harder on a critique than on
a census because a critique already carries the conductor's judgment. Plus the **stale steer** — my §5
fourth suspicion pointed at the weapon wheel, which Matt vetoed after launch; retracted in place at
§8 rather than deleted.

**Ledger:** TCP-52.
