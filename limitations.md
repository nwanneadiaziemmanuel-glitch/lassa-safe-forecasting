# Limitations

1. The weekly series is a compiled secondary surveillance dataset.
2. Structural completeness of the CSV does not prove complete surveillance reporting.
3. Reporting delay, backfill, revisions and surveillance-practice changes are not fully modelled.
4. 2025 is partial through epidemiological week 46.
5. Epi week 53 has only one observation in the supplied series and should not be over-interpreted.
6. The primary model is intentionally lightweight and is not a diffusion, mechanistic or deep-learning forecasting system.
7. The V1 synthetic augmentation method is a simple target-resampling stress-test baseline, not a validated generative model.
8. Archived V1 synthetic-fidelity results use the original analytical subsets; their maxima should not be interpreted as full-year maxima without that context.
9. Archived V1 uncertainty results used a single 95% interval score that was originally labelled WIS; V1.1 corrects the terminology to Interval Score (IS95).
10. Archived V1 augmentation, uncertainty and robustness tables were produced by an earlier analytical pipeline and are therefore separated from the corrected V1.1 core runner.
11. The V1.1 core analysis is an expanding year-based temporal holdout, not a full rolling-origin evaluation.
12. No external-country validation is included.
13. No clinical utility, causal inference or operational outbreak-response decision claim is made.
14. Individual-level surveillance records are not redistributed.
