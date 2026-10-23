# Attorney consultation brief: health-insurance claim-denial research and directory

This is a planning document for a first consultation. It is not legal advice. Legal points below come from a preliminary research pass and are marked "unverified" where they were not checked against the primary source. We are asking the lawyer to confirm, correct or replace them.

## 1. Summary of the plan

**Who:** An independent researcher with no institution. A sole-proprietor LLC exists. The work is non-commercial for now. We have not decided whether to form a nonprofit or a company.

**Phase A (first): publish research on official, insurer-reported denial statistics.**
- Source: the federal marketplace transparency file. Insurers report it. It is public domain.
- Coverage: individual-market plans on the federal platform only. It excludes employer coverage, Medicare Advantage and Medicaid.
- Known flaw: reported "denials" include administrative rejections and resubmissions, so the figures are not clean medical-necessity denial rates.
- Intent: possibly name insurers next to their reported figures, with plain caveats about what the data does and does not measure.

**Phase B (later): an opt-in directory of patient-submitted denial experiences.**
- Users submit: insurer, plan type, procedure or condition category, denial reason, appeal outcome, and optionally an uploaded denial letter.
- The site summarises submissions per insurer.
- Optional extra: a moderated, pseudonymous way for people in similar situations to contact each other.

**Not planned:** advertising, selling data, individual appeal advice, or accepting minors. Risk-reducing design choices are listed under each issue below.

## 2. Issues in priority order

### HIGH 1. Health-data privacy (mainly Phase B)
- **Risk:** Users hand us health-related information. HIPAA probably does not apply to a site collecting users' own data directly (not a covered entity or business associate), but this is unverified against HHS guidance. Other regimes may apply instead:
  - FTC Health Breach Notification Rule. Unauthorized disclosure counts as a breach. Notice is due within 60 days, and to the FTC if 500 or more people are affected.
  - FTC Act section 5. The FTC acted against GoodRx and Premom over sharing health data with advertisers. Trackers on pages that hold health data are the classic trap.
  - Washington My Health My Data Act: consent, a separate health privacy policy, and a private right of action.
  - Nevada SB 370 and Connecticut SB 3: reported to have no nonprofit exemption (unverified).
  - California CCPA/CPRA sensitive-data rules: generally for for-profit businesses above thresholds.
  - State breach-notice and data-retention laws: not researched.
- **Best sources:** 16 CFR Part 318 (https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-318); FTC health breach guidance (https://www.ftc.gov/business-guidance/privacy-security/health-breach-notification-rule); HHS guidance on covered entities (https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html); Washington RCW chapter 19.373.
- **Lawyer must decide:** whether we are outside HIPAA; which state laws bind us given users can be anywhere; whether a launch should be limited by state; what consent and privacy-policy wording is required.
- **Design choices:** no ad or analytics trackers on submission pages; collect the minimum; separate health privacy policy; explicit consent; deletion on request; retention limit; breach response plan.

### HIGH 2. Defamation and business disparagement of named insurers (Phases A and B)
- **Risk:** Section 230(c)(1) protects hosting other people's content. It does not protect content the site itself creates or develops (230(f)(3)). A mandatory structured form that elicits the content may cost protection (Fair Housing Council v. Roommates.com, 9th Cir. en banc; not yet read by us). Statements we write, such as "Insurer X denies N percent of claims," are our own speech, including in Phase A. Anti-SLAPP statutes exist in about 40 states plus DC and vary a lot. How insurers actually handle takedown demands: not researched.
- **Best source:** 47 U.S.C. 230 (https://www.law.cornell.edu/uscode/text/47/230).
- **Lawyer must decide:** how to word insurer-specific statements in Phase A; whether our form design keeps 230 protection; which state's anti-SLAPP law is likely to apply; whether and how to run a takedown and reply process.
- **Design choices:** user-reported data only, labelled self-reported and not representative; mechanical summaries with method, sample size and date; official figures shown beside crowdsourced counts, noting they measure different things; insurer right of reply and a published takedown policy; no claims about why an insurer denies.

### MEDIUM 3. FTC rule on consumer reviews and testimonials (Phase B)
- **Risk:** 16 CFR Part 465 (effective October 2024) bans fake reviews and review suppression. Unclear whether a denial directory counts, or whether takedowns count as suppression.
- **Source:** https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465
- **Decide:** whether it applies; what moderation is safe.
- **Design:** published moderation criteria applied equally; no incentives; no removal for being negative.

### MEDIUM 4. Uploaded denial letters contain identifiers
- **Risk:** Letters carry names, member numbers, diagnoses and dates. No de-identification standard has been confirmed for sites outside HIPAA.
- **Decide:** whether to accept uploads at all; what counts as de-identified; handling subpoenas.
- **Design:** extract only structured fields, then delete the original; or no uploads at launch.

### MEDIUM 5. Peer-to-peer contact
- **Risk:** scams, harassment, and any duty of care we take on.
- **Decide:** terms, disclaimers, whether to offer it at all, insurance.
- **Design:** relay messaging (no contact details shared), double opt-in, block and report, moderation, pseudonyms.

### MEDIUM 6. Unauthorized practice of law or medicine
- **Risk:** State-specific. The sources found concern Medicaid and say that applying law to a person's particular facts is the practice of law, while general information is allowed. Unverified for our setting.
- **Decide:** where the line sits; required disclaimers.
- **Design:** general appeal information only, no tailored letters.

### MEDIUM 7. Minors
- **Risk:** COPPA applies to children under 13; teens raise separate state issues.
- **Decide:** whether an 18+ gate is enough.
- **Design:** 18+ only, age confirmation, no collection from known minors.

### LOW 8. State insurance advertising or unfair-practices rules on insurer comparisons
Not researched. Ask whether any state rule covers a non-insurer comparison.

### LOW 9. Nonprofit versus company structure
It affects some privacy statutes (Issue 1) but not defamation or Section 230. Ask about timing and whether the current LLC gives adequate liability separation.

## 3. Questions for the lawyer

**Privacy (Issue 1)**
1. Do you agree HIPAA does not apply to a site collecting users' own data directly? What would change that?
2. Does the FTC Health Breach Notification Rule apply, and what are our notice duties?
3. Which state health-privacy laws apply to a small, possibly non-commercial operator, and can we launch in limited states?
4. What consent flow and health privacy policy are required?
5. What retention period is defensible, and how do we handle subpoenas?

**Defamation and Section 230 (Issue 2)**
6. May we publish named-insurer figures from the official file, and what wording and caveats are safest?
7. Does a structured submission form risk losing Section 230 protection for Phase B summaries?
8. Are per-insurer summaries our own speech, and what method statements help?
9. Which anti-SLAPP law would likely apply, and what is our exposure to a demand letter?
10. How should we design the insurer reply and takedown policy?

**Reviews, uploads, contact, practice of law, minors (Issues 3-7)**
11. Does the FTC reviews rule apply, and is our moderation policy consistent with it?
12. Should we accept uploaded letters, and what de-identification is enough?
13. What terms and liability limits should messaging have, and is it worth offering?
14. Where is the line between general appeal information and unauthorized practice of law?
15. Is an 18+ gate sufficient?

**Structure and engagement (Issues 8-9)**
16. Should the work sit in the current LLC, a new entity or a nonprofit before Phase B? What insurance?
17. What must happen before Phase A versus only before Phase B?
18. Roughly what would policy and terms review cost, and is a limited-scope engagement possible?

## 4. Documents to bring
- This brief.
- LLC formation papers and operating agreement.
- A sample Phase A write-up with insurer tables and caveat wording.
- Mock-ups of the Phase B form and summary pages.
- Draft privacy policy, health privacy policy, terms and takedown policy (even rough).
- A data-flow sketch: what is collected, stored, who has access, what is deleted when, which third-party services.
- The official file's documentation and definition of "denial."
- Existing insurance policies; any funding or affiliation plans.

## 5. What we do NOT want from the lawyer
- No guarantee of outcome, or assurance that we will not be sued or receive a demand letter.
- No sign-off on facts or conclusions of the research (the research is ours and the legal points here are unverified).
- No ongoing role as our compliance monitor unless we agree it separately.
- No advice on individual users' insurance appeals or claims.
- We want identified risks, a ranking, options and a recommended order of steps, with clear statements of what is uncertain.
