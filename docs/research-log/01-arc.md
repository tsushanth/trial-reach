# How the project got here

1. **Starting question (before 2026-10-20).** What blocks curing cancer, where can AI help, what are the lowest-hanging
   fruit, what data exists. The chosen direction was extracting structure from clinical records, specifically dated first
   progression from longitudinal notes, which feeds real-world progression-free survival (rwPFS).
2. **Literature pass.** Searched and read work on language-model extraction from oncology notes and reports. Closest groups
   published preregistered or human-validated studies on single reports; none we found had public longitudinal note text
   with dated progression labels. Several of our first summaries of papers were wrong and were corrected
   ([03](03-mistakes-and-corrections.md)).
3. **Evaluation harness.** Built a patient-level evaluation harness: first-event date scoring with a plus or minus 30 day
   window, bootstrap intervals over patients, Kaplan-Meier and restricted mean survival comparisons, a mock extractor and a
   synthetic cohort generator. About 90 tests. Validated on synthetic data only.
4. **Data access search.** Established that no open dataset combines note text with dated progression labels. Mapped routes
   by kind ([04](04-data-landscape.md)): credentialed hospital notes, institutional partnerships, commercial data programs,
   consortium curated data, and open silver-labelled data.
5. **Real-data experiments.** Open silver labels (model-derived progression calls on radiology reports), a trial-matching
   benchmark, a literature audit of Mendelian-randomization papers, and consortium curated data once access was granted
   ([findings](findings/)).
6. **Reassessment (2026-10-22).** A novelty check showed the main curated-data finding (progression-free survival depends
   on whether imaging or oncologist notes define progression) had been reported by the data's own authors. The owner judged
   the body of work not yet useful research and widened the search to the whole medical field.
7. **Gap scan and new project (2026-10-22).** Four parallel literature scans by disease group, merged and spot-checked
   ([05](05-gap-scan.md)). Project 1 selected: trial eligibility reach.
