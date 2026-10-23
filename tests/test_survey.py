import numpy as np
import pandas as pd
import pytest

from trial_reach import survey as sv


def test_ckd_epi_2021_matches_hand_calculation():
    e = sv.ckd_epi_2021(pd.Series([1.0, 0.9]), pd.Series([60.0, 50.0]), pd.Series([1.0, 0.0]))
    assert e.iloc[0] == pytest.approx(64.5, abs=0.6) and e.iloc[1] == pytest.approx(104.0, abs=0.6)


def frame(n=40):
    rng = np.random.default_rng(0)
    d = pd.DataFrame({"SEQN": range(n), "age": rng.integers(18, 81, n).astype(float), "female": rng.integers(0, 2, n).astype(float),
                      "w_mec": rng.uniform(1000, 3000, n), "w_fast": rng.uniform(1000, 3000, n),
                      "psu": np.tile([1, 2], n // 2), "strata": np.repeat(np.arange(n // 4), 4)})
    d["egfr_or_crcl"] = rng.uniform(20, 120, n)
    d["hba1c"] = rng.uniform(4.5, 10, n)
    d["prior_stroke"] = (d.index % 5 == 0).astype(float)
    d["heart_failure"] = (d.index % 3 == 0).astype(float)
    d["hypertension"] = 1.0
    d["chd_or_angina"] = 0.0
    d["prior_mi"] = 0.0
    d["pregnant"] = 0.0
    d["diabetes"] = (d.hba1c >= 6.5).astype(float)
    return d


def test_unit_conversion_and_plausibility():
    assert sv.convert_value("serum_creatinine", 177, "umol/L") == pytest.approx(2.0, abs=0.01)
    assert sv.convert_value("hba1c", 53, "mmol/mol") == pytest.approx(7.0, abs=0.05)
    assert sv.convert_value("hba1c", 53, "%") is None  # 53 percent is not a believable HbA1c
    assert sv.convert_value("platelets", 100000, "cells/mm3") == 100.0
    assert sv.convert_value("egfr_or_crcl", 30, "mL/min") == 30.0


def test_translate_categorical_numeric_and_untranslatable():
    d = frame()
    f, w = sv.translate(d, "prior_stroke", "absent", None, None)
    assert (f == 1 - d.prior_stroke).all() and w == "w_mec"
    f, w = sv.translate(d, "egfr_or_crcl", "<", 30.0, "mL/min")
    assert (f == (d.egfr_or_crcl < 30).astype(float)).all()
    assert sv.translate(d, "lvef", "<", 35.0, "%") is None and sv.translate(d, "alcohol_use", "present", None, None) is None
    assert sv.translate(d, "hba1c", ">", 53.0, "%") is None
    assert sv.translate(d, "ldl_c", ">", 100.0, "mg/dL") is None  # column not present in this frame


def test_age_top_coding_leaves_over_80_unresolved():
    d = frame()
    d.loc[0, "age"] = 80.0
    f, _ = sv.translate(d, "age", ">", 85.0, "years")
    assert np.isnan(f.iloc[0])


def test_fails_direction_and_weighted_share():
    d = frame()
    flag = pd.Series([1.0, 0.0] * 20)
    assert (sv.fails(d, "inclusion", flag) == 1 - flag).all() and (sv.fails(d, "exclusion", flag) == flag).all()
    d["w_mec"] = 1.0
    r = sv.weighted_share(d, flag, pd.Series(True, index=d.index), "w_mec")
    assert r["p"] == pytest.approx(0.5) and r["n"] == 40 and r["se"] > 0
    r2 = sv.weighted_share(d, flag, d.heart_failure == 1, "w_mec")
    assert r2["n"] == int((d.heart_failure == 1).sum())


def test_standard_error_matches_simple_case():
    # two strata, two PSUs each, equal weights: p = mean of y; linearised variance equals sum over strata of n/(n-1) * sum (z_j - mean z)^2
    d = pd.DataFrame({"w": [1.0] * 8, "psu": [1, 1, 2, 2, 1, 1, 2, 2], "strata": [1] * 4 + [2] * 4})
    y = pd.Series([1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
    r = sv.weighted_share(d, y, pd.Series(True, index=d.index), "w")
    assert r["p"] == pytest.approx(3 / 8)
    z = (y - 3 / 8) / 8
    sums = pd.DataFrame({"s": d.strata, "p": d.psu, "z": z}).groupby(["s", "p"]).z.sum()
    expect = sum(2 / 1 * ((sums[s] - sums[s].mean()) ** 2).sum() for s in (1, 2))
    assert r["se"] == pytest.approx(np.sqrt(expect))


def test_burden_end_to_end_and_derive_minimal():
    d = frame()
    r = sv.burden(d, "stroke", "exclusion", "egfr_or_crcl", "<", 30.0, "mL/min")
    assert r["domain_n"] == int((d.prior_stroke == 1).sum()) and 0 <= r["p"] <= 1 and r["missing_in_domain"] == 0
    assert sv.burden(d, "stroke", "exclusion", "lvef", "<", 35.0, "%") is None
    demo = pd.DataFrame({"SEQN": [1, 2, 3], "RIDAGEYR": [60, 15, 45], "RIAGENDR": [2, 1, 1], "RIDEXPRG": [np.nan] * 3,
                         "WTMECPRP": [100.0, 100.0, 0.0], "SDMVPSU": [1, 2, 1], "SDMVSTRA": [1, 1, 1]})
    mcq = pd.DataFrame({"SEQN": [1, 2, 3], "MCQ160B": [1, 2, 1], "MCQ160E": [2, 2, 2], "MCQ160F": [2, 2, 2], "MCQ160C": [2, 2, 2], "MCQ160D": [2, 2, 2]})
    out = sv.derive({"DEMO": demo, "MCQ": mcq})
    assert list(out.SEQN) == [1] and out.heart_failure.iloc[0] == 1.0  # child and zero-weight person removed
