# gandalf conformance verdict — gear-spec §7.2 restyle-leaf (Wave B2) honors §7.6

**STATUS:** VERDICT (gandalf design-conformance review)
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward; author of the §7.6 ruling under review)
**Target:** engine commit `5f85014`, tag `rocket/v-gear-spec-restyle-leaf-1` (`gear_style_profile.py` + spec-note `2026-06-17-gear-spec-restyle-leaf-spec-note.md`)
**Ruling under conformance:** `canonical/story/styleprofile-output-shape-ruling-2026-06-17.md` (the §7.6 additive-nullable StyleProfile ruling — mine)
**Pairs with:** jack-ryan Gate-2 finding `agentic_orchestration/qa/findings/2026-06-17-gear-spec-restyle-leaf.md` (PASS-WITH-INFO — the ENGINEERING gate; this verdict is the DESIGN gate, non-duplicative).

---

## 0. Verdict in one line

**ENDORSE-WITH-NOTE.** The build honors the §7.6 ruling's letter AND its design spirit — the additive-nullable shape, the mesh-derived mode, the always-present fallback, the provisional-label discipline, and the unconditional accent system are all faithful. It also honors my **D7 AI-tell discipline** structurally (LLM fills narrow blanks only; structure is substrate-derived and code-enforced). The notes are **forward-looking render-pass dependencies + one schema-refinement to fold back into the ruling**, NOT rework. No PARK trigger; the tag stands.

## 1. What I reviewed (design layer — distinct from jack-ryan's gate)

jack-ryan verified the build conforms to the ruling's three rules mechanically, the schema fidelity against `synty_catalogue.db`, the ε=0.25 channel-test math, and the pure-leaf cross-seam invariant. I do **not** re-litigate those — they PASS and I concur. My review asks the design questions his gate does not:

1. Does the output shape serve the **player-facing differentiation intent** the pipeline doc set (base-mesh FIRST, accents SECOND, restyle THIRD — the multiplier)?
2. The emission curve lands in **my six-profile glowing-aura apex** (six-profile §7) — is rocket's magnitude choice coherent with the design intent there?
3. Does the build hold the **D7 AI-tell line** (human/substrate structure; LLM fills narrow blanks only)?
4. Are the provisional-label dependencies scoped so a downstream design surface won't hard-bind something that moves at the render pass?

## 2. Design conformance, rule by rule

| Ruling element | Design-intent question | Finding |
|---|---|---|
| **Additive-nullable palette** (§0) | Does it deliver the restyle MULTIPLIER without forcing the silhouette lane to carry dead fields? | ✅ One schema, two fill-densities. `per_region` carries the 5-zone richness Synty ships natively; `whole_tint` is a clean single entry. No waste, no loss — exactly the bifurcation the substrate forced. |
| **Rule 1 — mode mesh-derived** | Is the generator prevented from claiming richness it can't render? | ✅ `derive_mode()` reads `region_mask` presence; `build_palette` calls it internally — the caller cannot override mode. The discipline is structural, not advisory. |
| **Rule 2 — whole_tint always present** | Is no render path ever left untinted? | ✅ Required non-optional field; on `per_region` the `_degrade_to_whole_tint` reduction (mean tint / modal finish / **max emission**) always populates it. The "max emission survives the degrade" choice is a nice touch — the aura survives fallback rather than vanishing. |
| **Rule 3 — provisional labels** | Are the unrendered semantic labels kept from contaminating the decision-grade structure? | ✅ **Improved.** rocket split `zone_key` (decision-grade RGB-corner) from `region_key` (provisional label) — materializing my rule-3 distinction into the schema. See §4 note 1. |
| **Accent system (§3) fires unconditionally** | Does the silhouette-breaker (differentiation lever 2) deliver? | ✅ 17 verified rig sockets, L4-neutral (`BoneAttachment3D`/`SocketName`), invented sockets rejected with `ValueError`. The socket-count nuance ("12" colloquial vs 17 real) is reconciled in spec-note §1.3 — built superset-safe. See §4 note 2. |

**Differentiation-budget coherence:** the leaf delivers levers **2 (accents)** and **3 (restyle)** of the pipeline-doc §3 budget; lever 1 (base-mesh spread) is upstream selection, correctly NOT this leaf's job. The build is the multiplier-and-silhouette-breaker half, faithfully scoped.

## 3. The six-profile aura surface — the one magnitude call in my lane

The `EMISSION_BY_TIER` curve (`0.00 / 0.10 / 0.25 / 0.45 / 0.75`, Δ accelerating `0.10→0.15→0.20→0.30`) is rocket's magnitude choice, and it feeds **my** six-profile glowing-aura apex. I assess it directly:

- **Coherent — ENDORSE.** The accelerating curve makes legendary read as a **category jump, not a linear step** — this is the genre-correct rarity tell. Diablo III/IV legendary glow and PoE's influence-item visual language both make the apex tier *visually discontinuous*; a linear emission ramp would read as "slightly brighter," which is the wrong player signal. The 0.30 final jump to legendary 0.75 is the right shape.
- **The cloth-matte / metal+accent-glow assignment is the right player-feel default.** Glowing metal trim and accent runes read as craftsmanship/rarity in Synty's stylized idiom; glowing *cloth* would read as a status-effect, not a rarity tell. ENDORSE — with the render-pass caveat in §4 note 1 (the glow PLACEMENT inherits the provisional-label gate).
- **Emission rgb defaults to the region tint (D7-narrow-blank), star-lord §7.3 overrides per element.** This is exactly my D7 discipline — a sensible substrate default with the LLM filling only the narrow element-flavor blank. ENDORSE; see §4 note 3.

## 4. Notes (forward-looking — NOT rework)

1. **The `zone_key` / `region_key` split is a faithful refinement of my ruling §2 — fold it back.** My ruling §2 carried a single `region_key` doing double duty (decision-grade position + provisional label). rocket split them: `zone_key` (WHITE/CYAN/BLUE/YELLOW/MAGENTA — decision-grade) and `region_key` (primary/secondary/metal/leather/accent — provisional). This makes rule 3 *structurally* safe: downstream consumers key stable tints off `zone_key` and treat `region_key` as provisional. **Consequence I'm flagging:** the per-zone EMISSION assignment (metal+accent glow) is keyed to the provisional `region_key` label — so the legendary aura's **placement on the mesh** inherits the same render-pass gate that locks the labels (galadriel §7.4). The code couples them correctly (glow follows the label), so this is **"verify at render," not a defect** — but it means the render pass validates not just label semantics (jack-ryan INFO #3) but *where the legendary glow lands*. I will fold the zone_key/region_key split into the ruling §2 (light touch-up, §6 below).

2. **Accent authority = rig sockets, not DB slot taxonomy.** rocket correctly treats galadriel's rig extraction (17 sockets) as authoritative and the DB `is_accent` 10-slot taxonomy as a binding *hint* (concurs with jack-ryan INFO #1+#2). For my downstream design read: when star-lord §7.3 wiring fires, the accent-selection design must choose sockets from the rig vocabulary — the differentiation-lever-2 "silhouette-breaker" budget is spent in *socket space* (17 mount points), which is the right granularity.

3. **D7 line held in code.** The finish enum + invented-socket rejection + invented-finish fallback are D7 enforcement *in the implementation*, not just convention. The LLM (star-lord §7.3) can only pick from the manifest menu. This is the asset-layer analog of my D7 AI-tell discipline, enforced structurally. Strong positive — call it out so the pattern propagates to the star-lord wiring.

## 5. What this endorsement unblocks

- **star-lord §7.3** (constrained-LLM StyleProfile fill) — the field set is real and D7-safe; fill `region_tints`/`region_finishes` keyed by `zone_key`, override emission rgb per element flavor. Carry jack-ryan INFO #2 (rig-socket authority) + my §4 note 3 (D7 default) into its dispatch.
- **drax §7.5** (L4 adapter) — `classify_zone` is the render-time mirror; the adapter classifies identically. Carry my §4 note 1: do NOT hard-bind `region_key` label semantics OR the glow placement until the render pass locks them.
- These are sequenced **after** the manifest design-owned half + elrond substrate slice (per ruling §4) — this verdict does not collapse that sequencing; it confirms the leaf they build on is sound.

## 6. Ruling refinement I will apply (canonical hygiene)

I will add a one-line pointer to `styleprofile-output-shape-ruling-2026-06-17.md` §2 recording that the implementation refined the schema to a two-key form (`zone_key` decision-grade + `region_key` provisional), so downstream consumers reading the ruling see the split without re-deriving it from the code. This is a faithful refinement of rule 3, not a reversal — the ruling's design intent is unchanged.

## 7. Sign-off

**Conformance: ENDORSE-WITH-NOTE.** The B2 restyle-leaf honors the §7.6 ruling faithfully and improves it structurally; it honors the six-profile aura intent and the D7 AI-tell line. The notes are render-pass dependencies and a schema-refinement to fold back — no rework, no PARK, tag stands. The gear-spec restyle multiplier — the dominant differentiation lever — is real in code and sound.

**Signed:** gandalf, 2026-06-17. Anchors: §7.6 ruling; gear-spec architecture record §3.4/§6.2/§7.2; six-profile architecture §7; pipeline recommendation §3–§4; jack-ryan Gate-2 finding (concur).
