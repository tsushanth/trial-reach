# Trial eligibility reach: development findings (2026-10-22)

Development data only (60 of the 200 development trials; gold and validation untouched). Extraction by a 7B local model.

| Run | Parser / vocabulary | Kept / dropped items | Median criteria per trial | "other" | Computable share | Trials under half computable |
|---|---|---|---|---|---|---|
| 1 | first prompt, out-of-vocabulary items discarded | 458 / 867 | 4 | 1% | 66% (inflated: denominator lost items) | 17% |
| 2 | nothing discarded, original vocabulary | 1229 / 2 | 16.5 | 69% | 21% | 95% |
| 3 | vocabulary v0.2 (survey-measurable and named non-computable classes) | 1205 / 0 | 16 | 54% | 24% | 92% |

Run 3 details: median per-trial computable fraction 0.19; 1 of 59 parsed trials has at least 70% computable criteria; 1 trial
unparseable. Most remaining "other" items are specialist findings (angiographic lesion features, procedure details) that no
survey measures.

Reading: a national health survey can check only about a quarter of what cardiovascular trials require. A single
population-reach number per trial is therefore weakly informative for most trials. Per-criterion exclusion burden (what share of
adults is excluded by a measurable criterion such as age cap, kidney function threshold, blood pressure limit) remains well
defined and is the more robust target.

Speed: about 40 seconds per trial on a laptop with a 7B model; the full selection (13,735 trials) would take about 150 hours, so
the analysis needs a stratified sample or faster compute. Public registry text is not restricted, so a hosted model is an
option, subject to cost.
