#!/usr/bin/env python3
"""
WR3-KITE-COMMIT / R-WR3-12(8.6) — BOSS DUTY-CYCLE PRE-BUILD MEASUREMENT. READ-ONLY.

Answers the pre-build gate gandalf's stage-1 mechanism spec §8.6 opened: C2's `T_lock`
(WINDUP_S + RECOVERY_S) was chosen without knowing the boss's REALIZED inter-swing interval.
This instrument measures that interval over the FROZEN battery of record and projects the
implied movement-lock duty cycle at T_lock in {0.40, 0.60, 0.90} s.

NO simulation runs. NO writes under src/. Lives in the gamora notes support dir per the
F-WR2-5 / wr1_envelope_spec_support battery-instrument precedent. Instruments in notes are
instruments, not production code.

────────────────────────────────────────────────────────────────────────────────────────────
§0. IDENTITY ASSERTION OF THE FROZEN ROOT (wr2 cell precedent — assert before reading)

  I0  leg-dir name set == the three banked WR2-AFTER leg names, and each carries 150 traces
      (5 cells x 30 seeds), 450 total.
  I1  SHA-256 manifest: per-leg rolled digest over the sorted (basename, sha256) pairs of the
      60 BOSS traces, plus an all-leg roll. Printed, not asserted against a stored value —
      the assertion is that the digest is STABLE and reported, so any later re-read of this
      note can detect a moved root.
  V1  watch-seed footer: pre / boss/B / seed 74000802 -> elapsed_s == 37.0
  V2  pre-leg elapsed_s means: boss/A == 32.04, boss/B == 48.92 (battery-of-record §4.2)
  V4  nova firings: 132 total across the battery (44 per leg), attack_id containing ":nova:"

  If any of V1/V2/V4 or I0 fails the instrument ABORTS. No measurement is emitted on a dirty
  root. (V3 — the S-1 separation predicate — is NOT re-run here: it is a geometry gate, not a
  cadence gate, and F-WR2-5 already banked it clean over these same 450 traces.)

────────────────────────────────────────────────────────────────────────────────────────────
§1. JOIN FACTS (inherited from Cell BAT WARN-4 / F-WR2-5 §1)

  - `header` carries `entities[]` with `entity_id`, `is_player`, `entity_radius_m`,
    `movement_speed_ms`, `skills[]`. `is_boss` is FALSE on every entity — the boss join must
    go through the g5 header.
  - `g5_header.g5.opposition_roster[]` — the BOSS is the entry with `tier == "boss"`, joined
    to an entity_id by `entity_id.startswith(record.replace("/", "_"))`.
  - `tick` records carry per-entity `skill_cooldowns[]`, `commit_state`, position, `alive`.
  - damage resolutions: `record_type: "event"`, `event: "damage"`, with `source_id`,
    `target_id`, `skill_idx`, `geometry`, `amount`, `delivered`.
  - telegraph events: `event: "telegraph"`, `attack_id`, `attacker_id`, `wind_up_s`, `shape`.
    DEDUPED BY attack_id at the sink (replica_frame_emitter.py:416-419) — one telegraph per
    (attacker, skill) per fight, NOT one per swing. So telegraphs count DISTINCT ATTACKS, not
    firings, and cannot be used as a swing counter.

────────────────────────────────────────────────────────────────────────────────────────────
§2. WHAT COUNTS AS A BOSS SWING

  The fixture boss (`boss&quest/slith_wightmirecave01`, "Primordian, the Forgotten One")
  carries exactly two skills:
    idx 0  `slith_wightmirecave01_attack`   geometry point,  range 2.0 m   <- THE BASIC SWING
    idx 1  `primordian_frigidring_r4`       geometry circle, range 10.0 m  <- THE M-2 NOVA

  BASIC SWING RESOLUTION := damage event with source_id == boss_id AND geometry == "point".
      (skill_idx == 0 on this route; asserted, not assumed.)
  NOVA RESOLUTION := damage event with source_id == boss_id AND geometry == "circle".
      The nova resolves at an analytic ring crossing with skill_idx == -1 (the cast seam
      applies no damage on the cast tick), so it is separable from the swing by BOTH fields.

  WHIFFS DO NOT EXIST IN THE BEFORE BUILD. `_select_skill_for_entity` gates the melee on
  `nearest_dist <= range_m + target.entity_radius` (spatial_engine:2645 under bsep-v2, ON in
  every leg name), so an out-of-range boss does not select the skill and pays no cooldown.
  A selected point-geometry melee always produces exactly one hit. Therefore, in the frozen
  traces, DAMAGE-RESOLUTION COUNT == SWING COUNT. This is cross-checked mechanically below
  against the rising edges of `skill_cooldowns[0]`, which is set only at the attack site
  (spatial_engine:6294) — if the two counts disagree, a swing-without-damage channel exists
  and the identity above is false.

────────────────────────────────────────────────────────────────────────────────────────────
§3. THE TWO CADENCE QUANTITIES, AND WHY BOTH ARE REPORTED

  (a) I_realized — WALL-CLOCK strike-to-strike, t_s of consecutive basic-swing resolutions.
      Includes tick quantization (dt = 0.1 s), pursuit delay, and NOVA GATING: the nova
      shares `mob.action_available_at` with the melee (spatial_engine:5965 gate, :6294 tail),
      so a nova cast blackholes the melee for its own 6.0 s cooldown.

  (b) C_drawn — the GOVERNED free interval: `cooldown_seconds + U(gd_swing_pause)`, the exact
      quantity spec §3.4 says C2 does not change. Recovered EXACTLY from the trace, not
      modelled: at the swing tick the emitted `skill_cooldowns[0]` is the drawn value less one
      dt decay, so
              C_drawn = skill_cooldowns[0](swing tick) + tick_size_s
      Validated against the closed form the fixture composes:
              base   = T_base(1.0) / (rate_pct/100) = 1/0.90 = 1.111111 s
              pause  = U(BOSS_SWING_PAUSE_S) = U(0.30, 0.40)
              C_drawn in [1.411111, 1.511111]
      Any recovered value outside that band aborts the run — it would mean the recovery
      arithmetic (the one-dt offset) is wrong and every derived number with it.

      DEAD-ON-THE-SWING-TICK CARVE-OUT — found empirically, then explained mechanically rather
      than patched. The decay loop (spatial_engine:6467-6471) SKIPS any entity with
      `not e.is_alive`. The tick order is: player phase -> mob attack phase (the boss swings and
      arms its cooldown) -> ally-proxy realized-fight phase -> decay -> frame emit. So on the
      handful of ticks where an ally-proxy kills the boss AFTER the boss has already swung in
      that same tick, the decay is skipped for the boss and the emitted value IS the drawn value
      with no offset. The trace states this directly: those tick records carry the boss with
      `alive: false, hp: 0.0` and a `skill_cooldowns[0]` that lands inside the closed-form band
      with NO offset, while every alive-at-emit swing lands inside it WITH the offset. The rule
      is therefore mechanical, not heuristic:
              C_drawn = cd0[t] + tick_size   if boss alive in tick t's record
              C_drawn = cd0[t]               if boss dead   in tick t's record
      Both branches are band-checked. The split itself is the confirmation that the offset rule
      is right: 6 of 4432 recovered swings take the dead branch and all 6 are the fight's last
      swing on a player win.

  Each interval is classified:
      nova_gated     — a boss nova resolution or cast falls inside (t_i, t_{i+1}]
      pursuit_gapped — I_realized > C_drawn_i + dt + eps and not nova_gated (boss out of range
                       when the gate opened; it had to close before it could swing)
      clean          — neither: the boss was in reach the moment its cooldown expired

────────────────────────────────────────────────────────────────────────────────────────────
§4. THE DUTY-CYCLE MAP — DEFINITION, AND THE ASSUMPTION IT RIDES ON

  The frozen traces have NO LOCK: a swing resolves on the tick it fires and the boss's
  navigation phase consults no attack state. So the ENTIRE measured interval is FREE
  (unlocked) time. Post-C2 the boss is locked for T_lock = WINDUP_S + RECOVERY_S around each
  strike. Mapping the measured cadence onto the post-C2 cycle requires one choice the spec
  does not make — WHERE THE COOLDOWN CLOCK IS SET relative to windup entry — so BOTH readings
  are reported and named:

  M-ADD (spec-literal; PRIMARY). §3.4: "C2 changes no attack cadence: the free time between
      swings remains governed by the existing cooldown_seconds + the seeded gd_swing_pause
      draw." Free time is preserved; the lock is inserted ON TOP of it.
          cycle_after = I_free + T_lock                 (I_free := the measured interval)
          duty_ADD    = T_lock / (I_free + T_lock)      <- the commission's formula, verbatim

  M-ABS (cooldown-absorbing; ALTERNATIVE, upper bound on duty). The existing engine sets the
      cooldown AT the attack site (spatial_engine:6293-6294). If windup entry IS that site,
      the lock runs concurrently with the cooldown and the cycle does not lengthen.
          cycle_after = max(I_free, T_lock) = I_free    (I_free >> T_lock throughout)
          duty_ABS    = T_lock / I_free

  L_fight — FIGHT-LEVEL LOCKED FRACTION, the number that actually answers "what fraction of
      the fight is the boss movement-locked":
          L_fight(T_lock) = n_swings * T_lock / elapsed_s
      This is NOT duty: duty is measured over the attack cycle, L_fight over the whole fight,
      and they differ by exactly the fraction of the fight the boss spends not attacking at
      all (approach, pursuit, the 6.0 s nova blackhole). L_fight is the degeneracy test.

  NAMED ASSUMPTIONS (all four are load-bearing; none is hidden):
    A1 FROZEN-CADENCE. The projection holds the measured cadence and the measured fight
       length FIXED. Post-build, with K armed and C2-L1 whiffing live, the realized cadence
       and the fight length both move. This is a PRE-BUILD SANITY ENVELOPE, not a prediction
       of the post-build state.
    A2 IN-RANGE-ONLY LOCK. The boss enters windup only when the target is already in reach
       (spec §3.2 enter condition). Pursuit time is unlocked. Hence L_fight is built from
       REALIZED swing counts, not from extrapolated cycle counts.
    A3 NOVA SHARES THE ACTION GATE. Confirmed by read, not assumed. The spec scopes C2 to
       "the boss melee skill" packet and is silent on whether the nova cast also commits, so
       every statistic is reported BOTH pooled and nova-free.
    A4 TICK QUANTIZATION. dt = 0.1 s. T_lock is realized at tick granularity: 0.40 = 4 ticks,
       0.60 = 6, 0.90 = 9. The spec's §3.4 floor T_lock >= 0.387 s therefore realizes as
       >= 0.4 s, and 0.40 clears the floor by ONE HUNDREDTH of a tick.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict
from typing import Any, Optional

BAT = os.path.expanduser(
    "~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after"
)
LEGS = {
    "pre": "g5_m4cadence_nova_mitR2proxy_tg_dec_bsep_mv2_ntv2",
    "post": "g5_r3arm_m4cadence_nova_mitR3_tg_dec_bsep_mv2_ntv2",
    "pre_endpoint": "g5_m4cadence_nova_mitR2proxyresistslow_tg_dec_bsep_mv2_ntv2",
}
WATCH_SEED = 74000802
TICK_S = 0.1
EPS = 1e-9

# Closed form of the fixture boss cadence (kitcal_g5_scenarios.py:129 + gd_attack_speed.py:159).
CAD_BASE_S = 1.0 / 0.90                      # T_base 1.0 / clamped rate 90%
PAUSE_LO, PAUSE_HI = 0.30, 0.40              # BOSS_SWING_PAUSE_S, M — Primordian, measured
CAD_LO, CAD_HI = CAD_BASE_S + PAUSE_LO, CAD_BASE_S + PAUSE_HI

T_LOCKS = [0.40, 0.60, 0.90]
FLOOR_T_LOCK_S = 0.387                       # spec §3.4: 5.75*(T_lock-0.30) >= 0.5 m
PLAYER_SPEED_MS = 5.75
REACTION_LATENCY_S = 0.30
DAYLIGHT_MIN_M = 0.5
DEGENERATE_DUTY = 0.50


# ────────────────────────────────────────────────────────────────────────── loading

def load_trace(path: str) -> dict[str, Any]:
    header = g5h = footer = None
    ticks: list[dict] = []
    events: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rt = rec.get("record_type")
            if rt == "header":
                header = rec
            elif rt == "g5_header":
                g5h = rec
            elif rt == "tick":
                ticks.append(rec)
            elif rt == "event":
                events.append(rec)
            elif rt == "footer":
                footer = rec
    return {"path": path, "basename": os.path.basename(path), "header": header,
            "g5_header": g5h, "footer": footer, "ticks": ticks, "events": events}


def boss_id_of(tr: dict) -> Optional[str]:
    hdr = tr["header"]
    ids = {e["entity_id"] for e in hdr["entities"]}
    roster = (tr["g5_header"] or {}).get("g5", {}).get("opposition_roster", [])
    for r in roster:
        if r.get("tier") != "boss":
            continue
        prefix = r["record"].replace("/", "_")
        cands = sorted(eid for eid in ids if eid.startswith(prefix))
        if len(cands) == 1:
            return cands[0]
    return None


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ────────────────────────────────────────────────────────────────────── per-fight

def measure_fight(tr: dict, bid: str) -> dict[str, Any]:
    """All per-fight cadence measures. Raises on any structural surprise."""
    hdr = tr["header"]
    tick_s = float(hdr.get("tick_size_s", TICK_S))
    elapsed = float((tr["footer"] or {}).get("elapsed_s", 0.0))

    # boss skill table, asserted
    bent = [e for e in hdr["entities"] if e["entity_id"] == bid][0]
    skills = {int(s["skill_idx"]): s for s in bent.get("skills", [])}
    if skills.get(0, {}).get("geometry") != "point":
        raise ValueError(f"{tr['basename']}: boss skill 0 is not point geometry: {skills.get(0)}")

    swings: list[dict] = []       # basic-swing resolutions
    novas: list[dict] = []        # nova resolutions
    other: list[dict] = []
    for ev in tr["events"]:
        if ev.get("event") != "damage" or ev.get("source_id") != bid:
            continue
        geo = ev.get("geometry")
        if geo == "point":
            if int(ev.get("skill_idx", -99)) != 0:
                raise ValueError(f"{tr['basename']}: point damage with skill_idx "
                                 f"{ev.get('skill_idx')} — swing identity broken")
            swings.append(ev)
        elif geo == "circle":
            novas.append(ev)
        else:
            other.append(ev)

    nova_casts = [ev for ev in tr["events"]
                  if ev.get("event") == "telegraph" and ev.get("attacker_id") == bid
                  and ":nova:" in str(ev.get("attack_id", ""))]

    # de-dupe swings by tick (point geometry hits exactly one target, so this should be a no-op)
    by_tick: dict[int, dict] = {}
    for ev in swings:
        by_tick.setdefault(int(ev["tick"]), ev)
    if len(by_tick) != len(swings):
        raise ValueError(f"{tr['basename']}: {len(swings)} point-damage events collapse to "
                         f"{len(by_tick)} ticks — a swing hit more than one target")
    swing_ticks = sorted(by_tick)

    # ── mechanical cross-check: swing count vs rising edges of boss skill_cooldowns[0] ──
    cd0: dict[int, float] = {}
    boss_alive_at: dict[int, bool] = {}
    for rec in tr["ticks"]:
        for e in rec.get("entities", ()):
            if e.get("entity_id") == bid:
                cds = e.get("skill_cooldowns") or []
                if cds:
                    cd0[int(rec["tick"])] = float(cds[0])
                boss_alive_at[int(rec["tick"])] = bool(e.get("alive"))
                break
    edges = []
    prev_t = None
    for t in sorted(cd0):
        v = cd0[t]
        pv = cd0.get(prev_t, 0.0) if prev_t is not None else 0.0
        # a rising edge is any tick whose cooldown EXCEEDS the previous tick's (decay is
        # monotone-down at exactly dt per tick, so a rise can only be a re-arm at the attack site)
        if prev_t is not None and v > pv + EPS:
            edges.append(t)
        elif prev_t is None and v > EPS:
            edges.append(t)
        prev_t = t

    # ── NOVA OCCUPANCY of the SHARED action gate (A3). The nova telegraph is deduped at the
    # sink and is NOT emitted at all on a no-crossing fire, so it cannot count casts. The
    # cast is instead read off the rising edge of the boss's OWN skill_cooldowns[1], which is
    # written only at the attack site (spatial_engine:6293).
    cd1: dict[int, float] = {}
    for rec in tr["ticks"]:
        for e in rec.get("entities", ()):
            if e.get("entity_id") == bid:
                cds = e.get("skill_cooldowns") or []
                if len(cds) > 1:
                    cd1[int(rec["tick"])] = float(cds[1])
                break
    nova_cast_ticks = []
    _prev = None
    for t in sorted(cd1):
        v = cd1[t]
        if (_prev is None and v > EPS) or (_prev is not None and v > cd1[_prev] + EPS):
            nova_cast_ticks.append(t)
        _prev = t

    # ── C_drawn recovery, per swing (§3(b), incl. the dead-on-the-swing-tick carve-out) ──
    drawn: list[Optional[float]] = []
    terminal_flags: list[bool] = []
    for t in swing_ticks:
        if t not in cd0:
            drawn.append(None)
            terminal_flags.append(False)
            continue
        dead_at_emit = not boss_alive_at.get(t, True)
        terminal_flags.append(dead_at_emit)
        drawn.append(cd0[t] if dead_at_emit else cd0[t] + tick_s)

    # ── intervals ──
    nova_marks = sorted({float(ev["t_s"]) for ev in novas}
                        | {float(ev["t_s"]) for ev in nova_casts})
    intervals = []
    for i in range(len(swing_ticks) - 1):
        t0 = float(by_tick[swing_ticks[i]]["t_s"])
        t1 = float(by_tick[swing_ticks[i + 1]]["t_s"])
        dt = t1 - t0
        c = drawn[i]
        nova_in = any(t0 + EPS < m <= t1 + EPS for m in nova_marks)
        gapped = (c is not None) and (dt > c + tick_s + 1e-6) and not nova_in
        intervals.append({
            "t0": t0, "t1": t1, "dt": dt, "c_drawn": c,
            "class": "nova_gated" if nova_in else ("pursuit_gapped" if gapped else "clean"),
        })

    return {
        "basename": tr["basename"],
        "cell": hdr.get("cell"),
        "seed": hdr.get("seed"),
        "elapsed_s": elapsed,
        "tick_size_s": tick_s,
        "winner": (tr["footer"] or {}).get("winner"),
        "n_swings": len(swing_ticks),
        "n_nova_resolutions": len(novas),
        "n_nova_telegraphs": len(nova_casts),
        "n_nova_casts": len(nova_cast_ticks),
        "nova_cast_t_s": [t * tick_s for t in nova_cast_ticks],
        "first_swing_t_s": (swing_ticks[0] * tick_s if swing_ticks else None),
        "last_swing_t_s": (swing_ticks[-1] * tick_s if swing_ticks else None),
        "n_other_boss_damage": len(other),
        "n_cd0_rising_edges": len(edges),
        "swing_ticks": swing_ticks,
        "c_drawn": drawn,
        "c_drawn_terminal": terminal_flags,
        "n_terminal_swings": sum(terminal_flags),
        "intervals": intervals,
    }


# ───────────────────────────────────────────────────────────────────────── stats

def q(xs: list[float], p: float) -> float:
    """Linear-interpolation quantile, explicit so the number is reproducible."""
    if not xs:
        return float("nan")
    s = sorted(xs)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return s[lo] if lo == hi else s[lo] + (s[hi] - s[lo]) * (k - lo)


def summarize(xs: list[float]) -> dict[str, Any]:
    if not xs:
        return {"n": 0}
    return {
        "n": len(xs),
        "min": min(xs), "p25": q(xs, 0.25), "median": q(xs, 0.50),
        "p75": q(xs, 0.75), "max": max(xs),
        "mean": statistics.fmean(xs),
        "stdev": (statistics.pstdev(xs) if len(xs) > 1 else 0.0),
    }


def duty_block(i_free: float, t_lock: float) -> dict[str, float]:
    return {
        "T_lock_s": t_lock,
        "I_free_s": i_free,
        "duty_ADD": t_lock / (i_free + t_lock),
        "duty_ABS": t_lock / i_free,
    }


# ────────────────────────────────────────────────────────────────────────── main

def main() -> int:
    out: dict[str, Any] = {"instrument": "wr3_duty_cycle.py",
                           "run": "WR3-KITE-COMMIT / R-WR3-12(8.6)",
                           "root": BAT, "read_only": True}

    # ══ I0 : root shape ══
    if not os.path.isdir(BAT):
        print(f"ABORT I0: root missing {BAT}", file=sys.stderr)
        return 2
    found = sorted(d for d in os.listdir(BAT) if os.path.isdir(os.path.join(BAT, d)))
    expect = sorted(LEGS.values())
    i0 = {"legs_found": found, "legs_expected": expect, "pass": found == expect,
          "trace_counts": {}, "boss_trace_counts": {}}
    for leg, d in LEGS.items():
        tdir = os.path.join(BAT, d, "traces")
        all_t = sorted(f for f in os.listdir(tdir) if f.endswith(".jsonl"))
        boss_t = [f for f in all_t if f.startswith("boss__")]
        i0["trace_counts"][leg] = len(all_t)
        i0["boss_trace_counts"][leg] = len(boss_t)
        if len(all_t) != 150 or len(boss_t) != 60:
            i0["pass"] = False
    out["I0_root_shape"] = i0
    if not i0["pass"]:
        print(f"ABORT I0: {json.dumps(i0)}", file=sys.stderr)
        return 2

    # ══ I1 : SHA-256 manifest over the 180 boss traces ══
    i1 = {"per_leg": {}, "note": "rolled digest over sorted (basename, sha256) of BOSS traces"}
    roll_all = hashlib.sha256()
    for leg in sorted(LEGS):
        tdir = os.path.join(BAT, LEGS[leg], "traces")
        roll = hashlib.sha256()
        n = 0
        for f in sorted(os.listdir(tdir)):
            if not (f.startswith("boss__") and f.endswith(".jsonl")):
                continue
            digest = sha256_of(os.path.join(tdir, f))
            roll.update(f.encode()); roll.update(digest.encode())
            roll_all.update(LEGS[leg].encode()); roll_all.update(f.encode())
            roll_all.update(digest.encode())
            n += 1
        i1["per_leg"][leg] = {"n_boss_traces": n, "sha256_roll": roll.hexdigest()}
    i1["sha256_roll_all_boss"] = roll_all.hexdigest()
    out["I1_identity_manifest"] = i1

    # ══ load + measure ══
    fights: list[dict] = []
    boss_in_nonboss_cells: list[str] = []
    watch_elapsed = None
    elapsed_by: dict[tuple, list[float]] = defaultdict(list)
    nova_firings_by_leg: Counter = Counter()

    for leg in sorted(LEGS):
        tdir = os.path.join(BAT, LEGS[leg], "traces")
        for f in sorted(os.listdir(tdir)):
            if not f.endswith(".jsonl"):
                continue
            tr = load_trace(os.path.join(tdir, f))
            bid = boss_id_of(tr)

            # V4 nova firings (whole battery, all cells)
            nova_firings_by_leg[leg] += sum(
                1 for ev in tr["events"]
                if ev.get("event") == "telegraph" and ":nova:" in str(ev.get("attack_id", ""))
            )
            cell = (tr["header"] or {}).get("cell")
            ft = tr["footer"] or {}
            if ft.get("elapsed_s") is not None:
                elapsed_by[(leg, cell)].append(float(ft["elapsed_s"]))
            if leg == "pre" and cell == "boss/B" and int(tr["header"]["seed"]) == WATCH_SEED:
                watch_elapsed = float(ft.get("elapsed_s"))

            if bid is None:
                continue
            if not f.startswith("boss__"):
                boss_in_nonboss_cells.append(f"{leg}/{f}")
            m = measure_fight(tr, bid)
            m["leg"] = leg
            fights.append(m)

    # ══ V1 / V2 / V4 ══
    v1 = {"expected": 37.0, "observed": watch_elapsed,
          "pass": watch_elapsed is not None and abs(watch_elapsed - 37.0) < 1e-6}
    v2 = {}
    for cell, exp in (("boss/A", 32.04), ("boss/B", 48.92)):
        vals = elapsed_by[("pre", cell)]
        mean = statistics.fmean(vals) if vals else float("nan")
        v2[cell] = {"n": len(vals), "expected": exp, "observed_mean": mean,
                    "pass": abs(mean - exp) < 5e-3}
    v4 = {"per_leg": dict(nova_firings_by_leg), "total": sum(nova_firings_by_leg.values()),
          "pass": (sum(nova_firings_by_leg.values()) == 132
                   and all(v == 44 for v in nova_firings_by_leg.values()))}
    out["V1_watch_seed_footer"] = v1
    out["V2_pre_leg_elapsed_means"] = v2
    out["V4_nova_firings"] = v4
    out["boss_entity_outside_boss_cells"] = boss_in_nonboss_cells
    if not (v1["pass"] and all(x["pass"] for x in v2.values()) and v4["pass"]):
        print("ABORT: identity gates failed\n" + json.dumps(
            {"V1": v1, "V2": v2, "V4": v4}, indent=2), file=sys.stderr)
        return 3

    # ══ C_drawn band validation (the recovery arithmetic's own falsifier) ══
    all_drawn = [c for m in fights for c in m["c_drawn"] if c is not None]
    band_viol = [c for c in all_drawn if not (CAD_LO - 1e-6 <= c <= CAD_HI + 1e-6)]
    out["V5_c_drawn_band"] = {
        "closed_form_band_s": [CAD_LO, CAD_HI],
        "n": len(all_drawn), "n_violations": len(band_viol),
        "worst": (max(band_viol, key=lambda c: min(abs(c - CAD_LO), abs(c - CAD_HI)))
                  if band_viol else None),
        "summary": summarize(all_drawn),
        "n_terminal_swings": sum(m["n_terminal_swings"] for m in fights),
        "terminal_fights": [{"leg": m["leg"], "f": m["basename"], "winner": m["winner"],
                             "elapsed_s": m["elapsed_s"]}
                            for m in fights if m["n_terminal_swings"]],
        "pass": not band_viol,
    }
    if band_viol:
        print("ABORT V5: C_drawn recovery out of closed-form band", file=sys.stderr)
        return 4

    # ══ swing-count identity: damage resolutions vs cooldown rising edges ══
    mism = [{"f": m["basename"], "leg": m["leg"], "swings": m["n_swings"],
             "edges": m["n_cd0_rising_edges"]}
            for m in fights if m["n_swings"] != m["n_cd0_rising_edges"]]
    out["V6_swing_identity"] = {
        "n_fights": len(fights),
        "n_mismatched": len(mism),
        "mismatches": mism[:20],
        "claim": "damage-resolution count == swing count (no whiff channel in the BEFORE build)",
        "pass": not mism,
    }

    # ══ §1 per-fight swing counts ══
    per_fight_rows = []
    for m in fights:
        ivs = m["intervals"]
        clean = [x["dt"] for x in ivs if x["class"] == "clean"]
        per_fight_rows.append({
            "leg": m["leg"], "cell": m["cell"], "seed": m["seed"],
            "elapsed_s": m["elapsed_s"], "winner": m["winner"],
            "n_swings": m["n_swings"], "n_nova": m["n_nova_resolutions"],
            "n_nova_casts": m["n_nova_casts"],
            "swings_per_min": (60.0 * m["n_swings"] / m["elapsed_s"]) if m["elapsed_s"] else None,
            "median_interval_s": (q([x["dt"] for x in ivs], 0.5) if ivs else None),
            "median_clean_interval_s": (q(clean, 0.5) if clean else None),
        })
    out["per_fight"] = per_fight_rows

    def _grouped(key):
        g = defaultdict(list)
        for r in per_fight_rows:
            g[r[key]].append(r)
        return g

    out["swing_counts"] = {
        "pooled": summarize([r["n_swings"] for r in per_fight_rows]),
        "by_leg": {k: summarize([r["n_swings"] for r in v])
                   for k, v in _grouped("leg").items()},
        "by_cell": {k: summarize([r["n_swings"] for r in v])
                    for k, v in _grouped("cell").items()},
        "zero_swing_fights": sum(1 for r in per_fight_rows if r["n_swings"] == 0),
        "total_swings": sum(r["n_swings"] for r in per_fight_rows),
        "total_nova_resolutions": sum(r["n_nova"] for r in per_fight_rows),
    }

    # ══ §2 interval distributions ══
    all_iv = [x for m in fights for x in m["intervals"]]
    by_class = defaultdict(list)
    for x in all_iv:
        by_class[x["class"]].append(x["dt"])
    iv_leg = defaultdict(list)
    iv_cell = defaultdict(list)
    for m in fights:
        for x in m["intervals"]:
            iv_leg[m["leg"]].append(x["dt"])
            iv_cell[m["cell"]].append(x["dt"])

    out["intervals"] = {
        "pooled_all": summarize([x["dt"] for x in all_iv]),
        "pooled_by_class": {k: summarize(v) for k, v in sorted(by_class.items())},
        "class_counts": {k: len(v) for k, v in sorted(by_class.items())},
        "by_leg": {k: summarize(v) for k, v in sorted(iv_leg.items())},
        "by_cell": {k: summarize(v) for k, v in sorted(iv_cell.items())},
        "value_histogram_all": dict(sorted(Counter(round(x["dt"], 2) for x in all_iv).items())),
        "value_histogram_clean": dict(sorted(Counter(round(v, 2) for v in by_class["clean"]).items())),
        "c_drawn_governed_free_interval": summarize(all_drawn),
        "per_fight_median_of_medians": summarize(
            [r["median_interval_s"] for r in per_fight_rows if r["median_interval_s"] is not None]),
        "per_fight_median_of_clean_medians": summarize(
            [r["median_clean_interval_s"] for r in per_fight_rows
             if r["median_clean_interval_s"] is not None]),
    }

    # ══ §3 duty cycle ══
    med_all = out["intervals"]["pooled_all"]["median"]
    med_clean = out["intervals"]["pooled_by_class"]["clean"]["median"]
    med_drawn = out["intervals"]["c_drawn_governed_free_interval"]["median"]
    anchors = {"realized_median_all": med_all,
               "realized_median_clean": med_clean,
               "governed_C_drawn_median": med_drawn}

    duty = {"definition": {
        "duty_ADD": "T_lock / (I_free + T_lock)  — spec §3.4-literal; lock ADDED to a preserved free interval",
        "duty_ABS": "T_lock / I_free             — cooldown-absorbing; lock runs inside the existing interval",
        "L_fight": "n_swings * T_lock / elapsed_s — fraction of the WHOLE fight the boss is movement-locked",
        "assumptions": ["A1 frozen-cadence", "A2 in-range-only lock",
                        "A3 nova shares the action gate", "A4 tick quantization dt=0.1"],
    }, "anchors_s": anchors, "by_T_lock": {}}

    for tl in T_LOCKS:
        blk = {"T_lock_s": tl,
               "clears_spec_floor_0.387": tl >= FLOOR_T_LOCK_S,
               "floor_margin_s": tl - FLOOR_T_LOCK_S,
               "daylight_m": PLAYER_SPEED_MS * max(0.0, tl - REACTION_LATENCY_S),
               "daylight_vs_min_0.5m": PLAYER_SPEED_MS * max(0.0, tl - REACTION_LATENCY_S) - DAYLIGHT_MIN_M,
               "ticks": round(tl / TICK_S, 3),
               "on_anchor": {k: duty_block(v, tl) for k, v in anchors.items()}}
        lf = [(r["n_swings"] * tl / r["elapsed_s"]) for r in per_fight_rows if r["elapsed_s"]]
        blk["L_fight"] = summarize(lf)
        blk["L_fight_by_cell"] = {
            k: summarize([(r["n_swings"] * tl / r["elapsed_s"]) for r in v if r["elapsed_s"]])
            for k, v in _grouped("cell").items()}
        blk["degenerate_flags"] = {
            "duty_ADD_over_50pct_on_realized_median":
                duty_block(med_all, tl)["duty_ADD"] > DEGENERATE_DUTY,
            "duty_ABS_over_50pct_on_realized_median":
                duty_block(med_all, tl)["duty_ABS"] > DEGENERATE_DUTY,
            "L_fight_median_over_50pct": blk["L_fight"]["median"] > DEGENERATE_DUTY,
            "below_spec_floor": tl < FLOOR_T_LOCK_S,
        }
        duty["by_T_lock"][f"{tl:.2f}"] = blk

    # the full pre-registered fallback bracket, on the primary anchor
    bracket = {}
    for w in (0.25, 0.35, 0.50):
        for r_ in (0.15, 0.25, 0.40):
            tl = round(w + r_, 10)
            d = duty_block(med_all, tl)
            dl = PLAYER_SPEED_MS * max(0.0, tl - REACTION_LATENCY_S)
            lf = statistics.fmean([(x["n_swings"] * tl / x["elapsed_s"])
                                   for x in per_fight_rows if x["elapsed_s"]])
            bracket[f"W{w:.2f}xR{r_:.2f}"] = {
                "T_lock_s": tl, "clears_floor": tl >= FLOOR_T_LOCK_S,
                "daylight_m": dl, "daylight_ok": dl >= DAYLIGHT_MIN_M,
                "duty_ADD": d["duty_ADD"], "duty_ABS": d["duty_ABS"],
                "L_fight_mean": lf,
                "ticks_windup": round(w / TICK_S, 3), "ticks_recovery": round(r_ / TICK_S, 3),
            }
    duty["fallback_bracket_on_realized_median"] = bracket
    out["duty_cycle"] = duty

    # ══ nova occupancy of the shared action gate (A3) ══
    novacast_t = [t for m in fights for t in m["nova_cast_t_s"]]
    out["nova_occupancy"] = {
        "claim": "the nova occupies the SAME mob action gate as the melee "
                 "(spatial_engine:5965 gate, :6294 tail), so a cast blackholes the swing for "
                 "its own 6.0 s cooldown. Measured here to establish WHERE that blackhole "
                 "lands relative to the swing train.",
        "n_fights": len(fights),
        "fights_with_a_nova_cast": sum(1 for m in fights if m["n_nova_casts"]),
        "nova_casts_per_fight": dict(sorted(Counter(m["n_nova_casts"] for m in fights).items())),
        "nova_cast_t_s": summarize(novacast_t),
        "nova_resolutions_total": sum(m["n_nova_resolutions"] for m in fights),
        "nova_telegraph_events_total": sum(m["n_nova_telegraphs"] for m in fights),
        "first_swing_t_s": summarize([m["first_swing_t_s"] for m in fights
                                      if m["first_swing_t_s"] is not None]),
        "n_intervals_spanning_a_nova": sum(
            1 for m in fights for x in m["intervals"] if x["class"] == "nova_gated"),
        "reading": "one cast per fight, at fight open, BEFORE the first basic swing — so the "
                   "6.0 s nova blackhole never appears inside the inter-swing distribution.",
    }

    # ══ engagement decomposition — why L_fight < duty ══
    out["engagement"] = {
        "elapsed_s": summarize([m["elapsed_s"] for m in fights]),
        "approach_fraction": summarize([m["first_swing_t_s"] / m["elapsed_s"] for m in fights
                                        if m["first_swing_t_s"] is not None and m["elapsed_s"]]),
        "swing_span_fraction": summarize(
            [(m["last_swing_t_s"] - m["first_swing_t_s"]) / m["elapsed_s"] for m in fights
             if m["first_swing_t_s"] is not None and m["elapsed_s"]]),
        "attack_active_fraction": summarize(
            [m["n_swings"] * med_all / m["elapsed_s"] for m in fights if m["elapsed_s"]]),
        "note": "duty is measured over the ATTACK CYCLE; L_fight over the WHOLE fight. They "
                "differ by exactly the attack_active_fraction, which is < 1 because of the "
                "opening approach + the one-shot nova blackhole.",
    }

    # ══ engine-side cross-check the conductor should see ══
    out["telegraph_windup_crosscheck"] = {
        "TELEGRAPH_WIND_UP_DEFAULTS_S_point": 0.5,
        "source": "spatial_engine.py:223-228 ('point: 0.5 — degenerate nearest-1 marker: "
                  "reaction-margin floor tell')",
        "observed_boss_basic_telegraph_wind_up_s": sorted({
            float(ev["wind_up_s"]) for leg in LEGS
            for f in [os.path.join(BAT, LEGS[leg], "traces", "boss__B__seed74000802.jsonl")]
            for ev in load_trace(f)["events"]
            if ev.get("event") == "telegraph" and str(ev.get("attack_id", "")).endswith(":0")
            and str(ev.get("attacker_id", "")).startswith("boss")
        }),
        "note": "the emitted telegraph already advertises a 0.5 s wind-up for the boss basic "
                "swing and applies NO delay (cosmetic). WINDUP_S = 0.35 makes the advertised "
                "lead and the real strike disagree by 0.15 s.",
    }

    json.dump(out, sys.stdout, indent=1, default=str)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
