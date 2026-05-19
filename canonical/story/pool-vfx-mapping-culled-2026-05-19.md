# Pool × VFX Mapping — Culled-Pool Summary (Track B Re-Scoring Closure)

**Status:** **Canonical.** Filed 2026-05-19 by gandalf under autonomous-operation authority (VS2a hive-mind protocol § 4.0; pre-approval-batch authority Matt 2026-05-19). F5 Track B closure deliverable.

**Dispatch:** `agentic_orchestration/dispatches/2026-05-19-legolas-plus-gandalf-vs2a-F5-drift14-pool-vfx-catalogue-audit.md`
**F3 framework parent:** `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-19.md`
**Track A operational anchor:** `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-19.md` (legolas)
**Baseline supersedes:** `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` (2026-05-17 cull-decisions; consumed not replaced — Track B refinements are deltas against that baseline)

---

## § 0 — TL;DR (three lines)

1. **Track A verified the 156-entry manifest; Track B adjudicated 5 borderline cases.** Net manifest change: 2 entries upgraded C → D (`bone`, `web`); 3 entries kept tier with rationale-text corrections (`fume`, `blood`, `miasma`). **No `d1_status` changes; no allow-list shifts; auto-demote outcome unchanged.** Effective allow-list post-auto-demote remains **57** entries (target ~55; +2 variance acceptable per rocket math note § 2.4).
2. **The manifest is verified and stable.** Tier distribution (post-Track-B): A=29 / B=57 / C=39 / D=23 / E=8. Total `vfx_catalogue_mapping_clean = True`: 86 entries (unchanged). 3 auto-demote entries confirmed: `lantern`, `torch`, `tinder` (all fire-slot, all Tier-C object-framing, all d1_total 8–9, auto-demote to `eligible` at pool-load).
3. **Selector-side: hard-floor on `vfx_catalogue_mapping_clean` is SHIPPED** (Track 1+2 from 2026-05-17 cascade per `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`). **Track 3 (cluster-collapse logic on `canonical_pair_leak`) remains DEFERRED post-VS2a.** No new rocket dispatch needed. Drift-14 closure complete pending tag-fire `vs2a/v0.10-drift14-audit-complete`.

---

## § 1 — Adjudication outcomes for 5 borderline cases

Each adjudication applies the gandalf design lens per F3 framework § 5.2: *"would shipping this entry surface as 'X-strike with Y-VFX' produce cognitive dissonance the player would notice?"* Genre references are cited specifically (Diablo by version, PoE by skill name, Grim Dawn / Last Epoch by mechanic) per gandalf operating norms.

### § 1.1 `fume` — Tier-C confirmed; rationale text corrected

**Before:** Tier-C, `clean=False`, `eligible`, rationale: *"invisible-toxic gas; no visual register"*
**After:** Tier-C, `clean=False`, `eligible`, rationale: *"toxic-gas-cloud combat register; composite VFX achievable via Fellor smoke-vfx + chartreuse/sickly-palette shift (genre-standard poison-cloud rendering per D2/D3/PoE/Last Epoch); 'invisible' is mundane-chemistry sense not combat-visual; Tier-C confirmed gandalf-Track-B-2026-05-19"*

**Reasoning:** The original rationale text leaned toward Tier-E (*"no visual register"*) but the tier was assigned as C — internally inconsistent (legolas Track A § 5.1 surfaced this). The ARPG convention is unambiguous: poison-clouds, gas-effects, and toxic-fumes render as **visible chartreuse/sickly-green particle clouds** in every Diablo entry — D2 Necromancer Poison Nova; D3 Witch Doctor Plague of Toads / Toxic Dart cloud; D4 poison-status VFX. PoE Caustic Arrow and the entire Caustic skill family render as a visible standing poison-cloud. Last Epoch Disintegrate and Necrotic skill VFX use saturated greenish palettes on smoke-particles. The word's mundane-chemistry sense ("toxic gas you can't see") does not carry into combat-register; players read "fume" as "visible poison cloud" because that is the genre convention they have lived inside for 25+ years.

**Auto-demote impact:** None (already `eligible`).

### § 1.2 `bone` — Tier-D upgrade (C → D)

**Before:** Tier-C, `clean=False`, `eligible`, rationale: *"CULLED drift-14-biological-organic; biological-organic renders distinct from mineral earth; Tier C borderline; demoted to eligible"*
**After:** Tier-D, `clean=False`, `eligible`, rationale: *"CULLED drift-14-biological-organic; biological-organic renders categorically distinct from mineral earth (D2 Necromancer bone-spear, PoE Volatile Dead, Grim Dawn Bone Harvest all use bespoke white-fragment VFX, not modified earth-particles); coherent rendering requires death-necrotic substrate (vocab-frozen for Phase-1 P1); Tier-D upgrade gandalf-Track-B-2026-05-19; eligible status retained from biological-organic cull"*

**Reasoning:** The legolas Track A § 5.3 framing was precisely right — the manifest itself flagged "Tier C borderline" and the asymmetry with the rest of the biological-organic cull cluster (`marrow / husk / shell / chitin / scale / horn / tooth / claw` all Tier-D) is itself a tell that the original Tier-C assignment was the outlier, not the rule.

The genre evidence is unambiguous and consistent across the ARPG canon:
- **Diablo 2 Necromancer** — Bone Spear, Bone Spirit, Bone Armor, Bone Wall, Bone Prison are all rendered as **distinct white-fragment VFX**, not palette-shifted earth-effects. Blizzard committed to bone-as-its-own-substrate at the genre's founding.
- **Path of Exile** — Volatile Dead, Detonate Dead, Bone Offering, Spectral Throw (when used with bone-themed weapons): all use distinct corpse-fragment particle systems.
- **Grim Dawn** — Bone Harvest, Bone Spike: distinct bone-shard sprite work, not modified-earth.
- **Last Epoch** — Necromancer skills (Reaper Form, Aura of Decay): bone-fragments use the necrotic-particle substrate, not earth-substrate.

Across every major ARPG, bone-VFX is **categorically a separate substrate** — death/necromancy-adjacent, not earth-mineral. The white-calcified-fragment register reads to players as undead/necrotic content, not as "earth-themed combat material." Rendering bone as palette-shifted earth-particles would feel **wrong** in a way every ARPG-fluent player would immediately notice. This is the textbook Drift-14 failure mode: "X-strike with Y-VFX" cognitive dissonance.

The forward path for `bone` as a coherent pool entry is the **`shadow` substrate** (vocab-frozen for Phase-1 P1 per `canonical/story/substrate-expansion-decision-2026-05-17.md` § 7) once death-necrotic VFX coverage lands. Until then, Tier-D + eligible is correct: the entry remains in the pool for future substrate-expansion routing without surfacing through canonical-four selection.

**Auto-demote impact:** None (already `eligible` from biological-organic cull). Tier change is rubric-consistency cleanup.

### § 1.3 `blood` — Tier-C confirmed; rationale text separates VFX-axis from design-axis

**Before:** Tier-C, `clean=False`, `eligible`, rationale: *"CULLED drift-14-alternative-liquid; red-palette creates cultural-register mismatch; Tier C; demoted to eligible"*
**After:** Tier-C, `clean=False`, `eligible`, rationale: *"CULLED drift-14-alternative-liquid; (a) VFX-axis: Tier-C — palette-shift on water-VFX achievable (water-particle + saturated-red palette is genre-standard ARPG blood rendering pre-CodeManu-blood-effects-vol1 acquisition); (b) design-axis: eligible permanence is DESIGN-INTENT, not VFX-incoherence — cultural-register mismatch + Matt direction away from blood-themed seasons in demo tonal direction; rationale dimensions separated gandalf-Track-B-2026-05-19"*

**Reasoning:** Legolas Track A § 5.4 surfaced this as a two-question adjudication, which is correct. The two questions are structurally separate:

- **(a) VFX-axis Tier-C is correct under current catalogue state.** CodeManu `blood-effects-vol1` (180 blood-VFX animations) is not yet licensed; if acquired, `blood` would become Tier-A direct. Under the current catalogue, water-particle + saturated-red palette is the genre-standard cheap mapping — D3 Necromancer Blood-magic skills (Bone Spear has a blood-variant rune; Blood Rush; Siphon Blood) render through this exact pattern in vanilla VFX before bespoke blood-VFX assets land. PoE blood-themed builds (Blood Magic keystone visual cues; CI/blood interactions) use red-palette on water-particle compositing for skill-VFX coherence. The Tier-C call is correct.

- **(b) Design-axis eligible permanence is DESIGN-INTENT, not VFX-incoherence.** The 2026-05-17 cull rationale grounded the demotion in "cultural-register mismatch" — but that is a **permanent design call** about not centering blood-themed seasons in the demo's tonal direction, NOT a question of whether the VFX renders coherently. Even if CodeManu blood-effects-vol1 were acquired tomorrow and `blood` became Tier-A direct, the `eligible` status should remain because the design call is upstream of the VFX-mapping availability.

The rationale text refactor surfaces this two-axis separation for any future reader (especially if blood-VFX acquisition is later revisited): VFX-availability is a Tier-C → Tier-A pathway; design-intent eligibility is independent.

**Auto-demote impact:** None (already `eligible`).

### § 1.4 `web` — Tier-D upgrade (C → D)

**Before:** Tier-C, `clean=False`, `eligible`, rationale: *"fine-catching-suspended; composite VFX required; flex earth+wind"*
**After:** Tier-D, `clean=False`, `eligible`, rationale: *"biological-organic (spider-anatomy); strand-structure rendering crosses minor-compositing threshold per F3 framework § 2.1 — earth-VFX particles do not animate as suspended linear filaments; coherent rendering requires bespoke strand-particle motif (D2 Andariel web-prison + PoE Spider's Cage are custom sprite work, not palette-composites); Tier-D upgrade gandalf-Track-B-2026-05-19; eligible status retained"*

**Reasoning:** Legolas Track A § 5.5 framed this correctly — the distinguishing factor for Tier-C vs Tier-D per F3 framework § 2.1 is whether "composite VFX required" means *minor compositing* (sparkle overlay; texture-replacement) or *structural motif change*. Spider-web's defining visual is its **strand-geometry**: linear filaments arranged in a radial-or-grid pattern. The earth-VFX catalogue ships point-particles (stone particles; mineral debris) and dust-cloud particles. Neither animates as suspended linear strands.

Rendering "web" coherently in combat requires one of:
1. A new particle motif (strand-particles, not point-particles) — a fundamental rendering-system change, not a palette adjustment
2. Static overlay sprites (pre-rendered web-shapes layered on frame) — a different asset-type entirely from particle-VFX

Both cross from "minor compositing" (Tier-C) into "structural motif change" (Tier-D). Genre evidence:
- **Diablo 2** — Andariel's web-prison environmental hazard is a **custom sprite**, not a particle-composite. Maggot Lair web textures are tile-art, not generalizable.
- **Path of Exile** — Spider's Cage and Spider encounter environmental webs are **bespoke sprite work**, not particle systems. The spider-monster's web-attack telegraphs use dedicated VFX assets.
- **Grim Dawn** — Spider Queen encounters use custom web-sprite assets.
- **No ARPG renders "web" via palette-shifted particle effects** — the format mismatch is too severe.

The sub-category flag is `biological-organic` (spider-anatomy register) for forward-reference. Auto-demote outcome unchanged (already `eligible` from d1=7).

### § 1.5 `miasma` — Tier-C confirmed; rationale text clarifies vocab-obscure scope

**Before:** Tier-C, `clean=False`, `eligible`, rationale: *"toxic-choking-atmospheric; composite VFX required; vocab-obscure"*
**After:** Tier-C, `clean=False`, `eligible`, rationale: *"toxic-choking-atmospheric; composite VFX via Fellor smoke-vfx + sickly-greenish palette-shift; Tier-C confirmed gandalf-Track-B-2026-05-19; NOTE: 'vocab-obscure' tag is D1-axis concern (manual-override 2026-05-12 to eligible) NOT VFX-axis concern"*

**Reasoning:** Legolas Track A § 5.2 confirmed Tier-C and surfaced the `vocab-obscure` tag for clarification only. The risk surfaced is that a future reader (a Phase-1 P1 pool-addition author; a re-scoring contractor) could misread the `vocab-obscure` annotation as a VFX-mapping concern when it is in fact a D1-axis concern (vocabulary commonness — see project memory entry 2026-05-12 manual demote round 1 for `pall`/`miasma`/`rime`).

The two axes operate on different surfaces:
- **D1-axis vocab-obscure** → drives manual override of `d1_status` from `allow-list` to `eligible` (Matt judgment that average-player vocabulary doesn't cleanly cover the word).
- **VFX-axis Tier-C** → drives `vfx_catalogue_mapping_clean = False` (compositing required to render the substance-concept coherently).

Both axes happen to land `miasma` at `eligible`, but for different reasons. The rationale text now distinguishes them explicitly so the audit-trail is clean for forward readers.

**Auto-demote impact:** None.

---

## § 2 — Manifest verification — final state

### § 2.1 Tier distribution (post-Track-B)

| Tier | Pre-Track-B count | Post-Track-B count | Δ | `vfx_catalogue_mapping_clean` |
|---|---|---|---|---|
| A — Direct | 29 | 29 | 0 | True |
| B — Palette-shift | 57 | 57 | 0 | True |
| C — Composite | 41 | **39** | **−2** (`bone`, `web` → D) | False |
| D — Custom-required | 21 | **23** | **+2** | False |
| E — Non-visual | 8 | 8 | 0 | False |
| **Total clean (A+B)** | **86** | **86** | **0** | True |
| **Total blocked (C+D+E)** | **70** | **70** | **0** | False |

**Manifest integrity:** 156/156 entries verified. JSON validates. Total clean unchanged. Auto-demote outcome unchanged.

### § 2.2 Auto-demote ground-truth (unchanged from Track A)

| id | primary_slot | d1_total | tier | status |
|---|---|---|---|---|
| `lantern` | fire | 9 | C | allow-list → auto-demote → `eligible` |
| `torch` | fire | 9 | C | allow-list → auto-demote → `eligible` |
| `tinder` | fire | 8 | C | allow-list → auto-demote → `eligible` |

All three are confirmed Tier-C object-framing (carried-vessel / handheld / dry-fuel preparation); rationales correct as-filed; no Track B amendments needed.

### § 2.3 Post-auto-demote effective pool composition (unchanged)

| Status | Count | Target (rocket math note § 2.4) | Variance |
|---|---|---|---|
| allow-list (vfx-clean) | 57 | ~55 | +2 (acceptable) |
| eligible (vfx-acceptable) | 53 | — | — |
| quarantine (vfx-blocked) | 46 | — | — |
| **Total** | **156** | — | — |

The 2026-05-17 cull cascade + auto-demote logic yields a post-cull allow-list within 4% of target. No selector-side adjustment required.

### § 2.4 `canonical_pair_leak` coverage (unchanged)

21/21 entries with `canonical_pair_leak = True` confirmed by legolas Track A. Coverage is complete. No Track B amendments needed. Cluster-collapse logic (Track 3 of 2026-05-17 amendment) remains DEFERRED post-VS2a per F3 framework § 6.1.

---

## § 3 — Selector-side recommendation: NO new rocket dispatch

Per F3 framework § 6.1, the selector hard-floor on `vfx_catalogue_mapping_clean` is **already shipped** as of the 2026-05-17 implementation cascade:

- **Track 1 SHIPPED** — Pool loader auto-demote-on-load: entries with `d1_status == "allow-list"` AND `vfx_catalogue_mapping_clean == False` auto-demote to `eligible` with WARN log (`reincarnated-engine/src/reincarnated/element/pool.py` lines 73–99).
- **Track 2 SHIPPED** — `canonical_pair_leak` boolean dimension captured on all 156 manifest entries (data-layer infrastructure ready for future consumption).
- **Track 3 DEFERRED post-VS2a** — Cluster effective-selection-probability floor logic. Not required: the cull + cluster-collapse decisions (storm-cluster `gale`-kept-rest-demoted; biological-organic quarantine; alternative-liquid eligible) already structurally resolve the pressure at the data layer without needing a runtime selector mechanism. Revisit only if post-VS2a empirical regen surfaces a new cluster-pressure pattern not addressed by current cull state.

**No new rocket dispatch required from F5 Track B.** The 2026-05-19 manifest amendments are data-layer-only (`vfx_coverage_manifest.json` rationale text + 2 tier reclassifications); they ride the existing selector hard-floor without code change.

**Forward-extension recommendation (already in F3 framework § 6.2; re-stated for completeness):** All new pool entries (Phase-1 P1 substrate-expansion; future seasonal-vocabulary growth) MUST be added with paired commits — `pool.json` entry + `vfx_coverage_manifest.json` entry. The pool loader's conservative default (`missing manifest entry → vfx_catalogue_mapping_clean = False → auto-demote on next load`) is the safety net, but process discipline is the forward prescription. D15 candidate territory.

---

## § 4 — D15 forward-flag (filed via hive log REQUEST entry)

Per F3 framework § 7 forward-flag and Track B dispatch acceptance criterion: surface D15 discipline candidate to jack-ryan via hive log REQUEST entry.

**D15 candidate text (verbatim from F3 framework § 7):**
> *"Pool-vs-catalogue mapping must be scored at pool-introduction time, not deferred to ship-time. Any pool entry that will become player-visible at a downstream ship MUST be scored against the operational catalogue at pool-introduction time, not just against conceptual rubric properties."*

**Filing route:** REQUEST entry in `agentic_orchestration/hive-mind/engine-rebuild-log.md` (this dispatch's STATE entry will carry the REQUEST). Knight-rider routes to jack-ryan when capacity allows. Discipline-cluster pairing per F3 framework § 7: surface alongside D14 + D16 + R11(b) + Pattern P7 silent-drop cluster + Drift-11 sibling-cluster-sweep lesson — the cluster is at 6+ items, strong empirical basis for a coordinated jack-ryan engineering-disciplines pass.

---

## § 5 — Cross-references

- F3 framework parent: `canonical/story/d1-rubric-vfx-mapping-extension-2026-05-19.md`
- Track A operational anchor: `agentic_orchestration/research/knowledge/pool-vfx-catalogue-mapping-audit-2026-05-19.md`
- F5 dispatch: `agentic_orchestration/dispatches/2026-05-19-legolas-plus-gandalf-vs2a-F5-drift14-pool-vfx-catalogue-audit.md`
- VFX coverage manifest (amended): `reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json`
- Pool data: `reincarnated-engine/data/seasonal_elements/pool.json`
- Pool loader auto-demote logic: `reincarnated-engine/src/reincarnated/element/pool.py` lines 73–99
- 2026-05-17 cull baseline: `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md`
- Rocket selector-hardfloor dispatch (Track 1+2 shipped 2026-05-17): `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`
- Rocket math note (target ~55 allow-list): `reincarnated-engine/design/notes/drift-14-d1-substrate-native-rescore-math-2026-05-17.md`
- Drift-14 entry: `canonical/story/drift-audit.md` § Drift-14 (CLOSED per this Track B closure)
- Cipher migration architecture: `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + `canonical/story/form-bias-cadence-strategy.md` § 7.2
- Style register (score-don't-filter principle): `canonical/story/style-register.md`
- Substrate-expansion decision (Branch-A; carries Drift-14 forward to Phase-1 P1): `canonical/story/substrate-expansion-decision-2026-05-17.md`

---

## § 6 — Completion record

**Track B complete.** Filed 2026-05-19 by gandalf under autonomous-operation authority.

- [x] 5 borderline cases adjudicated (2 tier upgrades C→D; 3 rationale-text corrections)
- [x] Manifest amendments applied (`vfx_coverage_manifest.json` — 5 entries amended; JSON validates; 156 total entries)
- [x] No `d1_status` changes; no allow-list shifts; auto-demote outcome unchanged (57 effective post-demote)
- [x] Culled-pool summary doc filed (this doc)
- [x] Selector-side: no new rocket dispatch required (Track 1+2 shipped 2026-05-17; Track 3 DEFERRED post-VS2a)
- [x] D15 candidate surfaced via hive log REQUEST entry (concurrent with this filing)
- [x] Drift-14 entry update in `drift-audit.md` — status: **CLOSED**
- [x] Tag-fire request surfaced: `vs2a/v0.10-drift14-audit-complete` (Track A + B joint milestone)

**Drift-14 closure complete.** The canonical-bias residue dissolves from the per-season vocabulary surface. The rubric extension framework (F3) + audit pass (F5 Track A) + re-scoring closure (F5 Track B) + 2026-05-17 implementation cascade together close the structural gap. Future pool additions inherit the doctrine without re-derivation.

*Filed 2026-05-19 by gandalf at F5 Track B completion. F3 + F5 close Drift-14. The doctrine holds; the catalogue ships free of canonical-four bias residue. Mithrandir signs.*
