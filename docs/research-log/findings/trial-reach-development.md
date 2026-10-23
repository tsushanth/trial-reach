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

## Extraction quality problem and redesign (2026-10-22, development data only)

- Run 4 (whole-text extraction, decoding constrained to the fixed vocabulary): "other" fell to 5% and the computable share rose
  to 48%, but reading one trial by eye showed the rise was not real: the 7B model inverted polarity ("exclude if prior heart
  attack is absent"), listed conditions the text never mentions (hypertension, cancer history, anticoagulant use) and missed
  others (stroke, congenital heart disease, cardiomyopathy). Constrained decoding made the model fill the list. Three trials
  timed out.
- Redesign (method version 2): split the text in code into sections and lines (the section header decides inclusion or exclusion),
  one model call per line, a few-shot prompt, at most four items per line, and two grounding checks in code: "absent" is only
  accepted when the line contains a negation cue, and a threshold number must appear in the line. Nothing is repaired.
- Eyeball on one trial (19 lines): 7B with the few-shot line prompt got about 14 lines right with 4 to 5 wrong or spurious items
  (for example a rhythm line labelled cancer history); 14B got the hard lines right more often but added spurious "absent"
  items on others, and was 3 times slower (about 10 s per line versus 3.6 s). The grounding checks remove the spurious "absent"
  items. This is one trial and my own judgement, not a measurement; the gold set measures it.
- Speed: 7B takes about 70 s per trial, so 1,500 trials is about 30 hours and the 200 gold trials about 4 hours. 14B is about 3
  times that.
