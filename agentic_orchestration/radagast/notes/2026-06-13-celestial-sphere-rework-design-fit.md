# Design-Fit Verdict — Mantis Celestial-Sphere Rework + Figure-Lighting-Rig Repair

**STATUS:** CURRENT — radagast design-fit verdict (PC critique-pair design side, Pattern E). Sam runs Gate-1 process side in parallel.
**Date:** 2026-06-13
**Author:** radagast (PC-side design steward)
**Review target:** `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md` (DRAFT)
**Fired by:** david-h as design-fit subagent.
**Companion:** `agentic_orchestration/david-h/notes/2026-06-13-p0-1-s5-blocked-findings-and-routing.md`; cosmograph creation-moment architecture § 2.6 + § 12; avatar-projection-and-hall-of-heroes § 4.

---

## VERDICT: PASS-WITH-WARN

The dispatch is sound and fires once the ONE required wording amendment on repair #2 is folded (encodes the gandalf key-light ruling's three constraints). No BLOCK. The amendment is small and precise. Two forward design items noted separately; neither expands this dispatch's scope.

---

## (a) Sky-geometry canon fit — PASS

- Moving stars from the origin ±67 cloud onto the **R=8,000 interior sphere** is a correction TOWARD § 2.6, not drift. § 2.6 locks "the celestial sphere's interior surface is where constellations live"; the avatar-at-origin-looking-up POV is § 6.3 LOCKED. The ±67 origin cloud was a spike artifact, never canon.
- `cosmograph_sphere_001000stars_R8000.json` at R=8,000 matches the spherical-shell radius intent (§ 2.6 leaves radius "TBD per WS2 — must remain reachable-feeling"; R=8,000 is the working value). Confirm-the-handedness step in § 1 is the right discipline.
- **Keeping the volumetric nebula ON (repair #1.5) is REQUIRED for canon, not optional.** § 2.6 "3D nebula context: VDB volumetric clouds beyond the sphere"; § 6.3 "3D nebula context as exterior + visual depth. LOCKED." Killing the nebula to dodge the GPU crash would have violated locked geometry. The dispatch's framing — tame the cost, keep it on — is exactly right. The session-only CVar disarm correctly flagged as a band-aid (§ 2 Note).
- **Refinement flag (not a blocker):** § 12 retired per-primitive iconography and made the **rune-anchors-in-sky the ONLY player-facing iconography** (§ 12.2). Stars-on-the-sphere is the substrate layer; the 7 cluster rune-anchors sit ON that same sphere surface. This dispatch correctly scopes rune rendering OUT (§ 6, deferred to WS2 commission `2026-06-10-...ws2-niagara-cluster-rune-rendering-commission.md`). No action needed — just confirming the geometry mantis establishes here (R=8,000 interior surface, JSON-driven user-params) is the SAME surface the rune-anchors will later attach to. The Gate-A user-param architecture (`StarPositions`/`StarColors`) is forward-compatible with that. Good.

**Player consequence:** the player looks up and the sky is a real bounded celestial dome at touchable distance (§ 2.6 "player feels they could touch the sky"), with depth beyond — not a particle blob underfoot and not a black void. This repair is what makes S1 render the intended sky.

## (b) Figure key-light independence — PASS-WITH-WARN (amendment required)

**The gandalf ruling is folded, not re-litigated:** YES — the Earth avatar carries its own motivated standalone key light, independent of the sky. Direction ruled now; values tuned at the console downstream of exposure lock.

Repair #2's sub-steps are **directionally consistent** with the ruling — §§ 2.1 (re-aim moonlight at the camera-facing surfaces), 2.2 (real skylight source so fill survives an empty sky), 2.4 (rig stands alone, no `ns.celestialsphere` emissive dependency) all serve "motivated standalone key, direction-now." But the dispatch **under-encodes two of the ruling's three constraints**:

| Ruling constraint | § 3 status | Gap |
|---|---|---|
| (1) motivated + color-matched to night scene, soft, rim-biased, anchored to the avatar — natural light finding the figure, NOT a product-shot spotlight | PARTIAL — §§ 2.1/2.2 fix the mechanical black-silhouette but say nothing about CHARACTER of the light | A naive fix (crank a hard directional onto the figure) would pass acceptance #5 "reads in Lit" while violating the kit fantasy — it would read as a studio spotlight, breaking the "ordinary person standing on a hill at night" diegesis (§ 4.2: knoll reads as intentional ordinary place) |
| (2) avatar key must read DISTINCT from the diegetic spirit-glow — avatar key = mundane/grounded pole, spirit-glow = supernatural pole; the contrast IS the mythic content, must not blend | MISSING — § 3 never mentions the relationship to `RigB_SpiritGlowOnly` beyond the toggle test | This is the load-bearing one. If the avatar key and the spirit-glow share temperature/quality, the mundane-vs-becoming contrast collapses and the scene loses its mythic charge |
| (3) DIRECTION ruled now; VALUES (intensity/temp/falloff/rim) tuned at console downstream of exposure lock + DXGI gate | PARTIAL — § 3 implies live values ("10× still black") but doesn't state values are console-deferred | Without this, mantis may try to LAND final intensity/temperature headless, which can't be judged without Matt at the console (#5 mythic-weight judgment + exposure lock) |

**EXACT WORDING AMENDMENT — add to § 3 as a framing preamble before the sub-step table, and amend acceptance #5/#6.**

Add this block immediately under the § 3 "Diagnostics already EXCLUDED" line:

> **Design constraint on the repair (radagast design-fit, folding gandalf key-light ruling 2026-06-13):** The Earth avatar carries its OWN motivated key light, independent of the sky — its legibility is invariant to the knoll's lighting flux (genre-settled: Diablo char-select, Destiny Tower, Soulslike hubs). Three constraints on HOW:
> 1. **Motivated + grounded, not a product-shot spotlight.** Color-matched to the night scene, soft, rim-biased, anchored to the avatar — natural light finding the figure. The fix is not "crank a hard directional"; it is "give the figure a believable night-key + ambient fill that reads as the world lighting an ordinary person on a hill" (§ 4.2 knoll-reads-as-intentional-ordinary-place).
> 2. **DISTINCT from the diegetic spirit-glow.** The avatar key = the mundane/grounded pole (the human not-yet-become); `RigB_SpiritGlowOnly` = the supernatural pole (the becoming). The contrast IS the mythic content and must NOT blend — keep the avatar key's temperature/quality readably separate from the spirit-glow's. When both are present, a viewer must be able to tell "this is worldlight on a person" from "this is the spirit's own light."
> 3. **Direction-now, values-later.** This dispatch establishes the rig DIRECTION (standalone, motivated, distinct) headless. The VALUES — intensity / temperature / falloff / rim weight — are TUNED in the render-console session downstream of the exposure lock, with Matt at the console (DXGI gate + acceptance #5 mythic-weight judgment). Do NOT attempt to land final values headless.

Amend **acceptance #5** from:
> `SK_EarthAvatar` reads in Lit under Rig A from `Cam_GroundLookUp` (figure-lighting repair)

to:
> `SK_EarthAvatar` reads in Lit under Rig A from `Cam_GroundLookUp` as a **standalone motivated night-key + ambient fill** (no `ns.celestialsphere` dependency), reading as worldlight-on-an-ordinary-person — NOT a product-shot spotlight. Mechanical legibility lands headless; final intensity/temperature/falloff values are console-tuned (DXGI gate).

Amend **acceptance #6** to add, after "produces a visible, judgeable lighting difference on the figure":
> ...with the Rig A avatar-key reading DISTINCT in temperature/quality from the Rig B spirit-glow (mundane pole vs supernatural pole; the contrast must not blend).

**Player consequence:** with the amendment, the figure reads as a real person the night is touching, and when the spirit-glow rises it reads as something OTHER lighting them from within — the visual grammar of "human not-yet-become." Without it, the literal acceptance ("reads in Lit") is satisfiable by a spotlight that kills the diegesis and blends the two poles, and the scene's whole mythic premise goes flat. This is why it's WARN not pass-clean: the mechanical bug-fix and the design intent can diverge here, and the amendment closes that gap.

## (c) FigureStandIn / spirit-visual scoping — PASS (correctly out of scope; forward item logged)

- `FigureStandIn` (particle ball) as the spirit form is an explicit placeholder. The real spirit visual is § 4.5 Q5 (ambiguous → partial → defined visual logic), an EXPLICITLY DEFERRED refinement question gated on "WS2 prototype + art-direction iteration." Dispatch § 6 correctly puts it out of scope.
- For a Phase-1 **figure-lighting-readability** spike, placeholder-as-spirit is acceptable: the lighting subject under test is `SK_EarthAvatar` (the readable humanoid), not the spirit form. The figure carries the readability test; the blob does not need to.
- **One coupling caveat (not a blocker):** the gandalf ruling constraint (2) — avatar-key-distinct-from-spirit-glow — is only PARTIALLY judgeable while the spirit form is a particle ball. `RigB_SpiritGlowOnly` can be evaluated as a *light*, but the full mundane-vs-supernatural CONTRAST read needs the eventual ambiguous-spirit mesh. So acceptance #6's "judgeable difference" is judgeable for the LIGHTING POLES now; the final aesthetic contrast judgment carries forward to when the real spirit visual exists. Mantis should not treat a clean Rig A/B light-toggle on the placeholder as closing the contrast question — it closes the LIGHTING-RIG question only.

**FORWARD DESIGN ITEM (separate, do NOT expand this dispatch):** The ambiguous-spirit visual (§ 4.5 Q5) needs scoping before S5's *aesthetic* contrast judgment can fully close. Recommend david-h log this as a forward register item routed to a radagast↔Mac-gandalf consult (Q5 is gandalf-leaned: "luminescent mist-cloud roughly humanoid, translucent, soft edges, subtle internal motion") — Q5 is a cross-cutting creation-moment refinement, so it routes to Mac-gandalf per my drift-discipline, not authored PC-side. Trigger: WS2 prototype / art-direction iteration. Not this dispatch.

---

## Cross-cutting flags

- The gandalf key-light ruling is a cross-cutting creation-moment design call already made Mac-side; I am FOLDING it, not re-litigating (per invocation). No new consult needed for (b).
- The § 4.5 Q5 spirit-visual scoping (forward item under (c)) IS cross-cutting (creation-moment refinement, Mac-gandalf primary) — flagged for david-h to route as a radagast→Mac-gandalf consult when WS2 art-direction iteration triggers. Not now.

## Decidable now vs at console (DXGI gate)

- **Decidable headless (this dispatch):** sky geometry on R=8,000 sphere; nebula cost-cut; rig DIRECTION (standalone, motivated, distinct-pole); mechanical "figure no longer black in Lit"; Rig A/B light-toggle exists and is wired.
- **Deferred to console (Matt present):** final key-light VALUES (intensity/temperature/falloff/rim); the #5 mythic-weight judgment; the full aesthetic mundane-vs-supernatural contrast read (also partly gated on the real spirit visual per (c)). The amendment to acceptance #5/#6 encodes this split.

---

## Summary

- (a) sky geometry: **PASS** — corrects toward § 2.6/§ 6.3 canon; nebula-stays-on is required, not optional.
- (b) figure key-light: **PASS-WITH-WARN** — direction sound; fold the three-constraint amendment into § 3 + acceptance #5/#6 so the bug-fix can't diverge from the design intent (spotlight risk + pole-blending risk + values-headless risk).
- (c) FigureStandIn: **PASS** — correctly out of scope; forward Q5 spirit-visual item logged for a future Mac-gandalf consult; mantis must not over-read the placeholder light-toggle as closing the aesthetic contrast question.

**Net verdict: PASS-WITH-WARN.** Fires once the § 3 amendment is folded. Sam's Gate-1 process verdict composes in parallel.

**Authored:** radagast 2026-06-13, PC design-fit (Pattern E).
