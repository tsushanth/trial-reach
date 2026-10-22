# trial-reach

Who do cardiovascular clinical trials leave out?

This project uses a locally run open language model to turn the free-text eligibility criteria of registered trials into
structured rules, and then estimates what share of US adults with the condition those rules would admit, using public
national survey data. The aim is a transparent, reproducible measure of how well trial populations cover real patients.

Status: protocol stage. No results yet. See [PROTOCOL.md](PROTOCOL.md). The running record of all research so far, including
earlier work and its findings, is in [docs/research-log](docs/research-log/README.md).

## What this repository contains

Code, documentation and the protocol. Nothing else.

## The data rule

This is a public repository with a strict rule: **no personal information, no data, no record identifiers and no data
locations, ever.** The full policy is in [DATA_POLICY.md](DATA_POLICY.md) and is enforced by an automated check that runs
before each commit and in CI.

To work with the code you supply your own copy of public data outside this repository and point the code at it through an
environment variable. Nothing about where you keep it is recorded here.

## Getting started

```sh
sh scripts/install_hooks.sh     # activates the pre-commit and pre-push guards in your clone
python3 -m pytest -q            # tests
```

## License

MIT.
