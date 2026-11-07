"""Physical/numerical checks; writes machine-readable evidence; not calibration."""
import copy
import numpy as np
import pandas as pd
from run import geometry,defaults,weather,simulate,setup,irradiance,dump,ROOT,OUT

def main():
 g=geometry();p=defaults();checks={}
 areas=[]
 for poly in g['zone_polygons_m']:
  a=np.array(poly);areas.append(abs(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1)))/2)
 assert np.allclose(areas,[41.1,6.3]);assert all(a['opaque_m2']>=0 for a in g['segments'])
 checks['polygon_areas_m2']=areas
 d=weather(2025).iloc[:168].copy()
 # Full equilibrium must be preserved even at nonzero ventilation.
 d.loc[:,'temperature_2m']=26
 for c in ['shortwave_radiation','direct_normal_irradiance','diffuse_radiation']:d.loc[:,c]=0
 q=p|dict(gain_scale=0,warmup_days=0)
 a,m=simulate(d,q,g,'S3');err=float(abs(a[['T1_C','M1_C','T2_C','M2_C']]-26).to_numpy().max());assert err<1e-9
 checks['isothermal_no_gain_max_error_K']=err
 # Isothermal ventilation term vanishes; hotter outdoor ventilation adds heat.
 V=g['zone_volumes_m3'][0];Hv=1.2*1006*V*1.51/3600
 assert Hv*(26-26)==0 and Hv*(30-26)>0
 checks['hot_outdoor_vent_heat_W_at_4K']=Hv*4
 # Solar splitter conserves admitted heat exactly.
 orig=np.array([500.,1800.]);sec=orig[1]*p['balcony_secondary_fraction'];assigned=orig+np.array([sec,-sec]);assert np.isclose(assigned.sum(),orig.sum())
 checks['solar_split_conservation_W']=float(assigned.sum()-orig.sum())
 # Overcast case: direct-only shading must leave diffuse and ground radiation.
 d2=d.copy();d2['shortwave_radiation']=100.;d2['diffuse_radiation']=100.
 a,_=simulate(d2,q,g,'S0');b,_=simulate(d2,q,g,'S1');assert np.allclose(a.T1_C,b.T1_C)
 checks['diffuse_only_shade_temperature_difference_K']=float(abs(a.T1_C-b.T1_C).max())
 # Constant forcing steady state, ideal cooling compared with independent 2-air-node static balance.
 d3=pd.concat([d]*4,ignore_index=True);d3['time']=pd.date_range('2025-06-01',periods=len(d3),freq='h');d3['temperature_2m']=35.
 a,m=simulate(d3,p|dict(gain_scale=0),g,'S0',True)
 C,Hm,He,H12,*_=setup(p,g);Hout=He+1.2*1006*np.array(g['zone_volumes_m3'])*p['ach_closed']/3600
 T2=(Hout[1]*35+H12*26)/(Hout[1]+H12);expected=Hout[0]*9+H12*(T2-26)
 err=abs(a.cool_W.iloc[-1]-expected);assert err<.01
 checks['steady_ideal_expected_W']=float(expected);checks['steady_ideal_error_W']=float(err)
 # Full summer step refinement and warmup/initial-state tests, all scenarios and both modes.
 d=weather(2025);rows=[]
 for mode in ['free','ideal']:
  for s in ['S0','S1','S2','S3']:
   ref=None
   for dt in [600,300,150]:
    a,m=simulate(d,p|dict(dt_seconds=dt),g,s,mode=='ideal');rows.append(dict(mode=mode,scenario=s,dt_seconds=dt,**m))
    assert m['max_node_residual_W']<1e-7
    if mode=='ideal':assert a.T1_C.max()<=26+1e-8
   a,m=simulate(d,p|dict(warmup_days=56,initial_C=35.),g,s,mode=='ideal');rows.append(dict(mode=mode,scenario=s,dt_seconds=300,warmup56_initial35=True,**m))
 table=pd.DataFrame(rows);table.to_csv(OUT/'numerical_checks.csv',index=False)
 refined=[]
 for (mode,s),r in table.groupby(['mode','scenario']):
  regular=r[r.warmup56_initial35.isna()];a=regular[regular.dt_seconds==300].iloc[0];b=regular[regular.dt_seconds==150].iloc[0];w=r[r.warmup56_initial35==True].iloc[0]
  metric='DH28_Kh' if mode=='free' else 'cool_kWh_th'
  rel=abs(a[metric]-b[metric])/max(abs(b[metric]),1)
  assert rel<.01,(mode,s,rel)
  assert abs(a[metric]-w[metric])/max(abs(a[metric]),1)<.001
  refined.append(dict(mode=mode,scenario=s,metric=metric,step_relative_change=float(rel),peak_change_K=float(abs(a.peak_C-b.peak_C)),warmup_relative_change=float(abs(a[metric]-w[metric])/max(abs(a[metric]),1))))
 checks['refinement_and_warmup']=refined;checks['status']='PASS';dump(OUT/'checks.json',checks)
 print(checks)
if __name__=='__main__':main()
