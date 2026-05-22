# Dispatch — legolas: Meshy Pipeline Research (Weapon/Gear + Irregular-Monster Asset Strategy)

**Date:** 2026-05-22
**Author:** gandalf (commissioning research; design-side)
**Recipient:** legolas (Mode A — analytical research; read-only)
**Relay:** knight-rider on next session-start (or directly if you pick this up)
**Authority:** Matt 2026-05-22 (this session) — explicit research commission with Priority 1 directive on weapon/gear
**Priority:** HIGH — load-bearing for P1 W1.9 (Mixamo → Meshy swap) + G5-LITE Unity integration + canonical asset pipeline doc finalization
**Estimated effort:** 1-2 days analytical research
**Mode:** Mode A (analytical research; read-only). NOT Mode B (catalogue crawl).

---

## 0. TL;DR

Two-part research commission, **sequenced — Priority 1 must complete first**:

| Priority | Scope | Why it gates downstream |
|---|---|---|
| **1 — Weapon / gear animation in Unity + Meshy capability** | How Unity handles weapon and gear animation, whether Meshy can produce weapon/gear models, whether those models need their own animations or rely on bone-anchored attachment | Load-bearing for G5-LITE (P1+ Unity integration of signature_gear_archetype) and for the 15-archetype catalogue rule-table I authored 2026-05-22 (we need to know each archetype is producible through the Meshy path) |
| **2 — Irregular-monster asset strategy** | Asset Store coverage for slimes / serpents / multi-segments / amorphous monsters; shader-based approaches; hand-rigging budget realism | Closes the Meshy "no slimes, but we have monsters" gap Matt flagged 2026-05-22 |

Output: a single research note at `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` covering both priorities with explicit *answer / evidence / sources* sections.

---

## 1. Priority 1 — Weapon and gear animation in Unity + Meshy capability

### 1.1 Why this is Priority 1

Matt 2026-05-22 directive: before committing the Mixamo → Meshy swap canonically, we need to know whether the **gear pipeline** holds under Meshy. The 15-archetype catalogue I authored this morning (`canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2) names specific weapon and gear forms — blunderbuss, censer, kanabō, longbow, twin-daggers, greatsword, focus-orb, wand, warhammer, chain, scepter, horn, torch-staff, ritual-veil, plus the canonical 15th slot. Each must be producible through the chosen asset pipeline.

Additionally, G5-LITE (P1+; drax + Unity team) consumes `signature_gear_archetype` to render player class identity. If gear cannot be made + rigged + animated through the Meshy path, we have a cross-repo coherence gap right at the P1+ Unity-integration boundary.

### 1.2 Research questions

**1.2.1 How does Unity handle weapon and gear animation?**

- Standard pattern: weapon as separate GameObject attached to a humanoid hand bone (`B_R_Hand` / `RightHand`) via Animation Rigging or simple parenting?
- Does the weapon mesh need its own bones / armature, or does it rely on the character's hand-bone transform?
- For gear pieces (chest armor, shoulder pads, helmets, capes): mesh-deformed against character skeleton (skinned) vs. rigid attached props?
- For VFX-anchored gear (torch-staff with flame; censer with smoke trail; ritual-veil with flowing cloth): standard Unity VFX-attachment pattern via Animation Rigging anchor points?
- Reference Unity documentation: Animation Rigging package, Humanoid Avatar bone mapping, skinned-mesh-renderer vs. simple-mesh attachment

**1.2.2 Can Meshy produce weapon and gear models?**

- Meshy's "text-to-3D" or "image-to-3D" — what asset types does it cover? Just characters, or also props / weapons / gear?
- Meshy's documentation / marketing copy — what do they advertise for weapon and prop generation?
- Is the output format Unity-compatible (FBX, glTF, with correct pivot points for hand-attachment)?
- Texture / material handling — PBR (metallic-roughness) outputs Unity can consume natively?
- For armored gear (chest pieces, etc.) — does Meshy produce mesh that can be skinned to a humanoid skeleton, or only rigid props?

**1.2.3 Does Meshy need to animate weapons / gear for Unity's use?**

- The CRITICAL question: who animates the weapon arc during a sword swing?
  - **Hypothesis A**: the character's hand-bone animation drives the weapon (weapon is a static mesh attached to the bone; the swing comes from the character's animation; no weapon-specific animation needed)
  - **Hypothesis B**: the weapon needs its own animation track (e.g., a glaive that telescopes; a chain that whips; a flexible weapon)
  - **Hypothesis C**: hybrid — most weapons are static-mesh-attached (A); special weapons need additional rigging (B)
- For gear that has its own VFX (censer smoke, torch flame, ritual-veil flow): VFX Graph / Particle System driven by the gear's transform, not by an animation track per se?
- Confirm: does Meshy's "500+ prebuilt animations" cover character-only motion (walks / attacks / jumps), or also include weapon-specific animation tracks?

**1.2.4 What about the 15-archetype catalogue specifically?**

For each archetype in `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` § 2, classify the production path:

- **Standard (Hypothesis A)** — static mesh + bone-attachment: greatsword, warhammer, twin-daggers, longbow, wand, scepter, kanabō
- **VFX-anchored** — static mesh + Particle System / VFX Graph: censer (smoke), torch-staff (flame), focus-orb (glow), horn (sound-wave VFX)
- **Possibly Hypothesis B** — additional rigging needed: chain (segmented; whip motion), ritual-veil (flowing cloth; cloth-sim or animation), blunderbuss (smoke + recoil)
- **Slot 15** (gear-as-substrate § 3 final archetype — confirm name from canonical doc)

For each, flag whether Meshy's documented capability covers it OR whether an alternate path is needed (Asset Store, Blender, hand-author).

### 1.3 Priority 1 deliverable shape

A structured table:

```
Archetype     | Hypothesis | Meshy can mesh? | Meshy can rig/anim? | Alt path if needed
greatsword    | A          | YES (expected)  | N/A (bone-attached) | —
chain         | B?         | TBD             | TBD                 | Asset Store?
ritual-veil   | B          | TBD             | Cloth-sim Unity?    | Blender hand-author?
...
```

Plus: a confidence read on whether Meshy + Unity Animation Rigging covers the **dominant case** (~10-12 of 15 archetypes) cleanly, with the alt-path enumeration for the remainder.

---

## 2. Priority 2 — Irregular-monster asset strategy

### 2.1 Context

Meshy's marketing copy claims **humanoid + quadruped** rigging only. Matt 2026-05-22 flagged the gap: ARPGs lean heavily on irregular topology enemies (slimes, multi-segment serpents, multi-headed, eyeball / no-body, insectoid, floating, swarm). For Reincarnated specifically, the trial-boss-gallery + spirit-form-library framing wants wide body-plan variety.

Reading: this is a **scoping gap, not a swap-blocker.** Meshy still handles the dominant case (player forms; humanoid + quadruped monsters). Irregular monsters route to a different pipeline. Priority 2 enumerates that pipeline.

### 2.2 Research questions

**2.2.1 Asset Store coverage for irregular monsters**

- Which Unity Asset Store packs cover slimes / amorphous monsters? (Quirky Series; Synty POLYGON Fantasy; Toon Monsters series; PROTOFACTOR monsters; etc.)
- Which cover multi-segment serpents / dragons / hydras?
- Which cover insectoid / multi-limb creatures?
- Which cover floating / wraith / spirit creatures?
- Per-pack: estimated cost range, typical animation coverage, licensing for commercial indie use

Expand from the existing legolas Phase 1 audit (`agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/`) which already touched the Asset Store landscape; this is a more targeted irregular-monster-specific sweep.

**2.2.2 Shader-based approaches the indie ARPG community uses**

- Vertex-shader-driven amorphous monsters (slimes via animated vertex displacement + scrolling normal maps)
- Sprite-billboard approaches for spirits / wraiths (2D-in-3D)
- Procedural mesh deformation for swarms / particle-driven enemies
- Reference: indie ARPG dev blogs, GDC talks, Unity community examples

**2.2.3 Hand-rigging budget realism**

- For signature trial-room bosses (~5-10 per season in Reincarnated's seasonal-journey framing), what is a realistic per-monster hand-authoring budget?
  - Time: hours of Blender / ZBrush + Maya / Blender rigging per signature boss?
  - Skill level: solo-developer-feasible? Outsource-able?
  - Cost: rough estimate per boss if outsourced (Fiverr / Upwork specialty rates)?
- Pattern recommendation: which subset of trial-boss-gallery monsters warrants hand-authoring vs. Asset-Store-purchased?

### 2.3 Priority 2 deliverable shape

A structured table:

```
Monster category  | Best asset path        | Cost estimate | Coverage in Asset Store
slimes/amorphous  | Asset Store + shader   | $20-50/pack   | High
serpents/multi-seg| Asset Store            | $30-80/pack   | Medium
hydras/multi-head | Hand-author signature  | 8-16 hrs each | Low
eyeballs/no-body  | Asset Store + shader   | $20-50/pack   | Medium
insectoid         | Asset Store            | $20-60/pack   | High
floating/wraith   | Asset Store + sprite   | $20-40/pack   | High
swarms            | Procedural / particles | Engine effort | N/A
```

Plus: a per-season-budget framing (what does it cost in time + dollars to populate one season's monster roster under this strategy?).

---

## 3. Out of scope (for this dispatch)

- **Mode B catalogue crawl.** This is Mode A analytical research only. Do not enumerate every individual Asset Store pack; cover the landscape with representative examples.
- **Procurement decisions.** Findings inform Matt's procurement calls; do not pre-empt them. Cost estimates are guidance, not commitments.
- **Re-litigating the Meshy → Mixamo swap.** That decision is made (Matt 2026-05-22); this research scopes its boundary, doesn't re-debate it.
- **Animation-source for player forms.** Meshy's 500+ animations are confirmed sufficient per Matt's site review; do not re-research that.
- **Engine-side implementation.** Implementation pathways are rocket / drax territory; this dispatch is asset-strategy scoping.

---

## 4. Deliverable

Single research note: `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md`

Structure:

- § 1 Priority 1 — Weapon and gear animation findings (per § 1.3 table + commentary)
- § 2 Priority 2 — Irregular-monster asset strategy findings (per § 2.3 table + commentary)
- § 3 Open questions surfaced (anything you encountered that needs gandalf or Matt design call)
- § 4 Sources cited (Unity docs, Meshy docs, Asset Store packs, dev blogs, GDC talks — URL or specific document citation)
- § 5 Confidence flags per major claim (HIGH / MEDIUM / LOW with rationale)

Length target: ~1500-2500 words. Not a full Mode B catalogue; a sharp Mode A analytical sweep.

---

## 5. Downstream consumers (who reads your findings)

1. **gandalf** — folds findings into the canonical asset-pipeline doc (`canonical/story/asset-pipeline-meshy-swap-2026-05-22.md`) skeleton authored 2026-05-22; finalizes the canonical doc
2. **knight-rider** — relays findings to protocol v1.3 amendment workstream (W1.9 + W1.10 update)
3. **Matt** — reads to confirm the swap goes ahead cleanly; arbitrates any close-call findings
4. **drax** — when G5-LITE Unity integration begins, consults findings on weapon/gear attachment patterns
5. **Future T4-B catalogue authorship** — for Tier 4 keystones tied to specific gear archetypes (per `canonical/story/tier-4-architecture-defaults-2026-05-22.md` § 5)

---

## 6. Timing

- **Earliest fire:** any session 2026-05-22 onwards (no fire-gate; pre-authorized research commission)
- **Duration:** 1-2 days analytical work
- **No babysit.** Per Discipline #19 (RATIFIED 2026-05-22) — legolas runs as a bounded sub-agent with explicit deliverable; orchestrator does not monitor or watch; findings file lands as the cross-session continuity artifact

---

## 7. Cross-references

- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — canonical doc skeleton (gandalf-authored same session; awaits legolas findings to finalize)
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` — 15-archetype catalogue (the Priority 1 archetype enumeration consumes this)
- `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6 (LITE path) + § 3 (15-archetype catalogue source)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.2.2 W1.9 + W1.10 (target of protocol v1.3 amendment post-research)
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/` — Phase 1 reconnaissance (priorprecedent; existing Asset Store landscape research as starting point)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 19 — Discipline #19 RATIFIED; no babysit on this research

---

**Signed:** gandalf (story-and-design steward; research commissioner)
**For:** clean Mixamo → Meshy swap canonical close + irregular-monster pipeline scoping informed by empirical Unity + Meshy capability research.
