# Composed re-baseline DIAGNOSTIC STOP — three-fork design ruling

**Type:** gandalf design ruling (the 2c-equivalent felt-rhythm / band-shape call). Subagent ruling returned to knight-rider for a Matt halt.
**Date:** 2026-06-20
**Author:** gandalf (story-and-design steward)
**Authority:** instrument-validity workstream, gandalf-owned. gamora escalated a methodology+design fork at the Phase-5 composed-rebaseline validation gate (the brief reserves band-METHODOLOGY and magnitude calls to gandalf/Matt; gamora correctly STOPPED rather than wire a band she judged fake). Ruling the three forks.

**Evidence (read first-hand):**
- gamora STOP artifact: `agentic_orchestration/cycle-14-wave-5-season-001/composed-rebaseline-phase5-DIAGNOSTIC-STOP-20260620.json` (per-economy×per-shell median KPM table).
- My own prior ruling, now load-bearing: `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` — the encounter-measurement doctrine, ADOPTED by Matt 2026-06-19.

---

## 0. The one-line ruling

**gamora is right, and she is more right than she claimed.** The composed instrument's per-economy bimodality is not a new problem requiring a new band methodology to be invented under fork (1). It is the **exact failure the doctrine I authored — and Matt ADOPTED — five workstream-days ago already condemned**: a single KPM band is being applied to shells where it does not belong. The composed instrument did not break the band method; it **stopped lying well enough to hide that the band method was already wrong on these shells.** The fix is not "invent an economy-aware band." The fix is "finish wiring the doctrine that is already ruled." That collapses all three forks into one clean sequencing decision for Matt.

---

## 1. FORK 1 — economy/attribute-aware band: RULED, but reframed (and the reframe matters)

**gamora's recommendation (make the band economy-aware) is directionally correct but names the wrong axis.** Ruling:

**The band does NOT become per-economy. The band becomes WIN-CONDITION-aware — which the doctrine already ruled, and which the composed numbers now make unignorable.**

Look at the table through the doctrine's lens (§1 of the spine — the win-condition split, ADOPTED by Matt):

| | rage | combo | stamina | mana | what the doctrine says this shell IS |
|---|---|---|---|---|---|
| open_arena | 15.6 | 26.0 | 61.7 | 51.7 | **clear room** → KPM band, floor+ceiling |
| chokepoint | 14.9 | 27.2 | 53.5 | 49.5 | **clear room** → KPM band, floor+ceiling |
| magic_pack | 18.7 | 27.8 | 100 | 600 | **clear room** → KPM band, floor+ceiling |
| elite_pack | 8.3 | 13.0 | 600 | 428 | **clear room** → KPM band, floor+ceiling |
| mini_boss | 11.7 | 15.8 | 0.5 | 0.25 | **BOSS room** → survive+kill gate, KPM NEVER gates |
| boss | 7.9 | 11.0 | 2.6 | 0.58 | **BOSS room** → survive+kill gate, KPM NEVER gates |

Read the two boss rows. The casters' ~72× advantage on elite_pack and their crater to 0.25–0.58 on the boss rows are **the same phenomenon the clean-boss-run already measured** (spine §5: int/wis survive+kill ≈0.99, `a_dead=0.000`, but the gate KPM-rejects them). The composed instrument is reproducing the doctrine's central finding from the *composed* path: **the boss rows do not belong in a KPM band at all.** Banding them per-economy would not fix the lie — it would carve the lie into four economy-shaped pieces. mana@boss 0.58 KPM is not a "mana boss band"; it is a build that survives-and-kills the boss in ~217s (inside the 240s enrage timer the doctrine made the gate) and the KPM number is a meaningless byproduct of single-target TTK, exactly as §5.3 of the spine warned ("on a single-boss shell, no-kill ⇒ ≈0 KPM, so it is circular with timeout").

**So fork (1) resolves as:**
1. **Boss shells (mini_boss, boss_with_adds): the band is DELETED, not made economy-aware.** They move onto the survive-and-kill-within-the-enrage-timer gate the doctrine already ruled (spine §1, §6 — UNBUILT). KPM/TTK becomes measure-only, never gates. The 72×/cratered spread on these rows STOPS BEING A BAND PROBLEM the instant the doctrine's boss-gate is wired, because no band touches them.
2. **Clear shells (open, choke, magic, elite): the band stays a KPM band — and HERE the economy-awareness question is real but SMALLER than gamora's table implies.** The remaining within-shell spread on the clear rows (e.g. elite_pack rage 8.3 → combo 13.0 → caster 428/600) is partly the SAME timing-floor artifact (fork 2, below) contaminating the caster cells, NOT genuine cohort structure. Once the 600@0.3s timing-floor cells are excluded as artifacts (fork 2), the honest clear-room spread to band over is the build-spend economies (rage/combo: 8–28) plus throttled-caster cells. **Whether the residual clear-room band is per-economy or single-per-shell is NOT answerable until fork 2 is resolved** — because right now the caster clear-room cells are saturated junk, and you cannot fit a band over saturated junk. So I do NOT rule per-economy clear-room banding yet; I rule that the question is **downstream of fork 2** and is a magnitude-cleanup-then-re-measure question, not a methodology-invention question.

**Granularity ruling, stated plainly for Matt:** NOT per-economy as a new band methodology. The doctrine's win-condition split (already adopted) is the correct axis. Boss shells leave the band entirely; clear shells keep one KPM band per shell, and the per-economy-vs-single question on clear shells is deferred behind fork 2 because the caster clear cells are currently artifact-saturated. **gamora invented nothing; she rediscovered the adopted doctrine from a new direction.** That is the cleanest possible outcome — it means the methodology is not unsettled, it is unfinished-building.

---

## 2. FORK 2 — the 600@0.3s timing-floor: LEAVES the workstream, but with a NAMED entanglement boundary

**Ruling: fork 2 is a separate Matt-scheduled magnitude workstream. gamora's read is correct. BUT it is NOT cleanly separable on the clear shells — and the boundary must be drawn precisely or the clear-room band will be fit over garbage.**

Two distinct things are tangled in the 600 number, and they split cleanly along the win-condition line:

- **On BOSS shells, the timing-floor is irrelevant.** The boss cells (0.25–2.6 KPM) are the OPPOSITE of saturated — they are long single-target grinds. The 600-ceiling artifact never touches them. So for the boss shells, fork 2 has NOTHING to fix; the doctrine's boss-gate (fork 1) fully resolves them with zero magnitude work. **The boss rows do not block on fork 2 at all.**
- **On CLEAR shells, the timing-floor DOES contaminate the caster cells** (magic_pack mana 600, elite_pack stamina 600 / mana 428). A 3-mob pack one-shot in 0.3s saturates a KPM ceiling that is a fight-resolution artifact (sub-second clears divide by a duration floor), not a real throughput. **The clear-room band CANNOT be honestly fit while these cells are artifacts.** So fork 2 *blocks the clear-room band fit* but does *not* block the boss-gate.

**Verdict:** fork 2 leaves the instrument-validity workstream as a magnitude re-tune (SPATIAL_DAMAGE_SCALE / mob-HP; composes with the MOB_HP workstream, as gamora said). The entanglement is asymmetric and must be stated to Matt: **the boss-shell half of the band fix is unblocked and can land now; the clear-shell band re-fit is BLOCKED behind fork 2.** This is not "magnitude workstream first." It is "boss-gate now, clear-band after magnitude." The spine binds, the workstream does not need to halt — only the clear-room re-band waits.

---

## 3. FORK 3 — the design call (caster spike + caster crater): both are IDENTITY, not defect — within their correct win-condition

This is the seat's call and I will give it cleanly, because the doctrine already pre-decided the principle and the composed data just instantiated it.

**3a. The 600-KPM caster spike on small packs — is it defect or fantasy?**
**It is fantasy on the GAMEPLAY axis and artifact on the MEASUREMENT axis. Both are true and they do not conflict.**
- *Should an unthrottled greedy-capstone caster one-shot a 3-mob pack?* **YES — that is the caster power-fantasy and the genre delivers it.** The Diablo III caster (pre-nerf Tal Rasha / Archon) vaporizing a trash pack with a single capstone IS the class fantasy; PoE's clear-speed caster archetype is built on exactly this. A build-spend economy energy-metering the capstone (rage/combo, stable 8–28) and a caster pool-dumping it (burst-then-recover) is **legitimate economy differentiation** — it is the resource-economy BC axis doing its job. I rule the *behavior* is identity, NOT a defect to tune out.
- *BUT the 600 NUMBER is a measurement artifact*, not a measure of that fantasy. A sub-second clear divides kills by a duration floor and pins the KPM ceiling regardless of how much faster the build "could" go. So: **keep the caster burst fantasy; do NOT let the 600 cell into any band.** The clear-room CEILING the doctrine mandates (§2 — too-fast clear is a pacing defect) is the correct *gameplay* governor here: if a caster genuinely clears `open_arena` at 3× cohort pace, the run paces wrong (loot/XP fire-hose, packs evaporate) and the ceiling SHOULD reject it. That is a real design lever. But the 600@0.3s cell is not evidence of that — it is evidence the magnitude is uncalibrated (fork 2). **Tune the magnitude so the caster burst lands as a FAST clear (a real, measurable number well above cohort floor) rather than a SATURATED clear (600 ceiling-pin), then let the doctrine's clear-room ceiling do the pacing-governance.** Defect-to-tune: only the saturation. Identity-to-keep: the burst.

**3b. The caster boss-crater (~0.5 KPM, 217s) — Phase-4 over-correction or intended identity?**
**Intended identity at the boundary, and NOT a Phase-4 over-correction — the clean-boss-run already proved this.** Spine §5: int/wis survive+kill ≈0.99 with `a_dead=0.000` at faithful power. The caster does NOT crater on the boss in any way that matters — it KILLS the boss, in ~33–35s median TTK on the clean run. The 217s/0.58-KPM figure in the composed table is the *KPM metric* cratering on a single-target shell (circular with TTK per §5.3), NOT the caster *failing*. **There is no caster boss-crater to over-correct.** Phase-4 armor/resist symmetry did its job: casters eat the boss armor wall and still kill inside the timer. The "crater" is the KPM instrument being applied where the doctrine says it must not be applied. **Identity, not defect, not over-correction — and the proof is that the survive+kill metric (the correct one) shows the caster winning.** The mirror to 3a holds: casters burst-clear trash (fast, capped by pacing-ceiling) and grind-but-win bosses (slow KPM, fine TTK, gated only on survive+kill). That asymmetric shape IS the caster identity the doctrine exists to honor (spine §10).

**One genuine open design item inside 3b (flag, do not block):** STR is the inverse — it *fails* the boss-gate (timeout=1.000, spine §5a) where the caster passes. That asymmetry is already RULED (STR ships via the clear-room floor, anchor-gap as texture, §5a). So the full archetype-vs-boss picture is coherent: caster wins boss on survive+kill, STR routes around boss via clear-competence. No new design hole opened by the composed data.

---

## 4. The single decision to put in front of Matt

> **"The composed instrument reproduced the encounter-measurement doctrine you adopted 2026-06-19 — from the composed path, in numbers. The per-economy bimodality gamora STOPPED on is not a new band-methodology problem; it is the doctrine's boss-gate being UNBUILT. Decision: wire the already-ruled boss-gate now (boss shells leave the KPM band onto survive-and-kill-within-the-enrage-timer), which fully resolves the boss-row spread with zero magnitude work; and defer the clear-room re-band behind the SPATIAL_DAMAGE_SCALE/mob-HP magnitude workstream, because the caster clear-room cells are timing-floor artifacts (600@0.3s) that no honest band can fit until magnitude is calibrated. Nothing new is invented; the doctrine you adopted is finished-building on the half that's unblocked, and the other half waits on a magnitude pass you already had scheduled."**

That is one decision with two clauses (boss-gate now / clear-band-after-magnitude), both of which Matt has already ruled the *principle* of. He is ratifying a sequencing, not opening a new design question.

---

## 5. Sequencing implication — is the workstream still on its spine?

**The workstream is ON ITS SPINE. It has NOT forked into "fix the band method first."** Three statements for knight-rider:

1. **No new band methodology is needed.** The methodology is the adopted doctrine. Fork 1 dissolves into "finish wiring §6 of the doctrine spine" — a known, ruled, UNBUILT engine task (re-route boss shells off KPM at both tiers onto sg2 survive+kill; DPS/TTK to telemetry). This is the gamora/rocket boss-gate build the spine §6 + RULINGS already named. It is the SAME work, not new work.
2. **The boss half is unblocked; the clear half blocks on magnitude.** The single deliberate band refit the whole workstream protected can land for the boss shells now (they leave the band — that IS the refit for those shells). The clear-shell band re-fit is the one piece that waits on fork 2's magnitude pass. The measure-isolated discipline HOLDS: we changed exactly one thing per layer, and the layer that's left (clear-room magnitude) is cleanly isolated and Matt-scheduled separately.
3. **gamora re-fires nothing yet.** Do NOT have gamora re-fire `--full` for a per-economy×per-shell OLD→NEW table — that would be building a band methodology I just ruled against. The next engine action is the doctrine's boss-gate build (spine §6), not a band re-fire. After the magnitude workstream lands, THEN the clear-room band re-measures (and only then is the per-economy-vs-single clear-room question answerable).

**The spine bent toward the doctrine; it did not break.** The composed instrument was honest, gamora was disciplined to STOP, and the STOP surfaced that the doctrine I authored is the answer arriving early. That is the workstream working.

---

**Signed:** gandalf, 2026-06-20. Three-fork ruling on the composed re-baseline DIAGNOSTIC STOP: fork 1 reframed (win-condition-aware per the adopted doctrine, NOT per-economy; boss shells leave the band, clear shells defer to fork 2); fork 2 leaves the workstream as magnitude but blocks only the clear-room re-band, not the boss-gate; fork 3 ruled identity-not-defect for both caster spike (fantasy, with the 600-cell as artifact to magnitude-tune) and caster crater (no crater — survive+kill shows the caster winning). One decision for Matt: wire the ruled boss-gate now, defer clear-band behind the scheduled magnitude pass. Workstream on its spine.
