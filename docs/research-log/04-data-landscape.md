# Data landscape (kinds, access, status as of 2026-10-22)

No identifiers, forms, ids or contact details are recorded here.

| Kind of data | What it offers | Access | Status |
|---|---|---|---|
| Open model-derived (silver) progression calls on radiology reports for tens of thousands of cancer patients | Dated report-level calls; no text | Open | Used |
| Consortium curated cancer data (human-curated imaging, oncologist assessments, progression, regimens) | Gold-like dated labels; no note text | Application, terms: aggregates only, citation and acknowledgement required | Access granted and used (lung cohort) |
| Credentialed hospital notes (discharge, radiology) and a small oncology-note set | Real note text | Training, credentialing application, reference, per-dataset agreement | Application submitted 2026-10-22; response pending |
| Commercial real-world oncology datasets | Curated outcomes at scale | Institutional partner, protocol, ethics review, contract, months | Enquiry sent; no reply yet |
| Clinical NLP corpora with temporal annotation (cancer notes) | Notes with temporal labels | Membership and data use agreement | Not applied |
| Professional-society oncology data program | De-identified real-world data | Committee review, fees | Not applied |
| Trial matching benchmark (three annual editions) and an annotated eligibility corpus | Patient descriptions, trial text, graded labels | Open | Used |
| Public trial registry (interventional trials, eligibility text) | Criteria text and metadata | Open API, no key | Verified downloadable 2026-10-22 |
| Public national health survey with examination and laboratory data and weights | Population stand-in | Open files | Verified downloadable 2026-10-22 |
| Literature (open-access full text) | Papers for audits and extraction | Open API | Used |

Handling rules: only local models touch restricted note text; hosted assistants see aggregates only; restricted datasets are
kept outside every repository; terms of each source are followed (citation, acknowledgement, no redistribution).

Lessons: institutional routes take months and usually need a partner; open data with real note text and dated labels does
not exist; therefore projects that run on open data rank higher.
