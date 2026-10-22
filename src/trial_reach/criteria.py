"""Eligibility-criteria extraction: prompt, strict parser and the frozen computable-variable set.

No network and no data access here. The model call is injected by the caller, so tests run on invented text only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

VOCABULARY = (
    "age", "sex", "pregnancy_or_lactation", "systolic_bp", "diastolic_bp", "bmi", "egfr_or_crcl", "serum_creatinine",
    "hba1c", "diabetes", "ldl_c", "potassium", "hemoglobin", "nyha_class", "lvef", "prior_mi", "prior_stroke",
    "prior_hf_hospitalization", "atrial_fibrillation", "current_smoking", "cancer_history", "dialysis", "liver_disease",
    "anticoagulant_use", "life_expectancy", "other",
)
OPERATORS = (">=", ">", "<=", "<", "==", "!=", "present", "absent")
TYPES = ("inclusion", "exclusion")
COMPUTABLE = frozenset({
    "age", "sex", "pregnancy_or_lactation", "systolic_bp", "diastolic_bp", "bmi", "serum_creatinine", "egfr_or_crcl",
    "hba1c", "diabetes", "ldl_c", "potassium", "hemoglobin", "prior_mi", "prior_stroke", "current_smoking",
    "cancer_history", "dialysis", "liver_disease",
})
THRESHOLD_OPS = frozenset({">=", ">", "<=", "<", "=="})

PROMPT_V1 = """Read the eligibility criteria of a clinical trial and list every requirement as a separate item.

Eligibility criteria:
<<<
{text}
>>>

For each requirement give:
- "type": "inclusion" or "exclusion", as the trial states it
- "variable": one of {variables}
- "operator": one of {operators}
- "value": a number for threshold operators, otherwise null
- "unit": the unit as written, or null
Rules: split compound requirements; a range is two items; "not pregnant" is exclusion of pregnancy_or_lactation present;
use "other" when no listed variable fits; label only what the text says.

Reply with JSON only: {{"criteria": [{{"type": "...", "variable": "...", "operator": "...", "value": null, "unit": null}}]}}"""


def prompt_hash(prompt: str = PROMPT_V1) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()


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

    @property
    def computable(self) -> bool:
        return self.variable in COMPUTABLE


def parse(raw: str) -> tuple[list[Criterion] | None, int]:
    """(criteria, dropped). criteria is None if the output is unreadable. Invalid items are dropped and counted, never repaired."""
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
        if t not in TYPES or v not in VOCABULARY or op not in OPERATORS:
            dropped += 1
            continue
        if op in THRESHOLD_OPS:
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                dropped += 1
                continue
            val = float(val)
        else:
            val = None
        unit = c.get("unit")
        out.append(Criterion(t, v, op, val, str(unit) if unit not in (None, "") else None))
    return out, dropped


def computable_fraction(criteria: list[Criterion]) -> float | None:
    return None if not criteria else sum(c.computable for c in criteria) / len(criteria)


def extract(text: str, llm) -> tuple[list[Criterion] | None, int]:
    """llm: callable(prompt) -> raw string. Backend failures propagate to the caller, who records them."""
    return parse(llm(build_prompt(text)))
