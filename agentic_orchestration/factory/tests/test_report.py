"""Tier-0 rendering — the surface where a number acquires a meaning.

One rule is under test here, and it is the one the O4 probe made load-bearing: a
dollar figure is rendered with the provenance the RECEIPT recorded, never with a
caveat the renderer assumed. On a subscription lane the harness reports a
plausible-looking `total_cost_usd` that was never billed to anyone; a surface that
prints it unlabelled manufactures a spending claim out of nothing.
"""

from factory.report import _dollars_line
from factory.usage import DOLLARS_HARNESS_IMPUTED


def _totals(dollars, sources):
    return {"dollars": dollars, "dollars_sources": sources}


def test_a_null_figure_says_no_lane_priced_the_run():
    assert "NULL" in _dollars_line(_totals(None, []))


def test_the_subscription_caveat_comes_from_the_recorded_source():
    line = _dollars_line(_totals(0.0672, [DOLLARS_HARNESS_IMPUTED]))
    assert "$0.0672" in line
    assert "NOT a billed amount" in line


def test_a_figure_with_no_recorded_provenance_is_refused_a_meaning():
    """The falsification partner. The v1 renderer hard-coded the subscription
    caveat, so an unlabelled figure would have been dressed as one anyway (D-4)."""
    line = _dollars_line(_totals(9.99, []))
    assert "provenance unrecorded" in line
    assert "cannot be read as money spent" in line
    assert "subscription" not in line, "an unlabelled figure must not inherit a caveat"


def test_an_unregistered_source_is_printed_raw_not_guessed_at():
    line = _dollars_line(_totals(1.0, ["metered_api_billed"]))
    assert "metered_api_billed" in line
    assert "no gloss registered" in line
    assert "NOT a billed amount" not in line, "a new lane must not inherit the old caveat"


def test_two_lanes_both_travel():
    line = _dollars_line(_totals(1.0, [DOLLARS_HARNESS_IMPUTED, "metered_api_billed"]))
    assert "NOT a billed amount" in line and "metered_api_billed" in line
