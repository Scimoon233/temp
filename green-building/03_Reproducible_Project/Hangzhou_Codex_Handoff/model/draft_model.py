"""Draft extension: energy ledger and explicit structural sensitivity. Original model unchanged."""
from run import *

def simulate(d,p,g,scenario,cooled=False):
 C,Hm,He,H12,win,wall,uw,ui=setup(p,g);dt=p['dt_seconds'];n=int(3600/dt);assert n*dt==3600
 H12*=p.get('partition_H_scale',1.)
 beam,diff,refl,up=irradiance(d,p['rotation_deg'])
 if p.get('zero_solar',False):beam[:]=0;diff[:]=0;refl[:]=0
 # Infinite-width horizontal overhang above each balcony pane, direct beam only.
 # Projection is outward from glass plane; it is not the balcony's inward depth.
 depth=p.get('canopy_projection_m',0.)
 cosinc=np.divide(beam,d.direct_normal_irradiance.to_numpy()[:,None],out=np.zeros_like(beam),where=d.direct_normal_irradiance.to_numpy()[:,None]>0)
 shadow=np.clip(np.divide(depth*np.maximum(up[:,None],0),2.1*cosinc,out=np.zeros_like(beam),where=cosinc>1e-10),0,1)
 beam_balcony=beam*(1-shadow)
 if scenario in ['S1','S3']:solar=(1-p['shade_direct_removed'])*beam+(1-p['shade_diffuse_removed'])*diff+refl
 else:solar=beam+diff+refl
 qsol=solar@win.T*.7
 if depth>0:
  bsolar=beam_balcony*(1-p['shade_direct_removed'] if scenario in ['S1','S3'] else 1)+diff*(1-p['shade_diffuse_removed'] if scenario in ['S1','S3'] else 1)+refl
  qsol[:,1]=bsolar@win[1]*.7
 original_solar=qsol.copy()
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
 names=['solar','internal','opaque_solar','envelope','ventilation','interzone','storage','air_to_mass','cooling','direct_window','secondary_solar']
 ledger=np.zeros((len(d),2,len(names)))
 for counter,idx in enumerate(np.r_[warm,np.arange(len(d))]):
  energy=np.zeros((2,len(names)))
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
   ach=np.array([p['ach_open'] if mask&(1<<z) else p['ach_closed'] for z in range(2)])
   for z,ai in enumerate([0,2]):
    other=2-ai
    flux=[qsol[idx,z],gains[idx] if z==0 else 0,qwall[idx,z],He[z]*(tout[idx]-new[ai]),1.2*1006*V[z]*ach[z]/3600*(tout[idx]-new[ai]),H12*(new[other]-new[ai]),float(np.dot(C[ai:ai+2],new[ai:ai+2]-T[ai:ai+2]))/dt,Hm[z]*(new[ai]-new[ai+1]),cool if z==0 else 0,original_solar[idx,z] if z==0 else 0,secondary[idx] if z==0 else 0]
    energy[z]+=np.array(flux)/n
   T=new
  # Warmup indices occur twice; explicit counter avoids accidentally collecting warmup.
  if counter>=len(warm):arr[idx]=vals;ledger[idx]=energy
 cols=['T1_C','M1_C','T2_C','M2_C','cool_W','vent1_fraction','vent2_fraction','DH28_Kh','OH28_h','DH26_Kh','DH30_Kh','peak_substep_C']
 a=pd.DataFrame(arr,columns=cols);a.insert(0,'time_interval_end',d.time);a['Tout_interval_C']=tout;a['night_window']=night.astype(int)
 for z in range(2):a[f'solar_Z{z+1}_W']=qsol[:,z]
 a['internal_W']=gains
 metrics=dict(mean_C=arr[:,0].mean(),peak_C=arr[:,11].max(),night_mean_C=arr[night,0].mean(),OH28_h=arr[:,8].sum(),DH28_Kh=arr[:,7].sum(),DH26_Kh=arr[:,9].sum(),DH30_Kh=arr[:,10].sum(),cool_kWh_th=arr[:,4].sum()/1000,cool_kWh_th_m2=arr[:,4].sum()/1000/41.1,vent1_hours=arr[:,5].sum(),vent2_hours=arr[:,6].sum(),night_window_hours=int(night.sum()),max_node_residual_W=residual)
 for z in range(2):
  for k,name in enumerate(names):a[f'Z{z+1}_{name}_W']=ledger[:,z,k]
  balance=ledger[:,z,0:6].sum(axis=1)-ledger[:,z,6]-ledger[:,z,8]
  metrics[f'Z{z+1}_balance_max_W']=float(np.max(abs(balance)))
 return a,metrics
