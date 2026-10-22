# Report-level errors to patient-level first-progression error

- Simulation (open silver labels as proxy truth): independent report-level errors at precision and recall near 0.8 move
  the patient-level first-progression date by several months and shift median time to progression by about 6 months. Written
  before real curated labels were available.
- Real check (2026-10-22, 784 linked patients, curated imaging labels as truth, matched scans only, in-sample for the model,
  day offset between the two time axes fitted per patient): the model has scan-level precision 0.78 and recall 0.80;
  first-progression agreement within 30 days is **76.0%** (n = 551). Independent errors at the same precision and recall
  predict 68.0% (2.5 to 97.5%: 64.5 to 71.7%). Counting model calls on unmatched scans gives 65.7%.
- Reading: real errors cluster, so the independent-error simulation is conservative for this model. It should not be used to
  predict a specific model's patient-level error from report-level metrics.
- Caveats: in-sample, fitted offset, one cancer type, one institution.
