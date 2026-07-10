# Game (Playable Product) — End-to-End Product Pipeline (desired end state, current-state stamped)

> **STATUS:** MATT-FACING · LIVING — born 2026-07-10, third member of the product-pipeline family
> (Matt directive: *"What I need are the desired-state end-to-end pipelines of the actual products"*;
> format confirmed on the battle-sim + emission pair: *"the docs hit the mark"*).
>
> **PURGE-EXEMPT:** Matt-consumption surface — NEVER folded, retired, or purged without Matt's
> explicit ruling. Form-precedent: doc 39 §1 (2026-05-24).
>
> **Maintenance law — SAME-COMMIT (Matt condition 2026-07-10: "updated immediately and always"):**
> gandalf owns the doc; the commit that lands stage-changing work UPDATES that stage's stamp
> (**LIVE / PARTIAL / GAP**) in the SAME commit — the §2.7 FLOW-maintenance rule extended (owning
> agents: drax G1–G3/G6–G8 · star-lord G1 vendor APIs · galadriel G4/G7 · elrond G5). A build landed
> without its stamp update is an incomplete commit. Glance `/game` page renders this doc (contract v1.6).

**Siblings:** `pipeline-serial-content-emission.md` (makes the KITS this product dresses and spawns —
its E8 is this doc's G6 input) · `pipeline-battle-sim.md` (certifies what E-pipeline makes) ·
`pipeline-story.md` (makes the TEXT this product speaks) · `pipeline-arcade.md` (POST-LAUNCH mode
factory that composes all four). **This doc is the pipeline that turns
certified content + owned/generated assets into the thing a player runs:** the One-Realm MVP demo
(`../reap-die-rise-game/one-realm-mvp-scope.md` — THE DENOMINATOR), then launch builds.

---

## FLOW (end-to-end at a glance — Glance shape, contract § 2.7)

1. **G0 Design substrate** ← G0
2. **G1 Asset acquisition (two lanes)** ← G1
3. **G2 Mannequin, rig & retarget** ← G2
4. **G3 Ensemble assembly & band ladder** ← G3
5. **G4 Asset certification (Judge)** ← G4
6. **G5 Ensemble registry** ← G5
7. **G6 Scene & encounter assembly** ← G6
8. **G7 Capture & review loop** ← G7
9. **G8 Demo build & ship** ← G8

## The visual flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│ G0 · DESIGN SUBSTRATE (what the build consumes as law)                   │
│  • roster of record (serial tracker PART F: 31 + bench) + Matt's ~20 cut │
│  • race well (5 races, 2 mannequin frames) · run-composition model       │
│    (ONE-PEOPLE realm, 4 orders rotating, casting director)               │
│  • style register + Camera B′ (FOV 40 / −55° / 20 m, 8.02% D3 register)  │
│  • ensemble spec (../reap-die-rise-game/ensemble-asset-pipeline-spec.md) │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G1 · ASSET ACQUISITION — TWO LANES                                       │
│  LANE A (LIVE): owned Synty library (~60 packs, catalogue crawl)         │
│  LANE B (GAP · pilot-gated): GENERATED ensemble pieces —                 │
│   style bible → theme brief (LLM, narrow blanks) → ensemble sheet →      │
│   per-piece refs → image→3D vendor API → Blender reduce+Syntyfy          │
│   (MCP authors recipes; headless `blender -b -P` runs production)        │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G2 · MANNEQUIN, RIG & RETARGET (one mannequin per race-frame, forever)   │
│  human frame (human/orc/elf/dwarf — reskin tier) + goblin frame (Q7)     │
│  animation library retargets ONCE per frame · warp profiles (kit-level)  │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G3 · ENSEMBLE ASSEMBLY & BAND LADDER                                     │
│  rigid mounts (BoneAttachment3D) · skinned garments (weight transfer —   │
│  THE PILOT CRUX) · 5 slots × base/ornate mesh + 5 shader treatments =    │
│  band 1–10 per slot · stats→art interface = ONE INTEGER (loot-owned)     │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G4 · ASSET CERTIFICATION (galadriel Judge + automated checks)            │
│  budgets/LODs/skin-poses/seams/warps (scripted) · cohesion, style match, │
│  cross-kit distinctiveness, at-distance readability @ Camera B′ 20 m,    │
│  band monotonicity, mix cohesion (Judge) — asset-grain twin of A3 gates  │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G5 · ENSEMBLE REGISTRY (certified packets only)                          │
│  ensemble packet (kit_ref join to emission kits · pieces · lods ·        │
│  treatments · enemy_band_default · fitness_report) → referenceable       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G6 · SCENE & ENCOUNTER ASSEMBLY (Godot — drax)                           │
│  descent floors (three-gate authoring: G1 engine-truth → G2 register-CV  │
│  → G3 Matt) · casting director (faction-role rotation, anti-repeat) ·    │
│  W4 realm distribution · spawn/telegraph (band + race×register + affix)  │
│  · king-rig opening · hub→descent recurring transition (A′2)             │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G7 · CAPTURE & REVIEW LOOP (the judgment cycle)                          │
│  MP4 walkthrough harness (SHOOT-mode Metal, never --headless) ·          │
│  galadriel register-CV benchmarks vs genre peers · Matt live-play        │
│  rulings (Camera B′ precedent) — feeds fixes BACK to G1–G6               │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ G8 · DEMO BUILD & SHIP (One-Realm MVP — THE DENOMINATOR)                 │
│  GATE1 (surface-ledger all-✓) gates assembly-from-content ·              │
│  Binding-Rite-LITE + three-beat floors + escape + end-card ·             │
│  wishlist gates → Steam demo (AI-content disclosure at store setup)      │
└──────────────────────────────────────────────────────────────────────────┘
```

## Stage detail (Consumes / Does / Emits / State)

## G0 · Design substrate — **LIVE**
- **Consumes:** Matt rulings + ratified canon.
- **Is:** `../reap-die-rise-game/one-realm-mvp-scope.md` (THE DENOMINATOR) · roster PART F (31 + bench; Matt curates ~20, kit-grain certified) · `../reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md` (5 races / 2 frames, Leg-3-ready) · run-composition model (`../reap-die-rise-engine/faction-derivation-stack-spec-2026-07-06.md`: ONE-PEOPLE realm, 4 orders rotating) · Camera B′ ruled 2026-07-07 (dist 20 m, D3 register 8.02%) · `../reap-die-rise-story/style-register.md` · **ensemble spec canonized 2026-07-10** (`../reap-die-rise-game/ensemble-asset-pipeline-spec.md` + §13 annex).
- **State:** **LIVE** — all substrate docs exist and are Matt-ratified. Game-tracker PART A carries the locked presentation grammar (A1 "only author what the camera sees" · A2 F1-resolution · A3 three-gate method · A4 king-rig).

## G1 · Asset acquisition — **Lane A LIVE · Lane B GAP (pilot-gated)**
- **Lane A (owned library):** ~60 Synty POLYGON packs on disk (`~/Games/reincarnated-godot/Assets/Synty/`), catalogue crawl exists; register packs = the race×register dressing vocabulary (S1 weapon substrate already LIVE end-to-end).
- **Lane B (generated pieces — ensemble spec §6 Stages 0–5):** style-bible extraction (Stage 0 — frozen prompt blocks from the trailer generation history; trailer MP4s in `matt_notes_handoff_docs/`) → theme brief (LLM narrow-blank, D7 discipline) → ensemble sheet (theme locked at IMAGE layer, LAW 3) → per-piece refs → image→3D vendor (Tripo / 3D AI Studio, pinned versions — star-lord external-service seam) → Blender reduce+Syntyfy (planar decimate, palette-snap, chunkify, LOD chain — **LAW 4: MCP authors recipes, headless scripts run production, zero tokens at runtime**).
- **State:** Lane A **LIVE** · Lane B **GAP** — gates-on: **footsoldier smoke test** (~hours, image→mesh fidelity) then **plague-doctor pilot** (§10 go/no-go; crux = skinned-chest weight transfer; hybrid fallback keeps the lane viable). Steward lean (§13.6): fire the smoke test EARLY.

## G2 · Mannequin, rig & retarget — **LIVE (frames) · GAP (warp profiles)**
- **Does:** one mannequin per admitted race-frame, rigged once, forever (LAW 1 as generalized by the race well — annex §13.1). Human frame serves human/orc/elf/dwarf (reskin tier, bone-dump verified 21/21 sidekick-core); goblin frame = Q7 contract (`goblin_bone_map.tres` + `anim-goblin-locomotion`; drax retargets now). Synty modular faces = mannequin parameter; skin tone = palette parameter.
- **State:** frames **LIVE** (sidekick map render-proven on Wizard/King; race well Leg-3-ready) · **warp profiles GAP** (bone-scale presets + per-profile retarget validation unbuilt).

## G3 · Ensemble assembly & band ladder — **PARTIAL (rigid LIVE · skinned GAP · ladder GAP)**
- **Does:** rigid mounts via established `BoneAttachment3D` workflow (~60–70% of pieces) · skinned garments via deterministic weight-transfer recipe (ensemble spec §4.2 — **the single unproven span**) · band ladder binding: 5 slots × (base|ornate mesh) × 5 shader treatments = per-slot band 1–10; `band(slot) = power_to_band(realized_power(equipped[slot]))` — **LAW 6: the loot↔art interface is that one integer** (curve loot-owned; flag registered on the loot pair, annex §13.3). Enemies wear the ladder (trash 1–3 / elites 4–7 / bosses 8–10) = vertical threat telegraph.
- **State:** rigid **LIVE** (workflow established) · skinned **GAP** (pilot crux) · band ladder **GAP** (StyleProfile treatments unbuilt).

## G4 · Asset certification — **GAP (method ruled, checks unbuilt)**
- **Does:** automated (tri/material budgets, LOD presence, skin-weight validation poses, seam scan, warp retarget validation — drax scripts) + galadriel Judge (ensemble cohesion vs sheet · style match vs Synty/trailer anchor board · cross-kit distinctiveness · **at-distance readability at Camera B′ 20 m** · band monotonicity (sorted pairwise) · mixed-band cohesion). Asset-grain twin of the ruled A3 three-gate method; composes with E10 §7 telegraph channels (band = vertical, race×register = horizontal, affix = behavioral).
- **State:** **GAP** — method + protocol precedent exist (galadriel critic-in-the-loop, anchor boards); ensemble-specific checks unbuilt. LAW 5: nothing uncertified enters G5.

## G5 · Ensemble registry — **GAP (schema drafted)**
- **Does:** certified ensemble packets (`kit_ref` join to emission kits · pieces w/ mount/mesh/LOD/attach/treatments · pooled refs · `enemy_band_default` · fitness_report) become referenceable by character packets. glTF 2.0 + Godot import presets. elrond schema adjacency.
- **State:** **GAP** — schema drafted (ensemble spec §7); registry unbuilt. Join target: the same `kit_ref` grain the emission pipeline's feed-2 registry advances.

## G6 · Scene & encounter assembly — **PARTIAL**
- **Does:** descent floor authoring (three-gate: G1 engine-truth → G2 register-CV → G3 Matt; edge-socket/no-void ruleset banked) · casting director (faction-role rotation + anti-repeat; consumes bundle-v2 faction blocks) · W4 realm distribution (elf-native, human common, goblin war-camps in ravine) · spawn + telegraph binding (visible-engagement-band law ≈29 m at B′) · king-rig opening scene (A4 LIVE) · hub→descent recurring-transition (A′2 banked).
- **State:** **PARTIAL** — ravine at-grade level + F1-scale review room + king-rig EXIST; **first authored floor NOT yet** (tracker B2, MVP-CRITICAL); camera ratifies at that floor (B1); casting director sequences after bundle v2.

## G7 · Capture & review loop — **LIVE**
- **Does:** MP4 walkthrough harness (SHOOT-mode grabs run Metal **without** `--headless` — headless → Dummy rasterizer → null framebuffer; recorded harness law) · galadriel pixel-benchmarks vs genre peers (D3 hero-fraction escalation path named) · Matt live-play rulings (Camera B′ was ruled in this loop, 2026-07-07). Verdicts feed BACK to G1–G6.
- **State:** **LIVE** — harness exists; capture hold LIFTED (all captures fire under B′ dist 20).

## G8 · Demo build & ship — **GAP (the end state)**
- **Does:** assemble the One-Realm MVP: Binding-Rite-LITE assignment beat → three-beat floors (Temple 1 → Biome → Temple 2 → Escape, fodder-only escape horde) → hand-in reaction line → end-card; wishlist gates.
- **Gate:** **GATE1** — `surface-ledger.md` all-rows-✓ gates *assembly-from-emitted-content* (Matt: *"Once I agree on all surfaces… then we can proceed with the demo in full view"*); presentation-layer B-row work is UNGATED and proceeds now.
- **State:** **GAP** — the product this pipeline exists to emit. Ops note at store setup: Steam AI-generated-content disclosure (wording = future Matt call).

## Gaps at a glance

| Stage | Gap | Owner | Tracker home |
|---|---|---|---|
| G1 | Lane B unproven — footsoldier smoke test → plague-doctor pilot (go/no-go) | drax + star-lord (vendor APIs) + galadriel (judgment) | ensemble spec §10; KR sequences |
| G2 | Warp profiles + per-profile retarget validation | drax | ensemble spec §2/§8 |
| G3 | Skinned-garment weight transfer (pilot crux) · band-ladder StyleProfiles | drax | ensemble spec §4.2/§5 |
| G4 | Ensemble §8 checks (automated + Judge boards) | galadriel + drax | game tracker A3 twin |
| G5 | Ensemble registry + packet schema build | drax + elrond | ensemble spec §7 |
| G6 | First authored floor (B2) → camera ratification (B1) · casting director (post-bundle-v2) · Binding-Rite-LITE (B5) | drax | game tracker PART B |
| G8 | GATE1 (surface-ledger all-✓) → demo assembly | Matt + all seams | `surface-ledger.md` |
| G3/loot | `power_to_band` curve (LAW 6 integer) | loot-spec owners | annex §13.3 flag |

**Signed:** gandalf, 2026-07-10. The mannequin is the loom, the ensembles are the cloth, and the camera is the only judge that matters.
