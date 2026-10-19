# Steps Order — paired preprocessing order experiment

Reproducible synthetic sensitivity study for the order of **missing-value handling (MV)** and **outlier handling (OUT)** in configurable preprocessing pipelines. This repository provides the **corrected paired experiment**, replacing the historical non-matched comparison.

## Research question and design

For each of **15 configurations A–O**, run identical data through two sequences:

- **OUT-first:** OUT → MV → normalization → optional downstream stages
- **MV-first:** MV → OUT → (completion with same MV method if needed) → normalization → identical downstream stages

The evaluation uses three archived **synthetic** scenarios (Education, Medical, Usability), 50 multivariate sequences per scenario, 7,200 time points, three channels and a fixed 5-fold stratified Random Forest classifier. The intervention changes order, not feature extraction, folds, model configuration or later processing stages.

## Quick start

Requires **Python 3.11+** (tested Python 3.13; see `results/run_manifest.json`).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python validate_results.py
```

To explore saved results immediately, launch:

```bash
jupyter lab step_order.ipynb
```

The notebook starts with `RUN_EXPERIMENT=False`, reading the included verified results. To recompute all paired pipelines, use:

```bash
python reproduce.py
python compare_recomputed.py
```

This can take several minutes depending on your machine. Fresh results go to **`results_recomputed/`** and do not overwrite the supplied results. To run inside the notebook, switch `RUN_EXPERIMENT=True`; that original notebook evaluator is slower but follows the same design.

## Included files

```text
Steps_Order/
  README.md
  step_order.ipynb               # corrected canonical notebook
  reproduce.py                  # cached deterministic re-run
  validate_results.py          # quick structural and accuracy checks
  compare_recomputed.py        # compare freshly recomputed fold results
  requirements.txt
  data/                         # all 3 original NPZ datasets
  results/                      # all verified fold/pair/summary CSVs and metadata
  docs/METHODS.md               # precise protocol and limitations
  docs/RESULTS.md               # quantitative summary
  figures/                      # descriptive plots of paired accuracy
  legacy/                       # old source notebook and Excel files, historical only
  GITHUB_UPLOAD_ANLEITUNG_DE.md
```

## Principal results

- Education: best final Accuracy **0.74** in both orders.
- Medical: best final Accuracy **0.50** in both orders.
- Usability: best final Accuracy **0.58 OUT-first vs. 0.54 MV-first** for pipeline `O_limit10`.

The best Education and Medical configurations have no explicit OUT stage; compare **order-sensitive configurations**, not only the best overall setting, when interpreting an order effect. See `docs/RESULTS.md`.

## Scientific limitations

All domains are synthetic labels, not real clinical/educational/advertising cohorts. The synthetic generation procedure itself is incompletely documented; the archived arrays and evaluation are reproducible, but the original construction cannot be recreated from first principles. Because all three channels are missing together at missing time points, KNN reduces to a per-channel mean under the implemented per-sample estimator. Do not claim the result generalises across real domains.

## Provenance and older files

The files under `legacy/` document the earlier progressive branch (A–O) and shorter MV-first branch (A–E). They were not a controlled order-only comparison. Only `results/` and the corrected `step_order.ipynb` establish the results presented here.

The reported metrics were recomputed using the saved NPZ files and corrected evaluation code, with full fold-level results, reference comparison and environment metadata provided for independent review.

## Code and citation

Developed by Jennifer Landes in the context of the dissertation *Preprocessing of Eye-Tracking Data*, University of Regensburg. No DOI or published peer-reviewed order-effect result is asserted by this repository.
