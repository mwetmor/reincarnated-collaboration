# Race-Well Verification + E10 Leg 3 Remaining-Gates Memo

**From:** knight-rider (synthesis of the autonomous-run Lane 4 prep). **Date:** 2026-07-09.
**Type:** VERIFICATION RECORD (the race-well slate is RULED + CLOSED — canon `908e858`; this memo verifies it, it does NOT propose or re-open it). **One genuine decision is surfaced** (Walls v1-vs-defer); the slate verification itself needs no decision.

> **⚡ LIVE (queue-sweep 2026-07-15, gandalf):** ONE decision survives — ratify **Walls DEFER from E10 Leg 3 v1** (§3.1, KR+gamora recommendation). **Corpus evidence since (mega-probe, 2026-07-15 re-check):** across the characterized corpus only **3 rows carry wall-as-blocking-geometry** (`le-frost-wall-rm` = the one live solo-PvE walls-as-win-condition identity; `di-bone-wall-necro-pvp` = PvP-context; `poe2-wall-of-shields` = negative/dead row) — deferral costs ~1 live catalogue identity, cheap at scale. (The 4-kit projectile-bounce-off-arena-walls cluster is a DIFFERENT mechanic — terrain reflection, not summonable obstacles — untouched by this deferral.) §3.2 bone-dump probes are a drax work item, not a decision.
**Feeds:** E10 Leg 3 build readiness. **Gates:** Leg 3 build still GATES on Matt curating (already done: slate CLOSED at 5) + the drax bone-dump probes named in §3.

---

## 0. What this memo is
Matt's autonomous-run Lane 4 was "E10 Leg 3 PREP, not build." The race well was ruled + closed at 5 mid-run (canon `bestiary-race-well-design-2026-07-09.md`, `908e858`), which re-scoped Lane 4 from *curation proposal* to *verification of the ruled slate*. This synthesizes the four prep artifacts:
- **(a)** drax read-only Synty humanoid inventory — `agentic_orchestration/research/2026-07-09-synty-humanoid-asset-inventory.md` (`d7e2dff`)
- **(b)** rocket race-well budget-verification math note — `generation/math/race-well-budget-verification-2026-07-09.md` (`d8b249c`)
- **(b-consult)** elrond budget empirics — `agentic_orchestration/research/2026-07-09-elrond-race-well-budget-consult.md` (`ef87545`)
- **(c)** gamora Walls feasibility spike (Fork 3) — `agentic_orchestration/gamora/notes/2026-07-09-walls-feasibility-spike-fork3.md` (`5d3bb55`)

## 1. Race-well slate verification — CLEAN (FYI, no decision needed)

The ruled 5-race slate is verified **inside** the §3.1a admission budget `R ≤ P/(M×F)` and **backed by on-disk assets**.

| Race | Tier | Asset evidence (drax inventory) | Rig status |
|---|---|---|---|
| Human | base frame | ~10+ register packs (deepest) | verified by construction |
| Goblin | reframe | goblin-war-camp + own locomotion; Q7 artifacts | VERIFIED (retargets today) |
| Orc | reskin (Matt ruling) | native `Big_Ork` body on disk + modular-reskin path | file-inferred conformant; bone-dump resolves construction |
| Elf | reskin-likely | `DarkElf` in proven Sidekick rig family | file-inferred conformant; bone-dump pending |
| Dwarf | reskin-or-reframe | `Dwarf` body in Sidekick rig family | file-inferred conformant; bone-dump resolves tier |

**Budget check (rocket `d8b249c`):** at P=700 (byte-verified FLOOR), F=4 factions, `R_admitted = floor(P/(M×F))`:
- M=5–6 (design floor) → R≤35/29 · M≈8.5 (batch-1 observed) → R≤20 · **M≈35 (canon-sketch, BINDING) → 700/140 = 5.0 exactly → R_admitted = 5.**
- R=5 holds under every assumption except the M=40-at-P=700 corner — a floor-artifact (tightest M against the fixture-bank floor of P) that clears at the real batch-2 derivation population, and is further offset because F=4 is total-factions (per-race F<1, a conservative over-charge).
- **elrond over/under signal at 5 = CLEAN;** no cluster-math failure. 700/(5×4)=35 kits per race×faction — at the canon target, well above the ~5–6 floor.

**Caveat (elrond + rocket, pre-registered):** M and P are **proxy-only until batch-2 emits** (batch-1 is the fixture bank; batch-2 = the ≥100/cell derivation pop, unbuilt). P=700 is a floor; a larger batch-2 P only LOOSENS the budget, so **R=5 holding at the floor is the conservative/robust result.** The verification re-fires post-batch-2 (elrond derivation-stack §10 step 3).

**Disposition:** clean verification → **FYI row, no Matt decision.** The slate stands as ruled.

## 2. Asset bench (noted, NOT admitted)
drax found **~13 rig-conformant race-type candidates** total (incl. rig-PROVEN Troll on the goblin map). The 8 beyond the slate sit on the **bench, outside the closed well** — admission is a future Matt curation act, never an LLM derivation. Curation is a **selection problem, not a supply problem.** Two dedup flags for any future curation: `polygon-modular-fantasy-heroes` ≈ `polygon-modular-fantasy-hero-characters`; human-archetype bodies overlap across packs.

## 3. E10 Leg 3 remaining gates

1. **⚖ DECISION — Walls (Waller-class blocking geometry): DEFER from Leg 3 v1.** The Fork-3 feasibility spike (gamora `5d3bb55`) returns **DEEP-ARCHITECTURE-CHANGE**: the sim's space is concrete-positional but obstacle-free (straight-line nav, occluder-blind hit kernels, scalar-distance targeting; only `ChokeZone` static x-clamp exists). *Dynamically-spawned mid-encounter* is solved (injection primitive); *blocking geometry that alters the fight* needs a new spatial subsystem (obstacle type + obstacle-aware nav + hit-occlusion), math-note-first, multi-dispatch — NOT a Leg-3 rider. **Recommendation (Matt/gandalf ratify): pull + immobilize enter Leg 3 v1 on existing plumbing; Walls become a dedicated future spatial-layer workstream** (not a quiet cut — a named deferral, consistent with Fork 3's "worth the spike").
2. **drax bone-dump probes (write-scope, NEXT SESSION):** in-Godot `scripts/dump_bones.gd` on **DarkElf / Dwarf** (+ **Big_Ork** if the native body is chosen over modular reskin). This resolves the `verified=true` rig-binding flag + the Orc construction tier — the last gate before Leg 3 kit-gen may consume the well (`verified=true` required per canon §6.2).
3. **Orc construction choice** (modular human-frame reskin vs native `Big_Ork` body) — drax enumeration, resolved by the bone-dump probe. Both file-inferred conformant.

## 4. Decisions surfaced for Matt
- **(1) Ratify Walls DEFER from E10 Leg 3 v1** (§3.1) — the one genuine decision here. (Slate verification §1 = clean, no decision.)

## 5. Provenance
Canon: `908e858` (race well). Artifacts: `d7e2dff` (a), `d8b249c` (b), `ef87545` (b-consult), `5d3bb55` (c). All committed to their seams; **not pushed** (KR batches; this window's non-Gate-2 analysis artifacts await Matt review + a batch-push authorization).

**Sign-off:** knight-rider, 2026-07-09 (autonomous-run Lane 4 synthesis).
