# Three-Run Consolidated Ruling Sheet — R1–R8

**Date:** 2026-07-22 · **Filed by:** gandalf (`RUN-CONDUCTOR` wind-down deliverable, per Matt's return request: *"explain it all to me, along with an exhaustive detailed document rulings, paired with a copy-paste ruling chunk"*)
**Queue row:** Q40 (this sheet is the terminal ruling surface for Q39's closed run + the Wave-B build-lane HALT)
**How to rule:** edit the §4 copy-paste chunk and paste it back (or answer in-chat). Every slot carries a **DEFAULT** that governs if unruled — **only R2 is BLOCKING** (the Wave-B build stays halted until it's ruled).

---

## §0 What this sheet covers

Three parallel workstreams reached their terminal surfaces on 2026-07-22:

1. **The VDM-2 → Edition-next lap** (gandalf-conducted, desirable-run pattern) — **CLOSED**, both legs complete. Rulings R1, R3, R4, R6, R7 fall out of it.
2. **The KR Wave-B Reservation/Aura build lane** (knight-rider-conducted, spec-frozen build wave) — **HALTED at the S6 cert** on a genuine design fork. Ruling R2 (and optional R8) falls out of it.
3. **The Tier-3 encounter-geometry sequel** — chartered but **UNSTARTED** by design. Ruling R5 decides how it begins.

Per-run detail: §1 here; full evidentiary record in the two review books + the KR run-state (paths in §1).

---

## §1 The three runs — what was done, what was found, where each landed

### Run 1 — VDM-2 Leg A: the corpus re-verification + v2.0 migration (CLOSED, RATIFIED)

**Book of record:** `agentic_orchestration/gandalf/notes/2026-07-22-vdm2-leg-a-review-book.md`

- **What it was:** re-emit the entire 267-kit record class (the Q34-ruled corpus-of-record: D2/GD/PoE1/PoE2/LE) through the VDM-2 field-delta schema — six new mechanical blocks (gb_delivery / gb_range / gb_motion / gb_width / gb_speed / gb_cadence) + element_primary surfacing — migrating the store v1.1 → v2.0.
- **What it did:** per-game sequential re-emission (PoE1 → D2 → GD → PoE2 → LE, single-writer discipline), each game conductor-verified before the next; completeness signal fired exactly on target (`kit_delta_t4 = 267` at LE close). Iron-law conservation held throughout (585 total / 574 curated / 19 annex-games); store md5 pinned at close.
- **What it found (headline, RB-6):** the new geometry-band vocabulary is a real, near-**orthogonal delivery-register** — it describes *how a kit's damage occupies space and time* in terms the original 14 register coords don't capture. That finding became Leg B's input.
- **Where it landed:** CLOSED + RATIFIED. Four items parked (E-1 admission → **R4**; door-arg RFC → **R3**; Edition freeze → transformed into **R1** by Leg B's outcome; §1.6 scaling-curve → **R6**).

### Run 2 — Edition-next Leg B: the pre-registered E5 refit-behind-trigger (CLOSED at §8-C — E4 remains truth)

**Book of record:** `agentic_orchestration/gandalf/notes/2026-07-22-vdm2-leg-b-review-book.md` · **Gate report:** `research/curated/atlas/2026-07-22-legb-gate-report.md` · **Binding prereg:** `gandalf/design-inputs/2026-07-22-leg-b-edition-next-preregistration.md`

- **What it was:** a pre-registered decision tree, pinned BEFORE Leg A's data existed: *does v2.0 enrichment warrant an Edition-V re-derivation?* — with the trigger, the refit recipe, the anchor test, and the fallback all committed in advance (no tuning-to-pass possible).
- **What it did, step by step:** (STEP 1) trigger — **vocabulary arm FIRED** (19 new v2.0 levels carried by ≥20 kits each; the expression arm did NOT fire). (STEP 2) element_primary **admitted as axis input** under the pre-frozen A-LB6 rule (max mechanical Cramér's V 0.555). (STEP 3) faithful refit over 265 projectable record kits, 21 MFA blocks, 87-column indicator, 17 dimensions retained by parallel analysis — then the pre-registered anchor test: Procrustes-align the candidate plane to E4's served camera on 46 shared gateA anchors.
- **What it found:** the faithful v2.0 camera sits **58.54° rotated (with reflection)** off E4, congruence **0.7836 < 0.85 → FAIL**. Verified real, not a bug: the fail reproduces three ways (no-scale / Pearson / if-scaled); the max-movers **cluster** in exactly the melee/proc families the new blocks re-weight (d2-frenzy-barb, poe1-mjolner, d2-horker, d2-auradin — a bug scatters, structure clusters); the script imports E1's derivation machinery verbatim (no method drift).
- **Where it landed:** the pre-committed **§8-C honorable fallback** — E5 NOT served, **E4 remains truth**, rotation disclosed as evidence. No amendment cycle spent (every candidate "fix" was tuning-to-pass). The strategic finding: **v2.0's enrichment is real enough that a faithful new camera cannot line up with the old one** — which turns the parked Edition-freeze decision into the camera fork, **R1**. Ruled in-run as V-26 (veto-open). Run closed, all commits pushed.

### Run 3 — KR Wave-B Reservation/Aura MVP: the build lane (HALTED at S6 cert; ~80% shipped and green)

**State of record:** `agentic_orchestration/knight-rider/wave-b-reservation-aura-run-state.md` · **Spec draft:** `gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md` · **Math note:** engine `simulation/math/waveb-reservation-aura-sim-2026-07-22.md §8`

- **What it was:** the spec-frozen build wave for the Q34(b)-ruled aura/reservation MVP — 8 forks pre-ruled by Matt (§15-R: stackable-reserved 1b, radius-gated hard-edge 2b, no-cap 3a, capstone 4c deferred, Q35-parked vehicle, re-attunement ramp 6b, instant refund 7a, banner → gamora cost read → 8a).
- **What shipped (all smoke-green, pushed):** the full pipeline ran clean — Wave-A closeout refresh → gandalf DRIFT-CRITIC (PASS-WITH-FLAGS) → jack-ryan Gate-1 (PASS-WITH-AMENDMENTS, 5 amendments all folded) → **rocket LEAD** (new sibling module `generation/aura_geometry.py`; `aura_radius_m` + `aura_reattune_ramp_s` emitted; REMOTE-TRUTH untouched; MIGRATION written; 35/35 + 65/65 smokes) → **gamora Slices 1+2** (radius gate with origin-arg design; linear ramp with reservation-paid-at-t=0 + instant 7a refund; carrier-set widen byte-identical for non-aura kits; **the Σ<0.90 activation-block guard LIVE for the first time** — ERRATA 13's dormant semantics finally have their sim site, verified by AC-7-SIM smoke; banner 8a on the E4 ground-tether trio; 14/14 smokes). Two real numerical bugs caught and fixed in-slice (IEEE-754 float edge at the Σ ceiling → 1e-9 inward bias; a reservation double-count → migrated to carrier, taxed once).
- **What the S6 cert found (the HALT):** the aura family's **benefit side is unwired**. `aura_effective_benefit()` exists and composes correctly (`full · radius_gate · ramp`) but has **zero fight-loop call sites**; `full_benefit` defaults 1.0 and is never sourced from the kit; rocket's emission carries only positional/ramp geometry — no benefit-magnitude field exists anywhere. **Only the reservation TAX is wired.** Proof: sweeping both bands across their full ranges produces byte-identical fight outcomes (<1e-9). The spec draft's §6 premise — "expressibility ✓ (the aura's stat-mod resolves)" — is **empirically false**; the benefit layer the extension assumed present was never built. Not a Slice-1/2 defect: everything built is built-true; the thing the radius *gates* is what's missing.
- **Where it landed:** terminal HALT to Matt (the Q33-D2 fork-valve is unruled, so mid-build design forks cannot route anywhere else). Bands unfinalizeable (they gate an unwired benefit); AC-9 "aura-is-felt" currently NO. The fork is **R2**.

---

## §2 The rulings

Format per ruling: what's being decided → options with real tradeoffs → conductor lean with reasons → default if unruled → what fires on ruling.

---

### R1 — The Edition-V camera fork (Path A vs Path B)

**What's being decided:** does the atlas keep its E1→E4 camera (v2.0 admitted supplementary), or do we commission a new-camera Edition-V that reflects v2.0 faithfully at the cost of breaking lineage?

**Context:** Leg B proved a faithful v2.0 derivation rotates 58.54° off E4 and fails congruence (0.7836). The old camera can *hold* the new citizens (supplementary projection has done so for Editions II–IV); it cannot *reflect what v2.0 knows* without moving. Precedent: `2026-07-16-edition3-vs-refit-candidate-1-adoption.md` — the refit-candidate-1 rotation (117°) was resolved the same way §8-C now defaults: keep the lineage camera.

**Options:**
- **(A) Path A — lineage continuity (the §8-C default, ALREADY IN FORCE).** E4 remains served truth; the six blocks + RB-6 delivery-register live as queryable *supplementary* annotation. Preserves three editions of downstream axis-semantics trust (renderers, gate rosters, island prep, axis names). Cost: the primary map does not re-shape to what v2.0 now knows.
- **(B) Path B — new-camera Edition-V.** A fresh derivation charter over v2.0, accepting the E1→E4 break: new axes, re-derived names, every downstream consumer re-onboarded. Cost: a genuine commitment-class migration; the measurement justifying it exists, but no downstream *design need* has yet surfaced that E4's axes cannot answer.

**Conductor lean: (A) Path A.** Three reasons (Leg-B book §4): (i) the E-lineage discipline — the moved camera does not anchor, so keep the trusted one; (ii) nothing is lost — the enrichment exists, informs design, and is queryable; only *re-shaping the primary map* is deferred; (iii) a rotation proves a v2.0 camera would *differ*, not that E4 is *inadequate* — Path B wants a concrete design question E4 can't answer, and none has surfaced. If one ever does, the measurement that justifies Path B is already done and filed.

**Default if unruled:** Path A (it is already in force — this ratifies, not activates).
**Fires on ruling:** (A) → nothing; the world is already in this state. (B) → gandalf ELICITOR-authors a new derivation charter for your gate (a fresh desirable-pattern run, not a refit).

---

### R2 — The aura benefit-side fork ((A) tax-only MVP vs (B) benefit-bearing archetype) — **BLOCKING**

**What's being decided:** is the Wave-B aura a reservation-economy-only mechanic for now (benefit deferred), or do we wire the benefit side and certify the archetype whole?

**Context:** everything positional/economic is built and green; the benefit the radius gates does not exist. An aura today is a pure self-imposed tax — toggling it on makes the player strictly weaker (Σ-reservation paid, mobs feel nothing).

**Options:**
- **(A) Reservation-economy-only MVP.** Certify what's built; benefit becomes a later slice/capstone. *True cost:* the S6 cert must be **amended to drop its own AC-9** ("aura-is-felt" — currently NO and unpassable); bands stay unfalsifiable; the wave ships a trap option. Worse, in a sim-balanced engine a dead mechanic **poisons calibration**: the balance loop compensates aura-carrying kits elsewhere, and when the benefit wires later those kits double-dip against stale calibration. This is precisely the *"stagnant vestigial logic that becomes ingrained and baked into the engine across time"* failure mode (Matt 2026-05-27) — the one class of debt this project has declared worse than scope creep.
- **(B) Benefit-bearing archetype.** Wire the missing layer: (i) a **gandalf benefit-model design read** (what auras grant + magnitude bands, grounded in the D2/PoE corpus the draft already cites) → (ii) **rocket** emits one benefit-magnitude field (additive, sibling to the two shipped fields, Disc #40 scaffold-tagged, MIGRATION line) → (iii) **gamora** wires `aura_effective_benefit()` into the resolution path (the function exists; it needs call sites + kit-sourced `full_benefit`) → (iv) S6 cert runs **as originally spec'd**, bands finalize. *Cost:* one bounded design read + one small dispatch pair. The expensive parts (radius gate, ramp, Σ-guard, banner) are already built and stay untouched — (B) is additive, not rework.

**Conductor lean: (B), strongly — concurring with KR's own read.** The genre ground is unambiguous: **neither genre parent ever shipped a tax-only aura.** D2's paladin auras are benefit-WITHOUT-tax (Might, Fanaticism, Holy Fire — the Auradin identity IS the benefit landing on the field); PoE's reservation economy is benefit-WITH-tax (50% mana for Hatred is the price *of the power*; the aurabot archetype exists because the benefit is real). Our current state — tax without benefit — is the inverse of D2 and the broken half of PoE. The spec's own player-experience framing (§6: a paladin aura that *reaches* allies) presupposes the benefit. And AC-9 is the cert's own bar: an aura must be *felt*. Under (B) the benefit-model read is mine to author on your word — likely shape: 3–4 benefit families (damage-amp / defense / regen / speed, the D2 quartet), magnitudes banded so reservation tax ≈ benefit value at the Σ-budget equilibrium; the read is the design input, not this paragraph.

**Default if unruled: NONE — the build stays HALTED at the S6 cert** (Disc #3.6 re-engagement criterion: cert runnable only after this ruling). This is the sheet's only blocking slot.
**Fires on ruling:** (A) → KR re-scopes the S6 cert (AC-9 amendment — itself a spec walk-back Gate-1 should see). (B) → gandalf authors the benefit-model read → KR authors the rocket-primitive + gamora-wiring dispatch pair → S6 cert → bands finalize → MVP certs whole.

---

### R3 — The door-arg RFC (GO / HOLD)

**What's being decided:** authorize gandalf to author the corpus-wide door-arg vocabulary RFC (from the ~177 attested pairs Leg A surfaced), as decision-shaped forks + leans for your ruling.

**Context:** carried from Leg A (V-21). A season-lever is commitment-adjacent, so the vocabulary is presented for YOUR ruling, not conductor-silent. Severable; blocks nothing. Deliberately NOT rushed on post-compaction context — it wants a fresh full-context authoring session.

**Conductor lean: GO** (next fresh session in my lane). **Default if unruled:** stays parked, loses nothing.
**Fires on GO:** ELICITOR-authored RFC lands in `gandalf/design-inputs/`, parks at this queue for your ruling.

---

### R4 — The E-1 admission fold (FOLD / HOLD)

**What's being decided:** admit the Edition-next admission candidates — `di-druid-pvp-cc-stack-2026` (new row) · `d2-ghost-pvp` (re-key) · LA 4 · MULTI-PROJECTILE-VOLLEY (your own docket-quality signal) — into the atlas.

**Context:** carried from Leg A; the conservative default (no admission) governed the refresh beat unruled, exactly as chartered. **Leg B's outcome changed its price:** under Path A there is no re-derivation for admissions to ride, so the FOLD is now a *supplementary mint into E4* — the same cheap Path-A mint Editions II–IV used. Lower stakes than at the beat.

**Conductor lean: FOLD** (V-5; roster §D's own text says the d2-ghost re-key "rides edition re-mint"). **Default if unruled:** no admission; 585-conservation intact.
**Fires on FOLD:** elrond supplementary-mint pass (small, bounded); iron-law counts update; catalogue-completeness footnote (the two NULL-coords kits, Leg-B book §5) rides along.

---

### R5 — The Tier-3 encounter-geometry sequel (BEGIN / PARK)

**What's being decided:** how the third chartered run starts. It is design-heavy (encounter geometry — what the corpus's spatial grammar means for OUR fight-space), so launching it cold as an autonomous run would be the ELICITOR anti-pattern: its charter needs YOUR taste in the loop before it can be a desirable-pattern run.

**Conductor lean: BEGIN — a charter-elicitation session with you present** (ELICITOR grills the unmade decisions; the charter that emerges is then conductable autonomously like Legs A/B were). **Default if unruled:** parked, unstarted.
**Fires on BEGIN:** I bring the fork surface to a session you're in; charter → prereg → run, same discipline as this lap. *(Note: your island-naming gate — "after ALL THREE runs complete" — stays unmet until this run closes.)*

---

### R6 — The §1.6 scaling-curve assumption (RATIFY routing / PARK)

**What's being decided:** route the Gear-fold's load-bearing assumption — the court×register two-axis structure presupposes a **non-parabolic-over-fixed-interval endgame scaling curve**, else it re-collapses into pure damage-multiplication — into a jack-ryan Gate-1 progression/keystone conversation.

**Context:** carried from Leg A (item d). Unchanged by Path A (the constraint governs the structure's downstream viability whether it lives as Edition axes or supplementary register).

**Conductor lean: RATIFY the routing** (it is progression design; jack-ryan DESIGN-MODE is the right first table). **Default if unruled:** stays a review-book note.
**Fires on RATIFY:** KR schedules the Gate-1 conversation; outcome feeds keystone/progression canon.

---

### R7 — The run's ruling ledger (RATIFY ALL / veto rows)

**What's being decided:** the lap made **26 in-run conductor rulings (V-1..V-26)**, each recorded veto-open in the run-state ledger (`gandalf/notes/2026-07-22-vdm2-edition-next-lap-run-state.md`) — from V-1 (run combinability) through V-20 (blood-magic honest-NULL court), V-21 (door-arg deferral shape), to V-26 (the §8-C landing itself). Reasoning-boundary calls only; every commitment-boundary item halted to you (this sheet is that halt).

**Conductor lean: RATIFY ALL.** **Default if unruled:** all stand, veto-open indefinitely (the standing pattern).
**Fires on veto:** name the row(s) — the ledger records the veto and the affected artifact reverts/amends.

---

### R8 — OPTIONAL: the Q33-D2 fork-valve (WIRE / LEAVE)

**What's being decided:** whether KR's build lanes get a **reasoning-boundary fork-valve** — on hitting a mid-build design fork, KR routes it to a gandalf sub-agent ruling instead of terminal-HALTing to you.

**Context:** the aura fork just exercised this exact seam: D2 unruled → terminal HALT. Honest nuance: **this particular fork would have escalated to you anyway** — the benefit MODEL is commitment-adjacent (it defines what an archetype IS). The valve buys speed only on forks a design steward can rule inside already-ruled canon; it must never swallow commitment-class forks.

**Conductor lean: WIRE, with the boundary explicit** (reasoning-boundary forks → gandalf sub-agent ruling, recorded veto-open; commitment-boundary forks → still terminal-HALT to you; the sub-agent's first move is classifying which kind it holds — misclassification bias goes to HALT). **Default if unruled:** unruled; terminal-HALT continues (safe, slower).
**Fires on WIRE:** KR's authority-envelope row updates (Q33-D2 closes); jack-ryan sees the amendment.

---

## §3 Parked, deliberately NOT asked here

- **GX-02 shapeshift Wave-1 build slice** — waits on the SPEC-AUTHOR docket-to-spec pass in my lane (routed 2026-07-22; no ruling needed).
- **Island family-naming one-sitting** — YOUR gate ("after all three runs complete") is unmet while Tier-3 is unstarted; prep surface stays refresh-cheap.
- **Q35 gear-meaning ELICITOR grill** — ready on your signal (live queue row; nothing new).
- **Q33-D3 (KR lane naming) + D5 (model-lever experiment)** — parked per their queue row; R8 rules D2 only.

## §4 THE COPY-PASTE RULING CHUNK

Leans pre-filled — edit any slot you disagree with, delete the rest, paste back.

```
=== THREE-RUN RULING CHUNK — 2026-07-22 ===
R1 camera fork:   PATH A     # A = E4 stays truth, v2.0 supplementary (default, already in force) | B = commission new-camera Edition-V charter
R2 aura fork:     B          # BLOCKING. A = tax-only MVP (cert amended, AC-9 dropped) | B = benefit-bearing: gandalf benefit-model read -> rocket field + gamora wiring -> S6 cert as spec'd
R3 door-arg RFC:  GO         # GO = gandalf authors it next fresh session | HOLD = stays parked
R4 E-1 admission: FOLD       # FOLD = supplementary mint into E4 (di-druid new-row, d2-ghost re-key, LA-4, MULTI-PROJECTILE-VOLLEY) | HOLD = no admission
R5 tier-3 run:    BEGIN      # BEGIN = ELICITOR charter session with me present | PARK
R6 scaling curve: RATIFY     # RATIFY = route to jack-ryan Gate-1 progression conversation | PARK
R7 ledger:        RATIFY ALL # V-1..V-26 | or: "VETO V-nn: <reason>"
R8 fork-valve:    WIRE       # optional. WIRE = KR routes reasoning-boundary design forks to gandalf sub-agent (commitment forks still HALT) | LEAVE = terminal-HALT stays
=== END CHUNK ===
```

---

## §5 RULINGS RECEIVED — Matt, 2026-07-22 (chunk returned same-day)

| Slot | Matt's word | Disposition |
|---|---|---|
| **R1** | *"Can I see a quick rendering of the new camera with the new data before I rule please?"* | **HELD-FOR-EXHIBIT** — elrond commissioned same-turn: deterministic recompute (reproduction gate: B3 0.7836 / 58.54° / reflection must reproduce exactly) → side-by-side E4 vs E5-aligned render + delta arrows + loadings, watermarked NOT-SERVED, filed `research/curated/atlas/2026-07-22-e5-candidate-exhibit/`. Exhibit-only per §8-C — no serving artifact, no store touch. Precedent format: the E3-vs-E4 ruling plates. |
| **R2** | **B** (benefit-bearing, chain as sheet'd) | **✓ RULED B.** gandalf benefit-model design read commissioned same-turn → `gandalf/design-inputs/2026-07-22-aura-benefit-model-design-read.md` → KR authors rocket-primitive + gamora-wiring dispatch pair → S6 cert as originally spec'd (AC-9 intact). Wave-B lane unblocks on the read landing. |
| **R3** | **GO** | **✓ RULED GO** — gandalf authors the door-arg RFC next fresh full-context session (deliberately not this one). |
| **R4** | **FOLD** + MPV question | **✓ RULED FOLD; execution SEQUENCED BEHIND R1.** Matt's understanding confirmed correct: MULTI-PROJECTILE-VOLLEY's kits are already atlas citizens — MPV is an E4 provisional DOCKET carried as a naming/admission INPUT, never a mint row. Actual mint scope = 5 new rows (**LA 4** = the four Lost Ark skill-Destroyer pull-kits, Edition-III Stage-A pull-7 `function=pull` + `di-druid-pvp-cc-stack-2026`) + 1 re-key (`d2-ghost-pvp`→`d2-ghost-assassin-pvp` — touches 9 minted artifacts + canon_engine_key, and roster §D says it "rides edition re-mint"). Because the re-key's mechanics differ under Path A (E4 supplementary mint + served-artifact re-key) vs Path B (rides the new derivation), the mint fires on the R1 word — one elrond pass either way. |
| **R5** | **BEGIN** (Matt-present) | **✓ RULED BEGIN** — Tier-3 encounter-geometry ELICITOR charter grill OPENED in-session same-turn (four charter forks tabled). |
| **R6** | **RATIFY** | **✓ RATIFIED** — §1.6 scaling-curve routed to a jack-ryan Gate-1 progression conversation; KR schedules on next pass. |
| **R7** | **RATIFY ALL** | **✓ RATIFIED — V-1..V-26 stand ratified** (ledger banner stamped; veto record closes). Decisions-log capture rides the next KR/jack-ryan pass. |
| **R8** | **LEAVE** | **✓ RULED LEAVE** — no fork-valve; mid-build design forks terminal-HALT to Matt **by design**. Q33-D2 closes as ruled-LEAVE (D3 remains open). |

**Island-naming gate flag (surfaced with R4):** Matt's parenthetical — *"holding off from naming any until we reach Edition 5 and create islands again"* — vs the recorded gate ("after ALL THREE runs complete"). Under Path A there **is no Edition 5**; if "Edition 5" stays the naming precondition, naming defers indefinitely. Proposed re-anchor (Matt's word wanted with his R1 ruling): islands re-cut + named after **Tier-3 completes AND R1 is resolved**, on whichever camera R1 lands.

---

**Signed:** gandalf, 2026-07-22. Sources verified first-hand: both review books (RATIFIED against elrond's artifacts), the Leg-B gate report, the binding prereg, the KR run-state, the spec draft §6 premise line, the run-state ledger V-1..V-26. Veto open on everything I ruled; nothing here re-opens what you ruled (§15-R fork set, Q34, Q38 all untouched).
