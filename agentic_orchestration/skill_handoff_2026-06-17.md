# Skill Handoff — 2026-06-17

**Author:** knight-rider (autonomous hive-mode session)
**Matt directive driving the session:** "uncover how to complete the download crawl and then fire the crawl process" → escalated to "download all assets from the 157 folders that could possibly be used and get gandalf all of his info. You are the hive mind orchestrator."

---

## Headline: Synty gear-substrate acquisition workstream — discharged end-to-end

The full chain (crawl → download → catalogue → verify → gandalf design ruling) ran autonomously to completion. Matt's directive is met: every usable asset is downloaded, the substrate is catalogued + path-verified, and gandalf has both his info AND has ruled on it.

### What shipped

| Stage | Owner | State | Artifact |
|---|---|---|---|
| Crawl method cracked (Sky Pilot folder-tree + required browser UA header) | knight-rider | ✅ committed | `research/catalogue/synty-recon-2026-06-16/CRAWL-METHOD-CRACKED-2026-06-17.md` |
| Full enumeration: 157 collections / 620 files / ~51 GB all variants | knight-rider | ✅ committed | `full-fbx-variant-manifest.jsonl` + `collections-157.json` |
| FBX corpus pull: **136/136 zips, 8.8 GB, all `unzip -t` verified, 0 failures** | knight-rider | ✅ on disk | `~/Games/synty-corpus/fbx/` |
| Slice-verification (UV-separability #2 + accent-rig sockets #3) | galadriel | ✅ **both VERIFIED YES**, committed `8da65d1` | `slice-verification-2026-06-17.md` |
| Catalogue DB: 136 packs / 53,626 mesh assets / path-index PASS (0 misses) | elrond | ✅ committed `5197cc0` (script + MIGRATION; DB gitignored/regenerable) | `research/curated/synty_catalogue.db` + `scripts/build_synty_catalogue_2026_06_17.py` |
| §7.6 StyleProfile output-shape ruling (gear-spec design seam) | gandalf | ✅ AUTHORED — ⚠️ **UNCOMMITTED (untracked)** | `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` |

### ⚠️ OPEN — flag for next session / gandalf

**`canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` is untracked.** Gandalf authored it (self-served off galadriel's slice-verification — fired the §7.6 ruling the moment the §4 empirical gate cleared) but it sits uncommitted. Gandalf owns `canonical/` — knight-rider did NOT commit it (out of seam). Gandalf was active in a parallel session (descent/lighting workstream — commits `9e1cee9`, `00540d6`) so likely commits it at his boundary. **If it's still untracked next session, prompt gandalf to commit it — it is load-bearing (unblocks rocket §7.2 / star-lord §7.3 / elrond §7.1 / drax §7.5).**

### The §7.6 ruling in one line (for downstream consumers)
StyleProfile `palette` carries a **per-region palette array that gracefully degrades to a single whole-tint entry** when the bound mesh exposes no per-region mask. One schema, two fill-densities, keyed by lane (additive-nullable pattern). `mode` is mesh-derived at bind time, not generator-chosen. `whole_tint` always present as L3 fallback.

### Catalogue key decisions (elrond)
- **Separate `synty_catalogue.db`**, NOT extending `catalogue.db` — the existing DB is a 2D-sprite style-rubric catalogue; this is a 3D-FBX mesh catalogue; schema overlap near-zero. Cross-link by `collection_id` string key. Rationale in MIGRATION v1.11.
- Galadriel's lane bifurcation folded in: `packs.recolor_scheme` (`per_region_mask` vs `whole_atlas_swap`); `textures.channel_region_map` carries the 5-zone RGB-corner scheme. **Consumer caveat:** for the armor-restyle lane, filter on `structural_class='modular'`, NOT `recolor_scheme` (only the modular pack's mask is character-relevant).
- All 136 packs default `NOT_INCORPORATED` (Matt's lapse-ledger stipulation); stamp path smoke-tested. `distinctiveness_score` NULL across all (galadriel's later seam).

---

## In-flight / queued

- **No-FBX variant pull** — 21 Unity `.unitypackage` packs (Knights/Vikings/Western/Kids/Battle Royale/Gang Warfare/etc. + INTERFACE HUDs) → `~/Games/synty-corpus/nonfbx/`. Running (~10/21 at handoff). Script: `~/Games/synty-corpus/download_nofbx.sh`. **Next:** when complete, extract meshes from the `.unitypackage` files (Mac-side) → elrond second `full` populate pass (script is idempotent, upsert-keyed on `(collection_id, download_id)` — clean re-run, no manual reconciliation).
- **Cloud backup of full corpus** (task #7) — pending; do post-pull, pre-subscription-lapse. Storage verdict settled: even all-variants ~51 GB fits the Pi 106 GB microSD (partition-onto-Mac contingency permanently moot). FBX staged Mac-local because Pi SMB share was unmounted at session time.
- **Per-zone semantic labels** (which mask zone = metal vs leather) — galadriel §7.4 hook; needs one Godot/Blender import render pass. Provisional in the manifest until then. NOT a schema gate (zone count of 5 is decision-grade); only label-to-zone binding awaits the render. No Blender/assimp installed on host — tooling gap to close before that render.
- **EULA confirmation** at syntystore.com/pages/licences-overview — Matt open item (incorporation_status ledger is the mechanism; default NOT_INCORPORATED honors the "must incorporate before lapse" stipulation).

## rocket §7.2 sequencing (carried per gandalf §4)
rocket's L2 restyle-leaf shader + accent-attachment build is **Tier-2-gated-on-manifest** — fires only after (a) gandalf §7.6 ruling [done] AND (b) the manifest design-owned half + elrond substrate slice land [done]. The gate is now satisfied; rocket §7.2 is eligible to be dispatched next cycle. Accent-attachment fires unconditionally (12 named sockets verified).
