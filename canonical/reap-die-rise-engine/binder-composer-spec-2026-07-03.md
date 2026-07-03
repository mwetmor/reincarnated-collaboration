# The Binder + Composer — Upstream Assembly Spec (one registry, two appliers)

> **STATUS:** SPEC-CURRENT v1.0 (2026-07-03) — authored in the run window per Matt's G10 ruling ("yes, author it in the window"), **WIDENED same-session by Matt's upstream-assembly question** (*"could [we] assemble the kits with the gear and weapons or could we assemble the map pack assets into procedurally generated completed dungeon units?"*). The widening is answered YES in-session; this spec carries both halves.
> **§11 exception rows: ALL THREE RULED AS-LEANED (Matt 2026-07-03) — two-applier widening CONFIRMED · lighting DYNAMIC · staging AS-STAGED.** The spec is fully ruled; decisions-log registration rides jack-ryan's next batch (post-run).
> **Author:** gandalf (SPEC-AUTHOR) · **Ruled anchors:** zero-hand-authored-content (Matt 2026-07-02) · problem-class modality routing table (Matt 2026-07-02: spatial-perceptual → editor; systems/logic → text; regression → headless harness) · procgen mapping (loop-doc `reap-die-rise-story/gameplay-loop-design.md` ~§, "graph-grammar macro → prefab meta-tiles → WFC biome field") · Q6/Q7 derivation rule (vi) single visual identity · determinism contract (same kit → same look, every emission) · Glance truth-path discipline (no LLM in a deterministic path).

---

## 0. The gap this closes

The zero-hand-authored-content ruling makes the emission pipeline the sole source of shipped content — but between the emitted JSON and a rendered Godot scene sits an unowned mapping: *which Synty modules, which weapon mesh into which socket, which VFX per skill geometry, which chunks into which floor.* Unowned, that mapping accretes as ad-hoc GDScript inside the Godot project — unversioned, untestable, engine-locked. That is the drift path. This spec names the subsystem, splits it correctly, and assigns its seams.

Matt's upstream-assembly question is the same recognition from the process side: push the MCP/Godot-editor work upstream, between JSON emission and the editor. The answer is the architecture our genre validated thirty years ago — **Blizzard North's DRLG split**: humans hand-author *tile sets with connection edges* (perceptual work, paid once); an algorithm assembles *deterministically at scale* (paid never again). Torchlight, Grim Dawn, and PoE's area generation are descendants. We are not inventing; we are inheriting.

## 1. The principle

**The editor discovers · the registry remembers · the appliers apply at scale.**

The Matt-ruled routing table stands unmodified: spatial-perceptual work (sword-in-hand, chunk-socket solving, shading, feel) belongs to the editor — but as **discovery, once per family**, captured back as registry data. Composition (joining, selecting, placing by rule) is deterministic code. Verification is sampled headless capture + galadriel rubric. **MCP/editor never sits in the per-content-unit path.** Without this system, every emitted kit and floor is an editor session; with it, each is a manifest row.

## 2. ONE registry (the shared substrate)

A machine-readable catalog of everything we own, as **versioned data in git** (JSON/CSV — diffable, reviewable, elrond's catalogue discipline applied to our own library; same pattern as the style-register catalogue). **The seed already exists:** `reincarnated-godot/catalogue/` — `packs.json` + per-pack manifests + thumbnails across 22 crawled POLYGON packs, with 50+ packs on disk under `Assets/Synty/` including eight-plus dungeon/structure packs.

Row classes and their load-bearing fields:

| Class | Key fields (beyond id/pack/path/provenance) |
|---|---|
| `character-module` | rig family · body slot · register status |
| `weapon-mesh` | weapon type (maps from emitted weapon descriptors) · grip class · **socket transform (editor-discovered, per rig family)** |
| `anim-clip` | rig family · verb class (locomotion / cast / strike / summon…) · pace multiplier (editor-discovered) |
| `vfx` | element tag · skill-geometry class (maps from emitted geometry types) · scale factor |
| `chunk` | biome/structure family · **connection sockets: edge list + mate transforms (editor-discovered, once per chunk)** · room-size class (tight / large) · encounter-geometry class · register status |
| `prop` | biome tags · placement class |

**Tagging axes = the emission axes** (element, coordinates/identity-glyph, weapon type, geometry class, biome) so binding is a filter, not a translation. Every editor discovery (a socket solved, a pace tuned, a shading fix) is **captured as a row amendment — discovered once, remembered forever.** Q7 King Rig retarget output is registry data the moment it exists; the rig work pays twice.

## 3. Applier #1 — the BINDER (*what things are*)

Emission JSON → **resolved entity manifest**, per kit (and per monster/gear item):

- **Inputs:** the kit's emitted fields — element, BC coordinates, `identity_glyph` (scouting-glyph spec, same date), weapon descriptors, gear slots, proxy types — plus the binding-rule table.
- **Binding rules:** deterministic, data-driven, **seeded among equivalents — same kit → same look, every emission** (the Q6/Q7 name-derivation determinism contract, applied to appearance). Rule shape: emission-axis filter → registry query → seeded pick. `identity_glyph` may drive module-family selection (a SUMMONER should read at silhouette — same law as the glyph spec's art requirement). Q6/Q7 rule (vi) *single visual identity* for converged proxies gets its data here: a CONVERGENCE pair binds ONE merged visual, by rule.
- **Output:** per-kit manifest — module set · meshes at sockets (transforms from registry) · clip set · VFX id per skill geometry. The Godot shell consumes it dumbly: instantiate, attach, wire. **No LLM anywhere in the bind path** (flavor was already written at emission; binding is truth-path).
- **Player consequence:** at the G7a roster pick, every one of the 100–400 in-band candidates is *already viewable* — geared, armed, animated. The pick becomes curation, not production.

## 4. Applier #2 — the COMPOSER (*where things go*)

**Not new design — the realization system for ruled canon.** The loop-doc already settles the procgen mapping: *graph-grammar lays out the macro beat-sequence (Structure→Biome→Structure→Escape); prefab meta-tiles build the architectural structures; WFC builds the biome field.* The Composer is that sentence, built:

1. **Macro pass (graph grammar):** the beat sequence is fixed (legible, lore-true); node budgets come from the ruled pacing law — *room-size grammar is the pacing signal: tight-fast → open-tactical → tight-climactic → flight.*
2. **Structure pass (chunk-socket assembly):** for tight architectural stages — pick chunks by registry filters (structure family, room-size class, encounter-geometry needs), mate socket-to-socket using the editor-discovered edge transforms, place spawn markers per encounter-geometry class. This is the DRLG inheritance proper.
3. **Biome pass (WFC):** the open field composes by wave-function collapse over chunk/tile adjacency constraints — same registry, different algorithm, per the ruled mapping. Few-but-big rooms (the ruled anti-slog law).
4. **Output:** per-floor **scene manifest** — chunk ids + transforms + spawn markers + prop placements. Seeded: same floor seed → same floor.

**The genre lesson baked in from day one:** Diablo III vanilla's "same four Act 1 layouts" problem was never assembly tech — it was thin chunk vocabulary and timid grammar weights. The Composer's quality ceiling = vocabulary size × grammar expressiveness. Our eight-plus dungeon packs are a strong starting vocabulary; the grammar weights are design data (mine to tune, playtest-informed).

## 5. The shell contract (what Godot does — and doesn't)

- Instantiate manifests; attach at sockets; wire VFX; **bake navmesh at runtime** (NavigationServer3D — no per-unit editor/import step; load-bearing for keeping the path pure).
- **Lighting — the one design call this surfaces (§11 row 2):** baked lightmaps would drag every assembled unit back through an editor/import bake — re-coupling exactly what this spec decouples. **Lean: dynamic lighting** (Forward+ carries it; torchlight pools are the Diablo-lineage dungeon look regardless). Baked GI, if ever wanted, is a launch-era per-chunk (not per-unit) question.
- The shell stays thin: all content intelligence lives upstream in *our* system.

## 6. Verification — sampled, never exhaustive

Spatial-perceptual **verification** cannot move upstream (the drax evidence that killed the modality re-charter: text is complete but perceptually opaque). But it shrinks to a **sampling discipline**: per grammar/binding-rule revision, headless-capture N assembled units + bound kits → galadriel rubric (seam continuity, readability, register conformance) + numeric asserts → editor eyes on FAILURES only. Authoring moves upstream; only auditing stays down. Expected curve, stated honestly: the first chunk-set and first binding-rule table are editor-heavy (Blizzard North iterated tile sets for months; ours is faster — Synty pre-solved chunk aesthetics); per-unit cost then decays toward zero and stays.

## 7. Payoffs that fall out for free

1. **The coverage report.** Binder + Composer run headless in CI (pure data→data): every emitted kit must bind fully, every grammar node must have eligible chunks. Failures are **named gaps** — "no water-element staff VFX owned" — so the Synty purchase list and reskin queue stop being vibes and become a number, continuously.
2. **Godot becomes cheap-to-exit while we commit deeper.** Manifests are runtime-agnostic; the benched web lane's re-entry cost drops to a shell rewrite. Deepen the commitment, shallow the lock-in.
3. **Convergence with ruled direction.** Both appliers are late stages of the serial content pipeline — callable, non-agentic, autonomous. Their runs register in the same run registry (W1 #8) that Glance's staged RUN-STATE pane surfaces. One cockpit.

## 8. Seams

| Who | Owns |
|---|---|
| elrond | registry schema + curation discipline (his catalogue pattern; seed = `reincarnated-godot/catalogue/`) |
| gandalf | binding-rule semantics + grammar weights (design-spec-as-data: which emission axes drive which asset axes; pacing law encoding) |
| star-lord | hosts Binder + Composer as export-pipeline stages; CI coverage report |
| drax | solves sockets/chunks/pace in-editor (discovery); captures rows back to registry; builds the thin shell consumers |
| galadriel | sampled-verification rubric + capture harness |
| KR | sequences build waves post-run (§9) |

## 9. Staging — empirical entry criteria, not dates

| Stage | What | Entry criterion |
|---|---|---|
| S0 (now) | this spec + elrond registry-schema draft | ruled (G10) |
| S1 | slice hard-codes its handful of bindings **with Binder-shaped seams** (manifest-consuming code paths, hand-written manifests) | demo phase opens (post-W4 roster pick) |
| S2 | registry fills: Q7 King-Rig socket data · slice discoveries · first chunk-set solved | Q7 lands + first structure pack solved in-editor |
| S3 | Binder v1 built; coverage report live against the W4 registered bundle | S2 + W4 bundle exists (it will) |
| S4 | Composer v1 (structure pass) → then WFC biome pass | S3 + chunk vocabulary ≥ first structure family complete |

Rationale: the slice must not wait on the Binder (hand-bound with the right seams = zero rework), and the Binder must not build before real socket data exists (spec-first, build-on-evidence — the same recognition→validate→commit discipline as everything else).

## 10. Out of scope — permanently

- **Reading 1 stays rejected:** no own engine. Rendering, skeletal animation, particles, audio, packaging remain Godot's. This system is *content intelligence*, not runtime.
- **No LLM in bind or compose paths** (flavor is written at emission; these are truth-paths).
- **No touches to the live W0–W4 run.** Both appliers consume its output; nothing here adds a run step.

## 11. Exception rows — ALL RULED (Matt 2026-07-03, each as the stated lean)

| # | Question | Lean → **RULING (Matt 2026-07-03)** |
|---|---|---|
| 1 | **Scope-confirm the widening:** one registry + TWO appliers (Binder = entities; Composer = spaces) as one system, per your upstream-assembly question | confirm — the Composer is the realization of already-ruled procgen canon, not new scope |
| 2 | **Lighting:** dynamic (upstream-pure) vs baked lightmaps (re-couples editor/import per unit) | **dynamic** — genre-true and keeps the pipeline pure; revisit baked-GI per-chunk at launch-era |
| 3 | **Staging order** (§9): spec-now/build-on-evidence, slice hard-codes with Binder-shaped seams | as staged — S1 protects the slice's speed; S3 gates building on real socket data |

---

**Sign-off:** gandalf, 2026-07-03 (SPEC-AUTHOR). Anchors: G10 ruling + Matt's upstream-assembly widening (this session) · zero-hand-authored-content · modality routing table · loop-doc procgen mapping · Q6/Q7 rule (vi) + determinism contract · scouting-glyph spec (same date) · Glance contract §7 (RUN-STATE pane convergence). The maxim, extended: *editor discovers, registry remembers, the Binder applies at scale — and the Composer assembles.*
