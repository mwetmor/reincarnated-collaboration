"""The synced-triad test — Spec A § 3, acceptance item 4 (first half).

Dataclass, JSON schema, and prompt block must agree FIELD-FOR-FIELD. Drift
between what the code accepts and what the prompt promises is the first bug the
architecture exists to kill, so it is the first thing tested.
"""

from factory.envelope import (
    ENVELOPE_STATUSES,
    EnvelopeBase,
    EnvelopeError,
    dataclass_field_names,
    envelope_json_schema,
    envelope_prompt_block,
    extract_envelope,
    field_names,
)

import pytest


def test_dataclass_matches_the_field_table():
    assert dataclass_field_names() == field_names()


def test_json_schema_matches_the_field_table():
    schema = envelope_json_schema()
    assert tuple(schema["properties"]) == field_names()
    assert schema["additionalProperties"] is False
    assert tuple(schema["required"]) == field_names()
    assert schema["properties"]["status"]["enum"] == list(ENVELOPE_STATUSES)
    assert schema["properties"]["artifacts"]["items"]["type"] == "string"


def test_prompt_block_names_every_field_and_no_others():
    block = envelope_prompt_block()
    for name in field_names():
        assert f"`{name}`" in block, f"prompt block never mentions {name}"
    # The example object in the prompt must itself be a valid envelope.
    example = extract_envelope(block)
    assert set(example.to_dict()) == set(field_names())


def test_prompt_block_promises_the_statuses_the_code_accepts():
    block = envelope_prompt_block()
    for status in ENVELOPE_STATUSES:
        assert status in block


def test_triad_drift_would_be_caught():
    """Falsification: a field the dataclass has but the table lacks must fail the test.

    Simulated by comparing against a deliberately-short field list -- the same
    comparison the three tests above make, shown here to red on drift.
    """
    drifted = tuple(f for f in field_names() if f != "notes_for_next_agent")
    assert dataclass_field_names() != drifted


def test_unknown_field_is_rejected():
    with pytest.raises(EnvelopeError, match="unknown field"):
        EnvelopeBase.from_dict(
            {
                "status": "PASS",
                "summary": "s",
                "artifacts": [],
                "notes_for_next_agent": "",
                "cost_estimate": 12,
            }
        )


def test_bad_status_is_rejected():
    with pytest.raises(EnvelopeError, match="not one of"):
        EnvelopeBase.from_dict(
            {"status": "GREEN", "summary": "s", "artifacts": [], "notes_for_next_agent": ""}
        )


def test_missing_required_field_is_rejected():
    with pytest.raises(EnvelopeError, match="missing required"):
        EnvelopeBase.from_dict({"status": "PASS", "summary": "s"})


def test_extract_takes_the_last_fenced_block():
    text = (
        "thinking out loud\n"
        '```json\n{"status": "FAIL", "summary": "first", "artifacts": [], '
        '"notes_for_next_agent": ""}\n```\n'
        "then I fixed it\n"
        '```json\n{"status": "PASS", "summary": "second", "artifacts": ["a.txt"], '
        '"notes_for_next_agent": "n"}\n```\n'
    )
    env = extract_envelope(text)
    assert env.summary == "second"
    assert env.artifacts == ["a.txt"]


def test_extract_refuses_prose():
    with pytest.raises(EnvelopeError):
        extract_envelope("I did the thing. It went well, I think.")
