# Density-design contract — §4.C / §4.D (D4 proxy-port unblock)

**Type:** design-spec-as-math hand-off (gandalf seam → gamora builds). Unblocks D4 proxy-port (Axis-2A wiring).
**Date:** 2026-06-13
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-13 ("author the §4.C/§4.D density-design contract that unblocks D4 for the next batch").
**Composition:** oracle `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` v1.6 §4.C/§4.D (line ~189/192 — fixture is a hard W-D prerequisite, lands BEFORE Axis-2A wiring or wiring certifies against noise) + §6.3 arity-8 ruling (proxy-density = the EXISTING Axis-2A, Bucket-A re-open, no 9th axis, no new kit) + D4 record `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`.
**Hand-off boundary:** gandalf owns density-design INTENT + acceptance/discrimination criteria (this doc). gamora owns the spawn primitive + actor-lifetime/wave-structure IMPLEMENTATION + the bin-measurement code. KR sequences. Primitive stays **default-off (brownfield-safe)** per the §5.2 amendment pattern until a kit's build wires it on.

---

## 0. What this contract unblocks (one paragraph)

D4 wires the 8-tuple's **existing Axis-2A slot** so proxy-density *discriminates* (today it is Bucket-A: built, measurement-not-yet-wired). K5 already exists as the proxy canary — D4 adds **no new reference kit**. The blocker is not the wiring; it is that **the current room cannot discriminate proxy-density** (oracle line 192). A burst encounter that ends before a standing population accrues reads NONE for the proxy kit and the solo kit alike — that is noise wearing a measurement's clothes, exactly the keystone-one-layer-up failure the D1 catch closed for cond.4. This contract specifies the **room** (§4.D) where proxy-density genuinely expresses, so the 2A wiring certifies against signal, not noise.

---

## §4.D — Sustain-for-proxy fixture (D4-CRITICAL)

### Design intent
The proxy / summoner archetype's identity is a **sustained standing population over time**, not a burst. Genre anchors:
- **Diablo II Necromancer** — skeleton army + skeletal mages + golem + revives; the army is the build.
- **Diablo III Witch Doctor** — Gargantuan / Zombie Dogs / Fetish Army; (RoS) Necromancer — Command Skeletons, Army of the Dead, skeletal mages.
- **Diablo IV Necromancer** — skeletal warriors/mages + golem + Army of the Dead.
- **PoE** — Raise Spectre, Summon Raging Spirit (SRS), Raise Zombie, Summon Skeletons, Animate Guardian — the "standing army" of the minion archetype.
- **Last Epoch** — Acolyte → Necromancer (skeletons, wraiths) / Lich; Summon Wraith / Summon Skeleton.

The discrimination point: **a standing army's contribution only registers when it has time to stand.** A room cleared in ~3s never lets the population reach steady-state, so the proxy kit and the solo kit read the same bin. Proxy-density expresses **only under sustained pressure** where the standing population reaches a plateau.

### Fixture spec (gamora implements)
- **Sustained-wave encounter** where transient duration ≪ steady-state duration (the room must *last* long enough that the army plateaus and the plateau dominates the measurement window).
- **Spawn cadence keeps pressure continuous** — no lulls that let the room clear; the population the proxy must sustain against is itself sustained.
- **Actor-lifetime is build-expressed** — the proxy's summon-duration / re-summon cadence determines the steady-state population the kit can hold. The primitive owns spawn + lifetime; the kit's build owns how many / how often.

### Measurement (the Axis-2A bin)
- Axis-2A bin = **mean active proxy count over the steady-state window** → {none / light / heavy} per the existing 2A bin definition.
- The accumulator is a per-tick active-proxy count; the bin reads the **mean over the steady-state window** (not the peak — peak rewards a burst-summon spike that isn't the archetype).

### ACCEPTANCE — discrimination-test principle (load-bearing)
The lever is **proxy-summon presence**. Vary it and the bin MUST move:
- **K5** (proxy canary) reads **HEAVY** (or LIGHT, per its build) while **K1** (solo, no proxy) reads **NONE**, robustly across the N=9 seeds.
- If K5 and K1 read the **same** bin, the fixture does **NOT** discriminate → 2A is still noise, and the room (not the wiring) is the defect. Do NOT certify 2A against a room that fails this.
- This is the same gate the oracle now puts on §6.4: wired-not-default is necessary, **discriminates** is the claim. 2A graduates from category-(a) DEFERRED only when this acceptance passes.

### Composition with Axis-5 (D5 reference kit)
The sustained room is **also** where **Axis-5 resource-economy** expresses — a standing army is a resource sink / sustain question (can the kit *afford* the population it summons?). This fixture therefore composes with **D5's resource/CC-differentiated reference kit** (`dispatches/2026-06-13-rocket-reference-kit-coverage.md`): one room, two axes exercised (2A proxy-density + 5 resource-economy). gamora and rocket coordinate the shared room; the proxy kit's resource cost is the bridge.

### Methodology-hotspot flag (OP §4.2 — Discipline-#18 refinement)
The **steady-state window boundary** (where transient ends and the plateau begins) is set **EMPIRICALLY from the proxy-population time-series AFTER the fixture runs once** — NOT pre-committed. Capture the population-over-time curve, find the plateau, set the window to the plateau. Setting the window before the first run is consultation-in-the-dark — the exact extension-hotspot failure the #18 refinement guards (window-methodology fires AFTER baseline population data lands, not before).

---

## §4.C — Cluster-density-for-cascade (FORWARD / secondary)

### Design intent
The **cascade / chain-AOE** archetype (a **7th-kit candidate, NOT in arity-8** — no cascade kit exists yet) expresses via **chain-propagation that scales with target cluster-density**. Genre anchors: PoE Chain / Fork / Arc; Diablo Chain Lightning / Nova; LE proliferation/chain. The tighter the targets pack, the more the chain accrues — density is the lever.

### Spec
- **Lever:** cluster-density (tight pack vs spread) — the `GEOMETRY_PROPAGATION` parameter.
- **Acceptance:** a cascade kit's effective output **scales with cluster-density** (more chain-hits in a tight cluster) while a **non-cascade kit reads flat** across density. Discrimination = the density lever MOVES the cascade reading and does NOT move the non-cascade reading.

### Priority
**FORWARD / secondary.** gamora builds **§4.D first** (D4-critical). §4.C is the density-room spec that *receives* a cascade kit **if/when a 7th-kit cascade candidate is promoted** (Bucket-B promotion → arity 8→9, a separate gandalf ruling). It is captured here so the room exists in design before the kit does; it does NOT widen arity-8 and does NOT gate D4.

---

## Sequencing note — load-bearing (gandalf ↔ gamora)

**gamora must capture the mobility displacement HISTOGRAM on the CURRENT movement AI BEFORE D4's movement-AI rework.** D4 is a movement-AI-at-scale rework (KR D4 record). My pending **mobility lock-edge re-calibration** (`...-mobility-lock-edge-recalibration-PENDING.md`) needs the displacement histogram from the **pre-rework** AI — if D4 lands first, the histogram reflects the new AI and the lock-edge re-cal calibrates against a moved instrument. **Order: histogram-emit → THEN D4 rework.** This is the load-bearing reason D4 is **held out of the current autonomous batch** (it joins a later batch, after the histogram is banked and gamora has consumed this contract to spec the §4.D fixture).

---

**Signed:** gandalf, 2026-06-13
**For:** the §4.C/§4.D density-design contract that unblocks D4's proxy-port — §4.D sustain-for-proxy fixture (D4-critical: room where proxy-density discriminates, K5 HEAVY vs K1 NONE, steady-state window set empirically) + §4.C cluster-density-for-cascade (forward, 7th-kit, NOT arity-8) + the histogram-before-rework sequencing constraint that holds D4 out of the current batch.
