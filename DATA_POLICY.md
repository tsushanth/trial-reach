# Data policy

This repository is public. The rule is absolute:

> Nothing in this repository may contain personal information, data, record identifiers, or pointers to where data is kept.

## What is forbidden

- Any file of data, in any format: tables, spreadsheets, survey files, databases, archives, serialized objects, model files,
  documents and PDFs. The ignore file and the guard both reject these file types.
- Personal information of any kind: names of individuals other than the maintainer handle, email addresses, phone numbers,
  government or medical record numbers, and anything that could single out a person.
- Record identifiers: trial registry numbers, survey respondent numbers, patient or participant identifiers. Describe a
  record by its properties, never its identifier.
- Excerpts of source records, including eligibility text, free-text fields and survey values, even a single line. Tests use
  invented synthetic text only.
- Data locations: local file system paths, data directory names, download links to data files or data APIs, and the names of
  private or restricted datasets.
- Secrets: tokens, keys and passwords.

## What is allowed

- Code, tests that use invented synthetic examples, and documentation.
- Method descriptions that name a kind of public source in general terms, such as "a public trial registry" or "a national
  health survey", without identifiers, paths or links to the data.
- Aggregate results (counts, rates, intervals) once a protocol says they may be published. Aggregates must be large enough
  that no individual can be inferred.

## How it is enforced

- `scripts/check_no_data.py` scans every tracked and untracked file. It reports file, line and rule, never the matched text.
- `scripts/install_hooks.sh` installs it as a pre-commit hook.
- CI runs it on every push and pull request.
- Do not weaken a rule to let a commit through. Remove the offending content.

## If something slips through

Treat it as an incident: remove it, rewrite history so it is gone (not just deleted in a later commit), and rotate anything
that was a secret. Report it in an issue without repeating the content.
