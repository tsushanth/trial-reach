# Project 2: what official data say about health-insurance claim denials and appeals (research track)

Version 0.1, 2026-10-23. Written before any result exists. Changes after the first analysis run go in the change log with a reason.

## Why this, and what it is not

Owner idea: a directory that helps people choosing insurance and people who were denied. A parallel scan of prior art, public data, law and
credibility design (research log, 2026-10-23) concluded that a crowdsourced ranking of insurers cannot be defended: reports are self-selected,
denominators are unknown, and rankings written by the site carry legal risk. The owner chose the research track. This first study asks what
the **official, insurer-reported public data** can and cannot say, before any crowdsourcing. It publishes nothing about individual patients.

## Source (kind only)

The federal marketplace transparency file: one release per plan year, issuer- and plan-level counts of claims received, denied and
resubmitted, internal and external appeals filed and overturned, for individual-market qualified health plans on the federal marketplace
platform. Self-reported by issuers. Releases up to 2023 report one combined all-network figure; releases from 2024 split in-network and out-of-network claims. (An earlier draft of this
protocol wrongly said the split starts in 2022; see the change log.)
Assumption to verify against the data dictionary: the claims in a release refer to services two calendar years earlier.

## Questions (all descriptive; no causal claims)

1. **Level and spread.** For each service year with the split format, what is the distribution across issuers of the in-network claim
   denial rate (denied divided by received)? Report median, quartiles, and the share of issuers above 30%.
2. **Persistence.** Are issuer denial rates stable across consecutive service years (Spearman correlation among issuers with at least 1,000
   in-network claims in both years)? Low persistence would mean the differences between issuers are dominated by definition or reporting
   noise, not by real differences; high persistence would mean issuer differences are at least consistent.
3. **Reporting quality signals.** Share of issuer-years with suppressed or missing values; share with implausible values (denied greater
   than received; appeals overturned greater than appeals filed); share of issuers whose rate changes by more than 10 percentage points between
   consecutive years.
4. **Appeals.** Among denied claims, what share receive an internal appeal; among internal appeals, what share are overturned; and the same
   for external appeals. Report the distribution across issuers and the pooled figure.
5. **Denial composition (plan level, where reported).** Share of denials by reason category (referral, out-of-network, excluded service,
   medical necessity, benefit limit, member not covered, investigational, administrative, other). Is the issuer-level denial rate related to
   the administrative share?
6. **Resubmission.** Is the in-network denial rate related to the resubmission rate (resubmitted divided by received)? A positive relation
   would suggest many reported denials are corrected paperwork, which weakens the "denial equals refusal" reading.

## Definitions and rules fixed in advance

- Denial rate = in-network claims denied / in-network claims received at the issuer level. Out-of-network reported separately.
- Issuer unit = issuer id within state (issuer-level values repeat across plan rows and are taken once per issuer-state).
- Suppressed (`**`), not available (`*`), not applicable (`N/A`) and blank values are missing. Missing values are never imputed.
- Minimum size for any issuer-level statement: at least 1,000 claims received in the cell. Cells below it are excluded from rates and counted.
- Appeals rates use appeals filed divided by claims denied; overturn rate uses overturned divided by filed. Cells with fewer than 10 appeals excluded from the rate.
- Pooled figures sum numerators and denominators over included issuers (claim-weighted) and are labelled so; issuer distributions are unweighted.
- Implausible rows are reported in question 3 and excluded from questions 1, 2, 4.

## What will be published, and what will not

- In this repository: aggregate distributions, correlations, counts of issuers and data-quality shares. No issuer names and no issuer-level
  tables here.
- Named issuer-level tables stay private until the owner decides, after legal review (research log: defamation and presentation risk).
  Anything about named issuers, if later published, must be mechanically produced, carry the source's own caveats, show the denominator and year,
  and never be called a quality rating.
- Required caveats on every result: insurer-reported; marketplace individual plans on the federal platform only, so no employer plans, Medicare
  Advantage or Medicaid; denials include administrative rejections and are not final refusals; prior-authorization denials excluded; appeals are
  a small self-selected subset of denials.

## Threats to validity

- Definitions of "denied" may vary across issuers despite the instructions.
- The file covers a minority of insured people; results do not generalise to employer coverage.
- Issuers appear and exit; persistence is measured only on those present in consecutive years.
- With a census of reported claims, sampling error is not the issue; reporting error is, and cannot be measured from this file alone.

## Reproducibility

Code in `src/claim_denials`, tests on invented synthetic workbooks only. The code reads the source files from a directory given by an
environment variable. Nothing about where the files live is stored here.

## Change log

- 0.1 (2026-10-23): initial protocol.
- 0.2 (2026-10-23, after the first run showed no rates for the 2022 and 2023 releases, which turned out to use a combined all-network format; no
  analysis choice was changed on the basis of results): the primary series is the **all-network** denial rate, available in every release 2022 to
  2026 (combined figure, or in plus out for split releases). The in-network rate is secondary and exists for releases 2024 to 2026 only. Questions 1, 2
  and 6 use the all-network series as primary. The loader now also strips stray quotes from header names.
- 0.3 (2026-10-23, no data touched): attempted an extension to a Medicare Advantage prior-authorization series (organization determinations and
  reconsiderations, Part C reporting requirements, contract level, years about 2019 to 2024). Finding: the federal agency publishes the reporting
  requirements and technical specifications, but no downloadable file of the reported counts was found on its public reporting pages. The reported
  data exist only as a limited data set, one dataset per reporting section, sold per file and year through an order form and payment step, released
  about the fourth quarter of the following year with no guaranteed timing. Whether a data use agreement is required is UNVERIFIED (the pages
  fetched did not say; limited data sets from this agency normally need one). A separate service-level pilot collection announced in December 2025
  is not a public file. Decision: stop; no loader, no analysis, no result. If the owner later obtains the limited data set, the questions below
  are fixed in advance (same size rules as above: cells under 1,000 determinations and appeal cells under 10 excluded):
  (1) distribution across contracts of the denial rate by year; (2) Spearman persistence of contract rates across consecutive years;
  (3) appeal rate among denials and overturn rate among appeals, pooled and by contract distribution; (4) data quality (implausible or suppressed
  values); (5) pooled national denial rate compared with the published KFF figures (6.4 percent for 2023, 7.7 percent for 2024, prior authorization)
  as a cross-check only. Caveats to carry: self-reported; Medicare Advantage only; service determinations only; whether partial denials count as
  denials must be read from the dictionary before any run.
