# Dispatch — 2026-06-07 — jack-ryan Gate-2 — Cosmograph A/B Spike (Mode B kit-as-bounded-constellation)

**From:** knight-rider (orchestrator)
**To:** jack-ryan (PRIMARY — Gate-2 post-output review with INFO/WARN/BLOCK authority)
**Authority:** dispatch `2026-06-07-drax-cosmograph-a-b-spike.md` § 5.2 (jack-ryan Gate-2 at spike close) + gandalf mode-disposition verdict 2026-06-07 routing to knight-rider for Gate-2 dispatch
**Spike:** Cosmograph A/B spike — Mode A (primitive-galaxy) vs Mode B (kit-as-bounded-constellation) at `/forge`
**Cycle:** Post-cosmograph-Phase-A iteration spike
**Tag intent:** none (Gate-2 finding artifact; auto-commit per critique-pair pattern)
**Estimated horizon:** ~1 session

---

## 1. Spike status snapshot

- **Phase 1** (10-kit sample): GREEN — RENDERING-UNIT READABILITY confirmed; commit `0077e9e` (loadout, local)
- **Phase 2** (full 1000-kit corpus + LOD + Pixi.js pre-drawn layers): GREEN — commits `bb7176c` + `e63f667` + `986334d` (loadout, local)
- **Mode disposition** (gandalf verdict 2026-06-07): Mode B locked as default at `/forge` (no query param); Mode A retained as `?view=primitive` analyst diagnostic; "SPIKE·P2·1000 kits" badge retired; player-facing kit-discovery copy installed — commit `7d411a2` (loadout, local)
- **Findings + screenshots + dispatch completion record:** commit `bb9e5f4` (collab, local)

**Push state:** loadout is ahead 4 commits of origin/main; collab is ahead 1 of origin/main. Pushes pending Matt authorization per ADR-006. Local commits ARE the review surface.

---

## 2. Authoritative reading

1. **`agentic_orchestration/dispatches/2026-06-07-drax-cosmograph-a-b-spike.md`** — gandalf-authored spike dispatch including:
   - § 2 architectural framing (Mode A vs Mode B; toggle architecture; lasso semantics)
   - § 6 substrate-led discipline preservation (primitives ARE substrate truth; per-kit instances reference same primitive identity; rendering-layer choice does NOT manufacture substrate identity)
   - § 8 Q1 Finding 3 amendment (substrate-coverage validation OUT OF SCOPE for this spike — PROVISIONAL constellations were never Pareto-balanced)
   - Phase 1 + Phase 2 completion records at footer
2. **`agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-2-full-corpus-findings.md`** — drax Phase 2 verdict + § 5 force-config lock + § 7 architectural learning (Gate-1 Finding 4 REFUTED)
3. **`agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-1-sample-findings.md`** — Phase 1 verdict + initial force-config + first surfacing of UMAP-degenerate-for-Mode-B finding
4. **Screenshot pair Phase 2:** `phase-2-screenshot-primitive-full.png` + `phase-2-screenshot-constellation-full.png`
5. **`canonical/story/2026-06-05-cosmograph-pivot.md`** § 9 — primitive-as-star + kit-as-constellation architectural lock (substrate truth at geometry layer)
6. **`canonical/story/2026-06-06-cosmograph-phase-a-creation-moment-wave-close.md`** — Phase A production state Mode B inherits from
7. **`reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — especially Discipline #25 (semantic-layer rep-audit) + #41 (substrate-led; pre-imposed taxonomy interrogation)

---

## 3. Review scope per gandalf mode-disposition verdict § 3

Five review items surfaced by gandalf for jack-ryan's lens. **Gandalf is OUT of the Gate-2 loop unless jack-ryan surfaces a design-side BLOCK** (verbatim gandalf routing 2026-06-07).

### 3.1 Grid-layout architectural pivot — decisions-log candidacy

**Surface:** F-R force layout (Phase 1 starting baseline per dispatch § 3.3) was abandoned at Phase 2 full corpus and replaced with element-sorted 32×32 grid + sunflower spiral Stage 2 (per drax findings § 5).

**Drax's rationale (findings § 5 + § 7):** at 1000 kits, mean Jaccard ~0.224 with no clustering gradient — F-R aggregate spring attraction across 999 pairs overwhelms per-pair repulsion, collapses all centroids to ~40px separation. The shared 570-primitive vocabulary structurally precludes force-layout gradient exploitation.

**Gandalf instinct (verdict § 3.1):** YES, decisions-log entry warranted — "for uniform-similarity substrate corpora, element-sorted grid preferred over force-directed layout."

**Jack-ryan call:** does this clear the decisions-log threshold (architectural commitment with downstream-binding force vs routine implementation choice)?
- If YES: decisions-log entry authored by jack-ryan (per ownership lineage); architectural commitment captured for downstream Phase B kit-similarity embedding work + future elrond Phase B commission consideration
- If NO: route to drax findings doc as engineering note; no canonical lift
- Optional: discipline #N candidate ("substrate uniform-similarity → grid layout, NOT force layout") if pattern is generalizable beyond cosmograph

**Scope to verify:** is the F-R failure mode (uniform Jaccard collapses force gradient) load-bearing across future substrate-similarity render workstreams (mantis UE 3.7 STRETCH 3D cosmograph; future engine kit-galaxy variants), or is it cosmograph-local?

### 3.2 Substrate-led discipline at rendering layer — Discipline #25 semantic-layer rep-audit

**Surface:** per dispatch § 6, Mode B's per-kit primitive instances (e.g., `kit_001:fire` and `kit_002:fire` as separate render-time nodes) BOTH bind to the same underlying `fire` primitive in `primitive_registry.parquet`. Substrate identity is NOT manufactured at the rendering layer; the duplication exists ONLY for visualization.

**Per Discipline #25 (semantic-layer rep-audit):** verify drax's implementation honors this — that the per-kit instance node IDs do not propagate into any substrate-binding code path (substrate vote, primitive identity queries, downstream substrate analytics) and exist exclusively in the Pixi.js render-layer node enumeration.

**Files to inspect:**
- `reincarnated-loadout/src/components/Cosmograph/ConstellationModeCanvas.tsx` (Phase 2 rewrite — verify per-kit instance enumeration is render-only)
- `reincarnated-loadout/scripts/compute-constellation-layout.py` (Python pre-compute — verify it consumes `primitive_registry.parquet` as substrate truth, not generates duplicate substrate IDs)
- `constellation_layout.json` (the pre-computed packet — verify per-kit-primitive-instance identifiers do NOT escape the render layer)

**Verdict surface:** confirm rendering-layer composition (per-kit instances at Mode B) does not corrupt substrate vote at the geometry layer per dispatch § 6 contract.

### 3.3 `constellation_layout.json` payload — Vercel preview budget + cache discipline

**Surface (per drax findings § 3):** payload is 2.04MB raw / ~600KB estimated gzip. Localhost load ~20-30ms; Vercel preview load ~200-400ms cold cache.

**Items for jack-ryan:**
- Is 2.04MB / ~600KB gzip within acceptable Vercel preview budget for player-facing default? (Mode B is now first-paint at `/forge` no-param)
- Should Cache-Control headers be set explicitly on this asset (immutable + long-TTL given it's a deterministic pre-computed packet)?
- Is the cold-cache first-paint cost a player-facing acceptability concern, or is it preview-only and prod CDN behavior closes the gap?
- Pre-fetch or critical-path opportunity at Forge.tsx? Or is lazy-load on first Mode B mount sufficient?

**Verdict surface:** INFO/WARN if action needed; PASS if budget acceptable as-is.

### 3.4 `// TODO(drax)` grid-layout override breadcrumb — annotation form correctness

**Surface (per gandalf verdict § 3.5 + drax findings § 7):** drax annotated `// TODO(drax)` at the grid-layout override in `compute-constellation-layout.py` as a breadcrumb pending the conditional elrond Phase B kit-to-kit similarity 2D embedding commission (gandalf deferred per verdict § 4 until real-cycle 15+ kits exist).

**Jack-ryan call:**
- Breadcrumb form correct (TODO(drax) names owner; tracks override location)?
- Should this also surface as an AGENT_STATE.md item on drax's side, or is the in-code TODO sufficient given the elrond commission trigger is at a future workstream boundary (real-cycle 15+ kits)?
- Is the linkage between the breadcrumb and the deferred elrond commission discoverable (e.g., does the TODO reference the dispatch or findings doc)?

**Verdict surface:** PASS / INFO (suggest annotation refinement) / WARN if traceability gap.

### 3.5 Gate-2 standard checks

Per critique-pair-gate-protocol Gate-2 framework:
- **Math-before-code:** N/A — this spike is rendering-layer A/B; no math hotspot
- **Smoke-test discipline:** Phase 1 sample (10 kits) → Phase 2 full corpus is itself a smoke-then-scale pattern; verify the smoke-to-full transition discovered scaling failures empirically (F-R collapse) rather than papering over them — drax did surface the failure and pivot; ratify
- **Cross-seam impact:** consumes existing `cosmograph-substrate-trace-2026-06-06/` elrond packet read-only; no elrond commission fired; potential future commission FLAGGED (not fired)
- **Decisions-log as truth:** covered at § 3.1 above
- **Severity matters:** this is a SPIKE close (empirical visual-architecture validation), not a production-balance change; severity calibration accordingly
- **Discipline #1 (math-before-code):** N/A
- **Discipline #2 (smoke-test):** verified above
- **Discipline #25 (semantic-layer rep-audit):** covered at § 3.2
- **Discipline #41 (substrate-led):** covered at § 3.2

**BLOCK authority:** jack-ryan retains BLOCK authority per critique-pair-gate-protocol if any review item escalates beyond INFO/WARN.

---

## 4. Work-product files for review

### 4.1 Loadout (reincarnated-loadout, 4 local commits ahead of origin/main)

| Commit | Subject | Key files touched |
|---|---|---|
| `bb7176c` | Phase 2 main — full 1000-kit corpus + LOD + Pixi.js pre-drawn layers | `src/components/Cosmograph/ConstellationModeCanvas.tsx` (Phase 2 rewrite), `scripts/compute-constellation-layout.py`, `public/constellation_layout.json` (or equivalent path), Forge.tsx wiring |
| `e63f667` | dot-size fix — 16px inner / 32px outer for initial-scale visibility | ConstellationModeCanvas.tsx |
| `986334d` | AGENT_STATE checkpoint | `reincarnated-loadout/AGENT_STATE.md` |
| `7d411a2` | Forge — Mode B as default; player-facing copy; retire spike badge | `src/pages/Forge.tsx` |

### 4.2 Collaboration (reincarnated-collaboration, 1 local commit ahead of origin/main)

| Commit | Subject | Key files |
|---|---|---|
| `bb9e5f4` | Phase 2 findings + screenshots + dispatch completion record | `agentic_orchestration/drax/notes/2026-06-07-cosmograph-a-b-spike/phase-2-*` + dispatch footer Phase 2 completion record |

### 4.3 Vercel preview (behind Vercel auth)

`https://reincarnated-loadout-krulytb91-matthew-wetmore-s-projects.vercel.app`
- `/forge` → Mode B default (player-facing)
- `/forge?view=primitive` → Mode A analyst diagnostic

---

## 5. Acceptance + close criteria

**Gate-2 finding output:** `agentic_orchestration/qa/findings/2026-06-07-jack-ryan-gate-2-cosmograph-a-b-spike.md`

**Finding structure** (per critique-pair-gate-protocol Gate-2 + recent jack-ryan precedent `2026-06-02-qdx-phase-3-qdx-5-gate-2.md`):

1. **Verdict line:** PASS / PASS-with-INFO / PASS-with-WARN / BLOCK
2. **Per review-item disposition** (§ 3.1 through § 3.5 above) — each gets INFO / WARN / BLOCK / PASS with rationale
3. **Decisions-log determination** (§ 3.1) — explicit YES/NO with reasoning; if YES, the entry is authored by jack-ryan (separate file proposal or appended to next decisions-log entry batch per jack-ryan's authorship discipline)
4. **Discipline-amendment determination** — does any review item surface a new engineering discipline candidate (uniform-similarity substrate → grid layout pattern; rendering-layer per-kit instance dedup discipline; etc.)? Cite + propose or note "no new discipline"
5. **BLOCK escalations** — if any, name the BLOCK + the seam-owner re-fire vs Matt-escalation routing
6. **Auto-commit per critique-pair pattern** (CLAUDE.md addendum) — jack-ryan auto-commits findings doc + any decisions-log entry from this Gate-2

**Spike close trigger** (per dispatch § 5.2 amended): jack-ryan Gate-2 verdict landed + (if PASS) drax notified for push-authorization request to Matt + (if BLOCK) seam-owner re-fire OR Matt-escalation per BLOCK severity.

---

## 6. Out-of-scope reminders

- **NOT in scope:** substrate-coverage validation of the 1000 PROVISIONAL constellations (Move B simulated kits, never Pareto-balanced — explicitly deferred to Phase B real-cycle 15+ kits per dispatch § 8 Q1 amendment)
- **NOT in scope:** Vercel push authorization (Matt-explicit per ADR-006; jack-ryan does NOT authorize pushes)
- **NOT in scope:** mantis UE 3.7 STRETCH 3D-cosmograph design (downstream consumer; inherits metaphor verdict but separate workstream)
- **NOT in scope:** elrond Phase B kit-to-kit similarity 2D embedding commission (gandalf deferred until real-cycle 15+ kits exist)
- **NOT in scope:** redesign of Mode A primitive-galaxy (preserved as analyst diagnostic; no changes proposed in this spike)
- **NOT in scope:** re-engaging gandalf in the Gate-2 loop unless a design-side BLOCK surfaces (verbatim gandalf routing 2026-06-07)

---

## 7. Routing

- **Primary:** jack-ryan executes Gate-2 review per § 3 + authors finding per § 5
- **Auto-commit:** findings doc + any decisions-log entry per CLAUDE.md addendum (in-scope work-product of authorized Gate-2 task)
- **On PASS / PASS-with-INFO:** notify knight-rider; knight-rider surfaces Matt push-authorization request for both repos (collab `bb9e5f4`; loadout `bb7176c..7d411a2`)
- **On WARN / BLOCK:** route per critique-pair-gate-protocol BLOCK routing — seam-owner re-fire if within authority, Matt-escalation if architectural
- **Gandalf re-engagement:** ONLY if jack-ryan surfaces a design-side BLOCK (verbatim gandalf 2026-06-07: "I do not need to be in the Gate-2 loop unless jack-ryan surfaces a design-side BLOCK")

---

**Authored:** knight-rider 2026-06-07 per drax routing request + gandalf mode-disposition verdict routing to knight-rider for Gate-2 dispatch.

**End of dispatch.**
