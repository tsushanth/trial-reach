import numpy as np
import pandas as pd
import pytest

from trial_reach import analysis as an
from trial_reach import survey as sv


def frame():
    n = 8
    return pd.DataFrame({"age": [30, 50, 60, 70, 75, 80, 45, 55.0], "egfr_or_crcl": [90, 25, 40, 28, 100, 60, np.nan, 80.0],
                         "prior_stroke": [1.0] * 8, "heart_failure": [0.0] * 8, "hypertension": [1.0] * 8, "chd_or_angina": [0.0] * 8, "prior_mi": [0.0] * 8,
                         "w_mec": [1.0] * 8, "w_fast": [1.0] * 8, "psu": [1, 2] * 4, "strata": [1, 1, 2, 2, 3, 3, 4, 4]})


def test_keys_periods_and_single_burden():
    assert an.criterion_key("exclusion", "age", ">", 75, "years") == ("exclusion", "age", ">", 75.0, "years")
    assert an.period("2012-03") == "2010-2014" and an.period("1999") is None and an.period(None) is None
    ev = an.Evaluator(frame())
    r = ev.single_burden("stroke", an.criterion_key("exclusion", "egfr_or_crcl", "<", 30, "ml/min"))
    assert r["n"] == 7 and r["p"] == pytest.approx(2 / 7)  # two of seven measured people are under 30; the missing one is left out
    assert ev.single_burden("stroke", an.criterion_key("exclusion", "lvef", "<", 35, "%")) is None


def test_trial_lower_bound_combines_criteria_and_ignores_missing():
    ev = an.Evaluator(frame())
    crit = [{"type": "exclusion", "variable": "age", "operator": ">", "value": 75, "unit": "years"},
            {"type": "exclusion", "variable": "egfr_or_crcl", "operator": "<", "value": 30, "unit": "mL/min"},
            {"type": "inclusion", "variable": "lvef", "operator": "<=", "value": 40, "unit": "%"}]
    s = an.trial_summary(ev, "stroke", crit)
    # age > 75 fails for the 80-year-old (age 80 is top-coded so a statement about 75 is resolved normally); eGFR < 30 fails for two people
    assert s["n_criteria"] == 3 and s["n_translatable"] == 2 and s["translatable_fraction"] == pytest.approx(2 / 3)
    assert s["lower_bound_burden"] == pytest.approx(3 / 8) and s["n_combined"] == 2
    empty = an.trial_summary(ev, "stroke", [crit[2]])
    assert empty["lower_bound_burden"] is None and empty["n_combined"] == 0


def test_anyfail_and_subgroup_means():
    ev = an.Evaluator(frame())
    k = an.criterion_key("exclusion", "age", ">", 60, "years")
    arr, n = ev.anyfail([k])
    assert n == 1 and list(arr) == [0, 0, 0, 1, 1, 1, 0, 0]
    d = ev.d
    assert ev.weighted_mean(arr, (d.age >= 65).to_numpy().astype(float)) == pytest.approx(1.0)
    assert ev.weighted_mean(arr, (d.age < 65).to_numpy().astype(float)) == pytest.approx(0.0)
    assert ev.anyfail([an.criterion_key("exclusion", "lvef", "<", 35, "%")]) == (None, 0)
