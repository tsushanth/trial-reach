# Mistakes and corrections

Kept in full because they changed the direction of the work.

- **Misread papers (early).** Three first summaries of published work were wrong (what a reality-gap metric measured, what
  counted as ground truth in one study, and whether two cited works used language models). Corrected after re-reading.
- **Silver-label validity.** A claim that nobody could state the accuracy of one set of open silver labels was wrong: the
  authors validated against curated labels and trained on them. This also meant the curated data cannot independently
  validate that model (it is in-sample). Corrected; the error-propagation work was re-scoped to a simulation and later
  checked against real curated labels.
- **Independent-error assumption.** The error-propagation simulation assumed independent report-level errors and I guessed
  real clustering would make patient-level agreement worse. On real linked data it was better (see findings): clustering
  helped. The simulation is a conservative bound, not an estimate.
- **Novelty not checked first.** The progression-source finding was written up as a result before searching; the search
  showed the data authors had reported it in 2020. Lesson: check prior work before building or claiming.
- **Operational slips.** Overloaded a data portal with parallel requests; used a paper-download tool with a pirate-mirror
  fallback once and stopped; shell and path errors; wrong model tag recorded failures as errors and resume skipped them
  (fixed so errored rows are retried); a global git hooks path silently disabled a local hook (fixed 2026-10-22).
- **Memory limits.** Running a 14-billion-parameter model on a 16 GB laptop exhausted memory; an 8 GB second machine cannot
  run it at all.
