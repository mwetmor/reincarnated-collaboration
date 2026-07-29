# PROVISION-CAL — run charter (V-PREP supersession)

> **STATUS:** CHARTERED — Matt-approved 2026-07-28 (*"Agreed on all counts. GO ahead."*) — **launch gated on §5** (the surviving §4-fork rulings).
> **Conductor:** gandalf (`RUN-CONDUCTOR`), TCP program. **Pattern:** desirable-run pattern (`operating-procedures/desirable-run-pattern.md`); fit test §7 below.
> **Supersedes:** **V-PREP** (the L7 prep cell of `2026-07-26-tcp-wind-down-and-suite-architecture-handoff.md` §2). V-PREP's stage-prep duties fold in whole; what changed is scope — the 45-row provisioning menu (TCP-55 ⑧ provision-first standing) landed after V-PREP was designed, and Matt's caveat on the C-lean (2026-07-28) is that the plugin uplift must reach **W-MUR, W-PRO, and H** *before or within* the race, not after it. Calibrating that uplift IS the prep cell now.
> **Sibling context:** the G-5 replay-trace rider was delivered to and **accepted by** the KIT-CAL-1 conductor (folded into run `KC1-2026-07-27`); the REPLAY capstone (shape C+capstone, Matt-approved in principle) fires after TCP Waves α/β and is NOT this run's scope.

---

## §0 — Intent sentence (rubric law anchor)

**Calibrate the newly provisioned plugin suite into per-row VERDICTs — does each row LOAD on our stack, and does each tool-reaching row actually REACH its target surface — so that the L7 race and L6 ladder fire against tools at their uplifted capability, without this run ever answering BETTER.**

BETTER is the race's question (L7 arms under L-J frozen contestants). This run answers only LOADS? and REACHES?. Rubric-law self-check (pattern §6-obs-3): the decidable predicates below measure loads/reaches per row; the owner's question is *"did the uplift reach all three tools"* — which is only covered if **all four tiers execute**, not just the cheap tier. A run that verdicts Tier 1 and stalls is INCOMPLETE, not partially done.

## §1 — Bounded substrate (F1: count it, list it, diff it)

1. **The 45-row provisioning menu** — `agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md` §1, FROZEN as of its commit. New discoveries are findings for a next lap, never scope growth.
2. **The ten §6 checks** in that doc — the pre-named measurements research could not settle.
3. **The Synty werewolf pack** — verified present at `/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-werewolf/` (byte-identical to Matt's 2026-07-28 download modulo `.import` sidecars).
4. **The dark-fantasy-menus pack** — copied 2026-07-28 to `/Users/admin/Games/reincarnated-godot/Assets/Synty/interface-dark-fantasy-menus/SourceFiles/` (Core / DarkFantasyMenus / FBX / Sprites / Textures; 7 platform glyph families under Core/Icons_Input).
5. **The L7-V stage scene** (crypt) + its lighting facts (CEILING-1/2, SDFGI-not-glow, R-6 camera).

## §2 — Decidable target-state (F2: the run checks "done" without Matt)

The run is DONE when ALL of:

- **T-1 · VERDICT column complete:** every one of the 45 menu rows carries exactly one verdict from the closed enum — `LOADS-CLEAN` · `LOADS-DIRTY(<what>)` · `FAILS-LOAD(<evidence>)` · `REACHES(<probe>)` · `REACHES-NOT(<probe>)` · `EXCLUDED(<menu-§5 reason>)` · `GATED-Q46` — appended to the menu doc (legolas seam) with the measurement that earned it.
- **T-2 · The ten §6 checks each resolve** to a measured answer (or `GATED-Q46` where Q46 blocks the Murzak family — checks 1, 2, 3, 8, 10).
- **T-3 · Werewolf A-PREP riders complete:** (a) FBX imports clean into the Godot project; (b) 51-bone census captured and diffed against the retarget bone-map lineage (TCP-43: 27.69° mean rest Δ methodology); (c) bone-map applicability VERDICT (retarget-ready / needs-map / blocked); (d) werewolf registered as the **L6 second body** in the ladder brief.
- **T-4 · Menus glyph-coverage answer:** does Core/Icons_Input cover L8 arm-2's **6 missing glyphs** (the purchase-fork HALT)? YES dissolves the HALT (finding filed); NO names exactly which glyphs remain missing.
- **T-5 · Stage-prep duties (ex-V-PREP):** stage scene verified render-ready at the fixed ARPG camera; fork-#1 disposition executed per Matt's ruling (§5).

## §3 — The battery (four tiers; execution order = cheapest evidence first)

| Tier | Rows | Method | Verdict path |
|---|---|---|---|
| **1 — Pure resources** (scripts/scenes/shaders/effects; GODOT-VFX-LIBRARY et al.) | menu Layer-1 resource rows | install → instantiate → **double-render + `framediff`** (§6 check 9: accumulator lockout — SDFGI is the accumulator, glow is innocent; a temporal-feedback effect re-verdicts `LOADS-DIRTY(accumulator)`) | LOADS-CLEAN / LOADS-DIRTY |
| **2 — Runtime GDExtensions** (YParticles3D, GodotIK…) | binary rows | `lipo -info` on the extracted binary (arm64 slice present?) → load under Godot **4.6.3** headless → assert extension-load line (§6 check 7) | LOADS / FAILS-LOAD |
| **3 — Editor-only plugins** (Mixamo Animation Batcher, godot-synty-tools, bone-track tools) | editor rows | install → editor boot → tool-menu presence → the named functional probe where §6 pins one (check 5: row-24 `.import` patch both ways + drax `pose_gate.gd`; check 6: Base-Locomotion fixer on `A_MOD_BL_Walk_F_Masc`, pass/fail = head-y sign) — **under L-H all-or-none:** editor tooling verdicts as *available-to-all-arms-or-none*, never as a single arm's private uplift | LOADS + probe result |
| **4 — Murzak family + Pro probe** | ten Murzak extension rows + W-PRO | **GATED-Q46 until Matt rules.** Then: install Particles (smallest) → `dotnet build` → headless boot → assert `'[Godot-MCP] plugin loaded'` (§6 check 1) → install all ten → enumerate live manifest once, settle **58-vs-63** (check 2) → the ProcessMaterial one-call probe `node-modify {"ProcessMaterial":{...}}` + independent disk read (check 3 — **this single call decides whether W-MUR has an L7 cell worth running**) → `.claude/skills` write-set fingerprint before/after (check 8, T6 telemetry) → version-bump re-read 9.2.0→9.2.2 / 0.19.1→0.20.0 (check 10, L-C). Plus **Pro:** `apply_particle_preset` called once, rendered at the fixed camera, LOOKED AT (check 4; L-B — manifests describe existence, not behaviour) | GATED-Q46 → LOADS/REACHES chain |

## §4 — Boundary laws (carried in, not invented here)

- **L-B** — the manifest is the wire; a listed tool proves nothing until called.
- **L-H** — fairness: editor-only tooling to all three arms or to none. Tier-3 verdicts are arm-agnostic by construction.
- **L-J composition (the C-lean caveat made law):** calibration completes **BEFORE** the race freeze; contestants re-freeze **post-uplift**. The race then runs frozen. Uplift-after-freeze (retro-fitting mid-race) is forbidden — that is the drift L-J exists to kill.
- **L-N** — clear instrument before recording NO: a FAILS-LOAD verdict requires the load path itself verified against a known-good control first.
- **Boundary law of the run:** LOADS?/REACHES?, never BETTER.

## §5 — Launch gates (Matt rulings owed; leans re-stated, not presumed ruled)

| Gate | Fork (handoff §4) | Status |
|---|---|---|
| **G-L1** | #1 — crypt lit as daylit court (CEILING-1, 4.66× contrast): fix in-run or hold constant | **✓ RULED (Matt 2026-07-28): FIX** — executed as the program's first measured lighting-authoring datum (→ R-PC-3) |
| **G-L2** | #2 — **Q46** Murzak cloud telemetry: local-only config / accept / park | **✓ RULED (Matt 2026-07-28): LOCAL-ONLY** (*"Ok, agreed on local only"*, after capability-cost briefing: local-only = 100% Murzak capability, zero identity transmission). Verification mandatory: packet-quiet assert during Tier-4 boot BEFORE any LOADS verdict; if the env vars fail to silence the connection, the fork REOPENS to Matt as a measured finding (→ R-PC-6) |
| **G-L3** | #4 — caster body for L7 | **✓ RULED (Matt 2026-07-28): THE WEREWOLF** — normal variant per R-PC-1; one body serves L7 caster + L6 second body + REPLAY protagonist (→ R-PC-4) |
| *(folded)* | #3 — menu bulk-ruling | Lean stands: bulk-install CLEAN+licensed; the 4 named exceptions + 5 unlicensed rows verdict `EXCLUDED(licence)` per menu §5 unless Matt rules otherwise |

**Launch state: ALL GATES CLOSED (except the standing folded lean on #3, unobjected). RUN LAUNCHED 2026-07-28.**

## §6 — Rulings ledger (veto-open, running)

- **R-PC-1 (Matt, 2026-07-28):** the werewolf body is the **normal** variant — `SM_Chr_Werewolf_01` / `SK_Chr_Werewolf_01`. The undead variant (`SK_Chr_Werewolf_Undead_01`) is **NOT used**, in any cell, on any surface.
- **R-PC-2 (Matt-confirmed, 2026-07-28):** the Synty asset home is `/Users/admin/Games/reincarnated-godot/Assets/Synty/`. Menus pack copied in; werewolf pack verified already-present and import-touched by the engine.
- **R-PC-3 (Matt, 2026-07-28):** G-L1 ruled **FIX** — the crypt lighting defect is repaired in-run and measured as the program's first lighting-authoring datum.
- **R-PC-4 (Matt, 2026-07-28):** G-L3 ruled **WEREWOLF** — the L7 caster body is the normal Synty werewolf (composing with R-PC-1). The Sidekick `.glb` stands down as caster; remains available as control/reference.
- **R-PC-5 (steward, veto-open):** `Godot Shaders Library` (menu row 4, telemetry finding T3 — in-editor downloads from godotshaders.com by design) carries a **network-quiet fence**: it never runs during a timed/measured cell; verdict annotated `LOADS-DIRTY(network-by-design)` if it otherwise loads clean.
- **R-PC-7 (conductor, in-run, veto-open):** PC-W1-A returned the ruled body **LOADS-DIRTY(missing-embedded-texture)** — `SK_Chr_Werewolf_01.fbx` references a *different pack's* `.psd` (`PolygonFantasyGothic_Texture_01.psd`); all materials import albedo-null; the pack's own 4096² PNG loads clean standalone. **Ruling: the albedo re-wire to the pack's own PNG is in-scope stage prep** (charter §2 T-5 territory), executes in the PC-T12 cell (drax), and the re-wired body re-verdicts. Reasoning-boundary: this is repair-to-spec, not content authoring.
- **R-PC-8 (conductor, in-run, veto-open):** **fact correction + scope extension of R-PC-1.** The "51 bones" datum (Synty product page) belongs to `SM_Werewolf_01.fbx` (generic-named rig, which also BUNDLES the undead *mesh* — drax finding F6). The ruled body `SK_Chr_Werewolf_01.fbx` is **52 bones, UE-named** (7 inert `ik_*` helpers). Ruling: `SM_Werewolf_01.fbx` is **EXCLUDED from the pipeline entirely** (it is not the ruled body AND it carries undead content R-PC-1 forbids); the 52-bone SK rig is THE body everywhere. Composes with R-PC-1, narrows nothing Matt ruled.
- **R-PC-6 (Matt, 2026-07-28):** **Q46 RULED: LOCAL-ONLY.** The Murzak core addon runs with the four launch env vars suppressing the `wss://ai-game.dev` cloud connection; loopback transport only. **Verification is part of the ruling:** a packet-quiet assert during the Tier-4 boot precedes any Tier-4 LOADS verdict; a failed silence-check reopens the fork to Matt as a measured finding, never a silent acceptance. Capability basis confirmed pre-ruling: extensions are transport-agnostic (telemetry finding T2) — local-only forfeits nothing Murzak-compatible. T7 rider composes: `DOTNET_CLI_HOME` redirect per the known `env.sh` fix before the ten `dotnet restore` operations.

## §7 — Fit test + fallback + Matt interface

- **F1 enumerable:** 45 rows + 10 checks + 4 riders — countable, listable, diffable. YES.
- **F2 decidable:** every target in §2 is a measurement or a closed-enum verdict. YES.
- **F3 pre-drained:** foreseeable forks are the §5 gates (Matt's) + tier-internal reasoning calls (mine); residual forks are reasoning-boundaries. YES.
- **F4 authority-resident:** tool-calibration authority is the TCP conductor's own seam. YES.
- **Honorable fallback:** a tier failing wholesale (e.g., no Murzak extension loads on 4.6.3) is a **processable finding** — the family verdicts `FAILS-LOAD`, the race proceeds with those rows excluded, and the finding is the answer the race needed. A gate FAIL never kills the run.
- **Matt interface:** veto-open ledger (§6 grows in-run); red-flag pings only mid-run; the completed VERDICT table + §6-check answers delivered as one review surface at exit. **Owner-eye checkpoint (pattern §6-obs-2):** the Tier-4 Pro `apply_particle_preset` render and the fork-#1 lighting fix are *looked-at-by-Matt* gates, not conductor-judged.
- **Seam execution (pattern Element 7):** Godot-project installs/imports/probes → **drax** (named); menu VERDICT-column append + version-bump re-reads → **legolas** (named, his doc); render/framediff evidence → **galadriel** (named) where CV grading is needed; conductor writes no production code. Reconnaissance (`lipo`, `ls`, fingerprints) may use Explore-class, evidence-only.

---

## §8 — Wave results (running)

**PC-W1-A ✓ (drax, `5a87dbdc`; evidence `/Users/admin/Games/reincarnated-godot/tmp/pcw1a/`):**
- **T-3(a)** LOADS-DIRTY(missing-embedded-texture) → repair ruled in-run (R-PC-7).
- **T-3(b)** 52 bones (fact-corrected from 51 → R-PC-8).
- **T-3(c)** **RETARGET-READY** — `sidekick_bone_map.tres` unmodified; **0.0000° mean AND max rest-Δ across all 40 mapped profile bones** vs hero body, boss body, and base-locomotion clip character (TCP-43 instrument). The nonzero whole-skeleton means are carried entirely by inert IK helpers + eyes/eyebrows. Drax's own KT-2 pass (2026-07-23) had already provisioned this — the cell *measured*, it did not create.
- **T-3(d)** 2 meshes / 2 materials confirmed (albedo-null pending R-PC-7).
- **T-4** **0/6 COVERED — the L8 arm-2 purchase fork does NOT dissolve.** The six missing glyphs (`holy`/`shadow`/`physical`/`knockback`/`consecrate`/`freeze`) are *element/mechanic iconography*; the menus pack's Icons_Input is 653 *platform button prompts* — different problem domain. Zero hits across 2,784 files, nearest-24 contact sheet inspected and rejected. Fork stays on Matt's L8 HALT queue with sharpened options (different pack / commissioned icons).
- **Findings F1–F10 logged not acted** (drax note) — conductor flags F3 for the REPLAY brief: **the tail is an unparented 5-bone skeleton absent from the body rig** — a tail-less werewolf at the fixed ARPG camera is a player-visible absence; capstone prep must resolve mount-or-omit. F8 (headless `--import` silently prunes default-equal project settings) and F9 (`.md5` delete does not force reimport; only dest-`.scn` delete does) are **instrument findings** — carried into every later cell's method.

**PC-W1-B ✓ (legolas relaunch, `58f7bed9`; first attempt lost to stream timeout, nothing written):** **SAFE-TO-PROCEED-AS-CHARTERED on Q46** — the ruling-critical surface is unchanged on a **null git diff** (v0.19.1→v0.20.1: zero lines changed across all six config/identity/auth/transport source files; all four env vars identical in name+semantics; default still Cloud; no new remote host; same five identity fields). **Three CHANGED items absorbed into Tier-4 method (M-T4 amendments below).** One scoping sharpening: identity metadata is built unconditionally at `Start()` regardless of mode — mode controls only where it is SENT. **The packet-quiet assert is therefore "nothing leaves the host," never "the fields are never serialized."** Bonus in our favour: upstream PR #321 closed the silent-success class (`isError: false`, nothing written) that bit L3 — check 3 now runs on a clear instrument (L-N satisfied by upstream). Standing gap: McpPlugin 7.3.0→7.5.2 / ReflectorNet 5.3.2→5.4.0 unaudited and they carry the `SKILL.md` generator — check 8's fingerprint is MORE necessary, not less.

**M-T4 method amendments (conductor, from PC-W1-B; veto-open):**
1. **Install targets re-pinned:** core addon **v0.20.1** + server **9.2.4** (charter's v0.20.0/9.2.2 were already stale at write time — L-C vindicated twice in one day).
2. **Tool-census assert is the NAME SET, never the count:** tools went 39→42 but 3 are `McpToolType.System` so `tools/list` returns 39 again — a count assert is vacuous. Check 2's 58-vs-63 baseline moves accordingly.
3. **Consumer csproj pins:** ReflectorNet **5.4.0** / McpPlugin **7.5.2** or the addon won't compile; `godot-cli` ping endpoint moved `/api/tools/ping` → `/api/system-tools/ping` (shipped regression — don't diagnose it as our failure).

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-28. Chartered on Matt's *"GO ahead"*; fires on §5.
