# Proxy-Primary Architecture — Recognition Record (2026-06-12)

**Author:** gandalf
**Mode:** Pattern B (Matt terminal dialogue, Session 1)
**Status:** RECOGNITION RECORD — architectural commitments deferred per recognition → validate → commit discipline (OP § 3.4). Empirical gate named in § 5.
**Ratified by:** Matt, 2026-06-12 ("I like them all. approved" — Session 1 batch; charter captured at ruling record § 5)
**Companion:** `gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 5
**Anchors:** Legolas ARPG-trichotomy research; `canonical/47-damage-scaling-architecture-2026-05-27.md`; `qd-engine-bc-axes-lock-2026-05-20.md` § 3; Session 2 spec § 3 (ProxyCombatant); Session 4 spec § 1.1

---

## 1. The recognition

Matt, 2026-06-12 (paraphrased from verbatim): the canonical ARPG class-architecture split across 20 years of the genre is NOT physical-vs-caster. Legolas's research found a **trichotomy: physical vs caster vs proxy/summoner.** Diablo 2's Necromancer, PoE's minion-witch lineage, Grim Dawn's Cabalist pets, Last Epoch's Beastmaster/Necromancer, Torchlight's pet-classes — the summoner seat is structural across the genre, not a flavor variant of caster.

Reincarnated's current architecture (Session 4 § 1.1) defines kit architecture types entirely in damage-scaling terms — every kit is some flavor of "I deal the damage." Proxy capability exists only as a **bolt-on**: a physical or caster kit that picks up a PROXY-family T4 strategy. There is no kit composition where proxy/summon capability is *more core to the kit's nature than casting or physicality is.*

**The design goal (Matt-stated):** preserve hybridization (physical kits and caster kits CAN gain proxy capability), AND add a proxy-primary kit composition that achieves the canonical three-way balance. Matt flagged he has not fully thought it through — "maybe this would prove impossible" — hence recognition-record status, not commitment.

## 2. Substrate inventory — the measurement layer already reserves the seat

This is the strongest evidence the recognition is sound rather than speculative. Four independent substrate surfaces, designed BEFORE this recognition, already hold an empty chair for proxy-primary:

| Surface | Reservation |
|---|---|
| **Axis 2A (proxy density)** | 3-bin axis (none / supplemental / proxy-primary) — locked 2026-05-20, deferral retired at Session 2 ratification via ProxyCombatant. The `proxy-primary` bin EXISTS in the locked vocabulary and is currently unreachable by any generatable kit. |
| **Axis 2 `multi-spawn` bin** | Damage-geometry bin for damage arriving via spawned entities. Reachable today only as minority share on bolt-on proxy kits. |
| **Session 4 § 2.2 `Invoker` label** | One of the 18 identity labels names exactly this fantasy. Under vestigial-ontology discipline labels are NAME-ONLY post-generation — but the label's reachability is currently near-zero, which the Item-8 reachability report would flag anyway. |
| **Session 4 § 5.2 proxy-gear investment row** | The investment-profile table includes a proxy-scaling gear row with no architecture type that primarily consumes it. |

The substrate has been voting for this seat without us naming it. Naming it now is recognition; filling it is the deferred commitment.

## 3. Design sketch (NOT committed — shape of the eventual work)

1. **Fourth architecture type** at Session 4 § 1.1: `proxy_primary` alongside the existing damage-scaling types. Defining property: the kit's expected majority damage share arrives via proxy entities (`proxy_contribution_pct` ≥ ~0.5), with the player's direct skills oriented toward enablement (summon, command, buff, sacrifice-trigger) rather than direct damage.
2. **Doc-47 proxy scaling path.** The PoE minion-scaling lesson by name: minion builds died or dominated in eras where minion damage didn't share the player's scaling vocabulary (pre-3.4 support-gem starvation, then Necromancer-meta overshoot). Doc 47's damage-scaling architecture needs a proxy-scaling lane — gear/trait affixes that scale proxy damage/HP the way existing affixes scale skill damage — or proxy-primary kits will be structurally un-tunable at the balance loop.
3. **Trichotomy share target:** proxy-primary at roughly ~15–25% of the in-band kit population (genre-typical summoner share; D2 ladder and PoE league data both put dedicated summoner play in this band), NOT a forced 33/33/33.
4. **Proxies do not summon proxies** (Matt-ruled 2026-06-12). PROXY_FISSION's death-split is the sole bounded exception (recursion cap 4 entities, 30s expiry) — it is replication-on-death, not autonomous summoning. Genre precedent supports the ruling: no major ARPG grants minions their own minion trees; where it appeared (PoE spectres summoning adds) it was bounded by spectre-specific behavior, never a player-scalable loop.

## 4. Dependency sequencing (Matt-ratified)

**Q6 (PROXY_CONVERGENCE merge matrix) and Q7 (DUAL_PROXY compatibility pools) fire AFTER proxy-primary.** Rationale: both matrices enumerate proxy-type pairings, and a proxy-primary architecture type changes which pairings matter and what the matrices' coverage obligations are. Authoring them against the bolt-on-only world risks immediate rework. Q8 (companion strategy-pair matrix) is independent — companions carry full kits; ruled variant-agnostic.

Legolas Mode A pull (genre precedent for merge/dual-summon mechanics + summoner-archetype composition) services Q6/Q7 and § 3 here in one commission — fire when proxy-primary re-engages.

## 5. Empirical gate (the validate step — what re-opens this for commitment)

Per recognition → validate → commit, the architectural commitment (fourth architecture type + doc-47 proxy scaling lane) fires when:

1. **Gamora Items 1–2 land** (ProxyCombatant + symmetric kernel extension) and a smoke population of bolt-on proxy kits simulates clean;
2. **`proxy_contribution_pct` reachability check:** within that smoke population, verify the metric can reach ~0.5 under existing PROXY-family strategies when generation deliberately stacks them. If bolt-on stacking already approaches majority-share, the fourth type is a generation-prior + identity question (cheap). If the metric ceilings well below 0.5, the kernel/scaling work is load-bearing (doc-47 amendment first).

The gate is substrate evidence, not time-passage. Whichever branch the reachability check selects, the result routes back to a Pattern B session for the commit decision.

## 5.1 Gate resolution — KERNEL-CEILING sub-question RESOLVED (cheap branch selected)

**Gamora Items 1–2 landed 2026-06-12.** Result: 16/16 ProxyCombatant smoke tests pass; `proxy_contribution_pct = 0.556`; 0/60 golden-master cells moved vs. oracle.

**Reading the 0.556 — precisely what it proves and what it does not:**

- `0.556` is the **deterministic attribution identity** Σdm = 1.25 → 1.25 / 2.25 = 0.556 (proxy contributed 1.25 of 2.25 total damage units in a constructed test). The kernel faithfully attributes whatever proxy damage exists, and the metric **can represent a majority proxy share (> 0.5).** There is **no kernel attribution ceiling.**
- 0/60 golden-master cells moved → the ProxyCombatant extension is a clean brownfield addition; no existing balance was disturbed.

**Branch selection.** The gate's § 5 reachability check had two branches: (a) metric ceilings well below 0.5 → doc-47 scaling rework is load-bearing-first (EXPENSIVE); (b) metric reaches ~0.5 → fourth type is a generation-prior + identity question (CHEAP). The 0.556 result eliminates branch (a) **at the kernel/attribution layer:** the kernel does not cap proxy share, so the fourth type does not require a doc-47 scaling rework *as a precondition.* **The CHEAP branch is selected.**

**What is NOT yet proven (the honest caveat — recognition → validate → commit still holds).** 0.556 came from a **constructed attribution test**, not from a realistically-sampled generation run. The kernel-ceiling sub-question is resolved; the **corpus-population sub-question is still open:**

> Will realistically-sampled kits that stack PROXY-family strategies actually land `proxy_contribution_pct` ~0.5 **in emergent combat** (not in a constructed test), AND land in-band at the genre-typical ~15–25% trichotomy share?

That requires rocket Item 1 (generation) + a measurement pass over a real smoke corpus. Until that lands, the architecture-type commitment stays a **DRAFT**, not a hard lock. The doc-47 proxy-scaling lane is **downgraded from load-bearing-first to a tuning-time concern** (still likely wanted for balance-loop control of proxy kits, but no longer a gating precondition).

**Net:** the amendment below (Session 4 § 1.1) moves from *empirically-gated PENDING* → *DRAFT commit, cheap path, pending corpus-population validation.*

## 5.2 Identity-centroid decision — HIGH-CENTROID summoner (Matt-ratified 2026-06-12)

**Source:** Legolas Mode A proxy-summoner genre-precedent research (`legolas/research/2026-06-12-proxy-summoner-genre-precedent/findings.md`, Findings 7 + 9 + 11); Pattern B threshold dialogue, Matt-ratified ("high-centroid with the enablement-loop commitment").

**The question this resolves.** The original spec used `proxy_contribution_pct ≥ ~0.5` as the *defining property* of proxy-primary. That number was silently doing two different jobs: the **bin boundary** (where a kit starts counting as proxy-primary) and the **identity centroid** (what the typical generated proxy-primary kit aims at). The genre evidence forces them apart.

**The genre band.** Dedicated summoners run **90%+ minion damage**; their player hotbars carry **zero direct-damage skills** — only curses, offerings, auras, convocation, re-summon (Findings 7, 9). The three identity markers: (1) stat budget → proxy modifiers not player offense; (2) player active skills = enablement, not direct damage; (3) defensive survival investment.

**Why 0.5 fails by construction.** Marker (2) is load-bearing and **enablement skills deal no damage.** A kit at 0.5 contribution must produce the *other half* of its damage somehow — and the only source is player **direct-damage** skills, which violates marker (2). So a 0.5 kit is a **hybrid by mathematical necessity** (half caster, half proxy) wearing a proxy-primary label — *"a caster with strong pets,"* not the third chair. Only at a centroid high enough that the player's residual damage is **enablement-incidental** (a curse that chips, a sacrifice-trigger that bursts) do the markers hold. That floor is ~0.75+.

**Decision (Matt-ratified):**

| Parameter | Value | Status |
|---|---|---|
| **Axis 2A bin boundary** (supplemental → proxy-primary) | majority ≥ 0.5 | UNMOVED (locked vocabulary respected) |
| **Generation-target centroid** (the prior for the `proxy_primary` architecture type) | **~0.80** (population ~0.65–0.95) | RATIFIED |
| **Enablement-action loop** (player agency = command, not damage) | scope obligation on Session 3 + T4 PROXY family | ACCEPTED |
| **Rathma guardrail** | proxy-primary player payoff is COMMAND, never a player damage nuke (no minions-as-resource → player-ultimate drift; Finding 11) | RECORDED |

**The Necromancer / Warlock mapping (Matt's framing).** The two Axis 2A bins are not a quantity slider — they are **two recognized genre archetypes:**

- **Supplemental bin (~0.2–0.4)** = the **Warlock** position: a caster who *also* fields strong summons that hold space and pressure, but the damage lives with the player. Already supported for free as the bolt-on hybridization case.
- **Proxy-primary bin (~0.80 centroid)** = the **Necromancer** position: the player *is* his proxies; player skills command. The new architecture type.

We ship both. This confirms the locked Axis 2A axis was structurally right — we had merely not named what each bin *was.*

**Corpus-validation consequence (sharpens, does not weaken, § 5.1's open sub-question).** The hard-commit gate's reachability target moves from ~0.5 to **~0.80**. Gamora's 0.556 proved the kernel *can* represent majority share; 0.80 is a harder generation bar. The measurement pass (rocket Item 1 + corpus) must now show realistically-stacked PROXY kits clustering at ~0.80, not merely crossing 0.5. The doc-47 proxy-scaling lane's relevance rises accordingly (Finding 10: cap independent multiplicative scaling layers at 2–3 with a shared ceiling, per the PoE 3.8→3.15 cautionary history) — still tuning-time, not a precondition, but more likely to be wanted.

**Q7 / Q6 carry-throughs from the same research (for the upcoming dialogue):** Q7 DUAL_PROXY pools should encode **role complementarity** (tank + damage), not hard type-pair gating — the PoE Carrion Golem "bridge unit" is the cleanest precedent (Finding 6). Q6 PROXY_CONVERGENCE is genre-novel territory (LE Abomination is the sole precedent, a pre-combat ritual); our **averaged-stats** combination is the balance-safer choice (Finding 1). These are flagged for the Q6/Q7 session, not resolved here.

---

*Sign-off: gandalf, 2026-06-12. The genre kept three chairs at this table for twenty years; we built the room with three chair-shadows on the floor and only two chairs. The recognition is that the shadow was always load-bearing. Gamora's 0.556 confirms the third chair will hold weight — what remains is to prove the room fills it the way the genre's rooms always have.*
