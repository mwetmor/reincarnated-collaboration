# VFX P3 — Selection gate (galadriel, 2026-08-24)

**Run:** VFX ARCHETYPE-BINDING RUN, phase **P3** · charter `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executed by:** galadriel (primary judge, R-4), named sub-agent
**Governing:** charter § 3.2 (criterion) · § 3.3 (two-tier parameterization) · § 3.6 (telegraph literacy) · ledger **L-18 / L-19 / L-20 / L-25 / L-26 / L-27**
**Inputs:** `vfx_reference_candidate` (114 rows) + `vfx_archetype` (27 rows) in `agentic_orchestration/research/curated/corpus.db` — **read-only** · 26 dossiers at `agentic_orchestration/research/vfx-p2-dossiers/dossiers/` — **read-only, unmodified** · `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2 verified** (`_schema: gd-kit-framesets/2`, `_revision_note` carries the v1 retraction) · `canonical/reap-die-rise-story/style-register.md` · `drax/notes/2026-08-23-metal-vfx-smoke-probe.md` § 7
**Evidence artifacts:** `agentic_orchestration/galadriel/captures/2026-08-24-vfx-p3-selection/`

---

## 0 · What this note is, and what it is not

This is a **judged selection with receipts**, not a ranking of taste. Every row carries three § 3.2
axis scores, an L-19 causality class, an honest evidence tier, and the confounds I could see. Where
the picture was ambiguous I say so; where I could not see the picture at all I say that too.

**This is also the Judge-To corpus for Step 2's minted gate.** A reference I overclaim here becomes a
target a minted effect is scored against later. An honest 3 beats a flattering 5.

**Read-only discipline honoured:** `corpus.db` was opened `-readonly` throughout; the 26 dossiers were
read and not written; nothing outside `galadriel/` was modified.

---

## 1 · PRE-STEP E-1 — Judgment identity resolver (ledger L-27)

### 1.1 Verdict

> **RESOLVED → the skill is WAR CRY (Soldier mastery). It is NOT Judgment.**
> **Consequence per L-27: the 8 frames in `circle_candidate_unresolved/` are EXCLUDED from the
> `circle` style-candidate pool.** `circle` proceeds on its Codex candidates. The frames are retained
> as *self_buff/ring-adjacent semantics* only — noted, not pooled.

Attempt-2 galadriel's honorable pause was **correct, and its leading hypothesis was correct.** The
name it refused to write down was the wrong name.

### 1.2 Method — icon template-match, instrumented before it was read

L-27 ruled the resolver: match the HUD skill-bar icons in the frames against the published Grim Dawn
icons. I did that, and I **validated the instrument on two known-identity controls before reading the
probe**, because a template-match on 30×30 in-game icons under bloom is a weak instrument and a
single unvalidated number would not have been evidence.

**Reference icons** — fetched from the Grim Dawn wiki via its MediaWiki API (`grimdawn.fandom.com`,
`action=query&list=allimages`; direct page fetches 403 on a bot UA, the API does not). All 40×40 PNG:

| Skill | Mastery | File | Wiki source |
|---|---|---|---|
| War Cry | Soldier | `e1-icons/wiki-warcry.png` | `War_Cry_(Skill)_Icon.png` |
| Judgment | Oathkeeper | `e1-icons/wiki-judgment.png` | `Judgment_(Skill)_Icon.png` |
| Vire's Might | Oathkeeper | `e1-icons/wiki-vires_might.png` | `Vire's_Might_(Skill)_Icon.png` |
| Ascension | Oathkeeper | `e1-icons/wiki-ascension.png` | `Ascension_(Skill)_Icon.png` |
| Eye of Reckoning | Oathkeeper | `e1-icons/wiki-eor.png` | `Eye_of_Reckoning_(Skill)_Icon.png` |

**Probe plate** — `eor-test-1` at t=1398.900 (the moment attempt 2 identified as slot-3-lit, one frame
before the 1400.50 cooldown onset), native 1920×1080, no colour transform:

```
ffmpeg -nostdin -v error -ss 1398.900 -i "$V1" -frames:v 1 -vf "crop=200:60:730:1020" -y probe-plate2.png
```

**Slot geometry derived FROM THE FRAME, not assumed.** Column/row luminance profiling of the icon
band located three icon boxes at plate-x `(17–45)`, `(59–89)`, `(104–134)`, rows `24–53`. My first
pass used assumed offsets from the attempt-2 note and was **7 px off on slot 4** — which is exactly
why the control failed on that pass. Deriving the geometry fixed it.

**Scoring:** zero-mean normalized cross-correlation, RGB, reference bicubic-resized to the detected
box, with a **±2 px jitter budget applied identically to every reference** (so no reference gets a
search advantage). Scores in `e1-icons/E1-ncc-scores.json`.

### 1.3 Result

| Probe | War Cry | Judgment | Vire's Might | Ascension | Eye of Reckoning | Winner | Margin |
|---|---:|---:|---:|---:|---:|---|---:|
| slot 2 — **CONTROL**, known = Vire's Might | 0.3049 | 0.3778 | **0.5867** | 0.2341 | 0.3054 | ViresMight ✓ | +0.2089 |
| **slot 3 — PROBE** | **0.7279** | 0.5440 | 0.3833 | 0.2474 | 0.4333 | **WarCry** | **+0.1839** |
| slot 4 — **CONTROL**, known = Ascension | −0.0188 | 0.0090 | 0.0504 | **0.5144** | 0.0787 | Ascension ✓ | +0.4357 |

**Both controls resolve correctly. The probe resolves to War Cry with the highest absolute score in
the table.** Judgment is second at 0.544 — non-trivial, because both icons are warm-toned figures on
a red-brown field, which is precisely why the controls exist.

### 1.4 The eye agrees, and it is not close

`e1-icons/E1-comparison-sheet.png` — slot 3 (in-game) · wiki War Cry · wiki Judgment · slot 2
(in-game) · wiki Vire's Might, all at 8× nearest-neighbour.

The in-game slot-3 icon and the wiki War Cry icon are **the same artwork**: the same shouting profile
head in three-quarter left view, the same golden burst emanating rightward, the same shoulder line,
the same dark-brown-to-gold ramp. The wiki Judgment icon is a red field with a vertical white column
and downward-radiating wedges — it shares no element with the frame. `e1-icons/E1-control-sheet.png`
carries the two controls side by side at the same scale; both are visually identical to their
references.

### 1.5 Evidence paths

```
agentic_orchestration/galadriel/captures/2026-08-24-vfx-p3-selection/e1-icons/
  E1-comparison-sheet.png            probe + WarCry + Judgment + control pair
  E1-control-sheet.png               slot2|ViresMight  slot3|WarCry  slot4|Ascension  + Judgment
  E1-ncc-scores.json                 the numbers above
  wiki-{warcry,judgment,vires_might,ascension,eor}.png        reference icons (+ -x8 upscales)
  slot{2,3}-t*-x8.png                native in-game icon crops
  probe-plate2.png                   the geometry-derivation plate
  hotbar-slots23-t1400.400-x8.png    cooldown-state plate (slots 2+3 dark, countdown visible)
  matched-frame-crop-t1400.750-peak.png
  matched-frame-crop-t1401.100-ringmax.png    the two usable frames of the now-named event
```

### 1.6 What this closes, and what it opens

- **Closes:** the `circle` GD-frameset question. There is **no first-party GD frameset for `circle`**
  from the L-16 fixtures. T-A should carry that as a provenance note, not a silent gap.
- **Closes:** attempt-2's § 4.3 inference — the build does not slot Judgment. Confirmed by
  elimination across the read hotbar (EoR, Vire's Might, War Cry, Ascension).
- **Opens, mildly:** the 8 frames are now a *named* War Cry event and are therefore usable as a
  **`ring`-adjacent semantics datum**: a player-centred expanding annulus with a propagating front, a
  ground residue, and — as attempt 2 measured — **no contact response on the bodies it overtakes**.
  That is a second independent instance of the same L-19 failure mode as EoR, in a different skill,
  in the same game. I record it as a *finding*, not a candidate. It does not enter any pool.
- **E-2 is not needed** and should not consume Matt's attention at seal. E-1 answered it.

---

## 2 · Method for the main gate

Each candidate judged on the three § 3.2 axes, 1–5, each score tied to a specific cited property:

- **R — Readability at OUR gameplay camera.** Fixed 2.5D isometric-ish, Godot Forward+/Metal. Scored
  against the **P0-b coverage band 0.03 %–67 %** (drax § 7.5) as a sanity envelope: an effect that
  cannot be seen and an effect that eats the fight both fail. Occlusion of the *caster* is scored as
  a defect — that is EoR's failure #2, confirmed in pixels at L-25.
- **P — Parameterizability.** Survives Tier-1 recolour / rescale / motif-swap. A reference whose
  identity lives in one un-swappable texture scores ≤ 3. A reference whose identity lives in
  **geometry, motion or silhouette** scores 5, because those survive every parameter we intend to
  turn.
- **S — Style-register fit**, judged against `canonical/reap-die-rise-story/style-register.md` — the
  locked A-register (bounded stylized-low-poly-3D, Synty; premium carried ~40 % lighting / ~30 % VFX
  / ~20 % material / ~10 % geometry). **Never against source-game polish.** A reference whose effect
  is carried by *light and particles* scores high because those are the levers our register invests
  in and has twice measured at ceiling. A reference carried by high-fidelity mesh/texture detail, or
  by a 2D/top-down grammar that does not transfer to a fixed 2.5D 3D camera, scores lower.

**L-19 causality class** assigned per selection: `physical-cause` / `magical-cause` / `hybrid`. The
rule I applied: **the reference's causality class must match the archetype's nature.** A melee_strike
or ground_slam anchored by an action-decorating reference is a wrong pick even if pretty. An `aura`
or `self_buff` is *correctly* magical-cause — decoration is what it IS, and scoring it down for that
would be applying the criterion where it does not live.

**C-1 (source diversity):** applied at ties only, and I name every place I applied it.
**C-2 (windup scarcity):** flagged per row where the canonical lacks windup footage.

---

## 3 · Per-archetype selection table

`R/P/S` = readability / parameterizability / style-register-fit, 1–5. **Tier:** FRAMES-INSPECTED /
THUMBNAIL-ONLY / DOSSIER-TEXT-ONLY.

| # | Archetype | Canonical (game · skill · URL) | Runner-up | R | P | S | L-19 class | Flags | Tier | Rationale |
|---|---|---|---|:-:|:-:|:-:|---|---|---|---|
| 1 | **aura** | D2R · Conviction · `youtube.com/watch?v=aDa8ZWS8ano` | PoE War Banner / Dread Banner (`2USIImzhApw`) | 4 | 4 | 4 | magical-cause *(correct — an aura's nature)* | **WINDUP GAP** (N on all 5 — coherent, `motion=NULL`); **capture confound: streamer VOD, facecam bottom-left + donation ticker + title card** | THUMBNAIL-ONLY | The substrate's own top exemplar is literally "Conviction aura" — this is the on-substrate "same move" anchor. Chosen because it "communicates influence without filling the radius with opaque effects," which is the coverage-ceiling solve an always-on field needs; **C-1 applied** (3 of 5 candidates were PoE). Runner-up is the clean-capture companion. |
| 2 | **beam_channel** | PoE · Scorching Ray · `youtube.com/watch?v=A2ygiKOfLww` | GD Albrecht's Aether Ray (`aFvCDOf8HHk`) | 5 | 5 | 5 | hybrid — magical body, **physical consequence** (target burn + smoke persists on the body) | **Beam −Z orientation contract** (drax § 7.2) — T-A must carry aim-vector→yaw, not a default transform; lifecycle **sustained** | THUMBNAIL-ONLY (hq; no maxres) | The one archetype with a *measured* parameterizability receipt: the identical beam geometry survives two radically different MTX treatments in this same corpus (`Stygian` black-flame, `Shaper` celestial-white). Identity is in geometry, not texture — 5/5 earned, not asserted. The persistent contact marker is the L-19 discriminator over the alternatives. |
| 3 | **blink** | Lost Ark · Distortion · `youtube.com/watch?v=qEFT27d0IuA` | PoE Harbinger Flame Dash (`-n8g6QtQixc`) | 4 | 4 | 4 | magical-cause | R docked: "dark palette can lose contrast on dim terrain" — our register is dark-mood, so this is a **real** risk, not a footage artifact | THUMBNAIL-ONLY | Full lifecycle, and deliberately chosen from the **non-shared** part of the corpus to discharge the F-e falsifier (§ 4.2). Straight-line displacement *with damage along the path* — the traversal is visible and consequential, which is what `motion=straight_line` asserts. **C-1 applied.** |
| 4 | **chain** | PoE · Celestial Arc · `pathofexile.com/forum/view-thread/2922969` | PoE Automaton Arc (`view-thread/2170338`) | 5 | 4 | 4 | magical-cause | **PoE-forum 403** (Cloudflare, per L-15 — bot-block, not absence); no non-PoE tie existed | DOSSIER-TEXT-ONLY | Only candidate whose notes record **endpoint flashes preserving the hop rhythm rather than reading as one continuous sweep** — hop-discreteness is the archetype's whole identity (`motion=chain_hop`) and the thing that separates it from `beam_channel`. The single non-PoE option (Torchlight) is `flc=0` and explicitly noisy, so **C-1 had no tie to break**. |
| 5 | **circle** | GD · Ring of Steel · `youtube.com/watch?v=nYh9Wij7NUA` | PoE Celestial Warcry Effect (`view-thread/2921459`) | 4 | 5 | 5 | **physical-cause** | **F-a MERGE-CANDIDATE with `ring`** (§ 4.1); no timestamp — Ring of Steel is a segment of a full-mastery showcase | THUMBNAIL-ONLY | The **only** candidate across `circle`+`ring` that is action-CAUSED: real blades erupt, distributed on a literal circumference, with hit reactions on adjacent bodies. Under L-19 that outweighs the subdued 2016 palette — and the palette is scored against **our** register, not GD's, where a ring of simple blade meshes lifted by light is register-1 geometry reaching register-2 exactly as the A-holds ruling measured. **C-1 applied.** |
| 6 | **cone** | D3 · Seismic Slam · `gamestar.de/videos/diablo-3-skill-video-seismic-slam,65244.html` | PoE Celestial Tectonic Slam (`view-thread/2879022`) | 4 | 4 | 4 | **physical-cause** | **403 on fetch** (bot-block, same class as PoE — not verified absent); R docked: "earthy VFX blends with terrain" | DOSSIER-TEXT-ONLY | Literal substrate exemplar ("Seismic Slam"), and the only cone candidate with **enemy launch + knockback** — contact response on bodies, the L-19 axis EoR failed. **C-1 applied.** Runner-up deliberately avoids `ground_slam`'s shared primary (§ 5.3). |
| 7 | **dash_attack** | D3 · Furious Charge · `youtube.com/watch?v=0HvsOpRLqXc` | PoE 2 Shield Charge (`-jrsw_04QWQ`) | 5 | 5 | 5 | **physical-cause** | — | THUMBNAIL-ONLY | Both finalists are physical-cause; Furious Charge wins on merit because its contact response is **distributed along the path** (enemies knocked aside as the body passes), not merely terminal — the closest thing in the corpus to Matt's "clashing into flesh, bone and armour" outside `whirlwind` itself. P=5 because identity is silhouette + knockback with a brief trail: **zero texture dependency**, which is the ideal case for a shared-rig low-poly register. Runner-up is the *pose-carries-the-motion* reference — cite it in T-A for the animation seam. |
| 8 | **defensive_dash** | Hades II · Divine Dash · `youtube.com/watch?v=t3N_IP5Em5A` | Hades Tidal Dash (`BamVo7BTjtQ`) | 5 | 4 | **3** | magical-cause | **MERGE-CANDIDATE into `dash_attack` as a flourish layer** (§ 4.4); **WINDUP GAP** (N on all 5); **S=3: Hades is 2D top-down — the beat structure transfers, the surface does not** | THUMBNAIL-ONLY | Isolates the *defensive beat* — a gold-white deflection flash bound to the mover, with reflected-projectile impacts — "without requiring a persistent path ribbon." That is precisely a **§ 3.3 Tier-1 parameter layer**, not a geometry, which is the substance of my merge verdict. S honestly docked; do not let a 2D grammar set a 3D register. |
| 9 | **fork** | D3 · Elemental Arrow / Frost Arrow · `youtube.com/watch?v=K-eVr9I7xrs` | PoE Celestial Tornado Shot (`_XtINEHQqd0`) | 4 | 5 | 4 | **physical-cause** | R docked: rapid fire obscures branch points — isolated casts are the reference frames | THUMBNAIL-ONLY | "Unusually literal, forward-biased fork_split" — forward bias is correct for `prim=line`, and a solid arrow shattering into arrows is a plausible physical manifestation. **C-1 applied.** Runner-up carries the cleanest split-*node* read; cite it for the branch-point authoring. |
| 10 | **ground_slam** | D4 · Hammer of the Ancients · `youtube.com/watch?v=Q6V9qRmIbgU` | PoE Ground Slam base effect (`NI8590SoqPA`) | 5 | 5 | 5 | **physical-cause** | **No URL timestamp** (combat begins 1:09, in dossier text only) | THUMBNAIL-ONLY | The #1 substrate exemplar string, and textbook L-19: a weapon meets the ground and the ground answers, in a compact circular burst well inside the coverage band. Same franchise-grammar Matt praised. **C-1 applied** (4 of 5 were PoE). Runner-up is intentionally *not* elevated because it is `cone`'s shared primary (§ 5.3). |
| 11 | **ground_targeted_circle** | PoE · Astral Storm Call · `youtube.com/watch?v=lhQiZae-djE` | PoE Celestial Flameblast (`FcsRlt_wjxY`) | 5 | 5 | 5 | hybrid — magical marker, physical strike | ⚠ **100 %-PoE corpus at 115 skills** (§ 6.2) | **FRAMES-INSPECTED** (maxres thumbnail is a clean isolated showcase frame) | **The strongest evidence surface in the entire selection.** The thumbnail alone shows the whole grammar: character legible at frame-left, a crisp thin purple perimeter ring with a translucent interior, and the vertical strike descending into its centre. Marker-then-strike is the § 3.6 telegraph-literacy pattern for the largest archetype in the vote, and it is **two independently swappable layers** (decal + descending payload). Coverage comfortably mid-band; caster not occluded. |
| 12 | **leap_strike** | PoE · Demonic Leap Slam · `youtube.com/watch?v=TVLZ1wX443g` | Last Epoch Fury Leap (`SkYPspTspaM`) | 5 | 4 | 4 | **physical-cause** | **WINDUP DONOR** — the crouch is a genuine anticipation pose, one of the corpus's better windups (relevant to C-2) | THUMBNAIL-ONLY (hq) | "Restrained palette keeps the character trajectory and compact impact radius separable" — mass falls, ground answers, and the caster stays legible. Not a C-1 tie: the non-PoE alternative is explicitly "busier." Cite GD's leap-rune gifs as the *camera-clean* secondary. |
| 13 | **line** | D3 · Bone Spear · `youtube.com/watch?v=peMAi0k5j-g` | PoE Twilight Explosive Arrow (`view-thread/3256281`) | 5 | 5 | 5 | **physical-cause** | **No URL timestamp** (07:40 in dossier text) | THUMBNAIL-ONLY | Literal substrate exemplar, and the **pierce** behaviour is the discriminator that protects the `single_target` boundary (§ 4.5). Pale spear against dark floors is the highest-contrast read in the archetype, and our register is dark-mood. **C-1 applied.** Deliberately avoids the Essence Drain collision with `single_target`. |
| 14 | **melee_arc** | D3 · Grim Scythe · `news.blizzard.com/en-gb/article/20597129/necromancer-update-the-meleemancer` | PoE Celestial Lacerate (`_odu2eo6jP0`) | 5 | 5 | 5 | **physical-cause** | **Media = `gif`** (curation INFO finding); article fetch 200 OK — **a video companion is owed before Step 2** | DOSSIER-TEXT-ONLY | Literal substrate exemplar #1, and the purest L-19 read available: the arc **is the weapon's own path**, not an energy wave chasing it. "Substantially larger than the character, legible through combat clutter," short-lived so it never occludes. Blade-motif swap (scythe→axe→claw) is exactly the Tier-1 axis. **C-1 applied.** Runner-up is the video-backed layered-crescent construction reference. |
| 15 | **melee_strike** | Last Epoch · Rive · `forum.lastepoch.com/uploads/default/original/2X/0/0b88fc443d13e2e232e51cbfe567994741b3f8e0.mp4` | PoE Prismatic Double Strike (`NZ1bj_ysJFA`) | 5 | 5 | 5 | **physical-cause** | **Spot-checked: HTTP 200, 5.36 MB — live official-forum CDN video** | DOSSIER-TEXT-ONLY (verified live) | 115 skills, tied-largest archetype — the row where L-19 matters most. Rive **separates the three authoring layers explicitly** (character motion / weapon trail / hit response) and escalates on the third stroke, giving cadence coupling *and* a Tier-2 flourish hook with no bespoke asset. Physical-cause on every L-19 axis. **C-1 applied.** Runner-up is the cleanest no-confound isolation — use it for frame study. |
| 16 | **multi_projectile** | Last Epoch · Multishot · `youtube.com/watch?v=30kcRWUOKMU` | PoE Demonic Split Arrow (`CPmANn4zDOE`) | 4 | 5 | 4 | **physical-cause** | **No URL timestamp** (0:49 / 2:35 in dossier text); R docked for build-effect clutter — **a footage confound, named and discountable** | THUMBNAIL-ONLY | Makes the three parameter axes *visually explicit* — projectile count, angular spacing, range — which is the § 3.3 requirement rendered as a reference. The PoE alternative is the cleaner capture; I pair them the way L-19 blessed for `whirlwind`: **selected pick + clean-baseline companion.** Discounting a nameable footage confound is the same discipline that keeps Matt's confounded incumbent valid. |
| 17 | **orbit** | Last Epoch · Shurikens with Blade Shield · `youtube.com/watch?v=uUinnDksyzk&t=441s` | PoE Sawblade Blade Vortex (`n3PVnPYuKPI`) | 5 | 5 | 5 | **physical-cause** | **L-12 engine finding stands:** `orbit` is absent from `kit_compiler._RICH_TO_SPATIAL` and is silently gauged `point` | THUMBNAIL-ONLY | **C-1 applied on a genuine tie** — this and the Sawblade candidate match on every axis (solid payload, legible spacing, readable contact, negative space preserved around the caster). Non-PoE takes it. The preserved negative space is the explicit correction of EoR's failure #2 (caster swallowed by own effect). Cite PoE Blade Vortex (`rCro9h8reZw`) for stack-accumulation behaviour. |
| 18 | **placed_lane** | Last Epoch · Frost Wall · `forum.lastepoch.com/t/introducing-the-runemaster-coming-in-runes-of-power/60436` | PoE Stygian Flame Wall (`view-thread/2975769`) | 5 | 4 | 4 | **physical-cause** | Spot-checked HTTP 200; **beam/lane orientation contract applies** (drax § 7.2) | DOSSIER-TEXT-ONLY (verified live) | Endpoint legibility ("bright end pillars") is *the* hard readability problem for a lane at a fixed isometric camera — where does the wall stop? — and this is the only candidate that solves it explicitly. **C-1 applied.** **T-A constraint I am contributing regardless of pick:** at our locked camera any lane with vertical extent must be authored **non-opaque**; the runner-up's "bright base, darker upper wisps, not a completely opaque screen" is the pattern, and drax § 7.5's 67 % ceiling is the reason. |
| 19 | **ricochet_bounce** | Last Epoch · Shield Throw · `youtube.com/watch?v=FuYT1KrQorI` | GD Aegis of Menhir + Avenging Shield (`LTKKgKUMVdk`) | 4 | 5 | 4 | **physical-cause** | No URL timestamp (the "final training-dummy demonstration"); R docked — Manifest Armour procs can mask contacts | THUMBNAIL-ONLY | "Closest mechanical match" with the complete **return leg**, and its training-dummy segment deliberately exposes the individual path legs — the best authoring reference for a multi-segment path. Both finalists non-PoE, so C-1 is satisfied either way. |
| 20 | **ring** | D2R · Poison Nova · `youtube.com/watch?v=2lJi7VTOANQ` | D3 Condemn (`9gyow_LYzzE`) | 5 | 5 | 4 | **physical-cause** (discrete travelling particles) | **F-a MERGE-CANDIDATE with `circle`** (§ 4.1) — and see the strain admission there | THUMBNAIL-ONLY | `burst_around_self` expressed as a **travelling annulus of discrete particles rather than a filled disc**, with an **open centre that preserves character visibility** — the direct correction of the EoR failure mode confirmed in pixels at L-25. **C-1 applied.** Runner-up is the corpus's best **windup donor** for this family (a three-second charge) — cite it for C-2. |
| 21 | **self_buff** | PoE · Illusionist Aura Effect · `youtube.com/watch?v=KDer1UFJ9W8` | D3 Archon (`gamestar.de/videos/diablo-3-skill-video-archon,65241.html`) | 5 | 5 | 5 | magical-cause *(correct — a buff has no physical cause)* | **WINDUP GAP** (N on 3 of 4); **sub-shape finding — see § 6.5**; 3 of 4 candidates PoE, no tie to break | THUMBNAIL-ONLY | 112 skills that will frequently be **active during other skills** — so the governing property is *does not obscure the character*, and this is the only candidate whose notes assert exactly that ("communicates ownership and radius without obscuring the character"). Floor decal + local emitters = two swappable layers on our two cheapest register levers. |
| 22 | **single_target** | PoE · Project Essence Drain Effect · `youtube.com/watch?v=8LIQpG_OtFY` | PoE Ice Spear 3.5 (`cpvThDY-pnM`) | 5 | 5 | 5 | magical-cause | ⚠ **100 %-PoE corpus at 90 skills** (§ 6.2) | **FRAMES-INSPECTED** (maxres thumbnail is an isolated in-flight frame) | Verified at the pixel: the frame shows the payload mid-flight with **body, trail and impact-residue visibly separated**, the target already carrying green contact residue, and — critically — **the trail is narrow enough that it does not read as a beam**, which protects the `beam_channel` boundary (§ 4.3). Runner-up is the physical-cause alternative (solid shards) on identical delivery geometry; cite it for physical-element parameterizations. |
| 23 | **teleport** | D2R · Teleport · `youtube.com/watch?v=YaUOt4_zxjs` | PoE Stygian Flame Dash (`PykOVssTmTo`) | **3** | 4 | 4 | magical-cause | ⚠ **COVERAGE-FLOOR RISK** — "restrained arrival flash" sits near drax § 7.5's 0.03 % floor; **T-A must specify a minimum arrival-burst coverage** or the move will be invisible at our camera | THUMBNAIL-ONLY | The literal exemplar (`Teleport`, `Teleport (Enigma runeword)`) and the exact match to `motion=blink_translate`: cast gesture → **spatial discontinuity** → arrival flash, with no traversal. Deliberately chosen from outside the blink-shared set to discharge F-e (§ 4.2). **C-1 applied.** R=3 is the honest score and it is the most actionable number in this table. |
| 24 | **totem** | PoE · Ancestral Warchief · `youtu.be/53exbcqunns` | GD Mortar Trap (`UGyIZgmVWA0`) | 5 | **4** | 4 | **two-layered:** magical-cause (manifestation) + **physical-cause (the delegate's slam)** | **P=4 ceiling: a summon-delegate needs a MODEL, not only VFX** — this archetype cannot be fully parameterized in the VFX layer; 3 of 4 non-PoE options weaker on the anticipation axis | THUMBNAIL-ONLY (hq) | The only candidate with an explicit **anticipation beat on the delegate itself** (raised-arm before the slam). Telegraph literacy for an autonomous delegate is the hard problem — the player must read that the totem is *about to act*, and no other candidate teaches it. Its clean three-phase separation (summon / delegate-active / impact) is the authoring structure. |
| 25 | **vortex_pull** | Lost Ark · Vortex Gravity · `youtube.com/watch?v=v7mliS8dC40` | PoE Void Sphere (`view-thread/2933919`) | 5 | 4 | 4 | **hybrid — physical initiation → magical field** | ⚠ **AUTHOR-not-SELECT** (drax § 7.6 — we own zero attractor and zero particle-collision content); **no URL timestamp** (10:48 in dossier text); ⚠ **cross-seam: readability is carried by enemy motion, not by VFX** (§ 6.4) | THUMBNAIL-ONLY | An inward pull is inherently magical — but this candidate gives it a **physical cause**: a hammer strike initiates the gravitational eruption. That is the L-19 "plausible physical manifestation" pattern applied to an archetype that would otherwise have no way to earn it, and it is the strongest causality read in the archetype. Non-PoE. Runner-up is the purest sustained-pull motion spec. |
| 26 | **whirlwind** | D4 · Whirlwind (official Blizzard) · `youtube.com/watch?v=3BnHvNZ_4YM` **+ incumbent retained as validated semantics anchor** — `youtube.com/watch?v=KaMPoPywM40` | PoE Celestial Cyclone (`view-thread/2609048`) | 5 | 5 | 5 | **physical-cause — the L-19 exemplar itself** | ⚠ **NOT A DISPLACEMENT — but flagged anyway, see § 6.1**; ⚠ **the "clean baseline" is a general dev video with NO timestamp** (§ 6.1); GD EoR excluded per L-18, retained as negative anchor | THUMBNAIL-ONLY (title-card only; hq 320×180) | "Blade highlights synchronized with the weapon animation… localized hit effects preserve the rotating silhouette without obscuring nearby enemies" is the itemized form of Matt's verbatim criterion, minus both of his named confounds. The composition L-19 anticipated and L-26 confirmed: **owner-validated incumbent = semantics anchor; official clip = clean baseline.** Both rows stay in T-A. |
| — | **`knockback`** | **HELD — zero corpus (F-3, L-14). No selection made.** | — | — | — | — | — | HELD | — | See § 6.6 — I found supporting evidence for the vocabulary-leak hypothesis and record it for gandalf's F-3 disposition. |

### 3.1 Incumbent coverage rating (curation finding F008 — L-26 routed C-4)

**I knowingly leave `whirlwind` r0's temporal-coverage flags UNRATED, and this is a refusal, not an
omission.** Coverage flags in this corpus mean *the dossier lane inspected the phases and recorded
what it saw*. The incumbent was never phase-inspected; I have inspected only its thumbnail. Rating
it from a title card would manufacture a flag of exactly the kind elrond correctly refused to invent.
Its value to the run is not phase coverage — it is that **the owner's eye signed work built from it**,
which no coverage flag can express. `whirlwind` r1 supplies the phase-rated lifecycle.

---

## 4 · Over-split verdicts

My verdict is evidence for the conductor's P4 fold ruling. **gandalf rules; I judge.**

The decisive instrument is the P1 vote's own attested axes (`motion_signature_attested`,
`delivery_class_attested`, `engine_spatial_primitive`). Where two archetypes are **identical on all
three**, any distinction I draw is a distinction I am *reading into the label* — which is the
Discipline #41 hand-imposition the charter forbids at P1 and which I decline to smuggle in at P3.

### 4.1 F-a · `circle` ↔ `ring` — **MERGE-CANDIDATE (strong). F-a FIRES.**

| | `circle` | `ring` |
|---|---|---|
| motion | `burst_around_self` | `burst_around_self` |
| delivery | `zone` | `zone` |
| primitive | `circle` | `circle` |
| skills | 43 | 50 |

**Identical on every attested axis.** And the corpus converged independently, exactly as L-10
pre-registered:

- `circle` r1 and `ring` r1 are **the same URL** — `pathofexile.com/forum/view-thread/3177421`,
  Stormcult Shock Nova Effect.
- `circle` r4 and `ring` r4 are **the same skill**, GD Ring of Steel, at two different URLs
  (`nYh9Wij7NUA` / `TIwfKG231v4`). Two of four `ring` candidates duplicate `circle` candidates at
  skill identity.

**The falsifier test, answered honestly.** elrond's § 5 falsifier: *"if P3 lands different canonical
references without strain, the convergence was researcher sampling."* I did land different
canonicals — GD Ring of Steel for `circle`, D2R Poison Nova for `ring`. **But I could have swapped
them and every word of both rationales would still hold.** That is strain, and I will not disguise it
as discrimination. The property I leaned on (`ring` = open travelling annulus, `circle` = filled
simultaneous burst) is read off **the English words**, not off the substrate, which is identical.

**Verdict: MERGE-CANDIDATE, strong.** If gandalf folds them, my canonical for the merged class is
**GD Ring of Steel** — it is the only action-CAUSED reference in either pool, and under L-19 that is
decisive. D2R Poison Nova becomes the open-centre/annulus **variant reference**, and D3 Condemn the
windup donor. Nothing is lost by folding; a real § 3.6 telegraph-literacy asset is *gained*, because
one shared radial-burst grammar is easier for a player to learn than two that look alike anyway.

### 4.2 F-e · `blink` ↔ `teleport` — **DISTINCT.**

| | `blink` | `teleport` |
|---|---|---|
| motion | **`straight_line`** | **`blink_translate`** |
| delivery | `motion` | `motion` |
| primitive | none | none |

**The motion signature differs, on the substrate's own axis.** This is not a distinction I invented —
it is the attested value, and it is legible in the candidates without any added criterion: `blink`
candidates carry a **visible traversal** (Flame Dash's trail, Distortion's shadow streak, *damage
along the path*); `teleport` candidates carry a **spatial discontinuity** (D2R Teleport: "no
continuous bodily travel").

I landed different canonicals **without strain, from non-shared material, in different games**:
Lost Ark Distortion vs D2R Teleport. Neither is one of the shared candidates.

**Verdict: DISTINCT. The convergence was researcher sampling** — and elrond's own alternative reading
is the correct one. The two shared primaries are **Shadow Strike** and **Lightning Warp**, which are
precisely the skills that instantiate *both* mechanics. Zero-context researchers reaching for the
same boundary skills from two directions is evidence that the boundary cases are real, not that the
classes are one. **F-e does not fire.**

### 4.3 `beam_channel` ↔ `line` — **DISTINCT (clean).**

`straight_line`/**`beam`**/`line` vs `straight_line`/**`projectile`**/`line`. Delivery class differs
at substrate. It also differs in **lifecycle class** per drax § 7.4 — a beam is *sustained*, a
projectile is a travelling *burst*, and § 7.4 measured that spread at >5×. Different lifecycle
classes cannot share one VFX selection.

Confirmed at the pixel: `single_target`'s canonical frame shows a trail "narrow enough that it does
not read as a beam." The boundary is visible, not merely asserted.

### 4.4 `defensive_dash` / `self_buff` / `totem` — **split verdict.**

- **`self_buff` ↔ `totem`: DISTINCT, trivially.** Both `motion=NULL`, but delivery differs —
  **`aura`** vs **`summon_delegate`** — and the canonicals are not remotely confusable (a floor decal
  on the caster vs an autonomous ancestor performing its own slams). Zero strain.
- **`defensive_dash`: MERGE-CANDIDATE — but into `dash_attack`, not into these two.** This is the
  finding the watch-list pairing did not anticipate. `defensive_dash` has **`motion=NULL` AND
  delivery unbanded AND no engine primitive** — it is defined by *nothing attested*, on 4 members, at
  T4. But its `motion=NULL` is **an artefact of missing banding, not an attested no-path class**:
  Divine Dash and Dashing Strike plainly have straight-line paths, and **all five curated candidates
  are dashes**. Its `windup=N` across all five is the signature of an unbanded class, not of a
  pathless one.
  **Recommended disposition:** fold into `dash_attack` and carry "defensive" as a **§ 3.3 Tier-1
  parameter layer** (i-frame / deflect flourish), not as its own archetype. My canonical for it —
  Hades II Divine Dash — is itself the argument: it isolates a *deflection flash bound to the mover*
  "without requiring a persistent path ribbon." That is a layer, not a geometry.

### 4.5 `ground_slam` ↔ `melee_strike` — **DISTINCT on emitter geometry; substrate-identity caveat named.**

| | `ground_slam` | `melee_strike` |
|---|---|---|
| motion | `point_strike` | `point_strike` |
| delivery | `melee_arc` | `melee_arc` |
| primitive | `point` | `point` |

**Identical on all three attested axes** — the same shape as F-a, and I flag it as such. But unlike
`circle`/`ring`, the two candidate corpora separate on a property that is *visible in the footage and
consequential for authoring*: **which surface receives the strike.** `ground_slam` canonicals strike
the **ground plane** and propagate a radial/fan decal from a floor point; `melee_strike` canonicals
strike an **enemy body** and produce a body-anchored contact spark with no ground propagation. Those
are different emitters, different anchor transforms, different coverage profiles.

**Verdict: DISTINCT** — merging them would collapse a floor-decal emitter and a body-anchored spark
into one selection, which is the same class of error L-11 caught in the `_RICH_TO_SPATIAL` merge hop.
**Caveat for the conductor:** this distinction is *not* carried by the three attested axes, so if P4
adopts substrate-only merge authority, `ground_slam`/`melee_strike` is the **second-strongest merge
candidate after `circle`/`ring`** and should be ruled explicitly rather than left implicit.

### 4.6 `blink` ↔ `dash_attack` — **DISTINCT, but on the L-19 axis, not the substrate axes.**

Both are `straight_line`/`motion`/none — **identical on all three attested axes** (a third such pair).
They separate on **causality class**, which is a Matt-ruled criterion of record (L-19), not one I
invented: `dash_attack` is **physical-cause** (body mass collides, contact response along the path);
`blink` is **magical-cause** (displacement). L-19 states that parameterization must preserve causality
class — so one reference cannot anchor both, by the run's own law.

They also separate on § 3.6: the player must read *"he is closing to hit me"* differently from
*"he is escaping."* Merging them would destroy exactly the telegraph literacy L-11 protected.

**Verdict: DISTINCT** — with the same honest caveat as § 4.5.

### 4.7 Unregistered adjacency I noticed: `orbit` ↔ `whirlwind`

Not on the watch-list, but both are `orbit_fixed`/`motion`, differing only on primitive
(`orbit` absent from `_RICH_TO_SPATIAL` per L-12; `whirlwind` = `circle`).
**Verdict: DISTINCT, comfortably.** In `orbit` the **payload** revolves around a stationary-framed
character (blades, shurikens, hammers); in `whirlwind` the **character** rotates and the payload is
the character's own weapons. Different parent transform, different causality emphasis, and the two
canonicals share nothing. Recorded so it is ruled rather than assumed.

---

## 5 · Shared-primary audit of my own selections

I checked that no URL and no skill anchors two archetypes.

| Pair (from curation § 5) | Did it contaminate my picks? |
|---|---|
| `blink` ↔ `teleport` | **No.** Neither canonical is a shared candidate (§ 4.2). |
| `circle` ↔ `ring` | **No URL collision** — but see § 4.1; the separation is nominal, not substantive. |
| `cone` ↔ `ground_slam` | **No.** PoE Ground Slam (`NI8590SoqPA`) is a shared primary; I made it **runner-up on both sides and canonical on neither.** |
| `aura` ↔ `circle` | **No.** Stygian Plague Bearer selected for neither. |
| `line` ↔ `single_target` | **No.** Essence Drain is `line` r4 and `single_target` r2 — I took D3 Bone Spear for `line`, so it anchors only `single_target`. |
| `line` ↔ `vortex_pull` | **Non-signal.** The collision is PoE forum thread `3098201`, a *Vaal Orb MTX pack* showcase covering several skills. A thread collision, not a skill collision. Neither is a canonical. |

**Result: 26 canonicals, 26 distinct URLs, 26 distinct skills.** No double-anchoring.

---

## 6 · Flags for the conductor

### 6.1 Incumbent — **NOT displaced. But the "clean baseline" needs work before P4 seal.**

Per L-18(c) I must never displace silently. **I am not displacing.** My judged outcome for
`whirlwind` is exactly the composition L-19 anticipated and L-26 confirmed: the Matt-validated
incumbent stays as **semantics anchor of record**, and `whirlwind#1` serves as the **confound-free,
phase-rated clean baseline**. Both rows belong in T-A.

**But — flagging anyway, because it changes which URL a builder opens first:**

> ⚠ **`whirlwind#1` (`3BnHvNZ_4YM`) is not a Whirlwind clip.** oEmbed title:
> **"Diablo IV Quarterly Update Blog — Combat Improvements"**, official `@Diablo` channel. The
> thumbnail is a **title card** ("DIABLO IV — VFX: Combat Improvements"), and no `maxresdefault`
> exists — the upload is low-resolution (hq 320×180).

It is first-party Blizzard VFX material, so its *provenance* is sound and arguably ideal — but it is
a **general dev video in which Whirlwind is an un-timestamped segment.** L-26 read it as "official
Blizzard D4, full lifecycle," which is defensible for the footage inside it but misleading as a
reference a builder can open and use. **Owed before P4 seal:** a timestamp, and a check that its
resolution is adequate for frame extraction. If it is not, Matt's incumbent — which *is* a real
Whirlwind clip — carries more of the load than L-26 assumed, and its confounds matter more.

### 6.2 C-1 · PoE concentration — **discharged in selection, with two forced residuals**

Corpus is 53.5 % PoE (62/114 including PoE 2). **My canonical set is 7/26 = 26.9 % PoE** — the
concentration is halved at the point where it would have hardened into a register.

Non-PoE canonicals: Diablo III ×4, Last Epoch ×5, Diablo II: R ×3, Diablo IV ×2, Lost Ark ×2,
Grim Dawn ×1, Hades II ×1. C-1 was applied as an explicit tiebreak in rows 1, 3, 5, 6, 7, 9, 10, 13,
14, 15, 17, 18, 20, 23 and is named in each.

> ⚠ **Two archetypes had NO non-PoE option at all — their entire dossier is PoE:**
> **`ground_targeted_circle`** (115 skills, the largest archetype in the vote, and only **3**
> candidates — the charter floor) and **`single_target`** (90 skills). **205 skills, ~18 % of the
> voted corpus, anchored on a single studio's VFX grammar with no alternative in evidence.**
>
> This is C-1's warning arriving in its most concrete form, and selection cannot fix it — there was
> nothing to choose between. **Recommendation: a bounded non-PoE supplementary hunt for these two
> archetypes before P4 seal** (D3 Meteor / Blizzard / Firebats and D4 Blizzard for the first; D2R
> Glacial Spike / Bone Spirit and D3 Ray-of-Frost-class for the second are all named in the substrate
> exemplars and none was reached for). Both jobs sit at the top of the T1 tier by skill count, so the
> yield-per-job is the highest in the run.

### 6.3 Timestamp discipline — **systematic, actionable, and it will cost Step 2 real hours**

Several canonicals point at a *moment inside a long video*, and the timestamp lives only in the
dossier prose, not in the URL. The corpus is inconsistent about this — `dash_attack` r3/r4/r5 carry
`&t=` params; most others do not.

Affected among my canonicals and near-canonicals: `vortex_pull` (10:48), `ground_slam` (1:09),
`multi_projectile` (0:49 / 2:35), `line` (07:40), `ricochet_bounce` ("final training-dummy
demonstration"), `circle` (a segment of a full-mastery showcase, no time given), `whirlwind#1` (none
at all), `defensive_dash` r1 (**54:33 — inside a stream**), `leap_strike` runner-up (~4:15).

**Recommendation: T-A carries `t_start` / `t_end` columns**, populated from `why_it_fits` where the
dossier stated a time and marked `TBD` where it did not. Cheap now; expensive later.

### 6.4 `vortex_pull` — two flags, one of them cross-seam

1. **AUTHOR-not-SELECT** (drax § 7.6): we own zero attractor and zero particle-collision content. The
   reference is a *spec*, not a pack-selection. Already anticipated at L-20; confirmed here at the
   selection.
2. **The archetype's readability is carried by a non-VFX system.** In every candidate, the inward
   vector is legible because **enemies visibly move** — "enemy displacement," "large enemy
   displacement," "enemy movement supplies an especially readable inward vector." No VFX we mint can
   supply that. **`vortex_pull` cannot be validated at Step 2's minted gate on VFX alone**; it needs
   engine-side enemy displacement to read at all. Routing this to gandalf as a P4 cross-seam note.

### 6.5 `self_buff` carries two sub-shapes under one archetype

Its 112 skills split visibly in the corpus between a **decal/shell buff** (Molten Shell, Illusionist
Aura, Immortal Call — the caster remains the caster) and a **transformation** (Archon; and the
substrate's own exemplar list contains **`Werewolf`** and **`Fade`**). A transformation replaces the
silhouette entirely; a decal buff must not touch it. These are opposite requirements on the same
property, and one canonical cannot serve both. **Recommend T-A carry a sub-flag** (`buff-decal` /
`transformation`), with D3 Archon as the transformation reference. Not a merge question — a
*split* question, and the only one I found.

### 6.6 `knockback` — HELD, with supporting evidence for the F-3 vocabulary-leak hypothesis

No selection made (zero corpus, F-3 held per L-14). Recording what I can see, for gandalf's
disposition: `knockback` is the **only** archetype in the vote with **`motion=NULL` AND delivery
unbanded AND `engine_spatial_primitive` absent AND a single member** (`Ancient Spear (Rage Flip
rune)`). Every other archetype has at least one attested axis or an engine primitive. That profile
is consistent with a vocabulary leak rather than a real class. It is also the same *shape* as
`defensive_dash` (§ 4.4) — two unbanded T4 classes, one with 1 member and one with 4 — which
suggests the residue of unbanded skills is worth one look as a group at a future lap.

### 6.7 Corpus smells — smaller items

- **`melee_arc`'s canonical is a `gif`** on a Blizzard news article (fetch 200 OK). It is the right
  reference on merit; a **video companion is owed** before it anchors a 76-skill archetype at Step 2.
- **`aura`'s canonical is a streamer VOD** with a facecam, a donation ticker and a title card
  occupying the frame. Chosen anyway — it is the substrate's literal exemplar and the confound is
  nameable and discountable, which is the same standard that keeps Matt's confounded incumbent valid
  — but the confound belongs in T-A's provenance note, not hidden in a score.
- **403s are bot-blocks, not absences** — confirmed on `pathofexile.com` (known, L-15) and
  `gamestar.de` (new; same Cloudflare signature, 5.6 KB challenge page). Do not let a future
  automated link-check read these as dead.
- **`teleport`'s R=3 is the most actionable score in the table.** A "restrained arrival flash" near
  drax's 0.03 % coverage floor is a move the player will not see at our camera. T-A should carry a
  **minimum arrival-burst coverage** for this archetype specifically.
- **`totem`'s P=4 is a real ceiling, not a mark-down.** A summon-delegate needs a *model*; Tier-1
  element parameterization can recolour its attack but not its body. 97 skills sit behind that
  limit and it should be stated in T-A rather than discovered in Step 2.

---

## 7 · What the Mirror saw

The corpus was assembled by twenty-six workers who could not see each other. Where they reached for
the same material, the run's instinct was to suspect duplication — and in one place it was right, and
in one place it was exactly wrong. `circle` and `ring` are one thing wearing two names: the substrate
says so on every axis it measures, and my own two rationales could be swapped without a word
changing, which is the plainest confession a judge can make. `blink` and `teleport` are two things
that happened to be photographed at the same crossroads, because Shadow Strike and Lightning Warp
genuinely stand in both roads at once.

And the sharpest thing in the glass is not a merge at all. It is that the eight frames nobody would
name have now been named, and the name is the one the pause leaned toward — **War Cry, not
Judgment.** The honourable refusal to write down a probable-wrong name preserved the corpus for a
day, and a fifteen-minute icon match repaid it. That is the discipline working exactly as designed:
**nothing guessed, nothing polluted, and the answer arrives anyway.**

Twice now — Eye of Reckoning, and now War Cry — the same failure has shown itself in the same game:
an effect that expands, that leaves a mark on the ground, and that **never touches the bodies it
passes through**. Matt named it from taste before either audit ran. The pixels have now agreed with
him twice, in two different skills, by two different instruments. That is no longer an opinion about
Grim Dawn. It is a measured property of a whole way of making effects — and the single clearest thing
this run has to teach the thing we build next.

---

*galadriel, 2026-08-24. Read-only on `corpus.db`, on all 26 dossiers, and on every working tree
outside `galadriel/`. No dossier byte was modified. No sub-agents invoked (HARD NO, standing).*
