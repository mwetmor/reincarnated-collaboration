# Reap. Die. Rise. — Canonical Spec Set (Index + Supersession Map)

**STATUS:** CURRENT (load-bearing) — the v2 canonical design set for the game now titled **Reap. Die. Rise.** Integrated 2026-06-29 (Path A).
**Steward:** gandalf (story-and-design steward).
**Provenance:** Matt mobile-session design docs authored over several days to 2026-06-29; re-homed from `matt_notes_handoff_docs/new_docs_and_content_2026-06-29/` and renamed to drop the legacy `reincarnated-` prefix (`da6d3b5`).
**Companion (LIVING):** `canonical/story/current-to-end-state.md` — the current→end-state tracker measures the *engine's distance to this spec*. Open it every session.
**Cross-ref:** `canonical/00-ground-state.md` §1 (CURRENT-doc spine).

**What this directory is:** the nine documents here are the authoritative v2 design. They re-register the frame (isekai → death-faith; the **spirit guide is RETIRED** — its advisory function splits to **(A)** the **demigod-jailer** as tutorial instructor + **(B)** the separate caged **patron god** as a seldom-heard guidance voice; banter/retort-axis owner OPEN, flag #6) and crystallize the roguelite-descent + ARPG-build-depth loop. This index encodes: (1) the naming lexicon, (2) the intra-set supersession chronology, (3) per-doc status + specialist routing, (4) what this set supersedes in **prior** canon (the Path B correction/delete seed), and (5) the open contradictions surfaced for Matt's ruling.

---

## 1. Naming lexicon (locked; exact per `story-keystone.md` §18)

| Element | Form | Use |
|---|---|---|
| **Display title** | **Reap. Die. Rise.** (with periods) | title art, store, prose |
| **Product / URL / handle slug** | **reapdierise** (no spaces/punctuation) | domain, social handle, store URL — grab early (the three words are individually common) |
| **Repo / file slug** | **reap-die-rise** (hyphens) | this directory + file renames (Matt-confirmed convention; distinct from the punctuation-free product slug) |
| **Sacred motto (Latin)** | **Mete. Morere. Resurge.** ("Reap. Die. Rise-again.") | the crusade's holy words. *Mete* (metere, to reap) · *Morere* (mori, to die) · *Resurge* (resurgere, to rise *again* — encodes the reincarnation loop). Alt middle for a soldier's-fall flavor: **Occumbe.** |
| **World-name** | **the Necroverse** — the death-cosmos of countless worlds the crusade traverses | in-world lore/copy; optional colon-subtitle. ("Necro-" is saturated in games — flavor only, clash-check before branding.) |
| **The contested utopia** | **Pax** — the crusade's named holy goal; the promised universal peace | the game's "Gaia" (cf. *Foundation*): a Latin common noun (un-ownable → in-world ideal, never a title/brand). Means different things per knowledge-tier; holds the central irony (*salvation or annihilation?*). |
| **Terminal-state names** | **the Necropolis** (the necro-city/world the crusade builds) → **the Necrocosm** (the terminal deadening — necropolis having consumed all worlds) | the crusade is the engine turning Necropolis into Necrocosm |

One-line: **Reap. Die. Rise.** (what you do) · *Mete. Morere. Resurge.* (the holy words) · **the Necroverse** (where) · **Pax** (what it's all *for* — and the slow horror of learning what Pax truly is).

---

## 2. The set + intra-set supersession chronology

The set was authored across several mobile sessions; later docs override earlier ones on overlapping ground. **The chronology of the patron/story frame (latest governs):**

```
design-decisions-session §1  (earliest patron sketch — STALE)
        ↓ superseded by
story-expansion §3/§11        (patron = hijacked benign fortune-deity; descent = soul-temple breach)
        ↓ superseded ON ONE POINT by
story-keystone §14            (the realms are ALIVE, made to rebel — NOT drained/conquered)
```

**Two precise intra-set supersessions to honor:**

1. **Patron origin** — `story-expansion.md:177` (closing note) states it outright: *"the patron shifts from 'original sealed death-god whose freedom is apocalyptic' to 'hijacked lesser fortune-deity whose soul-feeding produces a hollow, will-draining peace.'"* The patron is **Daikoku** (of the Seven Lucky Gods / Shichifukujin), whose root is **Mahakala** — a death/destruction deity wearing the mask of luck. → `design-decisions-session §1`'s sealed-death-deity sketch is **dead**; do not cite it.

2. **Descent target** — `story-keystone.md:24` carries an explicit `[SUPERSEDES]`: *"Any framing of the descent as conquest of peaceful realms (§11) or as re-enactment over already-won/drained ground."* The present-tense truth: **the descent is into living realms that have been *made to rebel*; the defenders genuinely fight a kindled uprising.** Expansion §11's "breach into a *peaceful* realm's soul-temple" is right about the *mechanism* (breach the soul-temple, fight the wardens of the font, not civilians) but keystone §14 overrides its *tone* (the realms are warm, vital, alive — the deadening has **not** happened yet; the faint wrongness is the inexplicable ferocity of a peaceful world's uprising). When expansion and keystone differ on whether the realms are alive: **keystone governs.**

**Systems vs story split:** for the *loop/systems* layer, `gameplay-loop-design.md` and `design-decisions-session.md` (§§3–12) govern. For the *story/frame* layer, `story-keystone.md` governs, then `story-expansion.md` for the detail keystone does not repeat. `design-decisions-session.md` §1 (patron) is the one section of that doc that is **superseded** — its systems sections are live.

---

## 3. Per-doc index

| Doc | Status | One-line | Governs | Routing |
|---|---|---|---|---|
| **story-keystone.md** | CURRENT (latest story canon) | The Manufactured Rebellion; the Deadening clock; Four-Veils knowledge stratification; player-selected-not-designed; naming lexicon (§18); **the first-reaping & god-speech system (§19); the reap-beat mechanical staging + Godot impl (§20)** | the story frame — supersedes expansion where they differ; §§19–20 lock the reap-beat design + impl contract | gandalf (story); drax/radagast (§§19–20 reap-beat impl) |
| **story-expansion.md** | CURRENT (story detail) | Patron = hijacked benign fortune-deity (Daikoku/Mahakala); peace-as-lobotomy; player-as-reluctant-antagonist; descent = soul-temple breach; Reincarnate-opening (believer→apostate) | frame detail keystone does not repeat | gandalf |
| **design-decisions-session.md** | CURRENT (systems) — §1 superseded | 14 decisions: kit count (launch ~100 / architect 400+, §3), 24×24 QD-grouping matchup matrix (§4), capstone-state probabilistic dimension (§5), gear model (§7), PvP level-50-only (§8), **co-op CUT** (§9), cross-cutting principles (§11), staging-logic checkpoint validation (§12) | engine/systems decisions; §1 patron sketch is dead | gandalf → gamora/rocket/star-lord |
| **gameplay-loop-design.md** | CURRENT (END-STATE AUTHORITY) | The master loop. §1a WB-Nemesis patent clearance; §8 Nemesis mechanic (lieutenant-becoming, +3 kept); §23 Run Model (25-min / 20-floor three-beat descent, conduit-harvest economy, hand-in-vs-keep micro-choice) | the loop the engine is built to satisfy | gandalf (design-fit); all seams |
| **performance-target-specs.md** | CURRENT (PERF AUTHORITY) | Godot density 50–150 simultaneous; GTX-1650 floor; Mac/Metal is the *flattering* machine | the horde-density + perf targets | drax/galadriel |
| **backend-networking-stack.md** | CURRENT (tech) | PvE server-light (Steam Cloud/identity/leaderboards); PvP post-launch (GodotSteam, ~40-CCU ceiling, architect-the-door) | networking posture | drax + knight-rider |
| **build-architecture.md** | CURRENT (tech) | Godot 4.7 pinned; ONE shared project (export presets, not parallel codebases); mobile-first; JSON→typed-Resource boundary; §4.2 team-topology rec | the build/runtime architecture | drax + radagast |
| **godot-agent-contract.md** | CURRENT (tech, frozen specs) | 3 frozen specs for the Godot assembly agent: geometry/scale/socket, character-scene template, Judge rubric + camera | the drax Godot-assembly contract | drax (primary) |
| **vfx-pipeline.md** | CURRENT (tech) | 2.5D Diablo/PoE look in Godot; mobile VFX floor | the VFX pipeline target | drax + galadriel |

*(The scored-narrated opening scene — `reincarnated_opening_scored_narrated_scene.mp4`, the "first completed scene" / trailer — remains on disk in the staging folder, gitignored as heavy media. It cannot be perceived by gandalf; route a frame-extraction + design-coherence read to galadriel if a perceptual pass is wanted.)*

---

## 4. What this set supersedes in PRIOR canon (the Path B correction/delete seed)

The v2 set re-registers the frame. The following prior-canon shifts are **named here** so the Path B purge + the patron-frame correction pass (tasks #3/#4) act on a precise list, not a vibe. *Thematic supersessions only — specific per-doc dispositions are confirmed in the Path B spine-membership classification.*

| Prior frame | v2 replacement | Affected prior canon (reconcile/correct, not blind-delete) |
|---|---|---|
| isekai / reborn traveler | death-faith / ascending conqueror | already noted in tracker PART 0.2 |
| **spirit guide** (warm future-self advisor-voice) | **RETIRED as an entity** (Matt 2026-06-30) — advisory function splits: **(A)** the **demigod-jailer** (antagonistic-helpful steerer/mentor, NOT the future self; keystone §16–17, §19.1) = **tutorial instructor**; **(B)** the separate caged **patron god** Daikoku/Mahakala (communed-with, unreadable §19.3) = **seldom-heard guidance**. *Banter / retort-axis owner OPEN — Matt deciding, flag #6.* | spirit-guide design docs; tracker III.9 |
| **original sealed death-god** | **hijacked benign fortune-deity** (Daikoku/Mahakala) | any story doc carrying the sealed-deity origin — **task #4 correction** |
| descent into dungeon/underworld | **breach into a living realm's guarded soul-temple** (siphon the soul-mirror, fight the wardens) | descent/dungeon framing docs |
| conquest of drained/peaceful realms | **manufactured rebellion in *living* realms** (keystone §14) | any "drained ground" / "re-enactment" framing |
| earth realm (contemporary-Earth) | time-agnostic **home realm** (same structural function: one creation, face propagation) | earth-avatar / cosmograph creation-moment canon; tracker III.9 |
| seasonal-release content model | engine content types / future-product scope | retired 2026-06-02; do not reintroduce |
| co-op / multiplayer combat | **co-op CUT** (PvP level-50-only, post-launch — §8/§9) | any co-op design surface |

**Discipline note:** these are *frame* supersessions. The descent-as-soul-temple-breach **keeps the word "descent"** and the mythic resonance; the patron reframe **keeps** the cosmograph (re-anchored as the patron's domain) and the reincarnation mechanic. Reconcile, do not amputate — the structure mostly survives; the *false origins* are what die.

---

## 5. Open contradictions surfaced (for Matt's ruling — task #5)

- **Flag #2 — "what banks from a run?"** `gameplay-loop-design.md` §8 (the Nemesis mechanic) keeps the **lieutenant-becoming** as a persistent gain (+3, you keep what you kill), but §23.3 states the **champion-body is NOT kept** at run-end. These need reconciliation: *what persists across the roguelite reset — the becoming/identity, or nothing of the body?* The likely intent: the **roster entry** (the record of who you became) banks; the **run-specific embodied power** resets. But the two sections read in tension and Matt should rule the exact persistence contract before the engine's per-kit-level model (tracker III.2) is specced against it.

- **Flag #6 — the loop-doc's "patron companion" IS the keystone's demigod-mentor (intra-set contradiction; added 2026-06-30).** `gameplay-loop-design.md` §§2c/14/15/16 makes the **patron deity** the voice-in-your-head antagonistic-helpful banter companion (build-helper/tutor, "you owe it" debt, defiance↔devotion retort axis, Hades/GLaDOS register) — "demigod" never appears. But `story-keystone.md` §§16-17/§19 (the latest story canon, which governs the frame per §3) puts that guidance/mentor voice on the **demigod-jailer** (§19.1 "demigod-mentor"; the Mercer voice) and makes the **patron god** the rare, *unreadable* caged deity (§19.3). Matt's 2026-06-30 correction ("the patron is a god; the demigod is the jailer") fixes the cosmology but not the loop-doc's labeling. *Does the §§14-16 companion subsystem — banter, "you owe it," retort axis, the §435 LLM-vs-templated tech decision — re-label from "the patron" to "the demigod-mentor" (patron god then the deeper caged deity)?* **gandalf-lean — PARTIALLY RULED by Matt 2026-06-30:** the spirit guide is now **RETIRED** and its function-split ruled — **(A)** the **demigod** owns the **tutorial-instruction** voice; **(B)** the caged **death-god/patron** owns the rare **seldom-heard guidance**. The residual OPEN question narrows to the loop-doc's **daily banter + defiance↔devotion retort axis** (§§15-16): *who owns the ongoing antagonistic-helpful relationship — the demigod-mentor or the death-god?* Matt is **actively deciding** it ("working through the decision regarding the banter"). gandalf offers (does NOT harden): the "captor who needs you" register fits the demigod-jailer better than a caged unreadable god — but it's **Matt's live call**; do NOT silently swap patron→demigod across the loop doc. Full write-up: flag-memo Flag #6.
- **Flags #3/#4/#5** (temporal-triad collapse · season→run molt-trigger · §1 device-orphans) live in full at `agentic_orchestration/gandalf/notes/2026-06-29-path-a-frame-reconciliation-flags.md`.

---

**Signed:** gandalf, 2026-06-29 (Path A integration). This index is CURRENT; it updates when the spec set changes. The LIVING tracker (`current-to-end-state.md`) measures the engine against this spec.
