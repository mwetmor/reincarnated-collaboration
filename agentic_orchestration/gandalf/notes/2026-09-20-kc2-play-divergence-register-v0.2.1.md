# KC2-PLAY · THE DIVERGENCE REGISTER — **v0.2.1** (dated change table; composes with v0.2)

> **STATUS:** CURRENT — **v0.2.1, 2026-09-20. SUPERSEDES v0.2 FORWARD.**
> ⚑ **v0.2 (`a987334b`) is NOT edited** — it was already committed when KP-19 landed, so this is a **new file carrying a dated change table**, per the conductor's own instruction. **v0.2 remains the body of record for every row this table does not move**, including § E (the five attribution classes), § F.1–F.2 (the canonicalisation rule and its computed worked digest `bf648e51…`), and all four pins **P-a…P-d**, which are **unchanged and re-verified** this session.
> **Occasioned by:** charter ledger **KP-19** (Matt, **G1–G4 RULED**) and **KP-18(a)** (conductor, figure height).
> **Companion:** `2026-09-20-kc2-play-ta-prereg-v1.3.md` (`66d2fc89`). **No `DIV` row is graded by T-A, by construction.**
> ⚑ **Still zero recordings** — § F.3's window is open, so the hash move below un-pools nothing.
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1.

---

## § A · CHANGE TABLE — v0.2 → v0.2.1

| # | row | v0.2 | **v0.2.1** | authority |
|---|---|---|---|---|
| 1 | ⚑ **`DIV-16`** *(alias `DIV-arena-shape`)* | *(absent)* | ⚑ **NEW — PLAY's playable boundary is AUTHORED-TO-ART, derived from the painting; ORACLE keeps the circle** | **KP-19 · Matt G1** |
| 2 | ⚑ **`DIV-17`** *(alias `DIV-scale-fig`)* | *(absent)* | ⚑ **NEW — the cliffside's 130 px figure convention vs the arena's 1.9 m body** | **KP-18(a)** |
| 3 | **`DIV-14`** potion | PLAY *"bound to a key"* — **the key itself veto-open (F3 is Matt's)** | ⚑ **PLAY key = `1`, manual, auto-fire OFF. RULED by Matt; the key is no longer open.** ORACLE unchanged: auto-fire at **θ 0.22972972972972974** | **KP-19 · Matt G4** (*"Potion Key = 1"*) |
| 4 | **`DIV-13`** entry state | RULED **veto-open**, *"surfaced to Matt at G-IMG"* | ⚑ **RULED BY MATT. Opens at wave 151. No longer veto-open.** A played wave 150 remains a labelled pre-roll excluded from every statistic; `entry_state_source` stays in the header | **KP-19 · Matt G3** (*"agreed on G2 and G3"*) |
| 5 | **`DIV-09`** `u` | *"a registered runtime CHOICE, not a pin"*, conductor-ratified against the wave (KP-9) | ⚑ **RATIFIED BY MATT at `u = 0.285`.** Everything else stands unchanged — it is **still a CHOICE, not a measurement**: `u` remains **UNPINNABLE-FROM-COMMITTED-DATA**, the operative sub-window is still `[0.246, 0.324]`, and the claim class is still `PRESENTATION-CHOICE-NOT-MODEL-TRUTH`. ⚑ **Matt ratifying a choice does not convert it into a measurement**, and the handoff sentence must not start saying it does | **KP-19 · Matt G2** |
| 6 | **register hash** | moved at v0.1 (ND-08) | ⚑ **MOVES AGAIN** — two rows added, three statuses changed. Epoch unchanged (§ B.3) | — |
| 7 | **counts** | 15 DIV · 8 ND = 23 | ⚑ **17 DIV · 8 ND = 25** | — |

---

## § B · THE TWO NEW ROWS

### ⚑ `DIV-16` · ARENA BOUNDARY — **AUTHORED TO ART** *(alias `DIV-arena-shape`)*

| | |
|---|---|
| **ORACLE** | **unchanged and untouched** — `arena_fold` armed only in the `W1` arm: **CIRCLE, `R_wall = 43.758085029822276 m`**, response **STOP, never slide**, derived as `max\|emitter\| 35.758085 + PLACEMENT_EXTENTS_M 8.0`. In every other arm `arena_fold = None` and the plane is unbounded. **T-A grades this config and no other** (`TA-X-10`, `TA-X-11`). |
| **PLAY** | ⚑ **the playable boundary is DERIVED FROM THE PAINTING.** Matt verbatim: *"it looks right, but we will need to think through how we can make the edges to fit a cathedral. It doesn't need to be exact, so **I would prefer to fit it around the art rather than have the art fit the edges.**"* The video-measured ring becomes a **suggestion drawn in the annotation layer, never a frozen mask edge**; the painting places the nave's structures — walls, arcades, fallen timbers, dais, rubble — where they fit the scene, and **the runtime reads a mask derived from a painting Matt has passed** (mask-from-paint — **the reverse of the cliffside's guide→paint direction**). |
| ⚑ **What is STILL FROZEN** | the **projection law** · **`ppm_plate` = 100.6176** · **`u` = 0.285** — so **every range and radius is still true metres on the plane** · the **register** · the **pools as hazards** (positions suggested, final positions read from the paint). ⚑ *The boundary's SHAPE is authored; the metric it is measured in is not.* |
| **Authority** | **KP-19, Matt G1** — a **design ruling that inverts the guide method for the wall**, and only for the wall. |
| **How it is tested (T-A cannot grade it)** | **(i) the mask-from-paint instrument** — the mask is generated from the passed painting by a declared, re-runnable procedure, and the procedure's output is the artifact the runtime loads (never a hand-traced polygon); **(ii) R2D geometry probes** — containment resolves **in the runtime, in metres, against the mask polygon**, and `R2D-3`'s **zero `CollisionObject2D` / `CollisionShape2D` / `CollisionPolygon2D` / `Area2D`** assertion holds on the plate, on every token and on every VFX node; **(iii)** the mask's enclosed area and max chord are **emitted into the telemetry header**, so the confound below is a number in every recording rather than an argument after one. |
| **Expected direction on T-B** | ⚑ **NAMED CONFOUND, DIRECTION UNBOUNDED.** The arena's **area and shape** now differ from the referent's ring by however much the art required, and **nobody can bound that before the painting exists.** Everything that scales with arena size moves with it: time-to-contact, kiting room, how often the wall matters, how often a pool is crossed, and per-wave duration. It **compounds with `DIV-09`'s 1.32× operative window on `u`.** ⚑ **Every T-B row sensitive to arena size carries the mask's area and max chord beside it, or it is uninterpretable** — the same rule `DIV-07` used to carry for banner occupancy. |
| **Player-facing sentence (handoff)** | ⚑ *"The walls are wherever the cathedral put them. We measured a ring from your video and then let the painting win — fallen pillars, arcades and rubble make the edges, because an arena that fits its art reads better than an arena that fits a tracing. Distances are still true metres, but the room is not the same room as the one in your footage, and where a wave takes longer or shorter than you remember, this is the first thing to suspect."* |

⚑ **Why this is one of the most consequential rows in the register, said plainly:** `DIV-01` was a divergence with a *known* magnitude — 77.0 m across against the sim's 87.5 m, **12 % tighter**, a number we could print. `DIV-16` replaces the known magnitude with **a magnitude that does not exist until an artist and Matt agree on a picture.** That is the right call for the game — *the thing Matt asked for is a place, and a place has to look like somewhere* — and it is honestly the largest single unquantified term in `PLAY`. **Both halves belong on the record, and the T-B report must never quote an arena-sensitive figure without the mask's own geometry beside it.**

### ⚑ `DIV-17` · FIGURE SCALE — the cliffside's convention is not inherited *(alias `DIV-scale-fig`)*

| | |
|---|---|
| **ORACLE** | no figure, no canvas, no pixels — the sim has no drawn body at all. The only body-scale quantity it carries is the model's own metres. |
| ⚑ **The two conventions** | **The cliffside** drew the Keeper at **130 px** on a **100.6176 px/m** canvas ⇒ an implied **2.14 m** figure. **The arena** draws her body at **`h_fig` = 1.9 m ⇒ 115.2 px** on the plate at `ppm_plate`. **They disagree by 12.6 %**, and the arena's is the one that governs here. |
| **PLAY** | **`h_fig` = 1.9 m STANDS.** The painter's scale figure (IMAGE 2 of the arena guide) is the Keeper cell at **115.2 px on the plate**. ⚑ **The cliffside's 130 px is a CLIFFSIDE CONVENTION, registered here and never inherited.** |
| **Authority** | **KP-18(a)**, conductor. |
| ⚑ **Why 1.9 and not 2.14** | **because feel-fidelity lives in the RATIOS, not in a nominal height.** 1.9 m is what keeps the **EoR-ring-to-body ratio (2.62)** and the **monster-to-body ratios** identical to Grim Dawn's. A 2.14 m body would keep the ring's *metres* and change what the player *sees* the ring to be relative to himself — which is exactly the judgment T-C is for, decided by an inherited canvas habit instead of by the model. *(And `ppm` itself is derived at `h_fig` = 1.9: `ZOOM-GD` 75.668 px/m, `ZOOM-HOUSE` 160.394 — the pair corrected at Gate-1 BLOCK-A, re-affirmed at KP-0e.)* |
| **How it is tested** | the painter's scale figure is asserted at **115.2 px** in the guide; `ppm` is **derived, not typed** (`R2D-2`); `R2D-5`'s geometry-true probe asserts the EoR ring against its **3.0 m** pack value, so the **2.62 ratio is a consequence of two asserted numbers** rather than a third asserted number. |
| **Expected direction on T-B** | ⚑ **None on any runtime statistic** — nothing in the model reads a pixel. It enters **T-C** (Matt's eye) and, through what he can see, the **PILOT** class. A build that inherited 130 px would read **12.6 % smaller in the room** and would drift every *"does it read at the right scale"* verdict in one direction, invisibly. |
| **Player-facing sentence (handoff)** | *"Your character is drawn 1.9 m tall here, slightly smaller than in the cliffside scene. That is deliberate: it is the height that makes your spin ring and the monsters the same relative sizes they were in Grim Dawn, which is what you are actually comparing."* |

---

## § C · STATUS MOVES ON EXISTING ROWS

**`DIV-14` POTION — the key is `1`.** ORACLE: auto-fire at **θ 0.22972972972972974** (`PotionLimb.TRACE_CONSISTENT`, the cell of record). PLAY: **key `1`, manual, auto-fire OFF**; recorder emits `potion_use` with `trigger ∈ {"auto_theta","player_input"}` and ORACLE asserts `trigger == "auto_theta"` on 100 % of uses. Direction on T-B unchanged: it lands squarely on the HP trace (**B-11…B-18**), moving *time at full health* (42.84 %), *time below 50 %* (3.46 %) and *HP min* (5,360 / 20,005 = 26.79 %) together. **Handoff sentence unchanged and now complete:** *"The health potion is on key 1 and it is yours to press. The simulation drank automatically whenever it dropped below about 23 % health; you will not, and the health graph is where that shows."*

**`DIV-13` ENTRY STATE — ruled by Matt.** PLAY resumes the `cp150` fixture and **opens at wave 151**. A played wave 150 is a **labelled pre-roll excluded from every statistic**; `entry_state_source ∈ {"cp150_fixture","played_150"}` stays in the header and the grader still **refuses to pool the two**. ⚑ The reason is unchanged and worth keeping visible: otherwise the first graded wave's entry conditions are pilot-determined and the whole 151–160 comparison inherits **the cold-start confound sibling S6 exists to measure — which is out of scope.**

**`DIV-09` `u` — ratified by Matt at 0.285.** ⚑ **Ratification changes the row's AUTHORITY, not its CLAIM CLASS.** `u` is still **UNPINNABLE-FROM-COMMITTED-DATA** (every route reduces to `u = s/g`; two committed ground scales 2.3–2.4× apart; the spawn-points↔green-zones registration **tested and REJECTED**, invariant differing 29×); the operative sub-window is still **`[0.246, 0.324]`**; the claim class is still **`PRESENTATION-CHOICE-NOT-MODEL-TRUTH`**. **A choice Matt has ratified is a ratified choice, not a measurement**, and the handoff page must keep saying so.

---

## § D · HASH AND EPOCH

**The register hash MOVES** — `DIV-16` and `DIV-17` are added; `DIV-09`, `DIV-13`, `DIV-14` change status. The machine form, the eight-clause canonicalisation rule and the conformance digest **`bf648e51d14fc9313c4fce7774c5567628e1d3aca48d68c6a29d0d9225fe165e`** (497 canonical bytes) are **unchanged from v0.2 § F.1–F.2** and govern.

⚑ **Epoch unchanged: EPOCH 1, begun at v3.2 (`e0117429…`). EPOCH 0 produced zero recordings and no runtime has yet written a telemetry file** — so this hash move, like BLOCK-2's pin correction before it, **un-pools nothing.** That window closes the moment the first recording lands, and every move after it splits an epoch. **Recorded because "pre-declared and never needed" is a disposition and silence is not.**

**Pins re-verified this session, unchanged from v0.2:** `P-a` widths `1c971da9…` · `P-b` galadriel note `8186202c…` · `P-c` expected-values.json `a8b85331…` · `P-d` release-labels.json `15dace60…`.

**Emitter consequence:** the skeleton emitted **9** rows against v0.2's 23; it is now **9 against 25**. § F's *mismatch → `COVERAGE FAIL` at prereg `P-1`* is the right catch and **fires at T-0** unless the emitter is filled at W3.

---

## § E · OPEN QUESTIONS — one lean each

**OQ-1 · ⚑ Two id conventions have just entered the register, and that is the defect I fixed in the prereg one version ago.** The ledger cites **`DIV-arena-shape`** and **`DIV-scale-fig`**; this register's ids are **`DIV-nn`**. → **Lean: the numeric ids are canonical and the ledger's labels are recorded aliases** — because **the canonicalisation rule sorts rows ascending by `id`**, so a mixed scheme makes **row order, and therefore the hash, depend on which convention an emitter happened to pick.** That is WARN-3's class of defect one level up, and it is free to close now. *(Adopt the labels instead if you prefer — but then adopt them for all 25 rows, not two.)*

**OQ-2 · `DIV-16` removes the one number `DIV-01` could print.** → **Require the mask's enclosed area and max chord in every telemetry header, and make the T-B grader refuse to print an arena-sensitive row without them.** Same instrument as the quoting cap, same reason: a confound named in prose is discovered at the controls; a confound in the header is discovered by a script.

**OQ-3 · `DIV-01` and `DIV-16` now describe the same surface at two stages** — a video-measured ring, then a painted boundary derived from art. → **Keep both rows.** `DIV-01` is the lineage (*what we measured and why the arena is not the sim's circle*); `DIV-16` is the operative rule (*what the runtime actually loads*). Collapsing them loses the record of a method that was deliberately inverted on Matt's word.

**OQ-4 · The back-and-forth is now the method** (*"a bit of back and forth as we decide what cathedral structures fit best"*). → **Register each passed painting by sha in the ledger, and re-derive the mask only from a passed sha.** Otherwise the boundary the runtime loads and the painting Matt approved can drift apart silently — and by KP-19's own design there is no frozen edge to catch it.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v0.2, v0.1 and v0 not edited** — v0.2 was already committed when KP-19 landed, so this is a new dated change table, as instructed. **All four pins re-verified this session; none retyped.** **Law 3 held; GL-12 held; K-7 held** — ORACLE's circle `R_wall` is untouched by every ruling above. No production code, no dispatch, no push.*
