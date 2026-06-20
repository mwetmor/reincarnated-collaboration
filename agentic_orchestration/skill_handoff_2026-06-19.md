# Skill Handoff — 2026-06-19

**Author:** knight-rider
**Prior handoff:** `skill_handoff_2026-06-18.md`

## Workstream OPENED this session — Crypt-Vault Node Vignette PoC (map pipeline)

gandalf (out of a Pattern B design dialogue with Matt; Matt go: "ok, let's give it a shot") commissioned knight-rider to **sequence the first node-authoring PoC of the "From JSON to Seasons" map pipeline** and kick off the first authoring pass. Sequenced + dispatch authored.

**Authoritative spec (gandalf):** `agentic_orchestration/gandalf/notes/2026-06-19-crypt-vault-node-poc-brief.md`
**Dispatch authored:** `agentic_orchestration/dispatches/2026-06-19-drax-crypt-vault-node-poc.md` (Pattern B; drax authoring + Gate 1, then galadriel Gate 2)
**Validated tool:** satelliteoflove/godot-mcp v4.0.1 (legolas smoke-test — all 4 checks PASS): `agentic_orchestration/legolas/research/2026-06-19-godot-mcp-comparison/smoke-test-result.md`

### What the PoC proves
The author-in-MCP, **structure-first, three-gate** method produces a coherent, composable NODE (architected-dungeon clear-room, crypt-vault theme) that passes Matt — fixing the spatial-coherence failures the prior open-loop snapshot-scoring loop shipped (overlapping crypts, half-hidden doors, floating floors, reasonless walls). Vertical slice of ONE node-type. **Nothing scales to a 2nd node-type / multi-node stitching / fight execution until Matt passes this one** (brief §7).

### Three gates (in order)
1. **Gate 1 — Structural (drax, camera-INDEPENDENT, via MCP engine-truth):** no AABB overlaps; GridMap cells valid + door=wall-variant; A* entrance→exit; vertical-nav (mezzanine via stair); fight-spawn parity (annulus rule).
2. **Gate 2 — Register (galadriel, multi-angle CV):** hold the cathedral register band (composite ≥ 3.6; lighting ≥ 4; VFX ≥ 4) across SEVERAL framings.
3. **Gate 3 — Coherence (Matt):** judges an **ORBIT render set** (+ walk-through if feasible) — NEVER a single hero angle. Matt's verdict + REASONS are calibration samples for the eventual automated coherence judge (the HITL investment that removes HITL later).

### Repo ground-state knight-rider verified (corrects/extends brief §6 — encoded in the dispatch)
- **The godot-mcp addon is NOT currently installed** (`reincarnated-godot/addons/` has only `godot-sqlite` + `sidekick_creator`; smoke-test fully reverted). drax step 1 is broader than "enable plugin" → **re-install addon, THEN enable, THEN wire `.mcp.json`** (none exists in either repo).
- **`project.godot` enables only `sidekick_creator`** (+ `[addons]` block lines 11-14). Friction #4: enabling MCP rewrites project.godot and silently dropped an unrelated block in the smoke-test — diff-review must PRESERVE the sidekick_creator config.
- **Clear-room shells:** `reincarnated-godot/data/arena_scenarios.json` (6 scenarios). knight-rider lean = `elite_pack` (28×28 square, 3 non-player spawns, most "room"-like vault chamber); `magic_pack` (32.7×14 trash room) viable alternate; boss_with_adds + mini_boss OUT (not clear-rooms). drax makes the final call + justifies; preserve footprint + spawns at parity.
- **galadriel CV instruments** live galadriel-owned at `agentic_orchestration/galadriel/pipeline/` (`register-metrics.mjs`, `lifecycle-score.mjs`, `arch-grammar-band-probe.mjs`).
- **MCP single-client constraint (port 6550, friction #7):** drax authors + closes his MCP session FIRST, THEN galadriel scores (offline on captured frames — preferred), or galadriel as sub-agent inheriting drax's connection. Never a 2nd concurrent client.

### Deliverables (per dispatch)
1. MCP enablement in a deliberate diff-reviewed commit (own commit).
2. Crypt-vault clear-room NODE: structure-first GridMap (walls/floor/door-as-wall-variant/one-stair+mezzanine), 3–4 grid-snapped sarcophagi, scatter clutter only, entrance+exit sockets, cathedral register held constant, footprint+spawns at parity.
3. Gate 1 PASS (structural) + Gate 2 PASS (register) + ORBIT render set for Matt's Gate 3.
4. **First-draft Act-Graph node schema DERIVED from the authored node** (brief §5 — substrate-led; explicitly NOT canonicalized).

### Gate-1 (jack-ryan pre-fire) disposition
Assessed **NOT required** to publish: no engine code, no telemetry/fixture-dict/decisions-log change; design-side review carried by gandalf's authoritative brief; node schema is explicitly non-canonical PoC draft. Cross-seam Principle-6 gate = N/A (arena_scenarios.json read-only; no contract change). Gate 2 (galadriel) + Gate 3 (Matt) are the binding gates. Flagged to gandalf for overrule if desired.

### Launch (Matt's one-command friction — Pattern B; drax needs own session + open Godot editor for MCP WS:6550)
```bash
cd ~/Games/reincarnated-godot && claude --agent drax
```
The dispatch is the newest drax-matching dispatch (verified) — drax picks it up at session-start.

### Status
- Dispatch authored + discoverable. **Awaiting drax session launch** (Pattern B — Matt/drax-initiated; requires open Godot editor for the MCP bridge).
- Next: drax first-pass result (Gate 1 structural + the node + orbit set) → galadriel Gate 2 → gandalf rules to green across 1+2 → Matt Gate 3 coherence. No scale to a 2nd node until Matt passes.

---

## Carryover from prior sessions (not re-litigated here)
- 2026-06-18 three-flag flip cycle (D4 proxy-default-on + keystone-faithful-default-on) landed + jack-ryan smoke-clean; tags Matt-gated (ADR-006), carried in the run-close PUSH GATE per decisions-log.
- gamora clean-boss-numbers harness dispatch (`2026-06-19-gamora-clean-boss-numbers-harness.md`) in flight separately.
