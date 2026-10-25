# Confirmatory plan for burden-analysis run B (written 2026-10-24, before any confirmatory step has been run)

Status of the evidence this plan governs: **run B is post-hoc and exploratory.** Run A (as pre-specified in protocol 0.3 and 0.7) failed its own validity check, run B changed the
analysis after the run A results were seen (protocol 0.8), and every trial in the registry selection was in run B's inputs. Nothing from run B may be described as confirmed,
tested or established until the steps below are done and reported. This file records what is pre-specified for those steps and what would change the conclusion.

## 1. How the post-hoc correction is labelled (applies to every document in this repository)

- Run A = "pre-specified, failed validity check, not interpretable". Run B = "post-hoc corrected, exploratory". Confirmatory steps below = "confirmatory C1 to C4".
- Every findings file that reports run B numbers carries the header label "exploratory (post-hoc run B)" and links to this plan. Numbers from run B are never reused in an abstract,
  title or summary sentence without that label.
- What was seen before the change, for the record: the run A trial-level numbers (median lower-bound burden 82%, upper quartile 100%) and the 25 most-used criteria with their burdens.
  The changes (group from each trial's own condition list; own-disease criteria never scored; measurement-based criteria only in the headline) were motivated by the implausibility
  and by the three mechanisms found in the criteria, not by the direction or size of any result of interest. The 200 gold trials and 200 validation trials were part of run B's inputs; no
  trial in the selection is untouched for exploratory purposes.
- Deviations from this plan after it is committed are added as dated entries at the end of this file with the reason, and any result obtained under a deviation is labelled exploratory.

## 2. What can and cannot be confirmed

Cannot be confirmed with the existing trial set, so they remain exploratory: the trend claims over registration period (upper age limits roughly 26% to 32% of trials, kidney-function
criteria roughly 25% falling to 20%), the sponsor comparisons, and the distribution of trial-level lower bounds. Reason: every trial was inspected in aggregate before the correction, and a
fresh set large enough to confirm a 6.7 percentage-point difference (25.6% against 32.3%) at 80% power and a two-sided 1% level needs about 1,060 trials per period group; newly completed
trials will not reach that within a year. These claims stay descriptive: "among trials registered and completed 2005 to 2024, X% set an upper age limit", not "the practice is changing".

Can be confirmed or refuted with independent data or independent labels: C1 to C4.

## 3. Confirmatory steps, pre-specified

**C1. Extraction accuracy by independent human labels.** At least 25% of the 200 held-out gold trials (50 trials: 20 blind, 30 reviewed) labelled by a person who has not seen the model output (form built; reviewer to be a person outside the project's
modelling). Metric: item-level F1 on measurable (computable) variables, trials as the unit, 95% interval by bootstrap over trials, exactly as in the protocol. Pass: F1 at least 0.80 and the lower interval limit at
least 0.75. The first-pass F1 of 0.889 (interval 0.873 to 0.904) is provisional until this is done.
If it fails: the extraction is declared not validated; run B burden numbers are withdrawn from any write-up; the finding becomes a negative methods result.

**C2. Group-assignment accuracy.** A random sample of 200 trials from those assigned to a group, checked by a person against the trial's own condition list and title: is the trial genuinely about the assigned condition group (heart failure,
hypertension, coronary disease, stroke) and not about a different disease sharing a word (pulmonary, portal, ocular, intracranial hypertension; non-cardiac heart failure caveats)? Metric: misassignment rate with a 95% Wilson interval.
Pass: upper interval limit at most 10%. If it fails: tighten the rules in the grouping module, rerun run B, and relabel the rerun as exploratory.

**C3. Survey-side replication on independent cycles.** Recompute the single-criterion burdens (age caps at 65, 70, 75; eGFR under 30, 45, 60; systolic blood pressure over 160 and 180; HbA1c over 8 and 9; BMI over 40) in each condition group using two earlier
examination-survey cycles (2013 to 2014 and 2015 to 2016), design-based, same derivation code, no changes after seeing the results. Pre-specified expectation: for each criterion and group the earlier-cycle estimate lies within
5 percentage points (absolute) of the 2017 to 2020 estimate, or within the combined 95% interval of the two. A criterion that violates this is reported as unstable across cycles and not interpreted as a general figure.
If more than a third of the listed criteria are unstable, the burden table is withdrawn as a "typical burden" claim and kept only as a description of one survey cycle.

**C4. Extraction stability across models and runs.** Re-extract a random 500 trials with a second, differently built model under the same prompt and schema and rerun the first model on the same 500. Metric: criterion-level agreement (the same set of measurable criteria for a trial)
as the average Jaccard index over trials, and the change in each trial's measurable-criterion count. Pre-specified expectation: average Jaccard at least 0.80 between the two models and at least 0.90 between two runs of the same model. This measures stability, not
correctness, and is reported as such. If it fails, the headline criterion-level burdens are reported with a stated sensitivity range instead of single numbers.

**Prospective hold-out (optional, for later).** On a pre-set later date (six months after the registry snapshot, about 2027-04-24) refetch the registry and take trials newly completed since the snapshot in the same conditions and years window. If at least 1,000 are available,
recompute the usage shares and compare with the pre-snapshot sets; otherwise report the counts and stop. This is the only route to confirming a trend claim and may not be available.

## 4. Multiplicity and reporting

- Hypotheses are limited to C1 to C4 and the listed criteria in C3 (10 criterion-group sets). No other result is called confirmed. Where several estimates are tested for stability, the rule is the fixed expectation above, not a p value.
- Every confirmatory result is reported whether it passes or fails, in the research log with its date, the exact definition used, and the sample.
- Publication conditions: C1 and C2 pass; C3 and C4 reported in full; run A shown as a failed first attempt; claims about trends and sponsors worded as descriptive.

## 5. What would change the conclusion

| Result | Consequence |
|---|---|
| C1 F1 below 0.80 or lower limit below 0.75 | extraction not validated; no burden numbers published; negative methods result |
| C2 upper limit of misassignment above 10% | group rules fixed and run B repeated (still exploratory) |
| C3 more than a third of the criteria unstable across cycles | burden table withdrawn as a general figure; kept as a one-cycle description |
| C4 agreement below the stated levels | criterion-level numbers reported with a sensitivity range |
| Prospective hold-out reverses the usage-share direction | trend language removed even as exploratory |
| A later survey cycle or definition change moves a headline burden by more than 5 points | table updated; old numbers kept with the date |

## 6. Constraints

No data, record identifiers, local paths or links to data services are stored here (the repository rule). Hand-labelled items and checked samples are kept outside the repository; only aggregate counts and intervals are written back.

## Addendum 2026-10-25 (before C3 was run): operational details, one correction

- Correction to section 3: C3 lists 11 criteria, not "10 criterion-group sets": age over 65, 70, 75; eGFR under 30, 45, 60; systolic blood pressure over 160 and 180; HbA1c over 8 and 9; BMI over 40; each in 4 condition groups (44 cells).
- Cells: a cell passes if the earlier-cycle estimate is within 5 percentage points (absolute) of the 2017 to 2020 estimate, or the difference is within 1.96 times the square root of the sum of the two squared standard errors. A criterion is "unstable" in a cycle if it fails in 2 or more of its 4 groups.
  The burden table is withdrawn as a general figure if more than a third of the 11 criteria (4 or more) are unstable in either cycle.
- Cycle adaptation, fixed here, limited to variable names: weights renamed to the two-year examination and fasting weights of each cycle; blood pressure in 2013 to 2016 comes from the auscultatory readings (mean of the first three
  available readings) instead of the oscillometric device used from 2017; everything else (age 18 and over, kidney function equation, condition definitions, design-based errors) is unchanged. The blood-pressure device change is a known measurement difference; a blood-pressure criterion that fails
  is reported as such and flagged as possibly caused by the device change, but it still counts as a failure.

## Result log

**C3 run 2026-10-25 (survey-side replication; aggregate only).** Two earlier examination-survey cycles (2013 to 2014 and 2015 to 2016; 6,113 and 5,992 adults; condition-group samples 182 to 2,459 and 214 to 2,432 people, heart failure the smallest),
same derivation and design-based errors, only the name adaptations fixed in the addendum above. Of 88 criterion-group-cycle cells, **4 failed** the pre-specified rule (a difference above 5 points and outside the combined 95% interval): age caps in heart failure
in 2015 to 2016 (over 65: 66% against 50%; over 70: 52% against 39%) and two kidney-function cells in stroke in 2013 to 2014 (eGFR under 45: 14.8% against 7.5%; under 60: 32% against 23%). **No criterion was unstable** (a criterion needs 2 or more failing groups), so
the burden table is not withdrawn. The blood-pressure criteria, whose device changed in 2017, did not fail in any cell. Reading: the single-criterion burdens are broadly reproducible across survey cycles; the heart-failure and stroke groups are small and their estimates move
by several points, so burdens for those groups should be quoted with their intervals. Result of C3: PASS under the pre-specified rule.

**C1 reviewer note (2026-10-25).** The owner will do the human review personally. The owner has not seen the model output or the first-pass labels, but directed the project and has read the labelling guide and this plan; this is a weaker independence than a reviewer outside the project, and
the review is therefore recorded as "project owner, blind to model output". If time allows a second reviewer should label a subset so agreement can be reported.

## Addendum 2026-10-25 (before C4 was run): C4 scoring details

- Sample: 500 trials drawn at random (seed 20261025) from those with an extraction and a condition group. Three extractions of each: the original run (model A, haiku class), a repeat of model A, and model B (a differently built, larger model of the same family, sonnet class). Same prompt text and schema for all.
- Item key per trial: role, variable, operator and value rounded to 4 decimals, restricted to the measurable (computable) variables. Per-trial agreement is the Jaccard index of the two item sets; two empty sets count as 1.0 (both extractions agree there is nothing measurable). Averages are reported with and without such trials, and the count of trials with a different number of measurable items is reported.
- Pass rule as in section 3: average Jaccard at least 0.80 between model A and model B, and at least 0.90 between the original and the repeat of model A; the stated rule is on the average over all 500 trials (empty-empty counted as 1.0).
- Spend cap in code: 12 US dollars across the two new runs.

