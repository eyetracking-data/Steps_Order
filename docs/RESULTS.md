# Results of the corrected paired experiment

All reported values in this directory were freshly recomputed from the corrected code and the three archived NPZ datasets. They match the corrected dissertation working notes.

| Synthetic scenario | Raw Accuracy | Best OUT-first | Best MV-first | Mean MV-first − OUT-first (outlier configurations only) |
|---|---:|---:|---:|---:|
| Education | 68% | 74% (J_interp_std) | 74% (J_interp_std) | -2.89 pp |
| Medical | 44% | 50% (N_median_smooth) | 50% (N_median_smooth) | -1.33 pp |
| Usability | 40% | 58% (O_limit10) | 54% (O_limit10) | -0.89 pp |

**Important:** The best pipelines in Education and Medical have *no explicit outlier stage*. Their equality between orders is therefore expected, and should not be presented as evidence that the order of actual outlier operations has no effect. The signed average in the last column is restricted to the nine configurations with a real OUT stage.

For an exact pairwise inspection, use `results/order_comparison.csv`. The raw records are `results/fold_results.csv`, with 450 rows (3 datasets × 5 folds × 15 pipelines × 2 orders). The unprocessed baseline has 15 rows in `results/raw_baseline_folds.csv`.

## Main conclusion

Operator order can affect classification, but no sequence wins in every configuration. On average the archived order-sensitive combinations slightly favour OUT-first. Individual combinations favour MV-first. These are observations on small synthetic scenarios, **not evidence of real-world clinical or educational performance**.

## Reproducing results

```bash
python validate_results.py
python reproduce.py
python compare_recomputed.py
```

`reproduce.py` recalculates the full paired experiment into `results_recomputed/` (leaving these reference files unmodified); it uses memoisation for identical preprocessing branches but executes the same numerical definitions from `step_order.ipynb`.
