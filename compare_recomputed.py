"""Compare a full rerun (results_recomputed/) with the supplied reference fold results."""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parent
ref=ROOT/'results'/'fold_results.csv'
new=ROOT/'results_recomputed'/'fold_results.csv'
if not new.exists():
    raise SystemExit('No recomputed results. First run: python reproduce.py')
key=['dataset','fold','order','pipeline']
a=pd.read_csv(ref).sort_values(key).reset_index(drop=True)
b=pd.read_csv(new).sort_values(key).reset_index(drop=True)
assert a[key].equals(b[key]),'Row keys differ'
for metric in ['accuracy','f1','auroc']:
    diff=np.max(np.abs(a[metric].to_numpy()-b[metric].to_numpy()))
    print(f'{metric}: maximum absolute difference = {diff:.12g}')
    assert np.allclose(a[metric],b[metric],atol=1e-12,rtol=0),metric
print('PASS: recomputed paired fold results match reference results.')
