# Reap. Die. Rise. — Character & Gear Ensemble Pipeline (Technical Spec)

> **STATUS:** CANONICAL — CURRENT. **Canonized 2026-07-10** (gandalf ultra-think ingest, Matt-directed) from Matt's mobile-session handoff `matt_notes_handoff_docs/reap-die-rise-ensemble-asset-pipeline.md` (text §§1–12 verbatim; the handoff original is bannered superseded-by-canon per the loot-draft/minigame-draft precedent). Production-pattern lineage: Blender→engine asset work driven by Claude-MCP recipe sessions + headless python poly-reduction batch — LAW 4 encodes it. **§13 is the gandalf reconciliation annex** (canonization-time cross-checks against the 2026-07-09 race well + camera/loot/certification canon). Consumed by `../current-to-end-state/pipeline-game.md` stages G1–G5 (the generated-asset lane).

**Audience:** the build team (Claude agent team on the Mac).
**Author:** Matt (mobile session). **Canonization + annex:** gandalf, 2026-07-10.
**Status:** design spec. Supersedes the gear-ART portions of `reap-die-rise-agnostic-loot-system.md` (see §11). Loot *mechanics* (operators, affixes, soul-binding, gleaning) are untouched — this doc is the ART layer and its mapping to stats.
**Core correction this doc encodes:** characters are NOT generated or authored as characters. A character = **mannequin + face + worn ensemble**. Head, chest, and legs are always covered, so only gear is ever visible (plus skin at deliberate gaps). The identity unit is the **themed ensemble**; the asset unit is the **piece**. There is no whole-character generation lane, no per-character rigging, no 400-character problem.

---

## 1. Doctrine (non-negotiable)

**LAW 1 — One mannequin, one rig, forever.** The Synty base body is the canonical mannequin on the canonical skeleton. It is rigged once. No body is ever rigged again. All animation retargets to this rig once.

**LAW 2 — Pieces, not characters.** All generation produces gear pieces that mount to or skin onto the mannequin. AI never generates a rigged character.

**LAW 3 — Theme is locked at the image layer.** Ensemble cohesion is established in a single reference sheet image (frozen style-bible prompts — the trailer-proven workflow) BEFORE any 3D generation. 3D never invents theme; it realizes the sheet.

**LAW 4 — MCP authors recipes; scripts run production.** Interactive Claude+Blender MCP sessions exist only to develop and revise the recipe scripts. Batch production is headless `blender -b -P <script>.py`, one mesh at a time, orphan-purge between meshes (M2 memory), zero tokens at runtime. All `.blend` templates under version control.

**LAW 5 — Nothing enters the registry uncertified.** Every piece and every ensemble passes §8 certification (Judge + automated checks) before the content engine may reference it.

**LAW 6 — Stats→art is one integer.** The only interface between the loot system and the art system is the per-slot **band (1–10)**. Art never reads item identity; loot never reads meshes.

---

## 2. The Mannequin

- **Body:** Synty base body mesh (male/female variants as needed), canonical skeleton, existing animation library retargeted once.
- **Face:** the Synty modular face pack (owned). Faces are a mannequin parameter, not a gear slot.
- **Skin:** skin tone is a palette parameter on the mannequin material. Mannequin skin renders wherever gear coverage gaps are deliberate ("naked/mannequin-skin" pieces show the character through the gear).
- **Warp profiles:** per-kit proportion warps (gaunt / hulking / hunched / towering / etc.) as bone-scale presets applied to the canonical rig. Worn gear follows automatically. Warps constrained to tested bands; §8 includes retarget validation per warp profile.

---

## 3. Slot Architecture

### 3.1 Banded per-kit slots (the ensemble; 2 meshes each → 10 assets per kit)
| Slot | Class (typical) | Notes |
|---|---|---|
| HEAD | rigid | helmet/mask/crown — highest identity weight |
| SHOULDERS | rigid | pauldrons/mantles — silhouette multiplier |
| CHEST | skinned | torso garment — always covered |
| LEGS | skinned | pants/skirt/robe-lower — always covered |
| WEAPON | rigid | the soul weapon's manifestation for this kit/body |

### 3.2 Pooled faction slots (shared vocabulary, not per-kit)
Hands/gloves, boots, belts, back attachments, accessories/trinkets. Pooled within faction/element families; selected by theme brief; palette-snapped per kit. These add texture without multiplying the per-kit asset bill.

### 3.3 Coverage & seam conventions
- Head, chest, legs are ALWAYS equipped (mannequin never reads as undressed).
- Seam design conventions are mandatory in theme briefs: helmet↔chest resolved by gorget/hood/collar; glove↔sleeve by cuff overlap; chest↔legs by belt/waist sash. §8 includes a seam check.

---

## 4. Piece Classes

### 4.1 Rigid mounts (~60–70% of pieces)
Helmets, masks, shoulders, bracers, belts, back totems, weapons. Single-bone attachments via the established `BoneAttachment3D` workflow. No skinning. Most reduction-forgiving class; batch at will.

### 4.2 Skinned garments (chest, legs, robes, coats)
Generated FITTED to the mannequin's T-pose, then weighted by **weight transfer from the mannequin body mesh** — deterministic Blender recipe:
1. Data Transfer (vertex groups, nearest-face-interpolated) from mannequin body → garment.
2. Limit total influences (4), normalize, one smooth pass.
3. Validate on test poses: walk mid-stride, attack apex, cast, crouch/jump extremes.
4. Auto-flag vertices exceeding deformation error threshold → agent fix-pass or reject.
Works because garments conform to the body they were generated on. This is the same mechanism modular packs use internally.

---

## 5. The Band Ladder (stats → art)

### 5.1 Structure: 10 bands = 2 mesh tiers × 5 treatment steps
- **BASE mesh** serves bands 1–5; **ORNATE mesh** serves bands 6–10.
- **Treatment steps (1–5 within each mesh)** are StyleProfile shader presets, escalating on fixed axes: palette richness/saturation → wear/cleanliness → trim/accent → emissive intensity → (top bands) glow/FX particles. Band 10 = ornate mesh at full treatment.
- Per kit: 5 slots × 2 meshes = **10 authored assets**; the shader ladder supplies the other half of the ten steps free.

### 5.2 Banding is PER-SLOT (decision)
Each slot's band derives from the realized (post-gleaning) power of the soul gear equipped in that slot. Consequences (intended): every meaningful drop visibly upgrades a piece of you; mixed states are information (band-9 crown over band-4 rags reads your build honestly). Cross-band cohesion is a design rule (each kit's ladder lives in one palette family with escalating ornament) and a certification check.

### 5.3 Mapping function
```
band(slot)        = power_to_band(realized_power(equipped[slot]))   # 1..10; curve owned by loot system
mesh(kit, slot)   = band <= 5 ? pieces[kit][slot].base : pieces[kit][slot].ornate
treatment(band)   = ((band - 1) % 5) + 1                            # 1..5 shader preset
render(kit, slot) = mesh + StyleProfile(kit.palette, treatment)
```
`power_to_band` (percentile bands over the power curve) is a loot-system tuning knob; this pipeline only consumes the integer.

### 5.4 Enemies wear the ladder
Enemy tier → band assignment in character packets: trash 1–3, elites 4–7, bosses 8–10. Bands 1–8 live forever on the enemy population; **band is legible threat telegraphing at ARPG camera distance** (certified in §8). Reincarnation targets render at their tier's band until worn by the player's soul.

### 5.5 Above the ladder
Marquee named uniques remain bespoke silhouette-breaking pieces (Recipe A hero lane) that sit visually ABOVE band 10 — the chase stays special in an endgame of 9–10s. Horizontal endgame variety = the 400 kit themes, not the band axis.

### 5.6 Fiction (one line, for the story bible later)
The band is the soul's power made visible on whatever flesh it wears — the same body, worn by a mightier soul, blazes.

---

## 6. Generation Chain (stages)

**Stage 0 — Style bible extraction (one-time, do first).** Pull the exact prompt blocks from the trailer generation history that produced Synty-cohesive output. Freeze as `style_bible/character_block.md` (+ the environment block for the separate environment doc). Version it; pin generation-vendor model versions; keep the reference-anchor image set immutable.

**Stage 1 — Theme brief.** Content engine turns kit tags (element, faction, archetype, silhouette class) into a theme brief (LLM call, same constraint discipline as loot naming: brief must specify seam conventions, palette family, identity motifs).

**Stage 2 — Ensemble sheet.** One image: the full character in-theme, style-bible prefix mandatory. The sheet IS the theme contract.

**Stage 3 — Per-piece refs.** Isolated per-slot images derived from the sheet (3/4 view, neutral background, T-pose-compatible orientation, unarmed for garments).

**Stage 4 — Image→3D.** Vendor slot (Tripo / 3D AI Studio API; pinned versions; async polling). High-quality mode; Smart-Poly only for simple rigid props.

**Stage 5 — Reduce + Syntyfy (the frozen Blender recipe).**
- High-ratio reduction: planar decimate + limited dissolve (rigid pieces); low-target quad remesh or rebuild-over-reference for hero/complex pieces.
- Shade flat / auto-smooth per style bible.
- Strip PBR maps; bake to vertex colors or gradient atlas; palette-snap to the kit's StyleProfile palette.
- **Chunkify pass** (as needed): proportion exaggeration + detail cull to match Synty bulk.
- Emit LOD chain (LOD0/1/2 descending targets) — mandatory for horde tiers on M2.

**Stage 6 — Mount or skin.** Rigid → attachment socket metadata for `BoneAttachment3D`. Skinned → §4.2 weight-transfer recipe.

**Stage 7 — Band treatments.** Register base/ornate meshes; bind the 5 treatment presets (shader profiles) per the kit palette.

**Stage 8 — Certify (§8) → registry.** glTF 2.0 export with Godot import presets. Only certified ensembles are referenceable by character packets.

**Starting mesh budgets (tune via profiling):** rigid mounts 150–800 tris; skinned garments 500–2,000; assembled character LOD0 ≤ ~8k; draw calls minimized via per-ensemble atlas merge (script stage).

---

## 7. Ensemble Packet Schema

```json
{
  "packet_type": "ensemble",
  "kit_ref": "...",
  "theme_brief": "...",
  "sheet_ref": "img://...",
  "palette_profile": "styleprofile://...",
  "warp_profile": "warp://gaunt_02",
  "pieces": [
    {
      "slot": "HEAD|SHOULDERS|CHEST|LEGS|WEAPON",
      "mount_type": "rigid|skinned",
      "mesh_base": "gltf://...",
      "mesh_ornate": "gltf://...",
      "lods": ["...","...","..."],
      "attach": { "bone": "...", "offset": {} },
      "treatments": ["tp1","tp2","tp3","tp4","tp5"]
    }
  ],
  "pooled_refs": { "hands": "...", "boots": "...", "belt": "...", "back": "..." },
  "enemy_band_default": 3,
  "fitness_report": { "certified": false, "checks": {} }
}
```

---

## 8. Certification (Judge + automated)

Automated: tri/material/texture budgets per class; LOD presence; skin-weight validation poses pass (no flagged vertices); seam gap scan at rest + test poses; warp-profile retarget validation.

Judge (pairwise, per established critic-in-the-loop protocol — decomposed audit passes, anchor boards, swap-consistency):
1. **Ensemble cohesion** — pieces read as one theme (vs. the sheet).
2. **Style match** — vs. Synty/trailer anchor board (the piece belongs in this game).
3. **Cross-kit distinctiveness** — silhouette+palette distinguishable from nearest-neighbor kits at combat camera distance.
4. **At-distance readability** — kit identity (and therefore threat) reads at ARPG range before abilities fire.
5. **Band monotonicity** — for each slot ladder, band N+1 reads strictly more powerful than band N at combat camera (sorted-sequence pairwise audit). A ladder that doesn't sort visually fails.
6. **Cross-band mix cohesion** — randomized mixed-band ensembles still read as one character (palette-family rule holding).

---

## 9. Compression Policy & Production Math

- **Distinctiveness budget:** the 60–100 wearable champion/boss kits get fully unique 5-slot ensembles. Trash tiers ship as ensemble-family variants (shared base garments within faction vocabulary; unique HEAD/WEAPON; palette + warp deltas) — reads as coherent worldbuilding, matches genre norms.
- **Pooled slots** (§3.2) never multiply per kit.
- **Rarity/band treatments** multiply looks per mesh free.
- **Realistic bill:** ~1,500–2,500 generated pieces expresses 400 themed kits (ceiling 4,000 = 400 × 10 only if every kit were fully unique — it should not be).
- **Cost shape:** generation dollars are trivial; the bottleneck is per-piece QC. Pilot must measure **pass rate**; ≥~80% clean with agent fix-pass on the remainder ⇒ full production is batch-weeks.

---

## 10. The Plague-Doctor Pilot (go/no-go for the whole lane)

**Step 0 — Footsoldier smoke test (pre-pilot, ~hours).** Run the existing trailer footsoldier reference image through image→3D → Stage 5. Question: does the mesh preserve what the image promised (chunk, facets, palette)? This validates the only unproven span (image→mesh fidelity) at zero new asset-design cost.

**Step 1 — The ensemble.** Theme brief → ensemble sheet → all 5 slots. CHEST at BOTH meshes (base + ornate) so §8 check 5 gets exercised; other slots one mesh each is acceptable for the pilot.

**Step 2 — Assembly.** Mount/skin on the mannequin + Synty face + one warp profile. Apply treatments at bands 2, 5, 7, 10.

**Step 3 — Animation truth.** Walk / attack / cast / crouch on the retargeted library.

**Step 4 — Judgment.** In Godot at combat camera: side-by-side vs. one untouched Synty character and one trailer frame. Full §8 pass.

**Pass/fail:**
- PASS = style match ≥ anchor threshold; chest deforms cleanly through attack apex (no flagged vertices); band 10 vs band 2 monotonicity obvious at distance; total labor ≤ ~1 day/ensemble at pilot pace.
- **The crux is the skinned chest** — weight-transfer quality on generated garment topology is the single link with no prior proof. If it fails: fallback = Synty garment meshes for CHEST/LEGS (retextured/palette-snapped per kit) + generated rigid pieces for identity — the hybrid remains fully viable and only shrinks the skinned lane, not the system.

**Outcome routing:** PASS → write the batch scripts, begin the 60–100 champion ensembles. FAIL on chest only → hybrid fallback above. FAIL on style fidelity → escalate chunkify pass / stylized-ref strategy before any scale decision.

---

## 11. Superseded & Interfaces (do not regress)

- SUPERSEDED: agnostic-loot doc's "pooled gear art ≈ 30 models per slot globally + rarity tint" → replaced by **per-kit themed ensembles + band ladder** (this doc). Loot MECHANICS in that doc stand unchanged.
- "Soul weapons/gear manifest per-body" now has its concrete art answer: carried soul gear renders in the current body's ensemble vocabulary at the computed band (WEAPON slot = that kit's manifestation meshes).
- Gleaning/pickup color (loot doc §3) is unchanged and distinct: pickup color = gleanable rarity; **band = realized power of equipped gear** per slot.
- Character packets (story/AI layers) reference `ensemble` packets by `kit_ref`; enemy tiers set `enemy_band_default`.

## 12. Out of Scope / Open Decisions

- Non-humanoid kits (beasts, wraiths) — separate smaller lane on Synty creature bases; does not ride the mannequin rail.
- Environment/room pipeline — separate doc (style-bible environment block extraction shares Stage 0).
- Animation library sourcing/expansion (Mixamo/Synty retarget) — solved-by-retarget, catalog TBD.
- Exact `power_to_band` curve — loot-system owned.
- Ops note: Steam requires AI-generated-content disclosure at store setup (checkbox; not a blocker — decide wording later).

---

## 13. Reconciliation annex (gandalf, canonization 2026-07-10 — cross-checks against ratified canon)

Ultra-think verdict on ingest: **SOUND — the spec slots into the game pipeline as the generated-asset lane** (`pipeline-game.md` Lane B, stages G1–G5). Six reconciliations, none of which reopen a Matt ruling; #1 is *forced* by a newer ruling and is the only wording amendment:

**13.1 LAW 1 generalizes per race-frame (FORCED by the 2026-07-09 race-well ruling — newer canon wins the conflict point).** LAW 1's letter ("no body is ever rigged again") predates the ratified bestiary race well (`../reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md`), which admits **Goblin as a REFRAME race** — own skeleton, own BoneMap, own locomotion set (Q7 artifacts exist; drax retargets it now). The consistent reading, and the one this canon adopts: **one mannequin PER ADMITTED RACE-FRAME, rigged once, forever.** v1 = TWO mannequins: the human-frame mannequin (serves human/orc/elf/dwarf — all reskin-tier, bone-dump-verified standard skeletons) + the goblin-frame mannequin (already paid). The LAW's spirit — rig once, never per-character, retarget the library once per frame — is precisely the race well's admission criterion; they are the same law at two grains. Reframe admission stays a **curation act** (well CLOSED), so mannequin count stays single-digit forever. Warp profiles (§2) compose, not conflict: race silhouette is MESH-baked (Q17 finding — Big_Ork/Dwarf bulk lives in the mesh, skeleton standard); warps are **kit-level** bone-scale variation *within* a frame. Two complementary silhouette channels.

**13.2 Scale vocabulary: §5.5/§9's "400 themed kits" and "60–100 champion ensembles" are LAUNCH-scope numbers.** The demo denominator is Matt-curated **~20 kits from the 31-row roster of record** (serial tracker PART F), ONE realm, ONE-PEOPLE family, 4 orders rotating (run-composition model, 2026-07-06/08 rulings). Demo-scale asset bill: ~20 champion-grade ensembles + ONE faction family's trash-variant vocabulary — the §9 compression policy applies identically at both scales. The pipeline doc stamps demo-scale; launch numbers are the growth path, not the gate.

**13.3 Band ladder ↔ the canonized loot pair (interface flag, no rewrite here).** §11's supersession targets the *handoff* loot draft's pooled-art paragraph. The canonized pair (`../reap-die-rise-story/agnostic-loot-story-spec.md` + `../reap-die-rise-engine/agnostic-loot-engine-spec.md`, 2026-07-07) carries loot MECHANICS — unaffected. What the pair now OWES this spec: the **`power_to_band` curve** (LAW 6's one integer; loot-owned tuning knob, percentile bands over realized power). Flag registered for the loot-spec owners' next touch; until then the interface is this doc's §5.3 signature. Gleaning-color vs band distinction (§11) already composes with the ruled gleaning/cementing chain (story tracker 2026-07-07).

**13.4 Stage 0 style bible IS game-tracker B4's concrete half.** B4 ("style-register application to the game layer," MVP-CRITICAL) asked how `../reap-die-rise-story/style-register.md` binds asset choices. For GENERATED assets the answer is now mechanical: the frozen style-bible prompt blocks (extracted from the trailer generation history — the trailer MP4s live in `matt_notes_handoff_docs/`) ARE the register made executable at the image layer; the §8 style-match check (anchor board) is its enforcement. B4's remaining half (register binding on *library* Synty picks) stays open on the tracker.

**13.5 §8 certification lands in galadriel's seam and extends the ruled three-gate method.** Game-tracker A3 (G1 engine-truth → G2 register-CV → G3 Matt) is the ruled floor-authoring gate chain; §8 is its ASSET-grain twin — automated checks (drax scripts: budgets, LODs, skin-weight poses, seam scan, warp retarget) + Judge passes (galadriel: cohesion, style match, cross-kit distinctiveness, at-distance readability, band monotonicity, mix cohesion) at **Camera B′ 20 m** (the ruled register — readability checks 4–5 certify at the actual gameplay camera; composes with E10 §7's telegraph channels: band = vertical threat, race×register = horizontal identity, affix = behavioral). Seam map for KR sequencing: **drax** Blender-MCP recipes + headless batch + mounts/skinning · **star-lord** image-gen + image→3D vendor APIs (pinned versions, async polling — his external-service discipline) · **galadriel** Judge + anchor boards · **elrond** ensemble-packet registry/schema adjacency · **gamora/rocket** untouched (LAW 6 keeps stats↔art at one integer).

**13.6 Pilot sequencing (named fork, KR/Matt tempo call — no rescope here).** The plague-doctor pilot (§10) is the go/no-go for **Lane B** (generated pieces), not for the demo as such: the demo can ride Lane A (Synty register packs + palette work) if the pilot slips — Lane B buys the per-kit identity ceiling and the launch-scale 400-theme ambition. The pilot is cheap (footsoldier smoke test ~hours; full pilot ≤ ~1 day/ensemble pace) and its crux (skinned-chest weight transfer) has a fully-viable hybrid fallback (§10), so the steward lean is: fire the smoke test EARLY — it de-risks the only unproven span at near-zero cost and its verdict shapes demo dressing strategy before floor-authoring locks visual vocabulary. Non-humanoid creature lane (§12) = the race well's mob-only kinds (skeleton/zombie/werewolf frames) — separate rail, already named there.

**Signed:** gandalf, 2026-07-10 (canonization annex). The mannequin is the loom; the ensembles are the cloth.
