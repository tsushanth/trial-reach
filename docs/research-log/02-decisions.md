# Decisions and reasons

- **Patient-level evaluation, not note-level.** Clinical use needs the first-event date; report-level accuracy hides how
  errors propagate. (Early.)
- **Local models only for any restricted text.** Terms of the restricted datasets forbid sending notes to hosted services.
- **Preregister before looking.** Prompts, policies and sample sizes frozen and hashed before held-out runs; development and
  test data kept separate.
- **No tuning on the 2022 or 2023 trial-matching sets.** The criterion-level method was developed only on unused 2021
  topics; 2023 was a single frozen run (2026-10-22 results in findings).
- **Unknown-criterion policy: lenient.** Chosen on development data only; strict policies did worse.
- **Stop the larger-model 2023 run (2026-10-22).** The 7B result already answered the main claim; partial output not analysed.
- **Move to the whole medical field (2026-10-22).** Owner direction: use language models to advance medical research, start
  with the most serious ailments, and rank easy data access higher.
- **Choose project 1 (2026-10-22).** Highest data access (both sources verified downloadable with no application), a
  question about whose health the evidence covers, and a method the harness already supports.
- **Public repository with a strict no-data rule (2026-10-22).** Code, protocol and aggregate findings only; enforced by
  an automated guard in hooks and CI. Reading used: names of public source kinds are allowed in prose; identifiers, paths,
  links, excerpts and personal information are not.
