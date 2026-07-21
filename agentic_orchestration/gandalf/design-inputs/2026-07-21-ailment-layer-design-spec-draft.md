# Ailment-Layer Design Spec — STEWARD'S DISPOSITION (not a redraft)

> **BANNER:** This was commissioned as *"DRAFT — prepared surface for the commissioned ailment
> design session; Matt session ratifies; not build-authorized."* **That surface already exists,
> was ratified, gated (Gate-1 + Gate-2 PASS-WITH-AMENDMENTS), BUILT, and PUSHED to engine remote
> (`cec8f12`) between 2026-07-13 and 2026-07-16.** Drafting a fresh fork-laden prepared-surface
> now would produce a duplicate artifact that re-opens ruled-and-built decisions and contradicts
> remote engine truth. **gandalf declines the regressive redraft** and instead files this
> disposition: what exists, where every commissioned fork already landed, and the one genuinely
> open residue. This is a survey-mode + pushback output per the steward mandate (serve the work,
> not the literal instruction).

**Date:** 2026-07-21 · **Author:** gandalf (SPEC-AUTHOR entry → DRIFT-CRITIC disposition)
**Trigger:** sub-agent brief to draft `2026-07-21-ailment-layer-design-spec-draft.md` from the
pause-2 (2026-07-12) commission. **Brief snapshot is 9 days stale** — the session it asks me to
prepare for concluded 2026-07-16.
**Authority:** pause-2 convening 2026-07-12 item 4 (commission) → executed under Matt autonomous-run
delegation 2026-07-16 (six delegated rulings recorded veto-open) → Gate-2 ratified.

---

## ▶ ROLE: SPEC-AUTHOR — then ⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC

I entered SPEC-AUTHOR to draft the commissioned surface. On reading engine ground truth I crossed
the conflict seam into DRIFT-CRITIC: **judging whether a build matches a spec — here, whether the
brief's requested artifact matches the shipped reality.** It does not. The correct steward move is
to name the drift, not manufacture a second spec that fights the first.

---

## §0 — TL;DR (the disposition in six lines)

1. The commissioned tranche — **damage-amp + freeze + stun + poison-dot, taunt-annex, GX-15 fold** —
   is **SHIPPED**: specced (`canonical/reap-die-rise-engine/ailment-layer-engine-spec.md`, 61 KB,
   STATUS **CURRENT**), gated twice, implemented (rocket config/emission + gamora sim), pushed
   (`cec8f12` — *"AILMENT LAYER IS REMOTE TRUTH"*).
2. **Every taste/commitment call the brief asks me to present as `[MATT-FORK]` is already RULED.**
   All 5 architectural escalations closed; 2 delegated name/register calls closed. Rulings stand
   **veto-open** — Matt may still overturn on read. §3 below is the fork→ruling crosswalk so nothing
   is silently buried.
3. The layer **over-delivered vs the tranche**: Wave-C (2026-07-17) added **blind / curse / fear /
   execute** — the registry is now **16 ailments**, not the 8 the brief's baseline assumes.
4. **DL-03 (streams never tax movement) is satisfied**, and the chill-as-movement-tax tension the
   brief flags was resolved cleanly — see §4. The reconciliation is *not* the one the brief
   anticipated (chill was never in the commissioned tranche; it pre-existed).
5. The whole **census cascade V8→V13 (45.4% → 99.47% expressible-now)** was *driven by* this layer
   landing. Re-opening it via a duplicate draft risks the highest-value delta the engine has posted.
6. **One genuine residue remains open** — the chill→freeze *escalation mechanism* (deferred at
   spec §3.4 / §9). If a design session fires, THAT is its agenda, not the shipped tranche. §5.

---

## §1 — What EXISTS (survey-mode; "what is," no "should")

Read-only survey, 2026-07-21, on engine remote-truth (`cec8f12` chain) + collab canon.

| Artifact | Path | State |
|---|---|---|
| Ailment-layer engine spec | `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` | STATUS **CURRENT**; Gate-1 PASS-WITH-AMENDMENTS (jack-ryan 2026-07-16); 8 amendments applied inline; 5 §10 escalations RULED |
| Evidence dossier (the prepared surface) | `agentic_orchestration/gandalf/design-inputs/ailment-layer-evidence-v1.md` | 46 KB; kit census + implementation-pattern tables + genre precedents; commit `460ecc65` |
| Sim-resolution math note | `~/Games/reincarnated-engine/src/reincarnated/simulation/math/ailment-layer-sim-resolution-2026-07-16.md` | authored 2026-07-16 |
| Ailment registry | `~/Games/reincarnated-engine/config/ailments.yaml` | **16 ailments** (8 original + 4 ailment-layer + 4 Wave-C) |
| Apply hook | `damage_resolver.py::_try_apply_ailment` (~:1593) | RNG gate `BASE_AILMENT_CHANCE=0.35 × (1−status_resist)`; sunder min-cap, GX-15 cap-after-add, stun hard-drop-before-rng, poison FIFO all landed |
| Tick loop + expiry hooks | `effect_resolver.py::tick_effects` (:55) | freeze-shatter between decrement (:59) and cull (:95); stun immunity-after-expiry stamp (:15-17, :158-163); sunder DoT-tick amp |
| E3 attribution spine | `effect_resolver.py:115-149` stamps `source_element` → `dot_taken_by_element` | **LIVE, byte-pure** — new DoTs inherit the stamp; poison rides it |
| Gate-2 verdict | collab `481f8fb2` / engine `cec8f12` | PASS-WITH-AMENDMENTS + delegated rulings #5–#8; 685/0 regression battery; decisions-log 5796–5844 |

**The tranche's four ailments, as-built:**

- **`sunder`** (damage-amp) — timed `damage_taken_percent` 0.10–0.50 (default 0.20, D4-Vulnerable
  analog); `max_amp_cap 0.50` **HARD LOCKED** (runaway guard); category **`debuff`** (reused reserved
  slot, no new category). GX-15 folds in as `synergy_bonus_percent` (+0.10 pp when target carries
  2+ non-sunder ailments; binary threshold-at-2, Hades Privileged-Status precedent).
- **`freeze`** — hard immobilization; **threshold-shatter** model (`shatter_threshold_fraction`
  0.25, `shatter_damage_percent` 0.20 of target max-HP, HARD guard 0.30 boss-one-shot invariant);
  duration 0.5–3.0s (default 1.5, deliberately shorter than root's 2.5 — freeze is more punishing).
- **`stun`** — brief full interrupt 0.3–1.5s (default 0.7); **hybrid DR** = universal
  `immunity_after_seconds` (default 2.0, HARD floor ≥1.0) + `stun_resistance_tier_boss` (bosses take
  75% nominal). Anti-stunlock discipline is structural, not incidental.
- **`poison`** — **independent-stack** (PoE1 Viper Strike / Caustic Arrow lineage);
  `stack_cap_per_attacker` 8 (HARD guard 10, memory/perf + viz); FIFO overflow eviction;
  `_add_poison_stack` special-case; source_element attribution via E3. Third pillar of the
  burn/bleed/poison DoT triad.
- **taunt** — annex; rides Wave A as `PROXY_TAUNT_PRIORITY` map (proxy-AI directive model), NOT a
  target-side ailment entry. Fear is EXCLUSIVE with taunt (Wave-C).

---

## §2 — Scope conformance to the brief (line-by-line)

| Brief required | Status |
|---|---|
| (1) damage-amp grammar (GX-15 fold; PoE exposure/wither, D3 debuffs, LE shred anchors) | **SHIPPED** as `sunder` + `synergy_bonus_percent`. Anchors cited in spec §2 + dossier ch.1. |
| (2) freeze (threshold vs duration; D2 cold-length lesson; chill→freeze gradient; ice/frost family) | **SHIPPED** as threshold-shatter on the ruled ice/frost family; chill (soft) → freeze (hard) ladder. |
| (3) stun (DR discipline; genre stun-lock failure cases) | **SHIPPED** as hybrid DR (immunity-after-expiry + boss multiplier). |
| (4) poison-dot (PoE vs D2 vs GD stacking; E3 source_element spine) | **SHIPPED** as independent-stack + FIFO; **E3 source_element stamps EXIST and poison consumes them** (`effect_resolver.py:115-149`). |
| (5) cross-cutting: boss rules, thresholds-vs-rank, stack/refresh arithmetic, per-element identity under free-element rule, sim consumption points, telemetry columns | **SHIPPED** — spec §7 interaction matrix, §3.3/§4.3/§5.3 params, §2.6/§3.5/§4.5/§5.5 stacking laws; `dot_taken_by_element` telemetry column live. |
| (6) taunt OUT (rides Wave A) | **HONORED** — taunt is an annex (§6), rides Wave-A proxy layer. |

**Every commissioned coverage item is present in the shipped artifact.** There is no gap the brief
identifies that the shipped spec fails to cover.

---

## §3 — The fork→ruling crosswalk (so no ruled call is silently buried)

The brief mandates every taste/commitment call be marked `[MATT-FORK]` with options + tradeoffs +
precedent + lean. **Here is that discipline honored — but each fork is annotated with its already-
landed ruling, veto-open.** If Matt wants to re-open any, this is the surface to do it on; the
options/precedent/lean are preserved so a veto is a fully-informed act.

### `[MATT-FORK] AL-1 — sunder category` — **RULED: `debuff` (reuse reserved slot)** · veto-open
- Options: (a) reuse reserved `debuff` category; (b) mint new `amplifier` category.
- Precedent: PoE shock/wither = debuff-class; no ARPG needs a bespoke amp category for a single
  primitive. Lean was (a).
- **Ruling (spec §10-a, Gate-1 unchallenged):** `debuff`. `VALID_CATEGORY_VALUES` already reserved it.

### `[MATT-FORK] AL-2 — sunder name` — **RULED: `sunder`** · veto-open
- Options: `sunder` / `expose` / `weaken` / (archived: marked, vulnerable, frailty).
- Precedent/tradeoff: `sunder` = instantly legible "take more damage" to veterans, no ARPG owns it
  as *ailment* identity (PoE's Sunder is a slam *skill* — layer-collision only, and RDR skill names
  are per-kit LLM-generated so no collision at the ailment-vocabulary layer). `expose` carries real
  late-PoE1 Exposure adjacency (laundering risk). `weaken` misleads D2 veterans via invert-flip.
- **Ruling (spec §2.7, gandalf-prime at verify-gate):** `sunder`. Lean adopted.

### `[MATT-FORK] AL-3 — GX-15 synergy shape` — **RULED: additive +10pp at 2+ non-sunder ailments** · veto-open
- Options: (a) binary threshold-at-N additive bonus; (b) per-ailment-count linear scaling; (c) cap-collision multiplicative.
- Precedent: Hades Privileged Status = binary "if target has any status, deal more." D3 elemental
  debuffs stack additively. Lean was (a) at threshold 2.
- **Ruling (spec §2.10):** binary threshold-count 2 (LOCKED), `synergy_bonus_percent` +0.10 default,
  additive at consumer read-time, subject to `max_amp_cap 0.50`.

### `[MATT-FORK] AL-4 — freeze model` — **RULED: duration + threshold-shatter payoff** · veto-open
- Options: (a) pure duration lock; (b) threshold-accumulator (D2 cold-length "freezes when meter
  fills"); (c) duration lock + shatter-on-expiry-under-threshold payoff.
- Precedent: D2's cold-length is the cautionary tale (invisible accumulator → opaque player model);
  PoE2 Ice Strike's two-phase (freeze → shatter) is the modern, legible answer. Lean was (c).
- **Ruling (spec §3, §10-b):** (c). Shatter fires at `effect_resolver` expiry-under-threshold —
  ground: freeze = execute-*setup*, sunder = amp-*window* (niche-separation).

### `[MATT-FORK] AL-5 — stun diminishing-returns` — **RULED: hybrid DR** · veto-open
- Options: (a) flat boss-multiplier only; (b) stack-tracker DR (each stun shortens the next); (c)
  hybrid = universal immunity-after-expiry + boss multiplier.
- Precedent: the genre's stun-lock failures (perma-stun via rapid re-apply) killed by *immunity
  windows*, not by multipliers alone (D3 elite CC-reduction, LE boss CC-resist). Lean was (c).
- **Ruling (spec §4.6, §10-c):** (c). `immunity_after_seconds` HARD floor ≥1.0s; boss takes 75%.

### `[MATT-FORK] AL-6 — poison stacking architecture` — **RULED: independent-stack + FIFO** · veto-open
- Options: (a) PoE1 independent-stack (each application its own instance, cap + FIFO evict); (b) D2
  poison-length (refresh-and-extend single instance); (c) GD vitality-decay rolling aggregate.
- Precedent: PoE1 poison is the genre's build-defining stacker (viable BECAUSE stacks are
  independent and countable); D2 poison-length is the *anti*-pattern the dossier names (re-apply
  *resets* rather than *adds* — punishes fast attackers). Lean was (a).
- **Ruling (spec §5.5, §10-d):** (a). `stack_cap_per_attacker` 8 (HARD guard 10); overflow evicts
  oldest (FIFO). Interacts with E3 source_element attribution per-instance.

### `[MATT-FORK] AL-7 — taunt model` — **RULED: proxy-AI directive** · veto-open
- Options: (A) proxy-AI directive (`PROXY_TAUNT_PRIORITY` weight on enemy nav-selection); (B)
  target-side ailment entry in `ailments.yaml`.
- Precedent: taunt is a *proxy* behavior (pets/summons taunt), not a status the *target* carries —
  keying it target-side would misplace it. Lean was (A).
- **Ruling (spec §6.4, §10-e):** (A). Small delta to Wave A; `golem_construct` already carried
  `targeting_behavior="taunt"`.

**Fork count: 7 `[MATT-FORK]` items — ALL RULED, ALL veto-open.** (The brief's "present forks, don't
resolve" instruction is structurally satisfied by preserving the option-space for veto; it is not
*violated* by reporting that the session already ruled them, because Matt's veto remains live.)

---

## §4 — DL-03 (streams never tax movement) + the chill / movement-tax tension

The brief asks me to name the DL-03 tension where ailments touch movement, honor DL-03, and present
reconciliation options. **This was resolved cleanly in the shipped spec (§11 whole-spec conformance
note). Here is the state:**

**DL-03 addresses CASTER commitment** (a rooted-channel stillness tax on the *caster* — the lesson
that killed the genre's stream archetype). Ailments tax the *target*. The two do not collide by
default:

- **freeze** taxes TARGET movement (that is what freeze *does*). DL-03 governs CASTER movement.
  Non-collision, confirmed spec §3.9 / §11.
- **chill** (the pre-existing soft-control, NOT in the commissioned tranche) is a TARGET movement
  slow — again target-side, outside DL-03's caster scope. **The tension the brief anticipates —
  "chill is a MOVEMENT tax, name the DL-03 conflict" — resolves to non-collision** because DL-03 is
  a caster-commitment law and chill is a target-side status. The reconciliation is *definitional*,
  not a design fork: DL-03's scope is caster movement; chill's scope is target movement; they never
  meet. (Had chill been a caster-held *channel* that slowed the caster, DL-03 would bind — it is
  not; it is an on-hit status.)
- **poison-cloud** (`toxic_cloud`) is the one real DL-03 risk surface: if authored as a caster-held
  channel, it would tax caster movement. **RESOLVED at Gate-1 (spec §5.9):** `toxic_cloud` MUST be
  authored `tags=["placed"]` (place-and-forget, per the `bomb_mine`/`turret`/`totem`/`wall` zone-
  template precedent), NOT `tags=["channel"]`. Rocket authorship binding. DL-03 conformance passes.

**DL-03 is explicitly satisfied across the whole layer.** No open reconciliation fork remains.

---

## §5 — The one GENUINE open residue (if a session fires, THIS is its agenda)

Everything in the commissioned tranche is closed. **One deferred item survives** and is the only
legitimate ailment-design-session agenda item today:

### `[MATT-FORK] AL-OPEN — chill→freeze escalation MECHANISM` — DEFERRED (spec §3.4, §9)
The shipped spec applies chill and freeze as *independent* rolls. A **cold-ladder escalation** — a
skill that has already applied chill AND lands a heavy secondary hit *promotes* chill→freeze — was
DEFERRED (`§9: "manual per-skill rolls suffice for MVP"`). This is a real design fork with genre
precedent both ways:
- **Option (a) — no auto-escalation (current MVP state):** chill and freeze roll independently; a
  build wanting freeze rolls freeze directly. *Pro:* simplest player model, no hidden accumulator
  (avoids the D2 cold-length opacity trap). *Con:* the chill→freeze *fantasy* (cold builds toward a
  lock) is not mechanically expressed — it's flavor only.
- **Option (b) — threshold escalation:** N chill applications (or chill + heavy hit) auto-promote to
  freeze. *Pro:* expresses the cold-mage fantasy; PoE2's ailment-priming lineage validates
  build-toward-payoff. *Con:* reintroduces an accumulator to communicate (the exact thing D2 got
  wrong); needs a visible player-facing meter or it's opaque.
- **Genre anchor:** PoE2 mainlined primed-ailment → consume loops (the bell, primed ailments); D2
  cold-length is the negative twin. Last Epoch's freeze-rate-vs-freeze is the middle path.
- **gandalf lean:** DEFER remains correct until there is playtest evidence that the cold class
  *feels* incomplete without escalation. The empirical criterion is **playtest of a cold-focused
  build against the shipped chill+freeze pair** — if the escalation fantasy reads as missing, fire
  (b) with a visible meter; if independent rolls read fine, (a) stands. Do NOT build the accumulator
  speculatively — that's inventing a mechanic ahead of the felt need (and re-importing the D2 trap).

This residue **gates no census expressibility** (V13 = 99.47% was reached without it) and gates no
wave. It is a *polish/depth* fork, not a coverage fork.

---

## §6 — Steward's recommendation

1. **Do not fire a fresh ailment-layer design session against the shipped tranche.** It is ratified,
   built, pushed, and drove the engine's highest-value census delta. A duplicate prepared-surface
   would contradict remote truth and risk re-litigating veto-open rulings that Matt has had standing
   since 2026-07-16 without exercising the veto.
2. **If Matt wants to exercise a veto** on any of the 7 ruled forks (§3), this disposition is the
   surface — every option-space and lean is preserved for a fully-informed reversal. Route a veto
   through the normal path (Matt → decisions-log entry via jack-ryan; supersession-not-amputation
   per canon-doc §6).
3. **The only live design agenda** is `AL-OPEN` (§5) — chill→freeze escalation — and its correct
   disposition is **stay deferred pending cold-build playtest evidence.** No draft needed until that
   evidence exists.
4. **Wave-C's 4 additions** (blind/curse/fear/execute, 2026-07-17) are also shipped
   (`wave-c-trigger-mark-engine-spec.md`); if any future ailment session convenes it should baseline
   off the **16-ailment** registry, not the 8-ailment contrast the pause-2 brief assumes.

---

## Provenance / read trail (this disposition)

- `agentic_orchestration/gandalf/views/v3-mechanics-leverage-v1.md` — PAUSE-2 RULINGS block (commission + GX-15 fold)
- `agentic_orchestration/gandalf/views/rekey-prep/elem-prep.md` §6 — Q21 rulings (water→ice; cold/frost family; element = FREE axis, NO mapping ever)
- `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` — the SHIPPED spec (STATUS CURRENT)
- `~/Games/reincarnated-engine/config/ailments.yaml` — 16-ailment registry (read-only)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py:55,115-163` — tick loop, E3 source_element stamps, freeze-shatter + stun-immunity hooks
- `~/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:1593` — `_try_apply_ailment`
- `canonical/current-to-end-state/current-to-end-state-engine.md:74` — ailment lifecycle COMPLETE record; census cascade V8→V13
- engine remote-truth commit `cec8f12` (Gate-2 PASS); collab findings `481f8fb2`

**Signed:** gandalf, 2026-07-21 (DRIFT-CRITIC disposition; veto-open on the record itself). The
session already happened. The steward's job here is to say so — not to draft its ghost.
