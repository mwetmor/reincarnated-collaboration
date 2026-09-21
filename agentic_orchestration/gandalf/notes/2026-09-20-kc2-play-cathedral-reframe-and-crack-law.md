# The Cathedral — reframed to the Diablo register, and the CRACK LAW (damage as authored data)

> **STATUS:** CURRENT — supersedes § 2/§ 5/§ 6 F-S7 of `2026-09-20-kc2-play-arena-scene-plan.md` where they made the cathedral a Keepers-of-Hours building. Author gandalf (`SCENEWRIGHT` § 1–2; `SPEC-AUTHOR` § 3–4), 2026-09-20. **Matt verbatim:** *"the domed temple was meant to be the keeper's domain from Last Epoch, while the Cathedral is meant to be from Diablo 4/2."* And on Astra's floors: *"multiple, nearly symmetrical spiderweb cracks across every floor tile and every object … gives the idea that immense age caused the destruction as opposed to a very recent war … not consistent with reality and takes away from the smoothness and beauty of a cathedral."*
> The register card's FORBIDDEN list still binds every prompt: no source-game names. This note may name them; the brief describes the qualities.

---

## 1 · What the cathedral IS (the Diablo register, by its qualities)

The two references pull in one direction and it is not "gothic ruin." It is **a militant faith's stronghold** — the D2 Act-I cathedral/monastery and the D4 cathedral-of-the-Light both belong to a church that *fought*: heavy, fortified, built by a crusading order to hold a border against Hell, and lost to it. Its qualities, which the brief carries in place of names:

- **Mass before grace.** Romanesque weight with gothic verticals: thick piers you could hide a horse behind, round-arched crypt vaults, a nave that is half fortress. Cold **grey-white and black stone**, not the Keepers' blue-ivory-brass. Iron everywhere — bound doors, portcullis grilles over side chapels, chains, iron-strapped reliquaries, iron braziers.
- **The iconography of a faith of the sun and the chain**: a sun-disc behind the altar (the rose window is a sun, not an astrolabe), the order's sigil a chained sun; saints as armoured knights; candles by the thousand; wax running down stone; red-and-white banners; reliquary bones in glass.
- **The desecration is demonic, not merely ruinous.** This is the D2/D4 grammar: **flesh where stone was** — bodies hung from the vault on hooks, flayed banners of skin over the order's banners, blood pooled in the floor's low places, a crater where the altar's sun-disc fell, ritual marks cut into the flagstones, the congregation's bones in a heap the shape of a pyre, something *grown* in the crypt breaches (pale, wet, wrong). The beauty is the order's — the sun-disc, the candle-light on white stone, the iron and gold; the horror is the hell that came through it.
- **And it is RECENT.** This is the correction Matt's crack complaint really carries: the cathedral was whole *this week*. Its surfaces are **smooth, polished, beautiful** — worn by feet and knees and centuries of wax, not by age. The violence is **local, legible, and fresh**: you should be able to stand on the floor and *read the battle* — where the blast went off, where the fire started, which pier gave, which wall was breached from outside. Everything the battle did not touch is intact.

The Keepers' domed temple stays in the far layer as itself. The two buildings are two registers in one world — the astronomers on their hill and the crusaders on their crag — and the cliffside's reveal-by-walking now points at the crag.

## 2 · The battle that made this room (the story the floor tells)

Damage in this scene is **authored data, not painter's habit**: a short list of EVENTS, each with a position, a kind and a magnitude, from which the damage map is COMPUTED (§ 3) and given to the painter as a mask the way the floor plane is. For the chancel chunk (B1d, the proof image), four events:

| id | event | where (chunk px / m from the gate) | what it did |
|---|---|---|---|
| **E1** | **Blast** at the crossing, a demon-gate opening | south of the gate, on the nave axis; ≈ 6 m south | crater; radial cracks; ejecta thrown NORTH up the dais steps; scorch ring |
| **E2** | **Fire** started in the choir stalls | east side, between the piers | the stalls burned; soot fan up the east wall; wax and candle-trees melted; flagstones scorched but NOT cracked |
| **E3** | **Pier failure** — the apse's north-east pier gave | NE of the dais | the vault above it fell in a wedge; a talus cone of vault rubble at the angle of repose; the stones that fell cracked the flagstones they LANDED on — one fracture each, not webs |
| **E4** | **Breach from OUTSIDE** — the west wall broken inward by siege | west edge, mid-chunk | debris thrown INWARD; the sunset floods through the hole |

Everything else: **intact**. Polished flagstones with wax and blood on them; the sun-disc inlay unbroken except where E1's ejecta struck; the altar overturned by E1, not crumbled.

## 3 · THE CRACK LAW — where a real cathedral breaks, mathematically

**The complaint in one sentence:** *spiderweb cracks on every surface encode AGE; a battle encodes DIRECTION.* Real fracture in dressed stone follows the loads and the joints, and it is sparse. The rules below are the ones the damage map implements (each is a function of the event list; no painter judgement in where a crack goes):

1. **Cracks follow JOINTS before they cross tiles.** A flagstone floor fails along mortar lines first (weak plane). A crack crosses a tile only under a **point load** (something fell on it) or **bending over a void** (a crypt vault beneath). So: no tile carries a crack unless an event puts a load on it. *Painter instruction: every tile without a crack line in the mask is smooth.*
2. **Blast (E1): radial + concentric, decaying.** From epicentre `p`, radial cracks along `n` rays with angular jitter, length `L(θ) = L0 · (1 + 0.3·noise)`, crack density ∝ `1/r²`; a crater of radius `r_c` (broken/missing tiles); a spall ring `r_c < r < 2r_c` (tiles cracked in 1–2 pieces along joints); beyond `3r_c` nothing. **Ejecta** are thrown away from `p` with a cosine distribution about the blast's free direction (toward the open nave / up the steps) — debris density ∝ `cos(φ) · e^{-r/λ}`. Blast **scorch** is a ring, darkest at the crater lip, and it is black-grey, not brown.
3. **Fire (E2): burns UP and along fuel; it does not crack floors.** Scorch on the floor = a *fuel map* (where pews, stalls, timber, cloth were) blurred by wind; soot on walls = a **V-shaped plume above the fire's origin** (the V opens upward; the apex marks the seat of the fire — this is how real fire investigators find origin). Limestone near intense fire **spalls** (surface flakes, pinkish calcination) — texture, not cracks. Wax runs downhill. Cracks from fire only where thermal shock met a load (a hot pier base under weight) — a single vertical crack in the pier, not on the floor.
4. **Collapse (E3): a pier fails → the bays it carried fall.** The fall zone is the **wedge of vault the pier supported** (the bays adjacent to it); rubble lands in a **talus cone** at ~35° repose centred under the failed bay; vault ribs lie along their own span direction. Each fallen block that hits an intact tile leaves **one impact fracture** (a single line or a small radial star of ≤ 3 short rays, *under the block*, nowhere else). The pier itself shows the failure mode: crushed at the base, sheared, leaning.
5. **Breach (E4): a wall broken from outside throws debris INWARD**, biggest pieces nearest the wall, a fan of smaller stone into the nave; the hole's edges are jagged along the coursing (stone breaks along its beds). The floor inside the breach is scarred by the debris (impact fractures, rule 4), the floor *outside* is untouched.
6. **Settlement over the crypt: ONE long crack.** Where the crypt vault below has been broken (a breach), the floor above cracks along the **crown line of the vault** — one long line with short branches, following the joints — and sags. This is the only long crack the floor is allowed.
7. **Recency test:** cracks are **clean-edged, pale inside** (fresh stone), with dust and grit beside them; old cracks are dark, rounded, grown with moss — none of those here.

**The map.** A `damage_mask.png` for each chunk with classes: `crater` · `spall_ring` · `crack_line` (thin polylines) · `impact_fracture` (small marks) · `scorch` (fire) · `blast_scorch` · `soot_plume` (walls) · `debris` (density) · `settlement_crack`. Computed from the event list by a deterministic script (seeded), so a repaint gets the same battle. The painter is told: **cracks ONLY where `crack_line`/`impact_fracture`/`settlement_crack` are drawn; every other stone surface is smooth and whole.**

**The gate (so we can refuse a spiderweb, not just dislike it):** on the painted chunk, per floor tile, count dark thin-line pixels (Canny/thin-line filter, luminance below the tile's median − k·σ) and **line junctions**; a tile with junction count ≥ 3 that carries no `crack_line` mask pixels is a **spiderweb violation**; pass = violations ≤ 2 % of tiles. Astra's receipt does not judge this; the CHECK does.

## 4 · What changes in the scene plan (delta)

- § 2 identity → § 1 above (**F-S7 re-ruled by Matt's correction: NOT a Keepers cathedral**); the Keepers' astrolabe/hour-ring motifs move OUT of the cathedral and stay with the domed temple in the far layer.
- § 5 items re-keyed to the sun-and-chain order: the hierarch in the apse becomes **a knight-saint of the order hung on his own sun-disc** with the disc's gold face behind him and the fire behind that (F-S3 stands in shape); the rose window → the sun window; the hour-ring → the order's sun inlay; brass instruments → iron reliquaries and chains.
- **New standing gate for every painted chunk: the crack law CHECK (§ 3).**
- B1d (this proof) replaces B1a as the style pass of record; B1c (establishing image) follows Matt's word on B1d.

*Tracker-delta: game tracker SESSION-DELTA. — gandalf, 2026-09-20.*


---

## ⚑ CORRIGENDUM-FORWARD 1 (2026-09-20, drax's built instruments — `tools/crack_check.py`, `tools/mask_from_paint.py`, `02ea3bb4f`) — governs over § 3's gate and § 3's class list

**The law's SUBSTANCE is confirmed by measurement.** Same instrument, same 182 cells, same window: **B1a 49.45 % junction-dense · B1d 9.89 % (3.30 % violations)** — a **15×** improvement, robust 4–5.6× across four floor windows and across k ∈ [1.5, 2.5]. B1d's six residual cells are **painted rubble just outside the dilated `debris` mask, not spiderwebs**. Matt's eye and the instrument agree, and the law is what moved the number.

**⚑ The GATE as I wrote it was WRONG, and at k ≥ 2.5 it INVERTS.** *"luminance below the cell's median − k·σ"* is **self-normalising**: a cracked cell's own σ raises its bar while a smooth cell's σ collapses, so shading noise clears it. Measured: at k = 2.5 the written form scores **B1a 13.19 % vs B1d 17.03 %**, and at k = 3.0 **3.30 % vs 11.54 %** — *it grades the painting Matt complained about as CLEANER than the one that fixed it.* **A gate that can invert is not a gate.** Superseded, named in place; the replacement is drax's and both ship (`--threshold bth|written`) so the finding stays reproducible.

**The gate of record (every parameter declared, none inferred):**
- **Threshold** the *black-top-hat response* at `max(k·σ, absolute floor 10/255)`, `k = 2.0`, top-hat disk r = 0.03 m — same k, same σ, **5× separation**, no inversion.
- **Cell = 0.6 m fixed in PLATE METRES** (60.37 × 48.18 px), never "one flagstone": the painter chooses the module (**B1a 0.596 m, B1d 0.795 m — measured by floor autocorrelation**), so a flagstone-relative cell moves the denominator under us. 0.6 m is ≤ one flagstone in both, which is the binding constraint (a cell wider than a flagstone straddles mortar joints, and joints are junctions).
- **Junctions clustered 8-connected** (one X skeletonises to 2–4 adjacent ≥3-neighbour pixels; unclustered the counts roughly double and "≥ 3" means something else) · **spur prune 0.05 m** (stubs otherwise inflate ~2×) · **min line component 10 px** · **mask dilation 0.08 m**.
- **Reading B adopted:** a cell carrying ANY authored damage class (incl. `debris`/`talus`) is **not an intact flagstone** and the law does not govern it — painted rubble has stone outlines, not cracks. **Caveat carried, not hidden:** on one chunk the dilated mask covers 43.5 % of the window, leaving only **30 of 182 cells declared intact**, so reading B is statistically thin per chunk.
- **Pass line restated as a CELL COUNT graded over ≥ 3 chunks**, never "≤ 2 % on one": 182 cells ⇒ one cell = 0.55 pp, so "≤ 2 %" is unresolvable beyond ±1 cell. Of record: **≤ 3 violating cells per chunk AND ≤ 2 % pooled over the wave's chunks.**
- **Floor region:** the id mask has **no wall class and no void class** — KP-19 deleted them, so § 3's *"per floor tile, from the id mask"* **had no referent in first-party data.** Until guide v2 re-introduces a floor class, the gate runs over a **declared window in plate metres**, printed in the manifest and identical across paintings. ⚑ **Do not substitute the derived walkable mask for a floor mask** — it contains piers and arcades, and masonry coursing is junction-dense (B1d scores 8.21 % there). A boundary is not a floor.
- **`settlement_crack` (§ 3 rule 6) is named by the law and emitted by nothing** — `damage_map.py`'s class table never had it. Added to the generator this commit; a chunk with no crypt breach legitimately emits none, and the script now says so rather than leaving the gate pointing at a colour that does not exist.

## ⚑ CORRIGENDUM-FORWARD 2 (same source) — TWO DESIGN CATCHES, one of them mine

1. **⚑ THE PLAYER SPAWNS IN THE CRATER.** `damage_map.py` put **E1 at `[0.0, 0.0]` — the north gate**, which is the arena's `spawn` in the emitted `walkable.json`; the painting obeyed, and B1d's blast star and its lava are centred on the player's entry. **And my own § 2 event table says E1 is *"≈ 6 m south"* of the gate** — the note and the script disagreed, the script won because it was the thing that ran, and nobody read the note against it. *The same family this run has now corrected four times: a ruling that did not travel to the instrument.*
   **Conductor ruling (veto-open, goes to Matt with the S-set):** **the demon-gate blast is at the CROSSING — mid-nave, where the transepts meet — and the player enters from the SOUTH FAÇADE**, up the road from the crag, which is exactly where the cliffside's approach lands. The measured geometry's north gap becomes the **chancel's breach**, not the player's door. *Player consequence, and it is the better scene:* you come up the road, through the shattered façade, and walk north up the nave — the crater where hell came through is **between you and the altar**, and the hanging knight-saint is what you are walking toward.
2. **⚑ MASK-FROM-PAINT CANNOT DERIVE INTERIOR OBSTACLES, and must not pretend to.** The painter greened only the far background, so every near structure drawn inside the frame (piers, arcade, talus, breach debris) fell **inside** the derived walkable region — hence **93.12 % of frame, AREA 181.265 m², MAX CHORD 18.928 m as an UPPER BOUND.** The fix is the cliffside's own architecture, not a second key: **the painting gives the OUTER boundary (green = outside the world, per KP-19); INTERIOR obstacles come from the dressing pass as PROPS, each carrying its own footprint and sort line** (§ 4 B6, R-C3-62). That keeps art leading the edge while the things you collide with stay authored objects the runtime can reason about.
   Also of record: drax decides "a pool moved" **by overlap, never proximity** — his first cut used centroid distance and teleported the west pool 14 m onto a brazier. `pool_1` is `UNCONFIRMED_BY_PAINT, suggestion stands`; seven painted molten fields matched no suggested pool and are listed for the guide-v2 author. **Inventing a hazard position is content synthesis and is not the instrument's to do.**
