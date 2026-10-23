# Status (updated 2026-10-22)

**Goal.** Do real, publishable public-good research in medicine with language models, using data that an independent
researcher can actually get. Priority is the most serious ailments, and easy data access ranks a question higher.

**Where we are.** Earlier work on extracting disease-progression dates from clinical notes produced a tested evaluation
harness and several honest side findings, but no result that stands alone as new clinical-AI research (see
[findings](findings/) and [01-arc.md](01-arc.md)). On 2026-10-22 the owner judged that this is not yet useful research and
asked to keep searching. A literature gap scan ([05-gap-scan.md](05-gap-scan.md)) ranked five projects. Project 1 was chosen.

**Active project (this repository).** Who do cardiovascular trials leave out? Local-model structuring of trial eligibility
criteria plus a public survey to estimate population reach. Protocol: [PROTOCOL.md](../../PROTOCOL.md), version 0.1.
Current step (2026-10-22): development extraction runs showed only about a quarter of trial criteria are computable from a
population survey ([findings](findings/trial-reach-development.md)); deciding whether to reframe from per-trial reach to
per-criterion exclusion burden before gold labelling starts. Gold and validation sets untouched.

**Project 1 update (2026-10-23):** bulk extraction complete (13,335 trials, about $9.3 of hosted-model spend, 0.004% lines failed). First full burden run failed validity checks and was corrected
post-hoc (protocol 0.8); corrected run B findings in `docs/research-log/findings/trial-reach-burden.md` (exploratory). Prior-work check: partly done (closest is a 2026 study of BMI criteria in 352 GLP-1
trials with the same survey); positioning is scale, automation, cardiovascular focus, trends and sponsor analysis (`findings/trial-reach-prior-work.md`). Human review form built (private); awaiting the reviewer.

**Second project (research track, started 2026-10-23): official claim-denial data.** Protocol `projects/claim-denials/PROTOCOL.md`, first findings
`projects/claim-denials/FINDINGS.md` (pooled reported denial rate about 17% to 21%, persistence of issuer differences only moderate in early years,
under 0.5% of denied claims appealed, reported denials include resubmissions). The crowdsourced directory idea was scanned by five parallel
research tracks (prior art, public data, legal and privacy, credibility design, appeal avenues); decision: no crowdsourced ranking of insurers;
research first, any outcomes collection only after a lawyer reviews and ideally with an existing appeal-tool partner. Issuer-level tables stay private.

**Paused or parked.**
- Progression-date extraction from notes: waiting on real notes with dated labels (credentialing application submitted;
  response pending). Harness exists locally and is not yet in this repository.
- Larger-model run of the 2023 trial-matching test: stopped on 2026-10-22, partial output deliberately not analysed.
- Literature audit tool: fresh-sample numbers recorded in findings; human spot-check of adjudications still owed.

**Decision 2026-10-22 (owner): treat hosted extraction of public registry text as permitted** ("otherwise they would have had us sign
something"). Not confirmed against the registry's terms page; recorded as an assumption. Model: claude-haiku-5-5, per-line extraction,
structured output, public trial text only, hard spend cap in code. Estimated cost for about 1,900 trials: a few dollars (about 38,000
short calls). Waiting on a credential supplied by the owner in the environment.

**Open questions for the owner.**
1. Wording of the data rule: allowed to name kinds of public source in general terms in prose (current reading)?
2. Reframe project 1 to criterion-level exclusion burden (recommended), and local sample versus hosted model for extraction at scale?
3. Second reviewer for gold labels: named (independent family member, blind to model output).

**Standing constraints.**
- Only local models touch any restricted note text. Hosted assistants see aggregates only.
- Pre-register methods before looking at held-out results; report negative results.
- Check prior work before building (the novelty check on the first GENIE finding showed it was already known).
