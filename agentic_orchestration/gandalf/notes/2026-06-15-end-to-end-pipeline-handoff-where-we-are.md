# Handoff — Where we are toward the full end-to-end pipeline (engine → JSON packet → Godot)

**Type:** session handoff / orientation doc (gandalf seam).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"write a handoff session doc … listing where we are towards the full end to end engine pipeline, producing a JSON packet and reaching godot (and what major milestones are left standing in the way)."*
**Factual basis:** pipeline-state map verified against live code 2026-06-15 (engine `export/`, demo, loadout, godot spike). Survey-mode: § 1–2 report what EXISTS; § 4 lists what's MISSING. The two are kept separate.
**Companions:**
- `agentic_orchestration/gandalf/notes/2026-06-15-godot-register2-a-holds-ruling.md` — the A-holds ruling (register validated).
- `canonical/story/style-register.md` § "A-vs-B RESOLVED" — the locked register.
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` (v3) — generation-identity state.

---

## 0. TL;DR — one screen

The **engine half** of the pipeline is mature and PROVEN end-to-end: it generates balanced seasons and emits a rich, schema-versioned **JSON packet** that two web surfaces already consume. The **Godot half** — the ship-target render surface — has a **validated visual register** (the register-2 lift scored 4.50/5) but is on a **completely separate track**: it renders a *hardcoded* Synty knight from the Synty asset DB, with **no code path that ingests an engine season packet.**

**The single load-bearing gap: the engine-JSON → Godot bridge does not exist.** Everything visual we've validated sits on a hardcoded form. Until the bridge is built, generated content cannot reach the validated render surface. That bridge — not more generation, not more art — is the critical-path long-pole to "a generated season reaches Godot as a playable form."

```
GENERATE ──► VALIDATE ──► JSON PACKET ──► [ web: demo + loadout ]   ◄── EXISTS, proven
  (engine)    (sim)        (v1.0)      └─► [ GODOT ] ✗ NO BRIDGE     ◄── THE GAP
                                            register validated 4.50/5
                                            on a HARDCODED form only
```

---

## 1. The pipeline as it EXISTS today (what is)

| Stage | State | Where |
|---|---|---|
| **1. Content generation** | **EXISTS, mature.** Anchors, 8-element system, kits/classes, weapon substrate (89,839 rows), monsters, gear. Produces a full season. | engine `generation/`, `element/`, `anchor/`, `foundation/` |
| **2. Simulation + balance** | **EXISTS, mature.** Fight engine, balance loop, gauntlet sim; the **cycle-14 BALANCED pool** (`v1_scope=1` ≈ 2,499 rows, caster-enriched) is the live anchor. | engine `simulation/` |
| **3. JSON export packet** | **EXISTS, schema-versioned.** `export_season()` writes `exports/<season_id>/`: `metadata.json`, `classes.json`, `monsters.json`, `gear_pool.json`, `gauntlet_recipe.json` (+ `damage_formula.md` / `design_context.md`). Schema = Pydantic dataclasses, `EXPORT_FORMAT_VERSION = "1.0"`. **`classes.json` already carries `main_weapon` per class** — the identity-bearing surface (post weapon-as-identity). | engine `export/season_exporter.py`, `export/schemas.py` |
| **4a. Pixi demo (consumer)** | **EXISTS.** Reads the export packet directly (`loader.ts` fetches `metadata/classes/monsters/gear_pool/gauntlet_recipe`). Fed via **hand-committed static copies** (`scripts/copy-seasons.js` copies engine `exports/` → `public/seasons/`; ~12 seasons committed). **Pixi is a throwaway sketch surface — NOT the ship target.** | `reincarnated-demo/src/data/loader.ts` |
| **4b. Loadout app (consumer)** | **EXISTS, deployed (Vercel).** Reads a **DIFFERENT, older format** — the engine's *intermediate* `seasons/<id>/` per-class JSON + `manifest.json`, plus separate `cycle14-…-faction-clusters.json` / `…-wave-b-identities.json`, via build-time `import.meta.glob`. Not the flat export packet. | `reincarnated-loadout/src/hooks/useSeasonData.ts` |
| **5. Godot (ship-target render)** | **SEPARATE TRACK.** Renders a Synty modular character composed from the **Synty Sidekick asset SQLite DB** (`Proto_Side_Kick_Data`) via `addons/sidekick_creator/`. `render_lift.gd` / `render_composed.gd` **hardcode** the knight part dictionaries. **No JSON loaded; no engine-data connection.** The register-2 lift (4.50/5) was captured on THIS hardcoded form. | `reincarnated-godot/scripts/render_lift.gd`, `addons/sidekick_creator/sidekick_character.gd` |

## 2. What's been validated recently (wins to bank — the foundation is real)

- **JSON packet is real and rich (Stage 3).** Schema-versioned, two live consumers. The `main_weapon` field means the packet already speaks the weapon-as-identity language.
- **Visual register PROVEN → A holds (2026-06-15).** Cheap Synty modular geometry + the lighting/VFX/material lift = **register-2**, measured 4.50/5 (both mandatory gates at 5). The roster can ship on cheap geometry uniformly lifted; fidelity budget goes to VFX + lighting. (Ruling: `…-godot-register2-a-holds-ruling.md`.)
- **Godot pivot de-risked.** Godot 4.6 runs; the #106073 modular-import bug is empirically retired; Synty Sidekick validated as the player base ("it is perfect!"); modular **compose + auto-animation retarget cleared** on the shared Synty rig; dual-machine 8GB-Mac/RTX-PC workflow confirmed.
- **Generation identity sharpened.** Weapon-as-identity L1 committed (proxy-rooted, gate-green); the "physical-as-pseudo-element" smuggle deleted on the built path (Prediction 2 closed).

## 3. The gap, named precisely

The pipeline is **two independent dead-ends joined by nothing:**
1. `engine → export packet → web (demo/loadout)` — complete, proven, but terminates at the *web* layer (and Pixi is throwaway).
2. `Godot → Synty asset DB → hardcoded knight` — a validated *render* surface with no *data* input.

**Nothing carries an engine season packet into Godot.** No reader, no adapter, no Godot-targeted export format, no form-composition mapping from generated class data to Synty parts. "End-to-end to Godot" is exactly this missing seam. It is an **architecture + design** gap, not an art gap — the art register is already proven.

## 4. Major milestones left standing in the way (critical-path-ordered)

Grouped by track. Each: what's missing, the gate, the likely owner. **Track B is the critical-path long-pole.**

### Track A — Generation correctness (engine-side; in flight, nearly there)

| # | Milestone | State / gate | Owner |
|---|---|---|---|
| **A1** | **Weapon-as-identity Phase 2 — kit_size dissolution** (Pred 1: weapon-rooted physical kit reaches 10–13 skills *without* the sparse rage/combo/focus/stamina pools). **The recognition's HEADLINE gate.** | **FIRING NOW.** Validate-in-progress. | rocket / gandalf / jack-ryan |
| **A2** | **proxy → literal `selected_weapon.weapon_type_family` root.** Structural-honesty fix (current L1 root is an empirical-equivalent proxy, not structural). | DEFERRED "as time allows"; runtime guardrail covers the gap. No gate scheduled. | rocket |
| **A3** | **Summon runtime-label** (Pred 3: skill-composition drives summoner-vs-direct, not a coordinate bin). | DEFERRED → gamora proxy/companion pass. | gamora |

*Generation is otherwise mature — A1–A3 are refinements on a working generator, not blockers to producing a packet.*

### Track B — The engine-JSON → Godot BRIDGE (the structural long-pole; does not exist)

| # | Milestone | What's missing | Owner (likely) |
|---|---|---|---|
| **B1** | **Define the Godot-facing contract.** Does Godot read the existing `classes.json`/`monsters.json` packet directly, or does it need a Godot-targeted adapter/format? (Note the existing consumer-format fragmentation: demo reads the flat export, loadout reads the older intermediate format — the bridge is the moment to decide the canonical Godot contract.) | A design+architecture decision, unmade. | gandalf (design) + star-lord (export) + drax (Godot) |
| **B2** | **Build the Godot-side reader.** A `.gd` ingest that loads a season packet and drives composition (no JSON is read in Godot today). | The reader itself. | drax |
| **B3** | **Form-composition mapping.** Engine class data (`main_weapon`, element, role, parts) → Synty part selection + weapon-socket attachment + the lift recipe + per-skill VFX. Today the knight is hardcoded dicts; this must become data-driven off the packet. **`main_weapon` is the natural key** (weapon-as-identity makes the weapon the composition root). | The mapping layer. | drax + gandalf (design spec) |

*B1–B3 are the seam that makes the pipeline "end-to-end." Until they exist, the validated 4.50/5 render surface cannot show a single generated form.*

### Track C — Visual register completion (humanoid PROVEN; residuals)

| # | Milestone | State | Owner |
|---|---|---|---|
| **C1** | **Non-humanoid body-plans** (doc-37 Tier-2 skeletal: quadruped/serpentine/dragonling; Tier-3 non-skeletal: slime/swarm/cloud-being) — register coherence + retarget beside humanoids. | Residual long-pole; untouched by the humanoid spike. | drax + gandalf |
| **C2** | **Generative-self / Meshy pipeline** — distinct ascended forms (the gacha pillar). Must clear the same lift AND sit coherently beside Synty in-frame (the A3 rig-to-shared-skeleton crux). | Proof owed; Meshy test form not yet run. | drax + gandalf + Matt |
| **C3** | **Element → VFX coupling** — map the 8-element system onto the `GPUParticles3D` library (spike used generic fire; production needs fire-skill→fire-FX, etc.). | Deferred to a later pass per the spike guardrails. | drax + gandalf |
| **C4** | **Bestiary roster realized in-engine** — Tier-1 bipedal monsters ride the shared Synty humanoid rig (largely solved); Tier-2/3 = C1. | Partly solved by Synty family; depends on C1. | drax |

### Track D — The playable loop (beyond pure rendering; the game on top of the pipeline)

| # | Milestone | State | Owner |
|---|---|---|---|
| **D1** | **Live combat loop in Godot** — input-driven play of the actual sim (today the sim runs headless in Python; the demo plays a JS approximation). | Not started in Godot. | drax + gamora |
| **D2** | **Seasonal-journey structure** — rooms/hallways/descent + the Earth-meta-layer hub. | Design exists; not in Godot. | gandalf (design) + drax |
| **D3** | **Narrative surfaces** — Spirit Guide presence, Court of Forms, ascension moments, the AI-tell-safe onboarding. | Design exists (canonical/story); not in Godot. | gandalf + drax |

## 5. The critical path (the one-sentence answer)

To make a *generated season reach Godot as a playable form*: **Track B (the bridge) is the gating long-pole** — it is the only fully-missing structural seam. Track A (generation) is nearly done and not blocking. Track C-humanoid is proven; C-residuals (non-humanoid, generative-self) and Track D (the playable loop) extend the bridge once it exists but do not need to precede it. **Build B1→B3 and a generated form renders on the validated 4.50/5 surface for the first time.**

## 6. Cross-cutting state notes (for continuity)

- **Consumer-format fragmentation is real** (demo = flat export packet; loadout = older intermediate format). Stated as fact, not yet a decision — but B1 (the Godot contract) is the natural moment to decide whether Godot adopts the export packet or a third format, and whether the formats converge.
- **Pixi/demo1 is throwaway** — not the ship target; do not invest the bridge there. Godot is the ship surface.
- **PC node** — the RTX/32GB PC is the Godot render + high-validate leg; the 8GB Mac runs the Python engine + agent team. Retiring Unreal (the pivot) does not abandon the PC.
- **Deferred-but-tracked:** "curated world, generative self" synthesis (recognize → validate via pack-coverage survey → commit to style-register) is OPEN; the Meshy test form (C2) is the next concrete generative-self step, awaiting Matt's pick of a distinctive ascended form.

---

**Signed:** gandalf, 2026-06-15
**For:** a session handoff mapping the end-to-end pipeline — the engine half (generate → balance → schema-versioned JSON packet → two live web consumers) EXISTS and is proven; the Godot ship-surface has a measured register-2 visual register (4.50/5) but renders only a hardcoded Synty form; the single load-bearing gap is the **engine-JSON → Godot bridge** (Track B: contract + reader + form-composition mapping), which does not exist and is the critical-path long-pole, with generation-correctness (Track A) nearly done, the humanoid register proven and non-humanoid/generative-self residual (Track C), and the playable loop (Track D) the game-layer that extends the bridge once built.
