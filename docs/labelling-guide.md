# Labelling guide for eligibility criteria (v0.1, written before any gold labelling)

A criterion is one atomic requirement from the eligibility text. Split compound sentences into one item per requirement.
Keep requirements joined by "or" as one item flagged `any_of` in the notes; they are scored but excluded from the
computable-criteria estimate in v0.1 (see the protocol).

For each criterion record:

| Field | Values |
|---|---|
| type | `inclusion` or `exclusion`, as the trial states it (a negated inclusion is still inclusion; an exclusion stays exclusion) |
| variable | one value from the fixed vocabulary below, else `other` |
| operator | `>=`, `>`, `<=`, `<`, `==`, `!=`, `present`, `absent` |
| value | a number for threshold operators; empty for `present` and `absent` |
| unit | the unit as written, normalized to a short standard form; empty if none |

## Vocabulary

age, sex, pregnancy_or_lactation, systolic_bp, diastolic_bp, bmi, egfr_or_crcl, serum_creatinine, hba1c, diabetes, ldl_c,
potassium, hemoglobin, nyha_class, lvef, prior_mi, prior_stroke, prior_hf_hospitalization, atrial_fibrillation, current_smoking,
cancer_history, dialysis, liver_disease, anticoagulant_use, life_expectancy, other

## Rules

1. Label what the text says, not what the trial probably meant.
2. "Not pregnant" is exclusion of `pregnancy_or_lactation` present. "No history of X" is exclusion of X present.
3. A range ("18 to 75 years") is two items (`age >= 18`, `age <= 75`).
4. Unclear thresholds ("elevated", "adequate") get `other`.
5. Prior or recent time windows ("within 6 months") are recorded in a free-text note and do not change the variable.
6. Statements about consent, willingness, compliance, or study procedures are `other`.
7. If the same requirement is stated twice, record it once.

## Computable set (frozen with the protocol)

A criterion is computable from the survey only if its variable is in this set: age, sex, pregnancy_or_lactation,
systolic_bp, diastolic_bp, bmi, serum_creatinine, egfr_or_crcl (estimated with a fixed published equation), hba1c, diabetes, ldl_c,
potassium, hemoglobin, prior_mi, prior_stroke, current_smoking, cancer_history, dialysis, liver_disease. Everything else is
not computable. The set is decided from what the survey measures, not from what makes the results look better.

## Quality control

- Labelling is done blind to model output.
- A second reviewer labels a random 25% of the gold set; agreement (Cohen kappa on variable, exact match on value) is reported.
- Disagreements are resolved by discussion and logged by category, not by trial.
