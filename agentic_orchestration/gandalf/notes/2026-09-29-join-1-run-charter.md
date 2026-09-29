# JOIN-1 RUN — charter v0.1 (DRAFT, NOT LAUNCHED)

> **STATUS:** v0.1 DRAFT, 2026-09-29, gandalf (`ARCHITECT` → prospective `RUN-CONDUCTOR`). **NOT LAUNCHED.** Awaiting (1) jack-ryan Gate-1, (2) the REFERENT-v1 seal (precondition J-P1), (3) Matt's launch sheet (§ 6) and launch word. Authorized as paper-only prep by Matt at seal-lap **L3** (KC2-PLAY ledger KP-84).
> **Course of record:** `2026-09-28-join-key-architect-pass.md` **§ 8 governs** (Q85–Q89 + E-1, KP-83). **Canon:** `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` (three layers · fidelity-grade LAW § 4 · E-1 RULED · E-2 open).
> **P0 input (landed):** elrond `elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` (`78797db4b`; KP-85). **Predecessor:** Run KC2-PLAY (closes at the REFERENT-v1 seal, Q89).

---

## § 0 — Intent (whose words, what outcome)

**Matt, 2026-09-28:** *"finish making this as a join key to being in other kits from other ARPGs by first testing out its viability as an arena replica and then tweaking the replica until it sits in between our games and contains what is needed to join the other kits in."* · R-J1: *"Between grim dawn and the other games.. then we leave levers open specifically to be tweaked as we go to reach our own version of fun."* · Q86: *"Is there any reason not to simply add all of the mechanisms into the game? … we will run everything through the battle sim and tune the kits to the game's balance thresholds."*

**Terminal artifact:** the EoR arena running **three configurations of one runtime**: `ORACLE` (graded; unchanged), `PLAY` (Matt's; unchanged), and **`JOIN`**. `JOIN` hosts kits from other games: their kit-internal mechanisms enter **natively**; the kit↔world boundary is adjudicated by **ONE rulebook** (Grim Dawn's rules as default, widened only by **lever**). **D2 Whirlwind Barbarian** is playable in it beside the Warlord, and the **golden master** (REFERENT-v1 replayed through the rulebook) stays byte-green throughout. The run **ENDS at the handoff**; Matt plays the joined kit after it, as a HITL session.

## § 1 — Bounded substrate (frozen at launch)

| # | Substrate | Pin |
|---|---|---|
| J-S1 | **REFERENT-v1**: the sealed pack (baton v3.4.2 model `5cab7433…` / reference `978f54ab…`), runtime digest, register hash, T-A grade, Matt's T-C word | the seal record (KC2-PLAY close) |
| J-S2 | The **P0 census**: 49 mechanisms · 15 INTERNAL / 25 BOUNDARY (8 AS-IS · 14 WIDEN · 3 GD-EMPTY) / 5 OUT-OF-ARENA / 1 HELD · **16 candidate levers, all OPEN** · the boundary list extended by target multiplicity, movement↔engagement coupling and the damage-family registry (KP-85) | `78797db4b` |
| J-S3 | **The kit** `d2-ww-barb`: `Skills.txt` rows 151 + 149 (D2 1.13 classic, `fabd/diablo2 @ 45112569…`, DATAMINED) + the D2 formula set (MODEL-VERIFIED) + `kits-export/d2-ww-barb.json` | derived at launch |
| J-S4 | The corpus EoR kit `kits-export/gd-eor-warlord.json` (APPROX) + the kit compiler (`simulation/kit_compiler/`) | derived at launch |
| J-S5 | The seal lap's instruments: U-P-N-3/4 bodies-in-disc census, the heal-ratio probe, the T-A harness | commits of record |

**Named out-of-scope, pre-declared:** the house profile (our own fun; Phase C) · any lever moved off its GD setting without a ruling · era profiles (E-2 beyond GD's own checklist) · PoE lanes beyond paper · the four OUT-OF-ARENA rows · allies and party scope (dockets 2/12, ruled) · loot and progression.

## § 2 — The central design

1. **Union + one boundary rulebook** (Q86). A foreign kit's resources, skills, leech, accumulators and procs are **INTERNAL**: ported natively with their home data at their lane's grade. Hit resolution, damage-family vs resistance, mitigation order, CC/status on monsters, the tick clock, target multiplicity, movement↔engagement coupling and the damage-family registry are **BOUNDARY**: one rulebook adjudicates them for every kit.
2. **The rulebook starts as Grim Dawn's, extracted.** Today it is welded to one character's operands (P0 finding 5: `RESIST_PCT`, the offense band and the armour table are REFERENT-v1's). **J2 separates FORM from OPERAND** so a second kit can bring its own operands through the same equations.
3. **Levers.** Every WIDEN row becomes a lever: `id · primitive · GD setting (default) · per-game settings + grades · range · load class · status OPEN`. GD-EMPTY rows are **build items**, not levers, and each gets a declared default that is inert for the GD profile.
4. **Golden master (the line in the sand).** The GD-REFERENT profile, run through the rulebook, must reproduce REFERENT-v1 on **every EXACT row of prereg v1.6**, on every commit that touches the join path. **A lever change that breaks the replay is a regression, not a design choice.**
5. **The ablation map (the bridge, § 4.4 of the ARCHITECT pass).** Before any lever moves, each mechanism is switched off alone under the scripted pilot, and the move in the feel metrics is recorded: HP occupancy, energy excursion + ceiling duty, wave durations, frac-moving, terminal wave, heal:intake, bodies-in-disc. That classes every mechanism **LOAD-BEARING / INCIDENTAL** and yields **GD's E-2 signature-feel checklist by measurement.**
6. **E-1 (ruled): tune toward our balance thresholds; home margin measured and recorded.** A joined kit's **home-game margin** (its power against its own frontier) and its **arena margin** are both measured; the distance between them is its **fidelity cost**, recorded and never hidden.

## § 3 — Fit test

- **F1 Enumerable? YES:** J-S1..S5; 49 mechanisms, 16 levers, one kit.
- **F2 Decidable? YES,** except the feel verdict, which is converted to the post-run HITL boundary.
- **F3 Pre-drainable? PARTLY.** Five forks are drained on the launch sheet (§ 6). The residual forks are lever *forms* (reasoning-boundaries), not their settings.
- **F4 Authority-resident? YES** for the rulebook, levers and golden master (the conductor authored the ARCHITECT pass). ⚠ `SPEC-AUTHOR → DRIFT-CRITIC` at every fold against it; jack-ryan Gate-2 is the independent check.

## § 4 — Decidable target-state (DONE when every row evaluates, without Matt)

1. **Ablation map filed:** every INTERNAL/BOUNDARY mechanism of the Warlord classed LOAD-BEARING / INCIDENTAL with its measured deltas; GD's E-2 checklist derived from it.
2. **Self-join (B0) graded:** `gd-eor-warlord.json` → kit compiler → the arena, compared against REFERENT-v1. **Every lost quantity is listed as a named schema gap** (the self-join is the evidence the GD-SLICE lock never had).
3. **Rulebook v0:** boundary rules extracted into a named module in the oracle and in the port; FORM separated from OPERAND; **golden master GREEN** on all EXACT rows.
4. **Lever registry v0:** 14 settable levers + 2 build items registered, every one OPEN at GD's setting, each with a negative control proving the lever is live (flipping it off-default moves the relevant metric; flipping it back restores the golden master byte-for-byte).
5. **Kit #2 joined:** D2 WW Barb in `JOIN` with **every mechanism mapped INTERNAL / BOUNDARY / OUT-OF-ARENA, zero unmapped** (a coverage gate on the kit's own census); its D2-side levers set to D2's values **for that kit only**; home margin and arena margin both recorded. It is playable in the desktop build beside the Warlord.
6. **Handoff packet:** build + how-to-play for the Barbarian + the lever registry + the ablation map + the fidelity-cost table + findings. jack-ryan Gate-2 on the whole.

## § 5 — Waves (seams execute; the conductor writes no production code)

| Wave | Seat | Piece | Gate |
|---|---|---|---|
| **J0** | gamora (oracle) · drax (port) | **Ablation map** under `ORACLE` + scripted pilot; print-only, never a T-A artifact | § 4.1 |
| J0 | elrond | **Docket-disposition sweep** (P0 misfit d) + GD-SLICE **freeze-not-drop**, with `boundary_class` / `vocab_scope` / `mechanism_grade` / `magnitude_grade` proposed (schema change ⇒ launch-sheet **J-L4**) · the 675 MEASURED→DATAMINED re-grade routed to jack-ryan | findings + MIGRATION |
| **J1** | elrond + gamora | **Self-join (B0)** | § 4.2 |
| **J2** | gamora (oracle) → star-lord (pack rows for the rulebook's law + operands) → drax (port) | **Rulebook v0**, FORM/OPERAND split; golden master | § 4.3; jack-ryan Gate-2 |
| **J3** | drax + gamora | **Levers v0** — first `crit_model` (three witnesses; GD `pth-tiered` default), then the D2-needed six (`tick_quantisation`, `packets_per_tick`, `max_hp_change_policy`, `pth_floor_pct` / `pth_ceiling_pct`, `proportional_damage_offense` / `_mitigable`) | § 4.4 |
| **J4** | legolas (D2 formulas + primary rows) → gamora (adapter / conversion key) → star-lord (kit rows) → drax (build) | **D2 WW Barb joined** + home/arena margins | § 4.5 |
| **J5** | conductor · jack-ryan | handoff packet · Gate-2 | § 4.6 |

## § 6 — Matt interface (LAUNCH SHEET — one word each; one recommendation each)

| # | Fork | Recommendation |
|---|---|---|
| **J-L1** | **Ruling-vs-ruling conflict:** Q86 "add everything natively" vs docket **5** `permanent-gap-record` for **life-cost casting** | **Q86 supersedes; docket 5 is re-dispositioned SUPERSEDED-BY-Q86** (life-cost casting becomes INTERNAL, entering natively when a kit that uses it joins). Record the supersession; never silently delete |
| **J-L2** | Does kit #3 (non-physical, conductor ruling KP-85) ride in JOIN-1, or open JOIN-2? | **JOIN-2.** Keep JOIN-1 to one foreign kit so its target-state stays decidable. Candidate for JOIN-2: **D2 Fire Sorceress** (294 DATAMINED numeric rows already banked; the same D2 adapter; exercises the damage-family registry) |
| **J-L3** | "Our balance thresholds" (E-1): tune kit #2 in JOIN-1, or record only? | **Record only in JOIN-1.** Measure home margin + arena margin and file the fidelity cost; **tuning waits until the thresholds are pinned as numbers** (an ELICITOR sitting on doc 50's bounded-viability band). Tuning against an unpinned target is a fitted constant with extra steps |
| **J-L4** | Cross-seam schema change: freeze GD-SLICE `is_core`, add `boundary_class` / `vocab_scope` / `mechanism_grade` / `magnitude_grade` to `corpus.db` (ADR-002: a cross-seam schema change is Matt's) | **Approve**, as additive columns with nothing dropped (the le-park / `source_urls` precedent) |
| **J-L5** | Push posture | **Push-as-work-lands on collaboration + engine + godot** for the run (as KC2-PLAY L1); loadout/demo untouched |

**HALT-to-Matt boundaries:** golden master RED that the conductor cannot attribute to a named defect · jack-ryan BLOCK · committed-truth conflict · free disk < 40 GiB by `df -h` (unit stated, per KP-91) · any lever moved off GD's setting outside kit #2's own profile · a write outside a seat's named tree · two failed attempts at one gate by one seat.

## § 7 — Standing laws carried in

KC2 lineage (K-7 · Law 3 · D4 prereg-alone · digests derived, never retyped, **and labelled FILE vs ROWSET**, KP-101 · corrigenda-forward · § 4.11 value-set sweep) · **the Commission Rule** · `--only` commits with explicit FILE lists · `git status --porcelain` pre / `git show --stat HEAD` post · the heavy lock · captures encoded straight to video · **derive, don't relay** (KP-65, KP-86, KP-95, KP-100: four relay defects in two laps, three of them the conductor's).

## § 8 — Open-questions gate (ARCHITECT)

| Question | State |
|---|---|
| Where the middle sits; union + one rulebook; E-1 target | **RESOLVED** (R-J1, Q86, E-1; KP-82/83) |
| J-L1 … J-L5 | **OPEN — Matt** (launch sheet) |
| **J-P1: REFERENT-v1 sealed** | **GATED:** T-A under prereg v1.6 + Q83(b) + Matt's T-C yes |
| C-11: the oracle's ~×1.9 over-lethality (deaths at 151–156 vs 160) | **GATED+TRACKED:** issued if Matt's T-C says "too deadly", else at JOIN-1 J0 |
| `ABS-C-I14-2-SOURCED-UNFOLDED` (≤ 2.2 %) | **GATED+TRACKED:** folded at the next forward revision of the reference |
| Lever *settings* for the house profile | **Out of scope** (Phase C; R-J1 "as we go") |

---

**Signed:** gandalf (`ARCHITECT`), 2026-09-29. *The replica earned the right to be moved by being proved first; JOIN-1 earns the right to tune by measuring first.*
