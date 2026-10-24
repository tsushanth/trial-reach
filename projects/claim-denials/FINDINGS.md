# Findings, first pass (2026-10-23): official marketplace transparency data

Aggregates only; issuer-level tables are kept private (see the protocol). Source: insurer-reported counts for individual-market plans on the
federal marketplace platform, releases 2022 to 2026, service years assumed to be the release year minus two. The assumption is supported:
pooled in-network denial rates of 19.7% (service year 2023) and 18.7% (2024) match the 20% and 19% published by KFF for those years from the same
file. Issuer-state cells with fewer than 1,000 claims are excluded from rates; implausible rows (denied above received, or overturned above filed)
are excluded and number 0 to 2 per release.

## Q1. Level and spread of the all-network denial rate across issuers

| Service year | Issuers with a rate | Median | Quartiles | Share above 30% | Pooled, claim-weighted |
|---|---|---|---|---|---|
| 2020 | 144 | 18.0% | 11.2 to 27.9 | 20% | 18.3% |
| 2021 | 161 | 15.9% | 9.4 to 22.3 | 10% | 16.6% |
| 2022 | 172 | 18.4% | 14.2 to 23.4 | 14% | 17.8% |
| 2023 | 174 | 20.7% | 15.2 to 26.8 | 18% | 20.9% |
| 2024 | 155 | 21.0% | 17.0 to 27.1 | 13% | 20.4% |

About a fifth of reported claims are denied in this market, and the middle half of issuers sits within roughly 10 percentage points of each other.

## Q2. Persistence of issuer rates

Spearman correlation of issuer rates in consecutive service years: 0.53 (2020 to 2021), 0.51 (2021 to 2022), 0.75 (2022 to 2023), 0.82 (2023 to 2024),
among 139 to 155 issuers. The share of issuers whose rate moved by more than 10 percentage points in a year: 25%, 22%, 7%, 14%.
Reading: issuer differences are only moderately persistent in the early years and clearly persistent in the latest two, which is also when the release
began to split in-network and out-of-network claims. Rates from the early years should not be used to compare issuers.

## Q3. Reporting quality

0 to 2 implausible issuer-rows per release (of 185 to 230). Issuers without a usable rate (suppressed, missing, or under 1,000 claims): 69, 69, 37, 32, 30
across the five releases. Large year-to-year swings for a quarter of issuers in the early years point to reporting inconsistency.

## Q4. Appeals

Internal appeals filed per denied claim: 0.1% to 0.4%. Pooled share of internal appeals overturned: 37%, 41%, 43%, 44%, 34% by service year 2020 to 2024.
External appeals: pooled overturn 37%, 49%, 64%, 35%, 36%, but only 15 to 33 issuers meet the minimum of 10 appeals, so these are noisy. Almost all denials are never appealed.

## Q5. Denial reasons (plan level)

Reason categories changed over the years, and a large "other" bucket (32% to 76%) limits interpretation. For service years 2022 to 2024: administrative 18% to 23%,
excluded service 12% to 17%, referral 7% to 8%, out-of-network 6% to 10%, medical necessity 5% (2% to 3% in 2020 and 2021). Medical necessity is a small share of reported denials.
The issuer denial rate is not positively related to the administrative share (Spearman -0.26, -0.18, -0.02).

## Q6. Denials and resubmission (service years 2022 to 2024)

Issuer denial rate and the share of claims resubmitted are positively related (Spearman 0.45, 0.36, 0.26). Part of what is reported as denial is claims that are corrected and sent
again, so a reported denial is not necessarily a final refusal.

## What this supports and does not support

- It supports: the level of reported denials in this market, the persistence of issuer differences in recent years, how rarely denials are appealed, and a warning that reported denials include administrative rejections and resubmissions.
- It does not support: any statement that an issuer is better or worse, comparisons with employer plans, Medicare Advantage or Medicaid, or conclusions about final refusals. Counts are insurer-reported and unaudited here.
- Next options: add the Medicare Advantage prior-authorization series; check the survey-year definitions; plan the lawyer review before any issuer-level publication.

## Medicare Advantage prior authorization, free route (2026-10-24; protocol 0.4; provisional, read by an assistant from public pages, not yet re-checked)

No organisation names here (private working table only).

- **Cross-check, published national figures (health-policy research organisation, from the federal determinations data):** 2024: 52.8 million determinations, 7.7% denied, 11.5% of denials appealed, 80.7% of appeals partly or fully overturned. 2023: 49.8 million, 6.4% denied, 11.7% appealed.
  2022: 7.4% denied in the text, other 2022 figures only in a chart. Per-parent denial rates for 2024 ranged from about 4% to about 13% among the four largest parents with text figures.
- **Payers' own postings (first postings under the 2026 rule, calendar-year 2025 data):** of the 10 largest parents, 5 had a retrievable page (the page for 4 of them covered one contract or region, not the whole parent); 4 had no findable Medicare Advantage page; 1 could not be identified.
  Standard-request denial percentages in the retrievable postings ranged from about 6% to 16% (one contract each, except one parent summed over its contracts: about 13%), expedited from about 4% to 17%.
- **Comparability problems found:** parents post at different levels (all contracts in one table, one document per contract, or by region); "approved after appeal" has different or unstated denominators; one parent posts percentages only, others counts; decision times are in days or in hours; no payer states whether withdrawn requests are excluded; one parent's web headline excludes categories that its document includes.
- **One unexplained gap:** an independent published 2025-postings brief gives a different standard denial rate for the largest parent (17%) than the sum computed here from its contract table (13.5%); not resolved.
- **A third-party tracker's claims** (coverage, national rate) are unverified and conflict with the published enrollment figure for the largest parent.
- **Reading:** a pooled cross-organisation comparison from postings is not currently feasible without per-contract reading of dozens of documents and assumptions about definitions. The national figures from the published analysis remain the usable benchmark; contract-level history would need the paid limited data set.
