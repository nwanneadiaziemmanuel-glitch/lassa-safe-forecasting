# Changelog

## 1.1.0 — 2026

- Added leakage-controlled expanding temporal holdout for the core forecasting runner.
- Corrected 52-week seasonal-naive target alignment.
- Added explicit forecast-horizon alignment tests.
- Replaced misleading WIS terminology in the methodology with 95% Interval Score (IS95) for the single-interval calculation.
- Renamed the augmentation concept in the methodology to lightweight synthetic target augmentation / empirical target resampling with Gaussian perturbation.
- Added `docs/result_provenance.md`.
- Separated original V1 analytical tables and figures into `archive_v1/` directories.
- Added pinned Python dependencies.
- Expanded automated tests to four tests covering data audit, target alignment, seasonal alignment and interval scoring.
- Corrected the methodology SVG XML.
- Completed the MIT License text.
- Updated `CITATION.cff` to version 1.1.0.


## 1.1.1
- Added a PNG rendering of the methodology diagram for reliable viewing across GitHub and mobile clients.
- Retained the SVG source for vector-quality use.
