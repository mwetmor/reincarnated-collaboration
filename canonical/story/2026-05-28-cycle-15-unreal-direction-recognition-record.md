# Cycle 15 Unreal Direction — Recognition Record (Architectural Commitments Deferred)

> **STATUS:** CURRENT (recognition load-bearing as of 2026-05-28; AMENDED 2026-05-29 — § 5 operational status updated (UE install deferred until D9 close + UE 5.7.4 FC02 failure-mode capture as operational lesson); AMENDED 2026-05-28 evening — 2.5D camera-angle pre-configuration transformer-pattern row added per Matt substance recovery; AMENDED 2026-05-28 earlier — substantial substance recovery re: transformer/pass-through architecture + asset pipeline scaffold + drax-pushback clarification + agent draft authorship + M2-install scope) — Recognition record only. Architectural commitments DEFERRED per recognition → empirical validation → commit discipline; gates on Cycle 14 D9 close + Matt + critique-pair adjudication.

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward) — written from Matt's recollection of pre-freeze sub-agent gandalf Pattern B dialogue + design-side current-context surfacing
**Status:** RECOGNITION — durable capture of direction; commitments deferred
**Authority:** Matt 2026-05-28 (this session — direction substance confirmed from prior pre-freeze Pattern B dialogue with sub-agent gandalf; recognition record authorized)

**Companion docs:**
- `canonical/29-design-overview.md` (strategic anchor; Phase 0 seasonal journey + Earth Self + form library)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D7 AI-tell line + delivery strategy)
- `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` (load-bearing Cycle 14 architecture; substrate-led design discipline)
- `agentic_orchestration/AGENTS.md` (synthetic team topology + seam-owner pattern)
- `agentic_orchestration/gandalf/notes/2026-05-28-mac-mini-freeze-diagnosis.md` (context for why this record is authored from recollection rather than direct conversation reference)

---

## 0. Why this recognition record exists

A sub-agent gandalf Pattern B dialogue with Matt on 2026-05-28 (pre-freeze; in the 06:41 → 18:30 window) surfaced a substantial Cycle 15 architectural direction. The dialogue was not captured to a durable file before the Mac mini M2 freeze (per gandalf incident note 2026-05-28-mac-mini-freeze-diagnosis.md) consumed the session. The conversation's specific architectural reasoning chain is canonically lost.

**What survives:**
- Matt's recollection of the substance (this session, post-freeze)
- Empirical evidence the direction was real: UE_5.7 install present at `/Users/Shared/Epic Games/UE_5.7` since 2026-05-04; fresh Epic Games Launcher DMG downloaded and verified post-freeze (this session)
- Current-gandalf substantive engagement with the direction from canonical context

**What does NOT survive:**
- The specific architectural reasoning chain sub-agent gandalf proposed
- Per-axis genre-lineage references that grounded the recommendation
- Any specific per-seam scope commitments

This record captures the recognition durably so future framing-audit + freeze-recovery scenarios have a substrate to read.

## 1. The recognition (substance per Matt recollection)

**Cycle 15 focus (recognition):** singular focus on shipping Reincarnated as the actual battle sim brought to life in Unreal. The Cycle 14 substrate-led engine readiness work (Path α v1 closure + Wave 5 production cascade per D9 ratified close-criterion) delivers the calibrated combat substrate; Cycle 15 brings that substrate to playable life in Unreal Engine.

**Project architecture reframing:** the long-cited project topology of `reincarnated-engine` (Python combat simulation) + `reincarnated-demo` (Pixi.js demo1) + `reincarnated-loadout` (React/Vite loadout web app) extends with a fourth canonical repo: an Unreal player client. The engine remains the calibration + simulation substrate; the player client renders the simulation as playable combat.

**New seam agent (recognition):** a new "Unreal" seam agent should be added to the synthetic engineering team to own the Unreal player-client seam. This continues the team's seam-SME pattern (each major technology surface gets a seam-owner agent who is the canonical authority for that seam).

**Operational status:** Matt is acting on the recommendation NOW (parallel to this canonical capture):
- Epic Games Launcher DMG re-downloaded and verified post-freeze (this session)
- Minimal Unreal install in progress at `/Users/Shared/Epic Games/UE_5.7` (continued from May 4 install)

## 2. Design-side reasoning (current-gandalf reconstruction from canonical context)

The direction aligns with established canonical anchors:

### 2.1 Strategic alignment with canonical 29

`canonical/29-design-overview.md` frames Reincarnated as "Phase 0 = the seasonal journey portion of a larger eventual game." The "larger eventual game" implies a player-facing playable surface beyond demo + loadout. Unreal is the natural target for that playable surface — 3D combat rendering at production polish, mature toolchain for cross-platform shipping, existing project asset structure (UE_5.7 install) already in place.

### 2.2 Engine output → player client architecture — TRANSFORMER / PASS-THROUGH PATTERN (load-bearing dev-time-savings discipline)

The substrate-led Cycle 14 architecture (per c-hybrid 2026-05-28 § 1) produces calibrated kits + encounters + per-cell semantics. That output has been validated as substrate; what's missing is the playable rendering. The Unreal seam would own:
- Engine kit-definition → Unreal gameplay data binding (Python catalogue / engine output → Unreal data tables / Blueprint structs)
- Combat playback (the engine simulates; Unreal renders the simulation as visible combat with timing, animation, hit effects)
- Player input + camera + UI (the layers that turn calibrated combat into played combat)
- Asset pipeline integration (Meshy + image-pass-through assets per existing D7 AI-tell-line discipline)

**The overarching architecture principle (recovered from pre-freeze Pattern B with Matt this session):** **a transformer / pass-through layer (app/file structure on the Python engine side) adjusts what is emitted by the game engine to fit what Unreal needs.** This is load-bearing dev-time-savings discipline. The principle: **don't replicate Python engine work on the Unreal C++ side; emit JSON from Python that Unreal C++ consumes.** Specific recovered examples:

| Domain | Don't (Unreal-side replication) | Do (transformer/pass-through) |
|---|---|---|
| **Real-time combat** | Implement combat math in Unreal C++ | Python engine emits sequenced-action JSON; Unreal C++ converts the sequenced actions to real-time playback. **Python simulation; Unreal renders the simulation** — preserves substrate-led discipline + lets Unreal stay focused on rendering excellence |
| **VFX** | Configure VFX from scratch per skill in Niagara | Buy VFX packs from Unreal Marketplace; map them to JSON as C++-readable geometry / timing / geospatial data. Engine emits "skill X at timing T at location L with magnitude M with geometry G"; Unreal renders pre-built VFX pack triggered by the JSON spec |
| **Asset pipeline** (current scaffold) | Build automated rigging + animation pipeline | **Manual scaffold:** stock-pile character + weapon reference images via GPT image generation; pass-through to Meshy (auto-rigs + auto-animates); manual import into Unreal. Pipeline-ify later when volume justifies |
| **2.5D camera-angle pre-configuration** (LOAD-BEARING — recovered 2026-05-28 evening from Matt) | Tune per-action / per-VFX exaggeration in Unreal C++ to compensate for 2.5D ARPG camera angle (Diablo-style quasi-top-down). Substantial C++ work; replicated N× across every skill / attack / VFX | Engine emits a **`2.5D`-flagged output** on 2D geometry / skill move-set data. Unreal C++ reads the flag and applies the appropriate camera-aware exaggeration profile to all flagged actions. **1× flag at Python emission vs N× per-action exaggeration mapping at Unreal C++ — leverage scales linearly with action count.** Why this is load-bearing: the 2.5D camera angle is the standard ARPG perspective (Diablo / PoE / Last Epoch / Grim Dawn all use it); sword actions + skill motions render TRUNCATED / SNUBBED at this camera angle without exaggeration; failure-mode is "combat looks competent but feels limp" — the budget-ARPG signature. Genre solutions: D2 hand-painted exaggeration baked into sprites; D3/D4 animation-curve over-exaggeration; PoE VFX dramatically larger than physical-realism warrants. Naming this at architecture layer (Python flag) vs implementation layer (per-action C++ tuning) is the correct call — leverage scales with the calibrated kit catalogue's action count |

This pattern's genre lineage is strong — Quake III's bot scripting was data-driven; StarCraft Brood War unit behavior was data-table-driven; Diablo III's rune system was per-rune data tweaks. The "Python emits JSON; Unreal consumes" architecture is established game-engineering pattern for small-team / single-developer-plus-LLMs project shape. It massively reduces Unreal-side complexity AND keeps the engine substrate as the canonical truth.

**Architectural implication:** the transformer/pass-through layer is its OWN load-bearing architectural commitment — distinct from the engine seam (rocket / gamora / star-lord) AND distinct from the Unreal seam itself. Open question: does the transformer live in the engine repo (extension of star-lord's export seam) OR in the Unreal seam repo (Python-side ETL adjacent to Unreal client) OR as its own bridge component? **Design-call territory deferred per § 4.**

### 2.3 Composition with existing seams

The synthetic team currently has 10 seam-owners. The Unreal seam adds an 11th. Composition boundaries that need design-call adjudication (DEFERRED — see § 4):

| Adjacent seam | Boundary question |
|---|---|
| **drax** (player-facing demo + loadout web) | RESOLVED (per pre-freeze sub-agent gandalf design call, recovered this session): NEW SEAM, not drax-absorption. Matt initially proposed re-purposing drax (he authored demo v1 Pixi.js); sub-agent gandalf pushed back that Unreal scope is BOTH "larger AND specifically different" — single-seam ownership would overload drax. drax stays focused on existing demo + loadout web; Unreal gets dedicated new seam. **Architecturally ratified by sub-agent gandalf pre-freeze; surfaces for Matt re-confirmation at Cycle 15 entry but the design-side call is already locked.** |
| **star-lord** (export + telemetry + LLM) | star-lord owns engine output emission; the Unreal seam owns consumption. Hand-off boundary needs explicit format spec (likely JSON catalogue → Unreal data table import) |
| **rocket** (generation) | rocket produces calibrated kits; Unreal seam renders them. No direct boundary; Unreal seam consumes downstream of rocket's output |
| **gamora** (simulation) | gamora simulates combat in Python; Unreal renders combat playback. Open question: does Unreal re-simulate (Unreal-side combat logic) or playback-render (Python-side simulation → Unreal display layer)? **Load-bearing architectural choice; design-call territory** |
| **galadriel** (visual perception) | galadriel's CV pipeline could compose with Unreal-rendered output for visual-similarity scoring against genre peers (current pipeline operates against demo + loadout screenshots; extends naturally to Unreal screenshots) |

### 2.4 Genre-lineage read

The "engine + Unreal player client" pattern has direct ARPG analog in Last Epoch (Eleventh Hour Games — Unity, but same architecture pattern: simulation core + Unity rendering), Path of Exile (Brian Weissman's custom engine + heavy rendering layer), and Grim Dawn (TQ engine + custom rendering). The genre's commercial-shipping target is consistent: the simulation substrate gets its own rendering client. Web demos serve the marketing + onboarding layer; the playable game lives in a native rendering client.

Unreal specifically over Unity: better Apple Silicon support trajectory (Unreal 5.4+ Apple Silicon native), stronger 3D character + combat lineage (Lyra sample / Combat sample frameworks), better aligned with isekai/anime visual targets (cel-shading + stylized lighting via the Lumen + Niagara pipeline). The choice is design-aligned.

### 2.5 Cycle 15 as singular focus

The recognition includes a SINGULAR focus framing for Cycle 15. Per c-hybrid 2026-05-28 + Path α work, Cycle 14 has been substrate-led engine readiness + bounded-viability calibration. That work is foundational but invisible to a player. Cycle 15 as "ship the battle sim brought to life in Unreal" reframes the project from "engine readiness" to "player-visible playable combat."

That singular framing is design-strong:
- Quality-orientation shift (per `gandalf/notes/2026-05-27-quality-orientation-shift-five-moves-package.md`) is already in cycle architecture; Cycle 15 Unreal focus operationalizes "quality > timeline" against a player-visible deliverable
- Singular focus prevents Cycle 15 scope drift (the failure mode caught at Cycle 14 multi-track expansion)
- Player-experience anchor (gandalf role definition core discipline) finally gets its target surface — combat that players actually see and feel

## 3. Naming candidates for the Unreal seam agent (deferred to Matt election)

The synthetic team uses Marvel Guardians + LotR character names. Naming candidates for the Unreal seam, organized by thematic fit:

### Marvel side (Guardians family alignment with rocket / gamora / star-lord / drax)

| Name | Fit reasoning |
|---|---|
| **Groot** | "Bringing to life" theme literal fit; Guardians family; simple memorable; "I am Groot" = embodied form-bearer; established cross-multiplatform brand recognition |
| **Mantis** | Empath; gives form to feeling; Guardians family but stretches the seam description |
| **Nebula** | Cybernetic embodiment; Guardians family; thematically darker (less player-experience-warm) |
| **Vision** | Synthezoid; mind-in-matter embodiment perfect for "engine simulation rendered visible"; NOT Guardians but Avengers — adjacent universe |

### LotR side (wizards/Maiar + Steward archetype)

| Name | Fit reasoning |
|---|---|
| **Faramir** | Steward of Gondor; careful with what he commits; loyal to design intent; embodies "the keeper of the visible realm" |
| **Beorn** | Skin-changer; embodiment-shifter; "bringing the substrate to outward form" literal fit |
| **Aulë** | The Smith Vala; maker of physical things; canonically obscure but thematically precise |
| **Tom Bombadil** | Master of his domain; gives names and form to things; eccentric and lore-loved |

**Gandalf-side lean:** **Groot** or **Faramir**. Groot for the Guardians-family-alignment + memorable + embodied-form-bearer fit; Faramir for the Steward + careful-scope + design-intent-loyal fit. Either works architecturally; the choice is more about which mythic register Matt wants the seam to occupy.

NOT a strong design-side recommendation either way; Matt's call.

## 4. Deferred architectural commitments (recognition-validate-commit discipline)

The following are explicitly DEFERRED per recognition → empirical validation → commit:

| Deferred commitment | Empirical-evidence criterion gating commit |
|---|---|
| Cycle 15 formal scope ratification (singular Unreal focus) | Cycle 14 D9 close completed (3 seasons × Gate-2 + A/B + disciplines batch + Matt tag) — surfaces Cycle 15 entry pre-scope from clean Cycle 14 closure state |
| New "Unreal" seam agent canonical authoring | Matt election on naming + scope boundaries; reincarnated-engine-vs-reincarnated-unreal repo decision; sample minimal-UE-scaffold validated as viable starting point |
| Drax-vs-Unreal-seam boundary | Sample data binding spike validates whether drax can absorb Unreal scope or whether single-seam-overload triggers new-seam carve-out |
| Engine → Unreal data binding architecture | Architecture spike: JSON catalogue export → Unreal data table import vs alternative (DataAsset / DataDriven prototyping) |
| Simulation-vs-rendering boundary (re-simulate-in-Unreal vs Python-simulation-playback-in-Unreal) | Pattern A-deep design verdict with gandalf + jack-ryan critique-pair; load-bearing architectural commitment |
| Unreal sample project scope (minimal viable scaffold) | Matt + Unreal seam agent (once authored) joint scoping pass |
| Asset pipeline composition (Meshy + image-pass-through-into-Unreal) | star-lord pipeline + Unreal seam alignment pass; D7 AI-tell-line discipline preserved at Unreal output layer |
| **Transformer / pass-through layer architecture** (engine-side ETL) | Design-call: does the transformer live in engine repo (star-lord extension), Unreal seam repo (Python-side ETL adjacent to Unreal client), or as its own bridge component? Pattern A-deep verdict with gandalf + jack-ryan + star-lord + (new) Unreal-seam-agent input |
| **Real-time-combat JSON spec** (sequenced-actions emission format) | Engine emits what? Per-tick actions? Per-skill-firing events? Per-encounter-resolution summaries? Format design call gates on which Unreal-side replay granularity supports the rendering target |
| **VFX-pack acquisition + JSON-mapping spec** | Which VFX packs to buy? What JSON schema does the engine emit to trigger pack-rendering? Design-call between gandalf (genre lineage + visual target) + galadriel (visual-similarity scoring against genre peers) + Unreal seam agent (pack-integration mechanics) |
| **2.5D camera-angle exaggeration profile spec** | What exaggeration multipliers / curves apply to which action classes (horizontal swings vs vertical chops vs ranged projectiles vs AoE bursts)? Genre-lineage-informed defaults (PoE-style VFX over-scale; D3-style animation arc exaggeration; D2-style sprite-baked exaggeration). Design-call: gandalf authors exaggeration-profile spec; galadriel CV-scores against genre peers (Diablo / PoE / Last Epoch / Grim Dawn reference screenshots); Unreal seam implements profile-driven exaggeration mapping in C++. Compose with VFX-pack design call — the same exaggeration profile applies to the pack triggers |
| **Minimal-install scope for M2 Mac mini 8GB host** | Web research (this session, post-freeze): UE 5.7 native Apple Silicon supported; SM6 + Nanite on M2; **memory: testing showed instances using over 7GB on M2 hosts — 8GB host is genuinely tight + sensitive to context (other Claude sessions + sub-agents + Unreal editor simultaneously will hit memory thrash signature like the pre-freeze incident).** Recommended minimal install scope: macOS + Windows target platforms only (deselect iOS / Android / Linux / consoles); deselect Templates and Feature Packs; deselect Engine Source (~30+ GB saved); deselect Editor Debug Symbols (~50+ GB saved). Likely landing footprint: ~30-50 GB instead of 100-180 GB full install. **Operational discipline candidate:** when Unreal editor is running, KR Mode A sub-agent invocations should sequence single-seam under R47.4 with EXPLICIT host-RAM check accounting for Unreal editor working set |
| **Agent draft authorship sequence** | RECOMMENDED: gandalf authors design recommendation at `agentic_orchestration/gandalf/recommendations/2026-05-XX-unreal-seam-agent-design-recommendation.md` (scope boundaries + persona + mythic-register naming + authority + discipline composition); KR drafts canonical `.claude/agents/<name>.md` from the recommendation; jack-ryan Gate-1 review; Matt election + ratification; KR commits canonical agent file. Each authorship step has clear seam-owner; clean separation of design vs canonical-write authorities. See § 6 for current-gandalf commitment to author the recommendation at Matt election time |

## 5. Operational status (this session post-freeze)

| Item | Status |
|---|---|
| UE_5.7 partial install (31 GB at /Users/Shared/Epic Games/UE_5.7) | **DELETED 2026-05-28 evening** — was abandoned partial install (failed at 75% on 2026-05-04); reclaimed for clean reinstall |
| Epic Games Launcher DMG | RE-DOWNLOADED + VERIFIED clean post-freeze (2026-05-28) |
| EGL backup logs (~2.1 GB on 2026-05-28 + 673 MB on 2026-05-29) | RECLAIMED (durable disk-cache pressure relief per Discipline #48 R47.2-style pattern) |
| Minimal Unreal install (Matt parallel work) | **DEFERRED until Cycle 14 D9 close per Matt 2026-05-29 sequencing call** (was: attempted twice 2026-05-29; both attempts failed at 75% with FC02 / FileConstructionFail — see § 5.1 install failure-mode capture below) |
| Unreal seam agent | NOT YET AUTHORED — deferred per § 4 |
| Cycle 14 D9 close | IN PROGRESS — Phase A1 closed 2026-05-29 (Path α v1 closure record commit `308c51b`); Phase A2 unattended cascade queued under Matt-pre-authorized gates ($50 LLM soft cap + Pattern E autonomous Gate-2 + per-workstream push + R48.4 single-seam) |
| Cycle 15 entry pre-scope | DEFERRED to Cycle 14 D9 close (Phase A2 completion → Matt v1 tag ratification) |

### 5.1 UE 5.7.4 install failure-mode capture (operational lesson for future invocations)

**Failure pattern: FC02 / IS-IN-FC02 / FileConstructionFail at 75% install completion (reproducible).**

Two install attempts on 2026-05-29; both failed at exactly 75% with identical error signature:

```
ErrorCode: FC02
FailureReasonText: A file corruption has occurred. Please try again.
FailureType: FileConstructionFail
NumFailedDownloads: 0
Retry 0/1/2/3: all FileConstructionFail with FC02
Alert code: IS-IN-FC02
```

**Critical signal:** `NumFailedDownloads: 0` — chunks downloaded fine; failure is in CHUNK CONSTRUCTION (chunk-assembly into final files; CRC validation failing at write-out). NOT a network problem.

**Root-cause hypothesis (gandalf 2026-05-29):** memory exhaustion during chunk construction on 8 GB M2 unified RAM. EGL's chunk-assembly phase needs RAM to hold chunks for CRC + write-assembly. With KR session + gandalf session + EGL itself + system processes all resident, the construction phase doesn't get sufficient headroom; writes corrupt mid-flight; CRC fails; EGL retries; same memory state; same failure.

**Architectural failure family:** same root-cause as the 2026-05-28 Mac mini freeze (memory thrash on 8 GB unified RAM under multi-process load). Different symptom (silent CRC corruption vs WindowServer wedge); same root cause. **Discipline #48 R48.4 single-seam constraint directly applies** to UE install operations on this host.

**Mitigation for future install attempts:**
- Strict R48.4 single-seam during install (close all other Claude sessions; pause KR sub-agent fan-out; close other apps)
- Delete partial install state before retry (cleared APFS metadata)
- Delete accumulated EGL logs (Disc #48 host-cache-pressure relief)
- Disable Warp AI background indexing
- **UE 5.6 fallback** if UE 5.7.4 keeps failing — 5.7.4 (Nov 2025) shipped ~6 months ago in our timeline; 5.6 has longer Apple Silicon installer maturity
- Consider VPN to different region (forces different Akamai CDN edge node) if FC02 persists even with clean host state
- Source-build path (`github.com/EpicGames/UnrealEngine`) is last-resort fallback — requires Xcode + Epic account linking + hours of compilation; heavy for 8 GB RAM host but bypasses EGL chunk-assembly entirely

**Operational composition with Discipline #48:** UE install attempts are R48.4 single-seam operations. KR sub-agent fan-out is incompatible with UE install. Sequence strictly.

## 6. What to do when this recognition record is referenced

**For sub-agent gandalf invocations at Cycle 15 entry pre-scope (any future invocation reaching this scope):** read this record at session-start; treat it as the AUTHORITATIVE recovery of the pre-freeze direction; do not require Matt to re-explain the substance. Design-call work can proceed from this anchor. **Gandalf-side commitment:** when Matt elects to fire the Unreal seam agent authoring (post Cycle 14 D9 close OR parallel-to-D9-close per Matt direction), current-gandalf authors `agentic_orchestration/gandalf/recommendations/2026-05-XX-unreal-seam-agent-design-recommendation.md` covering scope boundaries + persona authoring + mythic-register naming + authority + discipline composition; KR pulls from that recommendation to draft the canonical .claude/agents/<name>.md.

**For knight-rider at Cycle 15 entry:** the new "Unreal" seam agent authoring is an architectural-commitment-grade artifact (new .claude/agents/<name>.md + operating-procedure skill); requires Matt election + critique-pair adjudication; surfaces at Cycle 15 framing brief authoring time.

**For jack-ryan at engineering-disciplines review:** consider whether a new Discipline #48 candidate is warranted for "freeze-recovery + recognition-record-authoring" pattern. This memo + the freeze incident note + the discipline #42 pushback memo together demonstrate the recognition-record pattern as load-bearing operational practice.

**For drax (current player-facing seam):** the recognition does NOT pre-empt drax's current scope (demo + loadout web). Cycle 14 work continues unchanged; drax-vs-Unreal-seam boundary is deferred to § 4 architectural spike.

**For Matt at Cycle 14 D9 close:** this record is the durable substrate for "what Cycle 15 looks like" once D9 closes. The framing-audit + recognition-validate-commit discipline composed here gives KR a clean entry surface for Cycle 15 framing brief authoring.

---

## 7. Mythic-weight close (gandalf-side)

The work has reached its threshold. The substrate is being completed; the calibration is honest; the engine is becoming player-ready. What comes next is the rendering — the making-visible — the bringing-to-life of what has been carefully constructed.

This is the inflection point every great ARPG passes through: the moment when the system stops being "the math that makes combat work" and starts being "the world the player inhabits." D2 had it at the Beta-to-launch act-content moment; PoE had it at the Act-rework moment; Last Epoch had it at the Multiplayer-shipping moment. The infrastructure is real; the music must now play.

Reincarnated's substrate is honest. The player-experience anchor that gandalf has been holding through Cycle 14 finds its target surface in Cycle 15. The journey shapes the world; the world hosts the journey. Unreal is where the threshold is crossed.

The recognition is captured. The commitments wait on D9.

---

**Signed:** gandalf (story-and-design steward)
**For:** the durable canonical capture of the pre-freeze sub-agent gandalf + Matt Pattern B Cycle 15 Unreal direction recognition; recovery from canonical loss via Matt's recollection + current-context substantive engagement; explicit deferred-commitments framing per recognition → empirical validation → commit discipline; Cycle 15 entry pre-scope anchor for future invocations + KR framing brief authoring.
