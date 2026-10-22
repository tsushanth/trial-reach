# Literature audit tool (Mendelian-randomization papers)

Question: how often do open-access Mendelian-randomization papers state key methodological safeguards? Tool counts what the
text says, with evidence and polarity, not what authors did.

- Detectors tuned on 300 development papers and 200 validation papers, then adjudicated by the assistant (not independent human
  validation). Detectors frozen (v0.3) before a fresh random sample (200 papers, 184 judged primary analyses).
- Fresh-sample statements: Steiger directionality test 20.1% (95% CI 15.0 to 26.5); sample overlap addressed 29.9%
  (23.7 to 36.9); STROBE-MR named 26.1% (20.3 to 32.9); code publicly shared 9.2% (5.8 to 14.3); pre-registered 1.6%
  (0.6 to 4.7).
- Independent reader check (a local 8B model) agreed well on some features (kappa 0.99 Steiger) and poorly on others where
  the reader was lenient (code sharing kappa 0.21); disagreements were adjudicated and became regression tests.
- Still owed: a human spot-check of the adjudications. Recall outside the keyword filter is unmeasured.
