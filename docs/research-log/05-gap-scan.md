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
