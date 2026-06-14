# Godot pivot — modular-asset strategy + dual-machine workflow (recognition)

**Type:** recognition record (gandalf seam) — architectural commitments DEFERRED pending legolas/galadriel empirical grounding + the drax Godot spike. Captured while fresh per recognition→validate→commit.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt Pattern-B dialogue 2026-06-14 (style-register pivot session, continued).
**Companion docs:**
- `canonical/story/style-register.md` § "Register pivot" — the engine/register pivot this asset-strategy serves.
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the non-humanoid body-plan discipline that makes non-humanoid forms the long-pole.
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — the precedent pattern (LLM composes from a curated substrate; does not generate raw assets).
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — the Unreal-era asset plan whose SHAPE this preserves (engine swapped, strategy held constant).

---

## 0. TL;DR — Recognition Record (commitments deferred per § 6 empirical gates)

Matt's modular-pack decomposition resolves most of the register-feasibility tension by **rhyming with the engine's established substrate-honest spine.** The form-library's "infinite" becomes **combinatorial composition from a curated modular-parts substrate + LLM-generates-the-recipe** (part selection / palette / naming / lore / stats), NOT LLM-generates-raw-mesh. Player-character = a purchased modular character-CREATOR pack (guaranteed register-2 quality + known-good shared rig). The remaining pool splits: humanoid NPCs/summons = modular-pack-solved; **NON-humanoid monsters (doc-37 body-plans) = the real long-pole.** Per-season Matt+son human-modular-assembly is a **legitimate primary-or-fallback** (genre-proven; caps the volume problem), not a defeat. This **consciously rescopes the infinite-forms pillar** — eyes-open, not silent drift. Dual-machine workflow (low-Mac-edit / high-PC-validate) endorsed; mechanism below.

## 1. The modular-pack decomposition (Matt 2026-06-14)

- **Player character** → built from a PURCHASED modular character-creator pack (swappable parts on a shared skeleton). Combinatorial appearance variety + a known-good rig, authored to register-2.
- **Remaining pool** (humanoid NPCs, summoned humanoids, monsters) → open question: can it hit a *"similar"* hand-painted look?
  - **Ideal:** yes, via [register-2-capable modular monster/creature packs + stylized Godot shaders + reserve gen].
  - **Fallback (acceptable):** Matt + son assemble these **once per season** via modular monster/NPC/summoned-combatant kits (human-in-the-loop modular assembly).

## 2. Why it rhymes with the spine (substrate-honest)

This is the SAME pattern as the weapon-substrate work: the LLM **composes from a bounded, curated substrate** (modular parts) rather than generating unbounded raw assets. The LLM's job shifts from "generate the mesh" (which the substrate — gen tooling — cannot reliably deliver at register-2 + clean topology) to "generate the recipe" (which it does well). Substrate-honest: match the design target to what the substrate actually delivers. Matt's instinct is consistent with how the rest of the engine already thinks.

**Risk-isolation virtue (Matt's "keep the plan similar to Unreal"):** we are already taking on engine-risk (Unreal→Godot). Holding the asset-strategy SHAPE constant (modular-pack-for-player + reserve-gen-for-differentiating, per `asset-pipeline-meshy-swap`) and swapping only the engine isolates ONE variable. Changing engine + pipeline + strategy simultaneously would confound the spike. Good engineering discipline: change one thing.

## 3. The humanoid / non-humanoid split (the real long-pole)

A modular HUMANOID creator pack solves player + humanoid NPCs + humanoid summons cleanly. But doc-37's **non-humanoid body-plans (slime, swarm, dragonling, cloud-being, serpentine, quadruped)** are NOT served by a humanoid kit — they need separate modular monster/creature kits (which exist; legolas is surveying) OR the gen path OR per-season human assembly. **Non-humanoid is where the form-bias discipline AND the register-feasibility question both bite hardest** — the commission + spike must treat it as the hard case, not an afterthought. Register-COHERENCE across the player-pack and the monster-pack is load-bearing (a Torchlight-hand-painted player beside flat-Synty monsters clashes in-frame — the same style-coherence problem that bit the 2D register).

## 4. Conscious pillar-rescope (Discipline #13 — the HEALTHY version)

The "infinite LLM-generated forms" pillar is being rescoped from *LLM-generates-raw-infinite-meshes* → *LLM-composes-forms-from-a-rich-modular-substrate, the roster growing per season*. This is **conscious rescoping, not drift** — named here so it is eyes-open. Differentiation re-anchors on **LLM-composition + per-form lore/naming/stats**, not on raw-mesh-generation. This is **genre-proven**: commercial gacha rosters (Genshin, etc.) are finite, human-authored, and grow over time — the per-season-curated-modular-roster is arguably MORE commercially-aligned than the infinite-gen ideal, which becomes a long-horizon stretch rather than a v1 dependency. The spirit-swap differentiation (load-bearing per design-intent memory) survives intact — it never required raw-infinite-gen, only a rich form-pool the player swaps through.

## 5. Dual-machine workflow architecture (Matt 2026-06-14)

Matt wants to do MOST Godot work on the Mac in a super-low-tuned instance, reserving the PC for VFX/fog/high-graphics validation — to avoid PC-switching and cut dev-cycle time. Endorsed; Gemini's instinct is sound (Godot's editor is lightweight — feasible on 8GB M2, unlike Unreal). Mechanism:

- **ONE Godot project, git-synced** between Mac and PC checkouts. The same text-scene property (`.tscn`/`.gd`/`.tres`) that made us pick Godot makes this trivial — diff/merge cleanly. No project duplication.
- **Per-machine render-quality presets:** a `mac-dev-low` preset (Compatibility/Mobile renderer, reduced viewport scale, shadows/particles off) + a `pc-validate-high` preset (full VFX/fog/lighting), toggled by a git-ignored local config or env var, so the same scene renders cheap on Mac and rich on PC.
- **Loop:** build + script + lay out on Mac at low settings (fast) → commit/push → PC pulls → run at high settings to validate VFX/fog.
- **"SSH effortlessly with minimal Matt checks" — two distinct things:** (a) AGENTS driving PC Godot (headless builds/exports/scene-runs) → SSH + `godot --headless`, already low-friction (SSH-key auth + standing wave-close push); (b) MATT seeing high-graphics output without walking to the PC → SSH won't show pixels; use **display-streaming** (Sunshine on PC + Moonlight on Mac — gamer-grade, low-latency, free; or Parsec). That is the "effortless" path: stay at the Mac, PC renders, pixels stream back.
- **Fold a workflow-verification item into the spike:** confirm the low-Mac-edit → high-PC-validate loop (git-sync + per-machine presets + display-stream) works on the real hardware before committing the whole pipeline to it. Cheap to verify, expensive to discover broken later.

## 6. Empirical gates (what validates before canonical commit)

- **legolas** (LAUNCHED 2026-06-14): register-2-capable Godot modular packs (humanoid + monster) exist, ship-licensable, shared-rig-compatible, register-coherent across player+monster; AND/OR gen can hit register-2 + clean retargetable topology.
- **galadriel** (LAUNCHED 2026-06-14): the register-2 target + texture-richness metric + premium-feel decomposition (texture vs geometry vs lighting vs VFX).
- **drax Godot spike:** player-pack + non-humanoid-similar-look + per-season-assembly fallback + the dual-machine workflow loop, all proven on real hardware. Spike starts against the galadriel target.
- THEN: canonical amendment to `style-register.md` (corrected register taxonomy — register-2 target, not the coarse A/B-low-poly-vs-fuller framing) + a form-library asset-architecture doc.

## 7. Disposition / routing

- legolas + galadriel commissions: **LAUNCHED** 2026-06-14 (background). drax spike brief authored AFTER they return (folds findings + galadriel target).
- **KR:** cascade sequencing (doc 38 § D1 Unreal supersession; Meshy→Godot demotion; mantis/PC-UE-seam raison d'être; drax spike). Still owes the physical-pool DEFER relay so cutover Stage 2 fires.
- **jack-ryan:** decisions-log entry for the register+engine overturn.
- Canonical `style-register.md` NOT re-carved on the corrected register taxonomy until the gates resolve (consistent with the recognition→validate→commit hold stated to Matt).

---

**Signed:** gandalf, 2026-06-14
**For:** the Godot-pivot asset-strategy + dual-machine-workflow recognition — modular-pack composition rhymes with the substrate-honest spine (LLM composes recipes from curated parts, not raw meshes); player solved by a purchased creator pack, non-humanoid monsters are the long-pole, per-season human-modular-assembly is a genre-proven legitimate fallback; the infinite-forms pillar is consciously (not silently) rescoped to combinatorial-from-substrate; and the low-Mac-edit/high-PC-validate loop is one git-synced project + per-machine render-presets + display-streaming.
