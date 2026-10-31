> Label: exploratory (post-hoc run B, and run C its header-corrected rerun; C is the corrected one). Not confirmed; see ../confirmatory-plan-run-b.md before citing any number.

# Trial eligibility reach: exclusion burden, first full runs (2026-10-23)

Aggregates only. Extraction: frozen hosted pipeline (line level, protocol 0.6) over 13,335 trials; survey: 2017 to March 2020 national examination survey, adults, design-weighted
(protocol 0.7). All numbers below are exploratory or provisional: the extraction accuracy rests on provisional gold (F1 0.889 on measurable criteria, no human review yet), and run B is a
post-hoc correction (protocol 0.8).

## Run A (as specified): failed, not interpretable

Median trial-level lower-bound burden 82%, upper quartile 100%. Causes found by inspecting the top criteria: trials were placed in a condition group by which search found them first (and the
hypertension search also returned pulmonary, portal and ocular hypertension trials); criteria that define a trial's own disease were scored against that disease's population and failed 100% by
construction; and history, diagnosis and medication flags ignore the qualifiers the extraction dropped (recent, severe, uncontrolled), so the survey's "ever" flag overstates them.

## Run B (corrected; exploratory)

Group from each trial's own condition list; own-disease criteria never scored; headline uses measurement-based criteria only (history and medication flags kept separate as ever-history upper bounds, never combined).
9,759 trials were assigned a group (heart failure 1,748; hypertension 2,394; coronary 2,722; stroke 2,895); 3,576 had none (other diseases, atrial fibrillation only).

**How much of a trial can the survey check?** Median 16% of a trial's criteria are measurement-based and translatable (quartiles 8% to 25%); 83% of trials have at least one; only 64 trials (under 1%) have 70% or more.
Reading: a survey can say little about most of what trials require. Whole-trial reach is therefore not estimated for most trials; criterion-level burden is.

**Single-criterion burden (share of adults in the condition group a criterion excludes):**

| Criterion | Trials using it | Heart failure | Hypertension | Coronary | Stroke |
|---|---|---|---|---|---|
| Exclude age over 65 | | 50% | 36% | 53% | 52% |
| Exclude age over 70 | | 39% | 23% | 37% | 39% |
| Exclude age over 75 | | 27% | 14% | 26% | 25% |
| Exclude eGFR under 60 | 166 | 29% | 12% | 21% | 23% |
| Exclude eGFR under 45 | 106 | 15% | 4% | 7% | 8% |
| Exclude eGFR under 30 | 639 | 5% | 1% | 2% | 2% |
| Exclude systolic BP over 180 | 272 | 1% | 1% | 2% | 2% |
| Exclude systolic BP over 160 | | 9% | 9% | 9% | 12% |
| Exclude HbA1c over 9% | | 7% | 3% | 4% | 4% |
| Exclude BMI over 40 | | 18% | 12% | 10% | 8% |
| Require systolic BP 140 or more | 456 | 73% | 64% | 75% | 66% |

(The last row reflects trials of uncontrolled hypertension; many adults with hypertension are treated and controlled. It is large in non-hypertension groups probably because of trials that list several conditions.)

**Use of restrictive criteria (share of trials):** an upper age limit in 26% (2005 to 2009), 30%, 27%, 32% (2020 to 2024), median cap 75 (quartiles 65 to 80); a kidney-function criterion in 25%, 26%, 23%, 20% (declining);
a pregnancy exclusion in 41% to 46% (near-zero burden in an adult survey population, since the survey measures pregnancy only for women of child-bearing age).

**Trial-level lower bound** (share failing at least one measurement-based criterion, where any such criterion exists; 8,144 trials): median 11% (quartiles 0.1% to 75%), strongly bimodal; by group: stroke 0.1%, coronary 3%, heart failure 7%,
hypertension 80% (blood-pressure entry criteria). By start period: median 20% (2005 to 2009), 14%, 8%, 10% (2020 to 2024). By sponsor: industry 45%, other 6%, federal 2%. For women versus men and for age 65 plus versus under 65 the medians are similar
(10.5% vs 10.5%; 6.5% vs 5.4%). The 64 most checkable trials have a median lower bound of 78% (reach at most about 22%).

**History flags (ever-history upper bounds, not combined):** for example diabetes exclusion removes up to about 27% of hypertension adults; prior stroke up to 18% of coronary adults; these are overstated because severity and timing were dropped.

## What this does and does not show

Shows: how common and how restrictive the measurable criteria are (age caps, kidney thresholds, laboratory limits), and that a quarter to a third of cardiovascular trials set an upper age limit.
Does not show: total reach of any single trial, anything about final trial enrolment, or effects on outcomes. The survey is a cross-section, criteria timing and severity are partly lost, and eGFR uses one equation for both eGFR and creatinine-clearance wording.

## Before anyone relies on it

1. The human review of the gold labels (at least 25%) must confirm the extraction accuracy.
2. The run B correction is post-hoc; a fresh confirmatory analysis plan should be written before any publication, ideally with a held-out validation set of trials.
3. Check the several-conditions assignment (first listed condition) and the pulmonary and other exclusions on a hand-checked sample.

## Run C (run B with the section-header fix; exploratory, 2026-10-31)

**What was wrong in run B.** The rule that splits a trial's eligibility text into inclusion and exclusion sections did not recognise several header forms (bulleted or bold headers, headers with words before or after
the phrase). Lines under such a header kept the previous section's role, so exclusion lines were read as inclusion in about 1.2% of trials (168 trials; 1,717 of 192,210 lines; 99% of the flips were exclusion read as
inclusion). A read-only count found 305 trials whose split changed under a first version of the fix; the final rule (which also accepts words before the phrase) changes 462, of which 445 had an extraction.

**What was done.** Header rule fixed (method version 2.1; the model prompt and its hash are unchanged), with tests for each header form and for content lines that must not count as headers. The 445 trials were
re-extracted with the same hosted model and cap (11,007 lines, 1 failed; about $0.56). Everything else in the analysis is run B's code and inputs. Run B's results are kept unchanged and remain the frozen
record; **run C is the corrected one and is the run to cite for any number below, always labelled exploratory and next to run B.**

| Aggregate | Run B | Run C |
|---|---|---|
| Trials analysed / with a lower bound | 9,759 / 8,144 | 9,759 / 8,144 |
| Median translatable fraction | 0.156 | 0.156 |
| Trials with at least 70% translatable (n) | 64 | 64 |
| Median lower-bound burden, all trials | 0.110 | 0.104 |
| Upper quartile of lower-bound burden | 0.745 | 0.718 |
| Median, coronary / heart failure / hypertension / stroke | 0.033 / 0.066 / 0.803 / 0.001 | 0.028 / 0.066 / 0.802 / 0.001 |
| Median, industry-sponsored trials | 0.448 | 0.348 |
| Median, 2005 to 2009 / 2010 to 2014 | 0.198 / 0.141 | 0.174 / 0.116 |
| High-translatable trials: median lower bound (reach upper bound) | 0.777 (0.223) | 0.777 (0.223) |

At trial level, 268 trials had a lower bound in both runs and a changed extraction: 110 went down, 4 went up, 99 moved by more than 0.10 and 87 by more than 0.25. No trial gained or lost its lower bound.
Direction is as expected: an exclusion line read as an inclusion requirement counted everyone without the condition as excluded, so run B overstated burden in the affected trials.

**Reading.** The overall picture, the translatable-fraction results and the high-translatable result do not change. Group-level medians change little, but the upper quartiles and the industry-sponsor median move
noticeably, so any statement about sponsor differences or period trends should use run C. Limits: these are still lower bounds; the new rule for headers with words before the phrase is a judgement
(443 distinct newly matched forms were reviewed by form, not line by line); 17 of the 462 affected trials had no extraction and are outside this comparison.
