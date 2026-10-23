"""Assign a trial to a condition group from the trial's own list of conditions (not from which search found it)."""

from __future__ import annotations

import re

NOT_THIS_DISEASE = re.compile(r"pulmonary|portal|ocular|intraocular|intracranial|pre-?eclampsia|gestation|pregnan|renovascular|retinopath|neonat", re.I)
RULES = [
    ("heart_failure", re.compile(r"heart failure|cardiac failure|\bhfref\b|\bhfpef\b|congestive", re.I)),
    ("stroke", re.compile(r"stroke|cerebral infarct|cerebrovascular|brain ischemi|brain ischaemi|transient ischemic|transient ischaemic", re.I)),
    ("coronary", re.compile(r"coronary|myocardial infarct|heart attack|angina|\bstemi\b|\bnstemi\b|ischemic heart|ischaemic heart", re.I)),
    ("hypertension", re.compile(r"hypertension|high blood pressure|hypertensive", re.I)),
]
OWN_CONDITION_VARIABLES = {
    "heart_failure": {"heart_failure"}, "hypertension": {"hypertension"}, "coronary": {"chd_or_angina", "prior_mi"}, "stroke": {"prior_stroke"},
}


def groups_of(conditions: list[str]) -> list[str]:
    """Groups matched by any listed condition, in the order the trial lists them (first match per condition)."""
    out: list[str] = []
    for c in conditions or []:
        if NOT_THIS_DISEASE.search(c):
            continue
        for name, rx in RULES:
            if rx.search(c):
                if name not in out:
                    out.append(name)
                break
    return out


def primary_group(conditions: list[str]) -> str | None:
    g = groups_of(conditions)
    return g[0] if g else None
