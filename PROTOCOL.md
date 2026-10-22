# Protocol: who do cardiovascular trials leave out?

Written before any result exists. Version 0.1, 2026-10-22. Changes after the first analysis run must be recorded below with
a date and a reason, and results under changed rules reported as exploratory.

## Questions

1. **Extraction accuracy.** How accurately does a locally run open language model convert free-text eligibility criteria
   into structured criteria (type, variable, operator, value, unit)?
2. **Population reach.** For adults with a given cardiovascular condition, what share would pass a trial's computable
   eligibility criteria, per trial and in aggregate, and how does this vary by start year, sex, age group and kidney function?

Question 2 is reported only if question 1 meets the pre-set accuracy bar below.

## Sources (kinds only; no identifiers or links are stored here)

- A public trial registry: eligibility text and trial metadata for interventional studies.
- A public national health survey with examination and laboratory data and survey weights, used as a stand-in for the US
  adult population.

## Trial selection

Interventional trials of heart failure, hypertension, coronary artery disease or myocardial infarction, and stroke; adult
participants; completed status; start year 2005 to 2024; eligibility text present. Atrial fibrillation is excluded from
the population estimate because the survey does not measure it, and is reported only for extraction accuracy.
Trials are split by a fixed random seed into development (prompt design, rule map design), validation (threshold setting) and a
held-out gold set. The gold set is never used for design decisions.

## Extraction method

- A local open-weight model, temperature 0, JSON output, frozen prompt; prompt hash and model tag recorded before the gold run.
- Invalid or unparseable outputs are counted and never repaired silently.
- Each criterion is labelled inclusion or exclusion with a variable from a fixed vocabulary, an operator, a value and a unit,
  or marked not computable.

## Gold standard

- 200 trials from the held-out set, criteria labelled by hand. The labelling guide is written before labelling.
- Limitation, stated up front: the first labelling pass is done with AI assistance; a clinician or trained reviewer must check at
  least a random 25% and the disagreement rate is reported. Until that check exists the extraction results are labelled provisional.

## Computable criteria and the population estimate

- A fixed map from criterion variables to survey variables is written and frozen before estimation. Criteria with no survey
  counterpart (for example imaging measurements, rhythm findings, or biomarkers not measured) are **not computable**.
- Report, per trial, the computable fraction of criteria. Estimate reach as an **upper bound**: non-computable criteria are
  assumed satisfied. Also report the share of trials where fewer than half the criteria are computable, since reach there is
  weakly informative.
- Disease definition in the survey (self-report, measured values, treatment) is fixed in advance and varied only in labelled
  sensitivity analyses.
- Survey weights and design variables are used; intervals account for the complex design. Cycles are combined with weights
  adjusted accordingly.
- Kidney function is estimated from creatinine with a published equation, fixed in advance.

## Accuracy bar (decides whether question 2 is reported)

Criterion-level agreement with the gold set on computable variables must reach F1 of at least 0.80, with the lower end of a
95% interval (bootstrap over trials) at least 0.75. If not, report the extraction study as a negative or partial result and do
not publish population estimates.

## Pre-declared analyses

- Distribution of reach across trials; trend by start year; by sex and age group; by kidney function.
- Association of reach with sponsor type and phase (descriptive).
- Nothing else is a primary analysis. Anything further is labelled exploratory.

## Threats to validity

- The survey is a cross-section, not a patient registry; a trial population is not a general population.
- Exclusion criteria that need clinical judgement are not computable and bias reach upward.
- Registry text can differ from the protocol actually used.
- Language-model errors can silently shift reach; mitigated by the gold set and the accuracy bar.
- Overlap with prior work on trial eligibility and representativeness; a literature check is part of the write-up.

## Reporting

Aggregate results only, with the exact model tag, prompt hash, seed and software version. No record-level material is
published or stored in this repository.

## Change log

- 0.1 (2026-10-22): initial protocol.
