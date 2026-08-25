"""U-1 fleet flight-recorder — test suite.

    python3 -m unittest discover agentic_orchestration/flight/tests

Stdlib unittest only. No network, no LLM, no writes outside tempdirs — except the
founding-corpus tests, which write into a tempdir and read the real corpus READ-ONLY.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FLIGHT_DIR = os.path.dirname(HERE)
AO_DIR = os.path.dirname(FLIGHT_DIR)
REPO_ROOT = os.path.dirname(AO_DIR)
BIN = os.path.join(FLIGHT_DIR, "bin")
sys.path.insert(0, FLIGHT_DIR)

import schema  # noqa: E402
import tape  # noqa: E402

# The spec § 1 aggregate, carried here as a CROSS-CHECK, not as an authority.
# If the raw files disagree, the raw files win and this test reports the delta.
SPEC_SUMS = {
    "tokens_input": 72375471,
    "tokens_cached_input": 67431424,
    "tokens_output": 259471,
    "tokens_reasoning": 154000,
}


def run_bin(name, *args):
    p = subprocess.run([sys.executable, os.path.join(BIN, name)] + list(args),
                       capture_output=True, text=True)
    return p


class TestSchema(unittest.TestCase):
    """Rows here are synthetic; `check_paths=False` where a source path is not a real file."""

    @staticmethod
    def row(event, ts="2026-08-24T00:00:00Z", **kw):
        kw.setdefault("check_paths", False)
        return schema.make_row(event, ts, **kw)

    def test_row_id_is_deterministic_and_content_addressed(self):
        a = self.row("START", unit_id="u/1", unit_kind="job")
        b = self.row("START", unit_id="u/1", unit_kind="job")
        c = self.row("START", ts="2026-08-24T00:00:01Z", unit_id="u/1", unit_kind="job")
        self.assertEqual(a["row_id"], b["row_id"])
        self.assertNotEqual(a["row_id"], c["row_id"])

    def test_none_is_dropped_never_stored(self):
        r = self.row("CLOSE", unit_id="u/1", unit_kind="job",
                            tokens_input=None, rc=0)
        self.assertNotIn("tokens_input", r)
        self.assertEqual(r["rc"], 0)

    def test_verdict_illegal_outside_gate_curation_close(self):
        with self.assertRaises(schema.SchemaError):
            self.row("START", unit_id="u/1",
                            unit_kind="job", verdict="PASS")

    def test_tokens_illegal_outside_close(self):
        with self.assertRaises(schema.SchemaError):
            self.row("START", unit_id="u/1",
                            unit_kind="job", tokens_input=10)

    def test_gate_requires_named_gatekeeper(self):
        with self.assertRaises(schema.SchemaError):
            self.row("GATE", unit_id="u/1",
                            unit_kind="job", gate_id="g1", verdict="PASS")
        ok = self.row("GATE", unit_id="u/1", unit_kind="job", gate_id="g1",
                      gatekeeper="jack-ryan", verdict="PASS", derived_from=["finding.md"])
        self.assertEqual(ok["gatekeeper"], "jack-ryan")

    def test_snapshot_is_not_unit_bound(self):
        r = self.row("SNAPSHOT", currency="anthropic-max",
                            meter_raw={"session_pct_used": 34})
        self.assertIsNone(r["unit_id"])
        with self.assertRaises(schema.SchemaError):
            self.row("SNAPSHOT", currency="anthropic-max",
                            meter_raw={"x": 1}, unit_kind="job")

    def test_unknown_field_is_refused(self):
        with self.assertRaises(schema.SchemaError):
            self.row("START", unit_id="u/1",
                            unit_kind="job", cost_dollars=1.23)

    def test_negative_or_float_token_refused(self):
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1",
                            unit_kind="job", tokens_input=-1)
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1",
                            unit_kind="job", tokens_input=1.5)

    def test_month_routing_uses_event_ts(self):
        self.assertEqual(schema.month_of("2026-07-31T23:59:59Z"), "2026-07")


SRC = ["agentic_orchestration/flight/SCHEMA.md"]   # a real path, so B-5's disk check passes


class TestTapeRoundtrip(unittest.TestCase):

    def test_append_and_fold_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            rows = [
                schema.make_row("ENQUEUE", "2026-08-01T00:00:00Z", unit_id="u/1", unit_kind="job"),
                schema.make_row("START", "2026-08-01T00:01:00Z", unit_id="u/1", unit_kind="job",
                                lane="codex-serial", provider="openai"),
                schema.make_row("CLOSE", "2026-08-01T00:05:00Z", unit_id="u/1", unit_kind="job",
                                lane="codex-serial", provider="openai", rc=0,
                                tokens_input=100, derived_from=SRC),
                schema.make_row("START", "2026-08-01T00:02:00Z", unit_id="u/2", unit_kind="job",
                                lane="codex-serial", provider="openai"),
                schema.make_row("ENQUEUE", "2026-08-01T00:03:00Z", unit_id="u/3", unit_kind="job"),
            ]
            for r in rows:
                path, status = tape.append_row(r, d)
                self.assertEqual(status, "appended")
            self.assertTrue(path.endswith("records-2026-08.jsonl"))

            back, raw = tape.load(d)
            self.assertEqual(raw, 5)
            folded = schema.fold(back)
            self.assertEqual(folded["u/1"]["state"], "SEALED")
            self.assertEqual(folded["u/2"]["state"], "IN-FLIGHT")
            self.assertEqual(folded["u/3"]["state"], "QUEUED")
            self.assertEqual(folded["u/1"]["latest"]["event"], "CLOSE")
            self.assertEqual(folded["u/1"]["latest"]["tokens_input"], 100)
            self.assertEqual(tape.audit(d), [])

    def test_duplicate_row_id_refused_unless_forced(self):
        with tempfile.TemporaryDirectory() as d:
            r = schema.make_row("START", "2026-08-01T00:00:00Z", unit_id="u/1", unit_kind="job")
            self.assertEqual(tape.append_row(r, d)[1], "appended")
            self.assertEqual(tape.append_row(r, d)[1], "duplicate")
            self.assertEqual(tape.append_row(r, d, force=True)[1], "appended")
            _, raw = tape.load(d)
            self.assertEqual(raw, 2)

    def test_corrections_supersede_without_rewriting_disk(self):
        with tempfile.TemporaryDirectory() as d:
            wrong = schema.make_row("CLOSE", "2026-08-01T00:05:00Z", unit_id="u/1",
                                    unit_kind="job", rc=0, tokens_input=999, derived_from=SRC)
            tape.append_row(wrong, d)
            right = schema.make_row("CLOSE", "2026-08-01T00:06:00Z", unit_id="u/1",
                                    unit_kind="job", rc=0, tokens_input=100, derived_from=SRC,
                                    corrects=wrong["row_id"])
            tape.append_row(right, d)

            rows, raw = tape.load(d)
            self.assertEqual(raw, 2, "both rows must remain ON DISK — append-only")
            self.assertEqual(len(rows), 1, "the superseded row leaves the FOLD only")
            self.assertEqual(rows[0]["tokens_input"], 100)

            # and the wrong row is still physically present, byte for byte
            with open(os.path.join(d, "records-2026-08.jsonl"), encoding="utf-8") as fh:
                on_disk = fh.read()
            self.assertIn('"tokens_input":999', on_disk)
            self.assertEqual(tape.audit(d), [])

    def test_correction_must_target_an_existing_row_with_same_unit_and_event(self):
        """B-1: the correction path is only a correction path if it is constrained."""
        with tempfile.TemporaryDirectory() as d:
            real = schema.make_row("CLOSE", "2026-08-01T00:05:00Z", unit_id="u/1",
                                   unit_kind="job", rc=0)
            tape.append_row(real, d)

            orphan = schema.make_row("CLOSE", "2026-08-01T00:06:00Z", unit_id="u/1",
                                     unit_kind="job", rc=1, corrects="deadbeefdeadbeef")
            with self.assertRaises(schema.SchemaError):
                tape.append_row(orphan, d)

            wrong_unit = schema.make_row("CLOSE", "2026-08-01T00:06:00Z", unit_id="u/2",
                                         unit_kind="job", rc=1, corrects=real["row_id"])
            with self.assertRaises(schema.SchemaError):
                tape.append_row(wrong_unit, d)

            _, raw = tape.load(d)
            self.assertEqual(raw, 1, "no illegal correction reached disk")

    def test_appender_cli_refuses_illegal_row_with_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            p = run_bin("flight_record", "START", "--unit-id", "u/1", "--unit-kind", "job",
                        "--records-dir", d, "--ts", "2026-08-01T00:00:00Z",
                        "--tokens-input", "5")
            self.assertEqual(p.returncode, 2, p.stderr)
            self.assertIn("REFUSED", p.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, "records-2026-08.jsonl")))

    def test_appender_cli_writes_a_valid_row(self):
        with tempfile.TemporaryDirectory() as d:
            p = run_bin("flight_record", "snapshot", "--currency", "anthropic-max",
                        "--meter", "session_pct_used=34", "--meter", "week_pct_used=61",
                        "--ts", "2026-08-01T00:00:00Z", "--records-dir", d)
            self.assertEqual(p.returncode, 0, p.stderr)
            rows, _ = tape.load(d)
            self.assertEqual(rows[0]["meter_raw"], {"session_pct_used": 34, "week_pct_used": 61})
            self.assertEqual(schema.validate(rows[0]), [])


class TestG1Amendments(unittest.TestCase):
    """jack-ryan's six BLOCKING amendments, each with a test that fails without it."""

    @staticmethod
    def row(event, ts="2026-08-24T00:00:00Z", **kw):
        return schema.make_row(event, ts, **kw)

    def test_B1_row_id_exists_and_is_content_addressed(self):
        r = self.row("START", unit_id="u/1", unit_kind="job")
        self.assertEqual(r["row_id"], schema.compute_row_id(r))
        self.assertEqual(len(r["row_id"]), 16)

    def test_B2_verdict_requires_a_named_gatekeeper(self):
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", rc=0,
                     verdict="PASS", derived_from=SRC)
        ok = self.row("CLOSE", unit_id="u/1", unit_kind="job", rc=0,
                      verdict="PASS", gatekeeper="galadriel", derived_from=SRC)
        self.assertEqual(ok["gatekeeper"], "galadriel")

    def test_B2_rc_alone_never_becomes_a_verdict_on_the_founding_tape(self):
        """The exhibit: job 01 exited rc=0 while its .err logged AuthRequired."""
        err = os.path.join(REPO_ROOT, "agentic_orchestration/research/vfx-p2-dossiers/"
                                      "usage/01-ground_targeted_circle.err")
        with open(err, encoding="utf-8") as fh:
            self.assertIn("AuthRequired", fh.read())

    def test_B3_field_matrix_is_normative_in_both_directions(self):
        with self.assertRaises(schema.SchemaError):      # FORBIDDEN where not allowed
            self.row("HALT", unit_id="u/1", unit_kind="job", tokens_input=5, derived_from=SRC)
        with self.assertRaises(schema.SchemaError):      # REQUIRED where mandated
            self.row("GATE", unit_id="u/1", unit_kind="job", gatekeeper="jack-ryan",
                     verdict="PASS", derived_from=SRC)   # no gate_id
        self.assertEqual(schema.FIELD_MATRIX["CLOSE"]["provider"], "O",
                         "B-3 lean ADOPTED: identity is denormalized onto CLOSE")

    def test_B4_field_set_is_closed_and_no_field_is_named_for_a_metric(self):
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", cache_hit_rate=0.93)
        # FINDING-C (G-2, ACCEPT-WITH-CONDITION): the exception LIST is pinned by equality,
        # not iterated around. Iteration alone let a future custodian discharge a B-4 failure
        # by appending one identifier and keeping the suite green — accretion-by-one-
        # reasonable-field (R-L47-2) relocated from the field list to the exception list.
        # Adding a second exception now costs exactly what adding a field costs: a red suite,
        # a v:2 bump, and a custodian-signed note. The grandfather stands; the gate closes.
        self.assertEqual(
            schema.METRIC_NAME_EXCEPTIONS, ("warn_count",),
            "METRIC_NAME_EXCEPTIONS is PINNED to exactly ('warn_count',) by jack-ryan's G-2 "
            "condition. Growing it is a schema change: bump v, sign a custodian note, and "
            "amend this literal deliberately — never as a side effect of a red test.")
        for f in schema.FIELD_ORDER:
            if f in schema.METRIC_NAME_EXCEPTIONS:
                continue
            for tok in schema.METRIC_NAME_TOKENS:
                self.assertNotIn(tok, f.lower(), "field %r is named for a metric" % f)
        # --- G-2b BLOCK-1: the CLOSED FIELD SET itself, pinned by equality -------------
        # jack-ryan proved the outer door was open: he added `cost_estimate` to COST_FIELDS —
        # one line, reaching ALL_FIELDS and FIELD_MATRIX together — and the row validated CLEAN,
        # owed no derived_from (an estimate names no source), left SCHEMA_REVISION untouched and
        # kept the suite at 70/70 green. An ESTIMATE primitive is precisely what HARD RULE #2
        # ("Never estimate. Absent is absent.") exists to forbid, and it was admitted silently.
        # FINDING-C pinned the EXCEPTION list; nothing pinned the FIELD list, so accretion-by-
        # one-reasonable-field (R-L47-2) simply moved one level up. It is pinned here now.
        # This literal is the schema's field set of record. Adding, removing OR renaming any
        # field turns this test RED — which is the entire cost B-4 asked for and the custodian's
        # v1.1 note claimed to be paying. Amend it DELIBERATELY, alongside a FIELD_SINCE entry
        # and a SCHEMA_REVISIONS row — never as a side effect of making a red test go green.
        self.assertEqual(
            schema.FIELD_ORDER,
            ("v", "row_id", "ts", "event", "unit_id", "unit_kind", "parent_id",
             "workstream", "operator", "seam", "repo", "backfill", "corrects", "derived_from",
             "provider", "lane", "pin", "model_echo", "harness", "harness_version",
             "currency", "curator",
             "verdict", "gate_id", "gatekeeper", "warn_count", "fabrication_check",
             "tokens_input", "tokens_cached_input", "tokens_cache_write", "tokens_output",
             "tokens_reasoning", "cost_usd", "rc", "attempt", "retry_of", "artifacts",
             "meter_raw"),
            "B-4 + G-2b BLOCK-1: FIELD_ORDER is the CLOSED FIELD SET, pinned by equality. If "
            "this test is red, a field was added, removed or renamed. That is a schema change: "
            "amend this literal deliberately, add the FIELD_SINCE entry, sign a SCHEMA_REVISIONS "
            "row — and ask first whether the field is a MEASUREMENT or a DERIVATION.")
        # ALL_FIELDS is the frozen twin the validator actually consults; a pin on one that the
        # other can drift away from is not a pin. Held equal here, and length-checked so a
        # duplicated entry (which frozenset would silently swallow) cannot hide.
        self.assertEqual(schema.ALL_FIELDS, frozenset(schema.FIELD_ORDER))
        self.assertEqual(len(schema.FIELD_ORDER), len(schema.ALL_FIELDS),
                         "a duplicated field name would be invisible in ALL_FIELDS")

    def test_B5_derived_from_is_a_list_whose_paths_must_exist(self):
        with self.assertRaises(schema.SchemaError):   # tokens with no source
            self.row("CLOSE", unit_id="u/1", unit_kind="job", tokens_input=100)
        with self.assertRaises(schema.SchemaError):   # source that is not on disk
            self.row("CLOSE", unit_id="u/1", unit_kind="job", tokens_input=100,
                     derived_from=["no/such/file.jsonl"])
        with self.assertRaises(schema.SchemaError):   # a bare string is not a list
            self.row("CLOSE", unit_id="u/1", unit_kind="job", tokens_input=100,
                     derived_from=SRC[0])
        ok = self.row("CLOSE", unit_id="u/1", unit_kind="job", tokens_input=100,
                      derived_from=SRC)
        self.assertIsInstance(ok["derived_from"], list)

    def test_B5_anchor_suffix_resolves_to_the_file(self):
        ok = self.row("START", unit_id="u/1", unit_kind="job",
                      pin="gpt-5.6-sol@xhigh",
                      derived_from=["agentic_orchestration/workflow-upgrades.md#§ U-4"])
        self.assertTrue(ok["derived_from"][0].endswith("#§ U-4"))

    def test_B6_vendor_lane_enqueue_requires_a_named_curator(self):
        with self.assertRaises(schema.SchemaError):
            self.row("ENQUEUE", unit_id="u/1", unit_kind="job", lane="codex-serial")
        ok = self.row("ENQUEUE", unit_id="u/1", unit_kind="job", lane="codex-serial",
                      curator="galadriel")
        self.assertEqual(ok["curator"], "galadriel")
        # a non-vendor lane owes no curator — the rule is scoped, not blanket
        self.row("ENQUEUE", unit_id="u/2", unit_kind="job", lane="claude-agent")

    def test_WARN1_sla_class_key_and_min_n_are_declared_in_schema(self):
        self.assertEqual(schema.SLA_CLASS_KEY, ("lane", "unit_kind"))
        self.assertGreaterEqual(schema.SLA_MIN_N, 2)


class TestG2Findings(unittest.TestCase):
    """jack-ryan's G-2 render findings, each with a test that fails without the fix."""

    @staticmethod
    def _fr():
        """Load `bin/flight_report` as a module (it is extension-less, so import by loader)."""
        import importlib.util
        import importlib.machinery
        path = os.path.join(BIN, "flight_report")
        spec = importlib.util.spec_from_loader(
            "flight_report", importlib.machinery.SourceFileLoader("flight_report", path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_FINDING3_owner_comes_from_enqueue_start_never_from_a_later_gate(self):
        """A gatekeeper who judged ONE event is not thereby the owner of the run (#9).

        Reproduces the exact shape that mis-rendered: gandalf ENQUEUEs and STARTs `run:X`,
        jack-ryan files the LATEST row (a GATE). Folding operator off `latest` returns
        jack-ryan; folding it off the unit's own identity-bearing rows returns gandalf.
        """
        fr = self._fr()
        rows = [
            schema.make_row("ENQUEUE", "2026-08-24T22:59:53Z", unit_id="run:X", unit_kind="run",
                            operator="gandalf", lane="claude-agent"),
            schema.make_row("START", "2026-08-24T23:10:24Z", unit_id="run:X", unit_kind="run",
                            operator="gandalf", lane="claude-agent"),
            schema.make_row("GATE", "2026-08-24T23:20:54Z", unit_id="run:X", unit_kind="run",
                            operator="jack-ryan", gate_id="G-1", gatekeeper="jack-ryan",
                            verdict="PASS-WITH-FINDINGS", derived_from=SRC),
        ]
        unit = schema.fold(rows)["run:X"]
        self.assertEqual(unit["latest"]["event"], "GATE")
        self.assertEqual(unit["latest"]["operator"], "jack-ryan",
                         "precondition: the LATEST row really is the gatekeeper's")
        self.assertEqual(fr.unit_identity(unit)["operator"], "gandalf",
                         "FINDING-3: owner folds from ENQUEUE/START, never from a later GATE")
        self.assertEqual(fr.last_actor(unit), "jack-ryan",
                         "last-actor stays available as its OWN answer, in its own column")

    def test_FINDING3_holds_on_the_live_tape_for_the_run_that_exposed_it(self):
        rows, _ = tape.load(FLIGHT_DIR)
        units = schema.fold(rows)
        u = units.get("run:U1-BUILD")
        self.assertIsNotNone(u, "the unit that exposed FINDING-3 must still be on the tape")
        fr = self._fr()
        self.assertEqual(fr.unit_identity(u).get("operator"), "gandalf")

    def test_FINDING2_rendered_lanes_partition_the_tape(self):
        """Every unit in exactly one lane: none dropped, none doubled, none invented."""
        fr = self._fr()
        rows, _ = tape.load(FLIGHT_DIR)
        units = schema.fold(rows)

        # the auditor itself must be able to CATCH all three failure shapes
        uids = sorted(units)
        self.assertEqual(fr.partition_audit(units, {"A": uids}), [])
        self.assertTrue(any("falls in NO lane" in x
                            for x in fr.partition_audit(units, {"A": uids[1:]})))
        self.assertTrue(any("renders in 2 lanes" in x
                            for x in fr.partition_audit(units, {"A": uids, "B": uids[:1]})))
        self.assertTrue(any("not a unit on the tape" in x
                            for x in fr.partition_audit(units, {"A": uids + ["ghost/1"]})))

        # …and the report it guards must actually pass it, loudly, in its own output
        p = run_bin("flight_report", "--records-dir", FLIGHT_DIR, "--repo-root", REPO_ROOT,
                    "--stdout", "--no-probes", "--now", "2026-08-25T00:00:00Z")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("PARTITION ✓", p.stdout)
        self.assertNotIn("render check FAILED", p.stdout)
        self.assertIn("%d unit(s) on tape = " % len(units), p.stdout)

    def test_FINDING1_every_u1_build_row_in_the_fold_declares_itself_backfill(self):
        """The U1-BUILD rows are reconstruction, and the tape must SAY so.

        Corrections, never rewrites: the undeclared originals stay on disk untouched and are
        superseded by rows carrying `backfill: true`.
        """
        rows, raw = tape.load(FLIGHT_DIR)               # post-correction fold
        live = [r for r in rows if r.get("workstream") == "U1-BUILD"]
        self.assertTrue(live, "precondition: U1-BUILD rows are on the tape")
        for r in live:
            self.assertIs(r.get("backfill"), True,
                          "undeclared backfill survives the fold: %s %s"
                          % (r["event"], r["row_id"]))
        on_disk = schema.read_tape(tape.tape_files(FLIGHT_DIR))
        self.assertTrue(any(r.get("workstream") == "U1-BUILD" and not r.get("backfill")
                            for r in on_disk),
                        "the superseded originals must REMAIN on disk — the tape does not lie "
                        "about what was believed at the time")
        self.assertGreater(raw, len(rows))


class TestAM1SchemaV11(unittest.TestCase):
    """AMENDMENT AM-1 (revision 1.1) — the custodian amendment, and its blast radius."""

    @staticmethod
    def row(event, ts="2026-08-24T00:00:00Z", **kw):
        return schema.make_row(event, ts, **kw)

    def test_revision_marker_and_lineage_are_declared(self):
        self.assertEqual(schema.SCHEMA_REVISION, "1.1")
        self.assertEqual(schema.SCHEMA_VERSION, 1,
                         "the ROW-FORMAT version does not move on a purely additive amendment: "
                         "bumping it would fork the validator to keep 67 legal rows legal, and "
                         "ONE validator with zero exceptions is a HARD gate property (G2-T3)")
        self.assertEqual([r[0] for r in schema.SCHEMA_REVISIONS], ["1.0", "1.1"])
        for rev, date, who, why in schema.SCHEMA_REVISIONS:
            self.assertTrue(date and who and why, "every revision signs itself")

    def test_11a_grok_serial_replaces_grok_judge_in_the_lane_enum(self):
        self.assertIn("grok-serial", schema.LANES)
        self.assertNotIn("grok-judge", schema.LANES)
        self.assertIn("grok-serial", schema.VENDOR_LANES)
        with self.assertRaises(schema.SchemaError):
            self.row("START", unit_id="u/1", unit_kind="job", lane="grok-judge")

    def test_11a_the_rename_was_TAPE_SAFE(self):
        """The rename is only legal because no row spent the old name. Re-checked here."""
        rows = schema.read_tape(tape.tape_files(FLIGHT_DIR))
        self.assertEqual([r for r in rows if r.get("lane") == "grok-judge"], [],
                         "a `grok-judge` row exists — the rename is no longer tape-safe and "
                         "needs a correction pass, not an enum edit")

    def test_11a_grok_serial_is_a_vendor_lane_and_owes_a_curator_at_enqueue(self):
        with self.assertRaises(schema.SchemaError):
            self.row("ENQUEUE", unit_id="u/1", unit_kind="job", lane="grok-serial")
        ok = self.row("ENQUEUE", unit_id="u/1", unit_kind="job", lane="grok-serial",
                      curator="galadriel")
        self.assertEqual(ok["curator"], "galadriel")

    def test_11b_grok_sub_currency(self):
        self.assertIn("grok-sub", schema.CURRENCIES)
        ok = self.row("CLOSE", unit_id="u/1", unit_kind="job", currency="grok-sub", rc=0)
        self.assertEqual(ok["currency"], "grok-sub")
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", currency="grok-subscription")

    def test_11c_cost_usd_is_close_only(self):
        ok = self.row("CLOSE", unit_id="u/1", unit_kind="job", cost_usd=0.00286,
                      derived_from=SRC)
        self.assertEqual(ok["cost_usd"], 0.00286)
        for ev in ("START", "ENQUEUE", "GATE", "CURATION", "HALT"):
            with self.assertRaises(schema.SchemaError):
                self.row(ev, unit_id="u/1", unit_kind="job", cost_usd=0.001,
                         derived_from=SRC, gate_id="g", gatekeeper="x", verdict="PASS")

    def test_11c_cost_usd_must_name_its_source_and_be_a_non_negative_number(self):
        with self.assertRaises(schema.SchemaError):    # reported cost with no named artifact
            self.row("CLOSE", unit_id="u/1", unit_kind="job", cost_usd=0.00286)
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", cost_usd=-1, derived_from=SRC)
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", cost_usd="0.003",
                     derived_from=SRC)

    def test_11c_cost_usd_survives_the_no_metric_name_rule_without_a_new_exception(self):
        """The exception list is still exactly one name — AM-1 did not widen the door."""
        self.assertEqual(schema.METRIC_NAME_EXCEPTIONS, ("warn_count",))
        self.assertIn("cost_usd", schema.ALL_FIELDS)

    def test_row_min_revision_is_derived_from_keys_never_stamped(self):
        pre = self.row("CLOSE", unit_id="u/1", unit_kind="job", rc=0)
        post = self.row("CLOSE", unit_id="u/1", unit_kind="job", cost_usd=0.5,
                        derived_from=SRC)
        self.assertEqual(schema.row_min_revision(pre), "1.0")
        self.assertEqual(schema.row_min_revision(post), "1.1")
        self.assertNotIn("revision", post, "a per-row revision stamp is a stored summary")

    def test_BLOCK2_row_min_revision_asks_VALUES_not_only_keys(self):
        """G-2b BLOCK-2 — the test that FAILED against the pre-fix function, on his proof case.

        `row_min_revision` was the mechanism offered in place of B-4's `v:2` stamp, and it asked
        only `FIELD_SINCE` — i.e. only KEYS. But 2 of AM-1's 3 amendments introduced NO key: the
        1.1-a lane rename and the 1.1-b currency live in VALUES. jack-ryan reconstructed the
        genuine v1.0 validator from `a4f7a569` and proved the gap: it REJECTS `lane:
        "grok-serial"` (`lane must be one of [… 'grok-judge' …]`) and REJECTS `currency:
        "grok-sub"`, while the function called both rows 1.0-readable.

        The live grok row answered "1.1" only BY LUCK — it happens to carry `cost_usd`. A
        `grok-serial` START row cannot carry one (cost is CLOSE-only), so it would have reported
        "1.0" and been unreadable by the 1.0 reader it named.

        The previous test exercised only the field axis — the only axis implemented — so it
        structurally could not fail on this defect (the B4-P14 cannot-fail class). This one can.
        """
        # 1.1-a — his exact proof case: a lane value, on an event that CANNOT carry cost_usd.
        start = self.row("START", unit_id="u/1", unit_kind="job", lane="grok-serial")
        self.assertNotIn("cost_usd", start, "the proof case must not answer via the key axis")
        self.assertEqual(schema.row_min_revision(start), "1.1",
                         "a `grok-serial` row is unreadable by a v1.0 validator — the rename is "
                         "an amendment that lives in a VALUE, and a revision answer derived from "
                         "keys alone cannot see it")
        # 1.1-b — same shape, the currency axis, again with no 1.1 KEY anywhere on the row.
        cur = self.row("SNAPSHOT", currency="grok-sub", meter_raw={"seen": 1})
        self.assertEqual(schema.row_min_revision(cur), "1.1")
        # and the pre-1.1 values on those same fields still answer 1.0 — the map is per-VALUE,
        # not per-field: widening it to "any row naming a lane needs 1.1" would be the opposite
        # defect, over-reporting every one of the 67 pre-amendment rows into a revision they
        # never needed.
        self.assertEqual(schema.row_min_revision(
            self.row("START", unit_id="u/1", unit_kind="job", lane="codex-serial")), "1.0")
        self.assertEqual(schema.row_min_revision(
            self.row("SNAPSHOT", currency="chatgpt-sub", meter_raw={"seen": 1})), "1.0")
        # the map is DECLARED in schema, greppable (G2-T6), never inlined in the function
        self.assertEqual(schema.VALUE_SINCE["lane"]["grok-serial"], "1.1")
        self.assertEqual(schema.VALUE_SINCE["currency"]["grok-sub"], "1.1")

    def test_BLOCK2_no_pre_amendment_row_on_the_live_tape_is_over_reported(self):
        """The fix must not push the 67 pre-AM-1 rows into a revision they never needed."""
        rows = schema.read_tape(tape.tape_files(FLIGHT_DIR))
        needs_11 = [r for r in rows if schema.row_min_revision(r) == "1.1"]
        self.assertEqual([r["row_id"] for r in needs_11], ["dfbe28b17c2520f0"],
                         "exactly one row on the tape needs revision 1.1 — the founding grok "
                         "row, which needs it on ALL THREE axes (lane, currency, cost_usd)")

    def test_WARN1_a_lane_declared_to_report_no_cost_may_not_carry_one(self):
        """G-2b WARN-1 — prose in § 3 becomes a parse error on the lane where it is banked."""
        with self.assertRaises(schema.SchemaError):
            self.row("CLOSE", unit_id="u/1", unit_kind="job", lane="codex-serial",
                     cost_usd=12.50, tokens_input=100, derived_from=SRC)
        # the lane that DOES report one is untouched
        ok = self.row("CLOSE", unit_id="u/1", unit_kind="job", lane="grok-serial",
                      cost_usd=0.00286, derived_from=SRC)
        self.assertEqual(ok["cost_usd"], 0.00286)
        # a lane with no banked measurement of its stream is UNDECLARED, not "reports none":
        # asserting the negative for a lane nobody probed would be the unmeasured claim this
        # recorder refuses. Absence from the map is permissive, deliberately.
        self.assertNotIn("claude-agent", schema.LANE_REPORTS_COST)
        self.row("CLOSE", unit_id="u/1", unit_kind="job", lane="claude-agent",
                 cost_usd=0.01, derived_from=SRC)
        # and it did not disturb the tape: no existing row is retro-invalidated
        self.assertEqual(tape.audit(FLIGHT_DIR), [])

    def test_pre_amendment_rows_remain_valid_untouched(self):
        """Backward compatibility is the whole reason `v` did not move."""
        self.assertEqual(tape.audit(FLIGHT_DIR), [])

    def test_the_founding_grok_row_says_only_what_section_9_1_measured(self):
        rows, _ = tape.load(FLIGHT_DIR)
        gk = [r for r in rows if r.get("lane") == "grok-serial"]
        self.assertEqual(len(gk), 1, "exactly one founding grok row")
        r = gk[0]
        self.assertEqual(r["event"], "CLOSE")
        self.assertIs(r.get("backfill"), True)
        self.assertEqual(r["provider"], "xai")
        self.assertEqual(r["currency"], "grok-sub")
        self.assertEqual(r["cost_usd"], 0.00286)
        self.assertEqual(r["harness_version"], "1.0.5")
        self.assertEqual(r["model_echo"], "grok-4.6-build")
        self.assertTrue(any("codex-lane-protocol-and-busy-check-SPEC.md" in s
                            for s in r["derived_from"]))
        # NOT in the § 9.1 record ⇒ NOT on the row. A null is a fact.
        for absent in ("tokens_input", "tokens_cached_input", "tokens_cache_write",
                       "tokens_output", "tokens_reasoning", "rc", "verdict", "pin",
                       "gatekeeper", "artifacts"):
            self.assertNotIn(absent, r,
                             "%s is not in the § 9.1 measurement record and must not be on the "
                             "row — PROBE-OK is the lane's own self-report, and a verdict never "
                             "self-reports (B-2)" % absent)


class TestFoundingNormalization(unittest.TestCase):
    """Runs the real normalizer against the real corpus, into a throwaway tape."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="flight-founding-")
        cls.first = run_bin("normalize_vfx_corpus", "--records-dir", cls.tmp)
        cls.second = run_bin("normalize_vfx_corpus", "--records-dir", cls.tmp)
        cls.rows, cls.raw = tape.load(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_normalizer_ran(self):
        self.assertEqual(self.first.returncode, 0, self.first.stderr)
        self.assertEqual(self.second.returncode, 0, self.second.stderr)

    def test_idempotent_second_run_appends_nothing(self):
        self.assertIn("rows appended: 0", self.second.stdout)
        rows2, raw2 = tape.load(self.tmp)
        self.assertEqual(raw2, self.raw)

    def test_exact_founding_row_counts(self):
        starts = [r for r in self.rows if r["event"] == "START"]
        closes = [r for r in self.rows if r["event"] == "CLOSE"]
        self.assertEqual(len(starts), 30)
        self.assertEqual(len(closes), 30)
        self.assertTrue(all(r.get("backfill") is True for r in starts + closes))

    def test_every_row_validates(self):
        for r in self.rows:
            self.assertEqual(schema.validate(r), [], "invalid founding row: %r" % r)

    def test_every_close_pins_a_raw_artifact_that_exists(self):
        for r in self.rows:
            if r["event"] != "CLOSE":
                continue
            self.assertIsInstance(r["derived_from"], list)
            for src in r["derived_from"]:
                self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, src.split("#")[0])),
                                "derived_from does not resolve: %s" % src)
            for a in r.get("artifacts") or []:
                self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, a["path"])))
                self.assertEqual(os.path.getsize(os.path.join(REPO_ROOT, a["path"])), a["bytes"])

    def test_token_sums_measured_from_raw_files(self):
        """The RAW FILES WIN. This reports any delta against the spec's stated aggregate."""
        got = {}
        for f in ("tokens_input", "tokens_cached_input", "tokens_output", "tokens_reasoning"):
            got[f] = sum(r.get(f) or 0 for r in self.rows if r["event"] == "CLOSE")
        deltas = {k: (got[k], SPEC_SUMS[k]) for k in SPEC_SUMS if got[k] != SPEC_SUMS[k]}
        self.assertEqual(deltas, {},
                         "MEASURED != spec § 1 aggregate. The raw files win; the spec figure is "
                         "the thing to correct. measured=%r" % (got,))

    def test_no_gate_row_was_invented(self):
        self.assertEqual([r for r in self.rows if r["event"] == "GATE"], [])

    def test_B2_no_founding_row_carries_a_verdict_derived_from_rc(self):
        """Amendment B-2: rc=0 is a mechanical fact; 30 jobs were never judged at job grain."""
        for r in self.rows:
            if r["event"] == "CLOSE":
                self.assertIsNone(r.get("verdict"),
                                  "founding CLOSE rows must carry rc and NO verdict")
        self.assertTrue(all(r.get("rc") == 0 for r in self.rows if r["event"] == "CLOSE"))

    def test_INFO3_no_enqueue_row_was_fabricated(self):
        self.assertEqual([r for r in self.rows if r["event"] == "ENQUEUE"], [])

    def test_B5c_harness_version_is_null_because_no_stream_carries_one(self):
        self.assertTrue(all(r.get("harness_version") is None for r in self.rows))
        self.assertTrue(all(r.get("model_echo") is None for r in self.rows))

    def test_INFO7_err_sidecar_rides_along_as_evidence(self):
        for r in self.rows:
            if r["event"] == "CLOSE":
                self.assertTrue(any(s.endswith(".err") for s in r["derived_from"]),
                                "CLOSE row omits its .err sidecar: %s" % r["unit_id"])

    def test_the_one_curation_row_names_its_curator_and_its_source(self):
        cur = [r for r in self.rows if r["event"] == "CURATION"]
        self.assertEqual(len(cur), 1)
        self.assertEqual(cur[0]["verdict"], "PASS")
        self.assertEqual(cur[0]["gatekeeper"], "elrond")
        self.assertEqual(cur[0]["warn_count"], 6)
        for src in cur[0]["derived_from"]:
            self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, src.split("#")[0])))


class TestReport(unittest.TestCase):

    LANES = ("AWAITING MATT", "IN-FLIGHT", "AT GATE", "HEALTH", "SEALED")

    def _render(self, records_dir, probes=True):
        args = ["flight_report", "--records-dir", records_dir, "--repo-root", REPO_ROOT,
                "--stdout", "--now", "2026-08-25T00:00:00Z"]
        if not probes:
            args.append("--no-probes")
        p = run_bin(*args)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_report_renders_the_five_lanes_from_the_live_tape(self):
        out = self._render(FLIGHT_DIR)
        for lane in self.LANES:
            self.assertIn(lane, out, "missing lane header: %s" % lane)
        self.assertIn("VIEW ONLY", out)
        self.assertIn("THE LAW", out)

    def test_report_renders_on_an_empty_tape_too(self):
        with tempfile.TemporaryDirectory() as d:
            out = self._render(d, probes=False)
            for lane in self.LANES:
                self.assertIn(lane, out)

    def test_report_is_idempotent_for_a_pinned_now(self):
        a = self._render(FLIGHT_DIR, probes=False)
        b = self._render(FLIGHT_DIR, probes=False)
        self.assertEqual(a, b)

    def test_report_surfaces_the_founding_aggregate(self):
        out = self._render(FLIGHT_DIR, probes=False)
        self.assertIn("VFX-AB", out)
        self.assertIn("72.4M", out)   # tok-in rollup, derived at render time
        self.assertIn("93.2%", out)   # cache hit-rate, derived at render time

    def test_probe_failure_is_loud_not_silent(self):
        """A missing queue file must render as a probe failure, never as 'none open'."""
        with tempfile.TemporaryDirectory() as fake_root:
            p = run_bin("flight_report", "--records-dir", FLIGHT_DIR,
                        "--repo-root", fake_root, "--stdout",
                        "--now", "2026-08-25T00:00:00Z")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("probe failed:", p.stdout)


class TestLanesSection(unittest.TestCase):
    """AM-1 § 13.1 — the vendor LANE CARDS, and the honesty rules they must not break."""

    @staticmethod
    def _fr():
        import importlib.util
        import importlib.machinery
        path = os.path.join(BIN, "flight_report")
        spec = importlib.util.spec_from_loader(
            "flight_report", importlib.machinery.SourceFileLoader("flight_report", path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    @staticmethod
    def _cfg(fr, key):
        return [c for c in fr.LANE_CARDS if c["key"] == key][0]

    def test_the_section_renders_both_vendor_lanes_with_the_degraded_tag_and_Q62_verbatim(self):
        p = run_bin("flight_report", "--records-dir", FLIGHT_DIR, "--repo-root", REPO_ROOT,
                    "--stdout", "--now", "2026-08-25T00:00:00Z")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = p.stdout
        self.assertIn("LANES", out)
        self.assertIn("`codex-serial`", out)
        self.assertIn("`grok-serial`", out)
        self.assertIn("degraded — D-2 CLI pending", out)
        self.assertIn("liveness-NOW is the § 3 CLI check's answer; the board is a VIEW "
                      "(THE LAW) and may lag its refresh.", out)
        self.assertIn("claude lanes (summarised", out)

    def test_every_answer_state_is_lane_spec_vocabulary(self):
        fr = self._fr()
        allowed = {"open", "busy-lock", "busy-out-of-band", "queue-pending",
                   "auth-expired", "cli-missing", "busy-unknown"}
        self.assertEqual(set(fr.STATE_PRECEDENCE), allowed)

    def test_union_is_fail_closed_false_busy_over_false_open(self):
        fr = self._fr()
        cfg = self._cfg(fr, "codex-serial")
        ok_auth = dict(state="ok", rc=0, text="Logged in", cli="/x/codex", on_path=True)
        free = dict(free=True, path="/tmp/l.lock", acquired=False, why="no lock file")
        rl = [dict(path="a/_run-log.tsv", present=True, rows=1, cols=4, marker="rc=0",
                   terminal=True, enqueued=0, backlog_derivable=False)]

        self.assertEqual(fr.lane_answer(cfg, free, [], rl, ok_auth)["state"], "open")
        held = dict(free=False, path="/tmp/l.lock", acquired=True, why=None)
        self.assertEqual(fr.lane_answer(cfg, held, [], rl, ok_auth)["state"], "busy-lock")
        oob = [(4242, "/opt/homebrew/bin/codex exec --json 'go'")]
        self.assertEqual(fr.lane_answer(cfg, free, oob, rl, ok_auth)["state"],
                         "busy-out-of-band")
        # a leg that FAILED is ambiguity, and ambiguity renders busy — never open
        self.assertEqual(fr.lane_answer(cfg, None, [], rl, ok_auth)["state"], "busy-unknown")
        self.assertEqual(fr.lane_answer(cfg, free, None, rl, ok_auth)["state"], "busy-unknown")
        # an unrecognised run-log marker reads NON-terminal (fail-closed)
        weird = [dict(path="a/_run-log.tsv", present=True, rows=1, cols=6, marker="DONE",
                      terminal=False, enqueued=0, backlog_derivable=True)]
        self.assertEqual(fr.lane_answer(cfg, free, [], weird, ok_auth)["state"], "busy-lock")

    def test_WARN2_queue_pending_is_OPEN_per_Amendment_H_and_colours_fire_safe(self):
        """G-2b WARN-2 — backlog is not occupancy, and the colour must say so.

        Amendment H binds the § 10.3 selection law to the § 3 vocabulary: **"Open" = `open` OR
        `queue-pending`**. `STATE_PRECEDENCE` correctly ranks `queue-pending` above `open` (the
        backlog is the more specific fact and deserves to be the one named), but the card then
        coloured every non-`open` state AMBER — so a lane that is OPEN and first-choice under
        ratified law told Matt, at a glance, to look elsewhere.
        """
        fr = self._fr()
        cfg = self._cfg(fr, "codex-serial")
        ok_auth = dict(state="ok", rc=0, text="Logged in", cli="/x/codex", on_path=True)
        free = dict(free=True, path="/tmp/l.lock", acquired=False, why=None)
        backlog = [dict(path="a/_run-log.tsv", present=True, rows=3, cols=6, marker="rc=0",
                        terminal=True, enqueued=2, backlog_derivable=True)]
        ans = fr.lane_answer(cfg, free, [], backlog, ok_auth)
        self.assertEqual(ans["state"], "queue-pending", "precedence is unchanged by WARN-2")
        self.assertTrue(fr.safe_to_fire(ans))
        self.assertEqual(fr.state_marker(ans), fr.GREEN,
                         "Amendment H: `queue-pending` is OPEN and first-choice. Amber here tells "
                         "Matt to look elsewhere at a lane he should fire into — a colour he acts "
                         "on, diverging from ratified law")
        self.assertIn("safe to fire: YES", fr.safe_to_fire_line(ans))
        self.assertIn("backlog is not occupancy", fr.safe_to_fire_line(ans))
        # the predicate is pinned BY STATE NAME (lane spec § 3) and exported, so a consumer
        # binds to it rather than re-deriving a colour of its own
        self.assertEqual(fr.SAFE_TO_FIRE_STATES, ("open", "queue-pending"))

    def test_WARN2_the_other_state_classes_keep_their_colours(self):
        """The fix is scoped: occupied stays amber, closed stays red, coverage still caps green."""
        fr = self._fr()
        mk = lambda st, na=(): fr.state_marker(dict(state=st, na=list(na)))
        self.assertEqual(mk("open"), fr.GREEN)
        for st in fr.OCCUPIED_STATES:
            if st == "busy-unknown":
                continue
            self.assertEqual(mk(st), fr.AMBER, "%s: occupied is not closed — ENQUEUE behind it" % st)
        for st in fr.CLOSED_STATES + ("busy-unknown",):
            self.assertEqual(mk(st), fr.RED)
        # #70 is independent of the predicate: fire-safe on reduced coverage is NOT a full green
        self.assertEqual(mk("open", na=["leg 1"]), fr.AMBER)
        self.assertEqual(mk("queue-pending", na=["leg 1"]), fr.AMBER)

    def test_WARN2_the_card_renders_the_safe_to_fire_predicate_at_all(self):
        """The second half of WARN-2: the card showed no predicate line whatsoever."""
        p = run_bin("flight_report", "--records-dir", FLIGHT_DIR, "--repo-root", REPO_ROOT,
                    "--stdout", "--now", "2026-08-25T00:00:00Z")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("safe to fire:", p.stdout)

    def test_a_leg_that_does_not_exist_is_not_ambiguity_but_is_declared_as_coverage(self):
        """NOT-APPLICABLE ≠ UNREACHABLE. Grok has no lock and no run-log by construction."""
        fr = self._fr()
        cfg = self._cfg(fr, "grok-serial")
        auth = dict(state="ok", rc=0, text="logged in", cli="/x/grok", on_path=False)
        ans = fr.lane_answer(cfg, None, [], None, auth)
        self.assertEqual(ans["state"], "open")
        self.assertEqual(len(ans["na"]), 2)
        self.assertTrue(any("COVERAGE" in r and "1 of 3 legs" in r for r in ans["reasons"]),
                        "a one-leg answer must declare its coverage, never read as a full green")

    def test_argv_match_is_anchored_so_the_instrument_never_convicts_itself(self):
        fr = self._fr()
        cfg = self._cfg(fr, "codex-serial")
        free = dict(free=True, path="/tmp/l.lock", acquired=False, why="none")
        auth = dict(state="ok", rc=0, text="ok", cli="/x/codex", on_path=True)
        mentions = [(1, "/bin/zsh -c 'grep codex exec ~/notes.md'"),
                    (2, "python3 flight/bin/some_tool --lane codex-serial")]
        ans = fr.lane_answer(cfg, free, mentions, [], auth)
        self.assertEqual(ans["state"], "open")
        self.assertEqual(ans["advisories"], [])

    def test_interactive_tui_is_ADVISORY_and_never_moves_the_state(self):
        """Q62 RULED advise-only, vendor-generic: a TUI does not close the lane."""
        fr = self._fr()
        for key, argv in (("codex-serial", "codex"), ("grok-serial", "grok")):
            cfg = self._cfg(fr, key)
            free = dict(free=True, path="/tmp/l.lock", acquired=False, why="none")
            auth = dict(state="ok", rc=0, text="ok", cli="/x/" + argv, on_path=True)
            ans = fr.lane_answer(cfg, free, [(99, argv)], [] if cfg["runlogs"] else None, auth)
            self.assertEqual(ans["state"], "open")
            self.assertTrue(any("interactive-%s-present" % cfg["vendor"] in a
                                for a in ans["advisories"]))

    def test_leader_sock_reads_busy_for_grok(self):
        """The shared-leader backend is the concurrency door the serial law forbids."""
        fr = self._fr()
        cfg = self._cfg(fr, "grok-serial")
        auth = dict(state="ok", rc=0, text="ok", cli="/x/grok", on_path=False)
        ans = fr.lane_answer(cfg, None, [(7, "/usr/bin/node /x/leader.sock-host")], None, auth)
        self.assertEqual(ans["state"], "busy-out-of-band")

    def test_auth_and_cli_states_are_carried_not_invented(self):
        fr = self._fr()
        cfg = self._cfg(fr, "codex-serial")
        free = dict(free=True, path="/tmp/l.lock", acquired=False, why="none")
        expired = dict(state="auth-expired", rc=1, text="not logged in",
                       cli="/x/codex", on_path=True)
        self.assertEqual(fr.lane_answer(cfg, free, [], [], expired)["state"], "auth-expired")
        missing = dict(state="cli-missing", text="CLI not found")
        self.assertEqual(fr.lane_answer(cfg, free, [], [], missing)["state"], "cli-missing")

    def test_lane_units_membership_is_shared_not_reimplemented(self):
        fr = self._fr()
        rows, _ = tape.load(FLIGHT_DIR)
        units = schema.fold(rows)
        self.assertEqual(len(fr.lane_units(units, "grok-serial")), 1)
        self.assertEqual(len(fr.lane_units(units, "codex-serial")), 30)

    def test_the_lane_probes_write_NOTHING(self):
        """THE LAW, made mechanical for the new probes: a view with a footprint is not a view.

        Snapshots every file under `flight/` and under the lane-lock dir, renders with ALL
        probes live (including the leg-1 acquire and both vendor auth CLIs), and requires the
        byte-for-byte state to be identical afterwards.
        """
        import hashlib

        def snap():
            out = {}
            roots = [FLIGHT_DIR, os.path.expanduser("~/.reincarnated/lane-locks")]
            for root in roots:
                if not os.path.isdir(root):
                    out[root] = "(absent)"
                    continue
                for dirpath, dirnames, filenames in os.walk(root):
                    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                    for f in sorted(filenames):
                        fp = os.path.join(dirpath, f)
                        with open(fp, "rb") as fh:
                            out[fp] = hashlib.sha256(fh.read()).hexdigest()
            return out

        before = snap()
        p = run_bin("flight_report", "--records-dir", FLIGHT_DIR, "--repo-root", REPO_ROOT,
                    "--stdout", "--now", "2026-08-25T00:00:00Z")
        self.assertEqual(p.returncode, 0, p.stderr)
        after = snap()
        self.assertEqual(before, after,
                         "a probe changed disk state. The check derives; it never emits — a "
                         "probe that writes walks the checker into the data path, which is "
                         "THE LAW's failure mode arriving through the instrument.")


class TestTheLaw(unittest.TestCase):
    """Structural checks that the constitution holds in the source, not just in the prose."""

    def test_no_llm_or_network_imports_anywhere(self):
        banned = ("anthropic", "openai", "urllib.request", "requests", "http.client", "socket")
        files = [os.path.join(FLIGHT_DIR, f) for f in ("schema.py", "tape.py")]
        # Files only: a `__pycache__/` directory appears in `bin/` as soon as another seam
        # imports `flight_report` as a module (the Tier-2 board does exactly that), and the
        # import ban is a property of SOURCE, not of whatever the interpreter caches beside it.
        files += [os.path.join(BIN, f) for f in os.listdir(BIN)
                  if os.path.isfile(os.path.join(BIN, f))]
        files += [os.path.join(FLIGHT_DIR, "tests", "test_flight.py")]
        for path in files:
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            for b in banned:
                self.assertNotIn("import %s" % b, src, "%s imports %s" % (path, b))

    def test_the_view_has_no_write_verb_onto_the_tape(self):
        with open(os.path.join(BIN, "flight_report"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("append_row", src, "flight_report must never append to the tape")

    def test_live_tape_passes_the_whole_tape_audit(self):
        """ONE validator, zero exceptions, across every workflow on the tape (G2-T3)."""
        self.assertEqual(tape.audit(FLIGHT_DIR), [])

    def test_live_tape_stores_no_unknown_and_no_metric_named_key(self):
        """G2-T6, done mechanically against the frozen allow-list."""
        rows, _ = tape.load(FLIGHT_DIR)
        seen = set()
        for r in rows:
            seen |= set(r.keys())
        self.assertEqual(seen - schema.ALL_FIELDS, set(), "unknown key on the tape")
        for k in seen:
            if k in schema.METRIC_NAME_EXCEPTIONS:
                continue
            for tok in schema.METRIC_NAME_TOKENS:
                self.assertNotIn(tok, k.lower(), "metric-named key on the tape: %s" % k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
