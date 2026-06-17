# Sidekick Character Creator — Modularity Research
**Date:** 2026-06-16
**Mode:** B (catalogue recon — focused asset investigation)
**Commissioner:** legolas self-dispatch per task brief
**Sources:** syntystore.com product pages, Synty blog, Unity Asset Store listing (see source list)

---

## Pack manifest entry (raw)
- collection_id: 157753 / order_item_id: 311325427
- has_fbx_source: false
- all_downloads: icon PNG only (2.71 MB) — no FBX, Unity, Unreal, or Godot package listed in Matt's order record
- Interpretation: the "Character Creator" (collection_id 157753) is the TOOL entitlement, not a downloadable asset pack. The per-theme content packs (Elven Warriors, Fantasy Knights, etc.) are separate line items on the store and require individual purchase or All Access.

---

## Q1 — Modular vs baked

MODULAR. Sidekick is Synty's dedicated modular character assembly system. Parts mix and match across packs. The Creator Tool bakes a finalized character into a single optimized prefab (combined skinned mesh renderers) for runtime performance — but assembly is per-slot, not a single baked export from the start.

---

## Q2 — Slot granularity

Confirmed slot list from Starter Pack product page:

| Slot group | Slots |
|---|---|
| Head/face | head, hair, facial hair, eyebrows, eyes, ears, nose, teeth, tongue |
| Torso/limbs | torso, upper arms, lower arms, hands, hips, legs, feet |
| Attachments | head attachments, face attachments, back attachments, shoulder attachments, elbow attachments, knee attachments, hip attachments (front/back/left/right), wraps |

Total: ~22 discrete slot categories.

**Export format:**
- Unity: 2021.3+ package (URP + Built-in render pipelines)
- Unreal Engine: plugin files for UE 5.3–5.7 + content zip (5 of 17 packs have UE versions as of 2026-06-16)
- FBX export: possible via third-party Unity script (right-click hierarchy > Export to FBX), NOT a first-party built-in feature of the tool itself. Not engine-agnostic out of the box.
- **Unity-first.** The Creator Tool is Unity-only per Synty's own announcement. UE versions ship as standalone content packs, not tool-integrated.

---

## Q3 — Entitlement

- The Creator Tool (collection_id 157753) is available **exclusively with Synty's All Access Pass** (confirmed by Synty blog intro).
- Matt's order record shows only an icon PNG download — no asset package. This is consistent with the tool being a pass-gated entitlement that is accessed through the Synty Store interface, not a standalone downloadable.
- Individual content packs (e.g., Elven Warriors, Fantasy Knights) are $199.99 USD each; 17 Unity packs + 5 UE packs available. All show "Sold out" on the storefront as of crawl date — may be All Access only or temporarily unavailable for individual purchase.
- Free Starter Pack exists (Unity + UE) — usable for viability testing without additional spend.

**SyntyPass / All Access:** the Creator Tool requires it. Whether Matt's current subscription (which includes collection_id 157753) covers individual content packs independently is not determinable from public pages alone — flagged as hands-on-verification required.

---

## Q4 — POLYGON style compatibility

Confirmed compatible. Synty marketing states Sidekick themes are "designed to work consistently with Synty's POLYGON environments." Launch themes (Apocalyptic, Sci-Fi, Fantasy, Historical) map directly to POLYGON pack equivalents. Cross-mixing Sidekick characters with POLYGON weapons/enemies is the stated design intent.

Style register: same low-poly, flat-shaded, stylized-3d aesthetic as POLYGON. Not pixel-art; not hand-drawn. Geometry density is higher than POLYGON (modular swappable parts = more mesh complexity per character) but visual register matches.

---

## Flags for gandalf / downstream

1. **Unity-tool dependency.** The modular assembly workflow lives in the Unity Editor. Pixi.js consumption would require: (a) assembling a character in Unity, (b) baking to combined mesh, (c) exporting FBX via third-party script, (d) processing into sprite sheets. This is a longer pipeline than POLYGON's direct FBX → sprite-sheet path.
2. **UE packs exist but are standalone content, not tool-integrated.** If the project consumes via UE pipeline (Mantis seam), the UE packs give modular mesh files but not the Creator Tool's assembly interface.
3. **Matt's entitlement boundary unclear.** The order record (collection_id 157753) appears to be the tool-access token, not individual content packs. Whether All Access covers all 17 content packs requires store login verification — not determinable from public pages.
4. **Bake-to-single-mesh is the runtime form.** Decomposition = `decomposed` at assembly time; `monolithic` after bake. For pixi.js wiring the baked form would behave identically to POLYGON FBX — fixed silhouette per character preset.

---

## Source list

- https://syntystore.com/products/sidekick-character-creator (product page, accessed 2026-06-16)
- https://syntystore.com/blogs/blog/introducing-sidekick-character-creator (announcement blog, accessed 2026-06-16)
- https://syntystore.com/collections/sidekick-character-packs (collection page, accessed 2026-06-16)
- https://syntystore.com/products/sidekick-modular-characters-starter-pack (starter pack detail, accessed 2026-06-16)
- https://curiouser-kate.itch.io/unity-script-synty-sidekick-multi-parts-in-one-character (third-party FBX export script reference)
- pack-manifest.jsonl (Matt's Synty order record, crawl date 2026-06-16)
