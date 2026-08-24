# VFX Archetype-Binding Spec — **T-A + T-K**

> **STATUS: DRAFT — awaiting DRIFT-CRITIC + Matt seal ratification.**
> **Run:** VFX ARCHETYPE-BINDING RUN · **Phase P4** (terminal deliverable) · charter
> `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md`
> **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Authored by:** gandalf (`SPEC-AUTHOR`), named sub-agent
> **Binding inputs:** charter § 1 / § 3 / § 4 / § 5 + ruling ledger **L-1 … L-34** ·
> `elrond/notes/2026-08-23-vfx-p1-archetype-vote.md` · `elrond/notes/2026-08-24-vfx-p2-dossier-curation.md` ·
> `elrond/notes/2026-08-24-vfx-p2-supplement-curation-delta.md` ·
> `galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` + `…-delta.md` (delta supersedes row-by-row) ·
> `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2** ·
> `drax/notes/2026-08-23-metal-vfx-smoke-probe.md` § 7 · `canonical/reap-die-rise-story/style-register.md`
> **Substrate of record:** `agentic_orchestration/research/curated/corpus.db` (read-only throughout)

---

## 0 · What this document is, what it is not, and three authoring decisions flagged for DRIFT-CRITIC

**This is a binding spec a specialist builds against.** It contains two tables:

- **T-A** — skill archetype → canonical VFX binding (**24 ACTIVE rows + `knockback` HELD**).
- **T-K** — kit-skill → (archetype, element parameter block, tier-2 flag).

**It is not** a build plan, an asset list, or an authorization to mint. Step 2 (drax mints; galadriel
minted-gate; DRIFT-CRITIC) is a separate KR-sequenced workstream that consumes this document
(charter § 1, L-5).

**No production code is specified here.** Where a change must land in the engine, the loadout, or a
Godot scene, this document names the *seam owner* and routes it — it does not write the change.

### 0.1 Three authoring decisions, stated up front rather than buried

**(a) T-K is specified as a derivation, not transcribed as 1,135 static rows.** The kit-skill →
archetype binding already exists, row-complete and reversible, in `vfx_archetype_member`
(1,158 rows, `vote_run = 'vfx-archetype-vote-2026-08-23'`). Transcribing it into markdown would
create a second copy that drifts from the first the moment a kit is re-mapped. § 4 therefore
specifies the **exact executable derivation** (the fold-aware query of record), proves it against
live counts, and shows verbatim sample rows so the row shape is inspectable. **If the conductor
judges that the charter's "T-K table" requires a materialized artifact, the materialization is a
one-statement view creation and belongs to elrond's seam — it is named as an owed action in § 6, not
performed here** (I am read-only on `corpus.db`).

**(b) The Tier-1 element parameter does NOT bind to the referent corpus's element field.** The
engine's own resolution chain (`skills[].element_primary` → `canon_corpus.original_element` →
`"physical"`) resolves into a **source-game** vocabulary of ~20 values (`physical`, `pierce`, `cold`,
`chaos`, `vitality`, `aether`, `n/a`, `mixed(fire/cold/lightning)`, …). That is *provenance of the
referent skill*, not our runtime element. Our runtime element is **seasonally generated** from
`data/seasonal_elements/pool.json` and keys on the **slot**. § 4.2 specifies the slot binding and
carries the referent element as annotation only, explicitly stamped "not the runtime parameter."

**(c) One new authoring axis is SPEC-ASSERTED here: the Tier-1 *surface class***
(`PAYLOAD-CARRIED` / `TRAIL-BOUNDED` / `FIELD-CARRIED`, § 3.0). It is a design decision, not a
substrate reading. It is corroborated by a substrate measurement (§ 4.2.3) at the extremes and
**contradicted in the middle** — `aura` and `self_buff` are magical-cause yet element-agnostic in the
referent corpus. The measurement is printed with the contradiction visible, and the axis carries a
Step-2 revisit trigger. It is labelled SPEC-ASSERTED in every row that uses it.

---

## 1 · Design law digest — the charter § 3 rulings, restated for a builder

These are **LAW for Step 2**. Reopening any of them is a HALT to Matt (charter § 5), not a design
conversation.

1. **Archetype-first factory.** One canonical VFX per archetype; variation is parameter layers
   (D3 rune-system / PoE gem+MTX precedent). **Never bespoke-per-kit-skill.** 1,135 kit-skills bind
   to 24 effects, not to 1,135 effects.
2. **"Best" is judged, not vibed.** Readability at our gameplay camera · parameterizability
   (recolour / rescale / motif-swap survivable) · style-register fit. Every selection in T-A carries
   galadriel's three axis scores and its receipts (P3 note + delta).
3. **Two-tier variation.** **Tier-1** element parameterization ships **WITH** the base binding — a
   fire whirlwind and a water whirlwind differ at base, or kits read as reskins. **Tier-2** bespoke
   signature flourish is deferred and deserving-based; **the deserving list is Matt's ratification,
   not this run's** (§ 5).
4. **Reference-anchoring boundary — stated once, permanently.**

   > Reference imagery anchors **skill semantics + readability** — *"same move, our style"* —
   > mediated by the locked style register. **Never pixel-style imitation.**

   Every URL in T-A is a **semantics + readability target**, not a look target. "Match the reference"
   means *a player who knows that game recognizes this move and reads what it does*; it does **not**
   mean the pixels resemble the source. The sim-side Law-3 referent-figure quarantine is a different
   layer and is untouched.
5. **Matt manual capture is a fallback lane only** — per-skill `matt_to_do/` rows, filed only after
   both automated lanes come back empty.
6. **Player consequence anchor — telegraph literacy.** Shared archetype VFX means the player learns
   the visual language **once**; the element tint reads damage type on sight. This is why the folds
   at L-29 are gains, not losses: one radial-burst grammar is easier to learn than two that look
   alike anyway.

### 1.1 The owner criterion of record (L-19) — the lens every row is scored through

> Matt, verbatim: *"the diablo franchise does a great job of making it feel more real as a plausible
> physical manifestation of exceptionally rapidly spinning weapons, clashing into flesh, bone and
> armor, whereas the Grim Dawn EOR Warlord's artistic rendering of the same move feels more like a
> generic magical aura that happens to be spinning along with the character."*

**Operative axis: action-CAUSED vs action-DECORATING.** Does the VFX read as *physically caused by
the move* (weapon speed, material impact against flesh/bone/armour) or as *decoration attached to the
move* (an aura that happens to spin)?

**Parameterization consequence, binding on Tier-1:** *element tinting must preserve causality class.*
A tinted weapon-trail stays physical. **Tinting cannot rescue an aura, and expanding a tint surface
can destroy a physical read.** This is the single most load-bearing sentence in this document for
Step-2 authoring, and § 3.0's Tier-1 surface class exists to operationalize it.

**Twice independently confirmed in pixels, in two different Grim Dawn skills, by two different
instruments** (L-25 Eye of Reckoning; L-28 War Cry): an effect that expands, leaves a ground mark,
and **never touches the bodies it passes through**. Matt named it from taste before either audit ran.
That is the failure mode Step 2 is built to avoid.

### 1.2 The locked style register — what "S" is scored against

`canonical/reap-die-rise-story/style-register.md`: **register A — bounded stylized-low-poly-3D
(Synty), rendered in Godot 4 through a fixed 2.5D ARPG camera.** Premium feel measured at
**~40 % lighting · ~30 % VFX · ~20 % material · ~10 % geometry**; the register-2 result was reached
on register-1 modular geometry with one hero-skill bloom and a dark-mood rig.

**Two consequences that bind T-A:**

- **Style-register fit is scored against OUR register, never against source-game polish.** A 2016
  Grim Dawn palette is not a defect; a 2D top-down grammar that does not transfer to a fixed 2.5D 3D
  camera **is** (hence the honest `S = 3` docks on both Hades / Hades II references).
- **VFX is 30 % of the premium budget and is a lever we have twice measured at ceiling.** A
  reference whose effect is carried by *light and particles* is a good fit by construction. A
  reference carried by high-fidelity mesh/texture detail is not, at our budget.
- **Our register is dark-mood.** Every "loses contrast on dim terrain" dock in T-A is therefore a
  **real risk**, not a footage artifact. Three rows carry it (`blink`, `single_target` runner-up,
  `cone`).

---

## 2 · Presentation constraints inherited from P0-b (drax) — binding on every T-A row

**Probe of record:** `agentic_orchestration/drax/notes/2026-08-23-metal-vfx-smoke-probe.md`
(KR-dispatched, drax-executed, tag `drax/v-godot-vfx-metal-probe-1`; closed at L-20).

### 2.1 Verdict inherited

**Metal does NOT constrain VFX work.** 13 probes / 8 GPU feature classes; 13/13 ffprobe gates; **zero
M-FEAT**. Throughput 535 renders/hr median (357–658). Metal cold-start +17 ms vs MoltenVK
+960–3,974 ms. Neither revisit limb armed ⇒ **R-1(a) carries empirical backing and the cross-host
question stays closed.**

### 2.2 The P0-b inheritance block — **pinned wording (L-31), reproduced verbatim; do not paraphrase**

> **cross-check: 14 sampled frames/clip measured (JSONs of record), 4 stills/arm retained, 76/clip
> uncompared, byte-identity structurally N/A; determinism: all-frame.**

Reading, so no downstream consumer weakens either arm:

- **Cross-check arm — weakened in coverage, strengthened in exactness where measured.** 14 frames per
  clip were compared (deliberate spread sampling per BR-2 lineage), with **0 lit px AND 0
  max-channel-delta on every sample** — exactly equal, not merely under the LIT ≥ 12 bar. 76
  frames/clip were never pixel-compared. The delta JSONs are durably recorded **although their input
  PNGs were pruned by FG-12** — the measurements are *documented, not reproducible*, and the coverage
  gap **cannot** be closed without a re-render. **Ruled at L-31: corrected wording suffices, NO
  re-render lap** — the finding is not load-bearing (zero M-FEAT is the verdict's primary evidence).
- **Driver-level byte-identity is structurally N/A** — two drivers never emit byte-identical PNGs;
  `"byte_identical": false` in every cross-check JSON is *correct behaviour*, not a failure.
- **Determinism arm — DO NOT WEAKEN. All-frame, complete coverage: 13/13 byte-identical SHA on the
  `use_fixed_seed` arm.** Drift isolates to the **GPUParticles3D emitter seed**; the
  runtime-instancing hypothesis is retired (drift occurred on scene-preloaded arms ⇒ never a
  necessary condition). Honest residual held: pinning ×4 → 3-of-4; pinning collapses the dominant
  term, it is not a complete fix.
- **Cross-run recommendation inherited:** future pixel gates on VFX-bearing clips **pin
  `use_fixed_seed`**, converting `sa_gate.py`'s standing refusal into a measurable arm. (Formal
  ratification + jack-ryan routing is a conductor act — § 6.4.)

### 2.3 The seven authoring constraints (drax § 7) — every one binds Step 2

| # | Constraint | Consequence in T-A |
|---:|---|---|
| **C-1** | **Both vendor packs ship shadow-casting geometry on VFX meshes.** `b_smoke` and `b_beam` each drop a hard black blob on the floor beside the effect. Binbun ships an explicit `shadow_caster.tres`. Class ASSET; reproduces on MoltenVK — not a Metal signal. | **Disable shadow casting on additive/emissive VFX meshes at mount time**, or the effect paints a black hole beside itself. Applies to **every** row. |
| **C-2** | **Beam-class assets are authored along −Z.** Mounted at identity in front of a camera looking down that axis, a beam is photographed end-on and reads as a blob. | **Orientation contract: aim-vector → yaw, explicit, never a default transform.** Binds `beam_channel`, `line`, `placed_lane`, `chain`. |
| **C-3** | **Additive stacking blows to white over a light floor.** Floor albedo 0.20 washed the frame; 0.085 reads correctly. Twice-attested (with the 2026-06-19 spell-VFX finding). | **Tier-1 recolour survivability must be judged against the actual stage albedo**, or "parameterizability" is assessed on a lie. Binds the Step-2 minted gate, not a single row. |
| **C-4** | **Effect lifetimes vary by more than 5×.** Measured: `p_turb` 16 frames (0.53 s burst) · `p_slam` 36 · `b_expl` 77 · `p_flame`/`p_spike`/`b_poison`/`s_fire` all 90 (continuous). | **T-A carries a lifecycle class column** (burst / decaying / sustained; composite permitted). *A telegraph that lasts 0.53 s and one that never stops are not interchangeable at the same archetype.* |
| **C-5** | **Peak screen coverage spans 0.03 % → 67 %.** `p_trail` at 535 px is effectively invisible at our camera; `b_expl` 46 %; `x_attr` 67 %. | **Readability is scored against a floor AND a ceiling.** One occludes the fight, the other cannot be seen. Drives `teleport`'s spec'd arrival-burst floor (§ 3.1.22) and `placed_lane`'s non-opacity constraint (§ 3.1.20). |
| **C-6** | **We own zero particle-collision and zero attractor content.** Both work perfectly on this stack. | **`vortex_pull` is AUTHOR-not-SELECT** — its reference is a *spec*, not a pack-selection (§ 3.1.19). Any archetype wanting debris-that-lands is in the same class. |
| **C-7** | **`beam_vfx` (Binbun assets-5) resolves only via `uid://`** — its internal resource paths point at the `.gdignore`d nested tree while all 9 other Binbun packs use the symlinked flat form. **A UID-cache rebuild would break the beam pack.** Class ASSET. | Fragile dependency under `beam_channel` / `line` / `placed_lane`. Logged, not fixed (Assets/ is read-only). **Step-2 pre-flight: verify the beam pack loads before scheduling those three rows.** |

### 2.4 Throughput limb — **NOT ruled here**

drax reported the raw number and correctly declined to invent a threshold; L-13(b)/L-20(ii) reserve
the limb-2 ruling for the conductor at P4, against the **actual** Step-2 cadence. **A SPEC-AUTHOR
sub-agent does not rule a conductor's pre-registered gate.** The datum and the arithmetic are banked
for that ruling in § 6.4; the spec-author's lean is stated there and is not binding.

### 2.5 Attestation — the 5.5 s onset residual (conductor's DRIFT-CRITIC checklist item)

> **ATTESTED: NO T-A row consumes probe-derived ONSET timing.**

What T-A *does* inherit from the P0-b probe is enumerated exhaustively so the checklist item can be
discharged by reading rather than re-auditing: **(i)** the seven § 7 authoring constraints (§ 2.3);
**(ii)** the coverage band 0.03 %–67 % as a readability floor/ceiling (drax § 7.5) — used at
`teleport` and `placed_lane`; **(iii)** the lifecycle-class *schema* and the >5× spread that motivates
it (drax § 7.4 on-frame windows: 16 / 36 / 77 / 90 frames) — **used to justify that a lifecycle column
must exist, never to set any archetype's timing**; **(iv)** the throughput datum, banked for CR-2 only.

**The only cadence NUMBERS in T-A are `whirlwind`'s spin-up 0.70 s / spin-down 0.80 s (§ 3.1.12), and
they come from galadriel's `framesets.json` v2 — measured at 60 fps from unmodified native Grim Dawn
pixels, not from a probe clip.** No other row specifies a duration.

---

## 3 · **T-A** — archetype → canonical VFX binding

**Shape: 24 ACTIVE rows + `knockback` HELD** (27 voted archetypes − `ring` folded − `defensive_dash`
folded − `knockback` held). Post-fold accounting verified live against `corpus.db`:
**1,135 skills · 511 kits · zero skills lost to the folds.**

### 3.0 Column semantics — read this before reading a row

| Field | Meaning · legend |
|---|---|
| **Canonical reference of record** | The single reference a builder opens FIRST. A semantics + readability target under § 1.4 — **never a look target.** |
| **Co-reference / variant / donor** | Additional references with a **named, distinct role**. `CO-REFERENCE` = independent second opinion of equal standing. `VARIANT` = the reference for a Tier-1 layer flag. `DONOR` = supplies one phase or property the canonical lacks (windup donor, cadence donor). `CORROBORATOR` = provenance support only, not openable as a master. |
| **t_start / t_end** | Seek point(s) into the reference. `TBD` = the dossier stated no time and one has not been derived. **`TBD-UNRESOLVABLE`** = a hunt has already established that no frame-exact source exists — **do not re-hunt** (L-34 / delta § 8.1). `reference_window` = a measured `(t_start, t_end)` pair; **a start without an end walks a builder into a different grammar later in the same clip.** |
| **Evidence tier** | `FRAMES-INSPECTED-BY-EXTRACTION` (master downloaded, frames cut and judged) > `FRAMES-INSPECTED` (a real gameplay still was examined) > `THUMBNAIL-ONLY` > `DOSSIER-TEXT-ONLY` > `TITLE-CARD` (a maxres still exists but contains **no gameplay** — it teaches nothing about the effect) · `OWNER-ATTESTATION` (the owner's eye signed work built from it; orthogonal to the pixel tiers, and **stronger than all of them for the question it answers**). |
| **link_status** | `LIVE` · `UNVERIFIED-BOT-BLOCKED` (HTTP 403 with a Cloudflare challenge — **the page is NOT dead; a human browser resolves it in ~30 s**) · `UNVERIFIED` (genuinely unknown). **Confirmed bot-blocked domains: `pathofexile.com`, `gamestar.de`, `bluetracker.gg`. A future automated link-check must not read 403 as absence.** |
| **Emitter geometry** | Anchor (world-ground / body-anchored / caster-centred / mover-bound / delegate-bound) · engine spatial primitive (annotation only, never merge authority) · **layer decomposition** — the independently swappable layers, which is what makes Tier-1 possible at all. |
| **L-19 causality class** | `physical-cause` / `magical-cause` / `hybrid` / `two-layered`. **A reference's causality class must MATCH the archetype's nature.** Scoring an `aura` down for being decorative applies the criterion where it does not live — decoration is what an aura *is*. |
| **Lifecycle class** | `burst` / `decaying` / `sustained`, per drax C-4. **Composite permitted** (e.g. `burst → decaying`) where layers genuinely differ; stated with its basis. Windup / active / impact coverage carried beside it. |
| **Tier-1 element-param axis** | **SPEC-ASSERTED surface class** (§ 0.1c): `PAYLOAD-CARRIED` (element is the payload's identity; the tint carries most of the variation) · `TRAIL-BOUNDED` (element rides a weapon trail / impact spark **only**; expanding the surface converts a physically-caused effect into a decorated one — the EoR failure) · `FIELD-CARRIED` (element tints a decal/field that must not obscure the caster). Stated with *what takes the tint* and *what must NOT*. |
| **Confound register** | Named **in the row**, never folded into a score. `confound_class` is two-valued and the distinction is load-bearing (L-34 amendment (a)): **`frame-external`** (facecam, HUD, damage numbers, watermark — occupies screen area, never touches the effect; **trivially discountable by cropping**) vs **`effect-internal`** (build add-ons and cosmetics entangled with the very effect being referenced; **not croppable — requires subtracting a layer from inside the thing you are measuring**). *Do not equate them.* |
| **Notes / residuals** | Spec-asserted axes, Step-2 revisit triggers, cross-seam dependencies, and gaps. Everything here is visible on purpose. |

### 3.1a Index — the 24 active rows

| # | Archetype | skills / kits | tier | Canonical (game · skill) | L-19 | Lifecycle | Tier-1 surface | Evidence tier |
|---:|---|---:|:-:|---|---|---|---|---|
| 1 | `ground_targeted_circle` | 115 / 102 | T1 | PoE · Astral Storm Call **+ D3 Meteor (co-ref)** | hybrid | burst → decaying | PAYLOAD | FRAMES-INSPECTED |
| 2 | `melee_strike` | 115 / 98 | T1 | Last Epoch · Rive | physical | burst | TRAIL | DOSSIER-TEXT (link verified live) |
| 3 | `self_buff` | 112 / 102 | T1 | PoE · Illusionist Aura Effect | magical *(correct)* | sustained | FIELD | THUMBNAIL-ONLY |
| 4 | `totem` | 97 / 80 | T1 | PoE · Ancestral Warchief | two-layered | sustained + burst sub-events | PAYLOAD *(attack only — body is a MODEL)* | THUMBNAIL-ONLY |
| 5 | `circle` *(⊕ `ring`)* | 93 / 88 | T1 | Grim Dawn · Ring of Steel | physical | burst | PAYLOAD | THUMBNAIL-ONLY |
| 6 | `single_target` | 90 / 77 | T1 | PoE · Project Essence Drain | magical | burst (travel + impact) | PAYLOAD | FRAMES-INSPECTED |
| 7 | `melee_arc` | 76 / 63 | T1 | D3 · Grim Scythe | physical | burst | TRAIL | FRAMES-INSPECTED |
| 8 | `aura` | 73 / 61 | T1 | D2R · Conviction | magical *(correct)* | sustained | FIELD | THUMBNAIL-ONLY |
| 9 | `multi_projectile` | 68 / 63 | T1 | Last Epoch · Multishot | physical | burst | TRAIL | THUMBNAIL-ONLY |
| 10 | `line` | 51 / 48 | T1 | D3 · Bone Spear | physical | travelling burst | PAYLOAD | THUMBNAIL-ONLY |
| 11 | `dash_attack` *(⊕ `defensive_dash`)* | 36 / 35 | T2 | D3 · Furious Charge | physical | burst | TRAIL | THUMBNAIL-ONLY |
| 12 | `whirlwind` | 33 / 33 | T2 | **D4 · Whirlwind — Matt incumbent** | physical *(the L-19 exemplar)* | sustained channel, ramps **measured** | TRAIL | **OWNER-ATTESTATION + DOSSIER-TEXT** |
| 13 | `ground_slam` | 27 / 25 | T2 | D4 · Hammer of the Ancients | physical | burst | TRAIL | THUMBNAIL-ONLY |
| 14 | `beam_channel` | 23 / 21 | T2 | PoE · Scorching Ray | hybrid | **sustained** | PAYLOAD | THUMBNAIL-ONLY |
| 15 | `blink` | 18 / 18 | T3 | Lost Ark · Distortion | magical | burst | PAYLOAD | THUMBNAIL-ONLY |
| 16 | `cone` | 18 / 18 | T3 | D3 · Seismic Slam | physical | burst | TRAIL | DOSSIER-TEXT-ONLY |
| 17 | `orbit` | 18 / 18 | T3 | Last Epoch · Shurikens + Blade Shield | physical | sustained | TRAIL | THUMBNAIL-ONLY |
| 18 | `chain` | 17 / 16 | T3 | PoE · Celestial Arc | magical | burst (hop rhythm) | PAYLOAD | DOSSIER-TEXT-ONLY |
| 19 | `vortex_pull` | 15 / 15 | T3 | Lost Ark · Vortex Gravity | hybrid | sustained field | PAYLOAD | THUMBNAIL-ONLY |
| 20 | `placed_lane` | 9 / 9 | T3 | Last Epoch · Frost Wall | physical | sustained (placed) | PAYLOAD | DOSSIER-TEXT (link verified live) |
| 21 | `ricochet_bounce` | 9 / 8 | T3 | Last Epoch · Shield Throw | physical | burst (multi-leg) | TRAIL | THUMBNAIL-ONLY |
| 22 | `teleport` | 8 / 8 | T3 | D2R · Teleport | magical | burst | PAYLOAD | THUMBNAIL-ONLY |
| 23 | `leap_strike` | 8 / 8 | T3 | PoE · Demonic Leap Slam | physical | burst | TRAIL | THUMBNAIL-ONLY |
| 24 | `fork` | 5 / 5 | T3 | D3 · Elemental Arrow (Frost Arrow) | physical | burst | PAYLOAD | THUMBNAIL-ONLY |
| — | **`knockback`** | 1 / 1 | T4 | **HELD — zero corpus (F-3)** | — | — | — | — |

**26 canonicals across 26 distinct URLs and 26 distinct skills, pre-fold; no double-anchoring.** The
invariant was self-audited by the judge at P3 § 5 and re-verified unbroken by the P3 delta.

### 3.1b The fold record (L-29) — the folds are **lossless**

| Folded | Into | Authority | What survives, and where |
|---|---|---|---|
| **`ring` (50 skills / 47 kits)** | **`circle`** | L-29(1). Identical on all three attested axes (`burst_around_self` / `zone` / `circle`); the zero-shared-context corpus converged as falsifier **F-a** pre-registered (`circle` r1 ≡ `ring` r1 by URL; `circle` r4 ≡ `ring` r4 by skill); the judge's swap-test confirmed strain and said so. | `ring` is recorded as an **alias** of `circle`. Its distinguishing read — the **open travelling annulus** — survives as the **`annulus` Tier-1 layer flag** with D2R Poison Nova as the layer's variant reference. Merged name is `circle` because that is the attested engine primitive. |
| **`defensive_dash` (4 skills / 4 kits)** | **`dash_attack`** | L-29(2). Its `motion = NULL` is an **unbanded artefact, not an attested pathless class** — all 5 curated candidates are dashes, and `windup = N` across all five is the signature of an unbanded class. It is a *layer*, not a geometry. | Survives as the **`defensive` Tier-1 flourish layer** (i-frame / deflect flash bound to the mover), reference Hades II Divine Dash. Zero kit overlap with `dash_attack` (verified), so 32 + 4 = 36 exactly. |

**Distinctness ruled explicitly rather than left implicit (L-29(3)–(8)):** `blink` ↔ `teleport`
DISTINCT (substrate's own motion axis: `straight_line` vs `blink_translate`; shared primaries are
boundary skills — evidence the boundary is real). `beam_channel` ↔ `line` DISTINCT (delivery class
**and** lifecycle class — sustained vs travelling burst cannot share one selection). `ground_slam` ↔
`melee_strike` DISTINCT **on a spec-asserted axis** — see § 3.1.13. `blink` ↔ `dash_attack` DISTINCT
on L-19 causality class (magical escape vs physical closing-to-hit) — one reference cannot anchor
both *by the run's own law*. `orbit` ↔ `whirlwind` DISTINCT (payload revolves vs character rotates —
different parent transform). `self_buff` NOT split; carries a sub-flag instead.

---

### 3.1 The rows

---

#### 3.1.1 · `ground_targeted_circle` — 115 skills / 102 kits · **T1 · the largest archetype in the vote**

- **Canonical:** Path of Exile · **Astral Storm Call Effect** · `https://www.youtube.com/watch?v=lhQiZae-djE` · **t_start TBD** · link LIVE
- **CO-REFERENCE of record (non-PoE, frames-inspected):** Diablo III · **Meteor rune set** · aggregator `https://www.purediablo.com/meteor-runestoned-videos` (LIVE, HTTP 200) — **resolved to five direct video IDs; the aggregator is the provenance record, the videos are the masters:** `wgjPrZWejm0` (Alabaster) · `O4_HTOkjOAc` (Indigo) · `PukGmsq8PBc` (Obsidian) · `Z4QL-S9jhHI` (Crimson) · `TTqAvf2n-E4` (Golden). All live, all `Diablo3Inc`, all 1280×720 real gameplay. **Carry the ARTIFACT's rune names (2012 pre-release colour runes), not the dossier's live-game names** — the dossier named base/Comet/Meteor Shower/Star Pact/Molten Impact; the page hosts the colour runes. INFO-class naming mismatch, not fabrication.
- **Runner-up:** PoE · Celestial Flameblast Effect · `FcsRlt_wjxY`
- **Frame-set pointer:** none first-party. Galadriel evidence stills: `galadriel/captures/2026-08-24-vfx-p3-delta/thumbs/{lhQiZae-djE,meteor-*}-maxres.jpg`
- **Emitter geometry:** world-ground anchored · primitive `circle` · **two independently swappable layers — (a) a crisp thin perimeter annulus with a TRANSLUCENT interior (cracked-ground decal, internal detail visible *through* it), (b) a vertical payload descending on the centre axis.** Caster legible at frame-edge, entirely outside the effect. Measured coverage ≈ 20 % — mid-band against C-5.
- **L-19:** `hybrid` — magical marker, physical strike.
- **Lifecycle:** **composite — `burst` (payload) → `decaying` (residue).** Basis: the Alabaster frame shows a *previous cast's residue coexisting with a fresh cast* — a lifecycle state no other reference in the corpus shows.
- **Coverage:** windup Y / active Y / impact Y (both canonical and co-reference).
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. **Tint both layers; motif-swap on the descending payload** (bolt → meteor → shard → column). **P = 5 is RECEIPTED on the co-reference, not argued:** five rune variants, five videos, one preserved grammar (circular footprint + vertical payload + persistent residue) across fire / ice / arcane / holy. Same class of evidence that earned `beam_channel` its 5.
- **Confound register:** ⚠ **canonical's L-19 physical half is UNWITNESSED — ASC's frame contains NO ENEMIES AT ALL** (an MTX showcase on empty ground); its "physical strike" is inferred from a cracked-ground decal, never from a body. **Meteor's physical half IS witnessed** (damage numbers on enemies inside the circle, bodies burning on residue, bodies knocked prone). On the run's own Matt-ruled criterion the non-PoE co-reference has the better receipt. · Meteor Indigo (`O4_HTOkjOAc`) **blooms out its own interior at large scale** — the failure mode to avoid when scaling this archetype up. · `class=frame-external` on Meteor (crowd, full HUD, damage numbers, minimap, watermark) — and **the circle still reads through all of it**, which is the harder test.
- **Notes / residuals:** **The deciding axis was perimeter definition under telegraph literacy** — for 115 skills the player must read *"a thing is going to land THERE"* before it lands, and ASC's ring is the crispest perimeter in either pool. GD Devastation was rejected because it "establishes the circular footprint temporally rather than through a hard perimeter" — the archetype's telegraph deleted — and its sustained-bombardment lifecycle collides with a burst archetype besides. · **Laboratory-vs-field asymmetry recorded, scores unmoved:** ASC's R = 5 was measured in a zero-enemy void; Meteor's R = 4 under a crowd and a full HUD. **If Step 2 wants a field-measured target rather than a showcase-measured one, open Meteor.** · **C-1 source concentration: 100 % → 50 % PoE. Discharged by co-reference, not by displacement.**

---

#### 3.1.2 · `melee_strike` — 115 skills / 98 kits · **T1 · tied-largest**

- **Canonical:** Last Epoch · **Rive** · `https://forum.lastepoch.com/uploads/default/original/2X/0/0b88fc443d13e2e232e51cbfe567994741b3f8e0.mp4` · t_start n/a (skill-isolated clip) · **link LIVE — spot-checked HTTP 200, 5.36 MB, first-party official-forum CDN video**
- **Runner-up:** PoE · Prismatic Double Strike Effect · `NZ1bj_ysJFA` — **the cleanest no-confound isolation in the pool; use it for frame study.**
- **Frame-set pointer:** none extracted. **The canonical is a downloadable MP4 — it is an extraction master waiting to be cut, and cutting it is the cheapest evidence upgrade available on any T1 row.**
- **Emitter geometry:** body-anchored (strikes an **enemy body**, not the ground plane) · primitive `point` · **three explicitly separated authoring layers — (a) character motion, (b) weapon trail, (c) hit response on the target.** No ground propagation.
- **L-19:** `physical-cause` on every axis. **This is the row where L-19 matters most** — 115 skills, and the archetype whose failure mode is precisely "an energy wave chasing the weapon."
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED`. **Tint the weapon trail and the hit-response spark. Do NOT expand the tint into a body-surrounding field** — 70 % of this archetype's referent members carry no element at all (§ 4.2.3), and a field-sized tint on a weapon strike is the EoR conversion in miniature.
- **Confound register:** none named on the canonical.
- **Notes / residuals:** **Rive escalates on the third stroke** — cadence coupling *and* a Tier-2 flourish hook that costs **no bespoke asset** (§ 5 Class-B pattern). · **`ground_slam` ↔ `melee_strike` distinctness is SPEC-ASSERTED, not substrate-attested** — see § 3.1.13 for the full statement and the Step-2 revisit trigger; it applies symmetrically to this row.

---

#### 3.1.3 · `self_buff` — 112 skills / 102 kits · **T1**

- **Canonical:** Path of Exile · **Illusionist Aura Effect** · `https://www.youtube.com/watch?v=KDer1UFJ9W8` · t_start TBD · link LIVE
- **SUB-FLAG (L-29(8)) — the row carries two sub-shapes under one archetype, NOT split:** `buff-decal` (Molten Shell, Illusionist Aura, Immortal Call — **the caster remains the caster**) and `transformation` (**the silhouette is replaced entirely**; substrate exemplars `Werewolf`, `Fade`). **Transformation reference: D3 · Archon · `https://www.gamestar.de/videos/diablo-3-skill-video-archon,65241.html` · link UNVERIFIED-BOT-BLOCKED (Cloudflare, 5.6 KB challenge page — not dead).**
- **Runner-up:** D3 Archon (as above, in its transformation role).
- **Emitter geometry:** caster-centred · primitive `none` · **two swappable layers — (a) a floor decal under the caster, (b) local body-adjacent emitters.** Both sit on our two cheapest register levers (lighting + particles).
- **L-19:** `magical-cause` — **and that is CORRECT for this archetype.** A buff has no physical cause; scoring it down for being decorative would apply the criterion where it does not live.
- **Lifecycle:** `sustained`.
- **Coverage:** ⚠ **WINDUP GAP — `windup = N` on 3 of 4 candidates.** Coherent, not under-research: this is one of P1's `motion_signature_attested = NULL` archetypes.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `FIELD-CARRIED`. **The governing property is: does not obscure the character.** 112 skills that will frequently be **active during other skills** — every other archetype's VFX must remain readable *through* this one. Tint the decal and the local emitters; **cap opacity and radius, and never let a Tier-1 recolour raise coverage.**
- **Confound register:** 3 of 4 candidates PoE — **no tie existed, so C-1 could not be applied.** Concentration recorded, not laundered.
- **Notes / residuals:** ⚠ **The one genuine SPLIT question found in the whole run, deliberately NOT executed here.** A transformation *replaces* the silhouette; a decal buff *must not touch it*. Those are opposite requirements on the same property and one canonical cannot serve both. **Whether `transformation` deserves a Tier-2 bespoke treatment is on Matt's deserving list (§ 5, Class-A item 2) — it is a commitment boundary, not a reasoning boundary.**

---

#### 3.1.4 · `totem` — 97 skills / 80 kits · **T1**

- **Canonical:** Path of Exile · **Ancestral Warchief** · `https://youtu.be/53exbcqunns` · t_start TBD · link LIVE
- **Runner-up:** Grim Dawn · Mortar Trap · `UGyIZgmVWA0`
- **Emitter geometry:** **delegate-bound** (the effect is anchored to an autonomous summoned body, not to the caster) · primitive `none` · **three-phase separation: summon / delegate-active / impact** — that separation *is* the authoring structure.
- **L-19:** **`two-layered`** — `magical-cause` (the manifestation) + `physical-cause` (the delegate's slam). Both must be authored; collapsing them loses the archetype.
- **Lifecycle:** `sustained` (delegate presence) **with `burst` sub-events** (each delegate attack). Composite by construction.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED` — **but on the delegate's ATTACK only.** ⚠ **PARAMETERIZATION CEILING, stated here rather than discovered in Step 2 (L-30): a summon-delegate needs a MODEL. Tier-1 can recolour what the totem throws; it cannot recolour what the totem IS.** `P = 4` is that ceiling, not a mark-down. **97 skills sit behind this limit**, and it is a *model-pipeline* dependency, not a VFX one.
- **Confound register:** 3 of 4 non-PoE alternatives were weaker on the anticipation axis — named, so the selection is not read as a source-preference.
- **Notes / residuals:** **Selected on the hardest property in the archetype: telegraph literacy for an autonomous delegate.** The player must read that the totem is *about to act*, and this is the only candidate with an explicit **anticipation beat on the delegate itself** (raised arm before the slam). No other candidate teaches it. · **The delegate-body question routes to § 5 (Class-A item 3) as a CONDITIONAL Tier-2 candidate** — conditional because a body is not a flourish, and the cost sits in a different pipeline.

---

#### 3.1.5 · `circle` *(⊕ `ring`)* — 93 skills / 88 kits · **T1** · alias: **`ring`**

- **Canonical:** Grim Dawn · **Ring of Steel** · `https://www.youtube.com/watch?v=nYh9Wij7NUA` · **t_start TBD** (a segment of a Nightblade active-skill showcase) · link LIVE · secondary: `grimdawn.fandom.com/wiki/Ring_of_Steel_(Skill)`
- **VARIANT reference — the `annulus` Tier-1 layer flag (folded `ring` members):** D2R · **Poison Nova** · `https://www.youtube.com/watch?v=2lJi7VTOANQ` — `burst_around_self` expressed as a **travelling annulus of discrete particles rather than a filled disc, with an OPEN CENTRE that preserves character visibility.**
- **WINDUP DONOR:** D3 · **Condemn** · `https://www.youtube.com/watch?v=9gyow_LYzzE` — a three-second charge; **the corpus's best windup donor for the radial-burst family** (relevant to the run-wide C-2 windup scarcity at 80.5 %).
- **Runner-up:** PoE · Celestial Warcry Effect · `pathofexile.com/forum/view-thread/2921459` · link UNVERIFIED-BOT-BLOCKED
- **Frame-set pointer:** ⚠ **NONE. There is no first-party GD frameset for this archetype**, and that is a provenance fact rather than a silent gap: the 8 frames captured under a `circle` hypothesis were resolved by icon template-match (L-28) to **War Cry (Soldier)**, not Judgment, and are **EXCLUDED from this pool**. They are retained at `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/circle_candidate_unresolved/` as a **finding, not a candidate** — see Notes.
- **Emitter geometry:** caster-centred, ground-plane · primitive `circle` · **layers — (a) a distributed set of solid blade meshes erupting on a literal circumference, (b) hit reactions on adjacent bodies.** Under the `annulus` flag, layer (a) becomes a travelling front with an open interior.
- **L-19:** **`physical-cause` — and this was decisive.** Ring of Steel is the **only action-CAUSED reference in either the `circle` or the `ring` pool**: real blades erupt, distributed on a circumference, with hit reactions on the bodies they reach. Under L-19 that outweighed its subdued 2016 palette — and the palette is scored against **our** register, where a ring of simple blade meshes lifted by light is register-1 geometry reaching register-2 exactly as the A-holds ruling measured.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. **Motif-swap the erupting element (blades → shards → flame tongues → bolts); tint the front and the contact response. The `annulus` flag switches interior fill OFF** — that is a Tier-1 layer toggle, not a second effect.
- **Confound register:** none named on the canonical beyond the missing timestamp.
- **Notes / residuals:** **Fold receipt (F-a fired as pre-registered at L-10).** The judge's own confession stands as the strongest evidence: *"I did land different canonicals — but I could have swapped them and every word of both rationales would still hold. That is strain, and I will not disguise it as discrimination."* The distinguishing property was read off **the English words**, not the substrate, which is identical on all three attested axes. · **§ 3.6 telegraph GAIN: one radial-burst grammar to learn, not two that look alike.** · **The excluded War Cry frames are a LOGGED FINDING with design weight:** a player-centred expanding annulus with a propagating front, a ground residue, and **no contact response on the bodies it overtakes** — *a second independent instance of the EoR L-19 failure mode, in a different skill, in the same game.* It is the clearest statement in the run of what NOT to build.

---

#### 3.1.6 · `single_target` — 90 skills / 77 kits · **T1**

- **Canonical:** Path of Exile · **Project Essence Drain Effect** · `https://www.youtube.com/watch?v=8LIQpG_OtFY` · t_start TBD · link LIVE · **FRAMES-INSPECTED** (maxres is an isolated in-flight gameplay frame)
- **RUNNER-UP — CHANGED at the P3 delta (L-34/2), superseding PoE Ice Spear:** Last Epoch · **Javelin (base skill)** · `https://forum.lastepoch.com/uploads/default/original/2X/1/185da7e8e62d88f1b64406ec8b34379003e29ec2.mp4` · **md5 `49fd1aa76498a5e908182ee5c6a4ef33` · h264 1280×500 @ 30 fps · 224 frames · 7.467 s** · **reference_window MEASURED: t ≈ 0.40 – 0.90 s** · **FRAMES-INSPECTED-BY-EXTRACTION** (224 frames cut and judged) · secondary: official skill-reveal thread `forum.lastepoch.com/t/…/43481`
- **Frame-set pointer:** `galadriel/captures/2026-08-24-vfx-p3-delta/frames/lejz-{0.53,0.60,0.67,0.73,4.60,5.10,5.60,6.20}.png` + master `evidence/le-javelin.mp4` (documented transform: `crop=700:420:380:60`, 2× lanczos; raw master preserved beside the crops).
- **Emitter geometry:** projectile · primitive `point` · **three visibly separated layers on the canonical — (a) payload body, (b) trail, (c) impact residue on the target.** Javelin's construction is **(a) a solid dark mesh body + (b) a brief luminous wake** — identity carried by geometry, `P = 5` earned on the same grounds `dash_attack` earned it.
- **L-19:** canonical `magical-cause`; **runner-up `physical-cause` with contact WITNESSED** (t ≈ 5.60 s: a white burst on an enemy body with the red streak leading into it). **Cite the runner-up for physical-element parameterizations.**
- **Lifecycle:** `burst` (travel + impact).
- **Coverage:** windup Y / active Y / impact Y on both.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. **Tint all three layers; motif-swap the payload body (orb → spear → shard → bolt).** The two references between them supply both causality classes on identical delivery geometry — **the cleanest Tier-1 evidence pair in T-A.**
- **Confound register:** **⚠ THE LOAD-BEARING BOUNDARY — why the primary holds.** Essence Drain's trail is **narrow enough that it does not read as a beam**; Javelin's flight streak spans **≈ 40 % of the crop width and reads as an elongated luminous LINE.** Under L-29(4) (`beam_channel` ↔ `line` DISTINCT on delivery *and* lifecycle class) protecting that boundary is load-bearing for the archetype's identity. **Essence Drain protects it; Javelin softens it.** · Javelin `R = 4` dock, `class=frame-external`: prismatic/rainbow streaks from an unrelated effect at frame-right in **every** frame of the first segment. · **Javelin honest limits:** the dark spear against dark-green/brown terrain at t = 0.53 / 0.73 is **genuinely low-contrast** and identity is carried almost entirely by the wake — **a real risk in our dark-mood register**; and the clip is **1280×500, horizontally letterboxed — vertical framing and vertical coverage CANNOT be assessed from it.** It is a geometry and phase-separation master, not a camera-framing reference. · Canonical carries the same laboratory-conditions caveat as § 3.1.1: one figure, no crowd, no HUD.
- **Notes / residuals:** ⚠ **`reference_window` has a `t_end` for a reason: later segments of the Javelin clip show denser multi-projectile multi-hit behaviour that MUST NOT be read as base `single_target` grammar.** A `t_start` without a `t_end` walks a builder straight into that trap. · **C-1: 100 % → 50 % PoE** (pool 4 → 8, all four additions non-PoE full-lifecycle video). Primary held on a pixel-measured axis, not on inertia — the judge named the incentive to move it and went looking for the displacing evidence.

---

#### 3.1.7 · `melee_arc` — 76 skills / 63 kits · **T1**

- **Canonical (provenance of record):** Diablo III · **Grim Scythe** · `https://news.blizzard.com/en-gb/article/20597129/necromancer-update-the-meleemancer` · media `gif` · link LIVE (HTTP 200)
- **EXTRACTION + TEMPORAL MASTER — accepted at the P3 delta (L-34/4), completing P3 § 6.7:** `https://www.youtube.com/watch?v=aWvMqUT9MQ8` (D3 Grim Scythe + Leech) · **no seek required — a short skill-specific demonstration, not a showcase** (dossier states this explicitly) · **FRAMES-INSPECTED**, 1280×720 real gameplay · windup Y / active Y / impact Y. **Same skill as the canonical — ZERO identity drift. Counted as ONE reference in two media, not two references.**
- **CADENCE / ANTICIPATION DONOR:** Hades II · Moonstone Axe combo (Aspect of Melinoë) · `https://www.youtube.com/watch?v=K8h8MksLWRU&t=93s` · **t_start 01:33** · `S = 3` — **Hades II is hand-drawn 2D top-down: the beat structure transfers, the surface does not. Use it for BEATS. Do not let it set a 3D style target.**
- **UPPER-BOUND SPECTACLE REFERENCE — accepted, CAPPED:** Lost Ark · Tempest Slash · `https://www.youtube.com/watch?v=lYrecr253lY&t=67s` · **t_start 01:07** · ⚠ **SHARED SOURCE** — see Notes.
- **Runner-up:** PoE · Celestial Lacerate Effect · `_odu2eo6jP0` (video-backed layered-crescent construction reference).
- **Frame-set pointer:** `galadriel/captures/2026-08-24-vfx-p3-delta/thumbs/aWvMqUT9MQ8-maxres.jpg`
- **Emitter geometry:** caster-origin, frontal, ground-plane · primitive `cone` · **layers — (a) a broad TRANSLUCENT pale crescent on the ground plane (radius ≈ 2× character height), (b) contact response on bodies inside it.** Measured coverage ≈ 12 % — comfortably mid-band. **Caster legible at the arc's origin and NOT occluded; terrain visible THROUGH the arc — the explicit correction of EoR failure #2.**
- **L-19:** `physical-cause` — **the purest read available: the arc IS the weapon's own path, not an energy wave chasing it.** Contact WITNESSED in frame (three damage numbers 172k/183k/65k, magenta hit markers, gore spray on two enemies standing inside the arc).
- **Lifecycle:** `burst` — short-lived, so it never occludes.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED`. **Blade-motif swap (scythe → axe → claw → greatsword) is exactly the Tier-1 axis, and it is the cheapest high-yield parameterization in T-A.** Tint the crescent and the contact spark; **do not thicken the crescent into a field** — 79 % of this archetype's referent members are element-agnostic (§ 4.2.3).
- **Confound register:** `class=frame-external` (full D3 HUD — orbs, hotbar, minimap, objectives panel — plus damage numbers, Greater-Rift context, rain particles). **All discountable at the `aura` standard, and here that standard genuinely applies** (unlike at `whirlwind` — § 3.1.12).
- **Notes / residuals:** ⚠ **Honest limit on the extraction master: the scythe blade itself is NOT in the frame** — the sweep has passed and only the trail remains. The L-19 "the arc IS the weapon's path" claim is therefore **confirmed-CONSISTENT** (crescent centred on the caster, frontally oriented, hit markers landing *on* the arc), **not proven.** One still cannot show a path; the full read needs the video's motion, which the companion now makes available. · **SHARED-SOURCE resolution of record (L-34): `lYrecr253lY` is `dash_attack`'s catalogue candidate #4 (Shoulder Charge, t = 251 s) AND this row's spectacle reference (Tempest Slash, t = 67 s). ADMITTED with distinct-segment reasoning — 184 s apart, different named skills, different archetype grammars — but PROMOTION TO PRIMARY IS PROHIBITED on either row without a fresh conductor ruling.** The L-29(6) prohibition's own predicate (differing causality classes) is **UNMET** here — both segments are physical-cause — and the judge said so rather than stretch the rule. **The video anchors NEITHER row.** Both rows carry their own `t_start` **and** a `shared_source` marker so a future dedupe pass cannot silently collapse one of them: *a shared source is not a duplicate row; it is two rows that open the same file at different minutes.*

---

#### 3.1.8 · `aura` — 73 skills / 61 kits · **T1**

- **Canonical:** Diablo II: Resurrected · **Conviction** · `https://www.youtube.com/watch?v=aDa8ZWS8ano` · t_start TBD · link LIVE
- **CLEAN-CAPTURE COMPANION (runner-up):** PoE · War Banner / Dread Banner · `https://www.youtube.com/watch?v=2USIImzhApw`
- **Emitter geometry:** caster-centred field · primitive `circle` · **layers — (a) a radius-defining ground ring/falloff, (b) sparse influence particles.** The selected property: it *"communicates influence without filling the radius with opaque effects"* — the coverage-ceiling solve an always-on field needs.
- **L-19:** `magical-cause` — **CORRECT for this archetype** (see § 3.0).
- **Lifecycle:** `sustained`.
- **Coverage:** ⚠ **WINDUP GAP — `windup = N` on all 5 candidates.** Coherent: `motion_signature_attested = NULL` archetype, not under-research.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `FIELD-CARRIED`. Tint the ring and the influence particles. **Radius and opacity are NOT Tier-1 knobs on this archetype** — they are the archetype's readability contract, and a recolour must not move them.
- **Confound register:** ⚠ **`class=frame-external` — a streamer VOD with a facecam bottom-left, a donation ticker, and a title card occupying frame area.** Chosen anyway: it is the substrate's literal top exemplar (`Conviction aura`) and the confound is **nameable and discountable by cropping** — the same standard that keeps Matt's incumbent valid. **Recorded in the row's provenance, NOT hidden in a score.** · **C-1 applied** — 3 of 5 candidates were PoE.
- **Notes / residuals:** **This row's confound class is the reference point for the whole document** — and it is precisely the class the `whirlwind` row does **not** share (§ 3.1.12, L-34 amendment (a)). Do not generalize "confound named ⇒ confound discountable" across the two.

---

#### 3.1.9 · `multi_projectile` — 68 skills / 63 kits · **T1**

- **Canonical:** Last Epoch · **Multishot** · `https://www.youtube.com/watch?v=30kcRWUOKMU` · **t_start 0:49** (second cited moment 2:35) · link LIVE
- **CLEAN-BASELINE COMPANION (runner-up):** PoE · Demonic Split Arrow Effect · `CPmANn4zDOE` — **paired the way L-19 blessed for `whirlwind`: selected pick + clean-baseline companion.**
- **Emitter geometry:** projectile fan from a caster origin · primitive `point` · **layers — (a) per-projectile body, (b) per-projectile trail, (c) per-impact response.** The reference makes the three parameter axes **visually explicit — projectile count, angular spacing, range** — which is § 3.3's requirement rendered as a picture.
- **L-19:** `physical-cause`.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` (projectile bodies + trails). **Count / spacing / range are ENGINE parameters, not Tier-1 element parameters — do not conflate them.** A fire multishot and a water multishot differ in tint and motif, not in fan geometry.
- **Confound register:** `R = 4` docked for build-effect clutter — **`class=frame-external`, nameable and discountable.** Discounting it is the same discipline that keeps the `whirlwind` incumbent valid; the companion supplies the clean capture.
- **Notes / residuals:** none outstanding.

---

#### 3.1.10 · `line` — 51 skills / 48 kits · **T1**

- **Canonical:** Diablo III · **Bone Spear** · `https://www.youtube.com/watch?v=peMAi0k5j-g` · **t_start 07:40** · link LIVE
- **Runner-up:** PoE · Twilight Explosive Arrow Effect · `pathofexile.com/forum/view-thread/3256281` · link UNVERIFIED-BOT-BLOCKED
- **Emitter geometry:** travelling linear payload · primitive `line` · **orientation contract applies (drax C-2): aim-vector → yaw, explicit.** Layers — (a) the travelling body, (b) a pierce-persistent trail, (c) per-target contact response.
- **L-19:** `physical-cause`.
- **Lifecycle:** **`travelling burst` — explicitly NOT `sustained`.** This is the axis on which L-29(4) separates this row from `beam_channel`; drax C-4 measured the class spread at > 5×, and **two different lifecycle classes cannot share one VFX selection.**
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. Tint body + trail + contact; motif-swap the body (bone spear → ice lance → lightning javelin).
- **Confound register:** none named. **Pale spear against dark floors is the highest-contrast read in the archetype — and our register is dark-mood**, so this is a positive, not a neutral.
- **Notes / residuals:** **The `pierce` behaviour is the discriminator that protects the `single_target` boundary** — a payload that continues through a target reads as a line; one that terminates reads as a projectile. **Selection deliberately avoided the Essence Drain collision** (Essence Drain is `line` candidate #4 *and* `single_target` #2; taking Bone Spear leaves it anchoring only `single_target`).

---

#### 3.1.11 · `dash_attack` *(⊕ `defensive_dash`)* — 36 skills / 35 kits · **T2** · alias: **`defensive_dash`**

- **Canonical:** Diablo III · **Furious Charge** · `https://www.youtube.com/watch?v=0HvsOpRLqXc` · t_start TBD · link LIVE
- **Runner-up:** PoE 2 · Shield Charge · `-jrsw_04QWQ` — **the *pose-carries-the-motion* reference; cite it for the ANIMATION seam, not the VFX seam.**
- **TIER-1 `defensive` FLOURISH-LAYER reference (the folded `defensive_dash` members):** Hades II · **Divine Dash** · `https://www.youtube.com/watch?v=t3N_IP5Em5A` · t_start TBD · **`S = 3` — Hades II is 2D top-down; the beat structure transfers, the surface does not.** The layer it isolates: **a gold-white deflection flash BOUND TO THE MOVER, with reflected-projectile impacts, *"without requiring a persistent path ribbon."*** That is a layer, not a geometry — which is the substance of the L-29(2) fold.
- **VARIANT reference (defensive conversion of the same motion):** D4 · Rushing Claw / Evasive Swipe · `https://www.youtube.com/watch?v=VjVUD8eLCFY` · **t_start 54:33** (inside a reveal stream).
- **Emitter geometry:** **mover-bound** (everything attaches to the travelling body) · primitive `none` · **layers — (a) silhouette + brief trail, (b) knockback/contact response DISTRIBUTED ALONG THE PATH, (c) [`defensive` flag] a deflection flash bound to the mover.**
- **L-19:** `physical-cause`. **Contact response is distributed along the path — enemies knocked aside as the body passes, not merely at the terminus. The closest thing in the corpus to Matt's "clashing into flesh, bone and armour" outside `whirlwind` itself.**
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y on the canonical; `windup = N` on all five folded `defensive_dash` candidates (the unbanded-class signature, per the fold reasoning).
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` — **and this row has the SMALLEST Tier-1 surface in T-A.** `P = 5` because identity is silhouette + knockback with a brief trail: **zero texture dependency**, the ideal case for a shared-rig low-poly register. **The corollary is a warning: there is very little here for an element tint to occupy, and the temptation to enlarge the trail into an aura is exactly the L-19 conversion.** 69 % of members are element-agnostic. **The `defensive` flag is a Tier-1 LAYER TOGGLE, not a separate effect.**
- **Confound register:** none named on the canonical.
- **Notes / residuals:** **L-29(6): DISTINCT from `blink` on causality class, not on the substrate axes** (both are `straight_line` / `motion` / none — a third identical-on-all-attested-axes pair). One reference cannot anchor both **by the run's own law**, and the player must read *"he is closing to hit me"* differently from *"he is escaping."* · `lYrecr253lY` @ 251 s is a catalogue candidate on this row; **promotion prohibited** (see § 3.1.7).

---

#### 3.1.12 · `whirlwind` — 33 skills / 33 kits · **T2** · ⚠ **the run's most owner-invested row and its thinnest pixel evidence**

- **PRIMARY (owner-validated incumbent, L-18/L-19, NOT displaced):** Diablo IV Season 14 · **Whirlwind Barbarian** · `https://www.youtube.com/watch?v=KaMPoPywM40` (Cliptis, community footage; oEmbed-verified) · t_start TBD · link LIVE · **evidence tier `OWNER-ATTESTATION + DOSSIER-TEXT`.**
  > **State it plainly rather than let "PRIMARY" imply a tier this row does not have:** the incumbent has never been phase-inspected. Its temporal-coverage flags are **UNRATED by deliberate refusal** — rating them from a title card would manufacture a flag. **Its value to the run is not phase coverage. It is that the owner's eye signed work built from it**, which no coverage flag can express.
- **PROVENANCE CORROBORATOR (demoted at L-30/L-32, NOT an extraction master):** D4 official · `https://www.youtube.com/watch?v=3BnHvNZ_4YM` — oEmbed title *"Diablo IV Quarterly Update Blog — Combat Improvements"*; the thumbnail is a **title card**; **no `maxresdefault` exists**. **`t_start = TBD-UNRESOLVABLE`** — job 29 established that no frame-exact source gives a time inside this video (GameSpot's mirror places the Combat Improvements segment at 05:22–06:55). `max_resolution = UNKNOWN`. **Do not re-hunt this; the hunt has been run and closed.**
- **LOAD-BEARING SILHOUETTE / CADENCE REFERENCES (L-34 amendment (b) — *not* "donors only"):**
  - D3, Blizzard March-2012 core-skill clip, **explicitly unmodified by runes** · `https://www.bluetracker.gg/diablo3/topic/us-en/4737240-in-development-class-skill-changes` · **link `UNVERIFIED-BOT-BLOCKED`** (Cloudflare `cf-mitigated: challenge`, 5,988 B "Just a moment" body) — **the page is NOT dead; a human opening it in a browser resolves the question in ~30 seconds.** Whether the embedded 2012 video still *plays* is genuinely unresolved. `windup = N`.
  - D3 **2008 pre-release build** · `https://www.youtube.com/watch?v=swOroVI1UaM&t=0s` · **predates the runestone system entirely, so cyclones and wings are not merely absent — they are structurally impossible.** **MEASURED, not assumed: no `maxresdefault` (HTTP 404 → the 120×90 / 1,097 B placeholder) — the identical low-resolution signature that demoted `3BnHvNZ_4YM`.** Usable for **silhouette, cadence and radius only** — not fine particles or material response. `windup = N`.
- **NEGATIVE STYLE ANCHOR *and* POSITIVE TIMING ANCHOR — read both halves:** Grim Dawn · **Eye of Reckoning** framesets · `galadriel/captures/2026-08-23-vfx-p2-gd-framesets/framesets.json` **v2**, frameset `ww-native-eor1` (12 frames, PNG 1920×1080, unmodified native pixels, `ffmpeg -ss <T> -frames:v 1`) + `ww-crop-eor1-set03` (5 frames).
  > ⚠ **A builder who reads "NEGATIVE STYLE ANCHOR" and closes the file loses the run's only measured whirlwind cadence data.** `ww-native-eor1.semantics`, verbatim: **`spin_up_s: 0.70` · `spin_down_s: 0.80`** (measured at 60 fps from native pixels) · **radius 150–160 px at 1080p ≈ 1.9× standing character height, constant** · anchoring *"rigidly player-centred; no lag, no elastic trail, no lean into movement vector"* · movement while channelling permitted and used constantly at full speed · **occlusion: renders over the caster's lower body and over enemies inside it — THE DEFECT TO CORRECT.**
  > **These are the only quantified whirlwind timing and geometry numbers in the entire corpus.** The negative *style* anchor is the positive *timing* anchor, and that is not a contradiction — it is L-18's two-skills/two-roles logic applied one level down.
- **Runner-up:** PoE · Celestial Cyclone Effect · `pathofexile.com/forum/view-thread/2609048` · link UNVERIFIED-BOT-BLOCKED
- **Emitter geometry:** caster-centred, rigidly player-anchored, **the CHARACTER rotates and the payload is the character's own weapons** · primitive `circle` · **layers — (a) weapon-trail highlights synchronized with the weapon animation, (b) localized hit effects on contact.** The reference property, itemized: *"blade highlights synchronized with the weapon animation… localized hit effects preserve the rotating silhouette without obscuring nearby enemies."*
- **L-19:** **`physical-cause` — this archetype IS the L-19 exemplar.** The criterion of record was articulated *about this move*.
- **Lifecycle:** **`sustained` channel with MEASURED ramps** (spin-up 0.70 s / spin-down 0.80 s). Beat model `channel` (framesets v2).
- **Coverage:** ⚠ **C-2 FIRES HARDEST HERE — `whirlwind` has ZERO windup reference anywhere in the corpus.** Both archival references `windup = N`; the incumbent UNRATED; `3BnHvNZ_4YM` claims `windup = Y` but is un-timestamped and un-openable — *a flag no builder can cash*; and the negative anchor's windup is, verbatim from framesets v2, *"PRESENT but it is a fade-in, not a windup — opacity ramps, no anticipation pose, no charge tell."* **For a channel-lifecycle archetype at our telegraph-literacy bar, on the run's most owner-invested row, this is a real gap and it is carried openly.** Partial compensation is the measured 0.70/0.80 ramp pair above.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED`. **Tint rides the WEAPON TRAIL and the contact spark. It must NOT expand into a caster-surrounding field.** 82 % of this archetype's referent members are element-agnostic — the highest in T-A after `leap_strike`. **A tinted weapon-trail stays physical; a tinted field IS Eye of Reckoning.** This row is where the L-19 parameterization consequence is least negotiable.
- **Confound register:** ⚠ **`class=effect-internal` — and the distinction from `aura` is load-bearing (L-34 amendment (a); do NOT restate the L-32 "same standard as `aura`'s VOD" equivalence, it is not exact).** The incumbent's confounds are (i) **Dust-Devil cyclone/tornado add-ons — S14 build modification, NOT base-skill VFX** and (ii) **cosmetic wings.** The tornadoes are *part of the very effect being referenced*; the wings attach to *the rotating character silhouette that IS the reference*. **Not croppable. Discounting them requires subtracting a layer from inside the thing you are measuring** — a strictly harder operation than cropping a facecam.
  > **The composition holds — but by a different mechanism than the one originally stated.** The incumbent's confounds are subtractable **only because two structurally confound-free references exist to subtract against** (2012 rune-free; 2008 pre-rune). That is why those two are LOAD-BEARING, not "donors only."
  > ⚠ **EXPLICIT STEP-2 DEPENDENCY, not a footnote: verify archival playback BEFORE minting.** If the bluetracker URL proves unplayable and the 2008 clip proves too degraded, **the Dust-Devil confound becomes UN-SUBTRACTABLE and this row's confidence drops materially below what "PRIMARY" implies** — not to zero (the owner's eye signed work built from it), but well below. Verifying is cheap; discovering it at mint time is not.
  > *Incidentally, the Dust-Devil layer is a live demonstration of our own two-tier architecture: a base archetype VFX with flourish layers stacked on top.*
- **Notes / residuals:** **CONFIRMED BY REFUTATION (L-34/3), which is stronger than confirmation by agreement.** Every whirlwind candidate in the corpus was probed for a frame-verified read: the incumbent is a **title card** (1280×720 promo art + facecam + "WHIRLWIND BARBARIAN" text); `3BnHvNZ_4YM` and `swOroVI1UaM` are **120×90 placeholders**; the bluetracker archive is a **locked door**; the job-29-rejected `XKBZXf9akXc` is a **title card**. **Not one whirlwind candidate yields a frame-verified read.** The composition is therefore not a compromise the run settled for — **it is the only shape the evidence supports.** · **Standard-asymmetry finding, recorded not actioned:** job 29 rejected `XKBZXf9akXc` (D4 beta Whirlwind) because its Dust-Devil status could not be verified — *the same confound the adopted primary carries and is forgiven for*. The rejection was correct for job 29's brief (clean-baseline verification) and is no longer coherent under the composition the run then adopted (best-available with named confounds). **Not proposed for adoption** — its thumbnail is a title card and it adds no pixel evidence. Recorded so a future reader does not trust the rejection log to mean what it meant on the day it was written. · **Incumbent-displacement rule (L-18(c)) satisfied: nothing was displaced, and the judge went looking for the evidence to displace it.**

---

#### 3.1.13 · `ground_slam` — 27 skills / 25 kits · **T2**

- **Canonical:** Diablo IV · **Hammer of the Ancients** · `https://www.youtube.com/watch?v=Q6V9qRmIbgU` · **t_start 1:09** (combat begins) · link LIVE
- **Runner-up:** PoE · Ground Slam updated base effect · `NI8590SoqPA` — **deliberately NOT elevated: it is `cone`'s shared primary, and elevating it would double-anchor two archetypes.**
- **Emitter geometry:** **world-ground anchored** — a radial/fan decal propagating from a floor point · primitive `point` · **layers — (a) weapon-meets-ground impact, (b) a compact circular ground burst well inside the coverage band, (c) contact response on bodies in range.**
- **L-19:** `physical-cause`, textbook: **a weapon meets the ground and the ground answers.** Same franchise grammar Matt praised.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` (weapon arc + ground-burst decal). 81 % of members are element-agnostic. **Tint the decal and the impact; do not convert the ground burst into a persistent field — that is `ground_targeted_circle`, a different archetype with a different telegraph.**
- **Confound register:** none named; the missing URL timestamp is resolved (1:09).
- **Notes / residuals:** ⚠ **SPEC-ASSERTED AXIS — the `ground_slam` ↔ `melee_strike` distinction (L-29(5)), ruled explicitly rather than left implicit.**
  > The two archetypes are **identical on all three attested substrate axes** (`point_strike` / `melee_arc` / `point`) — the same shape as the `circle`/`ring` pair that was folded. They are held DISTINCT on a property that is **visible in the footage and consequential for authoring, but NOT substrate-attested: the STRIKE SURFACE.** `ground_slam` strikes the **ground plane** and propagates a radial decal from a floor point; `melee_strike` strikes an **enemy body** and produces a body-anchored contact spark with no ground propagation. **Different emitters, different anchor transforms, different coverage profiles.** Merging them would collapse a floor-decal emitter and a body-anchored spark into one selection — the same class of error caught at L-11 in the `_RICH_TO_SPATIAL` merge hop.
  > **STEP-2 REVISIT TRIGGER (pre-registered here, not post-hoc):** if the minted `ground_slam` and minted `melee_strike` effects converge in authoring — same emitter, same anchor, same coverage envelope, distinguished only by a parameter — **then the axis did not hold and the pair folds at the next lap, with the receipt recorded.** This is the second-strongest merge candidate in the taxonomy after the one already folded.

---

#### 3.1.14 · `beam_channel` — 23 skills / 21 kits · **T2**

- **Canonical:** Path of Exile · **Scorching Ray** · `https://www.youtube.com/watch?v=A2ygiKOfLww` · t_start TBD · link LIVE (hq thumbnail; no maxres)
- **Runner-up:** Grim Dawn · Albrecht's Aether Ray · `aFvCDOf8HHk`
- **Emitter geometry:** caster-to-target sustained beam · primitive `line` · ⚠ **ORIENTATION CONTRACT MANDATORY (drax C-2): beam-class assets are authored along −Z. Mounted at identity in front of a camera looking down that axis, a beam is photographed END-ON and reads as a BLOB. T-A requires an explicit aim-vector → yaw contract on this row — never a default transform.** Layers — (a) beam body, (b) origin flare, (c) **persistent contact marker on the target** (burn + smoke that survives on the body).
- **L-19:** `hybrid` — magical body, **physical consequence.** The persistent contact marker is the discriminator over the alternatives: the beam *leaves a mark on the thing it touched.*
- **Lifecycle:** **`sustained`** — the defining property, and the axis on which L-29(4) separates this row from `line` (drax C-4 measured the class spread at > 5×).
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. **This is the ONE archetype with a MEASURED parameterizability receipt rather than an argued one: the identical beam geometry survives two radically different MTX treatments inside this same corpus** — `Stygian` black-flame and `Shaper` celestial-white. **Identity lives in geometry, not texture. `P = 5` is earned, not asserted.** Tint body + flare + contact marker; motif-swap the beam's internal texture freely.
- **Confound register:** none named. Third-highest element-commitment in the referent corpus (57 %).
- **Notes / residuals:** ⚠ **drax C-7 fragility applies:** the Binbun `beam_vfx` pack (assets-5) resolves **only via `uid://`** because its internal resource paths point at the `.gdignore`d nested tree. **A UID-cache rebuild would break the beam pack.** Step-2 pre-flight: verify the beam pack loads before scheduling this row, `line`, or `placed_lane`.

---

#### 3.1.15 · `blink` — 18 skills / 18 kits · **T3**

- **Canonical:** Lost Ark · **Distortion** · `https://www.youtube.com/watch?v=qEFT27d0IuA` · **t_start 05:18** · link LIVE
- **Runner-up:** PoE · Harbinger Flame Dash Effect · `-n8g6QtQixc`
- **Emitter geometry:** mover-bound with a **VISIBLE TRAVERSAL** · primitive `none` · layers — (a) a shadow/energy streak along the path, (b) **damage along the path**, (c) arrival resolution.
- **L-19:** `magical-cause`.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED` (streak + arrival).
- **Confound register:** ⚠ **`R = 4` docked — "dark palette can lose contrast on dim terrain." Our register IS dark-mood, so this is a REAL risk, not a footage artifact.** Tier-1 recolours on this row must be validated against the actual stage albedo (drax C-3).
- **Notes / residuals:** **F-e answered: DISTINCT from `teleport`, and the canonical was deliberately chosen from the NON-SHARED part of the corpus to prove it without strain.** The substrate's own motion axis differs (`straight_line` vs `blink_translate`) and the difference is legible in the candidates without any added criterion: `blink` carries a visible traversal *with damage along the path* — which is what `motion = straight_line` asserts — while `teleport` carries a spatial discontinuity. **The two shared primaries were Shadow Strike and Lightning Warp — precisely the skills that instantiate BOTH mechanics. Zero-context researchers reaching for the same boundary skills from two directions is evidence that the boundary cases are real, not that the classes are one.** · Also DISTINCT from `dash_attack` on causality class (§ 3.1.11).

---

#### 3.1.16 · `cone` — 18 skills / 18 kits · **T3**

- **Canonical:** Diablo III · **Seismic Slam** · `https://www.gamestar.de/videos/diablo-3-skill-video-seismic-slam,65244.html` · t_start TBD · **link UNVERIFIED-BOT-BLOCKED** (Cloudflare, same signature as `pathofexile.com`; **not verified absent**)
- **Runner-up:** PoE · Celestial Tectonic Slam Effect · `pathofexile.com/forum/view-thread/2879022` — **deliberately avoids `ground_slam`'s shared primary.**
- **Emitter geometry:** forward-biased fan from the caster, ground-plane · primitive `cone` · layers — (a) the propagating fan, (b) **enemy launch + knockback.**
- **L-19:** `physical-cause` — **the only cone candidate with enemy launch + knockback: contact response on bodies, the exact axis EoR failed.**
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` (the fan is the weapon's consequence, not an independent payload).
- **Confound register:** ⚠ **`R = 4` docked — "earthy VFX blends with terrain."** A real coverage-read risk at our camera; Tier-1 recolours must preserve figure/ground separation against the actual stage albedo. · Link is bot-blocked; **do not let an automated link-check read it as dead.**
- **Notes / residuals:** Literal substrate exemplar (`Seismic Slam` appears in the archetype's own exemplar list). **C-1 applied.**

---

#### 3.1.17 · `orbit` — 18 skills / 18 kits · **T3**

- **Canonical:** Last Epoch · **Shurikens with Blade Shield** · `https://www.youtube.com/watch?v=uUinnDksyzk&t=441s` · **t_start 441 s (7:21) — carried IN THE URL** · link LIVE
- **Runner-up:** PoE · Sawblade Blade Vortex · `n3PVnPYuKPI`
- **STACK-ACCUMULATION reference:** PoE · Blade Vortex · `rCro9h8reZw` — cite for how stack count reads as it builds.
- **Emitter geometry:** **the PAYLOAD revolves around a stationary-framed character** (parent transform on the orbit, not on the body) · primitive: **absent from the engine map — see residuals** · layers — (a) solid revolving payloads with legible spacing, (b) contact response, (c) **preserved negative space around the caster.**
- **L-19:** `physical-cause` (solid payloads with readable contact).
- **Lifecycle:** `sustained`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` — **motif-swap the orbiting payload (shuriken → blade → hammer → orb) and tint its trail. Payload COUNT and ORBIT RADIUS are engine parameters, not element parameters.**
- **Confound register:** none named — **C-1 was applied on a GENUINE tie** (this and the Sawblade candidate match on every axis: solid payload, legible spacing, readable contact, negative space preserved). Non-PoE takes it, and the tie is named rather than dressed up as discrimination.
- **Notes / residuals:** **The preserved negative space around the caster is the explicit correction of EoR failure #2** (caster swallowed by own effect) — do not lose it to a Tier-1 recolour that raises coverage. · ⚠ **CROSS-SEAM (L-12 finding F-1, routed to the engine seam via KR, POST-run): `orbit` is NOT a key of `kit_compiler._RICH_TO_SPATIAL`.** `.get(rich, "point")` silently gauges these 18 skills as **`point`** where the neighbouring `whirlwind` gauges as `circle`. Independently corroborated by this repo's `MIGRATION.md` V9 census (`geometry:orbit` = 6, residual blocked bucket). **The engine seam owns the fix; this spec does not write engine code.** VFX authoring is unaffected — the gap is in the run-time hit gauge, not in the identity vocabulary. · **L-29(7): DISTINCT from `whirlwind`** — payload revolves vs character rotates; different parent transform, different causality emphasis, canonicals share nothing.

---

#### 3.1.18 · `chain` — 17 skills / 16 kits · **T3**

- **Canonical:** Path of Exile · **Celestial Arc Effect** · `https://www.pathofexile.com/forum/view-thread/2922969` · t_start TBD · **link UNVERIFIED-BOT-BLOCKED** (Cloudflare, per L-15 — a bot-block, not absence)
- **Runner-up:** PoE · Automaton Arc Effect · `pathofexile.com/forum/view-thread/2170338`
- **Emitter geometry:** hop-to-hop discrete segments · primitive `line` · **orientation contract applies per segment (drax C-2)** · **layers — (a) the inter-target segment, (b) ENDPOINT FLASHES that preserve the hop rhythm.**
- **L-19:** `magical-cause`.
- **Lifecycle:** `burst` (hop rhythm).
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. ⚠ **Design warning specific to this row: `chain` is the MOST element-committed archetype in the referent corpus — 94 % of its members carry an explicit per-skill element, 12 of 17 lightning (§ 4.2.3). Tier-1 must ship the full live slot set for this archetype or it will read as "the lightning one," and a water or shadow chain will feel like a mistake rather than a variant.** This is the row where Tier-1 buys the most and where skipping it is most visible.
- **Confound register:** ⚠ **No non-PoE tie existed — the single non-PoE option (Torchlight: Infinite) is `full_lifecycle = 0` and explicitly noisy, so C-1 had nothing to break.** Concentration recorded, not laundered. · Link bot-blocked.
- **Notes / residuals:** **Hop-DISCRETENESS is the archetype's whole identity** (`motion = chain_hop`) and the property that separates it from `beam_channel`. The canonical is the only candidate whose notes record **endpoint flashes preserving the hop rhythm rather than reading as one continuous sweep.** If a minted chain reads as a sustained beam, the archetype has been lost.

---

#### 3.1.19 · `vortex_pull` — 15 skills / 15 kits · **T3** · ⚠ **AUTHOR-not-SELECT + cross-seam dependency**

- **Canonical (a SPEC, not a pack-selection — see below):** Lost Ark · **Vortex Gravity** · `https://www.youtube.com/watch?v=v7mliS8dC40` · **t_start 10:48** · link LIVE
- **Runner-up:** PoE · Void Sphere · `pathofexile.com/forum/view-thread/2933919` (the purest sustained-pull motion spec) · link UNVERIFIED-BOT-BLOCKED
- **Emitter geometry:** ground-anchored attractor field · primitive `circle` · layers — (a) a **physical initiation** (a hammer strike triggers the gravitational eruption), (b) the sustained inward field, (c) debris/particle response.
- **L-19:** **`hybrid` — physical initiation → magical field.** An inward pull is inherently magical; this candidate gives it a *physical cause*, which is the L-19 pattern applied to an archetype that would otherwise have no way to earn it.
- **Lifecycle:** `sustained` field.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED` (field + debris). **Provisional — the effect does not exist yet; see the two flags.**
- **Confound register:** none named beyond the resolved timestamp.
- **Notes / residuals — TWO FLAGS, one of them cross-seam:**
  1. ⚠ **AUTHOR-not-SELECT (drax C-6).** **We own ZERO attractor content and ZERO particle-collision content.** Both work perfectly on this stack and identically on MoltenVK — the gap is content, not capability. **This row's canonical is therefore a SPECIFICATION for an effect that must be authored, not a target to select a pack asset against.** Any archetype wanting debris-that-lands falls in the same class.
  2. ⚠ **CROSS-SEAM — the archetype's readability is carried by a NON-VFX SYSTEM.** In **every** candidate the inward vector is legible because **enemies visibly move**: *"enemy displacement," "large enemy displacement," "enemy movement supplies an especially readable inward vector."* **No VFX we mint can supply that.** Consequence, stated so it is not discovered at the gate: **`vortex_pull` CANNOT be validated at Step 2's minted gate on VFX alone** — it needs engine-side enemy displacement to read at all. **Routed to the engine seam via KR at run close** (same routing pattern as L-12's F-1). Until that lands, a minted `vortex_pull` scored on VFX alone will under-score for a reason that is not the VFX's fault.

---

#### 3.1.20 · `placed_lane` — 9 skills / 9 kits · **T3**

- **Canonical:** Last Epoch · **Frost Wall** · `https://forum.lastepoch.com/t/introducing-the-runemaster-coming-in-runes-of-power/60436` · t_start TBD · **link LIVE (spot-checked HTTP 200)**
- **Runner-up:** PoE · Stygian Flame Wall Effect · `pathofexile.com/forum/view-thread/2975769` · link UNVERIFIED-BOT-BLOCKED
- **Emitter geometry:** world-placed lane with vertical extent · primitive `line` · ⚠ **orientation contract applies (drax C-2)** · **layers — (a) a bright base along the lane, (b) darker upper wisps, (c) BRIGHT END PILLARS.**
- **L-19:** `physical-cause`.
- **Lifecycle:** `sustained` (placed, persistent).
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `FIELD-CARRIED` at the lane body, `PAYLOAD-CARRIED` at the end pillars. Tint both; **do not raise opacity** (see the constraint below).
- **Confound register:** none named.
- **Notes / residuals:** **Endpoint legibility is *the* hard readability problem for a lane at a fixed isometric camera — where does the wall stop? — and this is the only candidate that solves it explicitly** ("bright end pillars"). · ⚠ **T-A AUTHORING CONSTRAINT, contributed by the judge and binding regardless of which reference a builder opens: at our locked camera, ANY lane with vertical extent must be authored NON-OPAQUE.** The runner-up's pattern is the target — *bright base, darker upper wisps, not a completely opaque screen* — and **drax C-5's 67 % occlusion ceiling is the reason.** An opaque lane at this camera deletes the fight behind it. · drax C-7 beam-pack fragility applies (§ 3.1.14).

---

#### 3.1.21 · `ricochet_bounce` — 9 skills / 8 kits · **T3**

- **Canonical:** Last Epoch · **Shield Throw** · `https://www.youtube.com/watch?v=FuYT1KrQorI` · **t_start TBD — dossier locates the reference segment as the isolated three-ricochet demonstration in the FINAL ~5 SECONDS of the clip (end-relative, not absolute)** · link LIVE · secondaries: forum guide `forum.lastepoch.com/t/…/46581`, mechanics page `lastepoch.tunklab.com/ability?a=ShieldThrow`
- **Runner-up:** Grim Dawn · Aegis of Menhir + Avenging Shield · `LTKKgKUMVdk` — **both finalists are non-PoE, so C-1 is satisfied either way.**
- **Emitter geometry:** multi-segment travelling path with a **RETURN LEG** · primitive `line` · layers — (a) the payload body, (b) per-leg trail, (c) per-bounce contact response.
- **L-19:** `physical-cause`.
- **Lifecycle:** `burst` (multi-leg).
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED` — motif-swap the thrown body, tint the leg trails. **Leg COUNT and bounce range are engine parameters.**
- **Confound register:** ⚠ **`R = 4` docked — Manifest Armour procs can mask contacts** in the general footage. `class=frame-external`, nameable and discountable; **the final training-dummy segment is the reference precisely because it deliberately exposes the individual path legs** with the procs out of the way.
- **Notes / residuals:** **The complete return leg is the selection reason** — a ricochet that does not come back is a `multi_projectile` with extra steps. The training-dummy segment is the best authoring reference in the corpus for a multi-segment path.

---

#### 3.1.22 · `teleport` — 8 skills / 8 kits · **T3** · ⚠ **carries the most actionable score in T-A**

- **Canonical:** Diablo II: Resurrected · **Teleport** · `https://www.youtube.com/watch?v=YaUOt4_zxjs` · t_start TBD · link LIVE
- **Runner-up:** PoE · Stygian Flame Dash Effect · `PykOVssTmTo`
- **Emitter geometry:** **no traversal** · primitive `none` · **layers — (a) a cast gesture at origin, (b) SPATIAL DISCONTINUITY (nothing travels), (c) an arrival flash at destination.** This is the exact match to `motion = blink_translate`, and the literal substrate exemplar (`Teleport`, `Teleport (Enigma runeword)`).
- **L-19:** `magical-cause`.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED` (departure + arrival flashes).
- **Confound register:** ⚠ **`R = 3` — the honest score, and the most actionable number in the whole selection.** *"Restrained arrival flash."*
- **Notes / residuals:** ⚠ **COVERAGE-FLOOR RISK + a SPEC'D FLOOR (L-30 obligation discharged here).** A restrained arrival flash sits near **drax C-5's measured 0.03 % floor** (`p_trail` at 535 px is effectively invisible at our gameplay camera). **A move the player cannot see is not a telegraph.**
  > **SPEC'D MINIMUM (SPEC-ASSERTED, with its derivation and a revisit trigger — not a magic number): the arrival burst must reach a peak screen coverage of ≥ 1 % at the locked 2.5D camera**, measured by galadriel's existing coverage instrument at the Step-2 minted gate. **Derivation:** ~30× the measured-invisible datum (0.03 %) and ~2 orders below the measured occlusion ceiling (67 %), placing it low in the band without touching the floor. **Revisit trigger:** the FIRST minted `teleport` is scored against this floor *and against the eye*; if 1 % reads as invisible or as excessive at our camera, the number is corrected on that evidence and the correction is recorded. **The floor is asserted so a builder has something to hit, not because it has been measured.**
- **F-e:** DISTINCT from `blink` on the substrate's own motion axis (§ 3.1.15); canonical deliberately chosen from outside the shared set.

---

#### 3.1.23 · `leap_strike` — 8 skills / 8 kits · **T3** · **the corpus's best windup donor**

- **Canonical:** Path of Exile · **Demonic Leap Slam Effect** · `https://www.youtube.com/watch?v=TVLZ1wX443g` · t_start TBD · link LIVE (hq)
- **Runner-up:** Last Epoch · Fury Leap · `SkYPspTspaM` · ~t 4:15 — **explicitly "busier," so this was NOT a C-1 tie; the PoE pick wins on restraint.**
- **CAMERA-CLEAN SECONDARY:** Grim Dawn leap-rune gifs · `forums.crateentertainment.com/t/what-are-you-doing-visual-examples-of-…` (media `gif`).
- **Emitter geometry:** ballistic arc, caster-bound in flight, ground-anchored at impact · primitive `point` · layers — (a) **an anticipation crouch**, (b) the trajectory, (c) a compact impact radius.
- **L-19:** `physical-cause` — mass falls, the ground answers, and the caster stays legible.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y — ⚠ **and this row is a C-2 ASSET: the crouch is a genuine ANTICIPATION POSE, one of the best windups in the entire corpus.** With `circle`'s D3 Condemn charge, it is one of only two strong windup donors the run found against an 80.5 % windup-coverage corpus. **Cite it wherever a windup is missing and the beat structure transfers.**
- **Tier-1 element-param axis (SPEC-ASSERTED):** `TRAIL-BOUNDED`. ⚠ **100 % of this archetype's referent members are element-agnostic — the purest TRAIL-BOUNDED row in T-A (§ 4.2.3).** The element tint has almost nowhere to live except the impact. **Accept the small surface; do not manufacture one.**
- **Confound register:** none named.
- **Notes / residuals:** *"Restrained palette keeps the character trajectory and compact impact radius separable"* — the property to preserve under any Tier-1 recolour.

---

#### 3.1.24 · `fork` — 5 skills / 5 kits · **T3**

- **Canonical:** Diablo III · **Elemental Arrow / Frost Arrow** · `https://www.youtube.com/watch?v=K-eVr9I7xrs` · t_start TBD · link LIVE
- **Runner-up:** PoE · Celestial Tornado Shot Effect · `_XtINEHQqd0` — **carries the cleanest split-NODE read; cite it for the branch-point authoring specifically.**
- **Emitter geometry:** forward-biased split · primitive `line` · layers — (a) the parent payload, (b) **the branch point**, (c) the child payloads.
- **L-19:** `physical-cause` — *a solid arrow shattering into arrows is a plausible physical manifestation.* Forward bias is correct for `prim = line`.
- **Lifecycle:** `burst`.
- **Coverage:** windup Y / active Y / impact Y.
- **Tier-1 element-param axis (SPEC-ASSERTED):** `PAYLOAD-CARRIED`. Second-most element-committed archetype in the referent corpus (80 %) — Tier-1 buys a lot here.
- **Confound register:** ⚠ **`R = 4` docked — rapid fire obscures the branch points. ISOLATED CASTS ARE THE REFERENCE FRAMES**, not the sustained-fire segments.
- **Notes / residuals:** **The branch point is the archetype's identity.** If a minted fork's split is not legible, it is a `multi_projectile`.

---

### 3.2 · **`knockback` — HELD.** No selection made. 1 skill / 1 kit · T4

- **Status:** **HELD** per L-14 (excluded from P2 — the only archetype never given a dossier job) and re-affirmed at the P3 gate. **Zero corpus. No canonical, no runner-up, no scores.** Nothing is being hidden here; there is nothing to hide.
- **Sole member:** `Ancient Spear (Rage Flip rune)`.
- **F-3 vocabulary-leak evidence, strengthened at P3 § 6.6 and again by the post-fold shape:**
  `knockback` is the **only archetype in the vote with `motion_signature = NULL` AND delivery unbanded AND `engine_spatial_primitive` absent AND a single member.** Every other archetype has at least one attested axis or an engine primitive. **It is an EFFECT noun sitting in a GEOMETRY slot** — the signature of a vocabulary leak rather than a real class. It is also one of only two archetypes outside the engine's own `_RICH_TO_SPATIAL` keyspace (the other being `orbit`, which is a genuine class the engine's map is missing — the opposite finding).
- **Why it was kept rather than deleted:** Discipline #41 — **a cluster of one is a finding, not an error.** It is flagged in `vfx_archetype.vocab_flag`, tiered T4, and held.
- **PROPOSED disposition (conductor / Matt — not ruled by this spec):** **re-band the single member at the next kit-mapping lap.** If it re-bands to an attested geometry, the class dissolves and the skill joins its true archetype (`dash_attack` and `ground_slam` are the plausible destinations, on the referent skill's own shape — but naming the destination now would be exactly the hand-imposition the charter forbids). **If it survives re-banding, it earns a P2 dossier job and a T-A row at the next lap.** Either way the residue is examined as a group with the pre-fold `defensive_dash` members and the F-4 / F-2 unbanded groups (§ 6.3) — *the same shape appeared twice, which is worth one deliberate look rather than two ad-hoc guesses.*

---

## 4 · **T-K** — kit-skill → (archetype, element parameter block, tier-2 flag)

### 4.1 The binding rule, and why it is specified as a derivation

**Grain: one row per kit-skill** — `kit_mapping.mapping_json.skills[]` entry, keyed
`(kit_id, skill_ordinal)`. **The binding already exists row-complete in `vfx_archetype_member`**
(elrond, P1, `vote_run = 'vfx-archetype-vote-2026-08-23'`; 1,158 rows = 1,138 skill rows + 20
kit-level exception sentinels), and every row preserves `geometry_value_raw` /
`motion_signature_raw` / `delivery_class_raw` so the curation is a **projection, never a rewrite.**

Transcribing 1,135 rows into this document would create a second copy that drifts from the first the
moment a kit is re-mapped, and would silently outrank the reversible original. **T-K is therefore
specified as the exact fold-aware derivation below** (§ 0.1a states this as an authoring decision for
the conductor's DRIFT-CRITIC).

**The axis of record** is `kit_mapping.mapping_json.skills[].geometry_value` — **the field
`kit_compiler._rich_geometry_for_skill()` reads FIRST as authoritative** (`kit_reader.py:37`:
*"rich geometry_type from mapping (authoritative when present)"*). 99.7 % populated in the universe,
arity 27. **A VFX table keyed on this vocabulary lands on compiled kits by construction, because the
compiler IS the join.**

#### T-K — derivation of record

```sql
-- T-K: kit-skill -> (archetype, tier-1 layer flag)
-- Fold-aware per L-29(1) and L-29(2). Read-only. Reproduces 1,135 bound rows / 511 kits.
SELECT m.kit_id,
       m.skill_ordinal,
       m.source_skill,
       CASE m.archetype_id
            WHEN 'ring'           THEN 'circle'
            WHEN 'defensive_dash' THEN 'dash_attack'
            ELSE m.archetype_id
       END                                              AS archetype_id,
       CASE m.archetype_id
            WHEN 'ring'           THEN 'annulus'        -- Tier-1 layer flag: open travelling annulus
            WHEN 'defensive_dash' THEN 'defensive'      -- Tier-1 layer flag: i-frame / deflect flash
            ELSE NULL
       END                                              AS tier1_layer_flag,
       m.archetype_id                                   AS archetype_id_prefold,  -- lineage, never dropped
       m.geometry_value_raw,
       m.banded
FROM   vfx_archetype_member m
WHERE  m.vote_run     = 'vfx-archetype-vote-2026-08-23'
  AND  m.archetype_id IS NOT NULL
  AND  m.archetype_id <> 'knockback';                   -- HELD, § 3.2
```

**THE FOLDS ARE LOSSLESS, and this is the mechanism:** the folded archetype name does not disappear —
**it becomes a Tier-1 layer flag on the row**, and `archetype_id_prefold` retains the lineage. A row
that was `ring` is now `circle` + `annulus`; a row that was `defensive_dash` is now `dash_attack` +
`defensive`. **No skill changes its visual identity as a result of a fold; it changes which layer of
one shared effect carries that identity.**

#### Verification — the derivation executed live against `corpus.db`

| Check | Result |
|---|---|
| Bound rows returned | **1,135** (= 1,138 skill rows − 3 unassignable) |
| Distinct kits covered | **511** (96.2 % of the 531 active-combat universe; all 20 exclusions named in § 4.5) |
| Active archetype values returned | **24** — exactly the T-A active set |
| `tier1_layer_flag = 'annulus'` | **50** rows (the former `ring`) |
| `tier1_layer_flag = 'defensive'` | **4** rows (the former `defensive_dash`) |
| `circle` post-fold | **93 skills / 88 kits** (43 + 50 skills; kit overlap = 2, so 43 + 47 − 2 = 88 — **the overlap is real and the sum is NOT asserted**) |
| `dash_attack` post-fold | **36 skills / 35 kits** (32 + 4 skills; kit overlap = **0**, verified) |
| `knockback` excluded | **1** row held out |

### 4.2 The element parameter block — **Tier-1 binds to the SLOT, not to the element name, and not to the referent**

#### 4.2.1 The four rules

1. **Tier-1 keys on the ELEMENT SLOT TOKEN, never on the element name.** Element *names* are
   **seasonally generated** (`element/selector.py` proposes them per season; `pool.json` holds 214 of
   them — `ember`, `cinder`, `rime`, `hurricane`, `cloud`…) and they **drift by design.** The
   **slot** is stable and is what a palette / motif / trail-texture parameterization actually keys
   on. `pool.json` gives every element a `primary_slot` and optional `flex_slots`.
2. ⚠ **THE TRAP, and it is a real one: key on `water`, NEVER on `ice`.** The engine carries a
   **display rekey** — `simulation/resistance_matrix.py`:
   `_SUBSTRATE_DISPLAY_REKEY: dict[str, str] = {"water": "ice"}`, with the explicit in-code rule that
   **slot-routing tokens (`water_slot`, `primary_slot`, slot dict keys) are NEVER remapped.**
   `bc_target_player_class.py` therefore lists the player-facing canonical elements as
   `{fire, ice, earth, wind, lightning, holy, shadow, physical}` while the substrate slot is `water`.
   **A VFX table keyed on `ice` would silently miss the `water` slot on every row.** Tier-1 keys on
   the **substrate slot token**; `ice` is a display string and belongs only in player-facing text.
3. **The live slot vocabulary is FOUNDATION-DRIVEN, not hardcoded.** `element/selector.py`
   `_get_valid_slots(foundation)` computes it from `foundation.get_rotating_elements()`; the legacy
   constant is `VALID_SLOTS = ("fire", "wind", "water", "earth")`. **Tier-1 must therefore ship
   `live_rotating_slots + physical`, read at build time — not a frozen list.** Today that is
   **5 parameter values: `fire` · `wind` · `water` · `earth` · `physical`.**
4. **The eighth-through-tenth slots exist but are VOCAB-FROZEN.** `pool.json` carries
   `lightning` (13), `holy` (14) and `shadow` (12) as `primary_slot` values, but they are subject to
   the vocab freeze recorded in `vfx_coverage_manifest.json` (*"Frozen IDs: thunder, bolt, divine,
   umbra — reserved for Phase-1 P1 introduction; freeze enforced at load-time in
   `pool.py _validate_pool_invariants`"*). **Tier-1 is authored so those three slots DROP IN without
   re-authoring** — that is the whole point of parameterizing on the slot rather than the name.

#### 4.2.2 The engine already grades element→VFX feasibility — bind to it, do not duplicate it

`reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json` (v1.0, 2026-05-17; Drift-14
Track A legolas + Track B gandalf synthesis + rocket derivation) grades **156 elements** on
`vfx_mapping_tier`:

> **A** = direct vendor-catalogue coverage · **B** = palette-shift clean · **C** = composite required ·
> **D** = custom-commission or biological/organic rendering incoherent · **E** = non-visual.

**This is the pre-existing artifact Tier-1 binds to. This spec does not re-grade a single element** —
element grading is rocket's seam.

| Slot | A | B | C | D | E | Read |
|---|---:|---:|---:|---:|---:|---|
| `fire` | 9 | 13 | 10 | — | — | fully palette-shiftable; no D/E at all |
| `earth` | 8 | 23 | 8 | 14 | — | B-dominant; 14 custom-commission cases |
| `water` | 7 | 11 | 6 | 9 | — | healthy A/B core |
| `wind` | 5 | 10 | 15 | **8 E** | | **the hard slot** — C-dominant, and the only slot with non-visual entries |

⚠ **Coverage gap, stated as a fact and routed, not papered over:** the manifest covers **156 of the
214 pool elements**. **All 58 ungraded elements are `d1_status = 'allow-list'`** — i.e. every one of
them is *eligible for selection right now*. Of those 58: **38 are in the three frozen slots**
(holy 14 / lightning 12 / shadow 12 — correctly ungraded, they are not live), and **20 are LIVE-slot
pool additions made after the manifest was generated** (fire 6, water 6, earth 4, wind 4). Among the
100 allow-list elements, only **42 carry a tier at all** (A 23 / B 15 / C 4 — a healthy shape where
it exists).

> **Consequence for Step 2, stated plainly: Tier-1 element parameterization can claim graded
> feasibility for 42 of the 100 currently-selectable elements.** A season that rolls one of the 20
> ungraded live-slot elements will hit an ungraded VFX case. **This is not a blocker** — the slot
> binding still works and the effect still recolours — **but "recolour survivability is graded" is
> only true for the graded 42.** A manifest refresh is owed and is routed to rocket in § 6.3.

#### 4.2.3 The referent element is ANNOTATION ONLY — with the measurement that makes it useful anyway

The engine's own per-skill element chain is
`skills[].element_primary` → `canon_corpus.original_element` → `"physical"`
(`kit_compiler.py:544,558` — `skill_element = (skill.element_primary or element)`, emitted as
`canonical_element`). Executed over the bound corpus it resolves as: **375 from the skill field ·
510 from the kit field · 250 to the `"physical"` default** — into a **source-game vocabulary**
(`physical` 528, `fire` 150, `lightning` 101, `shadow` 100, `water` 62, `n/a` 61, `earth` 35,
`holy` 25, `pierce` 16, `cold` 15, `magic` 10, `poison` 10, `chaos` 5, `vitality` 5, `aether` 1,
`mixed(fire/cold/lightning)` 1, …).

> **This is NOT the runtime parameter and must never be bound as one.** It describes *what the
> referent skill was in its source game*. Our elements are seasonally generated. **T-K carries it as
> `referent_element` — annotation, stamped "not the runtime parameter."**

**But it measures something real, and this is where the Tier-1 surface class comes from.** Per
archetype, the share of members whose referent resolves to a non-elemental value (`physical`, `n/a`,
`pierce`, `bleed`, unknown):

| Element-AGNOSTIC ≥ 65 % → **TRAIL-BOUNDED** | | Element-COMMITTED ≤ 40 % → **PAYLOAD-CARRIED** | |
|---|---:|---|---:|
| `leap_strike` | **100 %** | `chain` | **6 %** |
| `whirlwind` | **82 %** | `fork` | 20 % |
| `ground_slam` | 81 % | `ground_targeted_circle` | 23 % |
| `melee_arc` | 79 % | `beam_channel` | 30 % |
| `ricochet_bounce` | 78 % | `circle` | 39 % |
| `melee_strike` | 70 % | `cone` | 39 % |
| `dash_attack` | 69 % | `totem` | 41 % |
| `placed_lane` | 67 % | | |

⚠ **The correlation with L-19 holds at the extremes and BREAKS in the middle — printed with the
contradiction visible.** The weapon-motion archetypes cluster at 70–100 % agnostic; the
payload-identity archetypes cluster at 6–41 % — **that is the L-19 causality axis corroborated by an
independent substrate measurement nobody designed for the purpose.** But **`aura` (62 %) and
`self_buff` (59 %) are magical-cause and yet element-agnostic**, because their referent skills are
stat-buffs whose element is a damage-type detail rather than a visual identity. **They are therefore
classified `FIELD-CARRIED` on design grounds, not on this measurement** — a third class exists
precisely because the two-class story is not true.

> **STEP-2 REVISIT TRIGGER on the surface class (pre-registered):** if a minted `TRAIL-BOUNDED`
> archetype's element variants are judged **indistinguishable at the gameplay camera**, the class
> assignment was too tight and that row moves toward `PAYLOAD-CARRIED` — with the receipt recorded.
> Conversely, if a `TRAIL-BOUNDED` variant is judged to have **lost its physical read**, the tint
> surface was expanded past the L-19 boundary and the class held correctly. **Both outcomes are
> informative; neither is a failure of the axis.**

### 4.3 T-K rollup — the element parameter block per archetype

**Every row ships Tier-1 with the base binding (charter § 3.3 — non-negotiable).** The columns below
specify *what the tint touches* and *what it must not*. The tier-2 column is **PROPOSED throughout —
it is Matt's ratification item, and § 5 is where it is asked.**

| Archetype | skills | Tier-1 surface (SPEC-ASSERTED) | Slot params shipped | Tint touches | Tint must NOT | Tier-2 (**PROPOSED — Matt ratifies at seal**) |
|---|---:|---|---|---|---|---|
| `ground_targeted_circle` | 115 | PAYLOAD | live slots + `physical` | perimeter decal · descending payload · residue | raise coverage past mid-band; soften the perimeter | — |
| `melee_strike` | 115 | TRAIL | live slots + `physical` | weapon trail · hit-response spark | become a body-surrounding field | **Class-B pattern** (third-stroke escalation, no bespoke asset) |
| `self_buff` | 112 | FIELD | live slots + `physical` | floor decal · local emitters | raise opacity/radius; obscure the character | ⚠ **Class-A: `transformation` sub-flag** |
| `totem` | 97 | PAYLOAD *(attack only)* | live slots + `physical` | the delegate's attack + impact | attempt to recolour the delegate's **body** (needs a MODEL) | ⚠ **Class-A CONDITIONAL: delegate body** |
| `circle` *(⊕ `ring`)* | 93 | PAYLOAD | live slots + `physical` | erupting element · front · contact | fill the interior when `annulus` is set | — |
| `single_target` | 90 | PAYLOAD | live slots + `physical` | payload body · trail · impact residue | widen the trail until it reads as a beam | — |
| `melee_arc` | 76 | TRAIL | live slots + `physical` | crescent · contact spark | thicken the crescent into a field | — |
| `aura` | 73 | FIELD | live slots + `physical` | radius ring · influence particles | change radius or opacity (readability contract) | — |
| `multi_projectile` | 68 | TRAIL | live slots + `physical` | projectile bodies · trails · impacts | alter count / spacing / range (engine params) | — |
| `line` | 51 | PAYLOAD | live slots + `physical` | body · pierce trail · contact | become sustained (that is `beam_channel`) | — |
| `dash_attack` *(⊕ `defensive_dash`)* | 36 | TRAIL *(smallest surface in T-A)* | live slots + `physical` | brief trail · knockback response · [`defensive`] deflect flash | enlarge the trail into an aura | — |
| `whirlwind` | 33 | TRAIL | live slots + `physical` | weapon trail · contact spark | **expand into a caster-surrounding field — that IS Eye of Reckoning** | ⚠ **Class-A: the owner-invested row** |
| `ground_slam` | 27 | TRAIL | live slots + `physical` | weapon arc · ground-burst decal | persist the decal into a field | — |
| `beam_channel` | 23 | PAYLOAD | live slots + `physical` | beam body · origin flare · contact marker | drop the persistent contact marker | — |
| `blink` | 18 | PAYLOAD | live slots + `physical` | traversal streak · arrival | go low-contrast on dark terrain | — |
| `cone` | 18 | TRAIL | live slots + `physical` | the fan · launch response | blend into terrain | — |
| `orbit` | 18 | TRAIL | live slots + `physical` | payload motif · trail | fill the negative space around the caster | — |
| `chain` | 17 | PAYLOAD | live slots + `physical` | segments · **endpoint flashes** | read as one continuous sweep | — |
| `vortex_pull` | 15 | PAYLOAD *(provisional — AUTHOR-not-SELECT)* | live slots + `physical` | field · debris | — *(effect does not exist yet)* | — |
| `placed_lane` | 9 | FIELD + PAYLOAD (pillars) | live slots + `physical` | lane body · **end pillars** | become opaque at vertical extent | — |
| `ricochet_bounce` | 9 | TRAIL | live slots + `physical` | thrown body motif · leg trails | alter leg count / range (engine params) | — |
| `teleport` | 8 | PAYLOAD | live slots + `physical` | departure + arrival flashes | fall below the ≥ 1 % arrival-burst floor | — |
| `leap_strike` | 8 | TRAIL *(100 % agnostic — smallest natural surface)* | live slots + `physical` | trajectory · impact | manufacture a surface that is not there | — |
| `fork` | 5 | PAYLOAD | live slots + `physical` | parent · **branch point** · children | obscure the branch point | — |
| **`knockback`** | 1 | **HELD** | — | — | — | — |

*"live slots + `physical`" = `foundation.get_rotating_elements()` + `physical`, read at build time.
Today: `fire` · `wind` · `water` · `earth` · `physical` (5 values). See § 4.2.1 rules 3 and 4.*

### 4.4 T-K row shape — verbatim sample from the live derivation

```
kit_id                    ord  source_skill                     archetype_id            tier1_layer_flag
------------------------  ---  -------------------------------  ----------------------  ----------------
chr-bleed-berserker        0   Take Down / Glacial Roll (…)     melee_strike            —
chr-bleed-berserker        1   Internal Hemorrhage erupti…      circle                  —
chr-bloodbinder-warlock    0   Poison skill activation (p…)     single_target           —
chr-bloodbinder-warlock    1   Living Blood companion swa…      totem                   —
chr-demon-legion-warlock   0   Hell Pit (main attack / de…)     single_target           —
chr-demon-legion-warlock   1   Demon army (Demonologist c…)     aura                    —
chr-fire-berserker         0   Fire skills (Dragon Storm …)     melee_strike            —
chr-fire-berserker         1   Dragonfire Garb explosion…       circle                  —
chr-fire-berserker         2   Smoldering Stone burning g…      ground_targeted_circle  —
chr-firestorm-warlock      0   Firestorm / Hell Pit (prim…)     ground_targeted_circle  —
```

**Read what this sample proves:** `chr-fire-berserker` — a single kit — binds three skills to three
different archetypes, and all three ship the same Tier-1 slot parameter. **That is the archetype-first
factory working: three effects drawn from a shared library of 24, tinted by one element, rather than
three bespoke authoring jobs.** It is also why the tier-2 "deserving" question is per-kit and not per
archetype (§ 5).

### 4.5 T-K residue — every exception named, none forced

**Nothing in this section is bound to an archetype. Forcing them would be the hand-imposition the
charter forbids at P1 and this spec declines to smuggle in at P4.**

| Class | n | What it is | Disposition |
|---|---:|---|---|
| **Unassignable skills** | **3** | `gd-blight-fiend-ritualist#0` (Summon Blight Fiend) · `gd-pet-conjurer#0` (Summon Briarthorn + Summon Familiar) · `gd-trozan-druid#1` (Wind Devil). `geometry_value` NULL **and** `skill_geometry_band` absent, so the engine's `_DELIVERY_TO_RICH` fallback has no input either. | **UNBOUND.** The engine would default them to `single_target` at compile — **a DEFAULT is not an ATTESTATION** (merge-log M-5, REJECTED). Their names read as summon-class, but assigning by reading the skill *name* is precisely the forbidden move. **Each of these kits carries a second, assigned skill, so no kit is lost.** |
| **Kits with no `kit_mapping` row** (sentinel ordinal −1) | **6** | `chr-crown-proc-engine` · `di-druid-pvp-cc-stack-2026` · `la-destroyer-gravity-{compression,force,impact}` · `la-destroyer-vortex-gravity` | Out of scope. Coverage gap, not a taxonomy gap. |
| **Kits with a mapping row but EMPTY `skills[]`** (sentinel ordinal −2) | **14** | `chr-arrow-storm-warden` · `chr-bee-warden` · `d2-wl-void-rift` · `d4-spiritborn-vortex` · `di-bombardment-wizard-pvp` · `di-minion-necro` · `di-spiritform-druid-pvp` · `gd-berserker-wereforms` · `hot-blood-catcher` · `hot-spirit-warrior` · `la-communication-overflow-summoner` · `la-enhanced-weapon-deadeye` · `la-master-summoner` · `ud-snowstorm-frost` | **Finding F-2** — structurally complete mapping rows (`motion_frame` / `scaffold` / `t4_doors` / `resource_economy` / `trigger_grammar` all present) with an empty `skills[]`. **A re-mapping lap would raise kit coverage 96.2 % → 98.9 % with NO change to the archetype set.** elrond's seam, separate lap (§ 6.3). |
| **F-4 — unassignable-by-construction** | 1 kit | `gd-berserker-wereforms` (the play-test-v1 fixture) maps to **zero** archetypes because its `skills[]` is empty; extracting framesets from it would have required hand-assigning skills to archetypes. **The honorable pause at L-16 was correct.** | Logged in `vfx_archetype_member.unassignable_reason`; folded into the F-2 lap. |
| **F-3 — `knockback`** | 1 skill | § 3.2. | HELD; re-band at the next kit-mapping lap. |

**Total accounting, asserted in-script at P1 and re-verified here: 511 bound kits + 6 sentinel-(−1)
+ 14 sentinel-(−2) = 531** — the full active-combat universe, with every exclusion named.

---

## 5 · **PROPOSED Tier-2 deserving list — MATT'S RATIFICATION ITEM**

> ## ⚠ THIS ENTIRE SECTION IS **PROPOSED**, NOT SPEC'D.
> **Charter § 3.3: *"the deserving list is Matt's ratification, not the run's."* Charter § 5 lists
> the tier-2 deserving list as a COMMITMENT BOUNDARY — a HALT-to-Matt item, always.**
> The `tier-2` column throughout § 4.3 is stamped **PROPOSED** for the same reason. **Nothing in this
> section is authorized by the run, and Step 2 mints nothing from it until Matt rules.**
>
> What is offered here is what a proposal owes: **named candidates, the specific reason each one
> cannot be carried by a Tier-1 parameter, the cost class, and a stated lean.** The lean is the
> spec-author's; the ruling is Matt's.

### 5.0 The rule this list is proposed against

Charter § 3.3 defines Tier-2 as *"bespoke signature flourish… the one or two skills carrying a kit's
fantasy."* **That is a per-KIT designation, not a per-archetype one** — which is why § 4.3's tier-2
column is nearly empty and why this section splits in two.

**The proposed deserving test — three predicates, all required:**

1. **Tier-1 CANNOT carry it.** The fantasy lives in a property a palette / motif / trail-texture swap
   does not reach (a silhouette, a body, a cadence).
2. **It is the thing the player would describe** when asked what the kit *is*.
3. **The cost is bounded and nameable** — one flourish layer, not an open-ended art commission.

⚠ **A distinction this list deliberately draws, because conflating them would inflate the ask:
AUTHORING NECESSITY IS NOT TIER-2 DESERVING.** `vortex_pull` must be authored from scratch (drax
C-6 — we own zero attractor content) — **that is a Step-2 authoring obligation on a BASE binding, not
a bespoke signature flourish, and it is NOT on this list.** Similarly `teleport`'s coverage floor is
a base-quality requirement, not a flourish.

### 5.1 Class A — archetype-level candidates (3)

*Where the archetype's fantasy is structurally beyond Tier-1's reach.*

| # | Candidate | Why Tier-1 cannot carry it | Cost class | Skills behind it | Spec-author lean |
|---:|---|---|---|---:|---|
| **A-1** | **`self_buff` → `transformation` sub-shape** (D3 Archon as the reference; substrate exemplars `Werewolf`, `Fade`) | **A transformation REPLACES the silhouette; a decal buff must NOT touch it.** These are opposite requirements on the same property, and one canonical cannot serve both. No recolour of a floor decal produces a werewolf. **This is the one genuine SPLIT question the run found** (P3 § 6.5), routed here by L-29(8) rather than executed. | **Model + rig**, not a VFX layer. Highest cost on this list. | subset of 112 | **LEAN: YES, but scoped.** Not "all transformations" — **one transformation treatment, reused as an archetype sub-shape**, exactly as the base bindings are reused. The alternative is that `Werewolf` ships as a tinted floor decal, which would be the most visible design failure available to us. |
| **A-2** | **`whirlwind`** | The owner-validated row, the L-19 exemplar, **82 % element-agnostic — the smallest Tier-1 surface of any T1/T2 archetype except `dash_attack`.** Tier-1 buys very little here by construction, and the row simultaneously carries the run's thinnest pixel evidence and the run's only measured cadence data. If any single archetype earns a bespoke pass, the evidence says it is this one. | **One flourish layer** on an existing base binding. Bounded. | 33 | **LEAN: YES.** This is the move Matt named from taste, twice, before any instrument was built. It is also the row where a mediocre base binding would be most obvious to the person who cares most. |
| **A-3** | **`totem` → the delegate BODY** | ⚠ **CONDITIONAL — and I flag the conflation risk myself.** Tier-1 can recolour what a totem *throws*; it cannot recolour what a totem *is* (§ 3.1.4, `P = 4` ceiling). **But a delegate body is a MODEL-pipeline cost, not a flourish** — it sits closer to A-1 than to A-2, and closer to an authoring obligation than to a signature. | **Model pipeline.** Unbounded unless scoped. | 97 | **LEAN: DEFER, and re-ask after A-1 rules.** If A-1 lands a transformation treatment, the delegate-body question may be answerable by the same pipeline at marginal cost. Ruling them independently risks buying the same capability twice. |

### 5.2 Class B — kit-signature slots (the charter's actual Tier-2 shape)

*"The one or two skills carrying a kit's fantasy" — per kit, not per archetype.*

**PROPOSED RULE, not a list:** each kit may nominate **at most one** kit-signature Tier-2 slot,
applied as a flourish **layer over its base archetype binding** — never as a replacement effect.

⚠ **PROPOSED SCOPING, and this is the load-bearing part of the ask: designate signature slots ONLY
for the kits in the demo-scope roster, whatever roster the game canon names** (`canonical/
reap-die-rise-game/`) — **not for all 511.** Designating 511 kit signatures is a content lap in its
own right and would swallow Step 2 whole. **This spec deliberately does NOT propose a roster; naming
one would pre-empt a decision that is not the run's** (§ 7).

**A named zero-cost pattern, offered as evidence that Class B need not be expensive:** `melee_strike`'s
canonical (LE Rive) **escalates on the third stroke.** That is a cadence-coupled flourish hook
**with no bespoke asset** — a Tier-2-shaped payoff bought out of the base binding's own structure.
**Where a kit's fantasy can be carried by a pattern like this, it should be, before any bespoke art is
commissioned.**

### 5.3 What ratification looks like

**Matt's ruling is needed on four things, and only four:**

1. **A-1** — ship a scoped `transformation` treatment? (YES / NO / scope amendment)
2. **A-2** — grant `whirlwind` a bespoke flourish layer? (YES / NO)
3. **A-3** — defer the delegate body behind A-1, or rule it independently now?
4. **Class B** — adopt the "at most one signature slot per kit, demo-scope roster only" rule, and
   name the roster boundary?

**If the seal does not resolve these, they belong in `canonical/matt_decision_needed/` as a single
ARCHITECT-shaped row rather than riding silently into Step 2** — filing that row is the conductor's
call at the run boundary, not this spec's (§ 6.4).

---

## 6 · Residuals register

Everything the run knows it has not closed. Nothing here is hidden inside a row's prose only — this
is the index a reader can act from.

### 6.1 Step-2 revisit triggers (pre-registered HERE, before the build — never post-hoc)

| # | Trigger | Fires when | Consequence |
|---:|---|---|---|
| **RT-1** | **`ground_slam` ↔ `melee_strike` strike-surface axis** (SPEC-ASSERTED, § 3.1.13) | the two minted effects converge in authoring — same emitter, same anchor, same coverage envelope, distinguished only by a parameter | **the axis did not hold; the pair folds at the next lap with the receipt recorded.** Second-strongest merge candidate after the one already folded. |
| **RT-2** | **Tier-1 surface class** (SPEC-ASSERTED, § 4.2.3) | a `TRAIL-BOUNDED` archetype's element variants read as **indistinguishable** at the gameplay camera | that row moves toward `PAYLOAD-CARRIED`, receipt recorded. *(Converse outcome — a variant that has **lost its physical read** — confirms the class held.)* |
| **RT-3** | **`teleport` arrival-burst floor of ≥ 1 %** (SPEC-ASSERTED with derivation, § 3.1.22) | the FIRST minted `teleport` is scored against the floor **and against the eye** | if 1 % reads as invisible **or** as excessive at our camera, the number is corrected on that evidence. **Asserted so a builder has something to hit, not because it has been measured.** |
| **RT-4** | **`whirlwind` confound subtractability** (§ 3.1.12) | archival donor playback is verified **before** minting | if BOTH donors fail (bluetracker unplayable **and** the 2008 clip too degraded), the Dust-Devil confound is **un-subtractable** and the row's confidence drops materially below what "PRIMARY" implies. **Verify first; do not discover this at mint time.** |
| **RT-5** | **drax C-7 beam-pack fragility** | before scheduling `beam_channel`, `line` or `placed_lane` | **pre-flight: confirm the Binbun `beam_vfx` pack still loads.** It resolves only via `uid://`; a UID-cache rebuild breaks it. |
| **RT-6** | **`vortex_pull` cannot be validated on VFX alone** (§ 3.1.19) | the minted gate reaches this row | **do not score it against the VFX rubric in isolation** — its readability is carried by engine-side enemy displacement. Either the engine dependency has landed, or the row is scored with the dependency named as the limiting factor. |
| **RT-7** | **C-1 source concentration** | any future reference lap | corpus-wide PoE share is **48.4 %** (61/126) after the supplement lane; the **canonical set is 7/26 = 26.9 % PoE.** **C-1 is REDUCED, NOT RETIRED.** Do not let one studio's VFX grammar become the de-facto register by accretion. |

### 6.2 Cross-seam routings (this spec names them; it does not execute them)

| # | Finding | Owner | Route |
|---:|---|---|---|
| **X-1** | **`orbit` is absent from `kit_compiler._RICH_TO_SPATIAL`** — 18 skills silently gauged `point` where `whirlwind` gauges `circle`. Corroborated by `MIGRATION.md` V9 (`geometry:orbit` = 6, residual blocked bucket). | **engine seam** | via KR, POST-run (L-12 pattern). VFX authoring unaffected — the gap is in the run-time hit gauge, not the identity vocabulary. |
| **X-2** | **`vortex_pull` readability requires engine-side enemy displacement** — no VFX we mint can supply the inward vector. | **engine seam** | via KR at run close (L-30). Ties to RT-6. |
| **X-3** | **`vfx_coverage_manifest.json` refresh** — 20 LIVE-slot pool elements (fire 6 / water 6 / earth 4 / wind 4) are allow-list but ungraded; 38 more sit in the three vocab-frozen slots. Only **42 of 100** allow-list elements carry a tier. | **rocket (element seam)** | via KR. **Not a Step-2 blocker** — the slot binding works regardless — but "recolour survivability is graded" is only true for the graded 42. |
| **X-4** | **T-K materialization**, if the conductor judges § 0.1a insufficient: create `v_vfx_kit_skill_binding` from the § 4.1 derivation. | **elrond (catalogue seam)** | one-statement view; additive; this spec is read-only on `corpus.db`. |
| **X-5** | **"Verification of artifacts is not verification of claims"** — KR's process note from the L-31 correction (Discipline #19.1 cheapest-refuting-test applied to relayed quantitative claims). | **jack-ryan** | discipline-amendment candidate at run close (already registered at L-31). |
| **X-6** | **`use_fixed_seed` pinning for pixel gates on VFX-bearing clips** — converts `sa_gate.py`'s standing refusal into a measurable arm. | **jack-ryan** | methodology candidate at the L-20(i) ratification (§ 6.4). |

### 6.3 Future-lap items (no scope growth here — named so they are not re-derived)

- **F-2 — 14 active combat kits with an empty `skills[]`** despite structurally complete mapping rows. A re-mapping lap raises kit coverage **96.2 % → 98.9 % with NO change to the archetype set.** *(elrond)*
- **F-3 / F-4 / pre-fold `defensive_dash` — the unbanded residue, examined AS A GROUP.** Three unbanded shapes surfaced independently in this run (`knockback` n=1, `defensive_dash` n=4, F-4's zero-skill fixture). **The same shape appearing three times is worth one deliberate look rather than three ad-hoc guesses.** *(elrond)*
- **`skill.flavor_text` is 0/648 in the demo bundle** despite the `_w3_flavor` field name (L-12 ii).
- **`data/kit_space` is STALE** — named so nobody mistakes it for current (L-12 iii).
- **`source_game` string variance is NOT normalized** — `Diablo 3` / `Diablo III` / `Diablo III, 2008 pre-release build`. **Build and season qualifiers are real provenance; do not normalize them.** Any P4-or-later rollup keyed on `source_game` must group them **deliberately.**
- **Reference-corpus link health:** re-checking is cheap, but **403 is never absence.** Confirmed bot-blocked: `pathofexile.com`, `gamestar.de`, `bluetracker.gg`.
- **`melee_strike`'s canonical is a downloadable MP4** — cutting it is the cheapest evidence-tier upgrade available on any T1 row (§ 3.1.2).

### 6.4 Conductor rulings owed at seal — **explicitly NOT ruled by this spec**

A SPEC-AUTHOR sub-agent does not rule a conductor's pre-registered gates. Three items are banked with
their evidence and a stated lean; **the ruling is the conductor's, at the seal.**

| # | Owed | Evidence banked | Spec-author lean (non-binding) |
|---:|---|---|---|
| **CR-1** | **L-20(i) — formally ratify the P0-b determinism METHOD NOTE**, including its cross-run recommendation, and route it to jack-ryan as a methodology candidate. | The L-13(a) reclassification was vindicated: a hard SHA gate would have reported **0/13 — a manufactured "Metal is broken" signal.** Measured instead, drift isolates to the **GPUParticles3D emitter seed**; the `use_fixed_seed` arm is **13/13 byte-identical, all-frame.** Honest residual held (pinned ×4 → 3-of-4). | **RATIFY.** The note's instrument caught a false-signal generator before it entered an empirical track. X-6 is its forward form. |
| **CR-2** | **L-13(b)/L-20(ii) — rule the P0-b throughput limb-2 threshold against the ACTUAL Step-2 cadence.** | **535 renders/hr median (357–658)**, one 90-frame 3.0 s 1080p capture, warm, including process launch. drax's labelled *proposal* (not a gate): a bake-off round of ~30 candidate effects × 2 renders = 60 renders lands in **~7 minutes** at the median. | **NOT-ARMED.** Step 2's cadence is **24 archetypes × a small variant count**, not several hundred renders inside a single interactive session. The arithmetic does not reach a hostile cadence. **But the ruling is the conductor's — a post-hoc gate inside a pre-registered charter is exactly the safety violation KR refused on the conductor's behalf, and this spec does not commit it by proxy.** |
| **CR-3** | **Whether § 5's four ratification questions ride to Matt at the seal, or are filed as an ARCHITECT row in `canonical/matt_decision_needed/`.** | § 5.3. | **Ride at the seal if the seal happens; file the row if it does not.** Tier-2 is a charter § 5 commitment boundary either way — it does not enter Step 2 unruled. |

### 6.5 Gaps carried openly (not owed to anyone — simply true)

- ⚠ **`whirlwind` has ZERO windup coverage anywhere in the corpus** (§ 3.1.12). Mitigated, not closed, by the negative anchor's measured 0.70 s / 0.80 s ramps.
- ⚠ **Run-wide windup scarcity: 80.5 %** vs active 100 % / impact 97.3 %. **Two strong windup donors exist and should be reused across rows** — D3 Condemn's three-second charge (`circle` family) and PoE Demonic Leap Slam's anticipation crouch (`leap_strike`).
- ⚠ **`ground_targeted_circle`'s canonical has its L-19 physical half UNWITNESSED** — the co-reference carries it (§ 3.1.1).
- ⚠ **`whirlwind`'s evidence tier is OWNER-ATTESTATION + DOSSIER-TEXT.** The row the owner cares most about is the row with the least pixel evidence in the run. **Saying so is the point.**
- ⚠ **The P0-b cross-check covers 14 sampled frames/clip**, not all 90; the inputs were pruned; the measurements are **documented, not reproducible** (§ 2.2). Ruled sufficient at L-31 — **not re-litigated here.**

---

## 7 · What this spec does NOT decide

Named so a builder does not read silence as permission.

1. **Which pack asset gets mounted.** T-A gives semantics, readability targets, emitter geometry and constraints. **Asset selection is drax's, at Step 2.**
2. **The Tier-2 deserving list.** § 5 is PROPOSED. **Matt's ratification** (charter § 5).
3. **The demo-scope kit roster.** § 5.2's Class-B scoping needs a roster boundary; **naming one would pre-empt a game-canon decision that is not this run's.**
4. **Element grading.** `vfx_mapping_tier` values are rocket's seam. **This spec binds to the manifest; it does not re-grade one element.**
5. **Engine changes** — the `orbit` map gap, enemy displacement for `vortex_pull`, the F-2 re-mapping lap. **Named and routed (§ 6.2); not written.**
6. **The Step-2 build sequence.** KR sequences; the build-wave dispatch request is drafted **at run seal only**, because it consumes these tables (L-5). **gandalf never conducts the build he will DRIFT-CRITIC.**
7. **The two pre-registered P0-b gate rulings** (§ 6.4 CR-1, CR-2) — the conductor's, at the seal.
8. **Anything requiring a § 3 charter ruling to be reopened.** That is a HALT to Matt, not a spec revision.

---

## 8 · Closing — what the tables are for

Twenty-four effects stand behind one thousand one hundred and thirty-five skills. That ratio is the
whole design: a player who learns what a descending payload inside a crisp perimeter *means* has
learned it for one hundred and fifteen skills at once, and the tint tells him which of them is about
to burn him. **Telegraph literacy is not a nicety here — it is the return on the archetype-first
factory, and it is the reason the folds at L-29 were gains.**

The sharpest thing these tables carry is not a selection. It is a failure mode, named twice from
taste before any instrument was built and then confirmed twice in pixels, in two different skills, in
the same game: **an effect that expands, that leaves a mark on the ground, and that never touches the
bodies it passes through.** Every `TRAIL-BOUNDED` row in § 4.3, every "must NOT" in the element
parameter block, and the whole of L-19 exist to keep that failure out of the thing we build.

And the row the owner cares most about is the row with the least evidence — a whirlwind nobody could
photograph, described from memory, built from a description, and approved by the only instrument that
has ever actually seen it. **That is not a weakness in the corpus. It is the argument for why the
owner's eye stays in the loop, and it is written into the row rather than dressed up as a score.**

---

*Authored by gandalf (`SPEC-AUTHOR`), 2026-08-24, VFX archetype-binding run **P4**. Read-only on
`corpus.db`, on the engine tree, on all 30 dossiers, and on every seam tree outside `gandalf/`. No
production code written. **STATUS: DRAFT — awaiting DRIFT-CRITIC by the conductor and Matt's seal
ratification.** The tier-2 deserving list (§ 5) is Matt's, and is marked PROPOSED throughout.*
