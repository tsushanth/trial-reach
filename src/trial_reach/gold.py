"""Gold labelling prompt, parser and scoring.

The first-pass gold labels are produced by a stronger model, BLIND to the extraction pipeline's output, from the labelling guide.
They are provisional until an independent human has reviewed a random share. Scoring compares item sets per line.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass

from trial_reach.criteria import COMPUTABLE, OPERATORS, THRESHOLD_OPS, VOCABULARY, split_lines

GOLD_SYSTEM = """You are labelling clinical trial eligibility criteria for a research dataset. The input is a numbered list of lines, each marked inclusion or exclusion by the trial's own section headers. For EVERY line, list the measurable conditions the line states about a patient.

For each condition give:
- variable: one value from this fixed vocabulary: {variables}
- operator: one of {operators}
- value: a number for threshold operators (>=, >, <=, <, ==), otherwise null
- unit: the unit as written, normalized to a short form, or null

Rules:
1. Label what the line says, not what the trial probably meant. Describe the patient state the line states. "Patients with a prior heart attack" is prior_mi present, whether the line is under inclusion or exclusion. "No history of stroke" is prior_stroke absent. The section decides whether it is required or disqualifying; you only describe the state.
2. A range ("18 to 75 years") is two items (age >= 18, age <= 75). Split compound lines into one item per requirement.
3. Use the most specific variable that fits. Use other_condition, other_drug_or_therapy, other_lab_value, procedure_or_device, imaging_or_ecg_finding, infection, psychiatric_or_cognitive, substance_use_disorder, allergy_or_intolerance, consent_or_compliance, study_logistics when a named class fits, and "other" only as a last resort.
4. Use a threshold operator only when the line gives a number; use present or absent otherwise. Use "absent" only when the line says the patient does not have the condition.
5. Vague thresholds ("elevated", "adequate") get the matching other_* class with operator present.
6. Time windows ("within 6 months") do not change the variable.
7. A line that states nothing measurable gets an empty list.
8. Every numbered line must appear in your answer exactly once, in order."""

GOLD_SCHEMA = {
    "type": "object",
    "properties": {"lines": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "n": {"type": "integer"},
            "items": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "variable": {"enum": list(VOCABULARY)},
                    "operator": {"enum": list(OPERATORS)},
                    "value": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                    "unit": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                },
                "required": ["variable", "operator", "value", "unit"],
                "additionalProperties": False,
            }},
        },
        "required": ["n", "items"],
        "additionalProperties": False,
    }}},
    "required": ["lines"],
    "additionalProperties": False,
}


def build_gold_prompt(text: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = split_lines(text)
    system = GOLD_SYSTEM.format(variables=", ".join(VOCABULARY), operators=", ".join(OPERATORS))
    user = "\n".join(f"{i + 1}. [{role}] {line}" for i, (role, line) in enumerate(lines))
    return system, user, lines


Item = tuple  # (type, variable, operator, value)


def _key(role: str, c: dict) -> Item:
    v = c.get("value")
    return (role, c["variable"], c["operator"], None if v is None else round(float(v), 4))


def parse_gold(raw: str, lines: list[tuple[str, str]]) -> dict[int, set[Item]] | None:
    """{line index: item set}, or None if the answer does not cover every line once in order."""
    try:
        d = json.loads(raw)
        got = d["lines"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    if [x.get("n") for x in got] != list(range(1, len(lines) + 1)):
        return None
    return {i: {_key(lines[i][0], c) for c in x["items"]} for i, x in enumerate(got)}


def pipeline_items(role_lines: list[tuple[str, str]], criteria: list[dict]) -> set[Item]:
    return {_key(c["type"], c) for c in criteria}


def prf(tp: int, fp: int, fn: int) -> tuple[float | None, float | None, float | None]:
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = 2 * p * r / (p + r) if p and r else (0.0 if p is not None and r is not None else None)
    return p, r, f


def score_trial(gold: set[Item], pred: set[Item], computable_only: bool = True) -> tuple[int, int, int]:
    """(tp, fp, fn). With computable_only, an item counts only if its variable is computable on either side."""
    if computable_only:
        gold = {g for g in gold if g[1] in COMPUTABLE}
        pred = {p for p in pred if p[1] in COMPUTABLE}
    return len(gold & pred), len(pred - gold), len(gold - pred)


def bootstrap_f1(per_trial: list[tuple[int, int, int]], n_boot: int = 2000, seed: int = 0) -> dict:
    tp, fp, fn = (sum(x[i] for x in per_trial) for i in range(3))
    p, r, f = prf(tp, fp, fn)
    rng = random.Random(seed)
    fs = []
    for _ in range(n_boot):
        s = [rng.choice(per_trial) for _ in per_trial]
        v = prf(*(sum(x[i] for x in s) for i in range(3)))[2]
        if v is not None:
            fs.append(v)
    fs.sort()
    return {"precision": p, "recall": r, "f1": f, "ci": (fs[int(0.025 * len(fs))], fs[int(0.975 * len(fs)) - 1]) if fs else None,
            "trials": len(per_trial), "tp": tp, "fp": fp, "fn": fn}
