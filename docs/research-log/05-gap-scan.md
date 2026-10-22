# Gap scan (2026-10-22)

**Method.** Four parallel literature scans by disease group (cardiovascular and stroke; respiratory and infectious disease;
neurology and mental health; cancer, metabolic, kidney and evidence synthesis). Each had to propose language-model-centred
questions answerable with open data, run at least three prior-work searches per candidate, cite only papers actually seen,
and mark novelty and data access. I then spot-checked the top candidate. Search tools were noisy and several queries
returned nothing, so every "no prior work found" is weak evidence. Agents read abstracts, mostly.

**Merged ranking** (question strength and data access judged separately; easy data ranks higher):

1. Who do trials leave out? A language model structures eligibility text; a public survey gives population reach
   (cardiovascular first, then kidney, neurology and psychiatry). Data access highest (both sources verified open).
   Novelty: partly done (manual single-trial versions; one non-model emulation study in asthma and COPD; a thesis extracting
   demographics for about 2,400 cardiovascular trials). **Selected.**
2. Registry versus paper safety (adverse event, death) discrepancies by language model. Manual single-cancer version exists.
3. Tuberculosis variant catalogue: can literature predict reclassification of uncertain variants? Most novel (no prior work
   in 7 searches) but evidence may be sparse and a direct download was unverified.
4. Classification of trial termination reasons. Mostly a methods contribution.
5. Audit of structured tumour stage against pathology report text. Extraction done by others; label audit not found.

Lower: HIV resistance reasoning, antimicrobial-resistance metadata, tuberculosis X-ray shortcut audit, brain transcriptome
re-annotation, subgroup-claim credibility.

**Crowded, do not re-search:** registry versus publication primary-outcome switching (pipelines and language-model methods
exist), polygenic score transfer across ancestries, machine-learning reclassification of uncertain variants (including a
temporal-evaluation angle, checked and found already done), spin detection, language-model patient-trial matching,
ECG and cardiology chatbots and question answering, tuberculosis and sepsis chatbots and prediction, antimicrobial peptide
design, outbreak surveillance with language models, systematic-review screening.

**Cross-scan pattern.** The same open stack (trial registry, public survey, open full text) supports several questions in
different disease areas: a trial-ecosystem programme may be more valuable than one disease.

**Also found.** The original curated-data progression finding was reported in 2020 (DOI 10.1200/JCO.2020.38.15_suppl.9622);
the cohort paper is DOI 10.1158/1078-0432.CCR-23-0580.

## Prior-work check for the reframed project 1 (2026-10-22; 4 searches, abstracts only, weak evidence of absence)

The reframed question (criterion-level exclusion burden against a population survey) is **partly done**:
- A systematic review of 50 studies of exclusion rates found a median of 77% of patients excluded, 83% for hypertension, mostly
  from age, comorbidity and co-prescribing; most studies applied only a subset of criteria, and no trend over time (DOI
  10.1186/s13063-020-4139-0).
- NIH-funded phase 3 trials in heart failure, arrhythmia, coronary disease, heart attack and stroke: 33% had arbitrary upper age
  limits, many excluded implicitly by comorbidity or co-medication (DOI 10.1111/jgs.15786).
- A 2026 analysis of body-mass-index criteria in 352 GLP-1 trials registered 2017 to 2020 estimated the share of adults meeting them
  using national survey data in the US and Korea (DOI 10.1371/journal.pone.0351415): the closest design, one criterion type.
- A 2026 analysis of older-adult exclusion in 207 vaccine trials compared exclusion criteria with age-specific prevalence
  (DOI 10.1016/j.jclinepi.2026.112343).
- Many single-trial eligibility analyses using the survey exist (for example for oral semaglutide, DOI 10.1186/s40842-026-00299-z).
- Eligibility criteria and racial disparities in pancreatic cancer trials, with hospital records (DOI 10.1200/jco.21.02492).
Not found: automated, language-model extraction of all measurable criteria across thousands of cardiovascular trials with
survey-based burden per criterion and trends. The contribution would be scale, automation, reproducibility and cardiovascular
focus, an incremental one. Positioning: methods and measurement paper, not a discovery paper.

## Hosted versus local extraction (2026-10-22)

Question: may public registry text be sent to a hosted model? Findings: the registry terms say data are provided by sponsors and
institutions, are free to use inside and outside the US, and that users may not claim proprietary rights in the database; the
assistant could not read the exact copyright clause (the page did not render for the tool). The model provider's usage policy
does not restrict structuring public text with no patient data. NLM's general policy: government works are not copyrighted but
NLM cannot guarantee the status of third-party items. Conclusion: probably permitted, not confirmed. The owner chose local
extraction. Revisit only after someone reads the terms page in a browser.
