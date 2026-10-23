# Prior-work and novelty check: criterion-level exclusion of US adults by cardiovascular trial eligibility criteria

Date of check: 2026-10-23. Scope: heart failure, hypertension, coronary disease, stroke trials; registry free-text criteria structured by a language model; criterion-level exclusion share estimated in a national health survey (NHANES), with trends over time and by sponsor.

Verification convention: "opened" means the abstract or full text was retrieved in this check. Anything where only an abstract or metadata was seen is marked as such. Items I could not open are marked UNVERIFIED. Works are cited by title, journal, year and DOI only.

## Verdict: PARTLY DONE

Each ingredient exists separately, and one 2026 paper combines most of them for a different disease area. No work found combines all of: (a) language-model structuring of registry criteria at scale, (b) cardiovascular focus across several conditions, (c) criterion-level survey-based exclusion shares, (d) trends over time and by sponsor. The cardiovascular, scaled, trend-and-sponsor version appears unpublished, but the method is no longer new, so novelty rests on scale, scope and the trend/sponsor analysis, not on the method.

Positioning statement for a paper: "Prior work has estimated trial-eligible population shares for single trials or single drug classes, using manually curated criteria; we automate criterion extraction with a language model across thousands of registered cardiovascular trials (2005 to 2024) and, for each measurable criterion, estimate the share of US adults with the condition it excludes, with trends over time and by sponsor type."

## Closest works

| # | Work (title, venue, year, DOI) | Criteria extraction | Trials | Population data | Level | Disease area, years | Difference from our plan |
|---|---|---|---|---|---|---|---|
| 1 | Fixed BMI eligibility criteria for GLP-1 receptor agonist trials and estimated trial-eligible proportions in Asian and non-Asian populations, PLoS One, 2026, 10.1371/journal.pone.0351415 | Automated first pass: keyword matching then numeric parsing of cutoffs, with an AI assistant stated to be used for automated parsing, followed by expert curation and duplicate review. Opened (full text via a summarizing fetch; extraction details should be re-read in the original before citing) | 352 | NHANES 2021-2023 and the Korean national survey 2021-2023, survey-weighted | Criterion-level (single cutoffs) plus sequential attrition for two composite profiles | GLP-1 agonist trials (diabetes, obesity), registered 2017-2020 | Closest methodological match. Differs: one drug class, 4-year window, focus on Asian vs non-Asian BMI disparity, no registration-year trend, no sponsor analysis reported, not cardiovascular. Population data postdate the trials. The extraction is keyword/regex-led with LLM assistance, not an LLM emitting (variable, operator, value) triples |
| 2 | Exclusion by design: enrollment criteria limit older adult participation in SARS-CoV-2 vaccine clinical trials, J Clin Epidemiol, 2026, 10.1016/j.jclinepi.2026.112343 | Manual extraction (abstract states criteria were extracted per trial; method detail UNVERIFIED) | 207 | US population age distribution and age-specific condition prevalence (source not confirmed; NHANES use UNVERIFIED) | Criterion-level, descriptive comparison of criteria use vs prevalence | COVID-19 vaccine trials, 2019-2025 | Abstract only opened (full text not accessible). Different disease, small N, older-adult focus, no per-criterion exclusion share |
| 3 | Exclusion rates in randomized controlled trials of treatments for physical conditions: a systematic review, Trials, 2020, 10.1186/s13063-020-4139-0 | Review of 50 prior studies (manual) | 305 trials in 31 conditions | Clinical populations in the underlying studies | Trial-level exclusion rates | Physical conditions, search to 2018 | Abstract opened. Median exclusion 77.1 percent; hypertension median 83.0 percent. No significant change over time and no funder difference found. Authors note most studies applied only a subset of criteria. Shows the headline finding exists; our contribution is the automated, cardiovascular, criterion-level, reproducible version |
| 4 | Adequacy of inclusion of older adults in NIH-funded phase III clinical trials, J Am Geriatr Soc, 2019, 10.1111/jgs.15786 | Manual review of registry records | 45 heart failure, 24 dysrhythmia, 106 coronary, 76 myocardial infarction, 113 stroke trials, plus non-cardiovascular conditions | None (compares to expected disease ages) | Trial-level and age-cap prevalence | NIH phase III, 1965-2015 | Abstract opened. About 33 percent had an upper age limit; 67 percent had mean/median age skewed younger. NIH-funded only, no survey linkage, no automation |
| 5 | Evaluating eligibility criteria of oncology trials using real-world data and AI, Nature, 2021, 10.1038/s41586-021-03430-5 (framework name: Trial Pathfinder) | Criteria from completed trials emulated in EHR data (manual emulation; detail beyond abstract UNVERIFIED) | Completed advanced NSCLC trials; 61,094 patients in a nationwide EHR database; other cancers as extension | Real-world EHR cohort | Criterion-level effect on hazard ratio and eligible pool | Oncology | Abstract opened, paper exists. Asks which criteria can be relaxed without changing treatment effect; ours asks who is excluded. Follow-ups apply it to myeloma (Journal of Comparative Effectiveness Research, 2024, 10.57264/cer-2023-0164) and asthma/COPD (Frontiers in Medicine, 2026, 10.3389/fmed.2026.1863026); all oncology or respiratory, few trials each |
| 6a | Characteristics of populations excluded from clinical trials supporting intensive blood pressure control guidelines, J Am Heart Assoc, 2021, 10.1161/JAHA.120.019707 | Manual mapping of trial criteria | Small set of intensive-BP trials | NHANES 2013-2016 | Trial-level eligible share (20.6 percent of adults with hypertension) and reasons | Hypertension | Abstract opened. Cardiovascular and NHANES-based, but manual, a handful of trials, one condition |
| 6b | Assessing cardiovascular risk to guide hypertension diagnosis and treatment, JAMA Cardiology, 2016, 10.1001/jamacardio.2016.2861 | Manual | 2 trials (SPRINT, HOPE-3) | NHANES 2007-2012 | Trial-level | Hypertension | Abstract opened. Same pattern: manual, two trials |
| 6c | Representation of patients with chronic kidney disease in clinical trials of cardiovascular disease medications, JAMA Network Open, 2024, 10.1001/jamanetworkopen.2024.0427 | Manual systematic review | 1,194 trials | None | Single criterion (CKD exclusion) trend: 66 to 79 percent, 2000 onward | Cardiovascular drug trials, 2000-2021 | Abstract opened. Cardiovascular, large, with a time trend, but one criterion, manual, and no population denominator |
| 6d | AutoCriteria: a generalizable clinical trial eligibility criteria extraction system powered by large language models, JAMIA, 2023, 10.1093/jamia/ocad218 | LLM extraction of entities, values, temporality | 180 annotated trials, 9 diseases | None | Extraction tool only | Multiple diseases | Abstract opened. Supports feasibility of LLM extraction (F1 about 89); no population linkage |
| 6e | Optimizing clinical trial eligibility design using NLP models and real-world data, JMIR AI, 2024, 10.2196/50800 | Deep-learning NLP pipeline | 3,281 industry-sponsored phase 2/3 trials | One health system EHR (about 2,775 lung cancer patients) as a pilot | Criterion-level impact on eligible patients (prototype) | Oncology, UC, Crohn disease, 2013-2020 | Abstract opened. Scaled extraction linked to EHR, but oncology/GI, one site, prototype, not cardiovascular, no NHANES |
| 6f | Criteria2Query (JAMIA, 2018, 10.1093/jamia/ocy178) and Criteria2Query 3.0 (J Biomed Inform, 2024, 10.1016/j.jbi.2024.104649) | Hybrid ML/rules (v1); generative LLM (v3) | 125 criteria evaluated (v1) | Converts to queries for OMOP-format clinical databases | Criterion-to-query tool | Multiple | Abstract/metadata opened. Enables the approach; no cardiovascular exclusion-share study |
| 6g | A natural language processing framework for structuring and visualizing clinical trial eligibility criteria at scale, JMIR Research Protocols, 2026, 10.2196/86425 | Embeddings, clustering, LLM summarization | 53,872 oncology trials | None | Criterion frequency by domain and time | Oncology | Abstract opened. Scaled and temporal, but no population linkage, oncology only |
| 6h | Exclusions affect representativeness of Alzheimer's disease trial participants, Alzheimer's and Dementia: Translational Research and Clinical Interventions, 2026, 10.1002/trc2.70191 | Manual, one trial | 1 trial | Health and Retirement Study linked to Medicare | Trial-level | Alzheimer prevention | Abstract opened. Shows population-survey eligibility estimation is an active pattern; one trial |

Also seen but not central: a medRxiv 2025 preprint applying text processing to 1,192 cardiovascular digital-health trials to quantify English-language restrictions (one criterion, no population estimate; seen via search snippet only, UNVERIFIED beyond that), and a 2020 case study using real-world data to rationalize Alzheimer trial criteria with an FDA-guidance motivation (abstract opened; not cardiovascular).

## What the existing work does not do

- No work found structures criteria with a language model across thousands of cardiovascular trials and links each measurable criterion to a nationally representative survey.
- Cardiovascular NHANES eligibility studies are manual and cover one to a few trials (blood pressure) with trial-level rather than criterion-level output.
- Large cardiovascular criteria reviews (kidney disease representation, 1,194 trials) are manual, single-criterion, and have no population denominator.
- The closest method paper (GLP-1/BMI) covers one drug class over four registration years, reports no registration-year trend and no sponsor analysis, and is not cardiovascular.
- Trial Pathfinder-style work answers "which criteria can be relaxed safely" in oncology or respiratory disease; it does not report the share of the general patient population excluded per criterion across a field.
- No found work tracks how exclusion shares per criterion changed from 2005 to 2024, or differs by sponsor class (industry vs academic vs government), for cardiovascular trials. The systematic review in row 3 reported no change over time or by funder, but at trial level, with heterogeneous manual methods.
- Reproducibility: none of the found works releases an end-to-end automated pipeline for this task (not checked exhaustively; UNVERIFIED for the full-text supplements).

## Searches (21 run; databases: PubMed, Europe PMC, OpenAlex, Semantic Scholar, medRxiv, web)

Found relevant material:
1. DOI lookups for the four named papers (all confirmed to exist; metadata and abstracts opened).
2. PubMed: Trial Pathfinder / oncology eligibility with real-world data (confirmed, plus two follow-ups).
3. PubMed: NHANES generalizability cardiovascular trials eligibility (found two blood pressure studies).
4. PubMed: SARS-CoV-2 vaccine trials older adults (abstract of work 2).
5. OpenAlex: LLMs extracting eligibility criteria at scale with real-world linkage (found AutoCriteria, the JMIR AI paper, the oncology-scale protocol, trial corpora).
6. OpenAlex: criteria to SQL / OMOP / LLM cohort translation (Criteria2Query lineage).
7. PubMed: broadening eligibility and FDA guidance (found only commentary and oncology-specific items).
8. PubMed: stroke/population-based eligible proportion (found Alzheimer and one Chinese SPRINT-eligibility survey study, not LLM-based).
9. OpenAlex: cardiovascular outcome trials, kidney disease exclusion (found the kidney representation review).
10. Web search: LLM criteria plus NHANES plus cardiovascular (found only the language-restriction preprint and an unrelated LLM retrieval paper).
11. Fetch of the GLP-1/BMI paper full text (opened).

Found nothing relevant:
12. PubMed: "large language model eligibility criteria structured population coverage" (zero results).
13. PubMed: "eligible population estimate heart failure trials ... real-world proportion eligible" (only a device-registry mapping study for one LVAD trial, 2021; not an LLM or survey approach).
14. PubMed: "heart failure randomized trials eligibility NHANES representativeness" (zero results).
15. PubMed: "cardiovascular trials exclusion criteria trends over time industry vs non-industry sponsor" (zero results).
16. PubMed: "trial generalizability ... GIST generalizability index" (zero results).
17. PubMed: "eligibility criteria heart failure trials ... renal function age cap analysis" (zero results).
18. PubMed: "hypertension trials NHANES proportion eligible SPRINT ACCORD" (zero results in the form run; the two blood pressure studies above came from search 3).
19. Semantic Scholar 2023 onward: "proportion of US adults excluded by trial eligibility criteria automated extraction NHANES" (zero results).
20. medRxiv: "eligibility criteria large language model population eligible NHANES trials" (only unrelated records returned).
21. Europe PMC: "GPT-4 extract numeric eligibility criteria ... population survey" (only conference-abstract front matter returned).
Also: PubMed Criteria2Query query errored (tool error), so that topic was covered via OpenAlex only.

Caveat: these tools index titles and abstracts; a paper that does this in its methods but not its abstract could be missed. A search in a full-text index and a forward-citation check of works 1 and 6e were not done.

## Main risk to novelty

1. The GLP-1/BMI paper (row 1) shows the design (registry criteria, automated parsing, NHANES, per-criterion shares) in 2026. A reviewer can call our method incremental. Mitigation: state clearly that we differ in scope (several cardiovascular conditions, 2005-2024 versus 2017-2020), in a validated LLM extraction to structured triples, in the trend and sponsor analyses, and in releasing a reproducible pipeline.
2. Similar work may be in preparation or in a full-text-only index; monitor before submission.
3. Dependence on LLM extraction quality: extraction error rates must be measured against a manually labeled sample or the claim of a scaled automated method is weak (AutoCriteria reports about 89 F1 for entities, a lower bar than our output needs).
4. Interpretation risk: a criterion's NHANES share ignores clinical judgement criteria and unmeasured conditions, so shares are lower bounds on exclusion. The older systematic review makes the same caveat.
5. NHANES has no registry-matching for disease definitions in some conditions (heart failure, stroke subtypes) and uses self-report; this may limit the "with the condition" denominator and invite criticism.
