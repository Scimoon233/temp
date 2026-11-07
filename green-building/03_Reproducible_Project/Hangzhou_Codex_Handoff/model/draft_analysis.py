from run import *
from draft_model import simulate
DEST=OUT/'draft_diagnostics'
def main():
 DEST.mkdir(exist_ok=True);g=geometry();p=json.loads((ROOT/'config/base.json').read_text())
 cases={'base':{},'canopy_0.5m':{'canopy_projection_m':.5},'canopy_1.0m':{'canopy_projection_m':1.},'partition_H_half':{'partition_H_scale':.5},'partition_H_double':{'partition_H_scale':2.},'combined_lower_gain':{'canopy_projection_m':1.,'gain_scale':.5,'balcony_secondary_fraction':0.}}
 rows=[];budgets=[];eqerr=[]
 dump(DEST/'cases.json',cases)
 for y in [2025,2026]:
  d=weather(y)
  for case,changes in cases.items():
   for mode in ['free','ideal']:
    for s in ['S0','S1','S2','S3']:
     a,m=simulate(d,p|changes,g,s,mode=='ideal');rows.append(dict(variant=case,year=y,mode=mode,scenario=s,**m))
     assert m['max_node_residual_W']<1e-7
     for z in [1,2]:
      assert m[f'Z{z}_balance_max_W']<1e-7
      for key in ['solar','internal','opaque_solar','envelope','ventilation','interzone','storage','air_to_mass','cooling','direct_window','secondary_solar']:
       x=a[f'Z{z}_{key}_W'].to_numpy()
       budgets.append(dict(variant=case,year=y,mode=mode,scenario=s,zone=z,term=key,net_kWh=x.sum()/1000,positive_kWh=np.maximum(x,0).sum()/1000,negative_kWh=np.minimum(x,0).sum()/1000))
     if case=='base':
      old=pd.read_csv(OUT/f'hourly/{y}_{mode}_{s}.csv')
      err=float(np.max(abs(old.T1_C-a.T1_C)));assert err<1e-6;eqerr.append(err)
      a.to_csv(DEST/f'{y}_{mode}_{s}_ledger.csv',index=False,float_format='%.9f')
   print(y,case,flush=True)
  for label,changes in {'zero_internal':{'gain_scale':0.},'zero_solar':{'zero_solar':True}}.items():
   for mode in ['free','ideal']:
    a,m=simulate(d,p|changes,g,'S0',mode=='ideal');rows.append(dict(variant=label,year=y,mode=mode,scenario='S0',**m))
  # Refinement for added shade and combined structural cases (S3, both modes).
  for label in ['canopy_1.0m','combined_lower_gain']:
   for mode in ['free','ideal']:
    a,m=simulate(d,p|cases[label]|dict(dt_seconds=150),g,'S3',mode=='ideal');rows.append(dict(variant=label+'_dt150',year=y,mode=mode,scenario='S3',**m))
 r=pd.DataFrame(rows);r.to_csv(DEST/'metrics.csv',index=False);pd.DataFrame(budgets).to_csv(DEST/'energy_budgets.csv',index=False)
 dump(DEST/'checks.json',dict(status='PASS',base_temperature_reproduction_max_K=max(eqerr),node_residual_max_W=float(r.max_node_residual_W.max()),zone_balance_max_W=float(r[['Z1_balance_max_W','Z2_balance_max_W']].max().max()),season_runs=len(r)))
 # Energy balance chart: signed system inputs/outputs; internal exchange cancels.
 b=pd.DataFrame(budgets);fig,axes=plt.subplots(1,2,figsize=(11,4))
 terms=['solar','internal','opaque_solar','envelope','ventilation','storage']
 for ax,y in zip(axes,[2025,2026]):
  a=b[(b.variant=='base')&(b.year==y)&(b['mode']=='free')&(b.scenario=='S0')].groupby('term').net_kWh.sum()
  ax.bar(terms,[a[t] for t in terms],color=['#dfae53','#dfae53','#dfae53','#578eae','#578eae','#888888']);ax.axhline(0,c='black',lw=.7);ax.set_title(f'{y} S0, whole system');ax.set_ylabel('Signed heat / storage (kWh_th)');ax.tick_params(axis='x',rotation=35)
 fig.tight_layout();fig.savefig(DEST/'heat_balance.png',dpi=200);plt.close(fig)
 # Day-level signed pathways around weather-defined representative week.
 for y in [2025,2026]:
  a=pd.read_csv(DEST/f'{y}_free_S0_ledger.csv',parse_dates=['time_interval_end']);week=json.loads((OUT/f'representative_week_{y}.json').read_text());a=a[a.time_interval_end.between(week['start'],week['end'])]
  fig,ax=plt.subplots(figsize=(12,4))
  for key in ['solar','internal','envelope','ventilation','interzone']:
   ax.plot(a.time_interval_end,a[f'Z1_{key}_W'],label=key,lw=1)
  ax.axhline(0,c='grey',lw=.5);ax.legend(ncol=5);ax.set_ylabel('Z1 heat flow (W)');fig.autofmt_xdate();fig.tight_layout();fig.savefig(DEST/f'heat_week_{y}.png',dpi=180);plt.close(fig)
 print('DONE',len(r))
if __name__=='__main__':main()
