# Result Provenance

| Result group | Location | Status | Reproduction path |
|---|---|---|---|
| Dataset audit | `results/v1_1_core/audit_summary.json` | Current V1.1 | `python -m src.run_analysis` |
| Feature matrix | `results/v1_1_core/feature_matrix.csv` | Current V1.1 | `python -m src.run_analysis` |
| Core forecast metrics | `results/v1_1_core/forecast_reproduction.csv` | Current V1.1 | `python -m src.run_analysis` |
| Annual totals | `results/v1_1_core/annual_totals.csv` | Deterministic dataset summary | Included dataset |
| Seasonality | `results/v1_1_core/seasonality_by_epi_week.csv` | Deterministic dataset summary | Included dataset |
| Original model comparison | `results/archive_v1/model_comparison.csv` | Frozen V1 archive | Historical analytical output |
| Original augmentation ablation | `results/archive_v1/augmentation_ablation.csv` | Frozen V1 archive | Historical analytical output |
| Original uncertainty results | `results/archive_v1/uncertainty_results.csv` | Frozen V1 archive | Historical analytical output; metric was originally labelled WIS |
| Original robustness results | `results/archive_v1/robustness_results.csv` | Frozen V1 archive | Historical analytical output |
| Original failure analysis | `results/archive_v1/failure_analysis.csv` | Frozen V1 archive | Historical analytical output |
| Original synthetic fidelity | `results/archive_v1/synthetic_fidelity.csv` | Frozen V1 archive | Historical analytical output; maxima refer to the original analytical subsets |
| Original figures | `figures/archive_v1/` | Frozen V1 archive | Historical analytical output; methodology diagram retained as PNG for reliable rendering |

## Why V1 results are retained

The project does not silently replace historical results when implementation details change. Preserving the original outputs makes the version transition auditable and prevents accidental rewriting of the research record.
