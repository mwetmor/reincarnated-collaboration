# NEXT-SESSION RECOMMENDATIONS — what to start with, in what order, and why

> **Authored:** gandalf, 2026-07-03, at Matt's halt directive (Doc 2 of 2). **Companion:** `2026-07-03-demo-readiness-run-full-findings.md` (Doc 1 — the full record; this doc assumes you've read at least Doc 1 §1).
> **Character:** recommendation document. Doc 1 reports what IS; this doc says what I think should happen next and why, with the tradeoffs named. The two decisions in it are **yours** — nothing here pre-commits them.
> **State in one line:** the run is CLOSED and clean; 700 martial kits banked; 35 finalists flavored; **the demo roster cannot complete until you rule the summoner/caster question**, and that ruling is the only thing on the board that everything else waits on.

---

## §1 START HERE — the summoner/caster ruling (the gate on everything)

**File:** `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (read top-to-bottom: original framing → my addendum → gamora autopsy → **jack-ryan's review verdict, whose corrected decomposition is the authoritative ruling input**).

**What changed since the file was opened.** The question began as "summoner emission." The evidence now shows **three absences sharing one recovery vehicle**: no emitted summoners (gen-path doesn't exist), no casters at all (4 cells never composed + 6 failed clear-shell calibration), no role variety (4/4/2/2 invariant). And the autopsy **improved the odds**: the 6 composed caster cells already pass the boss shells — their recovery is a band/geometry calibration question, not a mana-economy rebuild. The structural half (4 zero-composed INT cells + the summon path) is the real build.

### The options as they now stand

| | Option 1 — build the gen-path, re-fire as batch 2 | Option 2 — curated summoner seats + formal C/G4 amendment |
|---|---|---|
| What ships | Emitted summoners + casters + role variety (batch-2 survivors) | Martial-only emitted roster + 2 curated summoners, registry-flagged `curated-not-emitted` |
| Consistency | Consistent with your 2026-07-02 ruling ("balanced and pipeline emitted") as written | A **knowing reversal** of that ruling (the §5.2 hand-authored language it leans on is struck) |
| Cost | A scoped engine build (math-first + Gate-1) + one registered batch-2 run (~6h class, unattended-capable once specced) + calibration leg | Near-zero engine cost; decisions-log + spec v1.2 amendment + registry provenance field |
| Risk | Scope not yet bounded — the 4-cell INT composition gap is undiagnosed (see §2) | **Demo roster ships with zero caster-fantasy kits** — martial resource-feel across all seats; element pips can fake a mage *read* but not a mana economy |
| Player consequence | Roster carries the "raise the dead" promise on emitted content; caster archetype exists | The minute-one summoner promise is satisfied by curated content; the caster archetype is absent from the demo entirely |

### My recommendation (unchanged from the ruling session, sharpened by the autopsy): **Option 1.**

Grounds: (a) it is the only path consistent with your own 2026-07-02 integrity ruling; (b) one batch-2 vehicle now recovers three absences — the value of the build tripled while its calibration half got cheaper (bosses already cleared); (c) a demo roster with zero mana-economy kits is a genre-legible gap — Diablo-class ARPGs read "no caster class" as an unfinished roster, not a stylistic choice. **But** Option 1's build scope is honestly unbounded until the INT-composition gap is diagnosed — which is why §2 exists.

**If you rule Option 1, the asks on record:** authorize the gen-path build dispatch (math-first + Gate-1; new cross-seam `proxies` emission contract → ADR-004 MIGRATION) **with scope covering both structural gaps** — summon composition AND non-melee-INT composition — plus a calibration leg for the 6 clear-shell caster cells and the near-miss `melee_high_flat_dex` (6.00/9, the cheapest win on the board).
**If you rule Option 2:** the C/G4 amendment lands as decisions-log + spec v1.2 fold (jack-ryan), and the registry gains the `emitted`/`curated` provenance field (G9 fast-pass). I will file the design-consequence record (martial-only demo roster) so the reversal is priced, not silent.

---

## §2 The cheap evidence move you can fire BEFORE ruling (recommended)

**Read-only rocket diagnostic: why do the 4 non-melee INT cells compose zero candidates?** (~1–2h, no fights, no code changes — trace the composer path for those stems.) This is the one place where the ruling is currently exposed: if the cause is a config/eligibility filter, Option 1's scope shrinks sharply; if it is a missing composition capability adjacent to the summon gap, Option 1's scope is confirmed and its estimate hardens. Firing this first turns the ruling from "commit under scope uncertainty" into "commit against a named build." If you'd rather rule immediately on the corrected decomposition, that is also defensible — jack-ryan's verdict block was written to support exactly that.

---

## §3 Independent of the ruling — the G7a roster session (can run same session, either order)

**All inputs are complete for the 7 martial seats:** 35 flavored finalists (5 per seat, mixed-element + mono anchor), element pip live in the loadout, shortlist doc at `agentic_orchestration/w3-batch1-flavor-finalists-2026-07-03.md`. The pick is 1-of-5 per seat; wholly yours (G7a). Recommended mechanics: open the loadout app against the bundle-of-record, walk seat by seat; the mono anchor in each seat is the baseline read — pick it only if the mixed tail's flavor doesn't earn its secondary. Summoner seats (2–3) stay empty pending §1; caster seats don't exist yet (also §1).

---

## §4 Housekeeping queue (sub-hour items; any can ride whichever session fires first)

1. **gamora's 4 doc-only autopsy corrections** (jack-ryan-required; the BLOCKed plank must be re-grounded in the decision file — jack-ryan's block already carries the corrected text if you rule before gamora lands them).
2. **Spec v1.2 hygiene** (jack-ryan): strike the `ProxySpawn` lift + the unprovenance "2026-06-24" reference from criterion C — owed under BOTH ruling outcomes.
3. **Defensive-cohort fixture artifact** (gamora): `eligible_encounters_total=6` < floor 9 means Defensive can never pass, for any kit — fix the totals or document as-designed.
4. **API key rotation** (you): the flavor key transited chat this session. Hygiene verified clean in git, but rotate it.
5. **KR tracker-delta folds** — the remaining queue from the handoff @ `1148c7c`.
6. **E4 ECHO ally-attack channel** — named prerequisite; sequence it with (not before) the Option-1 build if that's the ruling, since both touch ally/proxy runtime.
7. **GLASS CANNON fragility stat pass** — gates the "glass" flavor texture claim; low urgency until roster picks land.

---

## §5 What NOT to start with (anti-recommendations, so the queue doesn't self-scramble)

- **Do not fire batch 2 before the ruling + the gen-path scoping.** A re-fire now repeats the known outcome for 4 cells (zero composed) and burns a 6h-class run partially blind. One batch, fired once, after the build — that's the whole point of the batch mechanism.
- **Do not re-tune clear-shell bands in isolation.** The calibration lever on the 6 caster cells is real, but sequencing it before the gen-path scoping risks tuning bands against a population that batch 2 will change anyway (proxy-live casters will not have solo-caster tempo).
- **Do not flavor the 665.** Shortlist-first was the right call; widen only if a G7a seat's five finalists all miss — per-item resumability makes that incremental.
- **Do not blind-purge the spec.** v1.2 hygiene is two named strikes, not a rewrite.

---

## §6 The recommended session shape (concrete)

1. **Open:** read Doc 1 §1 + the decision file's jack-ryan verdict block (~15 min).
2. **Either** fire the §2 rocket diagnostic and rule when it returns (same session, ~2h later), **or** rule immediately on the corrected decomposition. Then authorize the consequent dispatch (Option-1 build spec, or Option-2 amendment).
3. **While that runs:** the G7a roster session (§3) — it is pure pick-work, needs no engine state, and finishing it means the demo roster is complete the moment the summoner/caster seats resolve.
4. **Close:** housekeeping sweep (§4, items 1–4 are each sub-hour).

That sequence ends the session with: ruling made, build (or amendment) dispatched, 7 roster seats picked, hygiene clear — and the project's critical path runs through exactly one thing (the batch-2 build or the amendment fold), which is where it should be.

---

**Signed:** gandalf, 2026-07-03. The ruling is yours; the recommendation is mine; the evidence is in Doc 1 and the decision file, all corrected and cross-reviewed.
