# Galadriel Reference Image Manifest

**Provenance authority:** Matt (mhwetmore@gmail.com).
**Curation authority:** galadriel (maintains this manifest; gandalf authored the seed DoE set).
**Source authority (DoE set):** All DoE images are Matt-captured from his personal play sessions of Dungeon of Exile. No fair-use sourcing question; Matt is the rights-holder of his own play-session captures for internal benchmarking. Non-commercial visual-language reference only; not redistributed; not embedded in any shipped product.
**Source authority (3D-stylized-ARPG set, 2026-06-14):** public-source Steam store-page imagery (screenshots + header capsules), pulled via the public Steam appdetails API. Fair-use justification: genre-comparison for non-commercial internal benchmarking. Per-image provenance (app ID, source URL pattern, publisher, capture date) recorded in the 2026-06-14 set table below per galadriel agent-definition § "Reference image sourcing rules" (public-source acceptable WITH provenance metadata recorded).

**Canonical reference status:**
- **DoE set (mobile-feel cluster)** — locked mobile-ARPG *gameplay-feel + HUD-density + town-service-surface* reference per `canonical/story/mobile-feel-target-doe-2026-05-17.md`. **Survives the 2026-06-14 register pivot** for the gameplay/HUD/feel dimensions it anchors (DoE is itself a stylized-3D ARPG; its combat-density and service-surface reads are register-agnostic). It is NOT the *visual-register* anchor for the post-pivot 3D-stylized look — that role is the 2026-06-14 set below.
- **3D-stylized-ARPG set (2026-06-14)** — the **visual-register anchor** for the post-pivot Godot-3D-2.5D-camera lock per `canonical/story/style-register.md` § "Register pivot." Establishes the register-2 (premium-stylized) target the Godot vertical-slice spike is measured against.

**Retired references (2026-06-14):** Octopath Traveler / Triangle Strategy (the 2D-pixel HD-2D-lock visual anchors) are **RETIRED as the visual-register reference** per `style-register.md` § "Register pivot" → Cascade item 6. They were never in this manifest as image files (they were named anchors in the superseded 2D-lock doc); recorded here as formally retired so the lineage is inspectable. The DoE captures are NOT retired (see above — they anchor feel/HUD, not register).

---

## Reference set 1 — DoE mobile-feel cluster — 2026-05-18 (feel/HUD anchor; survives pivot)

| File | State | Date captured | Resolution | Notes |
|---|---|---|---|---|
| `DOE-combat-whisper-rift-2-2026-05-17.png` | **Combat** — Whisper Rift 2 (EASY); mid-fight; HUD module top-left (minimap + objective + countdown + skull); telegraphed AOE rectangles visible; floating damage numbers (22, 15, -3); slow status applied to enemies; "55 killed" counter; bottom UI showing character/skills (1, 2 active)/heal cooldown; level 5 79% XP | 2026-05-17 15:56 | 1290×2796 | The canonical combat reference. See § 1.2 of `mobile-feel-target-doe-2026-05-17.md` for the gameplay-pattern read. |
| `DOE-town-hub-wide-vendors-and-voidgate-2026-05-18.png` | **Town hub (wide)** — multi-vendor view: STASH (Organize Equipment), VOIDGATE (Go to the Rift, blue portal), CHAOS TREASURY ("Vault Merchant" Escher), APPEARANCE (Spellweaver Selas, winged-NPC); other players visible (lv.50 DmironByrd, lv.50 Plaaaau, lv.50 AquantRobin); chest/stash icon left-center | 2026-05-18 | 1290×2796 | Multi-vendor density; player-coexistence; service-NPC visual language. |
| `DOE-town-vendors-pets-gems-armory-2026-05-18.png` | **Town vendor row (inner)** — PETS (Beast Tamer Malcolm), GEMS (Blood Diamond Clemens), ARMORY (whisperer Hecate); vendor stalls with gem clusters, barrels, props; lantern foreground | 2026-05-18 | 1290×2796 | Vendor-stall environmental dressing; close-shop atmosphere. |
| `DOE-town-forge-darkgold-reforging-refinement-2026-05-18.png` | **Town forge area** — DARKGOLD FORGING ("Magic Steel" Sebastian), REFORGING (Soulquencher Groff in red), REFINEMENT (Forge Master Mord far left); grass and forge props; ambient torch lighting | 2026-05-18 | 1290×2796 | Forge-cluster NPC arrangement; service-vendor naming convention (function + title + name). |
| `DOE-town-forge-advanced-with-player-spell-2026-05-18.png` | **Town forge (alt-angle)** — ADVANCED FORGE (Blacksmith Charon), REFINEMENT, DARKGOLD FORGE labels; lv.50 SendU2Jesus player visible mid-casting (yellow burst + sword in hand); ambient lighting | 2026-05-18 | 1290×2796 | Player-cast-in-town moment; demonstrates that DoE allows visible action in towns (not strict combat-only zones). |
| `DOE-town-to-dungeon-transition-path-2026-05-18.png` | **Town-to-dungeon transition** — stone path leading away from town; lv.7 XufenKeller player, Seer Cassandra (purple-cloaked NPC), Nightwatcher Edgar; lantern + hedge; stone bridge in foreground; transition lighting shift (lit town → darker path) | 2026-05-18 | 1290×2796 | Travel/transition visual language; world-edge handling; NPC mix at town border. |
| `DOE-town-chaos-treasury-vault-merchant-2026-05-18.png` | **Town vendor close-up** — CHAOS TREASURY ("Vault Merchant" Escher) close conversation distance; lv.50 SendU2Jesus visible upper-area; stone tiles and weathered ground; building eaves bottom-right; STASH marker partially visible upper-right | 2026-05-18 | 1290×2796 | Close-up vendor interaction framing; vendor name + title typography; player-NPC proximity. |

---

## Reference set 2 — 3D-stylized-ARPG visual-register anchor — 2026-06-14 (post-pivot register anchor)

**Provenance (all rows):** public-source Steam store-page imagery, pulled via the public Steam appdetails API (`store.steampowered.com/api/appdetails?appids=<id>`). URL pattern: `https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/<id>/...ss_*.1920x1080.jpg`. Fair-use justification: genre-visual-register comparison for non-commercial internal benchmarking. Not redistributed; not embedded in any shipped product. Stored in `3d-stylized-arpg-2026-06-14/<title>/`.

**Two Matt-flagged 2026 Steam titles (load-bearing — Matt surfaced these as look-targets 2026-06-14):**

| File | Title / app | Register read | What it shows | Provenance |
|---|---|---|---|---|
| `zombies-and-bullets/ZB-0{1..6}.jpg` + `ZB-header.jpg` | **Zombies & Bullets** (Muriki Studio; app 2802870; "2026" planned). Matt: **"flawless" visual rendering.** | **Register 2 — premium soft-stylized.** Low-poly geometry (faceted rocks, cone trees, box crates, chunky chars) + soft GI-style lighting + AO + atmospheric depth-fog + rich VFX (flamethrower/explosion glow) + tonally-varied painted materials. | ZB-01 forest+explosion-VFX; ZB-02 forest flamethrower; ZB-03 **dark mine** (dramatic local light — closest to ARPG dungeon mood); ZB-04 bright ruins + player ground-ring; ZB-05 boss fight (Headmaster healthbar); ZB-06 **dark minecart** (near-black, single lantern carries mood). | Steam app 2802870; capture 2026-06-14; publisher Muriki Studio |
| `katana-dragon/KD-0{1..5}.jpg` + `KD-header.jpg` | **Katana Dragon** (Tsunoa Games; app 3303010; full release 2026-01-30). Matt: **"decent" rendering + "representative of play style."** | **Register ~1.5 — competent voxel.** Voxel geometry (cube-built everything) + pixel-filter render pass + decent warm lighting + AO in dioramas. Reads charming/competent but blockier + less premium than Z&B; per-voxel-face flat color = lower material richness. | KD-01 interior diorama (warm lamp light); KD-02 voxel grass field; KD-03 water/islands; KD-04 forest path; KD-05 (reserve). | Steam app 3303010; capture 2026-06-14; publisher Tsunoa Games |

**Genre-premium ceiling anchors (register-2 top of band; the "premium stylized ARPG" the spike aims at):**

| File | Title / app | Register read | What it shows | Provenance |
|---|---|---|---|---|
| `torchlight-infinite/TLI-0{1..4}.jpg` | **Torchlight Infinite** (XD Inc.; app 1974050; F2P, PC+mobile). Hand-painted-stylized + mobile-shipping ARPG — closest register-AND-platform twin to Reincarnated's target. | **Register 2 — premium, LOW texture-detail, MAX VFX/light.** The decisive thesis-evidence: TLI-01 is carried ~90% by one golden ritual-VFX bloom + dramatic darkness; geometry is plainly low-poly chamfered stone with near-flat shading. Reads AAA-stylized on almost no high-freq texture. | TLI-01 **golden ritual circle** (VFX-as-everything); TLI-02 loot-explosion endgame (colored beams + labels); TLI-03/04 (combat/zone). | Steam app 1974050; capture 2026-06-14; publisher XD Inc. |
| `last-epoch/LE-0{1..4}.jpg` | **Last Epoch** (Eleventh Hour Games; app 899770). Same camera + same loot-ARPG framing as Reincarnated's target; PBR-textured upper end of register 2. | **Register 2 — premium, HIGH texture-detail, MAX VFX/light.** Normal-mapped PBR floors + moderate-poly models + dynamic two-zone colored lighting (warm/cool) + dense ability VFX. The high-texture-budget premium endpoint. | LE-02 **dungeon** (red/gold spell arc + green poison glow + two-light-zone); LE-04 coastal (water shader + purple lightning beam); LE-01/03 (combat/zone). | Steam app 899770; capture 2026-06-14; publisher Eleventh Hour Games |

**Named-but-not-imaged anchors (cited in report; imagery not pulled this pass):** Diablo III/IV (canonical premium-stylized-ARPG lineage per `gandalf-design-lineage.md` Layer 2); Path of Exile 1/2; World of Warcraft (canonical hand-painted-stylized texture anchor — the original "rich hand-painted texture on low-poly geometry" reference). Directories scaffolded (`diablo/`, `path-of-exile/`, `wow/`) for a follow-on imagery pull if the second (candidate-evaluation) pass needs them.

**Derived evidence strips:** `3d-stylized-arpg-2026-06-14/_strips/register-spread.png` (TLI-ritual | ZB-cave | LE-dungeon | KD-interior — the register spread, all at the same 2.5D camera) and `_strips/dark-mood.png` (the dark-ARPG-dungeon-mood band Reincarnated needs).

---

## Galadriel reference-use rules

1. **Two reference roles, post-pivot.** DoE set = **feel/HUD/service-surface** anchor (survives pivot; register-agnostic gameplay reads). 3D-stylized-ARPG set = **visual-register** anchor (post-pivot premium-stylized-3D target). Do not conflate: a Godot spike capture is scored for *register* against set 2, and for *combat-feedback density / HUD* against set 1.
2. **State-matched / register-matched comparison only.** Compare like surfaces (dungeon-combat capture → ARPG dungeon references TLI-01 / LE-02 / ZB-03; bright-zone capture → ZB-04 / LE-04). Mismatched-mood comparison (dark spike vs bright field) is invalid for lighting/atmosphere axes.
3. **Provenance discipline.** Every reference image has a row in this manifest. Public-source rows record app ID + URL pattern + publisher + fair-use justification + capture date. Adding a reference without a row is a discipline-fail; galadriel surfaces in hive log as OBSERVATION.
4. **No redistribution.** Images stay in this repo tree; never embedded in shipped product; never published.
5. **Future captures.** DoE: Matt may add later play-session captures. 3D-ARPG set: the second pass (candidate asset-pack + Meshy-gen evaluation) extends this set with candidate-render captures scored against these anchors.

---

## Cross-references

- `canonical/story/mobile-feel-target-doe-2026-05-17.md` — DoE feel-target lock; gameplay-pattern read of the combat reference
- `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` — Tonight's invocation; Track C visual benchmark scope
- `.claude/agents/galadriel.md` — Galadriel agent definition (to be created by knight-rider at hive activation per pre-authorization matrix § 6 Row 1)

---

*Authored 2026-05-18 by gandalf. Reference set established for tonight's visual benchmark pilot. Provenance: Matt-captured DoE play-session screenshots; non-commercial internal benchmarking use only.*
