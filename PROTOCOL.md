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

Split (recorded 2026-10-22, before any extraction output was inspected): the selection above yielded 13,735 unique trials
(heart failure 2,217; hypertension 4,224; coronary 3,155; stroke 3,273; atrial fibrillation 866; a trial is counted once, in
the first condition group that found it). Seed 20261022; gold 200, validation 200, development 200, no overlap, each
stratified in proportion to group size (13, 46, 32, 62, 47 trials for atrial fibrillation, coronary, heart failure,
hypertension, stroke). The remaining trials are the analysis population for question 2. The id lists are kept outside this
repository.

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
- 0.1.1 (2026-10-22): split recorded (above). Second reviewer for 25% of gold labels named by the owner (an independent family
  member, blind to model output; background to be reported in aggregate).
- 0.2 (2026-10-22, development data only; gold and validation sets untouched): the first extraction prompt returned out-of-
  vocabulary variable names that the parser discarded, which silently removed non-computable criteria from the denominator and
  inflated the computable share (66% in run 1, from 60 development trials). Parser rule changed: items with a valid type are
  never discarded; an unknown variable becomes "other" (not computable) and the raw name is kept for diagnostics. With that fix
  the same 60 trials gave a median of 16.5 criteria per trial, 69% "other", 21% computable, and 95% of trials with fewer than
  half of criteria computable. Because 69% "other" is too coarse to interpret, the criterion vocabulary was revised (labelling
  guide v0.2): survey-measurable variables added, named non-computable classes added. The revision is defined by what the
  survey measures. Expected consequence, stated in advance: most trials will still have a low computable fraction, so population
  reach will be reported mainly as an upper bound for the minority of trials with a high computable fraction, plus the
  distribution of the computable fraction itself, which is a finding in its own right.
- 0.3 (2026-10-22, before any gold labelling; owner approved the reframe): questions reframed. Per-trial population reach is
  demoted to a descriptive secondary result because only about a quarter of criteria are computable from a population survey
  (development findings). New primary question 2: **criterion-level exclusion burden**. Definitions:
  - Target population: survey-weighted US adults meeting a fixed disease definition (heart failure, hypertension, coronary or
    prior heart attack, stroke; self-report, measurement or treatment as fixed in advance; atrial fibrillation is not measured and
    is excluded from the burden analysis).
  - For a measurable criterion (for example an age cap, a kidney function threshold, a blood pressure or HbA1c limit, pregnancy),
    the **exclusion burden** is the weighted share of the target population that fails that criterion on its own.
  - Reported per criterion type and threshold, by condition group, start year and sponsor class, together with how often trials use
    the criterion. Trial-level burden of a trial is the weighted share failing at least one of its measurable exclusions; this
    is a lower bound on total exclusion.
  - Secondary descriptive: distribution of the per-trial computable fraction; reach upper bound only for trials with at least
    70% computable criteria.
  Analysis sample: because local extraction takes about 40 seconds per trial, the analysis uses a stratified random sample
  of 1,500 trials (condition group and start-year strata, seed recorded) from the analysis population, excluding development,
  validation and gold trials. Extraction is local only (7B model). A hosted model was considered for speed; the registry's
  terms could not be fully read by the assistant and the owner chose local extraction. The accuracy bar (F1 at least 0.80, lower
  interval at least 0.75) is now assessed on computable-variable items only.
- 0.4 (2026-10-22, development data only): extraction method changed from whole-text to line-level (code-based section and line
  splitting, one model call per line, few-shot prompt, grounding checks in code), after whole-text extraction was found on
  inspection to invert polarity and invent criteria. Prompt and schema hashes are recorded by the code. Whether a 7B or larger
  model is used, and whether extraction runs locally or on a hosted service, is decided before the gold run and recorded here.
- 0.5 (2026-10-22, before the gold run): extraction runs on a hosted model (claude-haiku-5-5) instead of a local 7B, because
  local extraction was too inaccurate and too slow on development trials. Only public trial text is sent; no patient data. The owner
  treated this as permitted; the registry terms were not read in full by the assistant. The line-level method, grounding checks and
  schema are unchanged. Spend is capped in code. The model identifier, prompt hash and schema hash are recorded with every run.
- 0.6 (2026-10-23, before any gold or validation output was inspected): extraction configuration FROZEN. Model claude-haiku-5-5, thinking
  disabled, effort low, structured output, one call per line, line prompt hash 6be8edf200eaed93507e3bd9c32633ebf5799b4eb6cfcb0a0721e232b3a0134e.
  Pilot on 20 development trials: 353 lines, 0 failed, estimated cost $0.017, polarity and grounding correct on the trial that the
  local model got wrong; computable share 26% and 90% of trials under half computable, in line with the realistic early estimate (the
  local model's higher figures were inflated by wrong items). Because hosted extraction costs about $0.001 per trial, the analysis now
  covers ALL selected trials, not a 1,500-trial sample (supersedes the sampling rule in 0.3). Gold labelling plan: first pass by a
  stronger model (claude-opus-5-5) blind to the pipeline output, line by line, using the labelling guide; at least 25% reviewed by an
  independent human blind to both; agreement reported; the first pass alone is provisional.
- 0.7 (2026-10-23, before any burden estimate was computed): the SURVEY SIDE is fixed here.
  - Survey cycle: the 2017 to March 2020 pre-pandemic file set; adults aged 18 and over. Examination weights for examination and laboratory variables
    and questionnaire items; the fasting-subsample weights for LDL cholesterol and triglycerides. Age is top-coded at 80.
  - Design-based estimates: proportions are weighted ratios within a domain (the condition group); standard errors by Taylor linearisation over
    primary sampling units within strata, using all units (domain analysis). Strata with a single unit are skipped.
  - Condition groups (adults): heart failure (ever told by a doctor); hypertension (ever told, or taking blood-pressure medication, or measured mean
    systolic 140 or more or diastolic 90 or more); coronary or myocardial infarction (ever told of coronary heart disease, angina or heart attack);
    stroke (ever told). Atrial fibrillation is not measured and has no population.
  - Criterion translation: each structured criterion (variable, operator, value, unit) becomes a yes/no/missing flag per person. Present/absent
    variables use questionnaire items or fixed laboratory cut-offs (diabetes: ever told or HbA1c 6.5 or more; albuminuria: urine albumin-creatinine
    ratio 30 mg/g or more). Kidney function uses the 2021 race-free CKD-EPI creatinine equation for every "eGFR or creatinine clearance" criterion (a stated
    limitation: Cockcroft-Gault clearance cannot be told apart in the extracted criteria). Units are converted where the unit text is recognised; a value outside a
    plausible range after conversion makes the criterion untranslatable instead of guessed. Criteria with no translation are counted, not dropped silently.
  - A person fails a criterion if an inclusion criterion is false or an exclusion criterion is true. Missing measurements are left out of that criterion's
    denominator (complete case) and the number left out is reported.
  - Alcohol use has no translation (no clear single definition) and is reported as untranslatable. Sex criteria are not evaluated.
  - Trials are assigned to the first condition group that found them; trials listed under several conditions are analysed once, under that group.

