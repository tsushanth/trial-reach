# Patient-trial matching with small local models

Benchmark: graded labels (not relevant, excluded, eligible) for patient descriptions versus registered trials; three
annual editions. Metric: per-topic area under the ROC curve with intervals bootstrapped over topics; invalid outputs counted.

- **Baseline** (single label per pair, frozen prompt v2) over-predicts "excluded": on the 2022 edition it called 41% of
  eligible and 37% of not-relevant pairs excluded. Age and sex rule veto adds about +0.03 AUROC on eligible vs rest.
- **Criterion-level method (c1)**: one call per pair returns a per-criterion list (met, not met, unknown); the label is decided in
  code. Developed only on 56 unused 2021 topics: eligible-vs-rest AUROC 0.809 vs 0.813 baseline (paired difference -0.004,
  95% CI -0.051 to +0.042); relevant-vs-not +0.034 (CI +0.006 to +0.062). Lenient unknown policy chosen on dev.
- **Frozen final test, 2023 edition** (540 pairs, 37 topics, 7B model, 0 invalid outputs): eligible-vs-rest 0.797 vs 0.787
  (+0.010, CI -0.020 to +0.042); relevant-vs-not 0.863 vs 0.857 (+0.006, CI -0.021 to +0.033); 3-class accuracy 67.8% vs
  61.5% (descriptive, stratified sample). The dev gain on relevance did not replicate.
- **14B baseline on 2022** (secondary, 998 pairs): eligible-vs-rest 0.808 vs 0.811 for 7B. Model size did not help ranking; it
  moves the over-strict failure rather than removing it.
- **Conclusion:** criterion-level judging reduces over-strict "excluded" calls but does not improve ranking eligible above
  excluded at small-model scale. Clean negative result. Caveat: 2023 patients are templated non-oncology cases.
- **Stopped:** a 14B run on 2023 was stopped early by decision; partial output not analysed.
