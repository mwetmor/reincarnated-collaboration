# Run C-9 charter: Illuminated Archive (challenger register A/B) v1.0

> **STATUS:** v1.0, gandalf (RUN-CONDUCTOR), 2026-09-26. Matt: *"you are a run conductor.. please design the run and conduct it. Add appropriate Matt gates."* Forks were drained live in the same session (rulings R-C9-0 below). Ledger: `astra_test_01/burst/runs/C-9/ledger.json`. jack-ryan Gate-2 at close.
> **Supersedes** the two same-day hand-off dispatches (`agentic_orchestration/dispatches/2026-09-26-{gandalf-c9-illuminated-style-gate,drax-c9-cathedral-greyroom}.md`) as the run's governing text. The drax dispatch stays the grey-room work order.
> **Register status:** a CHALLENGER test. `style-register.md` and the H1 lane register are unchanged unless Matt rules otherwise at M7.

## 0. Intent

Answer: **does Matt prefer the Illuminated Archive register to H1 in play?** Illuminated Archive means painted-book subjects (characters and scenes) rendered in FFT-watercolor technique. It is tested as a 2×2 (cliffside and cathedral, each in H1 and in Illuminated), plus a character in each register, ending in a playtest with a style toggle.

## 1. Bounded substrate

| Item | Path |
|---|---|
| Brief (amended by the refs README) | `matt_notes_handoff_docs/rdr-art-illuminated-archive-brief.md` |
| References, ledger, rules | `matt_notes_handoff_docs/rdr-art-illuminated-archive-refs/` (`README.md`, `ledger.jsonl`, `metrics-2026-09-26.md`) |
| **Attach guard** | only ledger rows with `attach_to_generator: true` may enter a brief, workdir or `-i`. Enforced mechanically by `runs/C-9/conductor_scripts/refs_guard.py` before every wave. |
| A-side substrate (H1) | cliffside: `runs/C-3/artifacts/CS-chunk-A/chunk_A.png` and the shipped cliffside build; character: the Keeper |
| Scene geometry | cliffside: `runs/C-3/artifacts/CS-guides/chunk_A_guide.png` and the v4 grey room; **cathedral: the KC2-PLAY burning nave, the whole design** (R-C9-6, R-C9-7): `gandalf/notes/2026-09-20-kc2-play-cathedral-reframe-and-crack-law.md` (register, crack law, one-way hazard entrances: fire, blue-fire crypt, breaches and gallery stair; funnel to the middle; south-façade entry) and `…-arena-scene-plan.md` (layers, sunset, bare first, the fallen window); Matt's rulings KP-14/18/19/28/29 ("art leads the boundary"); arena guide lineage from drax `9c947ffe`. **S1 / S4 / S5 (layout, pools, world beyond) are PARKED with Matt for a sitting; C-9 does not pre-empt them, and P6 waits on it.** drax's C-9 Antwerp grey room (`3f9ae23c`) is superseded and kept as record. |
| Camera | ratified GD `player_lock` (yaw 47°, pitch 52.95°), orthographic canvas; Keeper at 12.5 % of 1080p = 130 px |
| Run register card | `runs/C-9/REGISTER_CARD.md` (conductor-owned data, sha-pinned per burst in the ledger) |

## 2. Rulings carried (R-C9-0; Matt, 2026-09-26, verbatim in the refs README)

- **Merge rule:** the painted book supplies subject, composition, iconography and palette; FFT supplies rendering (wash handling, pale highs, ink and hatching, uneven wash). This holds for characters and scenes alike.
- **Characters:** A = the Keeper. B = the Lalaing knight (Getty Ms. 114 fol. 129v, right-hand figure), skirt removed, poleaxe. The EoR Warlord is dropped.
- **Cathedral:** the Belles Heures choir is the style anchor; Spinola fol. 185 is architecture only; Antwerp is the building on the Crucible footprint.
- **Cliffside scenery:** the *Très Riches Heures* calendar plus Belles Heures landscapes; June Sainte-Chapelle, July bridge, September Saumur (the Keeper's domain).
- **FFT references are look-only** (copyrighted); the FFT half is carried in text. Matt's two Astra images are the fallback arm, not the default.
- **Brief amendments:** rich colour at a moderate value, vivid only on accents; hatching permitted (a variable at M6); imperfection designed, not random; `#00ff00` plate.

## 3. Sequence, phases and Matt gates

| Phase | Work | Seat | Gate |
|---|---|---|---|
| **P0** setup | run dir, ledger, conductor scripts, run register card, refs guard, texture patches, grey scale silhouette | conductor | — |
| **P1** tooling | **T5a: run-scoped register card.** `render_brief` and `run_burst` use `runs/<run>/REGISTER_CARD.md` when present; its sha is ledgered; runs without one stay byte-identical | Astra TOOLING → conductor DRIFT-CRITIC → freeze | — |
| **P2** style gate | wave of 4 GENERATE bursts: scene arm (chunk_A guide) × {ink, warm} and knight master × {ink, warm}, 2 images each | Astra | — |
| **P3** evaluation | CHECK (O1 palette + the C-9 tone metrics) + JUDGE (separate instance, C-9 rubric, hidden control = `chunk_A` must fail painted-book fidelity) | Astra + conductor | — |
| **M1** ⛔ | **STYLE GATE.** Packet: merged chunk vs `chunk_A`, knight vs Keeper, at game scale and full size, with numbers. **Matt rules:** GO (and picks the line arm) / ITERATE / ADD-ASTRA-ARM | **Matt** | nothing past M1 fires without it |
| **P2′** (parallel) | cathedral grey room on the Crucible arena | drax (named agent) | — |
| **M2** | ~~GREY ROOM~~ **Withdrawn (R-C9-6):** the cathedral follows the KC2-PLAY nave rulings; no new layout to approve | — | |
| **P4** | knight turnaround (masters per direction) | Astra | — |
| **M3** ⛔ | **TURNAROUND.** Includes the mirroring question: the H1 card forbids mirroring; C-8 mirrored | **Matt** | |
| **P5** | cliffside B full re-derivation: chunks from the M1 anchor, parallax from the TRH landmarks, dressing | Astra | — |
| **P6** | cathedral H1 and Illuminated paints from the M2 grey room | Astra | — |
| **M4** ⛔ | **SCENES.** Assembled cliffside B, cathedral A and cathedral B | **Matt** | |
| **P7** | motion: idle and walk in 8 directions; **imperfection three-way** (clean / carried by Grok / designed boil at 8–12 fps; hatching a variable) | Grok + conductor tools | needs the Grok top-up (`matt_to_do`) |
| **M5** ⛔ | **MOTION.** Matt picks the imperfection arm in motion, with 20 mobs on screen | **Matt** | |
| **P8** | playtest build: scene picker + style toggle; cathedral on the KC2-PLAY arena geometry | drax | — |
| **M6** ⛔ | **PLAYTEST.** Matt's and Hale's verdicts, logged separately, beside the conductor's metrics | **Matt** | |
| **M7** ⛔ | **REGISTER RULING.** Adopt, reject or keep as a dialect; any adoption is a register change and routes to canon (`style-register.md`) via recognition → validate → commit | **Matt** | then jack-ryan Gate-2, close |

## 4. Budgets

- **Images:** M1 cap 16 (8 planned + retries). Run cap 400, reported at every gate.
- **Grok:** P7 only; its balance is Matt's.
- **Codex:** Astra last ran clean 2026-09-21 (KC2-PLAY KP-B1g). H-C7-1 is treated as stale; T5a is the live check.

## 5. HALT rules

The lane's standard rules apply: two consecutive experiment FAILs; two VOIDs in a row; a JUDGE passing its control twice; three rate-limit backoffs; any write outside `out/`; a cap reached; any medium or bar change.

**C-9 additions:**
- **H-guard:** a look-only file reaching a brief or workdir. Refs-guard failure is a HALT, never a retry.
- **H-register:** any request to apply the Illuminated register outside C-9.

## 6. Carried disciplines

- The lane's invariants (`mechanical-process.md § 1`) and HOWTO procedures, including the concurrency law with KC2-PLAY (the heavy lock; FREEZE_NOTICES).
- Prompts are generated artifacts: the task text references the card, and FFT is described, never named. No franchise, studio or living-artist names.
- Veto-open ledger.
- `--only` commits.
- **Push:** none without Matt's word. C-9 has no standing push pattern.

## 7. Open-questions gate (ARCHITECT)

**RESOLVED:** see § 2.

**GATED + TRACKED:**

| Question | Gate |
|---|---|
| Line weight | M1 |
| Mirroring | M3 |
| Cathedral lighting (night by the engine light radius) | M4 |
| Hatching and imperfection arm | M5 |
| Adoption | M7 |

**Deferred to Hale/Matt at M7, not needed before:** brief § 9 items 2–4 (gold-leaf semantics; literal public-domain portraits; Children of the Planets). Item 1 (the hand per act) is moot for this run, which uses one house hand.

**OPEN:** none blocking P0–M1.
