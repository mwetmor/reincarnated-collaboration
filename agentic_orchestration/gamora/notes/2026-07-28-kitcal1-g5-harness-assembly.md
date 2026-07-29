# KIT-CAL-1 — G-5 HARNESS ASSEMBLY (findings)

**Run:** `KC1-2026-07-27` (KIT-CAL-1) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Author:** gamora (simulation seam), 2026-07-28
**Engine tag:** `gamora/v-g5-harness-1` · **COMMIT-NEVER-PUSH** (conductor pushes)
**Math / assembly note (the pin record):**
`reincarnated-engine/src/reincarnated/simulation/math/g5-harness-assembly-2026-07-28.md`
**MIGRATION:** `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`, entry dated 2026-07-28
**Gate 2:** REQUIRED, **NOT self-cleared.**

> **G-5 HAS NOT BEEN EXECUTED.** This is assembly. The dry-run smoke below is a plumbing proof; it
> reads no band and grades nothing. G-5 fires on the conductor's go, after Gate-2.

---

## 1. Headline

The harness is built and the plumbing carries current on all four tiers and both arms. **The dry
run found two defects — one mine, one the tree's — and the tree's is the one worth the
conductor's attention**, because it would have made G-5 report a fixture comparison it never ran.

---

## 2. THE FINDING — the received-side mirror had no producer

The smoke reported **`intake = 0.00 %maxHP` on every tier** while the boss arms reported **721 HP
of leech healing**. Those cannot both be true: leech heals only into headroom, so healing means
damage was taken.

`ReplicaFrameSink.on_hit` has carried **documented received-side semantics since KF-5** — *"the
received-side mirror (mob→player, `source_is_player=False`) labels `pct_postmit` ALSO as
`pct_received` so the Godot received floater reads it directly."* The mob→**player** damage channel
is a bespoke inline block that **never called it**. The mob→**ally** branch one screen above routes
through `_apply_skill_damage` and emits; the player branch does not.

So the contract had **no writer**:

- **Every replica trace ever emitted shows a player who takes no damage.**
- A consumer computing intake from the frame stream reads zero and **cannot distinguish
  zero-intake from unemitted-intake** — a false negative that looks like data.
- **For G-5:** N-7 through N-11 and the **entire S-3 hazard-shape signature** would have read
  identically zero. The harness would have produced numbers, passed its own asserts, and been
  wrong in the one direction nobody checks.

Same defect **class** jack-ryan BLOCKed in G-5 Wave 0 (a struct contract whose carrier had no
writer, with my own evidence hiding it). Repaired at the mob→player site — pure read, downstream of
every mutation, `None` on the default no-sink path, `delivered` overkill-clamped so both sides of
the trace mean the same thing. Guarded by a test written to fail if it regresses.

**Routed, not owned by this run:** this predates G-5 — it is **REPLICA-1's gap**. G-5 is simply the
first consumer that needed the received side. The other consumer is **drax's Godot/REPLICA lane**;
MIGRATION §2 states it for him. Anyone who has drawn conclusions from replica-frame intake should
re-read them.

**Second defect, mine:** `A-ENC-1` segmented encounters on *kill* gaps and fired on the boss tier at
23.1 s — which is just what a 14,812 HP grind looks like between the escorts dying and the boss
dying. `S1-gap5s-v1` cuts on combat **activity**, so the assertion now walks the activity series.
Widening the tolerance would have hidden C being computed against the wrong denominator at exactly
the tier where the A/B arms live.

---

## 3. Pins — what is enforced, and where

Full pin→code map at assembly note §10. The load-bearing ones:

| pin | enforcement |
|---|---|
| trash + champion HP **verbatim** (§14.19) | `TRASH_ROWS` / `CHAMPION_ROWS`, grade-tagged. Champion = **the frame-287 roster verbatim** (813 / 649 / 326×2) — the one tier whose entire opposition HP vector is measured |
| boss = Primordian 14,812 + trio | `boss_rows()`; **trio BUILT** (protos were already extracted) |
| mixed-pack hero = **MEASURED 4,702** | `HERO_MEASURED_HP` + `A-HP-3` fails if it is ever re-derived |
| A/B arms boss-only, leech as DOOR VALUE | `A-ARM-1` / `A-ARM-2` |
| arms **DISTRIBUTIONAL, not paired** | `A-ARM-3` — structural: no paired-delta surface exists |
| trash + champion sustain-free + insensitivity | `INS-1` |
| one body, not two (§14.22(1)) | `A-HP-2` — entity `max_hp` == kernel `max_hp`, per fight |
| O-d is the only leech to spatial HP (§14.22(2)) | `A-ARM-2` + NS-3 inherited |
| no accidental `freeze` (§14.22(3)) | `A-FRZ-1` — walks player kit AND every mob roster |
| P-1 W-c · P-3 normalized units · P-4 · P-5 · P-7 | assembly note §10 row-by-row |

---

## 4. The 1607 reconciliation — both halves

The conductor asked me to verify what the compiled kit carries. It carries **1600** (kit-spec v2 §2,
pre-G-8). Resolved two ways:

1. **`POOL_R3 = 1607.0`.** G-8's still-side orb ladder (…747 → 759 → 1600 → **1607**) supersedes it.
   The +0.44% moves no band.
2. **The half that matters more, and it was not stated anywhere:** **W-c *is* R2b**, and the
   759→1600 gear step lands at the R2/R3 boundary — **after** the window. So **the canonical G-5
   player pool is 759**, and 1607 belongs to the **R3 comparison arm alone** (report-only; it exists
   to serve S-2 and S-3). A harness that had "corrected 1600 to 1607" and run the whole comparison
   at 1607 would have been precisely wrong.

`1600` appears nowhere in the harness as a live literal (AST-checked, so the prose explaining the
supersession is still allowed to name it).

---

## 5. Trio protos — AVAILABLE, and used

Not a gap. Legolas's HP re-grade §4 Tier 3 already carried both escorts: classification,
life-modifier source, base-attack table, controller, attack-speed/run, slot counts, resistances,
base damage bands and raw ability slices. Built as **Deepmire Vanguard 577** (cl 10) + **Deepmire
Evocator 846** (cl 11), encounter total **16,235**. The trio's **cold identity is modelled on all
three actors** (both escorts carry cold riders; the Evocator is a ranged cold caster) — the HP
re-grade warns that generic-melee escorts would under-represent the cold channel by ~⅓ of incoming
events. **Nothing was invented.**

---

## 6. HALTs, carried not smoothed

- **HALT-1 — boss damage is HELD.** §14.10's hold stands and legolas is explicit: *"Primordian must
  not enter G-5 damage pinning until the clamp lands."* So it enters as a **swept named parameter**
  over the G-5a **measured** all-tier band `(33, 50, 67)`, declared in the artifact; the boss
  verdict must be read across the sweep, not at a point. The measured **260.50 post-mitigation
  ceiling** is a **falsification** gate (`A-DMG-1`), not a calibration.
- **HALT-2 — `primordian_frigidring` NAMED-ABSENT.** Two independent sufficient reasons: its
  magnitude is inside the held clamp, and compiling a `freeze` emitter is forbidden by §14.22(3)
  (post-wake, shatter is corpus-dormant, not structurally dormant). **Consequence in the honest
  direction: the sim boss is LESS bursty than the fixture boss, biasing the sim player toward
  SURVIVING where Matt died.** Per C-7 that is bias, not conservatism, and the boss verdict carries
  it.
- **HALT-3 — crit is not in the trace.** The rider asks for it; the resolver crits but no call site
  logs it (my own P-6 finding). Surfacing it means threading a return-shape change through
  `resolve_spatial_hit` — the mechanism change P-6 declined to glue. Not built. Named.
- **HALT-4 — escort damage rows D-HELD**, ride HALT-1's sweep by inheritance.

**One deviation with reasons (D-1):** Arm A's jitter band (3.25–6.75%) is **implemented but
defaulted OFF**, arms pinned at 0.050 / 0.080. The flip rule compares distributions; jitter adds
variance common to both arms and orthogonal to the quantity under test, which can only reduce the
test's power. Available as `--arm-a-jitter` if the conductor wants the roll variance represented.

---

## 7. Replay-trace rider (R-KC1-19) — **RIDING**, fallback not needed

`g5-replay-trace/v1`, a **strict superset** of `replica-frame/v1`: every v1 record emitted
unchanged, plus a `g5_header` (run id / tier / arm / seed / kit id / **opposition roster with
per-row grades** / door values / named-absent mechanisms) and a `leech` event.

**The conductor's premise correction is honoured exactly:** leech events come from **the O-d door's
own heal-application site**, read at the per-hit boundary from the two cumulative counters the door
already maintains. The kernel `on_lifesteal` the rider assumed has never been emitted in spatial.
Nothing is derived — the trace *differences a counter the door owns*, and a test reconciles the
event deltas to the door's own total.

Deterministic given the seed (byte-identical, proved). **Dropping it changes no metric** (proved) —
which is what keeps the §4 fallback cheap if the conductor ever wants it.

---

## 8. Dry-run smoke — PASS (plumbing)

8/8 static pins · 4 tiers · both boss arms · 2 INS-1 · 5 traces.

| tier | arm | leech | winner | t (s) | kills | A | B | C | intake %maxHP | leech healed |
|---|---|---|---|---|---|---|---|---|---|---|
| trash | none | 0.0000 | player | 4.30 | 8/8 | 4.000 | 1.000 | 2.000 | 53.61 | 0.0 |
| champion | none | 0.0000 | player | 4.40 | 4/4 | 2.000 | 1.000 | 2.000 | 36.99 | 0.0 |
| mixed_pack | none | 0.0000 | player | 10.30 | 6/6 | 1.500 | 1.333 | 3.000 | 75.41 | 0.0 |
| boss | A | 0.0500 | player | 27.30 | 3/3 | 1.000 | 1.000 | 3.000 | 146.03 | 721.4 |
| boss | B | 0.0800 | player | 27.30 | 3/3 | 1.000 | 1.000 | 3.000 | 146.03 | 999.1 |

**INS-1 non-vacuous:** trash + champion bit-identical under a door value of 0.0800, with 86.9 / 91.1
HP of heal ignored — the player took real damage, had real headroom, and the fight did not move.

**Read nothing into these numbers.** One seed, no sweep, boss damage at the HALT-1 default. (The
arms' leech totals differ 1 : 1.385 rather than 1 : 1.6 because the headroom clamp binds — an
observation about the clamp, not a finding about Battle Surge.)

---

## 9. Validation

| check | result |
|---|---|
| New suite `tests/test_kitcal_g5_harness.py` | **18/18** (non-vacuity by injection) |
| Door suites (BQ-3 + O-d) | **76/76**; pre-registered digest `25c212eb…` **unmoved** |
| KF-4 kit-compiler smoke | **36 GREEN / 0 RED / 1 GAP** — baseline unchanged |
| Full regression vs same-tree `git stash` baseline | **5,321 → 5,339** passed (**+18 = exactly the new tests**), 60 failed / 21 errors both sides, **failure NAMES diff-empty** |
| Byte-neutrality of both engine edits | proved A/B on a real fight |

**BQ-3's own containment fired on me and I did not weaken it:** T-8 (L5 static sweep) failed when
the harness landed — its failure message prescribes a deliberate allow-list entry, so exactly one
was added (`kitcal_g5_harness.py`; the L4 production-boundary asserts untouched). T-8c failed on my
key literal; fixed by importing `CALIBRATION_OVERRIDE_KEY`. Both tests were right.

**Output hygiene:** harness artifacts go to `src/reincarnated/simulation/output/kitcal_g5/` —
gamora's own output dir, never star-lord's.

⚠ **But I have to correct myself on the flagged file.** I first wrote here that
`src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json` was untouched; **that was
wrong and I checked it rather than asserting it.** My full-regression run rewrote it again (mtime
21:10), exactly as §14.20 recorded happening last session — deselecting `test_w3_emission_driver.py`
was **not sufficient**; some other test in the suite writes that path. A second stray also appeared
at the repo root during the same run: a 9-byte file literally named `54000`.

**Neither is committed. Both are left in the working tree, deliberately**, on the same reasoning as
§14.20: the conductor does not commit into another's seam, and neither do I. Both go to star-lord
via KR at wind-down, with the added information that **the writer is NOT `test_w3_emission_driver`**
— that is a new fact for him, and it means the previous session's deselect-based mitigation does not
hold. Anyone running the full engine regression is currently rewriting a file in star-lord's seam
without being told.

---

## 10. The invocation the conductor fires

Gated on Gate-2 PASS + the conductor's go:

```
cd ~/Games/reincarnated-engine
python3 -m reincarnated.simulation.spatial_gauntlet.kitcal_g5_harness --run --seeds 30
```

Defaults: seed base `74_000_800`, W-c pool 759, boss damage 50.0 (HALT-1 mid), trace ON, jitter OFF.
Artifact → `src/reincarnated/simulation/output/kitcal_g5/g5/kitcal_g5_g5_report.json`; traces →
`.../g5/traces/`.

The three variants the conductor will most likely also want, and they are one flag each:

```
--boss-dmg 33   /  --boss-dmg 67      # HALT-1 sweep ends (the boss verdict is read ACROSS these)
--r3-arm                              # R3 comparison arm: pool 1607 + poison DoT (S-2 / S-3)
--arm-a-jitter                        # Arm A drawn from the measured 3.25-6.75% band (D-1)
--no-trace                            # the R-KC1-19 §4 fallback; changes no metric
```

---

## 11. Open to the conductor

1. **The received-side-mirror finding** — my recommendation: route it to knight-rider for drax
   (REPLICA-1 / Godot lane), not into KIT-CAL-1's ledger. It is not G-5's defect and fixing it here
   is already done; what remains is *re-reading* anything downstream that consumed frame-file intake.
2. **HALT-1's sweep is not free** — three boss-damage settings × 30 seeds × 2 arms is 180 boss
   fights (~27 s each in the smoke). If the conductor wants the sweep inside G-5's window rather
   than after it, say so and I will report wall-clock before firing.
3. **Battle Surge's absence is quantified but the arms are the only instrument for it.** The A/B
   flip rule remains exactly as ratified; nothing in assembly touched it.
4. **The `leg3_pilot…json` flag has a new fact attached** (§9): deselecting `test_w3_emission_driver`
   does not stop the rewrite — a different test in the suite writes into star-lord's seam. Worth
   carrying into the KR hand-off rather than re-flagging the same file each session.

**Signed:** gamora, 2026-07-28. Assembly only. G-5 has not been executed.
