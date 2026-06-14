# Session hand-off — the path to a fully-extended 2D spatial engine + end-to-end entity→JSON→PC pipeline

**Type:** session hand-off / loose roadmap (gandalf seam).
**Date:** 2026-06-13
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-13.
**Purpose:** loosely list the journey toward the two destinations, mark what is DONE / IN-FLIGHT / NEXT / GATED / FORWARD, and set the next-session pickup. This is a path sketch, not a spec — the gates and seam-owners are firm; the ordering past the next batch is deliberately loose.

---

## 0. Where we are (one paragraph)

W-D (six-axis MEASURE) is **CLOSED** — oracle v1.6 (`canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`, commit `8974209`): 8 axes wired, the per-axis discrimination decompose is clean (0 category-(e) live obligations), arity locked at 8 (proxy-density = the existing Axis-2A, not a 9th axis). cond.4 = PASS, and — load-bearing — cond.4 can no longer masquerade as "the archive measures the kit," because §6.4 now gates that claim on the clean discrimination accounting + cond.5, which closes at W-F. A **parallel autonomous batch** is in flight: **Run A** (gamora — W-E throughput build + displacement-histogram emit + the 2 Gate-2 doc-lines) and **Run B** (rocket — D6 loader fix + D5 reference-kit). D4/proxy-port is parked for a later batch. The two destinations below are **loosely-coupled tracks** joined at a single keystone — the entity-packet schema.

---

## 1. The two destinations

1. **A fully-extended 2D spatial engine** — all 8 axes *discriminate* (not merely wired), the reference set exercises every axis, the 1D `search_estimator` is deleted, and the spatial engine is the **sole COMMIT-grade balance authority**.
2. **An end-to-end pipeline** — a generated, balanced entity leaves the engine as a **JSON packet**, crosses to the PC, and **manifests as a figure** in the UE world.

They proceed **in parallel** and meet at the **entity-packet schema** (Track 2, M2.2). The important design insight: the first end-to-end packet-to-PC does **not** have to wait for the fully-extended engine — a *provisional, caveated* entity can prove the whole pipeline while the engine extension continues. The schema is the joint.

---

## 2. TRACK 1 — extend the engine (the cert wave + axis closures)

| Stage | What | Owner | State |
|---|---|---|---|
| **M1.1** | W-D six-axis MEASURE — 8 axes wired, decompose clean, cond.4 PASS, arity=8 | gamora + gandalf | **DONE** (oracle v1.6) |
| **M1.2** | W-E throughput proof — commit-grade batch cost BOUNDED + TOLERABLE (~11 s / 34 survivors; ~54× cheaper/fight than 1D) | gamora | **CLOSED** (Run A `02e2a6f`; gandalf design-endorse + jack-ryan Gate-2 WARN→PASS; Matt-ratified 2026-06-14) |
| **M1.3** | Axis-discrimination closures — graduate the 6-of-8 not-yet-discriminating axes from *wired* → *discriminating* | mixed | **STAGED / partial** |
| **M1.3.5** | **Reduced-spatial inner-loop search substrate** — the cheap, spatially-honest evaluator the recompose loop runs on post-1D. The inner loop runs on **1D today** (`balance_loop.py::_primary_recompose_loop` → `search_estimator.simulate_fight`); §4.2 forbids 1D as the substitute, §4.3 forbids full-2D. **Acceptance spec DONE** (`gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md`); build pending sequencing. | gandalf (spec) + gamora (build) | **NEXT-CANDIDATE / hard W-F precondition** |
| **M1.4** | **W-F — the 1D-delete gate** — cond.5 (defensive-bridge boss re-validation) + §6.4 final close (discrimination accounting CLEAN). **Precondition: M1.3.5 must land first** — else the delete strands the recompose inner loop. On pass: 1D estimator deletes; spatial engine sole authority; `fight_engine.py` tombstone removed | gamora + critique pair | **GATED** (keystone; irreversible — stays human/critique-paired) |
| **M1.5** | Cascade / 7th-kit (§4.C cluster-density) — if promoted via Bucket-B, arity 8→9 | gandalf ruling | **FORWARD** (open design-call, not committed) |

**M1.3 detail — how each non-discriminating axis closes (discrimination-test principle: the lever must MOVE the bin):**
- **Mobility (Axis-1 mobility-half)** — (d) LOCK-EDGE; re-calibrate the 1D-era 30-tiles/min edge for spatial telemetry → gated on **Run A's displacement histogram** (gandalf).
- **Proxy / Axis-2A** — (a) DEFERRED; needs the **§4.D sustain-for-proxy fixture** (the room where a standing population discriminates) → **D4 proxy-port** (gamora + gandalf; the density contract is written; **held for a later batch**).
- **Resource / Control / Tempo (Axis-5 et al.)** — (b) UNDIFFERENTIATED; the hand-built set is uniform on these, so they are wired-but-not-*exercised*. **D5's resource/CC-differentiated kit exercises them** (rocket, Run B).
- **Defensive (Axis-4)** — (c) WRONG-ROOM; inverts in density rooms, discriminates in the **W-F boss room** (cond.5).
- **Variance** — partial; closes alongside the above.

**Track-1 "done" ≈** W-E closed [✓ 2026-06-14] + all axes discriminate + reduced-spatial inner-loop substrate built (M1.3.5) + W-F 1D-delete passed. The engine is then the single trustworthy, *discriminating* balance authority for spatial entities. (The cascade arity question can ride forward without blocking this.)

---

## 3. TRACK 2 — the end-to-end pipeline (entity → JSON packet → PC → manifest)

| Stage | What | Owner | State |
|---|---|---|---|
| **M2.1** | Measured-entity export — first JSON emit of kit data | star-lord | **NEXT / dispatched** (`dispatches/2026-06-13-star-lord-wd-export.md`; gated on gamora MIGRATION v1.31). **Caveat:** bins are wired-not-yet-fully-discriminating → the first export is structurally real but **NOT stamped "measures the kit"** until W-F. |
| **M2.2** | **Entity-packet schema — the convergence keystone** — the one JSON contract BOTH star-lord emits AND mantis ingests; must carry balanced-stats (engine) + form/manifestation-spec (what UE needs to render the figure) + element/anchor/foundation metadata | gandalf (intent) + star-lord (emit) + radagast/mantis (UE ingest) + elrond (schema steward) | **NEEDS DESIGN** (the joint where the two halves meet; today each half is proven independently) |
| **M2.3** | Transport Mac→PC — git push/pull as the file-based message bus + cross-host notes | KR / david-h | **ESTABLISHED** (federated team already runs on it) |
| **M2.4** | PC ingest + manifest — mantis reads JSON in UE → instantiates the entity as a figure → renders with celestial-sphere environment + figure-lighting (manifestation Phase-1 spike S1+S5) | mantis + david-h | **IN-FLIGHT / console-gated** (Wave 1 headless CLOSED; **Wave 2 M1–M7 console render is Matt-gated — DXGI, needs Matt's hands at the PC console**) |
| **M2.5** | Form→mesh→figure bridge — entity "form" (form-library / earth-self spirit, LLM-generated) → mesh (Meshy / image-pass-through AI-asset pipeline) → UE-renderable figure (the figure is a `FigureStandIn` placeholder today, Q5) | rocket + star-lord + mantis | **FORWARD** (AI-tell discipline D7 governs player-facing form quality) |
| **M2.6** | Round-trip — PC manifests + plays → telemetry feeds back to the engine, closing the loop | star-lord + PC team | **FURTHER FORWARD** |

**Track-2 "first light" ≈** M2.1 (export) + M2.4 (ingest) meet over a M2.2 (schema). That is the first time a real entity crosses Mac→PC as JSON and appears in the world — achievable with a **provisional** entity before Track 1 fully completes.

---

## 4. The convergence (the one thing to keep in view)

Track 1 produces a **balanced, discriminating entity**. Track 2 **carries it to the PC and manifests it**. The **entity-packet schema (M2.2)** is the joint: it must carry *both* Track-1's measured stats and Track-2's manifestation spec. Lock that schema and the two tracks click together; leave it unlocked and the export half and the render half keep proving themselves in isolation. **M2.2 is the highest-leverage forward design call** — it is what turns "two halves built from both ends" into "one pipeline." It is not yet scheduled; it is the natural Track-2 keystone to spec once the export (M2.1) emits its first real shape and the PC manifest (M2.4) ingests its first real figure.

---

## 5. Next-session pickup

1. **Run A (gamora) reviewed [✓ 2026-06-14]** — W-E throughput **CLOSED + ratified** (design-endorse + Gate-2 WARN→PASS); displacement histogram banked (REFUTED the clean static/mobile median gap — multimodal, room-geometry-dominated; the mobility lock-edge re-cal is now an instrument-choice, not an edge-tweak — gandalf owes the PENDING-note rework). 2 jack-ryan W-E doc-lines → gamora (async; land before W-F cites the datum).
2. **Run B (rocket) reviewed [✓ 2026-06-14]** — D6 loader fix (9 modules green) + D5 K7 reference-kit. D6 surfaced 4 pre-existing generation-drift failures → gandalf-gated triage queue (controller-vs-caster 160==160 is the meaty one).
3. **Plan the next batch.** Candidates, loosely: **M1.3.5 reduced-spatial inner-loop substrate** (NEW — hard W-F precondition; **acceptance spec DONE**, build is gamora's; sequence before W-F); **D4 proxy-port** (unblocked — histogram banked + density contract consumed); **W-D-export** (if MIGRATION v1.31 landed); opening **M2.2 (entity-packet schema)** as the Track-2 keystone. Sequencing is Matt's call (the substrate is the one with a hard downstream gate — W-F — behind it).

---

## 6. Parked / gated (carry, don't lose)

- **D4 proxy-port** — held; joins a later batch after Run A banks the histogram (the histogram MUST be captured on the *current* movement AI before D4's movement-AI rework) and gamora consumes the §4.C/§4.D density contract.
- **Mobility lock-edge re-cal** (gandalf) — gated on the histogram; non-blocking.
- **Cascade / arity-9** — forward design-call; §4.C cluster-density room specced, no cascade kit exists yet.
- **PC Tier-B console render** (M2.4 Wave 2) — Matt-gated; DXGI means render-evidence + the #5 mythic-weight figure-light judgment need Matt at the console, not an SSH session.
- **Form→mesh→figure bridge** (M2.5) — forward; the `FigureStandIn` placeholder stands in until it lands.

---

**Signed:** gandalf, 2026-06-13
**For:** the loose path toward (1) a fully-extended, fully-discriminating 2D spatial engine — W-E → axis closures → W-F 1D-delete — and (2) an end-to-end entity→JSON→PC pipeline — export → entity-packet schema → transport → PC manifest — two parallel tracks joined at the schema keystone, with the next session set to review the Run A / Run B outputs and plan the next batch.
