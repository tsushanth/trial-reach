# Status (updated 2026-10-22)

**Goal.** Do real, publishable public-good research in medicine with language models, using data that an independent
researcher can actually get. Priority is the most serious ailments, and easy data access ranks a question higher.

**Where we are.** Earlier work on extracting disease-progression dates from clinical notes produced a tested evaluation
harness and several honest side findings, but no result that stands alone as new clinical-AI research (see
[findings](findings/) and [01-arc.md](01-arc.md)). On 2026-10-22 the owner judged that this is not yet useful research and
asked to keep searching. A literature gap scan ([05-gap-scan.md](05-gap-scan.md)) ranked five projects. Project 1 was chosen.

**Active project (this repository).** Who do cardiovascular trials leave out? Local-model structuring of trial eligibility
criteria plus a public survey to estimate population reach. Protocol: [PROTOCOL.md](../../PROTOCOL.md), version 0.1.
Current step: labelling guide, criterion vocabulary, extraction prompt and parser (see the code in `src/trial_reach`).

**Paused or parked.**
- Progression-date extraction from notes: waiting on real notes with dated labels (credentialing application submitted;
  response pending). Harness exists locally and is not yet in this repository.
- Larger-model run of the 2023 trial-matching test: stopped on 2026-10-22, partial output deliberately not analysed.
- Literature audit tool: fresh-sample numbers recorded in findings; human spot-check of adjudications still owed.

**Open questions for the owner.**
1. Wording of the data rule: allowed to name kinds of public source in general terms in prose (current reading)?
2. Who does the clinical or trained-reviewer check on at least 25% of the gold-set labels?

**Standing constraints.**
- Only local models touch any restricted note text. Hosted assistants see aggregates only.
- Pre-register methods before looking at held-out results; report negative results.
- Check prior work before building (the novelty check on the first GENIE finding showed it was already known).
