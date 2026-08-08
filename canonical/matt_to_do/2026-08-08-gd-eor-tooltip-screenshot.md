# T14 — ONE screenshot: Eye of Reckoning tooltip (EoRWarlGuts character)

> **✓ SHORT-CIRCUITED 2026-08-08 — NO ACTION NEEDED (gandalf, KC2-SIM ledger L-22).** galadriel's
> sweep found the tooltip **inside the s2 video** (t ≈ 193–240, skill window open): **"Energy Cost:
> 176.4 per Second"** at Current Level 26 → per-tick reading (M2) confirmed, decomposed exactly
> (16.0 × 12.25 ticks/s × 0.90). The drain spec row is CLOSED (spec § 3.1); this screenshot is no
> longer needed. Row retained as record only.

**Parked:** 2026-08-08 (gandalf, KC2-SIM G-A close, ledger L-6 step (b)). ~~**Non-blocking.**~~ **RESOLVED-BY-FOOTAGE.**

## Action (~2 minutes, GD PC)

1. Launch Grim Dawn with the **EoRWarlGuts** Warlord.
2. Open the skill window (default `S`) → hover **Eye of Reckoning** (Oathkeeper mastery bar).
3. Screenshot with the tooltip fully visible — the **Energy Cost** line is the payload.
4. Drop it anywhere under `/Volumes/reincarnated/visual-artifacts/GD-matt-test/` with `eor-tooltip` in the filename.

No Crucible entry needed — the skill-window tooltip is state-independent. Playing this character is safe for our purposes: the run-end save is already copied + SHA-verified (`b8e6f510…`).

## What the number decodes

The DB record carries `skillManaCost = 16.0` at rank 26, but the **unit** is undecidable from the DB alone (P-E1, gap):

| Tooltip reads | Meaning |
|---|---|
| **≈ 16** energy/second | drain is **per-second** |
| **≈ 100** energy/second | the DB's 16.0 is **per-tick** (6.25 ticks/s at 100% Attack Speed) |

One number, 6.25× apart — unmissable.

## What it unblocks

The **last open constant in the EoR channel machine** for the KC2-SIM battle-sim spec. With it, the drain spec row sheds its declared dual-bound and the v1 energy micro-oracle binds on drain *rate*, not just ceiling/reserve (≈982 reserved ~~by Divine Mandate~~ *— CORRIGENDUM 2026-08-08 (gandalf, KC2-SIM L-41(c)): attribution error — Divine Mandate reserves ZERO (`characterManaLimitReserve = 0.0`); the 982 total's closing component is **Presence of Might (component skill), 300 flat** (spec § 3.2); beat-2 positive control: 982 − 300 = 682*). Without it the run still proceeds — dual-bound fallback pre-registered (ledger L-6), and **galadriel is sweeping existing footage for a tooltip frame that may short-circuit this row.**

**Source:** `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` § A.4 + L-6; `agentic_orchestration/legolas/notes/2026-08-07-pe1-eor-spin-parameters.md`.
