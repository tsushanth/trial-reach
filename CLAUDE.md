# Instructions for any assistant session working in this repository

1. Read `DATA_POLICY.md` before anything else. This repository is public. Never write personal information, data,
   record identifiers, data locations (paths, links to data files or data services) or source-record excerpts into any file,
   commit message, issue or pull request. Use invented synthetic text in tests.
2. Read `docs/research-log/00-status.md` and `docs/research-log/README.md` to recover context. At the end of every working
   session update `00-status.md` and add dated entries to the other log files. Aggregates only.
3. Method changes after a first analysis run must be recorded in the `PROTOCOL.md` change log with a reason. Results under
   changed rules are exploratory.
4. Run `sh scripts/install_hooks.sh` once per clone. Never bypass the guard hooks. Do not weaken a rule to let a commit pass.
5. Commits: no AI attribution lines in this public repository.
6. Restricted note text goes only to local models, never to a hosted service. Hosted assistants see aggregates only.
7. Check prior work before building or claiming novelty; say how many searches the check rested on.
