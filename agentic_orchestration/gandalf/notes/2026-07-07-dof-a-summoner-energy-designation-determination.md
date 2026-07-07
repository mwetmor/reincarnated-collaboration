# DoF-A — Summoner energy designation: DETERMINATION (focus)

> **STATUS:** DETERMINATION — design-steward ruling within gandalf authority (does NOT
> escalate to Matt; reasoning in §4). Records the resolution of the cross-seam DoF rocket
> routed from proxy-T4 B1-REBASE Phase-1 v3 re-fire (Matt 2026-07-07 arc-close batch).
> **Author:** gandalf (story-and-design steward), 2026-07-07.
> **Role-tags this session:** DRIFT-CRITIC (judging rocket's two pre-registered resolutions
> against fantasy + pipeline-economy) → SPEC-AUTHOR (the content designation I rule).
> **Routed by:** rocket, `generation/math/proxy-t4-b1-rebase-phase1-v3-refire-2026-07-07.md` §2.
> **Consumed by (GATES):** gamora A3 re-confirm (`simulation/math/proxy-t4-suite-rebase-eval-extension-2026-07-07.md` §2)
> + rocket's fixture-designation code (one additive `energy_type` field on `DemoSummonerSpec`).
> **Anchors:** doc-48 §3.1 LOCKED G1 economy table (`season_generation_pipeline.py:245-312`);
> combatant.py `_ENERGY_CONFIGS` (:415-426); emergent-necromancer discipline
> (`reap-die-rise-engine/2026-05-31-hypothesis-flow-pattern-library-architecture.md` §1.7.4);
> Matt item-4 (MELEE summoners kept in v2 curation — necromancer mandate).

---

## 1. DETERMINATION

**R-A1, with `focus`.** Re-designate the demo melee-summoner fixture's `energy_type` to
`focus`. This is rocket's recommendation and it is the correct call on BOTH grounds the DoF
names — thematic coherence AND pipeline economy. I additionally strengthen the rationale
beyond rocket's framing with a **mechanical-fantasy finding** (§3) that makes `focus` not
merely *acceptable* but *the right death-magic economy on its own kernel behavior*, and I
resolve a substrate-led-discipline concern (§4) that R-A1 is a legitimate curated departure,
not a taxonomy pre-imposition.

**R-A2 (count-axis separation) is REJECTED as the resolution** — not because it is wrong, but
because it *drops the marquee capstone from the demo*. Reasoning in §5.

---

## 2. Why `focus` is thematically coherent for the melee-summoner necromancer

The necromancer in Reincarnated is an **emergent** kit concept, not a pre-imposed class
(`…hypothesis-flow…` §1.7.4 — substrate declares shadow/umbra/bone/soul; the LLM + composition
synthesizes "Necromancer"). So the question is NOT "what resource does the Necromancer class
use" (there is no class). It is narrower and answerable: **for a hand-authored DEMO summoner
fixture whose fantasy is a second-body / raised-dead economy, which of the four valid
`energy_type` tokens {mana, rage, focus, stamina} reads truest?**

- **`mana`** — the default INT→mana (Magus) economy. Generic caster fuel. Reads as "wizard,"
  not "one who tethers the dead." It is the *absence* of a designation, not a designation.
- **`rage` / `stamina`** — martial/exertion economies. Wrong fantasy for a summoner (these are
  the barbarian/wildhunter registers).
- **`focus`** — attention/will/concentration. The reading rocket names ("soul/attention
  economy") is exactly right: a summoner does not *spend* their dead the way a mage spends
  mana; they *hold their attention on them.* Drop the focus and the tether frays. This is the
  D2 Necromancer's "you are commanding, not casting" fantasy, and the D4 Necromancer's
  Essence-as-attention resource, rendered in the one token our vocabulary already has for it.

Diablo precedent, named: D2's Necromancer summons persist while you divert mana elsewhere — the
army is *standing attention*, not *spent charge*. D4's Necromancer runs on **Essence**, a will/
soul pool distinct from mana precisely to signal "this is death-command, not spellcasting." The
generic-mana designation would erase that signal. `focus` restores it with zero new vocabulary.

**Melee-summoner specificity (Matt item-4):** the v2-curated summoner is MELEE (the Death
Knight / grave-warden who fights *among* their raised dead), ranged summoners excluded to
LAUNCH. A melee necromancer channeling *focus* to hold the horde while their own body is in the
fray is a sharper, more legible fantasy than a backline mana-caster — the resource you must
keep spending attention on *while* you melee is a real build-tension, not flavor paint.

## 3. The load-bearing finding — `focus` is mechanically the death-economy, not just nominally

This is the addition beyond rocket's note. I inspected the kernel (`combatant.py:156, 414-418`):

```
"focus": (100.0,  True,  -5.0),   # pool_max=100, start_full=True, regen=-5.0/s
# combatant.py:156 — "starts full, decays passively (mana_regen < 0), restored on skill use."
```

`focus` is the ONE energy_type in the vocabulary that **passively DECAYS and is REFILLED by
acting.** Every other economy either sits inert (rage/combo/charge-stack accumulate) or
regenerates upward (stamina, mana). `focus` bleeds out unless you keep channeling.

That is *mechanically* the summoner's tether: **an army you must keep feeding attention or it
decays.** The kernel already encodes the exact death-magic fantasy — a raised host that
requires active upkeep, not a fire-and-forget spell. Choosing `focus` is therefore not a
cosmetic string swap to open a gate; it lands the fixture on the single kernel economy whose
*behavior* matches its fantasy. This upgrades my confidence in R-A1 from "acceptable content
choice" to "the correct one on independent mechanical grounds."

(Note for the emission/balance seam, non-blocking: the passive-decay behavior interacts with
proxy upkeep in a way that could become a real build-tension knob later. That is gamora/
rocket's lane at B4, not this DoF. Flagging, not deciding.)

## 4. Why this is a design-steward call and NOT a Matt escalation

Two tests, both pass for in-authority:

1. **Substrate-led discipline (Discipline #41 / Pattern R-3 guard).** R-A1 does NOT pre-impose a
   class taxonomy. It designates the `energy_type` of ONE hand-authored *demo fixture* — a
   curation act on a specific instrument, explicitly analogous to the `shadow:soul` designer-
   curation-overlay precedent (`2026-06-01-flavor-pool…` — a single transparent designer
   judgment where substrate is silent, tagged as such). The population pipeline's doc-48
   economy table is UNTOUCHED (INT-caster cells still resolve to mana by G1). We are not
   overriding the economy *rule*; we are authoring a curated fixture that intentionally departs
   from the default, which the demo-fixture layer exists to do. That is content curation, which
   is my seam, not a genre-canon rule change, which would be Matt's.

2. **No new vocabulary, no rule change, no magnitude touch.** `focus` is an existing valid
   token with an existing kernel config. Nothing in the locked doc-48 table, the chassis
   constants, or the bars/bands moves. The blast radius is one additive field on
   `DemoSummonerSpec`, read by gamora's eval. A one-fixture curation designation inside frozen
   guardrails is exactly the kind of call the run-boundary discipline routes to gandalf *to
   decide*, not to escalate.

**Where it WOULD escalate (and does not, yet):** if this became "the Necromancer *class* runs
on focus as a shipped population economy" — i.e., we wanted to ADD a summoner row to the LOCKED
doc-48 G1 economy table so emitted summoner kits carry `focus` — THAT is a population-economy
canon change and routes to Matt (it changes what the generator ships, not what one demo fixture
reads). I explicitly scope THIS determination to the **demo fixture only.** The population-
economy question is registered as a forward decision below, not answered here.

## 5. Why R-A2 is rejected as the resolution

R-A2 (keep fixtures mana; separate A3 on the count axis alone: count-N horde → ASCENSION vs
count-1-full → FISSION) is *technically valid* — it makes A3 pass without the energy gate. But
it has a design cost rocket names and I weight as decisive: **SOVEREIGNTY stops being demoed by
the A3 fixture pair.**

SOVEREIGNTY is the "second hero" — a full-body proxy that fights as a peer, not a swarm. In the
proxy family it is the *marquee capstone*, the most legible and most aspirational of the five.
A demo whose fixture set cannot exhibit its top-billed capstone is a weaker demo. rocket's
coverage note ("SOVEREIGNTY still η-offerable to any non-mana full-body kit the corpus
produces") is true but cold comfort: *offerable-in-principle* is not *shown-in-the-demo*. The
demo's job is to make the marquee thing visible. R-A2 hides it to avoid a one-field content
designation that we should make anyway on fantasy grounds. Wrong trade.

R-A1 costs one additive field and gets us: (a) a correct death-magic economy, (b) SOVEREIGNTY
demoed, (c) the hidden eval-side `charge_stack` coupling removed (gamora reads the landed
designation instead of assuming an invalid token). R-A2 costs a fixture-set reshape and gets us
a demo that can't show its best capstone. R-A1 dominates.

**Also disposed:** the current eval-side `_A3_ENERGY = "charge_stack"` hard-code is retired by
this ruling regardless — `charge_stack` is not a valid `energy_type` (it is a substrate-family
token; the kernel `charge-stack` economy is the Assassin's build-hold-stacks pool, a different
fantasy entirely). Designating `focus` replaces an invalid-token assumption with a valid,
landed, correct designation.

## 6. Instructions to the gated consumers

- **rocket (fixture-designation code):** add the additive `energy_type = "focus"` field to the
  demo melee-summoner fixture(s) on `DemoSummonerSpec`, exposed so gamora's eval READS it (not
  assumes it). MIGRATION line owed per your §4.3 (new kit-level `energy_type` read for gamora).
  Population doc-48 table UNTOUCHED (this is fixture curation, not an economy-rule row).
- **gamora (A3 re-confirm):** §2 case-1 branch fires — re-run `rank_proxy_t4_family` on both
  fixtures under the landed `focus` designation; A3's v1.83 *conditional* PASS becomes
  *unconditional* PASS (bone→FISSION, crypt→SOVEREIGNTY via the now-open `energy≠mana` gate,
  different tops). Retire the `_A3_ENERGY = "charge_stack"` eval-side hard-code; read the
  landed field. Stamp the A3 designation (`focus`) in the artifact per your §4 "A3 designation
  stamp" hook.
- **DoF-B (F-f) is NOT in scope of this determination** — that is rocket's R-B1 disposition
  (consumer exists; live call site is B4-scoped), a generation/process call, not a fantasy or
  economy designation. No gandalf ruling needed there; jack-ryan Gate territory if it needs one.

## 7. Forward decision registered (NOT answered here) → for a future ELICITOR/Matt pass

**Q (population-economy canon):** should EMITTED summoner/necromancer population kits (not just
the demo fixture) carry `focus` rather than the doc-48 default (INT→mana)? This would mean
adding a summoner-shaped row to the LOCKED G1 economy table — a population-economy canon change,
Matt-gated. Empirical gate before it's worth asking: B4 emission surfaces real summoner kits and
we can see whether mana-summoners read as flat vs focus-summoners reading as tethered.
**Deferred, not decided.** The demo fixture designation (this note) does not prejudge it; it
only establishes that `focus` is the coherent reading when we DO curate a summoner deliberately.

---

## 8. Determination summary

| | |
|---|---|
| **DoF** | DoF-A — A3 energy designation (summoner-path proxy-T4) |
| **Ruling** | **R-A1 with `focus`** |
| **Grounds** | thematic (attention/tether economy; D2/D4 necromancer precedent) + mechanical (kernel `focus` passively decays, refilled by acting = the upkeep-army fantasy) + pipeline-economy (valid token, non-mana, opens SOVEREIGNTY) |
| **Authority** | gandalf design-steward (demo-fixture curation; NOT a population-economy canon change; substrate discipline held — doc-48 table untouched) |
| **Escalation** | NONE required for the demo fixture; population-economy version registered as a future Matt-gated fork (§7) |
| **Unblocks** | gamora A3 re-confirm (§2 case-1) + rocket fixture-designation code |
| **Rejected** | R-A2 (drops SOVEREIGNTY from the demo — wrong trade) |
