"""Recompute corrected Step Order benchmark.
Pipeline functions are read from step_order.ipynb; deterministic equivalent
intermediate results are cached to shorten runtime. Writes to results_recomputed/
so the supplied reference results are left unchanged.
"""
from pathlib import Path
import json,os,time
os.chdir(Path(__file__).resolve().parent)
nb=json.load(open(str(Path(__file__).resolve().parent / 'step_order.ipynb')))
for i in [1,3,5,7,9,11,13,15]:exec(''.join(nb['cells'][i]['source']),globals())

def run_cached(dataset_name,path):
    _, X_noisy, y=load_dataset(path)
    splitter=StratifiedKFold(n_splits=CV_SPLITS,shuffle=True,random_state=RANDOM_STATE)
    rows=[];start=time.time()
    for fold,(it,iv) in enumerate(splitter.split(X_noisy,y),1):
        Xt=X_noisy[it].astype(float);Xv=X_noisy[iv].astype(float);yt=y[it];yv=y[iv]
        rep={};features={}
        for order in ('out_first','mv_first'):
            for name,cfg in PIPELINES.items():
                rk=(order,cfg['outlier'],cfg['mv'])
                if rk not in rep:rep[rk]=repair_pair(Xt,Xv,cfg,order)
                fk=(rk,cfg['norm'],cfg['smooth'],cfg['butter'])
                if fk not in features:
                    pt,pv=finish_pipeline(*rep[rk],cfg)
                    features[fk]=(extract_features(pt),extract_features(pv))
                ft,fv=features[fk]
                if cfg['feat_limit'] is not None:
                    sel=make_random_forest();sel.fit(ft,yt)
                    idx=np.argsort(sel.feature_importances_)[::-1][:int(cfg['feat_limit'])]
                    ft,fv=ft[:,idx],fv[:,idx]
                metrics=score_features(ft,fv,yt,yv)
                rows.append(dict(dataset=dataset_name,fold=fold,order=order,pipeline=name,**metrics))
        print(f'{dataset_name}: fold {fold}/5 after {time.time()-start:.1f}s',flush=True)
    return pd.DataFrame(rows)

def main():
    out=Path('results_recomputed');out.mkdir(exist_ok=True);frames=[]
    for dataset,p in DATASETS.items():
        df=run_cached(dataset,p); df.to_csv(out/f'{dataset}_fold_results.csv',index=False);frames.append(df)
        print(dataset,'done',flush=True)
    df=pd.concat(frames,ignore_index=True);df.to_csv(out/'fold_results.csv',index=False)
    oc=summarize_order_results(df);oc.to_csv(out/'order_comparison.csv',index=False)
    print('FINISHED',flush=True)
    print(oc[oc.pipeline.isin(['O_limit10','J_interp_std','N_median_smooth'])].to_string(index=False),flush=True)
if __name__=='__main__':main()
