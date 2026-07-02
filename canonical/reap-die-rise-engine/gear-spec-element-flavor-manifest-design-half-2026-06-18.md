# Gear-Spec Element-Flavor Manifest — the Design-Owned Half (§6.2 / §7.6 completion)

> **STATUS:** CURRENT (load-bearing as of 2026-06-18) — completes the **design-owned half of the valid-values manifest** called for by `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` §6.2 + §7.6 ("Author the manifest design-owned half"). This is the **D7-narrow-blank menu** the star-lord §7.3 constrained-LLM StyleProfile-fill picks *within* — the element-flavoring vocabulary (six-profile §6) the restyle leaf consumes. Register in `canonical/00-ground-state.md` § 1 (next-session hygiene; the file is large — flagged for KR, not edited here).

**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward; design seam per architecture record §7.6)
**Resolves:** the open manifest design-owned half. After this, the §7.1 manifest node is `design-half [DONE here] + elrond substrate-slice [in-flight]`.
**Method discipline:** reconciled against disk FIRST. `FINISH_ENUM`, `EMISSION_BY_TIER`, the zone→region provisional map, the 17 accent sockets, and the full StyleProfile schema are **already in code** (`gear_style_profile.py`, rocket B2 `5f85014`, gandalf-ENDORSED 2026-06-17). This doc authors ONLY the genuinely-missing vocabulary — the per-element tint families + aura colors + placement intent — and references (does not re-author) what is built.
**Companions:**
- `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` — the §7.6 output-shape ruling (zone_key/region_key split this menu keys to).
- `canonical/story/six-profile-set-architecture-2026-06-16.md` §6 (element-flavoring) + §7 (glowing-aura apex) — the CONSUMER this menu feeds.
- `reincarnated-engine/src/reincarnated/generation/gear_style_profile.py` — the built schema + `FINISH_ENUM` + `EMISSION_BY_TIER` this menu completes.
- `agentic_orchestration/gandalf/notes/2026-06-17-gear-spec-b2-restyle-leaf-conformance-verdict.md` §5 — names exactly what star-lord §7.3 needs (this menu).

---

## 0. The ruling in one line

The element-flavor manifest is a **discrete per-element tint menu** (4 core elements × a 4-member tint family + one aura color + a finish-lean), plus a **zone-assignment guidance rule** and a **single emission-placement rule**. The star-lord §7.3 LLM picks ONE tint per zone *from the dominant element's family* — a genuinely narrow blank (not "any RGB"), honoring D7. Structure is gandalf-authored + code-enforced; the LLM chooses within the menu only.

## 1. Why a DISCRETE menu (the D7 discipline made concrete)

D7 (the AI-tell line) licenses the LLM to fill a *narrow constrained blank*, never the player-facing whole. A continuous tint range ("pick any RGB that reads as fire") re-opens the whole — the model authors the look. A **discrete 4-member family per element** closes it: the model's only freedom is *which of fire's four tints* lands on *which zone*, guided by the zone rule (§3). This is the asset-layer analog of the same discipline that makes `FINISH_ENUM` a closed menu (B2 verdict §4 note 3) — the model picks from a curated set, it does not invent the set. **Curation is the human's; selection-within is the model's.** That is the PoE-uniques-vs-rares precedent applied to color (architecture §3.2).

## 2. The element tint menu (design-owned vocabulary)

Four core elements (`element/selector.py:40` VALID_SLOTS = fire/wind/water/earth). Each ships a **4-member family** (hex + RGB-float for the engine), an **aura color** (the six-profile §7 emission rgb), and a **finish-lean** (which `FINISH_ENUM` members read element-appropriate — guidance for the LLM's `region_finishes` pick).

| Element | Family member (hex / RGB-float) | Aura color (emission rgb) | Finish-lean |
|---|---|---|---|
| **fire** | ember-crimson `#B3261E`/(.70,.15,.12) · forge-orange `#E2622A`/(.89,.38,.16) · ash-gold `#C9923B`/(.79,.57,.23) · coal-dark `#3A1512`/(.23,.08,.07) | forge-glow **(1.00, 0.45, 0.15)** | metallic / lacquered (heat-treated); matte coal on cloth |
| **water** | deep-tide `#1E4FB3`/(.12,.31,.70) · glacier-cyan `#46B6C9`/(.27,.71,.79) · foam-white `#D6ECF2`/(.84,.93,.95) · abyss-navy `#122642`/(.07,.15,.26) | glacier-glow **(0.30, 0.70, 1.00)** | satin / lacquered (wet sheen); matte on cloth |
| **wind** | pale-sky `#C9D8E2`/(.79,.85,.89) · silver-gust `#A6AEB0`/(.65,.68,.69) · sage-breeze `#B8CBA8`/(.72,.80,.66) · storm-gray `#5A6468`/(.35,.39,.41) | air-glow **(0.80, 1.00, 0.88)** | satin / matte (soft, airy) |
| **earth** | loam-brown `#6B4A2A`/(.42,.29,.16) · amber-ochre `#B8862B`/(.72,.53,.17) · stone-gray `#8A857C`/(.54,.52,.49) · moss-green `#5C6B3A`/(.36,.42,.23) | amber-glow **(0.85, 0.68, 0.28)** | worn / matte (mineral, rough); metallic on ore-veins |

**Genre anchor:** these are the genre's settled elemental color-languages — Diablo/PoE fire reads orange-red, cold/water reads cyan-blue, earth reads brown/stone/moss. Wind here absorbs air/sky flavor (only 4 slots; no separate lightning slot) → pale white-silver-sage. The aura colors are deliberately *more saturated than the body tints* so the legendary glow reads as the element even when the body palette is muted.

**Non-elemental / physical gear** (no element slot): a neutral material family — iron-steel `#6E7378`/(.43,.45,.47) · leather-tan `#7A5A3A`/(.48,.35,.23) · bone-ivory `#D8CFB8`/(.85,.81,.72) · charcoal `#2E3033`/(.18,.19,.20). **No element aura** — emission rgb defaults to the region tint (the built D7-default), scalar still rarity-driven by `EMISSION_BY_TIER`. A legendary physical item glows by *rarity* (bright metal trim) but carries no element hue.

## 3. Zone-assignment guidance (the LLM's narrow blank, per zone)

Keyed to `zone_key` (decision-grade, per §7.6) → provisional `region_key` (galadriel render pass locks the label, §7.4). The LLM picks ONE family member per present zone, guided:

| zone_key | provisional region | Pick guidance (from the dominant element's family) |
|---|---|---|
| WHITE | primary | the element's **mid-value signature** (forge-orange / deep-tide / pale-sky / loam-brown) — the largest body area; the at-a-glance element read |
| CYAN | secondary | a **complementary** family member (the darker or lighter sibling) — supporting body area |
| BLUE | metal | a **treated-metal** member + a metallic/lacquered finish (ash-gold / foam-white / silver-gust / amber-ochre) — **carries the aura** |
| YELLOW | leather | a **darker** member + worn/satin finish (coal-dark / abyss-navy / storm-gray / moss-green) — straps/bindings |
| MAGENTA | accent | the **most saturated** member — the element's loudest read; **carries the aura** |

On `whole_tint` meshes (silhouette lane, no mask): the single whole-mesh entry takes the **primary** pick; no per-zone richness (correct — the substrate has none to give).

## 4. Emission-placement rule (the six-profile §7 apex)

**The aura lands on metal (BLUE) + accent (MAGENTA) ONLY.** Cloth/primary (WHITE), secondary (CYAN), and leather (YELLOW) stay matte (scalar ≈ 0). Confirming + designing-the-intent-behind rocket's coded default (B2 verdict §3 + §4 note 1):

- **scalar** = `EMISSION_BY_TIER[tier]` (built: common 0.00 → legendary 0.75, accelerating). Per-region on `per_region`; whole-mesh on `whole_tint` (which keeps **max** emission through the degrade — built).
- **rgb** = the element **aura color** (§2). Physical/non-elemental → rgb defaults to the region tint (no hue).
- **Why metal+accent, not cloth:** glowing metal trim + accent runes read as *craftsmanship / rarity* in Synty's stylized idiom; glowing *cloth* reads as a *status-effect*, the wrong player signal (B2 verdict §3 — ENDORSED there, designed here). This is the Diablo-legendary / PoE-influence visual-discontinuity tell: the apex tier is *visually discontinuous*, and it lands where the eye reads "made special," not "afflicted."
- **PROVISIONAL gate:** placement is keyed to the provisional `region_key` label; the galadriel render pass (§7.4) locks which zone_key IS metal/accent. Until then, metal=BLUE / accent=MAGENTA is the working binding. **This is "verify at render," not a defect** (B2 verdict §4 note 1).

## 5. Multi-element + the two §6.2 residuals

- **Multi-element gear** (item carries a secondary element): the **primary element drives primary/secondary/metal/leather**; the **secondary element flavors the accent zone only** (a fire-bodied piece with a water-rune accent reads cleanly as "fire, water-touched"). One element owns the body read; the second is a grace note. Keeps silhouette legibility — the anti-pattern is a two-element body that reads as muddy neither.
- **§6.2 residual — wear model (0..1 continuous):** **DEFERRED-by-substrate.** The Synty slice surfaced no continuous wear channel; `FINISH_ENUM` already carries "worn" as a discrete finish, which covers the MVP read. Fold a continuous wear model in **only if** a later pack surfaces a wear-map (additive-nullable; no retrofit). Not authored blind.
- **§6.2 residual — overlay families:** **DEFERRED-by-substrate.** No overlay-atlas verified in the slice. Overlay-as-category is a real future lever (heraldry / faction sigils / damage-scarring) but designing the family taxonomy before the substrate shows what an overlay IS would be designing-in-the-dark (architecture §5 framing-audit). Re-open when an overlay-bearing pack is catalogued; the faction-sigil overlay is the natural first instance (composes with the content-emission faction work).

## 6. What this unblocks — and what it does NOT

**UNBLOCKS:**
- **star-lord §7.3** (constrained-LLM StyleProfile-fill) — the menu it fills *within* now exists. Fill `region_tints` per zone from the dominant element's family (§2) per the zone guidance (§3); `region_finishes` from `FINISH_ENUM` per the finish-lean; override emission rgb to the element aura color on metal+accent (§4). D7-narrow-blank: the model picks *within* the menu, never authors it. Sequenced **after** this + the elrond substrate slice (architecture §4; B2 verdict §5) — this doc is the precondition, not the build trigger.
- The §7.1 manifest node's **design-owned half** is now CLOSED. Remaining on §7.1: elrond's substrate slice (per-mesh mode + zone-count + sockets), in-flight.

**DOES NOT unblock / still gated:**
- The **galadriel render pass** (§7.4) still locks the provisional zone_key→region_key labels AND the legendary-glow placement (§4). Provisional until then.
- The **wear model + overlay families** — deferred-by-substrate (§5); not gated on a decision, gated on substrate surfacing them.
- This is the **visual** layer — explicitly NOT the content-emission pipeline (kits/factions/monsters/npcs/gear/weapons/flavortext JSON). It flavors the *render* of the gear leg; it emits nothing the sim consumes.

## 7. Sign-off

**Design-owned manifest half: AUTHORED.** The element-flavor vocabulary (per-element tint families + aura colors + finish-leans + zone guidance + emission placement) is the D7-narrow-blank menu the constrained-LLM fill picks within — curation human, selection-within model. It completes §6.2 (finish enum + emission-by-rarity already in code; wear + overlay deferred-by-substrate) and feeds the six-profile §6 element-flavoring + §7 aura apex. **Recognition → validate → commit honored:** the empirical precondition (the §7.6 slice-verified output shape + the built B2 leaf) is on disk; this menu is authored *against* that verified shape, not ahead of it.

**Signed:** gandalf (story-and-design steward), 2026-06-18.
