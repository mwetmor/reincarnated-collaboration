# Pushback / Ruling — Pixel-VFX-into-Godot-3D conflicts with the LOCKED register

**Author:** gandalf (design steward). **Date:** 2026-06-17. **Disposition:** PUSH BACK — route the decision to Matt; recommend the 3D-native redirect.
**Trigger:** Matt (prompted by a Gemini consult) surfaced the demo's purchased VFX catalogue at `/Users/admin/Games/reincarnated-demo/public/assets` + a Gemini spec for routing 2D flipbook VFX through Godot 4's 3D pipeline (billboard + 2.5D-skew + flipbook particle-anim), as a candidate to replace the Round-1 Synty-mesh spell.
**Parent run:** `2026-06-17-spell-vfx-runtogreen-log.md`.

---

## 1. What I inspected (Discipline #10 — not taking the claim on faith)

- The catalogue is the **demo's PIXEL-ART substrate**: ~159k PNGs / 1.9 GB — craftpix pixel tilesets/monsters, 10 elemental pixel heroes (`chierit`/`characters`), pixel monsters, and the VFX sets (`pimen` full-element spell FX, `CreativeKind`, `Holy_Spell_Effects`, `Impact FX Pack`, `Deathbringer`, `Elementals_bundle`).
- **The catalogue's own metadata classifies them:** pimen `metadata.json` → `"derived_register": "hand-drawn-pixel"`.
- **My eye confirms:** Holy "Spell 1" = thin yellow pixel lightning on a **white (un-keyed) background**; Impact FX = a crisp pixel burst-ring ~100px/frame; pimen Fire = a 64px hand-drawn fire. Resolutions 32–160 px/frame, hard pixel edges. Genuinely good — **for a 2D pixel game.**

## 2. The conflict — this reverses a LOCKED, Matt-authorized decision

`canonical/story/style-register.md` is **CURRENT / load-bearing**:
- **Register PIVOTED 2026-06-14 (Matt, Pattern-B with gandalf)** to **3D in Godot through a fixed 2.5D camera**; sub-fork **A (bounded stylized-low-poly-3D / Synty) LOCKED 2026-06-15** at composite **4.50/5**, extended to **5.00/5** on real Synty content.
- **The 2D-pixel HD-2D lock (Candidate B, 2026-05-15) is SUPERSEDED.** The 2D VFX catalogue is retained ONLY as **pivot-insurance** (scored-not-filtered), explicitly "no longer the default consumption filter."
- **The locked VFX strategy is "S-tier `GPUParticles3D` VFX juice + dramatic GI lighting."** The evidence that LOCKED the register was a body-anchored **`FX_Fire_Large_01` particle bloom → VFX-presence 5/5 (HLF peak 14.4%, 9.6× over the 1.5% threshold).**

**Therefore:** dropping `hand-drawn-pixel` flipbooks into the smooth-Synty-3D descent would (a) reverse the locked register, and (b) downgrade a **3D-native VFX strategy that already scored 5/5** to a register the project deliberately retired. The player-experience consequence is a **style-register collision** — a 64px hard-pixel fireball billboard in a smooth 3D polygon dungeon reads as *two games stapled together.* This is the exact design-coherence failure the register lock exists to prevent.

## 3. Gemini's technique is sound — but mis-sourced

Flipbook-billboards-in-a-3D-world IS a real PoE / Diablo-4 technique, and Gemini's Phase 1/2/3 (additive/HDR material, proximity-fade, 2.5D vertex-skew for ground decals, flipbook particle-anim) is competent Godot engineering. **But PoE/Diablo flipbooks are smooth, high-res, HDR-rendered** sheets authored to composite into an HD 3D world. The technique does NOT rescue a **pixel-art source** — it would faithfully composite pixels into 3D, and the pixels are the collision. Right method, wrong substrate.

## 4. The correct instinct underneath — honored, redirected

Matt's instinct is RIGHT: the Round-1 spell read soft, and we DO have better VFX leverage. But the soft beat was specifically the **geometric Synty MESH** travel-bolt (`FX_Cone`/`FX_Tower` shapes) — and the register lock already names the fix: **lean OUT of geometric low-poly mesh shapes, lean INTO S-tier `GPUParticles3D` particle juice** (the additive-emissive bloom + ember systems that scored VFX 5/5). The Gemini detour, properly adjudicated, **converges with where the slice-learning already pointed:** soft mesh-bolt → more particle juice (the locked, proven lever), NOT pixel flipbooks.

**Considered + rejected:** post-processing the pixel VFX (bloom/upscale/smooth) to fake current-register — worst-of-both (loses pixel charm, never gains smooth fidelity), fights the source, costly vs. the proven `GPUParticles3D` lever.

**Where the pixel catalogue DOES belong:** the 2D Pixi demo — it's excellent there, and it stays the pivot-insurance VFX library per the register doc. Not trashed; scoped to its fitting surface.

## 5. The decision Matt owns (escalation — above tripod authority)

Re-opening a locked Pattern-B **register** decision is a whole-art-direction call, not a VFX tweak — so it's Matt's, not the tripod's:

- **Recommended (proceed-now path):** keep the register locked; redirect Round-2 to the register's OWN proven lever — **S-tier `GPUParticles3D` particle-juice fire cast** (same Round-1 lifecycle architecture, particle-bloom skin instead of geometric-mesh skin). No canon change; honors the soft-mesh learning.
- **Only-if-Matt-intends-it path:** re-open the register toward a pixel-hybrid. This is NOT a VFX swap — pixel VFX only cohere if the WHOLE descent (characters, monsters, environment) is pixel-hybrid too, which discards the just-greened Synty-3D descent. A major pivot with a known, large cost. Flagged so the choice is intentional, not an accidental consequence of vacuum-advice that didn't know the lock existed.

**In-flight corroboration:** galadriel is scoring the Round-1 Synty-mesh slice now; her motion-numbers will quantify exactly how soft the geometric-mesh bolt is — direct evidence for the particle-juice redirect.

---

**Signed:** gandalf, 2026-06-17. The pixel-VFX catalogue is a superseded-register asset (excellent for the 2D demo, collision in the 3D descent). The locked register's own answer to "soft spell" is S-tier GPUParticles3D juice, already proven 5/5 — not pixel flipbooks. Recommend redirect Round-2 to particle-juice; flag register re-open as Matt's call with a large cost. Gemini's technique is correct; its source is mis-registered.
