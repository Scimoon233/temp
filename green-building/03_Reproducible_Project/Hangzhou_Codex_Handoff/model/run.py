"""Two-zone, four-node sensible RC experiment. All paths relative to project root."""
from pathlib import Path
import json, argparse, hashlib, platform
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'

def dump(path,obj):
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def geometry():
 w=3.897; r=3.728; h=20.6/w; b=6.3/w; step=(20.5-r*h)/1.228
 # Coordinates x east, y north. Reconstructed net-area polygons, not a trace.
 z1=[[0,0],[w+r,0],[w+r,h+step],[w+r-1.228,h+step],[w+r-1.228,h],[0,h]]
 z2=[[0,-b],[w,-b],[w,0],[0,0]]
 seg=[('E01',1,'N',w,0,True),('E02',1,'W',9.5/w,1.125,True),
 ('E03',1,'W',11.1/w,0,True),('E04',2,'W',b,3.15,True),
 ('E05',2,'S',w,7.77,True),('E06',2,'E',b,3.15,True),
 ('E07',1,'S',r,1.125,True),('E08',1,'E',h+step-2.6/1.228,0,False),
 ('E09',1,'E',2.6/1.228,0,False),('E10',1,'N',1.228,0,True),
 ('E11',1,'W',step,0,True),('E12',1,'N',r-1.228,1.275,True)]
 rows=[dict(id=i,zone=z,orientation=o,length_m=l,gross_m2=l*2.7,window_m2=a,opaque_m2=l*2.7-a,exterior=e) for i,z,o,l,a,e in seg]
 return dict(zone_polygons_m=[z1,z2],zone_areas_m2=[41.1,6.3],zone_volumes_m3=[110.97,17.01],height_m=2.7,partition_gross_m2=w*2.7,partition_glazed_m2=5.04,segments=rows,kitchen_projection_m=step)

def defaults():
 return dict(dt_seconds=300,warmup_days=28,initial_C=26.,mass_kJ_m2K=165.,mass_coupling_W_m2K=9.1,window_scale=1.,shade_direct_removed=.5,shade_diffuse_removed=0.,ach_closed=.44,ach_open=1.51,deltaT_K=1.,cooling_setpoint_C=26.,gain_peak_W_m2=16.7,gain_scale=1.,solar_air_fraction=.4,balcony_secondary_fraction=.25,interzone_mixing_ACH_small_zone=.1,rotation_deg=0.,east_exposed=False,opaque_absorptance=.6,outside_h_W_m2K=25.,ground_albedo=.2)

def weather(year):
 p=ROOT/f'data/03_weather_recent/era5_{year}_summer.csv'
 d=pd.read_csv(p,encoding='utf-8-sig');d.time=pd.to_datetime(d.time)
 assert len(d)==2208 and not d.isna().any().any()
 assert (d.time.diff().dropna()==pd.Timedelta(hours=1)).all()
 assert d.time.iloc[0]==pd.Timestamp(f'{year}-06-01') and d.time.iloc[-1]==pd.Timestamp(f'{year}-08-31 23:00')
 j=json.loads((ROOT/f'data/03_weather_recent/era5_openmeteo_{year}_summer.json').read_text())
 for c in d.columns[1:]: assert np.allclose(d[c],j['hourly'][c])
 return d

def irradiance(d,rotation=0.):
 # NOAA fractional-year equations; geometry at midpoint of preceding-hour radiation interval.
 t=d.time-pd.Timedelta(minutes=30)
 hour=t.dt.hour.to_numpy()+t.dt.minute.to_numpy()/60
 gamma=2*np.pi/365*(t.dt.dayofyear.to_numpy()-1+(hour-12)/24)
 eq=229.18*(.000075+.001868*np.cos(gamma)-.032077*np.sin(gamma)-.014615*np.cos(2*gamma)-.040849*np.sin(2*gamma))
 dec=.006918-.399912*np.cos(gamma)+.070257*np.sin(gamma)-.006758*np.cos(2*gamma)+.000907*np.sin(2*gamma)-.002697*np.cos(3*gamma)+.00148*np.sin(3*gamma)
 ha=np.deg2rad((hour*60+eq+4*120.25-480)/4-180);lat=np.deg2rad(30.25)
 up=np.sin(lat)*np.sin(dec)+np.cos(lat)*np.cos(dec)*np.cos(ha)
 east=-np.cos(dec)*np.sin(ha);north=np.cos(lat)*np.sin(dec)-np.sin(lat)*np.cos(dec)*np.cos(ha)
 beams=[]
 for az in [0,90,180,270]:
  a=np.deg2rad(az+rotation)
  beams.append(d.direct_normal_irradiance.to_numpy()*np.maximum(east*np.sin(a)+north*np.cos(a),0)*(up>0))
 diffuse=np.tile(d.diffuse_radiation.to_numpy()*.5,(4,1)).T
 reflected=np.tile(d.shortwave_radiation.to_numpy()*.1,(4,1)).T
 return np.array(beams).T,diffuse,reflected,up

def setup(p,g):
 mat=pd.read_csv(ROOT/'data/02_materials/liubo_materials_S1.csv',encoding='utf-8-sig')
 def resistance(name):
  a=mat[mat.element==name];return float((a.thickness_mm/1000/a.conductivity_W_mK).sum())
 uw=1/(.13+resistance('Exterior wall')+.04)
 ui=1/(.13+resistance('Interior Wall')+.13)
 window=np.zeros((2,4));wall=np.zeros((2,4));order={'N':0,'E':1,'S':2,'W':3}
 for a in g['segments']:
  if not a['exterior'] and not p['east_exposed']:continue
  z=a['zone']-1;o=order[a['orientation']];aa=a['window_m2']*p['window_scale']
  assert 0<=aa<=a['gross_m2'],a
  window[z,o]+=aa;wall[z,o]+=a['gross_m2']-aa
 A=np.array(g['zone_areas_m2']);V=np.array(g['zone_volumes_m3'])
 C=np.array([1.2*1006*V[0],A[0]*p['mass_kJ_m2K']*1000,1.2*1006*V[1],A[1]*p['mass_kJ_m2K']*1000])
 Hmass=A*p['mass_coupling_W_m2K'];Hext=uw*wall.sum(axis=1)+6.7*window.sum(axis=1)
 H12=ui*(g['partition_gross_m2']-g['partition_glazed_m2'])+6.7*g['partition_glazed_m2']+1.2*1006*V[1]*p['interzone_mixing_ACH_small_zone']/3600
 return C,Hmass,Hext,H12,window,wall,uw,ui

def simulate(d,p,g,scenario,cooled=False):
 C,Hm,He,H12,win,wall,uw,ui=setup(p,g);dt=p['dt_seconds'];n=int(3600/dt);assert n*dt==3600
 beam,diff,refl,up=irradiance(d,p['rotation_deg'])
 if scenario in ['S1','S3']:solar=(1-p['shade_direct_removed'])*beam+(1-p['shade_diffuse_removed'])*diff+refl
 else:solar=beam+diff+refl
 qsol=solar@win.T*.7
 secondary=qsol[:,1]*p['balcony_secondary_fraction'];qsol[:,0]+=secondary;qsol[:,1]-=secondary
 qwall=(beam+diff+refl)@wall.T*uw*p['opaque_absorptance']/p['outside_h_W_m2K']
 endpoint=d.temperature_2m.to_numpy(); tout=(endpoint+np.r_[endpoint[0],endpoint[:-1]])*.5
 # Interval midpoint for schedules, including 00 timestamp -> previous day 23:30.
 hours=((d.time-pd.Timedelta(minutes=30)).dt.hour.to_numpy())
 night=(hours>=21)|(hours<7)
 profile=np.where((hours>=18)|(hours<8),1.,.3)
 gains=41.1*p['gain_peak_W_m2']*p['gain_scale']*profile
 base=np.zeros((len(d),4));f=p['solar_air_fraction']
 base[:,0]=f*qsol[:,0]+.5*gains+qwall[:,0];base[:,1]=(1-f)*qsol[:,0]+.5*gains
 base[:,2]=f*qsol[:,1]+qwall[:,1];base[:,3]=(1-f)*qsol[:,1]
 V=np.array(g['zone_volumes_m3']);cache={}
 for mask in range(4):
  ach=np.array([p['ach_open'] if mask&(1<<z) else p['ach_closed'] for z in range(2)])
  ho=He+1.2*1006*V*ach/3600
  L=np.zeros((4,4))
  for a,b,h in [(0,1,Hm[0]),(2,3,Hm[1]),(0,2,H12)]:L[a,a]+=h;L[b,b]+=h;L[a,b]-=h;L[b,a]-=h
  L[0,0]+=ho[0];L[2,2]+=ho[1]
  M=np.diag(C/dt)+L;inv=np.linalg.inv(M)
  cache[mask]=(ho,L,inv)
 T=np.full(4,p['initial_C']);arr=np.zeros((len(d),12));residual=0.;nvent=scenario in ['S2','S3'];c=p['cooling_setpoint_C'];cap=C/dt
 # Repeated first seven days only: synthetic spin-up, excluded from metrics.
 warm=np.arange(p['warmup_days']*24)%168
 for idx in np.r_[warm,np.arange(len(d))]:
  measured=(len(warm)==0) # output phase tracked below using counter
  vals=np.zeros(12)
  for k in range(n):
   mask=0
   if nvent and night[idx]:
    if T[0]-tout[idx]>=p['deltaT_K']:mask|=1
    if T[2]-tout[idx]>=p['deltaT_K']:mask|=2
   ho,L,inv=cache[mask];q=base[idx].copy();q[0]+=ho[0]*tout[idx];q[2]+=ho[1]*tout[idx]
   rhs=cap*T+q;new=inv@rhs;cool=0.
   if cooled and new[0]>c:
    cool=(new[0]-c)/inv[0,0];new-=inv[:,0]*cool
   res=cap*(new-T)+L@new-q;res[0]+=cool
   residual=max(residual,float(np.max(np.abs(res))))
   vals[:4]+=new/n;vals[4]+=cool/n;vals[5]+=bool(mask&1)/n;vals[6]+=bool(mask&2)/n
   vals[7]+=max(new[0]-28,0)/n;vals[8]+=float(new[0]>28)/n
   vals[9]+=max(new[0]-26,0)/n;vals[10]+=max(new[0]-30,0)/n
   vals[11]=max(vals[11],new[0])
   T=new
  # Warmup indices occur twice; explicit counter avoids accidentally collecting warmup.
  if 'counter' not in locals():counter=0
  if counter>=len(warm):arr[idx]=vals
  counter+=1
 cols=['T1_C','M1_C','T2_C','M2_C','cool_W','vent1_fraction','vent2_fraction','DH28_Kh','OH28_h','DH26_Kh','DH30_Kh','peak_substep_C']
 a=pd.DataFrame(arr,columns=cols);a.insert(0,'time_interval_end',d.time);a['Tout_interval_C']=tout;a['night_window']=night.astype(int)
 for z in range(2):a[f'solar_Z{z+1}_W']=qsol[:,z]
 a['internal_W']=gains
 metrics=dict(mean_C=arr[:,0].mean(),peak_C=arr[:,11].max(),night_mean_C=arr[night,0].mean(),OH28_h=arr[:,8].sum(),DH28_Kh=arr[:,7].sum(),DH26_Kh=arr[:,9].sum(),DH30_Kh=arr[:,10].sum(),cool_kWh_th=arr[:,4].sum()/1000,cool_kWh_th_m2=arr[:,4].sum()/1000/41.1,vent1_hours=arr[:,5].sum(),vent2_hours=arr[:,6].sum(),night_window_hours=int(night.sum()),max_node_residual_W=residual)
 return a,metrics

def summaries(rows):
 r=pd.DataFrame(rows)
 for name in ['DH28_Kh','cool_kWh_th']:
  b=r[r.scenario=='S0'].set_index(['variant','year','mode'])[name]
  r[f'{name}_benefit']=r.apply(lambda x:b.loc[(x.variant,x.year,x['mode'])]-x[name],axis=1)
  r[f'{name}_reduction_pct']=r.apply(lambda x:100*x[f'{name}_benefit']/b.loc[(x.variant,x.year,x['mode'])] if b.loc[(x.variant,x.year,x['mode'])]!=0 else np.nan,axis=1)
 return r

def run_all(sensitivity=True):
 OUT.mkdir(exist_ok=True);(OUT/'hourly').mkdir(exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
 g=geometry();p=json.loads((ROOT/'config/base.json').read_text()) if (ROOT/'config/base.json').exists() else defaults()
 dump(ROOT/'config/base.json',p);dump(ROOT/'config/geometry_v2.json',g)
 pd.DataFrame(g['segments']).to_csv(OUT/'geometry_surfaces.csv',index=False)
 variants={'base':{}}
 if sensitivity:
  for key,values in dict(ach_open=[.8,3.],mass_kJ_m2K=[80.,260.],window_scale=[.8,1.1],shade_direct_removed=[.25,1.],deltaT_K=[0.,2.],balcony_secondary_fraction=[0.,.5],gain_scale=[.5,1.5],rotation_deg=[-30.,30.],mass_coupling_W_m2K=[4.55,18.2]).items():
   for value in values:variants[f'{key}={value}']={key:value}
  variants['east_exposed=True']={'east_exposed':True}
 dump(OUT/'variants.json',variants)
 rows=[];qa=[];weatherrows=[]
 for year in [2025,2026]:
  d=weather(year);beam,dif,ref,up=irradiance(d)
  closure=d.shortwave_radiation.to_numpy()-(d.direct_normal_irradiance.to_numpy()*np.maximum(up,0)+d.diffuse_radiation.to_numpy())
  qa.append(dict(year=year,hours=len(d),missing=int(d.isna().sum().sum()),radiation_midpoint_horizontal_closure_RMSE_W_m2=float(np.sqrt(np.mean(closure**2))),note='Midpoint geometry is approximate, not measured radiation validation.'))
  t=d.temperature_2m;night=((d.time.dt.hour>=21)|(d.time.dt.hour<7));hot=d.temperature_2m.rolling(168).mean().idxmax();start=hot-167
  dump(OUT/f'representative_week_{year}.json',dict(rule='Maximum rolling 168-hour outdoor endpoint temperature mean, earliest tie',start=str(d.time.iloc[start]),end=str(d.time.iloc[hot])))
  weatherrows.append(dict(year=year,mean_C=t.mean(),max_C=t.max(),min_C=t.min(),night_mean_C=t[night].mean(),night_hours_below26=int((night&(t<26)).sum()),night_hours_below28=int((night&(t<28)).sum()),representative_week_start=str(d.time.iloc[start])))
  for variant,change in variants.items():
   pp=p|change
   for mode in ['free','ideal']:
    for s in ['S0','S1','S2','S3']:
     a,m=simulate(d,pp,g,s,mode=='ideal');rows.append(dict(variant=variant,year=year,mode=mode,scenario=s,**m))
     if variant=='base':a.to_csv(OUT/f'hourly/{year}_{mode}_{s}.csv',index=False,float_format='%.6f')
   print(year,variant,flush=True)
 r=summaries(rows);r.to_csv(OUT/'all_metrics.csv',index=False);r[r.variant=='base'].to_csv(OUT/'base_metrics.csv',index=False)
 pd.DataFrame(weatherrows).to_csv(OUT/'weather_summary.csv',index=False);dump(OUT/'weather_QA.json',qa)
 interactions=[]
 for (v,y,m),a in r.groupby(['variant','year','mode']):
  a=a.set_index('scenario')
  for metric in ['DH28_Kh','cool_kWh_th']:
   interactions.append(dict(variant=v,year=y,mode=m,metric=metric,interaction=float(a.loc['S1',metric]+a.loc['S2',metric]-a.loc['S3',metric]-a.loc['S0',metric])))
 pd.DataFrame(interactions).to_csv(OUT/'interactions.csv',index=False)
 dump(OUT/'runtime.json',dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
 figures(r,g)

def figures(r,g):
 fig,axes=plt.subplots(2,2,figsize=(11,7))
 for i,y in enumerate([2025,2026]):
  for j,(mode,metric,label) in enumerate([('free','DH28_Kh','Overheating degree-hours >28 C (K h)'),('ideal','cool_kWh_th','Ideal sensible cooling (kWh_th)')]):
   a=r[(r.variant=='base')&(r.year==y)&(r['mode']==mode)]
   axes[i,j].bar(a.scenario,a[metric],color=['#667788','#eba447','#53a1b1','#4c895e']);axes[i,j].set_title(f'{y}: {label}');axes[i,j].grid(axis='y',alpha=.2)
 fig.tight_layout();fig.savefig(OUT/'figures/scenario_comparison.png',dpi=180);plt.close(fig)
 for y in [2025,2026]:
  week=json.loads((OUT/f'representative_week_{y}.json').read_text());fig,ax=plt.subplots(figsize=(12,4))
  for s in ['S0','S1','S2','S3']:
   a=pd.read_csv(OUT/f'hourly/{y}_free_{s}.csv',parse_dates=['time_interval_end']);a=a[a.time_interval_end.between(week['start'],week['end'])]
   ax.plot(a.time_interval_end,a.T1_C,label=s)
  ax.plot(a.time_interval_end,a.Tout_interval_C,'k--',lw=1,label='Outdoor');ax.axhline(28,c='grey',ls=':');ax.legend(ncol=5);ax.set_ylabel('Air temperature (C)');fig.autofmt_xdate();fig.tight_layout();fig.savefig(OUT/f'figures/week_{y}.png',dpi=180);plt.close(fig)
 fig,ax=plt.subplots(figsize=(6,5))
 for z,poly in enumerate(g['zone_polygons_m']):
  a=np.array(poly+[poly[0]]);ax.fill(a[:,0],a[:,1],alpha=.3,label=f'Z{z+1}: {g["zone_areas_m2"][z]} m2');ax.plot(a[:,0],a[:,1])
 ax.set_aspect('equal');ax.legend();ax.set_xlabel('East (m)');ax.set_ylabel('North (m)');fig.tight_layout();fig.savefig(OUT/'figures/geometry.png',dpi=180);plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(12,6))
 for ax,y in zip(axes,[2025,2026]):
  a=r[(r.year==y)&(r['mode']=='ideal')&(r.scenario=='S3')];ax.barh(a.variant,a.cool_kWh_th_reduction_pct);ax.set_xlabel('S3 sensible cooling reduction vs matching S0 (%)');ax.set_title(str(y));ax.tick_params(axis='y',labelsize=7)
 fig.tight_layout();fig.savefig(OUT/'figures/sensitivity.png',dpi=180);plt.close(fig)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--base-only',action='store_true');args=parser.parse_args();run_all(not args.base_only)
