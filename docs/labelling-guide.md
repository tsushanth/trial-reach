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

## Vocabulary (v0.2, 2026-10-22, revised on development data only)

Measured by the survey, therefore computable: age, sex, pregnancy_or_lactation, systolic_bp, diastolic_bp, bmi, egfr_or_crcl,
serum_creatinine, hba1c, diabetes, ldl_c, total_cholesterol, hdl_c, triglycerides, alt, ast, albumin, platelets, wbc, uric_acid,
albuminuria, potassium, hemoglobin, prior_mi, prior_stroke, heart_failure, hypertension, chd_or_angina, copd_or_asthma,
current_smoking, alcohol_use, cancer_history, dialysis, kidney_failure, liver_disease, statin_use, antihypertensive_use,
insulin_use.

Not measured, therefore not computable: nyha_class, lvef, atrial_fibrillation, prior_hf_hospitalization, life_expectancy,
anticoagulant_use, procedure_or_device, imaging_or_ecg_finding, other_lab_value, infection, psychiatric_or_cognitive,
substance_use_disorder, allergy_or_intolerance, consent_or_compliance, study_logistics, other_drug_or_therapy, other_condition,
other.

Why v0.2: in the first development run 69% of criteria fell into "other" and only 21% were computable once nothing was
dropped; many "other" items were measurable by the survey or clearly belong to a named non-computable class. The split
above is defined from what the survey measures, not from which result looks better.

## Rules

1. Label what the text says, not what the trial probably meant.
2. Describe the patient state the line states; the section header decides whether it is required (inclusion) or disqualifying (exclusion). "Patients
   with a prior heart attack" is prior_mi present under either header. "No history of stroke" is prior_stroke absent. "Not pregnant" is
   pregnancy_or_lactation absent. (Corrected 2026-10-23: an earlier draft of this guide said "no history of X" means exclusion of X present, which
   conflicts with how the first-pass labels were made; the labels and this guide now agree.)
3. A range ("18 to 75 years") is two items (`age >= 18`, `age <= 75`).
4. Unclear thresholds ("elevated", "adequate") get `other`.
5. Prior or recent time windows ("within 6 months") are recorded in a free-text note and do not change the variable.
6. Statements about consent, willingness, compliance, or study procedures are `other`.
7. If the same requirement is stated twice, record it once.

## Computable set (frozen with the protocol)

The computable variables are exactly the first group in the vocabulary. A threshold criterion with no usable number is not
computable. The set is decided from what the survey measures, not from what makes the results look better.

## Quality control

- Labelling is done blind to model output.
- A second reviewer labels a random 25% of the gold set; agreement (Cohen kappa on variable, exact match on value) is reported.
- Disagreements are resolved by discussion and logged by category, not by trial.
