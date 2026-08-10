"""The synced triad — dataclass, JSON schema, and prompt block in ONE module.

Spec A § 3. Drift between what the code ACCEPTS and what the prompt PROMISES is
the first bug this architecture exists to kill, so all three faces are generated
from a single `_FIELDS` table and `tests/test_envelope_triad.py` asserts they
agree field-for-field.

If you add a field: add it to `_FIELDS` AND to the dataclass. The triad test
fails loudly if you do only one.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, fields as dc_fields
from typing import Any

ENVELOPE_STATUSES = ("PASS", "FAIL", "PARTIAL")


class EnvelopeError(ValueError):
    """Raised when a worker's envelope cannot be parsed or fails validation."""


@dataclass(frozen=True)
class FieldSpec:
    name: str
    json_type: str
    required: bool
    description: str
    enum: tuple[str, ...] | None = None
    item_type: str | None = None


# ---------------------------------------------------------------------------
# THE SINGLE SOURCE OF TRUTH
# ---------------------------------------------------------------------------
_FIELDS: tuple[FieldSpec, ...] = (
    FieldSpec(
        name="status",
        json_type="string",
        required=True,
        description=(
            "PASS if the phase's target state was reached and you verified it; "
            "FAIL if it was not; PARTIAL if some declared work landed and some "
            "did not. Claiming PASS with red gates makes the phase red anyway "
            "(verdict_consistent) -- an honest FAIL costs less than a caught PASS."
        ),
        enum=ENVELOPE_STATUSES,
    ),
    FieldSpec(
        name="summary",
        json_type="string",
        required=True,
        description=(
            "What you did and what you verified, in prose. Name the numbers you "
            "reproduced from artifacts, not the numbers you were told."
        ),
    ),
    FieldSpec(
        name="artifacts",
        json_type="array",
        required=True,
        description=(
            "Every file you created or modified, as repo-relative paths. This "
            "list is checked against the actual git change-set (diff_matches_claims): "
            "an unclaimed write is a red, and a claimed file that does not exist "
            "is a red."
        ),
        item_type="string",
    ),
    FieldSpec(
        name="notes_for_next_agent",
        json_type="string",
        required=True,
        description=(
            "What the next phase needs and cannot derive from the artifacts: "
            "boundaries you found, assumptions you had to make, anything you "
            "named-absent. Empty string is allowed but rarely honest."
        ),
    ),
)

_FIELD_NAMES: tuple[str, ...] = tuple(f.name for f in _FIELDS)


@dataclass
class EnvelopeBase:
    """The seam envelope every phase emits. Field list is triad-locked to `_FIELDS`."""

    status: str
    summary: str
    artifacts: list[str] = field(default_factory=list)
    notes_for_next_agent: str = ""

    # -- construction ------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnvelopeBase":
        if not isinstance(data, dict):
            raise EnvelopeError(f"envelope must be a JSON object, got {type(data).__name__}")
        missing = [f.name for f in _FIELDS if f.required and f.name not in data]
        if missing:
            raise EnvelopeError(f"envelope missing required field(s): {', '.join(missing)}")
        unknown = [k for k in data if k not in _FIELD_NAMES]
        if unknown:
            raise EnvelopeError(f"envelope carries unknown field(s): {', '.join(sorted(unknown))}")

        status = data["status"]
        if status not in ENVELOPE_STATUSES:
            raise EnvelopeError(
                f"envelope status {status!r} not one of {'/'.join(ENVELOPE_STATUSES)}"
            )
        summary = data["summary"]
        if not isinstance(summary, str):
            raise EnvelopeError("envelope summary must be a string")
        artifacts = data["artifacts"]
        if not isinstance(artifacts, list) or not all(isinstance(a, str) for a in artifacts):
            raise EnvelopeError("envelope artifacts must be a list of strings")
        notes = data.get("notes_for_next_agent", "")
        if not isinstance(notes, str):
            raise EnvelopeError("envelope notes_for_next_agent must be a string")
        return cls(
            status=status,
            summary=summary,
            artifacts=list(artifacts),
            notes_for_next_agent=notes,
        )

    @classmethod
    def from_json(cls, text: str) -> "EnvelopeBase":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover - message pass-through
            raise EnvelopeError(f"envelope is not valid JSON: {exc}") from exc
        return cls.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in _FIELDS}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=False)

    @property
    def claims_pass(self) -> bool:
        return self.status == "PASS"


# ---------------------------------------------------------------------------
# Face 2 — the JSON schema
# ---------------------------------------------------------------------------
def envelope_json_schema() -> dict[str, Any]:
    props: dict[str, Any] = {}
    for f in _FIELDS:
        prop: dict[str, Any] = {"type": f.json_type, "description": f.description}
        if f.enum:
            prop["enum"] = list(f.enum)
        if f.item_type:
            prop["items"] = {"type": f.item_type}
        props[f.name] = prop
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "EnvelopeBase",
        "type": "object",
        "additionalProperties": False,
        "required": [f.name for f in _FIELDS if f.required],
        "properties": props,
    }


# ---------------------------------------------------------------------------
# Face 3 — the prompt block a worker actually reads
# ---------------------------------------------------------------------------
_PROMPT_HEADER = """\
## Envelope — how you report back (REQUIRED)

End your reply with exactly one fenced ```json block containing your envelope.
Nothing after it. These fields, no others:
"""

_PROMPT_FOOTER = """\
Gates run AFTER you stop, against the files on disk -- never against this
envelope's word. Do not describe work you did not verify.
"""


def envelope_prompt_block() -> str:
    lines = [_PROMPT_HEADER]
    for f in _FIELDS:
        type_note = f.json_type
        if f.enum:
            type_note = " | ".join(f.enum)
        elif f.item_type:
            type_note = f"array of {f.item_type}"
        req = "required" if f.required else "optional"
        lines.append(f"- `{f.name}` ({type_note}, {req}) -- {f.description}")
    example = {
        "status": "PASS",
        "summary": "…",
        "artifacts": ["path/one.py"],
        "notes_for_next_agent": "…",
    }
    lines.append("\nExample shape:\n```json\n" + json.dumps(example, indent=2) + "\n```\n")
    lines.append(_PROMPT_FOOTER)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Extraction from worker output
# ---------------------------------------------------------------------------
_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def extract_envelope(raw_text: str) -> EnvelopeBase:
    """Pull the envelope out of a worker's final message.

    Order: last fenced json block, then a whole-text JSON parse. If neither
    yields a valid envelope the caller gets an EnvelopeError -- and the phase
    stays FAILED, which is the correct default.
    """
    if raw_text is None:
        raise EnvelopeError("no worker output to extract an envelope from")
    blocks = _FENCE_RE.findall(raw_text)
    errors: list[str] = []
    for block in reversed(blocks):
        try:
            return EnvelopeBase.from_json(block)
        except EnvelopeError as exc:
            errors.append(str(exc))
    stripped = raw_text.strip()
    if stripped.startswith("{"):
        try:
            return EnvelopeBase.from_json(stripped)
        except EnvelopeError as exc:
            errors.append(str(exc))
    detail = "; ".join(errors) if errors else "no JSON object found in worker output"
    raise EnvelopeError(f"could not extract an envelope: {detail}")


def field_names() -> tuple[str, ...]:
    return _FIELD_NAMES


def dataclass_field_names() -> tuple[str, ...]:
    return tuple(f.name for f in dc_fields(EnvelopeBase))
