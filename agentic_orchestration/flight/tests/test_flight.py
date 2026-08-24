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
        for f in schema.FIELD_ORDER:
            if f in schema.METRIC_NAME_EXCEPTIONS:
                continue
            for tok in schema.METRIC_NAME_TOKENS:
                self.assertNotIn(tok, f.lower(), "field %r is named for a metric" % f)

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


class TestTheLaw(unittest.TestCase):
    """Structural checks that the constitution holds in the source, not just in the prose."""

    def test_no_llm_or_network_imports_anywhere(self):
        banned = ("anthropic", "openai", "urllib.request", "requests", "http.client", "socket")
        files = [os.path.join(FLIGHT_DIR, f) for f in ("schema.py", "tape.py")]
        files += [os.path.join(BIN, f) for f in os.listdir(BIN)]
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
