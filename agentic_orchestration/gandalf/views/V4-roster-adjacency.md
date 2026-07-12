# V4 — Roster Adjacency Map (all 48: K1–K29 + H1–H6 + B1–B13)

> **⚠ SUPERSEDED same-day by `V4r2-roster-adjacency-rebuilt.md` (Matt throw-out ruling 2026-07-12).** The roster-side inputs here came from the mobile-transcribed encoding (`rdr-roster-kits.jsonl`), which Matt ruled corrupted-by-lack-of-knowledge — proven (mobile-K23 ≠ real K23 Monk; "unrecoverable" kits all named in PART F). **§1 method laws SURVIVE and govern V4-r2 verbatim.** §2–§3 roster rows, F1's "MAC-FILL BACKFILL" unit, and F4's K23↔B12 consolidation flag are RETIRED. Corpus-side content remains valid.

**Date:** 2026-07-12 · **Author:** gandalf · **Source:** `rdr-kit-atlas-v3.csv` (506 placed canon rows joined against 35 roster + 13 bench rows) · **Commission:** Matt — "Run V4 to completion, including the bench kits."

---

## 1. Method — three rungs, evidence-bearing matches only

- **R1 identity-grade:** mutual-wildcard compatibility over all 12 slots (6 sampled + 4 measured + econ + elem), **≥5 comparable slots** required.
- **R2 BC-grade:** compatibility over the 10 BC slots (econ/elem dropped — the vocabulary-artifact fix), **≥4 comparable**.
- **R3 basin:** bc6 sampled-prefix compatibility, **≥3 comparable**; counted in distinct games.
- **Whitespace kits** get nearest-neighbor texture: closest positives (mismatch count + differing slots) + nearest **negative twin** within d2.
- `q` = comparable-slot count of a match (match quality). Matches vs both-abstain slots carry no evidence.

**Two method lessons (bugs caught mid-run, now law for the render harness):**
1. **Promiscuous-matcher guard:** low-completeness corpus keys (VS "Big Trouser," 4 known slots) wildcard-match half the roster vacuously. Without comparable-slot minimums, K3/K4/K8 falsely classified LINEAGE. Matches must be evidence-bearing.
2. **Multi-char wildcard:** the 2-char econ/elem groups abstain as `'__'`, which fails a naive `=='_'` test — silently blocking every roster kit with element-abstain from R1-matching any corpus kit with a known element (K7 was matching HoT filler instead of Tornado Shot). Wildcard test = *all chars are* `_`.

## 2. Classification (48 kits)

**8 LINEAGE · 4 VOCAB-RECOVERED · 2 WHITESPACE · 22 INSUFFICIENT (<4 BC slots) · 12 NO-COORDS**

| Kit | Name | bc | Class | R1/R2/R3g | Strongest evidence |
|---|---|---|---|---|---|
| K1 | Heavy Barbarian (D2 WW lineage) | 6 | **WHITESPACE** | 0/0/0 | NN d1(commit): Hammer of the Gods Titan (poe2), Smith of Kitava (poe2); d1(tempo): BvC (d2) · **⚠ neg-twin d1: Leap Attack Barbarian (d2)** |
| K2 | Light Fighter | 5 | **LINEAGE** | 16/26/13 | Boneshatter (poe1,q6); Bash Barbarian (d4,q6); WW STR baseline (undecember,q6) |
| K3 | Polearm Soldier | 5 | **WHITESPACE** | 0/0/0 | NN d1(range): Spectral Shield Throw (poe1); d1(tempo): Mjölner (poe1) · **⚠ neg-twin d1: Charged Dash (poe1)** |
| K4 | Thrown-Heavy / Atlatl | 5 | VOCAB-REC *(q4-marginal)* | 0/2/2 | Gorgeous Moon (vs,q4); Meteor Strike (hot,q4) — near-whitespace pending mac-fill |
| K5 | Ancestor-Warrior | 5 | **LINEAGE** | 1/3/3 | Emberquake Engineer (tl2,q6) |
| K6 | Dagger Assassin | 5 | **LINEAGE** | 11/24/10 | Whirlwind Rogue (tq2,q6); Lightning Strike, Frost Blades (poe1,q6) |
| K7 | Archer | 5 | **LINEAGE** | 20/30/13 | **Tornado Shot; Wander (poe1,q6); Quill Volley (d4,q6)** — sits on the V2 identity cell |
| K8 | Crossbow Sniper | 5 | VOCAB-REC *(q4-marginal)* | 0/2/2 | Gorgeous Moon (vs,q4); Meteor Strike (hot,q4) — near-whitespace; PoE2 crossbow post-cutoff check owed |
| K9 | Twin-Blade Fencer | 5 | **LINEAGE** | 10/15/7 | Umbral Blades (le,q6); Spiral Volley (poe2,q6) — the V2 le+poe2 twin cell |
| K10 | Falconer | 5 | **LINEAGE** | 2/2/2 | Ice Crystal Arrow (undecember,q6); Bowazon (d2,q6) |
| K11 | Trap Assassin | 5 | **LINEAGE** | 1/1/1 | **Trapsin (d2,q6) — self-identifying** |
| K12 | Standard Wizard | 3 | INSUFFICIENT | 0/0/14 | basin-member of the 14-game caster basin; mac-fill |
| K13/K14/K19/K21/K22 | — MAC FILL — | 0 | NO-COORDS | — | identity unrecoverable from transcript |
| K15 | Path-substrate (Option C) | 1 | INSUFFICIENT | — | mac-fill |
| K16–K18, K24–K25 | proxy-octet kits | 1 | INSUFFICIENT | — | mac-fill (octet coordinates live engine-side) |
| K20 | Orbiter-Spiral (Hammerdin coord) | 4 | VOCAB-REC *(q4-generic)* | 0/32/14 | neighbors are attribute-generic (Boneshatter q4) — **named Blessed-Hammer lineage NOT confirmed by join; verify at mac-fill** |
| K23 | Path-substrate channel-class | 4 | VOCAB-REC | 0/9/7 | WW Barbarian (di,q4); WW STR baseline, WW CwC (undecember,q4) — the channel-spin neighborhood |
| K26–K29 | ex-bench (Blood/Thorns/B-S/T4) | 2–3 | INSUFFICIENT | — | mac-fill (mechanics all have-core) |
| H1 | Guard Orbital -lite | 3 | INSUFFICIENT | — | mac-fill; GX-09 designed-addendum |
| H2–H4 | — MAC FILL — (hybrids) | 0 | NO-COORDS | — | identity unrecoverable |
| H5 | True Battlemage | 3 | INSUFFICIENT | 0/0/14 | caster-basin member; mac-fill |
| H6 | Timing-Axis Kit | 2 | INSUFFICIENT | — | mac-fill |
| B1–B3 | Blood Mage / Thorns / B-S Warrior | 0 | **RETIRED-INTO** (K26/K27/K28-K29) | — | promoted shells — no fill needed; successors carry coordinates |
| B4 | Bone-Wall Necromancer | 2 | INSUFFICIENT | — | mac-fill; GX-18 adjacency (Q15 Walls) |
| B5 | Teleport Sorceress | 3 | INSUFFICIENT | — | mac-fill; blocked-new (blink verb) |
| B6 | Dash-Weaver Martial | 3 | INSUFFICIENT | — | mac-fill; DL-02 movement-verb adjacency |
| B7 | Ring of Shields / Interceptor (full) | 3 | INSUFFICIENT | — | mac-fill; H1 is its -lite |
| B8 | Nested-Orbit Epicycle | 2 | INSUFFICIENT | — | mac-fill; GX-09 deep variant |
| B9 | Collapse-Bomb Caster | 2 | INSUFFICIENT | — | mac-fill |
| B10 | Vaal Blade Vortex (detach-and-seek) | 2 | INSUFFICIENT | — | mac-fill; GX-09 |
| B11 | Inversion Summoner | 1 | INSUFFICIENT | — | mac-fill; summon pillar |
| B12 | Spin-to-Win (D2 WW / Cyclone / Warpath) | 7 | **LINEAGE** | 4/7/6 | **WW STR baseline (undecember,q8)** — strongest single join in the table; Eye of Reckoning (gd,q7); Cyclone (poe1,q7); Warpath (le) |
| B13 | RIVAL Exile (enemy champion) | 0 | NO-COORDS | — | **scope question: enemy-champion, arguably not a player-kit row at all** |

## 3. Findings

**F1 — The join starves on OUR side, not the corpus side.** 34/48 kits sit below the evidence threshold, and the missing coordinates are not research — they are **engine-side transcription** (Part F roster table, substrate coordinates, the octet definitions). The mobile session flagged this as "mac-fill"; V4 quantifies it. Mac-fill queue: 8 identity-unrecoverable (K13/14/19/21/22, H2–H4) + 22 partial + 1 scope ruling (B13) − 3 no-fill-needed (B1–B3 retired shells). **Backfill then re-run V4 — the rerun is free once coordinates land.**

**F2 — Every full-coordinate roster kit lands where its name claims, except the deliberate two.** All 8 LINEAGE kits join their named genre lineage at q6+ (Trapsin→Trapsin; Archer→the archer identity cell; Fencer→the le+poe2 twin cell). The join machinery *works* — which makes the two whitespace claims trustworthy rather than artifacts.

**F3 — The two whitespace claims have narrative-grade adjacency texture.** K1: the genre ships its coordinate at **wind-up** (PoE2 Hammer of the Gods d1 on commit alone) but never at **channel**, and the nearest genre *failure* is Leap Attack (d1). K3: nearest success differs only on range (Spectral Shield Throw), nearest failure is Charged Dash (poe1's canonical mid-range-melee dud, d1). Frontier bordered by one failure each = **proceed-with-eyes-open, not sealed ground.** → V7 consumes this.

**F4 — Channel-spin family structure (K1/K23/B12) is deliberate, not redundant.** B12 holds the canonical genre spin coordinate (q8 join), K23 holds the path-substrate variant (same neighborhood at q4), K1 holds the never-shipped slow-spiky variant. Three occupants of one basin with distinct roles: genre-anchor / substrate-native / whitespace-probe. **K23↔B12 overlap is the one true consolidation question** — same corpus neighborhood, and B12 is benched while K23 is roster. Matt ruling candidate at anchor-proposal time.

**F5 — K20's Hammerdin claim is unverified by the join.** Its R2 neighbors are attribute-generic melee (q4), not Blessed Hammer. Either its measured slots are mis-transcribed or the Hammerdin coordinate differs from what Part F recorded. Verify at mac-fill before it seeds any anchor decision.

**F6 — Tier-2/3 games carry real evidence weight** (Matt's question A, revalidated): Athena Dash Core (hades1) and Swordsman (hot) at q6 for the fighters; Emberquake (tl2) as K5's only identity match; Whirlwind Rogue (tq2) leading K6. The breadth tiers are not decoration — they complete lineages T1 leaves thin.

## 4. Feed-forward

- **→ MAC-FILL BACKFILL (next unit, gates everything):** transcribe BC cells from engine-side canon into the atlas for the 31 fillable kits; rule B13 scope; then re-run V4 (script is deterministic).
- **→ V7:** whitespace + negative-twin adjacency (K1/K3 textures above are its seed rows).
- **→ ANCHOR PROPOSAL:** R1-density kits (K2/K6/K7/K9) mark basins where anchors are cheap; B12's q8 makes it the natural spin-anchor candidate despite bench status.
- **→ Render harness (specialist work once housing lands):** the two method lessons in § 1 are law for the deterministic implementation.

## 5. Reproduction

Deterministic joins over `rdr-kit-atlas-v3.csv` (session transcript 2026-07-12): mutual-wildcard with multi-char abstain groups, comparable-slot minima (R1≥5 of 12, R2≥4 of 10, R3≥3 of 6), positives-only matching, negative twins reported separately, Hamming nearest-neighbor over BC-10 for whitespace kits.
