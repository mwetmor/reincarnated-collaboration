# Drax Build Brief — Capture Resolution Bump + Architecture-Audit Camera

**STATUS:** ACTIVE BRIEF (drax build spec; Matt-authorized 2026-06-16)
**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-16 (Pattern-B battle-room visual session) — *"Yes, I authorize both."* Authorizes (1) a capture-resolution bump and (2) a standing architecture-audit camera, drafted here as one contract so drax builds and galadriel consumes against the same spec.
**Build owner:** drax (Godot capture harness — `scripts/render_capture.gd`, `render_descent_scene.gd`, `shoot_descent.gd`, the per-scene run scripts).
**Consumers:** gandalf (semantic-coherence read), galadriel (capture + CV probes).
**Routing:** KR sequences into the queue (or Matt authorizes direct). This is a spec, not a dispatch.
**Companion docs:**
- `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — §2-bis architectural-grammar rule + §5 benchmark-instrument note (the seed this promotes).
- `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter4-architectural-grammar-rescore.md` — the green iter4 scorecard a floating staircase survived.

---

## 0. TL;DR

Two changes to the capture pipeline, born from one finding: **galadriel's iter4 scorecard called architectural-grammar VALIDATED (falsifiers cleared, 18%→65%) and a floating staircase survived it** (zone5 sanctum, `descent_iter4_zone5_09.png`, upper-right). That defect is invisible to a luma histogram at any resolution AND to a top-down camera at any resolution — the first is a *kind-of-measurement* gap (statistical vs semantic), the second is *foreshortening* (a top-down view collapses vertical structure into the floor plane, so you cannot see whether a stair flight lands).

1. **Resolution bump** — differentiated: combat/lifecycle captures to 1440p; audit-camera captures to 4K. Comfort for human reads + galadriel's crops; near-zero cost where it matters.
2. **Architecture-audit camera** — a standing, oblique, low-angle camera pass *separate from the combat/zone cameras*, whose only job is to expose **load-paths**: do stairs land, do galleries rest on support, do arches spring from real feet. This is the input for the semantic-coherence gate (§5 — who audits).

---

## 1. Why (the gap, stated precisely)

Two orthogonal blindnesses produced the surviving defect:

- **Statistical ≠ semantic.** galadriel's instruments normalize to "960w inside-fit" grayscale luma and measure LDR/SHF/HLF/saturation distributions + a *defined* falsifier-probe set (orphan upright columns, wall-top-silhouette arches, free verticals, arch-feet-on-empty-floor). A floating *staircase* is an open-ended semantic-coherence failure outside that defined set. No resolution closes a kind-of-measurement gap.
- **Top-down foreshortens verticality.** The zone/combat cameras are near-top-down (elevated, fov 43–60). Looking down the vertical axis, a stair flight's rise projects onto almost nothing — ground-contact is unreadable. No resolution closes a foreshortening gap.

A bigger render is real quality-of-life, but it does not fix either blindness. The two changes below address resolution (comfort) and angle (the actual unlock) separately, and §5 names the human gate neither tool replaces.

## 2. Part 1 — Capture resolution bump

**Differentiated, cost-aware** (galadriel normalizes to 960w, so 4K on every lifecycle frame is wasted render):

| Capture class | Current | New | Rationale |
|---|---|---|---|
| Combat / lifecycle / zone / establishing | 1152×648 | **2560×1440 (1440p)** | Feeds galadriel's 960w-normalized instruments (unaffected by source res) + her qualitative crops (gains headroom). 1440p is ample; avoids paying 4K × 100-frame render cost. |
| **Architecture-audit camera (Part 2)** | n/a | **3840×2160 (4K)** | Few frames per scene (~2–4 azimuths × N zones); feeds the human semantic read + any future CV. Max detail where it matters; cheap because frame count is small. |

- Preserve 16:9; it's a viewport/Movie-Maker output param — a re-run, not a rebuild (captures are deterministic).
- IP handling **unchanged**: all captures stay git-ignored, local-only Synty-derivative IP regardless of size.

## 3. Part 2 — Architecture-audit camera

**Purpose:** expose vertical load-paths for the §2-bis read. NOT a gameplay camera; NOT scored for register-2; never shipped to a player. Its only job is to answer *"if this were stone and gravity were on, would it stand, and is it doing a job?"* for every stair, gallery, arcade, and arch.

**Spec:**
- **Angle — low oblique.** Pitch the look-direction ~**20–40° below horizontal** (markedly shallower than the near-top-down ZoneCams), so vertical structure projects to vertical screen-space and a stair's base-to-floor contact (or absence) is legible.
- **Coverage — orbit.** Minimum **4 azimuths per scene** (≈NE/SE/SW/NW) so no load-path hides behind another mass. PLUS at least one azimuth that frames each *known* architectural feature **side-on** (for the current descent: one that puts the zone5 gallery-and-stairs corner side-on).
- **Framing — feature-as-subject.** Each major architectural element (gallery run, stair flight, arcade, arch) should be the *subject* — large in frame — in at least one audit frame, not a distant corner detail.
- **Output:** 4K; naming `<scene>_audit_az<NN>_<frame>.png`; git-ignored as above.
- **Premium option (offer, don't require):** a slow 360° orbit *video* (Movie Maker) per scene. Motion parallax is the single strongest load-path reveal — a floating element "swims" against its background the instant the camera moves. If cheap, this beats stills for the audit.

## 4. Acceptance criteria — validate the instrument against the KNOWN defect

The team discipline is recognition→validate→commit; apply it to the *tooling*:

- Render the audit pass on the **current** zone5 scene — the one with the known floating staircase, unchanged.
- **PASS = the audit frame(s) make the floating staircase legibly float to a human reader.** If the new angle does NOT reveal the known defect, the angle is not low/oblique enough — iterate the pitch/azimuth until the known-positive case is unmistakable, *then* commit the camera.
- This validates the instrument on a known-positive before we trust it on unknowns — the same discipline as galadriel re-deriving phase boundaries from a capture's own curve rather than inheriting them.

## 5. Who runs the audit (Matt's question — layered answer)

**Immediate (this sweep) — mirrors the existing "galadriel scores, gandalf rules" division, extended to architectural coherence:**

| Role | Owner | Why |
|---|---|---|
| Build the camera + render audit frames | **drax** | Production capture-harness work — his lane. |
| Run the capture + the falsifier-probes that already exist + file the frames as evidence | **galadriel** | Her capture/scoring tooling; she catches what the *defined* probe-set catches. |
| **The open-ended semantic-coherence read — the load-path judgment no probe captures — and the canon call** | **gandalf (me)** | It is a *design* judgment grounded in the §2-bis rule I authored, exactly like the register-2 canon calls I make on galadriel's scorecards. galadriel perceives + measures; I judge coherence + rule. |

- **Not drax** for the read: don't grade your own homework (the same reason galadriel scores drax's builds, not drax — the self-scoring anti-pattern).
- **Not galadriel** for the *semantic* read: her instruments are statistical and her probe-set is closed; the open-ended "does this read as a building that could stand" judgment is the design-steward's, on her evidence.

**Maturing it — so the audit doesn't live forever on gandalf's scarce attention:**

Every novel defect class the human read catches (floating stairs = the first) gets *encoded* into a cheap, standing check:

- **Geometric support-failures (floating stairs / galleries / arches) → a scene-graph load-path validator**, engine-side and deterministic, in the mold of the existing `check_descent_parity.py`: walk the scene tree; for each structural mesh (stair, deck, arch, column), test whether supporting geometry exists beneath its base within tolerance; flag orphans. This catches the defect **at build time, no camera, no eyeballs** — far more reliable than CV for a geometric question, and it's the *better* long-run home than the audit camera for this specific class.
  - **galadriel correction (2026-06-16, empirically grounded — see her artifact):** the validator is even CHEAPER than scoped for the common case. **Tier 1 — transform-Y sibling-consistency walk on `.tscn` TEXT, no headless render.** The known zone5 float is a plain transform-Y mismatch: stair `SM_Bld_Base_Stairs_01` sits at world-Y **0.0** (pinned to the fighting floor) while its sibling deck `SM_Bld_Base_Floor_01` it should connect to sits at world-Y **6.0** — a 6-unit gap readable straight off the scene-text node transforms. No `.res` load, no AABB math, no camera. This is the first check to build.
  - **Tier 2 — AABB-precise extent check, at real cost (headless `.res`/MeshLibrary load), ONLY for sub-mesh-height gaps** the text-walk can miss (where a mesh's *modeled* base extent, not its origin, is what fails to land). Do NOT reach for this tier by default — galadriel's prior-pass artifact wrongly claimed the AABBs were "already in the file"; they are not (the 210 `aabb` lines in the scene are GPUParticles3D `visibility_aabb` culling boxes, unrelated to structural-mesh extent). True extent requires the headless load. Reserve Tier 2 for the defect classes Tier 1 demonstrably cannot reach.
  - **Acceptance fixture for the validator (known-positive):** Tier 1 MUST flag the zone5 stair (Y=0.0) against its deck sibling (Y=6.0). Validate the check on this known float before trusting it on unknowns — same recognition→validate→commit discipline as the camera (§4).
- **Genuinely perceptual coherence (read-clutter, figure/VFX balance) → a galadriel CV falsifier-probe**, where scene-graph can't reach. **galadriel confirmed (2026-06-16) her current probe-suite is structurally blind to this defect class** — no ground-contact term exists in any of the 6 probe outputs (upperBand/lower edge-density, storeyRatio, columnProfile_CV, periodicPeaks, maxAutocorr all read identically for a floating vs a landed stair). This is the empirical proof that the scorecard is necessary-but-not-sufficient and the scene-graph gate is a genuinely separate instrument, not a redundant one.

**The loop:** human eye finds the novel semantic defect → it's encoded as a deterministic scene-graph check (or a CV probe) → the check catches it forever after, cheaply. This is the same maturation the four §2-bis falsifier-probes already went through — each was once a human observation before it became an instrument. The audit camera + gandalf read is how we *find* the next class; the validators are how we *retire* it.

## 6. Cross-references

- §2-bis architectural-grammar rule + load-path invariant: `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` §2-bis; standalone ruling `agentic_orchestration/gandalf/notes/2026-06-15-columns-arches-architectural-grammar-rule.md`.
- §5 benchmark-instrument seed (top-down foreshortens the arcade rhythm; "render one oblique/lower-angle benchmark frame per scene") — this brief promotes that note to a standing camera.
- Scene-graph validator precedent: `reincarnated-godot/scripts/check_descent_parity.py`.
- The surviving-defect evidence: zone5 sanctum `descent_iter4_zone5_09.png` (local, git-ignored) — the floating staircase in the upper-right gallery corner, against the green iter4 scorecard `agentic_orchestration/galadriel/reports/2026-06-15-descent-iter4-architectural-grammar-rescore.md`.
- **galadriel's gap-confirmation + scene-graph re-scope:** `agentic_orchestration/galadriel/notes/2026-06-16-floating-staircase-gap-confirmation-cv-vs-scenegraph.md` (commit `a7cb87b`) — empirically confirms the probe-suite blindness (6 outputs, no ground-contact term), pins the ground truth (stair Y=0.0 vs deck Y=6.0), and supplies the Tier-1 / Tier-2 validator scoping folded into §5 above. **Confirms the resolution bump (§2) is instrument-safe:** her probes read native dimensions and scale-normalize all outputs, so 1440p/4K captures change nothing in the numeric scorecard — the bump buys human-read + crop headroom only, exactly as §2 scopes it.

---

**Signed:** gandalf, 2026-06-16.
**For:** the capture-pipeline contract that closes the two blindnesses behind the surviving zone5 floating staircase — a differentiated resolution bump (1440p combat / 4K audit) and a standing low-oblique architecture-audit camera validated against the known defect — plus the layered audit ownership (drax builds + renders; galadriel captures + runs the closed probe-set; gandalf runs the open-ended semantic-coherence read and rules; novel defect classes mature into deterministic scene-graph validators à la `check_descent_parity.py`).
