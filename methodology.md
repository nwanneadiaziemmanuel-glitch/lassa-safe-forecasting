# Methodology

## 1. Research question

Can a lightweight machine-learning model forecast short-horizon weekly Lassa fever surveillance signals under sparse, seasonal and highly variable conditions, while making uncertainty, robustness and data-quality limitations explicit?

The project is designed as a **trustworthy-AI forecasting study**, not as an operational outbreak-response system.

## 2. Data

The analytical dataset contains weekly aggregate Lassa fever surveillance observations derived from Nigeria Centre for Disease Control and Prevention (NCDC) epidemiological reports.

- Coverage: 30 December 2019 to 10 November 2025.
- Rows: 307 weekly observations.
- Variables: week dates, epidemiological year/week, suspected cases, confirmed cases, probable cases, deaths, extraction method, extraction timestamp and source report URL.
- Primary target: `confirmed_cases`.
- Secondary variables are retained for descriptive audit and interpretation.
- The repository contains aggregate surveillance data only; individual-level NCDC/SORMAS records are not redistributed.

## 3. Data-quality audit

Before modelling, the series is checked for:

- missing values;
- duplicate rows and duplicate week starts;
- seven-day date continuity;
- negative surveillance counts;
- impossible relationships among suspected, probable, confirmed and death counts; and
- consistency between week-start and week-end dates.

The supplied dataset passes these structural checks. Structural completeness should not be interpreted as proof of complete surveillance reporting, because reporting delay, backfill, revision and surveillance-practice changes may still exist.

## 4. Feature construction

Forecasting features are generated only from information available at the forecast origin:

- lags: 1, 2, 3, 4, 8, 13, 26 and 52 weeks;
- shifted rolling means over 4, 8, 13, 26 and 52 weeks; and
- epidemiological-week sine/cosine terms to represent annual seasonality.

Rolling statistics are shifted by one observation so that the current target is not included in its own predictors.

## 5. Primary model

The primary model is a shallow `GradientBoostingRegressor` with:

- 100 estimators;
- maximum tree depth = 2;
- learning rate = 0.05;
- Huber loss; and
- random seed = 42.

The model is intentionally lightweight so that the analysis can be reproduced on CPU-only hardware such as Google Colab or a modest personal computer.

## 6. Temporal evaluation and leakage control

The **V1.1 core analysis uses an expanding year-based temporal holdout**, not random train/test splitting and not a claim of full rolling-origin evaluation.

For each evaluation year (2022–2025):

1. observations before the evaluation year form the historical training period;
2. training targets are restricted to outcomes that also occur before the evaluation year's first week;
3. observations in the evaluation year are used as future forecast origins; and
4. the final forecast origins are excluded when their requested future target lies beyond the available evaluation period.

This target-date restriction is important because simply shifting the target across a year boundary can leak early evaluation-year outcomes into the training set.

The number of observations therefore represents **evaluable forecast origins**, not necessarily the total number of calendar weeks in the evaluation year.

## 7. Baselines

Two transparent baselines are retained conceptually for comparison:

### 52-week seasonal naive

At forecast origin `t`, the prediction for `t+h` uses the observation approximately 52 weeks before the target, i.e. the value at `t+h-52`.

### Historical epidemiological-week mean

The baseline predicts the historical mean for the corresponding epidemiological week using only the historical training period.

The corrected seasonal-naive alignment is implemented in `src/forecasting.py`.

## 8. Forecast horizons

The project evaluates 1-, 2-, 3- and 4-week-ahead forecasts.

For horizon `h`, the future target is aligned as:

`y(t+h)`

and is never used as a training target when that outcome falls inside the evaluation period.

## 9. Evaluation metrics

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between forecasts and observed counts. Lower values indicate smaller typical errors.

### Root Mean Squared Error (RMSE)

RMSE gives greater weight to large errors and is therefore useful for identifying poor performance during high-intensity weeks.

### Prediction-interval coverage

For a nominal 95% prediction interval, empirical coverage is the proportion of observed outcomes that fall between the lower and upper interval limits.

Coverage substantially below 95% indicates undercoverage relative to the nominal level.

### Interval Score (IS95)

The uncertainty analysis uses a single 95% prediction interval score. It combines interval width with penalties when observations fall outside the interval.

It is **not labelled WIS** in the corrected V1.1 methodology because a standard Weighted Interval Score requires multiple interval levels and a central point/median component.

## 10. Synthetic-data experiments

The historical V1 augmentation experiments are retained as an archival analytical record. The underlying method is more accurately described as **lightweight synthetic target augmentation** or **empirical target resampling with Gaussian perturbation**.

The method:

1. samples observed target values;
2. estimates a perturbation scale from first differences; and
3. adds Gaussian noise before clipping negative values to zero.

It is **not a residual bootstrap** and is not presented as realistic generative modelling of patient-level or biological data.

Targeted high-intensity sampling is treated as a stress-test ablation rather than as a validated synthetic-data generator.

## 11. Synthetic-data fidelity

Synthetic fidelity is assessed using descriptive properties such as:

- mean;
- standard deviation;
- median;
- upper quantiles;
- zero rate; and
- maximum values.

The archived V1 synthetic-fidelity table is preserved under `results/archive_v1/`. Its reported maxima are based on the original analytical subsets and must not be interpreted as full-calendar-year maxima without reference to that archived analysis.

## 12. Uncertainty analysis

The uncertainty module supports empirical prediction intervals. In the historical V1 analysis, the augmentation/interval-generation procedure should not be described as a formal residual bootstrap unless residual resampling is explicitly implemented. The corrected terminology used in this repository is **95% prediction interval** and **Interval Score (IS95)**.

The project focuses on whether uncertainty remains reliable under sparse and high-intensity surveillance conditions rather than assuming that nominal 95% intervals automatically provide 95% empirical coverage.

## 13. Robustness analysis

The historical V1 robustness experiments examine perturbations including:

- removal of the latest surveillance signal;
- removal of multiple recent signals;
- random missingness;
- short gaps;
- feature noise; and
- reporting spikes.

These archived experiments are retained under `results/archive_v1/` and should be read as stress-test evidence from the original V1 analytical pipeline, not as outputs generated by the corrected V1.1 core runner.

## 14. Reproducibility architecture

The V1.1 core analysis can be run from the repository root with:

```bash
python -m src.run_analysis
```

Outputs are written to `results/v1_1_core/`.

The V1 historical result tables and figures are preserved separately under `results/archive_v1/` and `figures/archive_v1/`. This separation prevents an archived result from being silently presented as if it were generated by the corrected implementation.

## 15. Key terms and abbreviations

| Term | Meaning |
|---|---|
| **AI** | Artificial Intelligence |
| **ML** | Machine Learning |
| **GB / GBR** | Gradient Boosting / Gradient Boosting Regressor |
| **LF** | Lassa fever |
| **NCDC** | Nigeria Centre for Disease Control and Prevention |
| **Epi week** | Epidemiological week used for surveillance reporting |
| **MAE** | Mean Absolute Error |
| **RMSE** | Root Mean Squared Error |
| **PI** | Prediction Interval |
| **95% PI** | Prediction interval intended to contain future observations with nominal 95% coverage |
| **IS95** | 95% Interval Score; an interval-quality score combining interval width and penalties for misses |
| **WIS** | Weighted Interval Score; reserved for analyses that actually combine multiple interval levels and a central point component |
| **SD** | Standard Deviation |
| **TS** | Time Series |
| **OOD** | Out-of-Distribution |
| **QC** | Quality Control |
| **CSV** | Comma-Separated Values |
| **JSON** | JavaScript Object Notation |
| **SVG** | Scalable Vector Graphics |
| **MD** | Markdown |
| **Synthetic data** | Artificially generated observations used for methodological experiments, not real surveillance observations |
| **Augmentation** | Addition of synthetic observations or signals to a training dataset |
| **Distribution shift** | Change in the data-generating distribution between training and evaluation conditions |
| **Temporal leakage** | Use of information from a future evaluation period during model training or feature construction |
| **Expanding temporal holdout** | Evaluation in which each test period is later than all observations used for training |
| **Reproducibility** | Ability to recreate an analysis from the specified data, code, environment and settings |
| **PI** | Prediction Interval |
| **95% PI** | Prediction interval with a nominal 95% level |
| **Coverage** | Proportion of observed outcomes contained within the prediction interval |
| **IS95** | Interval Score for one 95% prediction interval |
| **WIS** | Weighted Interval Score; not used for the corrected single-interval metric in V1.1 |
| **SD** | Standard Deviation |
| **OOD** | Out-of-Distribution |
| **TS** | Time Series |
| **QC** | Quality Control |
| **CSV** | Comma-Separated Values |
| **JSON** | JavaScript Object Notation |
| **SVG** | Scalable Vector Graphics |
| **MD** | Markdown |
| **SORMAS** | Surveillance Outbreak Response Management and Analysis System |
| **Synthetic data** | Artificially generated observations used for methodological experiments |
| **Augmentation** | Addition of synthetic observations to a training dataset |
| **Distribution shift** | Change in the data-generating distribution between periods or settings |
| **Temporal leakage** | Use of information from the future evaluation period during model training or feature construction |
| **Expanding temporal holdout** | Evaluation in which historical training data grow as later periods are evaluated |
| **Rolling-origin evaluation** | Repeated forecasting from successive origins; this is not the label used for the corrected year-based V1.1 analysis |
| **Reproducibility** | Ability to recreate a stated analysis from specified data, code, environment and settings |

## 16. Interpretation principle

The central scientific objective is not to demonstrate that machine learning or synthetic augmentation always improves outbreak forecasting. The objective is to expose where a forecasting system can fail and to evaluate point accuracy, uncertainty reliability, high-intensity performance, data perturbation sensitivity and reproducibility together.
