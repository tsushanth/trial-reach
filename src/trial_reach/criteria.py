"""Eligibility-criteria extraction: prompt, strict parser and the frozen computable-variable set.

No network and no data access here. The model call is injected by the caller, so tests run on invented text only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

VOCABULARY = (
    # measured by the survey (computable)
    "age", "sex", "pregnancy_or_lactation", "systolic_bp", "diastolic_bp", "bmi", "egfr_or_crcl", "serum_creatinine",
    "hba1c", "diabetes", "ldl_c", "total_cholesterol", "hdl_c", "triglycerides", "alt", "ast", "albumin", "platelets", "wbc",
    "uric_acid", "albuminuria", "potassium", "hemoglobin", "prior_mi", "prior_stroke", "heart_failure", "hypertension",
    "chd_or_angina", "copd_or_asthma", "current_smoking", "alcohol_use", "cancer_history", "dialysis", "kidney_failure",
    "liver_disease", "statin_use", "antihypertensive_use", "insulin_use",
    # not measured by the survey
    "nyha_class", "lvef", "atrial_fibrillation", "prior_hf_hospitalization", "life_expectancy", "anticoagulant_use",
    "procedure_or_device", "imaging_or_ecg_finding", "other_lab_value", "infection", "psychiatric_or_cognitive",
    "substance_use_disorder", "allergy_or_intolerance", "consent_or_compliance", "study_logistics", "other_drug_or_therapy",
    "other_condition", "other",
)
OPERATORS = (">=", ">", "<=", "<", "==", "!=", "present", "absent")
TYPES = ("inclusion", "exclusion")
COMPUTABLE = frozenset({
    "age", "sex", "pregnancy_or_lactation", "systolic_bp", "diastolic_bp", "bmi", "egfr_or_crcl", "serum_creatinine",
    "hba1c", "diabetes", "ldl_c", "total_cholesterol", "hdl_c", "triglycerides", "alt", "ast", "albumin", "platelets", "wbc",
    "uric_acid", "albuminuria", "potassium", "hemoglobin", "prior_mi", "prior_stroke", "heart_failure", "hypertension",
    "chd_or_angina", "copd_or_asthma", "current_smoking", "alcohol_use", "cancer_history", "dialysis", "kidney_failure",
    "liver_disease", "statin_use", "antihypertensive_use", "insulin_use",
})
THRESHOLD_OPS = frozenset({">=", ">", "<=", "<", "=="})

PROMPT_V1 = """Read the eligibility criteria of a clinical trial and list every requirement as a separate item.

Eligibility criteria:
<<<
{text}
>>>

For each requirement give:
- "type": "inclusion" or "exclusion", as the trial states it
- "variable": one of {variables} (use the most specific listed variable; "other" only as a last resort)
- "operator": one of {operators}
- "value": a number for threshold operators, otherwise null
- "unit": the unit as written, or null
Rules: split compound requirements; a range is two items; "not pregnant" is exclusion of pregnancy_or_lactation present;
when no listed variable fits, the variable must be exactly "other" (never invent a variable name); use "present" or "absent"
for requirements without a number; label only what the text says.

Reply with JSON only: {{"criteria": [{{"type": "...", "variable": "...", "operator": "...", "value": null, "unit": null}}]}}"""


SCHEMA = {
    "type": "object",
    "properties": {"criteria": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "type": {"enum": list(TYPES)},
            "variable": {"enum": list(VOCABULARY)},
            "operator": {"enum": list(OPERATORS)},
            "value": {"type": ["number", "null"]},
            "unit": {"type": ["string", "null"]},
        },
        "required": ["type", "variable", "operator", "value", "unit"],
    }}},
    "required": ["criteria"],
}


def prompt_hash(prompt: str = PROMPT_V1) -> str:
    """Hash of the prompt text and the decoding schema together: either changing is a new method version."""
    return hashlib.sha256((prompt + json.dumps(SCHEMA, sort_keys=True)).encode()).hexdigest()


def build_prompt(text: str, max_chars: int = 6000) -> str:
    text = (text or "").strip() or "(no eligibility text)"
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[truncated]"
    return PROMPT_V1.format(text=text, variables=", ".join(VOCABULARY), operators=", ".join(OPERATORS))


@dataclass(frozen=True)
class Criterion:
    type: str
    variable: str
    operator: str
    value: float | None
    unit: str | None
    variable_raw: str | None = None  # what the model wrote when it was outside the vocabulary (development diagnostics)

    @property
    def computable(self) -> bool:
        """Computable only if the variable is in the frozen set and a threshold operator has a usable number."""
        if self.variable not in COMPUTABLE:
            return False
        return self.operator not in THRESHOLD_OPS or self.value is not None


def parse(raw: str) -> tuple[list[Criterion] | None, int]:
    """(criteria, dropped). criteria is None if the output is unreadable.

    Rule (decided on development data, 2026-10-22): an item with a valid type is never discarded for an out-of-vocabulary
    variable or an unusable operator or value. It is kept as variable "other" (or kept with value None), which makes it
    not computable, so it stays in the denominator of the computable fraction. Only items with an invalid type or that are
    not objects are dropped, and those are counted."""
    i, j = raw.find("{"), raw.rfind("}")
    if i < 0 or j < i:
        return None, 0
    try:
        d = json.loads(raw[i : j + 1])
    except json.JSONDecodeError:
        return None, 0
    items = d.get("criteria") if isinstance(d, dict) else None
    if not isinstance(items, list):
        return None, 0
    out, dropped = [], 0
    for c in items:
        if not isinstance(c, dict):
            dropped += 1
            continue
        t, v, op = str(c.get("type", "")).lower(), str(c.get("variable", "")).lower(), str(c.get("operator", "")).lower()
        val = c.get("value")
        if t not in TYPES:
            dropped += 1
            continue
        raw_var = None
        if v not in VOCABULARY:
            raw_var, v, op, val = v, "other", "present", None
        elif op not in OPERATORS:
            op, val = "present", None
        if op in THRESHOLD_OPS:
            val = float(val) if isinstance(val, (int, float)) and not isinstance(val, bool) else None
        else:
            val = None
        unit = c.get("unit")
        out.append(Criterion(t, v, op, val, str(unit) if unit not in (None, "") else None, raw_var))
    return out, dropped


def computable_fraction(criteria: list[Criterion]) -> float | None:
    return None if not criteria else sum(c.computable for c in criteria) / len(criteria)


def extract(text: str, llm) -> tuple[list[Criterion] | None, int]:
    """llm: callable(prompt) -> raw string. Backend failures propagate to the caller, who records them."""
    return parse(llm(build_prompt(text)))
