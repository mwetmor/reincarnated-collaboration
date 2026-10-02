import json, sys
from reincarnated.simulation.kc2 import run as kr
from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
from reincarnated.simulation.scripts import gamora_kc2_play_v3p9_oracle_2026_10_02 as V9
from reincarnated.simulation.kc2 import player_offense as po
period = FP._period()
obs = []
real = kr.simulate_wave
def ob(*a, **kw):
    r = real(*a, **kw); w = r.waves[0]
    rec = {"wave": int(w["wave"]), "outcome": w.get("outcome"), "t_s": round(float(w["t_end_s"]) - float(w["t_start_s"]), 3)}
    if w.get("outcome") not in ("cleared", "player_death"):
        ev = r.rows_as_dicts(); dead = {x["target_id"] for x in ev if x["event_type"] == "death"}
        hits = {}
        for x in ev:
            if x["event_type"] in ("damage_dealt", "dot_tick") and x.get("source_id") == "player":
                hits[x["target_id"]] = hits.get(x["target_id"], 0) + 1
        mv = {m.actor_id: m for m in (r.movers or [])}
        rec["surviving_bodies"] = [{"id": a_["actor_id"], "rec": a_["record_path"].split("/")[-1],
            "res_phys": getattr(po.mitigation_at(a_["record_path"], rec["wave"]), "res_physical_pct", None),
            "hits": hits.get(a_["actor_id"], 0), "contact": getattr(mv.get(a_["actor_id"]), "contact_t_s", "n/a"),
            "ring_halt": getattr(mv.get(a_["actor_id"]), "mech_ring_halt_step", None)} for a_ in r.actors if a_["actor_id"] not in dead]
        rec["surviving_pets"] = [{"id": p["actor_id"], "rec": p["record_path"].split("/")[-1],
            "res_phys": getattr(po.mitigation_at(p["record_path"], rec["wave"]), "res_physical_pct", None),
            "res_bleed": getattr(po.mitigation_at(p["record_path"], rec["wave"]), "res_bleeding_pct", None),
            "hits": hits.get(p["actor_id"], 0)} for p in (r.pet_actors or []) if p["actor_id"] not in dead]
    obs.append(rec); return r
kr.simulate_wave = ob
try:
    res = V9.run_one("V39-NOHUNT", (18,), period)
finally:
    kr.simulate_wave = real
s = V9.summarise(res, (18,))
print(json.dumps({"artifact_class": "NOT-A-GRADED-RUN -- OBS-1 corrigendum witness (read-only re-run of v3.9 V39-NOHUNT salt 18, oracle unmodified)",
                  "per_salt_ratio": s["per_salt_ratio"], "leg_a_terminals": s["leg_a_terminals"],
                  "n_rows": len(res["salts"]["18"]["rows"]), "per_wave": obs}, indent=1, default=str))
