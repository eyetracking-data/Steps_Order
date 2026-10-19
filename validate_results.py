"""Fast integrity check of the included paired benchmark results (no model retraining)."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'
fold=pd.read_csv(RESULTS/'fold_results.csv')
paired=pd.read_csv(RESULTS/'order_comparison.csv')
raw=pd.read_csv(RESULTS/'raw_baseline_folds.csv')
summary=pd.read_csv(RESULTS/'dataset_summary.csv')
assert len(fold)==450,(len(fold),'fold rows')
assert len(paired)==45,(len(paired),'pipeline pairs')
assert len(raw)==15,(len(raw),'raw fold rows')
assert len(summary)==6,(len(summary),'best summary rows')
assert set(fold.order)=={'out_first','mv_first'}
assert set(fold.fold)=={1,2,3,4,5}
assert not fold[['accuracy','f1','auroc']].isna().any().any()
assert (fold.groupby(['dataset','pipeline','order']).size()==5).all()
for name in ['education','medical','usability']:
    data=np.load(ROOT/'data'/f'{name}_timeseries.npz')
    assert data['X_noisy'].shape==(50,7200,3),name
    assert set(np.unique(data['y']))=={0,1},name
    assert np.sum(data['y']==0)==25 and np.sum(data['y']==1)==25,name
expected={('education','out_first'):.74,('education','mv_first'):.74,('medical','out_first'):.50,('medical','mv_first'):.50,('usability','out_first'):.58,('usability','mv_first'):.54}
for key,value in expected.items():
    row=summary[(summary.dataset==key[0])&(summary.order==key[1])]
    assert len(row)==1 and np.isclose(row.best_final_accuracy.iloc[0],value,atol=1e-12),(key,row)
print('PASS: data shapes, 450 folds, 45 pairs, raw baselines and corrected headline accuracies.')
print(summary[['dataset','order','best_final_pipeline','best_final_accuracy']].to_string(index=False))
