"""Prepare explicitly labelled hourly candidates, without filling long gaps.
Usage: python prepare_weather_candidates.py PATH_TO_PREVIOUS_DATA_DIRECTORY
No airport data are used. No interpolation spans more than three hours.
"""
import bisect,csv,json,math,sys
from pathlib import Path
from datetime import datetime,timedelta

root=Path(__file__).resolve().parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'liubo_collected'
with (src/'hangzhou_city_2022_JulAug_observations.csv').open(encoding='utf-8-sig') as f:obs=list(csv.DictReader(f))
nodes=[]
for r in obs:
 if r['temperature_qc'] in ('1','5') and r['temperature_C']:
  td=float(r['dewpoint_C']) if r['dewpoint_C'] and r['dewpoint_qc'] in ('1','5') else None
  nodes.append((datetime.strptime(r['beijing_time'],'%Y-%m-%d %H:%M'),float(r['temperature_C']),td))
nodes.sort();times=[r[0] for r in nodes]
power=json.loads((src/'hangzhou_power_20220701_20220831_utc.json').read_text())['properties']['parameter']
rad={'grid_GHI_W_m2':'ALLSKY_SFC_SW_DWN','grid_DNI_W_m2':'ALLSKY_SFC_SW_DNI','grid_DHI_W_m2':'ALLSKY_SFC_SW_DIFF'}
def hourly_mean_under_linear_interpolation(t):
    # An hour stays within one three-hour linear segment when observations
    # are at integer hours. Its mean equals the value at the midpoint.
    midpoint=t+timedelta(minutes=30);i=bisect.bisect_left(times,midpoint)
    if not 0<i<len(nodes):return None
    a,b=nodes[i-1],nodes[i]
    if (b[0]-a[0]).total_seconds()>3*3600:return None
    fraction=(midpoint-a[0]).total_seconds()/(b[0]-a[0]).total_seconds()
    return a[1]+fraction*(b[1]-a[1])
out=[]
for h in range(62*24):
 t=datetime(2022,7,1)+timedelta(hours=h);i=bisect.bisect_left(times,t)
 temp=td=None;flag='missing';span=None
 if i<len(nodes) and times[i]==t:
  _,temp,td=nodes[i];flag='observed';span=0
 elif 0<i<len(nodes):
  a,b=nodes[i-1],nodes[i];span=(b[0]-a[0]).total_seconds()/3600
  if span<=3:
   frac=(t-a[0]).total_seconds()/(b[0]-a[0]).total_seconds()
   temp=a[1]+frac*(b[1]-a[1]);td=a[2]+frac*(b[2]-a[2]) if a[2] is not None and b[2] is not None else None
   flag='linear_interpolation_between_city_observations'
 rh=100*math.exp(17.625*td/(243.04+td)-17.625*temp/(243.04+temp)) if temp is not None and td is not None else None
 utc=t-timedelta(hours=8);key=utc.strftime('%Y%m%d%H')
 row={'beijing_time':t.strftime('%Y-%m-%d %H:%M'),'utc':utc.isoformat()+'Z',
      'city_temperature_C':temp,'city_temperature_method':flag,'bracketing_gap_hours':span,
      'city_hour_mean_temperature_C_derived':hourly_mean_under_linear_interpolation(t),
      'city_dewpoint_C':td,'RH_percent_derived':rh,
      'POWER_T2M_C':power['T2M'].get(key)}
 for label,k in rad.items():row[label]=power[k].get(key)
 row['weather_kind']='experimental_city_temperature_plus_POWER_grid_radiation'
 out.append(row)

def write(name,rows):
 with (root/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write('candidate_hourly_weather_2022_JulAug.csv',out)
week=[r for r in out if '2022-08-12'<=r['beijing_time'][:10]<='2022-08-18']
write('candidate_heatwave_2022_Aug12_18.csv',week)
qa={'hours':len(out),'observed_temperature_hours':sum(r['city_temperature_method']=='observed' for r in out),
    'interpolated_temperature_hours':sum(r['city_temperature_method'].startswith('linear') for r in out),
    'missing_temperature_hours':sum(r['city_temperature_C'] is None for r in out),
    'missing_radiation_hours':sum(r['grid_GHI_W_m2'] is None for r in out),
    'heatwave_week_hours':len(week),'heatwave_week_missing_temperature_hours':sum(r['city_temperature_C'] is None for r in week),
    'heatwave_week_observed_temperature_hours':sum(r['city_temperature_method']=='observed' for r in week),
    'heatwave_week_interpolated_temperature_hours':sum(r['city_temperature_method'].startswith('linear') for r in week),
    'heatwave_week_missing_radiation_hours':sum(r['grid_GHI_W_m2'] is None for r in week),
    'heatwave_week_missing_derived_hour_mean_temperature_hours':sum(r['city_hour_mean_temperature_C_derived'] is None for r in week),
    'notes':['Interpolation is processing, not a new observation.',
             'POWER official FAQ: timestamps identify the START of the hour; radiation values are hourly means.',
             'city_temperature_C is the value at the hour start; the separate hour-mean field is derived from linear interpolation, not an observed mean.',
             'No airport observations, long-gap interpolation, radiation bias adjustment, or façade transposition.',
             'The full July-August series has missing leading temperature/radiation and must not be treated as simulation-ready.',
             'The selected week is a candidate boundary condition, not the original 2017 calibration weather.']}
assert len(out)==1488 and len(week)==168
for r in out:
 if r['city_temperature_method']=='observed':assert times[bisect.bisect_left(times,datetime.strptime(r['beijing_time'],'%Y-%m-%d %H:%M'))]==datetime.strptime(r['beijing_time'],'%Y-%m-%d %H:%M')
 if r['city_temperature_method'].startswith('linear'):assert r['bracketing_gap_hours']==3
 if r['RH_percent_derived'] is not None:assert 0<=r['RH_percent_derived']<=101
(root/'candidate_weather_QA.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))
