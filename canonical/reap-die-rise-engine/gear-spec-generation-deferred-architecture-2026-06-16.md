# Gear-Spec Generation System — Deferred-Architecture Recognition Record — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md` § 1. The locked architecture for the **gear-spec generation system** (the layer that turns an emitted gear item → a renderable spec: armor StyleProfile via Synty+restyle, weapon mesh via corpus select+adapt, image-to-3D for hero legendaries). This is a **recognition record**: the *substrate-independent* architecture is committed NOW; the *substrate-dependent* layer is DEFERRED behind the Synty catalogue acquisition, with a named empirical gate (§ 4) per recognition→validate→commit. Authored from the Pattern-B equipment session with Matt 2026-06-16 after the catalogue-download pole-length surfaced.

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — deferred-architecture recognition record. Authored when Matt recognized the Synty catalogue download is a long pole and ruled to hold the gear-spec generation system for later (restoring gandalf's original sequencing recommendation). Captures what to LOCK now, what to DEFER, and why deferral is cheap.
**Authority:** Matt 2026-06-16 Pattern-B equipment session — "I think you were right to initially recommend that we save the synty/meshy/godot gear specs for later." This record makes the deferral disciplined: locks the stable architecture so resumption starts from a locked frame, not a blank page.
**Companion docs:**
- `matt_notes_handoff_docs/armor-weapon-pipeline-recommendation.md` — the IMPLEMENTATION recommendation this record wraps (L0–L4 layer model; StyleProfile schema § 5; valid-values manifest § 8; parametric restyle § 4; image-to-3D tooling). That doc is the *how*; this record is the *what's-locked / what's-deferred / why-deferral-is-cheap*.
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 6 + § 7 — the primary CONSUMER: element-flavoring (palette/finish/emission/theme_seed) + the glowing-aura apex both land in the StyleProfile this system generates. The #6 capstone references this record's deferred seam.
- `canonical/story/proxy-add-design-spec-2026-06-16.md` — the Proxy-Commander #6 kit-side surface; its set is element-flavored through this system when it lands.
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` D7 — the AI-tell line, the anchor that FORCES the drive-router (§ 3.2).
- The **Synty corpus acquisition workstream** (KR dispatch, in flight 2026-06-16) — the substrate acquisition whose first SLICE is this record's resumption gate (§ 4).

---

## 0. TL;DR

The gear-spec generation system is **deferred behind the Synty catalogue download** (a multi-day long pole). Matt ruled to hold it; this record makes the hold disciplined.

**The load-bearing recognition: the seam is already clean.** The generator is **pure-downstream and generate-forward** — it consumes fields the engine already emits, plus two standalone artifacts (the valid-values manifest and the Synty catalogue). Nothing upstream changes. So **the retrofit cost of deferring is near-zero** — exactly as a Diablo item's visual is a render-time function of (base type, rarity, set-membership), never a per-instance baked field you migrate. **The trap of deferral is therefore NOT retrofit. It is re-derivation** — losing the architecture and redoing the substrate-independent design work from a blank page.

**Consequence: the right deferral touches ZERO emission-path code.** Placeholder fields / stubs in the gear-emission path would be *premature*, not prudent — every StyleProfile output field is a guess against Synty geometry we have not cracked open (the framing-audit, § 5). Instead, bank three substrate-independent artifacts (§ 6): **(1) this record** (locks the stable architecture — the big time-saver); **(2)** the valid-values manifest's *design-owned* half; **(3)** the Synty-slice verification checklist.

**Resumption gate (empirical, NOT time-passage):** the Synty SLICE catalogued (a representative few armor packs + one weapon pack in elrond's catalogue) AND the slice-verification checklist answered (§ 4).

---

## 1. What the system IS (and where its seam sits)

The gear-spec generation system is the layer **downstream of mechanical gear emission** that turns an emitted gear item into a renderable spec:

- **Armor:** Synty mesh (fixed silhouette) + a **StyleProfile** (palette / finish-per-region / emission / overlay / accents / theme_seed) — the parametric restyle layer (pipeline doc § 4). Differentiation is the restyle, NOT new geometry.
- **Weapons:** select + adapt from the ~100k-weapon corpus (common via restyle; legendary/set via image-to-3D seeded from the reference picture). The "catalogue to select from, not a generation queue" discipline (pipeline doc § 1–2).
- **Armor catalogue parity:** the Synty packs (full Synty Pass, Matt-owned) are the *armor* analogue of the weapon corpus — a catalogue to select-and-adapt from. **This dissolves the weapon/armor asymmetry** the pipeline doc § 1 names: armor stops being "reference-poor" because Synty IS the reference catalogue. Selection becomes the primary differentiation lever; restyle is the multiplier.

### 1.1 The seam — pure downstream, generate-forward

The engine **already emits** the gear item's mechanical identity: `slot`, `tier`, `element`, `profile_affinity` (the six-profile keying), `set_id`. The generator is a **pure function** of those already-emitted fields + the manifest + the catalogue → a render spec. It writes NOTHING back into the emission path.

**Generate-forward:** we visualize the *current* season's gear; we never retroactively visualize archived kits. So there is no historical visual data to migrate when the generator lands later. This is the Diablo model (item look = render-time function of base/rarity/set; nothing persisted to retrofit) and it is what makes deferral near-free.

---

## 2. The L0–L4 architecture (pipeline doc made explicit) — locked vs deferred per layer

| Layer | What it is | Status |
|---|---|---|
| **L0 — valid-values manifest** | the enumerated menu (finishes, overlay families, Synty mesh/accent IDs) both the generator and the renderer speak | **SPLIT** — design-owned half LOCKABLE now (§ 6.2); substrate half (Synty IDs) DEFERRED |
| **L1 — theme primitive** | `theme_seed` = deterministic fn(element, set_id, profile_affinity); the weapon↔armor harmonization hook | **LOCKED** (§ 3.1) — pure derivation, no persisted field |
| **L2 — drive-router** | tier → authorship mechanism (restyle / agent-or-API / image-to-3D) | **TOPOLOGY LOCKED** (§ 3.2); leaf implementations DEFERRED |
| **L3 — validation + fallback** | schema-pin, valid-values enforcement, graceful fallback on a missing asset | **PRINCIPLE LOCKED** (§ 3.3); implementation DEFERRED |
| **L4 — render-target adapters** | engine-neutral spec → Godot `.tres` / UE material | **NEUTRALITY PRINCIPLE LOCKED** (§ 3.4); adapters DEFERRED |

---

## 3. What is LOCKED now (substrate-independent — stable regardless of Synty geometry)

These six commitments do not depend on what a Synty mesh looks like. Locking them is the bank-now value: resumption starts from a locked frame.

### 3.1 The consumed-fields input contract + theme_seed (L1)

The generator reads exactly: **`{ slot, tier, element, profile_affinity, set_id, theme_seed }`**.

- `slot`, `tier`, `element`, `profile_affinity`, `set_id` are **already emitted** by generation.
- `theme_seed` is a **derived, deterministic function of (element, set_id, profile_affinity)** — NOT a persisted field. It is recomputable any time from fields the gear already carries. It is the weapon↔armor harmonization hook (pipeline doc § 6 "link weapon + armor theme"): a weapon and an armor piece sharing a `theme_seed` read as a coherent set.
- **This contract is specified here, NOT stood up as code.** Given near-zero retrofit cost, building the input helper now buys nothing and risks rotting against schema evolution before we resume. Interface in the doc; implementation deferred. The contract is additive-extensible (the proxy-schema additive-nullable pattern, cd7cba3) if the generator later needs an extra field (e.g., `mechanical_signature` for flavor-text).

### 3.2 The drive-router topology (L2) — anchored on D7

Tier dictates **authorship mode**, not a single generation choice. The router is:

| Tier | Mechanism | Why |
|---|---|---|
| Common / Magic | **algorithmic parametric restyle** (one master shader, N profiles) | volume tier; procedural-from-base is correct and cheap |
| Rare / Set | **agent-on-rules OR constrained API-LLM** (StyleProfile-fill from the manifest menu) | curation tier; the LLM fills a narrow constrained blank, never the whole |
| Legendary / Hero | **image-to-3D** (Meshy / Rodin / Tripo, seeded from the corpus reference picture) | hero tier; bounded count warrants a unique silhouette |

This is **PoE's precedent, generalized:** uniques are hand-authored visual+mechanical pairs; rares are procedural-from-base. Tier dictates authorship. The split is **forced by D7 (the AI-tell line):** raw-LLM is licensed ONLY in the Rare/Set constrained-blank role (palette/finish/overlay IDs chosen from the manifest menu), never as the player-facing whole, and never for the mechanical content. The topology is substrate-independent; only the leaf mechanisms (the actual shader, the actual image-to-3D wiring) wait for substrate.

### 3.3 Validation + fallback principle (L3)

The generator returns **only** schema-valid output: palette as concrete hex, finish as a manifest enum, overlay/accents as IDs the renderer resolves. The named failure mode (pipeline doc § 6): the model inventing an overlay ID no asset resolves to. **The manifest is the model's menu; it may pick only from it; a missing-asset resolves to a deterministic fallback, never a hard break.** Principle locked; implementation deferred.

### 3.4 Engine-neutral presentation contract (L4)

The StyleProfile is an **abstract render-intent** (palette / finish / emission / overlay / accent / theme_seed), NOT a Godot `.tres` and NOT a UE material. Render-target adapters live at the L4 boundary. **Locking neutrality now prevents Godot-specific (or UE-specific) fields from being baked into the contract prematurely** — a cheap principle that saves a retrofit if the render target shifts (the project targets both Godot and UE across surfaces).

### 3.5 Generate-forward, pure-downstream (the meta-commitment)

No emission-path change, ever. The generator is a downstream pure function. This is what makes every other deferral cheap (§ 1.1).

### 3.6 Catalogue-to-select-from discipline

Differentiation is **selection + adaptation**, not mass mesh generation. Base-mesh spread across classes FIRST (the cheapest silhouette variety), accents SECOND (the only torso/legs silhouette-breaker), restyle THIRD (the multiplier, not the sole source). Per pipeline doc § 3's differentiation budget. This is the weapon-corpus discipline applied to armor via Synty.

---

## 4. What is DEFERRED — and the empirical gate that resumes it

**Deferred (substrate-dependent — would be refuted or reshaped by the real Synty catalogue):**

- The **StyleProfile output field set** beyond the input contract — palette-*region count*, finish-*per-region* structure (depends on Synty UV reality).
- The **drive-router leaf implementations** — the master shader / restyle layer; the agent-on-rules or API-LLM StyleProfile-fill; the image-to-3D pipeline wiring.
- The **accent-attachment system** (`BoneAttachment3D`-style sockets).
- The **valid-values manifest's substrate half** — concrete Synty mesh IDs, accent refs, resolved overlay IDs.
- The **render-target adapters** (Godot `.tres` / UE material emitters).

**Resumption gate (EMPIRICAL — NOT time-passage):**

1. **The Synty SLICE is catalogued** — a representative few armor packs (spanning chest/legs/boots) + one weapon pack, in elrond's catalogue DB. NOT the full corpus; the slice is enough to design the generator against (the pipeline doc § 9 "first proof to build" discipline). The full corpus pulls in the background on the Pi warehouse.
2. **The slice-verification checklist is answered** (§ 6.3) — the two load-bearing geometry assumptions confirmed or refuted:
   - **UV-region separability** — does a Synty chest mesh expose clean, remappable UV zones (primary / trim / metal / leather)? The entire "one shader, N palette profiles" lever rests on this. If Synty bakes regions into one atlas without separation, the palette-remap multiplier weakens and the architecture shifts weight onto base-mesh-spread + accents.
   - **Accent-rig sockets** — do Synty rigs support bone-attachment for accents (belts / shoulders / capes — the only silhouette-breaker on shared torso meshes)?

When the gate resolves, the deferred layer is built per the acceptance hooks (§ 7), and the locked architecture (§ 3) is the frame it builds within.

---

## 5. The framing-audit that justifies "don't stub" (OP § 4.1)

Matt's instinct asked: placeholder fields / stubs? The three-question framing-audit answers *no* for the emission path:

- **Q1 (load-bearing assumptions a stub would depend on):** Synty mesh UV-region structure, accent-rig availability, mesh granularity. All substrate-dependent.
- **Q2 (refuting evidence surfaceable in current scope):** the slice — and we have NOT cracked open a pack. A stubbed StyleProfile output field is a guess that the first catalogued mesh could refute.
- **Q3 (refine the framing rather than execute):** YES — defer the substrate-dependent layer; lock only the substrate-independent (§ 3). Build no emission-path stub.

The audit cleanly separates the layer that is safe to commit (the *question* — the input contract, the router topology, the manifest design-half) from the layer that must wait for the *answer* (the substrate). Committing the answer-layer now is designing-in-the-dark.

---

## 6. The bank-now artifacts (ZERO code)

### 6.1 This record (#1 — the must-do)

Locks § 3. The largest time-saver: resumption from a locked frame instead of re-derivation. ~1 doc (this one).

### 6.2 The valid-values manifest's design-owned half (#2 — bank-now-or-defer)

Half the manifest (pipeline doc § 8) is OURS, not Synty's, and is fully substrate-independent: the **finish enum** (matte-cloth / burnished-bronze / lacquered-black / worn-iron / …), the **wear model** (0..1), the **emission-by-rarity mapping**, the **overlay families** as categories. Author that half; leave the substrate slots (mesh refs, accent refs, concrete overlay IDs) empty. The slice then only fills the Synty half. **gandalf-owned** (it is design vocabulary).

### 6.3 The Synty-slice verification checklist (#3 — bank-now-or-defer)

The two load-bearing geometry assumptions of § 4 step 2, written as a checklist the first catalogued pack is run against — so the slice lands *actionable* (a real question to answer) instead of "now we start thinking." Substrate-independent (it is the question, not the answer).

---

## 7. Acceptance hooks per seam — WHEN the gate resolves

These fire only after the resumption gate (§ 4). Recorded now so the deferred work is concrete-when-resumed.

### 7.1 elrond (substrate seam)
- Catalogue the Synty slice (then corpus): pack/asset metadata, **slot taxonomy** (chest/legs/boots/weapon/…), **distinctiveness scoring**, filesystem-path index, and the **`incorporation_status` license ledger** (the Synty-Pass stipulation: assets not incorporated before subscription lapse are unusable after).
- Populate the manifest's **substrate half** (§ 6.2): the Synty mesh/accent IDs.

### 7.2 rocket (generation seam)
- Build the **L2 restyle leaf**: the master `ShaderMaterial` + the StyleProfile output field set (calibrated to the verified UV-region reality, § 4 step 2).
- Build the **accent-attachment system** (if § 4 step 2 confirms rig sockets).
- Wire the **L1 theme_seed derivation** into the generator (specified § 3.1).

### 7.3 star-lord (operational / LLM seam)
- The **image-to-3D pipeline** (Legendary/Hero tier) — Meshy/Rodin/Tripo image-to-3D seeded from corpus reference (pipeline doc § 7).
- The **constrained API-LLM StyleProfile-fill** for Rare/Set (D7-narrow-blank: manifest-menu IDs only; § 3.2–3.3).

### 7.4 galadriel (visual-perception seam)
- **Distinctiveness scoring** inputs (the CV/perception side of "do two classes sharing a Synty chest mesh read as distinct?") — runs on the working subset, NOT the full Pi corpus (heavy compute).

### 7.5 drax (player-surface seam)
- Consume the **L4 render-target adapter** output (Godot `.tres` / engine-neutral spec) in the player surface; render the six-profile glowing-aura apex (six-profile doc § 7) via the StyleProfile emission fields.

### 7.6 gandalf (design seam)
- Author the manifest **design-owned half** now (§ 6.2); rule on the StyleProfile output shape once the slice verifies the UV reality; own the slot-taxonomy + distinctiveness-scoring *intent* that elrond materializes.

---

## 8. Composition with the #6 capstone — deferral-by-reference

Deferring this system **does not block** the Proxy-Commander (#6) capstone spec, because the deferral is *by reference*:

- The #6 capstone specs the **mechanical** set in full (2pc-accelerate + 4pc-T4-scope global, element-agnostic mechanically — six-profile doc § 4–5).
- Its **visual-flavor clause points at this record's deferred seam:** "element-themed via StyleProfile — deferred to the gear-spec generation system; see this record." Mechanical-complete now, visual-deferred-by-reference.

This is the same composition the six-profile doc § 6 already anticipates (mechanically element-agnostic / visually element-flavored via StyleProfile). Nothing in the #6 capstone waits on Synty.

---

## 9. Predictions registered (for empirical validation)

Per recognition→validate→commit:

1. **The retrofit cost of deferral is near-zero** — when the generator lands, the gear-emission path requires NO change (it is consumed, not modified). (Empirical gate: the generator build touches zero emission-path code.)
2. **UV-region separability holds on Synty meshes** — the first catalogued chest mesh exposes ≥ 3 cleanly remappable UV zones, making palette-remap the primary differentiation lever as § 3.6 assumes. (Empirical gate: the slice-verification checklist, § 6.3. If FALSE, the architecture shifts weight to base-mesh-spread + accents — a reshape the deferral deliberately avoids committing to blind.)
3. **Accent-rig sockets are available** — Synty rigs support bone-attachment accents, supplying the torso/legs silhouette-breaker. (Empirical gate: same checklist. If FALSE, silhouette variety leans harder on base-mesh-spread.)
4. **The slice (not the full corpus) is sufficient to design the generator** — a few representative armor packs + one weapon pack let the L2 restyle leaf and the StyleProfile output shape be specified completely. (Empirical gate: the resumed design session reaches a buildable spec from the slice alone.)

**Empirical gate (NOT time-passage):** predictions 2–3 resolve at the slice-verification checklist; predictions 1 + 4 at the resumed build.

---

## 10. Cross-references

- `matt_notes_handoff_docs/armor-weapon-pipeline-recommendation.md` — the implementation recommendation (L0–L4; StyleProfile schema § 5; manifest § 8; restyle § 4; image-to-3D § 7 + tooling).
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 6 / § 7 — the consumer (element-flavor + aura apex through the StyleProfile); the #6 capstone references this record.
- `canonical/story/proxy-add-design-spec-2026-06-16.md` — Proxy-Commander #6 kit-side surface.
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` D7 — the AI-tell line forcing the drive-router.
- The **Synty corpus acquisition workstream** (KR dispatch in flight 2026-06-16) — the substrate acquisition whose first slice is the resumption gate.
- `canonical/00-ground-state.md` § 1 — this record registers as a new CURRENT entry.

**Decisions-log:** the deferral architecture (generate-forward pure-downstream; engine-neutral contract; tier→mechanism router anchored on D7; consumed-fields input contract; resumption gated on the Synty slice + verification checklist) warrants a decisions-log entry — routed to jack-ryan (gandalf recommends; Matt approves; knight-rider drafts; jack-ryan reviews).

---

## 11. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — the locked deferred-architecture for the gear-spec generation system. The seam is clean-downstream + generate-forward, so deferral costs near-zero retrofit; the trap is re-derivation, which this record forecloses by locking the substrate-independent architecture (§ 3) and naming the empirical resumption gate (§ 4). The right deferral touches ZERO emission-path code; bank-now value is three artifacts (§ 6), of which this record is the must-do.
**Composition:** with the armor-weapon pipeline recommendation (the implementation it wraps), the six-profile Set-Gear architecture (the consumer; the #6 capstone references the deferred seam), the proxy-add spec (#6 kit-side), D7 (AI-tell line), and the in-flight Synty acquisition workstream (the substrate whose slice resumes the work).
**For:** the disciplined hold of the gear-spec generation system — locked frame, named gate, no premature stubs — so the #6 capstone proceeds now by deferral-by-reference, and the generator build resumes from architecture rather than a blank page when the Synty slice lands.

**Signed:** gandalf (story-and-design steward), 2026-06-16.
