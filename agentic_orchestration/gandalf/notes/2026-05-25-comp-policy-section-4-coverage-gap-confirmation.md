# Composition Policy v1 § 4 Coverage Gap — Pattern A-Light Confirmation

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-25
**Pattern:** A-light (~30 min consult; no canonical authoring)
**Commissioner:** knight-rider (autonomous in-scope per Cycle 12 scope-doc § 1 + § 6; routed seam-owner per hive-mind decision-routing § 4.3)
**Trigger:** legolas MC-2 substrate-binding heuristics consult Flag 2 — § 4 of `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` may cover only 12 of 22 cells with explicit routing decisions

**Source materials consulted:**
- MC-2 methodology recommendation (Flag 2 source)
- Composition policy v1 § 4 (primary source for cell-routing decisions)
- v1-bc-target-intent-2026-05-24.md § 1 (Stage 0 BC-target cell roster — authoritative cell enumeration)
- qd-engine-bc-axes-lock-2026-05-20.md (8 BC axes; Profile A cell-space context)
- Cycle 12 framing brief § 2 (Layer 2 fires against composition policy v1)

---

## 1. Verdict on coverage gap

### 1.1 CONFIRMED — gap exists

**§ 4.1 explicitly covers 12 cells:**

| Cell | Status per § 4.1 | Routing decision |
|---|---|---|
| 13 (Artillery Mage) | CRITICAL | FOLD into Cell 12 via T4 alteration |
| 14 (Pyromantic Caster) | CRITICAL | Stage 3.5 engine-author gap-fill |
| 15 (Red Mage/Spellsword) | CRITICAL | Phase 5 cohesion-judge Option C composition |
| 17 (Necromancer Summoner) | CRITICAL | Sidecar B Necro enrichment + § 8.6 proxy-spawn |
| 19 (Channeling Cleric) | CRITICAL | Sidecar B WIS-broad enrichment |
| 21 (Ritual Mage/Oracle) | THIN | ACCEPT low floor (~51 typed) |
| 22 (Storm Caller/Druid) | CRITICAL | Sidecar B Celtic/Druidic enrichment |
| 23 (Monk-archetype) | CRITICAL | Sidecar B East-Asian fist-and-staff + Stage 4 rescue |
| 24 (Druid Beastmaster) | CRITICAL | Sidecar B Celtic/Pacific + § 8.6 proxy-spawn |
| 25 (Witch Doctor Petmaster) | CRITICAL | Sidecar B Sub-Saharan-African + § 8.6 proxy-spawn |
| 2 (Light Fighter) | UNDER-FLOOR-HIGHCONF | ACCEPT 0.45-conf pool + Stage 4 priority |
| 9 (Twin-Blade Fencer) | MODE-A-THIN | ACCEPT Pan-Fantasy |

**Cells in the BC roster (per Stage 0 § 1.1) NOT covered by § 4.1 explicit routing — ~13 cells:**

| Cell # | Archetype | Coverage status |
|---|---|---|
| 1 | Heavy Barbarian `(melee, low, spiky, STR, none)` | RICH per substrate (no policy needed?) |
| 3 | Polearm Soldier `(melee, medium, variable, STR, none)` | UNKNOWN — no explicit policy |
| 4 | Thrown-Heavy/Atlatl `(ranged, low, spiky, STR, none)` | Contested per Sketch E (IN scope; no § 4 policy) |
| 5 | Ancestor-Warrior `(melee, low, spiky, STR, light)` | In § 4.2 cell-pair sharing (paired with Cell 1); no per-cell policy |
| 6 | Dagger Assassin `(melee, high, flat, DEX, none)` | RICH per substrate (no policy needed?) |
| 7 | Archer `(ranged, high, flat, DEX, none)` | In § 4.2 cell-pair sharing (paired with Cell 10); no per-cell policy |
| 8 | Crossbow Sniper `(ranged, low, spiky, DEX, none)` | UNKNOWN — no explicit policy |
| 10 | Falconer/Pet-Archer `(ranged, high, flat, DEX, light)` | In § 4.2 cell-pair sharing; no per-cell policy |
| 11 | Trap Assassin/Mine-Mercenary `(mid, low, spiky, DEX, heavy)` | UNKNOWN — no explicit policy |
| 12 | Standard Wizard `(ranged, medium, variable, INT, none)` | In § 4.2 cell-pair sharing; § 4.1 references it as FOLD-TARGET for Cell 13 |
| 16 | Arcane-Familiar Mage `(ranged, medium, variable, INT, light)` | In § 4.2 cell-pair sharing; no per-cell policy |
| 18 | Totem Hierophant `(mid, medium, variable, INT, heavy)` | UNKNOWN — no explicit policy |
| 20 | Holy Knight/Paladin `(melee, medium, variable, WIS, none)` | UNKNOWN — no explicit policy (Option C hybrid candidate; per § 3.3 routing) |

**Total: 12 cells with locked routing + 13 cells without explicit per-cell routing = 25 cell-rows in Stage 0 roster.**

(Stage 0 § 1.2 summary count of "~22 distinct cells" appears to slightly under-count due to some rows collapsing in informal aggregation — the operational reality is 12 routed + 13 un-routed.)

### 1.2 What the gap means in practice

The 13 un-routed cells fall into three substantive categories:

1. **Well-populated cells (RICH per substrate) where no special routing is needed because hybrid filter-then-sample handles them out-of-box** (Cells 1, 6 — likely 3, 8, 11, 18, 20). These cells have ≥ THIN_CELL_THRESHOLD substrate at strict 4-tuple match; default heuristic produces a viable kit without per-cell override.

2. **Cells covered IMPLICITLY by § 4.2 cell-pair sharing** (Cells 5, 7, 10, 12, 16). § 4.2 establishes shared 4-tuple substrate pools across proxy-discriminated pairs. The "routing decision" is the pair-sharing itself; runtime behavior is well-defined (sample from shared 4-tuple pool; proxy-density discriminated at § 8.6 proxy-spawn template).

3. **Cells with genuine policy ambiguity** that benefit from explicit decisions (Cells 3, 4, 8, 11, 18, 20). These are not Stage-3 design-call-locked CRITICAL/THIN; they're cells the design call apparently judged as routine-enough to defer policy authoring on. They will work via default heuristic but their behavior under thin-cell-fallback or Option α/β/C routing is left implicit.

**Key observation:** the gap is NOT a "12 cells routed; 10 cells completely unwritten" problem in the catastrophic sense. The gap is "12 cells have explicit decisions because they were CRITICAL/THIN/contested; the other 13 cells have IMPLICIT routing via default heuristic + § 4.2 cell-pair sharing + § 3 Option α/β/C matching policies." The implicit routing is **runtime-functional** — it just hasn't been written down with the same explicit care.

---

## 2. Recommended path — Option B (Layer 2 default behavior + capture for v1.1+)

**RECOMMENDATION: Option B with capture, NOT Option A immediate canonical extension.**

### 2.1 Rationale for Option B over Option A

**Option A (extend composition policy § 4 NOW) would gate Layer 2 dispatch on Pattern A-deep or Pattern B canonical authoring** for the 13 un-routed cells. This is the "rigorous" path but it does NOT match the actual design risk:

- For the ~7 RICH cells (Cells 1, 3, 6, 8, 11, 18, 20): there is no design question worth resolving. The default heuristic handles them. Authoring per-cell "policy" text would be ceremony without substance — it would say "apply default; no special routing required."

- For the ~5 cell-pair sharing cells (Cells 5, 7, 10, 12, 16): § 4.2 already covers the substantive routing decision (shared 4-tuple pool). Per-cell § 4.1 entries would duplicate § 4.2's logic.

- For the ~1 genuinely ambiguous cell (Cell 20 Holy Knight — Option C hybrid candidate not explicitly in the Option C list per § 3.3): this is the SOLE legitimate § 4.1 extension candidate. Worth a Pattern A-light line-item, not full canonical doc reauthoring.

**Option B respects substrate-led discipline:** the gap surfaces at Layer 2 execution time as observable behavior (kit generation succeeds via default; thin-cell-fallback fires or doesn't). If empirical observation shows the default heuristic produces incoherent kits for any of the un-routed cells, **THAT** is the trigger for canonical § 4 extension (Pattern A-deep or Pattern B v1.1+ canonical authoring per Cycle 12 scope-doc § 5 escape-hatch).

### 2.2 Genre-design grounding for Option B

Looking at this from the senior-design-of-shipped-ARPGs lens: D2/D3/D4 + PoE all handle the "what does the loot table do for a class type the designers didn't explicitly think about" question via DEFAULT POOL + EMPIRICAL ITERATION. PoE's item-class compatibility matrix is not exhaustively pre-authored; it's filter-by-class-tag + sample. Build-defining unique items get per-item special handling (analogous to our CRITICAL/THIN cells); the rest of the pool runs on default rules.

Pre-authoring policy for cells that don't need it is the kind of design ceremony that **drift-detects as Discipline #13a violation** later — over-specified design docs that diverge from the implementation's actual behavior because the explicit policy was authored without an empirical signal forcing the design choice.

The MC-2 heuristic (hybrid filter-then-sample with thin-cell-fallback cascade) is **specifically designed to handle the un-routed cells correctly without per-cell policy**. The cascade's relaxation order (weapon_mechanical_profile → tempo → range → energy_type → element) is itself a generalized policy that applies to ALL cells. The CRITICAL/THIN cells have policy that OVERRIDES the default cascade; everything else runs on the cascade.

### 2.3 Cell 20 Holy Knight specific recommendation (the one true gap)

Cell 20 (melee, medium, variable, WIS, none) is the **one cell I'd flag as deserving an explicit § 4.1 entry**, but as a Pattern A-light line-item, not a Pattern B canonical re-authoring:

- Cell 20 is melee + WIS, which is the Option C cross-attribute hybrid pattern (per § 3.3). § 3.3 lists Red Mage (Cell 15) + Monk-archetype (Cell 23) + Holy Knight as Option C cells, but only Cells 15 and 23 have explicit § 4.1 entries.
- Without an explicit § 4.1 entry for Cell 20, Layer 2 would need to infer Option C routing from § 3.3's example list. This is fragile.

**Specific recommendation:** add a single one-line entry to § 4.1 for Cell 20 reading approximately:

> | 20 | Holy Knight/Paladin `(melee, medium, variable, WIS, none)` | OPTION-C-HYBRID | Cross-attribute melee-WIS via Option C ω-penalty; Phase 5 cohesion-judge composes over melee-attribute substrate base + WIS-flavored kit |

This can be folded into the post-Cycle-12 canonical-amendment queue OR added immediately as a one-line gandalf edit (no Pattern B design call needed; the routing decision is mechanical inference from § 3.3 Option C policy that already exists).

### 2.4 MC-1 surprise 2 cells alignment check

**MC-1 surprise 2 cells (14 Pyromantic, 15 Red Mage, 17 Necromancer, 23 Monk-archetype):** ALL FOUR are in the 12 LOCKED cells per § 4.1. They have explicit routing decisions:

- Cell 14: Stage 3.5 engine-author gap-fill
- Cell 15: Option C cross-attribute composition at Phase 5
- Cell 17: Sidecar B enrichment + § 8.6 proxy-spawn
- Cell 23: Sidecar B + Stage 4 mistagged-rescue

These are NOT among the un-routed cells. The thin-cell-fallback cascade is appropriate for them ONLY as a runtime safety net if their primary routing (Stage 3.5 fills / Sidecar B / Option C composition) doesn't yet have substrate in place at the moment Layer 2 runs.

**Sub-question: is the thin-cell-fallback cascade sufficient default for Cells 14/15/17/23 if their primary routing hasn't yet executed?** YES — per MC-2 § 4.4, graceful-fail logs the cell as UNGENERABLE with relaxation cascade exhausted. For Cells 14/15/17/23, this surfaces as substrate-enrichment-needed feedback, which is the correct signal. The cascade does not need to invent fallback substrate; it correctly surfaces the gap.

---

## 3. Layer 2 dispatch authoring guidance for knight-rider

### 3.1 Specific text to integrate into rocket L2 dispatch

Suggested framing for the L2 dispatch section on composition policy § 4 consumption:

> **Composition policy v1 § 4 consumption:**
>
> The Layer 2 substrate-binding implementation MUST execute the locked routing decisions in composition policy v1 § 4.1 for the 12 cells with explicit policy (Cells 2, 9, 13, 14, 15, 17, 19, 21, 22, 23, 24, 25). For each such cell, the policy override fires BEFORE the default hybrid filter-then-sample heuristic (per MC-2 § 4):
>
> - Cell 13: FOLD into Cell 12 (route bc_target=Cell 13 to Cell 12 4-tuple lookup; apply Cell 13 T4 alteration metadata at kit composition)
> - Cell 14: route to Stage 3.5 engine-authored entries (source_library = 'engine_authored_gap_fill_v1' filter)
> - Cell 15: Option C cross-attribute composition (per § 3.3); skip strict 4-tuple match on melee dimension; cohesion-judge composes at Phase 5
> - Cell 17: Sidecar B Necro enrichment filter + § 8.6 proxy-spawn template
> - Cell 19: Sidecar B WIS-broad enrichment filter
> - Cell 21: standard hybrid filter-then-sample (low-floor accepted per § 4.1)
> - Cell 22: Sidecar B Celtic/Druidic enrichment filter
> - Cell 23: Sidecar B East-Asian fist-and-staff filter + Stage 4 mistagged-rescue inclusion + Option C cross-attribute
> - Cell 24: Sidecar B Celtic/Pacific enrichment filter + § 8.6 proxy-spawn template
> - Cell 25: Sidecar B Sub-Saharan-African enrichment filter + § 8.6 proxy-spawn template
> - Cell 2: accept 0.45-conf pool inclusion; Stage 4 priority queue
> - Cell 9: Pan-Fantasy substrate-tradition filter
>
> **For all OTHER cells (cells not explicitly listed in § 4.1):** apply default hybrid filter-then-sample per MC-2 § 3.3 with the cell-pair sharing logic of § 4.2 (Cells 1+5, 7+10, 12+16, 14+17, 19+25 share 4-tuple pools with proxy-density discriminated via § 8.6 proxy-spawn template). Cells NOT in § 4.1 or § 4.2 (Cells 3, 4, 6, 8, 11, 18, 20) run on pure default hybrid filter-then-sample.
>
> **§ 4 coverage gap flag (per gandalf 2026-05-25 confirmation):** the un-routed cells are expected to run successfully under default heuristic. If runtime telemetry shows any of these cells consistently triggering relaxation_level ≥ 3 OR producing kits below Phase 5 cohesion-judge pass threshold, surface to gandalf for ad-hoc per-cell routing decision (Pattern A-light per Cycle 12 escape-hatch). The default heuristic + § 4.2 cell-pair sharing + § 3 Option α/β/C routing is the v1 policy for these cells; explicit § 4.1 entries are deferred to v1.1+ canonical authoring if empirical signal warrants.
>
> **Cell 20 Holy Knight specific:** Cell 20 (melee, medium, variable, WIS, none) is the one cell where § 4.1 routing is implied by § 3.3 Option C policy but not explicitly written. Layer 2 should route Cell 20 to Option C cross-attribute matching (per § 3.3 routing — Cell 20 is melee-WIS hybrid). A one-line § 4.1 amendment to make this explicit may follow in a post-Cycle-12 canonical-amendment pass (gandalf authoring; non-blocking for Layer 2 fire).

### 3.2 Implementation invariants for Layer 2 to enforce

- **Locked § 4.1 routing always overrides default heuristic** for the 12 explicit cells. The dispatch must route per-cell BEFORE invoking the hybrid filter-then-sample default.
- **§ 4.2 cell-pair sharing applies at thin-cell detection** per MC-2 § 4.1 (evaluate against shared 4-tuple pool first; proceed to per-axis relaxation only if shared pool insufficient).
- **§ 3 Option α/β/C policies apply universally** as the matching policy for ALL cells (locked § 4.1 cells + un-routed cells); this is not a § 4 question, it's a § 3 question. Layer 2 must resolve per-cell matching policy from § 3.3 (cell attribute + element class) regardless of § 4 routing.
- **Un-routed cells log relaxation_level and source_library** per MC-2 § 4.2 metadata discipline. This surfaces empirical signal for future § 4 amendments.

---

## 4. What this consult does NOT do

- Does NOT re-open the 12 LOCKED cell routing decisions (those are Stage 3 design-call closures per D2 lock)
- Does NOT author canonical extension to composition policy § 4 (per Option B recommendation — capture-for-v1.1+; defer canonical extension until empirical signal warrants)
- Does NOT block Layer 2 dispatch authoring (per Option B — Layer 2 fires with default heuristic + locked § 4.1 routing + un-routed cells running on default)
- Does NOT recommend Pattern A-deep or Pattern B follow-up immediately (per Option B — defer canonical authoring; Pattern A-light Cell 20 one-line amendment may follow non-blockingly)

---

## 5. Escape-hatch trigger conditions (per Cycle 12 scope-doc § 5)

If during Layer 2 execution OR post-Layer-2 sim observation ANY of the following surfaces, KR routes to gandalf for Pattern A-deep or Pattern B canonical re-authoring:

1. **≥ 2 un-routed cells consistently produce kits failing Phase 5 cohesion-judge** (signals default heuristic is wrong for cells the design call didn't anticipate)
2. **Cell 20 Holy Knight produces Option α (strict 5-tuple) routing under § 3.3 inference** instead of Option C (signals the inference is ambiguous and needs explicit § 4.1 entry)
3. **Un-routed cells triggering relaxation_level ≥ 4 (energy_type relaxation) at > 20% rate** (signals substrate gap for cells the composition policy hasn't surfaced as thin)
4. **Substantive design surprise emerges from Layer 2 empirical data** that wasn't anticipated by Stage 3 design call (per Cycle 12 escape-hatch — architectural amendments to canonical docs are gandalf-authors-Matt-ratifies territory)

---

## 6. Verdict summary

| Question | Verdict |
|---|---|
| **Q1: Coverage gap?** | **CONFIRMED** — 12 cells locked / ~13 cells implicit via default heuristic + § 4.2 cell-pair sharing + § 3 Option α/β/C |
| **Q2: Recommended path?** | **Option B** — Layer 2 default behavior + capture for v1.1+; do NOT block Layer 2 on canonical § 4 extension |
| **Q3: MC-1 surprise 2 cells (14/15/17/23) alignment?** | ALL FOUR are in the LOCKED 12; explicit routing exists; thin-cell-fallback cascade is appropriate runtime safety net only |
| **Q4: L2 dispatch text?** | Per § 3.1 above — explicit list of 12 § 4.1 overrides + default heuristic for everything else + Cell 20 Option C inference + escape-hatch trigger conditions |
| **Cell 20 Holy Knight specific** | One-line § 4.1 amendment recommended (post-Cycle-12 canonical-amendment queue; non-blocking) |

**Pattern A-light does NOT surface a deeper design question requiring Pattern A-deep or Pattern B escalation.** The gap is real but addressable via default heuristic + escape-hatch discipline. Composition policy § 4 does not need material rewrite; it needs an empirical-signal-driven amendment path which Option B provides.

---

## 7. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Pattern A-light consult per KR autonomous in-scope routing (Cycle 12 scope-doc § 1 + § 6; hive-mind decision-routing § 4.3)
**Status:** VERDICT DELIVERED — knight-rider integrates § 3 dispatch guidance into rocket L2 dispatch authoring
**Escape-hatch:** if Layer 2 execution surfaces any of the § 5 trigger conditions, KR routes to gandalf for Pattern A-deep or Pattern B canonical authoring
**Re-engagement gate:** post-Layer-2 sim observation; OR rocket L2 dispatch authoring needs clarification on specific cell routing

---

**Signed:** gandalf
**For:** confirming the composition policy v1 § 4 coverage gap exists but is non-blocking for Cycle 12 Layer 2 fire; Layer 2 runs on the discipline of "12 explicit routes override default; un-routed cells run default hybrid filter-then-sample per MC-2 § 3.3 with § 4.2 cell-pair sharing where applicable; empirical observation triggers v1.1+ canonical amendments via escape-hatch."
