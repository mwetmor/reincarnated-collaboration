# Proxy-Commander Set #6 — Capstone Design Spec — 2026-06-16

> **STATUS:** CURRENT (load-bearing as of 2026-06-16) — see `canonical/00-ground-state.md` § 1. The complete, buildable design-spec-as-math for the **Proxy-Commander flagship set (#6)** — the capstone of the six-profile Set-Gear architecture. Where the proxy-add spec supplies the **skills / gear / selector** and the six-profile doc supplies the **set's shape**, this doc CLOSES the set's open design-math: the 2pc/4pc formula intent + bounds, the definition of the inherited "offensive profile," the set-vs-test circularity resolution, the band-parity reconciliation, and the command-amplification mastery layer. Visual realization proceeds by **deferral-by-reference** to the gear-spec-generation recognition record.

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Status:** v1 — design-spec-as-math hand-off. Authored from the Pattern-B equipment session with Matt 2026-06-16, immediately after the gear-spec-generation deferral was committed. The capstone of the six-set arc — the sixth, most mechanically novel set, given the complete treatment because it is the one Matt insisted ships (*"I will not skip proxy"*).
**Authority:** Matt 2026-06-16 directed the #6 capstone spec as the next deliverable after the gear-spec deferral. This doc authors design intent (form, bounds, acceptance); **gamora** calibrates the magnitudes (the empirical layer); **rocket** materializes the set in `set_generator`; **star-lord** names/flavors; **drax** renders; **jack-ryan** gates. gandalf reviews. knight-rider sequences.
**Companion docs:**
- `canonical/story/proxy-add-design-spec-2026-06-16.md` — the SKILLS (§ 4) + GEAR MODIFIERS (§ 5) + SELECTOR (§ 8) + budget math (§ 7) this set sits atop. **This capstone spec does NOT re-specify those; it completes the SET.**
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 4 (2pc/4pc structure), § 5 (#6 shape row), § 6 (element-flavor), § 7 (aura apex), § 9 (6b instrument / T4-scope anchor) — the set's SHAPE this doc realizes.
- `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` — kits are measured at a 4-piece set; the **6b reference set is the measurement instrument** (§ 6 closure here routes the selector through it).
- `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — the visual layer (aura / element-flavor / construct echo) proceeds by deferral-by-reference to this record (§ 8 here).
- `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` — the Berserker's dodge layer; the structural PARALLEL to the Proxy-Commander's command layer (§ 4.3 here): each profile's mastery lives off the sim's parity books.
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 4 (85th-pct endgame band) / `canonical/46-concentration-architecture-2026-05-27.md` Layer 3 + D66.

---

## 0. TL;DR — what this doc CLOSES (it does not re-emit)

The Proxy-Commander set's **shape** is locked (six-profile § 5: 2pc accelerates the proxy chain-T4; 4pc = count/power/duration + "proxies inherit a share of your offensive profile"). The **skills / gear / selector** are locked (proxy-add spec). What was OPEN — and is closed here — is the set's buildable design-math:

| # | Open question | Closure (this doc) |
|---|---|---|
| **A** | What axis does the 2pc "accelerate"? | **§ 3** — proxy chain-T4 activation FRICTION (cadence/cooldown), not raw power. |
| **B** | The 4pc's two clauses — formula intent + bounds? | **§ 4** — Clause A (count/power/duration, parity-bounded); Clause B (offense-inheritance global). |
| **C** | What "offensive profile" do proxies inherit? | **§ 4.2** — the same scalar that scales the player's DIRECT output; share `s < 1`. |
| **D** | The command-amplification mastery layer? | **§ 4.3** — the 4pc rewards COMMANDING; live-only, OFF the sim's parity books (Berserker-dodge parallel). |
| **E** | Set-vs-test circularity? | **§ 6** — the `proxy_primary` flag is measured at the **6b reference set**, NOT the kit's own set. Set = confirmer+amplifier of innate dominance, not bootstrapper. |
| **F** | Band-parity reconciliation? | **§ 5** — the 4pc is IN the measured band (measurement contract), NOT excess on top. The set-complete kit lands AT band; sub-set lands BELOW (the climb). |

Visual realization (aura apex / element-flavor / construct echo) = **deferral-by-reference** to the gear-spec-generation record (§ 8). Scarcity discipline (proxies are generic constructs, NEVER Hall forms) holds at every clause.

---

## 1. Position — the capstone of the six-set arc

This is the sixth and final flagship set, and the only one given a full standalone spec (the other five rest on their six-profile § 5 shapes + gamora calibration, sufficient because they are less mechanically novel). It is the capstone for two reasons:

- **Most novel mechanics:** distributed output, designed attrition, the scaling-link genre-fix, and a command mastery layer — none of the other five sets carry all four.
- **The one Matt insisted ships:** *"I will not skip proxy."* Giving it the complete treatment is the proof that the six-set architecture is buildable end-to-end, not just shaped.

It composes with three already-committed docs and adds nothing they already say: the **proxy-add spec** (the kit-side surface — skills, gear, selector), the **six-profile doc** (the set's shape + the T4-scope-coexistence discipline), and the **measurement contract** (kits measured at 4-piece set; the 6b instrument). It defers its visual layer to the **gear-spec-generation record**.

---

## 2. The set at a glance

| Piece | Effect class | Scope | Magnitude |
|---|---|---|---|
| **2pc** | Accelerate the kit's chosen proxy chain-T4 — reduce its activation FRICTION (cadence/cooldown), the command-tempo entry nudge (§ 3) | chain-local | minor; Layer-1-capped where it touches bounded stats |
| **4pc — Clause A** | Proxies gain count / power / duration (§ 4.1) | proxy-scope global | T4-scope; parity-bounded (§ 5) |
| **4pc — Clause B** | Proxies inherit a share `s` of the player's offensive profile — the scaling-link goes GLOBAL (§ 4.2) | character-wide global | T4-scope at the anchor; `s < 1` |
| **4pc — command layer** | Inheritance is AMPLIFIED by recent command actions — live-only, off the sim's parity books (§ 4.3) | piloting headroom | NOT counted in band parity |
| **Aura apex** | Set-complete "commander's authority" glow, element-tinted, faint construct echo — deferral-by-reference to the gear-spec record (§ 8) | visual | deferred |

The 4pc is a **T4-SCOPE gear capstone that COEXISTS with the proxy chain-T4** (six-profile § 4.2; D66 held — the proxy chain-T4 is still one-at-a-time, the set capstone is a separate gear-scope). The 4-piece commitment is what EARNS the T4-scope (Layer 3).

---

## 3. The 2pc — proxy chain-T4 activation-friction accelerate (closes A)

The six-profile § 4.1 entry bonus is "accelerate the kit's OWN chosen chain-T4." For the Proxy-Commander, the chosen chain-T4 is a **proxy chain-T4 capstone** (the Q1–Q10 T4 work, with proxy added to T4 capstones 2026-06-16). "Accelerate" must be specified, because for a proxy build there are two very different things it could mean:

- **WRONG: raw proxy power** (more count/stronger constructs). That is the 4pc's job. Putting power in the 2pc re-creates the D3 "10000%-more-to-your-one-skill" set criticism (six-profile § 4.1) and front-loads the payoff.
- **RIGHT: activation friction.** The 2pc reduces the proxy chain-T4's **command-tempo friction** — its cooldown / ramp, and/or `proxy_spawn_cadence_s` for the chain-T4's summon. The chosen proxy capstone comes online faster and more often. This deepens the build the player already chose (the entry nudge) WITHOUT adding raw output.

**Formula intent (gamora calibrates magnitude):**
```
2pc:  proxy_chain_T4_cooldown  ×= (1 − c_2pc)        # c_2pc small, e.g. a modest % reduction
      (and/or)  proxy_spawn_cadence_s ×= (1 − c_2pc) for the chain-T4 summon
```
Bounded by Layer-1 caps where it touches a bounded stat. **Design rationale:** the 2pc is "command your chosen capstone more fluidly," the 4pc is "the profile-defining payoff." Keeping power out of the 2pc is what makes the 4-piece the meaningful commitment.

---

## 4. The 4pc — the profile-defining T4-scope capstone (closes B, C, D)

The 4pc has two mechanical clauses (six-profile § 5) plus one mastery layer (this doc's contribution).

### 4.1 Clause A — count / power / duration gain (parity-bounded)

The raw proxy-stat boost: proxies gain count, per-unit power, and duration.

**Formula intent:**
```
4pc Clause A:  proxy_count        +=  Δcount        (small int, ≤ proxy_max_active headroom)
               proxy_power_per    ×=  (1 + g_power)
               proxy_duration_s   ×=  (1 + g_dur)
```
**Bound (the load-bearing constraint — see § 5):** Δcount / g_power / g_dur are NOT free. They are calibrated so the **set-complete** kit lands at the parity band (doc 40 § 4), because the measurement contract measures kits AT a 4-piece set. Clause A is the bulk of "the set is the assumed-endgame power," not excess on top of it. `proxy_max_active` (proxy-add § 4.1) remains the hard wall against the D2-dominance failure even with the count boost.

### 4.2 Clause B — offense-inheritance global; define "offensive profile" (closes C)

This is the **scaling-link genre-fix** (proxy-add § 5.2) gone global — the *reason the set exists*. Proxy-add § 5.2 gives the form but leaves "offensive profile" undefined. Define it:

> **"The player's offensive profile" = the same effective scalar that scales the player's DIRECT output `O_direct`** — concretely, the player's effective weapon+skill damage stat (the quantity gear and node investment improve). NOT a separate `+minion damage` silo (that silo IS the PoE disconnection complaint, proxy-add § 2).

**Formula intent** (the global form of proxy-add § 5.2's `proxy_power_per = proxy_base_power + k_link × player_offensive_profile`):
```
4pc Clause B:  proxy_power_per  +=  s × player_offense_scalar
   where  player_offense_scalar = the scalar driving O_direct (weapon+skill effective damage)
          s = the inherited SHARE,  0 < s < 1   (gamora-calibrated at the T4-scope anchor)
```
**The share-bound `s < 1` is non-negotiable design:** the player's direct output must still matter — the army is an *extension* of your offense, not a clone-multiplier of it. If `s → 1` the player becomes irrelevant to their own damage (a worse version of the screensaver failure). `s` is calibrated so the inheritance is a **T4-magnitude payoff** (a meaningful jump felt as "my gear now arms my army") while keeping `O_proxy` in-band (§ 5).

**Player consequence (the emotional close):** gearing yourself gears your army. *"My constructs are extensions of me"* (proxy-add § 3) is this formula made felt — the PoE disconnection complaint dissolved by construction.

### 4.3 The command-amplification mastery layer (closes D — this doc's headline contribution)

The set is the **Commander's** set. It must reward COMMANDING, not make the army more autonomous — otherwise it fights the anti-screensaver discipline (proxy-add § 4.3) by rewarding passivity. The design move:

> **The offense-inheritance share `s` is AMPLIFIED for a window by recent command actions** (the target/redirect, sacrifice/detonate, rally/regroup verbs of proxy-add § 4.3). A freshly-commanded army inherits MORE; a neglected army inherits the baseline `s`.

**Formula intent:**
```
effective_s(t)  =  s_baseline  +  s_command × decay(t − t_last_command)
   s_command = the command-amplified bonus share (live-game-only)
   decay() = a short falloff window; lapses back to s_baseline if you stop commanding
```

**The critical discipline — this layer is OFF the sim's parity books.** The 2D spatial sim treats command verbs as no-ops (it cannot model piloting — the same treatment as the dodge layer). So **the sim measures inheritance at `s_baseline` only**; the parity band (§ 5) is calibrated at `s_baseline`. The command-amplification is **pure piloted upside** — it cannot inflate the sim-measured contribution (§ 6), and it cannot break band parity. It is the Proxy-Commander's *"mastery shows"* layer.

**The structural parallel (a design-coherence close):** this is exactly the Berserker's dodge layer (telegraph-dodge doc) in a different costume. Each skill-expression profile has its mastery in the **piloted layer, off the sim's parity books** — the Berserker's survivability lives in dodge, the Proxy-Commander's damage-ceiling lives in command. The autobattle/sim measures the floor; piloting is the ceiling; mastery shows. Two profiles, one discipline. This is *why* the command layer belongs in the set and not in the raw stats: it is the set's invitation to pilot.

---

## 5. Band-parity reconciliation — the 4pc is IN the band, not on top (closes F)

A reader could think "a T4-scope 4pc payoff" means the set pushes the kit ABOVE the balanced envelope. It does not — and the measurement contract is why:

- The canonical measured loadout includes **a 4-piece set** (measurement contract; the 6b reference set at the T4-scope anchor). So the **parity band (85th-pct endgame, doc 40 § 4) is the band AT 4-piece set.**
- Therefore the 4pc (Clauses A + B at `s_baseline`) is **part of the loadout the band is calibrated around**, NOT excess on top of a setless baseline. The set-complete Proxy-Commander lands **AT band** — differently-shaped (Axis-2A proxy-heavy, proxy-add § 3), comparable total efficacy.
- A kit at 2pc-only or bare lands **BELOW band** — that gap is the progression gradient (the climb toward your set). The "T4-scope payoff" is the jump **from sub-set TO set-complete, landing at band** — never above it.

This is the D3 **"the set IS the build"** model (Helltooth/Inna's/Mundunugu, proxy-add § 2): the set-complete state is the assumed-endgame power level, the band is drawn there, and chasing the set is the endgame. The 4pc *feels* like a big jump (because it is, relative to sub-set) while being perfectly in-band (because the band is drawn at set-complete). gamora calibrates Clause A + B `s_baseline` to hit this parity exactly.

---

## 6. Set-vs-test circularity resolution — measure the flag at the 6b instrument (closes E)

A genuine hazard: the `proxy_primary` test (proxy-add § 8) flags proxy-dominant casters by measuring `proxy_contribution_pct ≈ 0.5`, and the flagged kits GET the Proxy-Commander set — which boosts proxies (§ 4). If the test measured the kit **wearing its own Proxy-Commander set**, the set would inflate contribution and push borderline kits over threshold — **the set defining its own membership.** That is circular and dishonest.

**The resolution (composing with the measurement contract):**

> **The `proxy_primary` flag is measured at the canonical measured loadout — which is the 6b REFERENCE set (the element/profile-agnostic measurement INSTRUMENT), NOT the kit's own Proxy-Commander set.** A kit is flagged proxy-dominant only if its proxies do ≥ ~0.5 of the work at the *neutral* instrument. The Proxy-Commander set is then the **reward for innate proxy-dominance — a confirmer and amplifier, not a bootstrapper.**

This keeps the selector honest (it measures *innate* dominance, on the skills + nodes + neutral gear) and it composes cleanly with the measurement contract (all kits measured at the 6b instrument). When the shipped Proxy-Commander set later swaps in for the 6b reference (six-profile § 9, magnitudes coincide at the T4-scope anchor), it reinforces a dominance the kit ALREADY had — it does not manufacture it.

**This is also why the command-amplification (§ 4.3) must be off the sim's books:** if `s_command` counted in the sim, a borderline kit could be pushed over the `proxy_primary` threshold by a piloting layer the sim cannot even model. Measuring contribution at `s_baseline` on the neutral 6b instrument is the doubly-honest selector. **Genre note:** D3's pet sets were *enablers* (the set made pet builds top-tier); ours is deliberately a *confirmer* of innate dominance — the more honest model for a substrate-led, sim-flagged architecture, and it keeps the set from manufacturing its own profile.

---

## 7. The proxy budget math WITH the set (extends proxy-add § 7)

Proxy-add § 7 gives the setless budget. The set adds two terms; the parity target is unchanged (`O_proxy` in the 85th-pct band, § 5):

```
O_proxy(set-complete)  =  O_direct  +  O_proxies(set)

O_proxies(set)  =  N_active(set) × proxy_power_per(set) × uptime_factor

   N_active(set)      ≈  spawn_rate(2pc-accelerated) / death_rate ,  capped at proxy_max_active
                          # 2pc lowers cadence → higher spawn_rate; cap still walls D2-dominance
   proxy_power_per(set) =  proxy_base_power
                          +  s_baseline × player_offense_scalar     # 4pc Clause B (sim-measured share)
                          ,  then × (1 + g_power)                   # 4pc Clause A
```

- **Clauses A + B at `s_baseline` are calibrated to land `O_proxy(set-complete)` AT band** (§ 5). gamora solves for Δcount / g_power / g_dur / `s_baseline` jointly at the T4-scope anchor.
- **The command layer (`s_command`, § 4.3) is NOT in this equation** — it is live-only headroom, off the parity books.
- **Beast Taming** (proxy-add § 4.5) does NOT wear this set (it is expected sub-threshold and keeps its physical-ranged profile); its capture-acquisition budget stays in proxy-add § 7. The Proxy-Commander set is for caster kits the test flags proxy-dominant.
- **Discipline #18 timing (OP § 4.2):** the 4pc magnitude calibration is a math-hotspot EXTENSION — it fires AFTER the proxy CONTRIBUTION measure (proxy-add § 8 step 2) lands, since the parity target is expressed in contribution terms. Consultation-in-the-dark on the 4pc magnitude before the contribution baseline exists is the failure mode to avoid.

---

## 8. The visual layer — deferral-by-reference (composes with the gear-spec record)

Per the gear-spec-generation deferred-architecture record (committed 2026-06-16), the StyleProfile realization is held behind the Synty-slice gate. So this set's visual clauses are specified as INTENT and point at that seam — mechanical-complete now, visual-deferred-by-reference:

- **Aura apex** (six-profile § 7): set-complete lights the "commander's authority" glow — element-tinted via the StyleProfile `emission_*` fields. **Deferred** to the gear-spec record's L2 restyle leaf.
- **Construct echo:** the aura MAY extend a faint tinted rim to the army (the constructs read as *yours*) — **but the scarcity discipline is absolute (proxy-add § 4.4): the echo must NEVER make a construct read as a Hall-of-Heroes form.** Generic constructs, tinted; never ascended past-selves. This is a watch-flag for drax at render time.
- **Element-flavor** (six-profile § 6): a fire-Proxy-Commander's constructs read as ember, a water's as frost — StyleProfile-layer, mechanically agnostic. **Deferred** to the gear-spec record.

No part of the set's MECHANICAL spec waits on the visual deferral. The set ships mechanically; it lights up visually when the gear-spec system resumes.

---

## 9. Acceptance criteria (set-specific)

### 9.1 rocket (generation)
- Author the Proxy-Commander set #6 in the `set_generator` six-profile pass: 2pc = proxy-chain-T4 friction-accelerate (§ 3); 4pc = Clause A (count/power/duration) + Clause B (offense-inheritance global, `s × player_offense_scalar`, § 4.1–4.2).
- The 4pc carries the ONLY T4-scope on this kit's gear (Layer 3); enforce no individual legendary claims character/chain-wide scope.
- Hold D66: the proxy chain-T4 stays one-at-a-time; the 4pc is a separate gear-scope that coexists.
- Hold the no-skill-modifier rule (proxy-add § 5.3): the set adds proxy-scope + offense-inheritance globals, NOT levels to the summon skill.
- Math-note before code (Discipline #1).

### 9.2 gamora (simulation — the magnitude owner)
- Calibrate Clause A (Δcount / g_power / g_dur) + Clause B (`s_baseline`) + the 2pc `c_2pc` jointly so `O_proxy(set-complete)` lands AT the 85th-pct band (§ 5, § 7) — neither D3-evaporate nor D2-dominance (proxy-add § 7).
- **Measure `proxy_primary` at the 6b reference set, NOT the Proxy-Commander set** (§ 6) — the circularity-avoidance discipline. The flag reflects innate dominance.
- **Measure contribution at `s_baseline` only** — the command layer (`s_command`) is off the parity books (§ 4.3); do not let a piloting layer the sim cannot model affect the flag or the band.
- Sequence per Discipline #18 refinement: 4pc magnitude calibration fires AFTER the proxy CONTRIBUTION measure lands (§ 7).
- Validate in the 2D spatial sim (the sole battle sim).

### 9.3 star-lord (telemetry + LLM)
- Phase-5 LLM names/flavors the set (D7 narrow-blank — e.g. "Bonelord's Regalia," "the Conclave set"); the mechanical capstone is human-authored (this doc). Construct names are the skill-composition runtime label (weapon-as-identity § 4).
- Set-complete state + 4pc contribution flow to telemetry.

### 9.4 drax (player-surface)
- Render the command-agency verbs (proxy-add § 4.3) prominently — the set's mastery layer (§ 4.3) is the build's tempo; the UI must make commanding legible and rewarding.
- Render the aura apex + construct echo (§ 8) WITHOUT Hall-form confusion — the scarcity watch-flag.

### 9.5 jack-ryan (gate) — decisions-log
- The set-specific design rulings here (2pc-as-friction-accelerate; the `s < 1` offense-inheritance definition; the command-amplification-off-parity-books; the 6b-instrument circularity resolution; the 4pc-in-band reconciliation) warrant a decisions-log entry — gandalf recommends; Matt approves; knight-rider drafts; jack-ryan reviews. Composes with the proxy-add decisions-log entry (the `Proxy-adjusting` capability + the `proxy_primary` gate).

---

## 10. Predictions registered (for empirical validation)

Per recognition→validate→commit:

1. **The set-complete Proxy-Commander lands AT the 85th-pct band, differently-shaped** (Axis-2A proxy-heavy), with Clause A + B at `s_baseline`. *Gate:* gamora spatial-sim calibration (§ 5, § 7).
2. **The 6b-instrument flag is stable** — measuring `proxy_primary` at the neutral 6b set vs the kit's own Proxy-Commander set changes which kits are flagged (the circularity is real and the resolution matters). *Gate:* gamora measures both and confirms the divergence (§ 6).
3. **The command layer reads as mastery, not requirement** — a well-piloted Proxy-Commander exceeds its sim-measured floor (command-amplified), but an un-piloted one is still in-band (the floor is viable). *Gate:* playtest + the sim floor at `s_baseline` (§ 4.3). The Berserker-dodge parallel predicts this holds.
4. **The scaling-link dissolves the PoE disconnection complaint** — players report their gear arming their army. *Gate:* playtest, post-pipeline (§ 4.2).

**Empirical gate (NOT time-passage):** predictions 1–2 resolve at gamora's calibration + dual-instrument measurement (after the contribution measure lands); 3–4 at playtest.

---

## 11. Composition with prior canon

- **Proxy-add design spec** — supplies skills/gear/selector/budget; this doc completes the SET atop them. The two are the full Proxy-Commander surface.
- **Six-profile Set-Gear architecture** — § 5 #6 shape realized here; the 2pc/4pc structure (§ 4) + T4-scope-coexistence (§ 4.2) + aura (§ 7) inherited; the 6b/T4-scope-anchor (§ 9) is the circularity + parity backbone.
- **Measurement contract** — kits measured at 4-piece set → the band IS at set-complete (§ 5); the 6b reference set is the flag instrument (§ 6).
- **Gear-spec-generation deferred record** — the visual layer proceeds by deferral-by-reference (§ 8).
- **Telegraph-dodge doc** — the Berserker dodge layer is the structural parallel to the command layer (§ 4.3); one discipline, two profiles.
- **Companion commitment** — scarcity discipline: constructs generic, never Hall forms (§ 8).
- **Doc 46 Layer 3 / D66** — the 4pc is a gear-scope T4 coexisting with the one-at-a-time proxy chain-T4 (§ 2, § 9.1).

---

## 12. Cross-references

- `canonical/story/proxy-add-design-spec-2026-06-16.md` — skills/gear/selector/budget (§ 4–9).
- `canonical/story/six-profile-set-architecture-2026-06-16.md` § 4 / § 5 / § 6 / § 7 / § 9.
- `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` — 4-piece-set measurement + 6b instrument.
- `canonical/story/gear-spec-generation-deferred-architecture-2026-06-16.md` — the deferred visual seam (§ 8).
- `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` — the dodge-layer parallel (§ 4.3).
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 4 (band) / `canonical/46-concentration-architecture-2026-05-27.md` Layer 3 + D66.
- Engine: `generation/skill_schema.py` (proxy fields, cd7cba3); `generation/set_generator` (six-profile pass — to author); `simulation/spatial_gauntlet/` (calibration + contribution measure).
- `canonical/00-ground-state.md` § 1 — this doc registers as a new CURRENT entry.

---

## 13. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — the complete buildable design-spec-as-math for the Proxy-Commander flagship set (#6), the capstone of the six-profile Set-Gear architecture. Closes the set's open math: 2pc = proxy-chain-T4 friction-accelerate (not power); 4pc = count/power/duration (parity-bounded) + offense-inheritance global (`s < 1`, "extensions of me") + a command-amplification mastery layer that lives OFF the sim's parity books (the Berserker-dodge parallel); the `proxy_primary` flag measured at the neutral 6b instrument (circularity resolved); the 4pc reconciled as IN-band, not excess (the D3 set-IS-the-build model). Visual layer deferred-by-reference to the gear-spec-generation record. Scarcity discipline absolute throughout.
**Composition:** with the proxy-add spec (the surface beneath it), the six-profile architecture (the shape it realizes), the measurement contract (the band + instrument), the gear-spec deferral (the visual seam), the telegraph-dodge doc (the mastery-layer parallel), and doc 46 / doc 40 (T4-scope + endgame band).
**For:** rocket (author the set), gamora (calibrate the magnitudes + the dual-instrument flag), star-lord (name/flavor + telemetry), drax (command UI + aura render), jack-ryan (gate + decisions-log); knight-rider sequences; gandalf reviews. The proxy ships first-class, complete to the set — *"I will not skip proxy."*

**Signed:** gandalf (story-and-design steward), 2026-06-16.
