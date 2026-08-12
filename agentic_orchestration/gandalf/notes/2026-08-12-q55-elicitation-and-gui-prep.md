# Q55 elicitation sheet + GUI (editor) preparation plan — 2026-08-12

> **Role:** gandalf, `ELICITOR`. **Status:** ✓ RULED 2026-08-12 — Matt verbatim: *"(a) as leaned, S-pins as leaned, REG, GUI, conduct."* Five of six desk rows dispositioned (§ 3); Q56 remains open. Q55 queue row: `canonical/matt_decision_needed/README.md` (parked `72ffc385`). Companion beats this session: retention LAW adopted (`7e503a8b`); SB-1 shape presented, launch word pending.

---

## 1 · Q55 — the D5 revisit, decision-shaped

**What is being amended:** Matt's own D5 (2026-08-10): *"sandboxes deferred; fingerprinting is v1 containment."* The 25-round ladder then certified the **mechanical lane** under that posture (LIFT) while demonstrating the **agentic lane's** defect supply is structurally unbounded under detection (channels that can't carry their own counterexample; rollback verbs that destroy; rule-39-vs-unscoped-`Bash`). Amending D5 is Matt's commitment boundary; the landing declaration routes the threat-model boundary to Matt + gandalf by name.

**The structural argument that decides it:** detection enumerates **defects** — infinite, adversary-supplied. Isolation enumerates **capabilities** — finite, harness-supplied. Fork (a) converts an unbounded enumeration problem into a bounded one; fingerprinting demotes to the audit layer — *detection audits what isolation makes impossible.*

**Fresh host facts (measured this session):** Codex CLI ships **native sandbox modes** (`--sandbox read-only | workspace-write`; Seatbelt-backed on macOS); `/usr/bin/sandbox-exec` present (macOS 15.6.1); **no container runtime installed** (docker/colima/podman absent — containers are a v2 option requiring a matt_to_do install). Claude Code headless likewise carries sandboxing. **Fork (a)'s v1 build cost is therefore LOW** — the inner wall ships inside the worker CLIs; star-lord builds worktree provisioning + the apply gate + audit scan.

| fork | what it is | evidence posture | cost |
|---|---|---|---|
| **(a) OS boundary** — gandalf lean | agentic cells run in throwaway isolation (worktree-clone + CLI-native sandbox; no reach into `canonical/`, `.claude/`, engine tree, or the factory itself); fingerprints = audit layer | converts the problem class; ladder evidence says this is the only bounded shape | LOW v1 (CLI sandboxes exist); star-lord days-not-weeks |
| **(b) resume fingerprint-hardening** | written threat model + pre-registered round budget | **evidence-disfavored:** 25 rounds bought the mechanical lane, not the agentic one; a budget caps spend on a treadmill, doesn't bound the treadmill | unbounded tail risk |
| **(c) defer past SB-1** | agentic lane stays dark | costs nothing for SB-1 (unblocked anyway) — but now prices in the GUI: the editor-chat's delegated-work backend IS an agentic lane; also delays F2, JR-7, registry volume phase | compatible with (a): rule design now, build later |

**RECOMMENDATION: "(a) as leaned," built post-SB-1** — the (a)+(c)-timing composition the queue row itself names.

### Sub-pins under (a) — S-1..S-4 (each one word, or "S-pins as leaned")

| pin | decision | gandalf lean |
|---|---|---|
| **S-1 isolation mechanism v1** | layering: (1) throwaway git worktree = blast radius; (2) CLI-native sandbox `workspace-write` = inner wall (read scope ⊂ worktree + toolchain; NO `~/.zshrc`, keychain, `.claude/`, other repos); (3) empty-MCP law stands; (4) containers/pf-egress = v2 hardening only if audit demands (install → matt_to_do) | **as stated; mechanism detail is star-lord's in-seam under these constraints** |
| **S-2 propose/dispose asymmetry** | the worker NEVER commits to the repo of record — it emits patch + receipts; the mechanical lane validates (clean-sandbox tests + audit scan) and the HARNESS applies/commits | **pin it** — capability asymmetry is the deepest containment and it is how the spine already thinks |
| **S-3 certification of lane-open** | jack-ryan's stopping-rule recommendation (clause 1 = **class coverage**, not clean rounds) gets its finite domain: pre-registered **escape-class list** (fs-escape · network-escape · credential-reach · repo-of-record mutation · factory-self-mutation), each with a positive denial test + audit-log assertion; lane opens when every class is covered, jack-ryan Gate-2 on the lap | **adopt** — resolves the LANDING § 5 stopping-rule residue in the same word |
| **S-4 maiden workload (F2 pilot)** | registry classification: Codex cells tag/classify the ~11k catalogue assets (strata, class, search keywords) — reads = manifest + thumbnails; writes = tag rows in scratch; **zero code writes**; thumbnails themselves are mechanical-lane renders, not LLM work | **adopt** — bounded, receipt-checkable, low blast radius, and it feeds the GUI palette directly |

**Q56 interaction, noted not argued:** once a lane opens, the `dollars` column gains a truth to carry (subscription lanes price at ~0 marginal with tokens recorded) — this strengthens jack-ryan's KEEP; Matt rules Q56 separately.

---

## 2 · GUI preparation — the two surfaces Matt described, staged

**Matt's ask (verbatim intent):** drag-and-drop assets — parts/pieces and/or pre-made characters/rooms/VFX — (A) directly into Godot and/or (B) into a chat interface where an agent can reference and work with them.

**What it maps onto:** *two skins over the same contract layer* — extending two-skins-one-spine to three: factory New Run form · editor chat · Godot dock. One registry beneath all three (REG-1..3). Ground truth: `reincarnated-godot/catalogue/` is already data-first (11,070 assets, `packs.json`, generated HTML, ingest harness + `addons/godot-synty-tools` — the addon seam is open); incompleteness is ingest-scope, not architecture.

### The six GUI laws (pre-registered so the editor cannot drift)

1. **L1 References, not bytes** — drag payload = registry ID (`@asset:<pack>/<id>`); chat and dock never move meshes, they move nouns.
2. **L2 One data path** — every surface reads the registry; no surface-private asset lists (the stale-HTML lesson: hand-fed scope rots).
3. **L3 Placements are data** — scene composition stays diffable `.tscn` text, agent-readable; no editor-private state.
4. **L4 Turn-based sync via git (v1)** — Godot reloads on change; agent reads HEAD. NO live two-way socket; the live-collab world-editor is a named studio-killer scope trap.
5. **L5 Agent proposes, machinery disposes** — chat-agent edits land as patches through validation (S-2's asymmetry wearing the editor skin).
6. **L6 No product skin** — Spec B constraint stands until F-V2-1 graduation; this is a tool.

### Stages and their unlock conditions

| stage | delivers | unlocked by |
|---|---|---|
| **0** | registry schema (elrond, now) + ingest extension: missing Synty packs, Unity-vendor VFX, blender-decomp parts (drax, post-CP-A) + thumbnails (galadriel/mechanical, last) | REG-1..3 word |
| **1** | SB-1 close deposits: dressed arena = completed-room #1; werewolf + king harvest as completed-characters; workflow #0 receipts | SB-1 runs |
| **2** | **Godot registry dock v0** (drax): palette dock reading registry, native drag into viewport → instantiate. **Matt's drag-into-Godot arrives HERE — needs no factory, no Q55, no Tier-2 gate** | GUI-2 word + drax post-SB-1 |
| **3** | Tier-2 New Run form + web palette panel (Spec B build gate: receipts stable across ≥2 workflows — workflow #2 = galadriel capture-verify per R2) | workflow #2 lands |
| **4** | chat surface v0: palette + chat, reference-drag tokens, **conducted-session backend** (local Agent-SDK bridge) | Stage 3 + GUI-1 |
| **5** | chat backend swaps to **factory agentic lane**: drag → delegate → cell in sandbox → patch + receipts → scene updates; editor becomes the run instrument panel | **Q55 (a) + F2 built** |

**The convergence sentence:** Surface B's delegated loop *is* the agentic lane wearing a friendly skin — Q55 is the enabling ruling for both of Matt's asks this turn.

### Rules awaiting words (consolidated desk)

| id | rule | rec |
|---|---|---|
| **Q55** | (a) as leaned / (b) / (c) / composition — plus "S-pins as leaned" or per-pin words | **(a) as leaned, built post-SB-1; S-pins as leaned** |
| **REG-1..3** | registry-first · strata-open · staggered sequencing (from prior beat) | YES / adopt-open / charter-now |
| **GUI-1** | adopt the six laws + staged plan; gandalf authors the editor charter doc (SPEC-AUTHOR) on the word | YES |
| **GUI-2** | commission Godot dock v0 (drax, post-SB-1) | YES |
| **Q56** | dollars KEEP/DROP (steward tie) | Matt's re-rank |
| **SB-1** | launch word ("conduct") — shape presented, § 11 residue = Cell 0 | fire Act 0 |

---

## 3 · RULED — 2026-08-12, Matt verbatim: *"(a) as leaned, S-pins as leaned, REG, GUI, conduct."*

| id | word | disposition |
|---|---|---|
| **Q55** | "(a) as leaned, S-pins as leaned" | **Fork (a) GOVERNS** — OS boundary for agentic cells; fingerprinting demoted to audit layer; D5 amended. S-1..S-4 adopted as leaned. Build post-SB-1 (star-lord seam). Queue row struck same-commit. Unblocks F2 sequencing + agentic HOLD clause 2 + JR-7 INFO rider; LANDING § 5 stopping-rule residue resolves via S-3. |
| **REG-1..3** | "REG" | Adopted — registry-first · strata-open · staggered chain. elrond Stage-0 schema cell fired same-turn (design-only). |
| **GUI-1** | "GUI" | Six laws L1–L6 + staged plan 0–5 adopted; gandalf authors the editor charter doc (`SPEC-AUTHOR`) on the next beat. |
| **GUI-2** | "GUI" | Godot registry dock v0 commissioned (drax, post-SB-1 — Stage 2; no factory/Q55/Tier-2 dependency). |
| **SB-1** | "conduct" | **LAUNCHED** — Act 0 fired (drax Cell 0 countersign); rulings + pins in the run ledger (PL-6, L-0). |
| **Q56** | — | Not spoken; remains on the queue (steward tie, Matt's re-rank). |

**Two rider questions from the launch turn, answered in the launch reply (banked for lineage):**
- **godot-synty-tools scope:** import-time tooling for RAW vendor sources (bone maps, import generators, post-import scripts) — NOT the serving layer for assembled assets. Our assembled characters/rooms/VFX are native Godot artifacts (`.tscn`/`.tres`) served by the REGISTRY + dock, source-agnostically. Unity-vendor VFX cannot import as VFX; they decompose to parts and REBUILD as Godot GPUParticles at the assemblies stratum.
- **Codex routing doctrine:** *name the work, not the worker.* Cells get IDs, not seam names (seam names carry governance identity workers don't have and S-2 denies them). Codification per cell in workflow YAML (governing surface: task, scope, model pin, sandbox mode, acceptance, receipt fields) + a harness-GENERATED `AGENTS.md` dropped into the throwaway worktree (Codex-native config surface, templated from the cell spec, never hand-maintained). Model pinned per cell → `-c model=` → recorded in receipt. Routing table v1 is written FROM the S-4 pilot's receipts, not speculated in advance.

*Banked by gandalf (`ELICITOR` → `RUN-CONDUCTOR` at the launch word), 2026-08-12.*

---

## 4 · Post-launch elicitations (Matt requested same-session): Q56 + Q-R4

**Q56 — receipts `dollars` column, KEEP/DROP.** Premise change since the steward tie: the tie formed under D5 (agentic lane indefinitely dark → the column might NEVER carry truth; gandalf DROP was correct under that premise). Matt's fork-(a) ruling killed the premise: lanes open post-SB-1, the S-4 pilot's receipts carry model pins + token counts within weeks, and subscription lanes have a REAL answer ("$0 marginal, tokens recorded"). jack-ryan's forward-compat KEEP now has a concrete consumer. Residual hazard is unchanged though: a NULL dollars cell read as "cheap." **gandalf updated lean: KEEP + null-carrier rider** — `dollars: null` is only legal when `dollars_source` names WHY (`unpriced-lane` / `subscription-zero-marginal` / `metered-pending`), and render surfaces print the source word, never a blank or $0.00. The misreading dies at the render layer; forward-compat preserved; star-lord implements one enum + one render rule. One-word shapes: **"KEEP as leaned"** (with rider) / "KEEP" (bare) / "DROP".

**Q-R4 — who owns `registry/`** (physically in drax's repo; logically a data layer). Forks: **(a) ADR-004 pattern** — drax owns the FILES (his repo, his ingest writes them), elrond owns the SCHEMA (shape changes are elrond-authored specs), cross-seam changes ride MIGRATION entries; the deposit validator is schema-side authored, drax-repo hosted — giving L5/S-2's propose/dispose asymmetry a mechanical enforcement point. Exact precedent: the star-lord/elrond telemetry boundary. **(b)** elrond owns files too (registry moves out of the godot repo) — breaks locality; the dock and harness read `res://` paths beside the data. **(c)** drax owns schema too — invites the convenience-edit rot REG-1 legislates against, on a contract three surfaces depend on. **gandalf lean: (a).** One-word shape: **"ADR-004 pattern"**.

**RULED 2026-08-12 — Matt verbatim: *"KEEP as leaned, ADR-004 pattern"***

| id | word | disposition |
|---|---|---|
| **Q56** | "KEEP as leaned" | **KEEP + null-carrier rider GOVERNS** — `dollars` stays in the receipts schema; `dollars: null` legal ONLY with `dollars_source ∈ {unpriced-lane / subscription-zero-marginal / metered-pending}`; render surfaces print the source word, never blank/$0.00. Steward tie RESOLVED — the fork-(a) premise change re-ranked gandalf DROP → KEEP-with-rider. star-lord implements (one enum + one render rule) when the S-4/factory receipts lane builds post-SB-1. Queue row struck same-commit. |
| **Q-R4** | "ADR-004 pattern" | **Fork (a) GOVERNS** — drax owns registry FILES (godot repo; his ingest writes them); elrond owns SCHEMA (shape changes are elrond-authored specs); cross-seam changes ride MIGRATION entries; deposit validator **schema-side authored, drax-repo hosted** (mechanical enforcement point for the L5/S-2 propose/dispose asymmetry). Precedent: star-lord/elrond telemetry boundary. Binds elrond registry v2 (Q-R4 row), the Stage-2 dock, and the post-CP-A ingest cell. |

*Banked by gandalf (`ELICITOR`), 2026-08-12. Registry residue: Q-R1/R2/R5 dispositions ride veto-open (both / narrow / ship-the-9); Q-R3 routes to the drax ingest cell post-CP-A — its ownership frame is now this Q-R4 ruling.*
