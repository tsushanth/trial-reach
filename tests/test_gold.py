import json

from trial_reach import gold

TEXT = "Inclusion Criteria:\n* Age >= 18\n\nExclusion Criteria:\n* Prior stroke\n* Willing to consent\n"


def test_prompt_numbers_lines_with_roles_and_keeps_pipeline_out():
    system, user, lines = gold.build_gold_prompt(TEXT)
    assert user.splitlines() == ["1. [inclusion] Age >= 18", "2. [exclusion] Prior stroke", "3. [exclusion] Willing to consent"]
    assert "pipeline" not in system.lower() and len(lines) == 3


def test_parse_requires_every_line_once_in_order():
    _, _, lines = gold.build_gold_prompt(TEXT)
    ok = {"lines": [{"n": 1, "items": [{"variable": "age", "operator": ">=", "value": 18, "unit": "years"}]},
                    {"n": 2, "items": [{"variable": "prior_stroke", "operator": "present", "value": None, "unit": None}]},
                    {"n": 3, "items": []}]}
    got = gold.parse_gold(json.dumps(ok), lines)
    assert got[0] == {("inclusion", "age", ">=", 18.0)} and got[1] == {("exclusion", "prior_stroke", "present", None)} and got[2] == set()
    bad = {"lines": ok["lines"][:2]}
    assert gold.parse_gold(json.dumps(bad), lines) is None and gold.parse_gold("nope", lines) is None
    swapped = {"lines": [ok["lines"][1], ok["lines"][0], ok["lines"][2]]}
    assert gold.parse_gold(json.dumps(swapped), lines) is None


def test_scoring_counts_only_computable_and_bootstrap_runs():
    g = {("inclusion", "age", ">=", 18.0), ("exclusion", "lvef", "<", 35.0), ("exclusion", "prior_stroke", "present", None)}
    p = {("inclusion", "age", ">=", 18.0), ("exclusion", "prior_stroke", "absent", None), ("exclusion", "lvef", "<", 30.0)}
    assert gold.score_trial(g, p) == (1, 1, 1)  # lvef is not computable, so ignored; the stroke polarity is wrong
    assert gold.score_trial(g, p, computable_only=False) == (1, 2, 2)
    res = gold.bootstrap_f1([(5, 1, 1)] * 10 + [(4, 0, 2)] * 10, n_boot=200)
    assert 0.7 < res["f1"] < 0.9 and res["ci"][0] <= res["f1"] <= res["ci"][1]
    assert gold.prf(0, 0, 0) == (None, None, None)
