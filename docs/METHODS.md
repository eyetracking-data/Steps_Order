# Experimental methods — paired order sensitivity

## Study question

Does swapping **outlier handling (OUT)** and **missing-value handling (MV)** change downstream classification accuracy when the rest of a preprocessing pipeline stays fixed?

## Synthetic data

Three archived scenarios (`Education`, `Medical`, `Usability`), **not empirical data from those populations**. Each dataset contains 50 labelled multivariate time series (25 in each class), 7,200 time points per sample, three channels representing gaze X, gaze Y and pupil size. The assumed sample rate is 120 Hz. Approximately 5% of cells are missing in each scenario. In the archived arrays missingness affects all three channels at once for each affected time point.

The original synthetic generator and its complete prompt/history are not retained. The archived arrays make this analysis repeatable but do not permit reconstructing the original data-generation process.

## Controlled intervention

For each of 15 configurations A–O, compare:

- OUT-first: `OUT → MV → NORM → optional smoothing/filtering/feature restriction`.
- MV-first: `MV → OUT → (same MV method again *only if* the OUT stage marks values missing) → NORM → same later stages`.

Thus the only methodological intervention is the relative position of OUT and MV; the second filling operation is required to finish processing when Isolation Forest introduces NaNs. Configurations without an outlier stage are a negative control: the two orders are identical for them.

## Methods

The 15 configurations contain mean, KNN, LOCF or linear interpolation; no OUT / Isolation Forest / winsorisation / IQR clipping; standard or robust scaling; optional FFT or median smoothing, Butterworth filtering and supervised top-30/top-10 feature restriction. The complete definitions are in `results/pipeline_catalog.csv`.

Isolation Forest: `contamination=0.02`, random state 42, up to 30,000 complete time points drawn from training-fold series. Fit and transforms never use validation-fold class labels.

For the archived arrays, KNN applied per sample to a time point where *all channels* are missing reduces to per-channel means; the canonical code uses an equivalent fast path after checking this condition. This does **not** establish a general equivalence between KNN and mean imputation.

## Downstream classification

One-second windows (120 points), 50% overlap. Per-window statistics (mean, std, min, max for three channels), gaze-displacement velocity mean/std, and three dominant FFT magnitudes; per-sample aggregation with mean and std yields 34 features. Optional supervised feature selection happens inside the training fold.

`RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_split=5, min_samples_leaf=2, max_features='sqrt', bootstrap=True, class_weight='balanced', random_state=42)`; evaluation is stratified 5-fold CV (`shuffle=True`, seed 42) with the **same folds for both orders**. Accuracy is the primary outcome; F1 and AUROC are supplementary.

## Raw baseline

Each held-out fold is scored on the original noisy arrays using temporary linear interpolation **for numerical feature extraction only**. The two paired pipelines start from `X_noisy`, not from these temporarily interpolated baseline inputs. Raw folds are archived separately in `results/raw_baseline_folds.csv`.

## Interpretation

Comparison is exploratory, descriptive, and specific to the three synthetic archives; there is no statistical test proving a universal ordering effect. The scenario labels should not be treated as clinical or educational validation.

## Historical discrepancy

The older original A–O and A–E workbooks were not a matched pair. This repository replaces that earlier analysis with the controlled all-A–O comparison. The old artefacts are kept under `legacy/` for traceability.
