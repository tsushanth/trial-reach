"""Survey side of the trial-reach analysis: derive person-level variables from NHANES-style component tables, translate structured
trial criteria into per-person flags, and estimate design-based exclusion burden.

Pure functions on pandas data frames. The directory of survey files is supplied by the caller. Nothing about where the files live is stored here.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

FASTING_VARS = {"ldl_c", "triglycerides"}

# value ranges that make a unit-converted number believable; outside them the criterion is not translated
PLAUSIBLE = {
    "age": (18, 120), "systolic_bp": (60, 260), "diastolic_bp": (30, 150), "bmi": (10, 80), "egfr_or_crcl": (3, 200),
    "serum_creatinine": (0.1, 15), "hba1c": (3, 20), "ldl_c": (20, 400), "total_cholesterol": (50, 500), "hdl_c": (10, 150),
    "triglycerides": (20, 2000), "alt": (3, 1500), "ast": (3, 1500), "albumin": (1, 6), "potassium": (2, 8), "uric_acid": (1, 15),
    "albuminuria": (1, 5000), "platelets": (10, 1500), "wbc": (1, 100), "hemoglobin": (4, 20),
}


def yn(s: pd.Series) -> pd.Series:
    """Survey yes/no coding: 1 yes, 2 no; anything else (refused, don't know, not asked) is missing."""
    return pd.Series(np.where(s == 1, 1.0, np.where(s == 2, 0.0, np.nan)), index=s.index)


def ckd_epi_2021(creat_mg_dl: pd.Series, age: pd.Series, female: pd.Series) -> pd.Series:
    kappa = np.where(female == 1, 0.7, 0.9)
    alpha = np.where(female == 1, -0.241, -0.302)
    r = creat_mg_dl / kappa
    return 142 * np.minimum(r, 1) ** alpha * np.maximum(r, 1) ** -1.200 * 0.9938 ** age * np.where(female == 1, 1.012, 1.0)


def derive(t: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """t maps component names (DEMO, BPXO, BMX, BIOPRO, GHB, TCHOL, HDL, TRIGLY, CBC, ALB_CR, MCQ, BPQ, DIQ, SMQ, KIQ_U) to tables with SEQN.
    Missing components are allowed (their variables become missing)."""
    df = t["DEMO"][["SEQN", "RIDAGEYR", "RIAGENDR", "RIDEXPRG", "WTMECPRP", "SDMVPSU", "SDMVSTRA"]].copy()
    for name, tab in t.items():
        if name != "DEMO":
            df = df.merge(tab, on="SEQN", how="left", suffixes=("", f"_{name}"))
    g = lambda c: df[c] if c in df else pd.Series(np.nan, index=df.index)
    d = pd.DataFrame({"SEQN": df.SEQN, "age": g("RIDAGEYR"), "female": (g("RIAGENDR") == 2).astype(float), "w_mec": g("WTMECPRP"),
                      "w_fast": g("WTSAFPRP"), "psu": g("SDMVPSU"), "strata": g("SDMVSTRA")})
    d["pregnant"] = np.where(g("RIAGENDR") == 2, np.where(g("RIDEXPRG") == 1, 1.0, np.where(g("RIDEXPRG").isin([2, 3]), 0.0, np.nan)), 0.0)
    d["systolic_bp"] = df[[c for c in ("BPXOSY1", "BPXOSY2", "BPXOSY3") if c in df]].mean(axis=1, skipna=True) if "BPXOSY1" in df else np.nan
    d["diastolic_bp"] = df[[c for c in ("BPXODI1", "BPXODI2", "BPXODI3") if c in df]].mean(axis=1, skipna=True) if "BPXODI1" in df else np.nan
    d["bmi"] = g("BMXBMI")
    d["serum_creatinine"] = g("LBXSCR")
    d["egfr_or_crcl"] = ckd_epi_2021(d["serum_creatinine"], d["age"], d["female"])
    for out, col in (("hba1c", "LBXGH"), ("ldl_c", "LBDLDL"), ("total_cholesterol", "LBXTC"), ("hdl_c", "LBDHDD"), ("triglycerides", "LBXTR"),
                     ("alt", "LBXSATSI"), ("ast", "LBXSASSI"), ("albumin", "LBXSAL"), ("potassium", "LBXSKSI"), ("uric_acid", "LBXSUA"),
                     ("albuminuria", "URDACT"), ("platelets", "LBXPLTSI"), ("wbc", "LBXWBCSI"), ("hemoglobin", "LBXHGB")):
        d[out] = g(col)
    # questionnaire flags
    d["heart_failure"] = yn(g("MCQ160B"))
    d["prior_mi"] = yn(g("MCQ160E"))
    d["prior_stroke"] = yn(g("MCQ160F"))
    chd, ang = yn(g("MCQ160C")), yn(g("MCQ160D"))
    d["chd_or_angina"] = np.fmax(chd, ang)
    d["cancer_history"] = yn(g("MCQ220"))
    d["liver_disease"] = yn(g("MCQ160L"))
    d["copd_or_asthma"] = np.fmax(yn(g("MCQ160P")), yn(g("MCQ035")))
    d["current_smoking"] = pd.Series(np.where(g("SMQ040").isin([1, 2]), 1.0, np.where(g("SMQ040") == 3, 0.0, np.where(g("SMQ020") == 2, 0.0, np.nan))), index=df.index)
    d["dialysis"] = yn(g("KIQ025"))
    d["kidney_failure"] = yn(g("KIQ022"))
    told_htn, on_bp = yn(g("BPQ020")), yn(g("BPQ050A")).fillna(0.0)
    measured = ((d.systolic_bp >= 140) | (d.diastolic_bp >= 90)).astype(float).where(d.systolic_bp.notna() | d.diastolic_bp.notna())
    d["hypertension"] = pd.concat([told_htn, on_bp.where(on_bp == 1), measured], axis=1).max(axis=1, skipna=True).where(told_htn.notna() | measured.notna())
    d["antihypertensive_use"] = on_bp
    d["statin_use"] = yn(g("BPQ100D")).fillna(0.0)
    d["insulin_use"] = yn(g("DIQ050")).fillna(0.0)
    told_dm = yn(g("DIQ010"))
    dm_lab = (d.hba1c >= 6.5).astype(float).where(d.hba1c.notna())
    d["diabetes"] = pd.concat([told_dm, dm_lab], axis=1).max(axis=1, skipna=True).where(told_dm.notna() | dm_lab.notna())
    d["albuminuria_present"] = (d.albuminuria >= 30).astype(float).where(d.albuminuria.notna())
    return d[(d.age >= 18) & d.w_mec.notna() & (d.w_mec > 0)].reset_index(drop=True)


GROUPS = {
    "heart_failure": lambda d: d.heart_failure == 1,
    "hypertension": lambda d: d.hypertension == 1,
    "coronary": lambda d: (d.chd_or_angina == 1) | (d.prior_mi == 1),
    "stroke": lambda d: d.prior_stroke == 1,
}

CATEGORICAL = {  # variable -> column holding a 1/0/NaN flag
    "pregnancy_or_lactation": "pregnant", "diabetes": "diabetes", "prior_mi": "prior_mi", "prior_stroke": "prior_stroke",
    "heart_failure": "heart_failure", "hypertension": "hypertension", "chd_or_angina": "chd_or_angina", "copd_or_asthma": "copd_or_asthma",
    "current_smoking": "current_smoking", "cancer_history": "cancer_history", "dialysis": "dialysis", "kidney_failure": "kidney_failure",
    "liver_disease": "liver_disease", "statin_use": "statin_use", "antihypertensive_use": "antihypertensive_use", "insulin_use": "insulin_use",
    "albuminuria": "albuminuria_present",
}
NUMERIC = {"age", "systolic_bp", "diastolic_bp", "bmi", "egfr_or_crcl", "serum_creatinine", "hba1c", "ldl_c", "total_cholesterol", "hdl_c",
           "triglycerides", "alt", "ast", "albumin", "potassium", "uric_acid", "platelets", "wbc", "hemoglobin"}
OPS = {">=": lambda a, b: a >= b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b, "<": lambda a, b: a < b, "==": lambda a, b: a == b}


def convert_value(variable: str, value: float, unit: str | None) -> float | None:
    """Value in the survey's unit, or None if the unit or magnitude is not believable for this variable."""
    u = (unit or "").lower().replace("µ", "u").replace("μ", "u").replace(" ", "")
    v = float(value)
    if variable == "serum_creatinine" and ("umol" in u or "micromol" in u):
        v = v / 88.4
    elif variable == "hba1c" and "mmol/mol" in u:
        v = 0.09148 * v + 2.152
    elif variable in ("ldl_c", "total_cholesterol", "hdl_c") and "mmol" in u:
        v = v * 38.67
    elif variable == "triglycerides" and "mmol" in u:
        v = v * 88.57
    elif variable in ("albumin", "hemoglobin") and ("g/l" in u and "dl" not in u):
        v = v / 10
    elif variable == "albuminuria" and "mg/mmol" in u:
        v = v * 8.84
    elif variable in ("platelets", "wbc") and v > 1000 and any(k in u for k in ("mm3", "/ul", "cells")):
        v = v / 1000
    elif variable == "potassium" and "meq" in u:
        pass  # mEq/L equals mmol/L for potassium
    lo, hi = PLAUSIBLE.get(variable, (-math.inf, math.inf))
    return v if lo <= v <= hi else None


def translate(d: pd.DataFrame, variable: str, operator: str, value: float | None, unit: str | None):
    """Per-person flag Series (1.0 true, 0.0 false, NaN missing) for the statement, plus which weight applies; None if not translatable."""
    w = "w_fast" if variable in FASTING_VARS else "w_mec"
    if variable in CATEGORICAL and operator in ("present", "absent") and CATEGORICAL[variable] in d.columns:
        f = d[CATEGORICAL[variable]]
        return (f if operator == "present" else 1 - f), w
    if variable in NUMERIC and operator in OPS and value is not None and variable in d.columns:
        v = convert_value(variable, value, unit)
        if v is None:
            return None
        col = d[variable]
        flag = OPS[operator](col, v).astype(float).where(col.notna())
        if variable == "age" and v >= 80:  # ages are top-coded at 80, so statements about 80 or older are not resolvable for those coded 80
            flag = flag.where(col < 80)
        return flag, w
    return None


def fails(d: pd.DataFrame, role: str, flag: pd.Series) -> pd.Series:
    """1.0 where a person fails the criterion (inclusion false or exclusion true), NaN where the measurement is missing."""
    return (1 - flag) if role == "inclusion" else flag


def weighted_share(d: pd.DataFrame, y: pd.Series, domain: pd.Series, weight: str) -> dict:
    """Domain proportion of y with Taylor-linearised standard error over PSUs within strata. Persons with missing y or weight are left out."""
    ok = domain & y.notna() & d[weight].notna() & (d[weight] > 0)
    w = d[weight].where(ok, 0.0)
    tot = w.sum()
    n = int(ok.sum())
    if n == 0 or tot == 0:
        return {"n": n, "p": None, "se": None}
    p = float((w * y.fillna(0.0)).sum() / tot)
    z = (w * (y.fillna(0.0) - p) / tot).where(ok, 0.0)
    g = pd.DataFrame({"strata": d.strata, "psu": d.psu, "z": z}).groupby(["strata", "psu"]).z.sum().reset_index()
    var = 0.0
    for _, h in g.groupby("strata"):
        nh = len(h)
        if nh > 1:
            var += nh / (nh - 1) * float(((h.z - h.z.mean()) ** 2).sum())
    return {"n": n, "p": p, "se": math.sqrt(var)}


def burden(d: pd.DataFrame, group: str, role: str, variable: str, operator: str, value: float | None, unit: str | None) -> dict | None:
    t = translate(d, variable, operator, value, unit)
    if t is None:
        return None
    flag, w = t
    dom = GROUPS[group](d)
    res = weighted_share(d, fails(d, role, flag), dom, w)
    res["domain_n"] = int(dom.sum())
    res["missing_in_domain"] = int((dom & flag.isna()).sum())
    return res
