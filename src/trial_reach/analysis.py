"""Exclusion-burden analysis: join extracted trial criteria to the survey frame. Pure functions; inputs are in-memory tables.

Per protocol 0.3 and 0.7: burden of a criterion = weighted share of the condition group failing it alone; trial lower bound = weighted share failing
at least one translatable criterion that uses the examination weights (criteria needing the fasting subsample weights are reported singly but
not combined). Missing measurements never count as failing in the trial-level combination.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from trial_reach import survey as sv


def criterion_key(role: str, variable: str, operator: str, value, unit) -> tuple:
    v = None if value is None else round(float(value), 3)
    return (role, variable, operator, v, (unit or "").lower().replace(" ", ""))


def period(start: str | None) -> str | None:
    if not start:
        return None
    y = int(str(start)[:4])
    if y < 2005 or y > 2024:
        return None
    return f"{2005 + 5 * ((y - 2005) // 5)}-{2005 + 5 * ((y - 2005) // 5) + 4}"


class Evaluator:
    """Caches per-criterion person-level fail vectors for one survey frame."""

    def __init__(self, d: pd.DataFrame):
        self.d = d
        self._cache: dict = {}

    def fail_vector(self, key: tuple):
        if key not in self._cache:
            role, variable, operator, value, unit = key
            t = sv.translate(self.d, variable, operator, value, unit or None)
            self._cache[key] = None if t is None else (sv.fails(self.d, role, t[0]), t[1])
        return self._cache[key]

    def single_burden(self, group: str, key: tuple):
        fv = self.fail_vector(key)
        if fv is None:
            return None
        f, w = fv
        r = sv.weighted_share(self.d, f, sv.GROUPS[group](self.d), w)
        r["weight"] = w
        return r

    def anyfail(self, keys: list[tuple]):
        """(0/1 array of failing at least one examination-weight criterion, number combined), or (None, 0)."""
        vecs = [fv[0].fillna(0.0).to_numpy() for fv in (self.fail_vector(k) for k in keys) if fv is not None and fv[1] == "w_mec"]
        return (np.maximum.reduce(vecs), len(vecs)) if vecs else (None, 0)

    def weighted_mean(self, values: np.ndarray, mask: np.ndarray):
        w = self.d.w_mec.to_numpy() * mask
        tot = w.sum()
        return float((w * values).sum() / tot) if tot else None

    def trial_lower_bound(self, group: str, keys: list[tuple]):
        """(weighted share failing at least one examination-weight criterion, number of criteria combined) or (None, 0)."""
        vecs = []
        for k in keys:
            fv = self.fail_vector(k)
            if fv is not None and fv[1] == "w_mec":
                vecs.append(fv[0].fillna(0.0).to_numpy())
        if not vecs:
            return None, 0
        anyfail = np.maximum.reduce(vecs)
        dom = sv.GROUPS[group](self.d).to_numpy()
        w = self.d.w_mec.to_numpy()
        tot = (w * dom).sum()
        return (float((w * dom * anyfail).sum() / tot) if tot else None), len(vecs)


def trial_summary(ev: Evaluator, group: str, criteria: list[dict]) -> dict:
    """criteria: dicts with type, variable, operator, value, unit (the extraction output)."""
    keys = [criterion_key(c["type"], c["variable"], c["operator"], c.get("value"), c.get("unit")) for c in criteria]
    n = len(keys)
    translatable = [k for k in keys if ev.fail_vector(k) is not None]
    lb, used = ev.trial_lower_bound(group, translatable)
    return {"n_criteria": n, "n_translatable": len(translatable), "translatable_fraction": (len(translatable) / n) if n else None,
            "lower_bound_burden": lb, "n_combined": used, "keys": translatable}
